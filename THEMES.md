# Available Themes

All themes live in `theme/<name>.css`. Pass the name to `--theme`.

```
python LaTexHTML.py --input slides.md --theme <name>
```

---

## Theme Palette Reference

| Theme        | Primary       | Accent        | Body bg   | Visual character                          |
|--------------|---------------|---------------|-----------|-------------------------------------------|
| cambridgeus  | `#8B0000`     | `#C9A227` gold | `#F5F5F0` | Dark red + gold, classic Cambridge        |
| berlin       | `#0F2240`     | `#4A90D9` blue | white     | Deep navy, square bullets, uppercase pills |
| copenhagen   | `#1A4F8B`     | `#F0C040` gold | `#FAFAFA` | Royal blue, tab-shaped section bar        |
| frankfurt    | `#1A1A1A`     | `#CC0033` red  | white     | Near-black, red accent, circular section dots |
| singapore    | `#005F87`     | `#E6A817` amber| `#F0F7F7` | Teal gradient header, rounded pills       |
| darmstadt    | `#2D5A8E`     | `#7FB2D0` silver| `#F5F6F8`| Steel blue, underline frametitle          |
| boadilla     | `#3D6EA8`     | `#D4A820` gold | `#FAFAF5` | Soft blue, rounded corners, light section bar |
| madrid       | `#7A1A1A`     | `#C8A04A` tan  | `#FFF9F2` | Brick red + golden tan, warm body         |
| warsaw       | `#1A1A5E`     | `#8888CC` purple| white   | Deep indigo, full-width frametitle band   |
| annarbor     | `#00274C`     | `#FFCB05` maize| white    | Michigan blue + maize section bar         |
| pittsburgh   | `#1A1A1A`     | `#FFB81C` gold | white     | Black + bright gold, inverted title block |

---

## Notable styling differences

### Section bar
- **Copenhagen** — tab-shaped pills aligned to the bottom of the bar
- **Frankfurt** — circle dot per section (progress indicator style)
- **AnnArbor** — entire section bar is maize-colored
- **Boadilla** — light gray bar with dark blue pills (inverted from others)

### Frametitle
- **Warsaw** — full-width dark band spanning the slide
- **Pittsburgh** — gray background stripe spanning the slide
- **Singapore** — left-bordered with a subtle gradient fade
- **Copenhagen** — underline with gold accent instead of left border

### Title slide
- **Pittsburgh** — title in inverted dark block with gold text
- **Madrid** — warm cream gradient body
- **CambridgeUS** — white-to-gray gradient
