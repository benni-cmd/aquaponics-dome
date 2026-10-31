"""Pruefung Messstellen-Bauteile T90/T91 (W35, R39): je Komponente (Halter und Sonden aus messstellen.COMPS) Koerperzahl = Teile-Zeilen (Roadmap B1), Namen, Masse > 0, Ports (Lage in der Bounding-Box
des Koerpers, Spitzen am Rand in Richtung), Bauteilmasse gegen Parameter und Standardmasse, Interferenz 0. Erwartungen aus den Parametern der Spezifikation und den Quellen (R39, EN 1452), nicht aus den Bau-Funktionen.
Aufruf: python scripts/workshop/check_messstellen.py [schluessel ...]   (exit 1 bei FAIL)"""
import json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import messstellen as M

def interference(path):
    script = os.path.join(sc.TMP, "ws-ms-interf.json")
    out = os.path.join(sc.TMP, "ws-ms-interf-out.json")
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
    return find(d) or []

def ring(d, w):
    return math.pi / 4 * (d * d - (d - 2 * w) ** 2)

def ext(B, n, i):
    return B[n]["bbox"]["min"][i], B[n]["bbox"]["max"][i]

# ---- spezifische Pruefungen je Komponente (Erwartung aus Parametern)
def chk_tauch(ck, p, B):
    L = p["laenge"]
    ck.eq("Tauchrohr Aussen-D 40", ext(B, "Tauchrohr", 0)[1] - ext(B, "Tauchrohr", 0)[0], p["rohr_d"], 0.1)
    ck.eq("Tauchrohr Laenge 1000", ext(B, "Tauchrohr", 2)[1] - ext(B, "Tauchrohr", 2)[0], L, 0.1)
    exp = ring(p["rohr_d"], p["rohr_wall"]) * L
    ck.eq("Tauchrohr Volumen = Ringflaeche x Laenge (minus 2 Querbohrungen, 1,5 %)", B["Tauchrohr"]["volume_mm3"], exp, exp * 0.015)
    ck.eq("Eintauchtiefe = Klemmenhoehe 640 - Freibord (Rand Z 650 - Spiegel 515 = 135) im Bereich 300-700 (R39)", 1 if 300 <= p["schelle_z"] - (650 - 515) <= 700 else 0, 1)
    ck.eq("Klemmarm liegt ueber dem Beckenrand: Hakeninnenkante >= Ringradius + Wand 150 (Beckenwand params wall 150)", 1 if ext(B, "Klemme", 0)[1] - 20 >= p["schelle_od"] / 2 + 150 else 0, 1)
    ck.eq("Rohr-ID >= 30 (groesste Tauchsonde do_ind d25 plus Spiel)", 1 if p["rohr_d"] - 2 * p["rohr_wall"] >= 30 else 0, 1)
    ck.eq("Kappe sitzt auf dem Rohrende (z-Anlage)", ext(B, "Kappe", 2)[0], ext(B, "Tauchrohr", 2)[1], 0.1)

def chk_beruhig(ck, p, B):
    L = p["laenge"]
    ck.eq("Rohr Aussen-D 63", ext(B, "Rohr", 0)[1] - ext(B, "Rohr", 0)[0], p["rohr_d"], 0.1)
    ck.eq("Rohr Laenge 600", ext(B, "Rohr", 2)[1] - ext(B, "Rohr", 2)[0], L, 0.1)
    exp = ring(p["rohr_d"], p["rohr_wall"]) * L - 4 * p["rohr_wall"] * p["schlitz_w"] * p["schlitz_l"]
    ck.eq("Rohr Volumen = Ringflaeche x Laenge minus 4 Schlitze (2 %)", B["Rohr"]["volume_mm3"], exp, exp * 0.02)
    ck.eq("Rohr-ID >= 40 (Schwimmerschalter d30 hinein)", 1 if p["rohr_d"] - 2 * p["rohr_wall"] >= 40 else 0, 1)
    ck.eq("Schlitze liegen im Rohr (Schlitz-Oberkante <= Rohrlaenge, Unterkante >= 0)", 1 if (L - p["schlitz_l"]) / 2 >= 0 else 0, 1)
    ck.eq("Bodenkappe schliesst unten an (Oberkante = Rohr-Unterkante)", ext(B, "Bodenkappe", 2)[1], ext(B, "Rohr", 2)[0], 0.1)
    ck.eq("Deckelkappe sitzt oben auf (Unterkante = Rohr-Oberkante)", ext(B, "Deckelkappe", 2)[0], ext(B, "Rohr", 2)[1], 0.1)
    ck.eq("zwei Rohrschellen mit Abstand >= 300 (Rohr stabil gehalten)", 1 if ext(B, "Schelle_2", 2)[0] - ext(B, "Schelle_1", 2)[1] >= 300 else 0, 1)

def chk_zelle(ck, p, B):
    L = p["laenge"]
    ck.eq("Zellkoerper Laenge 220", ext(B, "Zellkoerper", 0)[1] - ext(B, "Zellkoerper", 0)[0], L, 0.1)
    ck.eq("Zellkoerper-Oberkante mit Stutzen = 22 + 30", ext(B, "Zellkoerper", 2)[1], p["hoehe"] / 2 + p["stutzen_h"], 0.1)
    xs = p["stutzen_x"]
    ck.eq("Sondenstutzen-Abstand >= 60 (Sonden d12 mit Kabelverschraubung)", 1 if min(b - a for a, b in zip(xs, xs[1:])) >= 60 else 0, 1)
    ck.eq("Anschluss Zulauf d20", ext(B, "Anschluss_Zulauf", 1)[1] - ext(B, "Anschluss_Zulauf", 1)[0], p["anschl_d"], 0.1)
    ck.eq("Anschluesse schliessen an den Zellkoerper an (x 0 bzw. 220)", abs(ext(B, "Anschluss_Zulauf", 0)[1] - 0) + abs(ext(B, "Anschluss_Ablauf", 0)[0] - L), 0, 0.1)
    ck.eq("Absperrhahn schliesst an den Ablaufstutzen an", ext(B, "Absperrhahn", 0)[0], ext(B, "Anschluss_Ablauf", 0)[1], 0.1)
    vz = math.pi / 4 * p["bohr_d"] ** 2 * L / 1e6
    ck.eq(f"Zellvolumen {vz * 1000:.0f} ml (Bohrung d28 x 220) < 0,2 l: schneller Austausch bei 3 l/min", 1 if vz < 0.2 else 0, 1)

SPECIAL = {"halter_tauch": chk_tauch, "halter_beruhig": chk_beruhig, "halter_zelle": chk_zelle}

def main(keys):
    ck = sc.Check("messstellen")
    for key in keys:
        c = M.COMPS[key]
        path = os.path.join(sc.ROOT, "designs", "components", key + ".sc")
        ev = sc.evaluate(path)
        B = {b["name"]: b for b in ev["bodies"]}
        p = {k: v[0] for k, v in c["params"].items()}
        names = [t[0] for t in c["teile"]]
        ck.eq(f"{key}: Koerper = Teile-Zeilen ({len(names)}) (Roadmap B1)", len(B), len(names))
        ck.eq(f"{key}: Koerpernamen gleich den Teile-Zeilen", 1 if set(B) == set(names) else 0, 1)
        ck.eq(f"{key}: jeder Koerper hat Masse > 0", 1 if all(b["mass_g"] > 0 for b in B.values()) else 0, 1)
        for (nm, dn, pos, dr, body, tip) in c["ports"](p):
            if body not in B:
                ck.eq(f"{key}: Port '{nm}' Koerper {body} vorhanden", 0, 1)
                continue
            bb = B[body]["bbox"]
            inside = all(bb["min"][i] - 0.3 <= pos[i] <= bb["max"][i] + 0.3 for i in range(3))
            ck.eq(f"{key}: Port '{nm}' liegt am Koerper {body}", 1 if inside else 0, 1)
            if tip:
                ax = [i for i in range(3) if dr[i]][0]
                edge = bb["max"][ax] if dr[ax] > 0 else bb["min"][ax]
                ck.eq(f"{key}: Port '{nm}' Spitze am Rand in Richtung {dr}", edge, pos[ax], 0.3)
        if key in SPECIAL:
            SPECIAL[key](ck, p, B)
        inter = [i for i in interference(path) if i.get("volume_mm3", 0) > 1.0]
        ck.eq(f"{key}: Interferenzen (Volumen > 1 mm3)", len(inter), 0)
        for i in inter[:6]:
            print("   Interferenz", key, i["a"], i["b"], round(i.get("volume_mm3", 0), 1), "mm3")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main([a for a in sys.argv[1:]] or list(M.COMPS)))
