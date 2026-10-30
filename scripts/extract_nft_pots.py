"""Topfpositionen in den NFT-Rinnen je Tischtyp -> data/nft_pots.json (D33/D43: 674 Topfloecher in 24 Tischen, aussen 4 Rinnen).
Lochraster aus scripts/workshop/tisch_geom.py (Zahl und Versatz je Reihe), Reihenlage und Hoehe aus den Rinnenprofil-Koerpern der Tischdatei (Rinne liegt mit 1,5 % Gefaelle: Oberkante Rippen linear von -X nach +X fallend).
Topfboden = Oberkante Rippen - 64,5 (Netztopf 63 hoch, Kragen 1,5 mm unter Rippenoberkante, wie nft_rinne.py render()). Koordinaten im Tischrahmen (X tangential, Y radial innen, Z ueber Boden).
Aufruf: python scripts/extract_nft_pots.py"""
import json, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop"))
import sc, tisch_geom as TG

p, d = sc.load_params("nft_tisch")
out = {"unit": "mm", "frame": "Tisch: X tangential, Y radial innen, Z ueber Boden; Topfboden-Z", "typen": {}}
for typ in ("innen", "mitte", "aussen"):
    G = TG.geometry(typ, p, d["typen"][typ]); ev = sc.evaluate(os.path.join(ROOT, "designs", "components", f"nft_tisch_{typ}.sc"))
    prof = sorted((b for b in ev["bodies"] if b["name"].startswith("Rinnenprofil")), key=lambda b: (b["bbox"]["min"][1] + b["bbox"]["max"][1]))
    assert len(prof) == G["n"], (typ, len(prof), G["n"])
    rows = sorted(G["rows"], key=lambda r: r["y"])
    pots = []
    for r, b in zip(rows, prof):
        mn, mx = b["bbox"]["min"], b["bbox"]["max"]; xc = (mn[0] + mx[0]) / 2; yc = (mn[1] + mx[1]) / 2
        slope = p["slope_pct"] / 100.0
        assert abs(yc - r["y"]) < 30, (typ, yc, r["y"])
        for i in range(r["n_holes"]):
            x = xc + r["shift"] + (i - (r["n_holes"] - 1) / 2) * TG.rinne_pitch()
            ztop = mx[2] - slope * (x - mn[0])   # Zulauf hoch bei -X
            pots.append([round(x, 1), round(yc, 1), round(ztop - 64.5, 1)])
    out["typen"][typ] = {"n_tisch_pots": len(pots), "pots": pots}
    print(typ, len(pots), "Reihen", [(r["n_holes"], round(r["shift"])) for r in rows])
json.dump(out, open(os.path.join(ROOT, "data", "nft_pots.json"), "w"), separators=(",", ":"))
tot = 10 * out["typen"]["innen"]["n_tisch_pots"] + 6 * out["typen"]["mitte"]["n_tisch_pots"] + 8 * out["typen"]["aussen"]["n_tisch_pots"]
print("gesamt (10 innen + 6 mitte + 8 aussen):", tot, "Soll 674 (D43)")
