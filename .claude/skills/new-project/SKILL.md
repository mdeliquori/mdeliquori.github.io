---
name: new-project
description: Scaffold a new portfolio project page from projects/project-template.html and add its card to the homepage. Use when the user wants to add a project to the site.
disable-model-invocation: true
argument-hint: "<project name or short description>"
---

Add a new project to the portfolio: $ARGUMENTS

1. **Gather details.** If not given, ask for: project title, one-to-two sentence summary, tool/skill tags (e.g. SolidWorks, FEA, MATLAB), and whether there are images, renders or a 3D model. Don't invent results, numbers or claims — use the template's placeholder prompts where content is missing.

2. **Pick a slug**: lowercase-hyphenated, e.g. `fs-suspension`. Page goes at `projects/<slug>.html`.

3. **Create the page** by copying `projects/project-template.html`:
   - Set `<title>` to `<Project Title> | Matteo Deliquori` and the `<h1>`.
   - Add a `<meta name="description">` (the template lacks one).
   - Replace the tags and remove the "Copy this file…" comment.
   - Keep the shared header/footer identical to the other project pages and keep `../` relative paths.

4. **Media**:
   - Reference images as `../assets/images/projects/<slug>-*.jpg` or `../assets/renders/<slug>-*.png`, with real `alt` text. If files don't exist yet, keep a `<div class="placeholder">` naming the expected path.
   - For a 3D model: `../assets/models/<slug>.glb`, embedded with `<model-viewer src="..." poster="..." alt="..." camera-controls>` and the pinned script tag from CLAUDE.md (add it once in `<head>` of that page only). Keep the static render as the hero.

5. **Add the card** to `index.html` inside `.project-grid`: copy an existing `<article class="project-card">` block, fill title/summary/tags, link to `projects/<slug>.html`, and image path without `../`. If replacing a placeholder card that still links to `project-template.html`, replace that one instead of adding.

6. **Verify**: every new `href`/`src` matches a real file with exact case (or is an intentional placeholder), `npx html-validate@8.18.2 index.html projects/*.html` passes, and both pages look right at phone width.

7. **Report** what was created and list the content/assets the user still needs to provide. Commit locally if asked; never push.
