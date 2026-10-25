#!/bin/bash
# Rebuild this video's motion layers into motion/: HyperFrames full-screen cards (MP4) and Remotion alpha overlays
# (PNG sequences, composited by make_long.py's "clip" overlay). Needs: cd ../motion && npm ci; npx hyperframes browser ensure
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
M=$HERE/../motion
O=$HERE/motion
mkdir -p "$O"
CH=$(ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | head -1)
cd "$M/hyperframes"
for c in size chapter crossing; do npx hyperframes render . -c $c.html -o "$O/$c.mp4" -q delivery --quiet >/dev/null; done
cd "$M/remotion"
r() { rm -rf "$O/$2"; npx remotion render src/index.ts $1 "$O/$2" --sequence --image-format=png --public-dir="$PWD/public" \
        --browser-executable="$CH" --props="$3" --log=error; }
r TitleSlam title '{"top":"WHAT IF","bottom":"AN ASTEROID HIT EARTH?"}'
r BigNumber speed '{"to":20,"unit":"KM/S","sub":"≈ 72,000 KM/H","y":0.42,"decimals":0,"dial":true}'
r Countdown t24 '{"from":86400,"label":"TIME TO IMPACT","rate":1}'
r Countdown t1 '{"from":3600,"label":"FINAL HOUR","rate":1}'
r Stamp notime '{"text":"NO TIME TO DEFLECT","sub":"LAUNCH WINDOW CLOSED"}'
r Reticle target '{"label":"IMPACT ZONE","value":"UNKNOWN","x":0.42,"y":0.42}'
r Callout dart '{"title":"NASA DART · 2022","sub":"A SPACECRAFT RAMMED AN ASTEROID ON PURPOSE"}'
