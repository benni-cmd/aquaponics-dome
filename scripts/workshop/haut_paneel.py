"""Haut-Paneel T40 (W19 Schritt 2): EIN Paneel je Dreieckstyp (AAB, BBB) als haut_paneel_<typ>.sc: ebenes Dreieck, Dicke panel_t, Rand edge_inset vor der Strebenachse (Dreieck um den Inkreismittelpunkt verkleinert), Material Polycarbonat, transparent.
Bezug: Inkreismittelpunkt des Strebendreiecks im Ursprung, Z = Aussennormale, Paneel Z 0..panel_t, Kante P0P1 (Typ-Kante) parallel X. Kanten: e0 = P0P1, e1 = P1P2, e2 = P2P0.
Aufruf: python scripts/workshop/haut_paneel.py [typ ...] [--render]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def tri_points(kanten, inset):
    """Strebendreieck (Seitenlaengen kanten = [P0P1, P1P2, P2P0]) und das um `inset` verkleinerte Paneeldreieck, beide um den Inkreismittelpunkt zentriert: (strebe, paneel)."""
    c, a, b = kanten                                # P0P1 = c, P1P2 = a, P2P0 = b
    x2 = (b * b + c * c - a * a) / (2 * c)
    pts = [(0.0, 0.0), (c, 0.0), (x2, math.sqrt(max(b * b - x2 * x2, 0.0)))]
    s = (a + b + c) / 2
    area = c * pts[2][1] / 2
    r = area / s
    inc = ((a * pts[0][0] + b * pts[1][0] + c * pts[2][0]) / (a + b + c), (a * pts[0][1] + b * pts[1][1] + c * pts[2][1]) / (a + b + c))
    strebe = [(x - inc[0], y - inc[1]) for x, y in pts]
    k = (r - inset) / r
    return strebe, [(x * k, y * k) for x, y in strebe], r

def build(typ):
    tuer = typ.endswith("_tuer")                      # W20: BBB mit Tuerausschnitt (Basisfeld BBB 149,2, D36)
    base = typ[:-5] if tuer else typ
    p, d = sc.load_params("haut_paneel")
    T = d["typen"][base]
    kanten = T["kanten_nominal"]
    strebe, pan, r = tri_points(kanten, p["edge_inset"])
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    b.add("material.create", name="Polycarbonat", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"])
    root = f"T40_Haut_Paneel_{typ}"
    b.add("component.create", name=root, grounded=True)
    b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_Paneel")
    b.add("sketch.line", points=[[round(x, 3), round(y, 3)] for x, y in pan], closed=True)
    b.add("sketch.finish")
    b.add("solid.extrude", distance="panel_t", operation="new", name="E_Paneel", body_name="Paneel")
    if tuer:                                           # Ausschnitt = Zarge (Aussenbreite x Hoehe in der Feldebene, tuer_komplett.json), reicht bis ueber die Basiskante hinaus; P0P1 = Basiskante, Zarge mittig
        G = json.load(open(os.path.join(sc.ROOT, "data", "components", "tuer_komplett.json"), encoding="utf-8"))["geometrie"]
        yb = strebe[0][1]                                        # Basiskante P0P1 (Strebenachse) im Paneel-KS
        b.add("sketch.create", plane={"origin": [0, 0, -1], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_Tuerausschnitt")
        b.add("sketch.rectangle.two_point", p0=[-G["zarge_aussen_w"] / 2, round(yb - 1, 3)], p1=[G["zarge_aussen_w"] / 2, round(yb + G["zarge_hoehe"], 3)])
        b.add("sketch.finish")
        b.add("solid.extrude", distance=p["panel_t"] + 2, operation="cut", targets=["Paneel"], name="E_Tuerausschnitt")
    b.add("material.assign", bodies=["Paneel"], material="Polycarbonat")
    b.add("appearance.assign", bodies=["Paneel"], color=d["werkstoff"]["farbe"], opacity=p["opacity"])
    b.add("component.metadata.set", component=root, part_number="T40", description=d["beschreibung"] + f" (Typ {typ})", revision="A", properties={"Werkstoff": d["werkstoff"]["name"], "Typ": typ})
    return b, strebe, pan, r

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["AAB", "BBB", "BBB_tuer"]
    for typ in typs:
        b, strebe, pan, r = build(typ)
        out = os.path.join(sc.ROOT, "designs", "components", f"haut_paneel_{typ}.sc")
        sc.run(b.write(f"haut_paneel_{typ}"), out)
        ev = sc.evaluate(out)
        bd = ev["bodies"][0]
        print(typ, "Flaechen", bd["faces"], "Volumen", round(bd["volume_mm3"] / 1e6, 2), "l", "Masse", round(bd["mass_g"] / 1000, 2), "kg", "Box", [round(v) for v in bd["bbox"]["min"]], [round(v) for v in bd["bbox"]["max"]], "Inkreisradius", round(r, 1))
        if "--render" in sys.argv:
            rd = os.path.join(sc.ROOT, "renders", "components", "haut_paneel")
            os.makedirs(rd, exist_ok=True)
            sc.snapshot(out, os.path.join(rd, f"haut_paneel_{typ}-01-draufsicht.png"), [0, 0, 4], 0.0, 1.5707, 6200, w=1000, h=800)
