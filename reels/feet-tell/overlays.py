"""Graphic overlays for this reel: arrow at her feet, split frame + "?", dotted toe line, glowing EXIT sign."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fonts import font

W, H = 1152, 2048
img = Path(__file__).resolve().parent / "img"


def glow(base, layer, color):
    """Paste a white-drawn RGBA layer onto base with a coloured neon glow (blur 14 + 5 under the sharp layer)."""
    tint = Image.new("RGBA", layer.size, color + (0,))
    tint.putalpha(layer.getchannel("A"))
    out = base.convert("RGBA")
    for r in (14, 5):
        out = Image.alpha_composite(out, tint.filter(ImageFilter.GaussianBlur(r)))
    sharp = Image.new("RGBA", layer.size, (255, 255, 255, 0))
    sharp.putalpha(layer.getchannel("A"))
    return Image.alpha_composite(Image.alpha_composite(out, tint), sharp).convert("RGB")


def arrow(d, x0, y0, x1, y1, w, head):
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - head * math.cos(a), y1 - head * math.sin(a)
    d.line([(x0, y0), (bx, by)], fill=(255, 255, 255, 255), width=w)
    px, py = math.sin(a) * head * 0.6, -math.cos(a) * head * 0.6
    d.polygon([(x1, y1), (bx + px, by + py), (bx - px, by - py)], fill=(255, 255, 255, 255))


# 1. Arrow pointing down at her sneakers.
im = Image.open(img / "s02-girl.jpg").convert("RGB")
L = Image.new("RGBA", im.size, (0, 0, 0, 0))
arrow(ImageDraw.Draw(L), 940, 1330, 790, 1570, 12, 56)
glow(im, L, (255, 220, 60)).save(img / "s02-arrow.jpg", quality=95)

# 2. Split frame: smiling face on top, feet pointing away below; version b adds a "?".
face = Image.open(img / "s03-face.jpg").convert("RGB")
cw = 620; ch = round(cw * 1012 / W)
fx, fy = int(0.6 * W), int(0.36 * H)
top = face.crop((fx - cw // 2, fy - ch // 2, fx + cw // 2, fy + ch // 2)).resize((W, 1012))
feet = ImageOps.mirror(Image.open(img / "s04-feet-away.jpg").convert("RGB"))
bot = feet.crop((0, 520, W, 520 + 1012 * W // W))
split = Image.new("RGB", (W, H), "black")
split.paste(top, (0, 0)); split.paste(bot.resize((W, 1012)), (0, 1036))
L = Image.new("RGBA", im.size, (0, 0, 0, 0))
ImageDraw.Draw(L).line([(0, 1024), (W, 1024)], fill=(255, 255, 255, 255), width=8)
split = glow(split, L, (255, 255, 255))
split.save(img / "x01-split.jpg", quality=95)
L = Image.new("RGBA", im.size, (0, 0, 0, 0))
ImageDraw.Draw(L).text((900, 1560), "?", font=ImageFont.truetype(font("bold"), 300), fill=(255, 255, 255, 255), anchor="mm")
glow(split, L, (255, 220, 60)).save(img / "x01-split-q.jpg", quality=95)

# 3. Dotted line along the floor from her toes to his feet.
im = Image.open(img / "s06-turned.jpg").convert("RGB")
L = Image.new("RGBA", im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(L)
x0, x1, y = 700, 470, 1690
for x in range(x0, x1 + 60, -44):
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 255, 255, 255))
arrow(d, x1 + 40, y, x1 - 20, y, 1, 46)
glow(im, L, (255, 220, 60)).save(img / "s06-dotted.jpg", quality=95)

# 4. Feet pointing to the exit + glowing red EXIT sign with an arrow (upper third, clear of captions).
im = Image.open(img / "s04-feet-away.jpg").convert("RGB")
L = Image.new("RGBA", im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(L)
d.rounded_rectangle([300, 300, 900, 560], radius=24, outline=(255, 255, 255, 255), width=10)
d.text((560, 430), "EXIT", font=ImageFont.truetype(font("bold"), 170), fill=(255, 255, 255, 255), anchor="mm")
arrow(d, 760, 430, 860, 430, 22, 60)
on = glow(im, L, (255, 40, 40))
on.save(img / "s07-exit.jpg", quality=95)
