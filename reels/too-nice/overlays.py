"""Graphics for "Being Too Nice Isn't Your Problem": title card + red slash, speech bubbles, fading man, KIND + DECISIVE."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from overlay_kit import RED, bubble, fade_man, glow, layer, text

img = Path(__file__).resolve().parent / "img"
op = lambda n: Image.open(img / n).convert("RGB")

# Title card over the moonlit sea, then the same card slashed in red.
card = op("x00-sea.jpg")
L = layer(card); text(ImageDraw.Draw(L), (576, 560), "NICE GUYS\nFINISH LAST", 150)
card = glow(card, L); card.save(img / "x00-card.jpg", quality=95)
L = layer(card); ImageDraw.Draw(L).line([(90, 760), (1060, 330)], fill=(255, 255, 255, 255), width=26)
glow(card, L, RED, sharp=(255, 90, 90)).save(img / "x00-card-slash.jpg", quality=95)

bubble(op("s04-ask.jpg"), (330, 290, 1110, 560), "Where do you\nwant to eat?", (760, 760), 66).save(img / "s04-ask-b.jpg", quality=95)
bubble(op("s05-shrug.jpg"), (90, 230, 1060, 520), "Anything's fine,\nwhatever you want.", (560, 700), 62).save(img / "s05-shrug-b.jpg", quality=95)
fade_man(op("s07-awkward.jpg"), op("s07-noman.jpg")).save(img / "s07-faded.jpg", quality=95)

tac = op("s10-tacos.jpg")
L = layer(tac); text(ImageDraw.Draw(L), (576, 420), "KIND + DECISIVE", 110)
glow(tac, L).save(img / "s10-tacos-t.jpg", quality=95)
