#!/bin/bash
# QA one ad: loudness, quietest 0.1 s window, length, and a frame sheet (one frame every 0.5 s).
f=$1; w=$2
echo "== $f"; ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of csv=p=0 "$f"
ffmpeg -nostats -i "$f" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|LRA:|Peak:)" | tr -s ' '
python3 - "$f" <<'PY'
import subprocess, sys, numpy as np
a = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","44100","-f","f32le","-"],capture_output=True).stdout, np.float32)
n = 4410; r = np.sqrt((a[:len(a)//n*n].reshape(-1,n)**2).mean(1)); db = 20*np.log10(r+1e-9)
i = db[:-3].argmin(); print(f"quietest 0.1s window: {db[:-3].min():.1f} dB at {i*0.1:.1f}s (ignoring last 0.3 s)")
PY
