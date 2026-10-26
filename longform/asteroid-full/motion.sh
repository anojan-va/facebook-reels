#!/bin/bash
# Rebuild this video's motion layers into motion/: HyperFrames full-screen cards (MP4) and Remotion alpha overlays
# (PNG sequences, composited by make_long.py's "clip" overlay). Needs: cd ../motion && npm ci; npx hyperframes browser ensure
# Usage: ./motion.sh [hf|rm]   (default: both)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
M=$HERE/../motion
O=$HERE/motion
mkdir -p "$O"
CH=$(ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | head -1)
if [ "${1:-hf}" = hf ] || [ -z "$1" ]; then
  cd "$M/hyperframes"
  for c in size crossing jet crater wave temp pyramid nudge dart; do npx hyperframes render . -c $c.html -o "$O/$c.mp4" -q delivery --quiet >/dev/null; done
  V() { npx hyperframes render . -c chapter.html -o "$O/$1.mp4" -q delivery --quiet --variables "$2" >/dev/null; }
  V ch1 '{"label":"CHAPTER ONE","big":"24 HOURS","sub":"TO IMPACT","size":330}'
  V ch2 '{"label":"CHAPTER TWO","big":"IMPACT","sub":"THE FIRST MINUTES","size":330}'
  V ch3 '{"label":"CHAPTER THREE","big":"THE SKY","sub":"CATCHES FIRE","size":330}'
  V ch4 '{"label":"CHAPTER FOUR","big":"THE LONG","sub":"NIGHT","size":330}'
  V ch5 '{"label":"CHAPTER FIVE","big":"THE WORLD","sub":"IT LEAVES BEHIND","size":300}'
  V ch6 '{"label":"CHAPTER SIX","big":"HOW WE","sub":"STOP IT","size":330}'
fi
if [ "${1:-rm}" = rm ] || [ -z "$1" ]; then
  cd "$M/remotion"
  r() { [ -d "$O/$2" ] && [ -z "$FORCE" ] && return; rm -rf "$O/$2"; npx remotion render src/index.ts $1 "$O/$2" --sequence --image-format=png \
          --public-dir="$PWD/public" --browser-executable="$CH" --props="$3" --log=error; }
  r TitleSlam title '{"top":"WHAT IF","bottom":"AN ASTEROID HIT EARTH?"}'
  r TitleSlam wewill '{"top":"WE WILL.","bottom":""}'
  r BigNumber speed '{"to":20,"unit":"KM/S","sub":"≈ 72,000 KM/H","y":0.42,"decimals":0,"dial":true}'
  r BigNumber alt100 '{"to":100,"unit":"KM UP","sub":"THE EDGE OF SPACE","y":0.42,"decimals":0,"dial":false}'
  r BigNumber sec5 '{"to":5,"unit":"SECONDS","sub":"THROUGH THE WHOLE ATMOSPHERE","y":0.42,"decimals":0,"dial":true}'
  r BigNumber megatons '{"to":100,"unit":"MILLION MEGATONS","sub":"OF ENERGY, IN UNDER A SECOND","y":0.42,"decimals":0,"dial":false}'
  r BigNumber km180 '{"to":180,"unit":"KM WIDE","sub":"THE CRATER THAT SETTLES","y":0.42,"decimals":0,"dial":false}'
  r BigNumber kmh800 '{"to":800,"unit":"KM/H","sub":"A TSUNAMI IN THE DEEP OCEAN","y":0.42,"decimals":0,"dial":true}'
  r BigNumber kms6 '{"to":6,"unit":"KM/S","sub":"DART HITS DIMORPHOS","y":0.42,"decimals":0,"dial":true}'
  r BigNumber pct3 '{"to":3.1,"unit":"%","sub":"PEAK CHANCE OF HITTING EARTH IN 2032","y":0.42,"decimals":1,"dial":true}'
  r BigNumber myr100 '{"to":100,"unit":"MILLION YEARS","sub":"BETWEEN 10 KM IMPACTS, ON AVERAGE","y":0.42,"decimals":0,"dial":false}'
  r Countdown t24 '{"from":86400,"label":"TIME TO IMPACT","rate":1}'
  r Countdown t1 '{"from":3600,"label":"FINAL HOUR","rate":1}'
  r Stamp notime '{"text":"NO TIME TO DEFLECT","sub":"LAUNCH WINDOW CLOSED"}'
  r Stamp noharvest '{"text":"NO HARVEST","sub":"ALMOST ANYWHERE ON EARTH"}'
  r Stamp nothreat '{"text":"NO KNOWN THREAT","sub":"FOR AT LEAST 100 YEARS"}'
  r Stamp ruledout '{"text":"RULED OUT","sub":"WITHIN WEEKS"}'
  r Reticle target '{"label":"IMPACT ZONE","value":"UNKNOWN","x":0.42,"y":0.42}'
  r Reticle city '{"label":"A FEW HUNDRED METRES","value":"ONE CITY","x":0.45,"y":0.42}'
  r Callout dart '{"title":"NASA DART · 2022","sub":"A SPACECRAFT RAMMED AN ASTEROID ON PURPOSE"}'
  r Callout chicx '{"title":"CHICXULUB · MEXICO","sub":"WHERE THE DINOSAUR KILLER HIT"}'
  r Callout hera '{"title":"ESA HERA","sub":"LAUNCHED OCTOBER 2024 · ON ITS WAY"}'
  r Callout yr4 '{"title":"ASTEROID 2024 YR4","sub":"DISCOVERED DECEMBER 2024"}'
  r Callout apophis '{"title":"APOPHIS · 13 APRIL 2029","sub":"PASSES ABOUT 32,000 KM FROM EARTH"}'
  r Callout osiris '{"title":"NASA OSIRIS-APEX","sub":"ON ITS WAY TO MEET APOPHIS"}'
  r Callout vault '{"title":"GLOBAL SEED VAULT","sub":"SVALBARD, NORWAY"}'
  r Callout rubin '{"title":"VERA C. RUBIN OBSERVATORY","sub":"CERRO PACHÓN, CHILE"}'
  r Callout neos '{"title":"NASA NEO SURVEYOR","sub":"PLANNED LAUNCH: 2027"}'
  r Callout drill '{"title":"PLANETARY DEFENSE EXERCISE","sub":"A PRACTICE ASTEROID, FROM WARNING TO EVACUATION"}'
fi
