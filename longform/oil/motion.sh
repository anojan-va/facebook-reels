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
  R gauge gauge
  T() { R timeline $1 "{\"set\":\"oil\",\"head\":\"A WORLD WITHOUT OIL\",$2}"; }
  T tl0 '"stop":0,"from":0,"label":""'
  T tlall '"stop":5,"from":0,"dur":3.85,"label":""'
  T tl10 '"stop":5,"label":"+ 10 YEARS"'
  V() { R chapter $1 "$2"; }
  V ch1 '{"label":"+ 1 HOUR","big":"ENGINES OFF","sub":"MAYDAY","size":290}'
  V ch2 '{"label":"+ 1 DAY","big":"STRANDED","sub":"LIGHTS STILL ON","size":320}'
  V ch3 '{"label":"+ 1 WEEK","big":"EMPTY SHELVES","sub":"NO NEW PLASTIC","size":260}'
  V ch4 '{"label":"+ 1 MONTH","big":"HUNGRY FARMS","sub":"WEARING OUT","size":270}'
  V ch5 '{"label":"+ 1 YEAR","big":"1900 MEETS 2050","sub":"THE REBUILD","size":230}'
fi
if [ "${1:-rm}" = rm ] || [ -z "$1" ]; then
  cd "$M/remotion"
  r() { [ -d "$O/$2" ] && [ -z "$FORCE" ] && return; rm -rf "$O/$2"; npx remotion render src/index.ts $1 "$O/$2" --sequence --image-format=png \
          --public-dir="$PWD/public" --browser-executable="$CH" --props="$3" --log=error; }
  r TitleSlam title '{"top":"WHAT IF","bottom":"THE WORLD RAN OUT OF OIL?"}'
  r TitleSlam ending '{"top":"WOULD YOU","bottom":"BE READY?"}'
  r Stamp gone '{"text":"GONE","sub":"EVERY DROP OF OIL"}'
  r BigNumber cars '{"to":1.5,"unit":"BILLION","sub":"VEHICLES ON THE WORLD'"'"'S ROADS","y":0.42,"decimals":1,"dial":false}'
  r BigNumber barrels '{"to":100,"unit":"MILLION","sub":"BARRELS OF OIL USED EVERY DAY","y":0.42,"decimals":0,"dial":true}'
  r BigNumber pools '{"to":6000,"unit":"OLYMPIC POOLS","sub":"OF OIL, EVERY SINGLE DAY","y":0.42,"decimals":0,"dial":false}'
  r Callout gimli '{"title":"AIR CANADA 143 · 1983","sub":"THE GIMLI GLIDER · OUT OF FUEL AT 41,000 FT"}'
  r BigNumber ships '{"to":50000,"unit":"CARGO SHIPS","sub":"SUDDENLY WITHOUT POWER","y":0.42,"decimals":0,"dial":false}'
  r BigNumber elec '{"to":3,"unit":"%","sub":"OF THE WORLD'"'"'S ELECTRICITY COMES FROM OIL","y":0.42,"decimals":0,"dial":false}'
  r BigNumber flights '{"to":100000,"unit":"FLIGHTS","sub":"ON A NORMAL DAY · TODAY: ALMOST NONE","y":0.42,"decimals":0,"dial":false}'
  r Callout spr '{"title":"STRATEGIC PETROLEUM RESERVE","sub":"SALT CAVES UNDER THE US GULF COAST · NOW EMPTY"}'
  r Stamp transport '{"text":"9 IN 10","sub":"OF TRANSPORT ENERGY COMES FROM OIL"}'
  r Stamp rationed '{"text":"RATIONED","sub":"FOOD · FUEL · MEDICINE"}'
  r Stamp noplastic '{"text":"NO NEW PLASTIC","sub":"PLASTIC IS MADE FROM OIL AND GAS"}'
  r BigNumber sea '{"to":80,"unit":"%","sub":"OF WORLD TRADE MOVES BY SEA","y":0.42,"decimals":0,"dial":false}'
  r Stamp polyester '{"text":"50%+","sub":"OF CLOTHING FIBRES ARE POLYESTER"}'
  r Callout drake '{"title":"PENNSYLVANIA · 1859","sub":"THE FIRST COMMERCIAL OIL WELL"}'
  r Callout brazil '{"title":"BRAZIL","sub":"MILLIONS OF CARS RUN ON SUGARCANE ETHANOL"}'
  r Callout synfuel '{"title":"COAL TO LIQUID FUEL","sub":"GERMANY IN WWII · SOUTH AFRICA TODAY"}'
fi
