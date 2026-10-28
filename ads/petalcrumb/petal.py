"""Petal & Crumb cake-jar ad (9:16): edit of three AI clips made by the user (clips/: v1 hand -> dreamy explosion,
v2 hero spin, v3 spoon scoop). Adds script/Poppins text overlays, soft transitions, the real label as the logo on the
end card, a dreamy music bed with the clips' own whooshes, and accent SFX.
python3 petal.py [--stills | --frame t1,t2]"""
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "nolidrop"))
import adkit as K  # noqa: E402
from make_reel import read_audio, write_wav  # noqa: E402

K.HERE = HERE   # voice / work paths resolve inside ads/petalcrumb

W, H, FPS, SR, CFPS = K.W, K.H, K.FPS, K.SR, 24
SCRIPT, POP, POPS = str(HERE / "fonts/GreatVibes.ttf"), str(HERE / "fonts/Poppins-Medium.ttf"), str(HERE / "fonts/Poppins-SemiBold.ttf")
LILAC, BLUSH, PLUM, CREAM = (150, 104, 160), (238, 178, 186), (96, 58, 96), (255, 248, 244)

# Voice-over (one TTS take, pauses tightened, 1.1x): word times drive the cuts and the text.
VO = dict(wav="vo/voice-1.wav", max_gap=0.4, speed=1.1, fixes={"petal": "Petal", "crumb.": "Crumb.", "Petal": "Petal"})
_v, WORDS = K.prepare_voice(VO["wav"], HERE / "work" / "vo", VO["max_gap"], VO["speed"], VO["fixes"])
VOICE = _v
wt = lambda i: WORDS[i][1]   # noqa: E731
# (clip, in, out, playback speed) - clip 2 plays a little slower so the hero holds through the ingredient list
SEGS = [("v1-transform", 0.0, 8.0, 1.0), ("v2-hero", 0.0, 6.0, 0.0), ("v3-spoon", 0.4, 3.9, 0.0)]
_s1 = 8.0
_s2_end = wt(26) - 0.2          # cut to the spoon just before "One spoon"
_s3_end = wt(31) - 0.12         # end card on "Petal and Crumb"
SEGS[1] = ("v2-hero", 0.0, 6.0, 6.0 / (_s2_end - _s1))
SEGS[2] = ("v3-spoon", 0.4, 3.9, 3.5 / (_s3_end - _s2_end))
starts = [0.0, _s1, _s2_end]
END_START = _s3_end
TOTAL = WORDS[-1][2] + 1.8
END = TOTAL - END_START


@lru_cache(maxsize=128)
def clip_frame(name, n):
    nmax = len(list((HERE / "work/frames" / name).glob("*.jpg"))) - 1
    n = int(min(max(n, 0), nmax))
    return np.ascontiguousarray(cv2.imread(str(HERE / "work/frames" / name / f"{n + 1:03d}.jpg"))[..., ::-1])


def seg_len(k):
    return (SEGS[k][2] - SEGS[k][1]) / SEGS[k][3]


def video(k, lt, z=1.0):
    name, a, _, sp = SEGS[k]
    fr = K.cover_np(clip_frame(name, (a + lt * sp) * CFPS), 0, 1, z, z, 0.5, 0.5).astype(np.float32)
    bl = cv2.GaussianBlur(fr, (0, 0), 1.2)
    return np.clip(fr * 1.3 - bl * 0.3, 0, 255)


@lru_cache(maxsize=64)
def txt(s, font, size, color=CREAM, glow=(120, 60, 110)):
    """Soft-shadowed text layer."""
    f = ImageFont.truetype(font, size)
    w = int(f.getlength(s)) + 80
    hh = int(size * 1.6) + 60
    im = Image.new("RGBA", (w, hh), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, hh), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((40, 20), s, font=f, fill=(*glow, 150))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(im).text((40, 20), s, font=f, fill=(*color, 255))
    return np.asarray(im)


@lru_cache(maxsize=16)
def chip(s, size=46):
    f = ImageFont.truetype(POPS, size)
    w = int(f.getlength(s)) + size * 1.4
    hh = int(size * 1.9)
    im = Image.new("RGBA", (int(w) + 20, hh + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 12, w + 10, hh + 12), hh // 2, fill=(90, 40, 80, 60))
    d.rounded_rectangle((10, 6, w + 10, hh + 6), hh // 2, fill=(255, 250, 248, 235))
    d.text((10 + size * 0.7, 6 + size * 0.36), s, font=f, fill=(*PLUM, 255))
    return np.asarray(im)


@lru_cache(maxsize=1)
def label_logo(size=520):
    """The real round Petal & Crumb label, cut out of the product photo (refs/product.jpg)."""
    im = Image.open(HERE / "refs/product.jpg").convert("RGB")
    cx, cy, ax, ay = 732, 985, 226, 238   # measured label ellipse, inset a few px from its rim
    crop = im.crop((cx - ay, cy - ay, cx + ay, cy + ay)).resize((size, size), Image.LANCZOS)
    k = size * 4 / (2 * ay)
    m = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(m).ellipse((size * 2 - ax * k, size * 2 - ay * k, size * 2 + ax * k, size * 2 + ay * k), fill=255)
    m = m.resize((size, size), Image.LANCZOS)
    rgba = np.dstack([np.asarray(crop), np.asarray(m)])
    pad = 40
    out = np.zeros((size + pad * 2, size + pad * 2, 4), np.uint8)
    sh = cv2.GaussianBlur(np.pad(np.asarray(m).astype(np.float32), pad), (0, 0), 16) * 0.35
    out[..., :3] = (110, 60, 90)
    out[..., 3] = np.roll(sh, 14, axis=0).astype(np.uint8)
    reg = out[pad:pad + size, pad:pad + size].astype(np.float32)
    a = rgba[..., 3:4] / 255.0
    reg[..., :3] = reg[..., :3] * (1 - a) + rgba[..., :3] * a
    reg[..., 3:4] = np.maximum(reg[..., 3:4], rgba[..., 3:4])
    out[pad:pad + size, pad:pad + size] = reg.astype(np.uint8)
    return out


def pop_in(fr, layer, x, y, lt, t0, s=1.0, dur=0.35, rise=40):
    p = (lt - t0) / dur
    if p <= 0:
        return
    k = K.ease_out(p)
    K.paste(fr, layer, x, y + (1 - k) * rise, s * (0.92 + 0.08 * K.ease_back(p, 2)), alpha=K.clamp(p * 1.6))


def petals(fr, t, n=14, seed=2, alpha=0.85):
    """Drifting pink petal shapes (end card)."""
    rng = np.random.default_rng(seed)
    for i in range(n):
        x0, sp, sz, ph = rng.uniform(0, W), rng.uniform(80, 160), rng.uniform(18, 34), rng.uniform(0, 6.28)
        y = (rng.uniform(0, H) + t * sp) % (H + 100) - 50
        x = x0 + 40 * math.sin(t * 1.3 + ph)
        ang = (t * 60 + ph * 57) % 180
        col = (int(240 - 10 * (i % 3)), int(170 + 12 * (i % 4)), int(185 + 8 * (i % 2)))
        lay = np.zeros((H, W), np.uint8)
        cv2.ellipse(lay, (int(x), int(y)), (int(sz), int(sz * 0.6)), ang, 0, 360, 255, -1, cv2.LINE_AA)
        m = cv2.GaussianBlur(lay, (0, 0), 1.5).astype(np.float32)[..., None] / 255 * alpha
        fr[:] = fr * (1 - m) + np.array(col, np.float32) * m


def end_card(lt):
    bg = video(1, 3.6, 1.15)
    fr = cv2.GaussianBlur(bg, (0, 0), 28) * 0.7 + np.array([250, 226, 230], np.float32) * 0.3
    petals(fr, lt)
    p = (lt - 0.1) / 0.5
    if p > 0:
        K.paste(fr, label_logo(), W / 2, 740, 1.0 + 0.1 * K.ease_back(p, 1.8), alpha=K.clamp(p * 1.5))
    pop_in(fr, txt("cake jars, layered with love", SCRIPT, 110, PLUM, (255, 255, 255)), W / 2, 1150, lt, 0.5)
    pop_in(fr, chip("order your jar today", 60), W / 2, 1330, lt, wt(34) - END_START - 0.1)
    return fr


def frame(nf):
    t = nf / FPS
    if t >= END_START:
        lt = t - END_START
        fr = end_card(lt)
        if lt < 0.5:   # soft dissolve from the spoon shot
            a = video(2, seg_len(2) - 0.02)
            k = K.ease_io(lt / 0.5)
            fr = a * (1 - k) + fr * k
        return np.clip(fr, 0, 255).astype(np.uint8)
    k = max(i for i, s in enumerate(starts) if s <= t + 1e-9)
    lt = t - starts[k]
    d = seg_len(k)
    if k == 0:
        fr = video(0, lt, 1.0 + 0.04 * K.ease_io(lt / d))
        hook = txt("this isn't just cake…", SCRIPT, 132, CREAM)
        brand = txt("it's Petal & Crumb", SCRIPT, 120, CREAM)
        if t < wt(4) - 0.1:
            pop_in(fr, hook, W / 2, 300, t, 0.1)
        elif t < wt(8) - 0.2:
            pop_in(fr, brand, W / 2, 300, t, wt(4) - 0.1)
    elif k == 1:
        fr = video(1, lt, 1.04)
        if lt < 0.18:   # soft white flash on the cut
            fr = fr + (255 - fr) * (1 - lt / 0.18) * 0.8
        if t >= wt(20) - 0.1:
            pop_in(fr, txt("all layered in one little jar", SCRIPT, 104, CREAM), W / 2, 300, t, wt(20) - 0.1)
    else:
        fr = video(2, lt, 1.08 + 0.05 * K.ease_io(lt / d))
        pop_in(fr, txt("one spoon", SCRIPT, 150, CREAM), W / 2, 330, t, wt(26) - 0.1)
        pop_in(fr, txt("and you're gone", SCRIPT, 120, CREAM), W / 2, 500, t, wt(28) - 0.1)
        if lt < 0.4:   # dreamy blur-in from the hero
            a = video(1, seg_len(1) - 0.02, 1.04)
            kk = K.ease_io(lt / 0.4)
            fr = cv2.GaussianBlur(a, (0, 0), 1 + 20 * kk) * (1 - kk) + cv2.GaussianBlur(fr, (0, 0), 1 + 20 * (1 - kk)) * kk
    if wt(8) - 0.1 <= t < starts[2]:   # ingredient chips appear as they are spoken
        for (s, x, y, w_) in [("vanilla & pink sponge", 330, 1180, 8), ("silky cream", 800, 1100, 12),
                              ("berry jam", 290, 1320, 14), ("white choc pearls", 760, 1420, 17)]:
            pop_in(fr, chip(s, 48), x, y, t, wt(w_) - 0.1)
    return np.clip(K.grain(fr, nf, 2.5), 0, 255).astype(np.uint8)


def build_audio(work):
    n = int(TOTAL * SR)
    mix = np.zeros((n, 2), np.float32)
    xf = int(0.03 * SR)
    for k, (name, a, b, sp) in enumerate(SEGS):   # the clips' own whooshes / swells
        seg = read_audio(HERE / "work/audio" / f"{name}.wav", start=a, dur=min(b - a, seg_len(k) * sp)) * 0.6
        seg[:xf] *= np.linspace(0, 1, xf)[:, None]
        seg[-xf:] *= np.linspace(1, 0, xf)[:, None]
        s0 = int(starts[k] * SR)
        e = min(s0 + len(seg), n)
        mix[s0:e] += seg[:e - s0]
    music = read_audio(K.ROOT / "reels/audio/music/fifth-of-february.mp3", start=1.6, dur=TOTAL + 0.5)[:n]
    g = np.ones(n, np.float32)
    fo = int(1.2 * SR)
    g[-fo:] = np.linspace(1, 0, fo)
    vo = np.zeros((n, 2), np.float32)
    vo[:min(len(VOICE), n)] = VOICE[:n]
    env = np.abs(vo).mean(axis=1)
    hop = 441
    fr_ = env[:len(env) // hop * hop].reshape(-1, hop).max(axis=1)
    dk, lvl = np.empty_like(fr_), 0.0
    for i, v in enumerate(fr_):
        lvl = max(v, lvl * 0.9)
        dk[i] = 0.4 if lvl > 0.02 else 1.0
    dk = np.convolve(dk, np.ones(10) / 10, "same")
    duck = np.concatenate([np.repeat(dk, hop), np.ones(n - len(dk) * hop)])
    mix = mix * duck[:, None] * 0.8 + vo
    mix += music * (g * duck)[:, None] * 0.4
    sfx = [("pop", 1.45, 0.6), ("whoosh2", 2.3, 0.5), ("whoosh", starts[1], 0.45), ("whoosh2", starts[2], 0.45),
           ("wink", END_START + 0.15, 0.8)] + [("ui-pop", wt(w_) - 0.1, 0.45) for w_ in (8, 12, 14, 17)]
    for name, at, gg in sfx:
        f, peak, pre, post, bg = K.SFX[name]
        pre = min(pre, peak, max(at, 0))
        clip = read_audio(f, start=peak - pre, dur=pre + post)
        fade = min(len(clip), int(0.1 * SR))
        clip[-fade:] *= np.linspace(1, 0, fade)[:, None]
        s = int((at - pre) * SR)
        e = min(s + len(clip), n)
        if e > s >= 0:
            mix[s:e] += clip[:e - s] * bg * gg
    pk = np.abs(mix).max()
    if pk > 0.98:
        mix *= 0.98 / pk
    write_wav(work / "mix.wav", mix, af="loudnorm=I=-14:TP=-1.5:LRA=11")


if __name__ == "__main__":
    work = HERE / "work"
    print("starts", [round(s, 2) for s in starts], "end", round(END_START, 2), "total", round(TOTAL, 2))
    if "--frame" in sys.argv:
        for tt in sys.argv[sys.argv.index("--frame") + 1].split(","):
            Image.fromarray(frame(int(float(tt) * FPS))).save(work / f"frame_{tt}.jpg", quality=90)
        sys.exit()
    if "--stills" in sys.argv:
        ts = [0.8, 3.2, 5.5, 7.6, wt(14), wt(18), wt(22), starts[2] + 0.6, wt(29), END_START + 0.6, TOTAL - 0.4]
        ims = [Image.fromarray(frame(int(x * FPS))).resize((270, 480)) for x in ts]
        S = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims):
            S.paste(im, (270 * i, 0))
        S.save(work / "stills.jpg", quality=85)
        print(work / "stills.jpg")
        sys.exit()
    build_audio(work)
    out = HERE / "output" / "petal-and-crumb-ad-vo.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", str(work / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)],
                         stdin=subprocess.PIPE)
    for nf in range(int(TOTAL * FPS)):
        p.stdin.write(frame(nf).tobytes())
    p.stdin.close()
    p.wait()
    print(out, f"{TOTAL:.2f}s")
