"""Pump-/Filtermodule T50: pumpe_klein, pumpe_gross (Montagetafel mit Kreiselpumpe) und filtermodul (flache Filterkassette).
Bezugspunkt: Mitte der Standflaeche; X Tafel-/Gehaeuselaenge, Y Dicke (Pumpe/Anschluesse auf +Y), Z hoch. Aufruf: python scripts/workshop/pumpe.py [typ ...] [--render]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

def tube(b, name, od, wall, base, axis, height, mat):
    b.add("solid.cylinder", diameter=od, height=height, base=base, axis=axis, operation="new", name="R_" + name, body_name=name)
    b.add("solid.cylinder", diameter=od - 2 * wall, height=height + 2, base=[base[i] - axis[i] for i in range(3)], axis=axis, operation="cut", targets=[name], name="B_" + name)
    b.add("material.assign", bodies=[name], material=mat)

def build_pumpe(typ, T, p, d):
    L, t, H = T["tafel_l"], T["tafel_t"], T["tafel_h"]
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    b.add("parameters.add", name="tafel_l", expression=f"{L} mm"); b.add("parameters.add", name="tafel_t", expression=f"{t} mm"); b.add("parameters.add", name="tafel_h", expression=f"{H} mm")
    b.add("material.create", name="PP Tafel", density_g_cm3=0.91, color="#d8dadc")
    b.add("material.create", name="Pumpe blau", density_g_cm3=1.5, color=d["werkstoff"]["farbe"])
    b.add("material.create", name="PVC grau Pumpe", density_g_cm3=1.4, color="#8d9296")
    b.add("material.create", name="Stahl Pumpe", density_g_cm3=7.85, color="#aeb4b8")
    b.add("material.create", name="Kabel schwarz", density_g_cm3=1.2, color="#222222")
    root = f"T50_Pumpenmodul_{typ.split('_')[1]}"
    b.add("component.create", name=root, grounded=True)
    # --- Montagetafel
    b.add("component.create", name="T50a_Tafel")
    b.add("solid.box", length="tafel_l", width="tafel_t", height="tafel_h", center=[0, 0, H / 2], operation="new", name="Tafelkoerper", body_name="Montagetafel")
    for sx in (-1, 1):   # Standwinkel hinten (gegen Kippen): senkrechter Schenkel an der Tafelrueckseite, waagerechter Schenkel am Boden
        xs = sx * (L / 2 - 60)
        b.add("solid.box", length=50, width=5, height=100, center=[xs, -t / 2 - 2.5, 50], operation="new", name=f"SW_V{sx}", body_name=f"Standwinkel_{'L' if sx < 0 else 'R'}")
        b.add("solid.box", length=50, width=80, height=5, center=[xs, -t / 2 - 40, 2.5], operation="join", targets=[f"Standwinkel_{'L' if sx < 0 else 'R'}"], name=f"SW_H{sx}")
        b.add("material.assign", bodies=[f"Standwinkel_{'L' if sx < 0 else 'R'}"], material="Stahl Pumpe")
    b.add("material.assign", bodies=["Montagetafel"], material="PP Tafel")
    # --- Konsole (Winkel 5 mm), traegt die Pumpe
    md, ml, kd, kl = T["motor_d"], T["motor_l"], T["kopf_d"], T["kopf_l"]
    z_s = p["pump_z"] - md / 2 - 8                              # Oberkante Konsole
    bw, bt = p["bracket_w"], p["bracket_t"]
    ycent = t / 2 + bt + md / 2 + 12                            # Pumpenachse vor der Tafel
    b.add("component.activate", component=root)
    b.add("component.create", name="T50b_Konsole")
    b.add("solid.box", length=bw, width=ycent + md / 2 + 10 - t / 2, height=bt, center=[0, t / 2 + (ycent + md / 2 + 10 - t / 2) / 2, z_s - bt / 2], operation="new", name="KH", body_name="Konsole")
    b.add("solid.box", length=bw, width=bt, height=40, center=[0, t / 2 + bt / 2, z_s - bt - 20 + 40 / 2 - 0], operation="join", targets=["Konsole"], name="KV")
    b.add("material.assign", bodies=["Konsole"], material="Stahl Pumpe")
    for sx in (-1, 1):
        zz = z_s - bt - 20 + 20
        b.add("parts.insert", family="hex_bolt", size="M6", length=16, point=[sx * (bw / 2 - 25), t / 2 + bt, zz], direction=[0, 1, 0], name=f"SchraubeK_{sx}")
        b.add("parts.insert", family="hex_nut", size="M6", point=[sx * (bw / 2 - 25), -t / 2, zz], direction=[0, -1, 0], name=f"MutterK_{sx}")
    # --- Pumpe: Sockel, Motor, Pumpenkopf, Saug- und Druckstutzen, Kabel mit Stecker
    b.add("component.activate", component=root)
    b.add("component.create", name="T50c_Pumpe")
    x0 = -(ml + kl) / 2
    za = z_s + 8 + md / 2                                       # Achshoehe
    b.add("solid.box", length=ml * 0.7, width=md * 0.6, height=8, center=[x0 + ml * 0.4, ycent, z_s + 4], operation="new", name="Sockel_R", body_name="Pumpensockel")
    b.add("material.assign", bodies=["Pumpensockel"], material="Stahl Pumpe")
    b.add("solid.cylinder", diameter=md, height=ml, base=[x0, ycent, za], axis=[1, 0, 0], operation="new", name="Motor_R", body_name="Motor")
    b.add("material.assign", bodies=["Motor"], material="Pumpe blau")
    b.add("solid.cylinder", diameter=kd, height=kl, base=[x0 + ml, ycent, za], axis=[1, 0, 0], operation="new", name="Kopf_R", body_name="Pumpenkopf")
    b.add("material.assign", bodies=["Pumpenkopf"], material="PVC grau Pumpe")
    sd, dd = T["saug_d"], T["druck_d"]
    tube(b, "Saugstutzen", sd, 3, [x0 + ml + kl - 4, ycent, za], [1, 0, 0], 70, "PVC grau Pumpe")
    tube(b, "Druckstutzen", dd, 3, [x0 + ml + kl / 2, ycent, za + kd / 2 - 4], [0, 0, 1], 74, "PVC grau Pumpe")
    cl = 150
    b.add("solid.cylinder", diameter=p["cable_d"], height=cl, base=[x0 - cl, ycent, za], axis=[1, 0, 0], operation="new", name="Kabel_R", body_name="Kabel")
    b.add("material.assign", bodies=["Kabel"], material="Kabel schwarz")
    b.add("solid.box", length=p["plug_l"], width=45, height=40, center=[x0 - cl - p["plug_l"] / 2, ycent, za], operation="new", name="Stecker_R", body_name="Stecker")
    b.add("material.assign", bodies=["Stecker"], material="Kabel schwarz")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T50", d["beschreibung"]), ("T50a_Tafel", "T50a", "Montagetafel mit Standwinkeln"), ("T50b_Konsole", "T50b", "Pumpenkonsole Winkel 5 mm"), ("T50c_Pumpe", "T50c", "Kreiselpumpe mit Stutzen, Kabel, Stecker")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, dict(x0=x0, ycent=ycent, za=za, z_s=z_s, kd=kd, ml=ml, kl=kl, L=L, H=H, t=t)

def build_filter(typ, T, p, d):
    L, t, H = T["box_l"], T["box_t"], T["box_h"]
    w, c, lt = p["wall"], p["mat_clear"], p["lid_t"]
    pd = T["port_d"]
    b = sc.Build()
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b.params_to_design(p, d, unit)
    b.add("parameters.add", name="box_l", expression=f"{L} mm"); b.add("parameters.add", name="box_t", expression=f"{t} mm"); b.add("parameters.add", name="box_h", expression=f"{H} mm")
    b.add("material.create", name="PP Filter", density_g_cm3=0.91, color="#c8d4dc")
    b.add("material.create", name="Filtermatte", density_g_cm3=0.05, color="#d9c27a")
    b.add("material.create", name="PVC grau Filter", density_g_cm3=1.4, color="#8d9296")
    b.add("material.create", name="Stahl Filter", density_g_cm3=7.85, color="#aeb4b8")
    root = "T50_Filtermodul"
    b.add("component.create", name=root, grounded=True)
    b.add("component.create", name="T50d_Gehaeuse")
    dep = t - lt                                                  # Gehaeusetiefe ohne Deckel
    b.add("solid.box", length="box_l", width=dep, height="box_h", center=[0, -t / 2 + dep / 2, H / 2], operation="new", name="Gehaeusekoerper", body_name="Filtergehaeuse")
    b.add("solid.box", length=L - 2 * w, width=dep - w + 1, height=H - 2 * w, center=[0, -t / 2 + w + (dep - w + 1) / 2, H / 2], operation="cut", targets=["Filtergehaeuse"], name="Innenraum")
    # Einlass oben (+X-Ende, vertikal), Auslass seitlich unten (-X-Wand, horizontal): Wanddurchbrueche
    xin = L / 2 - 60
    b.add("solid.cylinder", diameter=pd - 6, height=w + 2, base=[xin, -t / 2 + dep / 2, H - w - 1], operation="cut", targets=["Filtergehaeuse"], name="Durchbruch_Einlass")
    b.add("solid.cylinder", diameter=pd - 6, height=w + 2, base=[-L / 2 - 1, -t / 2 + dep / 2, 70], axis=[1, 0, 0], operation="cut", targets=["Filtergehaeuse"], name="Durchbruch_Auslass")
    b.add("material.assign", bodies=["Filtergehaeuse"], material="PP Filter")
    b.add("solid.box", length="box_l", width="box_t - lid_t", height="box_h", center=[0, 0, 0], operation="new", name="Dummy", body_name="Dummy") if False else None
    b.add("solid.box", length="box_l", width="lid_t", height="box_h", center=[0, t / 2 - lt / 2, H / 2], operation="new", name="Deckelplatte", body_name="Deckel")
    b.add("material.assign", bodies=["Deckel"], material="PP Filter")
    for k, (sx, zz) in enumerate(((-1, 0.2), (1, 0.2), (-1, 0.8), (1, 0.8), (0, 0.2), (0, 0.8)), 1):     # Deckelschrauben M6x14
        b.add("parts.insert", family="hex_bolt", size="M6", length=14, point=[sx * (L / 2 - 25), t / 2, H * zz], direction=[0, 1, 0], name=f"SchraubeD_{k}") if sx != 0 else None
    b.add("component.activate", component=root)
    b.add("component.create", name="T50e_Siebeinsatz")
    iw, ih, idp = L - 2 * w - 2 * c, H - 2 * w - 2 * c, dep - w - c - 2
    b.add("solid.box", length=iw, width=idp, height=ih, center=[0, -t / 2 + w + c + idp / 2, H / 2], operation="new", name="Matte", body_name="Siebeinsatz")
    b.add("material.assign", bodies=["Siebeinsatz"], material="Filtermatte")
    b.add("component.activate", component=root)
    b.add("component.create", name="T50f_Anschluesse")
    tube(b, "Einlassstutzen", pd, 3, [xin, -t / 2 + dep / 2, H - 4], [0, 0, 1], 64, "PVC grau Filter")
    tube(b, "Auslassstutzen", pd, 3, [-L / 2 - 60, -t / 2 + dep / 2, 70], [1, 0, 0], 64, "PVC grau Filter")
    # Montagelaschen (4 Stueck) mit Schrauben M6x16
    b.add("component.activate", component=root)
    b.add("component.create", name="T50g_Laschen")
    for k, (sx, zz) in enumerate(((-1, 0.15), (1, 0.15), (-1, 0.85), (1, 0.85)), 1):
        b.add("solid.box", length=30, width=5, height=40, center=[sx * (L / 2 + 15), -t / 2 + 2.5, H * zz], operation="new", name=f"Lasche_{k}_R", body_name=f"Lasche_{k}")
        b.add("solid.cylinder", diameter=7, height=8, base=[sx * (L / 2 + 15), -t / 2 - 1, H * zz], axis=[0, 1, 0], operation="cut", targets=[f"Lasche_{k}"], name=f"Laschenloch_{k}")
        b.add("material.assign", bodies=[f"Lasche_{k}"], material="Stahl Filter")
        b.add("parts.insert", family="hex_bolt", size="M6", length=16, point=[sx * (L / 2 + 15), -t / 2, H * zz], direction=[0, -1, 0], name=f"SchraubeL_{k}")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T50F", d["beschreibung"]), ("T50d_Gehaeuse", "T50d", "Filtergehaeuse mit Deckel"), ("T50e_Siebeinsatz", "T50e", "Siebeinsatz (Filtermatte)"), ("T50f_Anschluesse", "T50f", "Ein- und Auslassstutzen d50"), ("T50g_Laschen", "T50g", "Montagelaschen mit Schrauben M6")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, dict(L=L, H=H, t=t, xin=xin, dep=dep)

def render(typ, path, info):
    r = os.path.join(sc.ROOT, "renders", "components", typ)
    os.makedirs(r, exist_ok=True)
    if typ.startswith("pumpe"):
        views = {"01-iso": ([0, 0, info["H"] / 2], 2.5, 0.35, info["L"] * 2.0), "02-pumpe": ([info["x0"] + 100, info["ycent"], info["za"]], 2.5, 0.3, 700),
                 "03-rueckseite": ([0, 0, info["H"] / 2], 0.6, 0.3, info["L"] * 2.0), "04-seite": ([0, 0, info["H"] / 2], 1.5708, 0.0, info["L"] * 1.8)}
    else:
        views = {"01-iso": ([0, 0, info["H"] / 2], 0.6, 0.35, info["L"] * 2.2), "02-anschluesse": ([0, 0, info["H"] / 2], 0.3, 0.4, info["L"] * 1.6),
                 "03-rueckseite": ([0, 0, info["H"] / 2], 2.6, 0.3, info["L"] * 2.2)}
    for n, (tt, yaw, pitch, dist) in views.items():
        sc.snapshot(path, os.path.join(r, f"{typ}-{n}.png"), tt, yaw, pitch, dist, w=1000, h=700)
    if typ.startswith("pumpe"):
        sc.snapshot(path, os.path.join(r, f"{typ}-05-schnitt.png"), [0, info["ycent"], info["za"]], 0.0, 0.0, info["L"] * 1.6, w=1000, h=700, section="XZ")

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["pumpe_klein", "pumpe_gross"]
    p, d = sc.load_params("pumpe")
    for typ in typs:
        T = d["typen"][typ]
        b, info = build_pumpe(typ, T, p, d) if T["art"] == "pumpe" else build_filter(typ, T, p, d)
        b.cmds = [c for c in b.cmds if c]
        out = os.path.join(sc.ROOT, "designs", "components", f"{typ}.sc")
        sc.run(b.write(typ), out)
        ev = sc.evaluate(out)
        print(typ, "Koerper", len(ev["bodies"]), "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 2), "kg")
        if "--render" in sys.argv:
            render(typ, out, info)
