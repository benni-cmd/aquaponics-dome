"""Prototyp Scherenknoten (W74, R56): EINE Lochplatte und EINE Schere in einem Rohrstueck, Nasen ausgefahren (eingerastet).
Prinzip nach Foto reference/chemnitz/laschenknoten-foto.jpg: zwei gekreuzte Flachstahl-Laschen mit Drehpunktschraube;
innen im Rohr tragen sie je eine Nase, die durch ein Wandloch nach aussen ragt; aussen liegen beide Laschenaugen
deckungsgleich auf der Lochplatte und werden mit EINER Schraube festgeschraubt. Gedeckte Augen = Schere geschlossen = Nasen aussen.
Geoeffnet (Augen auseinander, halber Winkel ca. 6,5 Grad) ziehen die Nasen ins Rohr ein: so wird das Rohr aufgesteckt.

Koordinaten: Knotenpunkt = Ursprung, Z = Kuppelnormale (aussen), Lochplatte in der Tangentialebene,
Strebe in +X, um die Neigung B (18,0 Grad, asin(3708/12000)) nach innen gekippt. Die Laschen knicken ausserhalb der Platte
um diese Neigung ab; die Rohrachse (Mittelebene des Laschenpakets) geht durch den Knotenpunkt.
Alle Kopfmasse [A] (R56, Foto ohne Massstab). Rohr: Rundrohr 42,4 x 2,6 (Empfehlung R56).
Aufruf: python -X utf8 scripts/components/knoten_schere_proto.py [--check]   -> designs/components/knoten_schere_proto.sc"""
import math, os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "workshop"))
import sc

P = dict(tilt=math.degrees(math.asin(3708 / 12000)),
         plate_d=110, plate_t=8, bolt_circle_r=37, center_hole=20, plate_hole=11,
         link_w=20, link_t=5, eye_r=10, a_plate_to_pivot=50, bend_r=63,
         b_pivot_to_nose=58, nose_w=10, nose_out=3, tip_past_nose=8, pivot_hole=9,
         tube_d=42.4, tube_t=2.6, tube_len=250, pivot_out=12, wall_hole=13)
OUT = os.path.join(sc.ROOT, "designs", "components", "knoten_schere_proto.sc")
MAT, MATB, MATR = "Stahl Laserteil", "Stahl Schraube", "Stahl verzinkt"

th = math.radians(P["tilt"])
u = [math.cos(th), 0.0, -math.sin(th)]      # Strebenachse
nrm = [math.sin(th), 0.0, math.cos(th)]     # Normale der gekippten Laschenebene
Y = [0.0, 1.0, 0.0]
add = lambda a, b, s=1.0: [a[i] + s * b[i] for i in range(3)]
r4 = lambda v: [round(x, 4) for x in v]
z_mid = -P["bend_r"] * math.tan(th)                         # Mittelebene des Laschenpakets an der Knicklinie (Achse durch Ursprung)
z_top = z_mid - P["link_t"]                                 # Plattenoberkante (Lasche 1 liegt auf, Lasche 2 auf Lasche 1)
B0 = [P["bend_r"], 0.0, z_mid]
s_pivot = P["bolt_circle_r"] + P["a_plate_to_pivot"] - P["bend_r"]     # Lauflaenge ab Knick bis Drehpunkt
s_nose = s_pivot + P["b_pivot_to_nose"]
s_tip = s_nose + P["tip_past_nose"]
s_tube = s_pivot + P["pivot_out"]
nose_y = P["tube_d"] / 2 + P["nose_out"]                    # Nasenspitze von der Achse
w2 = P["link_w"] / 2

def arc(cx, cy, r, a0, a1, n=10):
    return [[round(cx + r * math.cos(a0 + (a1 - a0) * k / n), 4), round(cy + r * math.sin(a0 + (a1 - a0) * k / n), 4)] for k in range(n + 1)]

def build():
    b = sc.Build()
    for nm, col in ((MAT, "#8a8378"), (MATB, "#c9ced3"), (MATR, "#b9c0c8")):
        b.add("material.create", name=nm, density_g_cm3=7.85, color=col, pbr={"metallic": 0.8, "roughness": 0.5, "dielectric_ior": 1.5})
    root = "Knoten_Schere_Proto"
    b.add("component.create", name=root)
    # --- Lochplatte: Scheibe, 6 Loecher auf dem Lochkreis, Mittelbohrung
    b.add("solid.cylinder", diameter=P["plate_d"], height=P["plate_t"], base=[0, 0, z_top - P["plate_t"]], axis=[0, 0, 1], operation="new", name="Lochplatte_F", body_name="Lochplatte")
    b.add("solid.cylinder", diameter=P["center_hole"], height=P["plate_t"] + 2, base=[0, 0, z_top - P["plate_t"] - 1], axis=[0, 0, 1], operation="cut", targets=["Lochplatte"], name="Mittelbohrung")
    for k in range(6):
        a = math.radians(60 * k)
        b.add("solid.cylinder", diameter=P["plate_hole"], height=P["plate_t"] + 2, base=[round(P["bolt_circle_r"] * math.cos(a), 4), round(P["bolt_circle_r"] * math.sin(a), 4), z_top - P["plate_t"] - 1], axis=[0, 0, 1], operation="cut", targets=["Lochplatte"], name=f"Lochkreis_{k + 1}")
    b.add("material.assign", bodies=["Lochplatte"], material=MAT)
    # --- zwei Laschen: flaches Stueck auf der Platte (Auge), Knick, gekipptes Stueck mit Drehpunkt und Nase
    for k, side in ((1, -1), (2, 1)):                        # Lasche 1 unten, Nase nach -Y; Lasche 2 oben, Nase nach +Y
        body = f"Lasche_{k}"
        zb = z_mid - P["link_t"] if k == 1 else z_mid          # Unterseite der Lasche im flachen Stueck
        ext = 0.0 if k == 1 else 1.0                          # Knick: Lasche 1 innen (Teile ueberlappen sich selbst), Lasche 2 aussen (1 mm Zugabe schliesst den Keil)
        flat = arc(P["bolt_circle_r"], 0, w2, math.pi / 2, 3 * math.pi / 2) + [[P["bend_r"] + ext, -w2], [P["bend_r"] + ext, w2]]
        b.add("sketch.create", plane={"origin": [0, 0, round(zb, 4)], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name=f"S_{body}_flach")
        b.add("sketch.line", points=flat, closed=True)
        b.add("sketch.finish")
        b.add("solid.extrude", distance=P["link_t"], name=f"F_{body}_flach", body_name=body)
        if k == 1:                                            # Innenseite des Knicks: Biegewulst r 2,3 unter beiden Oberflaechen verbindet die Teile mit Volumen
            nb = [(nrm[i] + (0, 0, 1)[i]) for i in range(3)]; ln = math.sqrt(sum(x * x for x in nb)); nb = [x / ln for x in nb]
            cc = add(B0, nb, -2.5)
            b.add("solid.cylinder", diameter=4.6, height=P["link_w"], base=r4(add(cc, Y, -w2)), axis=Y, operation="join", targets=[body], name=f"Knick_{k}")
        # gekipptes Stueck: lokale x = Lauflaenge ab Knick, y = quer; Nase als Lappen an der Seite 'side'
        n0, n1 = s_nose - P["nose_w"] / 2, s_nose + P["nose_w"] / 2
        s0 = -ext
        if side < 0:
            poly = [[s0, -w2], [n0, -w2], [n0, -nose_y], [n1, -nose_y], [n1, -w2], [s_tip, -w2], [s_tip, w2], [s0, w2]]
        else:
            poly = [[s0, -w2], [s_tip, -w2], [s_tip, w2], [n1, w2], [n1, nose_y], [n0, nose_y], [n0, w2], [s0, w2]]
        off = -P["link_t"] if k == 1 else 0.0
        b.add("sketch.create", plane={"origin": r4(add(B0, nrm, off)), "x_dir": r4(u), "y_dir": Y}, name=f"S_{body}_schraeg")
        b.add("sketch.line", points=[[round(x, 4), round(y, 4)] for x, y in poly], closed=True)
        b.add("sketch.finish")
        b.add("solid.extrude", distance=P["link_t"], operation="join", targets=[body], name=f"F_{body}_schraeg")
        # Augenloch (Plattenschraube) und Drehpunktloch
        b.add("solid.cylinder", diameter=P["plate_hole"], height=40, base=[P["bolt_circle_r"], 0, z_top - 20], axis=[0, 0, 1], operation="cut", targets=[body], name=f"Auge_{k}")
        b.add("solid.cylinder", diameter=P["pivot_hole"], height=40, base=r4(add(add(B0, u, s_pivot), nrm, -20)), axis=r4(nrm), operation="cut", targets=[body], name=f"Drehloch_{k}")
        b.add("material.assign", bodies=[body], material=MAT)
    # --- Rohrstueck Rund 42,4 x 2,6 mit zwei gegenueberliegenden Wandloechern auf Hoehe der Nasen
    t0 = add(B0, u, s_tube)
    b.add("solid.cylinder", diameter=P["tube_d"], height=P["tube_len"], base=r4(t0), axis=r4(u), operation="new", name="Rohr_F", body_name="Rohrstueck")
    b.add("solid.cylinder", diameter=P["tube_d"] - 2 * P["tube_t"], height=P["tube_len"] + 2, base=r4(add(t0, u, -1)), axis=r4(u), operation="cut", targets=["Rohrstueck"], name="Rohr_innen")
    for k, side in ((1, -1), (2, 1)):
        c = add(add(B0, u, s_nose), nrm, -P["link_t"] / 2 if k == 1 else P["link_t"] / 2)
        base = add(c, Y, side * (P["tube_d"] / 2 - P["tube_t"] - 2))
        b.add("solid.cylinder", diameter=P["wall_hole"], height=P["tube_t"] + 4, base=r4(base), axis=[0, side, 0], operation="cut", targets=["Rohrstueck"], name=f"Wandloch_{k}")
    b.add("material.assign", bodies=["Rohrstueck"], material=MATR)
    # --- Schrauben: Plattenschraube M10 (Kopf oben auf Lasche 2, Mutter unter der Platte), Drehpunkt M8
    top_p = [P["bolt_circle_r"], 0, z_mid + P["link_t"]]
    bot_p = [P["bolt_circle_r"], 0, z_top - P["plate_t"]]
    piv = add(B0, u, s_pivot)
    ptop, pbot = add(piv, nrm, P["link_t"]), add(piv, nrm, -P["link_t"])
    ins = [("washer", "M10", None, top_p, [0, 0, 1], "Platte_ScheibeO"), ("hex_bolt", "M10", 35, add(top_p, [0, 0, 1], 2), [0, 0, 1], "Platte_Schraube"),
           ("washer", "M10", None, bot_p, [0, 0, -1], "Platte_ScheibeU"), ("hex_nut", "M10", None, add(bot_p, [0, 0, -1], 2), [0, 0, -1], "Platte_Mutter"),
           ("washer", "M8", None, ptop, nrm, "Dreh_ScheibeO"), ("hex_bolt", "M8", 25, add(ptop, nrm, 1.6), nrm, "Dreh_Schraube"),
           ("washer", "M8", None, pbot, [-x for x in nrm], "Dreh_ScheibeU"), ("hex_nut", "M8", None, add(pbot, nrm, -1.6), [-x for x in nrm], "Dreh_Mutter")]
    for fam, size, ln, pt, d, nm in ins:
        kw = dict(family=fam, size=size, point=r4(pt), direction=r4(d), name=nm)
        if ln: kw["length"] = ln
        b.add("parts.insert", **kw)
    for j, (*_, nm) in enumerate(ins, 1):
        b.add("body.rename", body=f"Body{j}", name=nm)
    b.add("material.assign", bodies=[x[-1] for x in ins], material=MATB)
    return b

def check():
    ev = sc.evaluate(OUT)
    bodies = {x["name"]: x for x in ev["bodies"]}
    c = sc.Check("knoten_schere_proto")
    c.eq("Koerperzahl (Platte, 2 Laschen, Rohr, 8 Normteile)", len(bodies), 12)
    c.eq("alle Koerper geschlossen", sum(1 for x in ev["bodies"] if x.get("closed")), 12)
    for nm in ("Lasche_1", "Lasche_2"):
        bb = bodies[nm]["bbox"]
        reach = max(abs(bb["min"][1]), abs(bb["max"][1]))
        c.eq(f"{nm}: Nase ragt {P['nose_out']} mm ueber die Rohraussenwand (|Y| max)", round(reach, 2), nose_y, 0.05)
    # Achse des Rohrs durch den Knotenpunkt: Abstand Ursprung zur Achsgeraden
    t0 = add(B0, u, s_tube); dist = math.sqrt(sum((t0[i] - u[i] * sum(t0[j] * u[j] for j in range(3))) ** 2 for i in range(3)))
    c.eq("Rohrachse geht durch den Knotenpunkt (Abstand mm)", round(dist, 3), 0.0, 0.01)
    # Durchdringung Lasche/Rohr nur als Nase im Wandloch: inspect.interference zwischen Laschen und Rohr
    script = os.path.join(sc.TMP, "ws-schere-int.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"bodies": ["Lasche_1", "Lasche_2", "Rohrstueck", "Lochplatte"]}}]}, open(script, "w"))
    import subprocess
    r = subprocess.run([sc.CLI, "run", script, "--in", OUT, "--results"], capture_output=True, text=True)
    res = json.loads(r.stdout)[0] if r.returncode == 0 else {}
    print("interference:", json.dumps(res)[:600])
    pairs = res.get("interferences", res.get("pairs", []))
    c.eq("Durchdringungen Laschen/Rohr/Platte", len(pairs), 0)
    m = {k: round(v.get("mass_g", 0)) for k, v in bodies.items()} if "mass_g" in next(iter(bodies.values())) else {}
    print("Massen g:", m)
    return c.done()

def render():
    d = os.path.join(sc.ROOT, "renders", "components", "knoten_schere_proto")
    glass = ["--body", "Rohrstueck:opacity=0.25"]
    views = (("01-iso", 0.75, 0.55, 330, []), ("02-iso-rohr-durchsichtig", 0.75, 0.55, 330, glass),
             ("03-draufsicht-durchsichtig", 0.0, 1.5607, 330, glass), ("04-seite", 0.0, 0.0, 330, glass),
             ("05-nase-detail", 0.35, 0.25, 220, []))
    for nm, yaw, pitch, dist, extra in views:
        tgt = [130, 0, -40] if nm != "05-nase-detail" else r4(add(B0, u, s_nose))
        sc.snapshot(OUT, os.path.join(d, f"knoten_schere_proto-{nm}.png"), tgt, yaw, pitch, dist, w=1200, h=800, extra=extra)
        print(os.path.join(d, f"knoten_schere_proto-{nm}.png"))

if __name__ == "__main__":
    if "--render" in sys.argv:
        render(); sys.exit(0)
    if "--check" not in sys.argv:
        b = build()
        sc.run(b.write("knoten-schere-proto"), OUT)
        n = sc.assign_part_materials(OUT, MATB)
        print("gespeichert", OUT, "Normteile nachgetragen:", n)
        print(f"Neigung {P['tilt']:.2f} Grad, Plattenoberkante z {z_top:.2f}, Drehpunkt s {s_pivot}, Nase s {s_nose}, Rohrende s {s_tube}, Knotenpunkt->Rohrende {math.hypot(B0[0], B0[2]) + s_tube:.1f} mm")
    sys.exit(check())
