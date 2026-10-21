"""Render a Facebook reel from images + narration, shot by shot.

Usage: python make_reel.py path/to/reel.json

reel.json:
{
  "out": "../output/my-reel.mp4",
  "audio": ["take-1.m4a", "take-2.m4a"],      # narration takes, joined in order
  "speed": 1.15,                              # optional, speed up the voice (pitch kept)
  "music": "../audio/music/just-chill.mp3",   # optional bed, ducked under the voice
  "music_volume": 0.4, "music_start": 0,      # optional
  "music_cues": [{"shot": 0, "music": "tense.mp3", "start": 3.1},   # optional instead of "music": switch tracks
                 {"shot": 7, "music": "warm.mp3"}],                 # at these shots' cuts to follow the mood
  "fade_out": 1.0,                            # optional, fade to black at the end (seconds)
  "beat_sync": true,                          # optional, stretch section pauses so those cuts land on music beats
                                              # (needs <music>.beats.json next to the track)
  "shots": [
    {"image": "a.jpeg", "text": "Exact words spoken during this shot.",
     "focus": "man-face" | "man" | "wide" | [x, y],   # what the camera looks at (x, y = 0..1 of the image)
     "zoom": 1.6,                             # framing: 1 = whole image, 2 = twice as close
     "drift": 0.05,                           # optional slow push during the shot (negative pulls out)
     "punch": true,                           # optional fast zoom-in at the cut
     "flash": true,                           # optional quick dim-in at the cut
     "pause_before": 0.25,                    # optional breath in the voice before this shot; music plays on, impact lands on the cut
     "music_drop": false,                     # optional, also silence the music during that pause
     "sfx": ["whoosh", {"name": "pop", "at": 0.4}]}   # at = seconds after the cut (default 0)
  ]
}
Shots cut where their first word is spoken (found with Whisper), so `text` must be the script verbatim, in order.
Relative paths resolve against the folder holding reel.json.
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel
from PIL import Image

from fonts import ffmpeg_path, font

W, H, FPS = 1080, 1920, 30
SR = 44100
TAKE_GAP = 0.3   # silence between takes, seconds
LEAD = 0.12      # cut to a shot this long before its first word
TAIL = 0.8       # hold after the last word

AUDIO = Path(__file__).parent / "audio" / "sfx"
# name: file, peak (s into the file), pre/post (s kept around the peak), gain
SFX = {
    "whoosh":  ("whoosh-cinematic.mp3", 0.28, 0.28, 0.8, 0.7),
    "whoosh2": ("whoosh-air.mp3", 1.09, 0.6, 0.25, 0.9),
    "pop":     ("pop.mp3", 0.06, 0.06, 0.5, 1.6),
    "impact":  ("impact-deep.mp3", 2.18, 0.03, 2.5, 0.8),
    "hook":    ("impact-intro.mp3", 0.15, 0.15, 2.5, 0.6),
    "correct": ("correct.mp3", 0.36, 0.36, 1.2, 0.45),
    "wrong":   ("wrong.mp3", 0.04, 0.04, 1.0, 0.3),
    "sparkle": ("sparkle.mp3", 0.11, 0.11, 0.35, 0.6),
    "heartbeat": ("heartbeat.mp3", 0.08, 0.08, 0.34, 1.0),
    "riser":   ("riser-short.mp3", 6.96, 2.0, 0.3, 0.5),
    "rewind":  ("rewind-tape.mp3", 0.18, 0.0, 1.6, 0.9),
    "glitch":  ("glitch-static.mp3", 0.05, 0.05, 0.5, 0.6),
    "bass":    ("bass-hit.mp3", 0.17, 0.12, 1.2, 1.0),
    "scratch": ("record-scratch.mp3", 0.3, 0.2, 0.55, 0.8),
}
VHS = ("noise=alls=28:allf=t,rgbashift=rh=10:bh=-10:gv=4,eq=saturation=0.55:contrast=1.15:brightness=0.03,"
       "drawgrid=w=iw:h=8:t=3:c=black@0.45,"
       f"drawtext=fontfile='{ffmpeg_path(font('symbol'))}':text='◀◀ REWIND':x=60:y=140:fontsize=64:fontcolor=white@0.9")

ASS_HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,Arial,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,1,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(t: float) -> str:
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def run(args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed:\n{r.stderr[-3000:]}")


def read_audio(path, start=None, dur=None) -> np.ndarray:
    seek = (["-ss", f"{start:.3f}"] if start else []) + (["-t", f"{dur:.3f}"] if dur else [])
    raw = subprocess.run(["ffmpeg", "-v", "error", *seek, "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def write_wav(path, a: np.ndarray, af=None):
    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        *(["-af", af] if af else []), "-ar", str(SR), "-c:a", "pcm_s16le", str(path)], input=np.clip(a, -1, 1).astype(np.float32).tobytes(),
                       capture_output=True)
    if p.returncode:
        sys.exit(p.stderr.decode()[-2000:])


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def align(script, heard):
    """Timing for every script word. Matched words take Whisper's times; the rest are spread between neighbours."""
    a, b = [norm(w) for w in script], [norm(w.word) for w in heard]
    found: dict[int, tuple[float, float]] = {}
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            h = heard[blk.b + k]
            found[blk.a + k] = (h.start, h.end)
    if not found:
        sys.exit("Whisper heard none of the script; check the narration files.")
    times: list[tuple[float, float]] = []
    for i in range(len(script)):
        if i in found:
            times.append(found[i])
            continue
        prev = max((k for k in found if k < i), default=-1)
        nxt = min((k for k in found if k > i), default=len(script))
        s = found[prev][1] if prev >= 0 else 0.0
        e = found[nxt][0] if nxt < len(script) else s + 0.4 * (nxt - prev)
        step = (e - s) / (nxt - prev)
        st = s + step * (i - prev - 1)
        times.append((st, st + max(step, 0.15)))
    return times


def music_bed(spec, base, starts, n):
    """The music under the whole reel, as one array of n samples.
    "music_cues": [{"shot": 0, "music": "tense.mp3", "start": 3.1, "volume": 1.0}, {"shot": 7, "music": "warm.mp3"}, ...]
    switches tracks at those shots' cuts with a short crossfade, so the music follows the narration's mood.
    A track that comes back resumes where it left off unless the cue gives "start". Without cues, "music" loops."""
    def load(path, start, dur):
        a = read_audio(path, start=start)
        reps = int(np.ceil(dur * SR / max(len(a), 1))) + 1
        return np.tile(a, (reps, 1))[: int(dur * SR)]
    cues = spec.get("music_cues") or [{"shot": 0, "music": spec["music"], "start": spec.get("music_start", 0)}]
    xf = int(0.25 * SR)
    bed = np.zeros((n + xf, 2), np.float32)
    resume = {}
    for k, cue in enumerate(cues):
        path = (base / cue["music"]).resolve()
        t0 = 0.0 if k == 0 else starts[cue["shot"]]
        t1 = starts[cues[k + 1]["shot"]] if k + 1 < len(cues) else n / SR
        src = cue.get("start", resume.get(path, 0.0))
        seg = load(path, src, t1 - t0 + xf / SR) * float(cue.get("volume", 1.0))
        if k:                     # fade in over the cut
            seg[:xf] *= np.linspace(0, 1, xf)[:, None]
        if k + 1 < len(cues):     # fade out under the next track
            seg[-xf:] *= np.linspace(1, 0, xf)[:, None]
        a = int(t0 * SR) - (xf // 2 if k else 0)
        a = max(a, 0)
        bed[a:a + len(seg)] += seg[: len(bed) - a]
        resume[path] = src + (t1 - t0)
    return bed[:n]


def focus_point(img: Path, focus) -> tuple[float, float, float]:
    """(x, y) on the image to look at, and how far down the frame to place it (0.5 = centre).
    Faces go in the upper third so the centred caption never covers them.
    'man'/'man-face' find the glowing yellow figure by colour; [x, y] or [x, y, frame_y] are explicit."""
    if isinstance(focus, list):
        return float(focus[0]), float(focus[1]), float(focus[2]) if len(focus) > 2 else 0.5
    if focus in (None, "wide"):
        return 0.5, 0.5, 0.5
    im = np.asarray(Image.open(img).convert("RGB").resize((192, 344)), dtype=np.int16)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    mask = (r > 170) & (g > 150) & (b < 110) & (r - b > 90)
    ys, xs = np.nonzero(mask)
    if len(xs) < 40:
        print(f"  ! no yellow figure found in {img.name}; centring")
        return 0.5, 0.5, 0.5
    x0, x1 = np.percentile(xs, [3, 97])
    y0, y1 = np.percentile(ys, [2, 98])
    cx = (x0 + x1) / 2 / 192
    if focus == "man-face":
        head = ys < y0 + (y1 - y0) * 0.2
        cx = xs[head].mean() / 192 if head.any() else cx
        return cx, (y0 + (y1 - y0) * 0.12) / 344, 0.32
    return cx, (y0 + y1) / 2 / 344, 0.5


def main():
    spec_path = Path(sys.argv[1]).resolve()
    base = spec_path.parent
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    shots = spec["shots"]
    out = (base / spec["out"]).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    work = out.parent / (out.stem + "_work")
    work.mkdir(exist_ok=True)

    # 1. Voice: join the takes, speed up, transcribe.
    takes = [str((base / a).resolve()) for a in spec["audio"]]
    inputs, parts = [], []
    for i, t in enumerate(takes):
        inputs += ["-i", t]
        parts.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=stereo,apad=pad_dur={TAKE_GAP}[a{i}]")
    n = len(takes)
    graph = (";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(n))
             + f"concat=n={n}:v=0:a=1,atempo={spec.get('speed', 1.0)}[voice]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[voice]",
         "-c:a", "pcm_s16le", str(work / "voice_raw.wav")])
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(work / "voice_raw.wav"), word_timestamps=True, language="en")
    heard = [w for s in segs for w in (s.words or [])]
    script, owner = [], []
    for si, sh in enumerate(shots):
        for w in sh["text"].split():
            script.append(w)
            owner.append(si)
    times = align(script, heard)
    matched = sum(1 for w in heard if norm(w.word) in {norm(s) for s in script})
    print(f"script {len(script)} words, heard {len(heard)} ({matched} matching)")

    # 2. Shot starts on the raw voice, then insert the pauses and shift everything after them.
    raw_starts = [0.0 if si == 0 else max(times[owner.index(si)][0] - LEAD, 0.0) for si in range(len(shots))]
    voice = read_audio(work / "voice_raw.wav")
    # beat_sync: stretch each section pause (0.12-0.6 s) so the cut lands on a music beat.
    beats = []
    if spec.get("beat_sync") and spec.get("music"):
        bf = (base / spec["music"]).resolve().with_suffix(".beats.json")
        if bf.exists():
            ms = spec.get("music_start", 0)
            beats = [b - ms for b in json.loads(bf.read_text())["beats"] if b >= ms]
        else:
            print(f"  ! beat_sync: no {bf.name}; make it with the venv (see CLAUDE.md)")
    pieces, pauses, cursor, shift = [], [], 0, 0.0   # pauses: (start, end) on the final timeline
    raw_points, gaps = [], []
    for si, sh in enumerate(shots):
        d = sh.get("pause_before", 0)
        if not d or si == 0:
            continue
        if beats:
            at = raw_starts[si] + shift
            nxt = next((b for b in beats if b >= at + 0.12), None)
            if nxt is not None and nxt - at <= 0.6:
                d = nxt - at
        cut = int(raw_starts[si] * SR)
        pieces += [voice[cursor:cut], np.zeros((int(d * SR), 2), np.float32)]
        pauses.append((raw_starts[si] + shift, raw_starts[si] + shift + d))
        raw_points.append(raw_starts[si]); gaps.append(d)
        cursor, shift = cut, shift + d
    pieces += [voice[cursor:], np.zeros((int(TAIL * SR), 2), np.float32)]
    voice = np.concatenate(pieces)
    total = len(voice) / SR

    # Raw voice time -> final time: add every pause inserted at or before t.
    def remap(t):
        return t + sum(g for p, g in zip(raw_points, gaps) if p <= t + 1e-6)

    starts = [remap(t) for t in raw_starts]
    times = [(remap(s), remap(e)) for s, e in times]
    ends = starts[1:] + [total]
    durations = [e - s for s, e in zip(starts, ends)]

    # 3. Soundtrack: voice + ducked music (dropped during pauses) + sound effects.
    mix = voice.copy()
    if spec.get("music") or spec.get("music_cues"):
        music = music_bed(spec, base, starts, len(voice))
        write_wav(work / "music.wav", music)   # bed alone, for checking the mood per section
        # Duck under speech: follow the voice envelope (fast attack, slow release).
        env = np.abs(voice).mean(axis=1)
        hop = 441
        frames = env[: len(env) // hop * hop].reshape(-1, hop).max(axis=1)
        gain_f = np.empty_like(frames)
        level = 0.0
        for i, v in enumerate(frames):
            level = max(v, level * 0.93)   # ~140 ms release per hop of 10 ms
            gain_f[i] = 0.45 if level > 0.02 else 1.0
        gain_f = np.convolve(gain_f, np.ones(8) / 8, "same")
        gain = np.repeat(gain_f, hop)
        gain = np.concatenate([gain, np.full(len(music) - len(gain), gain[-1] if len(gain) else 1.0)])
        # Music keeps playing through section pauses (a full drop sounded like a dead gap); only a
        # shot with "music_drop": true cuts it for a deliberate silence-then-hit.
        for si, (p0, p1) in zip([i for i, sh in enumerate(shots) if sh.get("pause_before") and i], pauses):
            if shots[si].get("music_drop"):
                a, b = int(p0 * SR), int(p1 * SR)
                gain[a:b] = 0.0
                gain[b: b + int(0.08 * SR)] *= np.linspace(0, 1, len(gain[b: b + int(0.08 * SR)]))
        fo = int(1.5 * SR)
        gain[-fo:] *= np.linspace(1, 0, fo)
        mix += music * gain[:, None] * spec.get("music_volume", 0.4)
    cues = []
    for si, sh in enumerate(shots):
        for cue in sh.get("sfx", []):
            cue = {"name": cue} if isinstance(cue, str) else cue
            cues.append((cue["name"], starts[si] + float(cue.get("at", 0.0)), float(cue.get("gain", 1.0))))
        if sh.get("pause_before") and si and not any(
                (c if isinstance(c, str) else c["name"]) == "impact" for c in sh.get("sfx", [])):
            cues.append(("impact", starts[si], 1.0))
    for name, at, g in cues:
        f, peak, pre, post, base_gain = SFX[name]
        pre = min(pre, peak, at)
        clip = read_audio(AUDIO / f, start=peak - pre, dur=pre + post)
        fade = min(len(clip), int(0.15 * SR))
        clip[-fade:] *= np.linspace(1, 0, fade)[:, None]
        s = int((at - pre) * SR)
        e = min(s + len(clip), len(mix))
        mix[s:e] += clip[: e - s] * base_gain * g
    peak_level = np.abs(mix).max()
    if peak_level > 0.98:
        mix *= 0.98 / peak_level
    write_wav(work / "mix.wav", mix, af="loudnorm=I=-14:TP=-1.5:LRA=11")   # social-video loudness

    # 4. Captions: one word at a time, held until the next word.
    with open(work / "captions.ass", "w", encoding="utf-8") as f:
        f.write(ASS_HEADER)
        for k, (word, (s, e)) in enumerate(zip(script, times)):
            nxt = times[k + 1][0] if k + 1 < len(times) else total
            e = min(nxt, e + 0.8)
            f.write(f"Dialogue: 0,{ts(s)},{ts(e)},Word,,0,0,0,,{word.replace('{', '').replace('}', '')}\n")

    # 5. Video: per shot framing on its focus point, slow drift, optional punch-in / dim flash.
    vin, vparts = [], []
    nin = 0   # input counter (a flip shot uses several inputs)
    for i, (sh, dur) in enumerate(zip(shots, durations)):
        frames = max(1, round(dur * FPS))
        if sh.get("flip"):
            # Rewind montage: flick through the listed images, a few frames each, fast pull-out, VHS look.
            per = int(sh.get("flip_frames", 3))
            subs = []
            for j, k in enumerate(range(0, frames, per)):
                n = min(per, frames - k)
                img = (base / sh["flip"][j % len(sh["flip"])]).resolve()
                vin += ["-loop", "1", "-framerate", str(FPS), "-t", f"{n / FPS:.3f}", "-i", str(img)]
                vparts.append(f"[{nin}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                              f"zoompan=z='1.25-0.2*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={FPS},"
                              f"trim=end_frame={n},setsar=1,scale=out_range=tv:out_color_matrix=bt709,format=yuv420p[f{i}_{j}]")
                subs.append(f"[f{i}_{j}]")
                nin += 1
            vparts.append("".join(subs) + f"concat=n={len(subs)}:v=1:a=0,{VHS}[v{i}]")
            continue
        img = (base / sh["image"]).resolve()
        vin += ["-loop", "1", "-framerate", str(FPS), "-t", f"{frames / FPS:.3f}", "-i", str(img)]
        nin += 1
        cx, cy, ay = focus_point(img, sh.get("focus", "wide"))
        z0 = max(1.0, float(sh.get("zoom", 1.0)))
        drift = float(sh.get("drift", 0.05))
        z = f"{z0}*(1+{drift}*on/{frames})"
        if drift < 0:   # pull out: start tighter, end on the framing
            z = f"{z0}*(1+{-drift}*(1-on/{frames}))"
        if sh.get("punch"):
            z = f"({z})*(1-0.15*max(0,1-on/5))"
        z = f"max(1,{z})"
        x = f"min(max({cx}*iw-iw/zoom/2,0),iw-iw/zoom)"
        y = f"min(max({cy}*ih-ih/zoom*{ay},0),ih-ih/zoom)"
        fx = ""
        if sh.get("flash"):
            fx += ",fade=t=in:st=0:d=0.3"
        if i == len(shots) - 1 and spec.get("fade_out"):
            d = spec["fade_out"]
            fx += f",fade=t=out:st={max(frames / FPS - d, 0):.3f}:d={d}"
        vparts.append(
            f"[{nin - 1}:v]scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
            f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS},"
            f"trim=end_frame={frames},setsar=1,scale=out_range=tv:out_color_matrix=bt709,format=yuv420p{fx}[v{i}]")
    ns = len(shots)
    vgraph = ";".join(vparts) + ";" + "".join(f"[v{i}]" for i in range(ns)) + f"concat=n={ns}:v=1:a=0,ass=captions.ass[vid]"
    run(["ffmpeg", "-y", "-v", "error", *vin, "-i", "mix.wav", "-filter_complex", vgraph,
         "-map", "[vid]", "-map", f"{nin}:a", "-c:v", "libx264", "-preset", "slow", "-crf", "25",
         "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709",
         "-color_trc", "bt709", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
         "-t", f"{total:.3f}", str(out)], cwd=work)
    for i, (s, d) in enumerate(zip(starts, durations)):
        print(f"  shot {i + 1:2d}  {s:5.2f}s  +{d:4.2f}s  {shots[i]['text'][:45]}")
    (work / "timeline.json").write_text(json.dumps([{"start": round(s, 3), "dur": round(d, 3), "text": sh["text"]}
                                                    for s, d, sh in zip(starts, durations, shots)], indent=1))
    print(f"{out}  ({total:.1f}s, {out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
