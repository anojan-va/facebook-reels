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
  R() { npx hyperframes render . -c $1.html -o "$O/$2.mp4" -q delivery --quiet ${3:+--variables "$3"} >/dev/null; }
  R lo lo; R notifs notifs
  R loading loading '{"msg":"NO INTERNET CONNECTION"}'
  R loading loading-6h '{"msg":"SOMETHING WENT WRONG"}'
  T() { R timeline $1 "{\"set\":\"days\",\"head\":\"A WEEK WITHOUT INTERNET\",$2}"; }
  T dweek '"stop":6,"from":0,"dur":2.4,"label":"7 DAYS"'
  T d4 '"stop":3,"label":"DAY 4"'
  T d5 '"stop":4,"label":"DAY 5 · EVENING"'
  T d7 '"stop":6,"label":"DAY 7"'
  V() { R chapter $1 "$2"; }
  V ch1 '{"label":"DAY 1","big":"WITHDRAWAL","sub":"NO SIGNAL","size":300}'
  V ch2 '{"label":"DAY 2","big":"EMPTY SHELVES","sub":"CASH ONLY","size":270}'
  V ch3 '{"label":"DAY 3","big":"LOST","sub":"NO MAPS","size":360}'
  V ch4 '{"label":"DAY 5","big":"WHO BROKE IT?","sub":"FOLLOW THE CABLES","size":200}'
  V ch5 '{"label":"DAY 6","big":"QUIET","sub":"SOMETHING CHANGED","size":340}'
fi
if [ "${1:-rm}" = rm ] || [ -z "$1" ]; then
  cd "$M/remotion"
  r() { [ -d "$O/$2" ] && [ -z "$FORCE" ] && return; rm -rf "$O/$2"; npx remotion render src/index.ts $1 "$O/$2" --sequence --image-format=png \
          --public-dir="$PWD/public" --browser-executable="$CH" --props="$3" --log=error; }
  r TitleSlam title '{"top":"WHAT IF","bottom":"THE INTERNET SHUT DOWN FOR A WEEK?"}'
  r TitleSlam classic '{"top":"CLASSIC","bottom":"INTERNET."}'
  r TitleSlam ending '{"top":"WHAT DO YOU","bottom":"DO FIRST?"}'
  r BigNumber users '{"to":5.5,"unit":"BILLION","sub":"PEOPLE SUDDENLY OFFLINE","y":0.42,"decimals":1,"dial":false}'
  r BigNumber phantom '{"to":89,"unit":"%","sub":"OF STUDENTS FELT PHANTOM VIBRATIONS (DROUIN, 2012)","y":0.42,"decimals":0,"dial":false}'
  r Stamp declined '{"text":"DECLINED","sub":"CARD MACHINE OFFLINE"}'
  r Stamp offline '{"text":"OFFLINE","sub":"CASH MACHINES DOWN"}'
  r Stamp faults '{"text":"150–200","sub":"CABLE FAULTS EVERY YEAR"}'
  r Stamp locked '{"text":"LOCKED OUT","sub":"THE BADGES NEEDED THE NETWORK"}'
  r Reticle gps '{"label":"YOU ARE HERE","value":"GPS: SATELLITES","x":0.5,"y":0.45}'
  r Callout sweden '{"title":"SWEDEN","sub":"MANY SHOPS NO LONGER TAKE CASH"}'
  r Callout crowdstrike '{"title":"JULY 19, 2024","sub":"ONE BAD UPDATE · THOUSANDS OF FLIGHTS GROUNDED"}'
  r Callout nyse '{"title":"NYSE · JULY 8, 2015","sub":"TRADING FROZEN FOR ALMOST 4 HOURS"}'
  r Callout egypt '{"title":"EGYPT · 2011","sub":"INTERNET SWITCHED OFF FOR ABOUT 5 DAYS"}'
  r Callout fb2021 '{"title":"OCTOBER 4, 2021","sub":"FACEBOOK, INSTAGRAM, WHATSAPP · ~6 HOURS DOWN"}'
fi
