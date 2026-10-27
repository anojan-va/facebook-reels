"""NoliDrop ad 3 - UGC "Don't go to the pool store yet", AI-video version.
Storyboard keyframes (Nano Banana Pro, storyboard.py) animated with Kling 3.0 (video.py); clip frames extracted to
work/clips/<id>/NNN.jpg (ffmpeg -q:v 2). The real app UI is keyed onto the green phone screens frame by frame; Noli drops
onto the phone as a sticker; screen-recording inserts and the end card are motion graphics.
python3 ad3.py [--plan | --stills | --frame t1,t2]"""
import math
from functools import lru_cache

import cv2
import numpy as np

import adkit as K
from ad3_motion import emoji, end_card, num_badge, pill, scribble, sticker

CLIP_FPS = 24


@lru_cache(maxsize=64)
def clip_frame(cid, n):
    n = int(min(max(n, 0), 96))
    im = cv2.imread(str(K.HERE / "work" / "clips" / cid / f"{n + 1:03d}.jpg"))[..., ::-1]
    return np.ascontiguousarray(im)


def keyed(frame, screen):
    """Key `screen` (PIL) into the green phone screen of one video frame (quad found per frame)."""
    im = frame.astype(np.int16)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    m = ((g > 110) & (g - r > 45) & (g - b > 45)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cs:
        return frame
    c = max(cs, key=cv2.contourArea)
    hull = cv2.convexHull(c)
    q = cv2.approxPolyDP(hull, 0.02 * cv2.arcLength(hull, True), True).reshape(-1, 2).astype(np.float32)
    if len(q) != 4:
        q = cv2.boxPoints(cv2.minAreaRect(c)).astype(np.float32)
    s, d = q.sum(axis=1), np.diff(q, axis=1).ravel()
    quad = np.float32([q[np.argmin(s)], q[np.argmin(d)], q[np.argmax(s)], q[np.argmax(d)]])
    sc = np.asarray(screen.convert("RGB")).astype(np.float32)
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [K.SW, 0], [K.SW, K.SH], [0, K.SH]]), quad)
    warped = cv2.warpPerspective(sc, M, (frame.shape[1], frame.shape[0]), flags=cv2.INTER_LINEAR)
    gm = np.clip(((g - np.maximum(r, b)) - 25) / 50.0, 0, 1).astype(np.float32)
    inside = np.zeros(gm.shape, np.uint8)
    cv2.fillConvexPoly(inside, quad.astype(np.int32), 1)
    gm = cv2.GaussianBlur(gm * inside, (3, 3), 0)[..., None]
    out = frame.astype(np.float32) * (1 - gm) + warped * gm
    gg = out[..., 1]
    lim = np.maximum(out[..., 0], out[..., 2]) + 10
    out[..., 1] = np.where((gg > lim) & (gm[..., 0] < 0.95), lim, gg)
    return out.astype(np.uint8), quad


def video(cid, ct, z=1.0, fx=0.5, fy=0.5, screen=None, rot=0.0, shake=0.6, t=0.0):
    """One clip frame at clip time ct, keyed (optional), scaled to 1080x1920 with a punch-in z."""
    fr = clip_frame(cid, ct * CLIP_FPS)
    quad = None
    if screen is not None:
        res = keyed(fr, screen)
        if isinstance(res, tuple):
            fr, quad = res
    out = K.cover_np(fr, 0, 1, z, z, fx, fy, rot=rot, shake=shake).astype(np.float32) if shake else \
        K.cover_np(fr, 0, 1, z, z, fx, fy, rot=rot).astype(np.float32)
    # light sharpen after the 720p -> 1080p upscale
    bl = cv2.GaussianBlur(out, (0, 0), 1.2)
    out = np.clip(out * 1.35 - bl * 0.35, 0, 255)
    if quad is not None:   # map the phone quad into frame coordinates (for stickers)
        ih, iw = fr.shape[:2]
        s = max(K.W / iw, K.H / ih) * z
        cx, cy = K.clamp(fx * iw, K.W / 2 / s, iw - K.W / 2 / s), K.clamp(fy * ih, K.H / 2 / s, ih - K.H / 2 / s)
        quad = (quad - [cx, cy]) * s + [K.W / 2, K.H / 2]
    return out, quad


# ------------------------------------------------------------------ scenes
def s_hook(t, d, a, ctx):
    fr, _ = video("K1", 0.15 + t, 1.0, 0.5, 0.45)
    return fr


def s_hook2(t, d, a, ctx):
    fr, _ = video("K1", 1.15 + t * 0.9, 1.32, 0.42, 0.33)
    p = (t - 0.15) / 0.25
    if p > 0:
        K.paste(fr, emoji("✋", 170), K.W * 0.82, 360, K.ease_back(p, 2.5), rot=-10)
    return fr


def s_strip(t, d, a, ctx):
    fr, _ = video("K2", 1.6 + t * 1.3, 1.08, 0.45, 0.5)
    for i, (txt, x, y) in enumerate([("green?", 0.26, 0.2), ("cloudy?", 0.7, 0.28)]):
        p = (t - 0.05 - i * 0.3) / 0.25
        if p > 0:
            K.paste(fr, pill(txt, 64, (110, 200, 60) if i == 0 else (225, 228, 235)), x * K.W, y * K.H, K.ease_back(p, 2.4),
                    rot=(-1) ** i * 6)
    return fr


def s_open(t, d, a, ctx):
    fr, _ = video("K3", 0.2 + t, 1.06, 0.5, 0.5, K.ui_home())
    return fr


def s_noli(t, d, a, ctx):
    """UGC Drop: Noli falls onto the phone screen with a splash and waves from it."""
    fr, q = video("K3", 0.2 + ctx["starts"][4] - ctx["starts"][3] + t, 1.06, 0.5, 0.5, K.ui_home())
    if q is None:
        return fr
    cx, top, bot = q[:, 0].mean(), (q[0, 1] + q[1, 1]) / 2, (q[2, 1] + q[3, 1]) / 2
    land = top + (bot - top) * 0.62
    hit = 0.22
    if t < hit:
        K.paste(fr, sticker("sprites/n-dive.png"), cx, -200 + (land - 150 + 200) * (t / hit) ** 1.5, 0.42)
    else:
        tt = t - hit
        K.ring(fr, cx, land, tt * 700, 7, alpha=max(0, 0.75 - tt * 1.3), sy=0.45)
        K.splash_drops(fr, tt, cx, land - 20, 16, power=0.75)
        K.paste(fr, sticker("sprites/n-wave.png"), cx, land + 40, 0.5 * K.spring(tt / 0.4), anchor="b", rot=-4 + 3 * math.sin(t * 5))
    return fr


def s_type(t, d, a, ctx):
    k = round(K.clamp(t / (d * 0.9)) * 20) / 20
    fr, _ = video("K5", 0.4 + t * 1.2, 1.25, 0.55, 0.3, K.ui_values(k))
    return fr


def s_whats_off(t, d, a, ctx):
    sc = K.ui_results(K.clamp(0.4 + t / d * 0.25))
    fr = K.screen_zoom(sc, K.SW / 2, 640, 1.0 + 0.05 * t).astype(np.float32)
    cy = (605 - 640) * max(K.W / K.SW, K.H / K.SH) * (1.0 + 0.05 * t) + K.H / 2
    scribble(fr, K.W / 2, cy, 470, 140, (t - 0.2) / 0.45)
    return fr


def s_fix_first(t, d, a, ctx):
    sc = K.ui_results(1.0)
    fr = K.screen_zoom(sc, K.SW / 2, 1000, 1.05).astype(np.float32)
    s = max(K.W / K.SW, K.H / K.SH) * 1.05
    cx, cy = (382 - K.SW / 2) * s + K.W / 2, (800 - 1000) * s + K.H / 2
    scribble(fr, cx, cy, 500, 130, (t - 0.1) / 0.4, (255, 190, 0), 13)
    p = (t - 0.35) / 0.25
    if p > 0:
        K.paste(fr, emoji("👆", 150), K.W * 0.78, cy + 190, K.ease_back(p, 2.5), rot=-15)
    return fr


def s_steps(t, d, a, ctx):
    # the clip shows one finger, then two at ~2.9 s: map it so "two" lands on the spoken word
    two_at = ctx["words"][40][1] - ctx["starts"][8] + 0.1
    ct = 2.9 - two_at + t
    fr, _ = video("K6", ct, 1.12, 0.5, 0.36)
    for i in range(2):
        at = 0.05 if i == 0 else two_at
        p = (t - at) / 0.22
        if p > 0:
            K.paste(fr, num_badge(str(i + 1)), K.W * (0.16 + i * 0.2), 330, K.ease_back(p, 2.6) * 0.8, rot=(-1) ** i * 8)
    return fr


def s_knows(t, d, a, ctx):
    # the wink in the clip (~2.2 s) lands on "knows"
    knows = ctx["words"][45][1] - ctx["starts"][9]
    fr, q = video("K7", 2.2 - knows + t, 1.05, 0.5, 0.42, K.ui_home())
    p = (t - knows - 0.05) / 0.35
    if p > 0:
        K.paste(fr, sticker("sprites/noli-thumbsup.png"), K.W * 0.22, K.H * 0.86, 0.42 * K.spring(p), rot=-8 + 3 * math.sin(t * 6),
                anchor="b")
    return fr


def post(fr, t, n):
    return K.grain(fr, n, 4)


cap = K.make_captions(K.INTER_BLACK, 82, 1330, color=K.WHITE, key=K.WHITE, stroke=9, stroke_color=(0, 0, 0), shadow=0, max_words=3,
                      mode="build", box=(0, 170, 235))
J = {"name": "swoosh-fast", "at": 0.0, "gain": 0.35}   # soft jump-cut whoosh
shots = [
    dict(w=0, scene=s_hook, sfx=[{"name": "pop", "at": 0.02}]),
    dict(w=3, scene=s_hook2, sfx=[J, {"name": "pop", "at": 0.15}]),
    dict(w=10, scene=s_strip, tr="whip", sfx=[{"name": "ui-pop", "at": 0.05}, {"name": "ui-pop", "at": 0.35}, {"name": "bubble", "at": 0.6, "gain": 0.6}]),
    dict(w=14, scene=s_open, sfx=[J, {"name": "tap", "at": 0.25}]),
    dict(w=18, scene=s_noli, sfx=[J, {"name": "cartoon-splash", "at": 0.22, "gain": 0.8}, {"name": "bloop", "at": 0.27}]),
    dict(w=21, scene=s_type, tr="whip", sfx=[{"name": "tap", "at": 0.2 + 0.14 * i} for i in range(6)]),
    dict(w=27, scene=s_whats_off, tr="zoom", cap_y=1700, sfx=[{"name": "select", "at": 0.25}]),
    dict(w=33, scene=s_fix_first, cap_y=1700, sfx=[J, {"name": "pop", "at": 0.35}, {"name": "ding", "at": 0.15, "gain": 0.6}]),
    dict(w=38, scene=s_steps, tr="whip", sfx=[{"name": "pop", "at": 0.05}, {"name": "pop", "at": 0.75}]),
    dict(w=42, scene=s_knows, sfx=[J, {"name": "wink", "at": 1.17}, {"name": "bloop", "at": 1.25}]),
    dict(w=46, scene=end_card, tr="slide", cap_y=1760, dur=3.0, sfx=[{"name": "pop", "at": 0.2}, {"name": "wink", "at": 0.45}]),
]

if __name__ == "__main__":
    spec = dict(name="nolidrop-ad-3", voice="ad3/voice-1.wav", max_gap=0.26, shots=shots, caption=cap, post=post,
                fixes={"Noly": "Noli", "Noly.": "Noli.", "1.": "one.", "2.": "two."},
                music=[{"t": 0.0, "file": "music/sounds-good.mp3", "start": 0.09, "vol": 1.0}], music_volume=0.28, duck=0.45,
                tail_gain=0.6)
    voice, words = K.prepare_voice(spec["voice"], K.HERE / "work" / spec["name"], spec["max_gap"], 1.0, spec["fixes"])
    shots[-1]["dur"] = words[-1][2] + 1.9 - (words[46][1] - 0.06)
    K.render(spec)
