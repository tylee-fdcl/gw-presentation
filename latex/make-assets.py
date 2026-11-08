#!/usr/bin/env python3
"""Build the PDF graphics the LaTeX theme includes, from the skill's brand SVGs.

- assets/stars-navy-yard.pdf, assets/stars-gw-blue.pdf: 16:9 backgrounds with the
  six-pointed star pattern tone-on-tone, bleeding off the right edge and fading
  toward the center (the HTML template's cover and dark big-idea treatment).
- assets/chevron-ribbon-buff.pdf: one seamless period of the buff chevron ribbon.
- assets/logo-*.png: copies of the GW Engineering lockups.

SVG to PDF uses the Chromium bundled with Playwright. Run from this folder:

    python3 make-assets.py

Requires: pip install playwright; python3 -m playwright install chromium
"""
import asyncio
import re
import shutil
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
SKILL = ROOT.parent / "skills" / "gw-presentation" / "assets"
OUT = ROOT / "assets"
W, H = 1280, 720
TILE_W, TILE_H = 540, 360  # on-slide size of one 207.36 x 138.24 star tile


def star_background(tile_svg: str, background: str) -> str:
    """Wrap the seamless star tile in a 1280 x 720 page with a horizontal fade."""
    tile = re.sub(r'<\?xml[^>]*\?>\s*', '', tile_svg)
    tile = re.sub(r'<svg[^>]*>', f'<svg width="{TILE_W}" height="{TILE_H}" viewBox="0 0 207.36 138.24">', tile, count=1)
    x0 = W * 0.45
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <pattern id="tile" patternUnits="userSpaceOnUse" width="{TILE_W}" height="{TILE_H}">{tile}</pattern>
  <linearGradient id="fade" gradientUnits="userSpaceOnUse" x1="{x0}" x2="{W * 0.835}">
    <stop offset="0" stop-color="black"/><stop offset="1" stop-color="white"/>
  </linearGradient>
  <mask id="mask"><rect x="{x0}" width="{W - x0}" height="{H}" fill="url(#fade)"/></mask>
</defs>
<rect width="{W}" height="{H}" fill="{background}"/>
<rect x="{x0}" width="{W - x0}" height="{H}" fill="url(#tile)" mask="url(#mask)"/>
</svg>'''


async def svg_to_pdf(page, svg: str, out: Path, width: float, height: float):
    await page.set_content(
        f'<html><head><style>@page{{size:{width}px {height}px;margin:0}}'
        f'html,body{{margin:0}}svg{{display:block}}</style></head><body>{svg}</body></html>')
    await page.pdf(path=str(out), width=f"{width}px", height=f"{height}px",
                   print_background=True, page_ranges="1")
    print("wrote", out.relative_to(ROOT))


async def main():
    OUT.mkdir(exist_ok=True)
    stars_blue = (SKILL / "battle-flag" / "gw-blue.svg").read_text()      # GW Blue stars
    stars_navy = re.sub("#033c5a", "#00223E", stars_blue, flags=re.I)      # Navy Yard stars
    chevron = (SKILL / "chevrons" / "ribbon" / "gw-buff.svg").read_text()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await svg_to_pdf(page, star_background(stars_blue, "#00223E"), OUT / "stars-navy-yard.pdf", W, H)
        await svg_to_pdf(page, star_background(stars_navy, "#033C5A"), OUT / "stars-gw-blue.pdf", W, H)
        # The ribbon tile is 156 x 12 units; render one period at 13 x 1 px per unit.
        ribbon = re.sub(r'<\?xml[^>]*\?>\s*', '', chevron)
        ribbon = re.sub(r'<svg[^>]*>', '<svg width="2028" height="156" viewBox="0 0 156 12">', ribbon, count=1)
        await svg_to_pdf(page, ribbon, OUT / "chevron-ribbon-buff.pdf", 2028, 156)
        await browser.close()
    for src, dst in (("gw-sch-seas-short-2c-rev.png", "logo-seas-reversed.png"),
                     ("gw-sch-seas-short-2c.png", "logo-seas.png")):
        shutil.copy(SKILL / "logos" / "seas" / src, OUT / dst)
        print("copied", dst)


asyncio.run(main())
