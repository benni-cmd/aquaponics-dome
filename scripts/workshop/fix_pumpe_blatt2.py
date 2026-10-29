"""Nachbesserung Blatt pumpe nach Spec-Pruefer (FAIL, 29.10.): Rolle der Module mit Gegenindizien, Anzahl/Duplikate, Herkunftswerte, Gewichte, Foerderstrom, Kleinigkeiten. Nach fix_pumpe_blatt.py ausfuehren."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "pumpe.json")
d = json.load(open(p, encoding="utf-8"))
bl = d["blatt"]
d["parameter"]["foot_h"]["herkunft"] = "[A] (derzeit ungenutzt) Standwinkel statt Fussleiste: 2 Winkel 50 x 100 x 5 hinten an der Tafel"
bl["funktion"] = ("Pump-/Filtermodule an den Tanks (Rolle ANNAHME): Pumpenmodul = Montagetafel mit Kreiselpumpe fuer den Umlauf (Foerderstrom laut docs/hydraulics.md 2.3 [E]: kleiner Tank ca. 12 l/min, grosser ca. 30 l/min, statische Hoehe ca. 1,3 m plus Reibung); "
                  "Filtermodul = flache Filterkassette mit Siebeinsatz (Feinfilter, Matte) im Wasserweg. GEGENINDIZIEN zur Rolle der 384er-Kassetten (Spec-Pruefer): alle 10 liegen radial zur Tankachse (Abstand 276 mm, r 84-468), Oberkante = Plattform-Oberkante (668/670) und innerhalb der Plattform - das sieht nach Stuetzrippen/Konsolen der Klasse Tank aus; die 502/693er-Tafeln stehen tangential am Boden. Entscheidung offen (Orchestrator).")
bl["abweichung"] = ("layout.json tanks[].modules: Tafel- und Kassettenmasse stimmen auf <= 1 mm (OBJ 501/502 x 5 x 345, 693 x 7 x 463, 384 x 43/44 x 418/419; Bauteil 502/693/384 mit Dicke 5/7/44); Lage je Modul: layout.json (yaw: Tafeln 22,9/40,7 bzw. 22,9/41,1 Grad, Kassetten 0/45/90/135 Grad versetzt; z0 Tafeln -6..3, Kassetten 249-256) - Integrator. "
                    "Anzahl: OBJ listet je Tank 4 (klein) bzw. 8 (gross) Eintraege (components.md: 4-8), davon 2 bzw. 1 Duplikate an derselben Position (Abstand <= 5 mm) -> 2 Tafeln je kleinem Tank, 2 Tafeln + 5 Kassetten je grossem Tank; gesamt 4 / 4 / 10. docs/hydraulics.md 3 sieht je Linie Pumpe A, Pumpe B und ein Feinsieb vor (4 Pumpen, 2 Siebe): Abweichung zu 8 Tafeln und 10 Kassetten offen. "
                    "Im OBJ sind es nur Boxen ohne Pumpe, Anschluesse oder Kabel: Pumpe, Konsole, Stutzen, Kabel sind [A]. Ausrichtung: Pumpenseite +Y; im OBJ steht die Tafel tangential zum Tank, +Y soll vom Tank weg zeigen (yaw des Integrators).")
bl["offen"] = ["ROLLE der Module ist Annahme mit Gegenindizien (Kassetten radial unter/in der Plattform, Oberkante = Plattform-OK: moeglicherweise Stuetzrippen der Klasse Tank; Tafeln tangential am Boden: Seitenbleche/Spritzschutz?) - Entscheidung Orchestrator", "Anzahl gegen Hydraulik: 4 Pumpenmodule (OBJ) gegen 4 Pumpen A/B + 2 Siebe (hydraulics.md 3); je Tank zwei Pumpen (Betrieb/Reserve) steht nirgends", "Pumpenfabrikat, Leistung (R07 pausiert); Foerderstrom 12 / 30 l/min nur als [E] aus hydraulics.md", "Schrauben der Pumpe auf dem Sockel (4 x M6), Standwinkel-Befestigung, Deckeldichtung und Deckel-Flansch nicht modelliert", "Kabel gerade und 150 mm kurz modelliert (real 1,5-3 m); Elektrik/Zufuehrung: Schaltschrank-Klasse", "Durchdringung Kassetten/Plattform und Pumpe/Tankkegel: Integrator/Tank pruefen"]
bl["stueckliste"] = [x + ("; zusaetzlich 4 Schrauben M6x20 fuer die Pumpe, 2 Schrauben M6 fuer die Standwinkel, Dichtung ID 16 (nicht modelliert)" if x.startswith("pumpe_") else "; zusaetzlich Deckeldichtung 1 (nicht modelliert)" if x.startswith("filtermodul") else "") for x in bl["stueckliste"]]
# Port Strom: Steckerende
for pt in bl["ports"]:
    if "Stromanschluss" in pt[0]:
        x = float(pt[2].split()[1].rstrip(","))
        pt[2] = pt[2] + f" (Steckermitte; Steckerende x {x - 27.5:.0f}, Kabel 150 mm)"
d["herkunft_tabelle"] = [
    ["Tafel klein 502 x 5 x 345 (2 je Tank, 4 gesamt)", "502 x 5 x 345 mm", "OBJ", "layout.json tanks 1 und 4 modules (4 Eintraege je Tank, 2 Duplikate zusammengefasst; OBJ 501-502)", "hoch"],
    ["Tafel gross 693 x 7 x 463 (2 je Tank, 4 gesamt)", "693 x 7 x 463 mm", "OBJ", "layout.json tanks 2 und 3 modules (3 Eintraege je Tank, 1 Duplikat)", "hoch"],
    ["Kassette 384 x 44 x 419 (5 je Tank gross, 10 gesamt)", "384 x 44 x 419 mm", "OBJ", "layout.json tanks 2 und 3 modules (OBJ 384 x 43/44 x 418/419, z0 249-256, yaw 0/45/90/135 Grad, radial zur Tankachse)", "hoch"],
    ["Rolle: Tafel = Pumpenmodul, Kassette = Filtermodul", "Annahme", "A", "docs/components.md (Bedeutung Annahme), hydraulics.md (Pumpen, Feinsieb); GEGENINDIZ: Kassetten radial in der Plattform, Oberkante = Plattform-OK (Spec-Pruefer)", "niedrig"],
    ["Anzahl 4 / 4 / 10 (aus 4 bzw. 8 OBJ-Eintraegen je Tank)", "4 / 4 / 10", "OBJ + E", "Duplikate (<= 5 mm Versatz) zusammengefasst; hydraulics.md 3 nennt 4 Pumpen + 2 Siebe (Abweichung offen)", "mittel"],
    ["Kreiselpumpe klein: Motor D90 x 150, Kopf D110 x 70, Achse 120 ueber der Tafelunterkante", "D90/150, D110/70, z 120", "A", "typische Teich-/Umwaelzpumpe; keine Quelle (R07 pausiert)", "niedrig"],
    ["Kreiselpumpe gross: Motor D110 x 180, Kopf D130 x 80", "D110/180, D130/80", "A", "typische Umwaelzpumpe; keine Quelle", "niedrig"],
    ["Foerderstrom klein ca. 12 l/min, gross ca. 30 l/min", "12 / 30 l/min", "E", "docs/hydraulics.md 2.3 (Verweilzeit 30 min im Absetzer)", "niedrig"],
    ["Saug-/Druckstutzen d40/d32 (klein), d50/d40 (gross)", "d40/d32; d50/d40", "A", "Rohr d50/d63 am Tank (R09 A); Pumpen-DN Annahme", "niedrig"],
    ["Konsole Winkel 5 mm, 150 breit; Pumpensockel 8 mm", "150 x 5 mm; 8 mm", "A", "Konstruktionspraxis", "niedrig"],
    ["Standwinkel 50 x 100 x 5 (2 je Tafel)", "50 x 100 x 5 mm", "A", "gegen Kippen der stehenden Tafel", "niedrig"],
    ["Kabel 3 x 1,5 mm2 D8, 150 mm modelliert; Schutzkontaktstecker 55 x 45 x 40", "D8 x 150; 55 x 45 x 40 mm", "A", "230 V Standard; Laenge kuerzer als real (1,5-3 m)", "niedrig"],
    ["Filtergehaeuse Wand 3 mm, Deckel 5 mm, Siebeinsatz mit 4 mm Spiel", "3 / 5 / 4 mm", "A", "Kunststoffgehaeuse Praxis", "niedrig"],
    ["Ein-/Auslass d50 (DN40): Einlass oben x = L/2 - 60, Auslass seitlich unten z 70", "d50; z 70", "A", "Wasserweg: Zulauf oben, Ablauf unten (Schwerkraft); keine Quelle", "niedrig"],
    ["Montagelaschen 30 x 5 x 40 mit M6x16, 4 je Kassette (z 15 % und 85 % der Hoehe)", "M6x16; 30x5x40 mm", "A", "Befestigung an Montageflaeche; keine Quelle", "niedrig"],
    ["Werkstoffe: Tafel/Gehaeuse PP 0,91, Stahl 7,85, PVC-U 1,4, Pumpe Kunststoff 1,5, Siebeinsatz 0,05", "0,91 / 7,85 / 1,4 / 1,5 / 0,05 g/cm3", "Fachwert + A", "Handbuchwerte; Masse im Modell = Summe je Koerper nach Werkstoff (pumpe_klein 5,3 kg, pumpe_gross 8,5 kg, filtermodul 1,8 kg)", "mittel"],
    ["Farbe Pumpe #2a5da8, Tafel grau, Stutzen grau", "#2a5da8", "A", "Module in keiner Referenz sichtbar", "niedrig"],
    ["Port-Koordinaten (Saug-, Druckstutzen, Strom, Standwinkel, Ein-/Auslass, Laschen)", "siehe Ports", "E", "berechnet aus den Parametern (fix_pumpe_blatt.py), Ursprung = Mitte der Standflaeche", "mittel"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pumpe.json (2) gepflegt")
