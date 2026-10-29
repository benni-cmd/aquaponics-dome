"""Blatt pumpe nach Spec-Pruefer Runde 4 (W12, 29.10. ~15:05): Klemmlaenge M6x20 ohne Scheibe, Standwinkel-Befestigung und -Masse, Pumpenbefestigung, Stummel-Fix.
Aufruf: python scripts/workshop/fix_pumpe_blatt6.py <Anzahl-PASS>; danach partsheet.py pumpe."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
n = sys.argv[1]
p = os.path.join(sc.ROOT, "data", "components", "pumpe.json")
s = open(p, encoding="utf-8").read()
def rep(old, new):
    global s
    assert s.count(old) >= 1, old[:60]
    s = s.replace(old, new)
rep("Klemmlaenge Tafel 5/7 + Konsole 5 + Mutter 5,2 = 15,2/17,2 mm, Schraube 20 mm steht >= 2 Gewindegaenge ueber), Scheiben ISO 7089 (nicht modelliert) [A]", "Klemmlaenge Tafel 5/7 + Konsole 5 + Mutter 5,2 = 15,2/17,2 mm ohne Scheibe, Schraube 20 mm steht 4,8/2,8 mm ueber der Mutter)")
rep("Schrauben M6x20 ISO 4017 mit Muttern ISO 4032 2 und Scheiben ISO 7089 2 (Scheiben nicht modelliert);", "Schrauben M6x20 ISO 4017 mit Muttern ISO 4032 2 (ohne Scheiben);")
rep("Klemmlaenge Tafel + Konsole 5 + Mutter 5,2 = 15,2 (klein) / 17,2 (gross); M6x16 stand 0,8 mm bzw. gar nicht ueber der Mutter", "Klemmlaenge ohne Scheibe Tafel + Konsole 5 + Mutter 5,2 = 15,2 (klein) / 17,2 (gross); M6x16 stand 0,8 mm bzw. gar nicht ueber der Mutter")
rep("Standwinkel 50x100x5 2,", "Standwinkel (senkrechter Schenkel 50 x 100 x 5, waagerechter 50 x 80 x 5) 2,")
rep("4 Schrauben M6 fuer die Standwinkel (je Winkel 2)", "4 Schrauben M6x16 mit Mutter fuer Winkel an Tafel (je Winkel 2) und je Winkel 1-2 Schrauben M6 mit Duebel in den Untergrund")
rep("Tafel steht auf 2 Standwinkeln; je Winkel 2 Schrauben M6 mit Duebel/Mutter (4 je Tafel, nicht modelliert) [A], am tragfaehigen Untergrund zu verschrauben", "Standwinkel an der Tafel: je Winkel 2 Schrauben M6x16 mit Mutter (4 je Tafel, nicht modelliert) [A]; Winkel am tragfaehigen Untergrund: waagerechter Schenkel mit 1-2 Schrauben M6 und Duebel (nicht modelliert) [A]")
rep("Pumpe auf dem Sockel: 4 Schrauben M6x30", "Pumpe auf dem Sockel: Befestigung des zylindrischen Motors ueber Pumpenfuss/Spannband (nicht modelliert, Motor liegt tangential), 4 Schrauben M6x30")
d = json.loads(s)
d["blatt"]["offen"].append("Pumpenbefestigung auf dem Sockel (Fuss oder Spannband fuer den zylindrischen Motor) nicht modelliert und ohne Fabrikat offen")
d["blatt"]["offen"].append("parts.insert liefert beim ersten Bolzen einen D6-Stummel auf dem Kopf; pumpe.py schneidet ihn mit einem Werkzeugkoerper ab (Body1, Pruefzeile Schraubenvolumen gleich)")
d["herkunft_tabelle"].append(["Standwinkel: senkrechter Schenkel 50 x 100 x 5, waagerechter 50 x 80 x 5", "50 x 100 x 5 / 50 x 80 x 5 mm", "A", "gegen Kippen der stehenden Tafel; Masse aus pumpe.py (Winkel hinten an der Tafel)", "niedrig"])
d["herkunft_tabelle"].append(["Pumpenschrauben M6x30 (Klemmlaenge 24,4 mm)", "M6x30 ISO 4017", "E", "Sockel 11 + Konsole 5 + 2 Scheiben je 1,6 (ISO 7089) + Mutter 5,2 = 24,4 mm; nicht modelliert", "niedrig"])
d["blatt"]["pruefung"][0] = d["blatt"]["pruefung"][0].replace("32/32", f"{n}/{n}").replace("30/30", f"{n}/{n}")
d["blatt"]["pruefung"][1] = d["blatt"]["pruefung"][1].replace("Runde 3 (FAIL knapp, 5 Befunde, eingearbeitet;", "Runde 3 (FAIL knapp, 5 Befunde, eingearbeitet) und Runde 4 (PASS knapp, 4 kleine Befunde, eingearbeitet;")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pumpe.json aktualisiert", n)
