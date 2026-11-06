"""Thumbnails for 'What if the world ran out of oil overnight?' (1280x720, no people).
Usage: python3 make_thumb.py -> thumbnail-1-gauge.jpg, thumbnail-2-earth.jpg, thumbnail-3-highway.jpg, thumbs-sheet.jpg"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../moon/thumb/options"))
sys.path.insert(0, os.path.join(HERE, "../../asteroid-full/thumb"))
os.chdir(os.path.join(HERE, "../../moon/thumb/options"))
from make_options import W, H, INTER, cover, text, vignette  # noqa: E402
os.chdir(os.path.join(HERE, "../../asteroid-full/thumb"))
from make_thumb import arrow  # noqa: E402
os.chdir(HERE)
ANTON = os.path.join(HERE, "../../fonts/Anton-Regular.ttf")
YEL, WHITE = (255, 214, 10, 255), (255, 255, 255, 255)


def pop(img, c=1.1, s=1.15):
    return ImageEnhance.Color(ImageEnhance.Contrast(img.convert("RGB")).enhance(c)).enhance(s).convert("RGBA")


def tag(img, xy, s, size, fill, bg, rot=0):
    f = ImageFont.truetype(INTER, size)
    b = f.getbbox(s)
    t = Image.new("RGBA", (b[2] - b[0] + 60, b[3] - b[1] + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, t.width - 1, t.height - 1], 16, fill=(*bg, 255), outline=(0, 0, 0, 255), width=6)
    d.text((30 - b[0], 20 - b[1]), s, font=f, fill=(*fill, 255))
    img.alpha_composite(t.rotate(rot, expand=True, resample=Image.BICUBIC), xy)

out = []
# 1. Fuel gauge on empty, text on the right.
img = vignette(pop(cover("art-a.jpg", 0.2, 0.5, 1.05)), 0.3)
text(img, (700, 60), "OIL:", ANTON, 170, WHITE, stroke=10)
text(img, (700, 240), "ZERO", ANTON, 230, (255, 60, 40, 255), stroke=10, glow=(255, 80, 0))
tag(img, (710, 540), "OVERNIGHT", 70, (20, 20, 20), (255, 214, 10), rot=-3)
img.convert("RGB").save("thumbnail-1-gauge.jpg", quality=92); out.append("thumbnail-1-gauge.jpg")

# 2. Earth with the last drop of oil.
img = vignette(pop(cover("art-b.jpg", 0.5, 0.5, 1.05)), 0.3)
text(img, (W // 2, 80), "THE LAST DROP", ANTON, 130, WHITE, anchor="mm", stroke=9)
tag(img, (W // 2 - 260, 590), "NO OIL. NO FOOD?", 56, (255, 255, 255), (220, 30, 30), rot=-2)
img.convert("RGB").save("thumbnail-2-earth.jpg", quality=92); out.append("thumbnail-2-earth.jpg")

# 3. Abandoned highway: "DAY 1 WITHOUT OIL" + arrow to the dry pump.
img = vignette(pop(cover("art-c.jpg", 0.4, 0.5, 1.05), 1.15, 1.1), 0.25)
text(img, (40, 40), "DAY 1", ANTON, 210, YEL, stroke=10, glow=(255, 150, 0))
text(img, (40, 290), "WITHOUT", ANTON, 120, WHITE, stroke=9)
text(img, (40, 430), "OIL", ANTON, 150, WHITE, stroke=9)
arrow(img, (560, 690), (790, 560))
img.convert("RGB").save("thumbnail-3-highway.jpg", quality=92); out.append("thumbnail-3-highway.jpg")

sheet = Image.new("RGB", (1280, 720), (20, 20, 20))
for i, f in enumerate(out):
    t = Image.open(f).resize((640, 360))
    ImageDraw.Draw(t).rounded_rectangle([12, 300, 70, 350], 12, fill=(255, 214, 10))
    ImageDraw.Draw(t).text((41, 325), str(i + 1), font=ImageFont.truetype(INTER, 40), fill=(0, 0, 0), anchor="mm")
    sheet.paste(t, ((i % 2) * 640, (i // 2) * 360))
sheet.save("thumbs-sheet.jpg", quality=88)
print("ok")
