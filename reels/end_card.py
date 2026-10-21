"""End cards: white text with a yellow neon glow on pure black, in the upper third (clear of the caption band).

Usage: python end_card.py out.jpg "First sentence." ["Second sentence."]
Writes out.jpg with all lines; with two sentences also out-1.jpg with only the first (reveal the second on the next shot).
"""
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw

from overlay_kit import glow, layer, text

W, H = 1152, 2048


def card(lines, out, size=92):
    im = Image.new("RGB", (W, H), "black")
    L = layer(im)
    d = ImageDraw.Draw(L)
    y = 430
    for k, s in enumerate(lines):
        block = "\n".join(textwrap.wrap(s, 20))
        text(d, (W // 2, y + block.count("\n") * size * 0.62), block, size if k == 0 else int(size * 0.9))
        y += (block.count("\n") + 1) * int(size * 1.25) + 70
    glow(im, L).save(out, quality=95)


if __name__ == "__main__":
    out, sents = Path(sys.argv[1]), sys.argv[2:]
    card(sents, out)
    if len(sents) > 1:
        card(sents[:1], out.with_name(out.stem + "-1" + out.suffix))
