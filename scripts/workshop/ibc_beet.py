"""IBC-Beet T30 (aussen_933 / aussen_993 / aussen_800 / innen_933): Wanne, Stuetzen, Sperrboden (V3, ungelocht), Medium (EIN Koerper), Glockensiphon mit Kerben, Medienschutz, Reinigungsschacht, Reduktion, Zulaufrohr.
Bezugspunkt: Mitte Wannenunterseite. Aufruf: python scripts/workshop/ibc_beet.py [typ ...] [--render]"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(__file__))
import sc

def rrect(b, plane_z, w, l, r, name):
    """Skizze mit gerundetem Rechteck (Mitte im Ursprung) auf Ebene z = plane_z."""
    b.add("sketch.create", plane={"origin": [0, 0, plane_z], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name=name)
    b.add("sketch.rectangle.rounded", p0=[-l / 2, -w / 2], p1=[l / 2, w / 2], radius=r)

def crect(b, plane_z, w, l, c, name):
    """Skizze mit rechteckigem Umriss und 45-Grad-Fasen der Eckenschenkel c (Mitte im Ursprung) auf Ebene z = plane_z (W26/D44)."""
    pts = []
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        pts += [[sx * l / 2, sy * (w / 2 - c)], [sx * (l / 2 - c), sy * w / 2]] if sx * sy > 0 else [[sx * (l / 2 - c), sy * w / 2], [sx * l / 2, sy * (w / 2 - c)]]
    pts = [[round(x, 3), round(y, 3)] for x, y in pts]
    b.add("sketch.create", plane={"origin": [0, 0, plane_z], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name=name)
    b.add("sketch.line", points=pts, closed=True)

def tube(b, name, od, wall, base, axis, height, op="new", targets=None):
    kw = dict(diameter=od, height=height, base=base, axis=axis, operation=op, name="R_" + name)
    if op == "new":
        kw["body_name"] = name
    else:
        kw["targets"] = targets
    b.add("solid.cylinder", **kw)
    nb = name if op == "new" else targets[0]
    b.add("solid.cylinder", diameter=od - 2 * wall, height=height + 2, base=[base[i] - axis[i] for i in range(3)], axis=axis, operation="cut", targets=[nb], name="B_" + name)

def shaft_cell(L, W, u_ziel):
    """M-BEET-TAUSCH 0c: Lage (x, y) des Reinigungsschachts auf einer ZELLMITTE des Netztopf-Rasters (gen_dome.bed_pot_grid: pot_pitch, pot_margin aus data/params.json, Raster symmetrisch zur Beetmitte, (u laengs, v quer)):
    je vier Toepfe im Abstand pitch*sqrt(2)/2 (92 mm, Soll >= Schachtradius 55 + Kragenradius 32 = 87). u: Zellmitte nahe u_ziel (alte Lage -Li/2 + 250); v: Zellmitte nahe 0 (ungerade Zeilenzahl: +pitch/2)."""
    P = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8"))
    pitch, mar = P["pot_pitch"]["value"], P["pot_margin"]["value"]
    nu, nv = int((L - 2 * mar) // pitch) + 1, int((W - 2 * mar) // pitch) + 1
    us = [(i - (nu - 1) / 2) * pitch + pitch / 2 for i in range(nu - 1)]      # Zellmitten laengs
    vs = [(j - (nv - 1) / 2) * pitch + pitch / 2 for j in range(nv - 1)]      # Zellmitten quer
    u = min(us, key=lambda x: (abs(x - u_ziel), x))
    v = min(vs, key=lambda x: (abs(x), -x))
    return u, v

def build(typ):
    p, d = sc.load_params("ibc_beet")
    T = d["typen"][typ]
    L, W, H = T["laenge"], T["breite"], T["hoehe"]
    wl, ft, cr, rw, rh = p["wall"], p["floor_t"], p["corner_r"], p["rim_w"], p["rim_h"]
    Lw, Ww = L - 2 * rw, W - 2 * rw               # Wandaussenmass; Randwulst bringt die Wanne auf das OBJ-Mass L x W
    Li, Wi = Lw - 2 * wl, Ww - 2 * wl
    fase = T.get("fase", 0)                      # Eckenfase am Randwulst-Umriss (innen_933: 120, D44); Innenkonturen parallel versetzt
    def rr(b_, z, w, l, r, name):
        if not fase:
            return rrect(b_, z, w, l, r, name)
        d_ = (W - w) / 2.0                       # Versatz gegen den Randwulst-Umriss
        return crect(b_, z, w, l, fase - d_ * (2 - math.sqrt(2)), name)
    z_ms = H - p["rim_gap"]                      # Medienoberflaeche
    z_m0 = z_ms - p["media_depth"]               # Medienunterkante = Oberkante Siebboden
    z_g0 = z_m0 - p["grid_t"]                    # Unterkante Siebboden
    x_sp = Li / 2 - 200                          # Siphon nahe dem Ablaufende (+X)
    x_sh, y_sh = shaft_cell(L, W, -Li / 2 + 250)  # Reinigungsschacht am Zulaufende (T30e-5), auf einer Zellmitte des Topfrasters (M-BEET-TAUSCH 0c; vorher x = -Li/2 + 250, y = 0: Toepfe in der Schachtwand)
    y_in, z_in = -(Wi / 2 - 50), H - p["inflow_below_rim"]
    if fase:                                     # Zulauf durch die gerade Stirnwand: y_in vor dem Beginn der Eckenfase (Befund Spec-Pruefer W26: bei y -392 lag die Wand schraeg und das Rohr ohne Loch)
        y_in = -(Ww / 2 - (fase - ((W - Ww) / 2.0) * (2 - math.sqrt(2))) - 40)
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    b.add("parameters.add", name="beet_laenge", expression=f"{L} mm"); b.add("parameters.add", name="beet_breite", expression=f"{W} mm"); b.add("parameters.add", name="beet_hoehe", expression=f"{H} mm")
    b.add("material.create", name="HDPE weiss", density_g_cm3=0.95, color=d["werkstoff"]["farbe"])
    b.add("material.create", name="Medium Blaehton", density_g_cm3=d["medium"]["dichte_g_cm3"], color=d["medium"]["farbe"])
    b.add("material.create", name="PP grau", density_g_cm3=0.91, color="#9aa0a4")
    b.add("material.create", name="PVC grau Beet", density_g_cm3=1.4, color="#8d9296")
    b.add("material.create", name="V2A Lochblech", density_g_cm3=7.9, color="#c3c8cc")
    root = f"T30_IBC_Beet_{typ}"
    b.add("component.create", name=root, grounded=True)
    # --- Wanne
    b.add("component.create", name="T30a_Wanne")
    rr(b, 0, Ww, Lw, cr + wl, "Aussenform"); b.add("sketch.finish")
    b.add("solid.extrude", distance=H, name="Wannenkoerper", body_name="Wanne")
    rr(b, H - rh, W, L, cr + wl + rw, "Randwulst"); b.add("sketch.finish")
    b.add("solid.extrude", distance=rh, operation="join", targets=["Wanne"], name="Randwulst")
    rr(b, ft, Wi, Li, cr, "Innenraum"); b.add("sketch.finish")
    b.add("solid.extrude", distance=H - ft + 1, operation="cut", targets=["Wanne"], name="Innenraum_Ausschnitt")
    b.add("solid.cylinder", diameter=p["bulkhead_d"], height=ft + 2, base=[x_sp, 0, -1], operation="cut", targets=["Wanne"], name="Bohrung_Bulkhead")
    b.add("solid.cylinder", diameter=p["inflow_d"] + 2, height=wl + 4, base=[-Lw / 2 - 2, y_in, z_in], axis=[1, 0, 0], operation="cut", targets=["Wanne"], name="Durchfuehrung_Zulauf")
    b.add("material.assign", bodies=["Wanne"], material="HDPE weiss")
    # --- Stuetzen (Klotz 60 x 60 unter dem Siebboden), Raster nx x 2
    b.add("component.activate", component=root)
    b.add("component.create", name="T30b_Stuetzen")
    nx = int(p["post_nx"]) if L > 2500 else 5
    sx = (Li - 200) / (nx - 1)
    b.add("solid.box", length=p["post"], width=p["post"], height=z_g0 - ft, center=[-Li / 2 + 100, -(Wi / 2 - 100), ft + (z_g0 - ft) / 2], operation="new", name="Klotz", body_name="Stuetze")
    b.add("solid.pattern.rectangular", bodies=["Stuetze"], dir1=[1, 0, 0], count1=nx, spacing1=sx, dir2=[0, 1, 0], count2=3, spacing2=(Wi - 200) / 2)
    b.add("material.assign", bodies=["Stuetze"] + [f"Stuetze ({k})" for k in range(2, 3 * nx + 1)], material="PP grau")
    # --- Siebboden
    b.add("component.activate", component=root)
    b.add("component.create", name="T30c_Siebboden")
    g = p["media_gap"]
    rr(b, z_g0, Wi - 2 * g, Li - 2 * g, cr - g, "Siebboden_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["grid_t"], name="Siebblech", body_name="Siebboden")
    # W40-BEET V3 (D77): Sperrboden OHNE Lochung (kein Wasserraum unter dem Medium); einzige Oeffnung = Durchfuehrung d36 fuer die Plattenhuelse
    b.add("solid.cylinder", diameter=p["bulkhead_d"], height=p["grid_t"] + 2, base=[x_sp, 0, z_g0 - 1], operation="cut", targets=["Siebboden"], name="Sieb_Standrohr")
    b.add("material.assign", bodies=["Siebboden"], material="PP grau")
    # --- Medium: EIN Koerper, Oberflaeche z_ms, Tiefe media_depth, Loch fuer den Medienschutz
    b.add("component.activate", component=root)
    b.add("component.create", name="T30d_Medium")
    rr(b, z_m0, Wi - 2 * g, Li - 2 * g, cr - g, "Medium_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["media_depth"], name="Mediumblock", body_name="Medium")
    b.add("solid.cylinder", diameter=p["guard_d"], height=p["media_depth"] + 2, base=[x_sp, 0, z_m0 - 1], operation="cut", targets=["Medium"], name="Medium_Schutzloch")
    b.add("solid.cylinder", diameter=p["shaft_d"], height=p["media_depth"] + 2, base=[x_sh, y_sh, z_m0 - 1], operation="cut", targets=["Medium"], name="Medium_Schachtloch")
    b.add("material.assign", bodies=["Medium"], material="Medium Blaehton")
    # --- Glockensiphon
    b.add("component.activate", component=root)
    b.add("component.create", name="T30e_Siphon")
    z_top = z_m0 + p["standpipe_over"]
    # Bulkhead: Huelse unter dem Boden bis Flansch auf dem Boden, Standrohr steckt darin
    # D77: Tankverbinder (Klebemuffe d32) mit Reduzierhuelse 32/25 fuer das Standrohr d25; Tankverbinder bleibt D36 mit Flansch D50
    bid, bd = p["bulkhead_id"], p["bulkhead_d"]
    tube(b, "Bulkhead", bd, (bd - bid) / 2, [x_sp, 0, -30], [0, 0, 1], 30 + ft + 4)
    b.add("solid.cylinder", diameter=p["bulkhead_flange"], height=4, base=[x_sp, 0, ft], operation="join", targets=["Bulkhead"], name="Flansch")
    b.add("solid.cylinder", diameter=bid, height=34 + ft + 4 + 1, base=[x_sp, 0, -31], operation="cut", targets=["Bulkhead"], name="Bulkhead_Sitz")
    b.add("material.assign", bodies=["Bulkhead"], material="PVC grau Beet")
    tube(b, "Reduzierhuelse_Boden", bid, (bid - p["standpipe_d"]) / 2, [x_sp, 0, -30], [0, 0, 1], 30 + ft + 4)
    b.add("material.assign", bodies=["Reduzierhuelse_Boden"], material="PVC grau Beet")
    # Plattenhuelse im Sperrboden: gleicher Tankverbinder, Flansch D50 auf der Wasserseite (Plattenoberkante), 3 mm Gewinde unter der Platte fuer die Kontermutter
    zp0, zp1 = z_g0 - 3, z_m0 + 4
    tube(b, "Plattenhuelse", bd, (bd - bid) / 2, [x_sp, 0, zp0], [0, 0, 1], zp1 - zp0)
    b.add("solid.cylinder", diameter=p["bulkhead_flange"], height=4, base=[x_sp, 0, z_m0], operation="join", targets=["Plattenhuelse"], name="Flansch_Platte")
    b.add("solid.cylinder", diameter=bid, height=zp1 - zp0 + 2, base=[x_sp, 0, zp0 - 1], operation="cut", targets=["Plattenhuelse"], name="Plattenhuelse_Sitz")
    b.add("material.assign", bodies=["Plattenhuelse"], material="PVC grau Beet")
    tube(b, "Reduzierhuelse_Platte", bid, (bid - p["standpipe_d"]) / 2, [x_sp, 0, zp0], [0, 0, 1], zp1 - zp0)
    b.add("material.assign", bodies=["Reduzierhuelse_Platte"], material="PVC grau Beet")
    # Reduktion kurz d40 x d25 (T30e-3): Klebemuffe d25 oben (Port z -30), Stutzen d40 unten; Bauhoehe 50 mm [A], Kaufmass pruefen
    rz = p["reduktion_h"]
    tube(b, "Reduktion", 34, (34 - p["standpipe_d"]) / 2, [x_sp, 0, -30 - 20], [0, 0, 1], 20)
    b.add("solid.cylinder", diameter=46, height=15, base=[x_sp, 0, -30 - 35], operation="join", targets=["Reduktion"], name="Reduktion_Uebergang")
    b.add("solid.cylinder", diameter=p["reduktion_stutzen_d"], height=rz - 35, base=[x_sp, 0, -30 - rz], operation="join", targets=["Reduktion"], name="Reduktion_Stutzen")
    b.add("solid.cylinder", diameter=22, height=rz + 2, base=[x_sp, 0, -30 - rz - 1], operation="cut", targets=["Reduktion"], name="Reduktion_Bohrung")
    b.add("material.assign", bodies=["Reduktion"], material="PVC grau Beet")
    tube(b, "Standrohr", p["standpipe_d"], p["standpipe_wall"], [x_sp, 0, -30], [0, 0, 1], z_top + 30)
    b.add("material.assign", bodies=["Standrohr"], material="PVC grau Beet")
    # Glocke: oben geschlossen, 2 Schlitze 10 x 40, Luftloch D10
    tube(b, "Glocke", p["bell_d"], p["bell_wall"], [x_sp, 0, z_m0], [0, 0, 1], p["bell_h"])
    b.add("solid.cylinder", diameter=p["bell_d"], height=p["bell_wall"], base=[x_sp, 0, z_m0 + p["bell_h"] - p["bell_wall"]], operation="join", targets=["Glocke"], name="Glockendeckel")
    # V3: 4 Kerben 10 x 12 am Fuss (z_m0 bis z_m0 + 12) statt 2 hoher Schlitze; Box beginnt 1 mm unter der Platte (Schnitt nur im Ziel Glocke)
    kh, kz = p["bell_slot_h"], p["bell_slot_z"]
    for k, (dx, dy) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
        b.add("solid.box", length=(p["bell_slot_w"] if dx == 0 else p["bell_wall"] + 8), width=(p["bell_slot_w"] if dy == 0 else p["bell_wall"] + 8), height=kh + 1,
              center=[x_sp + dx * (p["bell_d"] / 2 - p["bell_wall"] / 2), dy * (p["bell_d"] / 2 - p["bell_wall"] / 2), z_m0 + kz - 1 + (kh + 1) / 2], operation="cut", targets=["Glocke"], name=f"Kerbe_{k}")
    b.add("solid.box", length=p["air_hole"], width=p["bell_wall"] + 6, height=p["air_hole"], center=[x_sp, -(p["bell_d"] / 2 - p["bell_wall"] / 2), z_m0 + 50], operation="cut", targets=["Glocke"], name="Luftloch")
    b.add("material.assign", bodies=["Glocke"], material="PVC grau Beet")
    # Medienschutz S-A (R51 T30e-4, D77 Lochblech 5 mm vom Metallbauer): Rohr d110 x 1,5 V2A, h 320, lose Kappe.
    # Modellvereinfachung: real Rundloch d5 Teilung 8 (35 % offen); im Modell 2 Ringe x 12 Schlitze 5 x 50 (6000 mm2 = 15,8 x Standrohr). Box durch die Wand, dann kreisfoermig gemustert.
    tube(b, "Medienschutz", p["guard_d"], p["guard_wall"], [x_sp, 0, z_m0], [0, 0, 1], p["guard_h"])
    for ri, zr in enumerate((p["guard_ring_z1"], p["guard_ring_z2"])):
        b.add("solid.box", length=p["guard_wall"] + 6, width=p["guard_slot_w"], height=p["guard_slot_h"], center=[x_sp + p["guard_d"] / 2 - p["guard_wall"] / 2, 0, z_m0 + zr + p["guard_slot_h"] / 2],
              operation="cut", targets=["Medienschutz"], name=f"Schutzschlitz_{ri}")
        b.add("solid.pattern.circular", features=[f"Schutzschlitz_{ri}"], axis={"origin": [x_sp, 0, 0], "dir": [0, 0, 1]}, count=int(p["guard_slot_n"]))
    b.add("material.assign", bodies=["Medienschutz"], material="V2A Lochblech")
    b.add("solid.cylinder", diameter=p["guard_d"], height=p["cap_h"], base=[x_sp, 0, z_m0 + p["guard_h"]], operation="new", name="Kappe_Schutz", body_name="Schutzkappe")
    b.add("material.assign", bodies=["Schutzkappe"], material="PVC grau Beet")
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
    # --- Reinigungsschacht T30e-5 (D77/W40: stehend auf dem Sperrboden, kein Loch in der Platte): Rohr d110 x 3, Oberkante 20 mm ueber der Medienoberflaeche, lose Kappe, 2 Kerben 30 x 30 am Fuss
    b.add("component.activate", component=root)
    b.add("component.create", name="T30g_Schacht")
    sh_h = p["media_depth"] + p["shaft_over"]
    tube(b, "Reinigungsschacht", p["shaft_d"], p["shaft_wall"], [x_sh, y_sh, z_m0], [0, 0, 1], sh_h)
    sk = p["shaft_kerbe"]
    for k, sg in enumerate((1, -1)):
        b.add("solid.box", length=sk, width=p["shaft_wall"] + 8, height=sk + 1, center=[x_sh, y_sh + sg * (p["shaft_d"] / 2 - p["shaft_wall"] / 2), z_m0 - 1 + (sk + 1) / 2],
              operation="cut", targets=["Reinigungsschacht"], name=f"Schachtkerbe_{k}")
    b.add("material.assign", bodies=["Reinigungsschacht"], material="PVC grau Beet")
    b.add("solid.cylinder", diameter=p["shaft_d"], height=p["cap_h"], base=[x_sh, y_sh, z_m0 + sh_h], operation="new", name="Kappe_Schacht", body_name="Schachtkappe")
    b.add("material.assign", bodies=["Schachtkappe"], material="PVC grau Beet")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T30", d["beschreibung"]), ("T30a_Wanne", "T30a", "Wanne halbe IBC mit Randwulst, Bohrungen"), ("T30b_Stuetzen", "T30b", "Stuetzklotz 60x60 unter dem Siebboden"),
                       ("T30c_Siebboden", "T30c", "Sperrboden PP 8 mm ohne Lochung (V3, D77), Durchfuehrung d36 fuer die Plattenhuelse"), ("T30d_Medium", "T30d", "Medium Blaehton/Kies als ein Koerper"),
                       ("T30e_Siphon", "T30e", "Glockensiphon: Tankverbinder mit Reduzierhuelse 32/25 (Boden und Platte), Standrohr d25, Reduktion d40 x d25, Glocke d75 mit 4 Kerben, Medienschutz Lochblech d110 mit Kappe"), ("T30f_Zulauf", "T30f", "Zulauf-Tropfrohr d20"), ("T30g_Schacht", "T30g", "Reinigungsschacht d110 mit Kappe")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    info = dict(L=L, W=W, H=H, z_ms=z_ms, z_m0=z_m0, z_g0=z_g0, x_sp=x_sp, x_sh=x_sh, y_sh=y_sh, y_in=y_in, z_in=z_in, n_dr=n_dr, nx=nx)
    return b, info

def render(typ, path, info):
    r = os.path.join(sc.ROOT, "renders", "components", f"ibc_beet_{typ}")
    os.makedirs(r, exist_ok=True)
    L, H = info["L"], info["H"]
    Lw_ = L - 2 * 20
    views = {"01-iso": ([0, 0, H / 3], 0.6, 0.45, L * 1.25), "02-siphon": ([info["x_sp"], 0, info["z_m0"] + 120], 0.7, 0.5, 700),
             "03-zulauf": ([-Lw_ / 2 + 150, info["y_in"], info["z_in"]], 0.9, 0.4, 700), "04-medium": ([0, 0, info["z_ms"]], 0.3, 0.8, L * 0.9)}
    for n, (t, yaw, pitch, dist) in views.items():
        sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-{n}.png"), t, yaw, pitch, dist, w=1000, h=650)
    sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-05-schnitt.png"), [info["x_sp"] - 100, 0, H / 2], 3.14159, 0.0, 1300, w=1000, h=650, section="XZ")
    sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-06-schnitt-quer.png"), [info["x_sp"], 0, H / 2], 1.5708, 0.0, info["W"] * 2.0, w=900, h=650, section="x=%d,flip" % int(info["x_sp"]))

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["aussen_933", "aussen_993", "aussen_800", "innen_933"]
    for typ in typs:
        b, info = build(typ)
        out = os.path.join(sc.ROOT, "designs", "components", f"ibc_beet_{typ}.sc")
        sc.run(b.write(f"ibc_beet_{typ}"), out)
        ev = sc.evaluate(out)
        for x in ev["bodies"]:
            print(typ, x["name"], round(x["volume_mm3"] / 1e6, 3), "l", round(x["mass_g"] / 1000, 2), "kg", x["faces"], "F")
        if "--render" in sys.argv:
            render(typ, out, info)
