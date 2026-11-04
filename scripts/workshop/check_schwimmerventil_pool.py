"""Pruefung Schwimmerventil Pool T84 (W37-2): Masse (Uebergang, Gehaeuse, Wangen, Arm, Kugel), Port A (Muffe d25, Stirnflaeche), Kugelmitte 20 mm ueber dem Spiegel (Spiegel = Achse - 195 = Z 515 im Einbau), Spiegelhoehe gegen data/layout.json, Interferenz 0.
Aufruf: python -X utf8 scripts/workshop/check_schwimmerventil_pool.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
from check_lt_w39 import interference

NAME = "schwimmerventil_pool"

def main():
    p, d = sc.load_params(NAME)
    path = os.path.join(sc.ROOT, "designs", "components", NAME + ".sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check(NAME)
    bb = lambda n: B[n]["bbox"]
    ck.eq("Koerperzahl (Uebergang, Gehaeuse, 2 Wangen, Hebelarm mit Kugel)", len(B), 5)
    ck.eq("Uebergang: Aussen-Ø = Formstueck d25 (32,25)", bb("Uebergang")["max"][1] - bb("Uebergang")["min"][1], L.od_f(25), 0.1)
    ck.eq("Uebergang: Laenge 40", bb("Uebergang")["max"][0] - bb("Uebergang")["min"][0], 40, 0.1)
    ck.eq("Ventilgehaeuse: Ø 38 x 80", bb("Ventilgehaeuse")["max"][0] - bb("Ventilgehaeuse")["min"][0], 80, 0.1)
    ck.eq("Ventilgehaeuse Ø 38", bb("Ventilgehaeuse")["max"][1] - bb("Ventilgehaeuse")["min"][1], 38, 0.1)
    # Port A: Stirnflaeche der Muffe bei x 0, Normale -X, Mittelpunkt im Ursprung
    fs = sc.faces(path, "Uebergang")
    hit = any(f.get("plane_normal") and f["plane_normal"][0] < -0.999 and math.dist(f["centroid"], (0, 0, 0)) < 0.6 for f in fs)
    ck.eq("Port A Muffe d25: Stirnflaeche im Ursprung, Oeffnung -X", 1 if hit else 0, 1)
    ck.eq("Muffe d25: Zylinderflaeche r 12,5", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - 12.5) < 0.01 for f in fs) else 0, 1)
    # Kugel auf dem Spiegel
    k = B["Hebelarm_mit_Kugel"]
    zk_max, zk_min = k["bbox"]["max"][2], k["bbox"]["min"][2]
    kugel_unten = zk_min
    mitte_z = kugel_unten + p["kugel_d"] / 2
    spiegel_z = -p["ventil_h"]                                      # Spiegel im Bauteil-KS
    ck.eq(f"Kugelmitte {mitte_z:.1f} = Spiegel + 20 (Kugel schwimmt, Ventil geschlossen)", mitte_z, spiegel_z + p["kugel_auf"], 0.5)
    ck.eq(f"Kugel-Unterkante {kugel_unten:.1f} unter dem Spiegel (taucht ein)", 1 if kugel_unten < spiegel_z else 0, 1)
    ck.eq("Kugeldurchmesser 110 (x-Ausdehnung des Koerpers ab Kugelmitte)", (k["bbox"]["max"][0] - (p["hebel_x"] + p["arm_dx"])), p["kugel_d"] / 2, 0.5)
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))
    ck.eq("Parameter water_z = layout.json pool2.water_z (nur gelesen)", p["water_z"], lay["pool2"]["water_z"])
    prm = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8"))
    rim = prm["pool_rim"]["value"]
    ck.eq(f"Rohrachse liegt {p['ventil_h']} ueber dem Spiegel: Rand {rim} - Spiegel {p['water_z']} + 60", p["ventil_h"], rim - p["water_z"] + 60)
    ck.eq("Kugel y-Ausdehnung +-55 (Ø 110)", 1 if abs(k["bbox"]["max"][1] - 55) < 0.2 else 0, 1)
    mn, mx = sc.bbox_all(ev)
    ck.eq(f"Gesamt-Box X {mn[0]:.0f} bis {mx[0]:.0f}", 1 if abs(mn[0]) < 0.1 and mx[0] > 400 else 0, 1)
    bad, res = interference(path)
    ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(bad), 0)
    for i in bad[:5]:
        print("   ", i)
    print(f"INFO Masse gesamt {ev['total']['mass_g']:.0f} g")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
