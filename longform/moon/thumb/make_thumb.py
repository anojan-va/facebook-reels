"""Thumbnail for the Moon what-if video (1280x720): AI art + bold text, arrow, glow. No people (user rule).
Usage: python3 make_thumb.py  ->  thumbnail-no-moon.jpg"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

W, H = 1280, 720
ANTON = "../../fonts/Anton-Regular.ttf"
YELLOW, RED, WHITE = (255, 214, 10), (230, 30, 30), (255, 255, 255)


def cover(path, fx=0.5, fy=0.5, zoom=1.0):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = int((im.width - W) * fx)
    y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))


def outlined(draw_on, xy, text, size, fill, stroke=12, glow=None):
    f = ImageFont.truetype(ANTON, size)
    if glow:
        g = Image.new("RGBA", draw_on.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).text(xy, text, font=f, fill=(*glow, 255), stroke_width=stroke + 6, stroke_fill=(*glow, 255))
        draw_on.alpha_composite(g.filter(ImageFilter.GaussianBlur(18)))
    sh = Image.new("RGBA", draw_on.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + 8, xy[1] + 10), text, font=f, fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
    draw_on.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(draw_on).text(xy, text, font=f, fill=(*fill, 255), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return f.getbbox(text, stroke_width=stroke)


def arrow(canvas, p0, p1, color=RED, width=22):
    """Thick hand-drawn style arrow from p0 to p1 with a black outline."""
    d = ImageDraw.Draw(canvas)
    mid = ((p0[0] + p1[0]) / 2 - 40, (p0[1] + p1[1]) / 2 - 60)
    pts = [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * mid[0] + t ** 2 * p1[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * mid[1] + t ** 2 * p1[1])
           for t in np.linspace(0, 1, 40)]
    ang = np.arctan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0])
    L = 60
    head = [p1, (p1[0] - L * np.cos(ang - 0.5), p1[1] - L * np.sin(ang - 0.5)), (p1[0] - L * np.cos(ang + 0.5), p1[1] - L * np.sin(ang + 0.5))]
    for col, w, grow in [((0, 0, 0), width + 12, 8), (color, width, 0)]:
        d.line(pts[:-3], fill=(*col, 255), width=w, joint="curve")
        hh = [(p1[0] + grow * np.cos(ang), p1[1] + grow * np.sin(ang)),
              (head[1][0] - grow * np.cos(ang - 0.5), head[1][1] - grow * np.sin(ang - 0.5)),
              (head[2][0] - grow * np.cos(ang + 0.5), head[2][1] - grow * np.sin(ang + 0.5))]
        d.polygon(hh, fill=(*col, 255))


def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.15)
    im = ImageEnhance.Color(im).enhance(1.25)
    a = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    v = np.clip(1 - 0.5 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2), 0.45, 1)[..., None]
    return Image.fromarray(np.clip(a * v, 0, 255).astype(np.uint8))


def tw(text, size, stroke=12):
    b = ImageFont.truetype(ANTON, size).getbbox(text, stroke_width=stroke)
    return b[2] - b[0], b[3]


# --- Moon crumbling over the ocean, no people. "NO MOON?" stacked left, red "WHAT NOW?" box, arrow to the Moon.
bg = grade(cover("art-a.jpg", fx=0.75, fy=0.15, zoom=1.12)).convert("RGBA")
dark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(dark).rectangle([0, 0, 560, H], fill=(0, 0, 0, 120))
bg.alpha_composite(dark.filter(ImageFilter.GaussianBlur(90)))
outlined(bg, (40, 20), "NO", 300, YELLOW, glow=(255, 160, 0))
outlined(bg, (44, 315), "MOON?", 175, WHITE, stroke=11)
fl = ImageFont.truetype(ANTON, 100)
tx, ty = 62, 530
bb = fl.getbbox("WHAT NOW?", stroke_width=7)
d = ImageDraw.Draw(bg)
d.rectangle([tx + bb[0] - 22, ty + bb[1] - 12, tx + bb[2] + 22, ty + bb[3] + 12], fill=(*RED, 255), outline=(0, 0, 0, 255), width=7)
outlined(bg, (tx, ty), "WHAT NOW?", 100, WHITE, stroke=7)
arrow(bg, (330, 250), (760, 230))
bg.convert("RGB").save("thumbnail-no-moon.jpg", quality=92)
print("ok")
