"""Join separately rendered parts into the final video, with a short dip through black between parts.

Usage: python3 merge.py <out.mp4> part1.mp4 part2.mp4 ... [--dip 0.4] [--crf 21]
Writes <out.mp4> (1080p master) plus <out>-send.mp4 (< 400 MB, for chat upload) and <out>-720p.mp4 (< 100 MB, for git).
A changed part is re-rendered on its own (make_long.py partN.json) and the merge is simply run again.
"""
import argparse
import subprocess
from pathlib import Path


def duration(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("parts", nargs="+")
    ap.add_argument("--dip", type=float, default=0.4)
    ap.add_argument("--crf", type=int, default=21)
    a = ap.parse_args()
    parts = [Path(p) for p in a.parts]
    durs = [duration(p) for p in parts]
    inputs = sum((["-i", str(p)] for p in parts), [])
    v, au, graph, t = "[0:v]", "[0:a]", [], durs[0]
    for k in range(1, len(parts)):
        off = t - a.dip
        graph.append(f"{v}[{k}:v]xfade=transition=fadeblack:duration={a.dip}:offset={off:.3f}[v{k}]")
        graph.append(f"{au}[{k}:a]acrossfade=d={a.dip}[a{k}]")
        v, au = f"[v{k}]", f"[a{k}]"
        t = off + durs[k]
    out = Path(a.out)
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(graph), "-map", v, "-map", au,
                    "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    total = duration(out)
    # delivery copies sized to the upload limits
    send = out.with_name(out.stem + "-send.mp4")
    kbps = int(370 * 8 * 1024 / total) - 200
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-c:v", "libx264", "-preset", "medium", "-b:v", f"{kbps}k",
                    "-maxrate", f"{int(kbps * 1.4)}k", "-bufsize", f"{kbps * 2}k", "-c:a", "copy", "-movflags", "+faststart", str(send)], check=True)
    small = out.with_name(out.stem + "-720p.mp4")
    kbps7 = int(88 * 8 * 1024 / total) - 140
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-vf", "scale=1280:720", "-c:v", "libx264", "-preset", "medium",
                    "-b:v", f"{kbps7}k", "-maxrate", f"{int(kbps7 * 1.3)}k", "-bufsize", f"{kbps7 * 2}k", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", str(small)], check=True)
    for f in (out, send, small):
        print(f"{f}  {duration(f) / 60:.2f} min  {f.stat().st_size / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
