"""Huelle-Folie T42 (W27 Schritt 2, D39, R24): EIN Bauteil je Dreiecksform (AAB, BBB, BBB_tuer) als huelle_folie_<typ>.sc: zwei duenne transparente Folienlagen (PE 150 Mikrometer) im Abstand layer_gap (Luftpolster [A]),
je Lage das Strebendreieck um overlap/2 nach aussen vergroessert (Ueberstand ueber die Strebenachse, ziegelartige Ueberlappung mit dem Nachbarfeld), Lage 1 bei foil_z0 ueber der Strebenebene.
Bezug wie haut_paneel: Inkreismittelpunkt des Strebendreiecks im Ursprung, Z = Aussennormale, Z 0 = Ebene der Strebenachsen, Kante P0P1 (Basiskante beim Tuerfeld) parallel X.
Tuerfeld: Planenausschnitt = Zargen-Aussenmass minus door_overlap je Seite/oben (Folie liegt auf dem Aufsatzrahmen der Zarge), reicht nach unten durch den Ueberstand.
Aufruf: python scripts/workshop/huelle_folie.py [typ ...] [--render]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
from haut_paneel import tri_points

def build(typ):
    tuer = typ.endswith("_tuer")
    base = typ[:-5] if tuer else typ
    p, d = sc.load_params("huelle_folie")
    hp = json.load(open(os.path.join(sc.ROOT, "data", "components", "haut_paneel.json"), encoding="utf-8"))["typen"][base]
    kanten = hp["kanten_nominal"]
    strebe, _, r = tri_points(kanten, 0.0)
    oh = p["overlap"] / 2
    k = (r + oh) / r                                    # Inkreis-Aufmass: jede Kante wandert um oh nach aussen
    pts = [[round(x * k, 3), round(y * k, 3)] for x, y in strebe]
    b = sc.Build()
    unit = {kk: v["einheit"] for kk, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    b.add("material.create", name="PE Folie", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"])
    root = f"T42_Huelle_Folie_{typ}"
    b.add("component.create", name=root, grounded=True)
    for nm, z in (("Folie_innen", p["foil_z0"]), ("Folie_aussen", p["foil_z0"] + p["layer_gap"])):
        b.add("sketch.create", plane={"origin": [0, 0, z], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_" + nm)
        b.add("sketch.line", points=pts, closed=True)
        b.add("sketch.finish")
        b.add("solid.extrude", distance="foil_t", operation="new", name="E_" + nm, body_name=nm)
        b.add("material.assign", bodies=[nm], material="PE Folie")
        b.add("appearance.assign", bodies=[nm], color=d["werkstoff"]["farbe"], opacity=p["opacity"])
    if tuer:
        G = json.load(open(os.path.join(sc.ROOT, "data", "components", "tuer_komplett.json"), encoding="utf-8"))["geometrie"]
        yb = strebe[0][1]                                # Basiskante im Folien-KS
        hw = G["zarge_aussen_w"] / 2 - p["door_overlap"]
        b.add("sketch.create", plane={"origin": [0, 0, p["foil_z0"] - 1], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_Planenausschnitt")
        b.add("sketch.rectangle.two_point", p0=[-hw, round(yb - oh - 1, 3)], p1=[hw, round(yb + G["zarge_hoehe"] - p["door_overlap"], 3)])
        b.add("sketch.finish")
        b.add("solid.extrude", distance=p["layer_gap"] + p["foil_t"] + 2, operation="cut", targets=["Folie_innen", "Folie_aussen"], name="E_Planenausschnitt")
    b.add("component.metadata.set", component=root, part_number="T42", description=d["beschreibung"] + f" (Typ {typ})", revision="A", properties={"Werkstoff": d["werkstoff"]["name"], "Typ": typ})
    return b, pts, r

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["AAB", "BBB", "BBB_tuer"]
    for typ in typs:
        b, pts, r = build(typ)
        out = os.path.join(sc.ROOT, "designs", "components", f"huelle_folie_{typ}.sc")
        sc.run(b.write(f"huelle_folie_{typ}"), out)
        ev = sc.evaluate(out)
        print(typ, "Koerper", len(ev["bodies"]), "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 3), "kg", "Inkreisradius", round(r, 1))
        if "--render" in sys.argv:
            rd = os.path.join(sc.ROOT, "renders", "components", "huelle_folie")
            os.makedirs(rd, exist_ok=True)
            sc.snapshot(out, os.path.join(rd, f"huelle_folie_{typ}-01-draufsicht.png"), [0, 0, 60], 0.0, 1.5707, 6200, w=1000, h=800)
            sc.snapshot(out, os.path.join(rd, f"huelle_folie_{typ}-02-iso.png"), [0, 0, 100], 0.7, 0.5, 7000, w=1000, h=700)
