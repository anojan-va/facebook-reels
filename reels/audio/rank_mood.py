"""Rank candidate excerpts for a bittersweet, reflective mood (minor, ~80-95 BPM feel, soft steady beat)."""
import json, warnings, sys
import concurrent.futures as cf
warnings.filterwarnings("ignore")
from analyze_music import feats
import numpy as np, librosa

def one(u):
    f = "cand/" + u.split("/")[-1].replace(".mp3", ".wav")
    try:
        d = feats(f, offset=0, dur=40)
        y, sr = librosa.load(f, sr=11025, mono=True)
        seg = [np.sqrt((y[i:i + sr * 2] ** 2).mean()) for i in range(0, len(y) - sr * 2, sr * 2)]
        d["level_var"] = round(float(np.std(20 * np.log10(np.array(seg) + 1e-9))), 2)
        return u, d
    except Exception:
        return u, None

def score(f):
    bpm = f["bpm"]; feel = min(abs(bpm - 88), abs(bpm / 2 - 88), abs(bpm * 2 - 88))
    return (feel / 12 + max(0, 0.04 - f["minor_margin"]) * 15 + abs(f["perc"] - 0.25) / 0.12
            + abs(f["bright"] - 1300) / 450 + f["level_var"] / 3)

if __name__ == "__main__":
    cat = json.load(open(sys.argv[1]))
    with cf.ProcessPoolExecutor(6) as ex:
        res = dict(ex.map(one, cat))
    json.dump(res, open(sys.argv[1].replace(".json", "-features.json"), "w"), indent=1)
    for s, u in sorted((score(f), u) for u, f in res.items() if f)[:12]:
        print(f"{s:5.2f}  {cat[u][0][:26]:26s} {cat[u][1]:11s} {u.split('/')[-1]:8s} {res[u]}")
