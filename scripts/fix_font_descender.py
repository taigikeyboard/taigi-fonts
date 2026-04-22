#!/usr/bin/env python3
"""Fix font descender truncation by adjusting hhea/OS2 metrics.

Usage: python3 scripts/fix_font_descender.py <font-name>
Example: python3 scripts/fix_font_descender.py iansui
"""

from __future__ import annotations

import sys
from pathlib import Path

from fontTools import ttLib

# Target values referenced from Noto Sans CJK TC
NEW_HHEA_DESCENT = -250
NEW_OS2_DESCENT = -200

FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"


def resolve_font(name: str) -> Path:
    folder = FONTS_DIR / name
    for ext in ("ttf", "otf"):
        path = folder / f"font.{ext}"
        if path.exists():
            return path
    raise FileNotFoundError(f"No font.ttf or font.otf in {folder}")


def print_metrics(font_path: Path) -> int:
    font = ttLib.TTFont(font_path)
    hhea = font["hhea"]
    os2 = font["OS/2"]
    head = font["head"]

    print(f"Metrics for {font_path}")
    print(f"  hhea: ascent={hhea.ascent} descent={hhea.descent} lineGap={hhea.lineGap}")
    print(f"  OS/2: typoAsc={os2.sTypoAscender} typoDesc={os2.sTypoDescender} "
          f"winAsc={os2.usWinAscent} winDesc={os2.usWinDescent}")
    print(f"  head: unitsPerEm={head.unitsPerEm}")

    descent = hhea.descent
    font.close()
    return descent


def fix_descender(font_path: Path) -> Path:
    output_path = font_path.with_stem(f"{font_path.stem}-fixed")

    font = ttLib.TTFont(font_path)
    font["hhea"].descent = NEW_HHEA_DESCENT
    font["OS/2"].sTypoDescender = NEW_OS2_DESCENT
    font.save(output_path)
    font.close()

    print(f"Fixed: {output_path} (hhea.descent={NEW_HHEA_DESCENT}, "
          f"OS/2.sTypoDescender={NEW_OS2_DESCENT})")
    return output_path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/fix_font_descender.py <font-name>")
        print(f"Available: {', '.join(sorted(p.name for p in FONTS_DIR.iterdir() if p.is_dir()))}")
        sys.exit(1)

    font_path = resolve_font(sys.argv[1])

    original_descent = print_metrics(font_path)
    fixed_path = fix_descender(font_path)
    print_metrics(fixed_path)

    print(f"Original: {font_path} (descent={original_descent})")
    print(f"Fixed:    {fixed_path}")


if __name__ == "__main__":
    main()
