#!/usr/bin/env python3
"""Deterministic asset prep for the Lichforge landing page (Pillow only).

Usage: python3 scripts/prep_assets.py "path/to/lichforge logo vert.png"
The 1024x1536 source logo is not kept in this repo (it would be served publicly).
Writes assets/lichforge-logo.{png,webp}, assets/lichforge-og.png, assets/favicon.png, favicon.ico.
"""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# Source is 1024x1536 on black. LICHFORGE lettering ends ~y=1090; the divider
# and LICHFORGE.STUDIO line start ~y=1115 (rows 1092-1113 are background, max 7).
# The black background is turned into real transparency (black_to_alpha), and the
# page still applies mix-blend-mode: screen. Where a browser blends, the result is
# the same pixels as screen-blending the old black-backed logo; where it does not
# (seen on phones), there is no black left to show as a box behind the logo.
LOGO_BOX = (100, 270, 924, 1110)      # generous top/side padding for the teal smoke
FAVICON_BOX = (330, 330, 700, 700)    # tight square on the skull-anvil emblem

def save_png(im, path):
    im.save(path, format="PNG", optimize=False, compress_level=9)

def black_to_alpha(im):
    """RGB on black -> RGBA: alpha = brightest channel, colour un-premultiplied.

    Composited normally over a backdrop B this gives C + (1 - a) * B; with
    mix-blend-mode: screen it gives exactly C + B - C * B, the old look.
    """
    im = im.convert("RGB")
    px = []
    for r, g, b in im.getdata():
        a = max(r, g, b)
        if a == 0:
            px.append((0, 0, 0, 0))
        else:
            px.append((min(255, round(r * 255 / a)), min(255, round(g * 255 / a)),
                       min(255, round(b * 255 / a)), a))
    out = Image.new("RGBA", im.size)
    out.putdata(px)
    return out

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Image.open(Path(sys.argv[1])).convert("RGB")
    # Link previews (og:image) keep the black background: preview cards may be white.
    save_png(src.crop(LOGO_BOX), ROOT / "assets" / "lichforge-og.png")
    logo = black_to_alpha(src.crop(LOGO_BOX))
    save_png(logo, ROOT / "assets" / "lichforge-logo.png")
    logo.save(ROOT / "assets" / "lichforge-logo.webp", format="WEBP", quality=92, method=6)

    fav = src.crop(FAVICON_BOX).resize((256, 256), Image.LANCZOS)
    save_png(fav, ROOT / "assets" / "favicon.png")
    fav.save(ROOT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

if __name__ == "__main__":
    main()
