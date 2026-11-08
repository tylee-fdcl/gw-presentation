# GW Beamer theme

A LaTeX Beamer theme with the same look as the HTML and PowerPoint decks the skill makes: GW palette, Barlow Condensed display type with Avenir Next or Nunito Sans body text, the six-pointed star pattern on dark slides, buff rules, Buff 20% tiles, and the GW Engineering lockup on the first and last slides. It is for people who write their slides in LaTeX by hand (or on Overleaf) rather than asking an agent for a deck.

```latex
\documentclass[aspectratio=169]{beamer}
\usetheme{GW}
\title{Title}\author{Name}\date{Month 2026}
\begin{document}
\gwcoverframe{Event name}{Title of the talk}{A subtitle}{\insertdate}
\begin{frame}[t]{A standard slide}
    \framesubtitle{Eyebrow above the title}
    ...
\end{frame}
\gwclosingframe{Thank you}{Questions \& discussion}
\end{document}
```

`gw-theme-demo.tex` uses every component once; `gw-theme-demo.pdf` is its output.

## Files

| Path | Contents |
|---|---|
| `beamerthemeGW.sty` | The theme: fonts, colors, frame heading, lists, and the macros listed in its header comment (cover, big idea, split, divider, closing; cards, stat tiles, big-number rows, share pairs, bars, formula; chevron ribbon, gate crossbar, star accent) |
| `gw-theme-demo.tex` | One slide per component, with placeholder text |
| `assets/` | Star-pattern backgrounds and the chevron ribbon as vector PDFs, and the GW Engineering lockups; built from `skills/gw-presentation/assets/` by `make-assets.py` |
| `fonts/` | Static instances of the skill's free substitute fonts, cut from the variable fonts in `skills/gw-presentation/fonts/` by `make-static-fonts.py` (TeX engines can't pick a weight from a variable font) |

## Compiling

- **XeLaTeX** (recommended) or **LuaLaTeX**: brand fonts. Avenir Next is used for body text when it is installed; otherwise Nunito Sans from `fonts/`. Display, accent and heavy display always come from `fonts/`, so the output matches the HTML deck's free-font mode exactly.
- **pdfLaTeX**: same layouts with TeX Gyre Heros, Heros Condensed and Termes in place of the fonts above.
- Compile twice, from the folder that holds `beamerthemeGW.sty`, `assets/` and `fonts/`. To keep one copy of the theme elsewhere, say `\providecommand{\gwthemepath}{../gw-presentation/latex/}` before `\usetheme{GW}`.
- **Overleaf:** upload this folder (or add it to your project), set the compiler to XeLaTeX. Overleaf has no Avenir Next, so body text falls back to Nunito Sans.

## Proportions

The HTML template is 1280 × 720 px; a Beamer 16:9 page is 16 × 9 cm, so 80 px = 1 cm and 1 px = 0.354 pt. Every size in the theme is converted at that rate (a 50 px slide title is 17.7 pt, the 80 px side margin is 1 cm), so a Beamer slide and an HTML slide of the same layout line up when overlaid.

## Rebuilding the derived files

Only needed after changing the skill's SVGs or fonts.

```bash
pip install fonttools playwright && python3 -m playwright install chromium
cd latex
python3 make-static-fonts.py   # fonts/
python3 make-assets.py         # assets/*.pdf, assets/logo-*.png
```
