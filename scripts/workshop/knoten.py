"""Kuppelknoten T60 (4-, 5-, 6-wertig): Knotenkugel + Steckarme in den Strebenrichtungen (aus layout.json), M10-Verschraubung je Strebe, Ankerlasche an Basisknoten.
Ursprung = Knotenmitte; Richtungen im Koordinatensystem von layout.json. Aufruf: python scripts/workshop/knoten.py [id ...] [--render]  (ohne id: alle 26; ids 0-25)"""
import sys, os, math, json, itertools, shutil
sys.path.insert(0, os.path.dirname(__file__))
import sc

CENTER = (0.0, 0.0, -14.0)      # Kuppelmittelpunkt (Basis z = -14, Radius 6000, apex 5986)

def vsub(a, b): return [a[i] - b[i] for i in range(3)]
def vlen(a): return math.sqrt(sum(x * x for x in a))
def vunit(a):
    l = vlen(a)
    return [x / l for x in a]
def vdot(a, b): return sum(a[i] * b[i] for i in range(3))
def vcross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def vadd(a, b, s=1.0): return [a[i] + s * b[i] for i in range(3)]
def vscale(a, s): return [x * s for x in a]

def nodes():
    d = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    return d["nodes_list"], d["strut_len_mm"]

def neighbours(N, tol):
    nb = {i: [] for i in range(len(N))}
    for i, j in itertools.combinations(range(len(N)), 2):
        a, b = [N[i][k] for k in "xyz"], [N[j][k] for k in "xyz"]
        dd = vlen(vsub(a, b))
        for L, t in ((3279, "A"), (3708, "B")):
            if abs(dd - L) < tol:
                nb[i].append((j, t, dd)); nb[j].append((i, t, dd))
    return nb

def node_geometry(i, N, nb, p):
    pos = [N[i][k] for k in "xyz"]
    n = vunit(vsub(pos, CENTER))
    arms = []
    for j, t, dd in nb[i]:
        u = vunit(vsub([N[j][k] for k in "xyz"], pos))
        arms.append(dict(nachbar=j, typ=t, laenge=round(dd, 1), u=u, kipp=math.degrees(math.asin(max(-1, min(1, vdot(u, n)))))))
    theta_min = min(math.degrees(math.acos(max(-1, min(1, vdot(a["u"], b["u"]))))) for a, b in itertools.combinations(arms, 2))
    rb = p["ball_d"] / 2
    return dict(pos=pos, n=n, arms=arms, theta_min=theta_min, rho0=rb - p["arm_root"], ball_r=rb)

def build(i, N, nb, p, d):
    G = node_geometry(i, N, nb, p)
    val = N[i]["valence"]
    n, arms = G["n"], G["arms"]
    w = p["spigot_w"]
    b = sc.Build()
    for k, v in p.items():
        b.add("parameters.add", name=k, expression=f"{v} mm")
    b.add("material.create", name="Stahl Knoten", density_g_cm3=7.85, color=d["werkstoff"]["farbe"], pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    root = f"T60_Knoten_{val}_n{i + 1:02d}"
    b.add("component.create", name=root, grounded=True)
    # --- Knotenkugel
    b.add("component.create", name="T60a_Kugel")
    b.add("solid.sphere", diameter="ball_d", center=[0, 0, 0], operation="new", name="Kugel_R", body_name="Knotenkugel")
    b.add("material.assign", bodies=["Knotenkugel"], material="Stahl Knoten")
    # --- Steckarme je Strebe (Rechteckrohr; Hoehenrichtung = Kuppelnormale n, auf u projiziert)
    b.add("component.activate", component=root)
    b.add("component.create", name="T60b_Arme")
    arm_len = p["strut_end_offset"] + p["hub_insert"] - G["rho0"]
    for k, a in enumerate(arms, 1):
        u = a["u"]
        bperp = vunit(vsub(n, vscale(u, vdot(n, u))))
        xdir = vunit(vcross(bperp, u))                             # xdir x bperp = u
        origin = vscale(u, G["rho0"])
        b.add("sketch.create", plane={"origin": [round(x, 4) for x in origin], "x_dir": [round(x, 6) for x in xdir], "y_dir": [round(x, 6) for x in bperp]}, name=f"S_Arm{k}")
        b.add("frame.profile.insert", profile=dict(kind="rect_tube", width=w, height=w, wall=p["spigot_wall"]), at=[0, 0], anchor="center")
        b.add("sketch.finish")
        b.add("solid.extrude", distance=arm_len, name=f"F_Arm{k}", body_name=f"Arm_{k}")
        b.add("material.assign", bodies=[f"Arm_{k}"], material="Stahl Knoten")
        a["_bperp"] = bperp
    # --- Querbolzen M10 je Arm durch Steckarm und Strebe (Strebenende bei strut_end_offset)
    b.add("component.activate", component=root)
    b.add("component.create", name="T60c_Verschraubung")
    for k, a in enumerate(arms, 1):
        u, ax = a["u"], a["_bperp"]
        pb = vscale(u, p["strut_end_offset"] + p["bolt_dist"])
        b.add("solid.cylinder", diameter=p["bolt_hole"], height=w + 2, base=[round(x, 4) for x in vadd(pb, ax, -w / 2 - 1)], axis=[round(x, 6) for x in ax], operation="cut", targets=[f"Arm_{k}"], name=f"Loch_Arm_{k}")
        top = vadd(pb, ax, 15)                                      # Aussenflaeche der Strebe (30 x 30)
        bot = vadd(pb, ax, -15)
        b.add("parts.insert", family="washer", size="M10", point=[round(x, 4) for x in top], direction=[round(x, 6) for x in ax], name=f"ScheibeO_{k}")
        b.add("parts.insert", family="hex_bolt", size="M10", length=p["bolt_len"], point=[round(x, 4) for x in vadd(top, ax, p["washer_t"])], direction=[round(x, 6) for x in ax], name=f"Schraube_{k}")
        b.add("parts.insert", family="washer", size="M10", point=[round(x, 4) for x in bot], direction=[round(-x, 6) for x in ax], name=f"ScheibeU_{k}")
        b.add("parts.insert", family="hex_nut", size="M10", point=[round(x, 4) for x in vadd(bot, ax, -p["washer_t"])], direction=[round(-x, 6) for x in ax], name=f"Mutter_{k}")
    # --- Ankerlasche (nur Basisknoten, Wertigkeit 4): Platte nach unten, Loch D14 fuer M12
    if val == 4:
        b.add("component.activate", component=root)
        b.add("component.create", name="T60d_Ankerlasche")
        nh = vunit([n[0], n[1], 0.0])
        th = vunit(vcross([0, 0, 1], nh))
        zt = -G["ball_r"] + 6
        b.add("sketch.create", plane={"origin": [0, 0, round(zt, 3)], "x_dir": [round(x, 6) for x in nh], "y_dir": [round(x, 6) for x in th]}, name="S_Lasche")
        b.add("sketch.rectangle.center", center=[0, 0], corner=[p["lug_w"] / 2, p["lug_t"] / 2])
        b.add("sketch.finish")
        b.add("solid.extrude", distance=p["lug_l"], direction="negative", name="F_Lasche", body_name="Ankerlasche")
        b.add("solid.cylinder", diameter=p["lug_hole"], height=p["lug_t"] + 4, base=[round(-th[k_] * (p["lug_t"] / 2 + 2), 4) if k_ < 2 else round(zt - p["lug_l"] + 35, 4) for k_ in range(3)], axis=[round(x, 6) for x in th], operation="cut", targets=["Ankerlasche"], name="Laschenloch")
        b.add("material.assign", bodies=["Ankerlasche"], material="Stahl Knoten")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, f"T60_{val}", f"Kuppelknoten {val}-wertig, Knoten n{i + 1:02d}"), ("T60a_Kugel", "T60a", "Knotenkugel D100"), ("T60b_Arme", "T60b", "Steckarme"), ("T60c_Verschraubung", "T60c", "Schrauben M10 mit Scheiben und Muttern")) + ((("T60d_Ankerlasche", "T60d", "Ankerlasche Basisknoten"),) if val == 4 else ()):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, G

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:] if not a.startswith("--")]
    p, d = sc.load_params("knoten")
    N, _ = nodes()
    nb = neighbours(N, p["neighbor_tol"])
    arme = {}
    for i in ids or range(len(N)):
        b, G = build(i, N, nb, p, d)
        out = os.path.join(sc.ROOT, "designs", "components", f"knoten_{N[i]['valence']}_n{i + 1:02d}.sc")
        sc.run(b.write(f"knoten_{i + 1}"), out)
        ev = sc.evaluate(out)
        print(i + 1, "Wertigkeit", N[i]["valence"], "min. Armwinkel %.1f" % G["theta_min"], "Koerper", len(ev["bodies"]), "Masse %.2f kg" % (sum(x["mass_g"] for x in ev["bodies"]) / 1000))
        arme[i + 1] = dict(valenz=N[i]["valence"], pos=[round(x, 1) for x in G["pos"]], n=[round(x, 5) for x in G["n"]], rho0=round(G["rho0"], 1), ball_r=round(G["ball_r"], 1),
                           arme=[dict(nachbar=a["nachbar"] + 1, typ=a["typ"], laenge=a["laenge"], kipp_gegen_tangentialebene=round(a["kipp"], 2), u=[round(x, 6) for x in a["u"]]) for a in G["arms"]])
        if "--render" in sys.argv:
            r = os.path.join(sc.ROOT, "renders", "components", f"knoten_{N[i]['valence']}")
            os.makedirs(r, exist_ok=True)
            for nme, (yaw, pitch, dist) in {"01-iso": (0.7, 0.4, 700), "02-draufsicht": (0.0, 1.45, 600), "03-seite": (1.5, 0.1, 700)}.items():
                sc.snapshot(out, os.path.join(r, f"knoten_{N[i]['valence']}_n{i + 1:02d}-{nme}.png"), [0, 0, 0], yaw, pitch, dist, w=900, h=700)
    if not ids:
        json.dump(arme, open(os.path.join(sc.ROOT, "data", "components", "knoten_arme.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
