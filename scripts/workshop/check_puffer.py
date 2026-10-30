"""Vorpruefung Puffer-IBC T80 und Puffer-Station T81 (W28, D46): Handelsmass, Blase/Wasser/Nutzvolumen, Ports, Interferenz; Station: Stapelhoehe <= 2,5 m, Tragwerk, Messplatz/Dosierkonsole.
Erwartung unabhaengig vom Generator: Volumen aus der Blasen-Innenkontur und dem Wasserkoerper-Volumen (eval), Ports aus den Stutzen-Boxen.
Aufruf: python scripts/workshop/check_puffer.py [ibc|station ...]   (exit 1 bei FAIL)"""
import json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def interference(path):
    script = os.path.join(sc.TMP, "ws-puffer-interf.json"); out = os.path.join(sc.TMP, "ws-puffer-interf-out.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 240}}]}, open(script, "w"))
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

def check_ibc(ck):
    p, d = sc.load_params("puffer_ibc")
    path = os.path.join(sc.ROOT, "designs", "components", "puffer_ibc.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    bb = lambda n: B[n]["bbox"]
    # Handelsmass: Kaefig/Palette ueber alles 1200 x 1000, Deckelkante 1165
    x0 = min(bb(n)["min"][0] for n in B if n.startswith(("Kufe", "Deckplatte", "Rahmen", "Pfosten")))
    x1 = max(bb(n)["max"][0] for n in B if n.startswith(("Kufe", "Deckplatte", "Rahmen", "Pfosten")))
    y0 = min(bb(n)["min"][1] for n in B if n.startswith(("Kufe", "Deckplatte", "Rahmen", "Pfosten")))
    y1 = max(bb(n)["max"][1] for n in B if n.startswith(("Kufe", "Deckplatte", "Rahmen", "Pfosten")))
    ck.eq("IBC Laenge Palette/Kaefig 1200", x1 - x0, 1200, 0.1)
    ck.eq("IBC Breite Palette/Kaefig 1000", y1 - y0, 1000, 0.1)
    ck.eq("IBC Hoehe Deckeloberkante 1165", bb("Deckel")["max"][2], 1165, 0.1)
    ck.eq("Palettenhoehe 150 (Deckplatte Oberkante)", bb("Deckplatte")["max"][2], 150, 0.1)
    # Stab-Zahlen: Langseiten 2 x (5 senkrecht + 8 waagerecht), Stirnseiten 2 x (4 senkrecht + 8 waagerecht)
    ck.eq("Gitterstaebe gesamt (2 x 13 Langseite + 2 x 12 Stirnseite)", len([k for k in B if k.startswith("Stab_")]), 2 * 13 + 2 * 12)
    # Nutzvolumen: Wasserkoerper-Volumen (Messung) gegen 900 l; Blasen-Innenvolumen > 1000 l (Nenninhalt)
    ck.eq("Nutzvolumen Wasserkoerper (Liter) = 900", B["Wasser"]["volume_mm3"] / 1e6, p["nutz_l"], 0.5)
    wi, li, ri = p["blase_w"] - 2 * p["blase_wall"], p["blase_l"] - 2 * p["blase_wall"], p["blase_r"] - p["blase_wall"]
    inner_l = (li * wi - (4 - math.pi) * ri * ri) * (p["pal_h"] + p["blase_h"] - p["blase_wall"] - (p["pal_h"] + p["blase_wall"])) / 1e6
    ck.eq(f"Blasen-Innenvolumen {inner_l:.0f} l >= 1000 (Nenninhalt 1000 l) und <= 1100", 1 if 1000 <= inner_l <= 1100 else 0, 1)
    ck.eq("Wasserstand unter dem Ueberlauf-Stutzenboden (Stutzenunterkante - Wasseroberflaeche, mm >= 20)", 1 if bb("Ueberlauf")["min"][2] - bb("Wasser")["max"][2] >= 20 else 0, 1)
    ov = B["Ueberlauf"]["bbox"]
    ck.eq("Ueberlauf-Volumen bis Stutzenunterkante (Liter) liegt zwischen 900 und 1000", 1 if 900 <= (ov["min"][2] - (p["pal_h"] + p["blase_wall"])) * (li * wi - (4 - math.pi) * ri * ri) / 1e6 <= 1000 else 0, 1)
    # Ports: Lage und Richtung aus den Stutzenboxen
    ck.eq("Zulauf oben: Zapfenende y -545, z-Mitte 1100", abs(bb("Zulauf")["min"][1] + 545) + abs((bb("Zulauf")["min"][2] + bb("Zulauf")["max"][2]) / 2 - p["zulauf_z"]), 0, 0.6)
    ck.eq("Ueberlauf oben: Zapfenende y 545, z-Mitte 1090", abs(bb("Ueberlauf")["max"][1] - 545) + abs((bb("Ueberlauf")["min"][2] + bb("Ueberlauf")["max"][2]) / 2 - p["ueberlauf_z"]), 0, 0.6)
    ck.eq("Ablauf unten: Zapfenende y -615, z-Mitte 215", abs(bb("Ablauf_Zapfen")["min"][1] + 615) + abs((bb("Ablauf_Zapfen")["min"][2] + bb("Ablauf_Zapfen")["max"][2]) / 2 - p["ablauf_z"]), 0, 0.6)
    ck.eq("Ablauf DN50: Zapfen d63", bb("Ablauf_Zapfen")["max"][0] - bb("Ablauf_Zapfen")["min"][0], p["stub_od"], 0.1)
    ck.eq("Dachstutzen (Belueftung, Sensor) Oberkante <= 1195 (Stapelhoehe)", 1 if max(bb("Belueftung")["max"][2], bb("Sensorstutzen")["max"][2]) <= 1195 else 0, 1)
    ck.eq("Einfuelloeffnung DN150: Halsbohrung 150 gegen Deckel 235 (Deckel ueberdeckt die Oeffnung)", 1 if p["lid_d"] > p["neck_id"] else 0, 1)
    # Stutzen in Gittermaschen: Abstand der Seitenstutzen zu den senkrechten Staeben (x 200/400) >= 3 mm
    ck.eq("Seitenstutzen x 300 +- 31,5 zwischen den Staeben x 200 und 400 (Abstand >= 3 mm)", 1 if 300 - p["stub_od"] / 2 - (200 + p["rod_d"] / 2) >= 3 and 400 - p["rod_d"] / 2 - (300 + p["stub_od"] / 2) >= 3 else 0, 1)
    itf = interference(path)
    for x in itf[:8]:
        print("   Interferenz", x)
    ck.eq("Interferenzen im Puffer-IBC (Kaefig, Blase, Anschluesse, Palette)", len(itf), 0)

def main(which):
    ck = sc.Check("puffer")
    if "ibc" in which:
        check_ibc(ck)
    if "station" in which:
        import check_puffer_station as cps
        cps.check_station(ck, interference)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["ibc"]))
