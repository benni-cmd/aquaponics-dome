"""Feinfilter T55 (W31, D51): Behaelter mit herausnehmbarem Siebkorb, Deckel mit Spannverschluessen, Standrahmen, Einlauf/Auslauf d50, Ablass d40 mit Kugelhahn.
Bezugspunkt: Mitte der Standflaeche am Boden; X Laengsachse (Einlauf -X, Auslauf +X), Y Tiefe (Ablass -Y), Z hoch. Aufruf: python scripts/workshop/feinfilter.py [--render]"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import sc

def box(b, name, size, center, mat, op="new", targets=None):
    if op == "new":
        b.add("solid.box", length=size[0], width=size[1], height=size[2], center=center, operation="new", name="R_" + name, body_name=name)
    else:
        b.add("solid.box", length=size[0], width=size[1], height=size[2], center=center, operation=op, targets=targets, name="R_" + name + "_" + op)
    if mat and op == "new":
        b.add("material.assign", bodies=[name], material=mat)

def tube(b, name, od, wall, base, axis, height, mat):
    b.add("solid.cylinder", diameter=od, height=height, base=base, axis=axis, operation="new", name="R_" + name, body_name=name)
    b.add("solid.cylinder", diameter=od - 2 * wall, height=height + 2, base=[base[i] - axis[i] for i in range(3)], axis=axis, operation="cut", targets=[name], name="B_" + name)
    b.add("material.assign", bodies=[name], material=mat)

def sqtube(b, name, size, wall, center, mat):
    """Vierkantrohr (Quadrat-Profil, Achse = laengste Seite): aussen size, Wand wall, durchgehende Bohrung."""
    ax = max(range(3), key=lambda i: size[i])
    box(b, name, size, center, mat)
    inner = [s - 2 * wall for s in size]
    inner[ax] = size[ax] + 2
    b.add("solid.box", length=inner[0], width=inner[1], height=inner[2], center=center, operation="cut", targets=[name], name="B_" + name)

def build(p, d):
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    for nm, col, dens in (("PP Feinfilter", "#cfd3d6", 0.91), ("PVC Feinfilter", "#8d9296", 1.4), ("Edelstahl Feinfilter", "#b8bec2", 7.9),
                          ("Netz Edelstahl Feinfilter", "#8f959a", p["mesh_density"]), ("Stahl verzinkt Feinfilter", "#a9aeb2", 7.85), ("EPDM Feinfilter", "#222222", 1.1)):
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    L, W, H, w = p["tank_l"], p["tank_w"], p["tank_h"], p["wall"]
    zb = p["foot_h"]                                    # Behaelterunterkante
    il, iw = L - 2 * w, W - 2 * w                        # Innenmasse
    root = "T55_Feinfilter"
    b.add("component.create", name=root, grounded=True)
    # --- T55a Standrahmen: 4 Beine, Ring und Mittelstege (Auflage des Bodens), Fussplatten
    b.add("component.create", name="T55a_Standrahmen")
    s, sw = p["leg"], p["leg_wall"]
    ex, ey = L / 2 - s / 2, W / 2 - s / 2                # Beinmitte
    n = 0
    for sx in (-1, 1):
        for sy in (-1, 1):
            n += 1
            sqtube(b, f"Bein_{n}", [s, s, zb - p["plate_t"]], sw, [sx * ex, sy * ey, p["plate_t"] + (zb - p["plate_t"]) / 2], "Stahl verzinkt Feinfilter")
            box(b, f"Fussplatte_{n}", [p["plate"], p["plate"], p["plate_t"]], [sx * ex, sy * ey, p["plate_t"] / 2], "Stahl verzinkt Feinfilter")
    for sy in (-1, 1):
        sqtube(b, f"Ring_X_{'v' if sy < 0 else 'h'}", [L - 2 * s, s, s], sw, [0, sy * ey, zb - s / 2], "Stahl verzinkt Feinfilter")
        sqtube(b, f"Steg_X_{'v' if sy < 0 else 'h'}", [L - 2 * s, s, s], sw, [0, sy * ey, p["brace_z"]], "Stahl verzinkt Feinfilter")
    for sx in (-1, 1):
        sqtube(b, f"Ring_Y_{'l' if sx < 0 else 'r'}", [s, W - 2 * s, s], sw, [sx * ex, 0, zb - s / 2], "Stahl verzinkt Feinfilter")
    for i, xm in enumerate((-p["bar_dx"], 0, p["bar_dx"])):
        sqtube(b, f"Auflage_Y_{i + 1}", [s, W - 2 * s, s], sw, [xm, 0, zb - s / 2], "Stahl verzinkt Feinfilter")
    # --- T55b Behaelter (PP, Wand 5): Wanne, Auflageleisten, Gaenge fuer Einlauf/Auslauf/Ablass
    b.add("component.activate", component=root)
    b.add("component.create", name="T55b_Behaelter")
    box(b, "Behaelter", [L, W, H], [0, 0, zb + H / 2], "PP Feinfilter")
    b.add("solid.box", length=il, width=iw, height=H, center=[0, 0, zb + w + H / 2], operation="cut", targets=["Behaelter"], name="B_Behaelter")
    lw, lt, lz = p["ledge_w"], p["ledge_t"], zb + p["ledge_z"]
    ll = p["basket_l"]                                  # Leisten tragen den Flansch entlang der langen Wand
    for sy in (-1, 1):
        box(b, "Leiste_%s" % ("v" if sy < 0 else "h"), [ll, lw + 1, lt], [0, sy * (iw / 2 - lw / 2 + 0.5), lz - lt / 2], None, op="join", targets=["Behaelter"])
    zi, zo, zd = zb + p["inlet_z"], zb + p["outlet_z"], zb + p["drain_z"]
    b.add("solid.cylinder", diameter=p["inlet_d"], height=w + 2, base=[-L / 2 - 1, 0, zi], axis=[1, 0, 0], operation="cut", targets=["Behaelter"], name="Loch_Einlauf")
    b.add("solid.cylinder", diameter=p["outlet_d"], height=w + 2, base=[L / 2 - w - 1, 0, zo], axis=[1, 0, 0], operation="cut", targets=["Behaelter"], name="Loch_Auslauf")
    b.add("solid.cylinder", diameter=p["drain_d"], height=w + 2, base=[p["drain_x"], -W / 2 - 1, zd], axis=[0, 1, 0], operation="cut", targets=["Behaelter"], name="Loch_Ablass")
    # --- T55c Siebkorb: Flansch (Edelstahl 3 mm), Gewebehuelle, Eckstaebe, Bodenrahmen, Buegelgriffe
    b.add("component.activate", component=root)
    b.add("component.create", name="T55c_Siebkorb")
    bl, bw, bd, ft, fr = p["basket_l"], p["basket_w"], p["basket_d"], p["flange_t"], p["flange_ring"]
    zf = lz                                              # Flansch-Unterkante = Leistenoberkante
    box(b, "Korbflansch", [bl + 2 * fr, bw + 2 * fr, ft], [0, 0, zf + ft / 2], "Edelstahl Feinfilter")
    b.add("solid.box", length=bl, width=bw, height=ft + 2, center=[0, 0, zf + ft / 2], operation="cut", targets=["Korbflansch"], name="B_Korbflansch")
    zk0 = zf + ft - bd                                   # Korbunterkante
    box(b, "Korbgewebe", [bl, bw, bd], [0, 0, zk0 + bd / 2], "Netz Edelstahl Feinfilter")
    mt = p["mesh_t"]
    b.add("solid.box", length=bl - 2 * mt, width=bw - 2 * mt, height=bd, center=[0, 0, zk0 + mt + bd / 2], operation="cut", targets=["Korbgewebe"], name="B_Korbgewebe")
    r = p["rod"]
    n = 0
    for sx in (-1, 1):
        for sy in (-1, 1):
            n += 1
            box(b, f"Korbstab_{n}", [r, r, bd - mt], [sx * (bl / 2 - mt - r / 2), sy * (bw / 2 - mt - r / 2), zk0 + mt + (bd - mt) / 2], "Edelstahl Feinfilter")
    for sy in (-1, 1):
        box(b, f"Korbrahmen_X_{'v' if sy < 0 else 'h'}", [bl - 2 * mt - 2 * r, r, r], [0, sy * (bw / 2 - mt - r / 2), zk0 + mt + r / 2], "Edelstahl Feinfilter")
    for sx in (-1, 1):
        box(b, f"Korbrahmen_Y_{'l' if sx < 0 else 'r'}", [r, bw - 2 * mt - 2 * r, r], [sx * (bl / 2 - mt - r / 2), 0, zk0 + mt + r / 2], "Edelstahl Feinfilter")
    gh, gd, gx = p["handle_h"], p["handle_d"], p["handle_dx"]
    for sy in (-1, 1):
        nm = "Korbgriff_%s" % ("v" if sy < 0 else "h")
        gy = sy * (bw / 2 + fr / 2)
        for sx in (-1, 1):
            b.add("solid.cylinder", diameter=8, height=gh, base=[sx * gx, gy, zf + ft], axis=[0, 0, 1], operation="new" if sx < 0 else "join",
                  name=("R_" + nm) if sx < 0 else "Pfosten_%s" % nm, **({"body_name": nm} if sx < 0 else {"targets": [nm]}))
        b.add("solid.cylinder", diameter=gd, height=2 * gx + gd, base=[-gx - gd / 2, gy, zf + ft + gh], axis=[1, 0, 0], operation="join", targets=[nm], name="Buegel_" + nm)
        b.add("material.assign", bodies=[nm], material="Edelstahl Feinfilter")
    # --- T55d Deckel: Dichtung EPDM, Deckelplatte PP, Griff, vier Spannverschluesse (Bock + Hebel)
    b.add("component.activate", component=root)
    b.add("component.create", name="T55d_Deckel")
    zr = zb + H
    gt, lt2 = p["gasket_t"], p["lid_t"]
    box(b, "Dichtung", [L, W, gt], [0, 0, zr + gt / 2], "EPDM Feinfilter")
    b.add("solid.box", length=il, width=iw, height=gt + 2, center=[0, 0, zr + gt / 2], operation="cut", targets=["Dichtung"], name="B_Dichtung")
    zl = zr + gt
    box(b, "Deckel", [L + 2 * p["lid_over"], W + 2 * p["lid_over"], lt2], [0, 0, zl + lt2 / 2], "PP Feinfilter")
    gz = zl + lt2
    box(b, "Deckelgriff", [14, 14, 20], [-50, 0, gz + 10], "PP Feinfilter")
    box(b, "Deckelgriff_2", [14, 14, 20], [50, 0, gz + 10], None, op="join", targets=["Deckelgriff"])
    box(b, "Deckelgriff_3", [114, 20, 14], [0, 0, gz + 27], None, op="join", targets=["Deckelgriff"])
    n = 0
    for sy in (-1, 1):
        for sx in (-1, 1):
            n += 1
            yb = sy * (W / 2 + p["latch_t"] / 2)
            box(b, f"Spannbock_{n}", [p["latch_w"], p["latch_t"], p["latch_h"]], [sx * p["latch_dx"], yb, zr - p["latch_h"] / 2 + 2], "Edelstahl Feinfilter")
            box(b, f"Spannhebel_{n}", [p["latch_w"] - 6, 6, p["latch_h"] + 20], [sx * p["latch_dx"], sy * (W / 2 + p["latch_t"] + 3), zr - p["latch_h"] / 2 + 2 + 10], "Edelstahl Feinfilter")
    # --- T55e Anschluesse: Einlauf mit Innenwinkel, Auslauf-Durchfuehrung mit Dichtflanschen, Ablass mit Kugelhahn und Schlauchtuelle
    b.add("component.activate", component=root)
    b.add("component.create", name="T55e_Anschluesse")
    idn, wd = p["inlet_d"], p["wall_d50"]
    xe, xi = -L / 2 - p["inlet_out"], -p["inlet_in"]
    ylen = (xi - xe) + idn / 2
    b.add("solid.cylinder", diameter=idn, height=ylen, base=[xe, 0, zi], axis=[1, 0, 0], operation="new", name="R_Einlauf", body_name="Einlaufrohr")
    b.add("solid.cylinder", diameter=idn, height=idn / 2 + p["inlet_down"], base=[xi, 0, zi - p["inlet_down"]], axis=[0, 0, 1], operation="join", targets=["Einlaufrohr"], name="Einlauf_senkrecht")
    b.add("solid.cylinder", diameter=idn - 2 * wd, height=(xi - xe) + 1, base=[xe - 1, 0, zi], axis=[1, 0, 0], operation="cut", targets=["Einlaufrohr"], name="B_Einlauf_waagerecht")
    b.add("solid.cylinder", diameter=idn - 2 * wd, height=p["inlet_down"] + (idn - 2 * wd) / 2 + 1, base=[xi, 0, zi - p["inlet_down"] - 1], axis=[0, 0, 1], operation="cut", targets=["Einlaufrohr"], name="B_Einlauf_senkrecht")
    b.add("material.assign", bodies=["Einlaufrohr"], material="PVC Feinfilter")
    odn = p["outlet_d"]
    xa0, xa1 = L / 2 - w - p["outlet_collar_t"], L / 2 + p["outlet_out"]
    tube(b, "Auslaufrohr", odn, wd, [xa0, 0, zo], [1, 0, 0], xa1 - xa0, "PVC Feinfilter")
    for nm, xs in (("Auslauf_Flansch_innen", L / 2 - w - p["outlet_collar_t"]), ("Auslauf_Mutter_aussen", L / 2)):
        tube(b, nm, p["outlet_collar_d"], (p["outlet_collar_d"] - odn) / 2, [xs, 0, zo], [1, 0, 0], p["outlet_collar_t"], "PVC Feinfilter")
    dd, wd4 = p["drain_d"], p["wall_d40"]
    xd = p["drain_x"]
    y0, y1, y2 = -W / 2 + w + p["drain_in"], -W / 2 - p["drain_stub"], -W / 2 - p["drain_stub"] - p["valve_l"]
    tube(b, "Ablassstutzen", dd, wd4, [xd, y0, zd], [0, -1, 0], y0 - y1, "PVC Feinfilter")
    tube(b, "Kugelhahn_Ablass", p["valve_d"], (p["valve_d"] - 28) / 2, [xd, y1, zd], [0, -1, 0], y1 - y2, "PVC Feinfilter")
    box(b, "Kugelhahn_Hebel", [p["valve_lever"], 10, 8], [xd + p["valve_lever"] / 2 - 5, (y1 + y2) / 2, zd + p["valve_d"] / 2 + 4], "Stahl verzinkt Feinfilter")
    tube(b, "Schlauchtuelle", dd, wd4, [xd, y2, zd], [0, -1, 0], p["barb_l"], "PVC Feinfilter")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T55", d["beschreibung"]), ("T55a_Standrahmen", "T55a", "Standrahmen Vierkantrohr 30x30x2 verzinkt"), ("T55b_Behaelter", "T55b", "Behaelter PP 400x300x500, Wand 5, Leisten, Durchfuehrungen"),
                       ("T55c_Siebkorb", "T55c", "Siebkorb Edelstahl mit Gewebe, Flansch, Griffen"), ("T55d_Deckel", "T55d", "Deckel PP mit Dichtung EPDM, Griff, 4 Spannverschluesse"), ("T55e_Anschluesse", "T55e", "Einlauf d50, Auslauf d50, Ablass d40 mit Kugelhahn")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, dict(zb=zb, H=H, L=L, W=W, zi=zi, zo=zo, zd=zd, zl=zl)

def render(path, info):
    r = os.path.join(sc.ROOT, "renders", "components", "feinfilter")
    os.makedirs(r, exist_ok=True)
    zc = (info["zb"] + info["H"]) / 2
    views = {"01-iso": ([0, 0, zc], 2.5, 0.35, 1900), "02-vorn": ([0, 0, zc], 0.0, 0.2, 1700), "03-einlauf": ([-200, 0, info["zi"]], 2.2, 0.3, 700), "04-ablass": ([info["L"] / 2 - 200, -230, info["zd"]], 0.4, 0.3, 700)}
    for n, (tt, yaw, pitch, dist) in views.items():
        sc.snapshot(path, os.path.join(r, f"feinfilter-{n}.png"), tt, yaw, pitch, dist, w=1000, h=700)
    sc.snapshot(path, os.path.join(r, "feinfilter-05-schnitt.png"), [0, 0, zc], 0.0, 0.0, 1700, w=1000, h=700, section="XZ")

if __name__ == "__main__":
    p, d = sc.load_params("feinfilter")
    b, info = build(p, d)
    out = os.path.join(sc.ROOT, "designs", "components", "feinfilter.sc")
    sc.run(b.write("feinfilter"), out)
    ev = sc.evaluate(out)
    print("feinfilter Koerper", len(ev["bodies"]), "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 2), "kg")
    if "--render" in sys.argv:
        render(out, info)
