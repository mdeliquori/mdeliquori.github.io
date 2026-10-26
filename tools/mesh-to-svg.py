"""Draw a 3MF mesh as visible-edge linework for an SVG drawing view.

Usage: python tools/mesh-to-svg.py in.3mf [top|front|right|iso]
Stdlib only. Units stay in mm, Z-up as in the CAD file. Prints the view's
viewBox and one SVG path `d` string with hidden lines removed: feature edges
(sharp creases) plus silhouette edges, depth-tested against the mesh.
"""
import math
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"
CREASE_DEG = 30   # edges sharper than this are drawn
STEP = 0.1        # mm between visibility samples along an edge
DEPTH_EPS = 0.01  # mm; keeps an edge from hiding behind its own faces
SIMPLIFY = 0.03   # mm; Douglas-Peucker tolerance for the output polylines

# Camera direction (object -> eye) and up hint for each view
VIEWS = {
    "top": ((0, 0, 1), (0, 1, 0)),
    "front": ((0, -1, 0), (0, 0, 1)),
    "right": ((1, 0, 0), (0, 0, 1)),
    "iso": ((1, -1, 1), (0, 0, 1)),
}


def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    length = math.sqrt(dot(a, a)) or 1.0
    return (a[0] / length, a[1] / length, a[2] / length)


def read_mesh(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("3D/3dmodel.model"))
    scale = {"millimeter": 1.0, "centimeter": 10.0, "meter": 1000.0, "inch": 25.4}.get(root.get("unit", "millimeter"), 1.0)
    verts, tris, weld = [], [], {}
    for obj in root.iter(NS + "object"):
        mesh = obj.find(NS + "mesh")
        if mesh is None:
            continue
        remap = []
        for v in mesh.iter(NS + "vertex"):
            p = tuple(float(v.get(k)) * scale for k in ("x", "y", "z"))
            key = tuple(round(c, 4) for c in p)
            if key not in weld:
                weld[key] = len(verts)
                verts.append(p)
            remap.append(weld[key])
        for t in mesh.iter(NS + "triangle"):
            tri = tuple(remap[int(t.get(k))] for k in ("v1", "v2", "v3"))
            if len(set(tri)) == 3:
                tris.append(tri)
    centre = [(min(v[i] for v in verts) + max(v[i] for v in verts)) / 2 for i in range(3)]
    return [sub(v, centre) for v in verts], tris


def project(verts, view):
    eye, hint = (norm(v) for v in VIEWS[view])
    right = norm(cross(hint, eye))
    up = cross(eye, right)
    # Screen x right, y down (SVG), depth grows toward the eye
    return [(dot(p, right), -dot(p, up), dot(p, eye)) for p in verts], eye


def candidate_edges(verts, tris, eye):
    normals = [norm(cross(sub(verts[b], verts[a]), sub(verts[c], verts[a]))) for a, b, c in tris]
    faces = {}
    for i, (a, b, c) in enumerate(tris):
        for e in ((a, b), (b, c), (c, a)):
            faces.setdefault(tuple(sorted(e)), []).append(i)
    crease = math.cos(math.radians(CREASE_DEG))
    edges = []
    for e, fs in faces.items():
        if len(fs) != 2:
            edges.append(e)  # open boundary
            continue
        n1, n2 = normals[fs[0]], normals[fs[1]]
        facing = (dot(n1, eye) > 1e-6) != (dot(n2, eye) > 1e-6)
        if dot(n1, n2) < crease or facing:
            edges.append(e)
    return edges, normals


def build_occluders(screen, tris, normals, eye, cell):
    occ, grid = [], {}
    for i, (a, b, c) in enumerate(tris):
        if dot(normals[i], eye) <= 1e-6:
            continue  # closed mesh: back faces never show in front of front faces
        pa, pb, pc = screen[a], screen[b], screen[c]
        den = (pb[1] - pc[1]) * (pa[0] - pc[0]) + (pc[0] - pb[0]) * (pa[1] - pc[1])
        if abs(den) < 1e-12:
            continue
        k = len(occ)
        occ.append((pa, pb, pc, den))
        xs, ys = (pa[0], pb[0], pc[0]), (pa[1], pb[1], pc[1])
        for gx in range(math.floor(min(xs) / cell), math.floor(max(xs) / cell) + 1):
            for gy in range(math.floor(min(ys) / cell), math.floor(max(ys) / cell) + 1):
                grid.setdefault((gx, gy), []).append(k)
    return occ, grid


def hidden(x, y, z, occ, grid, cell):
    for k in grid.get((math.floor(x / cell), math.floor(y / cell)), ()):
        pa, pb, pc, den = occ[k]
        l1 = ((pb[1] - pc[1]) * (x - pc[0]) + (pc[0] - pb[0]) * (y - pc[1])) / den
        l2 = ((pc[1] - pa[1]) * (x - pc[0]) + (pa[0] - pc[0]) * (y - pc[1])) / den
        l3 = 1 - l1 - l2
        if min(l1, l2, l3) < -1e-9:
            continue
        if l1 * pa[2] + l2 * pb[2] + l3 * pc[2] > z + DEPTH_EPS:
            return True
    return False


def visible_runs(screen, edges, occ, grid, cell):
    runs = []
    for a, b in edges:
        pa, pb = screen[a], screen[b]
        length = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
        if length < 1e-4:
            continue  # edge seen end-on
        n = max(2, math.ceil(length / STEP) + 1)
        start = None
        for i in range(n):
            t = i / (n - 1)
            p = tuple(pa[j] + (pb[j] - pa[j]) * t for j in range(3))
            if not hidden(*p, occ, grid, cell):
                if start is None:
                    start = p
                last = p
            elif start is not None:
                runs.append((start[:2], last[:2]))
                start = None
        if start is not None:
            runs.append((start[:2], last[:2]))
    return [r for r in runs if math.dist(*r) > 1e-3]


def chain(runs):
    """Join segments that share endpoints into polylines."""
    key = lambda p: (round(p[0], 3), round(p[1], 3))
    ends = {}
    for i, (p, q) in enumerate(runs):
        ends.setdefault(key(p), []).append(i)
        ends.setdefault(key(q), []).append(i)
    used, lines = set(), []
    for i in range(len(runs)):
        if i in used:
            continue
        used.add(i)
        line = list(runs[i])
        for forward in (True, False):
            while True:
                tip = line[-1] if forward else line[0]
                nxt = next((j for j in ends[key(tip)] if j not in used), None)
                if nxt is None:
                    break
                used.add(nxt)
                p, q = runs[nxt]
                other = q if key(p) == key(tip) else p
                line.append(other) if forward else line.insert(0, other)
        lines.append(line)
    return lines


def simplify(points, tol):
    if len(points) < 3:
        return points
    (x1, y1), (x2, y2) = points[0], points[-1]
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    worst, idx = 0.0, 0
    for i in range(1, len(points) - 1):
        px, py = points[i]
        d = abs(dy * (px - x1) - dx * (py - y1)) / length if length else math.hypot(px - x1, py - y1)
        if d > worst:
            worst, idx = d, i
    if worst <= tol:
        return [points[0], points[-1]]
    return simplify(points[:idx + 1], tol)[:-1] + simplify(points[idx:], tol)


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    view = sys.argv[2] if len(sys.argv) > 2 else "iso"
    verts, tris = read_mesh(sys.argv[1])
    screen, eye = project(verts, view)
    edges, normals = candidate_edges(verts, tris, eye)
    cell = 1.0
    occ, grid = build_occluders(screen, tris, normals, eye, cell)
    lines = [simplify(l, SIMPLIFY) for l in chain(visible_runs(screen, edges, occ, grid, cell))]

    xs = [p[0] for l in lines for p in l]
    ys = [p[1] for l in lines for p in l]
    print(f'viewBox="{fmt(min(xs))} {fmt(min(ys))} {fmt(max(xs) - min(xs))} {fmt(max(ys) - min(ys))}"')
    d = []
    for l in lines:
        closed = len(l) > 2 and math.dist(l[0], l[-1]) < 1e-3
        pts = l[:-1] if closed else l
        d.append("M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts) + ("Z" if closed else ""))
    print(f'd="{"".join(d)}"')


if __name__ == "__main__":
    main()
