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
    R, w, rt = T["R"] - p["rim_w"], T["wall"], T["rt"]      # R = Radius des Koerpers; der Randwulst bringt den Aussenradius auf T["R"] (OBJ-Mass)
    z_t = T["z0"]                                         # tiefster Punkt des Tanks = OBJ-Spitze
    z_c = T["plat_z0"] + T["plat_t"]                       # Kegel endet auf der Plattform-Oberkante
    z_top = T["z0"] + T["H"]
    tan_a = (z_c - z_t) / (R - rt)
    ang = math.degrees(math.atan(tan_a))
    r_in = rt - w / math.sin(math.atan(tan_a))             # Innenkegel parallel (Wand w senkrecht)
    zc_i = z_t + (R - w - r_in) * tan_a
    return dict(R=R, w=w, rt=rt, z_t=z_t, z_c=z_c, z_top=z_top, tan_a=tan_a, ang=ang, r_in=r_in, zc_i=zc_i)

def bed_geometry(T, p, G):
    """Schwebebett (W32): Ring am Konus, Bettunterkante ueber dem Ring, Oberkante z_m aus Volumen = fill x water_l (Frustum + Zylinder - Luftrohr-Loch, 3 mm Spalt zur Wand)."""
    R, w, z_t, tan_a, r_in, zc_i = G["R"], G["w"], G["z_t"], G["tan_a"], G["r_in"], G["zc_i"]
    rr = R / 2                                            # Ring-Radius = Lage des Luftrohrs (x = R/2)
    ar = p["air_ring_d"] / 2
    z_ring = z_t + (rr + ar + p["ring_clear"] - r_in) * tan_a
    z0b = z_ring + ar + 2
    ins = p["bed_inset"]
    r0 = r_in + (z0b - z_t) / tan_a - ins
    r1 = R - w - ins
    h = zc_i - z0b
    v_f = math.pi * h / 3 * (r0 * r0 + r0 * r1 + r1 * r1)
    a_h = math.pi / 4 * (p["air_d"] + 2) ** 2
    target = p["fill"] * p["water_l"] * 1e6
    z_m = (target - v_f + math.pi * r1 * r1 * zc_i - a_h * z0b) / (math.pi * r1 * r1 - a_h)
    return dict(rr=rr, z_ring=z_ring, z0b=z0b, r0=r0, r1=r1, z_m=z_m, target_mm3=target)

def build(typ):
    p, d = sc.load_params("tank")
    T = d["typen"][typ]
    G = geometry(T, p)
    R, w, rt, z_t, z_c, z_top = G["R"], G["w"], G["rt"], G["z_t"], G["z_c"], G["z_top"]    # R = Koerperradius (ohne Randwulst)
    RR = T["R"]                                                                           # Aussenradius mit Randwulst
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
    pts = [[G["r_in"], z_t], [rt, z_t], [R, z_c], [R, z_top - p["rim_h"]], [RR, z_top - p["rim_h"]], [RR, z_top], [R - w, z_top], [R - w, G["zc_i"]]]
    b.add("sketch.line", points=pts, closed=True)
    b.add("sketch.finish")
    b.add("solid.revolve", axis="y", angle="360 deg", name="Tankkoerper", body_name="Tank")
    # Zulauf: tangential, Rohr d50/63 Achse parallel +Y, Achsenabstand R - w - d/2 (innen tangential), Wanddurchbruch
    di = T["inlet_d"]
    z_in = z_top - p["inlet_below_top"]
    xin = R - w - di / 2
    yin = math.sqrt(R ** 2 - xin ** 2)                    # Schnittpunkt Achse mit Aussenwand (negative Seite)
    b.add("solid.cylinder", diameter=di, height=2 * yin + 40, base=[xin, -yin - 20, z_in], axis=[0, 1, 0], operation="cut", targets=["Tank"], name="Durchbruch_Zulauf")
    if not T["biofilter"]:                                # Auslauf-Durchbruch d50 radial +X
        b.add("solid.cylinder", diameter=p["outlet_d"], height=w + 40, base=[R - w - 20, 0, z_top - p["outlet_below_top"]], axis=[1, 0, 0], operation="cut", targets=["Tank"], name="Durchbruch_Auslauf")
    if T["biofilter"]:                                    # Ueberlauf-Durchbruch d63 radial +X, 80 mm unter dem Rand
        b.add("solid.cylinder", diameter=p["outlet_d"] + 13, height=w + 40, base=[R - w - 20, 0, z_top - p["outlet_below_top"]], axis=[1, 0, 0], operation="cut", targets=["Tank"], name="Durchbruch_Ueberlauf")
    b.add("material.assign", bodies=["Tank"], material="PE Tank")
    # Deckel mit Leitrohr-Loch
    b.add("solid.cylinder", diameter=2 * RR + 2 * p["lid_over"], height=p["lid_t"], base=[0, 0, z_top], operation="new", name="Deckel", body_name="Deckel")
    b.add("solid.cylinder", diameter=p["guide_d"] + 2, height=p["lid_t"] + 2, base=[0, 0, z_top - 1], operation="cut", targets=["Deckel"], name="Deckel_Leitrohrloch")
    b.add("solid.cylinder", diameter=p["rev_d"], height=p["lid_t"] + 2, base=[-R / 2, 0, z_top - 1], operation="cut", targets=["Deckel"], name="Deckel_Revision")
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
        zg0 = z_t + (z_top - z_c) * p["guide_bottom_f"]                 # R09: ca. 1/3 der Zylinderhoehe ueber der Kegelspitze
        zo = z_top - p["outlet_below_top"]
        od = p["outlet_d"]
        b.add("solid.cylinder", diameter=gd, height=z_top + p["lid_t"] + 70 - zg0, base=[0, 0, zg0], operation="new", name="Leitrohr_R", body_name="Leitrohr")
        b.add("solid.cylinder", diameter=gd - 2 * gw, height=z_top + p["lid_t"] + 72 - zg0, base=[0, 0, zg0 - 1], operation="cut", targets=["Leitrohr"], name="Leitrohr_Bohrung")
        b.add("solid.cylinder", diameter=od - 2 * p["pipe_wall"], height=gw + 6, base=[gd / 2 - gw - 2, 0, zo], axis=[1, 0, 0], operation="cut", targets=["Leitrohr"], name="Leitrohr_Auslassloch")
        b.add("material.assign", bodies=["Leitrohr"], material="PVC grau Tank")
        # Auslaufrohr radial +X von der Leitrohrwand durch die Tankwand (100 mm unter dem Rand)
        x_a0 = gd / 2
        b.add("solid.cylinder", diameter=od, height=R + 130 - x_a0, base=[x_a0, 0, zo], axis=[1, 0, 0], operation="new", name="Auslaufrohr_R", body_name="Auslaufrohr")
        b.add("solid.cylinder", diameter=od - 2 * p["pipe_wall"], height=R + 132 - x_a0, base=[x_a0 - 1, 0, zo], axis=[1, 0, 0], operation="cut", targets=["Auslaufrohr"], name="Auslaufrohr_Bohrung")
        b.add("material.assign", bodies=["Auslaufrohr"], material="PVC grau Tank")
    else:   # Biofilter (W32, D55): Ueberlauf radial +X, Schwebebett aus losen K1-Traegern (EIN Koerper, fill x Wasserfuellung), Belueftungsgitter am Konus, Rueckhaltesiebe an Zulauf und Ueberlauf
        zo = z_top - p["outlet_below_top"]
        od = p["outlet_d"] + 13                         # d63
        b.add("solid.cylinder", diameter=od, height=w + 150, base=[R - w - 20, 0, zo], axis=[1, 0, 0], operation="new", name="Ueberlauf_R", body_name="Ueberlauf")
        b.add("solid.cylinder", diameter=od - 2 * p["pipe_wall"], height=w + 152, base=[R - w - 21, 0, zo], axis=[1, 0, 0], operation="cut", targets=["Ueberlauf"], name="Ueberlauf_Bohrung")
        b.add("material.assign", bodies=["Ueberlauf"], material="PVC grau Tank")
        BG = bed_geometry(T, p, G)
        # Schwebebett: Rotationskoerper des Innenprofils (3 mm Spalt zur Wand) von z0b bis z_m, Volumen = fill x water_l; Luftrohr-Loch
        b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [1, 0, 0], "y_dir": [0, 0, 1]}, name="S_Schwebebett")
        b.add("sketch.line", points=[[0, round(BG["z0b"], 3)], [round(BG["r0"], 3), round(BG["z0b"], 3)], [round(BG["r1"], 3), round(G["zc_i"], 3)], [round(BG["r1"], 3), round(BG["z_m"], 3)], [0, round(BG["z_m"], 3)]], closed=True)
        b.add("sketch.finish")
        b.add("solid.revolve", axis="y", angle="360 deg", name="Schwebebett", body_name="Biomedium")
        b.add("solid.cylinder", diameter=p["air_d"] + 2, height=BG["z_m"] - BG["z0b"] + 2, base=[R / 2, 0, BG["z0b"] - 1], operation="cut", targets=["Biomedium"], name="Biomedium_Luftloch")
        b.add("material.assign", bodies=["Biomedium"], material="Biomedium")
        # Belueftungsgitter am Konusboden: Ring (Rohr D20) mit zwei Kreuzarmen; Steigrohr D16 am Ring bis ueber den Deckel
        ar, rr, zr = p["air_ring_d"] / 2, BG["rr"], BG["z_ring"]
        b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [1, 0, 0], "y_dir": [0, 0, 1]}, name="S_Belueftungsring")
        b.add("sketch.circle.center", center=[round(rr, 3), round(zr, 3)], radius=ar)
        b.add("sketch.finish")
        b.add("solid.revolve", axis="y", angle="360 deg", name="Belueftungsring", body_name="Belueftungsgitter")
        b.add("solid.cylinder", diameter=2 * ar - 2, height=2 * rr, base=[-rr, 0, zr], axis=[1, 0, 0], operation="join", targets=["Belueftungsgitter"], name="Gitter_Arm_X")
        b.add("solid.cylinder", diameter=2 * ar - 2, height=2 * rr, base=[0, -rr, zr], axis=[0, 1, 0], operation="join", targets=["Belueftungsgitter"], name="Gitter_Arm_Y")
        b.add("material.assign", bodies=["Belueftungsgitter"], material="PVC grau Tank")
        b.add("solid.cylinder", diameter=p["air_d"], height=z_top + p["lid_t"] + 80 - (zr + ar), base=[rr, 0, zr + ar], operation="new", name="Luftrohr_R", body_name="Belueftungsrohr")
        b.add("material.assign", bodies=["Belueftungsrohr"], material="PVC grau Tank")
        # Zulaufsieb: Schlitzkappe auf dem Rohrende im Tank (Scheibe D = Zulauf-D, 4 mm, 5 Schlitze); beruehrt das Rohrende
        y1s = -yin + 40
        b.add("solid.cylinder", diameter=di, height=4, base=[xin, y1s, z_in], axis=[0, 1, 0], operation="new", name="Zulaufsieb_R", body_name="Zulaufsieb")
        for k in range(5):
            b.add("solid.box", length=di - 20, width=8, height=p["screen_slot"], center=[xin, y1s + 2, z_in + (k - 2) * 2 * p["screen_slot"]], operation="cut", targets=["Zulaufsieb"], name=f"Sieb_Schlitz_{k}")
        b.add("material.assign", bodies=["Zulaufsieb"], material="Stahl verzinkt")
        # Auslaufsieb: Kappe D110 (Wand 2, Boden 3) ueber dem Ueberlaufrohr; Flanschring stuetzt sie am Rohr, Ende 0,1 mm vor der Wand
        sdm, sl = p["screen_d"], p["screen_l"]
        x_end = math.sqrt((R - w) ** 2 - (sdm / 2) ** 2) - 0.1
        x_beg = x_end - sl
        b.add("solid.cylinder", diameter=sdm, height=sl, base=[x_beg, 0, zo], axis=[1, 0, 0], operation="new", name="Auslaufsieb_R", body_name="Auslaufsieb")
        b.add("solid.cylinder", diameter=sdm - 4, height=sl - 3 + 1, base=[x_beg + 3, 0, zo], axis=[1, 0, 0], operation="cut", targets=["Auslaufsieb"], name="Auslaufsieb_Hohl")
        b.add("solid.cylinder", diameter=sdm - 3, height=3, base=[x_end - 6, 0, zo], axis=[1, 0, 0], operation="join", targets=["Auslaufsieb"], name="Auslaufsieb_Flansch")
        b.add("solid.cylinder", diameter=od + 0.0, height=4, base=[x_end - 6 - 0.5, 0, zo], axis=[1, 0, 0], operation="cut", targets=["Auslaufsieb"], name="Auslaufsieb_Rohrsitz")
        b.add("material.assign", bodies=["Auslaufsieb"], material="Stahl verzinkt")
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
    if T["biofilter"]:
        # --- Stuetzrippen (Dreiecksknaggen, Kantholz 44 mm) radial unter dem Kegel, von der Plattform-Unterkante bis rib_z0 (Orchestrator-Entscheidung 29.10.: Klasse Tank)
        b.add("component.activate", component=root)
        b.add("component.create", name="T40g_Stuetzrippen")
        b.add("material.create", name="Holz Fichte", density_g_cm3=0.47, color="#c8a46a")
        zr0, zr1 = p["rib_z0"], T["plat_z0"]
        r_c = lambda z: rt + (z - z_t) / G["tan_a"]
        angs = d["rippenwinkel"]["wert"]
        for k, a_ in enumerate(angs, 1):
            ph = math.radians(T["rib_phase"] + a_)
            cx, sy = math.cos(ph), math.sin(ph)
            b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [round(cx, 6), round(sy, 6), 0], "y_dir": [0, 0, 1]}, name=f"S_Rippe{k}")
            b.add("sketch.line", points=[[round(r_c(zr0) + p["rib_gap"], 2), zr0], [p["rib_r_out"], zr0], [p["rib_r_out"], zr1], [round(r_c(zr1) + p["rib_gap"], 2), zr1]], closed=True)
            b.add("sketch.finish")
            b.add("solid.extrude", distance=p["rib_t"], direction="symmetric", name=f"F_Rippe{k}", body_name=f"Stuetzrippe_{k}")
            b.add("material.assign", bodies=[f"Stuetzrippe_{k}"], material="Holz Fichte")
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
        ln0 = math.hypot(dy, dz)
        sh = lw / 2 + 8                                       # Enden an den Beinkanten enden lassen
        a0 += sh * dy / ln0; z0d_ = z0d + sh * dz / ln0
        dy, dz = dy * (1 - 2 * sh / ln0), dz * (1 - 2 * sh / ln0)
        ln = math.hypot(dy, dz)
        off = (lw / 2 + 1.5)
        if along == "y":
            member(b, f"Diagonale_{k}", dict(width=3, height=p["diag_w"]), [sx * (ax + off), a0, z0d_], [1, 0, 0], [0, dz / ln, -dy / ln], ln, symmetric=False, kind="bar")
        else:
            member(b, f"Diagonale_{k}", dict(width=3, height=p["diag_w"]), [a0, sy * (ay + off), z0d_], [0, 1, 0], [-dz / ln, 0, dy / ln], ln, symmetric=False, kind="bar")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T40", d["beschreibung"]), ("T40a_Tank", "T40a", "Tankkoerper Kegel 45 Grad + Zylinder, Deckel"), ("T40b_Zulauf", "T40b", "tangentialer Zulauf"),
                       ("T40c_Leitrohr", "T40c", "Leitrohr mit Auslauf (Vortex) bzw. Schwebebett mit Belueftungsgitter und Sieben (Biofilter)"), ("T40d_Schlammventil", "T40d", "Schlammventil an der Kegelspitze"),
                       ("T40e_Plattform", "T40e", "Plattform mit Kegelsitz"), ("T40f_Beine", "T40f", "4 Beine, Streben, Diagonalen, Fussplatten")) + ((("T40g_Stuetzrippen", "T40g", "5 Stuetzrippen (Kantholz 44) radial unter dem Kegel"),) if T["biofilter"] else ()):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="B" if T["biofilter"] else "A", properties={"Werkstoff": d["werkstoff"]["name"]})
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
