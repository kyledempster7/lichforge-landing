#!/usr/bin/env python3
"""Checks that the landing-page logo cannot show a black box on any browser.

Run: python3 scripts/test_prep_assets.py   (needs Pillow)
"""
import random
import sys
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prep_assets import ROOT, black_to_alpha  # noqa: E402

LOGO = ROOT / "assets" / "lichforge-logo.png"


def screen(c, b):
    return c + b - c * b / 255


class LogoTransparency(unittest.TestCase):
    def test_logo_has_alpha_and_clear_corners(self):
        im = Image.open(LOGO)
        self.assertEqual(im.mode, "RGBA", "logo must carry real transparency")
        w, h = im.size
        for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (5, 5), (w - 6, h - 6)]:
            # The source background is near-black noise (max 7/255), so allow that faint alpha.
            self.assertLessEqual(im.getpixel((x, y))[3], 8, f"corner {(x, y)} is not transparent")

    def test_screen_blend_unchanged_and_normal_has_no_black(self):
        # Every source colour, composited the two ways a browser may draw it.
        rnd = random.Random(1)
        cols = [(0, 0, 0), (255, 255, 255), (3, 40, 44), (120, 200, 210)] + [
            tuple(rnd.randrange(256) for _ in range(3)) for _ in range(400)]
        src = Image.new("RGB", (len(cols), 1))
        src.putdata(cols)
        out = black_to_alpha(src)
        for c, (r, g, b, a) in zip(cols, out.getdata()):
            for bg in [(2, 5, 7), (6, 28, 35), (200, 30, 90)]:
                for ch, f, bk in zip(c, (r, g, b), bg):
                    blended = (1 - a / 255) * bk + (a / 255) * screen(f, bk)
                    self.assertLessEqual(abs(blended - screen(ch, bk)), 1.5)
                    normal = (1 - a / 255) * bk + (a / 255) * f
                    if c == (0, 0, 0):
                        self.assertEqual(normal, bk)  # pure black shows the backdrop


if __name__ == "__main__":
    unittest.main(verbosity=2)
