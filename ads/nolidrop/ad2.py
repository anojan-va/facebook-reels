"""NoliDrop ad 2 - "Your Brain on Green Water" (psychology hook). Night-pool look: navy/teal, neon, Bebas Neue,
glitch + ripple transitions; the grade flips to bright cyan when Noli drops in.
python3 ad2.py [--plan | --stills | --frame t1,t2]"""
import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import adkit as K

NEON = (40, 230, 255)
TAGS = [("PH", (255, 150, 40)), ("CHLORINE", (255, 70, 80)), ("ALGAE", (90, 230, 90)), ("CLOUDY", (200, 200, 220)),
        ("STABILIZER", (190, 120, 255))]
TAG_POS = [(0.24, 0.26), (0.72, 0.21), (0.78, 0.43), (0.22, 0.50), (0.55, 0.62)]


# ------------------------------------------------------------------ assets
@lru_cache(maxsize=32)
def neon_tag(text, color, size=78):
    f = ImageFont.truetype(K.BEBAS, size)
    w = int(f.getlength(text)) + 70
    h = int(size * 1.25)
    pad = 40
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((pad, pad, pad + w, pad + h), 22, outline=(*color, 255), width=7)
    d.text((pad + 35, pad + size * 0.14), text, font=f, fill=(*color, 255))
    g = im.filter(ImageFilter.GaussianBlur(14))
    out = Image.alpha_composite(Image.alpha_composite(Image.new("RGBA", im.size, (0, 0, 0, 0)), g), g)
    fill = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(fill).rounded_rectangle((pad, pad, pad + w, pad + h), 22, fill=(5, 15, 35, 200))
    out = Image.alpha_composite(out, fill)
    return np.asarray(Image.alpha_composite(out, im))


def big(text, size, color=K.WHITE, glow=0, glow_color=None):
    return K.text_im(text, K.BEBAS, size, color, 0, (0, 0, 0), 0, 2, glow, glow_color)


def slam(fr, text, cy, size, t, start=0.0, color=K.WHITE, glow=16, glow_color=NEON, cx=K.W / 2):
    """Text slams in from 1.6x with a quick settle."""
    p = (t - start) / 0.16
    if p <= 0:
        return
    s = 1 + 0.6 * (1 - K.ease_out(p))
    K.paste(fr, big(text, size, color, glow, glow_color), cx, cy, s, alpha=K.clamp(p * 1.5))


def mask_reveal(fr, text, cy, size, t, start, color=K.WHITE, dur=0.28, glow=0, glow_color=None):
    """Line rises out of an invisible mask (condensed-type reveal)."""
    p = K.ease_out((t - start) / dur)
    if p <= 0:
        return
    lay = big(text, size, color, glow, glow_color)
    h = lay.shape[0]
    off = int((1 - p) * h * 0.8)
    cut = lay.copy()
    cut = np.roll(cut, off, axis=0)
    cut[:off] = 0
    K.paste(fr, cut, K.W / 2, cy, 1.0)


def night(fr, k=1.0):
    """Night grade: crushed blacks, teal shadows."""
    f = fr.astype(np.float32)
    f = (f - 10) * 1.05
    f = f * np.array([0.78, 0.95, 1.08], np.float32) * k + f * (1 - k)
    return np.clip(f, 0, 255)


@lru_cache(maxsize=4)
def priority_card(scale=1.0):
    """The single PRIORITY #1 card everything collapses into."""
    w, h = 820, 420
    im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle((40, 40, 40 + w, 40 + h), 56, fill=(*NEON, 200))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(26)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, 40 + w, 40 + h), 56, fill=(255, 255, 255, 255))
    f1 = ImageFont.truetype(K.INTER_XB, 44)
    d.rounded_rectangle((90, 90, 90 + f1.getlength("PRIORITY #1") + 50, 160), 35, fill=(255, 238, 220, 255))
    d.text((115, 98), "PRIORITY #1", font=f1, fill=(220, 110, 10, 255))
    f2 = ImageFont.truetype(K.NUNITO, 64)
    d.text((92, 190), "Your pH is a little", font=f2, fill=(*K.NAVY, 255))
    d.text((92, 262), "too low", font=f2, fill=(*K.NAVY, 255))
    # mini range bar
    bx0, bx1, by = 92, 40 + w - 60, 380
    d.rounded_rectangle((bx0, by, bx1, by + 22), 11, fill=(255, 205, 160, 255))
    g0, g1 = bx0 + (1.0 / 2.2) * (bx1 - bx0), bx0 + (1.6 / 2.2) * (bx1 - bx0)
    d.rectangle((g0, by, g1, by + 22), fill=(80, 200, 120, 255))
    mx = bx0 + (0.6 / 2.2) * (bx1 - bx0)
    d.ellipse((mx - 18, by - 7, mx + 18, by + 29), fill=(*K.ORANGE, 255), outline=(255, 255, 255, 255), width=4)
    return np.asarray(im)


def under_bg(t, d, z0=1.05, z1=1.15, warp=6):
    fr = K.cover("img/bg-night-under.jpg", t, d, z0, z1, 0.5, 0.6).astype(np.float32)
    return K.water_warp(fr, t, amp=warp, freq=0.012, speed=1.6)


def bright_bg(t, d):
    """After the drop: the night pool lit bright cyan."""
    fr = K.cover("img/bg-night-pool.jpg", t, d, 1.15, 1.22, 0.5, 0.75).astype(np.float32)
    fr = K.blur(fr, 10)
    fr = fr * 0.55 + K.gradient((0, 120, 200), (0, 200, 240)) * 0.45
    fr = K.water_warp(fr, t, amp=4)
    return fr


# ------------------------------------------------------------------ scenes
def s_brain(t, d, a, ctx):
    fr = K.cover("img/bg-brain.jpg", t, d, 1.55, 1.2, 0.45, 0.47, ease=K.ease_out).astype(np.float32)
    fr = K.water_warp(fr, t, amp=5, freq=0.015)
    pulse = 0.5 + 0.5 * math.sin(t * 9)
    fr = K.radial_glow(fr, K.W * 0.48, K.H * 0.5, 650, (255, 40, 60), 0.18 + 0.12 * pulse)
    mask_reveal(fr, "YOUR BRAIN", 420, 210, t, 0.05, K.WHITE)
    mask_reveal(fr, "DOES THIS", 600, 150, t, 0.5, (255, 90, 100), glow=10, glow_color=(255, 40, 60))
    return K.vignette(fr, 0.5)


def s_turns_green(t, d, a, ctx):
    fr = K.cover("img/bg-pool-green.jpg", t, d, 1.5, 1.25, 0.5, 0.45, ease=K.ease_out).astype(np.float32)
    fr = night(fr) * 0.75
    fr = K.water_warp(fr, t, amp=5)
    slam(fr, "TURNS GREEN", 520, 200, t, 0.15, (130, 255, 110), 18, (60, 220, 60))
    return K.vignette(fr, 0.5)


def s_panic(t, d, a, ctx):
    fr = K.cover("img/bg-brain.jpg", t, d, 1.9, 2.1, 0.45, 0.45, shake=2.5).astype(np.float32)
    fr = K.radial_glow(fr, K.W / 2, K.H / 2, 900, (255, 30, 50), 0.35 + 0.25 * (int(t * 12) % 2))
    if int(t * 14) % 3 == 0:
        fr = K.transition("glitch", fr, fr, 0.2, int(t * 100))
    slam(fr, "PANIC", 820, 330, t, 0.05, (255, 60, 70), 22, (255, 0, 30))
    return K.vignette(fr, 0.55)


def tags_layer(fr, t, start=0.0, spread=1.0, rot=0.0, suck=None):
    """The five problem tags bursting out of the centre (suck = (x, y, k) pulls them into a point)."""
    for i, ((txt, col), (x, y)) in enumerate(zip(TAGS, TAG_POS)):
        p = (t - start - i * 0.09) / 0.3
        if p <= 0:
            continue
        e = K.ease_back(p, 1.8)
        tx = K.W / 2 + (x * K.W - K.W / 2) * e * spread
        ty = K.H * 0.42 + (y * K.H - K.H * 0.42) * e * spread
        ty += math.sin(t * 3 + i) * 10
        s = 1.0
        if suck:
            sx, sy, k = suck
            k = K.ease_in(K.clamp(k - i * 0.06))
            tx, ty = tx + (sx - tx) * k, ty + (sy - ty) * k
            s = 1 - 0.85 * k
        K.paste(fr, neon_tag(txt, col), tx, ty, s * min(1.0, e), rot=(-1) ** i * (6 + rot * math.sin(t * 5 + i)))


def s_problems(t, d, a, ctx):
    fr = night(under_bg(t, d))
    K.paste(fr, big("5", 520, (255, 255, 255), 30, NEON), K.W / 2, K.H * 0.42, 1.0 + 0.05 * t, alpha=0.18)
    tags_layer(fr, t, 0.0)
    return K.vignette(fr, 0.45)


def s_products(t, d, a, ctx):
    fr = K.cover("img/bg-cart.jpg", t, d, 1.25, 1.45, 0.5, 0.5).astype(np.float32)
    fr = K.radial_glow(fr, K.W / 2, K.H * 0.42, 700, NEON, 0.12)
    slam(fr, "5 PRODUCTS", 380, 190, t, 0.05, K.WHITE, 14, NEON)
    return K.vignette(fr, 0.45)


def s_at_once(t, d, a, ctx):
    fr = K.cover("img/bg-cart.jpg", t, d, 1.6, 1.9, 0.5, 0.45, rot=3 * math.sin(t * 6), shake=2.0).astype(np.float32)
    fr = night(fr)
    tags_layer(fr, t + 1.0, 0.0, spread=1.05, rot=12)
    slam(fr, "ALL AT ONCE", 1180, 180, t, 0.1, (255, 230, 80), 14, (255, 160, 0))
    return K.vignette(fr, 0.5)


def s_overload(t, d, a, ctx):
    fr = night(under_bg(t, d, 1.3, 1.4, 4)) * 0.55
    mask_reveal(fr, "PSYCHOLOGISTS CALL IT", 560, 92, t, 0.0, (170, 220, 240))
    mask_reveal(fr, "CHOICE", 760, 300, t, 0.62, K.WHITE, 0.3, 18, NEON)
    mask_reveal(fr, "OVERLOAD", 1030, 300, t, 0.9, NEON, 0.3, 18, NEON)
    return K.vignette(fr, 0.5)


def s_expensive(t, d, a, ctx):
    fr = night(under_bg(t, d, 1.2, 1.3)) * 0.7
    rng = np.random.default_rng(4)
    for i in range(16):
        x = rng.uniform(80, K.W - 80)
        sp = rng.uniform(900, 1500)
        y = -200 + ((t - rng.uniform(0, 0.6)) * sp) % (K.H + 400)
        if t > 0.05:
            K.paste(fr, big("$", int(rng.uniform(110, 220)), (120, 255, 150), 10, (40, 200, 80)), x, y, 1.0,
                    rot=rng.uniform(-25, 25) + t * 40 * (-1) ** i, alpha=0.85)
    slam(fr, "EXPENSIVE", 900, 250, t, 0.55, (255, 80, 90), 20, (255, 0, 40))
    return K.vignette(fr, 0.5)


def s_drop(t, d, a, ctx):
    """Signature Drop, night version: Noli falls through the dark water; the impact flips the grade to bright cyan."""
    hit = 0.42
    if t < hit:
        fr = night(under_bg(t, d, 1.1, 1.2)) * 0.8
        y = -250 + (K.H * 0.55) * (t / hit) ** 1.5
        K.bubbles(fr, t, 18, seed=9, region=(K.W * 0.35, K.W * 0.65, y, K.H), speed=300)
        K.paste(fr, K.sprite_np("sprites/n-dive.png"), K.W / 2, y, 0.6, sx=0.85, sy=1.2)
        return fr
    tt = t - hit
    fr = bright_bg(t, d)
    fr = K.radial_glow(fr, K.W / 2, K.H * 0.55, 900, (190, 250, 255), 0.5 * math.exp(-tt * 2) + 0.15)
    for k in range(3):
        rr = (tt - k * 0.12) * 1600
        if rr > 0:
            fr = K.ripple_warp(fr, K.W / 2, K.H * 0.55, rr, amp=30 * math.exp(-tt * 1.5), width=70)
            K.ring(fr, K.W / 2, K.H * 0.55, rr, 10, alpha=0.8 * math.exp(-tt * 2))
    K.splash_drops(fr, tt, K.W / 2, K.H * 0.6, 24, power=1.2)
    K.paste(fr, K.sprite_np("sprites/n-present.png"), K.W / 2, K.H * 0.86, 0.85 * K.spring(tt / 0.4), anchor="b", shadow=0.5)
    slam(fr, "THE OPPOSITE", 430, 190, tt, 0.15, K.WHITE, 12, (0, 90, 180))
    if tt < 0.1:
        fr = fr * (tt / 0.1) + 255 * (1 - tt / 0.1)
    return fr


def s_one_analysis(t, d, a, ctx):
    fr = bright_bg(t, d)
    K.paste(fr, big("1", 900, (255, 255, 255)), K.W * 0.3, K.H * 0.45, 1.0 + 0.04 * t, alpha=0.22)
    k = K.ease_out(t / 0.4)
    K.put_phone(fr, K.ui_results(K.clamp(t / d * 0.9 + 0.1)), K.W * 0.56, K.H * 0.47 + (1 - k) * 900, 0.72, rot=-5 + 3 * k,
                tilt=0.4 - 0.15 * K.ease_io(t / d))
    return fr


def s_one_priority(t, d, a, ctx):
    """Signature visual: the five chaos tags get sucked in and collapse into ONE card."""
    fr = bright_bg(t, d)
    suck = K.clamp((t - 0.05) / 0.55)
    if suck < 1:
        tags_layer(fr, 2.0, 0.0, 1.0, suck=(K.W / 2, K.H * 0.42, suck * 1.3))
    p = (t - 0.55) / 0.35
    if p > 0:
        K.paste(fr, priority_card(), K.W / 2, K.H * 0.42, K.spring(p, 2.6, 6), shadow=0.4)
        K.ring(fr, K.W / 2, K.H * 0.42, 300 + (t - 0.55) * 900, 8, alpha=max(0, 0.6 - (t - 0.55) * 1.2))
    return fr


def s_split(t, d, a, ctx):
    """Before / after split."""
    L = K.cover("img/bg-cart.jpg", t, d, 1.5, 1.6, 0.5, 0.45).astype(np.float32)
    L = night(L) * 0.55
    L = L * np.array([1.2, 0.7, 0.7], np.float32)
    R = bright_bg(t, d)
    k = K.ease_out(t / 0.5)
    x = int(K.W * (1 - 0.5 * k))
    fr = L.copy()
    fr[:, x:] = R[:, x:]
    cv2.line(fr, (x, 0), (x, K.H), (255, 255, 255), 8, cv2.LINE_AA)
    lw = K.W / 4
    K.paste(fr, big("5 AT ONCE", 120, (255, 120, 120)), lw, 420, 1.0)
    cx_ = K.W * 0.25
    p = (t - 0.3) / 0.2
    if p > 0:
        cv2.line(fr, (int(cx_ - 90), 560), (int(cx_ + 90), 740), (255, 70, 80), 22, cv2.LINE_AA)
        cv2.line(fr, (int(cx_ + 90), 560), (int(cx_ - 90), 740), (255, 70, 80), 22, cv2.LINE_AA)
    rx = K.W * 0.75
    if k > 0.6:
        K.paste(fr, big("1 STEP", 130, K.WHITE, 10, (0, 90, 180)), rx, 420, 1.0)
        K.paste(fr, big("RIGHT ORDER", 92, K.WHITE, 10, (0, 90, 180)), rx, 530, 1.0)
        q = (t - 0.55) / 0.25
        if q > 0:
            pts = np.array([[rx - 80, 660], [rx - 20, 720], [rx + 90, 590]], np.int32)
            cv2.polylines(fr, [pts], False, (80, 230, 120), 24, cv2.LINE_AA)
        K.paste(fr, priority_card(), rx, 1030, 0.5)
    return fr


def s_feature(t, d, a, ctx):
    fr = bright_bg(t + a.get("off", 0), d)
    screen = {"problem": K.ui_home(1), "problem2": K.ui_guide("problem"), "startup": K.ui_guide("startup"),
              "winter": K.ui_guide("winter")}[a["ui"]]
    side = a.get("side", 1)
    K.put_phone(fr, screen, K.W * (0.5 + 0.06 * side), K.H * 0.45, 0.72 + 0.04 * K.ease_io(t / d), rot=side * 4,
                tilt=side * 0.35)
    slam(fr, a["label"], 170, 150, t, 0.0, K.WHITE, 12, (0, 80, 170))
    return fr


def s_walks(t, d, a, ctx):
    fr = bright_bg(t, d)
    K.put_phone(fr, K.ui_guide("startup"), K.W * 0.66, K.H * 0.44, 0.66, rot=5, tilt=-0.3)
    K.paste(fr, K.sprite_np("sprites/n-wave.png"), K.W * 0.26, K.H * 0.9, 0.62 * K.spring(t / 0.4), anchor="b", shadow=0.5, flip=True)
    return fr


def s_dont_guess(t, d, a, ctx):
    fr = K.cover("img/bg-night-pool.jpg", t, d, 1.2, 1.28, 0.5, 0.7).astype(np.float32)
    fr = K.water_warp(fr, t, amp=3)
    mask_reveal(fr, "DON'T", 520, 260, t, 0.0, K.WHITE, 0.22)
    mask_reveal(fr, "GUESS.", 760, 260, t, 0.12, K.WHITE, 0.22)
    return K.vignette(fr, 0.4)


def s_knows(t, d, a, ctx):
    fr = K.cover("img/bg-night-pool.jpg", t, d, 1.3, 1.38, 0.5, 0.78).astype(np.float32)
    fr = K.water_warp(fr, t, amp=3)
    fr = K.radial_glow(fr, K.W / 2, K.H * 0.66, 750, NEON, 0.3)
    mask_reveal(fr, "NOLI", 380, 260, t, 0.0, NEON, 0.22, 16, NEON)
    mask_reveal(fr, "KNOWS.", 610, 260, t, 0.1, K.WHITE, 0.22)
    K.paste(fr, K.sprite_np("sprites/n-wink.png"), K.W / 2, K.H * 0.92, 0.9 * K.spring(t / 0.4), anchor="b", shadow=0.5)
    return fr


def end_card(t, d, a, ctx):
    """Night variant of the brand end card."""
    fr = K.cover("img/bg-night-pool.jpg", t, d, 1.1, 1.15, 0.5, 0.6).astype(np.float32)
    fr = K.water_warp(fr, t, amp=2.5)
    fr = fr * 0.8 + K.gradient((0, 40, 90), (0, 140, 200)) * 0.2
    fr = K.radial_glow(fr, K.W / 2, 320, 650, (60, 180, 255), 0.35)
    for x0, w_ in [(0, 70), (95, 26), (K.W - 70, 70), (K.W - 120, 24)]:
        strip = np.roll(fr[:, x0:x0 + w_].copy(), int(40 + 30 * math.sin(t * 2 + x0)), axis=0)
        fr[:, x0:x0 + w_] = strip * 0.7 + np.array([120, 220, 255], np.float32) * 0.3
    p = (t - 0.05) / 0.45
    K.paste(fr, K.logo_3d(210), K.W / 2, 300, 0.95 * K.spring(p) if p > 0 else 0)
    for i, (txt, sz) in enumerate([("No more pool headaches.", 76), ("Avoid unnecessary chemicals.", 54)]):
        q = (t - 0.35 - i * 0.12) / 0.3
        if q > 0:
            K.paste(fr, K.text_im(txt, K.FREDOKA, sz, K.WHITE, 0, K.NAVY, 6), K.W / 2, 500 + i * 85, 1.0, alpha=K.clamp(q * 2))
    q = (t - 0.6) / 0.35
    if q > 0:
        K.paste(fr, K.play_badge(560), K.W / 2, 740, K.ease_back(q, 2.2))
    q = (t - 0.2) / 0.45
    K.put_phone(fr, K.ui_home(), K.W * 0.74 + (1 - K.ease_out(q)) * 600, K.H * 0.72, 0.42, rot=6, tilt=-0.3, shadow=0.6)
    K.paste(fr, K.sprite_np("sprites/n-point.png"), K.W * 0.33, K.H * 0.97, 0.88 * K.spring(max(t - 0.1, 0) / 0.5), flip=True,
            anchor="b", shadow=0.5)
    return fr


def post(fr, t, n):
    return K.grain(fr, n, 4)


cap = K.make_captions(K.BEBAS, 128, 1420, color=K.WHITE, key=NEON, stroke=0, shadow=8, upper=True, max_words=2,
                      keys=("noli",), track=2)
shots = [
    dict(w=0, scene=s_brain, cap=False, sfx=["hook", {"name": "heartbeat", "at": 0.5}, {"name": "heartbeat", "at": 1.3}]),
    dict(w=6, scene=s_turns_green, tr="glitch", cap=False, sfx=[{"name": "bass", "at": 0.15}]),
    dict(w=10, scene=s_panic, tr="flash", cap=False, sfx=[{"name": "glitch", "at": 0.05}, {"name": "heartbeat", "at": 0.25}]),
    dict(w=12, scene=s_problems, tr="glitch", sfx=[{"name": "pop", "at": 0.09 * i} for i in range(5)]),
    dict(w=14, scene=s_products, tr="zoom", cap=False, sfx=[{"name": "impact", "at": 0.05, "gain": 0.7}]),
    dict(w=16, scene=s_at_once, tr="whip", cap=False, sfx=[{"name": "glitch-hit", "at": 0.1}]),
    dict(w=19, scene=s_overload, tr="dip", cap=False, sfx=[{"name": "boom", "at": 0.62, "gain": 0.6}, {"name": "bass", "at": 0.9}]),
    dict(w=24, scene=s_expensive, tr="glitch", sfx=[{"name": "key", "at": 0.1 + 0.12 * i} for i in range(4)] + [{"name": "wrong", "at": 0.6}]),
    dict(w=31, scene=s_drop, tr="ripple", cap=False, sfx=[{"name": "plunge", "at": 0.0, "gain": 0.6}, {"name": "splash", "at": 0.42},
                                                       {"name": "reveal", "at": 0.45}, {"name": "bloop", "at": 0.85}]),
    dict(w=35, scene=s_one_analysis, tr="whip", cap_y=1640, sfx=[{"name": "ui-pop", "at": 0.35}]),
    dict(w=37, scene=s_one_priority, tr="zoom", cap_y=1560, sfx=[{"name": "sweep", "at": 0.1}, {"name": "ding", "at": 0.6}]),
    dict(w=42, scene=s_split, tr="slide", cap_y=1640, sfx=[{"name": "wrong", "at": 0.3}, {"name": "correct", "at": 0.6}]),
    dict(w=50, scene=s_feature, a={"ui": "problem", "label": "GREEN WATER", "side": 1}, tr="whip", cap=False, sfx=["tap"]),
    dict(w=52, scene=s_feature, a={"ui": "problem2", "label": "CLOUDY WATER", "side": -1, "off": 1}, tr="slide", cap=False, sfx=["tap"]),
    dict(w=54, scene=s_feature, a={"ui": "startup", "label": "START-UP", "side": 1, "off": 2}, tr="whip", cap=False, sfx=["tap"]),
    dict(w=55, scene=s_feature, a={"ui": "winter", "label": "WINTERIZING", "side": -1, "off": 3}, tr="slide", cap=False, sfx=["tap"]),
    dict(w=56, scene=s_walks, tr="ripple", cap_y=1700, sfx=[{"name": "select", "at": 0.2 + 0.18 * i} for i in range(4)]),
    dict(w=61, scene=s_dont_guess, tr="dip", cap=False, sfx=[{"name": "bass", "at": 0.05}]),
    dict(w=63, scene=s_knows, tr="ripple", cap=False, sfx=[{"name": "sparkle", "at": 0.3}, {"name": "bloop", "at": 0.1}]),
    dict(w=65, scene=end_card, tr="splash", cap=False, dur=4.0, sfx=[{"name": "bloop", "at": 0.2}, {"name": "ding", "at": 0.65}]),
]

if __name__ == "__main__":
    spec = dict(name="nolidrop-ad-2", voice="ad2/voice-1.wav", max_gap=0.28, shots=shots, caption=cap, post=post,
                fixes={"Noly": "Noli", "drop.": "Drop."},
                music=[{"t": 0.0, "file": "music/infected-vibes.mp3", "start": 2.81, "vol": 1.0},
                       {"shot": 8, "offset": 0.42, "file": "music/dirty-thinkin.mp3", "start": 3.58, "vol": 1.0}],
                music_volume=0.42, duck=0.38)
    voice, words = K.prepare_voice(spec["voice"], K.HERE / "work" / spec["name"], spec["max_gap"], 1.0, spec["fixes"])
    shots[-1]["dur"] = words[-1][2] + 2.2 - (words[65][1] - 0.06)
    K.render(spec)
