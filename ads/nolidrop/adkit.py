"""Shared renderer for the NoliDrop 9:16 ads (1080x1920, 30 fps): PIL/numpy frames piped into ffmpeg.

An ad script (ad1.py ...) builds a list of shots and calls render(). Pipeline:
  1. voice: one TTS take -> Whisper word times (cached) -> pauses longer than `max_gap` squeezed out.
  2. shots: each starts on a word ("w": index into the spoken words) or after the voice ("after": seconds);
     a shot is a scene function scene(t, d, a, ctx) -> RGB uint8 frame, t = seconds into the shot, d = its length.
  3. transitions between shots ("tr": cut whip zoom flash splash glitch ripple slide), each with its SFX.
  4. captions (per-ad caption function) over every shot whose "cap" isn't False.
  5. audio: voice + music cues (ducked under the voice) + SFX at absolute times -> loudnorm -14 LUFS.
"""
import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "longform"))
from make_long import SFX as LONG_SFX  # noqa: E402
from make_reel import read_audio, write_wav  # noqa: E402

W, H, FPS, SR = 1080, 1920, 30, 44100
SFX = dict(LONG_SFX)
_S = HERE / "sfx"
SFX.update({   # name: (file, peak s into file, pre, post, gain) -- the peak lands on the cue time
    "splash":   (_S / "water-splash.mp3", 0.41, 0.2, 0.9, 0.9),
    "plunge":   (_S / "jump-water.mp3", 0.40, 0.38, 1.4, 0.7),
    "bloop":    (_S / "water-bubble.mp3", 0.12, 0.05, 0.16, 1.2),
    "bubble":   (_S / "liquid-bubble.mp3", 0.05, 0.04, 0.38, 0.9),
    "cartoon-splash": (_S / "cartoon-splash.mp3", 0.48, 0.44, 0.4, 0.8),
    "ui-pop":   (_S / "bubble-alert.mp3", 0.13, 0.11, 0.24, 0.8),
    "ding":     (_S / "positive-notif.mp3", 0.22, 0.17, 1.4, 0.6),
    "confirm":  (_S / "confirm-tone.mp3", 0.19, 0.19, 0.45, 0.6),
    "tap":      (_S / "device-click.mp3", 0.01, 0.01, 0.12, 0.9),
    "select":   (_S / "select-click.mp3", 0.07, 0.07, 0.22, 0.8),
    "type":     (_S / "typewriter.mp3", 0.15, 0.01, 0.11, 0.7),
    "key":      (_S / "atm-key.mp3", 0.01, 0.01, 0.22, 0.7),
})
F = HERE / "fonts"
FREDOKA, NUNITO, BEBAS, OSWALD = str(F / "Fredoka-Bold.ttf"), str(F / "Nunito-Black.ttf"), str(F / "BebasNeue.ttf"), str(F / "Oswald-Bold.ttf")
MONT = str(ROOT / "longform" / "fonts" / "Montserrat-Black.ttf")
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
INTER_M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
INTER_XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
INTER_BLACK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"
if not Path(MONO).exists():
    import glob
    MONO = (glob.glob("/usr/share/fonts/**/JetBrainsMono-Bold.ttf", recursive=True) or ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"])[0]

NAVY = (12, 42, 110)
CYAN = (0, 190, 240)
SKY = (40, 150, 255)
WHITE = (255, 255, 255)
RED = (232, 52, 52)
ORANGE = (255, 140, 30)
GREEN = (40, 190, 100)


# ------------------------------------------------------------------ easing / maths
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x)
    return x ** 3


def ease_io(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_back(x, c=1.7):
    x = clamp(x)
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def spring(x, f=3.2, damp=5.0):
    """0 -> 1 with an overshoot wobble (for pops)."""
    if x <= 0:
        return 0.0
    return 1 - math.exp(-damp * x) * math.cos(f * math.pi * x)


def lerp(a, b, x):
    return a + (b - a) * x


def prog(t, t0, dur):
    return clamp((t - t0) / dur)


# ------------------------------------------------------------------ images
@lru_cache(maxsize=64)
def load(path, mode="RGB"):
    return Image.open(HERE / path).convert(mode)


@lru_cache(maxsize=64)
def load_np(path, mode="RGB"):
    return np.asarray(load(path, mode))


def cover(path, t=0.0, d=1.0, z0=1.0, z1=1.08, fx=0.5, fy=0.5, dx=0.0, dy=0.0, rot=0.0, shake=0.0, ease=ease_io):
    """Full-frame image with a camera move: zoom z0->z1 around (fx, fy) of the image, pan dx/dy (frame fractions)."""
    im = load_np(path)
    ih, iw = im.shape[:2]
    k = ease(t / d) if d > 0 else 1.0
    z = lerp(z0, z1, k)
    s = max(W / iw, H / ih) * z
    cx, cy = fx * iw, fy * ih
    ox, oy = W / 2 + dx * W * k, H / 2 + dy * H * k
    if shake:
        ox += shake * math.sin(t * 37.0) * 8
        oy += shake * math.cos(t * 29.0) * 8
    # keep the image covering the frame
    hw, hh = W / 2 / s, H / 2 / s
    cx = clamp(cx, hw - (ox - W / 2) / s, iw - hw - (ox - W / 2) / s) if iw * s > W else cx
    cy = clamp(cy, hh - (oy - H / 2) / s, ih - hh - (oy - H / 2) / s) if ih * s > H else cy
    M = cv2.getRotationMatrix2D((cx, cy), rot, s)
    M[0, 2] += ox - cx
    M[1, 2] += oy - cy
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def sprite_np(path):
    return load_np(path, "RGBA")


def paste(fr, rgba, cx, cy, scale=1.0, rot=0.0, alpha=1.0, sx=1.0, sy=1.0, anchor="c", flip=False, shadow=0.0):
    """Alpha-composite an RGBA numpy layer onto fr (HxWx3 float32 or uint8, modified in place).
    anchor 'c' = centre at (cx, cy), 'b' = bottom-centre. sx/sy = squash/stretch."""
    if alpha <= 0.003 or scale <= 0.001:
        return fr
    src = rgba[:, ::-1] if flip else rgba
    h, w = src.shape[:2]
    a, b = scale * sx, scale * sy
    ax, ay = w / 2, (h if anchor == "b" else h / 2)
    cr, sr_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    M = np.array([[a * cr, b * sr_, 0], [-a * sr_, b * cr, 0]], np.float32)
    M[:, 2] = [cx - (M[0, 0] * ax + M[0, 1] * ay), cy - (M[1, 0] * ax + M[1, 1] * ay)]
    corners = np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1]], np.float32) @ M.T
    x0, y0 = np.floor(corners.min(axis=0)).astype(int)
    x1, y1 = np.ceil(corners.max(axis=0)).astype(int)
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
    if x1 <= x0 or y1 <= y0:
        return fr
    M2 = M.copy()
    M2[:, 2] -= [x0, y0]
    lay = cv2.warpAffine(src, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    la = lay[..., 3:4].astype(np.float32) / 255 * alpha
    if shadow:
        sh = cv2.GaussianBlur(la[..., 0], (0, 0), 18) * shadow
        off = int(24 * scale) + 6
        reg = fr[y0 + off:y1 + off, x0:x1] if y1 + off <= H else None
        if reg is not None and reg.shape[:2] == sh.shape:
            reg[:] = reg * (1 - sh[..., None] * 0.55)
    reg = fr[y0:y1, x0:x1]
    reg[:] = reg * (1 - la) + lay[..., :3] * la
    return fr


def to_rgba_np(im):
    return np.asarray(im.convert("RGBA"))


def blur(fr, r):
    if r <= 0.3:
        return fr
    return cv2.GaussianBlur(fr, (0, 0), r)


def grade(fr, sat=1.0, contrast=1.0, bright=0.0, tint=(1, 1, 1)):
    f = fr.astype(np.float32)
    if sat != 1.0:
        g = f.mean(axis=2, keepdims=True)
        f = g + (f - g) * sat
    if contrast != 1.0:
        f = (f - 128) * contrast + 128
    f = f * np.array(tint, np.float32) + bright
    return np.clip(f, 0, 255)


@lru_cache(maxsize=8)
def _vig(strength):
    y, x = np.ogrid[:H, :W]
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) / 1.414
    return (1 - strength * np.clip(r - 0.25, 0, 1) ** 1.6 * 1.6).astype(np.float32)[..., None]


def vignette(fr, s=0.35):
    return fr * _vig(round(s, 2))


def grain(fr, n, amt=5):
    rng = np.random.default_rng(n)
    noise = rng.normal(0, amt, (H // 2, W // 2, 1)).astype(np.float32)
    return fr + cv2.resize(noise, (W, H))[..., None]


def water_warp(fr, t, amp=6.0, freq=0.018, speed=2.0):
    """Refraction wobble (pool water)."""
    y, x = _grid()
    mx = x + amp * np.sin(y * freq + t * speed) + amp * 0.5 * np.sin(x * freq * 1.7 - t * speed * 1.3)
    my = y + amp * np.cos(x * freq * 0.9 + t * speed * 0.8)
    return cv2.remap(fr, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


@lru_cache(maxsize=1)
def _grid():
    y, x = np.mgrid[:H, :W].astype(np.float32)
    return y, x


def ripple_warp(fr, cx, cy, radius, amp=24.0, width=90.0):
    """A travelling ring that refracts the picture (the Drop ripple)."""
    y, x = _grid()
    dx, dy = x - cx, y - cy
    r = np.sqrt(dx * dx + dy * dy) + 1e-3
    k = np.exp(-((r - radius) / width) ** 2) * np.sin((r - radius) / width * 3.14)
    off = amp * k
    return cv2.remap(fr, x + dx / r * off, y + dy / r * off, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def ring(fr, cx, cy, radius, width=10, color=WHITE, alpha=0.8, sy=1.0):
    if radius <= 1 or alpha <= 0.01:
        return fr
    lay = np.zeros((H, W), np.uint8)
    cv2.ellipse(lay, (int(cx), int(cy)), (int(radius), int(radius * sy)), 0, 0, 360, 255, int(max(width, 1)), cv2.LINE_AA)
    lay = cv2.GaussianBlur(lay, (0, 0), 2).astype(np.float32)[..., None] / 255 * alpha
    fr[:] = fr * (1 - lay) + np.array(color, np.float32) * lay
    return fr


def radial_glow(fr, cx, cy, r, color, alpha):
    y, x = np.ogrid[:H, :W]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / r
    m = (np.clip(1 - d, 0, 1) ** 2 * alpha).astype(np.float32)[..., None]
    fr[:] = fr * (1 - m) + np.array(color, np.float32) * m
    return fr


def gradient(c0, c1, angle=90):
    y, x = _grid()
    if angle == 90:
        k = y / H
    else:
        a = math.radians(angle)
        k = ((x - W / 2) * math.cos(a) + (y - H / 2) * math.sin(a)) / (W + H) * 1.4 + 0.5
    k = np.clip(k, 0, 1)[..., None]
    return np.array(c0, np.float32) * (1 - k) + np.array(c1, np.float32) * k


# ------------------------------------------------------------------ text
@lru_cache(maxsize=512)
def text_im(text, font, size, color=WHITE, stroke=0, stroke_color=(0, 0, 0), shadow=0, track=0, glow=0, glow_color=None):
    """One line of text as RGBA numpy. shadow = soft drop shadow offset px."""
    f = ImageFont.truetype(font, size)
    widths = [f.getlength(c) + track for c in text]
    tw = int(sum(widths) - track) + 4 if track else int(f.getlength(text)) + 4
    asc, desc = f.getmetrics()
    pad = stroke + shadow * 2 + glow * 3 + 10
    im = Image.new("RGBA", (tw + pad * 2, asc + desc + pad * 2), (0, 0, 0, 0))

    def draw(d, fill, sw=0, sf=None, off=(0, 0)):
        x = pad + off[0]
        if track:
            for c, w in zip(text, widths):
                d.text((x, pad + off[1]), c, font=f, fill=fill, stroke_width=sw, stroke_fill=sf)
                x += w
        else:
            d.text((x, pad + off[1]), text, font=f, fill=fill, stroke_width=sw, stroke_fill=sf)
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        draw(ImageDraw.Draw(g), (*(glow_color or color), 255), stroke)
        g = g.filter(ImageFilter.GaussianBlur(glow))
        im = Image.alpha_composite(im, g)
        im = Image.alpha_composite(im, g)
    if shadow:
        s = Image.new("RGBA", im.size, (0, 0, 0, 0))
        draw(ImageDraw.Draw(s), (0, 20, 60, 150), stroke, (0, 20, 60, 150), (0, shadow))
        s = s.filter(ImageFilter.GaussianBlur(shadow * 0.8))
        im = Image.alpha_composite(im, s)
    d = ImageDraw.Draw(im)
    if stroke:   # outline pass, then a clean fill pass (heavy fonts with overlapping contours invert a one-pass stroke)
        draw(d, (*stroke_color, 255), stroke, (*stroke_color, 255))
    draw(d, (*color, 255))
    return np.asarray(im)


def text_w(text, font, size, track=0):
    f = ImageFont.truetype(font, size)
    return f.getlength(text) + track * (len(text) - 1)


@lru_cache(maxsize=64)
def brush_underline(width, height=26, color=CYAN, seed=1):
    """A hand-painted brush stroke (the brand's keyword underline)."""
    rng = np.random.default_rng(seed)
    im = Image.new("RGBA", (int(width) + 40, height * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    n = 40
    for i in range(n):
        x = 20 + width * i / (n - 1)
        th = height * (0.55 + 0.45 * math.sin(math.pi * i / (n - 1))) * (0.9 + 0.2 * rng.random())
        y = height * 1.5 + math.sin(i / n * 3.0) * height * 0.25
        d.ellipse((x - th * 0.6, y - th / 2, x + th * 0.6, y + th / 2), fill=(*color, 255))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(1.2)))


def reveal_x(rgba, k):
    """Wipe an RGBA layer in from the left (k 0..1)."""
    out = rgba.copy()
    cut = int(out.shape[1] * clamp(k))
    out[:, cut:, 3] = 0
    return out


def headline(fr, parts, cx, cy, size, font, t, start=0.0, stagger=0.08, color=WHITE, key=CYAN, stroke=0, stroke_color=NAVY,
             shadow=6, pop="back", underline=True, track=0, line_gap=1.08):
    """Multi-line headline. parts = list of lines, each a list of (word, is_key). Words pop in one by one.
    Returns the bottom y."""
    i = 0
    y = cy - (len(parts) - 1) * size * line_gap / 2
    for line in parts:
        sp = text_w(" ", font, size)
        ws = [text_w(w, font, size, track) for w, _ in line]
        x = cx - (sum(ws) + sp * (len(ws) - 1)) / 2
        for (w, k), ww in zip(line, ws):
            p = (t - start - i * stagger) / 0.32
            if p > 0:
                s = ease_back(p, 2.2) if pop == "back" else ease_out(p)
                lay = text_im(w, font, size, key if k else color, stroke, stroke_color, shadow, track)
                if k and underline:
                    u = brush_underline(int(ww), max(10, size // 7), key)
                    paste(fr, reveal_x(u, (t - start - i * stagger - 0.2) / 0.3), x + ww / 2, y + size * 0.62, 1.0,
                          alpha=0.95)
                paste(fr, lay, x + ww / 2, y + (1 - s) * size * 0.4, max(s, 0.01) if pop == "back" else 1.0,
                      alpha=clamp(p * 3))
            x += ww + sp
            i += 1
        y += size * line_gap
    return y


# ------------------------------------------------------------------ brand pieces
@lru_cache(maxsize=4)
def logo_3d(size=210):
    """The bubbly NoliDrop logo: white-to-cyan gradient letters, thick dark-blue outline, droplets over the 'p'."""
    f = ImageFont.truetype(FREDOKA, size)
    text = "NoliDrop"
    tw = int(f.getlength(text))
    asc, desc = f.getmetrics()
    pad = 60
    Wd, Hd = tw + pad * 2, asc + desc + pad * 2
    mask = Image.new("L", (Wd, Hd), 0)
    ImageDraw.Draw(mask).text((pad, pad), text, font=f, fill=255)
    out = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
    # shadow
    sh = Image.new("L", (Wd, Hd), 0)
    ImageDraw.Draw(sh).text((pad, pad + 14), text, font=f, fill=255, stroke_width=16, stroke_fill=255)
    out.paste(Image.new("RGBA", (Wd, Hd), (5, 25, 80, 170)), (0, 0), sh.filter(ImageFilter.GaussianBlur(12)))
    # outline
    ol = Image.new("L", (Wd, Hd), 0)
    ImageDraw.Draw(ol).text((pad, pad), text, font=f, fill=255, stroke_width=14, stroke_fill=255)
    out.paste(Image.new("RGBA", (Wd, Hd), (*NAVY, 255)), (0, 0), ol)
    # gradient fill
    g = np.zeros((Hd, Wd, 4), np.uint8)
    yy = np.linspace(0, 1, Hd)[:, None]
    top, bot = np.array([255, 255, 255]), np.array([90, 200, 255])
    k = np.clip((yy - 0.3) / 0.5, 0, 1)
    g[..., :3] = (top * (1 - k) + bot * k)[:, None, :].reshape(Hd, 1, 3).repeat(Wd, 1)
    g[..., 3] = 255
    out.paste(Image.fromarray(g), (0, 0), mask)
    # glossy highlight on the upper half of each letter
    hl = Image.new("L", (Wd, Hd), 0)
    ImageDraw.Draw(hl).text((pad, pad), text, font=f, fill=255)
    hl = Image.fromarray((np.asarray(hl) * (np.linspace(1, 0, Hd)[:, None] > 0.62)).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    out.paste(Image.new("RGBA", (Wd, Hd), (255, 255, 255, 150)), (0, 0), hl)
    # droplets over the 'p'
    d = ImageDraw.Draw(out)
    px = pad + f.getlength("NoliDro") + f.getlength("p") * 0.75
    for (ox, oy, r) in [(0, -0.05, 0.075), (0.12, -0.2, 0.05), (-0.08, -0.22, 0.035)]:
        x, y, rr = px + ox * size, pad + (0.32 + oy) * size, r * size
        d.ellipse((x - rr - 5, y - rr * 1.25 - 5, x + rr + 5, y + rr + 5), fill=(*NAVY, 255))
        d.ellipse((x - rr, y - rr * 1.25, x + rr, y + rr), fill=(120, 215, 255, 255))
        d.ellipse((x - rr * 0.5, y - rr * 0.9, x - rr * 0.05, y - rr * 0.4), fill=(255, 255, 255, 220))
    a = np.asarray(out)
    ys, xs = np.where(a[..., 3] > 5)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


@lru_cache(maxsize=4)
def wordmark(size=150):
    """Flat wordmark from the app icon: 'Noli' navy + 'Drop' cyan, cyan swoosh underline."""
    f = ImageFont.truetype(FREDOKA, size)
    w1, w2 = f.getlength("Noli"), f.getlength("Drop")
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (int(w1 + w2) + 40, asc + desc + 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((20, 10), "Noli", font=f, fill=(*NAVY, 255))
    d.text((20 + w1, 10), "Drop", font=f, fill=(*CYAN, 255))
    # swoosh
    cx = 20 + w1 + w2 * 0.45
    pts = [(cx - w2 * 0.45 + i * w2 * 0.9 / 30, asc + desc + 22 - 18 * math.sin(math.pi * i / 30)) for i in range(31)]
    d.line(pts, fill=(*CYAN, 255), width=12, joint="curve")
    return np.asarray(im)


@lru_cache(maxsize=4)
def play_badge(width=560):
    """The black 'GET IT ON Google Play' store badge, drawn in code."""
    h = int(width * 0.296)
    s = 3
    im = Image.new("RGBA", (width * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, width * s - 1, h * s - 1), radius=int(h * 0.16 * s), fill=(0, 0, 0, 255), outline=(166, 166, 166, 255), width=3 * s)
    # play triangle in four colours
    ix, iy, ih = h * 0.22 * s, h * 0.2 * s, h * 0.6 * s
    iw = ih * 0.86
    A, B, C = (ix, iy), (ix, iy + ih), (ix + iw, iy + ih / 2)
    M = (ix + iw * 0.55, iy + ih / 2)
    d.polygon([A, M, (ix, iy + ih / 2)], fill=(0, 210, 255, 255))
    d.polygon([(ix, iy + ih / 2), M, B], fill=(0, 200, 120, 255))
    d.polygon([A, (ix + iw * 0.78, iy + ih * 0.32), C, M], fill=(255, 210, 0, 255))
    d.polygon([B, (ix + iw * 0.78, iy + ih * 0.68), C, M], fill=(255, 60, 70, 255))
    d.polygon([A, (ix + iw * 0.7, iy + ih * 0.3), M], fill=(0, 230, 120, 255))
    d.polygon([A, M, (ix, iy + ih / 2)], fill=(0, 200, 255, 255))
    d.polygon([B, M, (ix + iw * 0.7, iy + ih * 0.7)], fill=(255, 55, 75, 255))
    tx = ix + iw + h * 0.16 * s
    d.text((tx, h * 0.17 * s), "GET IT ON", font=ImageFont.truetype(INTER_SB, int(h * 0.19 * s)), fill=(255, 255, 255, 255))
    d.text((tx - 2 * s, h * 0.36 * s), "Google Play", font=ImageFont.truetype(INTER_SB, int(h * 0.37 * s)), fill=(255, 255, 255, 255))
    return np.asarray(im.resize((width, h), Image.LANCZOS))


# ------------------------------------------------------------------ phone + app UI (English rebuild of the real screens)
SW, SH = 780, 1690   # screen pixels


@lru_cache(maxsize=4)
def _ui_fonts():
    return {k: ImageFont.truetype(NUNITO if k.startswith("n") else INTER_SB if k.startswith("s") else INTER_M, v)
            for k, v in {"n64": 64, "n52": 52, "n44": 44, "n38": 38, "n34": 34, "n30": 30, "s30": 30, "s26": 26, "s24": 24,
                         "s22": 22, "m26": 26, "m24": 24, "m22": 22, "m20": 20, "n90": 90, "n28": 28}.items()}


def _status(d, dark=False):
    f = _ui_fonts()
    c = (20, 20, 30) if dark else (255, 255, 255)
    d.text((54, 26), "9:41", font=f["s26"], fill=c)
    d.rounded_rectangle((SW - 120, 34, SW - 66, 58), 7, outline=c, width=3)
    d.rectangle((SW - 116, 38, SW - 80, 54), fill=c)
    for i, hh in enumerate([8, 12, 16, 20]):
        d.rectangle((SW - 190 + i * 11, 58 - hh, SW - 183 + i * 11, 58), fill=c)


def _tabbar(d, active=0):
    f = _ui_fonts()
    d.rectangle((0, SH - 150, SW, SH), fill=(255, 255, 255))
    d.line((0, SH - 150, SW, SH - 150), fill=(230, 236, 245), width=2)
    names = ["Home", "Analyze", "History", "Tools"]
    for i, n in enumerate(names):
        x = SW * (i + 0.5) / 4
        col = (20, 120, 230) if i == active else (150, 160, 175)
        if i == 0:
            d.polygon([(x - 20, SH - 100), (x, SH - 120), (x + 20, SH - 100), (x + 20, SH - 78), (x - 20, SH - 78)], fill=col)
        elif i == 1:
            d.ellipse((x - 16, SH - 122, x + 16, SH - 82), outline=col, width=5)
        elif i == 2:
            d.ellipse((x - 20, SH - 122, x + 20, SH - 82), outline=col, width=5)
            d.line((x, SH - 112, x, SH - 102, x + 9, SH - 96), fill=col, width=4)
        else:
            for k in range(2):
                for j in range(2):
                    d.rounded_rectangle((x - 20 + k * 22, SH - 122 + j * 22, x - 4 + k * 22, SH - 106 + j * 22), 4, fill=col)
        w = f["m20"].getlength(n)
        d.text((x - w / 2, SH - 70), n, font=f["m20"], fill=col)
    d.rounded_rectangle((SW / 2 - 110, SH - 22, SW / 2 + 110, SH - 14), 4, fill=(20, 20, 30))


def _noli_icon(size):
    im = load("sprites/noli-thumbsup.png", "RGBA").copy()
    im.thumbnail((size, size), Image.LANCZOS)
    return im


@lru_cache(maxsize=8)
def ui_home(highlight=-1):
    """Home screen. highlight = index of a card to glow (0 analyze, 1 problem, 2 start-up, 3 winterizing)."""
    f = _ui_fonts()
    im = Image.new("RGB", (SW, SH), (244, 248, 253))
    d = ImageDraw.Draw(im)
    # header photo (pool) with Noli
    hdr = load("img/bg-pool-sunny.jpg").copy()
    hdr = hdr.crop((0, int(hdr.height * 0.45), hdr.width, int(hdr.height * 0.45) + int(hdr.width * 600 / SW))).resize((SW, 600))
    im.paste(hdr, (0, 0))
    ov = Image.new("RGBA", (SW, 600), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle((0, 0, SW, 600), fill=(0, 40, 90, 70))
    im.paste(ov, (0, 0), ov)
    noli = _noli_icon(300)
    im.paste(noli, (SW - noli.width - 30, 600 - noli.height - 10), noli)
    d = ImageDraw.Draw(im)
    _status(d)
    d.text((48, 150), "Hello", font=f["n90"], fill=(255, 255, 255))
    d.text((50, 262), "A clean and healthy pool,", font=f["s30"], fill=(255, 255, 255))
    d.text((50, 302), "made simple.", font=f["s30"], fill=(255, 255, 255))
    y = 560
    # analyze card (blue)
    cards = [(y, 230, (24, 130, 240), "Analyze my water", "Enter your values and get", "customized recommendations", WHITE),
             (y + 260, 200, (255, 255, 255), "I have a problem", "Green water, cloudy water or", "another issue? Noli helps you", (25, 35, 60))]
    for i, (cy, ch, bg, title, l1, l2, fg) in enumerate(cards):
        if highlight == i:
            d.rounded_rectangle((26, cy - 8, SW - 26, cy + ch + 8), 40, outline=(0, 200, 255), width=8)
        d.rounded_rectangle((36, cy, SW - 36, cy + ch), 34, fill=bg, outline=None if i == 0 else (225, 232, 242), width=2)
        ix = 76
        if i == 0:
            d.ellipse((ix, cy + 50, ix + 96, cy + 146), fill=(255, 255, 255))
            d.polygon([(ix + 48, cy + 66), (ix + 72, cy + 106), (ix + 48, cy + 130), (ix + 24, cy + 106)], fill=(24, 130, 240))
        else:
            d.ellipse((ix, cy + 50, ix + 96, cy + 146), fill=(255, 232, 232))
            d.polygon([(ix + 48, cy + 66), (ix + 80, cy + 126), (ix + 16, cy + 126)], fill=RED)
            d.text((ix + 42, cy + 82), "!", font=f["n38"], fill=(255, 255, 255))
        d.text((ix + 130, cy + 40), title, font=f["n44"], fill=fg)
        d.text((ix + 130, cy + 100), l1, font=f["m24"], fill=fg if i == 0 else (90, 100, 120))
        d.text((ix + 130, cy + 132), l2, font=f["m24"], fill=fg if i == 0 else (90, 100, 120))
        d.text((SW - 90, cy + ch / 2 - 30), "›", font=f["n64"], fill=fg if i == 0 else (150, 160, 180))
    ty = y + 500
    for k, (title, l1, l2, col) in enumerate([("Start-up", "Prepare your pool", "for the season", (255, 170, 30)),
                                              ("Winterizing", "Protect your pool", "during winter", (70, 150, 255))]):
        x0 = 36 + k * (SW - 72 + 24) / 2
        x1 = x0 + (SW - 72 - 24) / 2
        if highlight == 2 + k:
            d.rounded_rectangle((x0 - 10, ty - 10, x1 + 10, ty + 320), 40, outline=(0, 200, 255), width=8)
        d.rounded_rectangle((x0, ty, x1, ty + 310), 34, fill=(255, 255, 255), outline=(225, 232, 242), width=2)
        d.ellipse((x0 + 30, ty + 34, x0 + 120, ty + 124), fill=(*col, ))
        if k == 0:
            d.ellipse((x0 + 58, ty + 62, x0 + 92, ty + 96), fill=(255, 255, 255))
        else:
            for a in range(6):
                ang = a * math.pi / 3
                d.line((x0 + 75, ty + 79, x0 + 75 + 30 * math.cos(ang), ty + 79 + 30 * math.sin(ang)), fill=(255, 255, 255), width=6)
        d.text((x0 + 30, ty + 150), title, font=f["n38"], fill=(25, 35, 60))
        d.text((x0 + 30, ty + 205), l1, font=f["m22"], fill=(90, 100, 120))
        d.text((x0 + 30, ty + 237), l2, font=f["m22"], fill=(90, 100, 120))
    _tabbar(d, 0)
    return im


def _topbar(d, title):
    f = _ui_fonts()
    _status(d, dark=True)
    d.text((40, 96), "‹", font=f["n64"], fill=(20, 120, 230))
    w = f["n38"].getlength(title)
    d.text((SW / 2 - w / 2, 112), title, font=f["n38"], fill=(25, 35, 60))


def ui_values(k=1.0):
    """'Analyze my water' entry screen; k = typing progress 0..1 (pH then chlorine)."""
    f = _ui_fonts()
    im = Image.new("RGB", (SW, SH), (244, 248, 253))
    d = ImageDraw.Draw(im)
    _topbar(d, "Analyze my water")
    d.text((48, 220), "Enter your values", font=f["n52"], fill=(25, 35, 60))
    d.text((48, 290), "From your test strip or test kit.", font=f["m26"], fill=(90, 100, 120))
    fields = [("pH", "6,8", ""), ("Free chlorine", "0", "ppm")]
    for i, (name, val, unit) in enumerate(fields):
        y = 380 + i * 230
        d.text((48, y), name, font=f["s30"], fill=(25, 35, 60))
        active = (i == 0 and k < 0.5) or (i == 1 and k >= 0.5)
        d.rounded_rectangle((40, y + 50, SW - 40, y + 170), 28, fill=(255, 255, 255), outline=(24, 130, 240) if active else (220, 228, 240), width=4 if active else 2)
        part = clamp((k - i * 0.5) / 0.4)
        shown = val[:int(round(part * len(val)))]
        d.text((76, y + 76), shown + (" " + unit if shown and unit and part >= 1 else ""), font=f["n52"], fill=(25, 35, 60))
        if active and int(k * 12) % 2 == 0:
            cx = 76 + f["n52"].getlength(shown) + 4
            d.rectangle((cx, y + 80, cx + 4, y + 140), fill=(24, 130, 240))
    for i, (name, ph) in enumerate([("Total alkalinity", "ppm"), ("Stabilizer (CYA)", "ppm")]):
        y = 840 + i * 200
        d.text((48, y), name, font=f["s30"], fill=(150, 160, 175))
        d.rounded_rectangle((40, y + 50, SW - 40, y + 150), 28, fill=(250, 252, 255), outline=(230, 236, 245), width=2)
        d.text((76, y + 74), ph, font=f["m26"], fill=(190, 198, 210))
    d.rounded_rectangle((40, SH - 330, SW - 40, SH - 210), 60, fill=(24, 130, 240) if k >= 0.95 else (160, 200, 245))
    w = f["n44"].getlength("Analyze")
    d.text((SW / 2 - w / 2, SH - 300), "Analyze", font=f["n44"], fill=(255, 255, 255))
    _tabbar(d, 1)
    return im


def ui_results(k=1.0, focus_priority=False):
    """Analysis results screen, revealed top to bottom as k goes 0..1. Mirrors the real app's screen."""
    f = _ui_fonts()
    im = Image.new("RGB", (SW, SH), (244, 248, 253))
    d = ImageDraw.Draw(im)
    _topbar(d, "Analysis results")
    steps = [0.0, 0.12, 0.25, 0.38, 0.5, 0.62, 0.75, 0.88]

    def on(i):
        return k >= steps[i]
    y = 190
    if on(0):
        d.rounded_rectangle((36, y, SW - 36, y + 110), 30, fill=(225, 240, 255))
        d.text((66, y + 18), "Several parameters need to be corrected.", font=f["s22"], fill=(20, 90, 180))
        d.text((66, y + 56), "We'll handle them in the right order, together.", font=f["m22"], fill=(20, 90, 180))
    y += 140
    if on(1):
        d.rounded_rectangle((36, y, SW - 36, y + 100), 28, fill=(255, 235, 235), outline=(245, 160, 160), width=2)
        d.ellipse((60, y + 28, 104, y + 72), fill=RED)
        d.text((76, y + 26), "!", font=f["n34"], fill=(255, 255, 255))
        d.text((124, y + 18), "Disinfectant at 0:", font=f["s26"], fill=(190, 30, 30))
        d.text((124, y + 54), "do not swim for now.", font=f["m24"], fill=(190, 30, 30))
    y += 130
    if on(2):
        d.text((44, y), "2 parameters to correct", font=f["n38"], fill=(25, 35, 60))
    y += 70
    for i, (name, val, col) in enumerate([("pH", "6,8", ORANGE), ("Chlorine", "0 ppm", RED)]):
        if on(3 + i):
            x0 = 36 + i * (SW - 72 + 20) / 2
            x1 = x0 + (SW - 72 - 20) / 2
            d.rounded_rectangle((x0, y, x1, y + 150), 28, fill=(255, 255, 255), outline=(225, 232, 242), width=2)
            d.text((x0 + 28, y + 22), name, font=f["s26"], fill=(90, 100, 120))
            d.text((x0 + 28, y + 62), val, font=f["n52"], fill=col)
            ax = x1 - 60
            d.polygon([(ax - 16, y + 80), (ax + 16, y + 80), (ax, y + 108)], fill=col)
            d.rectangle((ax - 5, y + 58, ax + 5, y + 82), fill=col)
    y += 190
    if on(5):
        if focus_priority:
            d.rounded_rectangle((22, y - 14, SW - 22, y + 560), 44, outline=(0, 200, 255), width=8)
        d.rounded_rectangle((36, y, SW - 36, y + 546), 34, fill=(255, 255, 255), outline=(225, 232, 242), width=2)
        d.rounded_rectangle((64, y + 30, 300, y + 80), 25, fill=(255, 240, 225))
        d.text((84, y + 38), "PRIORITY #1", font=f["s26"], fill=(220, 110, 10))
        d.text((64, y + 100), "Your pH is a little too low", font=f["n44"], fill=(25, 35, 60))
        # range bar 6.2 .. 8.4, green 7.2-7.8, marker at 6.8
        bx0, bx1, by = 80, SW - 80, y + 220
        d.rounded_rectangle((bx0, by, bx1, by + 26), 13, fill=(255, 205, 160))
        g0 = bx0 + (7.2 - 6.2) / 2.2 * (bx1 - bx0)
        g1 = bx0 + (7.8 - 6.2) / 2.2 * (bx1 - bx0)
        d.rectangle((g0, by, g1, by + 26), fill=(80, 200, 120))
        mx = bx0 + (6.8 - 6.2) / 2.2 * (bx1 - bx0)
        d.ellipse((mx - 20, by - 7, mx + 20, by + 33), fill=ORANGE, outline=(255, 255, 255), width=5)
        for v, xx in [("6,2", bx0), ("7,2", g0), ("7,8", g1), ("8,4", bx1)]:
            w = f["m22"].getlength(v)
            d.text((xx - w / 2, by + 44), v, font=f["m22"], fill=(110, 120, 140))
        d.text((g0 + 6, by - 44), "Recommended", font=f["m20"], fill=(40, 150, 80))
        if on(6):
            d.text((64, y + 330), "Increase your pH to bring it back", font=f["m26"], fill=(60, 70, 90))
            d.text((64, y + 366), "into the recommended range.", font=f["m26"], fill=(60, 70, 90))
        if on(7):
            d.rounded_rectangle((64, y + 430, SW - 64, y + 520), 45, fill=(24, 130, 240))
            w = f["n38"].getlength("Fix my pH with Noli")
            d.text((SW / 2 - w / 2, y + 450), "Fix my pH with Noli", font=f["n38"], fill=(255, 255, 255))
    y += 590
    if on(7):
        w = f["s26"].getlength("I'll take care of it myself")
        d.text((SW / 2 - w / 2, y), "I'll take care of it myself", font=f["s26"], fill=(20, 120, 230))
    _tabbar(d, 1)
    return im


def ui_guide(kind="startup"):
    """Start-up / Winterizing / problem guide screens (step list), kept to what the app offers."""
    f = _ui_fonts()
    im = Image.new("RGB", (SW, SH), (244, 248, 253))
    d = ImageDraw.Draw(im)
    title, col, steps = {
        "startup": ("Start-up", (255, 170, 30), ["Prepare your pool", "for the season"]),
        "winter": ("Winterizing", (70, 150, 255), ["Protect your pool", "during winter"]),
        "problem": ("I have a problem", RED, ["Green water?", "Cloudy water?"]),
    }[kind]
    _topbar(d, title)
    d.rounded_rectangle((36, 200, SW - 36, 640), 40, fill=col)
    noli = _noli_icon(330)
    im.paste(noli, (SW - noli.width - 50, 640 - noli.height - 20), noli)
    d = ImageDraw.Draw(im)
    d.text((76, 250), title, font=f["n64"], fill=(255, 255, 255))
    d.text((78, 340), steps[0], font=f["s30"], fill=(255, 255, 255))
    d.text((78, 382), steps[1], font=f["s30"], fill=(255, 255, 255))
    for i in range(4):
        y = 700 + i * 170
        d.rounded_rectangle((36, y, SW - 36, y + 140), 30, fill=(255, 255, 255), outline=(225, 232, 242), width=2)
        d.ellipse((66, y + 36, 134, y + 104), fill=(230, 242, 255))
        w = f["n38"].getlength(str(i + 1))
        d.text((100 - w / 2, y + 44), str(i + 1), font=f["n38"], fill=(20, 120, 230))
        d.rounded_rectangle((166, y + 44, 166 + [380, 300, 420, 260][i], y + 64), 10, fill=(214, 222, 236))
        d.rounded_rectangle((166, y + 80, 166 + [250, 330, 200, 300][i], y + 96), 8, fill=(232, 237, 245))
    _tabbar(d, 0)
    return im


@lru_cache(maxsize=2)
def phone_frame():
    """iPhone-like frame (RGBA) with a transparent screen hole; returns (frame, screen box)."""
    bw = 34
    fw, fh = SW + bw * 2, SH + bw * 2
    s = 2
    im = Image.new("RGBA", (fw * s, fh * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, fw * s - 1, fh * s - 1), 118 * s, fill=(190, 196, 205, 255))
    d.rounded_rectangle((5 * s, 5 * s, (fw - 5) * s, (fh - 5) * s), 113 * s, fill=(18, 18, 22, 255))
    d.rounded_rectangle((bw * s, bw * s, (bw + SW) * s, (bw + SH) * s), 88 * s, fill=(0, 0, 0, 0))
    im = im.resize((fw, fh), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((fw / 2 - 120, bw + 22, fw / 2 + 120, bw + 92), 35, fill=(5, 5, 8, 255))
    return np.asarray(im), (bw, bw, SW, SH)


@lru_cache(maxsize=2)
def _screen_mask():
    m = Image.new("L", (SW * 2, SH * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, SW * 2 - 1, SH * 2 - 1), 88 * 2, fill=255)
    return np.asarray(m.resize((SW, SH), Image.LANCZOS))


def phone_rgba(screen):
    """Phone with `screen` (PIL RGB SWxSH) inside, as RGBA numpy."""
    fr, (x, y, w, h) = phone_frame()
    out = fr.copy()
    sc = np.asarray(screen.convert("RGB"))
    m = _screen_mask()[..., None].astype(np.float32) / 255
    reg = out[y:y + h, x:x + w].astype(np.float32)
    rgb = reg[..., :3] * (1 - m) + sc * m
    a = np.maximum(reg[..., 3:4], m * 255)
    out[y:y + h, x:x + w] = np.concatenate([rgb, a], axis=2).astype(np.uint8)
    # glass glare
    return out


def screen_zoom(screen, cx, cy, z):
    """Crop of a screen around (cx, cy) in screen px, zoomed z, as an RGB full frame (for 'screen recording' close-ups)."""
    sc = np.asarray(screen.convert("RGB"))
    s = max(W / SW, H / SH) * z
    M = np.array([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]], np.float32)
    return cv2.warpAffine(sc, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def put_phone(fr, screen, cx, cy, scale, rot=0.0, tilt=0.0, alpha=1.0, shadow=0.6):
    """Phone on the frame; tilt = fake 3D yaw (-1..1) through a perspective warp."""
    ph = phone_rgba(screen)
    if abs(tilt) > 0.01:
        h, w = ph.shape[:2]
        k = tilt * 0.12
        src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        dst = np.float32([[0, h * max(k, 0)], [w, h * max(-k, 0)], [w, h - h * max(-k, 0)], [0, h - h * max(k, 0)]])
        dst[:, 0] = dst[:, 0] * (1 - abs(k) * 0.8) + (w * abs(k) * 0.4)
        ph = cv2.warpPerspective(ph, cv2.getPerspectiveTransform(src, dst), (w, h), flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    paste(fr, ph, cx, cy, scale, rot, alpha, shadow=shadow)
    return fr


# ------------------------------------------------------------------ green-screen phone composite (UGC POV shots)
@lru_cache(maxsize=8)
def green_quad(path):
    im = load_np(path).astype(np.int16)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    m = ((g > 150) & (g - r > 60) & (g - b > 60)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    hull = cv2.convexHull(c)
    eps = 0.02 * cv2.arcLength(hull, True)
    q = cv2.approxPolyDP(hull, eps, True).reshape(-1, 2).astype(np.float32)
    if len(q) != 4:
        rr = cv2.minAreaRect(c)
        q = cv2.boxPoints(rr).astype(np.float32)
    s = q.sum(axis=1)
    dd = np.diff(q, axis=1).ravel()
    quad = np.float32([q[np.argmin(s)], q[np.argmin(dd)], q[np.argmax(s)], q[np.argmax(dd)]])   # tl tr br bl
    # soft key matte (also keeps fingers in front of the screen)
    gm = np.clip(((g - np.maximum(r, b)) - 30) / 60.0, 0, 1).astype(np.float32)
    gm = cv2.GaussianBlur(gm, (3, 3), 0)
    return quad, gm


def keyed_screen(path, screen):
    """The POV photo with `screen` (PIL) warped into its green phone screen. Returns the image at its own size."""
    base = load_np(path).astype(np.float32)
    quad, gm = green_quad(path)
    sc = np.asarray(screen.convert("RGB")).astype(np.float32)
    src = np.float32([[0, 0], [SW, 0], [SW, SH], [0, SH]])
    Mp = cv2.getPerspectiveTransform(src, quad)
    warped = cv2.warpPerspective(sc, Mp, (base.shape[1], base.shape[0]), flags=cv2.INTER_LINEAR)
    m = gm[..., None]
    out = base * (1 - m) + warped * m
    # de-spill the green fringe on the phone edges
    g = out[..., 1]
    lim = np.maximum(out[..., 0], out[..., 2]) + 12
    out[..., 1] = np.where((g > lim) & (m[..., 0] < 0.9), lim, g)
    return out.astype(np.uint8)


def cover_np(im, t=0.0, d=1.0, z0=1.0, z1=1.08, fx=0.5, fy=0.5, rot=0.0, shake=0.0):
    ih, iw = im.shape[:2]
    k = ease_io(t / d) if d > 0 else 1
    z = lerp(z0, z1, k)
    s = max(W / iw, H / ih) * z
    cx, cy = fx * iw, fy * ih
    hw, hh = W / 2 / s, H / 2 / s
    cx = clamp(cx, hw, iw - hw)
    cy = clamp(cy, hh, ih - hh)
    ox, oy = W / 2, H / 2
    if shake:
        ox += shake * (math.sin(t * 13.0) * 6 + math.sin(t * 31.0) * 3)
        oy += shake * (math.cos(t * 11.0) * 6 + math.cos(t * 27.0) * 3)
    M = cv2.getRotationMatrix2D((cx, cy), rot, s)
    M[0, 2] += ox - cx
    M[1, 2] += oy - cy
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


# ------------------------------------------------------------------ particles
def bubbles(fr, t, n=26, seed=3, color=(220, 245, 255), alpha=0.6, speed=180, size=(6, 22), region=(0, W, 0, H)):
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = region
    for i in range(n):
        x = rng.uniform(x0, x1)
        r = rng.uniform(*size)
        ph = rng.uniform(0, 1)
        sp = speed * rng.uniform(0.6, 1.4)
        y = y1 - ((ph * (y1 - y0) + t * sp) % (y1 - y0))
        x += math.sin(t * 2 + i) * 10
        cv2.circle(fr, (int(x), int(y)), int(r), (*color,), 3, cv2.LINE_AA)
    return fr


def sparkles(fr, t, pts, color=(255, 255, 255), size=40):
    for i, (x, y, t0) in enumerate(pts):
        k = (t - t0) / 0.5
        if 0 < k < 1:
            s = math.sin(k * math.pi) * size
            for ang in (0, 90):
                a = math.radians(ang + k * 45)
                cv2.line(fr, (int(x - s * math.cos(a)), int(y - s * math.sin(a))), (int(x + s * math.cos(a)), int(y + s * math.sin(a))),
                         color, 5, cv2.LINE_AA)
    return fr


def splash_drops(fr, t, cx, cy, n=18, seed=5, color=(170, 230, 255), power=1.0):
    """Droplets thrown up from (cx, cy) at t=0, falling with gravity."""
    if t < 0 or t > 1.2:
        return fr
    rng = np.random.default_rng(seed)
    for i in range(n):
        ang = rng.uniform(-math.pi * 0.9, -math.pi * 0.1)
        v = rng.uniform(500, 1300) * power
        x = cx + math.cos(ang) * v * t
        y = cy + math.sin(ang) * v * t + 1800 * t * t
        r = rng.uniform(6, 16) * (1 - t / 1.3)
        if r > 1:
            cv2.ellipse(fr, (int(x), int(y)), (int(r), int(r * 1.3)), 0, 0, 360, color, -1, cv2.LINE_AA)
            cv2.circle(fr, (int(x - r * 0.3), int(y - r * 0.4)), max(1, int(r * 0.3)), (255, 255, 255), -1, cv2.LINE_AA)
    return fr


# ------------------------------------------------------------------ transitions
TR_SFX = {"whip": "swoosh-fast", "zoom": "tunnel", "flash": "shutter", "splash": "splash", "glitch": "glitch-hit",
          "ripple": "whoosh2", "slide": "swoosh", "cut": None, "drop": "splash", "dip": "whoosh"}
TR_LEN = {"whip": 0.22, "zoom": 0.28, "flash": 0.2, "splash": 0.36, "glitch": 0.2, "ripple": 0.36, "slide": 0.3, "cut": 0.0,
          "drop": 0.36, "dip": 0.3}


def transition(kind, a, b, k, n):
    """Blend frame a (outgoing) into b (incoming), k 0..1."""
    if kind == "whip":
        off = int(W * ease_io(k))
        out = np.empty_like(b)
        out[:, :W - off] = a[:, off:]
        out[:, W - off:] = b[:, :off]
        bl = int(60 * math.sin(k * math.pi)) | 1
        return cv2.blur(out, (bl, 1)) if bl > 1 else out
    if kind == "slide":
        off = int(H * ease_io(k))
        out = np.empty_like(b)
        out[:H - off] = a[off:]
        out[H - off:] = b[:off]
        bl = int(50 * math.sin(k * math.pi)) | 1
        return cv2.blur(out, (1, bl)) if bl > 1 else out
    if kind == "zoom":
        if k < 0.5:
            z = 1 + ease_in(k * 2) * 1.2
            M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
            return cv2.warpAffine(a, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        z = 1.6 - ease_out((k - 0.5) * 2) * 0.6
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
        return cv2.warpAffine(b, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    if kind == "flash":
        base = a if k < 0.4 else b
        w = 1 - abs(k - 0.4) / 0.6 if k > 0.4 else k / 0.4
        return base * (1 - w) + 255 * w
    if kind == "dip":
        base = a if k < 0.5 else b
        w = 1 - abs(k - 0.5) * 2
        return base * (1 - w)
    if kind == "glitch":
        base = (a if k < 0.5 else b).copy()
        rng = np.random.default_rng(n)
        for _ in range(9):
            y0 = rng.integers(0, H - 80)
            hh = rng.integers(20, 140)
            base[y0:y0 + hh] = np.roll(base[y0:y0 + hh], rng.integers(-90, 90), axis=1)
        base[..., 0] = np.roll(base[..., 0], 14, axis=1)
        base[..., 2] = np.roll(base[..., 2], -14, axis=1)
        return base
    if kind in ("splash", "ripple", "drop"):
        # a circle of water opens from the centre (or a ripple ring) revealing b
        r = ease_out(k) * math.hypot(W, H) * 0.62
        y, x = np.ogrid[:H, :W]
        cx, cy = W / 2, H * 0.48
        wob = 26 * np.sin(np.arctan2(y - cy, x - cx) * 9 + k * 6)
        d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) + wob
        m = np.clip((r - d) / 18, 0, 1).astype(np.float32)[..., None]
        out = a * (1 - m) + b * m
        out = ripple_warp(out.astype(np.float32), cx, cy, r, amp=40 * (1 - k), width=70)
        edge = np.exp(-((d - r) / 14) ** 2).astype(np.float32)[..., None] * 0.7 * (1 - k * 0.6)
        return out * (1 - edge) + 255 * edge
    return b


# ------------------------------------------------------------------ voice + timing
def prepare_voice(wav, work, max_gap=0.3, speed=1.0, fixes=None, extra=None):
    """Whisper words of the take, then squeeze every pause longer than max_gap down to max_gap.
    Returns (voice array, words [(text, start, end)])."""
    work.mkdir(parents=True, exist_ok=True)
    src = work / "voice_src.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(HERE / wav), "-af", f"atempo={speed}", "-ar", str(SR), "-ac", "2", str(src)], check=True)
    cache = work / "whisper.json"
    key = f"{wav}:{(HERE / wav).stat().st_mtime}:{speed}"
    if cache.exists() and json.loads(cache.read_text()).get("key") == key:
        words = json.loads(cache.read_text())["words"]
    else:
        from faster_whisper import WhisperModel
        mono = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                            capture_output=True).stdout, np.float32)
        segs, _ = WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(mono, word_timestamps=True, language="en")
        words = [[w.word.strip(), w.start, w.end] for s in segs for w in (s.words or [])]
        cache.write_text(json.dumps({"key": key, "words": words}))
    voice = read_audio(src)
    # cut long pauses (keep max_gap), with short fades at the seams
    pieces, cursor, shift, out_words = [], 0.0, 0.0, []
    lead = 0.02
    for i, (w, s, e) in enumerate(words):
        if i:
            gap = s - words[i - 1][2]
            if gap > max_gap:
                cut0 = words[i - 1][2] + max_gap / 2
                cut1 = s - max_gap / 2
                pieces.append(voice[int(cursor * SR):int(cut0 * SR)])
                cursor = cut1
                shift += cut1 - cut0
            if extra and i in extra:   # breathing room before this word (signature moments)
                cut = (words[i - 1][2] + s) / 2
                if cut > cursor:
                    pieces.append(voice[int(cursor * SR):int(cut * SR)])
                    cursor = cut
                pieces.append(np.zeros((int(extra[i] * SR), 2), np.float32))
                shift -= extra[i]
        out_words.append([w, s - shift, e - shift])
    pieces.append(voice[int(cursor * SR):])
    xf = int(0.01 * SR)
    for p in pieces[1:]:
        if len(p) > xf:
            p[:xf] *= np.linspace(0, 1, xf)[:, None]
    for p in pieces[:-1]:
        if len(p) > xf:
            p[-xf:] *= np.linspace(1, 0, xf)[:, None]
    voice = np.concatenate(pieces) if pieces else voice
    fixes = fixes or {}
    out_words = [[fixes.get(w, w), s, e] for w, s, e in out_words]
    return voice, out_words


# ------------------------------------------------------------------ captions
def phrase_groups(words, max_words=3):
    groups, cur = [], []
    for i, (w, s, e) in enumerate(words):
        cur.append(i)
        if len(cur) >= max_words or w[-1] in ".,?!" or (i + 1 < len(words) and words[i + 1][1] - e > 0.35):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def make_captions(font, size, y, color=WHITE, key=CYAN, stroke=10, stroke_color=NAVY, shadow=6, upper=False, max_words=3,
                  mode="phrase", box=None, keys=(), strip=".,", track=0):
    """Caption overlay fn(fr, words, t, shot, shot_start).
    mode 'phrase': the 1-3 word phrase with the spoken word in `key` colour; 'word': one word at a time (UGC pop).
    box: colour of a rounded highlight box behind the active word (TikTok style). keys: words always in key colour."""
    cache = {}

    def fn(fr, words, t, shot, s0):
        if id(words) not in cache:
            cache[id(words)] = phrase_groups(words, 1 if mode == "word" else max_words)
        groups = cache[id(words)]
        cy = shot.get("cap_y", y) if isinstance(shot, dict) else y
        for gi, g in enumerate(groups):
            g0 = words[g[0]][1] - 0.05
            g1 = (words[groups[gi + 1][0]][1] - 0.05) if gi + 1 < len(groups) else words[g[-1]][2] + 0.5
            g1 = min(g1, words[g[-1]][2] + 0.6)
            if not (g0 <= t < g1):
                continue
            if g0 < s0 - 0.01 and t - s0 < 0.05:
                pass
            toks = []
            for i in g:
                w = words[i][0].strip(strip) if strip else words[i][0]
                toks.append((w.upper() if upper else w, i))
            sp = max(text_w(" ", font, size), size * 0.27) + stroke * 1.6 + 4 + (30 if box is not None else 0)
            ws = [text_w(w, font, size, track) for w, _ in toks]
            tot = sum(ws) + sp * (len(ws) - 1)
            sc = 1.0
            if tot > W - 120:
                sc = (W - 120) / tot
            x = W / 2 - tot * sc / 2
            pop = ease_back((t - g0) / 0.18, 2.0)
            for (w, i), ww in zip(toks, ws):
                active = words[i][1] - 0.05 <= t
                cur = active and (i == g[-1] or t < words[i + 1][1] - 0.05)
                is_key = w.strip("?!.,").lower() in keys
                col = key if (cur and box is None) or is_key else color
                if box is not None and cur:
                    bw_, bh_ = ww * sc + 34, size * 1.24 * sc
                    bx = Image.new("RGBA", (int(bw_), int(bh_)), (0, 0, 0, 0))
                    ImageDraw.Draw(bx).rounded_rectangle((0, 0, bw_ - 1, bh_ - 1), int(size * 0.22), fill=(*box, 255))
                    bpop = ease_back((t - words[i][1] + 0.05) / 0.14, 2.4) if mode == "build" else pop
                    paste(fr, np.asarray(bx), x + ww * sc / 2, cy + size * 0.08 * sc, max(bpop, 0.01))
                lay = text_im(w, font, size, col, stroke, stroke_color, shadow, track)
                s_ = sc * (max(pop, 0.01) if mode == "word" or gi >= 0 else 1)
                if mode == "build":   # each word pops on as it is spoken
                    s_ = sc * max(ease_back((t - words[i][1] + 0.05) / 0.14, 2.4), 0.01)
                if cur and mode == "phrase":
                    s_ *= 1.06
                paste(fr, lay, x + ww * sc / 2, cy, s_, alpha=1.0 if active or mode == "phrase" else 0.0)
                x += (ww + sp) * sc
            break
    return fn


# ------------------------------------------------------------------ render
def render(spec):
    """spec: dict(name, voice, shots, caption=fn(fr, words_in_view, t), music=[(t_or_shot, file, start, vol)], sfx=[...],
    max_gap, speed, tail, fixes, post=fn(fr, t, n))."""
    name = spec["name"]
    work = HERE / "work" / name
    voice, words = prepare_voice(spec["voice"], work, spec.get("max_gap", 0.3), spec.get("speed", 1.0), spec.get("fixes"), spec.get("extra"))
    for i, (w, s, e) in enumerate(words):
        print(f"{i}:{w}[{s:.2f}]", end="  ")
    print()
    shots = spec["shots"]
    lead = 0.06
    starts = []
    for sh in shots:
        if "w" in sh:
            starts.append(max(0.0, words[sh["w"]][1] - lead) if sh["w"] else 0.0)
        else:
            starts.append(words[-1][2] + sh["after"])
    total = starts[-1] + shots[-1]["dur"]
    ends = starts[1:] + [total]
    print("shots:")
    for i, (sh, s, e) in enumerate(zip(shots, starts, ends)):
        print(f"  {i:2d} {s:6.2f} {e - s:5.2f}s  {sh['scene'].__name__:18s} {sh.get('tr', 'cut')}")
    if "--plan" in sys.argv:
        return
    # ---------------- audio
    n = int(total * SR) + SR
    vo = np.zeros((n, 2), np.float32)
    vo[:len(voice)] = voice[:n] * spec.get("voice_gain", 1.0)
    mix = vo.copy()
    music = np.zeros_like(vo)
    cues = spec.get("music", [])
    xf = int(0.08 * SR)
    for k, cue in enumerate(cues):
        at = lambda c: c["t"] if "t" in c else starts[c["shot"]] + c.get("offset", 0.0)  # noqa: E731
        t0 = at(cue)
        t1 = at(cues[k + 1]) if k + 1 < len(cues) else total + 1
        seg = read_audio(HERE / cue["file"], start=cue.get("start", 0.0), dur=t1 - t0 + 0.3) * cue.get("vol", 1.0)
        a = int(t0 * SR)
        if k:
            seg[:xf] *= np.linspace(0, 1, xf)[:, None]
        seg[-xf:] *= np.linspace(1, 0, xf)[:, None] if k + 1 < len(cues) else 1
        e = min(a + len(seg), n)
        music[a:e] += seg[:e - a]
    # duck under the voice
    env = np.abs(vo).mean(axis=1)
    hop = 441
    fr_ = env[:len(env) // hop * hop].reshape(-1, hop).max(axis=1)
    g, lvl = np.empty_like(fr_), 0.0
    for i, v in enumerate(fr_):
        lvl = max(v, lvl * 0.9)
        g[i] = spec.get("duck", 0.38) if lvl > 0.02 else 1.0
    g = np.convolve(g, np.ones(10) / 10, "same")
    gain = np.concatenate([np.repeat(g, hop), np.ones(n - len(g) * hop)])
    fo = int(spec.get("music_fade", 0.8) * SR)
    end_i = int(total * SR)
    gain[end_i - fo:end_i] *= np.linspace(1, 0, fo)
    gain[end_i:] = 0
    music *= gain[:, None] * spec.get("music_volume", 0.32)
    write_wav(work / "music.wav", music[:end_i])
    mix += music
    sfx_list = []
    for si, sh in enumerate(shots):
        tr = sh.get("tr", "cut")
        if si and TR_SFX.get(tr) and sh.get("tr_sfx", True):
            sfx_list.append((TR_SFX[tr], starts[si] + TR_LEN[tr] * 0.35, sh.get("tr_gain", 0.8)))
        for c in sh.get("sfx", []):
            c = {"name": c} if isinstance(c, str) else c
            sfx_list.append((c["name"], starts[si] + c.get("at", 0.0), c.get("gain", 1.0)))
    for name_, at, gg in sfx_list:
        f, peak, pre, post, bg = SFX[name_]
        pre = min(pre, peak, max(at, 0))
        clip = read_audio(f, start=peak - pre, dur=pre + post)
        fade = min(len(clip), int(0.1 * SR))
        clip[-fade:] *= np.linspace(1, 0, fade)[:, None]
        s = int((at - pre) * SR)
        e = min(s + len(clip), n)
        if e > s >= 0:
            mix[s:e] += clip[:e - s] * bg * gg
    mix = mix[:end_i]
    pk = np.abs(mix).max()
    if pk > 0.98:
        mix *= 0.98 / pk
    write_wav(work / "mix.wav", mix, af="loudnorm=I=-14:TP=-1.5:LRA=11")
    (work / "timeline.json").write_text(json.dumps({"total": total, "starts": starts, "words": words,
                                                    "sfx": [(a, round(b, 2)) for a, b, _ in sfx_list]}, indent=1))
    # ---------------- video
    out = HERE / "output" / f"{name}.mp4"
    out.parent.mkdir(exist_ok=True)
    nframes = int(total * FPS)
    only = None
    if "--stills" in sys.argv:
        only = sorted({int((s + (e - s) * 0.6) * FPS) for s, e in zip(starts, ends)} |
                      {int((s + 0.12) * FPS) for s in starts[1:]})
    ctx = {"words": words, "starts": starts, "ends": ends, "total": total}

    def frame(nf):
        t = nf / FPS
        si = max(i for i, s in enumerate(starts) if s <= t + 1e-9)
        sh = shots[si]
        fr = sh["scene"](max(0.0, t - starts[si]), ends[si] - starts[si], sh.get("a", {}), ctx).astype(np.float32)
        tr = sh.get("tr", "cut")
        L = TR_LEN.get(tr, 0)
        if si and L and t - starts[si] < L:
            p = shots[si - 1]
            a = p["scene"](t - starts[si - 1], ends[si - 1] - starts[si - 1], p.get("a", {}), ctx).astype(np.float32)
            fr = transition(tr, a, fr, (t - starts[si]) / L, nf).astype(np.float32)
        if sh.get("cap", True) and spec.get("caption"):
            spec["caption"](fr, words, t, sh, starts[si])
        if spec.get("post"):
            fr = spec["post"](fr, t, nf)
        return np.clip(fr, 0, 255).astype(np.uint8)

    if "--frame" in sys.argv:
        for tt in sys.argv[sys.argv.index("--frame") + 1].split(","):
            Image.fromarray(frame(int(float(tt) * FPS))).save(work / f"frame_{tt}.jpg", quality=90)
            print(work / f"frame_{tt}.jpg")
        return
    if only is not None:
        ims = [Image.fromarray(frame(k)).resize((270, 480)) for k in only]
        cols = 10
        rows = (len(ims) + cols - 1) // cols
        S = Image.new("RGB", (270 * cols, 480 * rows))
        d = ImageDraw.Draw(S)
        for i, (im, k) in enumerate(zip(ims, only)):
            S.paste(im, ((i % cols) * 270, (i // cols) * 480))
            d.text(((i % cols) * 270 + 6, (i // cols) * 480 + 4), f"{k / FPS:.2f}", fill=(255, 255, 0))
        S.save(work / "stills.jpg", quality=85)
        print(work / "stills.jpg")
        return
    jobs = int(spec.get("jobs", 4))
    import multiprocessing as mp
    bounds = [nframes * k // jobs for k in range(jobs + 1)]
    parts = [work / f"part{k}.mp4" for k in range(jobs)]

    def worker(k):
        p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", str(parts[k])],
                             stdin=subprocess.PIPE)
        for nf in range(bounds[k], bounds[k + 1]):
            p.stdin.write(frame(nf).tobytes())
        p.stdin.close()
        p.wait()
    ctx_mp = mp.get_context("fork")
    procs = [ctx_mp.Process(target=worker, args=(k,)) for k in range(jobs)]
    [p.start() for p in procs]
    [p.join() for p in procs]
    lst = work / "parts.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(work / "mix.wav"), "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
    for p in parts:
        p.unlink()
    print(out, f"{total:.2f}s")
