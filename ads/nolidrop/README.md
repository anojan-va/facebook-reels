# NoliDrop video ads (9:16, 1080x1920)

Three paid-social ads for the NoliDrop app (AI pool-care assistant, Google Play). Concepts and scripts: `concepts.md`.
No stock footage: motion graphics, rebuilt app UI, the brand mascot (Noli) and AI stills.

| Ad | File | Look | Voice (Gemini TTS) | Music (Mixkit) |
|---|---|---|---|---|
| 1 "The Receipt" | `ad1.py` | sunny cyan/white, Fredoka, splash transitions | Zephyr, polished/upbeat | `gear` |
| 2 "Your Brain on Green Water" | `ad2.py` | night pool, neon, Bebas Neue, glitch/ripple; grade flips at the Drop | Orus, punchy | `infected-vibes` → `dirty-thinkin` at the Drop |
| 3 UGC "Don't go to the pool store yet" | `ad3.py` | creator selfies + POV phone (green screen keyed), Inter Black word captions | Leda, casual | `sounds-good` |

Shared: the signature **Drop** (Noli splashes in, the ripple clears the water), the line "Don't guess. Noli knows.",
and an end card modelled on the brand's official vertical ad (logo, "No more pool headaches.", Play badge, Noli + Home screen).

## Rebuild
1. Voice: `./voices.sh` (the exact Gemini TTS calls used).
2. Images: `python3 ../../reels/polli.py gen1.json`, then `gen1b.json` (UGC refs need `u-hook.jpg`) and `gen2.json`.
3. Sprites: `python3 cutout.py img/n-*.jpg refs/noli-thumbsup.jpg` (white-background poses → RGBA in `sprites/`).
4. Render: `python3 adN.py --plan | --stills | --frame 6.5,20 | (full)` → `output/nolidrop-ad-N.mp4`
   (`work/<name>/stills.jpg` = contact sheet; `music.wav`/`mix.wav` for audio QA). `./qa.sh output/x.mp4` = loudness + gaps.

## Renderer (`adkit.py`)
PIL/numpy frames → ffmpeg (4 parallel chunks). Whisper word timings with long pauses squeezed (`max_gap`, `extra` adds a
breath before a word); shots start on word indexes; transitions `whip zoom flash splash ripple glitch slide dip` each with
an SFX; captions `phrase` / `build` (TikTok pop + highlight box); music cues ducked under the voice; mix loudnorm −14 LUFS.
App screens (`ui_home`, `ui_values`, `ui_results`, `ui_guide`) are English vector rebuilds of the real screens — only real
features (water analysis, PRIORITY #1 order, I have a problem, Start-up, Winterizing). No stats, savings figures or reviews.

Gotchas: Montserrat-Black renders hollow in PIL (reversed contours) → use Inter Black; Klein copies a reference image's
composition, which is how `bg-pool-blue` matches `bg-pool-green` for the ripple reveal.
