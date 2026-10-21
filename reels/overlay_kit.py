"""Glowing graphics drawn over generated images: neon text, speech bubbles, arrows, highlights, fades.

Klein can't spell, so every bubble/title/label in a reel is drawn here. Draw on an RGBA layer in white, then
glow(base, layer, colour) adds the neon halo (layer blurred 14 px + 5 px under the sharp lines).
Keep text out of the caption band (frame y 0.42-0.58).
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from fonts import font

YELLOW, RED, WHITE, GREY = (255, 220, 60), (255, 40, 40), (255, 255, 255), (120, 120, 120)


def layer(im):
    return Image.new("RGBA", im.size, (0, 0, 0, 0))


def glow(base, lay, color=YELLOW, sharp=WHITE):
    """Composite a white-drawn RGBA layer onto base with a coloured neon glow."""
    tint = Image.new("RGBA", lay.size, color + (0,))
    tint.putalpha(lay.getchannel("A"))
    out = base.convert("RGBA")
    for r in (14, 5):
        out = Image.alpha_composite(out, tint.filter(ImageFilter.GaussianBlur(r)))
    top = Image.new("RGBA", lay.size, sharp + (0,))
    top.putalpha(lay.getchannel("A"))
    return Image.alpha_composite(Image.alpha_composite(out, tint), top).convert("RGB")


def text(d, xy, s, size, name="bold", fill=WHITE + (255,)):
    d.multiline_text(xy, s, font=ImageFont.truetype(font(name), size), fill=fill, anchor="mm", align="center", spacing=size // 4)


def arrow(d, x0, y0, x1, y1, w, head, fill=WHITE + (255,)):
    a = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - head * math.cos(a), y1 - head * math.sin(a)
    d.line([(x0, y0), (bx, by)], fill=fill, width=w)
    px, py = math.sin(a) * head * 0.6, -math.cos(a) * head * 0.6
    d.polygon([(x1, y1), (bx + px, by + py), (bx - px, by - py)], fill=fill)


def bubble(im, box, s, tail, size=56, line=WHITE, txt=WHITE, color=YELLOW):
    """Speech bubble: black-filled rounded box with a white outline and a tail pointing at `tail` (x, y)."""
    x0, y0, x1, y1 = box
    base = im.convert("RGB")
    d = ImageDraw.Draw(base)
    cx = min(max(tail[0], x0 + 60), x1 - 60)
    edge = y1 if tail[1] > y1 else y0
    tri = [(cx - 34, edge), (cx + 34, edge), tail]
    d.rounded_rectangle(box, radius=40, fill=(0, 0, 0))
    d.polygon(tri, fill=(0, 0, 0))
    lay = layer(base)
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle(box, radius=40, outline=line + (255,), width=7)
    ld.line([tri[0], tail, tri[1]], fill=line + (255,), width=7)
    ld.line([(tri[0][0] + 6, edge), (tri[1][0] - 6, edge)], fill=(0, 0, 0, 255), width=9)
    out = glow(base, lay, color, sharp=line)
    lay = layer(out)
    text(ImageDraw.Draw(lay), ((x0 + x1) // 2, (y0 + y1) // 2), s, size, "semibold", fill=txt + (255,))
    return Image.alpha_composite(out.convert("RGBA"), lay).convert("RGB")


def yellow_mask(im):
    """0-255 mask of the yellow parts of the man: the whole old mannequin, or the new man's hoodie and glow."""
    a = np.asarray(im.convert("RGB")).astype(int)
    return Image.fromarray(np.clip(((a[..., 0] + a[..., 1]) / 2 - a[..., 2] - 25) * 4, 0, 255).astype("uint8"))


def fade_man(im, bg=None):
    """Make the yellow man see-through: replace his body and glow with `bg` (the same image generated without him,
    via a Klein edit) or black, then add back a faint yellow tint, a ghost of him, and a thin outline."""
    core = yellow_mask(im).point(lambda v: 255 if v > 200 else 0).filter(ImageFilter.GaussianBlur(5)).point(lambda v: 255 if v > 128 else 0)
    halo = core.filter(ImageFilter.MaxFilter(41)).filter(ImageFilter.GaussianBlur(10))
    out = Image.composite(bg if bg is not None else Image.new("RGB", im.size, "black"), im, halo)
    out = Image.composite(Image.blend(out, im, 0.18), out, core).convert("RGBA")
    tint = Image.new("RGBA", im.size, YELLOW + (0,)); tint.putalpha(core.point(lambda v: v * 0.12))
    edge = core.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
    line = Image.new("RGBA", im.size, (255, 240, 170, 0)); line.putalpha(edge.point(lambda v: v * 0.6))
    return Image.alpha_composite(Image.alpha_composite(out, tint), line).convert("RGB")


def focus_blur(im, ellipse, radius=9):
    """Blur everything outside `ellipse` (x0, y0, x1, y1), soft edge."""
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).ellipse(ellipse, fill=255)
    return Image.composite(im, im.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: v * 0.6),
                           m.filter(ImageFilter.GaussianBlur(60)))
