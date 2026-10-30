"""Thumbnails for the Mars what-if video (1280x720). No real faces: the astronaut's visor is mirrored.
Usage: python3 make_thumb.py -> thumbnail-1-contract.jpg, thumbnail-2-stuck.jpg, thumbnail-3-potato.jpg, thumbs-sheet.jpg"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../moon/thumb/options"))
os.chdir(os.path.join(HERE, "../../moon/thumb/options"))
from make_options import W, H, INTER, cover, text, vignette  # noqa: E402
os.chdir(HERE)
ANTON = os.path.join(HERE, "../../fonts/Anton-Regular.ttf")


def pop(img):
    return ImageEnhance.Color(ImageEnhance.Contrast(img.convert("RGB")).enhance(1.08)).enhance(1.15).convert("RGBA")


def tag(img, xy, s, size, fill, bg, rot=0):
    f = ImageFont.truetype(INTER, size)
    b = f.getbbox(s)
    t = Image.new("RGBA", (b[2] - b[0] + 60, b[3] - b[1] + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, t.width - 1, t.height - 1], 16, fill=(*bg, 255), outline=(0, 0, 0, 255), width=6)
    d.text((30 - b[0], 20 - b[1]), s, font=f, fill=(*fill, 255))
    t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(t, xy)


out = []
# 1. CONTRACT: "I AGREE" joke.
img = vignette(pop(cover("art-a.jpg", 0.8, 0.4, 1.08)), 0.3)
text(img, (40, 40), "I CLICKED", ANTON, 130, (255, 255, 255, 255), stroke=8)
text(img, (40, 190), "“I AGREE”", ANTON, 150, (255, 214, 10, 255), stroke=8, glow=(255, 150, 0))
tag(img, (40, 400), "1 YEAR ON MARS", 54, (255, 255, 255), (220, 40, 40), rot=4)
img.convert("RGB").save("thumbnail-1-contract.jpg", quality=92); out.append("thumbnail-1-contract.jpg")

# 2. STUCK: bored astronaut on a suitcase, Earth a tiny dot.
img = vignette(pop(cover("art-b.jpg", 0.75, 0.5, 1.15)), 0.3)
text(img, (40, 40), "DAY 365:", ANTON, 120, (255, 255, 255, 255), stroke=8)
text(img, (40, 180), "STILL HERE", ANTON, 150, (255, 214, 10, 255), stroke=8, glow=(255, 150, 0))
tag(img, (44, 400), "WHY CAN'T I LEAVE?!", 46, (20, 20, 20), (255, 255, 255), rot=-3)
img.convert("RGB").save("thumbnail-2-stuck.jpg", quality=92); out.append("thumbnail-2-stuck.jpg")

# 3. POTATO: potato as a trophy.
img = vignette(pop(cover("art-c.jpg", 1.0, 0.4, 1.2)), 0.3)
text(img, (30, 30), "MY FIRST", ANTON, 100, (255, 255, 255, 255), stroke=8)
text(img, (30, 140), "MARS", ANTON, 150, (255, 255, 255, 255), stroke=8)
text(img, (30, 310), "POTATO", ANTON, 170, (255, 214, 10, 255), stroke=8, glow=(255, 150, 0))
tag(img, (40, 560), "1 YEAR = 687 DAYS?!", 44, (255, 255, 255), (220, 40, 40), rot=3)
img.convert("RGB").save("thumbnail-3-potato.jpg", quality=92); out.append("thumbnail-3-potato.jpg")

sheet = Image.new("RGB", (1280, 1080), (20, 20, 20))
for i, f in enumerate(out):
    t = Image.open(f).resize((640, 360))
    ImageDraw.Draw(t).rounded_rectangle([12, 300, 70, 350], 12, fill=(255, 214, 10))
    ImageDraw.Draw(t).text((41, 325), str(i + 1), font=ImageFont.truetype(INTER, 40), fill=(0, 0, 0), anchor="mm")
    sheet.paste(t, ((i % 2) * 640, (i // 2) * 360))
sheet.save("thumbs-sheet.jpg", quality=88)
print("ok")
