"""NFT-Tisch T22 (aussen / mitte / innen): Rinnen mit Zickzack-Phase, Boecke, Laengsstreben, Zulaufverteiler, Sammelablauf.
Aufruf: python scripts/workshop/nft_tisch.py [typ ...] [--render]   (ohne Typ: alle drei)"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

STEEL = "#aeb4b8"

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

def build(typ):
    p, d = sc.load_params("nft_tisch")
    T = d["typen"][typ]
    n, rp, L, zc = T["n"], T["rinnen_abstand"], T["laenge"], T["z_rinne_mitte"]
    slope = p["slope_pct"] / 100.0
    ang = math.degrees(math.atan(slope))
    Wt = (n - 1) * rp + 130                                   # Tischbreite = Rinnenbreite + Abstaende
    yl = Wt / 2 - p["holm_overhang"] - p["leg_inset"]          # Beine bei +-yl
    holm_len = Wt + 2 * p["holm_overhang"]
    xb = [-(L / 2 - p["bock_inset"]), L / 2 - p["bock_inset"]]          # zwei Boecke = 4 Beine (Scope-Card nft_tisch)
    b = sc.Build()
    b.add("parameters.add", name="slope_pct", expression=str(p["slope_pct"]), unit="")
    for k in ("leg_w", "leg_wall", "holm_w", "holm_h", "strut_z"):
        b.add("parameters.add", name=k, expression=f"{p[k]} mm")
    b.add("parameters.add", name="rinnen_abstand", expression=f"{rp} mm")
    b.add("parameters.add", name="laenge", expression=f"{L} mm")
    b.add("parameters.add", name="z_rinne_mitte", expression=f"{zc} mm")
    b.add("parameters.add", name="n_rinnen", expression=str(n), unit="")
    b.add("material.create", name="Stahl verzinkt", density_g_cm3=7.85, color=STEEL, pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    b.add("material.create", name="PVC blau", density_g_cm3=1.4, color="#2a5da8")
    b.add("material.create", name="PVC grau", density_g_cm3=1.4, color="#8d9296")
    b.add("material.create", name="Schlauch hellblau", density_g_cm3=1.0, color="#7fc4ea")
    root = f"T22_NFT_Tisch_{typ}"
    b.add("component.create", name=root, grounded=True)
    # --- Rinnen (Phase A/B abwechselnd = Zickzack)
    b.add("component.create", name="T22b_Rinnen")
    rinne_names = []
    for k in range(n):
        y = (k - (n - 1) / 2) * rp
        phase = "ab"[k % 2]
        nm = f"Rinne_{k + 1}"
        rinne_names.append((nm, y, phase))
        b.add("component.insert_design", path=f"designs/components/nft_rinne_{T['rinne']}_{phase}.sc", name=nm)
        b.add("occurrence.move", occurrence=f"{nm}:1", translate=[0, y, zc])
        b.add("occurrence.move", occurrence=f"{nm}:1", axis=[0, 1, 0], angle=f"{ang:.5f} deg", origin=[0, y, zc], space="world")
    # --- Boecke
    for i, x in enumerate(xb, 1):
        zh = zc - x * slope                                     # Rinnenunterkante = Holmoberkante an dieser Stelle
        zb = zh - p["holm_h"]                                   # Holmunterkante = Beinoberkante
        leg_len = zb - p["foot_t"]
        b.add("component.activate", component=root)
        b.add("component.create", name=f"T22a_Bock_{i}")
        for sy, tag in ((-1, "L"), (1, "R")):
            member(b, f"Bein_{i}{tag}", dict(width=p["leg_w"], height=p["leg_w"], wall=p["leg_wall"]), [x, sy * yl, p["foot_t"]], [1, 0, 0], [0, 1, 0], leg_len, symmetric=False)
            # Fussplatte mit zwei Loechern und zwei Schrauben M8
            b.add("solid.box", length=p["foot_plate"], width=p["foot_plate"], height=p["foot_t"], center=[x, sy * yl, p["foot_t"] / 2], operation="new", name=f"FP_{i}{tag}", body_name=f"Fussplatte_{i}{tag}")
            for hx, hy in ((-25, -25), (25, 25)):
                b.add("solid.cylinder", diameter=p["foot_hole"], height=p["foot_t"] + 2, base=[x + hx, sy * yl + hy, -1], operation="cut", targets=[f"Fussplatte_{i}{tag}"], name=f"FL_{i}{tag}{hx}")
            b.add("material.assign", bodies=[f"Fussplatte_{i}{tag}"], material="Stahl verzinkt")
            for hx, hy in ((-25, -25), (25, 25)):
                b.add("parts.insert", family="hex_bolt", size="M8", length=30, point=[x + hx, sy * yl + hy, p["foot_t"]], direction=[0, 0, 1], name=f"Schraube_{i}{tag}{hx}")
        member(b, f"Holm_{i}", dict(width=p["holm_w"], height=p["holm_h"], wall=p["leg_wall"]), [x, 0, zh - p["holm_h"] / 2], [1, 0, 0], [0, 0, 1], holm_len)
        member(b, f"Querstrebe_{i}", dict(width=p["leg_w"], height=p["leg_w"], wall=p["leg_wall"]), [x, 0, p["strut_z"]], [1, 0, 0], [0, 0, 1], 2 * yl - p["leg_w"])
        # Diagonalen (Flachstahl 25 x 3, ausserhalb der Beinflaeche, gekreuzt), je Ende eine Schraube M6x40 mit Mutter durch das Bein
        z0, z1 = p["strut_z"], zb - 40
        for sx, (ya, yb_) in ((1, (-yl, yl)), (-1, (yl, -yl))):
            dy, dz = yb_ - ya, z1 - z0
            ln = math.hypot(dy, dz)
            xo = x + sx * (p["leg_w"] / 2 + 1.5)
            member(b, f"Diagonale_{i}{'a' if sx > 0 else 'b'}", dict(width=3, height=25), [xo, ya, z0], [1, 0, 0], [0, dz / ln, -dy / ln], ln, symmetric=False, kind="bar")
            for yy, zz in ((ya, z0), (yb_, z1)):
                b.add("parts.insert", family="hex_bolt", size="M6", length=40, point=[x + sx * (p["leg_w"] / 2 + 3), yy, zz], direction=[sx, 0, 0], name=f"SchraubeD_{i}{sx}{int(yy)}")
                b.add("parts.insert", family="hex_nut", size="M6", point=[x - sx * p["leg_w"] / 2, yy, zz], direction=[-sx, 0, 0], name=f"MutterD_{i}{sx}{int(yy)}")
        # Rinnenhalter: L-Winkel 3 mm je Rinnenseite, 25 breit, auf dem Holm neben der Rinnenwand, Schraube M5
        for (nm, y, ph) in rinne_names:
            for sy in (-1, 1):
                yc = y + sy * (65 + p["clip_t"] / 2)
                ytop = zh                                       # Holmoberkante
                tag = f"{i}_{nm}_{'L' if sy < 0 else 'R'}"
                # waagerechter Schenkel auf dem Holm (nach aussen von der Rinnenwand), senkrechter Schenkel an der Rinnenwand
                b.add("solid.box", length=p["clip_len"], width=25, height=p["clip_t"], center=[x, y + sy * (65 + 12.5), ytop + p["clip_t"] / 2], operation="new", name=f"CH_{tag}", body_name=f"Halter_{tag}")
                b.add("solid.box", length=p["clip_len"], width=p["clip_t"], height=25, center=[x, yc, ytop + 12.5], operation="join", targets=[f"Halter_{tag}"], name=f"CV_{tag}")
                b.add("solid.cylinder", diameter=5.5, height=p["clip_t"] + 2, base=[x, y + sy * (65 + 15), ytop - 1], operation="cut", targets=[f"Halter_{tag}"], name=f"CB_{tag}")
                b.add("material.assign", bodies=[f"Halter_{tag}"], material="Stahl verzinkt")
                b.add("parts.insert", family="hex_bolt", size="M5", length=12, point=[x, y + sy * (65 + 15), ytop + p["clip_t"]], direction=[0, 0, 1], name=f"SchraubeH_{tag}")
    # --- Laengsstreben zwischen den Boecken (an den Beinen, auf strut_z)
    b.add("component.activate", component=root)
    b.add("component.create", name="T22c_Laengsstreben")
    for i in range(len(xb) - 1):
        for sy, tag in ((-1, "L"), (1, "R")):
            member(b, f"Laengs_{i + 1}{tag}", dict(width=p["leg_w"], height=p["leg_w"], wall=p["leg_wall"]), [xb[i] + p["leg_w"] / 2, sy * yl, p["strut_z"]], [0, 1, 0], [0, 0, 1], xb[i + 1] - xb[i] - p["leg_w"], symmetric=False)
    # --- Zulaufverteiler (-X): Rohr D25 quer, n Stutzen D16, n Schlaeuche zu den Tuellen
    b.add("component.activate", component=root)
    b.add("component.create", name="T22d_Zulaufverteiler")
    xt = -(L / 2 + 29)                                            # Tuellenspitze (Rinne gerade betrachtet)
    z_in = lambda x: zc - x * slope + 70                          # Zulaufachse z an der Stirn
    zi = z_in(-L / 2)
    xs = xt - p["hose_gap"]                                       # Spitze der Verteilerstutzen
    xh = xs - 45 - p["hdr_od"] / 2                                # Achse des Verteilerrohrs
    ho = p["hdr_od"]
    hl = Wt + 2 * 60
    # Verteiler: erst Vollzylinder + Stutzen vereinigen (robust), dann Hauptbohrung und Stutzenbohrungen schneiden
    b.add("solid.cylinder", diameter=ho, height=hl, base=[xh, -hl / 2, zi], axis=[0, 1, 0], operation="new", name="VerteilerRohr", body_name="Verteiler")
    for (nm, y, ph) in rinne_names:
        b.add("solid.cylinder", diameter=16, height=xs - xh, base=[xh, y, zi], axis=[1, 0, 0], operation="join", targets=["Verteiler"], name=f"Stutzen_{nm}")
    b.add("solid.cylinder", diameter=ho - 2 * p["hdr_wall"], height=hl + 2, base=[xh, -hl / 2 - 1, zi], axis=[0, 1, 0], operation="cut", targets=["Verteiler"], name="VerteilerBohrung")
    for (nm, y, ph) in rinne_names:
        b.add("solid.cylinder", diameter=12, height=xs - xh + 1, base=[xh, y, zi], axis=[1, 0, 0], operation="cut", targets=["Verteiler"], name=f"Bohr_{nm}")
    b.add("solid.cylinder", diameter=ho - 2 * p["hdr_wall"] - 0.4, height=20, base=[xh, -hl / 2 + 2, zi], axis=[0, 1, 0], operation="new", name="StopfenV", body_name="Endstopfen_Verteiler")
    b.add("material.assign", bodies=["Verteiler", "Endstopfen_Verteiler"], material="PVC blau")
    for (nm, y, ph) in rinne_names:   # Schlauch ID 16 / AD 20 von der Stutzenspitze (minus 20) bis auf die Tuelle (20 mm)
        x0, x1 = xs - 20, xt + 20
        b.add("solid.cylinder", diameter=p["hose_od"], height=x1 - x0, base=[x0, y, zi], axis=[1, 0, 0], operation="new", name=f"SchlauchA_{nm}", body_name=f"Schlauch_{nm}")
        b.add("solid.cylinder", diameter=16, height=x1 - x0 + 2, base=[x0 - 1, y, zi], axis=[1, 0, 0], operation="cut", targets=[f"Schlauch_{nm}"], name=f"SchlauchI_{nm}")
        b.add("material.assign", bodies=[f"Schlauch_{nm}"], material="Schlauch hellblau")
    # --- Sammelablauf (+X): Rohr DN50 quer mit n Muffen DN32 auf den Ablaufstutzen
    b.add("component.activate", component=root)
    b.add("component.create", name="T22e_Sammelablauf")
    za = zc - L / 2 * slope + 20                                  # Ablaufachse an der +X-Stirn (tiefes Ende)
    xo = L / 2 + 34                                               # Stutzenspitze (4 Kappe + 30 Stutzen)
    co = p["col_od"]
    xc = xo + 5 + co / 2 - 10 + 0                                # Sammelrohrachse
    b.add("solid.cylinder", diameter=co, height=hl, base=[xc, -hl / 2, za], axis=[0, 1, 0], operation="new", name="SammelRohr", body_name="Sammelrohr")
    for (nm, y, ph) in rinne_names:
        b.add("solid.cylinder", diameter=40, height=xc - (L / 2 + 10), base=[L / 2 + 10, y, za], axis=[1, 0, 0], operation="join", targets=["Sammelrohr"], name=f"Muffe_{nm}")
    b.add("solid.cylinder", diameter=co - 2 * p["col_wall"], height=hl + 2, base=[xc, -hl / 2 - 1, za], axis=[0, 1, 0], operation="cut", targets=["Sammelrohr"], name="SammelBohrung")
    for (nm, y, ph) in rinne_names:
        b.add("solid.cylinder", diameter=32, height=xc - (L / 2 + 10) + 1, base=[L / 2 + 9, y, za], axis=[1, 0, 0], operation="cut", targets=["Sammelrohr"], name=f"MuffeBohr_{nm}")
    b.add("solid.cylinder", diameter=co - 2 * p["col_wall"] - 0.4, height=20, base=[xc, -hl / 2 + 2, za], axis=[0, 1, 0], operation="new", name="StopfenS", body_name="Endstopfen_Sammelrohr")
    b.add("material.assign", bodies=["Sammelrohr", "Endstopfen_Sammelrohr"], material="PVC grau")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T22", d["beschreibung"]), ("T22a_Bock_1", "T22a", "Bock aus Rechteckrohr: 2 Beine, Fussplatten mit M8, Querholm, Querstrebe, Rinnenhalter"),
                       ("T22b_Rinnen", "T22b", "Rinnen mit Zickzack-Phase A/B, geneigt 1 %"), ("T22c_Laengsstreben", "T22c", "Laengsstreben 30x30x2"),
                       ("T22d_Zulaufverteiler", "T22d", "Zulaufverteiler D25 mit n Stutzen und Schlaeuchen"), ("T22e_Sammelablauf", "T22e", "Sammelrohr DN50 mit n Muffen DN32")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, (n, rp, L, zc, Wt, xb, yl)

def render(typ, sc_path, info):
    n, rp, L, zc, Wt, xb, yl = info
    r = os.path.join(sc.ROOT, "renders", "components", f"nft_tisch_{typ}")
    os.makedirs(r, exist_ok=True)
    views = {"01-iso": ([0, 0, zc / 2], 0.7, 0.4, L * 1.5 + 1200), "02-zulauf": ([-L / 2, 0, zc], 0.9, 0.35, 1500),
             "03-bock": ([xb[0], 0, zc / 2], 0.5, 0.3, 1700), "04-ablauf": ([L / 2, 0, zc], -2.3, 0.35, 1500),
             "05-oberseite": ([0, 0, zc], 0.2, 1.0, Wt * 3)}
    for nme, (t, yaw, pitch, dist) in views.items():
        sc.snapshot(sc_path, os.path.join(r, f"nft_tisch_{typ}-{nme}.png"), t, yaw, pitch, dist, w=1000, h=650)

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["innen", "mitte", "aussen"]
    for typ in typs:
        b, info = build(typ)
        out = os.path.join(sc.ROOT, "designs", "components", f"nft_tisch_{typ}.sc")
        sc.run(b.write(f"nft_tisch_{typ}"), out)
        ev = sc.evaluate(out)
        mass = sum(x["mass_g"] for x in ev["bodies"])
        mn, mx = sc.bbox_all(ev)
        print(typ, "Koerper", len(ev["bodies"]), "Masse", round(mass / 1000, 1), "kg", [round(v) for v in mn], [round(v) for v in mx])
        if "--render" in sys.argv:
            render(typ, out, info)
