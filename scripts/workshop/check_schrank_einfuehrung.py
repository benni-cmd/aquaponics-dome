"""Pruefung Schrank-Einfuehrung T89 (W37-3 Teil 4): Boden 800 x 500 x 3 gegen data/params.json (cab_x, cab_y), beide Einfuehrungen (DN100, DN50) mit Loch im Boden, Dichtung unter und Mutter ueber dem Boden,
Achsabstand und freier Abstand (EMV mindestens 200 mm), Leerrohr-Enden (Stoss an der Muffe), Ports (Muffe A der Leerrohr-Boegen, Kabelausgang nach oben), Interferenz 0 inklusive Schrankwand.
Aufruf: python -X utf8 scripts/workshop/check_schrank_einfuehrung.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import schrank_einfuehrung as S
from check_lt_w39 import interference

NAME = "schrank_einfuehrung"

def main():
    p, d = sc.load_params(NAME)
    g = S.geom(p)
    path = os.path.join(sc.ROOT, "designs", "components", NAME + ".sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check(NAME)
    ext = lambda n, a: B[n]["bbox"]["max"][a] - B[n]["bbox"]["min"][a]
    prm = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8"))
    ck.eq("Koerperzahl (Boden, Wandstummel, 2 x (Einfuehrung, Dichtung, Mutter), 2 Leerrohr-Boegen)", len(B), 10)
    ck.eq(f"Boden-Breite {p['cab_x']} = params.json cab_x", ext("Schrankboden", 0), prm["cab_x"]["value"], 0.01)
    ck.eq(f"Boden-Tiefe {p['cab_y']} = params.json cab_y", ext("Schrankboden", 1), prm["cab_y"]["value"], 0.01)
    ck.eq("Boden Blech 3 mm", ext("Schrankboden", 2), p["boden_t"], 0.01)
    ck.eq("Boden-Unterkante liegt auf Z 0", B["Schrankboden"]["bbox"]["min"][2], 0, 0.01)
    fs = sc.faces(path, "Schrankboden")
    for dn in (100, 50):
        q = g[dn]
        hit = any(f.get("cylinder") and abs(f["cylinder"]["radius"] - q["hals"] / 2) < 0.01 and abs(f["cylinder"]["origin"][0] - q["cx"]) < 0.6 for f in fs)
        ck.eq(f"Boden: Loch DN{dn} Ø {q['hals']:g} bei X {q['cx']:g}", 1 if hit else 0, 1)
    ke = {100: ("Koerper", "Dichtung", "Gegenmutter"), 50: ("Koerper (2)", "Dichtung (2)", "Gegenmutter (2)")}
    for dn in (100, 50):
        q = g[dn]; k = q["kab"]; kn, dnm, mn = ke[dn]
        ck.eq(f"Einfuehrung DN{dn}: Kragen Ø {k['kragen']:g}", ext(kn, 0), k["kragen"], 0.05)
        ck.eq(f"Einfuehrung DN{dn}: Achse bei X {q['cx']:g}", (B[kn]["bbox"]["max"][0] + B[kn]["bbox"]["min"][0]) / 2, q["cx"], 0.05)
        ck.eq(f"Einfuehrung DN{dn}: Dichtung liegt unter dem Boden (Oberkante Z 0)", B[dnm]["bbox"]["max"][2], 0, 0.05)
        ck.eq(f"Einfuehrung DN{dn}: Gegenmutter liegt auf dem Boden (Unterkante Z {p['boden_t']:g})", B[mn]["bbox"]["min"][2], p["boden_t"], 0.05)
        ck.eq(f"Einfuehrung DN{dn}: Hoehe ueber dem Boden = Gewindehals {k['z_top'] - k['z_d1']:g}", B[kn]["bbox"]["max"][2], k["z_top"] - k["z_d1"], 0.05)
        ck.eq(f"Einfuehrung DN{dn}: Muffe unter dem Boden bis Z {-k['z_d1']:g}", B[kn]["bbox"]["min"][2], -k["z_d1"], 0.05)
    ck.eq(f"Achsabstand {abs(p['x_dn50'] - p['x_dn100']):g} mm (mindestens {p['emv_min']:g} EMV)", 1 if abs(p["x_dn50"] - p["x_dn100"]) >= p["emv_min"] else 0, 1)
    free = abs(p["x_dn50"] - p["x_dn100"]) - 61.5 - 28.0
    ck.eq(f"freier Abstand der Muffen am Boden {free:g} mm (mindestens {p['emv_min']:g})", 1 if free >= p["emv_min"] else 0, 1)
    gap = B["Leerrohrbogen (2)"]["bbox"]["min"][0] - B["Leerrohrbogen"]["bbox"]["max"][0]
    ck.eq(f"kleinster X-Abstand der Leerrohr-Boegen {gap:g} mm (mindestens {p['emv_min']:g}; die Boegen laufen auseinander)", 1 if gap >= p["emv_min"] else 0, 1)
    # Leerrohr-Boegen: Ende B stoesst an die Muffe der Einfuehrung, Muffe A offen
    lb = {100: "Leerrohrbogen", 50: "Leerrohrbogen (2)"}
    for dn in (100, 50):
        q = g[dn]; nm = lb[dn]
        ck.eq(f"Leerrohr-Bogen DN{dn}: Ende B stoesst an die Muffe (Oberkante Z {q['z_muffe_top']:g})", B[nm]["bbox"]["max"][2], q["z_muffe_top"], 0.05)
        fb = sc.faces(path, nm)
        dirx = q["sign"]
        hit = any(f.get("plane_normal") and f["plane_normal"][0] * dirx > 0.999 and math.dist(f["centroid"], (q["a_x"], q["cy"], q["a_z"])) < 0.8 for f in fb)
        ck.eq(f"Port Leerrohr DN{dn} (Muffe A, {'-X' if dirx < 0 else '+X'}): Stirnflaeche bei X {q['a_x']:g}, Z {q['a_z']:g}", 1 if hit else 0, 1)
        fk = sc.faces(path, ke[dn][0])
        top = q["kab"]["z_top"] - q["kab"]["z_d1"]
        hit = any(f.get("plane_normal") and f["plane_normal"][2] > 0.999 and abs(f["centroid"][2] - top) < 0.1 and abs(f["centroid"][0] - q["cx"]) < 0.6 for f in fk)
        ck.eq(f"Port Kabel DN{dn} nach oben in den Schrank: Stirnflaeche bei Z {top:g}", 1 if hit else 0, 1)
    ck.eq(f"Leerrohr DN50 unterflur: tiefster Punkt {B[lb[50]]['bbox']['min'][2]:.0f} (Plan Z -100 bis -400)", 1 if -400 <= B[lb[50]]["bbox"]["min"][2] <= -100 else 0, 1)
    print(f"INFO Leerrohr DN100 tiefster Punkt Z {B[lb[100]]['bbox']['min'][2]:.1f} (Biegeradius 500): tiefer als die Plantiefe -400 (offen, Hinweis im Blatt)")
    bad, res = interference(path)
    ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(bad), 0)
    for i in bad[:5]:
        print("   ", i)
    print(f"INFO Masse gesamt {ev['total']['mass_g']:.0f} g")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
