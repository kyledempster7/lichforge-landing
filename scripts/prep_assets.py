#!/usr/bin/env python3
"""Deterministic asset prep for the Lichforge landing page (Pillow only).

Usage: python3 scripts/prep_assets.py "path/to/lichforge logo vert.png"
The 1024x1536 source logo is not kept in this repo (it would be served publicly).
Writes assets/lichforge-logo.{png,webp}, assets/favicon.png, favicon.ico.
"""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
if len(sys.argv) != 2:
    sys.exit(__doc__)
SRC = Path(sys.argv[1])

# Source is 1024x1536 on black. LICHFORGE lettering ends ~y=1090; the divider
# and LICHFORGE.STUDIO line start ~y=1115 (rows 1092-1113 are background, max 7).
# Keep the black background (no background removal) for mix-blend-mode: screen.
LOGO_BOX = (100, 270, 924, 1110)      # generous top/side padding for the teal smoke
FAVICON_BOX = (330, 330, 700, 700)    # tight square on the skull-anvil emblem

def save_png(im, path):
    im.save(path, format="PNG", optimize=False, compress_level=9)

def main():
    src = Image.open(SRC).convert("RGB")
    logo = src.crop(LOGO_BOX)
    save_png(logo, ROOT / "assets" / "lichforge-logo.png")
    logo.save(ROOT / "assets" / "lichforge-logo.webp", format="WEBP", quality=92, method=6)

    fav = src.crop(FAVICON_BOX).resize((256, 256), Image.LANCZOS)
    save_png(fav, ROOT / "assets" / "favicon.png")
    fav.save(ROOT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

if __name__ == "__main__":
    main()
