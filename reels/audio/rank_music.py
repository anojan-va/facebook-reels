"""Rank candidate music excerpts (cand/*.wav) by similarity to a reference's features."""
import json, warnings
import concurrent.futures as cf
warnings.filterwarnings("ignore")
from analyze_music import feats

S = dict(bpm=152, bright=1502, minor_margin=0.10, perc=0.22, bass=23.89)   # sample.mp4 background

def one(u):
    try:
        return u, feats("cand/" + u.split("/")[-1].replace(".mp3", ".wav"), offset=0, dur=40)
    except Exception:
        return u, None

def dist(f):
    b = min(abs(f["bpm"] - S["bpm"]), abs(f["bpm"] * 2 - S["bpm"]), abs(f["bpm"] / 2 - S["bpm"])) / 20
    return (b + abs(f["bright"] - S["bright"]) / 400 + max(0, 0.05 - f["minor_margin"]) * 10
            + abs(f["perc"] - S["perc"]) / 0.15 + abs(f["bass"] - S["bass"]) / 8)

if __name__ == "__main__":
    cat = json.load(open("cand/catalog.json"))
    with cf.ProcessPoolExecutor(6) as ex:
        res = dict(ex.map(one, cat))
    json.dump(res, open("cand/features.json", "w"), indent=1)
    for d, u in sorted((dist(f), u) for u, f in res.items() if f)[:15]:
        print(f"{d:5.2f}  {cat[u][0][:28]:28s} {cat[u][1]:10s} {u.split('/')[-1]:9s} {res[u]}")
