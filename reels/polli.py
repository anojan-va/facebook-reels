"""Generate images with Pollinations (FLUX), in parallel.
Key: $POLLINATIONS_KEY, else ~/.pollinations-key (sk_...); in a Claude cloud session neither exists and the
network-secret proxy adds the Authorization header to requests for gen.pollinations.ai.

Usage: python polli.py jobs.json
jobs.json: {"model": "black-forest-labs/flux.2-klein-4b", "size": "1152x2048", "workers": 6,
            "jobs": [{"out": "scene-01.jpg", "prompt": "...", "refs": ["ref.jpg"], "seed": 1}, ...]}
refs (optional, local paths or URLs) are sent as reference images -> /v1/images/edits; without refs -> /generations.
Models: flux.2-klein-4b (refs up to 10, ~0.005 pollen), flux.1-schnell (text only, ~0.002 pollen).
"""
import base64
import concurrent.futures as cf
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://gen.pollinations.ai/v1/images"


def data_uri(ref: str) -> str:
    if ref.startswith(("http://", "https://", "data:")):
        return ref
    mime = mimetypes.guess_type(ref)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(Path(ref).read_bytes()).decode()


def generate(job: dict, model: str, size: str, key: str, tries: int = 3) -> str:
    out = Path(job["out"])
    body = {"prompt": job["prompt"], "model": job.get("model", model), "size": job.get("size", size),
            "response_format": "b64_json"}
    if job.get("seed") is not None:
        body["seed"] = job["seed"]
    endpoint = "generations"
    if job.get("refs"):
        body["image"] = [{"image_url": data_uri(r)} for r in job["refs"]]
        endpoint = "edits"
    last = ""
    for attempt in range(tries):
        req = urllib.request.Request(f"{API}/{endpoint}", data=json.dumps(body).encode(), method="POST",
                                     headers={"content-type": "application/json",
                                              **({"authorization": f"Bearer {key}"} if key else {})})
        try:
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read())
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
            return f"ok   {out.name}  {time.time() - t0:4.1f}s"
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}"
            if e.code in (400, 401, 402, 403):
                break   # not worth retrying: bad request, bad key, no balance, refused
        except Exception as e:  # network hiccup
            last = repr(e)[:200]
        time.sleep(3 * (attempt + 1))
    return f"FAIL {out.name}  {last}"


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    kf = Path.home() / ".pollinations-key"
    key = os.environ.get("POLLINATIONS_KEY") or (kf.read_text().strip() if kf.exists() else "")
    model = spec.get("model", "black-forest-labs/flux.2-klein-4b")
    size = spec.get("size", "1152x2048")
    with cf.ThreadPoolExecutor(spec.get("workers", 6)) as ex:
        for line in ex.map(lambda j: generate(j, model, size, key), spec["jobs"]):
            print(line, flush=True)


if __name__ == "__main__":
    main()
