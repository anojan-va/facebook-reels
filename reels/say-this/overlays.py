"""Graphics for "Never Say 'You're Beautiful' Like This": stacked bubbles (then greyed), Ctrl+C/V keys,
bracelet/book highlights, laugh sound-wave, "Wanna go up?", crowd blur."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from overlay_kit import GREY, bubble, focus_blur, glow, layer, text

img = Path(__file__).resolve().parent / "img"
op = lambda n: Image.open(img / n).convert("RGB")

# Pile of identical compliments beside her (right side, above the caption band); grey version = brain ignores them.
for name, line, col in (("s02-yawn-b.jpg", (255, 255, 255), (255, 220, 60)), ("s02-yawn-grey.jpg", GREY, (40, 40, 40))):
    im = op("s02-yawn.jpg")
    for k, (x, y) in enumerate([(640, 820), (600, 660), (660, 500), (590, 340), (650, 180)]):
        im = bubble(im, (x, y, x + 470, y + 130), "you're beautiful", (x + 20, y + 190), 46, line=line, txt=line, color=col)
    im.save(img / name, quality=95)

keys = op("x01-keys.jpg")
up = Image.new("RGB", keys.size, "black"); up.paste(keys.crop((0, 260, 1152, 2048)), (0, 0))
L = layer(up); d = ImageDraw.Draw(L)
text(d, (330, 600), "Ctrl\n+C", 110); text(d, (810, 590), "Ctrl\n+V", 110)
glow(up, L).save(img / "x01-keys-t.jpg", quality=95)

for src, out, box in (("s05-bracelet.jpg", "s05-bracelet-h.jpg", (350, 1150, 740, 1320)),
                      ("s06-book.jpg", "s06-book-h.jpg", (300, 720, 840, 1120))):
    im = op(src); L = layer(im)
    ImageDraw.Draw(L).ellipse(box, outline=(255, 255, 255, 255), width=10)
    glow(im, L).save(img / out, quality=95)

# Laugh sound-wave icon above-left of her head.
im = op("s07-laugh.jpg"); L = layer(im); d = ImageDraw.Draw(L)
for k, h in enumerate([40, 90, 150, 110, 180, 90, 130, 60, 30]):
    x = 90 + k * 34
    d.rounded_rectangle([x, 640 - h // 2, x + 16, 640 + h // 2], radius=8, fill=(255, 255, 255, 255))
glow(im, L).save(img / "s07-laugh-w.jpg", quality=95)

bubble(op("s10-wheel-point.jpg"), (60, 330, 620, 540), "Wanna go up?", (480, 720), 66).save(img / "s10-wheel-b.jpg", quality=95)
focus_blur(op("s09-crowd.jpg"), (250, 650, 1000, 1900)).save(img / "s09-crowd-blur.jpg", quality=95)
