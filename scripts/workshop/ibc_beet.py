"""IBC-Beet T30 (aussen_933 / aussen_993 / aussen_800 / innen_933), Aufbau nach Quelle A21 (U3b, D132 bis D135): Wanne, Stuetzen, Abtropfgitter, Vlies, Sieb, Medium (EIN Koerper),
Glockensiphon bis zum Wannenboden (durch das Gitter), Auslasswinkel, Rohr durch die +X-Stirnwand, Tankverbinder, Schlauchtuelle ID25, Luftschlauch mit Ausstroemerstab unten, Reinigungsschacht, Zulaufrohr.
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
    """M-BEET-TAUSCH 0c (Schacht) und -fix (Siphon/Medienschutz, D79): Lage (x, y) auf einer ZELLMITTE des Netztopf-Rasters (gen_dome.bed_pot_grid: pot_pitch, pot_margin aus data/params.json, Raster symmetrisch zur Beetmitte, (u laengs, v quer)):
    je vier Toepfe im Abstand pitch*sqrt(2)/2 (92 mm, Soll >= Schachtradius 55 + Kragenradius 32 = 87). u: Zellmitte nahe u_ziel (alte Lage -Li/2 + 250); v: Zellmitte nahe 0 (ungerade Zeilenzahl: +pitch/2)."""
    P = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8"))
    pitch, mar = P["pot_pitch"]["value"], P["pot_margin"]["value"]
    nu, nv = int((L - 2 * mar) // pitch) + 1, int((W - 2 * mar) // pitch) + 1
    us = [(i - (nu - 1) / 2) * pitch + pitch / 2 for i in range(nu - 1)]      # Zellmitten laengs
    vs = [(j - (nv - 1) / 2) * pitch + pitch / 2 for j in range(nv - 1)]      # Zellmitten quer
    u = min(us, key=lambda x: (abs(x - u_ziel), x))
    v = min(vs, key=lambda x: (abs(x), -x))
    return u, v

def layout(typ):
    """Alle Mass- und Lagewerte des Beets (lokal, Ursprung Mitte Wannenunterseite) aus Parametern und Typ; vom Generator und vom Check gemeinsam benutzt."""
    p, d = sc.load_params("ibc_beet")
    T = d["typen"][typ]
    L, W, H = T["laenge"], T["breite"], T["hoehe"]
    wl, ft, cr, rw = p["wall"], p["floor_t"], p["corner_r"], p["rim_w"]
    Lw, Ww = L - 2 * rw, W - 2 * rw
    Li, Wi = Lw - 2 * wl, Ww - 2 * wl
    fase = T.get("fase", 0)
    z_m0 = p["a21_boden"]                         # Medienunterkante = Oberkante des A21-Stapels = Soll-Beetboden (U3, D122)
    z_sv = z_m0 - p["a21_sieb_t"]                 # Unterkante Sieb = Oberkante Vlies
    z_vg = z_sv - p["a21_vlies_t"]                # Unterkante Vlies = Oberkante Gitter
    z_g0 = z_vg - p["a21_gitter_h"]               # Unterkante Gitter
    x_sp, y_sp = shaft_cell(L, W, Li / 2 - 200)
    lay = dict(p=p, d=d, T=T, L=L, W=W, H=H, wl=wl, ft=ft, cr=cr, rw=rw, Lw=Lw, Ww=Ww, Li=Li, Wi=Wi, fase=fase, z_m0=z_m0, z_ms=z_m0 + p["media_depth"], z_sv=z_sv, z_vg=z_vg, z_g0=z_g0,
               x_sp=x_sp, y_sp=y_sp, z_out=p["a21_auslass_z"], x_bo=Lw / 2 + 12, y_air=(Wi / 2 - 100) / 2, z_air=ft + p["a21_ausstroemer_d"] / 2 + 0.5, x_a0=-Li / 2 + 100, hole_d=p["bell_d"] + 4)
    return lay

def build(typ):
    Y = layout(typ)
    p, d, T = Y["p"], Y["d"], Y["T"]
    L, W, H, wl, ft, cr, rw = Y["L"], Y["W"], Y["H"], Y["wl"], Y["ft"], Y["cr"], Y["rw"]
    rh = p["rim_h"]
    Lw, Ww, Li, Wi, fase = Y["Lw"], Y["Ww"], Y["Li"], Y["Wi"], Y["fase"]
    z_m0, z_ms, z_sv, z_vg, z_g0 = Y["z_m0"], Y["z_ms"], Y["z_sv"], Y["z_vg"], Y["z_g0"]
    x_sp, y_sp, z_out, x_bo, y_air, z_air, x_a0, hole_d = Y["x_sp"], Y["y_sp"], Y["z_out"], Y["x_bo"], Y["y_air"], Y["z_air"], Y["x_a0"], Y["hole_d"]
    def rr(b_, z, w, l, r, name):
        if not fase:
            return rrect(b_, z, w, l, r, name)
        d_ = (W - w) / 2.0                       # Versatz gegen den Randwulst-Umriss
        return crect(b_, z, w, l, fase - d_ * (2 - math.sqrt(2)), name)
    g = p["media_gap"]
    gr = p["a21_gitter_rand"]
    x_sh, y_sh = shaft_cell(L, W, -Li / 2 + 250)  # Reinigungsschacht am Zulaufende (T30e-5), auf einer Zellmitte des Topfrasters (M-BEET-TAUSCH 0c)
    y_in, z_in = -(Wi / 2 - 50), H - p["inflow_below_rim"]
    if fase:                                     # Zulauf durch die gerade Stirnwand: y_in vor dem Beginn der Eckenfase (Befund Spec-Pruefer W26)
        y_in = -(Ww / 2 - (fase - ((W - Ww) / 2.0) * (2 - math.sqrt(2))) - 40)
    # Schlitzraster des Abtropfgitters: Teilung quer = Schlitz + Steg (20), laengs 300; zentriert; Rand hinter der Eckenfase / dem Eckenradius
    Lg, Wg = Li - 2 * gr, Wi - 2 * gr
    sb_, sl_, st_ = p["a21_gitter_schlitz_b"], p["a21_gitter_schlitz_l"], p["a21_gitter_steg"]
    nx_s = int((Lg - 20 + st_) // (sl_ + st_)); ny_s = int((Wg - 20 + st_) // (sb_ + st_))
    c_g = (fase - ((W - Wg) / 2.0) * (2 - math.sqrt(2))) if fase else (cr - gr)   # Schenkel der Eckenfase bzw. Eckenradius der Gitterkontur
    marg_x = (Lg - (nx_s * (sl_ + st_) - st_)) / 2.0
    assert marg_x >= c_g + 4, f"{typ}: Gitterschlitze reichen in die Ecke (Randabstand {marg_x:.0f} < {c_g + 4:.0f})"
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    b.add("parameters.add", name="beet_laenge", expression=f"{L} mm"); b.add("parameters.add", name="beet_breite", expression=f"{W} mm"); b.add("parameters.add", name="beet_hoehe", expression=f"{H} mm")
    b.add("material.create", name="HDPE weiss", density_g_cm3=0.95, color=d["werkstoff"]["farbe"])
    b.add("material.create", name="Medium Blaehton", density_g_cm3=d["medium"]["dichte_g_cm3"], color=d["medium"]["farbe"])
    b.add("material.create", name="PP grau", density_g_cm3=0.91, color="#9aa0a4")
    b.add("material.create", name="PP weiss", density_g_cm3=0.91, color="#eef0ee")
    b.add("material.create", name="PVC grau Beet", density_g_cm3=1.4, color="#8d9296")
    b.add("material.create", name="V2A Lochblech", density_g_cm3=7.9, color="#c3c8cc")
    b.add("material.create", name="PP Vlies", density_g_cm3=0.075, color="#d9dccf")     # Drainagevlies 150 g/m2 bei 2 mm (Annahme)
    b.add("material.create", name="Sieb Edelstahlgewebe 2 mm", density_g_cm3=1.24, color="#c3c8cc")   # Gewebe Draht 0,5 mm, Teilung 2,5: rund 1,24 kg/m2 bei 1 mm Ersatzdicke (Annahme)
    b.add("material.create", name="Schlauch hellblau", density_g_cm3=1.25, color="#7fb8d8")
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
    b.add("solid.cylinder", diameter=p["bulkhead_d"], height=wl + 4, base=[Li / 2 - 2, y_sp, z_out], axis=[1, 0, 0], operation="cut", targets=["Wanne"], name="Durchfuehrung_Auslass")
    b.add("solid.cylinder", diameter=p["a21_belueftung_d"] + 2, height=wl + 4, base=[-Lw / 2 - 2, y_air, z_air], axis=[1, 0, 0], operation="cut", targets=["Wanne"], name="Durchfuehrung_Luft")
    b.add("solid.cylinder", diameter=p["inflow_d"] + 2, height=wl + 4, base=[-Lw / 2 - 2, y_in, z_in], axis=[1, 0, 0], operation="cut", targets=["Wanne"], name="Durchfuehrung_Zulauf")
    b.add("material.assign", bodies=["Wanne"], material="HDPE weiss")
    # --- Stuetzen (Klotz 60 x 60 unter dem Gitter), Raster nx x 3; Klotz entfaellt, wo Glocke/Winkel (um die Siphonachse) oder das Auslassrohr (nach +X) laufen (D132)
    b.add("component.activate", component=root)
    b.add("component.create", name="T30b_Stuetzen")
    nx = int(p["post_nx"]) if L > 2500 else 5
    sx = (Li - 200) / (nx - 1)
    h_post = z_g0 - ft
    post_n = 0
    for iy in range(3):
        py = -(Wi / 2 - 100) + iy * (Wi - 200) / 2
        for ix in range(nx):
            px = -Li / 2 + 100 + ix * sx
            dx, dy = px - x_sp, py - y_sp
            if (abs(dx) < 70 and abs(dy) < 70) or (dx > -70 and abs(dy) < p["post"] / 2 + p["a21_winkel_d"] / 2 + 3):
                continue
            post_n += 1
            nm = "Stuetze" if post_n == 1 else f"Stuetze ({post_n})"
            b.add("solid.box", length=p["post"], width=p["post"], height=h_post, center=[round(px, 3), round(py, 3), ft + h_post / 2], operation="new", name="Klotz_%d" % post_n, body_name=nm)
    b.add("material.assign", bodies=["Stuetze"] + [f"Stuetze ({k})" for k in range(2, post_n + 1)], material="PP grau")
    # --- Abtropfgitter (PP-Rost, Stegrost mit laengs gestreckten Schlitzen), Vlies und Sieb darueber (A21)
    b.add("component.activate", component=root)
    b.add("component.create", name="T30c_Abtropfgitter")
    rr(b, z_g0, Wg, Lg, cr - gr, "Gitter_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["a21_gitter_h"], name="Gitterplatte", body_name="Abtropfgitter")
    b.add("solid.box", length=sl_, width=sb_, height=p["a21_gitter_h"] + 2, center=[-(nx_s - 1) / 2 * (sl_ + st_), -(ny_s - 1) / 2 * (sb_ + st_), z_g0 + p["a21_gitter_h"] / 2], operation="cut", targets=["Abtropfgitter"], name="Gitterschlitz")
    b.add("solid.pattern.rectangular", features=["Gitterschlitz"], dir1=[1, 0, 0], count1=nx_s, spacing1=sl_ + st_, dir2=[0, 1, 0], count2=ny_s, spacing2=sb_ + st_)
    b.add("solid.cylinder", diameter=hole_d, height=p["a21_gitter_h"] + 2, base=[x_sp, y_sp, z_g0 - 1], operation="cut", targets=["Abtropfgitter"], name="Gitter_Glockenloch")
    b.add("material.assign", bodies=["Abtropfgitter"], material="PP grau")
    b.add("component.activate", component=root)
    b.add("component.create", name="T30h_Vlies_Sieb")
    rr(b, z_vg, Wi - 2 * g, Li - 2 * g, cr - g, "Vlies_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["a21_vlies_t"], name="Vliesplatte", body_name="Vlies")
    b.add("solid.cylinder", diameter=hole_d, height=p["a21_vlies_t"] + 2, base=[x_sp, y_sp, z_vg - 1], operation="cut", targets=["Vlies"], name="Vlies_Glockenloch")
    b.add("material.assign", bodies=["Vlies"], material="PP Vlies")
    rr(b, z_sv, Wi - 2 * g, Li - 2 * g, cr - g, "Sieb_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["a21_sieb_t"], name="Siebplatte", body_name="Sieb")
    b.add("solid.cylinder", diameter=hole_d, height=p["a21_sieb_t"] + 2, base=[x_sp, y_sp, z_sv - 1], operation="cut", targets=["Sieb"], name="Sieb_Glockenloch")
    b.add("material.assign", bodies=["Sieb"], material="Sieb Edelstahlgewebe 2 mm")
    # --- Medium: EIN Koerper, Oberflaeche z_ms, Tiefe media_depth, Loecher fuer die Glocke und den Reinigungsschacht
    b.add("component.activate", component=root)
    b.add("component.create", name="T30d_Medium")
    rr(b, z_m0, Wi - 2 * g, Li - 2 * g, cr - g, "Medium_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["media_depth"], name="Mediumblock", body_name="Medium")
    b.add("solid.cylinder", diameter=hole_d, height=p["media_depth"] + 2, base=[x_sp, y_sp, z_m0 - 1], operation="cut", targets=["Medium"], name="Medium_Glockenloch")
    b.add("solid.cylinder", diameter=p["shaft_d"], height=p["media_depth"] + 2, base=[x_sh, y_sh, z_m0 - 1], operation="cut", targets=["Medium"], name="Medium_Schachtloch")
    b.add("material.assign", bodies=["Medium"], material="Medium Blaehton")
    # --- Glockensiphon (D133): Glocke steht auf dem Wannenboden, Kerben und Luftloch unter dem Gitter; Standrohr steckt im Auslasswinkel
    b.add("component.activate", component=root)
    b.add("component.create", name="T30e_Siphon")
    z_top = z_m0 + p["standpipe_over"]
    bid, bd = p["bulkhead_id"], p["bulkhead_d"]
    wd, sd = p["a21_winkel_d"], p["standpipe_d"]
    sock, sock_t = 29, 14                         # Mittelpunkt bis Muffenende 29, Muffentiefe 14 (D134; Muffengrund hinter dem Schenkel der anderen Muffe, sonst schneiden sich zwei gleich grosse Zylinder)
    # Auslasswinkel 90 Grad d25 (Klebemuffen): senkrechter Schenkel nach oben, waagerechter nach +X
    b.add("solid.cylinder", diameter=wd, height=wd / 2 + sock, base=[x_sp, y_sp, z_out - wd / 2], operation="new", name="Winkel_senkrecht", body_name="Auslasswinkel")
    b.add("solid.cylinder", diameter=wd, height=wd / 2 + sock, base=[x_sp - wd / 2, y_sp, z_out], axis=[1, 0, 0], operation="join", targets=["Auslasswinkel"], name="Winkel_waagerecht")
    b.add("solid.cylinder", diameter=sd, height=sock_t + 1, base=[x_sp, y_sp, z_out + sock - sock_t], operation="cut", targets=["Auslasswinkel"], name="Winkel_Muffe_oben")
    b.add("solid.cylinder", diameter=sd - 2 * p["standpipe_wall"], height=sock - sock_t + 1, base=[x_sp, y_sp, z_out], operation="cut", targets=["Auslasswinkel"], name="Winkel_Bohrung_oben")
    b.add("solid.cylinder", diameter=sd, height=sock_t + 1, base=[x_sp + sock - sock_t, y_sp, z_out], axis=[1, 0, 0], operation="cut", targets=["Auslasswinkel"], name="Winkel_Muffe_aussen")
    b.add("solid.cylinder", diameter=sd - 2 * p["standpipe_wall"] - 0.4, height=sock - sock_t + 1, base=[x_sp, y_sp, z_out], axis=[1, 0, 0], operation="cut", targets=["Auslasswinkel"], name="Winkel_Bohrung_aussen")
    b.add("material.assign", bodies=["Auslasswinkel"], material="PVC grau Beet")
    z_s0 = z_out + sock - sock_t                  # Standrohr beginnt am Muffengrund
    tube(b, "Standrohr", sd, p["standpipe_wall"], [x_sp, y_sp, z_s0], [0, 0, 1], z_top - z_s0)
    b.add("material.assign", bodies=["Standrohr"], material="PVC grau Beet")
    # Glocke: oben geschlossen, 3 Kerben am Fuss, Luftloch, Loch fuer das Auslassrohr
    z_b0 = ft + p["a21_standrohr_unten"]
    tube(b, "Glocke", p["bell_d"], p["bell_wall"], [x_sp, y_sp, z_b0], [0, 0, 1], p["bell_h"])
    b.add("solid.cylinder", diameter=p["bell_d"], height=p["bell_wall"], base=[x_sp, y_sp, z_b0 + p["bell_h"] - p["bell_wall"]], operation="join", targets=["Glocke"], name="Glockendeckel")
    kh, kz = p["bell_slot_h"], p["bell_slot_z"]
    for k, (dx, dy) in enumerate(((-1, 0), (0, 1), (0, -1))):
        b.add("solid.box", length=(p["bell_slot_w"] if dx == 0 else p["bell_wall"] + 8), width=(p["bell_slot_w"] if dy == 0 else p["bell_wall"] + 8), height=kh + 1,
              center=[x_sp + dx * (p["bell_d"] / 2 - p["bell_wall"] / 2), y_sp + dy * (p["bell_d"] / 2 - p["bell_wall"] / 2), z_b0 + kz - 1 + (kh + 1) / 2], operation="cut", targets=["Glocke"], name=f"Kerbe_{k}")
    b.add("solid.box", length=p["air_hole"], width=p["bell_wall"] + 6, height=p["air_hole"], center=[x_sp, y_sp - (p["bell_d"] / 2 - p["bell_wall"] / 2), p["a21_luftloch_z"]], operation="cut", targets=["Glocke"], name="Luftloch")
    b.add("solid.cylinder", diameter=sd + 2, height=p["bell_wall"] + 8, base=[x_sp + p["bell_d"] / 2 - p["bell_wall"] - 4, y_sp, z_out], axis=[1, 0, 0], operation="cut", targets=["Glocke"], name="Glocke_Auslassloch")
    b.add("material.assign", bodies=["Glocke"], material="PVC grau Beet")
    # Auslassrohr d25 waagerecht vom Muffengrund des Winkels durch Glocke, Tankverbinder und Wand bis zum Ende des Tankverbinders; danach die Schlauchtuelle
    x_wi, x_wo = Li / 2, Lw / 2                    # Wand innen / aussen
    x_r0 = x_sp + sock - sock_t
    tube(b, "Auslassrohr", sd, p["standpipe_wall"], [x_r0, y_sp, z_out], [1, 0, 0], x_bo - x_r0)
    b.add("material.assign", bodies=["Auslassrohr"], material="PVC grau Beet")
    bl = 4 + wl + 12
    tube(b, "Bulkhead", bd, (bd - bid) / 2, [x_wi - 4, y_sp, z_out], [1, 0, 0], bl)
    b.add("solid.cylinder", diameter=p["bulkhead_flange"], height=4, base=[x_wi - 4, y_sp, z_out], axis=[1, 0, 0], operation="join", targets=["Bulkhead"], name="Flansch")
    b.add("solid.cylinder", diameter=bid, height=bl + 2, base=[x_wi - 5, y_sp, z_out], axis=[1, 0, 0], operation="cut", targets=["Bulkhead"], name="Bulkhead_Sitz")
    b.add("material.assign", bodies=["Bulkhead"], material="PVC grau Beet")
    tube(b, "Reduzierhuelse_Auslass", bid, (bid - sd) / 2, [x_wi - 4, y_sp, z_out], [1, 0, 0], bl)
    b.add("material.assign", bodies=["Reduzierhuelse_Auslass"], material="PVC grau Beet")
    # Schlauchtuelle fuer Schlauch ID25 (D106): Rohr 25 / 20 mit zwei Widerhaken d28
    tl = p["a21_tuelle_l"]
    tube(b, "Schlauchtuelle", 25, 2.5, [x_bo, y_sp, z_out], [1, 0, 0], tl)
    for k, off in enumerate((10, 26)):
        b.add("solid.cylinder", diameter=28, height=4, base=[x_bo + off, y_sp, z_out], axis=[1, 0, 0], operation="join", targets=["Schlauchtuelle"], name=f"Widerhaken_{k}")
    b.add("solid.cylinder", diameter=20, height=tl + 2, base=[x_bo - 1, y_sp, z_out], axis=[1, 0, 0], operation="cut", targets=["Schlauchtuelle"], name="Tuelle_Bohrung")
    b.add("material.assign", bodies=["Schlauchtuelle"], material="PVC grau Beet")
    # --- Belueftung unten (D135): Luftschlauch d8 durch die -X-Stirnwand, Ausstroemerstab auf dem Wannenboden
    b.add("component.activate", component=root)
    b.add("component.create", name="T30i_Belueftung")
    x_l0 = -Lw / 2 - 40
    tube(b, "Luftschlauch", p["a21_belueftung_d"], 1.5, [x_l0, y_air, z_air], [1, 0, 0], x_a0 - x_l0)
    b.add("material.assign", bodies=["Luftschlauch"], material="Schlauch hellblau")
    b.add("solid.cylinder", diameter=p["a21_ausstroemer_d"], height=p["a21_ausstroemer_l"], base=[x_a0, y_air, z_air], axis=[1, 0, 0], operation="new", name="Stab", body_name="Ausstroemer")
    b.add("material.assign", bodies=["Ausstroemer"], material="PP weiss")
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
    # --- Reinigungsschacht T30e-5 (D77/W40: stehend auf dem Sieb, kein Loch im Stapel): Rohr d110 x 3, Oberkante 20 mm ueber der Medienoberflaeche, lose Kappe, 2 Kerben 30 x 30 am Fuss
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
    for nm, pn, ds in ((root, "T30", d["beschreibung"]), ("T30a_Wanne", "T30a", "Wanne halbe IBC mit Randwulst, Bohrungen fuer Auslass, Luft und Zulauf"), ("T30b_Stuetzen", "T30b", "Stuetzklotz 60x60 unter dem Abtropfgitter"),
                       ("T30c_Abtropfgitter", "T30c", "Abtropfgitter PP 25 mm (Stegrost) am Boden des Beets, Glockenloch"), ("T30d_Medium", "T30d", "Medium Blaehton/Kies als ein Koerper"),
                       ("T30e_Siphon", "T30e", "Glockensiphon bis zum Wannenboden: Standrohr d25, Auslasswinkel, Glocke d75 mit 3 Kerben, Auslassrohr, Tankverbinder mit Reduzierhuelse 32/25, Schlauchtuelle ID25"), ("T30f_Zulauf", "T30f", "Zulauf-Tropfrohr d20"),
                       ("T30g_Schacht", "T30g", "Reinigungsschacht d110 mit Kappe"), ("T30h_Vlies_Sieb", "T30h", "Vlies 2 mm und Sieb 1 mm ueber dem Gitter"), ("T30i_Belueftung", "T30i", "Luftschlauch d8 und Ausstroemerstab d16 unter dem Gitter")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    info = dict(L=L, W=W, H=H, z_ms=z_ms, z_m0=z_m0, z_g0=z_g0, z_vg=z_vg, z_sv=z_sv, x_sp=x_sp, y_sp=y_sp, x_sh=x_sh, y_sh=y_sh, y_in=y_in, z_in=z_in, n_dr=n_dr, nx=nx, post_n=post_n,
                z_out=z_out, y_air=y_air, z_air=z_air, x_bo=x_bo, x_wo=x_wo, nx_s=nx_s, ny_s=ny_s, hole_d=hole_d, x_a0=x_a0)
    return b, info

def render(typ, path, info):
    r = os.path.join(sc.ROOT, "renders", "components", f"ibc_beet_{typ}")
    os.makedirs(r, exist_ok=True)
    L, H = info["L"], info["H"]
    Lw_ = L - 2 * 20
    x_sp, y_sp, z_out = info["x_sp"], info["y_sp"], info["z_out"]
    views = {"01-iso": ([0, 0, H / 3], 0.6, 0.45, L * 1.25), "02-siphon": ([x_sp, y_sp, info["z_m0"] + 120], 0.7, 0.5, 700),
             "03-zulauf": ([-Lw_ / 2 + 150, info["y_in"], info["z_in"]], 0.9, 0.4, 700), "04-medium": ([0, 0, info["z_ms"]], 0.3, 0.8, L * 0.9),
             "07-auslass": ([info["x_bo"] + 20, y_sp, z_out], 2.2, 0.35, 450), "08-luftanschluss": ([-Lw_ / 2, info["y_air"], info["z_air"]], -0.8, 0.35, 450)}
    for n, (t, yaw, pitch, dist) in views.items():
        sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-{n}.png"), t, yaw, pitch, dist, w=1000, h=650)
    sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-05-schnitt.png"), [x_sp - 100, y_sp, H / 2], 3.14159, 0.0, 1300, w=1000, h=650, section="XZ")
    sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-06-schnitt-quer.png"), [x_sp, y_sp, H / 2], 1.5708, 0.0, info["W"] * 2.0, w=900, h=650, section="x=%d,flip" % int(x_sp))
    sc.snapshot(path, os.path.join(r, f"ibc_beet_{typ}-09-schnitt-unten.png"), [x_sp - 100, y_sp, 60], 3.14159, 0.0, 420, w=1000, h=650, section="XZ")

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
