---
name: new-project
description: Scaffold a new portfolio project page from projects/project-template.html and add its card to the homepage. Use when the user wants to add a project to the site.
disable-model-invocation: true
argument-hint: "<project name or short description>"
---

Add a new project to the portfolio: $ARGUMENTS

1. **Gather details.** If not given, ask for:
   - whether it is a **hardware** or **software** project (only hardware has a template so far),
   - the project title,
   - a one-to-two sentence summary,
   - tool/skill tags (e.g. SolidWorks, FEA, MATLAB),
   - whether there are images, renders or a 3D model. Don't invent results, numbers or claims — use the template's placeholder prompts where content is missing.

   Read `DESIGN.md` for layout and motion rules and `CONTENT.md` for where content goes.

2. **Pick a slug**: lowercase-hyphenated, e.g. `fs-suspension`. Page goes at `projects/<slug>.html`.

3. **Create the page** by copying `projects/project-template.html`:
   - Set `<title>` to `<Project Title> | Matteo Deliquori` and the `<h1>`.
   - Add a `<meta name="description">` (the template lacks one).
   - Fill the kicker, `.model-step` items, side label, meta strip, write-up and key figures. Remove the "Copy this file…" comment.
   - Keep the shared header/footer identical to the other project pages and keep `../` relative paths.

4. **Media**:
   - Reference images as `../assets/images/projects/<slug>/<slug>-*.png` or `../assets/renders/<slug>-*.png`, with real `alt` text. If files don't exist yet, keep a `<div class="placeholder">` naming the expected path.
   - Convert a `.3mf` with `python tools/3mf-to-glb.py <in>.3mf assets/models/<slug>.glb assets/renders/<slug>-poster.png`, then make the poster background transparent.
   - For a 3D model, point the template's existing `<model-viewer>` at `../assets/models/<slug>.glb` and give it a transparent `poster`. Don't add `camera-controls`: `model-scroll.js` turns them on only in the reduced-motion fallback. Keep the static renders in the gallery.

5. **Add the card** to `index.html` inside `.project-grid`: copy an existing `<article class="project-card">` block. Set `data-type`, the title (wrapped in `<a class="card-link">` to `projects/<slug>.html`), the summary and tags, and the image path without `../`. Remove `is-soon` and the "soon" tag. If replacing a placeholder card that still links to `project-template.html`, replace that one instead of adding.

6. **Verify**: every new `href`/`src` matches a real file with exact case (or is an intentional placeholder), `npx html-validate@8.18.2 index.html projects/*.html` passes, and both pages look right at phone width and with reduced motion.

7. **Report** what was created and list the content/assets the user still needs to provide. Commit locally if asked; never push.
