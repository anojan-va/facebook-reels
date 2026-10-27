"""Storyboard sheet for ad 3 (AI video UGC): keyframes with the app UI keyed in, VO, timing and the motion prompt."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import adkit as K
from ad3_motion import sticker

PANELS = [
    ("1", "0.0–2.4 s", "K1", None, "“Okay pool owners, don't go to the pool store yet.”", "Handheld selfie, she talks to camera, points down at the green pool; jump-cut punch-in on 'yet'."),
    ("2", "2.4–3.6 s", "K2", None, "“Green or cloudy water?”", "Hand dips the test strip into the green water, slow push-in, ripples."),
    ("3", "3.6–5.0 s", "K3", "home", "“Open NoliDrop first.”", "POV: phone held over the pool, slight sway. Real Home screen keyed onto the green screen."),
    ("4", "5.0–6.1 s", "K3", "home+noli", "“This is Noli.”", "Same clip: Noli drops onto the phone with a splash and waves (sticker + splash in the edit)."),
    ("5", "6.1–8.5 s", "K5", "values", "“You type in your water values, and it tells you what's off…”", "Over-the-shoulder: thumb taps the phone; values typed in, then a screen-recording insert of the results."),
    ("6", "8.5–9.9 s", None, "results", "“…and what to fix first.”", "Screen insert (motion graphics): PRIORITY #1 circled by a hand-drawn scribble."),
    ("7", "9.9–11.2 s", "K6", None, "“Step one, step two.”", "Selfie: she counts one, then two fingers while talking; number stickers pop."),
    ("8", "11.2–12.5 s", "K7", "home", "“Don't guess. Noli knows.”", "Selfie in front of the clear blue pool, phone by her cheek, knowing smile; Noli sticker pops in."),
    ("9", "12.5–16.0 s", None, "end", "“NoliDrop, it's on Google Play.”", "Brand end card (logo, Play badge, Noli + Home screen)."),
]
PW, PH = 405, 720
f_b = ImageFont.truetype(K.INTER_BLACK, 30)
f_m = ImageFont.truetype(K.INTER_SB, 22)
f_s = ImageFont.truetype(K.INTER_M, 19)


def wrap(d, text, font, width):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=font) > width:
            out.append(line)
            line = w
        else:
            line = t
    return out + [line]


def panel_img(key, ui):
    if key is None and ui == "results":
        sc = K.ui_results(1.0, focus_priority=True)
        return Image.fromarray(K.screen_zoom(sc, K.SW / 2, 1000, 1.05).astype(np.uint8))
    if key is None and ui == "end":
        import ad3_motion as ad3
        return Image.fromarray(np.clip(ad3.end_card(2.0, 3.0, {}, {}), 0, 255).astype(np.uint8))
    path = f"storyboard/{key}.jpg"
    if ui:
        screen = {"home": K.ui_home(), "home+noli": K.ui_home(), "values": K.ui_values(0.7)}[ui]
        im = K.keyed_screen(path, screen)
        if ui == "home+noli":
            q, _ = K.green_quad(path)
            fr = im.astype(np.float32)
            cx, cy = q[:, 0].mean(), q[:, 1].mean()
            K.paste(fr, sticker("sprites/n-wave.png"), cx, cy + (q[2, 1] - q[1, 1]) * 0.35, 0.45 * im.shape[0] / 1920, anchor="b")
            im = fr.astype(np.uint8)
        return Image.fromarray(im)
    return Image.open(path).convert("RGB")


cols = len(PANELS)
S = Image.new("RGB", (cols * (PW + 20) + 20, PH + 430 + 90), (245, 247, 250))
d = ImageDraw.Draw(S)
d.text((20, 20), "NoliDrop: Ad 3 (UGC, AI video) storyboard. Keyframes: Nano Banana Pro. App UI, Noli and captions are added in the edit.",
       font=f_b, fill=(12, 42, 110))
for i, (n, t, key, ui, vo, motion) in enumerate(PANELS):
    x = 20 + i * (PW + 20)
    im = panel_img(key, ui)
    im = im.resize((PW, int(im.height * PW / im.width)))
    im = im.crop((0, (im.height - PH) // 2, PW, (im.height - PH) // 2 + PH))
    S.paste(im, (x, 80))
    d.rounded_rectangle((x + 10, 90, x + 120, 130), 12, fill=(0, 170, 235))
    d.text((x + 22, 94), f"#{n}", font=f_b, fill=(255, 255, 255))
    d.text((x + 132, 98), t, font=f_m, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    y = 80 + PH + 14
    for ln in wrap(d, vo, f_m, PW):
        d.text((x, y), ln, font=f_m, fill=(20, 20, 30))
        y += 28
    y += 8
    tag = "VIDEO (image-to-video)" if key else "MOTION GRAPHICS"
    d.text((x, y), tag, font=f_s, fill=(0, 140, 200) if key else (220, 110, 10))
    y += 26
    for ln in wrap(d, motion, f_s, PW):
        d.text((x, y), ln, font=f_s, fill=(70, 75, 90))
        y += 25
S.save("storyboard/storyboard.jpg", quality=88)
print(S.size)
