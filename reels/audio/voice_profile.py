"""Voice fingerprint: median pitch, pitch spread, brightness, MFCC timbre. Usage: python voice_profile.py ref.m4a other.m4a ..."""
import sys, warnings
import numpy as np, librosa
warnings.filterwarnings("ignore")

def profile(path):
    y, sr = librosa.load(path, sr=16000, mono=True)
    f0, voiced, _ = librosa.pyin(y, fmin=60, fmax=300, sr=sr)
    f0 = f0[voiced & ~np.isnan(f0)]
    mf = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)[1:].mean(axis=1)
    return dict(pitch=float(np.median(f0)), spread=float(np.std(f0)),
                bright=float(librosa.feature.spectral_centroid(y=y, sr=sr).mean()), mfcc=mf)

def distance(a, b):
    return (abs(a["pitch"] - b["pitch"]) / 5 + abs(a["spread"] - b["spread"]) / 5
            + abs(a["bright"] - b["bright"]) / 100 + float(np.linalg.norm(a["mfcc"] - b["mfcc"])) / 10)

if __name__ == "__main__":
    ref = profile(sys.argv[1])
    for f in sys.argv[1:]:
        p = profile(f)
        print(f"{f.replace(chr(92), '/').split('/')[-1]:22s} pitch {p['pitch']:6.1f} Hz  spread {p['spread']:5.1f}  "
              f"bright {p['bright']:6.0f}  distance-to-ref {distance(ref, p):5.2f}")
