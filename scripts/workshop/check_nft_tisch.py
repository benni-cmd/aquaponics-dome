"""Vorpruefung NFT-Tisch gegen die Scope-Card (docs/scope-cards.md): Rinnenzahl, Rinnenabstand, Zickzack-Versatz pitch/2, Gefaelle, Hoehe Z, Boecke/Beine/Diagonalen, Verteiler- und Sammelrohr-Anschluesse.
Aufruf: python scripts/workshop/check_nft_tisch.py [typ ...]   (exit 1 bei FAIL)"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

def mean_hole_x(fs):
    xs = sorted({round(f["cylinder"]["origin"][0], 1) for f in fs if f.get("cylinder") and abs(f["cylinder"]["radius"] - 26) < 0.1 and abs(abs(f["cylinder"]["axis"][2]) - 1) < 0.02})
    return xs

def main(typs):
    p, d = sc.load_params("nft_tisch")
    rp_pitch = sc.load_params("nft_rinne")[0]["pitch"]
    ck = sc.Check("nft_tisch")
    for typ in typs:
        T = d["typen"][typ]
        n, rp, L, zc = T["n"], T["rinnen_abstand"], T["laenge"], T["z_rinne_mitte"]
        path = os.path.join(sc.ROOT, "designs", "components", f"nft_tisch_{typ}.sc")
        ev = sc.evaluate(path)
        B = {b["name"]: b for b in ev["bodies"]}
        rin = sorted([b for k, b in B.items() if k.startswith("Rinnenprofil")], key=lambda b: (b["bbox"]["min"][1] + b["bbox"]["max"][1]) / 2)
        ck.eq(f"{typ} Rinnenzahl", len(rin), n)
        ys = [(b["bbox"]["min"][1] + b["bbox"]["max"][1]) / 2 for b in rin]
        for i in range(len(ys) - 1):
            ck.eq(f"{typ} Rinnenabstand {i+1}", ys[i + 1] - ys[i], rp, 0.5)
        th = math.atan(p["slope_pct"] / 100)
        for i, b in enumerate(rin):
            mn, mx = b["bbox"]["min"], b["bbox"]["max"]
            rise = (mx[2] - mn[2]) - 100 * math.cos(th)
            ck.eq(f"{typ} Rinne {i+1} Gefaelle in %", 100 * rise / (mx[0] - mn[0]) if False else 100 * rise / L, p["slope_pct"], 0.03)
            z_mid = mn[2] + (L / 2) * math.sin(th)
            ck.eq(f"{typ} Rinne {i+1} Hoehe Boden bei x=0", z_mid, zc, 1.5)
        # Zickzack: Lochphase benachbarter Rinnen unterscheidet sich um pitch/2
        names = sorted([k for k in B if k.startswith("Rinnenprofil")], key=lambda k: (B[k]["bbox"]["min"][1] + B[k]["bbox"]["max"][1]) / 2)
        FM = sc.faces_multi(path, names + ["Verteiler", "Sammelrohr"])
        xs = [mean_hole_x(FM[k]) for k in names]
        ck.eq(f"{typ} Loecher je Rinne (erste)", len(xs[0]), math.floor(L / rp_pitch))
        for i in range(len(xs) - 1):
            off = (xs[i + 1][0] - xs[i][0])
            ck.eq(f"{typ} Zickzack-Versatz {i+1}/{i+2}", abs(off), rp_pitch / 2, 1.0)
        # Boecke
        xb = 3 if L > 2500 else 2
        ck.eq(f"{typ} Beine", len([k for k in B if k.startswith("Bein_")]), 2 * xb)
        ck.eq(f"{typ} Querholme", len([k for k in B if k.startswith("Holm_")]), xb)
        ck.eq(f"{typ} Querstreben", len([k for k in B if k.startswith("Querstrebe_")]), xb)
        ck.eq(f"{typ} Laengsstreben", len([k for k in B if k.startswith("Laengs_")]), 2 * (xb - 1))
        ck.eq(f"{typ} Diagonalen", len([k for k in B if k.startswith("Diagonale_")]), 2 * xb)
        ck.eq(f"{typ} Fussplatten", len([k for k in B if k.startswith("Fussplatte_")]), 2 * xb)
        ck.eq(f"{typ} Rinnenhalter", len([k for k in B if k.startswith("Halter_")]), n * 2 * xb)
        ck.eq(f"{typ} Schlaeuche", len([k for k in B if k.startswith("Schlauch_")]), n)
        # Holmoberkante trifft Rinnenunterkante an jedem Bock (Auflage ohne Spalt, +-1 mm)
        holm = sorted([b for k, b in B.items() if k.startswith("Holm_")], key=lambda b: b["bbox"]["min"][0])
        for h in holm:
            xh = (h["bbox"]["min"][0] + h["bbox"]["max"][0]) / 2
            z_rinne_boden = zc - xh * p["slope_pct"] / 100
            ck.eq(f"{typ} Auflage Holm bei x={xh:.0f}", h["bbox"]["max"][2], z_rinne_boden, 1.0)
        # Verteiler: Stutzen D16 je Rinne
        vf = FM["Verteiler"]
        stutz = {round(f["cylinder"]["origin"][1], 1) for f in vf if f.get("cylinder") and abs(f["cylinder"]["radius"] - 8) < 0.1 and abs(abs(f["cylinder"]["axis"][0]) - 1) < 0.02}
        ck.eq(f"{typ} Verteiler-Stutzen", len(stutz), n)
        sf = FM["Sammelrohr"]
        muff = {round(f["cylinder"]["origin"][1], 1) for f in sf if f.get("cylinder") and abs(f["cylinder"]["radius"] - 16) < 0.1 and abs(abs(f["cylinder"]["axis"][0]) - 1) < 0.02}
        ck.eq(f"{typ} Sammelrohr-Muffen", len(muff), n)
        # Muffenachse = Ablaufachse der Rinne (tiefes Ende, z = zc - L/2*slope + 20)
        zm = sorted({round(f["cylinder"]["origin"][2], 1) for f in sf if f.get("cylinder") and abs(f["cylinder"]["radius"] - 16) < 0.1})
        ck.eq(f"{typ} Muffenachse z", zm[0], zc - L / 2 * p["slope_pct"] / 100 + 20, 1.0)
        zv = sorted({round(f["cylinder"]["origin"][2], 1) for f in vf if f.get("cylinder") and abs(f["cylinder"]["radius"] - 8) < 0.1})
        ck.eq(f"{typ} Verteiler-Stutzenachse z", zv[0], zc + L / 2 * p["slope_pct"] / 100 + 70, 1.0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main([a for a in sys.argv[1:]] or ["innen", "mitte", "aussen"]))
