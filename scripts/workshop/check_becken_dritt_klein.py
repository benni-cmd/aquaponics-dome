"""Pruefung Drittbecken klein T14k (W34, R37 Befund 10): Durchmesser, Ring, Hoehe, Wassertiefe, Nennvolumen 0,4 m3, Grundflaeche 0,66 m2, Rand ueber dem Wasserspiegel, Interferenz 0.
Erwartungen aus den Quellen (R37: 0,4 m3 = Ø 0,8 x 0,8 m, Grundflaeche 0,66 m2 mit 60-mm-Ring; Rand 650 - Wasserspiegel 515 = 135), nicht aus dem Generator.
W37-2 Teil 3: vier Stutzen (K41 d20, K42 d25, K43 d25 Muffen; K49 Schlauchtuelle ID16) als eigene Koerper, Wanne unveraendert (Volumen), Ports an den Stirnflaechen, Interferenz 0.
Aufruf: python scripts/workshop/check_becken_dritt_klein.py   (exit 1 bei FAIL)"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
from check_lt_w39 import interference
import becken_dritt_klein as gen
import leitung as L

def main():
    p, d = sc.load_params("becken_dritt_klein")
    path = os.path.join(sc.ROOT, "designs", "components", "becken_dritt_klein.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check("becken_dritt_klein")
    ck.eq("Koerper (Wanne, Wasser, 4 Stutzen)", len(B), 6)
    w, wa = B["T14k_Wanne"], B["Wasser"]
    dia = lambda b: b["bbox"]["max"][0] - b["bbox"]["min"][0]
    ck.eq("Aussendurchmesser = 800 + 2 x 60 = 920", dia(w), 920, 0.5)
    ck.eq("Gesamthoehe 1055 (Boden 120 + Wasser 800 + Rand 135)", w["bbox"]["max"][2] - w["bbox"]["min"][2], 1055, 0.2)
    ck.eq("Unterkante Z 0", w["bbox"]["min"][2], 0, 0.1)
    ck.eq("Wasserspiegel (Oberkante Wasserkoerper) Z 920", wa["bbox"]["max"][2], 920, 0.2)
    ck.eq("Rand ueber dem Wasserspiegel 135 (Rand Z 650 - Wasserspiegel Z 515)", w["bbox"]["max"][2] - wa["bbox"]["max"][2], 650 - 515, 0.2)
    ck.eq("Wassertiefe 800 (Wasserkoerper)", wa["bbox"]["max"][2] - wa["bbox"]["min"][2], 800, 0.2)
    ck.eq("Boden 120 (Wasserunterkante)", wa["bbox"]["min"][2], 120, 0.2)
    r_o = dia(w) / 2
    hohl = (math.pi * r_o ** 2 * (w["bbox"]["max"][2] - w["bbox"]["min"][2]) - w["volume_mm3"]) / 1e6          # Hohlraum ab Boden bis zum Rand
    nenn = hohl * 800 / (1055 - 120)                                                                           # bis zum Wasserspiegel (zylindrisch)
    ck.eq(f"Nennvolumen bis Wasserspiegel {nenn:.0f} l = 0,4 m3 (R37 Befund 10)", nenn, 400, 5)
    ck.eq(f"Wasserkoerper {wa['volume_mm3'] / 1e6:.0f} l (Ø 790 x 800, 5 mm Luft zur Wand) zwischen 380 und 402", 1 if 380 <= wa["volume_mm3"] / 1e6 <= 402 else 0, 1)
    ck.eq(f"Grundflaeche mit Ring {math.pi * r_o ** 2 / 1e6:.2f} m2 = 0,66 (R37: 0,66 m2)", math.pi * r_o ** 2 / 1e6, 0.66, 0.01)
    ck.eq("Wandstaerke Ring 60 (Hohlraum 800 gegen aussen 920): Wasser-Luft 5 mm je Seite", (800 - dia(wa)) / 2, 5, 0.2)
    # --- W37-2 Teil 3: Wanne unveraendert, Stutzen
    ck.eq(f"Wanne unveraendert: Volumen {w['volume_mm3'] / 1e3:.1f} cm3 = Bestand 231314,5 cm3 (Blatt W34)", w["volume_mm3"] / 1e3, 231314.5, 1.0)
    z0 = 1055 + p["stutzen_h"] / 2
    for nm, port_pos, dr, art, dn in gen.stutzen_ports(p):
        sb = B["Stutzen_" + nm]
        ck.eq(f"Stutzen {nm}: Unterkante auf der Rand-Oberkante Z 1055", sb["bbox"]["min"][2], 1055, 0.1)
        ck.eq(f"Stutzen {nm}: Oberkante Z 1115 (Block 60 hoch)", sb["bbox"]["max"][2], 1115, 0.1)
        ck.eq(f"Stutzen {nm}: Achse Z {z0:g}", port_pos[2], z0, 0.01)
        ck.eq(f"Stutzen {nm}: Aussenende {math.hypot(port_pos[0], port_pos[1]):.0f} = Ring-Aussenradius 460 + 70", math.hypot(port_pos[0], port_pos[1]), 530, 0.01)
        fs = sc.faces(path, "Stutzen_" + nm)
        hit = any(f.get("plane_normal") and sum(f["plane_normal"][i] * dr[i] for i in range(3)) > 0.999 and math.dist(f["centroid"], port_pos) < 0.6 for f in fs)
        ck.eq(f"Port {nm} ({art}, {dn}) Stirnflaeche an {tuple(round(v, 1) for v in port_pos)}", 1 if hit else 0, 1)
        dd = int(dn[1:]) if art == "Muffe" else 16
        ck.eq(f"Stutzen {nm}: Bohrung Ø {dd} (Zylinderflaeche r {dd / 2:g})", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - dd / 2) < 0.01 for f in fs) else 0, 1)
    nm_d = {nm: dn for nm, _, _, _, dn in gen.stutzen_ports(p)}
    ck.eq("Ports: K41 d20, K42 d25, K43 d25, K49 ID16", 1 if nm_d == {"K41": "d20", "K42": "d25", "K43": "d25", "K49": "ID16"} else 0, 1)
    mn_all = min(b["bbox"]["min"][2] for b in ev["bodies"]); mx_all = max(b["bbox"]["max"][2] for b in ev["bodies"])
    ck.eq("Gesamtbox Z 0 bis 1115 (Bestand 1055 plus Stutzenbloecke)", 1 if abs(mn_all) < 0.1 and abs(mx_all - 1115) < 0.1 else 0, 1)
    inter, _ = interference(path)
    ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(inter), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
