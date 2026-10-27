"""NoliDrop ad 1 - "The Receipt" (problem -> solution). Sunny brand look: cyan/white, Fredoka, splash transitions.
python3 ad1.py [--plan | --stills]"""
import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from adkit import *  # noqa: F401,F403
import adkit as K

RECEIPT = [("SHOCK CHLORINE", "$24.90"), ("PH INCREASER", "$18.50"), ("ALGAECIDE", "$22.90"), ("FLOCCULANT", "$16.90"),
           ("STABILIZER", "$14.50"), ("CLEANER", "$19.90"), ("MISC.", "$6.20")]
STRIKE = [2, 3, 5]   # lines crossed out in the payoff (illustrative: products bought on a guess)


# ------------------------------------------------------------------ assets
@lru_cache(maxsize=32)
def receipt_im(n_lines=7, total=True, stamp=0.0, strikes=0):
    """The brand's receipt (from their Instagram post). n_lines printed, stamp 0..1 scale-in, strikes = lines crossed."""
    w, lh = 760, 74
    h = 300 + lh * 7 + 260
    im = Image.new("RGBA", (w, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    teeth = [(x, h + (18 if (x // 20) % 2 else 0)) for x in range(0, w + 1, 20)]
    d.polygon([(0, 0), (w, 0), *teeth[::-1]][:2] + teeth[::-1], fill=(252, 251, 246, 255))
    fm = ImageFont.truetype(K.MONO, 40)
    fb = ImageFont.truetype(K.MONO, 54)
    fs = ImageFont.truetype(K.MONO, 30)
    d.text((w / 2 - fb.getlength("POOL PRODUCTS") / 2, 70), "POOL PRODUCTS", font=fb, fill=(30, 30, 35))
    d.text((w / 2 - fs.getlength("*** RECEIPT ***") / 2, 150), "*** RECEIPT ***", font=fs, fill=(120, 120, 125))
    y = 230
    for i, (name, price) in enumerate(RECEIPT[:n_lines]):
        d.text((60, y), name, font=fm, fill=(40, 40, 45))
        d.text((w - 60 - fm.getlength(price), y), price, font=fm, fill=(40, 40, 45))
        if i in STRIKE[:strikes]:
            d.line((48, y + 26, w - 48, y + 22), fill=(*K.RED, 255), width=9)
        y += lh
    y = 230 + lh * 7 + 10
    d.line((50, y, w - 50, y), fill=(160, 160, 160), width=3)
    if total:
        d.text((60, y + 40), "TOTAL", font=fb, fill=(20, 20, 25))
        d.text((w - 60 - fb.getlength("$124.80"), y + 40), "$124.80", font=fb, fill=(20, 20, 25))
    a = np.asarray(im).copy()
    if stamp > 0:
        st = Image.new("RGBA", (520, 190), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((8, 8, 512, 182), 24, outline=(*K.RED, 235), width=12)
        f = ImageFont.truetype(K.FREDOKA, 104)
        sd.text((260 - f.getlength("$124.80") / 2, 30), "$124.80", font=f, fill=(*K.RED, 235))
        st = st.rotate(-12, expand=True, resample=Image.BICUBIC)
        s = 1 + (1 - K.ease_out(stamp)) * 1.6
        st = st.resize((int(st.width * s), int(st.height * s)), Image.LANCZOS)
        al = np.asarray(st).astype(np.float32)
        al[..., 3] *= K.clamp(stamp * 2)
        ph, pw = al.shape[:2]
        cx, cy = w // 2, int(h * 0.62)
        x0, y0 = cx - pw // 2, cy - ph // 2
        xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + pw, w), min(y0 + ph, a.shape[0])
        sub = al[ya - y0:yb - y0, xa - x0:xb - x0]
        reg = a[ya:yb, xa:xb].astype(np.float32)
        m = sub[..., 3:4] / 255
        reg[..., :3] = reg[..., :3] * (1 - m) + sub[..., :3] * m
        reg[..., 3:4] = np.maximum(reg[..., 3:4], sub[..., 3:4])
        a[ya:yb, xa:xb] = reg.astype(np.uint8)
    return a


@lru_cache(maxsize=1)
def blue_pool():
    return K.load_np("img/bg-pool-blue.jpg")


def _blue_pool_recolor():
    """The green pool, cleaned: algae hue shifted to turquoise, brighter, debris toned down."""
    im = np.asarray(K.load("img/bg-pool-green.jpg")).copy()
    hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    water = (h > 22) & (h < 85) & (s > 50)
    yy, xx = np.mgrid[:im.shape[0], :im.shape[1]]
    hsv[..., 0] = np.where(water, 92, h)
    hsv[..., 1] = np.where(water, np.clip(s * 0.85 + 40, 0, 255), s)
    # flatten the algae blotches: blend the value toward a smooth caustic pattern
    smooth = cv2.GaussianBlur(v, (0, 0), 25)
    caus = 18 * np.sin(xx * 0.05 + np.sin(yy * 0.03) * 2) * np.sin(yy * 0.045 + np.cos(xx * 0.02) * 2)
    hsv[..., 2] = np.where(water, np.clip(smooth * 0.55 + 120 + caus, 0, 255), v)
    out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    m = cv2.GaussianBlur(water.astype(np.float32), (0, 0), 3)[..., None]
    return (out * m + im * (1 - m)).astype(np.uint8)


def pool_frame(t, d, blue_r=None, z0=1.05, z1=1.18, cx=0.5, cy=0.5):
    """Top-down pool; inside radius blue_r (frame px) around the centre the water is clear blue."""
    g = K.cover("img/bg-pool-green.jpg", t, d, z0, z1, 0.5, 0.5).astype(np.float32)
    g = K.water_warp(g, t, amp=4)
    if blue_r is None or blue_r <= 0:
        return g
    b = K.cover_np(blue_pool(), t, d, z0, z1, 0.5, 0.5).astype(np.float32)
    b = K.water_warp(b, t + 1, amp=5)
    y, x = np.ogrid[:K.H, :K.W]
    dd = np.sqrt((x - K.W * cx) ** 2 + (y - K.H * cy) ** 2)
    m = np.clip((blue_r - dd) / 40, 0, 1).astype(np.float32)[..., None]
    return g * (1 - m) + b * m


def chip(text, size=56, bg=(255, 255, 255), fg=K.NAVY):
    f = ImageFont.truetype(K.FREDOKA, size)
    w = int(f.getlength(text)) + size
    h = int(size * 1.6)
    im = Image.new("RGBA", (w + 20, h + 26), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 14, w + 10, h + 14), h // 2, fill=(0, 30, 80, 60))
    d.rounded_rectangle((10, 6, w + 10, h + 6), h // 2, fill=(*bg, 255))
    d.text((10 + size / 2, 6 + size * 0.22), text, font=f, fill=(*fg, 255))
    return np.asarray(im)


chip = lru_cache(maxsize=64)(chip)


@lru_cache(maxsize=16)
def price_tag(text):
    f = ImageFont.truetype(K.FREDOKA, 64)
    w = int(f.getlength(text)) + 90
    im = Image.new("RGBA", (w + 20, 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(10, 65), (50, 15), (w, 15), (w, 115), (50, 115)], fill=(255, 214, 40, 255))
    d.ellipse((34, 56, 52, 74), fill=(255, 255, 255, 255))
    d.text((66, 26), text, font=f, fill=(30, 30, 35, 255))
    return np.asarray(im)


def sunny_bg(t, d, blur=14, z0=1.12, z1=1.2):
    fr = K.cover("img/bg-pool-sunny.jpg", t, d, z0, z1, 0.5, 0.62)
    return K.blur(fr, blur).astype(np.float32)


# ------------------------------------------------------------------ scenes
def s_receipt_hook(t, d, a, ctx):
    fr = K.cover("img/bg-tubs.jpg", t, d, 1.25, 1.35, 0.5, 0.6)
    fr = K.grade(K.blur(fr, 10), 0.9, 1.0, -30)
    n = min(7, int(t / 0.085) + 1)
    stamp = K.clamp((t - 0.72) / 0.16)
    rc = receipt_im(n, n >= 7, round(stamp, 2))
    k = K.ease_out(t / 0.5)
    scale = 1.05 + 0.18 * K.ease_io(t / d)
    shake = 10 * math.exp(-max(t - 0.78, 0) * 9) if t > 0.78 else 0
    K.paste(fr, rc, K.W / 2 + shake * math.sin(t * 90), 380 + (1 - k) * -700 + 520, scale, -4 + 4 * k, shadow=0.7)
    return fr


def s_still_green(t, d, a, ctx):
    fr = pool_frame(t, d, None, 1.0, 1.35)
    fr = K.grade(fr, 1.15, 1.08, -6)
    K.headline(fr, [[("Still", False), ("green?", True)]], K.W / 2, 560, 170, K.FREDOKA, t, 0.25, 0.12, key=(120, 230, 70),
               stroke=12, stroke_color=K.NAVY)
    return K.vignette(fr, 0.35)


def s_guess(t, d, a, ctx):
    fr = K.cover("img/bg-tubs.jpg", t, d, 1.05, 1.15, 0.45, 0.62).astype(np.float32)
    for i, (txt, x, y) in enumerate([("pH?", 0.27, 0.30), ("Chlorine?", 0.66, 0.24), ("Shock?", 0.73, 0.40), ("Algaecide?", 0.32, 0.45)]):
        p = (t - 0.1 - i * 0.16) / 0.3
        if p > 0:
            K.paste(fr, chip(txt, 60), x * K.W, y * K.H + math.sin(t * 3 + i) * 8, K.ease_back(p, 2.4), rot=(-1) ** i * 4)
    return fr


def s_buy(t, d, a, ctx):
    fr = K.cover("img/bg-tubs.jpg", t, d, 1.35, 1.6, 0.5, 0.72, shake=0.6).astype(np.float32)
    for i, (txt, x, y, r) in enumerate([("$24.90", 0.3, 0.30, -8), ("$22.90", 0.7, 0.26, 7), ("$16.90", 0.62, 0.43, -5),
                                        ("$19.90", 0.28, 0.48, 6), ("$14.50", 0.5, 0.18, -3)]):
        p = (t - i * 0.11) / 0.25
        if p > 0:
            K.paste(fr, price_tag(txt), x * K.W, y * K.H, K.ease_back(p, 2.6) * 1.15, rot=r)
    return fr


def s_drop(t, d, a, ctx):
    """The signature Drop: Noli falls into the green pool, splash, the ripple clears the water, Noli pops up."""
    hit = 0.36
    r = 0 if t < hit else K.ease_out((t - hit) / 0.75) * 1500
    fr = pool_frame(t, d, r, 1.12, 1.2)
    cx, cy = K.W / 2, K.H * 0.5
    if t >= hit:
        tt = t - hit
        for k in range(3):
            rr = (tt - k * 0.12) * 1500
            if rr > 0:
                fr = K.ripple_warp(fr, cx, cy, rr, amp=26 * math.exp(-tt * 1.5), width=60)
                K.ring(fr, cx, cy, rr, 9, alpha=0.75 * math.exp(-tt * 2.2), sy=1.0)
        K.splash_drops(fr, tt, cx, cy, 22, power=1.1)
    if t < hit:   # falling
        y = -300 + (cy + 40) * (t / hit) ** 1.6
        K.paste(fr, K.sprite_np("sprites/n-dive.png"), cx, y, 0.62 * (1 - 0.35 * t / hit), sx=0.85, sy=1.2, shadow=0)
    elif t > hit + 0.4:   # pops up waving
        p = (t - hit - 0.4) / 0.35
        K.paste(fr, K.sprite_np("sprites/n-wave.png"), cx, cy + 260, 0.95 * K.spring(p), anchor="b", shadow=0.6)
        K.headline(fr, [[("Meet", False), ("Noli", True)]], K.W / 2, 470, 170, K.FREDOKA, t, hit + 0.45, 0.12, stroke=12)
    if hit - 0.03 < t < hit + 0.08:
        fr = fr * 0.6 + 255 * 0.4
    return fr


def s_values(t, d, a, ctx):
    fr = sunny_bg(t, d, 16)
    fr = fr * 0.55 + np.array([0, 150, 235], np.float32) * 0.45
    k = K.ease_out(t / 0.45)
    typ = K.clamp((t - 0.35) / (d - 0.5))
    K.put_phone(fr, K.ui_values(round(typ * 24) / 24), K.W * 0.56, K.H * 0.46 + (1 - k) * 1200, 0.74, rot=4 - 4 * k,
                tilt=-0.35 + 0.2 * K.ease_io(t / d))
    K.paste(fr, K.sprite_np("sprites/n-point.png"), 190 + (1 - K.ease_out((t - 0.3) / 0.4)) * -400, K.H * 0.80, 0.5, flip=True,
            anchor="b", shadow=0.4, rot=6)
    return fr


def s_spots(t, d, a, ctx):
    k = K.clamp(t / (d * 0.85))
    sc = K.ui_results(min(0.62, 0.05 + k * 0.6))
    z = 1.0 + 0.08 * K.ease_io(t / d)
    fr = K.screen_zoom(sc, K.SW / 2, 700 + 40 * K.ease_io(t / d), z).astype(np.float32)
    # pulse rings on the two bad values
    for i, x in enumerate([0.27, 0.73]):
        p = (t - 0.35 - i * 0.18)
        if p > 0:
            K.ring(fr, x * K.W, 835 - 55 * K.ease_io(t / d), 120 + p * 260, 8, color=(K.ORANGE if i == 0 else K.RED),
                   alpha=max(0, 0.8 - p * 1.2))
    return fr


def s_priority(t, d, a, ctx):
    sc = K.ui_results(1.0, focus_priority=t > 0.35)
    z = 1.3 - 0.15 * K.ease_out(t / d)
    fr = K.screen_zoom(sc, K.SW / 2, 1050 - 80 * K.ease_io(t / d), z).astype(np.float32)
    K.sparkles(fr, t, [(240, 520, 0.4), (860, 470, 0.55), (930, 760, 0.7)], size=36)
    return fr


def s_order(t, d, a, ctx):
    fr = K.gradient((0, 170, 245), (0, 95, 200)).copy()
    fr = K.bubbles(fr, t, 30, color=(170, 225, 255), alpha=0.5)
    K.paste(fr, K.sprite_np("sprites/n-present.png"), K.W / 2, K.H * 0.86, 0.8 * K.spring(t / 0.45), anchor="b", shadow=0.5)
    for i, (num, txt, col) in enumerate([("1", "pH", K.ORANGE), ("2", "Chlorine", K.RED)]):
        p = (t - 0.15 - i * 0.28) / 0.3
        if p <= 0:
            continue
        y = 420 + i * 230
        card = Image.new("RGBA", (760, 190), (0, 0, 0, 0))
        dd = ImageDraw.Draw(card)
        dd.rounded_rectangle((0, 10, 759, 189), 50, fill=(0, 30, 80, 70))
        dd.rounded_rectangle((0, 0, 759, 179), 50, fill=(255, 255, 255, 255))
        dd.ellipse((26, 26, 154, 154), fill=(*col, 255))
        f = ImageFont.truetype(K.FREDOKA, 92)
        dd.text((90 - f.getlength(num) / 2, 28), num, font=f, fill=(255, 255, 255, 255))
        dd.text((190, 40), txt, font=f, fill=(*K.NAVY, 255))
        K.paste(fr, np.asarray(card), K.W / 2 + (1 - K.ease_out(p)) * 900, y, 1.0)
    return fr


def s_strike(t, d, a, ctx):
    fr = K.gradient((235, 250, 255), (170, 225, 255)).copy()
    strikes = min(3, int(max(t - 0.15, 0) / 0.32) + 1) if t > 0.15 else 0
    rc = receipt_im(7, True, 0.0, strikes)
    K.paste(fr, rc, K.W / 2, K.H * 0.40, 1.08 + 0.05 * K.ease_io(t / d), rot=-2, shadow=0.5)
    K.paste(fr, K.sprite_np("sprites/n-confused.png"), K.W * 0.84, K.H * 0.8, 0.36, anchor="b", rot=-6, shadow=0.4, flip=True)
    return fr


def s_dont_guess(t, d, a, ctx):
    fr = K.cover("img/bg-pool-sunny.jpg", t, d, 1.15, 1.25, 0.5, 0.65).astype(np.float32)
    fr = K.blur(fr, 4)
    K.headline(fr, [[("Don't", False), ("guess.", False)]], K.W / 2, 470, 175, K.FREDOKA, t, 0.0, 0.1, stroke=13)
    K.paste(fr, K.sprite_np("sprites/n-wink.png"), K.W / 2, K.H * 0.86, 0.95 * K.spring(t / 0.4), anchor="b", shadow=0.5)
    return fr


def s_knows(t, d, a, ctx):
    fr = K.cover("img/bg-pool-sunny.jpg", t, d, 1.3, 1.38, 0.5, 0.7).astype(np.float32)
    fr = K.blur(fr, 6)
    fr = K.radial_glow(fr, K.W / 2, K.H * 0.62, 700, (255, 255, 255), 0.35)
    K.headline(fr, [[("Noli", True), ("knows.", False)]], K.W / 2, 470, 190, K.FREDOKA, t, 0.0, 0.12, stroke=13)
    K.paste(fr, K.sprite_np("sprites/noli-thumbsup.png"), K.W / 2, K.H * 0.88, 1.05 * K.spring(t / 0.4), anchor="b", shadow=0.5,
            rot=math.sin(t * 4) * 2)
    K.sparkles(fr, t, [(250, 900, 0.25), (830, 820, 0.4), (780, 1250, 0.6), (300, 1300, 0.75)], size=46)
    return fr


def end_card(t, d, a, ctx):
    """Modelled on the brand's official vertical ad: 3D logo, two lines, Play badge, Noli pointing at the Home screen."""
    fr = K.cover("img/bg-pool-sunny.jpg", t, d, 1.08, 1.14, 0.5, 0.55).astype(np.float32)
    fr = K.water_warp(fr, t, amp=2.5)
    # refraction strips down the edges
    for x0, w_ in [(0, 70), (95, 26), (K.W - 70, 70), (K.W - 120, 24)]:
        strip = fr[:, x0:x0 + w_].copy()
        strip = np.roll(strip, int(40 + 30 * math.sin(t * 2 + x0)), axis=0)
        fr[:, x0:x0 + w_] = strip * 0.7 + 255 * 0.3
    lg = K.logo_3d(210)
    p = (t - 0.05) / 0.45
    K.paste(fr, lg, K.W / 2, 300 + (1 - K.ease_out(p)) * -300, 0.95 * K.spring(p) if p > 0 else 0, shadow=0)
    for i, (txt, sz) in enumerate([("No more pool headaches.", 76), ("Avoid unnecessary chemicals.", 54)]):
        q = (t - 0.35 - i * 0.12) / 0.3
        if q > 0:
            K.paste(fr, K.text_im(txt, K.FREDOKA, sz, K.WHITE, 0, K.NAVY, 6), K.W / 2, 500 + i * 85 + (1 - K.ease_out(q)) * 30,
                    1.0, alpha=K.clamp(q * 2))
    q = (t - 0.6) / 0.35
    if q > 0:
        K.paste(fr, K.play_badge(560), K.W / 2, 740, K.ease_back(q, 2.2))
        for s_ in (-1, 1):
            for j, ang in enumerate((-25, 0, 25)):
                a_ = math.radians(ang)
                x = K.W / 2 + s_ * (320 + 30 * math.cos(a_)) + s_ * math.sin(t * 6) * 4
                y = 740 + ang * 1.6
                cv2.line(fr, (int(x), int(y)), (int(x + s_ * 40 * math.cos(a_)), int(y + 40 * math.sin(a_))), (255, 255, 255), 6, cv2.LINE_AA)
    q = (t - 0.2) / 0.45
    K.put_phone(fr, K.ui_home(), K.W * 0.74 + (1 - K.ease_out(q)) * 600, K.H * 0.72, 0.42, rot=6, tilt=-0.3, shadow=0.6)
    K.paste(fr, K.sprite_np("sprites/n-point.png"), K.W * 0.33, K.H * 0.97, 0.88 * K.spring(max(t - 0.1, 0) / 0.5), flip=True,
            anchor="b", shadow=0.5)
    return fr


# ------------------------------------------------------------------ spec
def post(fr, t, n):
    fr = K.grain(fr, n, 3)
    return fr


cap = K.make_captions(K.FREDOKA, 92, 1390, keys=("noli", "green?", "order.", "need."))
shots = [
    dict(w=0, scene=s_receipt_hook, cap=True, sfx=["bass", {"name": "type", "at": 0.05}, {"name": "type", "at": 0.22},
                                                   {"name": "type", "at": 0.39}, {"name": "type", "at": 0.56},
                                                   {"name": "impact", "at": 0.8, "gain": 0.9}]),
    dict(w=1, scene=s_still_green, tr="glitch", cap=False, sfx=[{"name": "wrong", "at": 0.6}]),
    dict(w=7, scene=s_guess, tr="whip", sfx=[{"name": "ui-pop", "at": 0.1 + 0.16 * i} for i in range(4)]),
    dict(w=11, scene=s_buy, tr="zoom", sfx=[{"name": "key", "at": 0.11 * i} for i in range(5)]),
    dict(w=14, scene=s_drop, tr="whip", cap=False, sfx=[{"name": "riser", "at": 0.3, "gain": 0.6}, {"name": "splash", "at": 0.36},
                                                        {"name": "bloop", "at": 0.8}, {"name": "sparkle", "at": 1.0}]),
    dict(w=16, scene=s_values, tr="splash", cap_y=1640, sfx=[{"name": "tap", "at": 0.45 + 0.13 * i} for i in range(5)]),
    dict(w=20, scene=s_spots, tr="zoom", cap_y=1640, sfx=[{"name": "ui-pop", "at": 0.3}, {"name": "ui-pop", "at": 0.5}]),
    dict(w=24, scene=s_priority, tr="whip", cap_y=1640, sfx=[{"name": "ding", "at": 0.35}]),
    dict(w=31, scene=s_order, tr="slide", sfx=[{"name": "pop", "at": 0.2}, {"name": "pop", "at": 0.48}]),
    dict(w=35, scene=s_strike, tr="whip", cap_y=1560, sfx=[{"name": "scratch", "at": 0.2, "gain": 0.5}, {"name": "select", "at": 0.5},
                                                          {"name": "select", "at": 0.82}]),
    dict(w=42, scene=s_dont_guess, tr="flash", cap=False, sfx=[{"name": "pop", "at": 0.05}]),
    dict(w=44, scene=s_knows, tr="zoom", cap=False, sfx=[{"name": "sparkle", "at": 0.3}, {"name": "bloop", "at": 0.05}]),
    dict(w=46, scene=end_card, tr="splash", cap=False, dur=2.6 + 1.7,
         sfx=[{"name": "bloop", "at": 0.2}, {"name": "ding", "at": 0.65}, {"name": "sparkle", "at": 0.9}]),
]
# the end card lasts from "NoliDrop" to 2.6 s after "Play": dur is measured from its start (fixed below)

if __name__ == "__main__":
    import sys
    spec = dict(name="nolidrop-ad-1", voice="ad1/voice-1.wav", max_gap=0.4, shots=shots, caption=cap, post=post,
                extra={16: 0.5}, fixes={"NOLI.": "Noli.", "NOLI": "Noli", "Noly": "Noli", "Noly.": "Noli.", "drop.": "Drop.", "$124,": "$124.80…"},
                music=[{"t": 0.0, "file": "music/gear.mp3", "start": 1.16, "vol": 1.0}], music_volume=0.42, duck=0.4)
    # end card length: from its start to 2.6 s after the last word
    voice, words = K.prepare_voice(spec["voice"], K.HERE / "work" / spec["name"], spec["max_gap"], 1.0, spec["fixes"], spec["extra"])
    shots[-1]["dur"] = words[-1][2] + 2.6 - (words[46][1] - 0.06)
    K.render(spec)
