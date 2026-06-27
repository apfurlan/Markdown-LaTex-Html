# LaTexHTML

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![MathJax](https://img.shields.io/badge/MathJax-3-green?logo=latex&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![No frameworks](https://img.shields.io/badge/dependencies-pyyaml-orange)

> Convert Markdown presentations to **Beamer-style HTML slides** — no frameworks, no bundlers, just Python + CSS + MathJax.

---

## Demo

Write this in `slides.md`:

```markdown
---
title: "My Talk"
author: "Jane Doe"
theme: "warsaw"
sections:
  - Introduction
  - Results
---

# Introduction

## First Slide

- Point one
- Point two with $e^{i\pi} + 1 = 0$
```

Run:

```bash
python LaTexHTML.py --input slides.md
# → slides.html
```

Open `slides.html` in a browser and navigate with ← → arrow keys.

---

## Installation

```bash
pip install pyyaml
```

MathJax 3 is loaded automatically via CDN — no local install needed.

---

## Usage

```
python LaTexHTML.py --input FILE [--theme NAME] [--output FILE]
```

| Flag | Short | Description |
|---|---|---|
| `--input` | `-i` | Source `.md` file (required) |
| `--theme` | `-t` | Theme name — overrides frontmatter (default: `cambridgeus`) |
| `--output` | `-o` | Output `.html` file (default: same name as input) |

**Theme priority:** `--theme` CLI flag › `theme:` in frontmatter › `cambridgeus`

---

## Frontmatter Reference

```yaml
---
title: "Full Presentation Title"
title_short: "Short Title"        # shown in footer
subtitle: "Subtitle"
author: "Full Name"
author_short: "F. Name"           # shown in footer
affiliation: |
  Department Name
  University Name
date: "June 2026"
venue: "City, June 2026"          # shown in footer (falls back to date)
institution: "University Name"    # shown in slide header
department: "Department"          # shown in slide header

# Logo: use an image file…
logo: "logos/my_university.png"
# …or the built-in shield SVG
logo_text: "U"
logo_color: "#C9A227"

# Theme
theme: "warsaw"

# Navigation bar sections (order matters)
sections:
  - Introduction
  - Results
  - Conclusion
---
```

---

## Markdown Syntax

### Sections and slides

```markdown
# Section Name       ← updates the active section in the nav bar

## Slide Title       ← creates a new slide
```

The **first `## slide`** is always the title slide (uses frontmatter metadata).

### Inline formatting

| Markdown | Result |
|---|---|
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `` `code` `` | `code` |
| `[text]{.alert}` | red highlighted text |
| `$...$` | inline math (MathJax) |
| `$$\n...\n$$` | display math (MathJax) |
| `\[\n...\n\]` | display math (MathJax) |

### Images

```markdown
![Alt text](path/to/image.png)
![Alt text](path/to/image.png){width=60%}
```

Images are clipped to the slide body — slides always keep their fixed dimensions.

### Beamer blocks

```markdown
:::theorem Theorem (Name)
Content with $math$.
:::

:::definition Definition (Name)
Content.
:::

:::example Example (Name)
Content.
:::

:::alert ⚠ Warning
Content.
:::
```

### Two-column layout

```markdown
::::columns

:::col
Left column content.

![Image](chart.png){width=80%}
:::

:::col
:::theorem Right block
Embedding theorem.
:::
:::

::::
```

---

## Themes

| | Theme | Style |
|---|---|---|
| ![annarbor](docs/screenshots/annarbor.png) | `annarbor` | Michigan blue + maize |
| ![berlin](docs/screenshots/berlin.png) | `berlin` | Dark navy + blue |
| ![boadilla](docs/screenshots/boadilla.png) | `boadilla` | Soft blue, rounded |
| ![cambridgeus](docs/screenshots/cambridgeus.png) | `cambridgeus` | Dark red + gold |
| ![copenhagen](docs/screenshots/copenhagen.png) | `copenhagen` | Royal blue + gold tabs |
| ![darmstadt](docs/screenshots/darmstadt.png) | `darmstadt` | Steel blue + silver |
| ![frankfurt](docs/screenshots/frankfurt.png) | `frankfurt` | Black + red, progress dots |
| ![madrid](docs/screenshots/madrid.png) | `madrid` | Brick red + tan |
| ![pittsburgh](docs/screenshots/pittsburgh.png) | `pittsburgh` | Black + bright gold |
| ![singapore](docs/screenshots/singapore.png) | `singapore` | Teal + amber |
| ![warsaw](docs/screenshots/warsaw.png) | `warsaw` | Deep navy, full-width title band |

### Adding a new theme

1. Copy any existing `theme/*.css` as a starting point.
2. Edit only the variables in `:root` and the styles for `.section-pill`, `.frametitle`, `.slide-footer`.
3. Test: `python LaTexHTML.py --input example.md --theme mytheme`
4. Document it in `THEMES.md`.

### Slide dimensions

Controlled by CSS variables in each `theme/*.css`:

```css
:root {
  --slide-w:  800px;   /* total width  — use 960px for 16:9 */
  --slide-h:  600px;   /* total height */
  --head-h:   52px;
  --foot-h:   28px;
  --secbar-h: 22px;
}
```

---

## Navigation

| Action | Key / Button |
|---|---|
| Next slide | → or `Next` button |
| Previous slide | ← or `Prev` button |

---

## Project Structure

```
LaTexHTML.py        ← converter (single entry point)
example.md          ← example presentation source
example.html        ← generated output
theme/
  base.css          ← shared base styles (loaded before every theme)
  nav.js            ← shared navigation JavaScript
  warsaw.css        ← theme file (one per theme)
  ...
THEMES.md           ← theme palette reference
```

---

## Known Limitations

| Beamer feature | Status |
|---|---|
| `\pause` / overlays | not implemented |
| `\only`, `\uncover` | not implemented |
| Native PDF export | use Print → Save as PDF in the browser |
| Computer Modern fonts | replaced by Helvetica/sans-serif |
| Animations | not implemented |

---

## License

MIT
