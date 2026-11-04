"""Pruefung Geblaese-Baugruppe Luft T85 (W37-3 Teil 1): Koerperzahl, Pumpenquader und Masse (10 kg), Fuesse auf Z 0, Stutzen, Schleife (Rohrachse Z 710 ueber Spiegel Z 515 und Pool-Rand Z 650, Volumen nach Pappus),
Rueckschlagventil (Lage, Durchgang), Port Luftaustritt (+X, d20), Port Netzkabel (-Y), Stoss-Kontakt der Rohre, Interferenz 0.
Aufruf: python -X utf8 scripts/workshop/check_geblaese_luft.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import geblaese_luft as G
from check_lt_w39 import interference

NAME = "geblaese_luft"

def main():
    p, d = sc.load_params(NAME)
    g = G.geom(p)
    path = os.path.join(sc.ROOT, "designs", "components", NAME + ".sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check(NAME)
    bb = lambda n, a, k: B[n]["bbox"][k][a]
    ext = lambda n, a: bb(n, a, "max") - bb(n, a, "min")
    ck.eq("Koerperzahl (Pumpe, 4 Fuesse, Kabel, Stutzen, Schleife, Rueckschlagventil, Austrittsrohr)", len(B), 10)
    ck.eq("Pumpe 240 x 180 x 230: X", ext("Pumpe", 0), p["box_x"], 0.1)
    ck.eq("Pumpe Y", ext("Pumpe", 1), p["box_y"], 0.1)
    ck.eq("Pumpe Z", ext("Pumpe", 2), p["box_z"], 0.1)
    ck.eq("Pumpenmasse 10,0 kg (Beispiel Secoh JDK-S-200, Platzhalter)", B["Pumpe"]["mass_g"], p["pump_mass_g"], 100)
    ck.eq("Standflaeche: alle 4 Fuesse unten auf Z 0", sum(1 for i in range(1, 5) if abs(bb(f"Gummifuss_{i}", 2, "min")) < 0.01), 4)
    ck.eq("Fuesse Ø 40 x 15", ext("Gummifuss_1", 0) + ext("Gummifuss_1", 2), p["foot_d"] + p["foot_h"], 0.2)
    ck.eq(f"Pumpe sitzt auf den Fuessen: Unterkante Z {p['foot_h']}", bb("Pumpe", 2, "min"), p["foot_h"], 0.01)
    ck.eq("Stutzen d20 Aussen-Ø", ext("Stutzen_Luft", 0), p["out_d"], 0.1)
    ck.eq(f"Stutzen steht auf dem Gehaeuse: Z {g['z_top']:g}", bb("Stutzen_Luft", 2, "min"), g["z_top"], 0.01)
    ck.eq("Schleife beginnt am Stutzenende (Stoss, Z)", bb("Rohrschleife", 2, "min"), bb("Stutzen_Luft", 2, "max"), 0.01)
    # Schleife: Rohrachse Z 710
    za = p["apex_z"]
    ck.eq(f"Schleife: Oberkante des waagerechten Schenkels = Rohrachse {za} + 10", bb("Rohrschleife", 2, "max"), za + p["out_d"] / 2, 0.05)
    ck.eq(f"Schleife: waagerechtes Ende bei X {p['bend_r'] + p['arm_l']:g}", bb("Rohrschleife", 0, "max"), p["bend_r"] + p["arm_l"], 0.05)
    area = math.pi / 4 * (g["od"] ** 2 - g["idd"] ** 2)
    vs = area * (g["l1"] + math.pi / 2 * p["bend_r"] + p["arm_l"])
    ck.eq("Schleife: Volumen = Ringflaeche x Mittellinie (Pappus, mm3)", B["Rohrschleife"]["volume_mm3"], vs, vs * 0.004)
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))
    prm = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8"))
    wz, rim = lay["pool2"]["water_z"], prm["pool_rim"]["value"]
    ck.eq(f"Rohrachse {za} liegt {za - wz} ueber dem Spiegel Z {wz} (Reserve mindestens 150)", 1 if za - wz >= 150 else 0, 1)
    ck.eq(f"Rohrachse {za} liegt ueber dem Pool-Rand Z {rim} (+ 60 wie Schwimmerventil)", za, rim + 60, 0.01)
    # Rueckschlagventil
    ck.eq(f"Rueckschlagventil: Laenge {g['rsv_L']:g} (50 + 2 x Muffentiefe 16)", ext("Rueckschlagventil", 0), g["rsv_L"], 0.1)
    ck.eq("Rueckschlagventil beginnt am Schleifenende (Stoss, X)", bb("Rueckschlagventil", 0, "min"), bb("Rohrschleife", 0, "max"), 0.01)
    ck.eq("Rueckschlagventil Gehaeuse Ø 39", ext("Rueckschlagventil", 1), g["rsv_ob"], 0.1)
    ck.eq("Austrittsrohr beginnt am Ventilende (Stoss, X)", bb("Rohr_Austritt", 0, "min"), bb("Rueckschlagventil", 0, "max"), 0.01)
    fs = sc.faces(path, "Rueckschlagventil")
    ck.eq("Rueckschlagventil: Durchgang Ø 16,4 (Zylinderflaeche r 8,2)", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - g["idd"] / 2) < 0.01 for f in fs) else 0, 1)
    # Ports
    fa = sc.faces(path, "Rohr_Austritt")
    hit = any(f.get("plane_normal") and f["plane_normal"][0] > 0.999 and math.dist(f["centroid"], (g["x_end"], 0, za)) < 0.6 for f in fa)
    ck.eq(f"Port Luftaustritt d20: Stirnflaeche bei X {g['x_end']:g}, Z {za}, Oeffnung +X", 1 if hit else 0, 1)
    zc = p["foot_h"] + p["box_z"] / 2
    fk = sc.faces(path, "Netzkabel")
    hit = any(f.get("plane_normal") and f["plane_normal"][1] < -0.999 and math.dist(f["centroid"], (p["cable_x"], -p["box_y"] / 2 - p["cable_l"], zc)) < 0.6 for f in fk)
    ck.eq(f"Port Netzkabel: Stirnflaeche bei Y {-p['box_y'] / 2 - p['cable_l']:g}, Richtung -Y", 1 if hit else 0, 1)
    ck.eq("Netzkabel sitzt an der Gehaeuserueckseite (Y)", bb("Netzkabel", 1, "max"), -p["box_y"] / 2, 0.01)
    mn, mx = sc.bbox_all(ev)
    ck.eq(f"Gesamthoehe {mx[2]:.1f} (Rueckschlagventil-Gehaeuse oben)", mx[2], za + g["rsv_ob"] / 2, 0.05)
    bad, res = interference(path)
    ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(bad), 0)
    for i in bad[:5]:
        print("   ", i)
    print(f"INFO Masse gesamt {ev['total']['mass_g']:.0f} g; Leistung 204 W je Pumpe laut Netz-Kabeleintrag (nur Hinweis, Kabelrechnung Orchestrator)")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
