"""Vorpruefung Planen-Huelle (W27, D39, R24): keilschiene T43, huelle_folie T42, tuer_zarge_planenausschnitt T44.
Erwartung unabhaengig vom Generator: Profilflaeche aus der Skizze (Formel), Strebenlaengen und Dreiecksflaechen aus data/layout.json, 208 m2 aus R24, Interferenz per inspect.interference.
Aufruf: python scripts/workshop/check_huelle.py [keilschiene|folie|zarge ...]   (exit 1 bei FAIL)"""
import itertools, json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def comp(name):
    return os.path.join(sc.ROOT, "designs", "components", name + ".sc")

def interference(path):
    script = os.path.join(sc.TMP, "ws-huelle-interf.json"); out = os.path.join(sc.TMP, "ws-huelle-interf-out.json")
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

def strut_lengths():
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    return lay, sorted(set(lay["strut_len_mm"]))

def check_keilschiene(ck):
    p, d = sc.load_params("keilschiene")
    lay, lens = strut_lengths()
    A, B = lens[0], lens[-1]
    ck.eq("Strebenzahl laut layout.json = 65 = Anzahl Keilschienen", lay["struts"], sum(t["anzahl"] for t in d["typen"].values()))
    ck.eq("Typ A: len = Knotenabstand A - 2 x Knotenfreiraum", d["typen"]["A"]["len"], A - 2 * p["node_clear"], 1.0)
    ck.eq("Typ B: len = Knotenabstand B - 2 x Knotenfreiraum", d["typen"]["B"]["len"], B - 2 * p["node_clear"], 1.0)
    ck.eq("Gesamtlaenge Schienen in m (R24: ca. 228 m Knotenabstand, hier minus Freiraeume)", sum(t["anzahl"] * t["len"] for t in d["typen"].values()) / 1000, 30 * (A - 260) / 1000 + 35 * (B - 260) / 1000, 0.5)
    ck.eq("Gesamtlaenge gegen R24 (228 m) in Prozent Abweichung <= 8 %", 1 if abs(sum(t["anzahl"] * t["len"] for t in d["typen"].values()) / 1000 - 228) / 228 <= 0.08 else 0, 1)
    path = comp("keilschiene")
    ev = sc.evaluate(path)
    Bd = {b["name"]: b for b in ev["bodies"]}
    ext = lambda n, i: Bd[n]["bbox"]["max"][i] - Bd[n]["bbox"]["min"][i]
    w, h, t, lip, ft = p["ch_w"], p["ch_h"], p["ch_wall"], p["ch_lip"], p["foam_t"]
    ck.eq("Kanal Laenge (Konfiguration A)", ext("Kanal", 0), d["typen"]["A"]["len"], 0.05)
    ck.eq("Kanal Breite 25", ext("Kanal", 1), w, 0.05)
    ck.eq("Kanal Hoehe 15", ext("Kanal", 2), h, 0.05)
    area = w * t + 2 * t * (h - t) + 2 * (lip - t) * t
    ck.eq("Kanal Volumen = Profilflaeche (w*t + 2*t*(h-t) + 2*(lip-t)*t) x Laenge", Bd["Kanal"]["volume_mm3"], area * d["typen"]["A"]["len"], 20)
    ck.eq("Kanal Unterkante liegt auf dem Schaumband (z = 3)", Bd["Kanal"]["bbox"]["min"][2], ft, 0.01)
    ck.eq("Schaumband 25 x 3 x len", Bd["Schaumband"]["volume_mm3"], p["foam_w"] * ft * d["typen"]["A"]["len"], 20)
    ck.eq("Schaumband Unterkante z = 0 (Bezug)", Bd["Schaumband"]["bbox"]["min"][2], 0.0, 0.01)
    ck.eq("Federdraht Durchmesser 2", ext("Federdraht", 1), p["wire_d"], 0.02)
    ck.eq("Federdraht Laenge = len - 2 x 20", ext("Federdraht", 0), d["typen"]["A"]["len"] - 2 * p["wire_clear"], 0.05)
    ck.eq("Federdraht ist eigener Koerper", 1 if "Federdraht" in Bd else 0, 1)
    wb, kb = Bd["Federdraht"]["bbox"], Bd["Kanal"]["bbox"]
    ck.eq("Federdraht liegt im Kanal (Luft zum Grund 0,5 mm)", wb["min"][2] - (ft + t), p["wire_gap"], 0.01)
    ck.eq("Federdraht unter den Lippen (Oberkante < Lippen-Unterkante, Maul 17 mm > Draht)", 1 if wb["max"][2] < ft + h - t and w - 2 * lip > p["wire_d"] else 0, 1)
    ck.eq("Masse Kanal Typ A in kg (Dichte 2,7)", Bd["Kanal"]["mass_g"] / 1000, area * d["typen"]["A"]["len"] * 2.7 / 1e6, 0.002)
    # Konfiguration B: Zeile aktivieren, speichern, messen
    tmp = os.path.join(sc.TMP, "ws-keilschiene-B.sc"); script = os.path.join(sc.TMP, "ws-keil-B.json")
    json.dump({"commands": [{"command": "config.activate", "params": {"row": "B"}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--save", tmp, "--quiet"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER config B: " + r.stderr.strip())
    evb = sc.evaluate(tmp)
    Bb = {b["name"]: b for b in evb["bodies"]}
    ck.eq("Konfiguration B: Kanal Laenge", Bb["Kanal"]["bbox"]["max"][0] - Bb["Kanal"]["bbox"]["min"][0], d["typen"]["B"]["len"], 0.05)
    ck.eq("Konfiguration B: Federdraht Laenge", Bb["Federdraht"]["bbox"]["max"][0] - Bb["Federdraht"]["bbox"]["min"][0], d["typen"]["B"]["len"] - 2 * p["wire_clear"], 0.05)
    itf = interference(path)
    for x in itf[:6]:
        print("   Interferenz", x)
    ck.eq("Interferenzen Keilschiene (Schaumband, Kanal, Federdraht)", len(itf), 0)

def main(which):
    ck = sc.Check("huelle")
    if "keilschiene" in which:
        check_keilschiene(ck)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["keilschiene", "folie", "zarge"]))
