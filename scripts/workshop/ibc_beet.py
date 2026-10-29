"""IBC-Beet T30 (aussen_933 / aussen_993 / innen_933): Wanne, Stuetzen, Siebboden, Medium (EIN Koerper), Glockensiphon, Zulaufrohr.
Bezugspunkt: Mitte Wannenunterseite. Aufruf: python scripts/workshop/ibc_beet.py [typ ...] [--render]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

def rrect(b, plane_z, w, l, r, name):
    """Skizze mit gerundetem Rechteck (Mitte im Ursprung) auf Ebene z = plane_z."""
    b.add("sketch.create", plane={"origin": [0, 0, plane_z], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name=name)
    b.add("sketch.rectangle.rounded", p0=[-l / 2, -w / 2], p1=[l / 2, w / 2], radius=r)

def tube(b, name, od, wall, base, axis, height, op="new", targets=None):
    kw = dict(diameter=od, height=height, base=base, axis=axis, operation=op, name="R_" + name)
    if op == "new":
        kw["body_name"] = name
    else:
        kw["targets"] = targets
    b.add("solid.cylinder", **kw)
    nb = name if op == "new" else targets[0]
    b.add("solid.cylinder", diameter=od - 2 * wall, height=height + 2, base=[base[i] - axis[i] for i in range(3)], axis=axis, operation="cut", targets=[nb], name="B_" + name)

def build(typ):
    p, d = sc.load_params("ibc_beet")
    T = d["typen"][typ]
    L, W, H = T["laenge"], T["breite"], T["hoehe"]
    wl, ft, cr, rw, rh = p["wall"], p["floor_t"], p["corner_r"], p["rim_w"], p["rim_h"]
    Lw, Ww = L - 2 * rw, W - 2 * rw               # Wandaussenmass; Randwulst bringt die Wanne auf das OBJ-Mass L x W
    Li, Wi = Lw - 2 * wl, Ww - 2 * wl
    z_ms = H - p["rim_gap"]                      # Medienoberflaeche
    z_m0 = z_ms - p["media_depth"]               # Medienunterkante = Oberkante Siebboden
    z_g0 = z_m0 - p["grid_t"]                    # Unterkante Siebboden
    x_sp = Li / 2 - 200                          # Siphon nahe dem Ablaufende (+X)
    y_in, z_in = -(Wi / 2 - 50), H - p["inflow_below_rim"]
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    b.add("parameters.add", name="beet_laenge", expression=f"{L} mm"); b.add("parameters.add", name="beet_breite", expression=f"{W} mm"); b.add("parameters.add", name="beet_hoehe", expression=f"{H} mm")
    b.add("material.create", name="HDPE weiss", density_g_cm3=0.95, color=d["werkstoff"]["farbe"])
    b.add("material.create", name="Medium Blaehton", density_g_cm3=d["medium"]["dichte_g_cm3"], color=d["medium"]["farbe"])
    b.add("material.create", name="PP grau", density_g_cm3=0.91, color="#9aa0a4")
    b.add("material.create", name="PVC grau Beet", density_g_cm3=1.4, color="#8d9296")
    root = f"T30_IBC_Beet_{typ}"
    b.add("component.create", name=root, grounded=True)
    # --- Wanne
    b.add("component.create", name="T30a_Wanne")
    rrect(b, 0, Ww, Lw, cr + wl, "Aussenform"); b.add("sketch.finish")
    b.add("solid.extrude", distance=H, name="Wannenkoerper", body_name="Wanne")
    rrect(b, H - rh, W, L, cr + wl + rw, "Randwulst"); b.add("sketch.finish")
    b.add("solid.extrude", distance=rh, operation="join", targets=["Wanne"], name="Randwulst")
    rrect(b, ft, Wi, Li, cr, "Innenraum"); b.add("sketch.finish")
    b.add("solid.extrude", distance=H - ft + 1, operation="cut", targets=["Wanne"], name="Innenraum_Ausschnitt")
    b.add("solid.cylinder", diameter=p["bulkhead_d"], height=ft + 2, base=[x_sp, 0, -1], operation="cut", targets=["Wanne"], name="Bohrung_Bulkhead")
    b.add("solid.cylinder", diameter=p["inflow_d"] + 2, height=wl + 4, base=[-Lw / 2 - 2, y_in, z_in], axis=[1, 0, 0], operation="cut", targets=["Wanne"], name="Durchfuehrung_Zulauf")
    b.add("material.assign", bodies=["Wanne"], material="HDPE weiss")
    # --- Stuetzen (Klotz 60 x 60 unter dem Siebboden), Raster nx x 2
    b.add("component.activate", component=root)
    b.add("component.create", name="T30b_Stuetzen")
    nx = int(p["post_nx"]) if L > 2500 else 3
    sx = (Li - 200) / (nx - 1)
    b.add("solid.box", length=p["post"], width=p["post"], height=z_g0 - ft, center=[-Li / 2 + 100, -(Wi / 2 - 100), ft + (z_g0 - ft) / 2], operation="new", name="Klotz", body_name="Stuetze")
    b.add("solid.pattern.rectangular", bodies=["Stuetze"], dir1=[1, 0, 0], count1=nx, spacing1=sx, dir2=[0, 1, 0], count2=2, spacing2=Wi - 200)
    b.add("material.assign", bodies=["Stuetze"] + [f"Stuetze ({k})" for k in range(2, 2 * nx + 1)], material="PP grau")
    # --- Siebboden
    b.add("component.activate", component=root)
    b.add("component.create", name="T30c_Siebboden")
    g = p["media_gap"]
    rrect(b, z_g0, Wi - 2 * g, Li - 2 * g, cr - g, "Siebboden_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["grid_t"], name="Siebblech", body_name="Siebboden")
    gx, gy = int(p["grid_nx"]), int(p["grid_ny"])
    sxg, syg = (Li - 400) / (gx - 1), (Wi - 400) / (gy - 1)
    b.add("solid.cylinder", diameter=p["grid_hole"], height=p["grid_t"] + 2, base=[-Li / 2 + 200, -Wi / 2 + 200, z_g0 - 1], operation="cut", targets=["Siebboden"], name="Sieb_Loch")
    b.add("solid.pattern.rectangular", features=["Sieb_Loch"], dir1=[1, 0, 0], count1=gx, spacing1=sxg, dir2=[0, 1, 0], count2=gy, spacing2=syg)
    b.add("solid.cylinder", diameter=p["bulkhead_d"] + 4, height=p["grid_t"] + 2, base=[x_sp, 0, z_g0 - 1], operation="cut", targets=["Siebboden"], name="Sieb_Standrohr")
    b.add("material.assign", bodies=["Siebboden"], material="PP grau")
    # --- Medium: EIN Koerper, Oberflaeche z_ms, Tiefe media_depth, Loch fuer den Medienschutz
    b.add("component.activate", component=root)
    b.add("component.create", name="T30d_Medium")
    rrect(b, z_m0, Wi - 2 * g, Li - 2 * g, cr - g, "Medium_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["media_depth"], name="Mediumblock", body_name="Medium")
    b.add("solid.cylinder", diameter=p["guard_d"], height=p["media_depth"] + 2, base=[x_sp, 0, z_m0 - 1], operation="cut", targets=["Medium"], name="Medium_Schutzloch")
    b.add("material.assign", bodies=["Medium"], material="Medium Blaehton")
    # --- Glockensiphon
    b.add("component.activate", component=root)
    b.add("component.create", name="T30e_Siphon")
    z_top = z_m0 + p["standpipe_over"]
    # Bulkhead: Huelse unter dem Boden bis Flansch auf dem Boden, Standrohr steckt darin
    tube(b, "Bulkhead", p["bulkhead_d"], (p["bulkhead_d"] - p["standpipe_d"]) / 2, [x_sp, 0, -30], [0, 0, 1], 30 + ft + 4)
    b.add("solid.cylinder", diameter=p["bulkhead_flange"], height=4, base=[x_sp, 0, ft], operation="join", targets=["Bulkhead"], name="Flansch")
    b.add("solid.cylinder", diameter=p["standpipe_d"], height=34 + ft + 4 + 1, base=[x_sp, 0, -31], operation="cut", targets=["Bulkhead"], name="Bulkhead_Sitz")
    b.add("material.assign", bodies=["Bulkhead"], material="PVC grau Beet")
    tube(b, "Standrohr", p["standpipe_d"], p["standpipe_wall"], [x_sp, 0, -30], [0, 0, 1], z_top + 30)
    b.add("material.assign", bodies=["Standrohr"], material="PVC grau Beet")
    # Glocke: oben geschlossen, 2 Schlitze 10 x 40, Luftloch D10
    tube(b, "Glocke", p["bell_d"], p["bell_wall"], [x_sp, 0, z_m0], [0, 0, 1], p["bell_h"])
    b.add("solid.cylinder", diameter=p["bell_d"], height=p["bell_wall"], base=[x_sp, 0, z_m0 + p["bell_h"] - p["bell_wall"]], operation="join", targets=["Glocke"], name="Glockendeckel")
    for sg, nm in ((1, "SchlitzA"), (-1, "SchlitzB")):
        b.add("solid.box", length=p["bell_wall"] + 8, width=p["bell_slot_w"], height=p["bell_slot_h"], center=[x_sp + sg * (p["bell_d"] / 2 - p["bell_wall"] / 2), 0, z_m0 + p["bell_slot_z"] + p["bell_slot_h"] / 2], operation="cut", targets=["Glocke"], name=nm)
    b.add("solid.box", length=p["air_hole"], width=p["bell_wall"] + 6, height=p["air_hole"], center=[x_sp, -(p["bell_d"] / 2 - p["bell_wall"] / 2), z_m0 + 50], operation="cut", targets=["Glocke"], name="Luftloch")
    b.add("material.assign", bodies=["Glocke"], material="PVC grau Beet")
    # Medienschutz: Rohr D110, Seitenloecher in zwei Ringen
    tube(b, "Medienschutz", p["guard_d"], p["guard_wall"], [x_sp, 0, z_m0], [0, 0, 1], p["guard_h"])
    # Seitenloecher als quadratische Durchbrueche (Box gegen Zylinder: schnell; Zylinder-Zylinder-Schnitte kosten >1 min je Loch)
    gh = p["guard_hole"]
    for zr in (40, 120, 200):
        for k, (dx, dy) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
            b.add("solid.box", length=(gh if dx == 0 else p["guard_wall"] + 6), width=(gh if dy == 0 else p["guard_wall"] + 6), height=gh,
                  center=[x_sp + dx * (p["guard_d"] / 2 - p["guard_wall"] / 2), dy * (p["guard_d"] / 2 - p["guard_wall"] / 2), z_m0 + zr], operation="cut", targets=["Medienschutz"], name=f"Schutzloch_{zr}_{k}")
    b.add("material.assign", bodies=["Medienschutz"], material="PVC grau Beet")
    # --- Zulaufrohr (Tropfrohr) laengs, durch die Stirnwand
    b.add("component.activate", component=root)
    b.add("component.create", name="T30f_Zulauf")
    x0, x1 = -Lw / 2 - 60, Li / 2 - 300
    tube(b, "Tropfrohr", p["inflow_d"], p["inflow_wall"], [x0, y_in, z_in], [1, 0, 0], x1 - x0)
    n_dr = int((x1 - (-Lw / 2 + 150)) // p["inflow_pitch"]) + 1
    ih = p["inflow_hole"]
    for k in range(n_dr):                           # Tropfloecher als Boxen durch die untere Rohrwand
        b.add("solid.box", length=ih, width=ih, height=p["inflow_wall"] + 4, center=[-Lw / 2 + 150 + k * p["inflow_pitch"], y_in, z_in - p["inflow_d"] / 2 + p["inflow_wall"] / 2], operation="cut", targets=["Tropfrohr"], name=f"Tropfloch_{k}")
    b.add("solid.cylinder", diameter=p["inflow_d"] - 2 * p["inflow_wall"] - 0.4, height=20, base=[x1 - 18, y_in, z_in], axis=[1, 0, 0], operation="new", name="Stopfen", body_name="Endstopfen_Zulauf")
    b.add("material.assign", bodies=["Tropfrohr", "Endstopfen_Zulauf"], material="PVC grau Beet")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T30", d["beschreibung"]), ("T30a_Wanne", "T30a", "Wanne halbe IBC mit Randwulst, Bohrungen"), ("T30b_Stuetzen", "T30b", "Stuetzklotz 60x60 unter dem Siebboden"),
                       ("T30c_Siebboden", "T30c", "Siebboden Lochblech 5 mm"), ("T30d_Medium", "T30d", "Medium Blaehton/Kies als ein Koerper"),
                       ("T30e_Siphon", "T30e", "Glockensiphon: Bulkhead, Standrohr d25, Glocke d75, Medienschutz d110"), ("T30f_Zulauf", "T30f", "Zulauf-Tropfrohr d20")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    info = dict(L=L, W=W, H=H, z_ms=z_ms, z_m0=z_m0, z_g0=z_g0, x_sp=x_sp, y_in=y_in, z_in=z_in, n_dr=n_dr, nx=nx)
    return b, info

def render(typ, path, info):
    r = os.path.join(sc.ROOT, "renders", "components", f"ibc_beet_{typ}")
    os.makedirs(r, exist_ok=True)
    L, H = info["L"], info["H"]
    Lw_ = L - 2 * 10
    views = {"01-iso": ([0, 0, H / 3], 0.6, 0.45, L * 1.25), "02-siphon": ([info["x_sp"], 0, info["z_m0"] + 120], 0.7, 0.5, 700),
             "03-zulauf": ([-Lw_ / 2 + 150, info["y_in"], info["z_in"]], 0.9, 0.4, 700), "04-medium": ([0, 0, info["z_ms"]], 0.3, 0.8, L * 0.9)}
    for n, (t, yaw, pitch, dist) in views.items():
        sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-{n}.png"), t, yaw, pitch, dist, w=1000, h=650)
    sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-05-schnitt.png"), [info["x_sp"] - 100, 0, H / 2], 3.14159, 0.0, 1300, w=1000, h=650, section="XZ")
    sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-06-schnitt-quer.png"), [0, 0, H / 2], 1.5708, 0.0, info["W"] * 2.2, w=900, h=650, section="YZ")

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["aussen_933", "aussen_993", "innen_933"]
    for typ in typs:
        b, info = build(typ)
        out = os.path.join(sc.ROOT, "designs", "components", f"ibc_beet_{typ}.sc")
        sc.run(b.write(f"ibc_beet_{typ}"), out)
        ev = sc.evaluate(out)
        for x in ev["bodies"]:
            print(typ, x["name"], round(x["volume_mm3"] / 1e6, 3), "l", round(x["mass_g"] / 1000, 2), "kg", x["faces"], "F")
        if "--render" in sys.argv:
            render(typ, out, info)
