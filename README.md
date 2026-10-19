# mdeliquori.github.io

Personal portfolio site, hosted on GitHub Pages at https://mdeliquori.github.io

## Structure

```
index.html                  Homepage
projects/                   One HTML page per project (copy project-template.html)
assets/
  css/style.css             Site-wide styles
  js/main.js                Mobile nav and footer year
  images/profile/           Profile photo
  images/projects/          Project photos, drawings, plots
  renders/                  CAD renders
  models/                   3D model files (.glb/.gltf for web viewing, .stl)
  docs/                     CV and other PDFs
.nojekyll                   Serves files as-is (skips Jekyll processing)
```

## Local preview

Open `index.html` in a browser, or run `python -m http.server` in this folder and visit http://localhost:8000.
