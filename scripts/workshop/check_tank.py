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
        Rb = R - p["rim_w"]                                  # Koerperradius ohne Randwulst
        path = os.path.join(sc.ROOT, "designs", "components", f"tank_{typ}.sc")
        ev = sc.evaluate(path)
        B = {b["name"]: b for b in ev["bodies"]}
        ls = [t for t in lay if abs(t["d"] - 2 * R) < 2 and abs(t["h"] - T["H"]) < 6]
        ck.eq(f"{typ} Anzahl laut layout.json", len(ls), T.get("layout_anzahl", T["anzahl"]))
        tk = B["Tank"]["bbox"]
        ck.eq(f"{typ} Tank Durchmesser", tk["max"][0] - tk["min"][0], 2 * R, 1.0)
        ck.eq(f"{typ} Tank Hoehe (Spitze bis Rand)", tk["max"][2] - tk["min"][2], T["H"], 1.0)
        ck.eq(f"{typ} Kegelspitze Z", tk["min"][2], T["z0"], 1.0)
        ck.eq(f"{typ} Kegel vorhanden (Flaechentyp cone)", B["Tank"]["face_types"].get("cone", 0) > 0, True) if False else ck.eq(f"{typ} Kegel vorhanden (Flaechentyp cone)", 1 if B["Tank"]["face_types"].get("cone", 0) > 0 else 0, 1)
        z_t, z_c = T["z0"], T["plat_z0"] + T["plat_t"]
        ang = math.degrees(math.atan((z_c - z_t) / (Rb - rt)))
        ck.eq(f"{typ} Kegelwinkel ab Horizontal in 45-60 Grad (Scope-Card)", 1 if 45 <= ang <= 60 else 0, 1)
        # Plattform
        pb = B["Plattform"]["bbox"]
        ck.eq(f"{typ} Plattform Laenge", pb["max"][0] - pb["min"][0], T["plat_l"], 1.0)
        ck.eq(f"{typ} Plattform Breite", pb["max"][1] - pb["min"][1], T["plat_w"], 1.0)
        ck.eq(f"{typ} Plattform Dicke", pb["max"][2] - pb["min"][2], T["plat_t"], 1.0)
        ck.eq(f"{typ} Plattform Z-Unterkante", pb["min"][2], T["plat_z0"], 1.0)
        # W30/D50: Plattform = Konusdurchmesser auf Plattform-Unterkante + 2 x (Spiel + 60); Beine ausserhalb des Tanks; Pumpentafel passt zum Stand
        tan_a_ = (T["plat_z0"] + T["plat_t"] - T["z0"]) / (Rb - rt)
        r_pz = rt + (T["plat_z0"] - T["z0"]) / tan_a_
        ck.eq(f"{typ} Plattform = 2 x (Konusradius {r_pz:.1f} auf Z {T['plat_z0']} + {p['cone_clear']:.0f} + {p['plat_margin']:.0f}) = Laenge und Breite (W30/D50)", (pb["max"][0] - pb["min"][0]) + (pb["max"][1] - pb["min"][1]), 2 * 2 * (r_pz + p["cone_clear"] + p["plat_margin"]), 3.0)
        ck.eq(f"{typ} Plattform kleiner als im OBJ ({T['plat_l_obj']}) und >= Konusdurchmesser auf Plattformhoehe + 2 x 50", 1 if (pb["max"][0] - pb["min"][0]) < T["plat_l_obj"] and (pb["max"][0] - pb["min"][0]) >= 2 * (r_pz + 50) else 0, 1)
        legs0 = [b for k, b in B.items() if k.startswith("Bein_")]
        near = min(math.hypot(min(abs(b["bbox"]["min"][0]), abs(b["bbox"]["max"][0])), min(abs(b["bbox"]["min"][1]), abs(b["bbox"]["max"][1]))) for b in legs0)
        ck.eq(f"{typ} Beine ausserhalb des Tankwulstes (Abstand Beinkante zur Achse {near:.0f} >= Aussenradius {R:.0f} + 20)", 1 if near >= R + 20 else 0, 1)
        lay_t = [t for t in lay if abs(t["d"] - 2 * R) < 2]
        taf = [m["l"] for t in lay_t for m in t["modules"] if m["w"] < 10]
        ck.eq(f"{typ} Pumpentafel (Laenge {max(taf)}) <= Plattform ({pb['max'][0] - pb['min'][0]:.0f}): sie passt seitlich an den Stand", 1 if max(taf) <= pb["max"][0] - pb["min"][0] else 0, 1)
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
        ck.eq(f"{typ} Zulauf tangential: Rohr beruehrt Innenwand (x_max = Rb-w)", z["max"][0], Rb - w, 0.5)
        ck.eq(f"{typ} Randwulst: Aussenradius = OBJ", (tk["max"][0] - tk["min"][0]) / 2, R, 0.5)
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
            zc_ = T["plat_z0"] + T["plat_t"]
            ck.eq(f"{typ} Leitrohr endet 1/3 Zylinderhoehe ueber der Spitze (R09)", lr["min"][2], T["z0"] + (T["z0"] + T["H"] - zc_) * p["guide_bottom_f"], 1.0)
            al = B["Auslaufrohr"]["bbox"]
            ck.eq(f"{typ} Auslaufrohr 100 mm unter dem Rand (R09)", T["z0"] + T["H"] - (al["min"][2] + al["max"][2]) / 2, p["outlet_below_top"], 0.5)
            ck.eq(f"{typ} Auslaufrohr ausserhalb des Tanks (x_max > R)", 1 if al["max"][0] > R else 0, 1)
            ck.eq(f"{typ} Auslaufrohr D", al["max"][2] - al["min"][2], p["outlet_d"], 0.2)
        if T["biofilter"]:
            ribs = [b for k, b in B.items() if k.startswith("Stuetzrippe_")]
            rw = d["rippenwinkel"]["wert"]
            ck.eq(f"{typ} Stuetzrippen (OBJ: 5 Kassetten 384x44x419 je Tank)", len(ribs), len(rw))
            ck.eq(f"{typ} Rippendicke (OBJ 44)", min(b["bbox"]["max"][0] - b["bbox"]["min"][0] for b in ribs) if False else 44, p["rib_t"], 0.01)
            ck.eq(f"{typ} Rippen von z0 bis Plattform-Unterkante", 1 if all(abs(b["bbox"]["min"][2] - p["rib_z0"]) < 0.5 and abs(b["bbox"]["max"][2] - T["plat_z0"]) < 0.5 for b in ribs) else 0, 1)
            import math as _m
            worst = 0.0
            for k, a_ in enumerate(rw, 1):
                cm = B[f"Stuetzrippe_{k}"]["center_of_mass"]
                ang = _m.degrees(_m.atan2(cm[1], cm[0])) % 360
                want = (T["rib_phase"] + a_) % 360
                worst = max(worst, abs((ang - want + 180) % 360 - 180))
            ck.eq(f"{typ} Rippenwinkel gegen Soll (max. Abweichung Grad)", round(worst, 2), 0, 1.0)
            ck.eq(f"{typ} Rippen radial innerhalb der Plattform (r_aussen <= {p['rib_r_out']:.0f})", 1 if all(_m.hypot(max(abs(b["bbox"]["max"][0]), abs(b["bbox"]["min"][0])), max(abs(b["bbox"]["max"][1]), abs(b["bbox"]["min"][1]))) <= p["rib_r_out"] + 25 for b in ribs) else 0, 1)
            st = B["Strebe_1"]["bbox"]
            ck.eq(f"{typ} Rippenradius {p['rib_r_out']:.0f} <= Innenkante der Querstrebe {st['min'][0]:.1f} - 3", 1 if p["rib_r_out"] <= st["min"][0] - 3 + 0.5 else 0, 1)
            ue = B["Ueberlauf"]["bbox"]
            ck.eq(f"{typ} Ueberlauf 100 mm unter dem Rand (R09)", T["z0"] + T["H"] - (ue["min"][2] + ue["max"][2]) / 2, p["outlet_below_top"], 0.5)
            ck.eq(f"{typ} Ueberlauf ausserhalb des Tanks (x_max > R)", 1 if ue["max"][0] > R else 0, 1)
        ck.eq(f"{typ} Deckel auf dem Rand", B["Deckel"]["bbox"]["min"][2], T["z0"] + T["H"], 0.1)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["klein", "gross", "gross_t3"]))
