# Petal & Crumb - cake-jar product ad (9:16, 18.4 s)

User-made AI clips (Nano Banana start/end frames + Omni video, prompts in the chat): `clips/v1-transform.mp4` (hand ->
dreamy pastel explosion), `v2-hero.mp4` (hero spin), `v3-spoon.mp4` (spoon scoop). Clips, frames and work files stay local.
`petal.py` edits them: Great Vibes script + Poppins overlays, white flash and blur dissolve, the real round label (cut from
`refs/product.jpg`) as the end-card logo, the clips' own whoosh audio + `fifth-of-february` bed + accent SFX, -14 LUFS.
Rebuild: extract `work/frames/<clip>/NNN.jpg` and `work/audio/<clip>.wav` with ffmpeg, then `python3 petal.py`.

Voiced version (`output/petal-and-crumb-ad-vo.mp4`, 22.8 s): `vo/script.txt` recorded with
`python3 ../../reels/tts.py vo/script.txt vo/voice-1.wav Sulafat "warmly, softly and deliciously, like a premium dessert
commercial voice-over, a gentle smile in the voice, unhurried with small dreamy pauses"`, silence-trimmed, 1.1x. Cuts and
text follow the VO word times; music ducks under the voice. Logo = inset ellipse fitted to the label (a circle caught the jam).
