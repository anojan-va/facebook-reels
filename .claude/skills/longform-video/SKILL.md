---
name: longform-video
description: Make a 15–25 minute (or a short sample) 16:9 long-form psychology video for the same channel as the reels — highly edited, high-retention, mixing AI line-art images (glowing yellow man), stock videos/photos and motion graphics, with retention sound design. Use whenever the user asks for a long video, a YouTube/Facebook long-form video, a sample/pilot of one, or changes to one.
---

# Long-form psychology videos (16:9)

Same channel as the reels (`.claude/skills/facebook-reels/SKILL.md`): same voice, same yellow man, same music
library and the same feedback rules where they apply. Different editing: 1920x1080, a mix of
**AI line-art images + graded stock video + motion graphics**, and a cut or visual change every 1.5–3 s.

Everything lives in `longform/`: renderer `make_long.py` (schema in its docstring), stock search `stock.py`,
extra SFX in `longform/sfx/`, Anton font in `longform/fonts/`, one folder per video (`longform/<slug>/`),
renders in `longform/output/`. Sample to copy from: `longform/spotlight-effect/`.

## The user's feedback on long-form (never repeat)

| Video | What the user said | Rule |
|---|---|---|
| — | "not fully AI images" | Mix: roughly 35% AI images, 35% stock video, 30% motion graphics |
| — | "high user retention edit in audio and visuals" | Every cut has a transition SFX; every reveal has a graphic + hit |
| 1 | "duration not exceeding 20 minutes, 10–20 is good" | Aim for ~12–14 min (≈1,900–2,200 words at this voice's ~2.8 w/s); check the total before rendering |

## Pipeline

1. **Script** (~2.4 words/s → 20 min ≈ 2,900 words). Structure: cold-open hook (0–30 s, open loop: "and the one
   most people get wrong…") → promise ("7 tricks") → chapters (each opens with a chapter card, mini-hook, story or
   study, payoff) → re-hooks every ~60–90 s ("but that's not even the strangest part") → ending that loops back
   to the hook. Fact-check every study (author, year, numbers). Never invent statistics.
2. **Voice**: one take per chapter: `python3 ../../reels/tts.py chapters/chN.txt chapters/chN.wav`, all takes listed
   in order in `"audio"` (joined with `take_gap` 0.5 s). Score with `reels/audio/voice_profile.py` (convert
   `voice-ref.m4a` to wav first in the cloud); chapters land at 3–8, keep the closest of any retakes.
   The free Gemini quota is 10 requests/day and **failed 502 calls count too** (~250-word calls often 502).
   When it runs out, `tts.py` falls back to the same Charon voice through Pollinations
   (`google/gemini-3.8-flash-tts`, ≈ $0.02/min; force it with `tts.py --polli ...`). If a take scores > 8, retake it
   with the "deep low relaxed voice" style. The voice runs ~2.6–2.9 words/s.
3. **Word timings**: the renderer runs Whisper itself (cached in `<out>_work/whisper.json`).
   To plan shots first, transcribe with faster-whisper on a decoded array (see `make_long.py`; this VM's PyAV
   can't open files through faster-whisper).
4. **AI images** (`../../reels/polli.py gen.json`, Klein 4B, `"size": "2048x1152"`): house style from the reels
   skill, but "Horizontal 16:9 widescreen composition, cinematic framing", man description in every prompt,
   `refs: ["../../reels/refs/man.jpg"]` + "Use the reference image ONLY for how the yellow man looks… Completely
   replace the background." Review on a gridded sheet; reject colour leaks/real-looking faces of real people.
   Budget ≈ 1 image per 8–10 s of video (≈ 120–150 for 20 min, ~$0.6–0.8).
5. **Stock**: `python3 ../stock.py search "<query>" stock` → contact sheet `stock/cand/<query>.jpg`; pick by eye,
   `python3 ../stock.py get <hd-url> stock/<name>.mp4`. Write picks to `stock/credits.json`.
   Providers: Pexels (`PEXELS_API_KEY` env or network secret for `api.pexels.com`), Pixabay (`PIXABAY_API_KEY`),
   Mixkit (no key, 720p). Read a per-second strip of each clip to choose `start`. Stock is graded automatically
   (desaturated, contrasty, cool shadows) so it sits next to the black line-art.
6. **Shot list**: write `build.py` (copy `spotlight-effect/build.py`): per chapter a list of
   `(text, visual, extras)` with helpers `I()` image, `V()` stock, `K()` kinetic text, `CH()` chapter card, `LT()`
   study credit, `TITLE()`, `TAG()`, `SCAN()`, `R()` recap. It checks every shot text word-for-word against the
   chapter scripts and adds transitions, transition SFX, graphic SFX, chapter openers and music cues by rule, then
   writes `full.json` (schema: docstring of `make_long.py`). ~6–8 words per shot. Editing grammar:
   - **Hook**: stock close-up or the man, `sfx: ["hook"]`, `punch: true`, first 3 s never static.
   - **Abstract feeling** (anxiety, judging, thinking) → AI image with a camera move (`to`/`to_zoom`) or punch on
     the key word. **Real-world statement** → stock video. **Number, study, list, comparison** → motion graphic.
   - Never the same source type 3× in a row. Cuts 1.5–3 s; a motion graphic may hold 3–4 s if it animates.
   - Transitions (`in`): `whip` (default between shots), `zoom` (into a reveal), `flash` (onto a fact/number),
     `glitch` (twist / "but…"), `dip` (new section, with `pause_before: 0.25`). Each gets an SFX.
   - Motion graphics: `kinetic` (punch lines), `title` overlay (concept names), `year`, `lower_third` (study
     credit: authors + year), `grid` (people icons + % counter), `bars` (guess vs reality), `list` (locked teaser
     cards), `chapter` (TRICK #n + red stamp), `scan` (HUD box on a person), `tag` (◀◀ REPLAY timestamp).
     Keep graphics above y ≈ 0.75; captions sit at y 0.86. Set `captions: false` when the screen already
     shows the same words.
   - Captions: 1–3 word phrases, active word yellow, pop on each phrase (automatic).
   - Progress bar on (`"progress": true`).
7. **Sound design** (retention):
   - Music per section with `music_cues` (same library and mood rules as reels: echoes = intrigue, unforgiven =
     confident, out-of-this-world = tense, fifth-of-february = warm). Change track at chapter boundaries.
   - `music_fx: "muffle"` on a suspense line ("The real number?") — the bed goes underwater, then the reveal
     slams back with `bass`. Never real silence (reels rule: pauses ≤ 0.6 s).
   - `voice_fx: {"fx": "echo"}` on one punch word per section at most.
   - `amb` crowd murmur under crowd/room stock at 0.08–0.14.
   - SFX names: everything in the reels table plus `switch`, `click`, `tick`, `typing`, `shutter`, `sweep`,
     `swoosh`, `swoosh-fast`, `trailer`, `reveal`, `boom`, `tunnel`, `glitch-hit`, `glass`, `zap`.
   - Music: tracks loop around their end automatically (long videos resume tracks many times).
8. **Render**: `python3 ../make_long.py full.json --stills` first (≈ 10 min incl. Whisper: one frame per shot
   into `<out>_work/stills_NN.jpg`, 30 per sheet) → fix framing/dark clips/long static shots → full render
   (`--jobs 4` by default, ≈ 4–5 min per minute of video on this 4-core VM; a 20-min video ≈ 1.5 h — run it in the
   background). `--from/--to` renders one section.
9. **QA** (before replying): the stills sheets; total length in `timeline.json`; static shots > 4.5 s split;
   loudness ≈ −14 to −15 LUFS; quietest 0.1 s window > −40 dB; check muffle on `music.wav`.
10. **Deliver**: the 1080p master (≈ 1.1 MB/s) goes to the user with SendUserFile. GitHub only takes files < 100 MB,
    so commit a 720p copy re-encoded to fit (`deliveries/<slug>-720p.mp4`, two-pass at ~1.1 Mbps video) and the
    video folder without `img/`, stock clips or wavs.
