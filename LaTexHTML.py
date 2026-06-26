#!/usr/bin/env python3
"""
LaTexHTML — Convert Markdown presentations to Beamer-style HTML.

Usage:
    python LaTexHTML.py --input slides.md --theme warsaw
    python LaTexHTML.py --input slides.md --theme annarbor --output out.html
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pip install pyyaml")


# ── Frontmatter ──────────────────────────────────────────────────────────────

def parse_frontmatter(text: str):
    """Split YAML frontmatter from body. Returns (meta_dict, body_str)."""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end == -1:
        return {}, text
    meta = yaml.safe_load(text[3:end]) or {}
    body = text[end + 4:].lstrip('\n')
    return meta, body


# ── Inline renderer ──────────────────────────────────────────────────────────

def render_inline(text: str) -> str:
    """Apply inline Markdown transforms, leaving math delimiters untouched."""
    # [text]{.alert}  →  <span class="alert">text</span>
    text = re.sub(r'\[([^\]]+)\]\{\.alert\}', r'<span class="alert">\1</span>', text)
    # **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # *italic*  (not inside **)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


# ── Body parser ──────────────────────────────────────────────────────────────

def parse_body(body: str, meta_sections: list):
    """
    Parse body text into a list of slide dicts and the ordered section list.

    Slide dict keys:
        title       str   frame title (or ignored for title slide)
        section     str   current section when slide appears
        is_title    bool  True only for the very first slide
        lines       list  raw content lines
    """
    lines = body.splitlines()
    sections = list(meta_sections) if meta_sections else []
    current_section = sections[0] if sections else ''
    slides = []
    current = None

    for line in lines:
        # Top-level section heading  (# Heading, not ## Heading)
        if re.match(r'^# [^#]', line):
            name = line[2:].strip()
            if name not in sections:
                sections.append(name)
            current_section = name
            continue

        # Slide heading  (## Title)
        if re.match(r'^## ', line):
            if current is not None:
                slides.append(current)
            current = {
                'title': line[3:].strip(),
                'section': current_section,
                'is_title': False,
                'lines': [],
            }
            continue

        if current is not None:
            current['lines'].append(line)

    if current is not None:
        slides.append(current)

    # First slide is always the title slide
    if slides:
        slides[0]['is_title'] = True

    return slides, sections


# ── Block content renderer ───────────────────────────────────────────────────

def render_content(lines: list) -> str:
    """
    Convert a list of raw lines into HTML.

    Supported syntax:
        - Paragraphs (blank-line separated)
        - Bullet lists:  - item  or  * item
        - Sub-lists:     (2-space indent) - sub
        - Display math:  $$ ... $$  or  \\[ ... \\]
        - Beamer blocks: :::theorem Title ... :::
        - Two columns:   ::::columns / :::col ... ::: / ::::
    """
    out = []
    i = 0
    in_ul = False
    in_sub = False

    def flush_lists():
        nonlocal in_ul, in_sub
        if in_sub:
            out.append('</ul>')
            in_sub = False
        if in_ul:
            out.append('</ul>')
            in_ul = False

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()

        # ── blank line ────────────────────────────────────────────────
        if not s:
            flush_lists()
            i += 1
            continue

        # ── display math  \[ ... \] ───────────────────────────────────
        if s.startswith(r'\['):
            flush_lists()
            block = [s]
            if not (s.endswith(r'\]') and len(s) > 4):
                i += 1
                while i < len(lines) and r'\]' not in lines[i]:
                    block.append(lines[i])
                    i += 1
                if i < len(lines):
                    block.append(lines[i])
            out.append('\n'.join(block))
            i += 1
            continue

        # ── display math  $$  (standalone opening line) ───────────────
        if s == '$$':
            flush_lists()
            block = [s]
            i += 1
            while i < len(lines) and lines[i].strip() != '$$':
                block.append(lines[i])
                i += 1
            if i < len(lines):
                block.append(lines[i].strip())
            out.append('\n'.join(block))
            i += 1
            continue

        # ── display math  $$...$$ on one line ────────────────────────
        if s.startswith('$$') and s.endswith('$$') and len(s) > 4:
            flush_lists()
            out.append(s)
            i += 1
            continue

        # ── columns block  ::::columns ... :::: ───────────────────────
        if s == '::::columns':
            flush_lists()
            out.append('<div class="columns">')
            i += 1
            while i < len(lines) and lines[i].strip() != '::::':
                if lines[i].strip() == ':::col':
                    col_lines = []
                    i += 1
                    while i < len(lines) and lines[i].strip() not in (':::col', '::::', ':::'):
                        col_lines.append(lines[i])
                        i += 1
                    out.append('<div class="col">')
                    out.append(render_content(col_lines))
                    out.append('</div>')
                    # consume an optional ::: closing marker for the column
                    if i < len(lines) and lines[i].strip() == ':::':
                        i += 1
                else:
                    i += 1
            out.append('</div>')
            i += 1
            continue

        # ── beamer block  :::type [Title] ... ::: ────────────────────
        m = re.match(r'^:::([\w-]+)\s*(.*)', s)
        if m and not s.startswith('::::'):
            flush_lists()
            btype = m.group(1)
            btitle = m.group(2).strip()
            block_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != ':::':
                block_lines.append(lines[i])
                i += 1
            css = {
                'theorem':    'theorem',
                'definition': 'definition',
                'example':    'example',
                'alert':      'alert-block',
            }.get(btype, btype)
            inner = render_content(block_lines)
            header = (f'\n  <div class="block-header">{render_inline(btitle)}</div>'
                      if btitle else '')
            out.append(
                f'<div class="block {css}">'
                f'{header}'
                f'\n  <div class="block-body">{inner}</div>'
                f'\n</div>'
            )
            i += 1
            continue

        # ── sub-list item  (≥2 spaces indent) ────────────────────────
        if re.match(r'^\s{2,}[-*]\s', raw):
            if not in_ul:
                out.append('<ul class="itemize">')
                in_ul = True
            if not in_sub:
                out.append('<ul class="itemize sub">')
                in_sub = True
            content = re.sub(r'^\s+[-*]\s+', '', raw)
            out.append(f'<li>{render_inline(content)}</li>')
            i += 1
            continue

        # ── top-level list item ───────────────────────────────────────
        if re.match(r'^[-*]\s', s):
            if in_sub:
                out.append('</ul>')
                in_sub = False
            if not in_ul:
                out.append('<ul class="itemize">')
                in_ul = True
            content = re.sub(r'^[-*]\s+', '', s)
            out.append(f'<li>{render_inline(content)}</li>')
            i += 1
            continue

        # ── paragraph ─────────────────────────────────────────────────
        flush_lists()
        out.append(f'<p>{render_inline(s)}</p>')
        i += 1

    flush_lists()
    return '\n'.join(out)


# ── Slide renderer ───────────────────────────────────────────────────────────

_SHIELD_SVG = (
    '<svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M14 2 L24 6 L24 16 C24 22 14 26 14 26 C14 26 4 22 4 16 L4 6 Z"'
    ' fill="none" stroke="{color}" stroke-width="1.5"/>'
    '<text x="9" y="19" font-family="serif" font-size="13"'
    ' fill="{color}" font-weight="bold">{letter}</text>'
    '</svg>'
)


def render_slide(slide: dict, sections: list, meta: dict, idx: int, total: int) -> str:
    inst       = meta.get('institution', 'University')
    dept       = meta.get('department', '')
    logo_color = meta.get('logo_color', '#C9A227')
    logo_text  = meta.get('logo_text', inst[:1])

    logo_svg = _SHIELD_SVG.format(color=logo_color, letter=logo_text)

    # Section bar
    cur_sec = slide['section']
    pills = []
    for sec in sections:
        if not sec:
            continue
        cls = 'section-pill current' if sec == cur_sec else 'section-pill'
        pills.append(f'<span class="{cls}">{sec}</span>')
    section_bar = '<span class="section-sep">›</span>'.join(pills)

    # Body
    if slide['is_title']:
        affil = str(meta.get('affiliation', '')).replace('\n', '<br>')
        body_inner = (
            f'<div class="main-title">{meta.get("title", slide["title"])}</div>\n'
            f'    <div class="subtitle">{meta.get("subtitle", "")}</div>\n'
            f'    <div class="author">{meta.get("author", "")}</div>\n'
            f'    <div class="affiliation">{affil}</div>\n'
            f'    <div class="date">{meta.get("date", "")}</div>'
        )
        body_class = 'slide-body title-body'
    else:
        body_inner = (
            f'<div class="frametitle">{slide["title"]}</div>\n'
            + render_content(slide['lines'])
        )
        body_class = 'slide-body'

    author_short = meta.get('author_short', meta.get('author', ''))
    title_short  = meta.get('title_short',  meta.get('title',  '')[:35])
    venue        = meta.get('venue',         meta.get('date',   ''))
    active       = ' active' if idx == 0 else ''

    return f'''\
<!-- SLIDE {idx + 1} – {slide["title"]} -->
<div class="slide-wrap{active}" data-slide="{idx + 1}">
  <div class="slide-header">
    <div class="inst-logo">
      {logo_svg}
      <span class="inst-name">{inst}</span>
    </div>
    <div class="header-right">{dept}</div>
  </div>
  <div class="gold-line"></div>
  <div class="section-bar">
    {section_bar}
  </div>
  <div class="{body_class}">
    {body_inner}
  </div>
  <div class="slide-footer">
    <span>{author_short} — {title_short}</span>
    <span>{venue}</span>
    <span class="page-num">{idx + 1} / {total}</span>
  </div>
</div>'''


# ── HTML assembler ───────────────────────────────────────────────────────────

def build_html(meta: dict, slides: list, sections: list, theme: str) -> str:
    page_title = meta.get('title', 'Presentation')
    n = len(slides)

    slides_html = '\n\n'.join(
        render_slide(s, sections, meta, i, n) for i, s in enumerate(slides)
    )

    return f'''\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<script>
  window.MathJax = {{
    tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']] }},
    options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre'] }}
  }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
<link rel="stylesheet" href="theme/{theme}.css">
</head>
<body>

<div id="nav">
  <button id="prev-btn" onclick="changeSlide(-1)" disabled>&#9664; Prev</button>
  <span id="slide-counter">1 / {n}</span>
  <button id="next-btn" onclick="changeSlide(1)">Next &#9654;</button>
</div>

{slides_html}

<script src="theme/nav.js"></script>
</body>
</html>'''


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description='Convert a Markdown presentation to Beamer-style HTML.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument('--input',  '-i', required=True, metavar='FILE',
                    help='Source Markdown file (.md)')
    ap.add_argument('--theme',  '-t', default='cambridgeus', metavar='NAME',
                    help='Theme name — must match theme/<name>.css (default: cambridgeus)')
    ap.add_argument('--output', '-o', default=None, metavar='FILE',
                    help='Output HTML file (default: same name as input, .html extension)')
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.exit(f"Error: input file not found: {src}")

    dst = Path(args.output) if args.output else src.with_suffix('.html')
    theme_css = Path(__file__).parent / 'theme' / f'{args.theme}.css'
    if not theme_css.exists():
        available = sorted(p.stem for p in (Path(__file__).parent / 'theme').glob('*.css'))
        sys.exit(
            f"Error: theme '{args.theme}' not found.\n"
            f"Available themes: {', '.join(available)}"
        )

    text = src.read_text(encoding='utf-8')
    meta, body = parse_frontmatter(text)
    slides, sections = parse_body(body, meta.get('sections', []))

    if not slides:
        sys.exit("Error: no slides found. Use '## Slide Title' to define slides.")

    html = build_html(meta, slides, sections, args.theme)
    dst.write_text(html, encoding='utf-8')
    print(f"✓  {dst}  ({len(slides)} slides, theme: {args.theme})")


if __name__ == '__main__':
    main()
