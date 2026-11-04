"""NFT-Tisch T22 (aussen / mitte / innen), Rev. B (W16, D18): je Reihe eigene Rinnenlaenge (Zehneck-Seite minus 2 x corner_gap), Zulaufverteiler und Sammelrohr schraeg entlang der Sektorgrenze,
Portalbock mit Beinen ausserhalb der Beete (mitte/aussen) bzw. Auslegerbock mit Pfosten ausserhalb des Pools (innen). Geometrie: tisch_geom.py, Rinnenvarianten: rinnen_reihen.py.
Tisch-KS: X tangential (OBJ-yaw = Azimut + 90 Grad), Y radial nach INNEN, Z hoch; Instanz mit yaw = Azimut + 90 Grad auf die Sektorachse bei ap_c setzen.
Aufruf: python scripts/workshop/nft_tisch.py [typ ...] [--render]   (ohne Typ: alle drei)"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

STEEL = "#aeb4b8"
STRUT_Z = {"innen": 400}          # Laengsstreben der Ausleger unterhalb des Kragarms und ausserhalb des Beckenrands (A); sonst Parameter strut_z

def member(b, name, dims, origin, xdir, ydir, dist, symmetric=True, kind="rect_tube"):
    """Rechteckrohr: Profil in der Ebene (origin, xdir, ydir), Mitte auf origin, extrudiert um dist (symmetrisch oder in Normalenrichtung)."""
    b.add("sketch.create", plane={"origin": origin, "x_dir": xdir, "y_dir": ydir}, name="S_" + name)
    b.add("frame.profile.insert", profile=dict(kind=kind, **dims), at=[0, 0], anchor="center")
    b.add("sketch.finish")
    ex = dict(distance=dist, name="F_" + name, body_name=name)
    if symmetric:
        ex["direction"] = "symmetric"
    b.add("solid.extrude", **ex)
    b.add("material.assign", bodies=[name], material="Stahl verzinkt")

def skew(sgn):
    """Einheitsvektor und Streckung der schraegen Rohrachse entlang der Sektorgrenze (sgn -1: Zulaufseite -X, +1: Sammelrohr +X)."""
    k = math.sqrt(1 + TG.T18 ** 2)
    return [round(sgn * TG.T18 / k, 6), round(1 / k, 6), 0.0], k

def build(typ):
    p, d = sc.load_params("nft_tisch")
    T = d["typen"][typ]
    G = TG.geometry(typ, p, T)
    rows, n, zc, slope, Wt, xb = G["rows"], G["n"], G["zc"], G["slope"], G["Wt"], G["xb"]
    ang = math.degrees(math.atan(slope))
    xc = rows[0]["xc"]
    zrow = lambda x: zc - (x - xc) * slope                    # Rinnen-Unterkante/Holmoberkante an der Stelle x (Gefaelle zur +X-Seite)
    b = sc.Build()
    b.add("parameters.add", name="slope_pct", expression=str(p["slope_pct"]), unit="")
    for k in ("leg_w", "leg_wall", "holm_w", "holm_h", "strut_z", "corner_gap", "leg_clearance"):
        b.add("parameters.add", name=k, expression=f"{p[k]} mm")
    b.add("parameters.add", name="rinnen_abstand", expression=f"{G['rp']} mm")
    b.add("parameters.add", name="ap_c", expression=f"{G['apc']} mm")
    b.add("parameters.add", name="z_rinne_mitte", expression=f"{zc} mm")
    b.add("parameters.add", name="n_rinnen", expression=str(n), unit="")
    if G["bed_w"]:
        b.add("parameters.add", name="bed_outer_w", expression=f"{G['bed_w']} mm")
    b.add("material.create", name="Stahl verzinkt", density_g_cm3=7.85, color=STEEL, pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    b.add("material.create", name="PVC blau", density_g_cm3=1.4, color="#2a5da8")
    b.add("material.create", name="PVC grau", density_g_cm3=1.4, color="#8d9296")
    b.add("material.create", name="Schlauch hellblau", density_g_cm3=1.0, color="#7fc4ea")
    root = f"T22_NFT_Tisch_{typ}"
    b.add("component.create", name=root, grounded=True)
    # --- Rinnen (je Reihe eigene Laenge, Phase A/B abwechselnd = Zickzack)
    b.add("component.create", name="T22b_Rinnen")
    for r in rows:
        nm = f"Rinne_{r['k'] + 1}"
        b.add("component.insert_design", path=f"designs/components/nft_rinne_{typ}_r{r['k'] + 1}.sc", name=nm)
        b.add("occurrence.move", occurrence=f"{nm}:1", translate=[xc, r["y"], zc])
        b.add("occurrence.move", occurrence=f"{nm}:1", axis=[0, 1, 0], angle=f"{ang:.5f} deg", origin=[xc, r["y"], zc], space="world")
    # --- Boecke
    leg_w, lw = p["leg_w"], p["leg_wall"]
    for i, x in enumerate(xb, 1):
        zh = zrow(x)                                            # Rinnenunterkante = Holmoberkante an dieser Stelle
        zb = zh - p["holm_h"]                                   # Holmunterkante = Beinoberkante
        leg_len = zb - p["foot_t"]
        b.add("component.activate", component=root)
        b.add("component.create", name=f"T22a_Bock_{i}")
        for (lx, ly) in [(x, y) for (xx, y) in G["legs"] if abs(xx - x) < 1e-6]:
            tag = "A" if ly < 0 else "B"
            member(b, f"Bein_{i}{tag}", dict(width=leg_w, height=leg_w, wall=lw), [lx, ly, p["foot_t"]], [1, 0, 0], [0, 1, 0], leg_len, symmetric=False)
            fp = p["foot_plate"]
            b.add("solid.box", length=fp, width=fp, height=p["foot_t"], center=[lx, ly, p["foot_t"] / 2], operation="new", name=f"FP_{i}{tag}", body_name=f"Fussplatte_{i}{tag}")
            for hx, hy in ((-fp / 2 + 15, -fp / 2 + 15), (fp / 2 - 15, fp / 2 - 15)):
                b.add("solid.cylinder", diameter=p["foot_hole"], height=p["foot_t"] + 2, base=[lx + hx, ly + hy, -1], operation="cut", targets=[f"Fussplatte_{i}{tag}"], name=f"FL_{i}{tag}{int(hx)}")
            b.add("material.assign", bodies=[f"Fussplatte_{i}{tag}"], material="Stahl verzinkt")
            for hx, hy in ((-fp / 2 + 15, -fp / 2 + 15), (fp / 2 - 15, fp / 2 - 15)):
                b.add("parts.insert", family="hex_bolt", size="M8", length=30, point=[lx + hx, ly + hy, p["foot_t"]], direction=[0, 0, 1], name=f"Schraube_{i}{tag}{int(hx)}")
            # Winkelhalter T23 (W11): Eckwinkel zwischen Beininnenflaeche (zum Holm hin) und Holmunterkante; Bein mit ly < 0 -> Winkel nach +Y, sonst um 180 Grad gedreht
            sgn = 1 if ly < 0 else -1
            wn = f"Winkelhalter_{i}{tag}"
            fy = round(ly + sgn * leg_w / 2, 3)
            b.add("component.insert_design", path="designs/components/winkelhalter.sc", name=wn)
            b.add("occurrence.move", occurrence=f"{wn}:1", translate=[lx, fy, round(zb, 3)], move_grounded=True)
            if sgn < 0:
                b.add("occurrence.move", occurrence=f"{wn}:1", axis=[0, 0, 1], angle="180 deg", origin=[lx, fy, round(zb, 3)], space="world", move_grounded=True)
        if G["art"] == "portal":
            yl = G["yl"]
            hlen = 2 * yl + leg_w
            member(b, f"Holm_{i}", dict(width=p["holm_w"], height=p["holm_h"], wall=lw), [x, 0, zh - p["holm_h"] / 2], [1, 0, 0], [0, 0, 1], hlen)
            member(b, f"Querstrebe_{i}", dict(width=leg_w, height=leg_w, wall=lw), [x, 0, p["strut_z"]], [1, 0, 0], [0, 0, 1], 2 * yl - leg_w)
            # Diagonalen (Flachstahl 25 x 3, ausserhalb der Beinflaeche, gekreuzt), je Ende eine Schraube M6x40 mit Mutter durch das Bein
            z0, z1 = p["strut_z"], zb - 40
            for sx, (ya, yb_) in ((1, (-yl, yl)), (-1, (yl, -yl))):
                dy, dz = yb_ - ya, z1 - z0
                ln = math.hypot(dy, dz)
                xo = x + sx * (leg_w / 2 + 1.5)
                member(b, f"Diagonale_{i}{'a' if sx > 0 else 'b'}", dict(width=3, height=25), [xo, ya, z0], [1, 0, 0], [0, dz / ln, -dy / ln], ln, symmetric=False, kind="bar")
                for yy, zz in ((ya, z0), (yb_, z1)):
                    b.add("parts.insert", family="hex_bolt", size="M6", length=40, point=[x + sx * (leg_w / 2 + 3), yy, zz], direction=[sx, 0, 0], name=f"SchraubeD_{i}{sx}{int(yy)}")
                    b.add("parts.insert", family="hex_nut", size="M6", point=[x - sx * leg_w / 2, yy, zz], direction=[-sx, 0, 0], name=f"MutterD_{i}{sx}{int(yy)}")
        else:       # Auslegerbock: Kragarm vom Pfosten (aussen, +Y) ueber den Pool bis hinter die innerste Rinne
            y_in = Wt / 2 + p["holm_overhang"]                       # Kragarm-Ende ueber dem Wasser (radial innen = +Y)
            yl = G["yl"]                                             # Pfosten aussen = -Y
            hlen = y_in - yl + leg_w / 2
            member(b, f"Kragarm_{i}", dict(width=p["holm_w"], height=p["holm_h"], wall=lw), [x, (yl - leg_w / 2 + y_in) / 2, zh - p["holm_h"] / 2], [1, 0, 0], [0, 0, 1], hlen)
        # Rinnenhalter: L-Winkel 3 mm je Rinnenseite, 25 breit, auf dem Holm neben der Rinnenwand, Schraube M5
        for r in rows:
            y = r["y"]
            for sy in (-1, 1):
                yc = y + sy * (65 + p["clip_t"] / 2)
                ytop = zh
                tag = f"{i}_Rinne_{r['k'] + 1}_{'L' if sy < 0 else 'R'}"
                b.add("solid.box", length=p["clip_len"], width=25, height=p["clip_t"], center=[x, y + sy * (65 + 12.5), ytop + p["clip_t"] / 2], operation="new", name=f"CH_{tag}", body_name=f"Halter_{tag}")
                b.add("solid.box", length=p["clip_len"], width=p["clip_t"], height=25, center=[x, yc, ytop + 12.5], operation="join", targets=[f"Halter_{tag}"], name=f"CV_{tag}")
                b.add("solid.cylinder", diameter=5.5, height=p["clip_t"] + 2, base=[x, y + sy * (65 + 15), ytop - 1], operation="cut", targets=[f"Halter_{tag}"], name=f"CB_{tag}")
                b.add("material.assign", bodies=[f"Halter_{tag}"], material="Stahl verzinkt")
                b.add("parts.insert", family="hex_bolt", size="M5", length=12, point=[x, y + sy * (65 + 15), ytop + p["clip_t"]], direction=[0, 0, 1], name=f"SchraubeH_{tag}")
    # --- Laengsstreben zwischen den Boecken (an den Beinen, auf strut_z)
    b.add("component.activate", component=root)
    b.add("component.create", name="T22c_Laengsstreben")
    sz = STRUT_Z.get(typ, p["strut_z"])
    ys = sorted(set(round(y, 3) for (_, y) in G["legs"]))
    for j, y in enumerate(ys):
        member(b, f"Laengs_{j + 1}", dict(width=leg_w, height=leg_w, wall=lw), [xb[0] + leg_w / 2, y, sz], [0, 1, 0], [0, 0, 1], xb[1] - xb[0] - leg_w, symmetric=False)
    # Laengsdiagonalen (Flachstahl 25 x 3, ausserhalb der Beine) je Beinseite zwischen den Boecken: Laengsaussteifung (Befund Bild-Kritiker W16)
    for j, y in enumerate(ys):
        zbs = zrow(xb[1]) - p["holm_h"] - p["foot_t"]
        z0_, z1_ = sz, zbs - 40
        dx_, dz_ = xb[1] - xb[0], z1_ - z0_
        ln_ = math.hypot(dx_, dz_)
        yo = y + (leg_w / 2 + 1.5) * (1 if y > 0 else -1)
        member(b, f"LDiag_{j + 1}", dict(width=3, height=25), [xb[0], round(yo, 3), z0_], [0, 1, 0], [-dz_ / ln_, 0, dx_ / ln_], ln_, symmetric=False, kind="bar")
    # --- Zulaufverteiler (-X): schraeges Rohr D25 entlang der Sektorgrenze, je Reihe Stutzen D16 und Schlauch zur Tuelle
    b.add("component.activate", component=root)
    b.add("component.create", name="T22d_Zulaufverteiler")
    ho = p["hdr_od"]
    dvec, kk = skew(1)
    y0, y1 = G["ymid"] - Wt / 2 - 60, G["ymid"] + Wt / 2 + 60
    hl = (y1 - y0) * kk
    xbd = lambda y, sgn: sgn * ((G["apc"] - y) * TG.T18 - G["gap"])          # Sektorgrenze (Aussenkante des Rohrs) bei y
    zi_row = {r["k"]: zrow(r["xc"] - r["L"] / 2) + 70 for r in rows}
    zi = sum(zi_row.values()) / len(rows)
    xh0 = xbd(y0, -1) + ho / 2 * kk
    b.add("solid.cylinder", diameter=ho, height=hl, base=[round(xh0, 3), y0, round(zi, 3)], axis=dvec, operation="new", name="VerteilerRohr", body_name="Verteiler")
    stubs = []
    for r in rows:
        y = r["y"]
        xend = r["xc"] - r["L"] / 2
        xt = xend - 29                                            # Tuellenspitze
        xs = xt - p["hose_gap"]                                   # Spitze der Verteilerstutzen
        xh = xbd(y, -1) + ho / 2 * kk                             # Rohrachse bei y
        stubs.append((r, xt, xs, xh))
        b.add("solid.cylinder", diameter=16, height=xs - xh, base=[round(xh, 3), y, round(zi, 3)], axis=[1, 0, 0], operation="join", targets=["Verteiler"], name=f"Stutzen_Rinne_{r['k'] + 1}")
    b.add("solid.cylinder", diameter=ho - 2 * p["hdr_wall"], height=hl + 2, base=[round(xh0 - dvec[0], 3), y0 - dvec[1], round(zi, 3)], axis=dvec, operation="cut", targets=["Verteiler"], name="VerteilerBohrung")
    for (r, xt, xs, xh) in stubs:
        b.add("solid.cylinder", diameter=12, height=xs - xh + 1, base=[round(xh, 3), r["y"], round(zi, 3)], axis=[1, 0, 0], operation="cut", targets=["Verteiler"], name=f"Bohr_Rinne_{r['k'] + 1}")
    b.add("solid.cylinder", diameter=ho - 2 * p["hdr_wall"] - 0.4, height=20, base=[round(xh0 + dvec[0] * 2, 3), y0 + dvec[1] * 2, round(zi, 3)], axis=dvec, operation="new", name="StopfenV", body_name="Endstopfen_Verteiler")
    b.add("material.assign", bodies=["Verteiler", "Endstopfen_Verteiler"], material="PVC blau")
    for (r, xt, xs, xh) in stubs:   # Schlauch ID 16 / AD 20 von der Stutzenspitze (minus 20) bis auf die Tuelle (20 mm)
        x0, x1 = xs - 20, xt + 20
        zz = round(zi_row[r["k"]], 3)
        b.add("solid.cylinder", diameter=p["hose_od"], height=x1 - x0, base=[x0, r["y"], zz], axis=[1, 0, 0], operation="new", name=f"SchlauchA_{r['k'] + 1}", body_name=f"Schlauch_Rinne_{r['k'] + 1}")
        b.add("solid.cylinder", diameter=16, height=x1 - x0 + 2, base=[x0 - 1, r["y"], zz], axis=[1, 0, 0], operation="cut", targets=[f"Schlauch_Rinne_{r['k'] + 1}"], name=f"SchlauchI_{r['k'] + 1}")
        b.add("material.assign", bodies=[f"Schlauch_Rinne_{r['k'] + 1}"], material="Schlauch hellblau")
    # --- Sammelablauf (+X): schraeges Rohr DN50 entlang der Sektorgrenze mit Muffen DN32 je Reihe
    b.add("component.activate", component=root)
    b.add("component.create", name="T22e_Sammelablauf")
    co = p["col_od"]
    dvec2, kk = skew(-1)
    za_row = {r["k"]: zrow(r["xc"] + r["L"] / 2) + 20 for r in rows}
    za = sum(za_row.values()) / len(rows)
    xc0 = xbd(y0, 1) - co / 2 * kk
    b.add("solid.cylinder", diameter=co, height=hl, base=[round(xc0, 3), y0, round(za, 3)], axis=dvec2, operation="new", name="SammelRohr", body_name="Sammelrohr")
    muffs = []
    for r in rows:
        xe = r["xc"] + r["L"] / 2
        xcp = xbd(r["y"], 1) - co / 2 * kk
        muffs.append((r, xe, xcp))
        b.add("solid.cylinder", diameter=40, height=xcp - (xe + 10), base=[round(xe + 10, 3), r["y"], round(za_row[r["k"]], 3)], axis=[1, 0, 0], operation="join", targets=["Sammelrohr"], name=f"Muffe_Rinne_{r['k'] + 1}")
    b.add("solid.cylinder", diameter=co - 2 * p["col_wall"], height=hl + 2, base=[round(xc0 - dvec2[0], 3), y0 - dvec2[1], round(za, 3)], axis=dvec2, operation="cut", targets=["Sammelrohr"], name="SammelBohrung")
    for (r, xe, xcp) in muffs:
        b.add("solid.cylinder", diameter=32, height=xcp - (xe + 10) + 1, base=[round(xe + 9, 3), r["y"], round(za_row[r["k"]], 3)], axis=[1, 0, 0], operation="cut", targets=["Sammelrohr"], name=f"MuffeBohr_Rinne_{r['k'] + 1}")
    b.add("solid.cylinder", diameter=co - 2 * p["col_wall"] - 0.4, height=20, base=[round(xc0 + dvec2[0] * 2, 3), y0 + dvec2[1] * 2, round(za, 3)], axis=dvec2, operation="new", name="StopfenS", body_name="Endstopfen_Sammelrohr")
    b.add("material.assign", bodies=["Sammelrohr", "Endstopfen_Sammelrohr"], material="PVC grau")
    b.add("component.activate", component=root)
    bock_ds = "Portalbock aus Rechteckrohr: 2 Beine ausserhalb der Beete, Fussplatten mit M8, Querholm, Querstrebe, Diagonalen, Rinnenhalter" if G["art"] == "portal" else "Auslegerbock: Pfosten ausserhalb des Pools, Fussplatte mit M8, Kragarm ueber das Wasser, Rinnenhalter"
    for nm, pn, ds in ((root, "T22", d["beschreibung"]), ("T22a_Bock_1", "T22a", bock_ds),
                       ("T22b_Rinnen", "T22b", "Rinnen je Reihe eigene Laenge, Zickzack-Phase A/B, geneigt 1,5 %"), ("T22c_Laengsstreben", "T22c", "Laengsstreben 40x40x3"),
                       ("T22d_Zulaufverteiler", "T22d", "Zulaufverteiler D25 schraeg entlang der Sektorgrenze mit n Stutzen und Schlaeuchen"), ("T22e_Sammelablauf", "T22e", "Sammelrohr DN50 schraeg mit n Muffen DN32")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="B", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, G

def render(typ, sc_path, G):
    r = os.path.join(sc.ROOT, "renders", "components", f"nft_tisch_{typ}")
    os.makedirs(r, exist_ok=True)
    zc, Lm = G["zc"], G["Lmin"]
    views = {"01-iso": ([G["rows"][0]["xc"], 0, zc / 2], 0.7, 0.4, Lm * 1.5 + 1800), "02-zulauf": ([G["rows"][0]["xc"] - Lm / 2, 0, zc], 0.9, 0.35, 1800),
             "03-bock": ([G["xb"][0], 0, zc / 2], 0.5, 0.3, 2200), "04-ablauf": ([G["rows"][0]["xc"] + Lm / 2, 0, zc], -2.3, 0.35, 1800),
             "05-oberseite": ([0, 0, zc], 0.0, 1.5, max(Lm, G["Wt"]) * 2.2), "06-querschnitt-bock": ([G["xb"][0], 0, zc / 2], 1.5708, 0.0, 3200)}
    for nme, (t, yaw, pitch, dist) in views.items():
        sc.snapshot(sc_path, os.path.join(r, f"nft_tisch_{typ}-{nme}.png"), t, yaw, pitch, dist, w=1000, h=650, section="YZ" if nme.startswith("06") else None)

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["innen", "mitte", "aussen"]
    for typ in typs:
        b, G = build(typ)
        out = os.path.join(sc.ROOT, "designs", "components", f"nft_tisch_{typ}.sc")
        sc.run(b.write(f"nft_tisch_{typ}"), out)
        sc.assign_part_materials(out, "Stahl verzinkt", r"Body\d+|Winkel( \(\d+\))?|winkelhalter( \(\d+\))?")      # Normteile und Winkelhalter-Instanzen tragen sonst Default 1,29 g/cm3
        import normteile_benennen   # W60 5a: Normteile Body<n> -> Schraube_M8x30_k usw. (Gestalt); Teiledaten data/parts/nft_tisch_<typ>.json folgen
        normteile_benennen.benennen(out)
        ev = sc.evaluate(out)
        mass = sum(x["mass_g"] for x in ev["bodies"])
        mn, mx = sc.bbox_all(ev)
        print(typ, "Koerper", len(ev["bodies"]), "Masse", round(mass / 1000, 1), "kg", [round(v) for v in mn], [round(v) for v in mx])
        if "--render" in sys.argv:
            render(typ, out, G)
