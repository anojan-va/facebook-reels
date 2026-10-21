# Psychology reels for Facebook

When the user sends a reel script (or asks to change a reel), use the **`facebook-reels` skill**
(`.claude/skills/facebook-reels/SKILL.md`). It holds the whole pipeline: voice, images, editing rules, music
selection, sound effects, QA, and every piece of user feedback so far. Keep it up to date — when the user corrects
something, add a row to its feedback table.

Project layout: `reels/` (renderer `make_reel.py`, clients `tts.py` / `polli.py` / `flow.py`, audio library and
analysis scripts in `reels/audio/`, one folder per reel, finished videos in `reels/output/`). Reference look: `sample.mp4`.
