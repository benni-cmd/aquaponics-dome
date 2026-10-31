"""Menschenfigur 1,80 m T90 (W29, D47): Groessenreferenz aus einfachen Koerpern, Proportionen Drillis/Contini (Anteile der Koerperhoehe H).
Konfigurationen (data/components/mensch_referenz.json typen): aufrecht -> mensch_referenz.sc, messen -> mensch_referenz_messen.sc, arbeiten -> mensch_referenz_arbeiten.sc.
KS: Ursprung Fussmitte am Boden (Z 0), Blickrichtung +Y, rechte Hand +X. Oberkoerper um die Huefte (z = 0,53 H) um `lean` nach vorn geneigt, Arme per Zwei-Knochen-IK auf die Handziele.
Aufruf: python scripts/workshop/mensch.py [aufrecht|messen|arbeiten ...] [--render]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

OUT = {"aufrecht": "mensch_referenz", "messen": "mensch_referenz_messen", "arbeiten": "mensch_referenz_arbeiten"}

def v_add(a, b): return [a[i] + b[i] for i in range(3)]
def v_sub(a, b): return [a[i] - b[i] for i in range(3)]
def v_mul(a, k): return [a[i] * k for i in range(3)]
def v_dot(a, b): return sum(a[i] * b[i] for i in range(3))
def v_len(a): return math.sqrt(v_dot(a, a))
def v_unit(a): return v_mul(a, 1.0 / v_len(a))

def ik(S, T, l1, l2, pole):
    """Ellbogenpunkt zu Schulter S und Handziel T (Knochenlaengen l1, l2); der Ellbogen weicht zur Richtung pole aus."""
    d = v_sub(T, S)
    dist = min(v_len(d), l1 + l2 - 1.0)
    u = v_unit(d)
    a = (l1 * l1 - l2 * l2 + dist * dist) / (2 * dist)
    h = math.sqrt(max(l1 * l1 - a * a, 0.0))
    n = v_unit(v_sub(pole, v_mul(u, v_dot(pole, u))))
    return v_add(S, v_add(v_mul(u, a), v_mul(n, h)))

def limb(b, name, a, z_, dia, material, op="new", targets=None):
    ax = v_sub(z_, a)
    kw = dict(diameter=dia, height=round(v_len(ax), 3), base=[round(v, 3) for v in a], axis=[round(v, 5) for v in v_unit(ax)], operation=op, name="L_" + name)
    if op == "new":
        kw["body_name"] = name
    else:
        kw["targets"] = targets
    b.add("solid.cylinder", **kw)
    if op == "new":
        b.add("material.assign", bodies=[name], material=material)

def geometry(p, T):
    """Gelenkpunkte der Figur (mm) aus Parametern und Konfiguration."""
    H = p["height"]
    th = math.radians(T["lean"])
    hip, sh_h = p["k_hip"] * H, p["k_shoulder"] * H
    u = [0.0, math.sin(th), math.cos(th)]                          # Rumpf-Achse (nach oben, vorn geneigt)
    piv = [0.0, 0.0, hip]
    sh = {s: v_add(v_add(piv, v_mul(u, sh_h - hip - 40)), [s * (p["k_sw"] * H / 2 - 40), 0.0, 0.0]) for s in (-1, 1)}   # Schultergelenk 40 mm unter der Rumpfoberkante, Armaussenkante = Schulterbreite/2
    G = dict(H=H, th=th, u=u, piv=piv, sh=sh, hip=hip, sh_h=sh_h)
    G["l1"] = sh_h - 40 - p["k_elbow"] * H                          # Oberarm Schultergelenk -> Ellbogen (Ellbogen auf 0,63 H, Gelenk 40 unter der Rumpfoberkante)
    G["l2f"], G["lh"] = 250.0, 170.0                                 # Unterarm bis Handgelenk, Hand
    G["head_c"] = v_add(piv, v_mul(u, H - 95 - hip))                 # Kopfmitte: Scheitel bei H (aufrecht)
    arms = {}
    for s, key in ((1, "hand_r"), (-1, "hand_l")):
        if key in T:
            tgt = [T[key][0] * H, T[key][1] * H, T[key][2] * H]
            arms[s] = (tgt, ik(sh[s], tgt, G["l1"], G["l2f"] + G["lh"] / 2, [s * 0.3, 0.0, -1.0]))
        else:                                                         # Arme haengen
            e = [sh[s][0], sh[s][1], sh[s][2] - G["l1"]]
            wrist = [e[0], e[1], e[2] - G["l2f"]]
            arms[s] = ([wrist[0], wrist[1], wrist[2] - G["lh"] / 2], e)
    G["arms"] = arms
    return G

def build(typ):
    p, d = sc.load_params("mensch_referenz")
    T = d["typen"][typ]
    G = geometry(p, T)
    H = G["H"]
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, col in (("Kleidung blau", "#2f5fa8"), ("Weste orange", "#f08a24"), ("Haut", "#e0b48f"), ("Geraet dunkel", "#3a3f44")):
        b.add("material.create", name=nm, density_g_cm3=p["rho"], color=col)
    root = "T90_Mensch_" + typ
    b.add("component.create", name=root, grounded=True)
    u, piv, th = G["u"], G["piv"], G["th"]
    # --- Rumpf: Rechteck 466 x 230 in der Ebene normal zur Rumpfachse, von der Huefte bis zur Schulter (Westenfarbe)
    b.add("component.create", name="T90a_Rumpf")
    b.add("sketch.create", plane={"origin": piv, "x_dir": [1, 0, 0], "y_dir": [0, round(math.cos(th), 6), round(-math.sin(th), 6)]}, name="S_Rumpf")
    b.add("sketch.rectangle.rounded", p0=[-p["k_sw"] * H / 2, -115], p1=[p["k_sw"] * H / 2, 115], radius=60)
    b.add("sketch.finish")
    b.add("solid.extrude", distance=G["sh_h"] - G["hip"], name="F_Rumpf", body_name="Rumpf")
    b.add("material.assign", bodies=["Rumpf"], material="Weste orange")
    # --- Kopf: Kugel D190 + Hals D110 (Kopf 0,13 H = 234 Scheitel bis Kinn)
    b.add("component.activate", component=root)
    b.add("component.create", name="T90b_Kopf")
    hc = G["head_c"]
    b.add("solid.sphere", diameter=190, center=[round(v, 3) for v in hc], operation="new", name="K_R", body_name="Kopf")
    neck_a = v_add(piv, v_mul(u, G["sh_h"] - G["hip"] - 30))
    limb(b, "Kopf", neck_a, hc, 110, None, op="join", targets=["Kopf"])
    b.add("material.assign", bodies=["Kopf"], material="Haut")
    # --- Arme
    b.add("component.activate", component=root)
    b.add("component.create", name="T90c_Arme")
    for s, tag in ((1, "R"), (-1, "L")):
        tgt, elb = G["arms"][s]
        S = G["sh"][s]
        wrist = v_add(elb, v_mul(v_unit(v_sub(tgt, elb)), G["l2f"]))
        hand_end = v_add(wrist, v_mul(v_unit(v_sub(tgt, elb)), G["lh"]))
        limb(b, f"Arm_{tag}_Ober", S, elb, 80, "Kleidung blau")
        limb(b, f"Arm_{tag}_Unter", elb, wrist, 65, "Kleidung blau")
        limb(b, f"Hand_{tag}", wrist, hand_end, 70, "Haut")
    if "hand_l" in T and typ == "messen":                              # Messgeraet in der linken Hand
        tgt = [T["hand_l"][0] * H, T["hand_l"][1] * H, T["hand_l"][2] * H]
        b.add("solid.box", length=70, width=160, height=30, center=[round(tgt[0], 3), round(tgt[1] + 60, 3), round(tgt[2] + 20, 3)], operation="new", name="Geraet_R", body_name="Messgeraet")
        b.add("material.assign", bodies=["Messgeraet"], material="Geraet dunkel")
    # --- Beine und Fuesse (Beine stehen senkrecht, Fuesse auf dem Boden)
    b.add("component.activate", component=root)
    b.add("component.create", name="T90d_Beine")
    hip, knee, ank = p["k_hip"] * H, p["k_knee"] * H, p["k_ankle"] * H
    fw, fl = p["k_fw"] * H, p["k_fl"] * H
    for s, tag in ((1, "R"), (-1, "L")):
        x = s * 100.0
        limb(b, f"Bein_{tag}_Ober", [x, 0, hip], [x, 0, knee], 150, "Kleidung blau")
        limb(b, f"Bein_{tag}_Unter", [x, 0, knee], [x, 0, ank], 100, "Kleidung blau")
        b.add("solid.box", length=round(fw, 3), width=round(fl, 3), height=round(ank, 3), center=[x, round(fl / 2 - 70, 3), round(ank / 2, 3)], operation="new", name="Fuss_" + tag + "_R", body_name=f"Fuss_{tag}")
        b.add("material.assign", bodies=[f"Fuss_{tag}"], material="Geraet dunkel")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T90", d["beschreibung"]), ("T90a_Rumpf", "T90a", "Rumpf 466 x 230"), ("T90b_Kopf", "T90b", "Kopf und Hals"), ("T90c_Arme", "T90c", "Arme und Haende"), ("T90d_Beine", "T90d", "Beine und Fuesse")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": "Referenz"})
    return b, G

if __name__ == "__main__":
    typs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["aufrecht", "messen", "arbeiten"]
    for typ in typs:
        b, G = build(typ)
        out = os.path.join(sc.ROOT, "designs", "components", OUT[typ] + ".sc")
        sc.run(b.write(OUT[typ]), out)
        ev = sc.evaluate(out)
        mn, mx = sc.bbox_all(ev)
        print(typ, "Koerper", len(ev["bodies"]), "Flaechen", sum(x["faces"] for x in ev["bodies"]), "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 1), "kg bbox", [round(v) for v in mn], [round(v) for v in mx])
        if "--render" in sys.argv:
            rd = os.path.join(sc.ROOT, "renders", "components", "mensch_referenz")
            os.makedirs(rd, exist_ok=True)
            sc.snapshot(out, os.path.join(rd, f"mensch_referenz_{typ}-seite.png"), [0, 150, 900], 1.5708, 0.0, 4200, w=800, h=900)
            sc.snapshot(out, os.path.join(rd, f"mensch_referenz_{typ}-schraeg.png"), [0, 150, 900], 0.7, 0.2, 4200, w=800, h=900)
