"""Pruefung Lebendfutterbecken T14k (bisher Drittbecken klein; N-UNIFY-AUTOBAHN U3, D118/D120): Durchmesser, Ring, Hoehe, Wassertiefe, Nennvolumen, Rand ueber dem Wasserspiegel,
Wannenvolumen (Rechnung minus Wandloch), vier Stutzen K41/K42/K43/K49, Ueberlauf-Tuelle d63, Interferenz 0.
Erwartungen aus der Quelle `data/oasis-soll.json` (Bauteil feed: Ø 1000, Wasserspiegel 850, Rand 1000, steht auf dem Boden) und der Rechnung, nicht aus dem Generator.
Stand vor U3 (Drittbecken Ø 800, im Boden, Rand 135 ueber dem Wasser): Commit 044bdb0.
Aufruf: python scripts/workshop/check_becken_dritt_klein.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
from check_lt_w39 import interference
import becken_dritt_klein as gen
import becken_soll as BS
import leitung as L

def soll_feed():
    d = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    return next(b for b in d["bauteile"] if b["id"] == "feed")

def main():
    p, d = sc.load_params("becken_dritt_klein")
    S = soll_feed()
    D, WSP, RAND = S["masse_text_mm"]["durchmesser"], S["hoehen"]["wsp_ueber_fussboden_mm"], S["hoehen"]["rand_ueber_fussboden_mm"]   # 1000 / 850 / 1000
    RING, BODEN = 60, 120
    path = os.path.join(sc.ROOT, "designs", "components", "becken_dritt_klein.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check("becken_dritt_klein")
    ck.eq("Koerper (Wanne, Wasser, 4 Stutzen, Ueberlauf)", len(B), 7)
    w, wa = B["T14k_Wanne"], B["Wasser"]
    dia = lambda b: b["bbox"]["max"][0] - b["bbox"]["min"][0]
    ck.eq(f"Aussendurchmesser = {D} + 2 x {RING} = {D + 2 * RING}", dia(w), D + 2 * RING, 0.5)
    ck.eq(f"Gesamthoehe {RAND} (Quelle: Rand {RAND} ueber dem Fussboden, steht auf dem Boden)", w["bbox"]["max"][2] - w["bbox"]["min"][2], RAND, 0.2)
    ck.eq("Unterkante Z 0 (Standflaeche auf dem Fussboden)", w["bbox"]["min"][2], 0, 0.1)
    ck.eq(f"Wasserspiegel (Oberkante Wasserkoerper) Z {WSP} (Quelle: Wasserspiegel {WSP})", wa["bbox"]["max"][2], WSP, 0.2)
    ck.eq(f"Rand ueber dem Wasserspiegel {RAND - WSP} (Quelle: Rand {RAND} minus Wasserspiegel {WSP})", w["bbox"]["max"][2] - wa["bbox"]["max"][2], RAND - WSP, 0.2)
    ck.eq(f"Wassertiefe {WSP - BODEN} (Wasserspiegel {WSP} minus Boden {BODEN})", wa["bbox"]["max"][2] - wa["bbox"]["min"][2], WSP - BODEN, 0.2)
    ck.eq(f"Boden {BODEN} (Wasserunterkante)", wa["bbox"]["min"][2], BODEN, 0.2)
    r_o = dia(w) / 2
    loch = math.pi / 4 * L.od_f(63) ** 2 * RING / 1e6                                                       # Wandloch der Ueberlauf-Tuelle in l (60 mm Wand, Rechnung)
    ana = math.pi / 4 * ((D + 2 * RING) ** 2 * RAND - D ** 2 * (RAND - BODEN)) / 1e6                         # Wannenvolumen in l ohne Loch
    ck.eq(f"Wannenvolumen {w['volume_mm3'] / 1e6:.1f} l = Rechnung {ana:.1f} l minus Wandloch {loch:.2f} l", w["volume_mm3"] / 1e6, ana - loch, 0.1)
    nenn = math.pi / 4 * D ** 2 * (WSP - BODEN) / 1e6
    hohl = math.pi * r_o ** 2 * RAND / 1e6 - w["volume_mm3"] / 1e6 - loch                                   # gemessener Hohlraum (Wannenkoerper), ohne das Wandloch
    ck.eq(f"Nennvolumen bis Wasserspiegel {nenn:.0f} l (Ø {D} x {WSP - BODEN}), aus dem Wannenkoerper gemessen", hohl * (WSP - BODEN) / (RAND - BODEN), nenn, 1)
    ck.eq(f"Wasserkoerper {wa['volume_mm3'] / 1e6:.0f} l (Ø {D - 10} x {WSP - BODEN}, 5 mm Luft zur Wand)", wa["volume_mm3"] / 1e6, math.pi / 4 * (D - 10) ** 2 * (WSP - BODEN) / 1e6, 1)
    ck.eq(f"Grundflaeche mit Ring {math.pi * r_o ** 2 / 1e6:.3f} m2 = pi x 0,56^2", math.pi * r_o ** 2 / 1e6, math.pi * 0.56 ** 2, 0.005)
    ck.eq("Wasser-Luft 5 mm je Seite (Hohlraum gegen Wasserkoerper)", (D - dia(wa)) / 2, 5, 0.2)
    # Stutzen K41/K42/K43/K49 auf dem Rand (W37-2 Teil 3, unveraendert ausser der Hoehe)
    z0 = RAND + p["stutzen_h"] / 2
    for nm, port_pos, dr, art, dn in gen.stutzen_ports(p):
        sb = B["Stutzen_" + nm]
        ck.eq(f"Stutzen {nm}: Unterkante auf der Rand-Oberkante Z {RAND}", sb["bbox"]["min"][2], RAND, 0.1)
        ck.eq(f"Stutzen {nm}: Oberkante Z {RAND + 60} (Block 60 hoch)", sb["bbox"]["max"][2], RAND + 60, 0.1)
        ck.eq(f"Stutzen {nm}: Achse Z {z0:g}", port_pos[2], z0, 0.01)
        ck.eq(f"Stutzen {nm}: Aussenende {math.hypot(port_pos[0], port_pos[1]):.0f} = Ring-Aussenradius {r_o:.0f} + 70", math.hypot(port_pos[0], port_pos[1]), r_o + 70, 0.01)
        fs = sc.faces(path, "Stutzen_" + nm)
        hit = any(f.get("plane_normal") and sum(f["plane_normal"][i] * dr[i] for i in range(3)) > 0.999 and math.dist(f["centroid"], port_pos) < 0.6 for f in fs)
        ck.eq(f"Port {nm} ({art}, {dn}) Stirnflaeche an {tuple(round(v, 1) for v in port_pos)}", 1 if hit else 0, 1)
        dd = int(dn[1:]) if art == "Muffe" else 16
        ck.eq(f"Stutzen {nm}: Bohrung Ø {dd} (Zylinderflaeche r {dd / 2:g})", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - dd / 2) < 0.01 for f in fs) else 0, 1)
    nm_d = {nm: dn for nm, _, _, _, dn in gen.stutzen_ports(p)}
    ck.eq("Ports: K41 d20, K42 d25, K43 d25, K49 ID16", 1 if nm_d == {"K41": "d20", "K42": "d25", "K43": "d25", "K49": "ID16"} else 0, 1)
    # Ueberlauf-Tuelle d63 (D120): Rohr-Innenunterkante = Wasserspiegel, Achse WSP + 28,5, Richtung Anzuchtbecken
    ub = B["T14k_Ueberlauf"]
    ID = 57
    zc = (ub["bbox"]["min"][2] + ub["bbox"]["max"][2]) / 2
    ck.eq(f"Ueberlauf: Rohr-Innenunterkante = Wasserspiegel {WSP} (Achse {zc:.1f} minus ID/2)", zc - ID / 2, WSP, 0.2)
    ck.eq("Ueberlauf: Aussendurchmesser = Muffe d63 (od_f 72,15)", ub["bbox"]["max"][2] - ub["bbox"]["min"][2], L.od_f(63), 0.3)
    az = BS.ue_azimut("feed", "nursery")
    r_end = r_o + p["stutzen_len"]
    cx = (ub["bbox"]["min"][0] + ub["bbox"]["max"][0]) / 2; cy = (ub["bbox"]["min"][1] + ub["bbox"]["max"][1]) / 2
    ck.eq(f"Ueberlauf: Richtung Anzuchtbecken Azimut {az:.1f} Grad (Bauplaetze data/oasis-lage.json), Mitte der Box liegt auf diesem Strahl", 1 if abs(math.cos(math.radians(az)) * cy - math.sin(math.radians(az)) * cx) < 3 else 0, 1)
    ck.eq(f"Ueberlauf: Aussenende am Radius {r_end:.0f}", max(math.hypot(x, y) for x in (ub["bbox"]["min"][0], ub["bbox"]["max"][0]) for y in (ub["bbox"]["min"][1], ub["bbox"]["max"][1])), r_end, 40)
    fs = sc.faces(path, "T14k_Ueberlauf")
    ck.eq("Ueberlauf: Bohrung Ø 57 (Zylinderflaeche r 28,5)", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - ID / 2) < 0.01 for f in fs) else 0, 1)
    ck.eq("Ueberlauf: Muffe d63 (Zylinderflaeche r 31,5)", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - 31.5) < 0.01 for f in fs) else 0, 1)
    ck.eq("Ueberlauf: Tuelle liegt unter dem Rand (Oberkante unter Z %d)" % RAND, 1 if ub["bbox"]["max"][2] < RAND else 0, 1)
    mn_all = min(b["bbox"]["min"][2] for b in ev["bodies"]); mx_all = max(b["bbox"]["max"][2] for b in ev["bodies"])
    ck.eq(f"Gesamtbox Z 0 bis {RAND + 60} (Wanne {RAND} plus Stutzenbloecke)", 1 if abs(mn_all) < 0.1 and abs(mx_all - (RAND + 60)) < 0.1 else 0, 1)
    inter, _ = interference(path)
    ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(inter), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
