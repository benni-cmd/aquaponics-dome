#!/bin/sh
# Aufruf: scripts/build.sh <stufe> <runde> [variante]   (Standard a_plus: designs/dome.sc, renders/round-NN.png;
#         ring_b2: designs/dome-ring_b2.sc, renders/ring_b2/round-NN.png; Pfade aus scripts/variante.py, N-VARIANTEN V1b)
cd "$(dirname "$0")/.." || exit 1
CLI="/c/Program Files/SolidCraft/solidcraft-cli.exe"
V="${3:-a_plus}"
P() { python -X utf8 -c "import sys; sys.path.insert(0, 'scripts'); import variante; print(variante.pfad('$1', '$V', root='.').replace(chr(92), '/'))" || exit 1; }
SCRIPT=$(P dome_script) || exit 1; MODELL=$(P modell) || exit 1; BILDER=$(P bilder_dir) || exit 1
mkdir -p "$BILDER"
python scripts/components/strebe.py >/dev/null && python scripts/gen_dome.py "$1" "$SCRIPT" --variante "$V" || exit 1
"$CLI" run "$SCRIPT" --save "$MODELL" --quiet || exit 1
N=$(printf '%02d' "$2")
"$CLI" snapshot "$MODELL" --out "$BILDER/round-$N.png" --width 909 --height 766 \
  --camera '{"target":[0,0,3300],"yaw":0.0,"pitch":0.5,"distance":21500}' --no-grid --no-axes
"$CLI" snapshot "$MODELL" --out "$BILDER/section-$N.png" --width 909 --height 600 --camera '{"target":[0,0,1500],"yaw":0.0,"pitch":0.15,"distance":22000}' --section XZ --no-grid --no-axes >/dev/null
