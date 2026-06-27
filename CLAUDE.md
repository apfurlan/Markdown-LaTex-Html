# CLAUDE.md — LaTexHTML Project

## Visão geral

Este projeto converte **Markdown → HTML** para apresentações no estilo LaTeX Beamer,
usando **Python + CSS + MathJax 3**, sem frameworks, sem bundlers.

O fluxo de trabalho é:

```bash
python LaTexHTML.py --input minha_apresentacao.md --theme warsaw
# gera: minha_apresentacao.html
```

---

## Estrutura do projeto

```
LaTexHTML.py          ← conversor Python (único ponto de entrada)
example.md            ← apresentação de exemplo (fonte Markdown)
example.html          ← saída gerada pelo conversor
theme/
  nav.js              ← navegação JavaScript compartilhada (← → e botões)
  cambridgeus.css     ← tema CambridgeUS (dark red + gold)
  berlin.css          ← tema Berlin (dark navy + blue)
  copenhagen.css      ← tema Copenhagen (royal blue + gold tabs)
  frankfurt.css       ← tema Frankfurt (black + red, progress dots)
  singapore.css       ← tema Singapore (teal + amber)
  darmstadt.css       ← tema Darmstadt (steel blue + silver)
  boadilla.css        ← tema Boadilla (soft blue, rounded)
  madrid.css          ← tema Madrid (brick red + tan)
  warsaw.css          ← tema Warsaw (deep navy, full-width title band)
  annarbor.css        ← tema AnnArbor (Michigan blue + maize)
  pittsburgh.css      ← tema Pittsburgh (black + bright gold)
THEMES.md             ← paleta e diferenças visuais de cada tema
CLAUDE.md             ← este arquivo
beamer-cambridgeus.html  ← demo HTML legado (mantido como referência)
```

---

## Sintaxe Markdown do conversor

### Frontmatter YAML

```yaml
---
title: "Título Principal"
title_short: "Título Curto"       # usado no rodapé
subtitle: "Subtítulo"
author: "Nome Completo"
author_short: "N. Sobrenome"      # usado no rodapé
affiliation: |
  Departamento
  Universidade
date: "Mês Ano"
venue: "Local, Mês Ano"           # usado no rodapé (padrão: date)
institution: "Nome da Universidade"
department: "Departamento"
logo_text: "C"                    # letra no ícone SVG
logo_color: "#C9A227"             # cor do ícone SVG
theme: "warsaw"                   # tema padrão (pode ser sobrescrito por --theme na CLI)
sections:
  - Introdução
  - Resultados
  - Conclusão
---
```

### Slides e seções

```markdown
# Nome da Seção        ← muda a seção ativa na barra de navegação

## Título do Slide     ← cria um novo slide (frametitle)
```

O primeiro `## Slide` é sempre o slide de título (usa os metadados do frontmatter).

### Conteúdo dos slides

| Markdown | Resultado |
|---|---|
| `- item` | lista com marcador |
| `  - sub` | sub-lista (2 espaços) |
| `**negrito**` | negrito |
| `*itálico*` | itálico |
| `` `code` `` | código inline |
| `[texto]{.alert}` | texto em vermelho (alert) |
| `$...$` | math inline (MathJax) |
| `$$\n...\n$$` | math display (MathJax) |
| `\[\n...\n\]` | math display (MathJax) |

### Blocos Beamer

```markdown
:::theorem Theorem (Nome)
Conteúdo com $math$.
:::

:::definition Definition (Nome)
Conteúdo.
:::

:::example Example (Nome)
Conteúdo.
:::

:::alert ⚠ Aviso
Conteúdo.
:::
```

### Duas colunas

```markdown
::::columns

:::col
Conteúdo da coluna esquerda.

:::definition Bloco esquerdo
$H^s = ...$
:::
:::

:::col
Conteúdo da coluna direita.

:::theorem Bloco direito
Embedding theorem.
:::
:::

::::
```

---

## Adicionando um novo tema

1. Crie `theme/<nome>.css` baseado em qualquer tema existente.
2. Altere apenas as variáveis em `:root` e os estilos de `.section-pill`, `.frametitle`, `.slide-footer`.
3. Teste com: `python LaTexHTML.py --input example.md --theme <nome>`.
4. Documente no `THEMES.md`.

---

## Matemática (MathJax 3)

| Modo     | Delimitadores          |
|----------|------------------------|
| Inline   | `$...$` ou `\(...\)`   |
| Display  | `$$...$$` ou `\[...\]` |

Math é passado verbatim para o browser — o MathJax re-tipografa ao navegar entre slides via `MathJax.typesetPromise()`.

---

## Dependência Python

```bash
pip install pyyaml
```

MathJax carrega via CDN automaticamente no HTML gerado.

---

## Dimensões dos slides (por tema)

Controladas por variáveis CSS em `:root` de cada `theme/*.css`:

```css
--slide-w: 800px;    /* largura total — mude para 960px para 16:9 */
--slide-h: 600px;    /* altura de referência */
--head-h:  52px;
--foot-h:  28px;
--secbar-h:22px;
```

---

## Limitações conhecidas

| Recurso Beamer      | Status                                           |
|---------------------|--------------------------------------------------|
| `\pause` / overlays | ❌ Não implementado                              |
| Exportar PDF nativo | ❌ Use "Imprimir → Salvar como PDF" no navegador |
| Fontes Computer Modern | ❌ Substituídas por Helvetica/sans-serif       |
| Animações           | ❌ Não implementado                              |
| `\only`, `\uncover` | ❌ Não implementado                              |

---

## Convenções para Claude

- **Nunca** usar frameworks externos (React, Vue, Tailwind).
- O **input** é sempre `.md`; o **output** é sempre `.html` gerado pelo `LaTexHTML.py`.
- Não editar HTMLs de saída manualmente — editar o `.md` e regenerar.
- Estilos ficam em `theme/*.css`; nunca embutir CSS inline no HTML gerado.
- Para alterar paleta de um tema: modificar apenas as variáveis em `:root` do CSS correspondente.
- Navegação JS é compartilhada em `theme/nav.js` — não duplicar nem modificar.
- O seletor de slides é `.slide-wrap` — não alterar essa classe.
- MathJax é carregado **uma vez** no `<head>` pelo conversor — não duplicar.
