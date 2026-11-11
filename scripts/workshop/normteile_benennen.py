"""W60 5a (Gruppe Tische, Rinnen, Beete, Toepfe): benennt die Normteil-Koerper `Body<n>` der Tisch-Dateien und des Winkelhalters um,
ohne die Geometrie neu zu bauen (body.rename auf der vorhandenen .sc, speichert dieselbe Datei).
parts.insert benennt nur die Komponente; die Koerper heissen Body<n>. Die Gestalt (Bounding-Box) sagt, welches Normteil es ist:
  M8x30, M6x40, M6x16, M6x55 (Sechskantschrauben), M5x12, Mutter M6 (Gestaltwerte aus dem Modell, Toleranz 0,3 mm).
Namen: Schraube_<Gewinde>x<Laenge>_<k> und Schraube_Mutter_M6_<k> (Mutter mit Praefix Schraube_, damit die Stueckliste sie wie die anderen
Normteile ueber die Gestalt dem Schraubensatz zuordnet, scripts/bom_artikel.py zuordnen()). k zaehlt je Klasse in der Reihenfolge der Body-Nummern.
Aufruf: python -X utf8 scripts/workshop/normteile_benennen.py          (idempotent: Dateien ohne Body<n> bleiben unveraendert)
Die Generatoren nft_tisch.py und winkelhalter.py rufen benennen(pfad) nach dem Bau auf, damit ein Neubau dieselben Namen liefert."""
import os, re, json, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

D = os.path.join(sc.ROOT, "designs", "components")
# sortierte Bounding-Box-Masse (mm) -> Namensstamm
KLASSEN = [((13.0, 15.0, 35.3), "Schraube_M8x30"), ((10.0, 11.5, 44.0), "Schraube_M6x40"), ((8.0, 9.2, 15.5), "Schraube_M5x12"),
           ((10.0, 11.5, 20.0), "Schraube_M6x16"), ((10.0, 11.5, 59.0), "Schraube_M6x55"), ((5.2, 10.0, 11.5), "Schraube_Mutter_M6")]
TOL = 0.3
DATEIEN = ["nft_tisch_mitte", "nft_tisch_aussen", "nft_tisch_innen", "winkelhalter"]


def klasse(b):
    d = sorted(b["bbox"]["max"][i] - b["bbox"]["min"][i] for i in range(3))
    for ref, stamm in KLASSEN:
        if all(abs(a - r) <= TOL for a, r in zip(d, ref)):
            return stamm
    return None


BENANNT = re.compile(r"(Schraube_(?:M\d+x\d+|Mutter_M6))_(\d+)(?: \(\d+\))?")   # schon benanntes Normteil (eingefuegte Komponente), ab der zweiten Instanz mit Zusatz ' (m)'


def plan(bodies):
    """{Body<n>: neuer Name}; bricht ab, wenn ein Body<n> keiner Klasse zugeordnet werden kann.
    D136 (U3b): Ein Tisch enthaelt den seit W60 5a benannten Winkelhalter schon mit Namen wie Schraube_Mutter_M6_1; ein Zaehler ab 1 liess die eigenen
    Normteile denselben Namen doppelt treffen (`another body is called Schraube_Mutter_M6_1`). Der Zaehler je Klasse beginnt jetzt hinter dem hoechsten
    schon vergebenen Index dieser Klasse; Klassen ohne vorhandene Namen zaehlen wie bisher ab 1 in der Reihenfolge der Body-Nummern."""
    zaehler = {}
    for b in bodies:
        m = BENANNT.fullmatch(b["name"])
        if m:
            zaehler[m.group(1)] = max(zaehler.get(m.group(1), 0), int(m.group(2)))
    nums = sorted((int(b["name"][4:]), b) for b in bodies if re.fullmatch(r"Body\d+", b["name"]))
    out = {}
    for n, b in nums:
        st = klasse(b)
        if st is None:
            sys.exit(f"FEHLER: {b['name']} passt zu keiner Klasse (Masse {sorted(b['bbox']['max'][i] - b['bbox']['min'][i] for i in range(3))})")
        zaehler[st] = zaehler.get(st, 0) + 1
        out[b["name"]] = f"{st}_{zaehler[st]}"
    return out


def benennen(path):
    ev = sc.evaluate(path)
    pl = plan(ev["bodies"])
    if not pl:
        return {}
    cmds = [{"command": "body.rename", "params": {"body": k, "name": v}} for k, v in pl.items()]
    script = os.path.join(sc.TMP, "ws-normteile-rename.json")
    json.dump({"commands": cmds}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--save", path, "--quiet"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER rename " + path + ": " + r.stderr.strip() + r.stdout.strip())
    return pl


if __name__ == "__main__":
    for k in DATEIEN:
        pl = benennen(os.path.join(D, k + ".sc"))
        print(k, "umbenannt:", len(pl))
        # Teiledaten nachfuehren: Koerpernamen der Teilezeilen
        pf = os.path.join(sc.ROOT, "data", "parts", k + ".json")
        d = json.load(open(pf, encoding="utf-8"))
        if pl:
            for t in d["teile"]:
                if any(n in pl for n in t["koerper"]):
                    t["koerper"] = sorted((pl.get(n, n) for n in t["koerper"]), key=lambda s: (s.rsplit("_", 1)[0], int(s.rsplit("_", 1)[1])))
            with open(pf, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write("\n")
