"""Draw chat bubbles onto a blank phone image (Klein can't spell more than 2-3 words).

Usage: python phone_text.py blank_phone.jpg out.jpg bubbles.json
bubbles.json: [{"text": "Had a great time\\ntonight!", "side": "right", "y": 0.36, "status": "Seen ✓✓"},
               {"text": "Still thinking about\\nthat terrible dessert 😂", "side": "left"}]
side: left (received) / right (sent). y: top of the bubble as a fraction of the image height
(default: stacked under the previous bubble). Emoji are drawn in colour with Segoe UI Emoji.
"""
import json
import re
import sys

from PIL import Image, ImageDraw, ImageFont

from fonts import emoji_image
from fonts import font as font_path

EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def draw(blank, out, bubbles):
    im = Image.open(blank).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    size = int(W * 0.04)
    font = ImageFont.truetype(font_path("regular"), size)
    small = ImageFont.truetype(font_path("regular"), int(size * 0.74))
    sym = ImageFont.truetype(font_path("symbol"), int(size * 0.74))
    esize = int(size * 1.05)
    lh, pad, y = int(size * 1.3), int(size * 0.7), H * 0.3

    def width(line):
        return sum(emoji_image(ch, esize).width + 4 if EMOJI.match(ch) else d.textlength(ch, font=font) for ch in line)

    for b in bubbles:
        lines = b["text"].split("\n")
        y = H * b["y"] if "y" in b else y
        bw = max(width(l) for l in lines) + 2 * pad
        bh = lh * len(lines) + pad
        if b.get("side", "left") == "right":
            x0 = W * 0.76 - bw
            tail = [(x0 + bw - 40, y + bh), (x0 + bw - 22, y + bh + 34), (x0 + bw - 78, y + bh)]
        else:
            x0 = W * 0.24
            tail = [(x0 + 40, y + bh), (x0 + 22, y + bh + 34), (x0 + 78, y + bh)]
        d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=int(size * 0.75), outline="white", width=4)
        d.polygon(tail, fill="black")
        d.line(tail, fill="white", width=4)
        for i, line in enumerate(lines):
            x = x0 + pad
            for ch in line:
                ty = y + pad * 0.4 + lh * i
                if EMOJI.match(ch):
                    e = emoji_image(ch, esize)
                    im.paste(e, (int(x + 2), int(ty + size * 0.2)), e)
                    x += e.width + 4
                else:
                    d.text((x, ty), ch, font=font, fill="white")
                    x += d.textlength(ch, font=font)
        y += bh + 50
        if b.get("status"):
            word, marks = (b["status"].split(" ", 1) + [""])[:2]
            tw = d.textlength(word + " ", font=small) + d.textlength(marks, font=sym)
            sx = x0 + bw - tw
            d.text((sx, y - 10), word + " ", font=small, fill=(170, 170, 170))
            d.text((sx + d.textlength(word + " ", font=small), y - 10), marks, font=sym, fill=(170, 170, 170))
            y += int(size * 1.2)
    im.save(out, quality=95)
    print(out)


if __name__ == "__main__":
    draw(sys.argv[1], sys.argv[2], json.loads(open(sys.argv[3], encoding="utf-8").read()))
