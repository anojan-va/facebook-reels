"""The Craft Hub reel 3 - UGC "POV: I went to a craft night alone". Edit of the user's five Google Omni clips (omni/,
frames extracted to work/clips/<name>/NNN.jpg, audio to work/omni-audio/<name>.wav). Her own lip-synced audio is kept;
jump cuts remove her pauses; captions, paper sticker labels, soft music bed, SFX and the brand end card are added.
python3 reel3.py [--stills | --frame t1,t2]"""
import math
import subprocess
import sys
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw

import craftkit as C
from craftkit import CREAM, GREEN, MUSTARD, TERRA, K, W, H
from make_reel import read_audio, write_wav  # noqa: E402 (on sys.path via adkit)

SR, FPS, CFPS = K.SR, K.FPS, 24
# (clip, in, out, zoom, focus y, sticker label, words [(text, clip time)])
SEGS = [
    ("c1-street", 1.05, 3.55, 1.0, 0.42, None,
     [("Making", 1.28), ("friends", 1.55), ("in", 1.75), ("Berlin", 1.85), ("as", 2.45), ("an", 2.6), ("adult?", 2.8)]),
    ("c1-street", 4.50, 5.75, 1.28, 0.36, None, [("Impossible.", 4.62)]),
    ("c2-wave", 0.10, 2.40, 1.0, 0.5, ("went to a craft night alone", "😬"), []),
    ("c3-wheel", 2.05, 4.65, 1.0, 0.5, ("first time on the wheel", None), []),
    ("c4-cheers", 0.30, 2.80, 1.08, 0.5, ("strangers to friends in 2 hours", None), []),
    ("c5-mug", 0.35, 3.45, 1.0, 0.45, None,
     [("Okay,", 0.45), ("I", 1.0), ("came", 1.15), ("alone,", 1.3), ("I'm", 1.9), ("leaving", 2.05), ("with", 2.3),
      ("three", 2.55), ("friends,", 2.85)]),
    ("c5-mug", 4.38, 5.95, 1.25, 0.4, None, [("and", 4.4), ("a", 4.55), ("very", 4.65), ("wonky", 4.9), ("mug.", 5.25)]),
]
END = 2.8
starts, t = [], 0.0
for s in SEGS:
    starts.append(t)
    t += s[2] - s[1]
END_START = t
TOTAL = t + END
WORDS = []   # output-timeline words for the caption renderer
for k, s in enumerate(SEGS):
    ws = s[6]
    for j, (w, ct) in enumerate(ws):
        a = starts[k] + ct - s[1]
        e = starts[k] + (ws[j + 1][1] - s[1]) if j + 1 < len(ws) else starts[k] + s[2] - s[1] - 0.1
        WORDS.append([w, a, e])


@lru_cache(maxsize=96)
def clip_frame(name, n):
    n = int(min(max(n, 0), 143))
    return np.ascontiguousarray(cv2.imread(str(C.HERE / "work" / "clips" / name / f"{n + 1:03d}.jpg"))[..., ::-1])


def video_frame(k, lt):
    name, a, b, z, fy, _, _ = SEGS[k]
    ct = a + lt
    fr = clip_frame(name, ct * CFPS)
    zz = z * (1 + 0.025 * lt)   # slow handheld push
    out = K.cover_np(fr, 0, 1, zz, zz, 0.5, fy).astype(np.float32)
    bl = cv2.GaussianBlur(out, (0, 0), 1.2)
    return np.clip(out * 1.3 - bl * 0.3, 0, 255)


def sticker_label(fr, k, lt):
    lab = SEGS[k][5]
    if not lab:
        return
    text, emoji = lab
    layer = C.label(text, 60, CREAM, GREEN, C.HAND2, rot_seed=k)
    p = (lt - 0.15) / 0.25
    if p <= 0:
        return
    K.paste(fr, layer, W / 2, 360, K.spring(min(p, 3), 2.4, 5), rot=(-1) ** k * 3)
    if emoji:
        from fonts import emoji_image
        e = np.asarray(emoji_image(emoji, 120).convert("RGBA"))
        K.paste(fr, e, W / 2 + layer.shape[1] / 2 + 30, 285, K.ease_back((lt - 0.35) / 0.25, 2.5) if lt > 0.35 else 0.01)


cap = K.make_captions(K.INTER_BLACK, 80, 1340, color=K.WHITE, key=K.WHITE, stroke=9, stroke_color=(0, 0, 0), shadow=0,
                      max_words=3, mode="build", box=TERRA)


def frame(nf):
    t = nf / FPS
    if t >= END_START:
        lt = t - END_START
        fr = C.end_card(lt, END, {"line": "Craft & Connect nights from €10"}, {}).astype(np.float32)
        if lt < 0.32:   # page turn from the last clip
            a = video_frame(len(SEGS) - 1, SEGS[-1][2] - SEGS[-1][1] - 0.01)
            fr = C.transition("page", a, fr, lt / 0.32, nf).astype(np.float32)
        return np.clip(fr, 0, 255).astype(np.uint8)
    k = max(i for i, s in enumerate(starts) if s <= t + 1e-9)
    lt = t - starts[k]
    fr = video_frame(k, lt)
    sticker_label(fr, k, lt)
    if SEGS[k][6]:
        cap(fr, WORDS, t, {"cap_y": 1340}, starts[k])
    fr = fr * np.array([1.03, 1.0, 0.97], np.float32) + 2
    return np.clip(K.grain(fr, nf, 3), 0, 255).astype(np.uint8)


def build_audio(work):
    n = int(TOTAL * SR)
    dia = np.zeros((n, 2), np.float32)
    xf = int(0.012 * SR)
    for k, (name, a, b, *_rest) in enumerate(SEGS):
        seg = read_audio(C.HERE / "work" / "omni-audio" / f"{name}.wav", start=a, dur=b - a)
        g = 1.0 if SEGS[k][6] else 0.55   # b-roll: room sound / laughter a bit lower
        seg = seg * g
        seg[:xf] *= np.linspace(0, 1, xf)[:, None]
        seg[-xf:] *= np.linspace(1, 0, xf)[:, None]
        s0 = int(starts[k] * SR)
        e = min(s0 + len(seg), n)
        dia[s0:e] += seg[:e - s0]
    # music bed, ducked under speech
    music = read_audio(C.HERE / "music" / "happy-home.mp3", start=30.0, dur=TOTAL + 0.5)[:n]
    env = np.abs(dia).mean(axis=1)
    hop = 441
    fr_ = env[:len(env) // hop * hop].reshape(-1, hop).max(axis=1)
    g, lvl = np.empty_like(fr_), 0.0
    for i, v in enumerate(fr_):
        lvl = max(v, lvl * 0.9)
        g[i] = 0.35 if lvl > 0.02 else 1.0
    g = np.convolve(g, np.ones(10) / 10, "same")
    gain = np.concatenate([np.repeat(g, hop), np.ones(n - len(g) * hop)])
    fo = int(0.8 * SR)
    gain[-fo:] *= np.linspace(1, 0, fo)
    mix = dia + music[:n] * gain[:, None] * 0.22
    sfx = [("swoosh-fast", starts[1], 0.35), ("pop", starts[2] + 0.15, 0.9), ("swoosh-fast", starts[2], 0.4),
           ("pop", starts[3] + 0.15, 0.9), ("swoosh-fast", starts[3], 0.4), ("pop", starts[4] + 0.15, 0.9),
           ("swoosh-fast", starts[4], 0.4), ("swoosh-fast", starts[5], 0.4), ("swoosh-fast", starts[6], 0.35),
           ("bloop", starts[6] + 1.0, 0.8), ("page", END_START + 0.05, 1.0), ("wink", END_START + 0.6, 1.0)]
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
    write_wav(work / "music.wav", music[:n] * gain[:, None] * 0.22)
    write_wav(work / "mix.wav", mix, af="loudnorm=I=-14:TP=-1.5:LRA=11")


if __name__ == "__main__":
    work = C.HERE / "work" / "crafthub-reel-3"
    work.mkdir(parents=True, exist_ok=True)
    print("segments:", [(SEGS[k][0], round(starts[k], 2)) for k in range(len(SEGS))], "end", round(END_START, 2), "total", round(TOTAL, 2))
    if "--frame" in sys.argv:
        for tt in sys.argv[sys.argv.index("--frame") + 1].split(","):
            Image.fromarray(frame(int(float(tt) * FPS))).save(work / f"frame_{tt}.jpg", quality=90)
        sys.exit()
    if "--stills" in sys.argv:
        ts = [starts[k] + (SEGS[k][2] - SEGS[k][1]) * 0.6 for k in range(len(SEGS))] + [END_START + 1.5]
        ims = [Image.fromarray(frame(int(x * FPS))).resize((270, 480)) for x in ts]
        S = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims):
            S.paste(im, (270 * i, 0))
        S.save(work / "stills.jpg", quality=85)
        print(work / "stills.jpg")
        sys.exit()
    build_audio(work)
    out = C.HERE / "output" / "crafthub-reel-3.mp4"
    nfr = int(TOTAL * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", str(work / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)],
                         stdin=subprocess.PIPE)
    for nf in range(nfr):
        p.stdin.write(frame(nf).tobytes())
    p.stdin.close()
    p.wait()
    print(out, f"{TOTAL:.2f}s")
