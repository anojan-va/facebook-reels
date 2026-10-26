"""Thumbnails for the asteroid what-if video (1280x720): AI art + rembg face cutout + bold text, arrow, glow.
Usage: python3 make_thumb.py  ->  thumbnail-24-hours.jpg, thumbnail-earth.jpg"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from rembg import remove, new_session

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


sess = new_session("isnet-general-use")
face = remove(Image.open("art-face.jpg").convert("RGB"), session=sess)
a = np.asarray(face).copy()
import cv2
al = np.clip((a[..., 3].astype(np.float32) / 255 - 0.4) / 0.4, 0, 1)   # drop matte residue
n, lab, st, _ = cv2.connectedComponentsWithStats((al > 0).astype(np.uint8))
keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))                    # keep only the person (largest blob)
a[..., 3] = (al * (lab == keep) * 255).astype(np.uint8)
face = Image.fromarray(a)
face = face.crop(face.getbbox())


def place_face(bg, height, x, glow=(255, 140, 30)):
    f = face.resize((int(face.width * height / face.height), height), Image.LANCZOS)
    P = 60                                            # pad so the glow is not clipped into a box at the layer edge
    al = Image.new("L", (f.width + 2 * P, f.height + 2 * P), 0)
    al.paste(f.split()[3], (P, P))
    rim = Image.new("RGBA", al.size, (*glow, 0))
    rim.putalpha(al.filter(ImageFilter.GaussianBlur(16)))
    bg.alpha_composite(rim, (x + 6 - P, H - f.height - 2 - P)) if x + 6 - P >= 0 else \
        bg.alpha_composite(rim.crop((P - x - 6, 0, rim.width, rim.height)), (0, H - f.height - 2 - P))
    bg.alpha_composite(f, (x, H - f.height + 8))


def tw(text, size, stroke=12):
    b = ImageFont.truetype(ANTON, size).getbbox(text, stroke_width=stroke)
    return b[2] - b[0], b[3]


# --- A: fireball over the city (right), shocked face (bottom-left), "24 HOURS LEFT" right-aligned + arrow up to it
bg = grade(cover("art-a.jpg", fx=0.85, fy=0.0, zoom=1.15)).convert("RGBA")
place_face(bg, 470, -40)
w1, h1 = tw("24 HOURS", 150)
x1 = W - 30 - w1
outlined(bg, (x1, 420), "24 HOURS", 150, YELLOW, glow=(255, 120, 0))
fl = ImageFont.truetype(ANTON, 115)
tx, ty = x1 + w1 - 330, 568
bb = fl.getbbox("LEFT", stroke_width=7)
d = ImageDraw.Draw(bg)
d.rectangle([tx + bb[0] - 26, ty + bb[1] - 14, tx + bb[2] + 26, ty + bb[3] + 14], fill=(*RED, 255), outline=(0, 0, 0, 255), width=7)
outlined(bg, (tx, ty), "LEFT", 115, WHITE, stroke=7)
arrow(bg, (x1 + 60, 440), (x1 + 170, 300))
bg.convert("RGB").save("thumbnail-24-hours.jpg", quality=92)

# --- B: Earth being hit (right), shocked face (bottom-left), "WHAT IF?"
bg = grade(cover("art-c.jpg", fx=1.0, fy=0.5, zoom=1.3)).convert("RGBA")
place_face(bg, 470, -40)
w1, _ = tw("WHAT IF?", 170)
outlined(bg, (W - 30 - w1, 500), "WHAT IF?", 170, YELLOW, glow=(255, 120, 0))
bg.convert("RGB").save("thumbnail-earth.jpg", quality=92)
print("ok")
