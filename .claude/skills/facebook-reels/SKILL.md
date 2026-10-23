---
name: facebook-reels
description: Make a finished 9:16 psychology/dating Facebook reel from a script for the user's page — voice-over, line-art images with the glowing yellow man, shot-by-shot editing, mood-matched music, sound effects, one-word captions. Use whenever the user sends a reel script, asks to remake or fix a reel, change its music/voice/editing, or asks how reels are made here.
---

# Facebook psychology reels

The user sends a script; you deliver a finished MP4 in `D:\Claude\reels\output\`. Do the whole pipeline yourself —
never propose building an app. Reference look: `D:\Claude\sample.mp4` (9:16, ~45 s, black background, white line
art, the bearded man in the yellow hoodie (see below) + anime girl, one word at a time captions in the centre, dark trap bed).

**Main character (from reel 9 on — always him, never the old yellow mannequin):** `reels/refs/man-sheet.jpg`, the user's
character sheet "The Inner You": young man, short tousled brown hair, short neat brown beard, warm friendly eyes,
mustard-yellow hoodie, black cargo joggers, white sneakers, soft warm yellow glow around his outline. He is the only
colour in the frame; the world and the girl stay white line art on black. The sheet also has his expressions
(`man-expressions.jpg`) and optional outfits (blazer, olive jacket, grey tee with sling bag) for scenes that need them.

Everything lives in `D:\Claude\reels\`. Each reel gets its own folder `reels/<slug>/` (prompts.json, script.txt,
voice takes, img/, reel.json). Reuse the newest reel folder as a template — `reels/first-date/` is the most complete.

## The user's standing feedback (never repeat these mistakes)

| Reel | What the user rejected | Rule |
|---|---|---|
| 1 | Random zoom in/out | Camera follows the narration: frame whoever the line is about |
| 1 | One image held 5 s | New framing every 1.5–3 s |
| 1 | Same location the whole time | Explainer lines move to other places |
| 1 | No SFX / music | Always a music bed + SFX |
| 1 | Bright major "Just Chill" | Music must match the narration mood |
| 1 | Dead silence before First/Second/Third | Music never stops; pauses ≤ 0.6 s |
| 2 | Two voice takes = "two voices" | ONE TTS take per reel |
| — | Channel voice | Must sound like reel 1's opening voice |
| 4 | Voice slowed to 0.93× | Never slow below 1.0×; short script = short reel, say so |
| 4 | 5 phone screens, two in a row | ≤ 3 object/phone screens, never adjacent |
| 4 | Confident trap, then "Silent Descent", on a mistake/fix dating script | Music must follow the mood **per section** (`music_cues`) |
| 6 | "Body turned away, feet toward him" drawn the other way round (she faced him, feet away) | Check every body-language image says exactly what the line says (who faces whom, where the feet point). Klein always turns her face to the man — generate her alone in the pose, then paste the yellow man (cut out by his yellow pixels) on the side her feet point to |
| 6 | Feet close-ups with crossed / back-to-front feet | Feet shots: two natural feet side by side, both toes the same way, side profile; reject any odd anatomy |
| 7 | Man with three arms / extra hands on one side (s02 polite, s08 pointing) | **Anatomy check on every image**: count arms, hands, legs, feet per character at full size. Klein keeps the reference's hand-in-pocket and adds the new gesture as an extra arm — for any gesture, say what EACH arm does, add "exactly two arms and two hands, his hands NOT in his pockets", and make sure no arm crosses another face |
| 8 | New main character | From reel 9 on the main character is the bearded man in the yellow hoodie (`refs/man-sheet.jpg`), never the yellow mannequin. Always pass `refs/man.jpg` as reference 1 |
| 8 | Girl far shorter than the new man | Almost the same height: her head reaches his eyebrows, both at the same distance from the camera (Height rule) |
| 8 | Voice | Compared premium Pro voices (Charon/Orus/Algenib) with the channel voice: keep the channel voice (Flash, Charon, deep style). Premium only on request |
| 9 | Last 10 reels ended on black text cards | Never end on a text card: the closing lines play over closing images of the main character that conclude the story (e.g. "shh" + his busy shop; watering the sprout + standing on the glowing roots) |
| 9 | Second person / objects drawn black-filled | Only the hero is coloured (yellow). The second person, every other person, animal and object is drawn WHITE (white clothes, white fills) — never black-filled or a dark silhouette. Prompts: `reels/style_new.py` |
| 10 | Bad legs: third sneaker, ghost legs of background people tangled with his, crossed/twisted walking legs, one leg sticking out of a bed | **Leg check on every image, same as hands**: count legs and feet per person at full size (each leg → one foot, feet point like the knees, no legs from people behind merging in). Prefer standing still with both feet flat, kneeling on both knees, or framing from the waist up; for lying in bed use a top-down view with the blanket to the shoulders. When he must be alone say "completely ALONE, no figures" and leave out the other-people sentence |
| 10 | Arm-only close-ups of a glass looked like an unknown hand | Never show a disembodied hand/arm doing the story action: show the person (the teacher) whole. The hero is a seated student when the story says so |
| 10 | Young eagle among chickens not visible | When an animal must stand out from its group, make it solid WHITE-filled (eagle) and keep the group as thin outlines (chickens), and describe what makes it that animal (hooked beak, talons) |
| 11 | Glass of Water: worried shot read as an extra hand; sneakers on in bed; hero seated among schoolchildren | **STRICT anatomy gate, every image, every reel, no exceptions**: open each image at full size (≥ 600 px wide, never judge from a thumbnail sheet) and for EVERY person write down arms/hands/legs/feet = 2/2/2/2 and that each hand is attached to that person's own arm; any doubt = reject and regenerate (make 2–3 candidates and pick one that clearly passes). Repeat the count on the final frame sheet (start and end of each shot, so crops/zooms can't hide or create limbs). Prefer poses that show both hands clearly (hands on head, holding an object with both hands, arms at sides). Nobody wears shoes in bed. The hero is an adult: never seat him among children/students; classroom shots show only white students + the white teacher |
| 11 | "1 minute" teacher had THREE arms (one holding the glass + two hanging at his sides) — missed on review | **Holding-an-object check**: whenever a person holds something in one hand, trace that arm from shoulder to hand, then confirm the OTHER side has exactly one arm. Klein's most common mistake is adding both resting arms PLUS the gesturing arm. Prompt it explicitly: "exactly TWO arms: his RIGHT arm …; his LEFT arm …; nothing else hangs at his right side". Check every candidate at full size; 2 of 3 candidates had this error |
| 12 | Window & Mirror: a man with THREE hands shipped (hidden figure's hand next to the hero) | **Anatomy gate is mandatory, no exceptions**: for every image, every person, count hands one by one and trace each hand to its own shoulder; a hand or arm that belongs to nobody visible = reject. Prompt every two-person shot with "ONLY these two people, nobody else, no figure behind anyone" |
| 12 | Script says OLD man / grandfather / wise old man but the hero was drawn young | **Match the hero's age to the script**: use `refs/man-old.jpg` + `old_scene()` in `reels/style_new.py` (grey hair & beard, wrinkles, same yellow hoodie) whenever the narration says old/grandfather/elder |
| 12 | A child aged into an adult later in the same reel (Nails in the Fence) | **Character continuity**: a character keeps the same age, size and look in every shot of a reel — describe the child as a small child in every prompt where he appears, and compare all shots of a character side by side before rendering |
| 12 | Prop not in the hand that uses it (scissors floating idle) / tea pouring against gravity | **Props and physics check**: the tool must be held in the hand doing the action and touching what it acts on; liquids fall straight down, cups stand on surfaces, spills spread on the table/floor. For before/after pairs (pour → overflow) make the second shot as an EDIT of the first so the pose stays consistent |

## Where you are running

The same repo runs in two places. Check which one first (`uname` / the working directory):

| | Local Windows PC (`D:\Claude`) | Claude cloud session (Linux VM, repo clone) |
|---|---|---|
| Python for rendering | `python` | `python3` |
| Python for audio analysis (librosa) | `reels/.venv/Scripts/python` (global numpy breaks numba) | `python3` (setup script installs everything) |
| Keys | files `~/.pollinations-key`, `~/.flow-mcp/gemini-key` | none in the VM — network secrets; the proxy adds them. Never ask for keys |
| Fonts | Windows fonts | Liberation / DejaVu / Noto (via `cloud/setup.sh`); always go through `reels/fonts.py` |
| Flow fallback | available | NOT available (needs the local Chrome) — Pollinations only |
| Delivering the MP4 | `reels/output/<slug>.mp4` | copy to `deliveries/<slug>.mp4`, commit it **with the reel folder (no img/, no wav)**, push the branch, give the user the GitHub path |

Cloud environment setup (done once by the user): network access **Custom** with defaults plus `gen.pollinations.ai`,
`media.pollinations.ai`, `mixkit.co`, `assets.mixkit.co`, `huggingface.co`, `*.huggingface.co`, `*.hf.co`;
network secrets for `gen.pollinations.ai` (Authorization: Bearer), `aiplatform.googleapis.com` (`x-goog-api-key`, the
Vertex express key, premium voice) and `generativelanguage.googleapis.com` (`x-goog-api-key`, no prefix); setup script = `cloud/setup.sh`. If a request fails with 401/403 in the cloud, the
secret or allowlist is missing — tell the user which, don't work around it.
Cloud quirks: faster-whisper breaks with PyAV ≥ 16 (`metadata_errors` TypeError) — `cloud/setup.sh` pins `av<16`;
librosa can't read `voice-ref.m4a` there — convert it first (`ffmpeg -i ../audio/voice-ref.m4a <scratch>/voice-ref.wav`).

## Tools and keys (all already set up)

- **Voice (channel voice, default)**: `python reels/tts.py script.txt voice-cand-N.wav` → Gemini 2.5 Flash TTS on AI Studio,
  Charon, style "calm, confident, conversational, slightly slow, in a deep low relaxed voice, like a friendly psychology
  explainer" — one call = whole script. The user compared it with the premium voices and chose this one. Key:
  `$GEMINI_API_KEY` or `~/.flow-mcp/gemini-key` locally; the proxy in the cloud. Free tier: **3 requests/min, 10/day per
  Google project** (a second key from the same project shares the quota). Extra keys the user gives: pass them for the
  command only as `GEMINI_API_KEYS="k1,k2" python reels/tts.py …` — tts.py sends them as `?key=` (the cloud proxy
  overwrites an x-goog-api-key header with its stored, possibly exhausted, key) and moves to the next key on 429.
  Never write keys to a file.
  `--premium` = Gemini 2.5 Pro TTS on Vertex AI (paid, no cap; richer but ~125–135 Hz) — only if the user asks. Its key is a
  Vertex express key (`AQ.…`): `$GOOGLE_VERTEX_API_KEY` / `~/.vertex-key` locally, network secret for
  `aiplatform.googleapis.com` (`x-goog-api-key`) in the cloud. It does NOT work with Cloud Text-to-Speech / Chirp 3 HD.
  Never put a key in a command or a repo file.
- **Images (default)**: `python reels/polli.py jobs.json` → Pollinations FLUX.2 Klein 4B, parallel.
  Key: `$POLLINATIONS_KEY` or `~/.pollinations-key` locally; the proxy in the cloud. ~$0.005/image, 1152x2048. User approved the cost.
- **Character references** (committed, use these for the establishing image of a new reel):
  `reels/refs/man.jpg` (front/side/back of the main character — ALWAYS reference image 1 when he is in the shot),
  `reels/refs/man-hero.jpg`, `reels/refs/characters.jpg` (him + the girl on a platform, the approved look),
  `reels/refs/girl.jpg`. Old mannequin refs (`man-old-mannequin.jpg`, `characters-old.jpg`) are for old reels only.
  Previous reels' `img/` folders are not in git.
- **Images (fallback, local PC only)**: Google Flow via flow-mcp (`C:\Users\Anojan\flow-mcp`). `python reels/flow.py <method> '<json>'`.
  If the server is down: run `reels/start_flow.ps1` in the background, then
  `node reels/open_project.mjs https://flow.google.com/project/a1c4ad29-4d65-4914-a493-c127237e256a`.
  Only `generate` with `type:"image"`, `max_credits:0`. Never spend credits (no video, edit, continue).
- **Renderer**: `python reels/make_reel.py reels/<slug>/reel.json` (`python3` in the cloud; Whisper aligns captions).
- **Audio analysis** (librosa needs the venv — the global numpy breaks numba):
  `<audio python> reels/audio/<script>.py` (see the table above) — `analyze_music.py`, `rank_music.py`, `rank_mood.py`,
  `beats.py`, `voice_profile.py`.
- Local PC only: `ffprobe` is blocked on this PC (Application Control); `ffmpeg` works. Real ffprobe:
  `C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin\ffprobe.exe`.
- Never ask for a key in chat. Never publish anything.

## Pipeline

### 1. Read the script
- Count words. Pace is 2.3–2.5 words/s → 100 words ≈ 42 s. If the script is short of the target length, say so
  in the final message (don't pad or slow down).
- Identify the **mood arc** (confident? sad→hopeful? mistake/fix flips?) — it drives music and SFX.
- List the beats and every on-screen element the script asks for (numbers, ✗, speech bubbles, phone texts).

### 2. Voice — one take, channel voice
1. Write `script.txt` (the exact narration, plain quotes, `...` kept).
2. Make 2–3 takes: `python ../tts.py script.txt voice-cand-1.wav` (defaults: channel voice, Charon + the deep channel
   style above — it scored 3.9–4.8 against reel 1, the best matches so far).
3. Score vs the channel voice:
   `<audio python> ../audio/voice_profile.py ../audio/voice-ref.m4a voice-cand-*.wav` (the reference is reel 1's opening take)
   Keep the lowest distance (≈5 is fine; reference pitch ~89 Hz). If all takes are high-pitched (>105 Hz), spend
   one more with style `"... slightly slow, in a deep low relaxed voice, like a friendly psychology explainer"`.
4. Budget: 10 TTS calls/day on the channel voice. Tell the user how many are left if it gets low.

### 3. Images — Klein with references
- **House style** (start every prompt with it):
  "Minimalist illustration on a pure black background, clean thin white line art with no shading for the world and the
  woman. The only colour in the image is the man. No text, letters or captions in the image unless described. Vertical 9:16 composition."
  For shots with NO people use a version without any mention of the man ("…white lines only, no colour at all"), or
  Klein paints him in anyway.
- **Man** (in EVERY prompt where he appears, even background), with `refs/man.jpg` as reference image 1 and the prefix
  "Reference image 1 shows exactly how the man looks: copy his face, hair, beard, yellow hoodie, black cargo pants and white sneakers.":
  "The main character is a young man with short tousled brown hair, a short neat brown beard and warm friendly eyes, wearing a
  mustard-yellow hoodie, black cargo jogger pants and white sneakers, drawn in clean anime line art with flat colours and a soft
  warm yellow glow around his outline."
- **Girl**: "A young adult woman drawn in white anime-style line art only, NOT coloured: long light hair in a high ponytail,
  fitted t-shirt, plaid skirt, knee socks and white sneakers."
- **Height** (every prompt with both of them): "They stand at the SAME distance from the camera, their feet on the same
  line, both the same scale. She is almost as tall as he is: the top of her head reaches his eyebrows." When a girl image is
  a reference, say "…how the woman looks and the drawing style, NOT her size" — otherwise Klein copies her small scale
  and puts him in the foreground, and she looks child-sized.
- **Anatomy** (every prompt with people): "Normal human anatomy: each person has exactly two arms, two hands, two legs and two feet."
- One `Setting:` sentence per location, repeated verbatim in every prompt for that location. Then `Scene:` + action/emotion.
- **Order**: generate the establishing image (both characters, main location) first with a previous reel's image
  as ref and the prefix "Use the reference image ONLY for how the two characters look … Completely replace the
  background: no <old location items>." Check it. Then all other scenes in one parallel batch (`workers` = count).
- **Klein copies the reference's background and every character in it.** Pick refs accordingly:
  same location → establishing image + "Keep the characters, the <place> and the drawing style exactly as in the reference";
  new location → "Use the reference image ONLY for how the characters look… Completely replace the background…";
  girl-only scenes → a girl-only image as ref, or no ref + "Only the woman… white line art only, NOT yellow";
  objects/phones/brains → no ref + "no people".
  Klein ALSO copies the reference's pose and camera angle — same-location scenes come out as near-identical standing
  shots. For every action scene write the camera angle and pose explicitly and prefix "Use the reference image ONLY
  for how the two characters look and the drawing style. Draw a NEW composition and camera angle as described, NOT
  the same standing pose as the reference." (reel 5: lean / sip / laugh / hair-touch all needed this).
- **Text**: Klein can't spell beyond 2–3 words. For phone messages and "Seen ✓✓": generate a blank phone
  ("Only a phone, no people … its screen completely empty and black. No text anywhere.") and draw the bubbles with
  `python reels/phone_text.py blank.jpg out.jpg bubbles.json` (sent/received bubbles, status line, colour emoji —
  see its docstring). Other signs: same idea with PIL (`segoeui.ttf`, `seguisym.ttf`, `seguiemj.ttf`).
  Short glowing numbers/labels ("3", "2", "1s", red ✗) can go in the prompt.
  Titles and cards ("MIRRORING", "✗ copying every move / ✓ matching her energy"): generate the object with no text
  (brain, blank card) and add glowing text with PIL (`arialbd.ttf` titles, `segoeuib.ttf` lines, `seguisym.ttf` for
  ✗ ✓; glow = text layer blurred 14 px + 5 px under the sharp text). See `reels/mirror-trick/` for the code.
  **Keep text out of the caption band (frame y 0.42–0.58)**: put titles/graphics in the upper third, or shift the
  image up in PIL. For a two-item card, make a first version with only item 1 and reveal item 2 on the next shot.
- **Review every image** on a gridded contact sheet (red 10% grid, label in the corner). Reject: wrong location,
  extra characters, man not matching `refs/man.jpg` (beard, hoodie, joggers), garbled text, wrong emotion, the pose not saying what the line says.
  **Anatomy check** (zoom each character to ≥ 400 px wide, a contact-sheet thumbnail is too small): exactly two arms,
  two hands, two legs, two feet each — count the LEGS and FEET as carefully as the hands (no third foot, no extra leg,
  no legs merging with people behind); feet point the same way as the body; no arm crossing someone's face. Reject anything else. Regenerate rejects with a new seed and fixed refs.
  Move rejects to `img/rejected/`.
- Budget ~15–20 images: story beats in the main setting + ~5–8 in other locations (street, office, crosswalk,
  stage, bedroom, hallway) + 1–3 object shots (brain, heart, phone, number).
- Flow fallback quirks: generate scene 1 alone, then the rest with `reference_images`; `download_quality:"upscaled"`
  for 2K; if a reference upload keeps failing, drop the ref; never run downloads and generations together;
  `flow_download` by title prefix can return someone else's image — compare it to the original.

### 4. Shot list (`reel.json`) — editing rules
Schema: see the docstring at the top of `reels/make_reel.py`. Key fields per shot: `image`, `text` (verbatim,
consecutive, covering the whole script), `focus`, `zoom`, `drift`, `punch`, `flash`, `pause_before`, `sfx`,
`flip` (VHS rewind montage). Top level: `audio` (one take), `speed`, `music_cues` or `music`, `music_volume`, `fade_out`.

- **Cut every 1.5–3 s** (~18–22 shots for 40 s). No shot > 3.1 s; merge fragments < 0.8 s into a neighbour.
- **Camera follows the narration.** `focus: "man"` / `"man-face"` are found automatically (his yellow hoodie and warm glow; `man-face` lands on his face).
  Anything else: `[x, y, frame_y]` read off the gridded sheet. **Faces/bubbles at frame_y ≈ 0.3–0.36** so the
  centred caption never covers them.
- **Zoom grammar**: section opens WIDE (zoom 1.0, `drift` 0.05) → key phrase punches in (`punch: true`,
  zoom 1.8–2.2 on a face) → reaction shot of the other person. Reuse one image for wide + close-up.
  End shot: wide with `drift: -0.08` (pull out) + `fade_out: 1.0`.
- **Sections** ("First/Second/Third", "Mistake/Fix"): `pause_before: 0.25` + `sfx: [{"name": "whoosh", "at": -0.15}]`;
  an impact lands on the cut automatically. Never `music_drop`, never pauses > 0.6 s.
- **Hook** (shot 1): tightest framing, `sfx: ["hook"]` or `["bass"]`, optionally `flash`.
- **Variety**: never two object/phone screens in a row; max 3 per reel.
- `speed`: 1.0 by default; up to ~1.1 if the take reads slow (< 2.3 w/s). Never < 1.0.

### 5. Music — match the mood, per section
1. **Name the mood of each section** from the script (hook, each section, ending).
2. **Pick tracks** from the library below, or find new ones (step 3).
3. **Find new tracks**: scrape Mixkit mood/tag pages (`https://mixkit.co/free-stock-music/mood/<sad|romantic|emotional|hopeful|dark|dramatic|mysterious>/`,
   `/tag/<lo-fi|piano|trap|beats>/`, `/hip-hop/`) → `{mp3_url: (title, page)}` catalog → pull 40 s excerpts with
   ffmpeg (`-ss 15 -t 40`) into `audio/cand/` → rank with `rank_music.py` (target = sample.mp4 features) or
   `rank_mood.py` (edit its target). Features: BPM feel, brightness, minor/major margin, percussiveness, level steadiness.
4. **Check the whole track stays in its mood**: measure minor–major margin every 4 s; reject tracks that flip
   (e.g. River Flow). Choose the most consistent 20–30 s stretch.
5. Download the full mp3 into `audio/music/`, run `beats.py` (writes `<track>.beats.json`, prints where full level
   starts and strong beats). Start each cue on a strong beat after the intro.
   Typical arcs: tricks/facts → intrigue (`echoes`) then confident (`unforgiven`) at "here's the twist / use it";
   mistake/fix → tense (`out-of-this-world`) ↔ warm (`fifth-of-february`); any warm payoff/ending → `fifth-of-february`.
6. **Mood shifts → `music_cues`**: `[{"shot": 0, "music": tense, "start": 117.26}, {"shot": <fix shot>, "music": warm, "start": 1.6}, {"shot": <next mistake>, "music": tense}, ...]`.
   A returning track resumes where it left off. 0.25 s crossfade on the cut.
   Single mood → one cue (or `music` + `music_start`); with one track you may also set `"beat_sync": true` so section cuts land on beats.
7. **Verify on the bed alone** (`output/<slug>_work/music.wav`, never the full mix — the voice swamps the harmony):
   minor/major per section must match the intended mood.
8. Tell the user the picks are measured, not heard, and offer the alternatives.

**Music library** (`reels/audio/music/`, Mixkit licence: free on social media, no attribution):

| Track | Mood | Use for |
|---|---|---|
| `unforgiven.mp3` | dark minor trap, 152 BPM, steady (≈ sample.mp4) | confident/"tricks" reels (1–3) |
| `waka-floka-type.mp3`, `trapanomics.mp3` | dark trap, more dynamic / punchier | alternatives to unforgiven |
| `out-of-this-world.mp3` | tense, minor 96% of the track, ~86 BPM feel; start 117.26 | mistakes, awkward/tense moments |
| `fifth-of-february.mp3` | warm, major, romantic, 112 BPM; start 1.6 | fixes, hopeful/romantic endings |
| `echoes.mp3` | mysterious/intrigue, minor 96%, 112 BPM, low percussion; start 162.865 | hooks, "psychology fact" reveals, observing behaviour |
| `ode-to-loneliness.mp3` | flips minor/major (50%) | avoid |
| `silent-descent.mp3` | sad minor, soft beat | REJECTED for reel 4 (whole-reel) — only for purely sad beats |
| `river-flow.mp3` | flips minor/major every few seconds | avoid |
| `just-chill`, `sicilian-coffee`, `sweet-september`, `recline-and-chill`, `night-sky` | chill/bright | rejected mood for this channel |

### 6. Sound effects
Names usable in a shot's `sfx` (list of names or `{"name", "at", "gain"}`; `at` = seconds after the cut, may be negative).
Peaks are pre-aligned to the cut in `make_reel.py`'s `SFX` table.

| Name | Use |
|---|---|
| `hook` | first shot of the reel |
| `bass` | hard hit on a shocking hook line |
| `whoosh` | location change; section opener at `at: -0.15` |
| `whoosh2` | softer move to a reaction/close-up |
| `pop` | punch-ins, items appearing (several pops 0.3 s apart for stacking messages) |
| `impact` | added automatically on section cuts |
| `correct` / `wrong` | ✓ / ✗, good / bad behaviour (`at` 0.3–0.6) |
| `sparkle` | positive reveal, blush, heart, brain lighting up |
| `heartbeat` | tension or a meaningful pause |
| `glitch` | cracking number/heart, "something broke" |
| `rewind` | with a `flip` VHS rewind shot |
| `riser` | build-up into a reveal |
| `scratch` | record scratch / "freeze frame" hook |
Library is Mixkit (`audio/sfx/`); new ones: scrape `https://mixkit.co/free-sound-effects/<tag>/`, then measure onset/peak.

### 7. Render and QA (do all of it before replying)
1. Render. The renderer prints word matching ("heard N (M matching)") and the shot table, and writes
   `<slug>_work/timeline.json`, `music.wav`, `mix.wav`, `captions.ass`.
2. **Frames** (anatomy gate again: count 2 arms / 2 hands / 2 legs / 2 feet per visible person on frames at 10 % and 90 % of every shot): middle frame of every shot tiled into one sheet (`select='eq(n\,F)+…',tile=10x2`) — check framing,
   faces above captions, no stray characters, and the anatomy check again on every person in frame.
3. **Audio**: quietest 0.1 s window > −40 dB (no dead gaps); loudness ≈ −14 to −15 LUFS (`ebur128`);
   music mood per section measured on `music.wav`.
4. Shot lengths 0.8–3.1 s.
5. Reply with: output path, length/size/cost, how each script beat was shown, what differs from the script and why,
   remaining TTS budget if low. Keep it concise.

## After user feedback
Fix it, re-run QA, and add a row to the feedback table above so it never happens again.
