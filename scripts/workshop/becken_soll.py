"""Becken nach Leons Oasis-Quelle (N-UNIFY-AUTOBAHN U3, D118 bis D120): Wanne mit Hohlraum, Wasserkoerper, bei Anzucht- und
Lebendfutterbecken eine Ueberlauf-Tuelle d63 auf Wasserspiegelhoehe. Gemeinsamer Bau fuer pool_zentral (Fischtank, T5) und zweitbecken
(Anzuchtbecken, T6); becken_dritt_klein (Lebendfutterbecken, T14k) nutzt nur ueberlauf_tuelle().

Koordinaten: Welt (x, y aus data/oasis-lage.json Bauplatz, Z absolut = fussboden_z + Hoehe ueber Fussboden, D94: Z 400). Die Wasseroberkante
des Koerpers T5_Wasser/T6_Wasser ist der Messwert fuer scripts/check_oasis_soll.py (data/oasis-messung.json). Zahlen stehen in
data/components/<klasse>.json, die Soll-Werte in data/params.json (varianten_werte) und data/oasis-soll.json; check_pool_soll.py vergleicht sie.
Aufruf: python -X utf8 scripts/workshop/pool_zentral.py [--render] | zweitbecken.py [--render]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

LAGE_PFAD = os.path.join(sc.ROOT, "data", "oasis-lage.json")

# Konfiguration je Klasse: Koerpernamen, Teilenummer, Ziel des Ueberlaufs (Soll-ID in oasis-lage.json), eigene Soll-ID
CFG = {
    "pool_zentral": dict(tn="T5_Zentraltank", wn="T5_Wasser", root="T5_Fischtank", pn="T5", sid="fish", ziel=None),
    "zweitbecken": dict(tn="T6_Zweitbecken", wn="T6_Wasser", root="T6_Anzuchtbecken", pn="T6", sid="nursery", ziel="fish"),
}

def lage_xy(sid):
    """Bauplatz (x, y) der Soll-ID aus data/oasis-lage.json (U1)."""
    for b in json.load(open(LAGE_PFAD, encoding="utf-8"))["bauteile"]:
        if b["id"] == sid:
            return b["bauplatz"]["x_mm"], b["bauplatz"]["y_mm"]
    raise KeyError(sid)

def ue_azimut(von_sid, nach_sid):
    """Richtung der Ueberlauf-Tuelle: Azimut (Grad, Weltrahmen) vom Mittelpunkt des Beckens zum naechsten Becken der Kette (D120)."""
    x0, y0 = lage_xy(von_sid); x1, y1 = lage_xy(nach_sid)
    return math.degrees(math.atan2(y1 - y0, x1 - x0))

def ueberlauf_tuelle(b, p, tank, cx, cy, z_wsp, az_deg, name):
    """Wanddurchfuehrung d63 auf Wasserspiegelhoehe (D120): Rohr-Innenunterkante = z_wsp, Achse = z_wsp + ue_id/2; Stutzen von der inneren
    Wandflaeche (Radius wasser_d/2) bis ring + stutzen_len ausserhalb, Muffe d63 am Aussenende. Gibt (name, port_mitte, richtung) zurueck."""
    dn = int(p["ue_dn"]); od = L.od_f(dn); idm = p["ue_id"]
    ux, uy = round(math.cos(math.radians(az_deg)), 6), round(math.sin(math.radians(az_deg)), 6)
    z = round(z_wsp + idm / 2.0, 3)
    r_in = p["wasser_d"] / 2.0; r_out = r_in + p["ring"]; lang = p["ring"] + p["stutzen_len"]
    at = lambda r: [round(cx + r * ux, 3), round(cy + r * uy, 3), z]
    b.add("solid.cylinder", diameter=od, height=p["ring"] + 2, base=at(r_in - 1), axis=[ux, uy, 0], operation="cut", targets=[tank], name=name + "_Loch")
    b.add("solid.cylinder", diameter=od, height=lang, base=at(r_in), axis=[ux, uy, 0], operation="new", name=name, body_name=name)
    b.add("solid.cylinder", diameter=idm, height=lang + 2, base=at(r_in - 1), axis=[ux, uy, 0], operation="cut", targets=[name], name=name + "_Bohrung")
    b.add("solid.cylinder", diameter=dn, height=L.DEPTH[dn] + 1, base=at(r_in + lang - L.DEPTH[dn]), axis=[ux, uy, 0], operation="cut", targets=[name], name=name + "_Muffe")
    b.add("material.assign", bodies=[name], material="Stutzen PVC")
    return name, tuple(at(r_in + lang)), (ux, uy, 0.0)

def ports(klasse):
    """[(name, (x,y,z), (dx,dy,dz), 'd63')] der Ueberlauf-Tuelle (leer beim Fischtank)."""
    p, d = sc.load_params(klasse); c = CFG[klasse]
    if not c["ziel"]:
        return []
    az = ue_azimut(c["sid"], c["ziel"])
    ux, uy = math.cos(math.radians(az)), math.sin(math.radians(az))
    z = p["fussboden_z"] + p["wsp"] + p["ue_id"] / 2.0
    r = p["wasser_d"] / 2.0 + p["ring"] + p["stutzen_len"]
    return [(c["pn"] + "_Ueberlauf", (p["pos_x"] + r * ux, p["pos_y"] + r * uy, z), (ux, uy, 0.0), "d%d" % p["ue_dn"])]

def build(klasse):
    p, d = sc.load_params(klasse); c = CFG[klasse]
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    b.add("material.create", name="Beton", density_g_cm3=2.4, color="#9a9a96")
    b.add("material.create", name="Wasser", density_g_cm3=1.0, color="#6fb6e8")
    b.add("material.create", name="Stutzen PVC", density_g_cm3=1.4, color="#8d9296")
    b.add("component.create", name=c["root"], grounded=True)
    cx, cy, fz = p["pos_x"], p["pos_y"], p["fussboden_z"]
    d_out = p["wasser_d"] + 2 * p["ring"]
    z_bot = fz + p["wsp"] - p["tiefe"]                    # Aussenunterkante (Standflaeche): Fischtank -720, Anzuchtbecken 400 (= Fussboden)
    total = fz + p["rand"] - z_bot                        # Aussenhoehe bis Oberkante Wand
    b.add("solid.cylinder", diameter=d_out, height=total, base=[cx, cy, z_bot], axis=[0, 0, 1], operation="new", name=c["tn"], body_name=c["tn"])
    b.add("solid.cylinder", diameter=p["wasser_d"], height=total, base=[cx, cy, z_bot + p["boden"]], axis=[0, 0, 1], operation="cut", targets=[c["tn"]], name=c["tn"] + "_Hohlraum")
    b.add("material.assign", bodies=[c["tn"]], material="Beton")
    b.add("solid.cylinder", diameter=p["wasser_d"] - p["wasser_spiel"], height=fz + p["wsp"] - (z_bot + p["boden"]), base=[cx, cy, z_bot + p["boden"]], axis=[0, 0, 1], operation="new", name=c["wn"], body_name=c["wn"])
    b.add("material.assign", bodies=[c["wn"]], material="Wasser")
    if c["ziel"]:
        ueberlauf_tuelle(b, p, c["tn"], cx, cy, fz + p["wsp"], ue_azimut(c["sid"], c["ziel"]), c["pn"] + "_Ueberlauf")
    b.add("component.metadata.set", component=c["root"], part_number=d["teilenummer"], description=d["beschreibung"], revision=d["revision"], properties={"Werkstoff": d["werkstoff"]["name"]})
    return b

def main(klasse):
    c = CFG[klasse]
    out = os.path.join(sc.ROOT, "designs", "components", klasse + ".sc")
    sc.run(build(klasse).write(klasse), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v) for v in mn], [round(v) for v in mx], [(x["name"], round(x["volume_mm3"] / 1e6, 1), "l") for x in ev["bodies"]])
    if "--render" in sys.argv:
        p, _ = sc.load_params(klasse)
        rd = os.path.join(sc.ROOT, "renders", "components", klasse)
        os.makedirs(rd, exist_ok=True)
        zc = p["fussboden_z"] + (p["wsp"] + p["rand"]) / 2 - p["tiefe"] / 2
        tgt = [p["pos_x"], p["pos_y"], zc]
        sc.snapshot(out, os.path.join(rd, klasse + "-02-schnitt.png"), tgt, 0.0, 0.0, p["wasser_d"] * 1.7 + 1200, w=1000, h=700, section="y=%g" % p["pos_y"])
        sc.snapshot(out, os.path.join(rd, klasse + "-01-schraeg.png"), tgt, 0.7, 0.45, p["wasser_d"] * 1.9 + 1500, w=1000, h=700)
