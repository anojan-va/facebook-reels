"""Five thumbnail styles for the Moon video (1280x720, no people): split, poster, cartoon, wave, diagram.
Usage: python3 make_options.py  ->  option-1-split.jpg ... option-5-diagram.jpg + options-sheet.jpg"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

W, H = 1280, 720
ANTON = "../../../fonts/Anton-Regular.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf"


def cover(path, fx=0.5, fy=0.5, zoom=1.0):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x, y = int((im.width - W) * fx), int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H)).convert("RGBA")


def text(img, xy, s, font, size, fill, stroke=0, sfill=(0, 0, 0), anchor="la", track=0, glow=None, shadow=True):
    f = ImageFont.truetype(font, size)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if track:   # letter-spaced
        total = sum(f.getlength(c) for c in s) + track * (len(s) - 1)
        x = xy[0] - (total / 2 if anchor[0] == "m" else 0)
        for c in s:
            d.text((x, xy[1]), c, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill, anchor="l" + anchor[1])
            x += f.getlength(c) + track
    else:
        d.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill, anchor=anchor)
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        g.putalpha(layer.split()[3].filter(ImageFilter.GaussianBlur(18)))
        tint = Image.new("RGBA", img.size, (*glow, 0)); tint.putalpha(g.split()[3])
        img.alpha_composite(tint); img.alpha_composite(tint)
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh.putalpha(layer.split()[3].filter(ImageFilter.GaussianBlur(8)).point(lambda v: v * 0.7))
        img.alpha_composite(sh, (4, 6))
    img.alpha_composite(layer)
    return f.getbbox(s, anchor=anchor)


def vignette(img, k=0.55):
    yy, xx = np.mgrid[0:H, 0:W]
    v = np.clip(1 - k * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2), 0.35, 1)[..., None]
    a = np.asarray(img.convert("RGB")).astype(np.float32) * v
    return Image.fromarray(a.astype(np.uint8)).convert("RGBA")


out = []

# 1. SPLIT: the same town, Moon / no Moon, torn down the middle. Two small labels, no big headline.
L = Image.new("RGBA", (W, H), (0, 0, 0, 255)); L.paste(cover("a-before.jpg", 0.45, 0.4, 1.1), (-W // 4 + 40, 0))
R = ImageEnhance.Brightness(cover("a-after.jpg", 0.45, 0.4, 1.1)).enhance(0.9)
img = L.copy()
mask = Image.new("L", (W, H), 0)
pts = [(W // 2 + int(14 * np.sin(y / 23) + 9 * np.sin(y / 7)), y) for y in range(0, H + 10, 10)]
ImageDraw.Draw(mask).polygon(pts + [(W, H), (W, 0)], fill=255)
img.paste(R, (0, 0), mask)
ImageDraw.Draw(img).line(pts, fill=(255, 255, 255, 255), width=5)
for x, lab, col in ((W // 4, "TONIGHT", (255, 255, 255)), (3 * W // 4, "TOMORROW?", (255, 70, 70))):
    f = ImageFont.truetype(INTER, 54); b = f.getbbox(lab, anchor="mm")
    ImageDraw.Draw(img).rounded_rectangle([x + b[0] - 26, 600 + b[1] - 16, x + b[2] + 26, 600 + b[3] + 16], 18, fill=(0, 0, 0, 200))
    text(img, (x, 600), lab, INTER, 54, (*col, 255), anchor="mm", shadow=False)
img.convert("RGB").save("option-1-split.jpg", quality=92); out.append("option-1-split.jpg")

# 2. POSTER: minimalist film-poster look, empty sky, thin glowing ring, elegant serif title.
img = vignette(cover("b-poster.jpg", 0.5, 1.0, 1.25), 0.4)
ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(ring).ellipse([W // 2 - 110, 110, W // 2 + 110, 330], outline=(235, 240, 255, 255), width=5)
for r_ in (16, 8, 8):
    img.alpha_composite(ring.filter(ImageFilter.GaussianBlur(r_)))
img.alpha_composite(ring)
text(img, (W // 2, 470), "No Moon.", SERIF, 150, (240, 242, 248, 255), anchor="mm", glow=(140, 170, 255))
text(img, (W // 2, 575), "WHAT WOULD HAPPEN TO EARTH?", INTER, 30, (190, 200, 225, 255), anchor="mm", track=10)
img.convert("RGB").save("option-2-poster.jpg", quality=92); out.append("option-2-poster.jpg")

# 3. CARTOON: bright explainer style, chunky rounded text and a speech bubble.
img = Image.new("RGBA", (W, H), (0, 0, 0, 255)); img.paste(cover("c-cartoon.jpg", 0.5, 0.5, 1.05), (-150, 0)); img.paste(cover("c-cartoon.jpg", 0.0, 0.5, 1.05).crop((W - 150, 0, W, H)), (W - 150, 0))
d = ImageDraw.Draw(img)
d.polygon([(800, 380), (650, 470), (880, 390)], fill=(40, 20, 90, 255))
d.polygon([(808, 372), (668, 455), (868, 378)], fill=(255, 255, 255, 255))
d.rounded_rectangle([690, 60, 1250, 395], 60, fill=(255, 255, 255, 255), outline=(40, 20, 90, 255), width=10)
text(img, (970, 165), "WHERE'S", INTER, 84, (40, 20, 90, 255), anchor="mm", shadow=False)
text(img, (970, 290), "MY MOON?!", INTER, 78, (255, 140, 0, 255), anchor="mm", shadow=False)
img.convert("RGB").save("option-3-cartoon.jpg", quality=92); out.append("option-3-cartoon.jpg")

# 4. WAVE: dark disaster still, one headline across the empty sky, no boxes or arrows.
img = vignette(ImageEnhance.Contrast(cover("d-wave.jpg", 0.5, 1.0, 1.12)).enhance(1.15), 0.35)
text(img, (W // 2, 120), "THE MOON VANISHED.", ANTON, 118, (255, 255, 255, 255), anchor="mm", glow=(80, 160, 255))
text(img, (W // 2, 235), "THEN THE OCEANS CHANGED", INTER, 44, (120, 200, 255, 255), anchor="mm", track=6)
img.convert("RGB").save("option-4-wave.jpg", quality=92); out.append("option-4-wave.jpg")

# 5. DIAGRAM: data/HUD style, tilted Earth, big monospace numbers.
img = Image.new("RGBA", (W, H), (0, 0, 0, 255)); img.paste(cover("e-diagram.jpg", 0.5, 0.5, 1.05), (330, 0))
d = ImageDraw.Draw(img)
for i in range(0, W, 64):
    d.line([(i, 0), (i, H)], fill=(80, 140, 255, 22), width=1)
for j in range(0, H, 64):
    d.line([(0, j), (W, j)], fill=(80, 140, 255, 22), width=1)
text(img, (70, 150), "EARTH'S TILT", MONO, 40, (140, 190, 255, 255))
text(img, (60, 210), "23.5°", MONO, 150, (255, 255, 255, 255))
text(img, (70, 390), "WITHOUT THE MOON:", MONO, 40, (255, 120, 90, 255))
text(img, (60, 450), "80°?", MONO, 170, (255, 90, 60, 255), glow=(255, 60, 30))
img.convert("RGB").save("option-5-diagram.jpg", quality=92); out.append("option-5-diagram.jpg")

# contact sheet with option numbers
tiles = []
for i, f in enumerate(out, 1):
    t = Image.open(f).resize((640, 360))
    ImageDraw.Draw(t).rounded_rectangle([12, 12, 80, 80], 14, fill=(255, 214, 10))
    ImageDraw.Draw(t).text((46, 46), str(i), font=ImageFont.truetype(INTER, 48), fill=(0, 0, 0), anchor="mm")
    tiles.append(t)
sheet = Image.new("RGB", (1280, 1080), (20, 20, 20))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % 2) * 640, (i // 2) * 360))
sheet.save("options-sheet.jpg", quality=88)
print("ok")
