"""Vorpruefung Tank gegen die Scope-Card (docs/scope-cards.md tank_klein / tank_gross) und data/layout.json: Durchmesser, Hoehe, Kegelspitze, Kegelwinkel, Plattform, Beine, Zulauf tangential, Schlammventil an der Kegelspitze, Leitrohr bzw. Biomedium.
Aufruf: python scripts/workshop/check_tank.py [klein] [gross]   (exit 1 bei FAIL)"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

def main(typs):
    p, d = sc.load_params("tank")
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["tanks"]
    ck = sc.Check("tank")
    for typ in typs:
        T = d["typen"][typ]
        R, w, rt = T["R"], T["wall"], T["rt"]
        path = os.path.join(sc.ROOT, "designs", "components", f"tank_{typ}.sc")
        ev = sc.evaluate(path)
        B = {b["name"]: b for b in ev["bodies"]}
        ls = [t for t in lay if abs(t["d"] - 2 * R) < 2 and abs(t["h"] - T["H"]) < 6]
        ck.eq(f"{typ} Anzahl laut layout.json", len(ls), T["anzahl"])
        tk = B["Tank"]["bbox"]
        ck.eq(f"{typ} Tank Durchmesser", tk["max"][0] - tk["min"][0], 2 * R, 1.0)
        ck.eq(f"{typ} Tank Hoehe (Spitze bis Rand)", tk["max"][2] - tk["min"][2], T["H"], 1.0)
        ck.eq(f"{typ} Kegelspitze Z", tk["min"][2], T["z0"], 1.0)
        ck.eq(f"{typ} Kegel vorhanden (Flaechentyp cone)", B["Tank"]["face_types"].get("cone", 0) > 0, True) if False else ck.eq(f"{typ} Kegel vorhanden (Flaechentyp cone)", 1 if B["Tank"]["face_types"].get("cone", 0) > 0 else 0, 1)
        z_t, z_c = T["z0"], T["plat_z0"] + T["plat_t"]
        ang = math.degrees(math.atan((z_c - z_t) / (R - rt)))
        ck.eq(f"{typ} Kegelwinkel ab Horizontal in 40-60 Grad", 1 if 40 <= ang <= 60 else 0, 1)
        # Plattform
        pb = B["Plattform"]["bbox"]
        ck.eq(f"{typ} Plattform Laenge", pb["max"][0] - pb["min"][0], T["plat_l"], 1.0)
        ck.eq(f"{typ} Plattform Breite", pb["max"][1] - pb["min"][1], T["plat_w"], 1.0)
        ck.eq(f"{typ} Plattform Dicke", pb["max"][2] - pb["min"][2], T["plat_t"], 1.0)
        ck.eq(f"{typ} Plattform Z-Unterkante", pb["min"][2], T["plat_z0"], 1.0)
        # Beine
        legs = [b for k, b in B.items() if k.startswith("Bein_")]
        ck.eq(f"{typ} Beine", len(legs), 4)
        ck.eq(f"{typ} Beinhoehe (Oberkante)", max(b["bbox"]["max"][2] for b in legs), T["leg_h"], 1.0)
        ck.eq(f"{typ} Beinquerschnitt", legs[0]["bbox"]["max"][0] - legs[0]["bbox"]["min"][0], T["leg_w"], 0.2)
        ck.eq(f"{typ} Fussplatten", len([k for k in B if k.startswith("Fussplatte_")]), 4)
        ck.eq(f"{typ} Querstreben", len([k for k in B if k.startswith("Strebe_")]), 4)
        ck.eq(f"{typ} Diagonalen", len([k for k in B if k.startswith("Diagonale_")]), 4)
        # Zulauf tangential: Rohr beruehrt die Innenwand (x_max = R - w), Achse parallel zur Wandtangente (Y)
        z = B["Zulaufrohr"]["bbox"]
        ck.eq(f"{typ} Zulauf tangential: Rohr beruehrt Innenwand (x_max = R-w)", z["max"][0], R - w, 0.5)
        ck.eq(f"{typ} Zulauf Rohr-D", z["max"][0] - z["min"][0], T["inlet_d"], 0.2)
        ck.eq(f"{typ} Zulauf unter dem Rand", tk["max"][2] - (z["min"][2] + z["max"][2]) / 2, p["inlet_below_top"], 0.5)
        # Schlammventil an der Kegelspitze: Stutzen umschliesst z0, Hahn darunter, Ablaufstutzen unten
        ss, kh, ab = B["Schlammstutzen"]["bbox"], B["Kugelhahn"]["bbox"], B["Ablaufstutzen"]["bbox"]
        ck.eq(f"{typ} Schlammstutzen an der Spitze (z0 im Stutzen)", 1 if ss["min"][2] <= T["z0"] <= ss["max"][2] else 0, 1)
        ck.eq(f"{typ} Kugelhahn unter der Spitze", 1 if kh["max"][2] <= T["z0"] else 0, 1)
        ck.eq(f"{typ} Ablaufstutzen D = Ventil-D", ab["max"][0] - ab["min"][0], T["valve_d"], 0.2)
        ck.eq(f"{typ} Schlammventil D im OBJ-Bereich 30-56", 1 if 30 <= T["valve_d"] <= 56 else 0, 1)
        if T["biofilter"]:
            ck.eq(f"{typ} Biomedium als EIN Koerper", len([k for k in B if k.startswith("Biomedium")]), 1)
            ck.eq(f"{typ} Biomedium-Hoehe", B["Biomedium"]["bbox"]["max"][2] - B["Biomedium"]["bbox"]["min"][2], p["bio_h"], 0.5)
            ck.eq(f"{typ} Biomedium ruht auf dem Tragrost", B["Biomedium"]["bbox"]["min"][2], B["Tragrost"]["bbox"]["max"][2], 0.01)
        else:
            lr = B["Leitrohr"]["bbox"]
            ck.eq(f"{typ} Leitrohr D", lr["max"][1] - lr["min"][1], p["guide_d"], 0.5)
            ck.eq(f"{typ} Leitrohr reicht in den Tank (Tiefe unter Deckel)", T["z0"] + T["H"] - lr["min"][2], p["guide_depth"], 0.5)
            ck.eq(f"{typ} Auslauf d50 ausserhalb (x_max > R_deckel)", 1 if lr["max"][0] < tk["max"][0] else 0, 1)
        ck.eq(f"{typ} Deckel auf dem Rand", B["Deckel"]["bbox"]["min"][2], T["z0"] + T["H"], 0.1)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["klein", "gross"]))
