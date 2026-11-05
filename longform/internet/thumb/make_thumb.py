"""Thumbnails for 'What if the internet shut down worldwide for a week?' (1280x720, no people).
Usage: python3 make_thumb.py -> thumbnail-1-phone.jpg, thumbnail-2-unplugged.jpg, thumbnail-3-toilet-paper.jpg, thumbs-sheet.jpg"""
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
# 1. Cracked red phone over a city, text on the right.
img = vignette(pop(cover("art-a.jpg", 0.62, 0.5, 1.05)), 0.3)
text(img, (690, 70), "NO", ANTON, 170, WHITE, stroke=10)
text(img, (690, 250), "INTERNET", ANTON, 170, YEL, stroke=10, glow=(255, 150, 0))
tag(img, (700, 500), "FOR 7 DAYS", 70, (255, 255, 255), (220, 30, 30), rot=-3)
img.convert("RGB").save("thumbnail-1-phone.jpg", quality=92); out.append("thumbnail-1-phone.jpg")

# 2. Earth unplugged, question on top.
img = vignette(pop(cover("art-b.jpg", 0.5, 0.5, 1.1)), 0.3)
text(img, (W // 2, 80), "WHO UNPLUGGED", ANTON, 120, WHITE, anchor="mm", stroke=9)
text(img, (W // 2, 205), "THE INTERNET?", ANTON, 120, YEL, anchor="mm", stroke=9, glow=(255, 150, 0))
tag(img, (W // 2 - 220, 590), "7 DAYS OFFLINE", 56, (20, 20, 20), (255, 214, 10), rot=-2)
img.convert("RGB").save("thumbnail-2-unplugged.jpg", quality=92); out.append("thumbnail-2-unplugged.jpg")

# 3. Last toilet roll on an empty shelf: "DAY 2 WITHOUT INTERNET" + red arrow.
img = vignette(pop(cover("art-c.jpg", 0.0, 0.55, 1.45), 1.15, 1.1), 0.25)
text(img, (40, 40), "DAY 2", ANTON, 210, YEL, stroke=10, glow=(255, 150, 0))
text(img, (40, 290), "WITHOUT", ANTON, 120, WHITE, stroke=9)
text(img, (40, 430), "INTERNET", ANTON, 120, WHITE, stroke=9)
arrow(img, (560, 650), (760, 520))
img.convert("RGB").save("thumbnail-3-toilet-paper.jpg", quality=92); out.append("thumbnail-3-toilet-paper.jpg")

sheet = Image.new("RGB", (1280, 720), (20, 20, 20))
for i, f in enumerate(out):
    t = Image.open(f).resize((640, 360))
    ImageDraw.Draw(t).rounded_rectangle([12, 300, 70, 350], 12, fill=(255, 214, 10))
    ImageDraw.Draw(t).text((41, 325), str(i + 1), font=ImageFont.truetype(INTER, 40), fill=(0, 0, 0), anchor="mm")
    sheet.paste(t, ((i % 2) * 640, (i // 2) * 360))
sheet.save("thumbs-sheet.jpg", quality=88)
print("ok")
