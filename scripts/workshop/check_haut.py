"""Vorpruefung Haut (W19 Schritt 4): haut_paneel_<typ>.sc (Dicke, Flaeche, Kantenlaengen, Randabstand 15 mm zur Strebenachse, Felderzahl und Typen aus layout.json) und haut_profil.sc (Laenge A/B, Querschnitt 30 x 8, Wand 2, Masse).
Erwartung unabhaengig vom Bauskript: Heron-Formel und Inkreisradius aus den Strebenlaengen (3279 / 3708 aus layout.json dome.strut_len_mm). Aufruf: python scripts/workshop/check_haut.py   (exit 1 bei FAIL)"""
import json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def heron(a, b, c):
    s = (a + b + c) / 2
    A = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return A, A / s

def main():
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    pp, dp = sc.load_params("haut_paneel")
    ck = sc.Check("haut")
    A, B = sorted(set(lay["strut_len_mm"]))
    n_a, n_b = lay["strut_len_mm"].count(A), lay["strut_len_mm"].count(B)
    felder = dp["felder"]
    # --- Felder und Typen
    ck.eq("Felder (Euler V - E + F = 1: 65 - 26 + 1)", len(felder), lay["struts"] - lay["nodes"] + 1)
    ck.eq("Felder je Typ summieren auf alle Felder", sum(t["anzahl_felder"] for t in dp["typen"].values()), len(felder))
    nbase = sum(1 for n in lay["nodes_list"] if abs(n["z"] - lay["base_z"]) < 5)
    ck.eq("Kanteninzidenz: 3 x Felder = 2 x Streben - Randkanten (Basisring: Randkanten = Basisknoten)", 3 * len(felder), 2 * lay["struts"] - nbase)
    ck.eq("Basisfelder je Typ summieren auf die Randkanten (ein Basisfeld je Randkante)", sum(t["basisfelder"] for t in dp["typen"].values()), nbase)
    ck.eq("Tuerfeld (D36: nur das Basisfeld BBB 149,2)", sum(1 for f in felder if f["door"]), 1)
    ck.eq("Strebenzahl A + B = layout.json dome.struts", n_a + n_b, lay["struts"])
    # --- Paneele
    for typ, T in dp["typen"].items():
        path = os.path.join(sc.ROOT, "designs", "components", f"haut_paneel_{typ}.sc")
        ev = sc.evaluate(path)
        b = ev["bodies"][0]
        c, a, bb = T["kanten_nominal"]
        A_s, r = heron(a, bb, c)
        k = (r - pp["edge_inset"]) / r
        ck.eq(f"{typ} Dicke", b["bbox"]["max"][2] - b["bbox"]["min"][2], pp["panel_t"], 0.01)
        ck.eq(f"{typ} Flaeche (Heron des Strebendreiecks x ((r - 15)/r)^2)", b["volume_mm3"] / pp["panel_t"] / 1e6, A_s * k * k / 1e6, 0.001)
        fs = sc.faces(path, "Paneel")
        sides = sorted(f["area"] / pp["panel_t"] for f in fs if ":side:" in f["name"])
        exp = sorted(x * k for x in (a, bb, c))
        ck.eq(f"{typ} Randkanten gleich Strebenlaenge x k (max. Abweichung mm)", max(abs(x - y) for x, y in zip(sides, exp)), 0, 0.5)
        per = sum(sides)
        r_pan = 2 * (b["volume_mm3"] / pp["panel_t"]) / per
        ck.eq(f"{typ} Randabstand zur Strebenachse = Inkreisradius Strebe - Inkreisradius Paneel (mm)", r - r_pan, pp["edge_inset"], 0.05)
        ck.eq(f"{typ} Koerper", len(ev["bodies"]), 1)
        ck.eq(f"{typ} Material Polycarbonat", 1 if b["material"] == "Polycarbonat" else 0, 1)
        ck.eq(f"{typ} Masse bei Dichte 0,19 (kg)", b["mass_g"] / 1000, b["volume_mm3"] / 1e6 * 0.19, 0.01)
    # --- Randprofil
    path = os.path.join(sc.ROOT, "designs", "components", "haut_profil.sc")
    pr, dr = sc.load_params("haut_profil")
    ev = sc.evaluate(path)
    b = ev["bodies"][0]
    area = pr["cap_w"] * pr["cap_h"] - (pr["cap_w"] - 2 * pr["cap_wall"]) * (pr["cap_h"] - pr["cap_wall"])
    L = b["bbox"]["max"][0] - b["bbox"]["min"][0]
    ck.eq("Profil A Laenge", L, A, 0.01)
    ck.eq("Profil Breite", b["bbox"]["max"][1] - b["bbox"]["min"][1], pr["cap_w"], 0.01)
    ck.eq("Profil Hoehe", b["bbox"]["max"][2] - b["bbox"]["min"][2], pr["cap_h"], 0.01)
    ck.eq("Profil Querschnitt mm2 (30 x 8 - 26 x 6)", b["volume_mm3"] / L, area, 0.05)
    ck.eq("Profil Masse A (kg, Dichte 2,7)", b["mass_g"] / 1000, area * A * 2.7e-6, 0.005)
    s = os.path.join(sc.TMP, "hp-chk-b.json"); o = os.path.join(sc.TMP, "hp-chk-b.sc")
    json.dump({"commands": [{"command": "config.activate", "params": {"row": "B"}}]}, open(s, "w"))
    r_ = subprocess.run([sc.CLI, "run", s, "--in", path, "--save", o, "--quiet"], capture_output=True, text=True)
    bB = sc.evaluate(o)["bodies"][0] if r_.returncode == 0 else None
    ck.eq("Profil B Laenge (Konfiguration B)", (bB["bbox"]["max"][0] - bB["bbox"]["min"][0]) if bB else 0, B, 0.01)
    ck.eq("Kappen gesamt 30 x A + 35 x B", n_a + n_b, 65)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
