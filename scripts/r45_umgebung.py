"""R45 Frage 0: Was steht im Umkreis der beiden Absetzer (Tank_klein:1/:2)?

Liest nur scripts/dome-script.json (Bauskript), aendert nichts.
Aufruf: python -X utf8 scripts/r45_umgebung.py [Radius_mm]
"""
import json
import math
import sys
from pathlib import Path

RADIUS = float(sys.argv[1]) if len(sys.argv) > 1 else 1300.0
ROOT = Path(__file__).resolve().parent.parent
cmds = json.loads((ROOT / "scripts" / "dome-script.json").read_text(encoding="utf-8"))["commands"]

pos = {}  # occurrence -> (x, y, z), letzte Bewegung gewinnt
for c in cmds:
    if c.get("command") == "occurrence.move":
        p = c["params"]
        m = p.get("matrix")
        if m and len(m) == 12:
            pos[p["occurrence"]] = (m[3], m[7], m[11])

for ab in ("Tank_klein:1", "Tank_klein:2"):
    ax, ay, az = pos[ab]
    print(f"\n{ab} bei x {ax:.0f} y {ay:.0f} z {az:.0f}  (Abstand Domemitte {math.hypot(ax, ay):.0f} mm)")
    near = []
    for name, (x, y, z) in pos.items():
        if name == ab:
            continue
        d = math.hypot(x - ax, y - ay)
        if d <= RADIUS:
            near.append((d, name, x, y, z))
    for d, name, x, y, z in sorted(near)[:40]:
        print(f"  {d:6.0f} mm  {name:32s} x {x:7.0f} y {y:7.0f} z {z:6.0f}")
    print(f"  ({len(near)} Treffer im Radius {RADIUS:.0f} mm)")
