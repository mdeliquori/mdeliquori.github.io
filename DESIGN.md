# Design system

This is the single source of truth for how the portfolio looks and moves. It combines the three references in `assets/design guide/` into what the site actually uses. Read this file, not the references, unless you need the reasoning behind a choice.

| Source | What we took from it |
|---|---|
| `Hyperstudio.md` | Palette, hairline structure, weight-400 type, pill/ghost buttons, no shadows |
| `AuthKit.md` | The blueprint grid layer: 80px cells, radial fade mask, conic spotlight |
| `ORYZO.md` | Motion, and the hardware model stage: a centred object that turns while text swaps on both sides |
| [neal.fun](https://neal.fun) | The homepage project grid: image-led square tiles with the title underneath |

## Concept

**A technical drawing in light on black.** In light mode, the same drawing printed on paper: near-neutral white with black ink, never cream.
- The site reads like a mechanical drawing sheet: thin lines, a grid, zone markers, a title block.
- The parts are the only solid objects.
- Type is mono and calm, and gets its hierarchy from size, not weight.
- Each page spends its boldness in **one place**:
  - **Homepage:** the drawing-sheet hero with the name lettered in.
  - **Hardware page:** the pinned model stage.
- Everything else stays quiet.

## Tokens

All tokens are CSS variables in `:root` of `assets/css/style.css`. Never hardcode values.

### Colour
Every colour token is `light-dark(<light>, <dark>)`. Themes swap only these tokens; layout, type and motion are identical. A new colour needs both values. The light values were checked at ≥ 4.5:1 for text and ≥ 3:1 for strokes.

| Variable | Dark | Light | Use |
|---|---|---|---|
| `--color-bg` | `#101010` | `#f5f5f4` | Page canvas |
| `--color-bg-deep` | `#080808` | `#ebebe9` | Tile plates, placeholder boxes |
| `--color-text` | `#f3f3f3` | `#141414` | Headings, primary text |
| `--color-muted` | `#9c9c9c` | `#63635f` | Secondary text, captions, labels, nav |
| `--color-ash` | `#c1c1c1` | `#34342f` | Serif body text |
| `--color-border` | `#212121` | `#dcdcd8` | Default 1px hairline: sections, cards, tables |
| `--color-border-strong` | `#474747` | `#a9a9a4` | Sheet border, dashed "soon" borders, link underlines |
| `--color-contrast` | `#ffffff` | `#101010` | Maximum contrast: primary pill fill, focus ring, hovers |
| `--color-gold` | `#6f6759` | `#8a7e69` | Icon strokes, drawing zone markers and thin drawing lines only, never text |
| `--color-live` | `#98ff38` | `#2e9e1c` | The status dot only |
| `--grid-line` | `rgba(243,243,243,.05)` | `rgba(20,20,20,.06)` | Blueprint grid lines |
| `--grid-line-strong` | `rgba(243,243,243,.09)` | `rgba(20,20,20,.09)` | Small grid inside tile plates |
| `--spotlight` | `rgba(243,243,243,.07)` | `rgba(20,20,20,.04)` | Conic spotlight beam |
| `--header-bg` | `rgba(16,16,16,.82)` | `rgba(245,245,244,.85)` | Translucent sticky header (with blur) |

There's no accent colour. Hierarchy comes from contrast between text, muted and ash.

**Theme selection:**
- `:root { color-scheme: light dark }` follows the system, even without JS.
- `assets/js/theme.js`, loaded in `<head>`, sets `<html data-theme="light|dark">` from the saved toggle choice (`localStorage` key `theme`) or the system. `data-theme` pins `color-scheme`.
- With nothing saved, the page keeps following system changes.

### Type
| Variable | Family | Use |
|---|---|---|
| `--font-mono` | JetBrains Mono 400/500 | **Default for everything**: UI, headings, labels, buttons |
| `--font-serif` | Source Serif 4 400 | Long-form text only (`.serif`, step bodies) |

| Variable | Size | Use |
|---|---|---|
| `--text-display` | `clamp(48px, 10vw, 128px)` | Hero name. Line-height 0.92, tracking -0.055em |
| — | `clamp(40px, 6vw, 80px)` | Project title. Line-height 0.92, tracking -0.05em |
| `--text-heading` | 34px | Section headings, step headings, key-figure values |
| `--text-heading-sm` | 23px | Write-up headings |
| `--text-serif` | 20px | Serif body. Line-height 1.65, max 64ch |
| `--text-lead` | 18px | Hero lead |
| `--text-body` | 16px | Base, tile titles |
| `--text-small` | 14px | Nav, buttons, summaries, lists |
| `--text-caption` | 13px | Captions, tags, meta labels |

**Rules:**
- Weight is **400** for headings. 500 is used only for the `MD` wordmark.
- Large type gets negative tracking: -0.02em by default, tighter at display sizes.
- Write in **sentence case** everywhere. No all-caps labels.
- Long text stays under ~70 characters per line.

### Shape and space
| Variable | Value | Use |
|---|---|---|
| `--radius-tag` | 4px | Tags, status pill, nav toggle |
| `--radius` | 8px | Cards, plates, images, ghost button |
| `--radius-pill` | 9999px | Primary button, filter pills |
| `--max-width` | 1200px | Content column (`.container`) |
| `--gutter` | 24px (16px on phones) | Side padding |
| `--header-height` | 64px | Sticky header, used for stage heights and the pin offset |
| `--section-gap` | `clamp(96px, 12vw, 160px)` | Vertical padding of `.section` |
| `--grid-size` | 80px (48px on phones) | Blueprint cell size |

**Rules:**
- **No shadows.** Elevation comes only from 1px borders and contrast.
- **One breakpoint:** `@media (max-width: 720px)`.

## Structure and components

### Shared
- **Header (`.site-header`):** sticky and translucent, with a 1px bottom hairline. It holds:
  - the `MD` wordmark,
  - muted nav links on the right,
  - the `.status` pill with the green dot,
  - the `.theme-toggle` at the far right: a 32px square with the pill's border. It shows the mode you'd switch to, a sun in dark mode and a moon in light mode (16px, 1.5px `currentColor` strokes). The button is `hidden` until `theme.js` runs, so there's no dead button without JS. The switch is instant, with no transition.
  - On phones, the links collapse behind a "Menu" button and the pill hides; the toggle stays next to Menu.
- **Section (`.section`):** a 1px top hairline and generous vertical padding. Sections are separated by lines, never by background colour.
- **Section head (`.section-head`):** the heading on the left, with an optional muted line or controls on the right.
- **Buttons:**
  - `.btn-primary`: white pill with dark text, once per view.
  - `.btn-outline`: white 1px outline with an 8px radius.
  - `.text-link`: text with a hairline underline.
- **Blueprint layer (`.blueprint`):** add this class to any section to get the grid. `::before` draws the grid with a radial mask; `::after` draws the spotlight. GSAP can fade the grid with the `--grid-alpha` variable.
- **Placeholder (`.placeholder`):** a dashed box on `--color-bg-deep`. Remove it once real content exists.
- **Footer:** a hairline, the copyright, and "Back to top" (links to `#top`, which is the `<main>` id).

### Homepage (`index.html`)
```
[MD]                           Projects About Skills Contact  (● Open to internships)
┌─1──────2──────3──────4──────5──────6─┐   ← .sheet (zone markers .zones-x/.zones-y)
A ┌──────────────────────────────────┐ A
│ │ Mechanical engineering student   │ │   ← .hero-kicker
│ │ Matteo                           │ │   ← h1, one <span> per line
B │ De Liquori                       │ B
│ │ lead paragraph                   │ │
│ │ (View projects) [Download CV]    │ │   iso view top right: svg.drawing-iso
C │ front + A–A      ┌─────────────┐ │ C   ← svg.drawing-views (bottom left)
│ │ with dimensions  │ title block │ │ │   ← dl.title-block
│ └──────────────────┴─────────────┘ │
└─1──────2──────3──────4──────5──────6─┘
Projects                       (All)(Hardware)(Software)
[tile][tile][tile][tile]       ← 4 columns, 2 on phones
About    photo | serif text
Skills   3 bordered cells, gold icons
Contact  large email, links
```
- **Drawing views (`svg.sheet-drawing`):** real drawing views of the stand-in gear, inline SVG in mm, `aria-hidden`.
  - `.drawing-iso`: iso pictorial, top right of the frame, no dimensions. Outlines come from `tools/mesh-to-svg.py`, with hidden lines removed.
  - `.drawing-views`: front view plus section A–A, bottom left beside the title block, drawn at 3.5px per mm. It uses first-angle projection (the section sits to the right) and ISO 2203 gear conventions (teeth unhatched, pitch line dash-dot). Dimension arrows come from the `#dim-arrow` marker.
  - Line types (ISO 128):
    - `.edge`: visible outlines, `--color-muted`, wide.
    - `.thin`: centre, hatch, cut and dimension lines, `--color-gold`, narrow.
    - `.center`: dash-dot.
    - `.dim-text`: `--color-muted`.
  - Phones: the iso view sits small above the text and the dimensioned strip is hidden.
- **Tile (`.project-card`):**
  - a square `.card-plate` (8px radius, 1px border, a 20px grid on `--color-bg-deep`) with the image cropped to fill,
  - the title (16px) and a one-line muted summary (hidden on phones),
  - `.tag` labels.
  - `data-type="hardware|software"` drives the filter.
- **"Soon" state (`.is-soon`):**
  - the plate gets a dashed border, and the image is greyscale at 45% opacity,
  - there's no link,
  - a dashed `.tag-soon` label.
- **Software tile plate:** `pre.code-plate`, faint code text in place of an image.

### Hardware project page (`projects/project-template.html`)
```
[header]
┌──────────────────────────────────────────────────────┐
│ Back to projects                                     │
│ Hardware project, IP 2025                            │  ← .model-title
│ Servo mount                                          │
│                                                     I│
│ 01                ┌──────────┐    serif body text   P│  ← .model-step: h2 left, p right
│ The brief         │  model   │    (1–2 sentences)    │     model-viewer in the centre column
│                   └──────────┘                      2│  ← .model-side-label (vertical)
│ 01 / 04 ──────────progress──────── Scroll to turn    │  ← .model-hud
└──────────────────────────────────────────────────────┘
Gallery      2-up figures, 4:3, captions
Meta strip   Role | Team | Year | Tools (hairline table)
Write-up     heading column | serif text column (×3)
Key figures  3 bordered cells
All projects / Get in touch
```
- **Stage (`.model-stage.blueprint`):** viewport height minus the header. `.model-inner` is a 3-column grid (1fr / 1.3fr / 1fr): steps on the outer columns, the model in the middle.
- **Phones:** one column. The model takes ~46svh, with the step text underneath.
- **Static mode (default, no JS or reduced motion):**
  - `.model-steps` is a normal list under the model, with dashed dividers between steps,
  - `model-viewer` gets `camera-controls`, so the user can drag to rotate.
- **Motion mode:**
  - `model-scroll.js` adds `html.has-model-motion`,
  - the steps then stack in the same grid cell over the model row,
  - the HUD and side label appear.
- **`model-viewer` attributes:**
  - `environment-image="neutral"`, `tone-mapping="neutral"`, `exposure="0.95"`,
  - `shadow-intensity="0.6"`, `shadow-softness="1"`,
  - `interpolation-decay="30"`, `interaction-prompt="none"`,
  - `disable-zoom`, `disable-pan`, `loading="eager"`.
  - The poster is a transparent PNG.

### Software project page
Not built yet. Keep the same header, footer, write-up, meta strip and key figures. Replace the model stage with a code-focused opener: a repo link as the primary pill, then a code excerpt or screenshot in a `.card-plate`-style frame with no 3D. Use the same spend-boldness-once rule.

## Motion

- **Library:** all motion uses **GSAP 3.13.0** (jsDelivr, pinned): `gsap`, `ScrollTrigger`, `SplitText`, plus `Flip` on the homepage.
- **Where the code lives:**
  - `assets/js/main.js`: shared and homepage motion.
  - `assets/js/model-scroll.js`: the hardware stage only.

**Principles:**
- **Reduced motion:** every animation is registered inside `gsap.matchMedia()` under `(prefers-reduced-motion: no-preference)`. With reduced motion the page is static and complete.
- **No JS:** hidden starting states are set from JS only, so without JS everything is visible.
- **Restraint:**
  - one orchestrated page-load moment per page,
  - scroll reveals, once each, only for tiles, figures, About and Skills (each ≤ ~1.2s),
  - motion that answers the user (hover, filter) is fine.
  - No fade-up on every heading.
- **Easing:** `power3.out` for entrances, `power2.inOut` for transitions, `none` for scroll-scrubbed values.

| Where | What happens | Details |
|---|---|---|
| Homepage load | The header drops in, the grid fades in, the zone markers tick in, the title-block rows slide in, the name letters rise, then the kicker, lead and buttons | Timeline; header 0.6s. Letters use `SplitText` chars with `mask: "chars"`, `yPercent: 110`, stagger 0.035, after `document.fonts.ready` |
| Homepage drawing | The iso gear is drawn top to bottom, starting with the name letters. The strip is drafted in order: centre lines, outlines, hatching, then dimensions | Line art goes through `drawable()` in `main.js`, which splits multi-subpath paths (they would pop in), sets `pathLength="1"` and sorts top to bottom; `strokeDashoffset` 1 to 0, `power2.inOut`. Iso: 0.9s per piece, stagger amount 0.8, same delay as the letters. Strip: centre lines 0.9s, outlines 1.1s (1.2s each), hatching 1.9s, dimensions 2.1s |
| About | Once at `top 75%`: the photo zooms in while the text is written line by line | Photo scale 0.9 to 1 with fade, 0.8s `power3.out`. `SplitText` lines, `clipPath` inset 100% to 0 from the right edge, 0.35s each, stagger amount 0.5, then `revert()` |
| Skills | Once at `top 75%`, cell by cell (0.15s apart): the gold icon is drafted, then the heading and list items | Icons via `drawable()`, 0.6s. Text y 8 to 0 with fade, 0.4s, stagger 0.04, from 0.3s into each cell |
| Tiles | Stagger in once on scroll | `ScrollTrigger.batch`, start `top 88%`, y 32 to 0, stagger 0.1 |
| Tile hover | The image zooms to 1.06 and drifts up to ±6px toward the pointer | `gsap.quickTo` on x/y, 0.5s |
| Filter | Tiles reflow; leavers shrink and fade, enterers grow in | `Flip.from`, 0.6s, `absolute: true`. The filter still works without GSAP |
| Project page load | Title letters rise, then the back link and kicker | Same SplitText treatment |
| **Model stage** | Pins under the header for `steps × 100vh` (×0.75 on phones), `scrub: 1` | See below |
| Gallery and key figures | Reveal once on scroll | y 24 to 0, start `top 90%` |

**Model stage timeline** (`model-scroll.js`, one timeline unit per step):
- **Yaw:** 0 to 360° over the whole timeline, written to `viewer.orientation`.
- **Camera pitch:** 8° (near top-down) to 64° (3/4 view) during the first step, `power2.inOut`, written to `viewer.cameraOrbit`. This is the ORYZO top-down-to-3/4 reveal.
- **Step swap at each boundary `i`:**
  - the old step goes up and out (y 0 to -24, 0.18 units, starting at `i - 0.2`),
  - the new step comes in from below (y 24 to 0, 0.2 units, at `i`).
- **HUD:** the progress bar scales 0 to 1, and the counter shows `floor(progress × steps) + 1`.
- **Scroll length:** follows the number of `.model-step` items, so adding or removing a step needs no JS change.

## Content and imagery

- **Imagery:** the parts are the hero imagery. Use CAD renders or photos, ideally on dark or transparent backgrounds. 3D models must be `.glb` and need a transparent poster.
- **Copy:**
  - Write in plain language and sentence case.
  - Name things by what they are.
  - Never invent results or numbers. Unknown content stays as a visible `[placeholder]`.
- **Icons:** 1.5px gold strokes, outline only, 32px, inline SVG.

## Don't

- Don't add drop shadows, gradients as decoration, or background-colour bands between sections.
- Don't use bold headings or all-caps labels.
- Don't add a second accent colour. Gold is for strokes only and green is for the status dot only.
- Don't add a second "bold moment" to a page that already has one.
- Don't add numbered markers (01, 02) to things that aren't a sequence. The model steps are a sequence; tiles aren't.
- Don't add animations outside `gsap.matchMedia()`, and don't use CSS transitions or keyframe animations for motion.
