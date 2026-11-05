"""Pruefung W71-Leitungsteile (Ruecklauf-Sammler d110): Masse, Ports (Stirnflaechen), Durchfluss-Bilanz je Linie, Schwerkraft-Kapazitaet,
Luft zwischen den Muffen, Volumen unabhaengig per Raster, Interferenz 0 mit eingesteckten Testrohren und Gegenprobe (zu dickes Rohr kollidiert).
Aufruf: python -X utf8 scripts/workshop/check_lt_w71.py [--sc <datei>]   (exit 1 bei FAIL)"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w71 as W
from check_lt_w36 import interference, raster_volume

def main():
    path = sys.argv[sys.argv.index("--sc") + 1] if "--sc" in sys.argv else os.path.join(sc.ROOT, "designs", "components", "lt_sammler_d110.sc")
    g = W.geom(); ck = sc.Check("lt_sammler_d110")
    ev = sc.evaluate(path)
    ck.eq("Koerperzahl (ein Koerper: Stutzen und Zapfen verschmolzen)", ev["body_count"], 1)
    b = ev["bodies"][0]; bb = b["bbox"]
    ck.eq("Koerper geschlossen (closed)", 1 if b["closed"] else 0, 1)
    ck.eq("Material LT pvc (Katalog pvc_u)", 1 if b["material"] == "LT pvc" else 0, 1)
    ck.eq("Laenge", bb["max"][0] - bb["min"][0], g["L"], 0.1)
    ck.eq("Aussen-D Koerper (Formstueck d110)", bb["max"][1] - bb["min"][1], g["of"], 0.1)
    ck.eq("Oberkante = hoechste Zulauf-Muffe (d63)", bb["max"][2], max(g["tops"].values()), 0.1)
    ck.eq("Unterkante = Zapfen Zweitbecken", bb["min"][2], g["bottom"], 0.1)
    fs = sc.faces(path, "Sammler")
    cyl = [f["cylinder"] for f in fs if f.get("cylinder")]
    planes = [(f["plane_normal"], f["centroid"]) for f in fs if f.get("plane_normal")]
    for k, ((fn, ds, kante, q1, q2, art, lage), x) in enumerate(zip(W.S_ANSCHL, g["xs"]), 1):
        vert = [c for c in cyl if abs(abs(c["axis"][2]) - 1) < 0.01 and abs(c["origin"][0] - x) < 0.1]
        if lage == "oben":
            ck.eq(f"Zulauf {k} {fn}: Muffe d{ds} (Radius {ds / 2})", 1 if any(abs(c["radius"] - ds / 2) < 0.05 for c in vert) else 0, 1)
            ck.eq(f"Zulauf {k} {fn}: Stutzen aussen od_f(d{ds}) = {L.od_f(ds):.2f}", 1 if any(abs(c["radius"] - L.od_f(ds) / 2) < 0.05 for c in vert) else 0, 1)
            sh = any(p[2] > 0.999 and abs(c[0] - x) < 0.6 and abs(c[2] - (g["tops"][ds] - L.DEPTH[ds])) < 0.05 for p, c in planes)
            ck.eq(f"Zulauf {k} {fn}: Anschlag {W.S_SHOULDER} mm unter der Muffe bei z = {g['tops'][ds] - L.DEPTH[ds]:.2f}", 1 if sh else 0, 1)
        else:
            ck.eq(f"Abgang {k} {fn}: Zapfen d{ds}", 1 if any(abs(c["radius"] - ds / 2) < 0.05 for c in vert) else 0, 1)
        di = ds - 2 * L.wall_p(ds)
        ck.eq(f"Anschluss {k} {fn}: Bohrung d{di:.1f} bis in den Sammler", 1 if any(abs(c["radius"] - di / 2) < 0.05 for c in vert) else 0, 1)
    for name, pos, dr, art, dn in W.ports("lt_sammler_d110"):
        hit = any(sum(n[i] * dr[i] for i in range(3)) > 0.999 and math.dist(c, pos) < 0.6 for n, c in planes)
        ck.eq(f"Port {name} ({art}, {dn}) Stirnflaeche an {tuple(round(v, 2) for v in pos)}", 1 if hit else 0, 1)
    # Durchfluss-Bilanz: Zulaeufe minus Abgang = Auslauf (data/leitungsnetz.json K13/K15/K58/K33/K16 bzw. K29/K31/K59/K32)
    net = json.load(open(os.path.join(sc.ROOT, "data", "leitungsnetz.json"), encoding="utf-8"))
    soll = {k["id"]: k["soll_l_min"] for k in net["kanten"]}
    for lin, zu, ab, aus in ((1, ("K15", "K13", "K58"), "K33", "K16"), (2, ("K31", "K29", "K59"), None, "K32")):
        q_zu = sum(soll[k] for k in zu); q_ab = soll[ab] if ab else 0.0
        ck.eq(f"Linie {lin}: Zulauf {q_zu:g} minus Zweitbecken {q_ab:g} = Auslauf {aus} {soll[aus]:g} l/min", q_zu - q_ab, soll[aus], 0.01)
        ist_l = [a[3] if lin == 1 else a[4] for a in W.S_ANSCHL]; soll_l = [soll[ab] if ab else 0.0] + [soll[k] for k in zu]
        ck.eq(f"Linie {lin}: Teil-Sollwerte im Bauteil ungleich Netz", sum(1 for i, s in zip(ist_l, soll_l) if abs(i - s) > 0.01), 0)
    # Schwerkraft: Vollfuell-Kapazitaet nach Manning (n = 0,009 PVC) bei 1 % Gefaelle, gefordert >= 2 x hoechster Auslauf (Teilfuellung, Luft)
    D = g["bore"] / 1000; A = math.pi / 4 * D * D; Rh = D / 4
    q_cap = A * Rh ** (2 / 3) * 0.01 ** 0.5 / 0.009 * 60000
    q_max = max(soll["K16"], soll["K32"])
    ck.eq(f"Schwerkraft-Kapazitaet d{g['bore']:.1f} bei 1 % ({q_cap:.0f} l/min) >= 2 x {q_max:g}", 1 if q_cap >= 2 * q_max else 0, 1)
    # Luft zwischen benachbarten Muffen-Stutzen (od_f) und zwischen Zapfen und Muffe A >= 10 mm
    for k in range(len(W.S_ANSCHL) - 1):
        a1, a2 = W.S_ANSCHL[k], W.S_ANSCHL[k + 1]
        r1 = (L.od_f(a1[1]) if a1[6] == "oben" else a1[1]) / 2; r2 = L.od_f(a2[1]) / 2
        luft = g["xs"][k + 1] - g["xs"][k] - r1 - r2
        ck.eq(f"Luft Anschluss {k + 1} -> {k + 2} >= 10 (Ist {luft:.1f})", 1 if luft >= 10 else 0, 1)
    ck.eq(f"Abgang 1 beginnt hinter Muffe A (x {g['xs'][0] - W.S_ANSCHL[0][1] / 2:g} > {g['t']})", 1 if g["xs"][0] - W.S_ANSCHL[0][1] / 2 > g["t"] else 0, 1)
    # Volumen unabhaengig: CSG-Raster 1 mm, Toleranz 1 %
    R, rb, t = g["of"] / 2, g["bore"] / 2, g["t"]
    an = [(x, ds, lage) for (fn, ds, kante, q1, q2, art, lage), x in zip(W.S_ANSCHL, g["xs"])]
    def inside(x, y, z):
        r2 = y * y + z * z
        solid = 0 <= x <= g["L"] and r2 <= R * R
        for ax, ds, lage in an:
            q = (x - ax) ** 2 + y * y
            if lage == "oben" and q <= (L.od_f(ds) / 2) ** 2 and 0 <= z <= g["tops"][ds]: solid = True
            if lage == "unten" and q <= (ds / 2) ** 2 and g["bottom"] <= z <= 0: solid = True
        if not solid: return False
        if x < t and r2 < (W.S_D / 2) ** 2: return False
        if t <= x <= g["L"] - W.S_END and r2 < rb * rb: return False
        for ax, ds, lage in an:
            q = (x - ax) ** 2 + y * y; di = ds - 2 * L.wall_p(ds)
            if lage == "oben":
                if q < (ds / 2) ** 2 and z >= g["tops"][ds] - L.DEPTH[ds]: return False
                if q < (di / 2) ** 2 and 0 <= z: return False
            elif q < (di / 2) ** 2 and z <= 0: return False
        return True
    v = raster_volume(inside, (0, -R - 1, g["bottom"] - 1), (g["L"] + 1, R + 1, max(g["tops"].values()) + 1))
    ck.eq(f"Volumen {b['volume_mm3']:.0f} = CSG-Raster 1 mm ({v:.0f})", b["volume_mm3"], v, v * 0.01)
    # Interferenz: Testrohre bis Anschlag in jede Muffe (A: d110 von -X, Zulaeufe von oben) und auf den Zapfen eine Kappe-Muffe d50; dann Gegenprobe d+2
    def extra(plus):
        cmds = [{"command": "solid.cylinder", "params": {"diameter": S + plus, "height": 300, "base": [g["t"] - 300, 0, 0], "axis": [1, 0, 0], "operation": "new", "name": "Testrohr_A", "body_name": "Testrohr_A"}} for S in (W.S_D,)]
        cmds.append({"command": "solid.cylinder", "params": {"diameter": W.S_D - 2 * L.wall_p(W.S_D), "height": 302, "base": [g["t"] - 301, 0, 0], "axis": [1, 0, 0], "operation": "cut", "targets": ["Testrohr_A"], "name": "Testrohr_A_i"}})
        for k, (ax, ds, lage) in enumerate(an, 1):
            if lage != "oben": continue
            z0 = g["tops"][ds] - L.DEPTH[ds]; n = f"Testrohr_{k}"
            cmds.append({"command": "solid.cylinder", "params": {"diameter": ds + plus, "height": 300, "base": [ax, 0, z0], "axis": [0, 0, 1], "operation": "new", "name": n, "body_name": n}})
            cmds.append({"command": "solid.cylinder", "params": {"diameter": ds - 2 * L.wall_p(ds), "height": 302, "base": [ax, 0, z0 - 1], "axis": [0, 0, 1], "operation": "cut", "targets": [n], "name": n + "_i"}})
        return cmds
    hits, res = interference(path, extra(0.0))
    ck.eq(f"Interferenz 0: Testrohre d110/d63/d50/d40 bis Anschlag in den Muffen (geprueft {res.get('pairs_intersected')} Paare)", len(hits), 0)
    hits2, _ = interference(path, extra(2.0))
    ck.eq("Gegenprobe: Testrohre 2 mm zu dick kollidieren mit dem Sammler (4 Muffen)", len([h for h in hits2 if "Sammler" in (h["a"], h["b"])]), 4)
    print(f"INFO lt_sammler_d110: Volumen {b['volume_mm3']:.0f} mm3, Masse {b['mass_g'] / 1000:.3f} kg, Wasser im Sammler {math.pi * rb * rb * (g['L'] - W.S_END - t) / 1e6:.2f} l, Kapazitaet {q_cap:.0f} l/min")
    return ck.done()

S = W.S_D
if __name__ == "__main__":
    sys.exit(main())
