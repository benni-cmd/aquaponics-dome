#!/bin/sh
# Aufruf: scripts/build.sh <stufe> <runde>   (erzeugt designs/dome.sc, renders/round-NN.png)
cd "$(dirname "$0")/.." || exit 1
CLI="/c/Program Files/SolidCraft/solidcraft-cli.exe"
python scripts/components/strebe.py >/dev/null && python scripts/gen_dome.py "$1" scripts/dome-script.json || exit 1
"$CLI" run scripts/dome-script.json --save designs/dome.sc --quiet || exit 1
N=$(printf '%02d' "$2")
"$CLI" snapshot designs/dome.sc --out renders/round-$N.png --width 909 --height 766 \
  --camera '{"target":[0,0,3300],"yaw":0.0,"pitch":0.5,"distance":21500}' --no-grid --no-axes
"$CLI" snapshot designs/dome.sc --out renders/section-$N.png --width 909 --height 600 --camera '{"target":[0,0,1500],"yaw":0.0,"pitch":0.15,"distance":22000}' --section XZ --no-grid --no-axes >/dev/null
