"""Tuer komplett T50 (W20, D36, R13): Zarge aus Rechteckrohr (Schritt 2), Tuerblatt (Schritt 3) in der Feldebene des Basisfeldes BBB 149,2.
Feld-KS (siehe tuer_geom.py): Ursprung Mitte der Basiskante auf Z 0, X tangential, Y' hangaufwaerts in der Feldebene, Z' Feldnormale nach aussen. Zarge: Schwelle (s 0..rohr), Pfosten (je Seite, Lichte dazwischen), Sturz.
Tuerblatt (Schritt 3): Z' -11..29 (40 dick), Spiel unten 2 / oben 6 / seitlich 8, Anschlag innen (Z' -15..-12), oeffnet nach aussen (+Z'), Scharniere links (3 Aufschraubbaender), Druecker rechts, Dichtung auf dem Anschlag.
Aufruf: python scripts/workshop/tuer.py [--render]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tuer_geom as TGm

def rect_member(b, name, dims, origin, xdir, ydir, dist, symmetric=False):
    b.add("sketch.create", plane={"origin": origin, "x_dir": xdir, "y_dir": ydir}, name="S_" + name)
    b.add("frame.profile.insert", profile=dict(kind="rect_tube", **dims), at=[0, 0], anchor="center")
    b.add("sketch.finish")
    ex = dict(distance=dist, name="F_" + name, body_name=name)
    if symmetric:
        ex["direction"] = "symmetric"
    b.add("solid.extrude", **ex)
    b.add("material.assign", bodies=[name], material="Stahl verzinkt")

def build():
    p, d = sc.load_params("tuer")
    G = d["geometrie"]
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    r, wall, sh = p["rohr"], p["rohr_wand"], p["schwelle_h"]
    lw, lh = G["lichte_w"], G["lichte_h"]
    fw = G["zarge_aussen_w"]
    b.add("material.create", name="Stahl verzinkt", density_g_cm3=7.85, color="#aeb4b8", pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    root = "T50_Tuer_Komplett"
    b.add("component.create", name=root, grounded=True)
    b.add("component.create", name="T50a_Zarge")
    dims = dict(width=r, height=r, wall=wall)
    # Schwelle: s 0..sh, ueber die ganze Zargenbreite; Plane normal +X (x_dir Y', y_dir Z'), symmetrisch um X 0
    rect_member(b, "Schwelle", dims, [0, sh / 2, 0], [0, 1, 0], [0, 0, 1], fw, symmetric=True)
    # Pfosten: von der Schwelle bis zum Sturz, in Y'-Richtung (Plane x_dir Z', y_dir X -> Normale +Y')
    for sg, nm in ((-1, "Pfosten_links"), (1, "Pfosten_rechts")):
        rect_member(b, nm, dims, [sg * (lw / 2 + r / 2), sh, 0], [0, 0, 1], [1, 0, 0], lh)
    # Sturz: ueber den Pfosten, s = sh + lh .. + r
    rect_member(b, "Sturz", dims, [0, sh + lh + r / 2, 0], [0, 1, 0], [0, 0, 1], fw, symmetric=True)
    # --- Tuerblatt 1000 x 2000 x 40 (Sandwich), Z' -11..29
    bw, bh, bt = p["blatt_w"], p["blatt_h"], p["blatt_t"]
    z0b = -11.0
    s0b = sh + 2.0                                                              # Spiel unten 2 mm
    b.add("component.activate", component=root)
    b.add("component.create", name="T50b_Tuerblatt")
    b.add("material.create", name="Tuerblatt Sandwich", density_g_cm3=0.31, color="#d9d3c3")
    b.add("solid.box", length=bw, width=bh, height=bt, center=[0, s0b + bh / 2, z0b + bt / 2], operation="new", name="Blatt_R", body_name="Tuerblatt")
    b.add("material.assign", bodies=["Tuerblatt"], material="Tuerblatt Sandwich")
    # --- Anschlag innen (Flachstahl 14 x 3) auf Pfosten und Sturz, Dichtung (EPDM 6 x 1, Spalt Anschlag-Blatt 1 mm) auf dem Anschlag
    b.add("component.activate", component=root)
    b.add("component.create", name="T50c_Anschlag_Dichtung")
    b.add("material.create", name="EPDM schwarz", density_g_cm3=1.1, color="#222222")
    sx, sz0, sz1 = lw / 2, sh, sh + lh
    for sg, nm in ((-1, "Anschlag_links"), (1, "Anschlag_rechts")):
        b.add("solid.box", length=14, width=lh, height=3, center=[sg * (sx - 7), sz0 + lh / 2, -15 + 1.5], operation="new", name="AS_" + nm, body_name=nm)
    b.add("solid.box", length=lw - 28, width=14, height=3, center=[0, sz1 - 7, -15 + 1.5], operation="new", name="AS_Sturz", body_name="Anschlag_Sturz")
    b.add("material.assign", bodies=["Anschlag_links", "Anschlag_rechts", "Anschlag_Sturz"], material="Stahl verzinkt")
    for sg, nm in ((-1, "Dichtung_links"), (1, "Dichtung_rechts")):
        b.add("solid.box", length=6, width=lh - 14, height=1, center=[sg * (sx - 17), sz0 + (lh - 14) / 2 + 0, -12 + 0.5], operation="new", name="DI_" + nm, body_name=nm)
    b.add("solid.box", length=lw - 2 * 17 - 12, width=6, height=1, center=[0, sz1 - 17, -12 + 0.5], operation="new", name="DI_Sturz", body_name="Dichtung_Sturz")
    b.add("material.assign", bodies=["Dichtung_links", "Dichtung_rechts", "Dichtung_Sturz"], material="EPDM schwarz")
    # --- Beschlaege: 3 Aufschraubbaender links (Zargenlasche auf dem Pfosten Z' 15..19, Blattlasche auf dem Blatt Z' 29..33, Bolzen D10 dazwischen), Druecker rechts
    b.add("component.activate", component=root)
    b.add("component.create", name="T50d_Beschlaege")
    hx = -(bw / 2 + 5)
    for k, hs in enumerate((200, 1000, 1800), 1):
        s_c = s0b + hs
        b.add("solid.box", length=48, width=90, height=4, center=[hx - 20, s_c, 15 + 2], operation="new", name=f"SL_{k}", body_name=f"Scharnier{k}_Zargenlasche")
        b.add("solid.box", length=48, width=90, height=4, center=[hx + 20, s_c, 29 + 2], operation="new", name=f"BL_{k}", body_name=f"Scharnier{k}_Blattlasche")
        b.add("solid.cylinder", diameter=10, height=90, base=[hx, s_c - 45, 24], axis=[0, 1, 0], operation="new", name=f"BZ_{k}", body_name=f"Scharnier{k}_Bolzen")
        b.add("material.assign", bodies=[f"Scharnier{k}_Zargenlasche", f"Scharnier{k}_Blattlasche", f"Scharnier{k}_Bolzen"], material="Stahl verzinkt")
    gx, gs = bw / 2 - 60, s0b + 1000                                              # Druecker rechts auf Blatthoehe 1 m
    for face, zf, dz, nm in ((1, 29, 1, "aussen"), (-1, -11, -1, "innen")):
        b.add("solid.cylinder", diameter=50, height=4, base=[gx, gs, zf if face > 0 else zf - 4], axis=[0, 0, 1], operation="new", name=f"RO_{nm}", body_name=f"Rosette_{nm}")
        b.add("solid.cylinder", diameter=18, height=40, base=[gx, gs, zf + (4 if face > 0 else -4)] if face > 0 else [gx, gs, zf - 4], axis=[0, 0, face], operation="new", name=f"DH_{nm}", body_name=f"Druecker_Hals_{nm}")
        zl = zf + face * (4 + 40 - 9)
        b.add("solid.box", length=130, width=18, height=18, center=[gx - 45, gs, zl], operation="new", name=f"DL_{nm}", body_name=f"Druecker_Hebel_{nm}")
        b.add("material.assign", bodies=[f"Rosette_{nm}", f"Druecker_Hals_{nm}", f"Druecker_Hebel_{nm}"], material="Stahl verzinkt")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T50", d["beschreibung"]), ("T50b_Tuerblatt", "T50b", "Tuerblatt 1000 x 2000 x 40 (Sandwich)"), ("T50c_Anschlag_Dichtung", "T50c", "Anschlag Flachstahl innen und EPDM-Dichtung"), ("T50d_Beschlaege", "T50d", "3 Aufschraubbaender links, Druecker rechts"), ("T50a_Zarge", "T50a", "Zarge aus Rechteckrohr 30 x 30 x 2: Schwelle, 2 Pfosten, Sturz (Lichte 1016 x 2008)")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="B", properties={"Werkstoff": "Stahl verzinkt"})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "tuer_komplett.sc")
    sc.run(build().write("tuer_komplett"), out)
    ev = sc.evaluate(out)
    for x in ev["bodies"]:
        print(x["name"], x["faces"], round(x["mass_g"] / 1000, 2), "kg", [round(v, 1) for v in x["bbox"]["min"]], [round(v, 1) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "tuer_komplett")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "tuer_komplett-01-zarge.png"), [0, 1000, 0], 0.6, 0.3, 4200, w=1000, h=800)
