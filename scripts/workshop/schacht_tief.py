"""Tiefer Ventilschacht fuer Kugelhahn d63 (Vorbedingung M10-S2N Punkt 5, R47 M2), zwei Bauformen aus einem Generator:
  lt_schacht_kugelhahn_d63_tief_senkrecht  : KH1/KH2 (Notbypass K56/K57), Hahn senkrecht, Hahn-Port A 424 mm unter Flur;
                                             Querleitung d75 (Heber K01/K17 mit T5/T13) laeuft 250 mm unter Flur quer durch den Schacht;
                                             Rohr d63 verlaesst den Schacht unten durch den Boden.
  lt_schacht_kugelhahn_d63_tief_waagerecht : neue Stamm-Haehne auf K06-T-b/K22-T-b, Rohrachse waagerecht 186 mm unter Flur.
Grundlage: lt_schacht_kugelhahn_d63 (leitung_w36.py Teil 4, gleiche Wand, Werkstoffe, Deckel, Dichtung).
KS: Ursprung = Hahnmitte (Mitte Kugel), Z hoch; Flur/Deckeloberkante bei z = z_top.
Aufruf: python -X utf8 scripts/workshop/schacht_tief.py [senkrecht|waagerecht] [--json]"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w36 as W

FLUR_Z = 400.0                                   # Innenboden absolut (data/leitungstrassen.json z_bezug absolut, R47: absolut = relativ + 400)
HAHN_L = 50 + 2 * L.DEPTH[63]                   # 125: Kugelhahn d63 Port A bis B
KH_PORT_A_Z = -23.9                              # r_stuecke KH1/KH2 pos_a Z (absolut), dir -Z
QUER_Z = 150.0                                   # T5/T13 auf K01/K17 (d75), absolut
STAMM_Z = 214.0                                  # K06-T-b / K22-T-b Achse, absolut

def _mitte_senk():
    return KH_PORT_A_Z - HAHN_L / 2              # Hahnmitte absolut = -86,4

VAR = {
    "senkrecht": dict(
        rohrrichtung="senkrecht", innen_x=188.0, innen_y=400.0, versatz_x=-8.0, versatz_y=35.0, wand=8.0, boden=15.0,   # X aussen -110..94 (Deckel 96): K17-Bogen (Tangente -114) und T12-Abgang K21 (107,6) bleiben draussen; Y aussen -173..243: T6-Arm (-185) bleibt draussen
        z_top=FLUR_Z - _mitte_senk(),            # 486,4: Deckeloberkante = Flur
        z_boden_innen=-80.0,                     # 17,5 unter der Hahn-Stutzenunterkante (-62,5); Bogen K56-b/K57-b liegt unter dem Boden
        deckel_dicke=30.0, deckel_ueber=2.0,
        boden_loch=85.0, boden_dichtung_innen=73.0,          # Formstueck d63 aussen 72,15 passt durch; Rohr d63 mit Ringraumdichtung
        quer_z=QUER_Z - _mitte_senk(),           # 236,4: Achse K01/K17 im Schacht-KS
        quer_d=75.0, quer_loch=100.0, quer_dichtung_innen=86.0,   # Formstueck d75 aussen 84,75 (Bogenschenkel K17 am Rand) passt; Rohr d75 mit Ringraumdichtung
        dichtung_len=14.0),
    "waagerecht": dict(
        rohrrichtung="waagerecht", innen_x=240.0, innen_y=400.0, versatz_x=0.0, versatz_y=0.0, wand=8.0, boden=15.0,   # innen_x laengs Rohr 240: passt in die 400-mm-Gerade K22-T[1] (frei 263), Befund im Blatt
        z_top=FLUR_Z - STAMM_Z,                  # 186
        z_boden_innen=-150.0, deckel_dicke=30.0, deckel_ueber=2.0,
        rohr_loch=70.0, rohr_d=63.0, dichtung_len=14.0),
}
FNAME = {k: f"lt_schacht_kugelhahn_d63_tief_{k}" for k in VAR}
PN = {"senkrecht": "T70-SCH-KH63-TS", "waagerecht": "T70-SCH-KH63-TW"}

def geom(v):
    s = VAR[v]
    hx, hy = s["innen_x"] / 2, s["innen_y"] / 2
    g = dict(s)
    g.update(x_in=(s["versatz_x"] - hx, s["versatz_x"] + hx), y_in=(s["versatz_y"] - hy, s["versatz_y"] + hy),
             x_out=(s["versatz_x"] - hx - s["wand"], s["versatz_x"] + hx + s["wand"]), y_out=(s["versatz_y"] - hy - s["wand"], s["versatz_y"] + hy + s["wand"]),
             z_out_bottom=s["z_boden_innen"] - s["boden"], z_wall_top=s["z_top"] - s["deckel_dicke"],
             deckel_x=s["innen_x"] + 2 * s["wand"] + 2 * s["deckel_ueber"], deckel_y=s["innen_y"] + 2 * s["wand"] + 2 * s["deckel_ueber"])
    g["hoehe_wanne"] = g["z_wall_top"] - g["z_out_bottom"]
    g["tiefe_gesamt"] = s["z_top"] - g["z_out_bottom"]
    return g

def build(v):
    g = geom(v)
    b = sc.Build(); nm = "T70_Schacht_Kugelhahn_d63_tief_" + v
    for k, val in VAR[v].items():
        if isinstance(val, (int, float)):
            b.add("parameters.add", name=k, expression=f"{round(val, 3)} mm")
    b.add("material.create", name="LT pehd", density_g_cm3=0.95, color="#3a3d40")
    b.add("material.create", name="LT epdm", density_g_cm3=1.1, color="#1a1a1a")
    b.add("component.create", name=nm, grounded=True)
    cx, cy = g["versatz_x"], g["versatz_y"]
    ax, ay = g["x_out"][1] - g["x_out"][0], g["y_out"][1] - g["y_out"][0]
    b.add("solid.box", length=ax, width=ay, height=g["hoehe_wanne"], center=[cx, cy, (g["z_out_bottom"] + g["z_wall_top"]) / 2], operation="new", name="Wanne_R", body_name="Schachtwanne")
    b.add("solid.box", length=g["innen_x"], width=g["innen_y"], height=g["z_wall_top"] - g["z_boden_innen"] + 1, center=[cx, cy, (g["z_boden_innen"] + g["z_wall_top"] + 1) / 2], operation="cut", targets=["Schachtwanne"], name="Innenraum")
    seals = []
    if v == "senkrecht":
        # Bodendurchfuehrung (Rohr d63 nach unten)
        b.add("solid.cylinder", diameter=g["boden_loch"], height=g["boden"] + 20, base=[0, 0, g["z_out_bottom"] - 10], axis=[0, 0, 1], operation="cut", targets=["Schachtwanne"], name="Bodendurchfuehrung")
        z0 = g["z_out_bottom"] - 3
        b.add("solid.cylinder", diameter=g["boden_loch"], height=g["boden"] + 6, base=[0, 0, z0], axis=[0, 0, 1], operation="new", name="Dichtung_Boden_R", body_name="Dichtung_Boden")
        b.add("solid.cylinder", diameter=g["boden_dichtung_innen"], height=g["boden"] + 8, base=[0, 0, z0 - 1], axis=[0, 0, 1], operation="cut", targets=["Dichtung_Boden"], name="Dichtung_Boden_Bohrung")
        seals.append("Dichtung_Boden")
        # Querleitung d75 durch beide X-Waende (Achse y = 0, z = quer_z)
        x0, x1 = g["x_out"]
        b.add("solid.cylinder", diameter=g["quer_loch"], height=x1 - x0 + 20, base=[x0 - 10, 0, g["quer_z"]], axis=[1, 0, 0], operation="cut", targets=["Schachtwanne"], name="Querdurchfuehrungen")
        for nmx, xs in (("A", x0 - 3), ("B", x1 - g["wand"] - 3)):
            b.add("solid.cylinder", diameter=g["quer_loch"], height=g["dichtung_len"], base=[xs, 0, g["quer_z"]], axis=[1, 0, 0], operation="new", name=f"Dichtung_{nmx}_R", body_name=f"Dichtung_{nmx}")
            b.add("solid.cylinder", diameter=g["quer_dichtung_innen"], height=g["dichtung_len"] + 2, base=[xs - 1, 0, g["quer_z"]], axis=[1, 0, 0], operation="cut", targets=[f"Dichtung_{nmx}"], name=f"Dichtung_{nmx}_Bohrung")
            seals.append(f"Dichtung_{nmx}")
    else:
        x0, x1 = g["x_out"]
        b.add("solid.cylinder", diameter=g["rohr_loch"], height=x1 - x0 + 20, base=[x0 - 10, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Schachtwanne"], name="Wanddurchfuehrungen")
        for nmx, xs in (("A", x0 - 3), ("B", x1 - g["wand"] - 3)):
            b.add("solid.cylinder", diameter=g["rohr_loch"], height=g["dichtung_len"], base=[xs, 0, 0], axis=[1, 0, 0], operation="new", name=f"Dichtung_{nmx}_R", body_name=f"Dichtung_{nmx}")
            b.add("solid.cylinder", diameter=g["rohr_d"], height=g["dichtung_len"] + 2, base=[xs - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=[f"Dichtung_{nmx}"], name=f"Dichtung_{nmx}_Bohrung")
            seals.append(f"Dichtung_{nmx}")
    b.add("solid.box", length=g["deckel_x"], width=g["deckel_y"], height=g["deckel_dicke"], center=[cx, cy, g["z_wall_top"] + g["deckel_dicke"] / 2], operation="new", name="Deckel_R", body_name="Deckel")
    for sy in (-1, 1):
        b.add("solid.box", length=100, width=30, height=16, center=[cx, cy + sy * 140, g["z_top"] - 7], operation="cut", targets=["Deckel"], name=f"Griffmulde_{sy}")
    b.add("material.assign", bodies=["Schachtwanne", "Deckel"], material="LT pehd")
    b.add("material.assign", bodies=seals, material="LT epdm")
    if v == "senkrecht":
        desc = (f"Tiefer Ventilschacht fuer senkrechten Kugelhahn d63 (KH1/KH2): Wanne PE-HD innen 400 x 400, Hahnmitte {g['z_top']:.1f} unter Flur, "
                f"Bodendurchfuehrung fuer Rohr d63, Querdurchfuehrungen d100 fuer Leitung d75 {g['z_top'] - g['quer_z']:.0f} unter Flur, Deckel mit Griffmulden")
    else:
        desc = f"Ventilschacht fuer waagerechten Kugelhahn d63 (Stamm): Wanne PE-HD innen 400 x 400, Rohrachse {g['z_top']:.0f} unter Flur, Wanddurchfuehrungen mit Dichtung d63, Deckel mit Griffmulden"
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number=PN[v], description=desc, revision="A", properties={"Werkstoff": "PE-HD, EPDM-Dichtung"})
    return b, nm, g, seals

def ports(v):
    g = geom(v)
    out = []
    if v == "senkrecht":
        out.append(("Hahn Port A (oben)", (0.0, 0.0, HAHN_L / 2), (0.0, 0.0, 1.0), "Lage Kugelhahn", "DN50"))
        out.append(("Bodendurchfuehrung", (0.0, 0.0, g["z_out_bottom"]), (0.0, 0.0, -1.0), "Durchfuehrung", "DN50 (d63)"))
        out.append(("Querdurchfuehrung A", (g["x_out"][0], 0.0, g["quer_z"]), (-1.0, 0.0, 0.0), "Durchfuehrung", "DN65 (d75)"))
        out.append(("Querdurchfuehrung B", (g["x_out"][1], 0.0, g["quer_z"]), (1.0, 0.0, 0.0), "Durchfuehrung", "DN65 (d75)"))
    else:
        out.append(("Durchfuehrung A", (g["x_out"][0], 0.0, 0.0), (-1.0, 0.0, 0.0), "Durchfuehrung", "DN50 (d63)"))
        out.append(("Durchfuehrung B", (g["x_out"][1], 0.0, 0.0), (1.0, 0.0, 0.0), "Durchfuehrung", "DN50 (d63)"))
    out.append(("Deckel", (g["versatz_x"], g["versatz_y"], g["z_top"]), (0.0, 0.0, 1.0), "Oeffnung / Flur", f"{g['innen_x']:g}x{g['innen_y']:g}"))
    return [(n, tuple(round(c, 2) for c in p), d, a, dn) for n, p, d, a, dn in out]

def json_data():
    out = {"quelle": "scripts/workshop/schacht_tief.py", "flur_z_absolut": FLUR_Z, "bauformen": {}}
    for v in VAR:
        g = geom(v)
        out["bauformen"][FNAME[v]] = {"teilenummer": PN[v], "rohrrichtung": v, "parameter": {k: (round(x, 2) if isinstance(x, float) else x) for k, x in VAR[v].items()},
            "aussen": [g["x_out"][1] - g["x_out"][0], g["y_out"][1] - g["y_out"][0], round(g["tiefe_gesamt"], 1)],
            "einbau": ({"fuer": ["KH1 (K56, Linie 1)", "KH2 (K57, Linie 2)"], "hahnmitte_absolut_z": round(_mitte_senk(), 1), "deckel_oberkante_absolut_z": FLUR_Z,
                        "lage_x": "Schacht-X = Richtung K01-m (Linie 1) bzw. K17-m (Linie 2), weg vom Steigrohr K01/K17", "lage_y": "Z x X; Spindel/Hebel des Hahns zeigt nach Schacht +Y",
                        "hahn": "lt_kugelhahn_d63, Hahn-Z nach Welt -Z (Port A oben), Hahn +X (Spindel) nach Schacht +Y"} if v == "senkrecht" else
                       {"fuer": ["Stamm-Hahn L1 auf K06-T-b", "Stamm-Hahn L2 auf K22-T-b"], "rohrachse_absolut_z": STAMM_Z, "deckel_oberkante_absolut_z": FLUR_Z,
                        "lage_x": "Schacht-X = Rohrachse", "hahn": "lt_kugelhahn_d63, Hahn-Z = Rohrachse, Spindel (Hahn +X) nach Welt +Z, Hahnmitte im Ursprung"}),
            "ports": [{"name": n, "lage": list(p), "richtung": list(d), "art": a, "dn": dn} for n, p, d, a, dn in ports(v)]}
    return out

def render(v, fname, sc_path=None):
    """Schnitt y = 0 (Blick von -Y); sc_path erlaubt ein Pruefmodell mit Hahn und Rohren (check_schacht_tief.py)."""
    g = geom(v)
    out = os.path.join(sc.ROOT, "renders", "components", "leitungsteile", fname + ".png")
    sc.snapshot(sc_path or os.path.join(sc.ROOT, "designs", "components", fname + ".sc"), out, [g["versatz_x"], 0, (g["z_out_bottom"] + g["z_top"]) / 2], 3.14159, 0.25, 1700 if v == "senkrecht" else 1300,
                w=1000, h=800, section="y=0")
    return out

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or list(VAR)
    for v in want:
        b, nm, g, seals = build(v)
        out = L.save(b, nm, FNAME[v])
        print(FNAME[v], "->", out, {k: round(g[k], 1) for k in ("z_top", "z_out_bottom", "tiefe_gesamt")})
        if "--render" in sys.argv:
            try:
                print("Bild", render(v, FNAME[v]))
            except SystemExit as e:
                print("Bild FEHLER", e)
    if "--json" in sys.argv:
        p = os.path.join(sc.ROOT, "data", "components", "lt_schacht_tief.json")
        open(p, "w", encoding="utf-8").write(json.dumps(json_data(), indent=1, ensure_ascii=False) + "\n")
        print("geschrieben", p)
