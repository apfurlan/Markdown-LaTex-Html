---
# ── Presentation metadata ─────────────────────────────────────────────────────
title: "Fourier Analysis & Its Applications to PDEs"
title_short: "Fourier Analysis"
subtitle: "A Modern Perspective"
author: "Dr. Alice Thornton"
author_short: "A. Thornton"
affiliation: |
  Department of Applied Mathematics & Theoretical Physics
  University of Cambridge
date: "June 2026"
venue: "Cambridge, June 2026"

# ── Institution branding ──────────────────────────────────────────────────────
institution: "University of Cambridge"
department: "Dept. of Applied Mathematics"
logo_text: "C"
logo_color: "#C9A227"

# ── Section order in the navigation bar ──────────────────────────────────────
sections:
  - Introduction
  - Main Results
  - Applications
  - Conclusion
---

# Introduction

## Title Slide

<!-- This is the title slide — content here is ignored; metadata is used instead. -->

## Motivation

Many problems in mathematical physics reduce to understanding solutions of the form:

$$
u(x,t) = \sum_{n=-\infty}^{\infty} \hat{u}_n(t)\, e^{inx}
$$

Key questions we will address:

- Under what conditions does the Fourier series [converge]{.alert}?
- How do derivatives interact: $\widehat{u'} = i\xi\,\hat{u}$?
- Can we characterise smoothness via decay of $|\hat{u}(\xi)|$ as $|\xi|\to\infty$?
- What is the Sobolev regularity of a given PDE's solution?

# Main Results

## Core Results

:::definition Definition (Fourier Transform)
For $f \in L^1(\mathbb{R})$, the *Fourier transform* is defined by
$$
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x)\,e^{-2\pi i \xi x}\,dx, \quad \xi \in \mathbb{R}.
$$
:::

:::theorem Theorem (Plancherel)
If $f \in L^1(\mathbb{R}) \cap L^2(\mathbb{R})$, then $\hat{f}\in L^2(\mathbb{R})$ and
$$
\|f\|_{L^2} = \|\hat{f}\|_{L^2}.
$$
The Fourier transform extends to a *unitary isomorphism* on $L^2(\mathbb{R})$.
:::

## Heat Equation via Fourier Transform

Consider the initial value problem on $\mathbb{R}$:

$$\partial_t u = \Delta u, \quad u(x,0) = f(x).$$

:::example Example (Gaussian kernel)
Taking the Fourier transform in $x$ yields $\partial_t \hat{u} = -4\pi^2|\xi|^2 \hat{u}$,
so $\hat{u}(\xi,t) = e^{-4\pi^2|\xi|^2 t}\hat{f}(\xi)$.
Inverting: $u = K_t * f$ where
$$K_t(x) = \frac{1}{(4\pi t)^{n/2}}\exp\!\left(-\frac{|x|^2}{4t}\right).$$
:::

:::alert ⚠ Remark
The solution is [instantly smooth]{.alert} for $t>0$, even if $f$ is only in $L^2$.
This is the *smoothing effect* of the heat operator.
:::

# Applications

## Sobolev Spaces & Regularity

::::columns

:::col
:::definition Definition ($H^s$ space)
For $s\ge 0$, the Sobolev space $H^s(\mathbb{R}^n)$ is:
$$H^s = \bigl\{f\in L^2 : \langle\xi\rangle^s\hat{f}\in L^2\bigr\}$$
where $\langle\xi\rangle = (1+|\xi|^2)^{1/2}$.
:::

The index $s$ measures *fractional smoothness*: $f\in H^s$ iff $f$ has $s$ derivatives in $L^2$.
:::

:::col
:::theorem Sobolev Embedding
If $s > n/2 + k$, then
$$H^s(\mathbb{R}^n)\hookrightarrow C^k(\mathbb{R}^n).$$
:::

- $n=1$: $H^1 \hookrightarrow C^0$ (continuous functions)
- $n=3$: need $s>3/2$ for continuity
- Key tool for PDE well-posedness
:::

::::

# Conclusion

## Summary & Outlook

- The Fourier transform diagonalises constant-coefficient differential operators.
- Plancherel's theorem makes $L^2$ the natural setting for PDE analysis.
- Sobolev spaces $H^s$ quantify regularity and enable embedding theorems.
- The heat kernel $K_t$ illustrates [infinite-speed smoothing]{.alert}.

:::example Open Problems
- Regularity of Navier-Stokes solutions — Millennium Prize Problem.
- Unique continuation for Schrödinger operators.
- Sparse Fourier algorithms for high-dimensional PDEs.
:::

**Thank you.** | thornton@dpmms.cam.ac.uk
