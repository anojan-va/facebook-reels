"""Record the missing takes with as few Gemini calls as possible (10/day, failed calls count).
Each missing take is tried whole once; if that fails it is split at a line boundary into takeNa/takeNb (~100 words, fewer 502s).
Stops at the first 429 (daily quota). Usage: python3 rec2.py [max_calls]"""
import subprocess
import sys
import time
from pathlib import Path

C = Path(__file__).parent / "chapters"
strikes = 0
budget = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def rec(stem):
    global budget
    if (C / f"{stem}.wav").exists():
        return True
    if budget <= 0:
        return None
    budget -= 1
    r = subprocess.run([sys.executable, "tts_gemini.py", f"chapters/{stem}.txt", f"chapters/{stem}.wav"], cwd=C.parent,
                       capture_output=True, text=True)
    print(stem, "OK" if r.returncode == 0 else "FAIL " + (r.stdout + r.stderr).strip().splitlines()[0][:80], flush=True)
    global strikes
    if "429" in r.stdout + r.stderr:
        budget = 0          # every 429 also counts against the 10/day quota: stop at the first one
    else:
        strikes = 0
    time.sleep(65)
    return r.returncode == 0


for i in range(1, 10):
    t = f"take{i}"
    if (C / f"{t}.wav").exists() or ((C / f"{t}a.wav").exists() and (C / f"{t}b.wav").exists()):
        continue
    if not (C / f"{t}a.txt").exists():
        if rec(t):
            continue
        lines = (C / f"{t}.txt").read_text().strip().splitlines()
        n = sum(len(l.split()) for l in lines)
        acc, k = 0, 0
        while acc + len(lines[k].split()) / 2 < n / 2:
            acc += len(lines[k].split()); k += 1
        (C / f"{t}a.txt").write_text("\n".join(lines[:k]) + "\n")
        (C / f"{t}b.txt").write_text("\n".join(lines[k:]) + "\n")
    for h in "ab":
        rec(f"{t}{h}")
missing = [i for i in range(1, 10) if not (C / f"take{i}.wav").exists()
           and not ((C / f"take{i}a.wav").exists() and (C / f"take{i}b.wav").exists())]
print("MISSING", missing if missing else "none")
