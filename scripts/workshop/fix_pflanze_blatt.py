"""Blatt-Texte Salatkopf/Netztopf nach Kritiker-Runden (29.10.): Masse aus der Messung, Herkunft, Stueckliste."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
def load(n):
    return os.path.join(sc.ROOT, "data", "components", n + ".json"), json.load(open(os.path.join(sc.ROOT, "data", "components", n + ".json"), encoding="utf-8"))
p, d = load("salatkopf")
ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "salatkopf.sc"))
mn, mx = sc.bbox_all(ev)
w, h = mx[0] - mn[0], mx[2]
n_leaves = sum(g["n"] for g in d["blatt_gruppen"]["gruppen"])
bl = d["blatt"]
bl["querschnitt"] = f"Blattrosette: Kuppelkoerper (Kugel) mit {n_leaves} geneigten Blattscheiben in {len(d['blatt_gruppen']['gruppen'])} Gruppen (Neigung -14 bis 64 Grad, Blattdicke 4,5 mm), Wurzelhals D16 x 25 mm nach unten in den Netztopf; Groesse M: Breite {w:.0f} mm, Hoehe {h:.0f} mm ueber dem Topfrand. Blattscheiben ueberlappen sich gewollt (Pflanze); Vereinigung flacher Scheiben scheitert im Kernel, daher je Gruppe eigene Koerper."
bl["abweichung"] = f"keine OBJ-Vorgabe (Salatkoepfe stammen aus ref-6); Groesse M: Breite {w:.0f} mm, Hoehe {h:.0f} mm (Verhaeltnis {h / w:.2f}; ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite)."
bl["kritiker"] = "Runde 1/2: Referenz gewaehlt (Kugelhaufen, Rose), Runde 3 (Kontextpaket): siehe workshop-log"
for r in d["herkunft_tabelle"]:
    if r[0].startswith("Salat als Blattrosette"):
        r[0] = f"Salat als buschige Blattrosette ({n_leaves} Blaetter, 7 Gruppen, Kuppelkoerper)"
    if r[0].startswith("Breite M"):
        r[0], r[1] = f"Breite M ca. {w:.0f} mm, Hoehe {h:.0f} mm", f"{w:.0f} / {h:.0f} mm"
        r[3] = "ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite; Kopf ca. 1,5-2 x Topfkragen (64 mm)"
    if r[1] in ("-", "mm"):
        pass
for r in d["herkunft_tabelle"]:
    if r[0].startswith("Gruen"):
        r[1] = "#58a63f"
    if r[0].startswith("Anzahl"):
        r[1] = "je Pflanzplatz"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("salatkopf.json gepflegt")
