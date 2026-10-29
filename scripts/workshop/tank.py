"""Tank T40 (klein = Vortex-Absetzer, gross = Biofilter): Kegelboden 45 Grad auf Plattform mit 4 Beinen, tangentialer Zulauf, Leitrohr, Schlammventil an der Spitze.
Bezugspunkt: Mitte Standflaeche am Boden (Z=0). Aufruf: python scripts/workshop/tank.py [klein] [gross] [--render]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

def member(b, name, dims, origin, xdir, ydir, dist, symmetric=True, kind="rect_tube"):
    b.add("sketch.create", plane={"origin": origin, "x_dir": xdir, "y_dir": ydir}, name="S_" + name)
    b.add("frame.profile.insert", profile=dict(kind=kind, **dims), at=[0, 0], anchor="center")
    b.add("sketch.finish")
    ex = dict(distance=dist, name="F_" + name, body_name=name)
    if symmetric:
        ex["direction"] = "symmetric"
    b.add("solid.extrude", **ex)
    b.add("material.assign", bodies=[name], material="Stahl verzinkt")

def geometry(T, p):
    """Kegel 45 Grad (Spitze bei rt, z_t) bis zur Plattform-Oberkante; Zylinder darueber bis zur Tankoberkante."""
    R, w, rt = T["R"], T["wall"], T["rt"]
    z_t = T["z0"]                                         # tiefster Punkt des Tanks = OBJ-Spitze
    z_c = T["plat_z0"] + T["plat_t"]                       # Kegel endet auf der Plattform-Oberkante
    z_top = T["z0"] + T["H"]
    tan_a = (z_c - z_t) / (R - rt)
    ang = math.degrees(math.atan(tan_a))
    r_in = rt - w / math.sin(math.atan(tan_a))             # Innenkegel parallel (Wand w senkrecht)
    zc_i = z_t + (R - w - r_in) * tan_a
    return dict(R=R, w=w, rt=rt, z_t=z_t, z_c=z_c, z_top=z_top, tan_a=tan_a, ang=ang, r_in=r_in, zc_i=zc_i)

def build(typ):
    p, d = sc.load_params("tank")
    T = d["typen"][typ]
    G = geometry(T, p)
    R, w, rt, z_t, z_c, z_top = G["R"], G["w"], G["rt"], G["z_t"], G["z_c"], G["z_top"]
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    for k in ("R", "H", "z0", "wall", "rt", "plat_z0", "plat_t", "leg_h"):
        b.add("parameters.add", name=f"tank_{k}", expression=f"{T[k]} mm")
    b.add("material.create", name="PE Tank", density_g_cm3=0.95, color=d["werkstoff"]["farbe"])
    b.add("material.create", name="Stahl verzinkt", density_g_cm3=7.85, color="#aeb4b8", pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    b.add("material.create", name="PVC grau Tank", density_g_cm3=1.4, color="#8d9296")
    b.add("material.create", name="Ventil blau", density_g_cm3=1.3, color="#2a5da8")
    b.add("material.create", name="Biomedium", density_g_cm3=0.15, color="#c9b27a")
    root = f"T40_Tank_{typ}"
    b.add("component.create", name=root, grounded=True)
    # --- Tankkoerper: Kegel + Zylinder als EIN Rotationskoerper mit Wand
    b.add("component.create", name="T40a_Tank")
    b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [1, 0, 0], "y_dir": [0, 0, 1]}, name="Tankprofil")
    pts = [[G["r_in"], z_t], [rt, z_t], [R, z_c], [R, z_top], [R - w, z_top], [R - w, G["zc_i"]]]
    b.add("sketch.line", points=pts, closed=True)
    b.add("sketch.finish")
    b.add("solid.revolve", axis="y", angle="360 deg", name="Tankkoerper", body_name="Tank")
    # Zulauf: tangential, Rohr d50/63 Achse parallel +Y, Achsenabstand R - w - d/2 (innen tangential), Wanddurchbruch
    di = T["inlet_d"]
    z_in = z_top - p["inlet_below_top"]
    xin = R - w - di / 2
    yin = math.sqrt(R ** 2 - xin ** 2)                    # Schnittpunkt Achse mit Aussenwand (negative Seite)
    b.add("solid.cylinder", diameter=di, height=2 * yin + 40, base=[xin, -yin - 20, z_in], axis=[0, 1, 0], operation="cut", targets=["Tank"], name="Durchbruch_Zulauf")
    b.add("material.assign", bodies=["Tank"], material="PE Tank")
    # Deckel mit Leitrohr-Loch
    b.add("solid.cylinder", diameter=2 * R + 2 * p["lid_over"], height=p["lid_t"], base=[0, 0, z_top], operation="new", name="Deckel", body_name="Deckel")
    b.add("solid.cylinder", diameter=p["guide_d"] + 2, height=p["lid_t"] + 2, base=[0, 0, z_top - 1], operation="cut", targets=["Deckel"], name="Deckel_Leitrohrloch")
    if T["biofilter"]:
        b.add("solid.cylinder", diameter=p["air_d"], height=p["lid_t"] + 2, base=[R / 2, 0, z_top - 1], operation="cut", targets=["Deckel"], name="Deckel_Belueftung")
    b.add("material.assign", bodies=["Deckel"], material="PE Tank")
    # --- Zulaufrohr (tangential)
    b.add("component.activate", component=root)
    b.add("component.create", name="T40b_Zulauf")
    y0, y1 = -yin - 220, -yin + 40                       # 220 mm aussen, endet knapp hinter der Wand
    b.add("solid.cylinder", diameter=di, height=y1 - y0, base=[xin, y0, z_in], axis=[0, 1, 0], operation="new", name="Zulaufrohr_R", body_name="Zulaufrohr")
    b.add("solid.cylinder", diameter=di - 2 * p["pipe_wall"], height=y1 - y0 + 2, base=[xin, y0 - 1, z_in], axis=[0, 1, 0], operation="cut", targets=["Zulaufrohr"], name="Zulaufrohr_Bohrung")
    b.add("material.assign", bodies=["Zulaufrohr"], material="PVC grau Tank")
    # --- Leitrohr (Mittelrohr) mit Auslauf (nur Absetzer: Vortex)
    b.add("component.activate", component=root)
    b.add("component.create", name="T40c_Leitrohr")
    if not T["biofilter"]:
        gd, gw = p["guide_d"], p["guide_wall"]
        zg0 = z_top - p["guide_depth"]
        b.add("solid.cylinder", diameter=gd, height=p["guide_depth"] + p["lid_t"] + 70, base=[0, 0, zg0], operation="new", name="Leitrohr_R", body_name="Leitrohr")
        od = p["outlet_d"]
        b.add("solid.cylinder", diameter=od, height=gd / 2 + 140, base=[0, 0, z_top + p["lid_t"] + 35], axis=[1, 0, 0], operation="join", targets=["Leitrohr"], name="Auslauf_R")
        b.add("solid.cylinder", diameter=gd - 2 * gw, height=p["guide_depth"] + p["lid_t"] + 72, base=[0, 0, zg0 - 1], operation="cut", targets=["Leitrohr"], name="Leitrohr_Bohrung")
        b.add("solid.cylinder", diameter=od - 2 * p["pipe_wall"], height=gd / 2 + 142, base=[0, 0, z_top + p["lid_t"] + 35], axis=[1, 0, 0], operation="cut", targets=["Leitrohr"], name="Auslauf_Bohrung")
        b.add("material.assign", bodies=["Leitrohr"], material="PVC grau Tank")
    else:   # Biofilter: Biomediumkorb als EIN Koerper (Schuettung), Tragring, Belueftungsrohr
        rb = R - w - 25
        zb0 = z_top - p["bio_z_below_top"]
        b.add("solid.cylinder", diameter=2 * rb, height=p["bio_h"], base=[0, 0, zb0], operation="new", name="Biomedium_R", body_name="Biomedium")
        b.add("solid.cylinder", diameter=p["air_d"] + 2, height=p["bio_h"] + 2, base=[R / 2, 0, zb0 - 1], operation="cut", targets=["Biomedium"], name="Biomedium_Luftloch")
        b.add("material.assign", bodies=["Biomedium"], material="Biomedium")
        # Tragrost: Scheibe auf Konsolen an der Tankwand, 8 Schlitze (Wasserdurchtritt)
        b.add("solid.cylinder", diameter=2 * (R - w) - 2, height=10, base=[0, 0, zb0 - 10], operation="new", name="Tragrost_R", body_name="Tragrost")
        for k in range(4):
            b.add("solid.box", length=(2 * rb - 120), width=30, height=12, center=[0, (k - 1.5) * 100, zb0 - 5], operation="cut", targets=["Tragrost"], name=f"Rostschlitz_{k}")
        b.add("material.assign", bodies=["Tragrost"], material="PVC grau Tank")
        b.add("solid.cylinder", diameter=p["air_d"], height=z_top - zb0 + 120, base=[R / 2, 0, zb0 - 40], operation="new", name="Luftrohr_R", body_name="Belueftungsrohr")
        b.add("material.assign", bodies=["Belueftungsrohr"], material="PVC grau Tank")
    # --- Schlammventil an der Kegelspitze: Stutzen, Kugelhahn, Hebel
    b.add("component.activate", component=root)
    b.add("component.create", name="T40d_Schlammventil")
    vd, vl = T["valve_d"], p["valve_len"]
    b.add("solid.cylinder", diameter=vd, height=14, base=[0, 0, z_t - 12], operation="new", name="Stutzen_R", body_name="Schlammstutzen")
    b.add("solid.cylinder", diameter=vd - 8, height=16, base=[0, 0, z_t - 13], operation="cut", targets=["Schlammstutzen"], name="Stutzen_Bohrung")
    b.add("material.assign", bodies=["Schlammstutzen"], material="PVC grau Tank")
    b.add("solid.cylinder", diameter=vd + 16, height=vl, base=[0, 0, z_t - 12 - vl], operation="new", name="Hahn_R", body_name="Kugelhahn")
    b.add("solid.cylinder", diameter=vd - 8, height=vl + 2, base=[0, 0, z_t - 12 - vl - 1], operation="cut", targets=["Kugelhahn"], name="Hahn_Bohrung")
    b.add("solid.box", length=130, width=14, height=8, center=[(vd + 16) / 2 + 40, 0, z_t - 12 - vl / 2], operation="join", targets=["Kugelhahn"], name="Hahn_Hebel")
    b.add("material.assign", bodies=["Kugelhahn"], material="Ventil blau")
    b.add("solid.cylinder", diameter=vd, height=40, base=[0, 0, z_t - 12 - vl - 40], operation="new", name="Ablaufstutzen_R", body_name="Ablaufstutzen")
    b.add("solid.cylinder", diameter=vd - 8, height=42, base=[0, 0, z_t - 12 - vl - 41], operation="cut", targets=["Ablaufstutzen"], name="Ablauf_Bohrung")
    b.add("material.assign", bodies=["Ablaufstutzen"], material="PVC grau Tank")
    # --- Plattform mit Kegelsitz, Eckenaussparungen; Beine, Querstreben, Diagonalen, Fussplatten
    b.add("component.activate", component=root)
    b.add("component.create", name="T40e_Plattform")
    pl, pw, pt, pz = T["plat_l"], T["plat_w"], T["plat_t"], T["plat_z0"]
    lw = T["leg_w"]
    b.add("solid.box", length=pl, width=pw, height=pt, center=[0, 0, pz + pt / 2], operation="new", name="Platte", body_name="Plattform")
    b.add("solid.box", length=pl - 8, width=pw - 8, height=pt - 8, center=[0, 0, pz + pt / 2], operation="cut", targets=["Plattform"], name="Hohlraum")   # Blechkasten 4 mm, innen hohl
    cl = p["cone_clear"]
    r_at = lambda z: rt + (z - z_t) / G["tan_a"]
    b.add("solid.cone", radius=r_at(pz - 1) + cl, top_radius=r_at(pz + pt) + cl, height=pt + 1, base=[0, 0, pz - 1], operation="cut", targets=["Plattform"], name="Kegelsitz")
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.add("solid.box", length=lw + 1, width=lw + 1, height=pt + 2, center=[sx * (pl / 2 - lw / 2), sy * (pw / 2 - lw / 2), pz + pt / 2], operation="cut", targets=["Plattform"], name=f"Ecke_{sx}{sy}")
    b.add("material.assign", bodies=["Plattform"], material="Stahl verzinkt")
    b.add("component.activate", component=root)
    b.add("component.create", name="T40f_Beine")
    ft, fp = p["foot_t"], p["foot_plate"]
    legs = [(sx * (pl / 2 - lw / 2), sy * (pw / 2 - lw / 2)) for sx in (-1, 1) for sy in (-1, 1)]
    lh = T["leg_h"]
    for i, (lx, ly) in enumerate(legs, 1):
        member(b, f"Bein_{i}", dict(width=lw, height=lw, wall=T["leg_wall"]), [lx, ly, ft], [1, 0, 0], [0, 1, 0], lh - ft, symmetric=False)
        b.add("solid.box", length=fp, width=fp, height=ft, center=[lx, ly, ft / 2], operation="new", name=f"FP_{i}", body_name=f"Fussplatte_{i}")
        for hx, hy in ((-fp / 2 + 15, -fp / 2 + 15), (fp / 2 - 15, fp / 2 - 15)):
            b.add("solid.cylinder", diameter=p["foot_hole"], height=ft + 2, base=[lx + hx, ly + hy, -1], operation="cut", targets=[f"Fussplatte_{i}"], name=f"FL_{i}_{int(hx)}")
            b.add("parts.insert", family="hex_bolt", size="M8", length=30, point=[lx + hx, ly + hy, ft], direction=[0, 0, 1], name=f"Schraube_{i}_{int(hx)}")
        b.add("material.assign", bodies=[f"Fussplatte_{i}"], material="Stahl verzinkt")
    # Querstreben (4 Seiten) auf strut_z und Diagonalen (Flachstahl 25 x 3, 1 je Seite, ausserhalb der Beinflaeche)
    sz = T["strut_z"]
    ax = pl / 2 - lw / 2
    ay = pw / 2 - lw / 2
    for k, (cx, cy, dirx) in enumerate(((ax, 0, "x"), (-ax, 0, "x"), (0, ay, "y"), (0, -ay, "y")), 1):
        if dirx == "x":      # Strebe laeuft in Y
            member(b, f"Strebe_{k}", dict(width=lw, height=lw, wall=T["leg_wall"]), [cx, 0, sz], [1, 0, 0], [0, 0, 1], 2 * ay - lw)
        else:                # Strebe laeuft in X
            member(b, f"Strebe_{k}", dict(width=lw, height=lw, wall=T["leg_wall"]), [0, cy, sz], [0, 1, 0], [0, 0, 1], 2 * ax - lw)
    z0d, z1d = sz + lw / 2 + 10, pz - 40                      # Diagonale zwischen Strebe und Plattformunterkante
    for k, (sx, sy, along) in enumerate(((1, 0, "y"), (-1, 0, "y"), (0, 1, "x"), (0, -1, "x")), 1):
        half = ay if along == "y" else ax
        a0, a1 = -half, half
        dy, dz = a1 - a0, z1d - z0d
        ln = math.hypot(dy, dz)
        off = (lw / 2 + 1.5)
        if along == "y":
            member(b, f"Diagonale_{k}", dict(width=3, height=p["diag_w"]), [sx * (ax + off), a0, z0d], [1, 0, 0], [0, dz / ln, -dy / ln], ln, symmetric=False, kind="bar")
        else:
            member(b, f"Diagonale_{k}", dict(width=3, height=p["diag_w"]), [a0, sy * (ay + off), z0d], [0, 1, 0], [-dz / ln, 0, dy / ln], ln, symmetric=False, kind="bar")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T40", d["beschreibung"]), ("T40a_Tank", "T40a", "Tankkoerper Kegel 45 Grad + Zylinder, Deckel"), ("T40b_Zulauf", "T40b", "tangentialer Zulauf"),
                       ("T40c_Leitrohr", "T40c", "Leitrohr mit Auslauf (Vortex) bzw. Biomediumkorb (Biofilter)"), ("T40d_Schlammventil", "T40d", "Schlammventil an der Kegelspitze"),
                       ("T40e_Plattform", "T40e", "Plattform mit Kegelsitz"), ("T40f_Beine", "T40f", "4 Beine, Streben, Diagonalen, Fussplatten")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, G, dict(z_in=z_in, xin=xin, yin=yin)

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["klein", "gross"]
    for typ in typs:
        b, G, extra = build(typ)
        out = os.path.join(sc.ROOT, "designs", "components", f"tank_{typ}.sc")
        sc.run(b.write(f"tank_{typ}"), out)
        ev = sc.evaluate(out)
        print(typ, "Kegelwinkel %.1f Grad" % G["ang"], "Koerper", len(ev["bodies"]), "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 1), "kg")
        if "--render" in sys.argv:
            r = os.path.join(sc.ROOT, "renders", "components", f"tank_{typ}")
            os.makedirs(r, exist_ok=True)
            Hh = G["z_top"]
            for n, (t, yaw, pitch, dist) in {"01-iso": ([0, 0, Hh / 2], 0.7, 0.3, Hh * 3.2), "02-kegel": ([0, 0, G["z_t"] + 150], 0.7, 0.2, 1500), "03-zulauf": ([extra["xin"], -extra["yin"], extra["z_in"]], 0.4, 0.3, 900), "04-deckel": ([0, 0, Hh], 0.6, 0.7, 1500)}.items():
                sc.snapshot(out, os.path.join(r, f"tank_{typ}-{n}.png"), t, yaw, pitch, dist, w=1000, h=700)
            sc.snapshot(out, os.path.join(r, f"tank_{typ}-05-schnitt.png"), [0, 0, Hh / 2], 3.14159, 0.0, Hh * 2.6, w=900, h=900, section="XZ")
