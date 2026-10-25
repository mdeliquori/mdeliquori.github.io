# mdeliquori.github.io

Personal portfolio site, hosted on GitHub Pages at https://mdeliquori.github.io

- **[CONTENT.md](CONTENT.md)**: how to fill in your text, contact details, images and 3D models.
- **[DESIGN.md](DESIGN.md)**: the design system: colours, type, layouts, components and animations.

## Structure

```
index.html                    Homepage
projects/
  project-template.html       Hardware project template (copy for each new hardware project)
  ip-2025-servo-mount.html    Servo mount project page
assets/
  css/style.css               All styles; design tokens in :root
  js/main.js                  Nav, footer year, filter, shared GSAP animations
  js/model-scroll.js          Hardware page: scroll-driven 3D model stage
  images/profile/             Profile photo
  images/projects/<project>/  Project renders and photos, one folder per project
  renders/                    3D model posters (transparent PNG)
  models/                     3D models (.glb only)
  docs/                       CV and other PDFs
  design guide/               Original design references (consolidated in DESIGN.md)
tools/3mf-to-glb.py           Converts a .3mf export to .glb
.nojekyll                     Serves files as-is (skips Jekyll processing)
```

Built with plain HTML/CSS/JS. No build step. Animations use GSAP and the 3D viewer uses `<model-viewer>`, both from pinned CDN versions.

## Local preview

Run `python -m http.server` in this folder and visit http://localhost:8000. Opening `index.html` directly also works, but the 3D model needs the server.
