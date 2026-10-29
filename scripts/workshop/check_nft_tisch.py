"""Vorpruefung NFT-Tisch (Rev. B, W16/D18) gegen Scope-Card und tisch_geom.py: Rinnenzahl, Abstand, Rinnenlaenge je Reihe, Lochraster mit Zickzack-Phase pitch/2, Gefaelle, Hoehe Z,
Boecke (Portal bzw. Ausleger), Beinlage ausserhalb der Beete/des Pools, Auflagehoehe, Verteiler-/Sammelrohr-Anschluesse und Lage an der Sektorgrenze.
Aufruf: python scripts/workshop/check_nft_tisch.py [typ ...]   (exit 1 bei FAIL)"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

def hole_xs(fs):
    return sorted({round(f["cylinder"]["origin"][0], 1) for f in fs if f.get("cylinder") and abs(f["cylinder"]["radius"] - 26) < 0.1 and abs(abs(f["cylinder"]["axis"][2]) - 1) < 0.02})

def main(typs):
    p, d = sc.load_params("nft_tisch")
    pitch = sc.load_params("nft_rinne")[0]["pitch"]
    ck = sc.Check("nft_tisch")
    for typ in typs:
        T = d["typen"][typ]
        G = TG.geometry(typ, p, T)
        rows, n, zc, slope, xc = G["rows"], G["n"], G["zc"], G["slope"], G["rows"][0]["xc"]
        path = os.path.join(sc.ROOT, "designs", "components", f"nft_tisch_{typ}.sc")
        ev = sc.evaluate(path)
        B = {b["name"]: b for b in ev["bodies"]}
        names = sorted([k for k in B if k.startswith("Rinnenprofil")], key=lambda k: (B[k]["bbox"]["min"][1] + B[k]["bbox"]["max"][1]) / 2)
        ck.eq(f"{typ} Rinnenzahl", len(names), n)
        th = math.atan(slope)
        FM = sc.faces_multi(path, names + ["Verteiler", "Sammelrohr"])
        phases = []
        for r, nm in zip(rows, names):
            b = B[nm]
            mn, mx = b["bbox"]["min"], b["bbox"]["max"]
            yc = (mn[1] + mx[1]) / 2
            ck.eq(f"{typ} Rinne {r['k'] + 1} Querlage y", yc, r["y"], 0.5)
            ck.eq(f"{typ} Rinne {r['k'] + 1} Laenge (Zehneck-Seite {r['side']:.0f} - 2 x {G['gap']:.0f} - Ueberstaende)", ((mx[0] - mn[0]) - 100 * math.sin(th)) / math.cos(th), r["L"], 1.0)      # Bounding-Box einer um th geneigten Rinne: L cos + 100 sin
            rise = (mx[2] - mn[2]) - 100 * math.cos(th)
            ck.eq(f"{typ} Rinne {r['k'] + 1} Gefaelle in %", 100 * rise / r["L"], p["slope_pct"], 0.05)
            ck.eq(f"{typ} Rinne {r['k'] + 1} Hoehe Boden an der Rinnenmitte", mn[2] + (r["L"] / 2) * math.sin(th), zc, 1.5)
            hx = hole_xs(FM[nm])
            ck.eq(f"{typ} Rinne {r['k'] + 1} Loecher", len(hx), r["n_holes"])
            exp = [r["xc"] + r["shift"] + (i - (r["n_holes"] - 1) / 2.0) * pitch for i in range(r["n_holes"])]
            if hx and len(hx) == len(exp):
                ck.eq(f"{typ} Rinne {r['k'] + 1} Lochlage (max. Abweichung zur Rechnung, mm)", max(abs(a - b_) for a, b_ in zip(sorted(hx), exp)), 0, 1.5)
            phases.append((hx[0] % pitch) if hx else 0)
        for i in range(len(phases) - 1):
            dphi = abs(phases[i + 1] - phases[i])
            dphi = min(dphi, pitch - dphi)
            ck.eq(f"{typ} Zickzack-Versatz {i + 1}/{i + 2} = pitch/2", dphi, pitch / 2.0, 1.5)
        for i in range(n - 1):
            ys = [(B[nm]["bbox"]["min"][1] + B[nm]["bbox"]["max"][1]) / 2 for nm in names]
            ck.eq(f"{typ} Rinnenabstand {i + 1}", ys[i + 1] - ys[i], G["rp"], 0.5)
        # Boecke
        nb = len(G["xb"])
        beine = sorted([b for k, b in B.items() if k.startswith("Bein_")], key=lambda b: (b["bbox"]["min"][0], b["bbox"]["min"][1]))
        ck.eq(f"{typ} Beine ({G['art']})", len(beine), len(G["legs"]))
        ck.eq(f"{typ} Fussplatten", len([k for k in B if k.startswith("Fussplatte_")]), len(G["legs"]))
        ck.eq(f"{typ} Laengsstreben", len([k for k in B if k.startswith("Laengs_")]), 2 if G["art"] == "portal" else 1)
        ck.eq(f"{typ} Laengsdiagonalen (Laengsaussteifung)", len([k for k in B if k.startswith("LDiag_")]), 2 if G["art"] == "portal" else 1)
        ck.eq(f"{typ} Rinnenhalter", len([k for k in B if k.startswith("Halter_")]), n * 2 * nb)
        ck.eq(f"{typ} Schlaeuche", len([k for k in B if k.startswith("Schlauch_")]), n)
        for (lx, ly), b in zip(sorted(G["legs"]), beine):
            ck.eq(f"{typ} Bein bei x={lx:.0f} Lage y (ausserhalb Beet/Pool)", (b["bbox"]["min"][1] + b["bbox"]["max"][1]) / 2, ly, 0.6)
        if G["art"] == "portal":
            ck.eq(f"{typ} Querholme", len([k for k in B if k.startswith("Holm_")]), nb)
            ck.eq(f"{typ} Querstreben", len([k for k in B if k.startswith("Querstrebe_")]), nb)
            ck.eq(f"{typ} Diagonalen", len([k for k in B if k.startswith("Diagonale_")]), 2 * nb)
            ck.eq(f"{typ} Querholm lang genug (Beine ausserhalb Beetbreite {G['bed_w']})", min((b["bbox"]["max"][1] - b["bbox"]["min"][1]) for k, b in B.items() if k.startswith("Holm_")) - 2 * 0, 2 * G["yl"] + p["leg_w"], 1.0)
            tops = [(k, b) for k, b in B.items() if k.startswith("Holm_")]
        else:
            ck.eq(f"{typ} Kragarme", len([k for k in B if k.startswith("Kragarm_")]), nb)
            tops = [(k, b) for k, b in B.items() if k.startswith("Kragarm_")]
        for k, b in sorted(tops, key=lambda t: t[1]["bbox"]["min"][0]):
            xh = (b["bbox"]["min"][0] + b["bbox"]["max"][0]) / 2
            ck.eq(f"{typ} Auflage {k} bei x={xh:.0f} = Rinnenunterkante", b["bbox"]["max"][2], zc - (xh - xc) * slope, 1.0)
        # Verteiler: Stutzen D16 je Rinne, schraege Lage an der Sektorgrenze
        vf, sf = FM["Verteiler"], FM["Sammelrohr"]
        stutz = {round(f["cylinder"]["origin"][1], 1) for f in vf if f.get("cylinder") and abs(f["cylinder"]["radius"] - 8) < 0.1 and abs(abs(f["cylinder"]["axis"][0]) - 1) < 0.02}
        ck.eq(f"{typ} Verteiler-Stutzen", len(stutz), n)
        muff = {round(f["cylinder"]["origin"][1], 1) for f in sf if f.get("cylinder") and abs(f["cylinder"]["radius"] - 16) < 0.1 and abs(abs(f["cylinder"]["axis"][0]) - 1) < 0.02}
        ck.eq(f"{typ} Sammelrohr-Muffen", len(muff), n)
        y1 = G["Wt"] / 2 + 60
        ck.eq(f"{typ} Verteiler endet an der Sektorgrenze (x_min, aussen)", B["Verteiler"]["bbox"]["min"][0], -((G["apc"] + y1) * TG.T18 - G["gap"]), 8.0)
        ck.eq(f"{typ} Sammelrohr endet an der Sektorgrenze (x_max, aussen)", B["Sammelrohr"]["bbox"]["max"][0], (G["apc"] + y1) * TG.T18 - G["gap"], 8.0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main([a for a in sys.argv[1:]] or ["innen", "mitte", "aussen"]))
