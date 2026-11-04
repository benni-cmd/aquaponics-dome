"""Pruefung Aktivkohle-Station T83 (W37-2): Behaelter-Mass, Bett 21 l je Behaelter und Kontaktzeit 10,5 min, Kohlemasse, Ports (Stirnflaechen an den Blatt-Lagen), Reihenfolge der Bauteile im Strang, keine Vorratsflaeche, Interferenz 0.
Erwartungen aus R45 Abschnitt 5 und R53 (Handelsmasse, Rechnung scripts/r45_kohle.py), die Port-Lagen aus den Parametern und dem Netz (K39/K40/K41/K52), nicht aus dem Generator.
Aufruf: python -X utf8 scripts/workshop/check_aktivkohle_station.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
from check_lt_w39 import interference

NAME = "aktivkohle_station"

def main():
    p, d = sc.load_params(NAME)
    path = os.path.join(sc.ROOT, "designs", "components", NAME + ".sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check(NAME)
    bb = lambda n: B[n]["bbox"]
    n_b = int(p["behaelter"])
    zp = p["vessel_h"] - p["head_h"] / 2
    # --- Behaelter 10 x 35
    for k in range(1, n_b + 1):
        w = B[f"Behaelter_{k}"]
        ck.eq(f"Behaelter {k}: Aussen-Ø 254 (Handelsmass 10 Zoll)", bb(f"Behaelter_{k}")["max"][0] - bb(f"Behaelter_{k}")["min"][0], 254, 0.2)
        ck.eq(f"Behaelter {k}: Mantelhoehe 790 (889 - Kopf 99)", bb(f"Behaelter_{k}")["max"][2] - bb(f"Behaelter_{k}")["min"][2], 790, 0.2)
        ck.eq(f"Kopf {k}: Oberkante Z 889 (Handelsmass 35 Zoll)", bb(f"Kopf_{k}")["max"][2], 889, 0.2)
        inn = (math.pi * 127 ** 2 * 790 - w["volume_mm3"]) / 1e6
        ck.eq(f"Behaelter {k}: Innenvolumen {inn:.1f} l in 34..40 (Handel 10x35: 38 l, R53; keine Vorratsflaeche)", 1 if 34 <= inn <= 40 else 0, 1)
        bed = B[f"Kohlebett_{k}"]
        ck.eq(f"Kohlebett {k}: {bed['volume_mm3'] / 1e6:.1f} l = 21 l (R45)", bed["volume_mm3"] / 1e6, 21.0, 0.3)
        ck.eq(f"Kohlebett {k}: Masse {bed['mass_g'] / 1000:.2f} kg = 9,3 kg (0,441 kg/l, R53 Abschnitt 6)", bed["mass_g"] / 1000, 9.3, 0.3)
        ck.eq(f"Kohlebett {k} liegt im Innenraum (Ø 240 < 244, Boden > 5)", 1 if bb(f"Kohlebett_{k}")["max"][0] - bb(f"Kohlebett_{k}")["min"][0] < 244 and bb(f"Kohlebett_{k}")["min"][2] > p["vessel_wall"] else 0, 1)
    tot = sum(B[f"Kohlebett_{k}"]["volume_mm3"] for k in range(1, n_b + 1)) / 1e6
    tz = tot / 4.0
    ck.eq(f"Kontaktzeit {tz:.1f} min = Betten {tot:.1f} l / 4 l/min (scripts/r45_kohle.py: 42 l -> 10,5 min)", tz, 10.5, 0.2)
    # --- Vorfilter
    ck.eq("Sedimentgehaeuse: Ø 112 (10 Zoll Slim-Line, Handelsmass)", bb("Sedimentgehaeuse")["max"][0] - bb("Sedimentgehaeuse")["min"][0], 112, 0.2)
    ck.eq("Sedimentgehaeuse Oberkante = Behaelter-Mantelhoehe 790 (Koepfe auf gleicher Hoehe)", bb("Sedimentgehaeuse")["max"][2], 790, 0.2)
    ck.eq("Sedimentpatrone 20 um: 10 Zoll (250 mm) in der Hohlbohrung", bb("Sedimentpatrone")["max"][2] - bb("Sedimentpatrone")["min"][2], 250, 0.2)
    ck.eq("Kopf Sediment: Oberkante Z 889", bb("Kopf_Sediment")["max"][2], 889, 0.2)
    # --- Reihenfolge im Strang (Fluss +X): Hahn < Sediment < Behaelter 1 < Probehahn-T < Behaelter 2 < Begrenzer < K41 < K52 < Hahn K40
    cx = lambda n: (bb(n)["min"][0] + bb(n)["max"][0]) / 2
    seq = ["Hahn_Eingang", "Kopf_Sediment", "Kopf_1", "T_Probehahn"] + (["Kopf_2"] if n_b == 2 else []) + ["Begrenzer", "T_K41", "T_K52", "Hahn_K40"]
    xs = [cx(n) for n in seq]
    ck.eq("Reihenfolge Hahn, Vorfilter, Behaelter 1, Probehahn, [Behaelter 2], Begrenzer, K41, K52, Hahn K40 (x steigend)", 1 if xs == sorted(xs) else 0, 1)
    ck.eq("Probehahn-T liegt zwischen Behaelter 1 und 2 (R45: Probehahn zwischen den Behaeltern)", 1 if cx("Kopf_1") < cx("T_Probehahn") < (cx("Kopf_2") if n_b == 2 else 1e9) else 0, 1)
    ck.eq("Abzweige K41 und K52 hinter dem Begrenzer (R45 Zeile 307)", 1 if cx("T_K41") > bb("Begrenzer")["max"][0] and cx("T_K52") > cx("T_K41") else 0, 1)
    ck.eq("Begrenzer hinter Behaelter 2 (R45 Zeile 305)", 1 if bb("Begrenzer")["min"][0] > bb(f"Kopf_{n_b}")["max"][0] else 0, 1)
    # --- Ports: ebene Stirnflaeche mit Normale = Richtung, Mittelpunkt an der Lage
    ports = [("K39 Eingang d25", "Rohr_Eingang", (p["x_in"], 0, zp), (-1, 0, 0)),
             ("K40 Ausgang d25", "Rohr_Ausgang_K40", (p["x_out"], 0, zp), (1, 0, 0)),
             ("K41 Abzweig d20", "Rohr_K41", (p["t2_x"], p["abz_y"], zp), (0, 1, 0)),
             ("K52 Abzweig d25", "Rohr_K52", (p["t3_x"], -p["abz_y"], zp), (0, -1, 0)),
             ("Probehahn Tuelle d12", "Probehahn", (p["t1_x"], p["tap_y"], zp), (0, 1, 0))]
    fm = sc.faces_multi(path, sorted({b for _, b, _, _ in ports}))
    for label, body, pos, dr in ports:
        hit = any(f.get("plane_normal") and sum(f["plane_normal"][i] * dr[i] for i in range(3)) > 0.999 and math.dist(f["centroid"], pos) < 0.6 for f in fm[body])
        ck.eq(f"Port {label}: Stirnflaeche an {tuple(round(v, 1) for v in pos)}", 1 if hit else 0, 1)
    blatt = json.load(open(os.path.join(sc.ROOT, "data", "components", NAME + ".json"), encoding="utf-8"))["blatt"]["ports"]
    ck.eq("Blatt nennt 5 Ports", len(blatt), 5)
    for k in ("K39", "K40", "K41", "K52"):
        ck.eq(f"Blatt-Port {k} vorhanden", 1 if any(k in r[0] for r in blatt) else 0, 1)
    # --- Rohrmasse: Wand und Bohrung d25 und d20
    ck.eq("Rohr Eingang: Aussen-Ø 25", bb("Rohr_Eingang")["max"][1] - bb("Rohr_Eingang")["min"][1], 25, 0.1)
    ck.eq("Rohr K41: Aussen-Ø 20", bb("Rohr_K41")["max"][0] - bb("Rohr_K41")["min"][0], 20, 0.1)
    ck.eq("Leitungsachse Z 839,5 (Kopfmitte)", (bb("Rohr_Eingang")["min"][2] + bb("Rohr_Eingang")["max"][2]) / 2, zp, 0.1)
    # --- Koerper und Gesamtbox
    mn, mx = sc.bbox_all(ev)
    ck.eq(f"Gesamt-Box X {mn[0]:.0f} bis {mx[0]:.0f} (Eingang -800 bis Ausgang 900)", 1 if abs(mn[0] - p["x_in"]) < 0.2 and abs(mx[0] - p["x_out"]) < 0.2 else 0, 1)
    ck.eq(f"Gesamt-Box Y {mn[1]:.0f} bis {mx[1]:.0f} (K52 -250 bis K41 +250)", 1 if abs(mn[1] + p["abz_y"]) < 0.2 and abs(mx[1] - p["abz_y"]) < 0.2 else 0, 1)
    big = [n for n, v in B.items() if v["volume_mm3"] > 45e6 and not n.startswith("Konsole")]
    ck.eq("Keine Vorratsflaeche: kein Koerper ueber 45 l Volumen ausser Konsole", len(big), 0)
    bad, res = interference(path)
    ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(bad), 0)
    for i in bad[:5]:
        print("   ", i)
    print(f"INFO Koerper {len(B)}, Masse gesamt {ev['total']['mass_g'] / 1000:.1f} kg (davon Kohle {tot * 0.441:.1f} kg)")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
