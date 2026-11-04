#!/bin/bash
# Rebuild this video's motion layers into motion/: HyperFrames cards (MP4) and Remotion alpha overlays (PNG sequences).
# Needs: cd ../motion && npm ci; npx hyperframes browser ensure. Usage: ./motion.sh [hf|rm]; FORCE=1 re-renders Remotion layers.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
M=$HERE/../motion
O=$HERE/motion
mkdir -p "$O"
CH=$(ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | head -1)
if [ "${1:-hf}" = hf ] || [ -z "$1" ]; then
  cd "$M/hyperframes"
  for c in population lasts radio; do npx hyperframes render . -c $c.html -o "$O/$c.mp4" -q delivery --quiet >/dev/null; done
  T() { npx hyperframes render . -c timeline.html -o "$O/$1.mp4" -q delivery --quiet --variables "$2" >/dev/null; }
  T tl0 '{"stop":0,"from":0,"label":""}'
  T tl8 '{"stop":8,"from":0,"dur":2.6,"label":""}'
  T tl1 '{"stop":1,"label":"+ 1 DAY"}'
  T tl3 '{"stop":3,"label":"+ 1 MONTH"}'
  T tl5 '{"stop":5,"label":"+ 10 YEARS"}'
  T tl7 '{"stop":7,"label":"+ 1,000 YEARS"}'
  V() { npx hyperframes render . -c chapter.html -o "$O/$1.mp4" -q delivery --quiet --variables "$2" >/dev/null; }
  V ch1 '{"label":"+ 1 HOUR","big":"LIGHTS ON","sub":"NOBODY HOME","size":330}'
  V ch2 '{"label":"+ 1 WEEK","big":"MELTDOWN?","sub":"NOBODY WATCHING","size":300}'
  V ch3 '{"label":"+ 1 YEAR","big":"GREEN CRACKS","sub":"NATURE MOVES IN","size":300}'
  V ch4 '{"label":"+ 100 YEARS","big":"CONCRETE JUNGLE","sub":"STEEL FALLS","size":250}'
  V ch5 '{"label":"+ 10,000 YEARS","big":"WHAT REMAINS","sub":"STONE WINS","size":290}'
  V ch6 '{"label":"MILLIONS OF YEARS","big":"OUR LAST TRACE","sub":"ONE THIN LINE","size":270}'
fi
if [ "${1:-rm}" = rm ] || [ -z "$1" ]; then
  cd "$M/remotion"
  r() { [ -d "$O/$2" ] && [ -z "$FORCE" ] && return; rm -rf "$O/$2"; npx remotion render src/index.ts $1 "$O/$2" --sequence --image-format=png \
          --public-dir="$PWD/public" --browser-executable="$CH" --props="$3" --log=error; }
  r TitleSlam title '{"top":"WHAT IF","bottom":"ALL HUMANS DISAPPEARED?"}'
  r TitleSlam ending '{"top":"WHILE WE'"'"'RE","bottom":"STILL HERE"}'
  r BigNumber reactors '{"to":400,"unit":"REACTORS","sub":"WITH NOBODY AT THE CONTROLS","y":0.42,"decimals":0,"dial":true}'
  r BigNumber dogs '{"to":500,"unit":"MILLION","sub":"PET DOGS ON THEIR OWN","y":0.42,"decimals":0,"dial":false}'
  r BigNumber chickens '{"to":20,"unit":"BILLION","sub":"CHICKENS ON FARMS","y":0.42,"decimals":0,"dial":false}'
  r BigNumber cows '{"to":1,"unit":"BILLION","sub":"CATTLE ON FARMS","y":0.42,"decimals":0,"dial":false}'
  r BigNumber granite '{"to":1,"unit":"INCH","sub":"PER 10,000 YEARS (RUSHMORE GRANITE)","y":0.42,"decimals":0,"dial":false}'
  r BigNumber pyramid '{"to":4500,"unit":"YEARS","sub":"THE GREAT PYRAMID SO FAR","y":0.42,"decimals":0,"dial":false}'
  r Countdown hour '{"from":3600,"label":"WITHOUT HUMANS","rate":-1}'
  r Stamp nobody '{"text":"NOBODY HOME","sub":"8 BILLION PEOPLE, GONE"}'
  r Stamp lice '{"text":"EXTINCT","sub":"HUMAN HEAD LICE"}'
  r Stamp notrace '{"text":"PERMANENT","sub":"PLASTIC STAYS"}'
  r Callout chernobyl '{"title":"CHERNOBYL · 1986","sub":"EXCLUSION ZONE, NOW FULL OF WILDLIFE"}'
  r Callout pripyat '{"title":"PRIPYAT · UKRAINE","sub":"ABANDONED SINCE 1986"}'
  r Callout nyc '{"title":"NEW YORK SUBWAY","sub":"PUMPS MILLIONS OF LITRES A DAY"}'
  r Callout rushmore '{"title":"MOUNT RUSHMORE","sub":"CARVED IN GRANITE"}'
  r Callout voyager '{"title":"VOYAGER 1 & 2","sub":"CARRYING THE GOLDEN RECORD"}'
  r Callout anthro '{"title":"THE ANTHROPOCENE","sub":"THE AGE OF HUMANS"}'
  r Callout apollo '{"title":"APOLLO FOOTPRINTS","sub":"NO WIND, NO RAIN"}'
fi
