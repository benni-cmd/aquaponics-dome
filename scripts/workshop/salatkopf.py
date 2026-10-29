"""Salatkopf T12 (Rev. B, 29.10. W07): ca. 50 flache polygonale Blaetter (12-Eck, unregelmaessig) auf einem Halbellipsoid-Huegel, Herz-Prisma, Wurzelhals nach -Z.
Blatt = Skizze auf geneigter Ebene (Ursprung/Achsen nur Zahlen, in mm fuer head_d 100) + Extrusion; solid.scale mit head_d/100 liefert S/M/L (Konfiguration head_d 70/100/130). Ursprung = Kragenoberkante Netztopf, Hals D16 nach unten.
Aufruf: python scripts/workshop/salatkopf.py [--render]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

def norm(v):
    l = math.sqrt(sum(c * c for c in v))
    return [c / l for c in v]

def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

def build():
    p, d = sc.load_params("salatkopf")
    G = d["blatt_gruppen"]
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    b.add("component.create", name="T12_Salatkopf", grounded=True)
    b.add("material.create", name="Salat", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"])
    jt = G["jitter"]
    rnd = lambda i: (math.sin(i * 12.9898) * 43758.5453) % 1.0 - 0.5        # deterministisch in [-0.5, 0.5)
    a, c, t = G["a"], G["b"], G["dicke"]
    # --- Herz (niedriges Achteck-Prisma unter den Blaettern)
    hz = G["herz"]
    pts = [[round(hz["r"] * math.cos(math.radians(45 * k + 22.5)), 3), round(hz["r"] * math.sin(math.radians(45 * k + 22.5)), 3)] for k in range(8)]
    b.add("sketch.create", plane={"origin": [0, 0, hz["z0"]], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_Herz")
    b.add("sketch.line", points=pts, closed=True)
    b.add("sketch.finish")
    b.add("solid.extrude", distance=hz["h"], operation="new", name="Herz", body_name="Herz")
    bodies, colors = ["Herz"], {"Herz": "#3f8a35"}
    V = G["verteilung"]
    N = V["n"]
    s0 = math.sin(math.radians(V["theta_min"]))
    for i in range(N):
        cnt = i + 1
        th = math.asin(s0 + (1 - s0) * (i + 0.5) / N)                     # Fibonacci: gleichmaessige Flaechenverteilung ueber die Huegelflaeche
        ph = i * 2.399963
        phb = ph + math.radians(V["az_streu"]) * 2 * rnd(cnt * 7 + 1)      # Blattrichtung weicht vom Radius ab
        L = V["L"] * (1 + V["L_streu"] * 2 * rnd(cnt * 7 + 2))
        w = V["w"] * (1 + V["w_streu"] * 2 * rnd(cnt * 7 + 3))
        pitch = math.radians(V["pitch0"] + V["pitch_pro_theta"] * math.degrees(th) + V["pitch_streu"] * rnd(cnt * 7 + 4))
        roll = math.radians(V["roll_streu"] * 2 * rnd(cnt * 7 + 5))
        P = [a * math.cos(th) * math.cos(ph), a * math.cos(th) * math.sin(ph), c * math.sin(th)]
        v = [math.cos(pitch) * math.cos(phb), math.cos(pitch) * math.sin(phb), math.sin(pitch)]
        u0 = [-math.sin(phb), math.cos(phb), 0.0]
        n0 = cross(u0, v)
        u = norm([u0[k] * math.cos(roll) + n0[k] * math.sin(roll) for k in range(3)])
        poly = []
        for j, (fx, fy) in enumerate(G["umriss"]):
            jx = jt["punkt"] * 2 * rnd(cnt * 31 + j * 2 + 100)
            jy = jt["punkt"] * 2 * rnd(cnt * 31 + j * 2 + 101)
            poly.append([round((fx + jx) * w, 3), round(max(0.0, (fy + jy)) * L, 3)])
        nm = f"Blatt_{cnt:02d}"
        b.add("sketch.create", plane={"origin": [round(x, 4) for x in P], "x_dir": [round(x, 6) for x in u], "y_dir": [round(x, 6) for x in v]}, name="S_" + nm)
        b.add("sketch.line", points=poly, closed=True)
        b.add("sketch.finish")
        b.add("solid.extrude", distance=t, operation="new", name="E_" + nm, body_name=nm)
        bodies.append(nm)
        colors[nm] = G["farben"][(cnt * 5 + int(math.degrees(th))) % len(G["farben"])]
    b.add("solid.scale", bodies=bodies, factor="head_d / 100 mm", origin=[0, 0, 0])
    b.add("material.assign", bodies=bodies, material="Salat")
    for col in sorted(set(colors.values())):
        b.add("appearance.assign", bodies=[n for n in bodies if colors[n] == col], color=col)
    b.add("solid.cylinder", diameter="neck_d", height="neck_len + 5", base=[0, 0, "-neck_len"], operation="new", name="Hals_R", body_name="Hals")
    b.add("material.assign", bodies=["Hals"], material="Salat")
    b.add("appearance.assign", bodies=["Hals"], color="#8ab87a")
    b.add("config.configure", params=["head_d"])
    b.add("config.row", name="M")
    b.add("config.row", name="S", **{"from": "M"}, values={"param:head_d": "70 mm"})
    b.add("config.row", name="L", **{"from": "M"}, values={"param:head_d": "130 mm"})
    b.add("config.activate", row="M")
    b.add("component.metadata.set", component="T12_Salatkopf", part_number="T12", description=d["beschreibung"], revision="B",
          properties={"Werkstoff": d["werkstoff"]["name"], "Bezugspunkt": "Z=0 Kragenoberkante Netztopf"})
    return b

if __name__ == "__main__":
    b = build()
    script = b.write("salatkopf")
    out = os.path.join(sc.ROOT, "designs", "components", "salatkopf.sc")
    sc.run(script, out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "Flaechen", sum(x["faces"] for x in ev["bodies"]), "Box", [round(v, 1) for v in mn], [round(v, 1) for v in mx])
    if "--render" in sys.argv:
        r = os.path.join(sc.ROOT, "renders", "components", "salatkopf")
        for i, (yaw, pitch) in enumerate(((0.6, 0.4), (2.2, 0.15), (0.0, 1.45)), 1):
            sc.snapshot(out, os.path.join(r, f"salatkopf-0{i+1}.png"), [0, 0, 32], yaw, pitch, 230, w=800, h=650)
