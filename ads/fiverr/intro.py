"""Fiverr gig intro for Mano (social media video creator): 16:9 1920x1080 30 fps, ~28 s, music + SFX, no voice.
Built from the sample ads in deliveries/ shown in phone mock-ups, kinetic type and motion graphics, cut to the beat of
Mixkit "Trap Electro Vibes" (music/m126.mp3). Shares the NoliDrop kit (text, easing, paste, SFX table).
python3 intro.py [--extract | --stills | --frame t1,t2]"""
import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "ads" / "nolidrop"))
import adkit as K  # noqa: E402
from make_reel import read_audio, write_wav  # noqa: E402

W, H, FPS, SR = 1920, 1080, 30, 44100
K.W, K.H = W, H   # adkit's paste / grain / transition read these module globals
DLV = ROOT / "deliveries"
WORK = HERE / "work"
BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
XB = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
SB = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"
MED = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
INK = (9, 9, 18)
LIME = (200, 255, 61)
PINK = (255, 61, 127)
VIOLET = (120, 80, 255)
CYAN = (40, 210, 255)
WHITE = (255, 255, 255)
GREY = (170, 172, 190)

# music: offset so the track's first full-level beat (music 16.30 s) is the drop on beat 12 (output 6.42 s)
MUSIC, DROP_I = HERE / "music" / "m126.mp3", 12
_mb = json.load(open(HERE / "music" / "m126.beats.json"))["beats"]
_k = min(range(len(_mb)), key=lambda i: abs(_mb[i] - 16.30))
OFF = _mb[_k - DROP_I] - 0.15
BEATS = [b - OFF for b in _mb[_k - DROP_I:]]


def beat(i):
    return BEATS[i]


DROP = beat(DROP_I)
SV = [beat(DROP_I + 6 + 4 * i) for i in range(6)]   # name wall 6 beats, then five service scenes of one bar
PROOF, END = SV[5], beat(DROP_I + 34)
TOTAL = END + 4.4
PSTEP = (beat(1) - beat(0)) * 2.5    # proof ticks, spaced for the voice

# voice-over: one Gemini take (vo/voice-alnilam.wav, vo/script.txt) cut into phrases placed only where words sell;
# the services showreel stays music-only. name -> (phrase numbers in the take, output time; a string = set below)
VO_TAKE, VO_SPEED = "vo/voice-alnilam.wav", 1.2
VO_FASTER = {"scroll": 1.04, "sales": 1.1}   # extra tempo so the hook lands before the drop
VO_PLAN = {"scroll": ([0], beat(3) + 0.25), "sales": ([1], "after:scroll"), "mano": ([2], DROP + 0.4),
           "detail": ([4], SV[4] + 0.1), "fast": ([5], PROOF + 0.05), "eye": ([6], PROOF + 0.05 + PSTEP),
           "clear": ([7], PROOF + 0.05 + 2 * PSTEP), "brand": ([8], END + 0.1), "msg": ([9], "button")}


def _db(x, hop=441):
    m = x.mean(axis=1)
    nf = len(m) // hop
    return 20 * np.log10(np.sqrt((m[:nf * hop].reshape(nf, hop) ** 2).mean(axis=1)) + 1e-9)


def _runs(q, min_len):
    out, start = [], None
    for j, x in enumerate(list(q) + [False]):
        if x and start is None:
            start = j
        elif not x and start is not None:
            if j - start >= min_len:
                out.append((start, j))
            start = None
    return out


def _vo():
    """Cut the take into phrases at its silences (Whisper word times drift on this take, silences don't), squeeze
    pauses inside a phrase, and map the phrase's words onto it. -> {name: [start time, audio Nx2, [(word, s, e)]]}"""
    K.HERE = HERE
    voice, words = K.prepare_voice(VO_TAKE, WORK / "vo", 99.0, VO_SPEED)
    db = _db(voice)
    sil = _runs(db < db.max() - 42, 35)                     # >= 0.35 s = between lines
    edges = [0] + [x for r_ in sil for x in r_] + [len(db)]
    segs = [(edges[i] / 100, edges[i + 1] / 100) for i in range(0, len(edges) - 1, 2)]
    segs = [(a, b) for a, b in segs if b - a > 0.2]
    out = {}
    for name, (seg_ids, at) in VO_PLAN.items():
        a, b = segs[seg_ids[0]][0], segs[seg_ids[-1]][1]
        lead = np.where(db[int(a * 100):int(b * 100)] > db.max() - 42)[0]
        a = a + lead[0] / 100 if len(lead) else a
        a, b = max(a - 0.03, 0), min(b + 0.1, len(voice) / SR)
        clip_ = voice[int(a * SR):int(b * SR)]
        d2 = _db(clip_)
        keep, cur = [], 0                                    # pauses inside the phrase -> 0.12 s
        for r0, r1 in _runs(d2 < d2.max() - 28, 14):
            if r0 == 0 or r1 >= len(d2) - 2:
                continue
            keep.append(clip_[cur * 441:(r0 + 6) * 441])
            cur = r1 - 6
        keep.append(clip_[cur * 441:])
        f = int(0.008 * SR)
        for k_ in range(len(keep)):
            if k_:
                keep[k_][:f] *= np.linspace(0, 1, f)[:, None]
            if k_ < len(keep) - 1:
                keep[k_][-f:] *= np.linspace(1, 0, f)[:, None]
        clip_ = np.concatenate(keep)
        if name in VO_FASTER:
            write_wav(WORK / "vo" / "tmp.wav", clip_)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "vo" / "tmp.wav"), "-af", f"atempo={VO_FASTER[name]}",
                            str(WORK / "vo" / "tmp2.wav")], check=True)
            clip_ = read_audio(WORK / "vo" / "tmp2.wav")
        ws = [w for w in words if a <= w[2] - 0.01 <= b]
        w0, w1 = ws[0][1], ws[-1][2]
        L = len(clip_) / SR - 0.12   # words spread linearly over the phrase (good to ~0.1 s for pops)
        out[name] = [at, clip_, [(w, 0.02 + (s_ - w0) / (w1 - w0) * L, 0.02 + (e_ - w0) / (w1 - w0) * L) for w, s_, e_ in ws]]
    out["sales"][0] = out["scroll"][0] + len(out["scroll"][1]) / SR + 0.1
    out["msg"][0] = 0.0   # placed after "...stand out." below
    for v in out.values():
        v[2] = [(w, v[0] + ws_, v[0] + we) for w, ws_, we in v[2]]
    return out


END_OUT = None   # set after VO load: when MANO + the button come in (after "...stand out.")


# sample-ad excerpts: name -> (file, start s, length s); extracted to work/clips/<name>/NNN.jpg at 608x1080
CLIPS = {
    "n1-green": ("nolidrop-ad-1", 1.0, 3.0), "n1-app": ("nolidrop-ad-1", 8.0, 4.6), "n1-noli": ("nolidrop-ad-1", 16.6, 3.0),
    "n2-brain": ("nolidrop-ad-2", 0.0, 4.6), "n2-choice": ("nolidrop-ad-2", 8.9, 3.0), "n2-panic": ("nolidrop-ad-2", 3.6, 4.6),
    "n3-ugc": ("nolidrop-ad-3", 0.0, 3.0), "n3-phone": ("nolidrop-ad-3", 3.8, 4.6),
    "pc-burst": ("petal-and-crumb-ad-vo", 3.6, 4.6), "pc-spoon": ("petal-and-crumb-ad-vo", 14.8, 3.0),
    "pc-hero": ("petal-and-crumb-ad-vo", 5.0, 3.0),
    "c1-card": ("crafthub-reel-1", 6.8, 4.6), "c1-grid": ("crafthub-reel-1", 3.0, 3.0),
    "c2-friends": ("crafthub-reel-2", 5.0, 3.0), "c3-street": ("crafthub-reel-3", 0.0, 3.0),
    "c3-cheers": ("crafthub-reel-3", 8.6, 4.6), "c3-wheel": ("crafthub-reel-3", 5.6, 3.0),
}
SW, SH = 608, 1080


def extract():
    for name, (f, s, d) in CLIPS.items():
        out = WORK / "clips" / name
        out.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s), "-t", str(d), "-i", str(DLV / f"{f}.mp4"),
                        "-vf", f"fps={FPS},scale={SW}:{SH}", "-q:v", "2", str(out / "%03d.jpg")], check=True)
        print(name, len(list(out.glob("*.jpg"))))


@lru_cache(maxsize=None)
def _nframes(name):
    return len(list((WORK / "clips" / name).glob("*.jpg")))


@lru_cache(maxsize=400)
def clip(name, n):
    n = int(min(max(n, 0), _nframes(name) - 1))
    return np.ascontiguousarray(cv2.imread(str(WORK / "clips" / name / f"{n + 1:03d}.jpg"))[..., ::-1])


def clip_at(name, lt):
    return clip(name, int(max(lt, 0) * FPS))


# ------------------------------------------------------------------ easing
ease_o, ease_io, ease_back, spring, clamp = K.ease_out, K.ease_io, K.ease_back, K.spring, K.clamp


def p(t, t0, d):
    return clamp((t - t0) / d)


# ------------------------------------------------------------------ background
_gy, _gx = np.mgrid[0:135, 0:240].astype(np.float32)


def bg(t, cols=(VIOLET, PINK, CYAN), base=INK, amt=1.0):
    """Dark base with three slow, soft colour blobs (computed at 1/8 res, upscaled) + a faint dot grid."""
    f = np.zeros((135, 240, 3), np.float32) + np.array(base, np.float32)
    for i, c in enumerate(cols):
        cx = 120 + 95 * math.sin(t * 0.35 + i * 2.1)
        cy = 68 + 45 * math.cos(t * 0.28 + i * 1.7)
        r = 70 + 12 * math.sin(t * 0.5 + i)
        g = np.exp(-((_gx - cx) ** 2 + (_gy - cy) ** 2) / (2 * r * r))[..., None]
        f += np.array(c, np.float32) * g * 0.32 * amt
    fr = cv2.resize(f, (W, H), interpolation=cv2.INTER_CUBIC)
    return fr * _dots()


@lru_cache(maxsize=1)
def _dots():
    m = np.ones((H, W), np.float32)
    m[24::48, 24::48] = 1.9
    m = cv2.GaussianBlur(m, (0, 0), 0.8)
    return m[..., None]


@lru_cache(maxsize=4)
def _vig(s):
    y, x = np.ogrid[:H, :W]
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2) / 1.414
    return (1 - s * np.clip(r - 0.3, 0, 1) ** 1.5 * 1.7).astype(np.float32)[..., None]


def finish(fr, nf):
    fr = fr * _vig(0.45)
    return np.clip(K.grain(fr, nf, 3.5), 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ phone mock-up
@lru_cache(maxsize=16)
def _phone_parts(sh):
    sw = int(round(sh * 9 / 16))
    bz = max(int(sh * 0.022), 6)
    pw, ph = sw + 2 * bz, sh + 2 * bz
    s = 3   # supersampled shapes
    body = Image.new("RGBA", (pw * s, ph * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    R = int(sw * 0.15) * s
    d.rounded_rectangle([0, 0, pw * s - 1, ph * s - 1], R + bz * s, fill=(28, 28, 34, 255))
    d.rounded_rectangle([2 * s, 2 * s, pw * s - 1 - 2 * s, ph * s - 1 - 2 * s], R + bz * s - 2 * s, outline=(120, 122, 138, 255),
                        width=max(s, int(1.6 * s)))
    body = np.asarray(body.resize((pw, ph), Image.LANCZOS)).astype(np.float32)
    m = Image.new("L", (sw * s, sh * s), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, sw * s - 1, sh * s - 1], R, fill=255)
    mask = np.asarray(m.resize((sw, sh), Image.LANCZOS)).astype(np.float32)[..., None] / 255
    isl = Image.new("L", (sw * s, sh * s), 0)
    iw, ih = int(sw * 0.3) * s, int(sh * 0.028) * s
    ImageDraw.Draw(isl).rounded_rectangle([(sw * s - iw) // 2, int(sh * 0.018) * s, (sw * s + iw) // 2, int(sh * 0.018) * s + ih],
                                          ih // 2, fill=255)
    island = np.asarray(isl.resize((sw, sh), Image.LANCZOS)).astype(np.float32)[..., None] / 255
    # glass sheen: faint diagonal highlight
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    sheen = np.clip(1 - np.abs((xx / sw + yy / sh * 0.5) - 0.42) / 0.12, 0, 1)[..., None] * 0.06
    return sw, bz, body, mask, island, sheen


def phone(screen, sh):
    """RGBA uint8 phone showing `screen` (HxWx3) with a screen height of sh px."""
    sw, bz, body, mask, island, sheen = _phone_parts(int(sh))
    scr = cv2.resize(screen, (sw, int(sh)), interpolation=cv2.INTER_AREA).astype(np.float32)
    scr = scr * (1 - island) + 8 * island
    scr = scr + (255 - scr) * sheen
    out = body.copy()
    reg = out[bz:bz + int(sh), bz:bz + sw]
    reg[..., :3] = reg[..., :3] * (1 - mask) + scr * mask
    reg[..., 3:] = np.maximum(reg[..., 3:], mask * 255)
    return out.astype(np.uint8)


def glow(fr, cx, cy, rx, ry, color, a):
    """Soft coloured light behind an object."""
    x0, x1 = int(max(cx - rx * 2, 0)), int(min(cx + rx * 2, W))
    y0, y1 = int(max(cy - ry * 2, 0)), int(min(cy + ry * 2, H))
    if x1 <= x0 or y1 <= y0:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    g = np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) * 1.2)[..., None] * a
    reg = fr[y0:y1, x0:x1]
    reg[:] = reg + (np.array(color, np.float32) - reg * 0.35) * g


def put_phone(fr, name, lt, cx, cy, sh, rot=0.0, alpha=1.0, scale=1.0, shadow=0.8, light=None):
    if alpha <= 0.01 or scale <= 0.01:
        return
    if light:
        glow(fr, cx, cy, sh * 0.42 * scale, sh * 0.55 * scale, light, 0.55 * alpha)
    ph = phone(clip_at(name, lt), sh)
    K.paste(fr, ph, cx, cy, scale, rot=rot, alpha=alpha, shadow=shadow)


# ------------------------------------------------------------------ type
def txt(s, size, color=WHITE, font=BLACK, track=0, glow_=0, glow_color=None):
    return K.text_im(s, font, int(size), color, track=track, glow=glow_, glow_color=glow_color)


def word_pop(fr, s, x, y, size, t, t0, color=WHITE, font=BLACK, anchor="l", dur=0.32, glow_=0, out_t=None, track=0):
    """A word that springs up from below with a scale overshoot; x is its left edge (anchor l) or centre (c)."""
    k = (t - t0) / dur
    if k <= 0:
        return 0
    im = txt(s, size, color, font, track, glow_, color if glow_ else None)
    w = im.shape[1]
    a = clamp(k * 2.5)
    sc = 0.6 + 0.4 * spring(min(k, 4), 2.2, 5.5)
    dy = (1 - ease_o(clamp(k))) * size * 0.45
    if out_t is not None and t > out_t:
        q = clamp((t - out_t) / 0.18)
        a *= 1 - q
        dy -= q * size * 0.5
    cx = x + w / 2 if anchor == "l" else x
    K.paste(fr, im, cx, y + dy, sc, alpha=a)
    return w


def line_pop(fr, words, x, y, size, t, t0, gap=0.07, colors=None, font=BLACK, anchor="c", space=0.28, out_t=None, times=None):
    """A row of words popping in one after another; returns the total width."""
    ims = [txt(w, size, font=font) for w in words]
    ws = [im.shape[1] - 2 * (10) for im in ims]
    total = sum(ws) + size * space * (len(words) - 1)
    xx = x - total / 2 if anchor == "c" else x
    for i, w in enumerate(words):
        c = (colors or {}).get(i, WHITE)
        word_pop(fr, w, xx - 10, y, size, t, times[i] - 0.04 if times else t0 + i * gap, c, font, out_t=out_t)
        xx += ws[i] + size * space
    return total


def pill(text, size, fg=INK, bgc=LIME, font=XB, pad=(0.75, 0.42), outline=None):
    f_im = txt(text, size, fg, font)
    th, tw = f_im.shape[:2]
    pw, ph = int(tw + size * pad[0] * 2 - 20), int(size * (1 + pad[1] * 2))
    s = 3
    im = Image.new("RGBA", (pw * s, ph * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if outline:
        d.rounded_rectangle([0, 0, pw * s - 1, ph * s - 1], ph * s // 2, fill=(*bgc, 255) if bgc else None, outline=(*outline, 255), width=3 * s)
    else:
        d.rounded_rectangle([0, 0, pw * s - 1, ph * s - 1], ph * s // 2, fill=(*bgc, 255))
    im = im.resize((pw, ph), Image.LANCZOS)
    t_im = Image.fromarray(f_im)
    im.alpha_composite(t_im, ((pw - tw) // 2, (ph - th) // 2 + int(size * 0.02)))
    return np.asarray(im)


def pop_in(fr, im, cx, cy, t, t0, dur=0.3, rot=0.0, out_t=None, from_y=0.0):
    k = (t - t0) / dur
    if k <= 0:
        return
    sc = spring(min(k, 4), 2.0, 5.0)
    a = clamp(k * 3)
    if out_t is not None and t > out_t:
        q = clamp((t - out_t) / 0.18)
        a *= 1 - q
        sc *= 1 - 0.3 * q
    K.paste(fr, im, cx, cy + (1 - ease_o(clamp(k))) * from_y, max(sc, 0.01), rot=rot, alpha=a)


def bar_reveal(fr, x, y, w, h, k, color):
    """A solid bar that wipes in from the left (k 0..1) - used under labels."""
    ww = int(w * ease_io(clamp(k)))
    if ww > 0:
        fr[int(y):int(y + h), int(x):int(x + ww)] = color


def check_icon(size, color=LIME):
    s = 3
    im = Image.new("RGBA", (size * s, size * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, size * s - 1, size * s - 1], fill=(*color, 255))
    d.line([(size * s * 0.28, size * s * 0.52), (size * s * 0.44, size * s * 0.68), (size * s * 0.73, size * s * 0.35)],
           fill=(*INK, 255), width=int(size * s * 0.11), joint="curve")
    return np.asarray(im.resize((size, size), Image.LANCZOS))


def flash(fr, t, t0, d=0.22, a=0.85):
    k = (t - t0) / d
    if 0 <= k <= 1:
        fr += (255 - fr) * (1 - k) ** 2 * a


def punch(fr, t, t0, amt=0.05, d=0.35):
    """Zoom punch on a beat: frame scaled up then settling."""
    k = (t - t0) / d
    if 0 <= k <= 1:
        z = 1 + amt * (1 - ease_o(k))
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
        fr[:] = cv2.warpAffine(fr, M, (W, H), borderMode=cv2.BORDER_REFLECT)


def chroma(fr, px):
    if px >= 1:
        px = int(px)
        fr[..., 0] = np.roll(fr[..., 0], px, axis=1)
        fr[..., 2] = np.roll(fr[..., 2], -px, axis=1)


# ------------------------------------------------------------------ scenes (t = absolute seconds)
FEED = ["n1-green", "c1-card", "pc-burst", "n2-brain", "c3-street", "n3-ugc", "c2-friends", "n1-app", "pc-spoon",
        "c3-wheel", "n2-choice", "c1-grid"]


def s_hook(t):
    """0 - DROP: a fast blurred feed scrolls under SCROLL x3, freezes on STOP, then the promise builds to the drop."""
    fr = bg(t, amt=0.6)
    stop = beat(3)
    # feed of tiles scrolling upward (four columns), speed eases to zero at STOP
    if t < stop:
        spd = 2600 * (1 - 0.25 * t / stop)
        off = t * spd
    else:
        off = stop * 2600 * (1 - 0.125) + 40 * (1 - math.exp(-(t - stop) * 18))
    dim = 0.55 if t < stop else max(0.22, 0.55 - (t - stop) * 1.2)
    th = 520
    for c in range(5):
        x = 260 + c * 350
        for r in range(-1, 4):
            idx = (c * 3 + r + int((off + c * 170) // (th + 40))) % len(FEED)
            y = (r * (th + 40) - (off + c * 170) % (th + 40)) + 200
            ph = phone(clip_at(FEED[idx], 0.8), th)
            K.paste(fr, ph, x, y, 1.0, alpha=dim, shadow=0.0)
    if t < stop:
        bl = int(40 * (1 - 0.3 * t / stop)) | 1
        fr = cv2.blur(fr, (1, bl))
    else:
        fr = cv2.GaussianBlur(fr, (0, 0), clamp((t - stop) / 0.5) * 9 + 0.01)
        fr *= 1 - 0.35 * clamp((t - stop) / 0.4)
    # SCROLL. SCROLL. SCROLL.
    for i in range(3):
        b = beat(i)
        if t >= b and t < stop:
            k = (t - b) / 0.2
            im = txt("SCROLL", 190, WHITE if i == 2 else GREY, track=6)
            K.paste(fr, im, W / 2, H / 2 - 230 + i * 230 - (1 - ease_o(clamp(k))) * 120, 1.0, alpha=clamp(k * 3) * (0.35 if i < 2 and t > beat(i + 1) else 1))
    if t >= stop:
        k = (t - stop) / 0.25
        out = clamp((t - VO["scroll"][2][0][1] + 0.05) / 0.15)
        im = txt("STOP.", 330, LIME, glow_=18)
        K.paste(fr, im, W / 2, H / 2, 1.25 - 0.25 * ease_back(clamp(k), 2.2), alpha=clamp(k * 4) * (1 - out))
        flash(fr, t, stop, 0.18, 0.6)
        if t < stop + 0.25:
            chroma(fr, 18 * (1 - k))
    # promise, word by word on half beats
    if t >= VO["scroll"][2][0][1] - 0.1:
        line_pop(fr, ["Videos", "that", "stop", "the", "scroll"], W / 2, H / 2 - 70, 112, t, 0,
                 colors={2: LIME, 4: LIME}, times=[w[1] for w in VO["scroll"][2]])
        sw = [w[1] for w in VO["sales"][2]]   # "and get you sales" -> "and get views & sales."
        line_pop(fr, ["and", "get", "views", "&", "sales."], W / 2, H / 2 + 70, 112, t, 0,
                 colors={2: PINK, 4: PINK}, times=[sw[0], sw[1], sw[2], sw[2] + 0.12, sw[3]])
    return fr


WALL = ["n1-app", "pc-burst", "c3-cheers", "n2-brain", "c1-card", "n3-phone", "n2-panic"]


def s_wall(t):
    """DROP: a marquee of phones playing the ads, MANO name card on top."""
    lt = t - DROP
    fr = bg(t, amt=1.0)
    sh = 600
    sp = 395
    drift = lt * 70
    for i, name in enumerate(WALL):
        k = (lt - 0.03 * abs(i - 3)) / 0.45
        if k <= 0:
            continue
        x = W / 2 + (i - 3) * sp - drift
        y = 700 + (1 - ease_o(clamp(k))) * 500 + (24 if i % 2 else 0)
        rot = (i - 3) * -1.2
        put_phone(fr, name, lt, x, y, sh, rot=rot, alpha=clamp(k * 2), light=[VIOLET, PINK, CYAN][i % 3] if 1 < i < 5 else None)
    # dark band behind the title
    top = np.linspace(1, 0, 420, dtype=np.float32)[:, None, None]
    fr[:420] = fr[:420] * (1 - top * 0.75)
    mw = VO["mano"][2]
    word_pop(fr, "Hi, I'm", W / 2 - 230, 150, 96, t, mw[0][1] - 0.04, GREY, XB, anchor="c")
    word_pop(fr, "MANO", W / 2 + 190, 140, 150, t, mw[2][1] - 0.04, LIME, BLACK, anchor="c", glow_=10)
    k = (t - beat(DROP_I + 3)) / 0.4
    if k > 0:
        im = txt("SOCIAL MEDIA VIDEO CREATOR", 46, WHITE, SB, track=10)
        bar_reveal(fr, W / 2 - im.shape[1] / 2 + 6, 236, im.shape[1] - 12, 4, k, PINK)
        K.paste(fr, K.reveal_x(im, ease_o(clamp(k))), W / 2, 280, 1.0)
    flash(fr, t, DROP, 0.3, 0.9)
    punch(fr, t, DROP, 0.08, 0.5)
    if lt < 0.2:
        chroma(fr, 22 * (1 - lt / 0.2))
    return fr


# service scenes: (number, title, line or chips, hero clip, side clips, layout side, accent)
SERVICES = [
    ("01", "VIDEO ADS", ["Facebook", "Instagram", "TikTok", "YouTube"], "n2-panic", ["n1-noli", "pc-hero"], "R", PINK),
    ("02", "REELS & TIKTOKS", "Trendy, engaging short-form content", "c1-card", ["c2-friends"], "L", LIME),
    ("03", "YOUTUBE SHORTS", "Hook-driven videos built for reach", "n1-green", ["c3-wheel"], "R", CYAN),
    ("04", "UGC-STYLE ADS", "Authentic videos that build trust", "n3-ugc", ["c3-street"], "L", PINK),
    ("05", "PRO EDITING", ["Captions", "Music", "Transitions", "Effects"], "pc-burst", [], "C", LIME),
]
CHIP_COL = {"Facebook": (24, 119, 242), "Instagram": (225, 48, 108), "TikTok": (20, 20, 20), "YouTube": (255, 0, 0)}


def s_service(t, i):
    t0, t1 = SV[i], SV[i + 1]
    lt = t - t0
    num, title, sub, hero, side, lay, acc = SERVICES[i]
    fr = bg(t + i * 3, cols=(acc, VIOLET, CYAN) if acc != CYAN else (CYAN, VIOLET, PINK), amt=0.85)
    hb = (beat(1) - beat(0))
    if lay == "C":
        return s_editing(fr, t, lt, hb)
    px = 1440 if lay == "R" else 500        # phone group centre
    tx = 170 if lay == "R" else 1010        # text left edge
    # side phones behind the hero, fanned
    for j, nm in enumerate(side):
        k = (lt - 0.06) / 0.4
        dx = (-1 if (j == 0) == (lay == "R") else 1) * 250 if len(side) == 1 else (-260 if j == 0 else 260)
        put_phone(fr, nm, lt, px + dx * ease_o(clamp(k)), 560 + 40, 640, rot=(-7 if dx < 0 else 7) * ease_o(clamp(k)),
                  alpha=clamp(k * 2) * 0.9, scale=0.9)
    fr[:] = fr * 1.0
    k = lt / 0.4
    yb = 545 + (1 - ease_o(clamp(k))) * 700 - lt * 12
    put_phone(fr, hero, lt + (0.85 if i == 2 else 0.15), px, yb, 800, alpha=clamp(k * 2.5), light=acc)
    # text block
    word_pop(fr, num, tx, 300, 64, t, t0 + 0.05, acc, XB)
    bar_reveal(fr, tx + 100, 300 - 3, 140, 6, (lt - 0.1) / 0.3, acc)
    parts = title.split(" ")
    if len(title) > 11 and " " in title:   # two lines for long titles
        lines = [title.rsplit(" ", 1)[0], title.rsplit(" ", 1)[1]] if not title.startswith("UGC") else ["UGC-STYLE", "ADS"]
    else:
        lines = [title]
    size = 132
    for li, ln in enumerate(lines):
        word_pop(fr, ln, tx - 10, 420 + li * 140, size, t, t0 + 0.1 + li * 0.08, WHITE, BLACK, dur=0.3)
    y_sub = 420 + len(lines) * 140 + 30
    if isinstance(sub, list):   # platform chips on beats
        x = tx
        for ci, c in enumerate(sub):
            if ci == 2:
                x = tx
            im = pill(c, 40, WHITE, CHIP_COL.get(c, (40, 40, 60)))
            pop_in(fr, im, x + im.shape[1] / 2, y_sub + 10 + (ci // 2) * 82, t, t0 + 0.45 + ci * hb * 0.5, 0.3, from_y=30)
            x += im.shape[1] + 16
    else:
        k = (lt - 0.45) / 0.35
        if k > 0:
            im = txt(sub, 46, GREY, MED)
            K.paste(fr, K.reveal_x(im, ease_o(clamp(k))), tx - 10 + im.shape[1] / 2, y_sub, 1.0)
    if i == 2:   # "hook" call-out on the Shorts phone
        im = pill("HOOK IN 1s", 34, INK, CYAN)
        pop_in(fr, im, px + 300, 200, t, t0 + 0.7, 0.3, rot=-6)
        k = (lt - 0.85) / 0.25
        if k > 0:
            cv2.line(fr, (int(px + 230), 235), (int(px + 230 - 90 * ease_o(clamp(k))), int(235 + 90 * ease_o(clamp(k)))), CYAN, 5, cv2.LINE_AA)
    if i == 3:   # UGC: "real people" tag
        im = pill("REAL & RELATABLE", 32, WHITE, PINK)
        pop_in(fr, im, px, 960, t, t0 + 0.75, 0.3, rot=3)
    punch(fr, t, t0, 0.035, 0.35)
    return fr


def s_editing(fr, t, lt, hb):
    """Pro Editing: hero phone centre, editor timeline along the bottom, tool chips around the phone."""
    t0 = SV[4]
    k = lt / 0.4
    put_phone(fr, "pc-burst", lt + 0.4, W / 2, 430 + (1 - ease_o(clamp(k))) * 600, 640, alpha=clamp(k * 2.5), light=LIME)
    word_pop(fr, "05", 170, 300, 64, t, t0 + 0.05, LIME, XB)
    bar_reveal(fr, 270, 297, 140, 6, (lt - 0.1) / 0.3, LIME)
    word_pop(fr, "PRO", 160, 420, 132, t, t0 + 0.1, WHITE, BLACK)
    word_pop(fr, "EDITING", 160, 560, 132, t, t0 + 0.18, WHITE, BLACK)
    # timeline panel
    kk = ease_o(clamp((lt - 0.05) / 0.35))
    y0 = int(H - 250 * kk)
    panel = fr[y0:H, 120:W - 120]
    panel[:] = panel * 0.25 + np.array((22, 22, 34), np.float32) * 0.75
    if kk > 0.5:
        rows = [("V2", [(0.0, 0.22, PINK), (0.25, 0.48, VIOLET), (0.52, 0.8, PINK), (0.83, 1.0, VIOLET)]),
                ("V1", [(0.0, 0.35, CYAN), (0.37, 0.7, CYAN), (0.72, 1.0, CYAN)]),
                ("T", [(0.05, 0.18, LIME), (0.22, 0.36, LIME), (0.41, 0.55, LIME), (0.6, 0.74, LIME), (0.79, 0.93, LIME)]),
                ("A", [(0.0, 1.0, (90, 200, 140))])]
        x0, x1 = 230, W - 160
        for ri, (lab, segs) in enumerate(rows):
            yy = y0 + 30 + ri * 52
            K.paste(fr, txt(lab, 26, GREY, SB), 180, yy + 18, 1.0)
            for a, b, c in segs:
                grow = clamp((lt - 0.25 - a * 0.5 - ri * 0.05) / 0.25)
                if grow <= 0:
                    continue
                xa, xb = int(x0 + a * (x1 - x0)), int(x0 + (a + (b - a) * ease_o(grow)) * (x1 - x0))
                cv2.rectangle(fr, (xa + 2, yy), (xb - 2, yy + 38), [v * 0.85 for v in c], -1, cv2.LINE_AA)
                if lab == "A":   # waveform
                    xs = np.arange(xa, xb, 4)
                    amp = (np.abs(np.sin(xs * 0.05) * np.sin(xs * 0.013 + 1)) * 16 + 3).astype(int)
                    for xv, av in zip(xs, amp):
                        cv2.line(fr, (int(xv), yy + 19 - av), (int(xv), yy + 19 + av), (20, 60, 40), 2)
        ph = x0 + (x1 - x0) * clamp((lt - 0.2) / 1.9)   # playhead
        cv2.line(fr, (int(ph), y0 + 18), (int(ph), H - 10), WHITE, 3, cv2.LINE_AA)
        cv2.circle(fr, (int(ph), y0 + 16), 8, WHITE, -1, cv2.LINE_AA)
    # tool chips around the phone, one per half beat
    spots = [(1360, 250, -4), (1600, 360, 3), (1370, 480, 4), (1620, 590, -3)]
    for ci, c in enumerate(SERVICES[4][2]):
        x, y, r = spots[ci]
        im = pill("✓ " + c if False else c, 42, INK, [LIME, PINK, CYAN, WHITE][ci])
        pop_in(fr, im, x, y, t, t0 + 0.4 + ci * hb * 0.5, 0.3, rot=r, from_y=30)
    punch(fr, t, t0, 0.035, 0.35)
    return fr


PROOF_ITEMS = [("Fast", "delivery", LIME), ("Eye-catching", "edits", PINK), ("Clear", "communication", CYAN)]


def s_proof(t):
    lt = t - PROOF
    fr = bg(t, amt=0.7)
    # blurred wall drifting behind
    for i, name in enumerate(WALL[1:6]):
        x = W / 2 + (i - 2) * 420 + 60 - lt * 60
        put_phone(fr, name, lt + 1.5, x, 560 + (i % 2) * 30, 640, rot=(i - 2) * -2, alpha=0.9, shadow=0)
    fr = cv2.GaussianBlur(fr, (0, 0), 14)
    fr *= 0.42
    bb = beat(37) - beat(36)
    for j, (a, b, c) in enumerate(PROOF_ITEMS):
        tj = PROOF + 0.05 + j * PSTEP
        y = 330 + j * 200
        pop_in(fr, check_icon(110, c), 520, y, t, tj, 0.3)
        w = word_pop(fr, a, 610, y, 104, t, tj + 0.06, WHITE, BLACK)
        word_pop(fr, b, 610 + w + 6, y, 104, t, tj + 0.14, c, BLACK)
    punch(fr, t, PROOF, 0.05, 0.4)
    return fr


def s_end(t):
    lt = t - END
    fr = bg(t, cols=(LIME, VIOLET, PINK), amt=0.9)
    hb = (beat(1) - beat(0)) / 2
    out = END_OUT
    bw = [w[1] for w in VO["brand"][2]]
    line_pop(fr, ["Let's", "make", "your", "brand"], W / 2, H / 2 - 80, 120, t, 0, out_t=out, times=bw[:4])
    line_pop(fr, ["stand", "out."], W / 2, H / 2 + 70, 150, t, 0, colors={0: LIME, 1: LIME}, out_t=out, times=bw[4:])
    if t >= out:
        k = t - out
        im = txt("MANO", 220, WHITE, BLACK, track=14)
        K.paste(fr, im, W / 2, 330 - (1 - ease_o(clamp(k / 0.4))) * 60, 0.9 + 0.1 * ease_back(clamp(k / 0.4)), alpha=clamp(k / 0.2))
        k2 = (k - 0.25) / 0.4
        if k2 > 0:
            s = txt("SOCIAL MEDIA VIDEO CREATOR", 44, GREY, SB, track=10)
            K.paste(fr, K.reveal_x(s, ease_o(clamp(k2))), W / 2, 480, 1.0)
            bar_reveal(fr, W / 2 - 60, 530, 120, 5, k2, PINK)
        btn = pill("Message me today  →", 62, INK, LIME, BLACK, pad=(0.9, 0.5))
        ck = out + 1.45   # cursor click time
        press = 1 - 0.06 * math.exp(-((t - ck) / 0.06) ** 2) if t > ck - 0.2 else 1
        pop_in(fr, btn, W / 2, 700, t, out + 0.45, 0.35)
        if t > out + 0.45:
            glow(fr, W / 2, 700, 380, 90, LIME, 0.18 + 0.1 * math.sin(t * 6))
            K.paste(fr, btn, W / 2, 700, press, alpha=clamp((t - out - 0.45) / 0.1))
        # cursor flies in and clicks
        if t > out + 0.8:
            k3 = ease_io(clamp((t - out - 0.8) / 0.6))
            tx_ = W / 2 + btn.shape[1] / 2 - 70
            cx, cy = 1500 + (tx_ - 1500) * k3, 1000 + (715 - 1000) * k3
            K.paste(fr, _cursor(), cx + 18, cy + 26, press)
            if t > ck:
                r = (t - ck) * 500
                cv2.circle(fr, (int(tx_), 715), int(r), WHITE, 3, cv2.LINE_AA) if r < 260 else None
        k4 = (t - out - 1.0) / 0.4
        if k4 > 0:
            im = txt("Fast delivery  •  Eye-catching edits  •  Clear communication", 36, GREY, MED)
            K.paste(fr, im, W / 2, 860, 1.0, alpha=clamp(k4))
    flash(fr, t, END, 0.2, 0.4)
    fade = clamp((t - (TOTAL - 0.5)) / 0.5)
    return fr * (1 - fade)


@lru_cache(maxsize=1)
def _cursor():
    s = 3
    pts = [(0, 0), (0, 40), (11, 30), (19, 48), (26, 45), (18, 28), (32, 28)]
    im = Image.new("RGBA", (40 * s, 56 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([((x + 3) * s, (y + 3) * s) for x, y in pts], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2 * s)
    return np.asarray(im.resize((40 * 1, 56 * 1), Image.LANCZOS).resize((60, 84), Image.LANCZOS))


# ------------------------------------------------------------------ timeline
def scene_at(t):
    if t < DROP:
        return s_hook(t)
    if t < SV[0]:
        return s_wall(t)
    for i in range(5):
        if t < SV[i + 1]:
            return s_service(t, i)
    if t < END:
        return s_proof(t)
    return s_end(t)


CUTS = [(SV[0], "whip"), (SV[1], "whip"), (SV[2], "whip"), (SV[3], "whip"), (SV[4], "whip"), (PROOF, "zoom"), (END, "whip")]
TL = 0.2


def frame(nf):
    t = nf / FPS
    for c, kind in CUTS:   # transitions straddle the cut: outgoing frame frozen-ish, incoming from the cut
        if c - TL / 2 <= t < c + TL / 2:
            k = (t - (c - TL / 2)) / TL
            a = scene_at(min(t, c - 1e-3)).astype(np.float32)
            b = scene_at(max(t, c)).astype(np.float32)
            fr = K.transition(kind, a, b, k, nf).astype(np.float32)
            return finish(fr, nf)
    return finish(scene_at(t).astype(np.float32), nf)


# ------------------------------------------------------------------ audio
def build_audio():
    n = int(TOTAL * SR)
    m = read_audio(MUSIC, start=OFF, dur=TOTAL + 0.2)[:n]
    if len(m) < n:
        m = np.concatenate([m, np.zeros((n - len(m), 2), np.float32)])
    # filter build before the drop: low-passed track opening up, a breath of near-silence, then full on the drop
    d = int(DROP * SR)
    lp = m[:d].copy()
    out = np.zeros_like(lp)
    st = 0
    blk = 1024
    for s0 in range(0, d, blk):
        tt = s0 / SR / DROP
        fc = 280 * (6000 / 280) ** (tt ** 1.6)
        a = math.exp(-2 * math.pi * fc / SR)
        seg = lp[s0:s0 + blk]
        y = np.empty_like(seg)
        prev = out[s0 - 1] if s0 else np.zeros(2, np.float32)
        for c in range(2):   # one-pole x2 low-pass
            p1 = prev[c]
            x = seg[:, c]
            y1 = np.empty_like(x)
            for j in range(len(x)):
                p1 = (1 - a) * x[j] + a * p1
                y1[j] = p1
            y[:, c] = y1
        out[s0:s0 + blk] = y
    g = np.ones(d, np.float32) * 0.9
    gap = int(0.27 * SR)
    g[d - gap:] = np.linspace(0.9, 0.08, gap)
    m[:d] = out * g[:, None]
    fo = int(1.6 * SR)
    m[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    # voice phrases (light compression + presence), music ducked under each one
    vo = np.zeros((n, 2), np.float32)
    duck = np.ones(n, np.float32)
    for at, a, _w in VO.values():
        s0 = int(at * SR)
        e = min(s0 + len(a), n)
        vo[s0:e] += a[:e - s0]
        duck[max(s0 - int(0.06 * SR), 0):min(e + int(0.15 * SR), n)] = 0.32
    k = int(0.12 * SR)
    duck = np.convolve(duck, np.ones(k) / k, "same").astype(np.float32)
    write_wav(WORK / "vo_raw.wav", vo)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "vo_raw.wav"), "-af",
                    "highpass=f=70,equalizer=f=120:t=q:w=1:g=2,equalizer=f=3500:t=q:w=1.2:g=2.5,"
                    "acompressor=threshold=-22dB:ratio=3:attack=5:release=90:makeup=3", str(WORK / "vo_fx.wav")], check=True)
    vo = read_audio(WORK / "vo_fx.wav")[:n]
    vo = np.concatenate([vo, np.zeros((n - len(vo), 2), np.float32)]) if len(vo) < n else vo
    vo *= 0.55 / max(np.abs(vo).max(), 1e-6)
    mix = m * 0.8 * duck[:, None] + vo * 1.25
    sfx = [("swoosh-fast", beat(0), 0.5), ("swoosh-fast", beat(1), 0.55), ("swoosh-fast", beat(2), 0.6),
           ("bass", beat(3), 1.0), ("glitch-hit", beat(3), 0.45), 
           ("riser", DROP, 1.2), ("impact", DROP, 1.0), ("boom", DROP, 0.5), ("whoosh", DROP + 0.05, 0.5),
           ("pop", VO["mano"][2][2][1], 0.5), ("swoosh", beat(DROP_I + 3), 0.5)]
    for i in range(5):
        sfx += [("swoosh-fast", SV[i], 0.8), ("pop", SV[i] + 0.12, 0.45)]
    hb = (beat(1) - beat(0)) / 2
    for ci in range(4):
        sfx += [("ui-pop", SV[0] + 0.45 + ci * hb, 0.55), ("ui-pop", SV[4] + 0.4 + ci * hb, 0.55)]
    sfx += [("tick", SV[2] + 0.7, 0.8), ("pop", SV[3] + 0.75, 0.5)]
    bb = beat(37) - beat(36)
    sfx += [("tunnel", PROOF, 0.6)] + [("confirm", PROOF + 0.05 + j * PSTEP, 0.6) for j in range(3)]
    out_t = END_OUT
    sfx += [("swoosh-fast", END, 0.7), ("whoosh", out_t, 0.6), ("bass", out_t, 0.7), ("pop", out_t + 0.45, 0.6),
            ("tap", out_t + 1.45, 1.0), ("ding", out_t + 1.5, 0.8)]
    for name, at, gg in sfx:
        f, peak, pre, post, bg_ = K.SFX[name]
        pre = min(pre, peak, max(at, 0))
        c = read_audio(f, start=peak - pre, dur=pre + post)
        fade = min(len(c), int(0.1 * SR))
        c[-fade:] *= np.linspace(1, 0, fade)[:, None]
        s = int((at - pre) * SR)
        e = min(s + len(c), n)
        if e > s >= 0:
            mix[s:e] += c[:e - s] * bg_ * gg
    pk = np.abs(mix).max()
    if pk > 0.98:
        mix *= 0.98 / pk
    write_wav(WORK / "music.wav", m * duck[:, None])
    write_wav(WORK / "mix.wav", mix, af="loudnorm=I=-14:TP=-1.5:LRA=11")


WORK.mkdir(exist_ok=True)
VO = _vo() if (HERE / VO_TAKE).exists() else None
END_OUT = VO["brand"][0] + len(VO["brand"][1]) / SR + 0.05 if VO else END + 1.9
if VO:
    _m = END_OUT + 0.35
    VO["msg"][0] = _m
    VO["msg"][2] = [(w, s - VO["msg"][2][0][1] + _m, e - VO["msg"][2][0][1] + _m) for w, s, e in VO["msg"][2]]
    TOTAL = max(TOTAL, _m + len(VO["msg"][1]) / SR + 1.0)

if __name__ == "__main__":
    for k_, v_ in VO.items():
        print(f"  VO {k_:7s} {v_[0]:6.2f} - {v_[0] + len(v_[1]) / SR:6.2f}  {' '.join(w[0] for w in v_[2])}")
    print(f"drop {DROP:.2f} services {[round(x, 2) for x in SV]} proof {PROOF:.2f} end {END:.2f} total {TOTAL:.2f}")
    if "--extract" in sys.argv:
        extract()
        sys.exit()
    if "--frame" in sys.argv:
        for tt in sys.argv[sys.argv.index("--frame") + 1].split(","):
            Image.fromarray(frame(int(float(tt) * FPS))).save(WORK / f"frame_{tt}.jpg", quality=90)
        sys.exit()
    if "--stills" in sys.argv:
        ts = [1.0, 2.0, 3.6, DROP + 1.2, DROP + 3.0] + [SV[i] + 1.4 for i in range(5)] + [PROOF + 3.0, END + 1.2, TOTAL - 1.5]
        ims = [Image.fromarray(frame(int(x * FPS))).resize((480, 270)) for x in ts]
        S = Image.new("RGB", (480 * 4, 270 * math.ceil(len(ims) / 4)))
        for i, im in enumerate(ims):
            S.paste(im, (480 * (i % 4), 270 * (i // 4)))
        S.save(WORK / "stills.jpg", quality=85)
        print(WORK / "stills.jpg")
        sys.exit()
    build_audio()
    (HERE / "output").mkdir(exist_ok=True)
    out = HERE / "output" / "mano-fiverr-intro.mp4"
    pr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", str(WORK / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)],
                          stdin=subprocess.PIPE)
    for nf in range(int(TOTAL * FPS)):
        pr.stdin.write(frame(nf).tobytes())
    pr.stdin.close()
    pr.wait()
    print(out, f"{TOTAL:.2f}s")
