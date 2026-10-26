"""Style test: documentary 'After Effects' look built in code (14 s, 1920x1080, 30 fps).

Effects: title text BEHIND the subject (rembg cutout layered over the text), 2.5D parallax (subject and background
move at different speeds), organic ink-reveal transitions (fractal-noise mask), light leaks, B&W subject on a red
glow with a caption ribbon, a 3D-tilted newspaper with a highlighter wipe (HyperFrames card article.mp4), a red
brush-stroke title, dust particles, film grain, vignette and a moody grade. Sound: music bed + whooshes / hits.
Usage: python3 fx_demo.py  ->  fx-demo.mp4   (needs *-cut.png from rembg and article.mp4)
"""
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent.parent / "reels"))
from make_long import SFX, blit, ease_out, ease_io, ease_back, warp  # noqa: E402
from make_reel import read_audio, write_wav  # noqa: E402

W, H, FPS, SR = 1920, 1080, 30, 44100
DUR = 14.3
ANTON = str(HERE.parent / "fonts" / "Anton-Regular.ttf")
MONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"   # static bold face (the variable Montserrat loads as Thin in PIL)
IMG = HERE.parent / "asteroid-full" / "img"
YELLOW, WHITE, RED = (255, 214, 10), (245, 245, 245), (205, 32, 32)
rng0 = np.random.default_rng(7)


def load(name):
    return cv2.cvtColor(cv2.imread(str(IMG / f"{name}.jpg")), cv2.COLOR_BGR2RGB)


def load_cut(name):
    im = np.asarray(Image.open(HERE / f"{name}-cut.png").convert("RGBA")).copy()
    a = im[..., 3].astype(np.float32) / 255
    a = np.clip((a - 0.45) / 0.35, 0, 1)                      # drop faint matte residue, choke the edge a little
    im[..., 3] = (cv2.GaussianBlur(a, (0, 0), 1.2) * 255).astype(np.uint8)
    return im


def warp_rgba(im, fx, fy, z):
    """Same camera as make_long.warp, for an RGBA layer (transparent outside)."""
    ih, iw = im.shape[:2]
    s = max(W / iw, H / ih) * z
    vw, vh = W / s, H / s
    cx = min(max(fx * iw, vw / 2), iw - vw / 2)
    cy = min(max(fy * ih, vh / 2), ih - vh / 2)
    M = np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]])
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def over(dst, rgba, alpha=1.0):
    a = rgba[..., 3:4].astype(np.float32) / 255 * alpha
    return (dst.astype(np.float32) * (1 - a) + rgba[..., :3].astype(np.float32) * a).astype(np.uint8)


def text_rgba(txt, font, size, color, track=0, shadow=True):
    f = ImageFont.truetype(font, size)
    ws = [f.getlength(c) + track for c in txt]
    asc, desc = f.getmetrics()
    pad = 40
    im = Image.new("RGBA", (int(sum(ws)) + pad * 2, asc + desc + pad * 2), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(sh)
        x = pad
        for c, w in zip(txt, ws):
            d.text((x + 6, pad + 10), c, font=f, fill=(0, 0, 0, 170))
            x += w
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im)
    x, boxes = pad, []
    for c, w in zip(txt, ws):
        d.text((x, pad), c, font=f, fill=(*color, 255))
        boxes.append((x, x + w))
        x += w
    return np.asarray(im), boxes


def letters_in(fr, txt, font, size, color, cx, cy, t0, t, track=6, stagger=0.045):
    """Kinetic title: each letter drops in with a scale overshoot."""
    lay, boxes = text_rgba(txt, font, size, color, track)
    lw, lh = lay.shape[1], lay.shape[0]
    x0 = cx - lw / 2
    for i, (a, b) in enumerate(boxes):
        lt = t - t0 - i * stagger
        if lt <= 0 or txt[i] == " ":
            continue
        k = ease_back(lt / 0.32)
        piece = lay[:, max(int(a) - 20, 0):int(b) + 20]
        blit(fr, piece, x0 + (a + b) / 2, cy - 60 * (1 - min(k, 1)), scale=1 + 0.5 * (1 - min(lt / 0.22, 1)), alpha=min(1, lt / 0.1))


def fractal_noise(seed, h=135, w=240):
    r = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for o, amp in [(4, 1.0), (8, 0.5), (16, 0.25), (32, 0.13), (64, 0.07)]:
        g = r.random((max(h * o // 64, 2), max(w * o // 64, 2))).astype(np.float32)
        acc += cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC) * amp
    return (acc - acc.min()) / (acc.max() - acc.min())


def ink_mask(noise, p, center=(0.5, 0.5)):
    """Organic ink blot growing from `center`; p 0..1 -> mask 0..1 (full res), plus a rim for the dark ink edge."""
    h, w = noise.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx / w - center[0]) * 1.6) ** 2 + (yy / h - center[1]) ** 2)
    field = (1 - d) + 0.55 * noise
    thr = 1.55 - 1.9 * ease_io(p)
    m = np.clip((field - thr) / 0.06, 0, 1)
    rim = np.clip(1 - np.abs(field - thr) / 0.05, 0, 1)
    up = lambda a: np.clip(cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR), 0, 1)[..., None]  # noqa: E731
    return up(m), up(rim)


def light_leak(fr, t, t0, dur, seed=1):
    k = (t - t0) / dur
    if not 0 <= k <= 1:
        return fr
    env = np.sin(np.pi * k) ** 1.5
    r = np.random.default_rng(seed)
    leak = np.zeros((H // 4, W // 4, 3), np.float32)
    for _ in range(3):
        cx = r.uniform(0, W // 4) + (k - 0.5) * W // 4 * r.uniform(0.5, 1.2)
        cy = r.uniform(0, H // 4)
        col = np.array([255, r.uniform(110, 190), r.uniform(20, 70)], np.float32)
        yy, xx = np.mgrid[0:H // 4, 0:W // 4]
        g = np.exp(-(((xx - cx) / r.uniform(60, 140)) ** 2 + ((yy - cy) / r.uniform(50, 120)) ** 2))
        leak += g[..., None] * col
    leak = cv2.resize(leak, (W, H)) * env
    return np.clip(fr.astype(np.float32) + leak, 0, 255).astype(np.uint8)


def brush_layer(p, seed=3, y=0.66, height=170, width=1050):
    """Red brush stroke revealed left -> right with a ragged leading edge and bristle streaks."""
    r = np.random.default_rng(seed)
    lay = np.zeros((H, W, 4), np.uint8)
    x0 = (W - width) // 2
    xs = np.arange(width)
    top = (H * y - height / 2 + 14 * np.sin(xs / 90 + 1) + cv2.resize(r.random((1, 30)).astype(np.float32), (width, 1))[0] * 22).astype(int)
    bot = (H * y + height / 2 + 12 * np.sin(xs / 70) - cv2.resize(r.random((1, 30)).astype(np.float32), (width, 1))[0] * 22).astype(int)
    front = int(width * ease_out(p))
    for i in range(min(front, width)):
        lay[top[i]:bot[i], x0 + i] = (*RED, 255)
    streak = (r.random((height + 60, width)) > 0.985).astype(np.float32)
    streak = cv2.GaussianBlur(cv2.resize(streak, (width, height + 60)), (0, 0), sigmaX=18, sigmaY=0.6)
    sub = lay[int(H * y - height / 2 - 30):int(H * y + height / 2 + 30), x0:x0 + width]
    a = sub[..., 3].astype(np.float32) / 255
    a = np.clip(a - streak[:a.shape[0], :a.shape[1]] * 4, 0, 1)            # dry-brush gaps
    sub[..., 3] = (a * 255).astype(np.uint8)
    return lay


# ---------------------------------------------------------------- assets
bgA, cutA = load("torch-street"), load_cut("torch-street")
bgB, cutB = load("astronomer"), load_cut("astronomer")
bgD, cutD = load("survivors-fire"), load_cut("survivors-fire")
grayB = cv2.cvtColor(cv2.cvtColor(bgB, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
cutB_bw = cutB.copy()
g = cv2.cvtColor(cutB[..., :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
g = np.clip((g - 20) * 1.5, 0, 255).astype(np.uint8)
cutB_bw[..., :3] = cv2.cvtColor(g, cv2.COLOR_GRAY2RGB)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
red_glow = np.clip(1 - np.sqrt(((xx - W * 0.42) / (W * 0.55)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2), 0, 1)[..., None]
red_bg = (np.array([150, 14, 18], np.float32) * red_glow ** 1.4 + 6).astype(np.uint8)
noise1, noise2 = fractal_noise(11), fractal_noise(23)
art = subprocess.run(["ffmpeg", "-v", "error", "-ss", "0.2", "-i", str(HERE / "article.mp4"), "-t", "4.3", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     capture_output=True).stdout
art = np.frombuffer(art, np.uint8).reshape(-1, H, W, 3)
vig = np.clip(1 - 0.42 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.3, 0.4, 1)[..., None]
grain = [cv2.resize(rng0.normal(0, 5, (H // 2, W // 2)).astype(np.float32), (W, H))[..., None] for _ in range(6)]
dust = rng0.random((140, 4))   # x, y, size, speed


# ---------------------------------------------------------------- shots
def shot_a(t):   # 0 - 3.6: text behind the walking man, parallax push-in
    k = t / 3.6
    fr = warp(bgA, 0.5, 0.47, 1.75 + 0.10 * k)
    letters_in(fr, "24 HOURS", ANTON, 330, WHITE, W / 2, H * 0.34, 0.35, t, track=10)
    letters_in(fr, "TO IMPACT", ANTON, 210, YELLOW, W / 2, H * 0.62, 0.95, t, track=14, stagger=0.05)
    fr = over(fr, warp_rgba(cutA, 0.5, 0.47, 1.75 + 0.26 * k))   # subject on top, moving faster = depth
    return light_leak(fr, t, 0.0, 0.9, seed=4)


def shot_b(t):   # 3.0 - 6.8: B&W subject on red glow, caption ribbon
    lt = t - 3.0
    k = lt / 3.8
    fr = (red_bg.astype(np.float32) * 0.85 + warp(grayB, 0.5, 0.5, 1.15 + 0.05 * k).astype(np.float32) * 0.18).astype(np.uint8)
    fr = over(fr, warp_rgba(cutB_bw, 0.62 - 0.03 * k, 0.48, 1.2 + 0.12 * k))
    words = "SHE HAS ONE DAY TO WARN THE WORLD".split()
    n = int(np.clip((lt - 0.6) / 0.16, 0, len(words)))
    if lt > 0.45:
        bw = 1150 * ease_out((lt - 0.45) / 0.3)
        cy = H * 0.74
        fr[int(cy - 52):int(cy + 52), int(W / 2 - bw / 2):int(W / 2 + bw / 2)] = (fr[int(cy - 52):int(cy + 52), int(W / 2 - bw / 2):int(W / 2 + bw / 2)] * 0.15).astype(np.uint8)
        if n:
            lay, _ = text_rgba(" ".join(words[:n]), MONT, 46, WHITE, track=3, shadow=False)
            blit(fr, lay, W / 2, cy)
    return fr


def shot_c(t):   # 6.4 - 10.6: tilted newspaper, highlighter wipe (HyperFrames)
    i = min(int((t - 6.4) * FPS), len(art) - 1)
    return art[max(i, 0)].copy()


def shot_d(t):   # 10.2 - 14.3: parallax group + red brush title
    lt = t - 10.2
    k = lt / 4.1
    fr = warp(bgD, 0.5 + 0.03 * k, 0.5, 1.08 + 0.04 * k)
    fr = over(fr, warp_rgba(cutD, 0.5 - 0.02 * k, 0.55, 1.08 + 0.14 * k))
    if lt > 0.7:
        fr = over(fr, brush_layer(min(1, (lt - 0.7) / 0.45)))
    if lt > 1.05:
        lay, _ = text_rgba("DAY ONE", ANTON, 170, WHITE, track=18)
        s = 1 + 0.6 * (1 - ease_out((lt - 1.05) / 0.2))
        blit(fr, lay, W / 2, H * 0.66, scale=s, alpha=min(1, (lt - 1.05) / 0.08))
    if lt > 1.6:
        lay, _ = text_rgba("AFTER THE IMPACT", MONT, 40, (230, 230, 230), track=10, shadow=True)
        blit(fr, lay, W / 2, H * 0.79, alpha=min(1, (lt - 1.6) / 0.3))
    return fr


def frame(t):
    if t < 3.0:
        fr = shot_a(t)
    elif t < 3.7:                       # ink reveal A -> B
        m, rim = ink_mask(noise1, (t - 3.0) / 0.7, (0.6, 0.45))
        fr = (shot_a(t).astype(np.float32) * (1 - m) + shot_b(t).astype(np.float32) * m) * (1 - 0.65 * rim)
        fr = np.clip(fr, 0, 255).astype(np.uint8)
    elif t < 6.4:
        fr = shot_b(t)
    elif t < 6.8:                       # light-leak flash B -> C
        p = (t - 6.4) / 0.4
        fr = shot_b(t) if p < 0.5 else shot_c(t)
        fr = np.clip(fr.astype(np.float32) + 255 * np.sin(np.pi * p) ** 2 * np.array([1, 0.75, 0.45]), 0, 255).astype(np.uint8)
    elif t < 10.2:
        fr = shot_c(t)
    elif t < 10.9:                      # ink reveal C -> D
        m, rim = ink_mask(noise2, (t - 10.2) / 0.7, (0.35, 0.55))
        fr = np.clip((shot_c(t).astype(np.float32) * (1 - m) + shot_d(t).astype(np.float32) * m) * (1 - 0.65 * rim), 0, 255).astype(np.uint8)
    else:
        fr = shot_d(t)
    f = fr.astype(np.float32)
    f = (f - 128) * 1.08 + 122                                   # contrast
    lum = f.mean(axis=2, keepdims=True)
    f = lum + (f - lum) * 0.82                                   # slight desaturation
    f[..., 2] += 6 * (1 - lum[..., 0] / 255)                     # cool shadows
    f = f * vig + grain[int(t * FPS) % 6]
    for x, y, sz, sp in dust:                                    # drifting dust specks
        px = int((x * W + t * 25 * sp) % W)
        py = int((y * H - t * 40 * sp) % H)
        r = 1 + int(sz * 2.5)
        cv2.circle(f, (px, py), r, (235, 235, 235), -1, lineType=cv2.LINE_AA) if sz > 0.85 else None
    f *= min(1, t / 0.25) * min(1, (DUR - t) / 0.5)              # fade in / out
    return np.clip(f, 0, 255).astype(np.uint8)


def soundtrack():
    n = int(DUR * SR)
    mix = np.zeros((n, 2), np.float32)
    music = read_audio(HERE.parent.parent / "reels" / "audio" / "music" / "echoes.mp3", start=162.865, dur=DUR)[:n]
    env = np.ones(len(music), np.float32)
    env[: int(0.5 * SR)] = np.linspace(0, 1, int(0.5 * SR))
    env[-int(0.8 * SR):] = np.linspace(1, 0, int(0.8 * SR))
    mix[: len(music)] += music * env[:, None] * 0.55
    cues = [("trailer", 0.35, 0.7), ("impact", 0.4, 0.6), ("bass", 0.95, 0.7), ("tunnel", 3.3, 0.7), ("typing", 3.65, 0.5),
            ("whoosh", 6.6, 0.8), ("sweep", 7.4, 0.6), ("sweep", 7.95, 0.5), ("tunnel", 10.5, 0.7),
            ("swoosh-fast", 10.95, 0.8), ("impact", 11.25, 0.8), ("boom", 11.3, 0.5)]
    for name, at, g in cues:
        f, peak, pre, post, bg = SFX[name]
        pre = min(pre, peak, at)
        clip = read_audio(f, start=peak - pre, dur=pre + post)
        s = int((at - pre) * SR)
        e = min(s + len(clip), n)
        mix[s:e] += clip[: e - s] * bg * g
    mix *= 0.98 / max(np.abs(mix).max(), 1e-6)
    write_wav(HERE / "fx-demo.wav", mix, af="loudnorm=I=-15:TP=-1.5:LRA=11")


def main():
    soundtrack()
    out = HERE / "fx-demo.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", str(HERE / "fx-demo.wav"), "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        enc.stdin.write(frame(i / FPS).tobytes())
    enc.stdin.close()
    enc.wait()
    print(out)


if __name__ == "__main__":
    if len(sys.argv) > 1:   # QA: python3 fx_demo.py 1.2 3.4 ...  -> stills
        tiles = [cv2.resize(frame(float(t)), (640, 360)) for t in sys.argv[1:]]
        while len(tiles) % 3:
            tiles.append(np.zeros_like(tiles[0]))
        sheet = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
        cv2.imwrite(str(HERE / "qa.jpg"), cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR))
    else:
        main()
