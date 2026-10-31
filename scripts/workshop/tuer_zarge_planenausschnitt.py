"""Tuer-Zarge Planenausschnitt T44 (W27 Schritt 3, D39, R24): Uebergang von der Zarge (tuer_komplett) zum Planenausschnitt der Folie im Tuerfeld.
Aufsatzrahmen (Alu-Winkel: Steg auf der Zarge, Kragen als Auflage fuer die Folie), Dichtband EPDM auf dem Kragen, Klemmleiste (Alu-Flachprofil) ueber der Folienkante. Drei Seiten (links, rechts, oben); unten ist die Schwelle offen.
Bezug = Feld-KS von tuer_komplett: Ursprung Mitte der Basiskante auf Z 0, X tangential, Y' hangaufwaerts in der Feldebene, Z' Feldnormale nach aussen (Zargenrohre Z' -15..+15). Aufruf: python scripts/workshop/tuer_zarge_planenausschnitt.py [--render]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def box(b, name, size, center, op="new", targets=None):
    if op == "new":
        b.add("solid.box", length=size[0], width=size[1], height=size[2], center=center, operation="new", name="R_" + name, body_name=name)
    else:
        b.add("solid.box", length=size[0], width=size[1], height=size[2], center=center, operation=op, targets=[targets], name="R_" + name + "_" + op)

def build():
    p, d = sc.load_params("tuer_zarge_planenausschnitt")
    tp, td = sc.load_params("tuer_komplett")
    fp, fd = sc.load_params("huelle_folie")
    G = td["geometrie"]
    r, sh, lw, lh = tp["rohr"], tp["schwelle_h"], G["lichte_w"], G["lichte_h"]
    xc = lw / 2 + r / 2                                          # Mitte der Pfostenrohre
    ytop = sh + lh + r                                           # Oberkante Sturz = 2068
    yc = sh + lh + r / 2                                         # Mitte Sturzrohr
    z_face = r / 2                                               # Zargen-Aussenflaeche
    z_seal_top = fp["foil_z0"]                                   # Folie liegt auf dem Dichtband
    z_collar_top = z_seal_top - p["seal_t"]
    wt, cw, ct = p["web_t"], p["collar_w"], p["collar_t"]
    y0, y1 = sh, ytop + (cw - r) / 2                             # Kragen laeuft 5 mm ueber die Sturz-Oberkante hinaus (symmetrisch zu den Pfosten)
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    b.add("material.create", name="Aluminium Zarge", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color="#c4c9ce", pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    b.add("material.create", name="EPDM Dichtband Zarge", density_g_cm3=1.1, color="#222222")
    root = "T44_Tuer_Zarge_Planenausschnitt"
    b.add("component.create", name=root, grounded=True)
    # --- T44a Aufsatzrahmen: je Pfosten ein Steg (Z' 15 .. Kragen-Oberkante) mit Kragen oben, am Sturz ebenso; ein Koerper
    b.add("component.create", name="T44a_Aufsatzrahmen")
    hs = z_collar_top - z_face                                   # Steghoehe
    ly = (y0 + y1) / 2
    box(b, "Aufsatzrahmen", [wt, y1 - y0, hs], [-xc, ly, z_face + hs / 2])
    box(b, "Steg_rechts", [wt, y1 - y0, hs], [xc, ly, z_face + hs / 2], op="join", targets="Aufsatzrahmen")
    box(b, "Steg_oben", [2 * xc + wt, wt, hs], [0, yc, z_face + hs / 2], op="join", targets="Aufsatzrahmen")
    box(b, "Kragen_links", [cw, y1 - y0, ct], [-xc, ly, z_collar_top - ct / 2], op="join", targets="Aufsatzrahmen")
    box(b, "Kragen_rechts", [cw, y1 - y0, ct], [xc, ly, z_collar_top - ct / 2], op="join", targets="Aufsatzrahmen")
    box(b, "Kragen_oben", [2 * xc + cw, cw, ct], [0, yc, z_collar_top - ct / 2], op="join", targets="Aufsatzrahmen")
    # Ausklinkungen im Steg an den Scharnier-Zargenlaschen der Tuer (liegen auf der Zargen-Aussenflaeche Z' 15..19, x -549..-501): Lage aus tuer_komplett.sc gemessen
    evt = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "tuer_komplett.sc"))
    lugs = [x for x in evt["bodies"] if x["name"].endswith("Zargenlasche")]
    for i, lg in enumerate(sorted(lugs, key=lambda x: x["bbox"]["min"][1]), 1):
        mn, mx = lg["bbox"]["min"], lg["bbox"]["max"]
        sx = -1 if (mn[0] + mx[0]) / 2 < 0 else 1
        zt = mx[2] + p["notch_clear"]
        box(b, f"Ausklinkung_{i}", [wt + 2, (mx[1] - mn[1]) + 2 * p["notch_clear"], zt - z_face + 0.5], [sx * xc, (mn[1] + mx[1]) / 2, (z_face - 0.5 + zt) / 2], op="cut", targets="Aufsatzrahmen")
    b.add("material.assign", bodies=["Aufsatzrahmen"], material="Aluminium Zarge")
    # --- T44b Dichtband EPDM auf dem Kragen (liegt unter der Folie)
    b.add("component.activate", component=root)
    b.add("component.create", name="T44b_Dichtband")
    sw, st = p["seal_w"], p["seal_t"]
    box(b, "Dichtband", [sw, y1 - y0, st], [-xc, ly, z_collar_top + st / 2])
    box(b, "Dichtband_rechts", [sw, y1 - y0, st], [xc, ly, z_collar_top + st / 2], op="join", targets="Dichtband")
    box(b, "Dichtband_oben", [2 * xc + sw, sw, st], [0, yc, z_collar_top + st / 2], op="join", targets="Dichtband")
    b.add("material.assign", bodies=["Dichtband"], material="EPDM Dichtband Zarge")
    # --- T44c Klemmleiste Alu-Flachprofil ueber der Folienkante (Folie Z' 64 .. 64,15)
    b.add("component.activate", component=root)
    b.add("component.create", name="T44c_Klemmleiste")
    kw, kt = p["clamp_w"], p["clamp_t"]
    zk = z_seal_top + fp["foil_t"] + kt / 2
    box(b, "Klemmleiste", [kw, y1 - y0, kt], [-xc, ly, zk])
    box(b, "Klemmleiste_rechts", [kw, y1 - y0, kt], [xc, ly, zk], op="join", targets="Klemmleiste")
    box(b, "Klemmleiste_oben", [2 * xc + kw, kw, kt], [0, yc, zk], op="join", targets="Klemmleiste")
    b.add("material.assign", bodies=["Klemmleiste"], material="Aluminium Zarge")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T44", d["beschreibung"]), ("T44a_Aufsatzrahmen", "T44a", "Aufsatzrahmen Alu 3 mm, Steg 47, Kragen 40, 3 Ausklinkungen an den Scharnierlaschen"), ("T44b_Dichtband", "T44b", "Dichtband EPDM 20 x 2"), ("T44c_Klemmleiste", "T44c", "Klemmleiste Alu 30 x 3")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, dict(xc=xc, y0=y0, y1=y1, yc=yc, z_face=z_face, z_collar_top=z_collar_top, z_seal_top=z_seal_top, zk=zk)

if __name__ == "__main__":
    b, info = build()
    out = os.path.join(sc.ROOT, "designs", "components", "tuer_zarge_planenausschnitt.sc")
    sc.run(b.write("tuer_zarge_planenausschnitt"), out)
    ev = sc.evaluate(out)
    print("tuer_zarge_planenausschnitt: Koerper", len(ev["bodies"]), "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 3), "kg", info)
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "tuer_zarge_planenausschnitt")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "tuer_zarge_planenausschnitt-01-iso.png"), [0, 1050, 30], 0.6, 0.5, 4200, w=1000, h=800)
        sc.snapshot(out, os.path.join(rd, "tuer_zarge_planenausschnitt-02-querschnitt.png"), [info["xc"], 1000, 40], 3.14159, 0.0, 200, w=900, h=600, section="y=1000")
