#!/usr/bin/env python3
"""Generate the static font instances that the LaTeX theme needs.

XeTeX and pdfTeX cannot pick a weight from a variable font (they load its
default instance only), so the Beamer theme ships static instances cut from
the skill's bundled variable fonts with fontTools. Run from this folder:

    python3 make-static-fonts.py

Requires: pip install fonttools
"""
import shutil
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

SKILL_FONTS = Path(__file__).resolve().parent.parent / "skills" / "gw-presentation" / "fonts"
OUT = Path(__file__).resolve().parent / "fonts"

# (variable font, axis values, static file name, style name)
INSTANCES = [
    ("NunitoSans-VariableFont.ttf", {"wght": 400}, "NunitoSans-Regular.ttf", "Regular"),
    ("NunitoSans-VariableFont.ttf", {"wght": 700}, "NunitoSans-Bold.ttf", "Bold"),
    ("NunitoSans-Italic-VariableFont.ttf", {"wght": 400}, "NunitoSans-Italic.ttf", "Italic"),
    ("NunitoSans-Italic-VariableFont.ttf", {"wght": 700}, "NunitoSans-BoldItalic.ttf", "Bold Italic"),
    ("SourceSerif4-VariableFont.ttf", {"wght": 400}, "SourceSerif4-Regular.ttf", "Regular"),
    ("SourceSerif4-Italic-VariableFont.ttf", {"wght": 400}, "SourceSerif4-Italic.ttf", "Italic"),
    ("Oswald-VariableFont.ttf", {"wght": 500}, "Oswald-Medium.ttf", "Medium"),
    ("Oswald-VariableFont.ttf", {"wght": 600}, "Oswald-SemiBold.ttf", "SemiBold"),
]
# Already static in the skill: copied unchanged.
COPIES = [
    "BarlowCondensed-SemiBold.ttf", "BarlowCondensed-Bold.ttf",
    "BarlowCondensed-SemiBoldItalic.ttf",
    "OFL-barlowcondensed.txt", "OFL-nunitosans.txt", "OFL-sourceserif4.txt", "OFL-oswald.txt",
]


def set_names(font, family, style):
    """Give the instance a plain family/style name so fontspec sees one family."""
    name = font["name"]
    full = f"{family} {style}" if style != "Regular" else family
    ps = f"{family.replace(' ', '')}-{style.replace(' ', '')}"
    for rec in list(name.names):
        if rec.nameID in (1, 2, 3, 4, 6, 16, 17):
            name.removeNames(nameID=rec.nameID)
    for nid, val in ((1, family), (2, style), (3, f"{family}:{style}"), (4, full), (6, ps)):
        name.setName(val, nid, 3, 1, 0x409)
        name.setName(val, nid, 1, 0, 0)


def main():
    OUT.mkdir(exist_ok=True)
    for src, axes, dst, style in INSTANCES:
        vf = TTFont(SKILL_FONTS / src)
        axes = {**{a.axisTag: a.defaultValue for a in vf["fvar"].axes}, **axes}
        static = instantiateVariableFont(vf, axes, inplace=False)
        family = dst.split("-")[0]
        family = {"NunitoSans": "Nunito Sans", "SourceSerif4": "Source Serif 4"}.get(family, family)
        set_names(static, family, style)
        static.save(OUT / dst)
        print("wrote", dst)
    for f in COPIES:
        shutil.copy(SKILL_FONTS / f, OUT / f)
        print("copied", f)


if __name__ == "__main__":
    main()
