#!/bin/bash
# record takes listed as args, 25 s apart (Gemini 3/min limit); skips existing wavs
cd "$(dirname "$0")"
for i in "$@"; do
  [ -f chapters/take$i.wav ] && continue
  python3 tts_gemini.py chapters/take$i.txt chapters/take$i.wav && echo "take$i OK" || echo "take$i FAIL"
  sleep 25
done
