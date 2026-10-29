"""Einmalige Pflege des Blatt-Textes data/components/ibc_beet.json nach Bild-Kritiker (Siebboden 8 mm, Stuetzen, Randsims 20 x 14)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "ibc_beet.json")
d = json.load(open(p, encoding="utf-8"))
bl = d["blatt"]
bl["querschnitt"] = bl["querschnitt"].replace("Randwulst 10 x 12 mm", "Randsims 20 x 14 mm").replace("Siebboden 5 mm auf 6 (innen) bzw. 8 (aussen) Stuetzkloetzen 60 x 60", "Siebboden 8 mm auf 15 (innen, 5 x 3) bzw. 24 (aussen, 8 x 3) Stuetzkloetzen 60 x 60 (Abstand <= 420 mm)")
bl["stueckliste"] = [x.replace("6 (innen) / 8 (aussen) je Beet", "15 (innen) / 24 (aussen) je Beet").replace("Siebboden 5 mm (PP)", "Siebboden 8 mm (PP)") for x in bl["stueckliste"]]
bl["verbindungen"] = [x.replace("Siebboden liegt auf Stuetzkloetzen", "Siebboden (8 mm, Rasterlochplatte) liegt auf 15/24 Stuetzkloetzen") for x in bl["verbindungen"]]
bl["abweichung"] = "OBJ ibc_beds: Laenge/Breite/Hoehe wie layout.json (Messung 0 mm Abweichung); die Bezeichnung 'halbe IBC' (OBJ-Gruppe IBC_Open_Top) passt nicht zu 2953 mm (eine halbe IBC misst ca. 1200 x 1000): die 2953-mm-Wanne ist ein Sonderbau (verschweisste/laengere Wanne) - Bild-Kritiker Luecke 1, offen beim Orchestrator; Medium-Hoehe absolut Z 400 laut R03; Beetinnenraum im OBJ nicht modelliert -> Aufbau aus R03."
bl["offen"] += ["Wanne 2953 mm lang: 'halbe IBC' ist nur die OBJ-Bezeichnung; Fertigung als Sonderwanne (Bild-Kritiker Luecke 1, Einstufung: gueltig, Klaerung Orchestrator)", "Zulauf-Wanddurchfuehrung ohne Fitting/Dichtung modelliert (nur Bohrung D22, Gummitulle im Blatt)"]
for r in d["herkunft_tabelle"]:
    if r[0].startswith("Randwulst"):
        r[0], r[1], r[3] = "Randsims 20 x 14 mm", "20 / 14", "ref-5/ref-6: breiter flacher Randsims der weissen Wannen (Bild-Kritiker)"
    if r[0].startswith("Siebboden 5"):
        r[0], r[1] = "Siebboden 8 mm, Lochraster 20 x 5 D12 (vereinfacht)", "8 / D12"
    if r[0].startswith("Stuetzkloetze"):
        r[0], r[1], r[3] = "Stuetzkloetze 60x60, 15 (innen) / 24 (aussen)", "60 x 60", "Konstruktionspraxis; Abstand <= 420 mm wegen Medienlast (Bild-Kritiker); Wasserraum unter dem Medium ist Annahme"
    if r[1] in ("-", "mm"):
        pass
fill = {"Medium als EIN": "1 Koerper", "Siebboden 8": "8 mm", "Standrohr d25": "d25 / 220", "Glocke d75": "d75 x 250", "Medienschutz": "d110 x 320", "Bulkhead": "D36 / Flansch D50", "Zulauf 200": "200-500 l/h", "Werkstoff": "HDPE / Blaehton", "Zulauf-Tropfrohr": "d20, z 450 abs."}
for r in d["herkunft_tabelle"]:
    for k, v in fill.items():
        if r[0].startswith(k) and r[1] in ("-", "mm"):
            r[1] = v
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ibc_beet.json gepflegt")
