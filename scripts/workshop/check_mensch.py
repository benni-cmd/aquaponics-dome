"""Selbstcheck Menschenfigur T90 (W29, D47): Hoehe 1800, Schulterbreite 466, Proportionen Drillis/Contini aus den Koerper-Boxen, Masse, Flaechenzahl, Teilegroesse, Posen (Neigung, Handhoehe).
Erwartung aus den Anteilen der Koerperhoehe (Jobblatt W29), unabhaengig vom IK-Code.
Aufruf: python scripts/workshop/check_mensch.py   (exit 1 bei FAIL)"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def bodies(name):
    return {b["name"]: b for b in sc.evaluate(os.path.join(sc.ROOT, "designs", "components", name + ".sc"))["bodies"]}

def main():
    p, d = sc.load_params("mensch_referenz")
    H = p["height"]
    ck = sc.Check("mensch")
    B = bodies("mensch_referenz")
    bb = lambda n: B[n]["bbox"]
    zmax = max(b["bbox"]["max"][2] for b in B.values()); zmin = min(b["bbox"]["min"][2] for b in B.values())
    xs = (min(b["bbox"]["min"][0] for b in B.values()), max(b["bbox"]["max"][0] for b in B.values()))
    ck.eq("aufrecht: Gesamthoehe 1800 (Scheitel - Boden)", zmax - zmin, 1800, 2)
    ck.eq("aufrecht: Fuesse stehen auf dem Boden (Z 0)", zmin, 0, 0.1)
    ck.eq("aufrecht: Schulterbreite (Rumpf 466; Arme hangen innerhalb) = 0,259 H", xs[1] - xs[0], 0.259 * 1800, 10)
    ck.eq("aufrecht: Schulterhoehe (Rumpf Oberkante) = 0,818 H", bb("Rumpf")["max"][2], 0.818 * 1800, 2)
    ck.eq("aufrecht: Hueft-/Rumpfunterkante = 0,53 H", bb("Rumpf")["min"][2], 0.53 * 1800, 2)
    ck.eq("aufrecht: Kniehoehe (Unterkante Oberschenkel) = 0,285 H", bb("Bein_R_Ober")["min"][2], 0.285 * 1800, 2)
    ck.eq("aufrecht: Ellbogenhoehe (Unterkante Oberarm) = 0,63 H", bb("Arm_R_Ober")["min"][2], 0.63 * 1800, 2)      # Zylinderende senkrecht: Kante auf Ellbogenhoehe
    ck.eq("aufrecht: Fussbreite = 0,055 H", bb("Fuss_R")["max"][0] - bb("Fuss_R")["min"][0], 0.055 * 1800, 1)
    ck.eq("aufrecht: Fusslaenge = 0,152 H", bb("Fuss_R")["max"][1] - bb("Fuss_R")["min"][1], 0.152 * 1800, 1)
    ck.eq("aufrecht: Scheitel (Kopf Oberkante) = 1800 und Kopfkugel D190", abs(bb("Kopf")["max"][2] - 1800) + abs(bb("Kopf")["max"][0] - bb("Kopf")["min"][0] - 190), 0, 1.0)
    mass = sum(b["mass_g"] for b in B.values()) / 1000
    ck.eq(f"aufrecht: Masse {mass:.0f} kg zwischen 70 und 90", 1 if 70 <= mass <= 90 else 0, 1)
    for typ in ("aufrecht", "messen", "arbeiten"):
        Bt = B if typ == "aufrecht" else bodies("mensch_referenz_" + typ)
        faces = sum(b["faces"] for b in Bt.values())
        ck.eq(f"{typ}: Flaechenzahl {faces} < 800", 1 if faces < 800 else 0, 1)
        small = [k for k, b in Bt.items() if max(b["bbox"]["max"][i] - b["bbox"]["min"][i] for i in range(3)) <= 150]
        ck.eq(f"{typ}: alle Koerperteile laenger als 150 mm (Viewer blendet Kleinteile aus): zu klein {small}", len(small), 0)
        ck.eq(f"{typ}: Fuesse auf dem Boden", min(b["bbox"]["min"][2] for b in Bt.values()), 0, 0.1)
    for typ in ("messen", "arbeiten"):
        Bt = bodies("mensch_referenz_" + typ)
        T = d["typen"][typ]
        th = math.radians(T["lean"])
        r = Bt["Rumpf"]["bbox"]
        h, t = 0.818 * 1800 - 0.53 * 1800, 230.0
        ck.eq(f"{typ}: Rumpf Neigung {T['lean']} Grad: y-Ausdehnung = h sin + t cos", r["max"][1] - r["min"][1], h * math.sin(th) + t * math.cos(th), 3)
        ck.eq(f"{typ}: Rumpf Neigung: z-Ausdehnung = h cos + t sin", r["max"][2] - r["min"][2], h * math.cos(th) + t * math.sin(th), 3)
        ck.eq(f"{typ}: Scheitelhoehe liegt unter 1800 (Oberkoerper geneigt, 10 Grad ca. 11 mm)", 1 if max(b["bbox"]["max"][2] for b in Bt.values()) < 1795 else 0, 1)
        for tag, key in (("R", "hand_r"), ("L", "hand_l")):
            hb = Bt[f"Hand_{tag}"]["bbox"]
            c = [(hb["min"][i] + hb["max"][i]) / 2 for i in range(3)]
            tgt = [T[key][i] * 1800 for i in range(3)]
            ck.eq(f"{typ}: Hand {tag} Mitte (z {c[2]:.0f}) liegt am Ziel (Abstand mm)", math.dist(c, tgt), 0, 60)        # Hand = schraeger Zylinder: Boxmitte = Zylindermitte
        ck.eq(f"{typ}: Handhoehe 1100-1400 (Brust bzw. NFT-Tisch)", 1 if 1100 <= Bt["Hand_R"]["bbox"]["max"][2] <= 1400 else 0, 1)
    ck.eq("messen: Messgeraet in der linken Hand (Abstand Mitte Geraet - Hand L < 120)", math.dist([(bodies('mensch_referenz_messen')['Messgeraet']['bbox']['min'][i] + bodies('mensch_referenz_messen')['Messgeraet']['bbox']['max'][i]) / 2 for i in range(3)], [(bodies('mensch_referenz_messen')['Hand_L']['bbox']['min'][i] + bodies('mensch_referenz_messen')['Hand_L']['bbox']['max'][i]) / 2 for i in range(3)]), 0, 120)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
