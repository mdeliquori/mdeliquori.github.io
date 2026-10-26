# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Personal portfolio for a mechanical engineering student, aimed at recruiters. Served by GitHub Pages from `main` at https://mdeliquori.github.io.

## Stack: build-free, keep it that way

- Plain HTML/CSS/vanilla JS. No frameworks, bundlers, npm dependencies or Jekyll (`.nojekyll` disables it — don't remove it).
- Preview: `python -m http.server` from the repo root, then http://localhost:8000.
- Third-party scripts only via CDN `<script>` tags with an exact pinned version. Current pins:
  - GSAP 3.13.0 from `https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/` (`gsap`, `ScrollTrigger`, `SplitText`, and `Flip` on the homepage).
  - model-viewer 4.0.0 (see Projects).
- Fonts come from one Google Fonts `<link>`, the same on every page: JetBrains Mono (default) and Source Serif 4 (long text).
- Lint after changes (via npx, no package.json — don't add one):
  - HTML: `npx html-validate@8.18.2 index.html projects/*.html`
  - CSS: `npx stylelint@16.10.0 "assets/css/*.css"` (core rules only, see `.stylelintrc.json`)

## Conventions

- 2-space indent everywhere; JS uses double quotes and semicolons.
- Plain hyphenated class names (`.project-card`, `.btn-outline`), not BEM. Reuse existing classes before adding new ones.
- Colors, radius, max-width, fonts, type scale and grid live as variables in `:root` in `assets/css/style.css`. Use them and don't hardcode values.
- **Design: read `DESIGN.md` before any visual or motion change.** It is the single source of truth for tokens, components, layouts and every GSAP animation. Keep it in sync when the design changes.
  - It consolidates the references in `assets/design guide/` (Hyperstudio, AuthKit, ORYZO) and neal.fun. Only open those for background.
- Text is JetBrains Mono except long-form copy, which uses `.serif` (Source Serif 4).
- All animation uses GSAP, wrapped in `gsap.matchMedia()` with `prefers-reduced-motion: no-preference`. Pages must stay fully readable with no JS and with reduced motion, so set hidden initial states from JS only.
- One breakpoint: `@media (max-width: 720px)`. Check layouts at phone width.
- Section banners: `<!-- ===== Name ===== -->` in HTML, `/* ===== Name ===== */` in CSS.

## Shared header/footer are duplicated

There's no templating: the nav and footer are copied into every page. Any change must be applied to `index.html` and every file in `projects/`. Root links use `#about`; project pages use `../index.html#about` and `../assets/...`.

## Paths are case-sensitive

GitHub Pages is case-sensitive; Windows is not. A link that works locally can 404 live. Match filenames' case exactly, and prefer lowercase-hyphenated asset names.

## Projects

- Two project types:
  - **Hardware**: real parts. Template: `projects/project-template.html`. Worked example: `projects/ip-2025-servo-mount.html`.
  - **Software**: ML, hackathons and similar. These show code and link to the GitHub repo, with no 3D. There's no template yet.
- New project page = copy the template + add a `project-card` (with `data-type="hardware|software"`) in `index.html`. Use `/new-project`.
- Hardware page model stage (`assets/js/model-scroll.js`): the stage pins, the model turns 360° over the scroll, and each `.model-step` (heading left, serif body right) swaps in turn. The scroll length follows the number of steps.
- `CONTENT.md` is the user-facing guide to filling in content and linking images/models. Update it whenever page structure, file locations or the project workflow change.
- Images go in `assets/images/projects/<slug>/`, renders in `assets/renders/`, PDFs in `assets/docs/`. Always write meaningful `alt` text.
- 3D models: `.glb` only (convert STL/STEP first) in `assets/models/`, keep each under ~10 MB. Embed with Google's `<model-viewer>`:
  `<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>`
  Always set a `poster` render (transparent PNG) and keep static images on the page as the primary visual; the 3D view is an extra.
  Convert a single-body `.3mf` with `python tools/3mf-to-glb.py in.3mf assets/models/<slug>.glb assets/renders/<slug>-poster.png`. It is stdlib only. It centres the mesh, scales mm → m, goes Z-up → Y-up and smooths normals. The extracted poster has a white background, so make it transparent (e.g. a Pillow flood fill from the corners). Don't commit source CAD files (`.3mf`, `.stl`, `.step`).
- Homepage drawing views: `python tools/mesh-to-svg.py in.3mf top|front|right|iso` prints visible-edge SVG path data (hidden lines removed). It is stdlib only. The section and dimensions around it are hand-drawn in mm; see `DESIGN.md`.

## Placeholder content

The name, email, LinkedIn and `assets/docs/CV.pdf` are real. The About text, profile photo and project images are still placeholders. Unfilled text is in `[square brackets]`, and `CONTENT.md` lists where everything goes. Never invent real-looking personal details or project results. Leave a clear placeholder and tell the user.

## Git

Commit locally with clear messages, but **never push** — pushing to `main` deploys the live site. The user reviews and pushes.

## Current status & next steps (as of 2026-10-25)

The redesign is complete and merged into `main` locally. It needs the user to push before it goes live. It contains:
- the dark blueprint homepage,
- the neal.fun-style project grid with an HW/SW filter,
- the hardware template plus the servo mount page,
- `DESIGN.md`, `CONTENT.md` and `tools/3mf-to-glb.py`.

- **Placeholders the user fills in (see `CONTENT.md`):**
  - About text, profile photo,
  - all project copy and key figures,
  - a `.glb` of the servo mount. `assets/models/zahnrad-14.glb` is a stand-in gear.
- **Next:**
  1. Build the software project template. `DESIGN.md` has the brief: a code-focused opener with no 3D.
  2. Write the AMZ, SML and Hackathon pages. Their tiles are in a "soon" state.
- **Before each merge to `main`:**
  - Lint passes.
  - The link check is clean.
  - The layout is checked at phone width and with reduced motion.
  - The result matches `DESIGN.md`.
  - Do new work on a `dev` branch.
