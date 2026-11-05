"""Pruefung lt_kugelhahn_feder_d40 (W37-1, leitung_w37.py): Baulaenge und Muffen wie lt_kugelhahn_d40, Ports A/B wie die Bibliothek, Hebel in Ruhelage quer (geschlossen),
Federgehaeuse vorhanden, Eintrag in leitungsteile.json (w37_teile) und descriptions.json vor dem Sammeleintrag ^lt_, Interferenz 0.
Aufruf: python -X utf8 scripts/workshop/check_lt_w37.py   (exit 1 bei FAIL)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w37 as W37
from check_puffer_klein import interference

def main():
    ck = sc.Check("lt_w37")
    path = os.path.join(sc.ROOT, "designs", "components", "lt_kugelhahn_feder_d40.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ext = lambda n, i: (B[n]["bbox"]["min"][i], B[n]["bbox"]["max"][i])
    ref = {b["name"]: b for b in sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "lt_kugelhahn_d40.sc"))["bodies"]}
    ck.eq("Koerper (Kugelhahn, Federgehaeuse, Spindel, Hebel)", len(B), 4)
    z = ext("Kugelhahn", 2)
    ck.eq("Baulaenge = lt_kugelhahn_d40 (50 + 2 x 26)", z[1] - z[0], 50 + 2 * L.DEPTH[40], 0.1)
    ck.eq("Gehaeusevolumen = lt_kugelhahn_d40", B["Kugelhahn"]["volume_mm3"], ref["Kugelhahn"]["volume_mm3"], 1.0)
    hx, hy = ext("Hebel", 0), ext("Hebel", 1)
    hz = ext("Hebel", 2)
    ck.eq("Hebel quer zur Rohrachse (Laenge in Y 110 > Hoehe in Z)", 1 if (hy[1] - hy[0]) > 5 * (hz[1] - hz[0]) else 0, 1)
    ck.eq("Hebel-Laenge in Y", hy[1] - hy[0], W37.FED["hebel_l"], 0.1)
    fx = ext("Federgehaeuse", 0)
    ck.eq("Federgehaeuse Laenge", fx[1] - fx[0], W37.FED["l"], 0.1)
    pa, pb = W37.ports("lt_kugelhahn_feder_d40")
    lib = L.ports("lt_kugelhahn_d40")
    ck.eq("Port A wie Bibliothek (Lage, Richtung, DN)", 1 if (pa[1], pa[2], pa[4]) == (lib[0][1], lib[0][2], lib[0][4]) else 0, 1)
    ck.eq("Port B wie Bibliothek (Lage, Richtung, DN)", 1 if (tuple(map(float, pb[1])), pb[2], pb[4]) == (tuple(map(float, lib[1][1])), lib[1][2], lib[1][4]) else 0, 1)
    lt = json.load(open(os.path.join(sc.ROOT, "data", "components", "leitungsteile.json"), encoding="utf-8"))
    ck.eq("leitungsteile.json w37_teile Eintrag mit 2 Ports", len(lt.get("w37_teile", {}).get("lt_kugelhahn_feder_d40", {}).get("ports", [])), 2)
    ds = json.load(open(os.path.join(sc.ROOT, "data", "descriptions.json"), encoding="utf-8"))["bauteile"]
    first = next(e["match"] for e in ds if re.search(e["match"], "lt_kugelhahn_feder_d40"))
    ck.eq(f"descriptions: erster Treffer ist der eigene Eintrag ({first})", 1 if first == "^lt_kugelhahn_feder_d" else 0, 1)
    ck.eq("Interferenz (Paare)", len(interference(path)), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
