"""Music features: tempo, brightness, major/minor, percussiveness.
Usage: .venv python analyze_music.py [--strip-voice] files...
--strip-voice estimates the background under narration (REPET-SIM) before measuring."""
import sys, warnings
import numpy as np, librosa
warnings.filterwarnings("ignore")
MAJ = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
MIN = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])

def background(y, sr):
    S, ph = librosa.magphase(librosa.stft(y))
    filt = librosa.decompose.nn_filter(S, aggregate=np.median, metric="cosine", width=int(librosa.time_to_frames(2, sr=sr)))
    filt = np.minimum(S, filt)
    mask = librosa.util.softmask(filt, 2 * (S - filt), power=2)
    return librosa.istft(mask * S * ph, length=len(y))

def feats(path, offset=0, dur=60, strip=False):
    y, sr = librosa.load(path, sr=22050, mono=True, offset=offset, duration=dur)
    if strip:
        y = background(y, sr)
    h, p = librosa.effects.hpss(y)
    tempo = float(np.atleast_1d(librosa.beat.beat_track(y=p, sr=sr)[0])[0])
    chroma = librosa.feature.chroma_cqt(y=h, sr=sr).mean(axis=1)
    maj = max(np.corrcoef(np.roll(MAJ, k), chroma)[0, 1] for k in range(12))
    mnr = max(np.corrcoef(np.roll(MIN, k), chroma)[0, 1] for k in range(12))
    S = np.abs(librosa.stft(y))
    return dict(bpm=round(tempo), bright=round(float(librosa.feature.spectral_centroid(S=S, sr=sr).mean())),
                mode="minor" if mnr > maj else "major", minor_margin=round(float(mnr - maj), 2),
                perc=round(float(np.sqrt((p**2).mean()) / (np.sqrt((h**2).mean()) + 1e-9)), 2),
                bass=round(float(S[:24].mean() / S.mean()), 2))

if __name__ == "__main__":
    strip = "--strip-voice" in sys.argv
    for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
        print(f"{f.replace(chr(92), '/').split('/')[-1]:30s}", feats(f, offset=0 if strip else 20, strip=strip))
