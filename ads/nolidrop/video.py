"""Ad 3: animate the approved storyboard keyframes with an image-to-video model on Pollinations (async jobs).
Usage: python3 video.py K1 K2 ...  |  all     -> storyboard/clips/<id>.mp4
Model: Kling 3.0 Standard, 9:16, 720p, 4 s, no audio (the ad uses its own voice-over, music and SFX)."""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SB = HERE / "storyboard"
MODEL = "kwaivgi/kling-v3.0-std"
BASE = "https://gen.pollinations.ai"
KEEP = (" Keep the woman's face, hair, clothes and the backyard exactly as in the start image. Natural realistic motion, "
        "smartphone footage, no text, no extra people, hands anatomically correct with five fingers.")
GREEN = " The phone screen stays a flat uniform bright green the whole time, with no interface appearing on it."
PROMPTS = {
    "K1": "Handheld front-camera selfie video: she talks excitedly to the camera with natural mouth movement and expressive "
          "eyebrows, then points down at the green pool beside her, slight natural hand-held camera shake." + KEEP,
    "K2": "Her hand slowly dips the colourful test strip into the murky green pool water, small ripples spread across the "
          "surface, gentle hand-held push-in, sun glints on the water." + KEEP,
    "K3": "First-person POV: the hand holding the phone sways gently as she stands at the pool edge, the murky green water "
          "and floating algae drift slowly below, slight natural camera shake." + GREEN + KEEP,
    "K5": "She taps the phone screen with her thumb a few times while holding it in both hands, small natural head movement, "
          "the green pool water shimmers in the background." + GREEN + KEEP,
    "K6": "Handheld selfie video: smiling, she talks to the camera and counts on her hand, first one index finger raised, "
          "then she raises a second finger to show two, natural mouth movement." + KEEP,
    "K7": "Handheld selfie video: she smiles confidently and gives the camera a playful wink, holding the phone next to her "
          "cheek, the clear blue pool water sparkles behind her." + GREEN + KEEP,
}


def submit(sid, urls, duration=4, seed=1):
    q = {"model": MODEL, "image": urls[sid], "duration": duration, "aspectRatio": "9:16", "audio": "false", "seed": seed}
    url = f"{BASE}/video/{urllib.parse.quote(PROMPTS[sid])}?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(url, headers={"Prefer": "respond-async"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            if r.status == 200 and r.headers.get("content-type", "").startswith("video"):
                return sid, r.read(), f"direct {time.time() - t0:.0f}s"
            info = json.loads(r.read() or b"{}")
            loc = r.headers.get("Location") or f"/v1/jobs/{info.get('id')}"
    except urllib.error.HTTPError as e:
        return sid, None, f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}"
    job = loc if loc.startswith("http") else BASE + loc
    while time.time() - t0 < 1800:
        time.sleep(8)
        try:
            with urllib.request.urlopen(job, timeout=60) as r:
                st = json.loads(r.read())
        except urllib.error.HTTPError as e:
            return sid, None, f"poll HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}"
        s = str(st.get("status", "")).lower()
        if s in ("completed", "succeeded", "success", "done"):
            res = st.get("result_url") or st.get("url") or job.rstrip("/") + "/result"
            res = res if res.startswith("http") else BASE + res
            with urllib.request.urlopen(res, timeout=300) as r:
                return sid, r.read(), f"ok {time.time() - t0:.0f}s"
        if s in ("failed", "error", "cancelled", "expired"):
            return sid, None, f"job {s}: {json.dumps(st)[:300]}"
    return sid, None, "timeout"


if __name__ == "__main__":
    urls = json.loads((SB / "urls.json").read_text())
    ids = list(PROMPTS) if sys.argv[1] == "all" else [a for a in sys.argv[1:] if not a.startswith("seed=")]
    seed = next((int(a[5:]) for a in sys.argv[1:] if a.startswith("seed=")), 1)
    (SB / "clips").mkdir(exist_ok=True)
    with ThreadPoolExecutor(3) as ex:
        for sid, data, msg in ex.map(lambda s: submit(s, urls, 4, seed), ids):
            print(sid, msg, flush=True)
            if data:
                (SB / "clips" / f"{sid}.mp4").write_bytes(data)
