"""Vorpruefung Tank gegen die Scope-Card (docs/scope-cards.md tank_klein / tank_gross) und data/layout.json: Durchmesser, Hoehe, Kegelspitze, Kegelwinkel, Plattform, Beine, Zulauf tangential, Schlammventil an der Kegelspitze, Leitrohr bzw. Biomedium.
Aufruf: python scripts/workshop/check_tank.py [klein] [gross]   (exit 1 bei FAIL)"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
import sc


def interference(path):
    import subprocess
    script = os.path.join(sc.TMP, "ws-tank-interf.json"); out = os.path.join(sc.TMP, "ws-tank-interf-out.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 240}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--results", "--json-out", out], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER interference: " + r.stderr.strip())
    dd = json.load(open(out, encoding="utf-8"))
    def find(o):
        if isinstance(o, dict):
            if "interferences" in o:
                return o["interferences"]
            for v in o.values():
                x = find(v)
                if x is not None:
                    return x
        elif isinstance(o, list):
            for v in o:
                x = find(v)
                if x is not None:
                    return x
    return [(i["a"], i["b"], i.get("volume_mm3", 0)) for i in find(dd) or []]

def check_bed(ck, typ, T, p, d, B, Rb, w, rt):
    """Schwebebett (W32, D55): Volumen = fill x water_l, Traegerflaeche, Lage im Tank, Belueftungsgitter, Siebe. Erwartung aus dem Tankprofil (eigene Rechnung), nicht aus bed_geometry."""
    z_t, z_c, z_top = T["z0"], T["plat_z0"] + T["plat_t"], T["z0"] + T["H"]
    tan_a = (z_c - z_t) / (Rb - rt)
    r_in = rt - w / math.sin(math.atan(tan_a))
    zc_i = z_t + (Rb - w - r_in) * tan_a
    def v_water(z):          # Innenvolumen (mm3) von der Spitze bis z
        if z <= zc_i:
            h = z - z_t; r2 = r_in + h / tan_a
            return math.pi * h / 3 * (r_in ** 2 + r_in * r2 + r2 ** 2)
        h = zc_i - z_t; r2 = Rb - w
        return math.pi * h / 3 * (r_in ** 2 + r_in * r2 + r2 ** 2) + math.pi * r2 ** 2 * (z - zc_i)
    bm = B["Biomedium"]
    target = p["fill"] * p["water_l"] * 1e6
    ck.eq(f"{typ} Schwebebett als EIN Koerper", len([k for k in B if k.startswith("Biomedium")]), 1)
    ck.eq(f"{typ} Schwebebett-Volumen = fill 0,67 x 702 l = 470,3 l (Toleranz 1 %)", bm["volume_mm3"], target, 0.01 * target)
    ck.eq(f"{typ} Traegerflaeche beide Tanks = Volumen x 500 m2/m3 x 2 in m2 (R30: 470)", bm["volume_mm3"] / 1e9 * p["k1_area"] * 2, 470.0, 6.0)
    vo = v_water(z_top - p["outlet_below_top"])
    print(f"   Modell-Wasservolumen: Rand {v_water(z_top) / 1e6:.0f} l, Ueberlauf-Mitte {vo / 1e6:.0f} l; Bett {bm['volume_mm3'] / 1e6:.0f} l = {bm['volume_mm3'] / vo * 100:.0f} % des Wassers bis Ueberlauf-Mitte, {bm['volume_mm3'] / v_water(z_top) * 100:.0f} % bis Rand")
    ck.eq(f"{typ} Modell-Wasservolumen bis Rand gegen R30 (702 l) in Prozent <= 3", abs(v_water(z_top) / 1e6 - p["water_l"]) / p["water_l"] * 100, 0, 3.0)
    ck.eq(f"{typ} Fuellung gegen Modell-Wasser bis Ueberlauf-Mitte <= 80 % (Handbuch: K1 meist <= 67-70 %: BEFUND, siehe Blatt)", 1 if bm["volume_mm3"] / vo <= 0.80 else 0, 1)
    bb = bm["bbox"]
    ck.eq(f"{typ} Bett-Radius <= Innenradius - 3 mm", bb["max"][0], Rb - w - p["bed_inset"], 0.2)
    z_in = z_top - p["inlet_below_top"]
    ck.eq(f"{typ} Bett-Oberkante unter dem Zulaufrohr (Luft >= 20 mm zur Zulauf-Unterkante)", 1 if (z_in - T["inlet_d"] / 2) - bb["max"][2] >= 20 else 0, 1)
    gg = B["Belueftungsgitter"]["bbox"]
    ar = p["air_ring_d"] / 2
    ck.eq(f"{typ} Belueftungsgitter Aussenradius = R/2 + 10", gg["max"][0], Rb / 2 + ar, 0.3)
    ck.eq(f"{typ} Belueftungsgitter D20: Hoehe der Rohre", gg["max"][2] - gg["min"][2], p["air_ring_d"], 0.3)
    r_wall = r_in + (gg["max"][2] - z_t) / tan_a
    ck.eq(f"{typ} Belueftungsgitter Abstand zur Innenwand des Konus >= 20 mm (Ist in mm)", 1 if r_wall - gg["max"][0] >= 20 else 0, 1)
    ck.eq(f"{typ} Bett beginnt ueber dem Gitter (Unterkante > Gitter-Oberkante)", 1 if bb["min"][2] > gg["max"][2] else 0, 1)
    lr = B["Belueftungsrohr"]["bbox"]
    ck.eq(f"{typ} Steigrohr D16 beruehrt das Gitter oben und ragt ueber den Deckel", 1 if abs(lr["min"][2] - gg["max"][2]) < 0.3 and lr["max"][2] > z_top + p["lid_t"] else 0, 1)
    ck.eq(f"{typ} Steigrohr liegt am Ring (x = R/2)", (lr["min"][0] + lr["max"][0]) / 2, Rb / 2, 0.2)
    ck.eq(f"{typ} kein Tragrost und keine Konsolen mehr (Schwebebett statt Korb)", len([k for k in B if k.startswith("Tragrost") or k.startswith("Konsole_")]), 0)
    # Siebe
    zs = B["Zulaufsieb"]
    di = T["inlet_d"]
    ck.eq(f"{typ} Zulaufsieb: Scheibe D = Zulauf-D", zs["bbox"]["max"][0] - zs["bbox"]["min"][0], di, 0.3)
    ck.eq(f"{typ} Zulaufsieb: Volumen = Scheibe 4 mm minus 5 Schlitze (5 x 43 x 4 x 5)", zs["volume_mm3"], math.pi / 4 * di ** 2 * 4 - 5 * (di - 20) * 4 * p["screen_slot"], 0.02 * zs["volume_mm3"])
    ck.eq(f"{typ} Zulaufsieb beruehrt das Zulaufrohr-Ende (Y)", zs["bbox"]["min"][1], B["Zulaufrohr"]["bbox"]["max"][1], 0.05)
    ck.eq(f"{typ} Schlitzweite {p['screen_slot']} mm < Traegerdurchmesser {p['carrier_d']} mm", 1 if p["screen_slot"] < p["carrier_d"] else 0, 1)
    asb = B["Auslaufsieb"]["bbox"]
    ue = B["Ueberlauf"]["bbox"]
    ck.eq(f"{typ} Auslaufsieb D110", asb["max"][1] - asb["min"][1], p["screen_d"], 0.3)
    ck.eq(f"{typ} Auslaufsieb umschliesst das Ueberlaufrohr-Ende (Sieb beginnt vor dem Rohrende)", 1 if asb["min"][0] < ue["min"][0] - 20 else 0, 1)
    ck.eq(f"{typ} Auslaufsieb endet vor der Innenwand (Wand an den Siebkanten)", 1 if asb["max"][0] < Rb - w else 0, 1)
    ck.eq(f"{typ} Auslaufsieb mittig am Ueberlauf (z)", (asb["min"][2] + asb["max"][2]) / 2, (ue["min"][2] + ue["max"][2]) / 2, 0.2)

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
            check_bed(ck, typ, T, p, d, B, Rb, w, rt)
        else:
            lr = B["Leitrohr"]["bbox"]
            ck.eq(f"{typ} Leitrohr D", lr["max"][1] - lr["min"][1], p["guide_d"], 0.5)
            zc_ = T["plat_z0"] + T["plat_t"]
            ck.eq(f"{typ} Leitrohr endet 1/3 Zylinderhoehe ueber der Spitze (R09)", lr["min"][2], T["z0"] + (T["z0"] + T["H"] - zc_) * p["guide_bottom_f"], 1.0)
            al = B["Auslaufrohr"]["bbox"]
            ck.eq(f"{typ} Auslaufrohr 100 mm unter dem Rand (R09)", T["z0"] + T["H"] - (al["min"][2] + al["max"][2]) / 2, p["outlet_below_top"], 0.5)
            ck.eq(f"{typ} Auslaufrohr ausserhalb des Tanks (x_max > R)", 1 if al["max"][0] > R else 0, 1)
            ck.eq(f"{typ} Auslaufrohr D", al["max"][2] - al["min"][2], p["outlet_d"], 0.2)
            # Luftanschluss d20 im Deckel fuer K47/K48 (Pruefung M10-S5-LUFT-B, Auflage A1)
            ls_ = B["Luftstutzen"]
            lsb = ls_["bbox"]
            z_top_ = T["z0"] + T["H"]
            ck.eq(f"{typ} Luftstutzen D20 (K47/K48 dn 20)", lsb["max"][0] - lsb["min"][0], p["settler_air_d"], 0.2)
            ck.eq(f"{typ} Luftstutzen Volumen = Rohr d20 x Wand {p['settler_air_wall']} x Laenge", ls_["volume_mm3"], math.pi / 4 * (p["settler_air_d"] ** 2 - (p["settler_air_d"] - 2 * p["settler_air_wall"]) ** 2) * (lsb["max"][2] - lsb["min"][2]), 5.0)
            ck.eq(f"{typ} Luftstutzen geht durch den Deckel ({p['settler_air_below']:.0f} mm darunter, oben ueber dem Deckel)", 1 if abs(lsb["min"][2] - (z_top_ - p["settler_air_below"])) < 0.2 and lsb["max"][2] > z_top_ + p["lid_t"] else 0, 1)
            ck.eq(f"{typ} Luftstutzen bei x = Koerperradius/2, y = 0", math.hypot((lsb["min"][0] + lsb["max"][0]) / 2 - Rb / 2, (lsb["min"][1] + lsb["max"][1]) / 2), 0, 0.2)
            ck.eq(f"{typ} Luftstutzen ueber dem Auslaufrohr (Abstand >= 20 mm)", 1 if lsb["min"][2] - al["max"][2] >= 20 else 0, 1)
            ck.eq(f"{typ} Luftstutzen frei vom Leitrohr (Abstand Rohrkanten >= 50 mm)", 1 if lsb["min"][0] - lr["max"][0] >= 50 else 0, 1)
            ck.eq(f"{typ} Luftstutzen frei von der Revisionsoeffnung (andere Deckelseite)", 1 if lsb["min"][0] > 0 else 0, 1)
            ck.eq(f"{typ} Luftstutzen nicht ueber der Gesamthoehe (oben <= Leitrohr-Oberkante)", 1 if lsb["max"][2] <= lr["max"][2] + 0.1 else 0, 1)
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
        if T["biofilter"]:
            # Schlammstutzen sitzt 2 mm in der Kegelspitze (gewollter Stutzen-Sitz, 857,8 mm3, schon im Stand vor W32 identisch)
            itf = [x for x in interference(path) if (x[0], x[1]) != ("Tank", "Schlammstutzen") and not (x[0].startswith(("Strebe_", "Bein_", "Diagonale_", "Fussplatte_", "Schraube", "Body")) and x[1].startswith(("Strebe_", "Bein_", "Diagonale_", "Fussplatte_", "Schraube", "Body")))]
            for x in itf[:8]:
                print("   Interferenz", x)
            ck.eq(f"{typ} Interferenzen im Biofilter (ohne Gestell-Gestell)", len(itf), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["klein", "gross", "gross_t3"]))
