"""NoliDrop ad 3 - UGC "Before you go to the pool store...". Creator selfie jump cuts, POV phone-in-hand with the real
app screens keyed into a green screen, Noli as a sticker, TikTok-style word captions. A demo, not a testimonial.
python3 ad3.py [--plan | --stills | --frame t1,t2]"""
import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import adkit as K
from fonts import emoji_image

SUN = (255, 214, 10)


@lru_cache(maxsize=16)
def sticker(path, border=18):
    """Sprite with a white sticker outline and a soft shadow."""
    a = K.sprite_np(path)
    pad = border * 2
    a = np.pad(a, ((pad, pad), (pad, pad), (0, 0)))
    al = a[..., 3]
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border * 2 + 1, border * 2 + 1))
    out_a = cv2.dilate(al, k)
    out_a = cv2.GaussianBlur(out_a, (5, 5), 0)
    rgb = np.full(a.shape[:2] + (3,), 255, np.uint8)
    m = al[..., None].astype(np.float32) / 255
    rgb = (rgb * (1 - m) + a[..., :3] * m).astype(np.uint8)
    return np.dstack([rgb, out_a])


@lru_cache(maxsize=16)
def emoji(ch, size):
    return np.asarray(emoji_image(ch, size).convert("RGBA"))


@lru_cache(maxsize=16)
def pill(text, size=58, bg=(255, 255, 255), fg=(20, 20, 25)):
    f = ImageFont.truetype(K.INTER_BLACK, size)
    w = int(f.getlength(text)) + size
    h = int(size * 1.55)
    im = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 12, w + 8, h + 12), 22, fill=(0, 0, 0, 70))
    d.rounded_rectangle((8, 6, w + 8, h + 6), 22, fill=(*bg, 255))
    d.text((8 + size / 2, 6 + size * 0.2), text, font=f, fill=(*fg, 255))
    return np.asarray(im)


@lru_cache(maxsize=4)
def num_badge(n):
    """'Step 1 / 2' sticker: white-outlined cyan circle with the number."""
    s = 200
    im = Image.new("RGBA", (s + 20, s + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((10, 22, s + 10, s + 22), fill=(0, 0, 0, 60))
    d.ellipse((10, 10, s + 10, s + 10), fill=(255, 255, 255, 255))
    d.ellipse((24, 24, s - 4, s - 4), fill=(0, 170, 235, 255))
    f = ImageFont.truetype(K.INTER_BLACK, 120)
    d.text((10 + s / 2 - f.getlength(n) / 2, 22), n, font=f, fill=(255, 255, 255, 255))
    return np.asarray(im)


@lru_cache(maxsize=1)
def lock_screen():
    im = Image.new("RGB", (K.SW, K.SH))
    g = K.gradient((20, 40, 90), (0, 140, 200))
    im = Image.fromarray(cv2.resize(g.astype(np.uint8), (K.SW, K.SH)))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(K.INTER_SB, 190)
    d.text((K.SW / 2 - f.getlength("9:41") / 2, 260), "9:41", font=f, fill=(255, 255, 255))
    return im


@lru_cache(maxsize=48)
def pov(path, ui, k=None):
    screen = {"lock": lock_screen, "home": K.ui_home, "values": lambda: K.ui_values(k)}[ui]()
    return K.keyed_screen(path, screen)


def handheld(t, amt=1.0):
    return amt


def selfie(t, d, path, z0, z1, fx=0.5, fy=0.4):
    fr = K.cover_np(K.load_np(path), t, d, z0, z1, fx, fy, rot=0.8 * math.sin(t * 2.3), shake=1.6).astype(np.float32)
    return fr


def scribble(fr, cx, cy, rx, ry, k, color=(255, 50, 50), width=12):
    """Hand-drawn circle that draws itself (k 0..1)."""
    if k <= 0:
        return
    n = int(60 * K.clamp(k)) + 2
    pts = []
    for i in range(n):
        a = -math.pi * 0.6 + i / 60 * math.pi * 2.15
        wob = 1 + 0.04 * math.sin(i * 0.7)
        pts.append((cx + rx * wob * math.cos(a), cy + ry * wob * math.sin(a)))
    cv2.polylines(fr, [np.array(pts, np.int32)], False, color, width, cv2.LINE_AA)


# ------------------------------------------------------------------ scenes
def s_hook(t, d, a, ctx):
    return selfie(t, d, "img/u-hook.jpg", 1.08, 1.16, 0.45, 0.4)


def s_hook2(t, d, a, ctx):
    fr = selfie(t, d, "img/u-hook.jpg", 1.55, 1.62, 0.38, 0.3)
    p = (t - 0.15) / 0.25
    if p > 0:
        K.paste(fr, emoji("✋", 170), K.W * 0.8, 420, K.ease_back(p, 2.5), rot=-10)
    return fr


def s_cloudy(t, d, a, ctx):
    im = pov("img/pov-cloudy.jpg", "lock")
    fr = K.cover_np(im, t, d, 1.0, 1.1, 0.5, 0.5, shake=1.4).astype(np.float32)
    for i, (txt, x, y) in enumerate([("green?", 0.24, 0.22), ("cloudy?", 0.72, 0.62)]):
        p = (t - 0.1 - i * 0.3) / 0.25
        if p > 0:
            K.paste(fr, pill(txt, 64, (110, 200, 60) if i == 0 else (225, 228, 235)), x * K.W, y * K.H, K.ease_back(p, 2.4),
                    rot=(-1) ** i * 6)
    return fr


def s_open(t, d, a, ctx):
    im = pov("img/pov-cloudy.jpg", "home")
    fr = K.cover_np(im, t, d, 1.08, 1.2, 0.55, 0.45, shake=1.2).astype(np.float32)
    return fr


def s_noli(t, d, a, ctx):
    """UGC take on the Drop: Noli drops onto the phone screen with a splash, then waves as a sticker."""
    im = pov("img/pov-cloudy.jpg", "home")
    fr = K.cover_np(im, t, d, 1.2, 1.24, 0.55, 0.45, shake=1.0).astype(np.float32)
    hit = 0.25
    cx, cy = K.W * 0.53, K.H * 0.52
    if t < hit:
        K.paste(fr, sticker("sprites/n-dive.png"), cx, -200 + (cy - 100 + 200) * (t / hit) ** 1.5, 0.5)
    else:
        tt = t - hit
        K.ring(fr, cx, cy + 200, tt * 900, 8, alpha=max(0, 0.7 - tt * 1.2), sy=0.5)
        K.splash_drops(fr, tt, cx, cy + 180, 16, power=0.8)
        K.paste(fr, sticker("sprites/n-wave.png"), cx, cy + 260, 0.62 * K.spring(tt / 0.4), anchor="b", rot=-4 + 3 * math.sin(t * 5))
    return fr


def s_type(t, d, a, ctx):
    k = round(K.clamp(t / (d * 0.9)) * 20) / 20
    im = pov("img/pov-deck.jpg", "values", k)
    fr = K.cover_np(im, t, d, 1.25, 1.33, 0.6, 0.45, shake=1.0).astype(np.float32)
    return fr


def s_whats_off(t, d, a, ctx):
    sc = K.ui_results(K.clamp(0.4 + t / d * 0.25))
    fr = K.screen_zoom(sc, K.SW / 2, 640, 1.0 + 0.05 * t).astype(np.float32)
    # screen-recording look: red scribble round the two values
    cy = (605 - 640) * K.W / K.SW * (1.0 + 0.05 * t) + K.H / 2
    scribble(fr, K.W / 2, cy, 470, 140, (t - 0.2) / 0.45)
    return fr


def s_fix_first(t, d, a, ctx):
    sc = K.ui_results(1.0)
    z = 1.05
    fr = K.screen_zoom(sc, K.SW / 2, 1000, z).astype(np.float32)
    s = max(K.W / K.SW, K.H / K.SH) * z
    cx, cy = (382 - K.SW / 2) * s + K.W / 2, (800 - 1000) * s + K.H / 2
    scribble(fr, cx, cy, 500, 130, (t - 0.1) / 0.4, (255, 190, 0), 13)
    p = (t - 0.35) / 0.25
    if p > 0:
        K.paste(fr, emoji("👆", 150), K.W * 0.78, cy + 190, K.ease_back(p, 2.5), rot=-15)
    return fr


def s_steps(t, d, a, ctx):
    fr = selfie(t, d, "img/u-talk.jpg", 1.25, 1.3, 0.45, 0.35)
    for i in range(2):
        p = (t - 0.05 - i * 0.58) / 0.22
        if p > 0:
            K.paste(fr, num_badge(str(i + 1)), K.W * (0.2 + i * 0.24), 470, K.ease_back(p, 2.6), rot=(-1) ** i * 8)
    return fr


def s_knows(t, d, a, ctx):
    fr = selfie(t, d, "img/u-wink2.jpg", 1.12, 1.2, 0.45, 0.38)
    p = (t - 0.55) / 0.35
    if p > 0:
        K.paste(fr, sticker("sprites/noli-thumbsup.png"), K.W * 0.76, K.H * 0.74, 0.45 * K.spring(p), rot=8 + 3 * math.sin(t * 6), anchor="b")
    return fr


def end_card(t, d, a, ctx):
    """UGC variant: bright pool, big phone with the Home screen, Noli sticker, wordmark and Play badge."""
    fr = K.cover("img/bg-pool-sunny.jpg", t, d, 1.15, 1.2, 0.5, 0.7).astype(np.float32)
    fr = K.blur(fr, 10)
    fr = fr * 0.8 + 255 * 0.2
    q = (t - 0.0) / 0.4
    K.put_phone(fr, K.ui_home(), K.W / 2, K.H * 0.62 + (1 - K.ease_out(q)) * 900, 0.6, rot=-3, tilt=0.2, shadow=0.6)
    p = (t - 0.15) / 0.4
    if p > 0:
        K.paste(fr, K.wordmark(150), K.W / 2, 250, K.ease_back(p, 2.2))
    p = (t - 0.4) / 0.35
    if p > 0:
        K.paste(fr, K.play_badge(560), K.W / 2, 450, K.ease_back(p, 2.2))
    p = (t - 0.3) / 0.4
    if p > 0:
        K.paste(fr, sticker("sprites/n-point.png"), K.W * 0.2, K.H * 0.95, 0.5 * K.spring(p), flip=True, anchor="b", rot=6)
    return fr


def post(fr, t, n):
    fr = fr * np.array([1.03, 1.0, 0.96], np.float32) + 3   # warm phone-camera look
    return K.grain(fr, n, 5)


cap = K.make_captions(K.INTER_BLACK, 82, 1330, color=K.WHITE, key=K.WHITE, stroke=9, stroke_color=(0, 0, 0), shadow=0, max_words=3,
                      mode="build", box=(0, 170, 235))
J = {"name": "swoosh-fast", "at": 0.0, "gain": 0.35}   # soft jump-cut whoosh
shots = [
    dict(w=0, scene=s_hook, sfx=[{"name": "pop", "at": 0.02}]),
    dict(w=3, scene=s_hook2, sfx=[J, {"name": "pop", "at": 0.15}]),
    dict(w=10, scene=s_cloudy, tr="whip", sfx=[{"name": "ui-pop", "at": 0.1}, {"name": "ui-pop", "at": 0.4}]),
    dict(w=14, scene=s_open, sfx=[J, {"name": "tap", "at": 0.25}]),
    dict(w=18, scene=s_noli, sfx=[J, {"name": "cartoon-splash", "at": 0.25, "gain": 0.8}, {"name": "bloop", "at": 0.3},
                                  {"name": "sparkle", "at": 0.55}]),
    dict(w=21, scene=s_type, tr="whip", sfx=[{"name": "tap", "at": 0.2 + 0.14 * i} for i in range(6)]),
    dict(w=27, scene=s_whats_off, tr="zoom", cap_y=1700, sfx=[{"name": "select", "at": 0.25}]),
    dict(w=33, scene=s_fix_first, cap_y=1700, sfx=[J, {"name": "pop", "at": 0.35}, {"name": "ding", "at": 0.15, "gain": 0.6}]),
    dict(w=38, scene=s_steps, tr="whip", sfx=[{"name": "pop", "at": 0.05}, {"name": "pop", "at": 0.63}]),
    dict(w=42, scene=s_knows, sfx=[J, {"name": "bloop", "at": 0.6}, {"name": "sparkle", "at": 0.8}]),
    dict(w=46, scene=end_card, tr="slide", cap_y=1760, dur=3.0, sfx=[{"name": "pop", "at": 0.2}, {"name": "ding", "at": 0.45}]),
]

if __name__ == "__main__":
    spec = dict(name="nolidrop-ad-3", voice="ad3/voice-1.wav", max_gap=0.26, shots=shots, caption=cap, post=post,
                fixes={"Noly": "Noli", "Noly.": "Noli.", "1.": "one.", "2.": "two."},
                music=[{"t": 0.0, "file": "music/sounds-good.mp3", "start": 0.09, "vol": 1.0}], music_volume=0.3, duck=0.45)
    voice, words = K.prepare_voice(spec["voice"], K.HERE / "work" / spec["name"], spec["max_gap"], 1.0, spec["fixes"])
    shots[-1]["dur"] = words[-1][2] + 1.9 - (words[46][1] - 0.06)
    K.render(spec)
