"""Ad 3 (UGC, AI video) storyboard keyframes with Nano Banana Pro on Pollinations.
Each keyframe is saved to storyboard/<id>.jpg and its hosted URL to storyboard/urls.json (the video models need a public
start-frame URL). Refs: other keyframes' hosted URLs (keeps the creator consistent).
Usage: python3 storyboard.py K1            # one or more ids
       python3 storyboard.py all
"""
import base64
import concurrent.futures as cf
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "storyboard"
API = "https://gen.pollinations.ai/v1/images"
MODEL = "google/gemini-3-pro-image"

CREATOR = ("a friendly woman in her late 20s with shoulder-length wavy light-brown hair with sun-kissed highlights, "
           "sunglasses pushed up on her head, an opaque light-blue linen button-up shirt worn open over a thick opaque white crew-neck cotton t-shirt, and a thin gold necklace")
LOOK = ("Photorealistic vertical 9:16 frame from a casual TikTok/Instagram video filmed on an iPhone front camera: natural "
        "skin texture, slight handheld feel, warm golden-hour backyard light. Anatomically correct: two arms, two hands, "
        "five fingers on each hand. No text, no captions, no logos, no watermark, no camera app interface, no recording timer, no battery or status icons: a clean full-bleed photo.")
SAME = "Keep the woman exactly the same person as in the reference image (same face, hair, sunglasses, light-blue linen shirt over a white t-shirt, necklace) and the same backyard pool."
GREEN = ("The phone screen faces the viewer and is a perfectly flat uniform bright chroma-key green (#00FF00), filling the "
         "whole screen edge to edge, no reflections, no interface.")

SHOTS = {
    "K1": dict(refs=[], prompt=f"Selfie at arm's length of {CREATOR}, standing at the edge of her backyard swimming pool whose "
               "water is murky cloudy green with algae. She looks straight into the camera, eyebrows raised, mouth open "
               "mid-sentence like she is saying 'wait!', and points down at the green pool with her free hand. {LOOK}"),
    "K2": dict(refs=["K1"], prompt="Close-up, slightly high angle: the same woman's hand (pink nails, gold ring-free) holds a pool "
               "test strip just above the murky cloudy green pool water, the strip's colour pads clearly visible, the "
               "stone pool edge at the bottom of the frame, sun glints on the water. {SAME} {LOOK}"),
    "K3": dict(refs=["K1"], prompt="First-person POV looking down: the same woman's hand holds a modern smartphone in portrait "
               "orientation above the stone edge of her murky green pool, her bare feet visible at the bottom of the frame. "
               f"{GREEN} {{SAME}} {{LOOK}}"),
    "K5": dict(refs=["K1"], prompt="Close-up over-the-shoulder POV: the same woman sits on a sun lounger by her pool and holds a "
               "smartphone in both hands, her right thumb tapping the screen. "
               f"{GREEN} {{SAME}} {{LOOK}}"),
    "K6": dict(refs=["K1"], prompt="Selfie at arm's length of the same woman by her pool, smiling and explaining, holding up her "
               "free hand palm facing the camera with only the index finger pointing straight up (counting 'one'), other fingers folded, next to her face. {SAME} {LOOK}"),
    "K7": dict(refs=["K1"], prompt="Selfie at arm's length of the same woman, now relaxed and happy with a confident knowing smile, "
               "holding her phone up next to her cheek with the screen facing the camera. The camera is held a bit higher and wider so that "
               "the same backyard pool fills most of the background behind her, and it now has sparkling crystal-clear turquoise blue water with sunlight reflections. "
               f"{GREEN} {{SAME}} {{LOOK}}"),
}


def gen(sid, urls, seed=1, model=MODEL):
    sh = SHOTS[sid]
    prompt = sh["prompt"].format(LOOK=LOOK, SAME=SAME)
    body = {"model": model, "prompt": prompt, "size": "1080x1920", "response_format": "url", "seed": seed}
    endpoint = "generations"
    if sh["refs"]:
        body["image"] = [{"image_url": urls[r]} for r in sh["refs"]]
        endpoint = "edits"
    req = urllib.request.Request(f"{API}/{endpoint}", data=json.dumps(body).encode(), method="POST",
                                 headers={"content-type": "application/json"})
    t0 = time.time()
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            msg = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}"
            if e.code in (400, 401, 402, 403) or attempt == 2:
                return sid, None, msg
            time.sleep(5)
    item = data["data"][0]
    url = item.get("url")
    raw = base64.b64decode(item["b64_json"]) if item.get("b64_json") else urllib.request.urlopen(url, timeout=300).read()
    (OUT / f"{sid}.jpg").write_bytes(raw)
    return sid, url, f"ok {time.time() - t0:.0f}s"


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    uf = OUT / "urls.json"
    urls = json.loads(uf.read_text()) if uf.exists() else {}
    ids = list(SHOTS) if sys.argv[1] == "all" else sys.argv[1:]
    seed = 1
    if ids and ids[-1].startswith("seed="):
        seed = int(ids.pop()[5:])
    with cf.ThreadPoolExecutor(6) as ex:
        for sid, url, msg in ex.map(lambda s: gen(s, urls, seed), ids):
            print(sid, msg, url or "")
            if url:
                urls[sid] = url
    uf.write_text(json.dumps(urls, indent=1))
