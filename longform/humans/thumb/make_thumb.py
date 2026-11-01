"""Thumbnails for 'What if all humans disappeared tomorrow?' (1280x720, no people).
Usage: python3 make_thumb.py -> thumbnail-1-deer.jpg, thumbnail-2-liberty.jpg, thumbnail-3-split.jpg, thumbs-sheet.jpg"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../moon/thumb/options"))
os.chdir(os.path.join(HERE, "../../moon/thumb/options"))
from make_options import W, H, INTER, cover, text, vignette  # noqa: E402
os.chdir(HERE)
ANTON = os.path.join(HERE, "../../fonts/Anton-Regular.ttf")


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
# 1. Deer in jungle Times Square, centred title at the top.
img = vignette(pop(cover("art-b.jpg", 0.5, 0.35, 1.08)), 0.35)
text(img, (W // 2, 95), "0 HUMANS LEFT", ANTON, 130, (255, 255, 255, 255), anchor="mm", stroke=9)
tag(img, (W // 2 - 190, 560), "100 YEARS LATER", 52, (20, 20, 20), (255, 214, 10), rot=-2)
img.convert("RGB").save("thumbnail-1-deer.jpg", quality=92); out.append("thumbnail-1-deer.jpg")

# 2. Overgrown giant statue, text on the left.
img = vignette(pop(cover("art-c.jpg", 0.9, 0.2, 1.12)), 0.3)
text(img, (40, 60), "EARTH", ANTON, 150, (255, 255, 255, 255), stroke=9)
text(img, (40, 230), "WITHOUT", ANTON, 150, (255, 255, 255, 255), stroke=9)
text(img, (40, 400), "US", ANTON, 190, (255, 214, 10, 255), stroke=9, glow=(255, 150, 0))
img.convert("RGB").save("thumbnail-2-liberty.jpg", quality=92); out.append("thumbnail-2-liberty.jpg")

# 3. Split: city today | the same city as jungle.
L = pop(cover("art-a.jpg", 0.0, 0.3, 1.1))
R = pop(cover("art-b.jpg", 0.5, 0.35, 1.08))
img = L.copy()
img.paste(R.crop((W // 2 - 300, 0, W - 300, H)), (W // 2, 0))
d = ImageDraw.Draw(img)
d.rectangle([W // 2 - 4, 0, W // 2 + 4, H], fill=(255, 255, 255, 255))
for x, lab, bg, fg in ((W // 4, "TODAY", (255, 255, 255), (20, 20, 20)), (3 * W // 4, "WITHOUT US", (255, 214, 10), (20, 20, 20))):
    f = ImageFont.truetype(INTER, 60); b = f.getbbox(lab)
    w = b[2] - b[0] + 60
    tag(img, (x - w // 2, 590), lab, 60, fg, bg)
text(img, (W // 2, 90), "WHAT IF WE ALL VANISHED?", ANTON, 100, (255, 255, 255, 255), anchor="mm", stroke=9)
img.convert("RGB").save("thumbnail-3-split.jpg", quality=92); out.append("thumbnail-3-split.jpg")

sheet = Image.new("RGB", (1280, 720), (20, 20, 20))
for i, f in enumerate(out):
    t = Image.open(f).resize((640, 360))
    ImageDraw.Draw(t).rounded_rectangle([12, 300, 70, 350], 12, fill=(255, 214, 10))
    ImageDraw.Draw(t).text((41, 325), str(i + 1), font=ImageFont.truetype(INTER, 40), fill=(0, 0, 0), anchor="mm")
    sheet.paste(t, ((i % 2) * 640, (i // 2) * 360))
sheet.save("thumbs-sheet.jpg", quality=88)
print("ok")
