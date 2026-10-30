"""Render a long-form 16:9 video (1920x1080, 30 fps) for the psychology channel: AI line-art images, stock video,
motion graphics, transitions and retention-style sound design, frame by frame.

Usage: python3 make_long.py path/to/video.json [--preview] [--from S --to E]
  --preview  half resolution, fast encode (check timing/framing quickly)
  --from/--to render only that part of the timeline (seconds), for QA of one section

video.json (relative paths resolve against its folder):
{
  "out": "../output/my-video.mp4",
  "audio": "voice.wav", "speed": 1.0,
  "music_cues": [{"shot": 0, "music": "../../reels/audio/music/echoes.mp3", "start": 162.865}, ...],   # as in reels
  "music_volume": 0.35, "fade_out": 1.2, "progress": true,
  "shots": [{
    "text": "Exact words spoken during this shot.",          # verbatim and consecutive, like reels
    "v": {"img": "img/a.jpg", "focus": [x, y], "zoom": 1.1, "drift": 0.06,           # AI image / photo
          "to": [x, y], "to_zoom": 1.6, "spin": 2}                                   # optional camera move over the shot
       | {"video": "stock/a.mp4", "start": 2.0, "zoom": 1.05, "drift": 0.04, "focus": [x, y], "rate": 1.0}
       | {"mg": "<motion graphic name>", ...params},                                  # full-screen motion graphic
    "in": "cut" | "whip" | "zoom" | "flash" | "glitch" | "dip",                       # transition into this shot
    "punch": {"at": "@word", "zoom": 1.8, "focus": [x, y]},                           # fast push-in at a word
    "shake": ["@word", 0.0],                                                          # camera shake hits
    "fx": ["vhs"] | [{"name": "light_off", "at": "@off"}],
    "overlays": [{"mg": "lower_third", "at": "@Cornell", "title": "...", "sub": "..."}, ...],
    "captions": true,
    "sfx": ["whoosh", {"name": "pop", "at": "@word", "gain": 0.8}],                   # names: SFX table
    "amb": {"name": "crowd-murmur", "gain": 0.12},                                    # ambience bed under the shot
    "music_fx": "muffle",                                                             # low-pass the music during the shot
    "voice_fx": {"at": "@not", "fx": "echo"},                                          # echo tail on a word
    "pause_before": 0.25
  }]
}
Times in "at" are seconds after the cut, or "@word" (first word in the shot's text starting with it), or "@word+0.2".
"""
import argparse
import json
import math
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.signal import butter, sosfilt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "reels"))
from make_reel import SFX as REEL_SFX, align, music_bed, norm, read_audio, write_wav  # noqa: E402
from fonts import emoji_image, font  # noqa: E402

W, H, FPS, SR = 1920, 1080, 30, 44100
LEAD, TAIL = 0.12, 1.2
YELLOW = (255, 214, 10)
RED = (235, 50, 50)
WHITE = (245, 245, 245)
ANTON = str(HERE / "fonts" / "Anton-Regular.ttf")
INTER = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
if not Path(INTER).exists():
    INTER = INTER_SB = font("bold")

# name: (file, peak s into file, pre, post, gain) -- peak lands on the cue time
SFX = {k: (HERE.parent / "reels" / "audio" / "sfx" / v[0], *v[1:]) for k, v in REEL_SFX.items()}
LS = HERE / "sfx"
SFX.update({
    "switch":     (LS / "switch-pull.mp3", 0.43, 0.43, 0.6, 1.0),
    "click":      (LS / "switch-tap.mp3", 0.0, 0.0, 0.5, 1.0),
    "tick":       (LS / "tick.mp3", 0.0, 0.0, 0.12, 0.6),
    "typing":     (LS / "typing.mp3", 1.01, 0.0, 1.2, 0.5),
    "shutter":    (LS / "shutter.mp3", 0.19, 0.06, 0.2, 0.9),
    "sweep":      (LS / "sweep.mp3", 0.29, 0.16, 0.45, 0.8),
    "swoosh":     (LS / "swoosh-short.mp3", 0.16, 0.12, 0.8, 0.8),
    "swoosh-fast": (LS / "swoosh-fast.mp3", 0.11, 0.08, 0.45, 0.8),
    "trailer":    (LS / "whoosh-trailer.mp3", 1.06, 0.6, 0.3, 0.8),
    "reveal":     (LS / "reveal.mp3", 0.18, 0.15, 2.0, 0.7),
    "boom":       (LS / "boom.mp3", 0.93, 0.5, 3.5, 0.9),
    "tunnel":     (LS / "tunnel-woosh.mp3", 0.62, 0.32, 1.6, 0.6),
    "glitch-hit": (LS / "glitch-hit.mp3", 0.11, 0.1, 1.6, 0.6),
    "glass":      (LS / "glass-hit.mp3", 0.2, 0.16, 3.0, 0.7),
    "zap":        (LS / "electric-glitch.mp3", 0.3, 0.3, 0.6, 0.6),
})
AMB = {"crowd-murmur": LS / "crowd-murmur.mp3"}


# ---------------------------------------------------------------- drawing helpers
def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def ease_back(x):
    x = min(max(x, 0.0), 1.0)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


@lru_cache(maxsize=256)
def text_layer(text, path, size, color=WHITE, glow=0, stroke=0, track=0):
    """RGBA numpy layer of one line of text; glow = blur radius of a coloured halo; stroke = black outline px."""
    f = ImageFont.truetype(path, size)
    widths = [f.getlength(ch) + track for ch in text] if track else None
    tw = int(sum(widths) if track else f.getlength(text)) + 2
    asc, desc = f.getmetrics()
    pad = glow * 3 + stroke + 8
    im = Image.new("RGBA", (tw + pad * 2, asc + desc + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def draw(dd, fill, sw=0, sf=None):
        if track:
            x = pad
            for ch, w in zip(text, widths):
                dd.text((x, pad), ch, font=f, fill=fill, stroke_width=sw, stroke_fill=sf)
                x += w
        else:
            dd.text((pad, pad), text, font=f, fill=fill, stroke_width=sw, stroke_fill=sf)
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        draw(ImageDraw.Draw(g), (*color[:3], 255))
        g = g.filter(ImageFilter.GaussianBlur(glow))
        im = Image.alpha_composite(im, g)
        im = Image.alpha_composite(im, g)
        d = ImageDraw.Draw(im)
    draw(d, (*color[:3], 255), stroke, (0, 0, 0, 255) if stroke else None)
    return np.asarray(im)


def blit(fr, layer, cx, cy, scale=1.0, alpha=1.0, anchor="c"):
    """Alpha-blend an RGBA layer onto the RGB frame, centred at (cx, cy) px (anchor 'l' = left edge at cx)."""
    if alpha <= 0.003 or scale <= 0.01:
        return
    if abs(scale - 1) > 0.003:
        layer = cv2.resize(layer, (max(1, int(layer.shape[1] * scale)), max(1, int(layer.shape[0] * scale))),
                           interpolation=cv2.INTER_LINEAR)
    lh, lw = layer.shape[:2]
    x0 = int(cx - (0 if anchor == "l" else lw / 2))
    y0 = int(cy - lh / 2)
    fx0, fy0, fx1, fy1 = max(x0, 0), max(y0, 0), min(x0 + lw, fr.shape[1]), min(y0 + lh, fr.shape[0])
    if fx1 <= fx0 or fy1 <= fy0:
        return
    sub = layer[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0].astype(np.float32)
    a = sub[..., 3:4] / 255.0 * alpha
    reg = fr[fy0:fy1, fx0:fx1].astype(np.float32)
    fr[fy0:fy1, fx0:fx1] = (reg * (1 - a) + sub[..., :3] * a).astype(np.uint8)


def rect(fr, x0, y0, x1, y1, color, alpha=1.0):
    x0, y0, x1, y1 = [int(round(v)) for v in (x0, y0, x1, y1)]
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, fr.shape[1]), min(y1, fr.shape[0])
    if x1 <= x0 or y1 <= y0:
        return
    reg = fr[y0:y1, x0:x1].astype(np.float32)
    fr[y0:y1, x0:x1] = (reg * (1 - alpha) + np.array(color, np.float32) * alpha).astype(np.uint8)


@lru_cache(maxsize=64)
def person_icon(h, color, alpha=255):
    """Simple person pictogram (head + rounded body), RGBA, height h."""
    s = 4
    w = int(h * 0.55)
    im = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = (*color, alpha)
    r = h * s * 0.17
    d.ellipse([w * s / 2 - r, 0, w * s / 2 + r, 2 * r], fill=c)
    d.rounded_rectangle([w * s * 0.08, 2 * r + h * s * 0.05, w * s * 0.92, h * s], radius=int(w * s * 0.38), fill=c)
    return np.asarray(im.resize((w, h), Image.Resampling.LANCZOS))


def glow_layer(layer, radius=18):
    im = Image.fromarray(layer).filter(ImageFilter.GaussianBlur(radius))
    return np.asarray(im)


# ---------------------------------------------------------------- motion graphics
# Each takes (fr, t, d, p, ctx): fr = RGB frame to draw on, t = seconds since it started, d = its length,
# p = its params, ctx = shot context (word times relative to the shot, etc.).

def mg_kinetic(fr, t, d, p, ctx):
    """Big words slamming in one by one, centred; p: lines [[text, color], ...], "times": ["@word", ...]."""
    lines = p["lines"]
    times = [ctx.at(x) for x in p.get("times", [0.0] * len(lines))]
    size = p.get("size", 150)
    gap = size * 1.15
    y0 = H / 2 - gap * (len(lines) - 1) / 2 + p.get("dy", 0)
    for k, ((txt, col), t0) in enumerate(zip(lines, times)):
        lt = t - t0
        if lt < 0:
            continue
        col = YELLOW if col == "yellow" else RED if col == "red" else WHITE
        lay = text_layer(txt, ANTON, size, col, glow=12 if col != WHITE else 0, track=4)
        s = 1.0 + 0.5 * (1 - ease_out(lt / 0.18)) + 0.03 * t / max(d, 1)
        blit(fr, lay, W / 2, y0 + gap * k, scale=s, alpha=min(1, lt / 0.08))


def mg_title(fr, t, d, p, ctx):
    """Section title: tracking tightens, scale settles, a light sweep crosses once. p: text, sub, y."""
    y = p.get("y", 0.5) * H
    lay = text_layer(p["text"], ANTON, p.get("size", 140), YELLOW, glow=16, track=6)
    s = 0.85 + 0.15 * ease_back(t / 0.45) + 0.02 * t
    a = min(1, t / 0.12)
    # dark band behind for legibility
    rect(fr, 0, y - lay.shape[0] * 0.55, W, y + lay.shape[0] * 0.55 + (60 if p.get("sub") else 0), (0, 0, 0), 0.45 * a)
    sw = (t - 0.35) / 0.6
    if 0 < sw < 1:   # light sweep: brighten a diagonal band of the text
        lay = lay.copy()
        xs = np.arange(lay.shape[1])[None, :] + np.arange(lay.shape[0])[:, None] * 0.4
        band = np.clip(1 - np.abs(xs - sw * (lay.shape[1] + 200)) / 70, 0, 1)[..., None]
        rgb = lay[..., :3].astype(np.float32)
        lay = np.concatenate([np.clip(rgb + band * 200, 0, 255).astype(np.uint8), lay[..., 3:]], axis=2)
    blit(fr, lay, W / 2, y, scale=s, alpha=a)
    if p.get("sub") and t > 0.4:
        sub = text_layer(p["sub"], INTER_SB, 40, WHITE, track=6)
        blit(fr, sub, W / 2, y + lay.shape[0] * 0.5 + 18, alpha=min(1, (t - 0.4) / 0.25))


def mg_year(fr, t, d, p, ctx):
    """Year counter rolling back from p.from to p.to, with a label; sepia-dark background."""
    fr[:] = (18, 14, 10)
    k = ease_out(t / p.get("roll", 0.9))
    yr = round(p["from"] + (p["to"] - p["from"]) * k)
    lay = text_layer(str(yr), ANTON, 300, YELLOW if k >= 1 else WHITE, glow=20 if k >= 1 else 0, track=10)
    blit(fr, lay, W / 2, H * 0.46, scale=1.0 + (0.08 * (1 - ease_out((t - p.get("roll", 0.9)) / 0.25)) if k >= 1 else 0))
    if p.get("label"):
        lab = text_layer(p["label"], INTER_SB, 44, (200, 190, 170), track=10)
        blit(fr, lab, W / 2, H * 0.72, alpha=min(1, t / 0.3))
    # film scratches
    rng = np.random.default_rng(int(t * FPS))
    for _ in range(2):
        x = int(rng.uniform(0, W))
        rect(fr, x, 0, x + 2, H, (120, 110, 95), 0.25)


def grid_people(fr, t, d, p, ctx, cx=W / 2, cy=H * 0.40, cols=10, rows=2, h=150):
    n = cols * rows
    lit = p.get("lit", 0)
    if isinstance(lit, list) and len(lit) == 2:
        lit = lit + [0.0, d]
    if isinstance(lit, list):   # [from, to, "@start", "@end"] animate
        a, b = lit[0], lit[1]
        t0, t1 = ctx.at(lit[2]), ctx.at(lit[3])
        lit = a + (b - a) * ease_io((t - t0) / max(t1 - t0, 0.01))
    gapx, gapy = h * 0.75, h * 1.18
    x0 = cx - gapx * (cols - 1) / 2
    y0 = cy - gapy * (rows - 1) / 2
    dim = person_icon(h, (90, 90, 90))
    on = person_icon(h, YELLOW)
    for i in range(n):
        x, y = x0 + gapx * (i % cols), y0 + gapy * (i // cols)
        appear = min(1, max(0, (t - i * 0.02) / 0.15))
        blit(fr, dim, x, y, alpha=appear)
        f = min(1, max(0, lit - i))
        if f > 0:
            blit(fr, glow_layer(on, 10), x, y, alpha=0.6 * f)
            blit(fr, on, x, y, alpha=f, scale=1 + 0.12 * (1 - ease_out(f)))
    return lit


def mg_grid(fr, t, d, p, ctx):
    """2x10 people grid; p: lit (number or [from, to, "@a", "@b"]), label, pct (number or [from, to, "@a", "@b"]),
    "question": true shows a big pulsing '?'."""
    fr[:] = (8, 8, 10)
    grid_people(fr, t, d, p, ctx, cy=H * p.get("cy", 0.33), cols=p.get("cols", 10), rows=p.get("rows", 2), h=p.get("h", 150))
    if p.get("question"):
        fr[:] = (fr.astype(np.float32) * 0.3).astype(np.uint8)
        s = 1 + 0.06 * math.sin(t * 9)
        blit(fr, text_layer("?", ANTON, 380, YELLOW, glow=24), W / 2, H * 0.40, scale=s * ease_back(t / 0.3))
    if p.get("label"):
        blit(fr, text_layer(p["label"], INTER_SB, 46, WHITE, track=8), W / 2, H * 0.08, alpha=min(1, t / 0.2))
    pct = p.get("pct")
    if pct is not None:
        if isinstance(pct, list):
            a, b = pct[0], pct[1]
            t0, t1 = ctx.at(pct[2]), ctx.at(pct[3])
            v = a + (b - a) * ease_out((t - t0) / max(t1 - t0, 0.01))
            done = t >= t1
        else:
            v, done = pct, True
        lay = text_layer(f"{round(v)}%", ANTON, 170, YELLOW, glow=14 if done else 0)
        pop = 1 + 0.1 * (1 - ease_out((t - (ctx.at(pct[3]) if isinstance(pct, list) else 0)) / 0.2))
        blit(fr, lay, W / 2, H * 0.65, scale=pop)


def mg_bars(fr, t, d, p, ctx):
    """Two horizontal bars comparing values; p: bars [[label, value, color], ...], headline."""
    fr[:] = (8, 8, 10)
    if p.get("headline"):
        hl = text_layer(p["headline"], ANTON, 120, WHITE, track=4)
        blit(fr, hl, W / 2, H * 0.2, scale=1 + 0.3 * (1 - ease_out(t / 0.2)), alpha=min(1, t / 0.1))
    for k, (label, val, col) in enumerate(p["bars"]):
        col = YELLOW if col == "yellow" else (110, 110, 110)
        y = H * (0.48 + 0.2 * k)
        t0 = 0.15 + 0.25 * k
        g = ease_out((t - t0) / 0.6)
        bx, bw = 700, 820
        lab = text_layer(label, INTER_SB, 44, WHITE, track=4)
        blit(fr, lab, bx - 40 - lab.shape[1] / 2, y, alpha=min(1, max(0, (t - t0) / 0.2)))
        rect(fr, bx, y - 36, bx + bw, y + 36, (38, 38, 40), min(1, max(0, (t - t0) / 0.2)))
        rect(fr, bx, y - 36, bx + bw * val / 100 * g, y + 36, col, 1.0)
        if p.get("values", True):
            blit(fr, text_layer(f"{round(val * g)}%", ANTON, 84, col), bx + bw + 30, y, anchor="l", alpha=min(1, g * 3))


def mg_list(fr, t, d, p, ctx):
    """Teaser list: a big headline and n locked numbered cards that drop in one after another."""
    fr[:] = (8, 8, 10)
    n = p.get("n", 7)
    head = text_layer(p["headline"], ANTON, 120, YELLOW, glow=14, track=4)
    blit(fr, head, W / 2, H * 0.2, scale=1 + 0.4 * (1 - ease_out(t / 0.2)), alpha=min(1, t / 0.1))
    cw, ch, gap = 200, 260, 30
    x0 = W / 2 - (cw + gap) * (n - 1) / 2
    stagger = p.get("stagger", 0.22)
    for i in range(n):
        lt = t - 0.3 - i * stagger
        if lt < 0:
            continue
        k = ease_back(lt / 0.3)
        x, y = x0 + (cw + gap) * i, H * 0.6 + 140 * (1 - k)
        a = min(1, lt / 0.12)
        rect(fr, x - cw / 2, y - ch / 2, x + cw / 2, y + ch / 2, (30, 30, 34), a)
        rect(fr, x - cw / 2, y - ch / 2, x + cw / 2, y - ch / 2 + 8, YELLOW, a)
        blit(fr, text_layer(str(i + 1), ANTON, 120, WHITE), x, y - 20, alpha=a)
        blit(fr, text_layer("LOCKED", INTER_SB, 26, (150, 150, 150), track=4), x, y + 85, alpha=a)


def mg_chapter(fr, t, d, p, ctx):
    """Chapter card: small label, giant number, optional red stamp at a word."""
    fr[:] = (8, 8, 10)
    blit(fr, text_layer(p.get("label", "TRICK"), INTER_SB, 56, WHITE, track=14), W / 2, H * 0.16, alpha=min(1, t / 0.2))
    big = text_layer(p["text"], ANTON, 330, YELLOW, glow=22, track=6)
    blit(fr, big, W / 2, H * 0.44, scale=1 + 0.35 * (1 - ease_out(t / 0.22)) + 0.03 * t / max(d, 1), alpha=min(1, t / 0.08))
    if p.get("stamp"):
        ts = t - ctx.at(p.get("stamp_at", 0.6))
        if ts > 0:
            st = text_layer(p["stamp"], ANTON, 70, RED, glow=8, track=4)
            pad = 18
            box = np.zeros((st.shape[0] + pad * 2, st.shape[1] + pad * 2, 4), np.uint8)
            cv2.rectangle(box, (4, 4), (box.shape[1] - 5, box.shape[0] - 5), (*RED, 255), 6)
            box[pad:pad + st.shape[0], pad:pad + st.shape[1]] = np.maximum(box[pad:pad + st.shape[0], pad:pad + st.shape[1]], st)
            M = cv2.getRotationMatrix2D((box.shape[1] / 2, box.shape[0] / 2), 6, 1)
            box = cv2.warpAffine(box, M, (box.shape[1], box.shape[0]))
            blit(fr, box, W / 2, H * 0.70, scale=1 + 1.2 * (1 - ease_out(ts / 0.15)), alpha=min(1, ts / 0.06))
    if p.get("sub"):
        ts = t - ctx.at(p.get("sub_at", 0.35))
        if ts > 0:
            sub = text_layer(p["sub"], ANTON, 84, WHITE, track=4)
            blit(fr, sub, W / 2, H * 0.70 + 30 * (1 - ease_out(ts / 0.25)), alpha=min(1, ts / 0.2))


def mg_versus(fr, t, d, p, ctx):
    """Two columns: p.left = [header, word] (grey), p.right = [header, word] (yellow), right side revealed at p.at."""
    fr[:] = (8, 8, 10)
    rect(fr, W / 2 - 2, H * 0.18, W / 2 + 2, H * 0.72, (60, 60, 60), min(1, t / 0.2))
    for side, (hdr, word), col, t0 in ((-1, p["left"], (150, 150, 150), ctx.at(p.get("left_at", 0.0))),
                                       (1, p["right"], YELLOW, ctx.at(p.get("at", 0.8)))):
        lt = t - t0
        if lt < 0:
            continue
        x = W / 2 + side * W * 0.24
        blit(fr, text_layer(hdr, INTER_SB, 44, WHITE, track=10), x, H * 0.28, alpha=min(1, lt / 0.2))
        w = text_layer(word, ANTON, 150, col, glow=16 if side > 0 else 0, track=4)
        blit(fr, w, x, H * 0.48, scale=1 + 0.4 * (1 - ease_out(lt / 0.2)), alpha=min(1, lt / 0.08))


def mg_recap(fr, t, d, p, ctx):
    """Numbered list revealed item by item at p.times; the newest item is yellow."""
    fr[:] = (8, 8, 10)
    items = p["items"]
    times = [ctx.at(x) for x in p["times"]]
    blit(fr, text_layer(p.get("title", "RECAP"), ANTON, 90, YELLOW, glow=12, track=8), W / 2, H * 0.1, alpha=min(1, t / 0.2))
    shown = [i for i, t0 in enumerate(times) if t >= t0]
    for i in shown:
        lt = t - times[i]
        col = YELLOW if i == shown[-1] else WHITE
        row, colx = i % 4, (0 if i < 4 else 1)
        x = 170 + colx * 850
        y = H * 0.26 + row * 125
        blit(fr, text_layer(f"{i + 1}", ANTON, 80, col), x + 40 * (1 - ease_out(lt / 0.25)), y, anchor="l", alpha=min(1, lt / 0.15))
        blit(fr, text_layer(items[i], INTER_SB, 40, col), x + 90 + 40 * (1 - ease_out(lt / 0.25)), y, anchor="l", alpha=min(1, lt / 0.15))


# overlays (drawn on top of a shot)
def ov_lower_third(fr, t, d, p, ctx):
    k = ease_out(t / 0.35)
    out = ease_io((t - (d - 0.3)) / 0.3)
    x = 110 - 700 * (1 - k) - 700 * out
    y = H * p.get("y", 0.70)
    title = text_layer(p["title"], ANTON, 64, WHITE, track=3)
    rect(fr, x - 30, y - 50, x - 18, y + 70, YELLOW, 1.0)
    rect(fr, x - 18, y - 50, x + title.shape[1] + 30, y + 70, (0, 0, 0), 0.6)
    blit(fr, title, x, y - 12, anchor="l")
    if p.get("sub"):
        n = int(len(p["sub"]) * min(1, max(0, (t - 0.2) / 0.35)))   # typewriter
        if n:
            blit(fr, text_layer(p["sub"][:n], INTER_SB, 30, YELLOW), x + 4, y + 42, anchor="l")


def ov_scan(fr, t, d, p, ctx):
    """HUD scan box over a region [x0, y0, x1, y1] (0..1), corner brackets, moving scan line, typed label."""
    x0, y0, x1, y1 = p["box"]
    k = ease_back(t / 0.3)
    cx, cy = (x0 + x1) / 2 * W, (y0 + y1) / 2 * H
    hw, hh = (x1 - x0) / 2 * W * (1.4 - 0.4 * k), (y1 - y0) / 2 * H * (1.4 - 0.4 * k)
    a = min(1, t / 0.15)
    L = 50
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = int(cx + sx * hw), int(cy + sy * hh)
            cv2.line(fr, (px, py), (int(px - sx * L), py), YELLOW, 5)
            cv2.line(fr, (px, py), (px, int(py - sy * L)), YELLOW, 5)
    ly = cy - hh + (2 * hh) * ((t * 0.9) % 1)
    rect(fr, cx - hw, ly - 2, cx + hw, ly + 2, YELLOW, 0.7 * a)
    rect(fr, cx - hw, ly - 40, cx + hw, ly, YELLOW, 0.08 * a)
    lab = p.get("label", "")
    n = int(len(lab) * min(1, max(0, (t - 0.2) / 0.7)))
    if n:
        blit(fr, text_layer(lab[:n] + ("_" if int(t * 6) % 2 else ""), INTER_SB, 34, YELLOW, stroke=2), cx - hw, cy - hh - 36, anchor="l")


def ov_tag(fr, t, d, p, ctx):
    """Small HUD text tag (e.g. '◀◀ REPLAY  YESTERDAY 11:47 PM'), blinking dot."""
    x, y = p.get("pos", [0.05, 0.09])
    if int(t * 2.5) % 2 == 0:
        cv2.circle(fr, (int(x * W) + 12, int(y * H)), 12, RED, -1)
    blit(fr, text_layer(p["text"], INTER_SB, 40, WHITE, stroke=2, track=4), x * W + 40, y * H, anchor="l")


def ov_title(fr, t, d, p, ctx):
    mg_title(fr, t, d, p, ctx)


@lru_cache(maxsize=64)
def bubble_layer(text, mine, emoji=False):
    """One chat bubble as RGBA (iMessage-like: mine = blue on the right, theirs = grey on the left)."""
    f = ImageFont.truetype(INTER_SB, 44)
    lines, cur = [], ""
    for word in text.split():           # wrap long messages at ~22 characters
        if cur and len(cur) + 1 + len(word) > 22:
            lines.append(cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    lines.append(cur)
    tw = int(max(f.getlength(ln) for ln in lines))
    pad_x, pad_y = 34, 22
    asc, desc = f.getmetrics()
    lh = asc + desc + 6
    w, h = tw + pad_x * 2, lh * len(lines) + pad_y * 2 - 6
    s4 = 2
    im = Image.new("RGBA", (w * s4, h * s4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    col = (10, 132, 255, 255) if mine else (58, 58, 62, 255)
    d.rounded_rectangle([0, 0, w * s4 - 1, h * s4 - 1], radius=min(h, 2 * (asc + desc + pad_y * 2 - 6) // 2) * s4 // 2, fill=col)
    im = im.resize((w, h), Image.Resampling.LANCZOS)
    if text and ord(text[0]) > 0x2000:   # an emoji message: colour glyph instead of text
        em = emoji_image(text, 56)
        im = Image.new("RGBA", (em.width + 60, em.height + 40), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=im.height // 2,
                                             fill=(10, 132, 255, 255) if mine else (58, 58, 62, 255))
        im.alpha_composite(em, (30, 20))
        return np.asarray(im)
    for i, ln in enumerate(lines):
        ImageDraw.Draw(im).text((pad_x, pad_y + i * lh), ln, font=f, fill=(255, 255, 255, 255))
    return np.asarray(im)


def mg_curve(fr, t, d, p, ctx):
    """Emotional curve of an experience drawn left to right over p.draw seconds; dots + labels at the peak and the end.
    p.end_low = true draws an awkward fading ending instead of a high one."""
    fr[:] = (12, 12, 14)
    x0, x1, yb = 260, W - 260, H * 0.68
    cv2.line(fr, (x0, int(yb)), (x1, int(yb)), (90, 90, 90), 3)
    blit(fr, text_layer(p.get("title", "WHAT THEY REMEMBER"), INTER_SB, 44, WHITE, track=8), W / 2, H * 0.12, alpha=min(1, t / 0.2))
    xs = np.linspace(0, 1, 200)
    end = 0.15 if p.get("end_low") else 0.8
    ys = 0.35 + 0.12 * np.sin(xs * 9) + 0.5 * np.exp(-((xs - 0.45) / 0.07) ** 2) + (end - 0.35) * np.clip((xs - 0.8) / 0.2, 0, 1)
    k = ease_io(t / p.get("draw", 1.6))
    n = max(2, int(len(xs) * k))
    pts = np.stack([x0 + xs[:n] * (x1 - x0), yb - ys[:n] * 420], axis=1).astype(np.int32)
    cv2.polylines(fr, [pts], False, YELLOW, 8, cv2.LINE_AA)
    peak_i, end_i = int(0.45 * 199), 199
    for idx, label, at in ((peak_i, "PEAK", p.get("peak_at", 0.8)), (end_i, "END", p.get("end_at", 1.6))):
        ta = t - ctx.at(at)
        if n > idx and ta > 0:
            cx, cy = int(x0 + xs[idx] * (x1 - x0)), int(yb - ys[idx] * 420)
            cv2.circle(fr, (cx, cy), int(18 * min(1, ta / 0.2) + 4), WHITE, -1, cv2.LINE_AA)
            blit(fr, text_layer(label, ANTON, 70, RED if (label == "END" and p.get("end_low")) else YELLOW), cx, cy - 70, alpha=min(1, ta / 0.2))


def mg_chat(fr, t, d, p, ctx):
    """Phone chat thread: p.messages = [[text, "me"|"them", "@word"|seconds], ...]; p.status = text under the last
    message of mine (e.g. "Read 9:42 PM") shown at p.status_at; p.title = contact name."""
    fr[:] = (12, 12, 14)
    pw, ph = 760, 1000
    x0, y0 = W / 2 - pw / 2, H / 2 - ph / 2 + 60
    rect(fr, x0 - 14, y0 - 14, x0 + pw + 14, y0 + ph + 14, (40, 40, 44), 1.0)      # phone body
    rect(fr, x0, y0, x0 + pw, y0 + ph, (0, 0, 0), 1.0)                                # screen
    rect(fr, x0, y0, x0 + pw, y0 + 110, (22, 22, 24), 1.0)                            # header
    cv2.circle(fr, (int(W / 2), int(y0 + 42)), 26, (90, 90, 96), -1)
    blit(fr, text_layer(p.get("title", "Michael"), INTER_SB, 28, WHITE), W / 2, y0 + 88)
    msgs = [(m[0], m[1] == "me", ctx.at(m[2])) for m in p["messages"]]
    shown = [(txt, mine, t0) for txt, mine, t0 in msgs if t >= t0]
    y = y0 + 150
    bottom = y0 + ph - 40
    layers = [(bubble_layer(txt, mine), mine, t0) for txt, mine, t0 in shown]
    total_h = sum(l.shape[0] + 18 for l, _, _ in layers)
    y = max(y0 + 150, bottom - total_h) if total_h > bottom - y - 60 else y
    for lay, mine, t0 in layers:
        k = ease_back((t - t0) / 0.25)
        cx = x0 + pw - 30 - lay.shape[1] / 2 if mine else x0 + 30 + lay.shape[1] / 2
        blit(fr, lay, cx, y + lay.shape[0] / 2, scale=0.6 + 0.4 * k, alpha=min(1, (t - t0) / 0.1))
        y += lay.shape[0] + 18
    if p.get("status") and t >= ctx.at(p.get("status_at", 999.0)):
        st = text_layer(p["status"], INTER_SB, 26, (150, 150, 155))
        blit(fr, st, x0 + pw - 30 - st.shape[1] / 2, y + 6, alpha=min(1, (t - ctx.at(p["status_at"])) / 0.2))


def mg_marker(fr, t, d, p, ctx):
    """Lines of text; words listed in p.mark get a yellow highlighter stroke swiped behind them at p.times[i]."""
    fr[:] = tuple(p.get("bg", (14, 14, 16)))
    lines = p["lines"]
    times = [ctx.at(x) for x in p.get("times", [0.0] * len(lines))]
    size = p.get("size", 120)
    gap = size * 1.35
    y0 = H * 0.45 - gap * (len(lines) - 1) / 2
    for k, (txt, t0) in enumerate(zip(lines, times)):
        lt = t - t0
        if lt < 0:
            continue
        marked = txt in p.get("mark", [])
        lay = text_layer(txt, ANTON, size, (15, 15, 15) if marked else WHITE, track=3)
        y = y0 + gap * k
        if marked:
            sw = ease_out(lt / 0.35)
            lw = lay.shape[1] + 40
            rect(fr, W / 2 - lw / 2, y - size * 0.45, W / 2 - lw / 2 + lw * sw, y + size * 0.5, YELLOW, 1.0)
            if sw < 0.98:   # text shows only over the stroke while it swipes in
                continue
        blit(fr, lay, W / 2, y + 20 * (1 - ease_out(lt / 0.2)), alpha=min(1, lt / 0.12))


def mg_quote(fr, t, d, p, ctx):
    """Quote card: big yellow quote mark, the line typed out word by word, optional attribution."""
    fr[:] = (14, 14, 16)
    blit(fr, text_layer("\u201c", ANTON, 300, YELLOW, glow=12), W * 0.16, H * 0.3, alpha=min(1, t / 0.2))
    words = p["text"].split()
    t_end = ctx.at(p.get("end", d * 0.7))
    n = max(1, int(len(words) * min(1, t / max(t_end, 0.1)) + 0.999))
    lines, cur = [], ""
    for w in words[:n]:
        if len(cur) + len(w) > p.get("width", 26):
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    for k, ln in enumerate(lines):
        blit(fr, text_layer(ln, ANTON, 96, WHITE, track=2), W * 0.2, H * 0.36 + k * 120, anchor="l")
    if p.get("by") and t > t_end:
        blit(fr, text_layer(p["by"], INTER_SB, 38, YELLOW, track=6), W * 0.2, H * 0.36 + len(lines) * 120 + 30,
             anchor="l", alpha=min(1, (t - t_end) / 0.3))


def mg_reason(fr, t, d, p, ctx):
    """Chapter card variant: 'REASON' label and a huge number on the left, title lines slide in on the right."""
    fr[:] = (10, 10, 12)
    k = ease_out(t / 0.4)
    blit(fr, text_layer(p.get("label", "REASON"), INTER_SB, 46, YELLOW, track=14), 200, H * 0.28, anchor="l", alpha=min(1, t / 0.2))
    blit(fr, text_layer(p["num"], ANTON, 380, YELLOW, glow=18), 190 - 120 * (1 - k), H * 0.53, anchor="l", alpha=min(1, t / 0.15))
    rect(fr, 760, H * 0.3, 768, H * 0.3 + H * 0.46 * k, WHITE, 0.85)
    t0 = ctx.at(p.get("title_at", 0.3))
    for i, ln in enumerate(p["title"]):
        lt = t - t0 - i * 0.12
        if lt < 0:
            continue
        col = YELLOW if i == len(p["title"]) - 1 and p.get("last_yellow", True) else WHITE
        blit(fr, text_layer(ln, ANTON, 110, col, track=3), 830 + 60 * (1 - ease_out(lt / 0.3)), H * 0.38 + i * 130,
             anchor="l", alpha=min(1, lt / 0.15))


def mg_checklist(fr, t, d, p, ctx):
    """Checklist recap: items with boxes; item i appears and gets ticked at p.times[i] (-1 = already done)."""
    fr[:] = (12, 12, 14)
    blit(fr, text_layer(p.get("title", "THE FIX"), ANTON, 90, YELLOW, glow=10, track=6), W / 2, H * 0.1, alpha=min(1, t / 0.2))
    times = [ctx.at(x) for x in p["times"]]
    for i, (item, t0) in enumerate(zip(p["items"], times)):
        lt = t - t0
        if lt < 0:
            continue
        y = H * 0.24 + i * 102
        x = W * 0.25
        a = min(1, lt / 0.15)
        cv2.rectangle(fr, (int(x - 30), int(y - 30)), (int(x + 30), int(y + 30)), (200, 200, 200), 4)
        if lt > 0.15:
            cv2.line(fr, (int(x - 18), int(y)), (int(x - 4), int(y + 16)), YELLOW, 8)
            cv2.line(fr, (int(x - 4), int(y + 16)), (int(x + 24), int(y - 20)), YELLOW, 8)
        blit(fr, text_layer(item, INTER_SB, 50, YELLOW if lt < 1.0 and t0 >= 0 else WHITE), x + 60, y, anchor="l", alpha=a)


CAVEAT = str(HERE / "fonts" / "Caveat-Bold.ttf")


def mg_lesson(fr, t, d, p, ctx):
    """Inverted chapter card: white page, 'LESSON' label, big black number, title lines, yellow marker bar."""
    fr[:] = (246, 244, 238)
    k = ease_out(t / 0.35)
    blit(fr, text_layer(p.get("label", "LESSON"), INTER_SB, 44, (40, 40, 40), track=14), W / 2, H * 0.17, alpha=min(1, t / 0.2))
    num = text_layer(p["num"], ANTON, 300, (15, 15, 15))
    blit(fr, num, W / 2, H * 0.42, scale=1.25 - 0.25 * k, alpha=min(1, t / 0.12))
    t0 = ctx.at(p.get("title_at", 0.35))
    for i, ln in enumerate(p["title"]):
        lt = t - t0 - i * 0.15
        if lt < 0:
            continue
        lay = text_layer(ln, ANTON, 92, (15, 15, 15), track=3)
        y = H * 0.7 + i * 104
        if i == len(p["title"]) - 1:
            sw = ease_out(lt / 0.3)
            rect(fr, W / 2 - lay.shape[1] / 2 - 10, y - 30, W / 2 - lay.shape[1] / 2 - 10 + (lay.shape[1] + 20) * sw, y + 44, YELLOW, 1.0)
        blit(fr, lay, W / 2, y, alpha=min(1, lt / 0.15))


@lru_cache(maxsize=16)
def polaroid_layer(path, caption, rot):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2)).resize((560, 560), Image.Resampling.LANCZOS)
    card = Image.new("RGBA", (620, 760), (250, 248, 242, 255))
    card.paste(im, (30, 30))
    f = ImageFont.truetype(CAVEAT, 64)
    try:
        f.set_variation_by_axes([700])
    except Exception:
        pass
    ImageDraw.Draw(card).text((310, 680), caption, font=f, fill=(30, 30, 30, 255), anchor="mm")
    shadow = Image.new("RGBA", (700, 840), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle([50, 50, 650, 790], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    shadow.alpha_composite(card, (40, 40))
    return np.asarray(shadow.rotate(rot, expand=True, resample=Image.Resampling.BICUBIC))


def mg_polaroid(fr, t, d, p, ctx):
    """Memory card: up to three polaroids (image + handwritten caption) dropped onto a dark table one by one."""
    fr[:] = (20, 18, 16)
    items = p["items"]   # [[abs image path, caption, "@word"|seconds], ...]
    n = len(items)
    for i, (img, cap, at) in enumerate(items):
        lt = t - ctx.at(at)
        if lt < 0:
            continue
        rot = [-7, 5, -3][i % 3]
        lay = polaroid_layer(img, cap, rot)
        x = W / 2 + (i - (n - 1) / 2) * 520
        k = ease_back(lt / 0.35)
        blit(fr, lay, x, H * 0.5 - 60 * (1 - k), scale=0.72 * (1.25 - 0.25 * k), alpha=min(1, lt / 0.12))


def ov_notify(fr, t, d, p, ctx):
    """iPhone-style notification banner sliding down from the top: app icon, sender, message."""
    k = ease_back(t / 0.4)
    out = ease_io((t - (d - 0.3)) / 0.3)
    y0 = -160 + 210 * k - 210 * out
    x0, bw, bh = W / 2 - 430, 860, 140
    rect(fr, x0, y0, x0 + bw, y0 + bh, (40, 40, 44), 0.92)
    rect(fr, x0 + 24, y0 + 30, x0 + 104, y0 + 110, (52, 199, 89), 1.0)
    blit(fr, text_layer("\u2709", font("symbol"), 46, WHITE), x0 + 64, y0 + 68)
    blit(fr, text_layer(p.get("title", "Messages"), INTER_SB, 34, WHITE), x0 + 128, y0 + 48, anchor="l")
    blit(fr, text_layer(p["text"], INTER_SB, 32, (200, 200, 205)), x0 + 128, y0 + 96, anchor="l")
    blit(fr, text_layer("now", INTER_SB, 26, (150, 150, 155)), x0 + bw - 70, y0 + 48)


def mg_loop(fr, t, d, p, ctx):
    """A circular arrow spinning around a centre word ("OPEN LOOP"); small labels orbit on the ring."""
    fr[:] = (8, 10, 18)
    cx, cy, r = W // 2, int(H * 0.45), 300
    a0 = (t * 70) % 360
    cv2.ellipse(fr, (cx, cy), (r, r), a0, 0, 300, YELLOW, 10, cv2.LINE_AA)
    ang = math.radians(a0 + 300)
    tip = (int(cx + r * math.cos(ang)), int(cy + r * math.sin(ang)))
    tang = ang + math.pi / 2              # direction of travel along the ring
    base = (tip[0] - 50 * math.cos(tang), tip[1] - 50 * math.sin(tang))
    pts = np.array([(int(tip[0] + 18 * math.cos(tang)), int(tip[1] + 18 * math.sin(tang))),
                    (int(base[0] + 34 * math.cos(ang)), int(base[1] + 34 * math.sin(ang))),
                    (int(base[0] - 34 * math.cos(ang)), int(base[1] - 34 * math.sin(ang)))], np.int32)
    cv2.fillPoly(fr, [pts], YELLOW, cv2.LINE_AA)
    blit(fr, text_layer(p.get("text", "OPEN LOOP"), ANTON, 110, WHITE, track=4), cx, cy, scale=1 + 0.03 * math.sin(t * 4), alpha=min(1, t / 0.2))
    for i, lab in enumerate(p.get("labels", [])):
        a = math.radians(a0 * 0.5 + i * 360 / max(1, len(p["labels"])))
        blit(fr, text_layer(lab, INTER_SB, 34, (190, 200, 220), track=4), cx + (r + 110) * math.cos(a), cy + (r + 70) * math.sin(a), alpha=min(1, t / 0.4))


def mg_receipt(fr, t, d, p, ctx):
    """A restaurant receipt slides up; at p.paid_at a red PAID stamp slams on and the receipt fades."""
    fr[:] = (10, 10, 14)
    k = ease_out(t / 0.4)
    rw, rh = 460, 640
    x0, y0 = W / 2 - rw / 2, H * 0.5 - rh / 2 + 120 * (1 - k)
    tp = ctx.at(p.get("paid_at", 999.0))
    fade = 1 - 0.6 * ease_io((t - tp - 0.6) / 0.6) if t > tp else 1.0
    rect(fr, x0, y0, x0 + rw, y0 + rh, (238, 236, 228), 0.97 * fade)
    blit(fr, text_layer(p.get("title", "TABLE 7"), INTER_SB, 40, (30, 30, 30), track=6), W / 2, y0 + 60, alpha=fade)
    for i, (item, price) in enumerate(p.get("items", [["Late-night talks", "\u221e"], ["Inside jokes", "12"], ["Almost-dates", "3"], ["Closure", "?"]])):
        y = y0 + 150 + i * 70
        blit(fr, text_layer(item, INTER_SB, 30, (40, 40, 40)), x0 + 40, y, anchor="l", alpha=fade)
        pl = text_layer(price, INTER_SB, 30, (40, 40, 40))
        blit(fr, pl, x0 + rw - 40 - pl.shape[1] / 2, y, alpha=fade)
    rect(fr, x0 + 30, y0 + rh - 150, x0 + rw - 30, y0 + rh - 146, (60, 60, 60), fade)
    blit(fr, text_layer(p.get("status", "UNPAID"), ANTON, 70, RED), W / 2, y0 + rh - 85, alpha=fade if t < tp else 0)
    if t > tp:
        ts = t - tp
        st = text_layer("PAID", ANTON, 160, (40, 170, 70), track=10)
        pad = 20
        box = np.zeros((st.shape[0] + pad * 2, st.shape[1] + pad * 2, 4), np.uint8)
        cv2.rectangle(box, (4, 4), (box.shape[1] - 5, box.shape[0] - 5), (40, 170, 70, 255), 10)
        box[pad:pad + st.shape[0], pad:pad + st.shape[1]] = np.maximum(box[pad:pad + st.shape[0], pad:pad + st.shape[1]], st)
        M = cv2.getRotationMatrix2D((box.shape[1] / 2, box.shape[0] / 2), -12, 1)
        box = cv2.warpAffine(box, M, (box.shape[1], box.shape[0]))
        blit(fr, box, W / 2, y0 + rh * 0.62, scale=1 + 1.4 * (1 - ease_out(ts / 0.15)), alpha=min(1, ts / 0.06))


def mg_timer(fr, t, d, p, ctx):
    """Countdown ring: p.start minutes counting down fast, label underneath; ends on p.end_label in yellow."""
    fr[:] = (8, 10, 18)
    total = p.get("seconds", 600)
    run = p.get("run", max(d - 0.6, 0.5))
    k = ease_io(t / run)
    left = total * (1 - k)
    cx, cy, r = W // 2, int(H * 0.44), 250
    cv2.circle(fr, (cx, cy), r, (45, 50, 70), 14, cv2.LINE_AA)
    if k < 1:
        cv2.ellipse(fr, (cx, cy), (r, r), -90, 0, 360 * (1 - k), YELLOW, 14, cv2.LINE_AA)
    txt = f"{int(left) // 60:02d}:{int(left) % 60:02d}" if k < 1 else p.get("end_label", "PASSED")
    blit(fr, text_layer(txt, ANTON, 150, YELLOW if k >= 1 else WHITE, glow=14 if k >= 1 else 0), cx, cy)
    blit(fr, text_layer(p.get("label", "THE CRAVING"), INTER_SB, 44, (190, 200, 220), track=10), cx, cy + r + 80, alpha=min(1, t / 0.3))


MG = {"kinetic": mg_kinetic, "title": mg_title, "year": mg_year, "grid": mg_grid, "bars": mg_bars,
      "list": mg_list, "chapter": mg_chapter, "versus": mg_versus, "recap": mg_recap,
      "chat": mg_chat, "marker": mg_marker, "quote": mg_quote, "reason": mg_reason, "checklist": mg_checklist,
      "curve": mg_curve, "lesson": mg_lesson, "polaroid": mg_polaroid, "loop": mg_loop, "receipt": mg_receipt, "timer": mg_timer}
OV = {"notify": ov_notify, "lower_third": ov_lower_third, "scan": ov_scan, "tag": ov_tag, "title": ov_title, "kinetic": mg_kinetic}


# ---------------------------------------------------------------- sources
class ImageSource:
    def __init__(self, path, v, dur):
        im = cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)
        self.im, self.v, self.dur = im, v, dur

    def frame(self, t, extra_zoom=1.0, extra_focus=None, shake=(0, 0)):
        v = self.v
        ih, iw = self.im.shape[:2]
        k = ease_io(t / max(self.dur, 0.01))
        f0 = v.get("focus", [0.5, 0.5])
        f1 = v.get("to", f0)
        z0 = v.get("zoom", 1.0)
        z1 = v.get("to_zoom", z0)
        fx, fy = f0[0] + (f1[0] - f0[0]) * k, f0[1] + (f1[1] - f0[1]) * k
        drift = v.get("drift", 0.05)
        z = (z0 + (z1 - z0) * k) * (1 + drift * min(max(t, 0), self.dur) / max(self.dur, 0.01))
        if drift < 0:
            z = (z0 + (z1 - z0) * k) * (1 - drift * (1 - min(max(t, 0), self.dur) / max(self.dur, 0.01)))
        if extra_focus is not None:
            fx, fy = extra_focus
        return warp(self.im, fx, fy, max(z * extra_zoom, 1.0), v.get("spin", 0) * t / max(self.dur, 0.01), shake)


def warp(im, fx, fy, z, rot=0.0, shake=(0, 0)):
    """Crop the image around (fx, fy) at zoom z (1 = whole image covers the frame) into a W x H frame."""
    ih, iw = im.shape[:2]
    cover = max(W / iw, H / ih)
    s = cover * z
    vw, vh = W / s, H / s           # visible source size
    cx = min(max(fx * iw, vw / 2), iw - vw / 2)
    cy = min(max(fy * ih, vh / 2), ih - vh / 2)
    M = cv2.getRotationMatrix2D((cx, cy), rot, s)
    M[0, 2] += W / 2 - cx + shake[0]
    M[1, 2] += H / 2 - cy + shake[1]
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


GRADES = {   # stock-footage looks, picked per video with "style": {"grade": ...}
    "cool": "eq=saturation=0.62:contrast=1.12:brightness=-0.035:gamma=0.95,colorbalance=rs=-0.04:bs=0.05:rh=0.03:gh=0.01",
    "night": "eq=saturation=0.45:contrast=1.12:brightness=-0.05:gamma=0.92,colorbalance=rs=-0.08:gs=-0.02:bs=0.12:rm=-0.05:bm=0.06,curves=all='0/0.03 0.5/0.45 1/0.94'",
    "bw": "hue=s=0.05,eq=contrast=1.2:brightness=-0.035:gamma=0.94,curves=all='0/0.03 0.5/0.46 1/0.95'",
    "warm": "eq=saturation=0.72:contrast=1.1:brightness=-0.03:gamma=0.96,colorbalance=rs=0.05:gs=0.01:bs=-0.04:rh=0.06:bh=-0.05,curves=all='0/0.04 0.5/0.48 1/0.96'",
}
STYLE = {"grade": "cool", "captions": "phrase", "caption_y": 0.86, "vignette": 0.38, "grain": 4, "chip": None}


class VideoSource:
    """Stock clip, graded to the channel look (desaturated, contrasty, cool shadows), read frame by frame."""
    def __init__(self, path, v, dur):
        self.v, self.dur = v, dur
        rate = v.get("rate", 1.0)
        vf = (f"setpts=PTS/{rate},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              + (GRADES[STYLE["grade"]] if v.get("grade", True) else "null"))
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-stream_loop", "-1", "-ss", str(v.get("start", 0)), "-i", str(path),
                                   "-t", f"{dur + 1.5:.3f}", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.idx, self.last = -1, np.zeros((H, W, 3), np.uint8)

    def frame(self, t, extra_zoom=1.0, extra_focus=None, shake=(0, 0)):
        want = max(0, int(round(t * FPS)))
        while self.idx < want:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            self.last = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            self.idx += 1
        v = self.v
        drift = v.get("drift", 0.03)
        z = v.get("zoom", 1.0) * (1 + drift * min(max(t, 0), self.dur) / max(self.dur, 0.01))
        f = extra_focus or v.get("focus", [0.5, 0.5])
        return warp(self.last, f[0], f[1], max(z * extra_zoom, 1.0), 0, shake)

    def close(self):
        self.p.kill()


class MgSource:
    def __init__(self, v, dur, ctx):
        self.v, self.dur, self.ctx = v, dur, ctx

    def frame(self, t, extra_zoom=1.0, extra_focus=None, shake=(0, 0)):
        fr = np.zeros((H, W, 3), np.uint8)
        MG[self.v["mg"]](fr, max(t, 0), self.dur, self.v, self.ctx)
        if extra_zoom != 1.0 or shake != (0, 0):
            fr = warp(fr, 0.5, 0.5, extra_zoom, 0, shake)
        return fr


class Ctx:
    """Word timing inside one shot, to resolve '@word' times."""
    def __init__(self, words, start):
        self.words, self.start = words, start   # words: [(word, t_start_abs)]

    def at(self, x):
        if isinstance(x, (int, float)):
            return float(x)
        m = re.match(r"@([^+\-]+)([+\-][\d.]+)?$", x)
        key, off = norm(m.group(1)), float(m.group(2) or 0)
        for w, ts in self.words:
            if norm(w).startswith(key):
                return ts - self.start + off
        print(f"  ! '{x}' not found in shot; using 0")
        return off


# ---------------------------------------------------------------- frame effects
def fx_vhs(fr, t):
    out = fr.copy()
    out[..., 0] = np.roll(fr[..., 0], 6, axis=1)
    out[..., 2] = np.roll(fr[..., 2], -6, axis=1)
    out[::4] = (out[::4] * 0.6).astype(np.uint8)
    rng = np.random.default_rng(int(t * FPS) + 7)
    y = int(rng.uniform(0, H - 40))
    out[y:y + 30] = np.roll(out[y:y + 30], int(rng.uniform(-40, 40)), axis=1)
    return out


def fx_glitch(fr, t, amt=1.0):
    out = fr.copy()
    rng = np.random.default_rng(int(t * 1000))
    sh = int(18 * amt)
    out[..., 0] = np.roll(fr[..., 0], sh, axis=1)
    out[..., 2] = np.roll(fr[..., 2], -sh, axis=1)
    for _ in range(int(6 * amt)):
        y = int(rng.uniform(0, H - 60))
        h = int(rng.uniform(10, 60))
        out[y:y + h] = np.roll(out[y:y + h], int(rng.uniform(-120, 120) * amt), axis=1)
    return out


def motion_blur(fr, px, axis=1):
    px = int(px)
    if px < 3:
        return fr
    k = np.zeros((1, px) if axis == 1 else (px, 1), np.float32)
    k[:] = 1.0 / px
    return cv2.filter2D(fr, -1, k)


def zoom_blur(fr, amt):
    if amt < 0.01:
        return fr
    acc = fr.astype(np.float32)
    for i in range(1, 4):
        z = 1 + amt * i / 3
        acc += warp(fr, 0.5, 0.5, z)
    return (acc / 4).astype(np.uint8)


# ---------------------------------------------------------------- captions
def phrases_for(words_abs, shot_of, shots):
    """Group words into caption phrases of up to 3 words (break at punctuation and shot boundaries)."""
    out, cur = [], []
    for i, (w, s, e) in enumerate(words_abs):
        if not shots[shot_of[i]].get("captions", True):
            if cur:
                out.append(cur)
                cur = []
            continue
        if cur and (shot_of[cur[-1]] != shot_of[i] or len(cur) >= 3):
            out.append(cur)
            cur = []
        cur.append(i)
        if re.search(r"[.,?!…]$|\.\.\.$", w):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


@lru_cache(maxsize=48)
def caption_layer(words, active):
    if STYLE["captions"] == "pill":
        return caption_pill(words, active)
    if STYLE["captions"] == "punch":
        return caption_punch(words, active)
    if STYLE["captions"] == "underline":
        return caption_underline(words, active)
    f = ImageFont.truetype(INTER, 66)
    sp = f.getlength(" ")
    ws = [f.getlength(w) for w in words]
    tw = int(sum(ws) + sp * (len(words) - 1)) + 40
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (tw + 40, asc + desc + 50), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    d = ImageDraw.Draw(im)
    x = 30
    for k, (w, wl) in enumerate(zip(words, ws)):
        ds.text((x + 4, 30), w, font=f, fill=(0, 0, 0, 200), stroke_width=8, stroke_fill=(0, 0, 0, 200))
        d.text((x, 24), w, font=f, fill=(*(YELLOW if k == active else WHITE), 255), stroke_width=7, stroke_fill=(0, 0, 0, 255))
        x += wl + sp
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    return np.asarray(Image.alpha_composite(sh, im))


def caption_underline(words, active):
    """Caption variant: lowercase, soft dark plate behind the phrase, yellow underline under the spoken word."""
    f = ImageFont.truetype(INTER_SB, 60)
    low = [w.lower() for w in words]
    sp = f.getlength(" ")
    ws = [f.getlength(w) for w in low]
    asc, desc = f.getmetrics()
    tw = int(sum(ws) + sp * (len(low) - 1))
    im = Image.new("RGBA", (tw + 100, asc + desc + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 8, tw + 80, asc + desc + 44], radius=22, fill=(0, 0, 0, 150))
    x = 50
    for k, (w, wl) in enumerate(zip(low, ws)):
        d.text((x, 18), w, font=f, fill=(255, 255, 255, 255))
        if k == active:
            d.rounded_rectangle([x, asc + desc + 22, x + wl, asc + desc + 30], radius=4, fill=(*YELLOW, 255))
        x += wl + sp
    return np.asarray(im)


def caption_punch(words, active):
    """Caption variant: tall condensed caps; the spoken word is yellow and 20% bigger, no box."""
    base, big = 78, 94
    fs, fb = ImageFont.truetype(ANTON, base), ImageFont.truetype(ANTON, big)
    up = [w.upper() for w in words]
    ws = [(fb if k == active else fs).getlength(w) for k, w in enumerate(up)]
    sp = fs.getlength(" ")
    asc, desc = fb.getmetrics()
    im = Image.new("RGBA", (int(sum(ws) + sp * len(up)) + 80, asc + desc + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 40
    for k, (w, wl) in enumerate(zip(up, ws)):
        f = fb if k == active else fs
        y = 16 if k == active else 16 + (big - base) * 0.8
        d.text((x, y), w, font=f, fill=(*(YELLOW if k == active else WHITE), 255), stroke_width=6, stroke_fill=(0, 0, 0, 255))
        x += wl + sp
    return np.asarray(im)


def caption_pill(words, active):
    """Caption variant: bold white words, the spoken word inside a yellow rounded box in black type."""
    f = ImageFont.truetype(INTER, 62)
    sp = f.getlength(" ") + 6
    ws = [f.getlength(w.upper()) for w in words]
    asc, desc = f.getmetrics()
    h = asc + desc
    im = Image.new("RGBA", (int(sum(ws) + sp * len(words)) + 80, h + 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 40
    for k, (w, wl) in enumerate(zip(words, ws)):
        if k == active:
            d.rounded_rectangle([x - 14, 14, x + wl + 14, 14 + h + 14], radius=16, fill=(*YELLOW, 255))
            d.text((x, 20), w.upper(), font=f, fill=(10, 10, 10, 255))
        else:
            d.text((x, 20), w.upper(), font=f, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0, 255))
        x += wl + sp
    return np.asarray(im)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--from", dest="t_from", type=float, default=0)
    ap.add_argument("--to", dest="t_to", type=float)
    ap.add_argument("--jobs", type=int, default=4, help="render this many chunks in parallel")
    ap.add_argument("--stills", action="store_true", help="QA: one frame from 70%% into every shot, as contact sheets")
    ap.add_argument("--audio-only", action="store_true", help="rebuild the soundtrack and swap it into the existing render")
    ap.add_argument("--part", help=argparse.SUPPRESS)   # internal: render one chunk, video only, into this file
    args = ap.parse_args()
    spec_path = Path(args.spec).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    STYLE.update(spec.get("style", {}))
    shots = spec["shots"]
    out = (base / spec["out"]).resolve()
    if args.preview:
        out = out.with_name(out.stem + "_preview.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    work = out.parent / (Path(spec["out"]).stem + "_work")
    work.mkdir(exist_ok=True)

    # 1. Voice + word timing (Whisper gets a decoded array; this PyAV build can't open files itself).
    run = lambda a: subprocess.run(a, check=True, capture_output=True)  # noqa: E731
    takes = spec["audio"] if isinstance(spec["audio"], list) else [spec["audio"]]
    gap = spec.get("take_gap", 0.4)   # breath between takes (chapters)
    ins = sum((["-i", str(base / a)] for a in takes), [])
    graph = "".join(f"[{i}:a]aresample={SR},aformat=channel_layouts=stereo,apad=pad_dur={gap if i < len(takes) - 1 else 0}[a{i}];"
                    for i in range(len(takes)))
    graph += "".join(f"[a{i}]" for i in range(len(takes))) + f"concat=n={len(takes)}:v=0:a=1,atempo={spec.get('speed', 1.0)}[v]"
    run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", graph, "-map", "[v]", "-c:a", "pcm_s16le",
         str(work / "voice_raw.wav")])
    voice = read_audio(work / "voice_raw.wav")
    from faster_whisper import WhisperModel
    mono16 = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(work / "voice_raw.wav"), "-ac", "1", "-ar",
                                           "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    cache = work / "whisper.json"
    key = "|".join(f"{a}:{(base / a).stat().st_mtime}" for a in takes) + f"-{spec.get('speed', 1.0)}-{gap}"
    if cache.exists() and json.loads(cache.read_text()).get("key") == key:
        heard = [type("Wd", (), w) for w in json.loads(cache.read_text())["words"]]
    else:
        segs, _ = WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(mono16, word_timestamps=True, language="en")
        heard = [w for s in segs for w in (s.words or [])]
        cache.write_text(json.dumps({"key": key, "words": [{"word": w.word, "start": w.start, "end": w.end} for w in heard]}))
    script, owner = [], []
    for si, sh in enumerate(shots):
        for w in sh["text"].split():
            script.append(w)
            owner.append(si)
    times = align(script, heard)
    print(f"script {len(script)} words, heard {len(heard)}")

    # 2. Cuts and pauses (as in reels: a pause is silence inserted in the voice before a shot).
    raw_starts = [0.0 if si == 0 else max(times[owner.index(si)][0] - LEAD, 0.0) for si in range(len(shots))]
    pieces, cursor, pts, gaps = [], 0, [], []
    for si, sh in enumerate(shots):
        d = sh.get("pause_before", 0)
        if d and si:
            cut = int(raw_starts[si] * SR)
            pieces += [voice[cursor:cut], np.zeros((int(d * SR), 2), np.float32)]
            pts.append(raw_starts[si])
            gaps.append(d)
            cursor = cut
    pieces += [voice[cursor:], np.zeros((int(spec.get("tail", TAIL) * SR), 2), np.float32)]
    voice = np.concatenate(pieces)
    total = len(voice) / SR

    def remap(t):
        return t + sum(g for p, g in zip(pts, gaps) if p <= t + 1e-6)
    starts = [remap(t) for t in raw_starts]
    times = [(remap(s), remap(e)) for s, e in times]
    ends = starts[1:] + [total]
    ctxs = []
    for si in range(len(shots)):
        ctxs.append(Ctx([(script[i], times[i][0]) for i in range(len(script)) if owner[i] == si], starts[si]))

    def abs_at(si, x):
        return starts[si] + ctxs[si].at(x)

    # 3. Audio: voice fx, music (+ muffle), ambience, sfx, mix.
    for si, sh in enumerate(shots):
        vf = sh.get("voice_fx")
        if vf and vf.get("fx") == "echo":
            t0 = abs_at(si, vf["at"])
            wi = next(i for i in range(len(script)) if owner[i] == si and abs(times[i][0] - t0) < 0.02)
            a, b = int(times[wi][0] * SR), int(min(times[wi][1] + 0.08, total) * SR)
            word = voice[a:b].copy()
            for k, (dl, g) in enumerate([(0.16, 0.42), (0.32, 0.24), (0.48, 0.12)]):
                s = b + int((dl - 0.0) * SR) - (b - a) // 2
                e = min(s + len(word), len(voice))
                lp = sosfilt(butter(2, 3000 - k * 800, fs=SR, output="sos"), word, axis=0)
                voice[s:e] += lp[: e - s] * g
    mix = voice.copy()
    if spec.get("music_cues") or spec.get("music"):
        music = music_bed(spec, base, starts, len(voice))
        mf = np.zeros(len(music), np.float32)
        for si, sh in enumerate(shots):
            if sh.get("music_fx") == "muffle":
                a, b = int(starts[si] * SR), int(ends[si] * SR)
                mf[a:b] = 1
        if mf.any():
            ramp = int(0.15 * SR)
            mf = np.convolve(mf, np.ones(ramp) / ramp, "same")
            muff = sosfilt(butter(4, 450, fs=SR, output="sos"), music, axis=0)
            music = music * (1 - mf[:, None]) + muff * mf[:, None] * 1.4
        if not args.part:
            write_wav(work / "music.wav", music)
        env = np.abs(voice).mean(axis=1)
        hop = 441
        frames = env[: len(env) // hop * hop].reshape(-1, hop).max(axis=1)
        gain_f, level = np.empty_like(frames), 0.0
        for i, v in enumerate(frames):
            level = max(v, level * 0.93)
            gain_f[i] = 0.42 if level > 0.02 else 1.0
        gain_f = np.convolve(gain_f, np.ones(8) / 8, "same")
        gain = np.repeat(gain_f, hop)
        gain = np.concatenate([gain, np.full(len(music) - len(gain), 1.0)])
        fo = int(spec.get("music_fade", 2.0) * SR)
        gain[-fo:] *= np.linspace(1, 0, fo)
        mix += music * gain[:, None] * spec.get("music_volume", 0.35)
    for si, sh in enumerate(shots):
        amb = sh.get("amb")
        if amb:
            a, b = int(starts[si] * SR), int(ends[si] * SR)
            src = read_audio(AMB[amb["name"]], start=5 + si * 3.1, dur=(b - a) / SR + 0.1)[: b - a]
            fade = min(len(src) // 2, int(0.3 * SR))
            src[:fade] *= np.linspace(0, 1, fade)[:, None]
            src[-fade:] *= np.linspace(1, 0, fade)[:, None]
            mix[a:a + len(src)] += src * amb.get("gain", 0.12)
    cues = []
    for si, sh in enumerate(shots):
        for c in sh.get("sfx", []):
            c = {"name": c} if isinstance(c, str) else c
            cues.append((c["name"], abs_at(si, c.get("at", 0.0)), float(c.get("gain", 1.0))))
        if sh.get("pause_before") and si and not any((c if isinstance(c, str) else c["name"]) == "impact" for c in sh.get("sfx", [])):
            cues.append(("impact", starts[si], 0.8))
    for name, at, g in cues:
        f, peak, pre, post, bg = SFX[name]
        pre = min(pre, peak, max(at, 0))
        clip = read_audio(f, start=peak - pre, dur=pre + post)
        fade = min(len(clip), int(0.12 * SR))
        clip[-fade:] *= np.linspace(1, 0, fade)[:, None]
        s = int((at - pre) * SR)
        e = min(s + len(clip), len(mix))
        if e > s >= 0:
            mix[s:e] += clip[: e - s] * bg * g
    pk = np.abs(mix).max()
    if pk > 0.98:
        mix *= 0.98 / pk
    if not args.part:
        write_wav(work / "mix.wav", mix, af="loudnorm=I=-14:TP=-1.5:LRA=11")
    if args.audio_only:
        tmp = out.with_name(out.stem + "_newaudio.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-i", str(work / "mix.wav"), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(tmp)], check=True)
        tmp.replace(out)
        print(f"{out}  (new soundtrack)")
        return

    # 4. Video, frame by frame.
    scale_out = 0.5 if args.preview else 1.0
    t_from = args.t_from
    t_to = min(args.t_to or total, total)
    n0, n1 = int(t_from * FPS), int(t_to * FPS)
    if args.jobs > 1 and not args.part and not args.stills and n1 - n0 > 300:
        # Split the frames into chunks, render them in parallel child processes, then join and add the audio.
        bounds = [n0 + (n1 - n0) * k // args.jobs for k in range(args.jobs + 1)]
        parts = [work / f"part{k}.mp4" for k in range(args.jobs)]
        kids = [subprocess.Popen([sys.executable, __file__, str(spec_path), "--from", f"{bounds[k] / FPS:.6f}",
                                  "--to", f"{bounds[k + 1] / FPS:.6f}", "--part", str(parts[k]), "--jobs", "1",
                                  *(["--preview"] if args.preview else [])]) for k in range(args.jobs)]
        if any(k.wait() for k in kids):
            sys.exit("a render chunk failed")
        (work / "parts.txt").write_text("".join(f"file '{p_}'\n" for p_ in parts))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(work / "parts.txt"),
                        "-ss", f"{t_from:.3f}", "-t", f"{t_to - t_from:.3f}", "-i", str(work / "mix.wav"), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
        for p_ in parts:
            p_.unlink()
        for i, (s_, e_) in enumerate(zip(starts, ends)):
            print(f"  shot {i + 1:2d}  {s_:6.2f}s  +{e_ - s_:4.2f}s  {shots[i]['text'][:50]}")
        (work / "timeline.json").write_text(json.dumps([{"start": round(a, 3), "dur": round(b - a, 3), "text": sh["text"]}
                                                        for a, b, sh in zip(starts, ends, shots)], indent=1))
        print(f"{out}  ({total:.1f}s, {out.stat().st_size / 1e6:.1f} MB)")
        return
    if args.part:
        out = Path(args.part)
    enc = None if args.stills else subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", *([] if args.part else ["-ss", f"{t_from:.3f}", "-t", f"{t_to - t_from:.3f}", "-i", str(work / "mix.wav")]),
                            "-vf", f"scale={int(W * scale_out)}:{int(H * scale_out)}" if args.preview else "null",
                            "-c:v", "libx264", "-preset", "ultrafast" if args.preview else "medium",
                            "-crf", "26" if args.preview else "21", "-pix_fmt", "yuv420p",
                            *(["-an"] if args.part else ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest"]),
                            str(out)], stdin=subprocess.PIPE)
    # grain + vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = 1 - STYLE["vignette"] * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.2
    vig = np.clip(vig, 0.45, 1)[..., None].astype(np.float32)
    rng = np.random.default_rng(3)
    grain = [cv2.resize(rng.normal(0, STYLE["grain"], (H // 2, W // 2)).astype(np.float32), (W, H))[..., None] for _ in range(6)]

    words_abs = [(script[i], times[i][0], times[i][1]) for i in range(len(script))]
    phr = phrases_for(words_abs, owner, shots)
    phr_span = []
    for k, ph in enumerate(phr):
        s = words_abs[ph[0]][1]
        e = words_abs[ph[-1]][2] + 0.35
        if k + 1 < len(phr):
            e = min(e, words_abs[phr[k + 1][0]][1])
        if ends[owner[ph[0]]] < e:   # don't carry a phrase over the cut
            e = ends[owner[ph[0]]]
        phr_span.append((s, e))

    sources = {}

    def src(si):
        if si not in sources:
            sh = shots[si]
            v = sh["v"]
            dur = ends[si] - starts[si]
            if "img" in v:
                sources[si] = ImageSource(base / v["img"], v, dur)
            elif "video" in v:
                sources[si] = VideoSource(base / v["video"], v, dur)
            else:
                sources[si] = MgSource(v, dur, ctxs[si])
        return sources[si]

    def shot_frame(si, T):
        """Shot si at absolute time T, with its punch, shake, fx and overlays."""
        sh = shots[si]
        t = T - starts[si]
        ez, ef = 1.0, None
        pu = sh.get("punch")
        if pu:
            if pu is True:
                pu = {"at": 0.0, "zoom": 1.15}
            tp = ctxs[si].at(pu.get("at", 0.0))
            k = ease_out((t - tp) / 0.16) if t >= tp else 0.0
            ez = 1 + (pu.get("zoom", 1.5) / max(sh["v"].get("zoom", 1.0), 1) - 1) * k
            if pu.get("focus") and k > 0:
                f0 = sh["v"].get("focus", [0.5, 0.5])
                ef = [f0[0] + (pu["focus"][0] - f0[0]) * k, f0[1] + (pu["focus"][1] - f0[1]) * k]
        shake = (0, 0)
        for s_at in sh.get("shake", []):
            ts = t - ctxs[si].at(s_at)
            if 0 <= ts < 0.35:
                amp = 18 * (1 - ts / 0.35)
                shake = (amp * math.sin(ts * 90), amp * math.cos(ts * 70))
        fr = src(si).frame(t, ez, ef, shake)
        fr = np.ascontiguousarray(fr)
        for fx in sh.get("fx", []):
            fx = {"name": fx} if isinstance(fx, str) else fx
            if fx["name"] == "vhs":
                fr = fx_vhs(fr, T)
            elif fx["name"] == "letterbox":   # cinematic bars for story moments
                k = ease_out(t / 0.35) if fx.get("anim") else 1.0
                bh = int(H * 0.11 * k)
                if bh:
                    fr[:bh] = 0
                    fr[H - bh:] = 0
            elif fx["name"] == "light_off":
                ta = t - ctxs[si].at(fx["at"])
                if ta > 0:
                    flick = [1, 0.25, 0.9, 0.15, 0.6, 0.08][min(int(ta * FPS / 2), 5)]
                    fr = (fr.astype(np.float32) * flick).astype(np.uint8)
        for ov in sh.get("overlays", []):
            t0 = ctxs[si].at(ov.get("at", 0.0))
            dur = ov.get("dur", (ends[si] - starts[si]) - t0)
            if t0 <= t < t0 + dur:
                OV[ov["mg"]](fr, t - t0, dur, ov, ctxs[si])
        return fr

    TR = 4   # transition half-length in frames
    todo = range(n0, n1)
    if args.stills:
        todo = [int((s_ + 0.7 * (e_ - s_)) * FPS) for s_, e_ in zip(starts, ends)]
        tiles = []
    try:
        for n in todo:
            T = n / FPS
            si = max(i for i in range(len(shots)) if starts[i] <= T + 1e-6)
            # transitions around cut si (in) and cut si+1 (out)
            fr = None
            for cut in (si, si + 1):
                if cut <= 0 or cut >= len(shots):
                    continue
                kind = shots[cut].get("in", "cut")
                dn = n - int(round(starts[cut] * FPS))   # frames relative to the cut
                if kind == "cut" or not (-TR <= dn < TR):
                    continue
                p = (dn + TR) / (2 * TR)               # 0..1 across the transition
                A = shot_frame(cut - 1, T)
                B = shot_frame(cut, T)
                if kind == "whip":
                    if p < 0.5:
                        fr = np.roll(A, -int(W * ease_io(p) * 0.6), axis=1)
                    else:
                        fr = np.roll(B, int(W * (1 - ease_io(p)) * 0.6), axis=1)
                    fr = motion_blur(fr, 160 * math.sin(math.pi * p))
                elif kind == "zoom":
                    fr = zoom_blur(warp(A, .5, .5, 1 + 0.6 * p), 0.25 * math.sin(math.pi * p)) if p < 0.5 else \
                        zoom_blur(warp(B, .5, .5, 1 + 0.6 * (1 - p)), 0.25 * math.sin(math.pi * p))
                elif kind == "flash":
                    base_fr = A if p < 0.5 else B
                    w = 1 - abs(p - 0.5) * 2
                    fr = (base_fr.astype(np.float32) * (1 - w) + 255 * w).astype(np.uint8)
                elif kind == "glitch":
                    fr = fx_glitch(A if p < 0.5 else B, T, 1 - abs(p - 0.5) * 1.6)
                elif kind == "spin":      # rotate + zoom through the cut
                    base_fr = A if p < 0.5 else B
                    ang = (p - 0.5) * 40
                    z = 1 + 0.35 * math.sin(math.pi * p)
                    M = cv2.getRotationMatrix2D((W / 2, H / 2), ang, z)
                    fr = cv2.warpAffine(base_fr, M, (W, H), borderMode=cv2.BORDER_REFLECT)
                    fr = zoom_blur(fr, 0.12 * math.sin(math.pi * p))
                elif kind == "iris":      # B opens from a growing circle in the centre
                    r = int(ease_io(p) * math.hypot(W, H) / 2)
                    mask = np.zeros((H, W), np.uint8)
                    cv2.circle(mask, (W // 2, H // 2), max(r, 1), 255, -1, cv2.LINE_AA)
                    m = (mask.astype(np.float32) / 255)[..., None]
                    fr = (A.astype(np.float32) * (1 - m) + B.astype(np.float32) * m).astype(np.uint8)
                    cv2.circle(fr, (W // 2, H // 2), max(r, 1), YELLOW, 6, cv2.LINE_AA)
                elif kind == "push":      # B pushes A out to the left
                    off = int(W * ease_io(p))
                    fr = np.hstack([A[:, off:], B[:, :off]]) if off else A.copy()
                    fr = motion_blur(fr, 120 * math.sin(math.pi * p))
                elif kind == "slide":     # B pushes A up out of frame
                    off = int(H * ease_io(p))
                    fr = np.vstack([A[off:], B[:off]]) if off else A.copy()
                    fr = motion_blur(fr, 90 * math.sin(math.pi * p), axis=0)
                elif kind == "blur":      # blurred dissolve
                    w = ease_io(p)
                    mix_ = (A.astype(np.float32) * (1 - w) + B.astype(np.float32) * w).astype(np.uint8)
                    k = int(2 + 40 * math.sin(math.pi * p)) | 1
                    fr = cv2.GaussianBlur(mix_, (k, k), 0)
                elif kind == "dip":
                    base_fr = A if p < 0.5 else B
                    fr = (base_fr.astype(np.float32) * abs(p - 0.5) * 2).astype(np.uint8)
            if fr is None:
                fr = shot_frame(si, T)
            # look: vignette + grain
            f32 = fr.astype(np.float32) * vig + grain[n % 6]
            # fade out
            if spec.get("fade_out") and T > total - spec["fade_out"]:
                f32 *= max(0, (total - T) / spec["fade_out"])
            fr = np.clip(f32, 0, 255).astype(np.uint8)
            # captions
            for k, (s, e) in enumerate(phr_span):
                if s - 0.05 <= T < e:
                    ph = phr[k]
                    act = max([j for j, wi in enumerate(ph) if words_abs[wi][1] <= T + 0.03] or [0])
                    lay = caption_layer(tuple(re.sub(r"[{}]", "", words_abs[wi][0]) for wi in ph), act)
                    pop = 1 + 0.12 * (1 - ease_out((T - s) / 0.12))
                    blit(fr, lay, W / 2, H * STYLE["caption_y"], scale=pop)
                    break
            if spec.get("progress"):
                rect(fr, 0, H - 7, W * T / total, H, YELLOW, 0.9)
            if STYLE["chip"] and T > STYLE["chip"].get("from", 0):
                chip = text_layer(STYLE["chip"]["text"], INTER_SB, 30, (20, 20, 20), track=4)
                cw = chip.shape[1] + 36
                a = min(1, (T - STYLE["chip"].get("from", 0)) / 0.3)
                rect(fr, W - 60 - cw, 44, W - 60, 96, YELLOW, 0.92 * a)
                blit(fr, chip, W - 60 - cw / 2, 70, alpha=a)
            if args.stills:
                tile = cv2.resize(fr, (384, 216), interpolation=cv2.INTER_AREA)
                cv2.putText(tile, str(len(tiles) + 1), (6, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 40, 40), 2)
                tiles.append(tile)
                for k in list(sources):
                    if hasattr(sources[k], "close"):
                        sources[k].close()
                    del sources[k]
                continue
            enc.stdin.write(fr.tobytes())
            for k in [k for k in sources if ends[k] < T - 1.0]:   # free finished sources
                if hasattr(sources[k], "close"):
                    sources[k].close()
                del sources[k]
            if n % 300 == 0 and not args.part or args.part and (n - n0) % 600 == 0:
                print(f"  frame {n}/{n1}  ({T:.1f}s)", flush=True)
    finally:
        if enc:
            enc.stdin.close()
            enc.wait()
        for s in sources.values():
            if hasattr(s, "close"):
                s.close()
    if args.part:
        return
    if args.stills:
        for k in range(0, len(tiles), 30):
            grp = tiles[k:k + 30] + [np.zeros_like(tiles[0])] * (30 - len(tiles[k:k + 30]))
            sheet = np.vstack([np.hstack(grp[r * 5:(r + 1) * 5]) for r in range(6)])
            path = work / f"stills_{k // 30:02d}.jpg"
            cv2.imwrite(str(path), cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])
            print(path)
    for i, (s, e) in enumerate(zip(starts, ends)):
        print(f"  shot {i + 1:2d}  {s:6.2f}s  +{e - s:4.2f}s  {shots[i]['text'][:50]}")
    (work / "timeline.json").write_text(json.dumps([{"start": round(s, 3), "dur": round(e - s, 3), "text": sh["text"]}
                                                    for s, e, sh in zip(starts, ends, shots)], indent=1))
    if not args.stills:
        print(f"{out}  ({total:.1f}s, {out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
