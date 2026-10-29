"""Pumpenmodule T50: pumpe_klein, pumpe_gross (Montagetafel mit Kreiselpumpe). Die Klasse filtermodul entfaellt (Entscheidung D16: die Kassetten 384 x 44 x 419 sind Stuetzrippen der Tankplattform, Klasse Tank).
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
    sockel_h = (kd - md) / 2 + 1                                 # Sockelhoehe: Pumpenkopf (groesser als Motor) hat 1 mm Luft zur Konsole
    z_s = p["pump_z"] - md / 2 - sockel_h                       # Oberkante Konsole
    bw, bt = p["bracket_w"], p["bracket_t"]
    ycent = t / 2 + bt + md / 2 + 12                            # Pumpenachse vor der Tafel
    b.add("component.activate", component=root)
    b.add("component.create", name="T50b_Konsole")
    b.add("solid.box", length=bw, width=ycent + md / 2 + 10 - t / 2, height=bt, center=[0, t / 2 + (ycent + md / 2 + 10 - t / 2) / 2, z_s - bt / 2], operation="new", name="KH", body_name="Konsole")
    b.add("solid.box", length=bw, width=bt, height=40, center=[0, t / 2 + bt / 2, z_s - 20], operation="join", targets=["Konsole"], name="KV")
    b.add("material.assign", bodies=["Konsole"], material="Stahl Pumpe")
    for sx in (-1, 1):
        zz = z_s - 20                                           # Schrauben mittig im haengenden Vertikalschenkel (z_s - 40 .. z_s), Kopf ausserhalb der Platte
        b.add("parts.insert", family="hex_bolt", size="M6", length=20, point=[sx * (bw / 2 - 25), t / 2 + bt, zz], direction=[0, 1, 0], name=f"SchraubeK_{sx}")
        b.add("parts.insert", family="hex_nut", size="M6", point=[sx * (bw / 2 - 25), -t / 2, zz], direction=[0, -1, 0], name=f"MutterK_{sx}")
    # parts.insert liefert beim ersten Bolzen (Body1) einen D6-Stummel auf dem Kopf (12 statt 10 Flaechen, Befund Spec-Pruefer Runde 4): Werkzeugkoerper schneidet ihn ab
    b.add("solid.box", length=12, width=6, height=12, center=[-(bw / 2 - 25), t / 2 + bt + 4.05 + 3, z_s - 20], operation="new", name="Stummelwerkzeug_R", body_name="Stummelwerkzeug")
    b.add("solid.combine", target="Body1", tools=["Stummelwerkzeug"], operation="cut")
    # --- Pumpe: Sockel, Motor, Pumpenkopf, Saug- und Druckstutzen, Kabel mit Stecker
    b.add("component.activate", component=root)
    b.add("component.create", name="T50c_Pumpe")
    x0 = -(ml + kl) / 2
    za = z_s + sockel_h + md / 2                                # Achshoehe (= pump_z)
    b.add("solid.box", length=ml * 0.7, width=md * 0.6, height=sockel_h, center=[x0 + ml * 0.4, ycent, z_s + sockel_h / 2], operation="new", name="Sockel_R", body_name="Pumpensockel")
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
    return b, dict(x0=x0, ycent=ycent, za=za, z_s=z_s, kd=kd, ml=ml, kl=kl, L=L, H=H, t=t, sockel_h=sockel_h)

def render(typ, path, info):
    r = os.path.join(sc.ROOT, "renders", "components", typ)
    os.makedirs(r, exist_ok=True)
    views = {"01-iso": ([0, 0, info["H"] / 2], 2.5, 0.35, info["L"] * 2.0), "02-pumpe": ([info["x0"] + 100, info["ycent"], info["za"]], 2.5, 0.3, 700),
             "03-rueckseite": ([0, 0, info["H"] / 2], 0.6, 0.3, info["L"] * 2.0), "04-seite": ([0, 0, info["H"] / 2], 1.5708, 0.0, info["L"] * 1.8)}
    for n, (tt, yaw, pitch, dist) in views.items():
        sc.snapshot(path, os.path.join(r, f"{typ}-{n}.png"), tt, yaw, pitch, dist, w=1000, h=700)
    sc.snapshot(path, os.path.join(r, f"{typ}-05-schnitt.png"), [0, info["ycent"], info["za"]], 0.0, 0.0, info["L"] * 1.6, w=1000, h=700, section="XZ")

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["pumpe_klein", "pumpe_gross"]
    p, d = sc.load_params("pumpe")
    for typ in typs:
        T = d["typen"][typ]
        b, info = build_pumpe(typ, T, p, d)
        b.cmds = [c for c in b.cmds if c]
        out = os.path.join(sc.ROOT, "designs", "components", f"{typ}.sc")
        sc.run(b.write(typ), out)
        sc.assign_part_materials(out, "Stahl Pumpe")                 # Normteile (Body<n>) auf Stahl (Dichte 7,85)
        ev = sc.evaluate(out)
        print(typ, "Koerper", len(ev["bodies"]), "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 2), "kg")
        if "--render" in sys.argv:
            render(typ, out, info)
