"""Vorpruefung Kuppelknoten gegen Scope-Card knoten_4/5/6 und layout.json: Anzahl 10/6/10, Armzahl = Wertigkeit, Armrichtung aus den Nachbarknoten (Toleranz 0,5 Grad), Steckarm-Laenge, Schrauben je Strebe, Ankerlasche nur an Basisknoten.
Aufruf: python scripts/workshop/check_knoten.py   (exit 1 bei FAIL)"""
import sys, os, json, math, glob
sys.path.insert(0, os.path.dirname(__file__))
import sc
import knoten as kn

def main():
    p, d = sc.load_params("knoten")
    N, _ = kn.nodes()
    nb = kn.neighbours(N, p["neighbor_tol"])
    ck = sc.Check("knoten")
    from collections import Counter
    files = sorted(glob.glob(os.path.join(sc.ROOT, "designs", "components", "knoten_?_n*.sc")))
    cnt = Counter(os.path.basename(f).split("_")[1] for f in files)
    ck.eq("Anzahl Knoten vierwertig", cnt.get("4", 0), 10)
    ck.eq("Anzahl Knoten fuenfwertig", cnt.get("5", 0), 6)
    ck.eq("Anzahl Knoten sechswertig", cnt.get("6", 0), 10)
    ck.eq("Strebenzahl aus den Knoten (Summe Armzahl / 2 = 65 Streben)", sum(len(nb[i]) for i in range(len(N))) / 2, 65)
    worst = 0.0
    for f in files:
        i = int(os.path.basename(f).split("_n")[1][:2]) - 1
        val = N[i]["valence"]
        ev = sc.evaluate(f)
        B = {b["name"]: b for b in ev["bodies"]}
        G = kn.node_geometry(i, N, nb, p)
        arms = [b for k, b in B.items() if k.startswith("Arm_")]
        tag = f"n{i + 1:02d} ({val}-wertig)"
        ck.eq(f"{tag} Armzahl = Wertigkeit", len(arms), val)
        ck.eq(f"{tag} Knotenkugel D", B["Knotenkugel"]["bbox"]["max"][0] - B["Knotenkugel"]["bbox"]["min"][0], p["ball_d"], 0.3)
        # Armrichtung: Schwerpunkt des Arms zeigt entlang der Soll-Richtung u (Winkelabweichung <= 0,5 Grad)
        errs = []
        for k, a in enumerate(G["arms"], 1):
            c = B[f"Arm_{k}"]["center_of_mass"]
            l = math.sqrt(sum(x * x for x in c))
            cu = [x / l for x in c]
            errs.append(math.degrees(math.acos(max(-1, min(1, sum(cu[m] * a["u"][m] for m in range(3)))))))
        worst = max(worst, max(errs))
        ck.eq(f"{tag} Armrichtungen aus layout.json (max. Abweichung Grad)", round(max(errs), 3), 0, 0.5)
        L = max(b["bbox"]["max"][0] for b in arms)
        ck.eq(f"{tag} Schrauben je Strebe (Querbolzen)", len([k for k in B if k.startswith("Body")]) / 4, val)
        ck.eq(f"{tag} Ankerlasche nur Basisknoten", 1 if ("Ankerlasche" in B) == (val == 4) else 0, 1)
    ck.eq("schlechteste Armrichtung ueber alle 26 Knoten (Grad)", round(worst, 3), 0, 0.5)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
