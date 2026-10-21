"""Write <track>.beats.json (beat times + strength) and print where the track is at full level.
Usage: .venv python beats.py music/track.mp3 ..."""
import json, sys, warnings
import numpy as np, librosa
warnings.filterwarnings("ignore")
for f in sys.argv[1:]:
    y, sr = librosa.load(f, sr=22050, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    o = librosa.onset.onset_strength(y=y, sr=sr)
    st = [round(float(o[librosa.time_to_frames(b, sr=sr)]), 2) for b in beats]
    json.dump({"tempo": float(np.atleast_1d(tempo)[0]), "beats": [round(float(b), 3) for b in beats], "strength": st},
              open(f.rsplit(".", 1)[0] + ".beats.json", "w"))
    hop = sr
    lv = [20 * np.log10(np.sqrt((y[i:i + hop] ** 2).mean()) + 1e-9) for i in range(0, len(y) - hop, hop)]
    full = np.median(lv)
    first_full = next(i for i, v in enumerate(lv) if v > full - 3)
    strong = [b for b, s in zip(beats, st) if b >= first_full and s >= np.percentile(st, 85)][:3]
    print(f"{f}: {len(y)/sr:.0f}s tempo {float(np.atleast_1d(tempo)[0]):.0f}  full level from {first_full}s  "
          f"strong beats after that: {[round(float(b), 2) for b in strong]}")
