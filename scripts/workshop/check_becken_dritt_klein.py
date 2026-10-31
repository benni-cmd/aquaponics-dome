"""Pruefung Drittbecken klein T14k (W34, R37 Befund 10): Durchmesser, Ring, Hoehe, Wassertiefe, Nennvolumen 0,4 m3, Grundflaeche 0,66 m2, Rand ueber dem Wasserspiegel, Interferenz 0.
Erwartungen aus den Quellen (R37: 0,4 m3 = Ø 0,8 x 0,8 m, Grundflaeche 0,66 m2 mit 60-mm-Ring; Rand 650 - Wasserspiegel 515 = 135), nicht aus dem Generator.
Aufruf: python scripts/workshop/check_becken_dritt_klein.py   (exit 1 bei FAIL)"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import check_puffer_klein as cp

def main():
    p, d = sc.load_params("becken_dritt_klein")
    path = os.path.join(sc.ROOT, "designs", "components", "becken_dritt_klein.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check("becken_dritt_klein")
    ck.eq("Koerper (Wanne, Wasser)", len(B), 2)
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
    inter = [i for i in cp.interference(path) if i.get("volume_mm3", 0) > 1.0]
    ck.eq("Interferenzen (Volumen > 1 mm3)", len(inter), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
