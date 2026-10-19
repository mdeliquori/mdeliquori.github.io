# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Personal portfolio for a mechanical engineering student, aimed at recruiters. Served by GitHub Pages from `main` at https://mdeliquori.github.io.

## Stack: build-free, keep it that way

- Plain HTML/CSS/vanilla JS. No frameworks, bundlers, npm dependencies or Jekyll (`.nojekyll` disables it — don't remove it).
- Preview: `python -m http.server` from the repo root, then http://localhost:8000.
- Third-party scripts only via CDN `<script>` tags with an exact pinned version.
- Lint after changes (via npx, no package.json — don't add one):
  - HTML: `npx html-validate@8.18.2 index.html projects/*.html`
  - CSS: `npx stylelint@16.10.0 "assets/css/*.css"` (core rules only, see `.stylelintrc.json`)

## Conventions

- 2-space indent everywhere; JS uses double quotes and semicolons.
- Plain hyphenated class names (`.project-card`, `.btn-outline`), not BEM. Reuse existing classes before adding new ones.
- Colors, radius, max-width and font live as variables in `:root` in `assets/css/style.css` — use them, don't hardcode values.
- One breakpoint: `@media (max-width: 720px)`. Check layouts at phone width.
- Section banners: `<!-- ===== Name ===== -->` in HTML, `/* ===== Name ===== */` in CSS.

## Shared header/footer are duplicated

There's no templating: the nav and footer are copied into every page. Any change must be applied to `index.html` and every file in `projects/`. Root links use `#about`; project pages use `../index.html#about` and `../assets/...`.

## Paths are case-sensitive

GitHub Pages is case-sensitive; Windows is not. A link that works locally can 404 live. Match filenames' case exactly, and prefer lowercase-hyphenated asset names.

## Projects

- New project page = copy `projects/project-template.html` + add a `project-card` in `index.html`. Use `/new-project`.
- Images go in `assets/images/projects/`, renders in `assets/renders/`, PDFs in `assets/docs/`. Always write meaningful `alt` text.
- 3D models: `.glb` only (convert STL/STEP first) in `assets/models/`, keep each under ~10 MB. Embed with Google's `<model-viewer>`:
  `<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>`
  Always set a `poster` render and keep a static image as the primary visual — the 3D view is an extra.

## Placeholder content

Email, LinkedIn URL, About text, profile photo, project images, and `assets/docs/CV.pdf` are still placeholders. Never invent real-looking personal details or project results — leave a clear placeholder and tell the user.

## Git

Commit locally with clear messages, but **never push** — pushing to `main` deploys the live site. The user reviews and pushes.

## Current status & next steps (as of 2026-10-19)

Site is still the unstyled skeleton with placeholder content. Agreed plan:

- **Waiting on the user:** content for one flagship project (write-up, photos/renders, results, optional `.glb`). Design around that real content rather than placeholders; other projects get filled in later.
- **Design workflow:** first explore 2–3 visual directions for the homepage and project page as a Design artifact (Claude Design canvas) using the flagship content. The user picks one. Then record the tokens in `:root` of `style.css` (or a Design System artifact). Then implement with the `frontend-design` plugin installed (the user runs `/plugin install frontend-design@claude-plugins-official`).
- **Branching:** do the redesign on a local `dev` branch so the live site (`main`) is untouched until the user merges and pushes.
- **Order:**
  1. Get the content inventory and flagship material from the user.
  2. `git checkout -b dev`.
  3. Make the Design canvas and iterate on it with the user.
  4. Record the design tokens.
  5. Implement in `index.html`, `projects/project-template.html` and `style.css`.
  6. Build the flagship page with `/new-project`.
  7. Add the remaining projects as their content arrives.
- **Before merging to `main`:** lint passes, link check is clean, layout is checked at phone width, and the result matches the approved design.
- **Known lint issue:** the nav `<button>` lacks `type="button"` in `index.html` and the project template; fix it during implementation.

Update or remove this section as steps complete.
