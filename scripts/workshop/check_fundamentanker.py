"""Vorpruefung Fundamentanker gegen Scope-Card (Block 400x400x600, 2 Bolzen, Anschlusslaschen) UND gegen die Ankerlasche der Knoten (Lochhoehe, Spaltweite, Loch-D): Querpruefung der Schnittstelle.
Aufruf: python scripts/workshop/check_fundamentanker.py   (exit 1 bei FAIL)"""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(__file__))
import sc

def main():
    p, d = sc.load_params("fundamentanker")
    pk, dk = sc.load_params("knoten")
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    ck = sc.Check("fundamentanker")
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "fundamentanker.sc"))
    B = {b["name"]: b for b in ev["bodies"]}
    ck.eq("Anzahl = Basisknoten (OBJ)", lay["node_valence"]["4"], dk and 10)
    bb = B["Betonpunkt"]["bbox"]
    ck.eq("Betonpunkt X", bb["max"][0] - bb["min"][0], p["block_x"], 0.1)
    ck.eq("Betonpunkt Y", bb["max"][1] - bb["min"][1], p["block_y"], 0.1)
    ck.eq("Betonpunkt Z", bb["max"][2] - bb["min"][2], p["block_z"], 0.1)
    pb = B["Ankerplatte"]["bbox"]
    ck.eq("Ankerplatte steht auf dem Beton", pb["min"][2], bb["max"][2], 0.01)
    ck.eq("Ankerplatte Seite", pb["max"][0] - pb["min"][0], p["plate_s"], 0.1)
    anchors = [b for k, b in B.items() if k.startswith(("Body", "Anker_")) and abs((b["bbox"]["max"][2] - b["bbox"]["min"][2]) - (p["anchor_len"] + 10)) < 25]
    ck.eq("Verbundanker M16 (2 Stueck)", len(anchors), 2)
    ck.eq("Anker reichen in den Beton", min(b["bbox"]["min"][2] for b in anchors) < bb["max"][2] - 250, True) if False else ck.eq("Anker reichen mind. 250 mm in den Beton", 1 if all(bb["max"][2] - b["bbox"]["min"][2] >= 250 for b in anchors) else 0, 1)
    # Schnittstelle zum Knoten: Lochhoehe, Spalt, Loch-D
    knoten_z = -dk_ball_r(pk) + 6 - pk["lug_l"] + 35
    ck.eq("Lochhoehe = Lochhoehe der Knotenlasche (knoten.json)", p["lug_hole_z"], knoten_z, 0.01)
    ga, gi = B["GabelAussen"]["bbox"], B["GabelInnen"]["bbox"]
    gap = ga["min"][1] - gi["max"][1]
    ck.eq("Gabelspalt = Knotenlasche + 2 mm", gap, pk["lug_t"] + p["lug_clear"], 0.01)
    ck.eq("Knotenlasche passt in die Gabel (Spalt > Lasche)", 1 if gap > pk["lug_t"] else 0, 1)
    ck.eq("Gabelhoehe ueber der Lochmitte (Gabel reicht ueber das Loch)", 1 if ga["max"][2] > p["lug_hole_z"] + 30 else 0, 1)
    ck.eq("Lochdurchmesser = Loch der Knotenlasche D14", p["bolt_hole"], pk["lug_hole"], 0.01)
    ck.eq("Gabelbreite >= Lasche + Spiel", 1 if ga["max"][0] - ga["min"][0] >= pk["lug_w"] else 0, 1)
    qb = [b for k, b in B.items() if k.startswith(("Body", "Querbolzen")) and abs((b["bbox"]["max"][1] - b["bbox"]["min"][1]) - 45) < 25 and (b["bbox"]["max"][2] - b["bbox"]["min"][2]) < 40]
    ck.eq("Querbolzen M12 vorhanden (durch beide Laschen)", 1 if any(b["bbox"]["min"][1] < gi["min"][1] and b["bbox"]["max"][1] > ga["max"][1] for b in B.values() if b["name"].startswith(("Body", "Querbolzen"))) else 0, 1)
    return ck.done()

def dk_ball_r(pk):
    return json.load(open(os.path.join(sc.ROOT, "data", "components", "knoten.json"), encoding="utf-8"))["parameter"]["ball_d"]["wert"] / 2

if __name__ == "__main__":
    sys.exit(main())
