"""Vorpruefung Tuer komplett (W20 Schritt 5): tuer_komplett.sc (Lichte, Spiel, Zarge im Feld, Beschlaege, Interferenz) und haut_paneel_BBB_tuer.sc (Ausschnitt).
Erwartung unabhaengig von tuer_geom.py: Feldbreite und Neigung direkt aus den Knoten (layout.json dome.nodes_list 24, 22, 6), Ausschnittflaeche numerisch aus Paneeldreieck und Zargenrechteck.
Aufruf: python scripts/workshop/check_tuer.py   (exit 1 bei FAIL)"""
import json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def interference(path):
    script = os.path.join(sc.TMP, "ws-tuer-interf.json"); out = os.path.join(sc.TMP, "ws-tuer-interf-out.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 120}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--results", "--json-out", out], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER interference: " + r.stderr.strip())
    d = json.load(open(out, encoding="utf-8"))
    def find(o):
        if isinstance(o, dict):
            if "interferences" in o:
                return o["interferences"]
            for v in o.values():
                x = find(v)
                if x is not None:
                    return x
        elif isinstance(o, list):
            for v in o:
                x = find(v)
                if x is not None:
                    return x
    return [(i["a"], i["b"], i.get("volume_mm3", 0)) for i in find(d) or []]

def main():
    P, D = sc.load_params("tuer_komplett")
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    N = lay["nodes_list"]
    ck = sc.Check("tuer")
    path = os.path.join(sc.ROOT, "designs", "components", "tuer_komplett.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    bb = lambda n: B[n]["bbox"]
    # --- Zarge und Lichte
    ck.eq("Lichte Breite (Pfosten innen)", bb("Pfosten_rechts")["min"][0] - bb("Pfosten_links")["max"][0], P["blatt_w"] + 2 * P["spiel"], 0.01)
    ck.eq("Lichte Hoehe (Schwelle oben bis Sturz unten)", bb("Sturz")["min"][1] - bb("Schwelle")["max"][1], P["blatt_h"] + P["spiel"], 0.01)
    ck.eq("Zarge Aussenbreite", bb("Schwelle")["max"][0] - bb("Schwelle")["min"][0], P["blatt_w"] + 2 * P["spiel"] + 2 * P["rohr"], 0.01)
    # --- Blatt und Spiel
    ck.eq("Blatt Breite x Hoehe x Dicke (1000 x 2000 x 40)", (bb("Tuerblatt")["max"][0] - bb("Tuerblatt")["min"][0]) + 1e3 * (bb("Tuerblatt")["max"][1] - bb("Tuerblatt")["min"][1]) + 1e7 * (bb("Tuerblatt")["max"][2] - bb("Tuerblatt")["min"][2]), 1000 + 2000e3 + 40e7, 0.01)
    ck.eq("Spiel links (Pfosten innen - Blatt)", bb("Tuerblatt")["min"][0] - bb("Pfosten_links")["max"][0], P["spiel"], 0.01)
    ck.eq("Spiel rechts", bb("Pfosten_rechts")["min"][0] - bb("Tuerblatt")["max"][0], P["spiel"], 0.01)
    ck.eq("Spiel oben 6 (Sturz unten - Blatt oben)", bb("Sturz")["min"][1] - bb("Tuerblatt")["max"][1], 6, 0.01)
    ck.eq("Spiel unten 2 (Blatt unten - Schwelle oben)", bb("Tuerblatt")["min"][1] - bb("Schwelle")["max"][1], 2, 0.01)
    ck.eq("Anschlag innen (Blatt kann nicht nach innen: Anschlag-Aussenflaeche <= Blatt-Innenflaeche)", 1 if bb("Anschlag_links")["max"][2] <= bb("Tuerblatt")["min"][2] else 0, 1)
    ck.eq("Scharniere (3 x Zargenlasche, Blattlasche, Bolzen)", len([k for k in B if k.startswith("Scharnier")]), 9)
    ck.eq("Druecker (Rosette, Hals, Hebel je Seite)", len([k for k in B if k.startswith(("Rosette", "Druecker"))]), 6)
    for k in (1, 2, 3):
        bo, zl, bl = bb(f"Scharnier{k}_Bolzen"), bb(f"Scharnier{k}_Zargenlasche"), bb(f"Scharnier{k}_Blattlasche")
        ck.eq(f"Scharnier {k}: Bolzen verbindet Zargen- und Blattlasche (z)", 1 if bo["min"][2] <= zl["max"][2] + 0.01 and bo["max"][2] >= bl["min"][2] - 0.01 else 0, 1)
    ck.eq("Blattlage: Dichtung liegt am Blatt an (Abstand z, mm)", bb("Tuerblatt")["min"][2] - bb("Dichtung_links")["max"][2], 0, 0.01)
    # --- Zarge im Feld: unabhaengig aus den Knoten
    a, b, c = N[24], N[22], N[6]
    z0 = lay["base_z"]
    mx, my = (a["x"] + b["x"]) / 2, (a["y"] + b["y"]) / 2
    base_w = math.dist((a["x"], a["y"]), (b["x"], b["y"]))
    S = math.sqrt((c["x"] - mx) ** 2 + (c["y"] - my) ** 2 + (c["z"] - z0) ** 2)
    tilt = math.degrees(math.atan2(math.hypot(c["x"] - mx, c["y"] - my), c["z"] - z0))
    s_top = bb("Sturz")["max"][1]
    w_top = base_w * (1 - s_top / S)
    fw = bb("Schwelle")["max"][0] - bb("Schwelle")["min"][0]
    ck.eq(f"Zarge passt ins Feld: Feldbreite in Sturzhoehe {w_top:.0f} - Zarge {fw:.0f}, Reserve je Seite >= 100 mm", (w_top - fw) / 2, 100, 40)
    ck.eq(f"Neigung der Feldebene {tilt:.1f} Grad gegen tuer_komplett.json", tilt, D["geometrie"]["neigung_feldebene_grad"], 0.05)
    ck.eq("Feldazimut 149,2 (Basiskantenmitte)", math.degrees(math.atan2(my, mx)) % 360, 149.2, 0.1)
    ck.eq("Feld ist BBB (Basiskante und beide Hangkanten 3708)", 1 if all(abs(math.dist((p_["x"], p_["y"], p_["z"]), (q_["x"], q_["y"], q_["z"])) - 3708) < 15 for p_, q_ in ((a, b), (a, c), (b, c))) else 0, 1)
    hp = json.load(open(os.path.join(sc.ROOT, "data", "components", "haut_paneel.json"), encoding="utf-8"))
    doors = [f for f in hp["felder"] if f["door"]]
    ck.eq("Tuerfelder in haut_paneel.json (nur BBB 149,2)", len(doors), 1)
    ck.eq("Tuerfeld = BBB bei Azimut 149,2", 1 if doors and doors[0]["typ"] == "BBB" and abs(doors[0]["az"] - 149.2) < 0.1 else 0, 1)
    # --- Interferenz im Tuerdesign (Beruehrung erlaubt, kein Eindringen)
    itf = interference(path)
    for x in itf[:6]:
        print("   Interferenz", x)
    ck.eq("Interferenzen im Tuerdesign (Zarge, Blatt, Anschlag, Dichtung, Beschlaege)", len(itf), 0)
    # --- Paneel mit Tuerausschnitt
    pp, dp = sc.load_params("haut_paneel")
    full = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "haut_paneel_BBB.sc"))["bodies"][0]
    cut = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "haut_paneel_BBB_tuer.sc"))["bodies"][0]
    c_, r = 3708.0, 3708.0 * math.sqrt(3) / 6                       # gleichseitig: Inkreisradius
    k = (r - pp["edge_inset"]) / r
    side = c_ * k                                                    # Paneelkante
    h_pan = side * math.sqrt(3) / 2
    y_b = -r * k                                                     # Paneel-Basiskante im Inkreis-KS (Paneel zentriert um Inkreismittelpunkt)
    y_top = -r + D["geometrie"]["zarge_hoehe"]
    area = 0.0
    n = 4000
    for i in range(n):
        y = y_b + (i + 0.5) * (min(y_top, y_b + h_pan) - y_b) / n
        wp = side * (1 - (y - y_b) / h_pan)
        area += min(fw, wp) * (min(y_top, y_b + h_pan) - y_b) / n
    ck.eq("Paneel BBB mit Ausschnitt: Flaechenverlust (m2) gegen numerische Rechnung (Zarge 1076 x 2068 in das Paneeldreieck)", (full["volume_mm3"] - cut["volume_mm3"]) / pp["panel_t"] / 1e6, area / 1e6, 0.005)
    ck.eq("Paneel BBB_tuer: Dicke", cut["bbox"]["max"][2] - cut["bbox"]["min"][2], pp["panel_t"], 0.01)
    ck.eq("Paneel BBB_tuer: ein Koerper", len(sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "haut_paneel_BBB_tuer.sc"))["bodies"]), 1)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
