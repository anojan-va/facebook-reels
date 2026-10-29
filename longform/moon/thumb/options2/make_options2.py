"""Six more thumbnail styles for the Moon video (1280x720, no people): torn sky, eraser, phone alert, newspaper,
stranded boats, flat graphic poster. Usage: python3 make_options2.py -> option-6..11 + options2-sheet.jpg"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../options"))
os.chdir(os.path.join(HERE, "../options"))   # importing make_options re-renders options 1-5 in its own folder
from make_options import W, H, INTER, SERIF, cover, text, vignette  # noqa: E402
ANTON = os.path.join(HERE, "../../../fonts/Anton-Regular.ttf")
os.chdir(HERE)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
out = []

# 6. TORN SKY: the sky ripped open where the Moon was. One quiet question on the right.
img = vignette(ImageEnhance.Contrast(cover("torn.jpg", 0.2, 0.5, 1.1)).enhance(1.1), 0.3)
text(img, (1230, 300), "WHO", ANTON, 130, (255, 255, 255, 255), anchor="rm")
text(img, (1230, 430), "TOOK IT?", ANTON, 130, (255, 214, 10, 255), anchor="rm", glow=(255, 160, 0))
img.convert("RGB").save("option-6-torn.jpg", quality=92); out.append("option-6-torn.jpg")

# 7. ERASER: a giant Moon with a pink eraser rubbing a stripe out of it.
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
src = Image.open("bigmoon.jpg").convert("RGB")
g = np.asarray(src.convert("L")); ys, xs = np.where(g > 60)
box = (xs.min(), ys.min(), xs.max(), ys.max())
S = 640
mo = src.crop(box).resize((S, S), Image.LANCZOS).convert("RGBA")
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
circle = (((xx - S / 2) ** 2 + (yy - S / 2) ** 2) < (S / 2 - 2) ** 2).astype(np.float32)
dist = np.abs((xx - S * 0.62) + (yy - S * 0.5)) / np.sqrt(2)                   # stroke from top-right to bottom-left
edge = 70 + 10 * np.sin((xx - yy) / 13) + 6 * np.cos((xx + yy) / 7)
along = (xx - yy)                                                                # erase only the upper-right part of the stroke
keep = np.clip((dist - edge) / 5, 0, 1)
keep = np.where(along > -120, keep, 1.0)
a_ = (circle * keep * 255).astype(np.uint8)
m = np.asarray(mo).copy(); m[..., 3] = a_
MX, MY = 600, 40
img.alpha_composite(Image.fromarray(m), (MX, MY))
rng = np.random.default_rng(3); dc = ImageDraw.Draw(img)
for _ in range(70):
    t = rng.uniform(0, 1); x = MX + S * 0.62 + 60 + t * 260 + rng.uniform(-60, 60); y = MY + S * 0.5 - (x - MX - S * 0.62) + rng.uniform(-50, 50)
    if 0 < y < H and x < W:
        r = rng.uniform(3, 8); dc.ellipse([x - r, y - r, x + r, y + r], fill=(225, 225, 225, 255))
er = Image.new("RGBA", (300, 140), (0, 0, 0, 0)); de = ImageDraw.Draw(er)
de.rounded_rectangle([0, 0, 300, 140], 28, fill=(255, 120, 150, 255), outline=(30, 30, 30, 255), width=6)
de.rounded_rectangle([190, 0, 300, 140], 28, fill=(40, 90, 200, 255), outline=(30, 30, 30, 255), width=6)
er = er.rotate(45, expand=True, resample=Image.BICUBIC)
img.alpha_composite(er, (MX + int(S * 0.62) + 60, MY - 40))
text(img, (60, 230), "ERASED", ANTON, 160, (255, 255, 255, 255))
text(img, (66, 430), "WHAT HAPPENS", INTER, 44, (255, 214, 10, 255))
text(img, (66, 485), "TO EARTH?", INTER, 44, (255, 214, 10, 255))
img.convert("RGB").save("option-7-eraser.jpg", quality=92); out.append("option-7-eraser.jpg")

# 8. PHONE ALERT: an emergency alert lock screen over the empty night sky (fictional alert).
img = vignette(cover("nightsky.jpg", 0.5, 0.5, 1.05), 0.3)
px, py, pw, ph = 690, 40, 380, 760
ph_ = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(ph_)
dp.rounded_rectangle([px - 14, py - 14, px + pw + 14, py + ph + 14], 64, fill=(20, 20, 24, 255))
dp.rounded_rectangle([px, py, px + pw, py + ph], 52, fill=(10, 18, 40, 255))
img.alpha_composite(ph_.filter(ImageFilter.GaussianBlur(25)), (10, 20)); img.alpha_composite(ph_)
scr = cover("nightsky.jpg", 0.3, 0.3, 1.6).crop((0, 0, pw, ph))
msk = Image.new("L", (pw, ph), 0); ImageDraw.Draw(msk).rounded_rectangle([0, 0, pw, ph], 52, fill=255)
img.paste(scr, (px, py), msk)
text(img, (px + pw // 2, py + 150), "21:47", INTER_SB, 110, (255, 255, 255, 255), anchor="mm")
text(img, (px + pw // 2, py + 230), "Tuesday", INTER_SB, 30, (220, 225, 240, 255), anchor="mm")
card = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dk = ImageDraw.Draw(card)
dk.rounded_rectangle([px + 18, py + 300, px + pw - 18, py + 520], 30, fill=(245, 245, 250, 240))
img.alpha_composite(card)
dk = ImageDraw.Draw(img)
dk.ellipse([px + 40, py + 322, px + 84, py + 366], fill=(230, 40, 40, 255))
text(img, (px + 62, py + 344), "!", INTER, 32, (255, 255, 255, 255), anchor="mm", shadow=False)
text(img, (px + 98, py + 344), "EMERGENCY ALERT", INTER, 26, (200, 30, 30, 255), anchor="lm", shadow=False)
for i, line in enumerate(["The Moon is no longer", "visible anywhere on", "Earth. This is not a drill."]):
    text(img, (px + 42, py + 400 + i * 36), line, INTER_SB, 27, (20, 20, 30, 255), anchor="lm", shadow=False)
text(img, (60, 230), "NOT A", ANTON, 150, (255, 255, 255, 255))
text(img, (60, 400), "DRILL.", ANTON, 150, (255, 60, 60, 255), glow=(255, 30, 30))
img.convert("RGB").save("option-8-alert.jpg", quality=92); out.append("option-8-alert.jpg")

# 9. NEWSPAPER: a fictional front page, tilted on a dark desk.
paper = Image.new("RGBA", (1000, 760), (238, 232, 218, 255)); dn = ImageDraw.Draw(paper)
text(paper, (500, 70), "The Night Herald", SERIF_B, 76, (25, 25, 25, 255), anchor="mm", shadow=False)
dn.line([(40, 125), (960, 125)], fill=(25, 25, 25, 255), width=4); dn.line([(40, 133), (960, 133)], fill=(25, 25, 25, 255), width=2)
text(paper, (500, 160), "FICTIONAL EDITION  ·  SPECIAL REPORT", INTER_SB, 20, (90, 90, 90, 255), anchor="mm", shadow=False)
text(paper, (500, 265), "MOON VANISHES", SERIF_B, 100, (15, 15, 15, 255), anchor="mm", shadow=False)
text(paper, (500, 365), "Scientists: “The tides are already changing”", SERIF, 40, (40, 40, 40, 255), anchor="mm", shadow=False)
photo = ImageEnhance.Color(cover("nightsky.jpg", 0.5, 0.2, 1.0)).enhance(0).resize((560, 315))
pd = ImageDraw.Draw(photo)
for k in range(24):
    a0 = k * 15; pd.arc([200, 40, 360, 200], a0, a0 + 8, fill=(255, 255, 255, 255), width=4)
paper.paste(photo, (40, 410))
for i in range(9):
    dn.line([(630, 420 + i * 34), (960 - (40 if i % 3 == 2 else 0), 420 + i * 34)], fill=(150, 145, 135, 255), width=12)
img = Image.new("RGBA", (W, H), (22, 18, 16, 255))
sh = Image.new("RGBA", paper.size, (0, 0, 0, 200)).rotate(-6, expand=True, fillcolor=(0, 0, 0, 0)).filter(ImageFilter.GaussianBlur(25))
pr = paper.rotate(-6, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
img.alpha_composite(sh, (130, 30)); img.alpha_composite(pr, (110, 0))
img = vignette(img, 0.45)
img.convert("RGB").save("option-9-newspaper.jpg", quality=92); out.append("option-9-newspaper.jpg")

# 10. STRANDED BOATS: the effect, not the cause - an empty harbour.
img = vignette(ImageEnhance.Contrast(cover("stranded.jpg", 0.5, 0.75, 1.1)).enhance(1.1), 0.3)
text(img, (W // 2, 105), "WHERE DID THE", ANTON, 110, (255, 255, 255, 255), anchor="mm")
text(img, (W // 2, 225), "SEA GO?", ANTON, 130, (255, 214, 10, 255), anchor="mm", glow=(255, 160, 0))
img.convert("RGB").save("option-10-stranded.jpg", quality=92); out.append("option-10-stranded.jpg")

# 11. FLAT GRAPHIC: Swiss-poster style, solid colour, no photo.
img = Image.new("RGBA", (W, H), (255, 204, 0, 255)); dg = ImageDraw.Draw(img)
dg.ellipse([760, 120, 1200, 560], fill=(20, 20, 20, 255))
dg.ellipse([840, 200, 1120, 480], fill=(255, 204, 0, 255))
for k in range(30):
    a0 = k * 12; dg.arc([850, 210, 1110, 470], a0, a0 + 6, fill=(20, 20, 20, 255), width=8)
dg.rectangle([0, 600, W, 720], fill=(20, 20, 20, 255))
text(img, (60, 150), "NO", ANTON, 230, (20, 20, 20, 255), shadow=False)
text(img, (60, 370), "MOON?", ANTON, 190, (20, 20, 20, 255), shadow=False)
text(img, (60, 660), "TIDES  ·  SEASONS  ·  DAYS  ·  ANIMALS", INTER, 40, (255, 204, 0, 255), anchor="lm", shadow=False, track=4)
img.convert("RGB").save("option-11-flat.jpg", quality=92); out.append("option-11-flat.jpg")

tiles = []
for i, f in enumerate(out, 6):
    t = Image.open(f).resize((640, 360))
    ImageDraw.Draw(t).rounded_rectangle([12, 12, 96, 80], 14, fill=(255, 214, 10))
    ImageDraw.Draw(t).text((54, 46), str(i), font=ImageFont.truetype(INTER, 46), fill=(0, 0, 0), anchor="mm")
    tiles.append(t)
sheet = Image.new("RGB", (1280, 1080), (20, 20, 20))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % 2) * 640, (i // 2) * 360))
sheet.save("options2-sheet.jpg", quality=88)
print("ok2")
