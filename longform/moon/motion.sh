#!/bin/bash
# Rebuild this video's motion layers into motion/: HyperFrames full-screen cards (MP4) and Remotion alpha overlays
# (PNG sequences, composited by make_long.py's "clip" overlay). Needs: cd ../motion && npm ci; npx hyperframes browser ensure
# Usage: ./motion.sh [hf|rm]   (default: both). Set FORCE=1 to re-render Remotion layers that exist.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
M=$HERE/../motion
O=$HERE/motion
mkdir -p "$O"
CH=$(ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | head -1)
if [ "${1:-hf}" = hf ] || [ -z "$1" ]; then
  cd "$M/hyperframes"
  for c in bary bulge tilt daylength eclipse400; do npx hyperframes render . -c $c.html -o "$O/$c.mp4" -q delivery --quiet >/dev/null; done
  V() { npx hyperframes render . -c chapter.html -o "$O/$1.mp4" -q delivery --quiet --variables "$2" >/dev/null; }
  V ch1 '{"label":"CHAPTER ONE","big":"THE FIRST","sub":"NIGHT","size":330}'
  V ch2 '{"label":"CHAPTER TWO","big":"THE TIDES","sub":"FALL","size":330}'
  V ch3 '{"label":"CHAPTER THREE","big":"LOST CLOCKS","sub":"THE ANIMALS","size":300}'
  V ch4 '{"label":"CHAPTER FOUR","big":"WOBBLING","sub":"SEASONS","size":330}'
  V ch5 '{"label":"CHAPTER FIVE","big":"THE LENGTH","sub":"OF A DAY","size":300}'
  V ch6 '{"label":"CHAPTER SIX","big":"NO MOON","sub":"A DIFFERENT WORLD","size":330}'
fi
if [ "${1:-rm}" = rm ] || [ -z "$1" ]; then
  cd "$M/remotion"
  r() { [ -d "$O/$2" ] && [ -z "$FORCE" ] && return; rm -rf "$O/$2"; npx remotion render src/index.ts $1 "$O/$2" --sequence --image-format=png \
          --public-dir="$PWD/public" --browser-executable="$CH" --props="$3" --log=error; }
  r TitleSlam title '{"top":"WHAT IF","bottom":"THE MOON DISAPPEARED?"}'
  r TitleSlam together '{"top":"HOLDING IT","bottom":"ALL TOGETHER"}'
  r BigNumber x100 '{"to":100,"unit":"× BRIGHTER","sub":"FULL MOON VS STARLIGHT","y":0.42,"decimals":0,"dial":false}'
  r BigNumber m16 '{"to":16,"unit":"METRES","sub":"BAY OF FUNDY TIDAL RANGE","y":0.42,"decimals":0,"dial":true}'
  r BigNumber deg235 '{"to":23.5,"unit":"°","sub":"EARTH TILT TODAY","y":0.42,"decimals":1,"dial":true}'
  r BigNumber yr41k '{"to":41000,"unit":"YEARS","sub":"ONE GENTLE WOBBLE CYCLE","y":0.42,"decimals":0,"dial":false}'
  r BigNumber ms2 '{"to":2,"unit":"MS","sub":"LONGER EVERY CENTURY","y":0.42,"decimals":0,"dial":true}'
  r BigNumber cm38 '{"to":3.8,"unit":"CM / YEAR","sub":"THE MOON IS DRIFTING AWAY","y":0.42,"decimals":1,"dial":true}'
  r BigNumber d370 '{"to":370,"unit":"DAYS","sub":"IN A YEAR, AGE OF DINOSAURS","y":0.42,"decimals":0,"dial":false}'
  r BigNumber myr600 '{"to":600,"unit":"MILLION YEARS","sub":"UNTIL THE LAST TOTAL ECLIPSE","y":0.42,"decimals":0,"dial":false}'
  r BigNumber coral100 '{"to":100,"unit":"+ SPECIES","sub":"SPAWNING IN THE SAME NIGHTS","y":0.42,"decimals":0,"dial":false}'
  r Stamp nospring '{"text":"NO MORE KING TIDES","sub":"ONLY THE SUN IS LEFT"}'
  r Stamp myth '{"text":"MYTH","sub":"THE MOON IS NOT AN ASTEROID SHIELD"}'
  r Stamp noeclipse '{"text":"NO MORE ECLIPSES","sub":"EVER"}'
  r Callout fundy '{"title":"BAY OF FUNDY · CANADA","sub":"THE HIGHEST TIDES ON EARTH"}'
  r Callout rance '{"title":"LA RANCE · FRANCE","sub":"TIDAL POWER SINCE 1966"}'
  r Callout reef '{"title":"GREAT BARRIER REEF","sub":"MASS CORAL SPAWNING AFTER A FULL MOON"}'
  r Callout grunion '{"title":"GRUNION · CALIFORNIA","sub":"SPAWNING ON THE HIGHEST TIDES"}'
  r Callout delaware '{"title":"DELAWARE BAY · USA","sub":"HORSESHOE CRAB SPAWNING"}'
  r Callout beetle '{"title":"DACKE ET AL. · NATURE 2003","sub":"DUNG BEETLES STEER BY MOONLIGHT"}'
  r Callout lions '{"title":"PACKER ET AL. · 2011","sub":"LIONS HUNT BEST ON DARK NIGHTS"}'
  r Callout arctic '{"title":"LAST ET AL. · 2016","sub":"ARCTIC ZOOPLANKTON FOLLOW THE MOON"}'
  r Callout laskar '{"title":"LASKAR ET AL. · NATURE 1993","sub":"A MOONLESS EARTH COULD TIP CHAOTICALLY"}'
  r Callout lissauer '{"title":"LISSAUER ET AL. · 2012","sub":"SMALLER, SLOWER SWINGS"}'
  r Callout meyers '{"title":"MEYERS & MALINVERNO · 2018","sub":"1.4 BILLION YEARS AGO: ~18.5-HOUR DAYS"}'
  r Callout apollo '{"title":"APOLLO 11 · 1969","sub":"LASER MIRRORS STILL USED TODAY"}'
  r Callout theia '{"title":"GIANT IMPACT THEORY","sub":"A MARS-SIZED PLANET HITS THE YOUNG EARTH"}'
  r Reticle tilt45 '{"label":"TILT","value":"45°","x":0.38,"y":0.42}'
fi
