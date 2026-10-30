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
  for c in weight sol delay year olympus; do npx hyperframes render . -c $c.html -o "$O/$c.mp4" -q delivery --quiet >/dev/null; done
  V() { npx hyperframes render . -c chapter.html -o "$O/$1.mp4" -q delivery --quiet --variables "$2" >/dev/null; }
  V ch1 '{"label":"DAY 0","big":"LAUNCH","sub":"7 MONTHS TO GO","size":330}'
  V ch2 '{"label":"DAY 1","big":"WELCOME","sub":"TO MARS","size":330}'
  V ch3 '{"label":"WEEK 1","big":"NEW HOME","sub":"TINY & EXPENSIVE","size":320}'
  V ch4 '{"label":"MONTH 3","big":"NEW NORMAL","sub":"THE WEIRD PART","size":280}'
  V ch5 '{"label":"MONTH 7","big":"LONELY","sub":"PARTY ANYWAY","size":330}'
  V ch6 '{"label":"MONTH 10","big":"ROAD TRIP","sub":"BIGGEST VOLCANO","size":300}'
  V ch7 '{"label":"DAY 365","big":"GOING HOME?","sub":"READ THE FINE PRINT","size":260}'
fi
if [ "${1:-rm}" = rm ] || [ -z "$1" ]; then
  cd "$M/remotion"
  r() { [ -d "$O/$2" ] && [ -z "$FORCE" ] && return; rm -rf "$O/$2"; npx remotion render src/index.ts $1 "$O/$2" --sequence --image-format=png \
          --public-dir="$PWD/public" --browser-executable="$CH" --props="$3" --log=error; }
  r TitleSlam title '{"top":"WHAT IF","bottom":"YOU LIVED ON MARS FOR A YEAR?"}'
  r TitleSlam classic '{"top":"CLASSIC","bottom":"YOU."}'
  r TitleSlam readit '{"top":"READ THE","bottom":"TERMS AND CONDITIONS"}'
  r BigNumber months7 '{"to":7,"unit":"MONTHS","sub":"TO GET THERE","y":0.42,"decimals":0,"dial":true}'
  r BigNumber g38 '{"to":38,"unit":"%","sub":"OF EARTH GRAVITY","y":0.42,"decimals":0,"dial":true}'
  r BigNumber co2 '{"to":95,"unit":"% CO₂","sub":"THE AIR ON MARS","y":0.42,"decimals":0,"dial":true}'
  r BigNumber pressure '{"to":1,"unit":"%","sub":"LESS THAN 1% OF EARTH AIR PRESSURE","y":0.42,"decimals":0,"dial":false}'
  r BigNumber sec15 '{"to":15,"unit":"SECONDS","sub":"WITHOUT YOUR HELMET","y":0.42,"decimals":0,"dial":true}'
  r BigNumber minus60 '{"to":-60,"unit":"°C","sub":"AVERAGE TEMPERATURE","y":0.42,"decimals":0,"dial":false}'
  r BigNumber g122 '{"to":122,"unit":"GRAMS","sub":"OF OXYGEN MADE BY MOXIE","y":0.42,"decimals":0,"dial":false}'
  r BigNumber pct1 '{"to":1,"unit":"% / MONTH","sub":"BONE LOSS WITHOUT EXERCISE (SPACE STATION)","y":0.42,"decimals":0,"dial":false}'
  r BigNumber days520 '{"to":520,"unit":"DAYS","sub":"SEALED IN A FAKE SPACESHIP","y":0.42,"decimals":0,"dial":false}'
  r BigNumber m26 '{"to":26,"unit":"MONTHS","sub":"BETWEEN TRIPS HOME","y":0.42,"decimals":0,"dial":true}'
  r Stamp helmet '{"text":"NEVER TAKE IT OFF","sub":"RULE NUMBER ONE"}'
  r Stamp toxic '{"text":"TOXIC SOIL","sub":"WASH BEFORE FARMING"}'
  r Stamp myth '{"text":"MYTH","sub":"MARS WIND FEELS LIKE A BREEZE"}'
  r Stamp nope '{"text":"NOT SO FAST","sub":"MISSION CONTROL"}'
  r Callout moxie '{"title":"MOXIE · PERSEVERANCE","sub":"NASA, 2021–2023"}'
  r Callout curiosity '{"title":"NASA CURIOSITY","sub":"MEASURED RADIATION ON THE SURFACE"}'
  r Callout opportunity '{"title":"OPPORTUNITY ROVER","sub":"LOST IN THE 2018 GLOBAL DUST STORM"}'
  r Callout mars500 '{"title":"MARS-500 · MOSCOW","sub":"2010–2011"}'
  r Callout moons '{"title":"PHOBOS & DEIMOS","sub":"THE TWO MOONS OF MARS"}'
  r Callout olympus '{"title":"OLYMPUS MONS","sub":"ABOUT AS WIDE AS ARIZONA"}'
  r Reticle sunset '{"label":"SUNSET COLOUR","value":"BLUE","x":0.5,"y":0.4}'
fi
