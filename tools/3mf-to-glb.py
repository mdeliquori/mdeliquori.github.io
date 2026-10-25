"""Convert a single-mesh 3MF to a binary glTF (.glb) with crease-angle smoothed normals.

Usage: python tools/3mf-to-glb.py in.3mf out.glb [poster.png]
Stdlib only. Units mm -> m, mesh centred on its bounding box, Z-up -> Y-up.
"""
import json
import math
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"


def read_mesh(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("3D/3dmodel.model"))
        thumb = z.read("Metadata/thumbnail.png") if "Metadata/thumbnail.png" in z.namelist() else None
    unit = {"millimeter": 0.001, "centimeter": 0.01, "meter": 1.0, "inch": 0.0254}.get(root.get("unit", "millimeter"), 0.001)
    verts, tris = [], []
    for obj in root.iter(NS + "object"):
        mesh = obj.find(NS + "mesh")
        if mesh is None:
            continue
        base = len(verts)
        for v in mesh.iter(NS + "vertex"):
            x, y, z = (float(v.get(k)) * unit for k in ("x", "y", "z"))
            verts.append((x, z, -y))  # Z-up -> Y-up
        for t in mesh.iter(NS + "triangle"):
            tris.append(tuple(base + int(t.get(k)) for k in ("v1", "v2", "v3")))
    return verts, tris, thumb


def build_glb(verts, tris):
    mins = [min(v[i] for v in verts) for i in range(3)]
    maxs = [max(v[i] for v in verts) for i in range(3)]
    centre = [(a + b) / 2 for a, b in zip(mins, maxs)]
    verts = [tuple(v[i] - centre[i] for i in range(3)) for v in verts]

    # Face normals (area-weighted), then per-corner normals smoothed across edges
    # sharper than CREASE stay hard, so teeth flanks are smooth but faces stay crisp.
    crease = math.cos(math.radians(35))
    face_n, face_w = [], []
    for a, b, c in tris:
        pa, pb, pc = verts[a], verts[b], verts[c]
        u = [pb[i] - pa[i] for i in range(3)]
        w = [pc[i] - pa[i] for i in range(3)]
        n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        length = math.sqrt(sum(x * x for x in n)) or 1e-12
        face_n.append(tuple(x / length for x in n))
        face_w.append(length)
    vert_faces = [[] for _ in verts]
    for f, tri in enumerate(tris):
        for v in tri:
            vert_faces[v].append(f)

    pos, nrm = bytearray(), bytearray()
    for f, tri in enumerate(tris):
        nf = face_n[f]
        for v in tri:
            acc = [0.0, 0.0, 0.0]
            for g in vert_faces[v]:
                ng = face_n[g]
                if ng[0] * nf[0] + ng[1] * nf[1] + ng[2] * nf[2] >= crease:
                    for i in range(3):
                        acc[i] += ng[i] * face_w[g]
            length = math.sqrt(sum(x * x for x in acc)) or 1.0
            pos += struct.pack("<3f", *verts[v])
            nrm += struct.pack("<3f", *(x / length for x in acc))

    count = len(tris) * 3
    half = [(b - a) / 2 for a, b in zip(mins, maxs)]
    binary = bytes(pos + nrm)
    gltf = {
        "asset": {"version": "2.0", "generator": "3mf-to-glb.py"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0, "NORMAL": 1}, "material": 0}]}],
        "materials": [{
            "name": "Machined aluminium",
            "pbrMetallicRoughness": {"baseColorFactor": [0.78, 0.78, 0.8, 1.0], "metallicFactor": 0.85, "roughnessFactor": 0.38},
        }],
        "buffers": [{"byteLength": len(binary)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos), "target": 34962},
            {"buffer": 0, "byteOffset": len(pos), "byteLength": len(nrm), "target": 34962},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": count, "type": "VEC3",
             "min": [-h for h in half], "max": half},
            {"bufferView": 1, "componentType": 5126, "count": count, "type": "VEC3"},
        ],
    }
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    binary += b"\0" * (-len(binary) % 4)
    total = 12 + 8 + len(js) + 8 + len(binary)
    return (struct.pack("<4sII", b"glTF", 2, total)
            + struct.pack("<I4s", len(js), b"JSON") + js
            + struct.pack("<I4s", len(binary), b"BIN\0") + binary), [2 * h for h in half]


def main():
    src, out = sys.argv[1], sys.argv[2]
    verts, tris, thumb = read_mesh(src)
    glb, size = build_glb(verts, tris)
    with open(out, "wb") as f:
        f.write(glb)
    print(f"{len(verts)} verts, {len(tris)} tris -> {out} ({len(glb) / 1024:.0f} KB), size m: {size}")
    if len(sys.argv) > 3 and thumb:
        with open(sys.argv[3], "wb") as f:
            f.write(thumb)
        print("poster ->", sys.argv[3])


if __name__ == "__main__":
    main()
