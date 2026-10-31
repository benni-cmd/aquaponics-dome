"""W32 (D55): data/descriptions.json fuer feinfilter und tank_gross nachziehen (Schwebebett, Hauptstrom-Feinfilter). Aufruf: python scripts/workshop/fix_w32_descriptions.py <tank-pruefungen z. B. 70/70>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

tank_count = sys.argv[1] if len(sys.argv) > 1 else "offen"
p = os.path.join(sc.ROOT, "data", "descriptions.json")
d = json.load(open(p, encoding="utf-8"))
E = {e["match"]: e for e in d["bauteile"]}

t = E["^tank_gross"]
t["was"] = "Tank mit Kegelboden und einem Schwebebett aus losen K1-Trägern: hier siedeln die Filterbakterien."
t["status"] = f"umgebaut W32 (Schwebebett), Selbstcheck {tank_count}, kein Prüfer-Lauf"
t["ablauf"] = [
    "Das Belüftungsgitter am Konusboden bläst Luft ein; die K1-Träger schweben und scheuern sich frei.",
    "Bakterien auf den Trägern (ca. 500 m² je m³ Schüttung) wandeln Ammonium über Nitrit in Nitrat um.",
    "Siebe an Zulauf und Überlauf (Schlitz 5 mm) halten die Träger im Tank.",
    "Ein Überlauf hält den Wasserstand, der Auslass führt das Wasser ab.",
    "Schlamm sinkt zur Kegelspitze und wird über den Kugelhahn abgelassen.",
]
for g in t["aufbau"]:
    if g["t"] == "Filter":
        g["p"] = [
            "Schwebebett: 470 l K1-Schüttung (67 % von 702 l), Oberkante Z 1353 unter dem Zulauf",
            "Belüftungsgitter Ø20 (Ring + 2 Arme) am Konus, Steigrohr Ø16 durch den Deckel",
            "Zulaufsieb (Schlitzkappe) und Auslaufsieb (Kappe Ø110), Schlitz 5 mm",
        ]
t["masse"]["Schwebebett im Modell"] = "ein Körper, 470 l Schüttvolumen (0,67 × 702 l); das Modell fasst 687 l bis zum Rand und 628 l bis zum Überlauf: Füllung 68 % bzw. 75 % des Modellwassers (Befund)"
t["grenzen"] = ("Die einzelnen K1-Träger sind nicht modelliert, das Bett ist ein Körper (Siebschlitze und Belüftungsbohrungen auch nicht). K1-Fläche 500 m²/m³ nur über Suchzusammenfassungen belegt (R30). "
                "Das Bett füllt 75 % des Modellwassers bis zum Überlauf (R30 rechnet mit 702 l): Überlauf tiefer oder Füllung 421 l offen. Luftmenge und Gebläse nicht gerechnet.")
t["quelle"] = "docs/parts/tank.md, docs/research/R30.md, docs/decisions.md D55"

f = E["^feinfilter"]
f["was"] = "Behälter mit herausnehmbarem Siebkorb im Hauptstrom: fängt die feinen Schwebstoffe aus den 110 l/min der Linie."
f["status"] = "neu bemessen W32 (Hauptstrom), Selbstcheck 54/54, kein Prüfer-Lauf"
f["ablauf"] = [
    "Das Wasser der Linie (110 l/min) fließt über ein senkrechtes Einlaufrohr Ø63 in den Siebkorb.",
    "Es tritt durch das Edelstahlgewebe (100 µm) in die Ablaufkammer unter dem Korb.",
    "Der Auslauf Ø63 führt zur Saugseite der großen Pumpen.",
    "Alle 1–2 Wochen: Spülanschluss öffnen, Deckel öffnen, Korb herausheben und ausspülen, Behälter über den Kugelhahn ablassen.",
]
f["aufbau"] = [
    {"t": "Behälter", "p": ["PP 630 × 440 × 610 mm, Wand 10 mm, Deckel mit Dichtung und 4 Spannverschlüssen", "Auflageleisten tragen den Korbflansch"]},
    {"t": "Siebkorb", "p": ["Edelstahl 560 × 370 × 400 mm, Gewebehülle mit Stützrahmen, Gewebe 100 µm", "2 Bügelgriffe zum Herausheben"]},
    {"t": "Wasserwege", "p": ["Einlauf Ø63 oben seitlich, Auslauf Ø63 unten seitlich", "Ablass Ø40 mit Kugelhahn und Schlauchtülle", "Spülanschluss Ø25 mit Kugelhahn und Spritzrohr", "Ports"]},
    {"t": "Unterbau", "p": ["Standrahmen Vierkantrohr 40 × 40 mm, 250 mm hoch (Eimer unter dem Ablass), 4 Auflagestege unter dem Boden"]},
]
f["masse"] = {
    "Anzahl": "2 (eine je Linie)",
    "Leermasse": "40,5 kg, im Betrieb ca. 175 kg",
    "Inhalt": "154 l bis zum Rand",
    "Siebfläche": "0,84 m² benetzt (Soll 0,825 m² = 6,6 m³/h ÷ 8 m/h)",
    "Durchfluss": "110 l/min je Linie (Hauptstrom), Siebbelastung 7,9 m/h [A], Rohrgeschwindigkeit 0,72 m/s",
}
f["grenzen"] = ("Die Siebbelastung 8 m/h ist eine Annahme (R30 nennt keine belegte Auslegungsgröße). Kein Notüberlauf bei verstopftem Korb. Höhenlage und Platz (ca. 770 × 680 mm, 855 mm hoch) prüft die Montage (M10); "
                "die Netzliste führt den Feinfilter noch mit Ø50 und 12,5 l/min. Fabrikate von Gewebe, Spannverschlüssen und Kugelhähnen offen.")
f["quelle"] = "docs/parts/feinfilter.md, docs/filter-konzept.md Art 2, docs/research/R30.md, docs/decisions.md D55"
f["rolle"] = ("Art 2 der Filterarten (docs/filter-konzept.md, R30): Sieb im HAUPTSTROM vor den großen Pumpen (110 l/min je Linie, W32/D55). Vorher (W31) im Absetzer-Teilstrom (12,5 l/min = 11 %, Gewebe 150 µm) – Befund R30: 89 % des Wassers umgingen das Sieb. "
              "Jetzt Gewebe 100 µm (Mortensen 2000: 30/60/100 µm = 99/48/21 % Schwebstoffe) und Siebfläche aus Strom ÷ Siebbelastung.")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
