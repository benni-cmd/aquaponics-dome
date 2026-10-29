"""Vorpruefung NFT-Rinne gegen die Scope-Card (docs/scope-cards.md): Lochreihen = 1, Loecher = floor(Laenge/pitch), Breite 130, Hoehe 100, Wand, Lochmitte = Pflanzenmitte, Zickzack-Phase A/B = pitch/2, Ports.
Aufruf: python scripts/workshop/check_nft_rinne.py   (exit 1 bei FAIL)"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

def holes(path):
    fs = sc.faces(path, "Rinnenprofil")
    cyl = [f["cylinder"] for f in fs if f.get("cylinder") and abs(abs(f["cylinder"]["axis"][2]) - 1) < 1e-6 and abs(f["cylinder"]["radius"] - 26) < 0.1]
    return sorted({(round(c["origin"][0], 2), round(c["origin"][1], 2)) for c in cyl}), fs   # jede Bohrung besteht aus zwei Halbzylinder-Flaechen

def main():
    p, d = sc.load_params("nft_rinne")
    ck = sc.Check("nft_rinne")
    pos = {}
    for row, L in (("l_a", 3232), ("l_b", 3232), ("m_a", 1983), ("m_b", 1983), ("k_a", 1304), ("k_b", 1304)):
        path = os.path.join(sc.ROOT, "designs", "components", f"nft_rinne_{row}.sc")
        ev = sc.evaluate(path)
        prof = [b for b in ev["bodies"] if b["name"] == "Rinnenprofil"][0]
        mn, mx = prof["bbox"]["min"], prof["bbox"]["max"]
        ck.eq(f"{row} Laenge", mx[0] - mn[0], L, 0.5)
        ck.eq(f"{row} Breite", mx[1] - mn[1], 130, 0.2)
        ck.eq(f"{row} Hoehe", mx[2] - mn[2], 100, 0.2)
        hs, fs = holes(path)
        ck.eq(f"{row} Loecher", len(hs), math.floor(L / p["pitch"]))
        ck.eq(f"{row} Lochreihen", len({y for _, y in hs}), 1)
        ck.eq(f"{row} Reihe in Mittellinie y", abs(hs[0][1]), 0, 0.01)
        gaps = [hs[i + 1][0] - hs[i][0] for i in range(len(hs) - 1)]
        ck.eq(f"{row} Lochabstand", min(gaps), p["pitch"], 0.01); ck.eq(f"{row} Lochabstand max", max(gaps), p["pitch"], 0.01)
        ck.eq(f"{row} Lochdurchmesser", 2 * 26, p["hole_d"], 0.01)
        mid = (hs[0][0] + hs[-1][0]) / 2
        ck.eq(f"{row} Phase (Mitte der Reihe)", mid, (-62.5 if row.endswith("a") else 62.5), 0.01)
        pos[row] = mid
        # Wand: innere Seitenflaeche bei y = +-(65 - wall)
        inner = max(abs(f["centroid"][1]) for f in fs if f.get("plane_normal") and abs(f["plane_normal"][1]) > 0.99 and abs(f["centroid"][1]) < 64)
        ck.eq(f"{row} Wandstaerke", 65 - inner, p["wall"], 0.01)
        # Ports an den Kappen
        z = {b["name"]: b for b in ev["bodies"]}
        for nm, od, zz in (("KappeZulauf", p["inlet_od"], p["inlet_z"]), ("KappeAblauf", p["drain_od"], p["drain_z"])):
            cf = [f["cylinder"] for f in sc.faces(path, nm) if f.get("cylinder") and abs(abs(f["cylinder"]["axis"][0]) - 1) < 1e-6]
            ck.eq(f"{row} {nm} Aussen-D", max(2 * c["radius"] for c in cf), od, 0.01)
            ck.eq(f"{row} {nm} Achse z", cf[0]["origin"][2], zz, 0.01)
    for l in "lmk":
        ck.eq(f"Zickzack {l}: Versatz A/B", pos[l + "_b"] - pos[l + "_a"], p["pitch"] / 2, 0.01)
    sys.exit(ck.done())

if __name__ == "__main__":
    main()
