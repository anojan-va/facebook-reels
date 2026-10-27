# Psychology reels for Facebook

When the user sends a reel script (or asks to change a reel), use the **`facebook-reels` skill**
(`.claude/skills/facebook-reels/SKILL.md`). It holds the whole pipeline: voice, images, editing rules, music
selection, sound effects, QA, and every piece of user feedback so far. Keep it up to date — when the user corrects
something, add a row to its feedback table.

Project layout: `reels/` (renderer `make_reel.py`, clients `tts.py` / `polli.py` / `flow.py`, audio library and
analysis scripts in `reels/audio/`, one folder per reel, finished videos in `reels/output/`). Reference look: `sample.mp4`.

# Long-form videos (16:9, 15–25 min)

When the user asks for a long video (or a sample of one), use the **`longform-video` skill**
(`.claude/skills/longform-video/SKILL.md`): AI line-art + stock video + motion graphics, renderer `longform/make_long.py`,
stock search `longform/stock.py`, sample project `longform/spotlight-effect/`.

# Video ads (9:16 paid social)

App/product ads live in `ads/<brand>/` (first: `ads/nolidrop/`, see its README). Shared renderer `ads/nolidrop/adkit.py`
(motion graphics, rebuilt app UI, mascot sprites, green-screen phone keying, captions, ducked music, SFX, −14 LUFS).
No stock footage for ads. Show concepts/scripts to the user before spending on voice and images.
