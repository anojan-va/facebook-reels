"""Find and download stock videos and photos for long-form videos.

Usage:
  python stock.py search "<query>" <out-dir> [--type video|photo] [--provider auto|pexels|pixabay|mixkit] [--n 8]
      Downloads up to n small previews into <out-dir>/cand/<query>/ and writes a numbered contact sheet
      <out-dir>/cand/<query>.jpg (middle frame of each video) so you can pick by eye. Prints one line per candidate.
  python stock.py get <hd-url> <out-file> [--start S --dur D]
      Downloads the full-quality file; for videos, optionally keeps only S..S+D seconds.

Providers (auto = the first that works, in this order):
  pexels   videos + photos, 1080p/4K. Key: $PEXELS_API_KEY, or a network secret for api.pexels.com (Authorization header).
  pixabay  videos + photos, 1080p.    Key: $PIXABAY_API_KEY (Pixabay takes the key as a URL parameter).
  mixkit   videos only, 720p, no key (Mixkit licence: free, no attribution).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}


def fetch(url: str, headers=None, timeout=60) -> bytes:
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def pexels(q, kind, n):
    key = os.environ.get("PEXELS_API_KEY", "")
    base = "https://api.pexels.com/videos/search" if kind == "video" else "https://api.pexels.com/v1/search"
    url = f"{base}?query={urllib.parse.quote(q)}&orientation=landscape&per_page={n}"
    data = json.loads(fetch(url, {"authorization": key} if key else {}))
    out = []
    if kind == "video":
        for v in data.get("videos", []):
            files = sorted((f for f in v["video_files"] if f.get("width") and f["width"] >= 640 and f.get("file_type") == "video/mp4"),
                           key=lambda f: f["width"])
            if not files:
                continue
            hd = next((f for f in files if f["width"] >= 1920), files[-1])
            out.append({"id": f"pexels-{v['id']}", "title": v["url"].rstrip("/").split("/")[-1], "preview": files[0]["link"],
                        "hd": hd["link"], "dur": v.get("duration"), "size": f"{hd['width']}x{hd['height']}", "page": v["url"]})
    else:
        for p in data.get("photos", []):
            out.append({"id": f"pexels-{p['id']}", "title": p.get("alt") or "", "preview": p["src"]["medium"],
                        "hd": p["src"]["original"], "size": f"{p['width']}x{p['height']}", "page": p["url"]})
    return out


def pixabay(q, kind, n):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        raise RuntimeError("no PIXABAY_API_KEY")
    base = "https://pixabay.com/api/videos/" if kind == "video" else "https://pixabay.com/api/"
    data = json.loads(fetch(f"{base}?key={key}&q={urllib.parse.quote(q)}&per_page={max(n, 3)}&safesearch=true"
                            + ("" if kind == "video" else "&orientation=horizontal&image_type=photo")))
    out = []
    for h in data.get("hits", [])[:n]:
        if kind == "video":
            v = h["videos"]
            hd = v.get("large") if v.get("large", {}).get("url") else v["medium"]
            out.append({"id": f"pixabay-{h['id']}", "title": h.get("tags", ""), "preview": v["tiny"]["url"], "hd": hd["url"],
                        "dur": h.get("duration"), "size": f"{hd['width']}x{hd['height']}", "page": h["pageURL"]})
        else:
            out.append({"id": f"pixabay-{h['id']}", "title": h.get("tags", ""), "preview": h["webformatURL"],
                        "hd": h.get("largeImageURL"), "size": f"{h['imageWidth']}x{h['imageHeight']}", "page": h["pageURL"]})
    return out


def mixkit(q, kind, n):
    if kind != "video":
        raise RuntimeError("mixkit has no photos")
    html = fetch(f"https://mixkit.co/free-stock-video/discover/{urllib.parse.quote(q.replace(' ', '-'))}/").decode("utf-8", "replace")
    out, seen = [], set()
    for m in re.finditer(r'https://assets\.mixkit\.co/[^"\s]+?-360\.mp4', html):
        url = m.group(0)
        if url in seen:
            continue
        seen.add(url)
        vid = re.search(r"/(\d+)(?:-video)?-360\.mp4", url).group(1)
        slug = re.search(rf'/free-stock-video/([a-z0-9-]+-{vid})/', html)
        out.append({"id": f"mixkit-{vid}", "title": slug.group(1) if slug else vid, "preview": url,
                    "hd": url.replace("-360.mp4", "-720.mp4"), "size": "1280x720",
                    "page": f"https://mixkit.co/free-stock-video/{slug.group(1)}/" if slug else ""})
        if len(out) >= n:
            break
    return out


PROVIDERS = {"pexels": pexels, "pixabay": pixabay, "mixkit": mixkit}


def search(q, kind="video", provider="auto", n=8):
    order = list(PROVIDERS) if provider == "auto" else [provider]
    errors = []
    for p in order:
        try:
            res = PROVIDERS[p](q, kind, n)
            if res:
                return p, res
            errors.append(f"{p}: no results")
        except Exception as e:  # missing key, 401, network
            errors.append(f"{p}: {str(e)[:120]}")
    sys.exit("no stock results — " + "; ".join(errors))


def sheet(files, out):
    """Numbered contact sheet: middle frame of each candidate, 4 per row."""
    tiles = []
    for i, f in enumerate(files):
        t = Path(f).with_suffix(".thumb.jpg")
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                             capture_output=True, text=True).stdout.strip()
        ss = float(dur) / 2 if dur and dur != "N/A" else 0
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.2f}", "-i", f, "-frames:v", "1", "-vf",
                        f"scale=480:270:force_original_aspect_ratio=increase,crop=480:270,"
                        f"drawtext=text='{i}':fontcolor=red:fontsize=44:x=12:y=8:box=1:boxcolor=black@0.6", str(t)])
        if t.exists():
            tiles.append(str(t))
    if not tiles:
        return
    cols = 4
    rows = (len(tiles) + cols - 1) // cols
    inputs = sum((["-i", t] for t in tiles), [])
    layout = "|".join(f"{(k % cols) * 480}_{(k // cols) * 270}" for k in range(len(tiles)))
    pad = f"pad={cols * 480}:{rows * 270}" if len(tiles) > 1 else "null"
    graph = ("".join(f"[{k}:v]" for k in range(len(tiles))) + f"xstack=inputs={len(tiles)}:layout={layout}:fill=black"
             if len(tiles) > 1 else "[0:v]null")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, str(out)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["search", "get"])
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--type", default="video")
    ap.add_argument("--provider", default="auto")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--start", type=float)
    ap.add_argument("--dur", type=float)
    args = ap.parse_args()
    if args.cmd == "get":
        out = Path(args.b)
        out.parent.mkdir(parents=True, exist_ok=True)
        raw = out.with_suffix(".src" + out.suffix)
        raw.write_bytes(fetch(args.a, timeout=300))
        if args.start is not None or args.dur is not None:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(args.start or 0), *(["-t", str(args.dur)] if args.dur else []),
                            "-i", str(raw), "-an", "-c:v", "libx264", "-crf", "16", "-preset", "fast", str(out)], check=True)
            raw.unlink()
        else:
            raw.rename(out)
        print(out)
        return
    q, root = args.a, Path(args.b)
    provider, res = search(q, args.type, args.provider, args.n)
    d = root / "cand" / re.sub(r"[^a-z0-9]+", "-", q.lower())
    d.mkdir(parents=True, exist_ok=True)
    files = []
    for i, r in enumerate(res):
        ext = ".mp4" if args.type == "video" else ".jpg"
        f = d / f"{i:02d}{ext}"
        try:
            f.write_bytes(fetch(r["preview"]))
            files.append(str(f))
        except Exception as e:
            print(f"  ! preview {i} failed: {e}")
        print(f"{i:2d}  {provider:7s} {r['size']:>9s}  {str(r.get('dur') or ''):>4s}  {r['title'][:50]:50s}  {r['hd']}")
    (d / "results.json").write_text(json.dumps(res, indent=1))
    sheet(files, d.with_suffix(".jpg"))
    print(d.with_suffix(".jpg"))


if __name__ == "__main__":
    main()
