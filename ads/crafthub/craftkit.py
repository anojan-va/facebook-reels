"""Craft-paper look for The Craft Hub reels, on top of ../nolidrop/adkit.py (renderer, audio, captions).
Brand: cream #fffaf6, deep green #1f3b2c, terracotta #d45541; fonts Annie Use Your Telescope (hand titles),
Architects Daughter (hand text), Poppins (labels). Visual language: scrapbook / stop-motion paper craft -
torn photo cards, washi tape, stitched lines, handwritten labels, paper-cut people; motion on "twos" with a jitter."""
import math
import sys
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "nolidrop"))
import adkit as K  # noqa: E402

K.HERE = HERE   # renders, work files, images and voice resolve inside ads/crafthub
W, H = K.W, K.H
F = HERE / "fonts"
HAND, HAND2 = str(F / "AnnieUseYourTelescope.ttf"), str(F / "ArchitectsDaughter.ttf")
POP, POPX = str(F / "Poppins-SemiBold.ttf"), str(F / "Poppins-ExtraBold.ttf")
CREAM, PAPER = (255, 250, 246), (247, 239, 228)
GREEN, TERRA, TERRA_D = (31, 59, 44), (212, 85, 65), (179, 74, 58)
MUSTARD, SAGE, BLUSH, INK = (222, 178, 64), (170, 190, 150), (244, 206, 192), (38, 40, 36)

_S = HERE / "sfx"
K.SFX.update({   # name: (file, peak s, pre, post, gain)
    "paper":    (_S / "paper-slide.mp3", 0.36, 0.3, 0.12, 1.0),
    "page":     (_S / "page-turn.mp3", 0.14, 0.12, 0.2, 1.0),
    "paperq":   (_S / "paper-quick.mp3", 0.42, 0.25, 0.35, 0.9),
    "scribble": (_S / "scribble.mp3", 0.17, 0.12, 0.4, 0.8),
    "pencil":   (_S / "pencil.mp3", 0.3, 0.3, 0.6, 0.8),
    "snip":     (_S / "scissors.mp3", 2.09, 0.3, 0.22, 0.9),
    "tape":     (_S / "tape-rip.mp3", 1.52, 0.45, 0.4, 0.8),
    "crumple":  (_S / "crumple.mp3", 0.26, 0.2, 0.4, 0.8),
    "slice":    (_S / "paper-slice.mp3", 0.1, 0.06, 0.2, 0.9),
})
K.TR_SFX.update({"tear": "crumple", "page": "page", "slide": "paper", "whip": "paperq"})
K.TR_LEN.update({"tear": 0.3, "page": 0.32})


# ------------------------------------------------------------------ stop motion
def st(t, fps=12):
    """Time quantised to stop-motion steps."""
    return math.floor(t * fps) / fps


def jit(t, i=0, amt=1.0, fps=12):
    """Per-step jitter (x, y, rot) for 'boiling' paper pieces."""
    rng = np.random.default_rng(int(t * fps) * 131 + i * 17)
    return rng.uniform(-3, 3) * amt, rng.uniform(-3, 3) * amt, rng.uniform(-0.8, 0.8) * amt


# ------------------------------------------------------------------ paper
@lru_cache(maxsize=16)
def _paper(color, seed):
    rng = np.random.default_rng(seed)
    base = np.ones((H, W, 3), np.float32) * np.array(color, np.float32)
    n = cv2.resize(rng.normal(0, 1, (H // 6, W // 6)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    fine = rng.normal(0, 1, (H, W)).astype(np.float32)
    tex = n * 4.0 + cv2.GaussianBlur(fine, (0, 0), 0.8) * 3.0
    fib = np.zeros((H, W), np.float32)
    for _ in range(260):   # paper fibres
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        a, L = rng.uniform(0, math.pi), rng.uniform(10, 40)
        cv2.line(fib, (int(x), int(y)), (int(x + L * math.cos(a)), int(y + L * math.sin(a))), float(rng.uniform(-1, 1)), 1, cv2.LINE_AA)
    tex += cv2.GaussianBlur(fib, (0, 0), 0.6) * 10
    out = base + tex[..., None]
    y, x = np.ogrid[:H, :W]
    v = 1 - 0.08 * (((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return np.clip(out * v[..., None], 0, 255).astype(np.float32)


def paper(color=CREAM, t=0.0, seed=1):
    """Paper background that 'boils' slightly between two textures (stop-motion)."""
    return _paper(color, seed + (int(t * 6) % 2) * 1000).copy()


@lru_cache(maxsize=32)
def torn_card(path, w=760, pad=26, seed=1, crop=0.9, tint=(255, 255, 252)):
    """A photo (white-background product shot) on a white card with deckled/torn edges, as RGBA."""
    im = Image.open(HERE / path).convert("RGB")
    s = min(im.size) * crop
    cx, cy = im.width / 2, im.height / 2
    im = im.crop((int(cx - s / 2), int(cy - s / 2), int(cx + s / 2), int(cy + s / 2))).resize((w - 2 * pad, w - 2 * pad), Image.LANCZOS)
    ch = w + 40   # a polaroid-ish lip at the bottom
    card = Image.new("RGB", (w, ch), tint)
    card.paste(im, (pad, pad))
    rng = np.random.default_rng(seed)
    m = Image.new("L", (w, ch), 0)
    d = ImageDraw.Draw(m)
    pts = []
    for side in range(4):
        n = 60
        for i in range(n):
            k = i / n
            j = rng.uniform(0, 7)
            if side == 0: pts.append((k * w, j))
            elif side == 1: pts.append((w - j, k * ch))
            elif side == 2: pts.append((w - k * w, ch - j))
            else: pts.append((j, ch - k * ch))
    d.polygon(pts, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(0.8))
    rgba = np.dstack([np.asarray(card), np.asarray(m)])
    return _with_shadow(rgba)


def _with_shadow(rgba, off=12, blur=14, alpha=0.32):
    h, w = rgba.shape[:2]
    p = off + blur * 2
    out = np.zeros((h + p * 2, w + p * 2, 4), np.uint8)
    sh = np.zeros((h + p * 2, w + p * 2), np.float32)
    sh[p + off:p + off + h, p + off // 2:p + off // 2 + w] = rgba[..., 3] / 255.0
    sh = cv2.GaussianBlur(sh, (0, 0), blur) * alpha
    out[..., :3] = 30
    out[..., 3] = (sh * 255).astype(np.uint8)
    a = rgba[..., 3:4].astype(np.float32) / 255
    reg = out[p:p + h, p:p + w].astype(np.float32)
    reg[..., :3] = reg[..., :3] * (1 - a) + rgba[..., :3] * a
    reg[..., 3:4] = np.maximum(reg[..., 3:4], rgba[..., 3:4])
    out[p:p + h, p:p + w] = reg.astype(np.uint8)
    return out


@lru_cache(maxsize=32)
def washi(w=260, h=70, color=MUSTARD, pattern="dots", seed=1):
    """Translucent washi tape strip with zig-zag torn ends."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    z = 8
    pts = [(z * (i % 2), i * h / 10) for i in range(11)] + [(w - z * (i % 2), h - i * h / 10) for i in range(11)]
    d.polygon(pts, fill=(*color, 205))
    if pattern == "dots":
        for x in range(20, w - 10, 34):
            for y in range(14, h, 28):
                d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255, 150))
    elif pattern == "stripes":
        for x in range(-h, w, 26):
            d.line((x, h, x + h, 0), fill=(255, 255, 255, 120), width=8)
    a = np.asarray(im).copy()
    return a


@lru_cache(maxsize=64)
def label(text, size=56, bg=CREAM, fg=GREEN, font=None, pad=28, rot_seed=0):
    """Handwritten paper label (torn strip)."""
    f = ImageFont.truetype(font or HAND2, size)
    tw = int(f.getlength(text))
    w, h = tw + pad * 2, int(size * 1.55)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(rot_seed + len(text))
    pts = [(rng.uniform(0, 4), 0)] + [(w - rng.uniform(0, 6), rng.uniform(0, 4)), (w - rng.uniform(0, 4), h - rng.uniform(0, 4)),
                                      (rng.uniform(0, 6), h)]
    d.polygon(pts, fill=(*bg, 255))
    d.text((pad, h / 2 - size * 0.62), text, font=f, fill=(*fg, 255))
    return _with_shadow(np.asarray(im), 6, 8, 0.25)


def text(txt, size, color=GREEN, font=None, stroke=0, stroke_color=CREAM):
    return K.text_im(txt, font or HAND, size, color, stroke, stroke_color, 0, 0)


def hand_line(fr, pts, k, color=TERRA, width=9, seed=0, t=0.0):
    """Hand-drawn polyline that draws itself (k 0..1) and boils slightly."""
    if k <= 0:
        return
    rng = np.random.default_rng(int(t * 12) * 7 + seed)
    pts = np.array(pts, np.float32)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    L = seg.sum() * K.clamp(k)
    out, acc = [pts[0]], 0.0
    for i, s in enumerate(seg):
        if acc + s >= L:
            out.append(pts[i] + (pts[i + 1] - pts[i]) * ((L - acc) / max(s, 1e-6)))
            break
        acc += s
        out.append(pts[i + 1])
    out = np.array(out) + rng.uniform(-1.5, 1.5, (len(out), 2))
    cv2.polylines(fr, [out.astype(np.int32)], False, color, width, cv2.LINE_AA)


def underline(fr, x0, x1, y, k, color=TERRA, t=0.0, seed=0):
    n = 24
    pts = [(x0 + (x1 - x0) * i / (n - 1), y + 8 * math.sin(i / (n - 1) * math.pi * 1.2)) for i in range(n)]
    hand_line(fr, pts, k, color, 11, seed, t)


def tick(fr, x, y, s, k, color=TERRA, t=0.0):
    hand_line(fr, [(x - s * 0.5, y), (x - s * 0.1, y + s * 0.42), (x + s * 0.6, y - s * 0.55)], k, color, int(s * 0.16), 3, t)


def star(fr, x, y, s, color=MUSTARD, t=0.0, seed=0):
    for a in range(4):
        ang = a * math.pi / 4 + 0.2
        hand_line(fr, [(x - s * math.cos(ang), y - s * math.sin(ang)), (x + s * math.cos(ang), y + s * math.sin(ang))], 1, color, 6, seed + a, t)


def heart(fr, x, y, s, color=TERRA, t=0.0, seed=0):
    pts = [(x + s * 16 * math.sin(a) ** 3, y - s * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)))
           for a in np.linspace(0, 2 * math.pi, 40)]
    hand_line(fr, pts, 1, color, 7, seed, t)


def stitches(fr, x0, y0, x1, y1, k, color=TERRA, t=0.0):
    """Dashed 'stitch' border around a rectangle that sews itself on."""
    per = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    pts = []
    for (ax, ay), (bx, by) in zip(per, per[1:]):
        n = int(math.hypot(bx - ax, by - ay) / 28)
        pts += [(ax + (bx - ax) * i / n, ay + (by - ay) * i / n) for i in range(n)]
    m = int(len(pts) * K.clamp(k))
    for i in range(0, m - 1, 2):
        cv2.line(fr, (int(pts[i][0]), int(pts[i][1])), (int(pts[i + 1][0]), int(pts[i + 1][1])), color, 6, cv2.LINE_AA)


@lru_cache(maxsize=8)
def stamp(txt="SELLS OUT FAST", color=TERRA, r=150):
    s = r * 2 + 40
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = s / 2
    d.ellipse((c - r, c - r, c + r, c + r), outline=(*color, 230), width=10)
    d.ellipse((c - r + 22, c - r + 22, c + r - 22, c + r - 22), outline=(*color, 230), width=4)
    f = ImageFont.truetype(POPX, int(r * 0.26))
    words = txt.split()
    lines = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [txt]
    for i, ln in enumerate(lines):
        w = f.getlength(ln)
        d.text((c - w / 2, c - r * 0.32 + i * r * 0.34 - (len(lines) - 1) * 0), ln, font=f, fill=(*color, 230))
    a = np.asarray(im.rotate(-14, resample=Image.BICUBIC)).copy()
    rng = np.random.default_rng(3)   # ink texture
    holes = rng.random(a.shape[:2]) < 0.12
    a[..., 3] = np.where(holes, (a[..., 3] * 0.35).astype(np.uint8), a[..., 3])
    return a


@lru_cache(maxsize=4)
def wordmark(size=170):
    """'The Craft Hub' in the site's hand font, terracotta, with a green hand-drawn underline."""
    f = ImageFont.truetype(HAND, size)
    t = "The Craft Hub"
    w = int(f.getlength(t)) + 60
    im = Image.new("RGBA", (w, int(size * 1.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((30, 0), t, font=f, fill=(*TERRA, 255))
    pts = [(40 + (w - 80) * i / 30, size * 1.22 + 10 * math.sin(i / 30 * math.pi)) for i in range(31)]
    d.line(pts, fill=(*GREEN, 255), width=9, joint="curve")
    return np.asarray(im)


def sprite(name):
    return K.sprite_np(f"sprites/{name}.png")


def put(fr, layer, x, y, s=1.0, rot=0.0, t=0.0, i=0, pop=None, alpha=1.0, anchor="c", jitter=1.0, flip=False):
    """Paste with stop-motion jitter; pop = (t0, dur) springs the scale in."""
    sc = s
    if pop is not None:
        p = (st(t) - pop[0]) / pop[1]
        if p <= 0:
            return
        sc = s * K.spring(min(p, 3), 2.4, 5)
    jx, jy, jr = jit(t, i, jitter)
    K.paste(fr, layer, x + jx, y + jy, sc, rot + jr, alpha, anchor=anchor, flip=flip)


# ------------------------------------------------------------------ transitions (paper)
_orig_transition = K.transition


def transition(kind, a, b, k, n):
    if kind == "tear":   # a jagged vertical tear opens from the middle
        rng = np.random.default_rng(7)
        ys = np.arange(H)
        edge = np.cumsum(rng.normal(0, 6, H))
        edge = cv2.GaussianBlur(edge.reshape(-1, 1).astype(np.float32), (1, 0), 3).ravel() if False else edge
        half = K.ease_in(k) * W * 0.6
        x = np.arange(W)[None, :]
        cx = (W / 2 + edge - edge.mean())[:, None]
        m = (np.abs(x - cx) < half).astype(np.float32)[..., None]
        out = a * (1 - m) + b * m
        rim = ((np.abs(np.abs(x - cx) - half) < 7) & (half > 2)).astype(np.float32)[..., None]
        return out * (1 - rim) + 250 * rim
    if kind == "page":   # page turn: a diagonal fold sweeps across with a shadow
        y, x = np.ogrid[:H, :W]
        pos = (1 - K.ease_io(k)) * (W + H) - H * 0.25
        d = (x + y * 0.45) - pos
        m = (d > 0).astype(np.float32)[..., None]
        out = a * (1 - m) + b * m
        sh = np.clip(1 - np.abs(d) / 60, 0, 1)[..., None] * 0.35
        return out * (1 - sh)
    return _orig_transition(kind, a, b, k, n)


K.transition = transition


# ------------------------------------------------------------------ end card
def end_card(t, d, a, ctx):
    fr = paper(CREAM, t, 5)
    put(fr, washi(300, 70, TERRA, "stripes", 2), 170, 180, rot=-28, t=t, i=1, pop=(0.15, 0.3))
    put(fr, washi(300, 70, SAGE, "dots", 3), 920, 1700, rot=-24, t=t, i=2, pop=(0.25, 0.3))
    put(fr, wordmark(170), W / 2, 560, t=t, i=3, pop=(0.05, 0.4))
    put(fr, text("craft workshops & community", 58, GREEN, HAND2), W / 2, 750, t=t, i=4, pop=(0.3, 0.3))
    put(fr, text("in Berlin", 58, GREEN, HAND2), W / 2, 830, t=t, i=5, pop=(0.35, 0.3))
    for j, (nm, x, y, r) in enumerate(a.get("cards", [("img/o-mug.jpg", 300, 1150, -8), ("img/o-hoop.jpg", 780, 1180, 7)])):
        put(fr, torn_card(nm, 420, 18, seed=j + 9), x, y, rot=r, t=t, i=10 + j, pop=(0.35 + 0.1 * j, 0.35))
    btn = Image.new("RGBA", (640, 130), (0, 0, 0, 0))
    bd = ImageDraw.Draw(btn)
    bd.rounded_rectangle((0, 0, 639, 129), 65, fill=(*GREEN, 255))
    fb = ImageFont.truetype(POPX, 58)
    bd.text((320 - fb.getlength("thecrafthub.de") / 2, 24), "thecrafthub.de", font=fb, fill=(*CREAM, 255))
    put(fr, np.asarray(btn), W / 2, 1500, t=t, i=6, pop=(0.55, 0.35), jitter=0.4)
    if a.get("line"):
        put(fr, text(a["line"], 56, TERRA, HAND2), W / 2, 1640, t=t, i=7, pop=(0.7, 0.3))
    return fr


def post(fr, t, n):
    return K.grain(fr, n, 3)


cap = K.make_captions(HAND2, 86, 1500, color=(255, 255, 255), key=MUSTARD, stroke=10, stroke_color=GREEN, shadow=0,
                      max_words=3, track=1)
