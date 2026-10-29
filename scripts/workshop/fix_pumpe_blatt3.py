"""Blatt pumpe nach Orchestrator-Entscheidung (29.10. ~08:55): Klasse filtermodul entfaellt, die 10 Kassetten 384x44x419 sind Stuetzrippen der Tankplattform (Klasse Tank); Pumpe bleibt (4 Pumpentafeln). Nach fix_pumpe_blatt.py und fix_pumpe_blatt2.py ausfuehren."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "pumpe.json")
d = json.load(open(p, encoding="utf-8"))
d["typen"].pop("filtermodul", None)
d["beschreibung"] = "Pumpenmodule an den Tanks: Montagetafel mit Kreiselpumpe, Konsole, Saug-/Druckstutzen, Kabel mit Stecker, Standwinkel; klein (502 x 5 x 345) und gross (693 x 7 x 463), je 2 je Tank"
d["quelle_masse"] = "data/layout.json tanks[].modules: klein 502 x 5 x 345 (2 je Tank), gross 693 x 7 x 463 (2 je Tank); Rolle Pumpentafel ist Annahme (docs/components.md); Pumpe aus Hydraulik-Konzept (docs/hydraulics.md)"
d["anzahl"] = {"soll": "Pumpenmodul klein 4, gross 4", "quelle": "data/layout.json tanks[].modules (Duplikate zusammengefasst)"}
for k in ("mat_clear", "lid_t", "wall"):
    d["parameter"].pop(k, None)
bl = d["blatt"]
bl["funktion"] = ("Pumpenmodul an den Tanks (Rolle ANNAHME): Montagetafel mit Kreiselpumpe fuer den Umlauf; Foerderstrom laut docs/hydraulics.md 2.3 [E]: kleiner Tank ca. 12 l/min, grosser ca. 30 l/min, statische Hoehe ca. 1,3 m plus Reibung. "
                  "ENTSCHEIDUNG Orchestrator 29.10.: Die 10 Kassetten 384 x 44 x 419 (layout.json tanks 2/3) sind KEINE Filtermodule, sondern Stuetzrippen/Konsolen der Tankplattform (Klasse Tank, Annahme A); die Klasse filtermodul entfaellt (Alternative Filterkassette: Entwurf entfernt).")
bl["querschnitt"] = "Montagetafel PP (502x5x345 bzw. 693x7x463) stehend auf zwei Standwinkeln; Konsole aus Winkel 5 mm mit Pumpensockel; Pumpe: Motor (D90 x 150 / D110 x 180) + Pumpenkopf (D110 x 70 / D130 x 80), Saugstutzen axial, Druckstutzen nach oben; Kabel mit Stecker."
bl["ports"] = [x for x in bl["ports"] if not x[0].startswith("filtermodul")]
bl["varianten"] = ["pumpe_klein", "pumpe_gross"]
bl["render_dirs"] = []
bl["stueckliste"] = [x for x in bl["stueckliste"] if not x.startswith("filtermodul") and "Filtermodul" not in x] + ["Module gesamt: Pumpenmodul klein 4, gross 4 (layout.json tanks[].modules; Duplikate zusammengefasst)"]
bl["pruefung"] = ["scripts/workshop/check_pumpe.py (Ergebnis renders/components/pumpe_klein/check.txt)", "Kein Bild-Kritiker: die Module sind in keiner Referenz sichtbar; Spec-Pruefer (FAIL -> behoben); Orchestrator-Entscheidung 29.10. zur Rolle"]
bl["verbindungen"] = [x for x in bl["verbindungen"] if "Filtermodul" not in x]
bl["montage"] = [x for x in bl["montage"] if not x.startswith("Filtermodul")]
bl["lokal"] = "Pumpe: handelsuebliche Kreiselpumpe (Teich-/Umwaelzpumpe) auf Montagebrett."
bl["abweichung"] = bl["abweichung"].replace("Kassetten 0/45/90/135 Grad versetzt; z0 Tafeln -6..3, Kassetten 249-256", "Tafeln z0 -6..3").replace("und 384 x 43/44 x 418/419", "").replace("Kassetten", "Tafeln")
bl["abweichung"] += " Die 384er-Kassetten sind Stuetzrippen der Tankplattform (Klasse Tank, Entscheidung Orchestrator 29.10.) und gehoeren nicht zu dieser Klasse."
bl["offen"] = ["Rolle der 502/693er-Tafeln als Pumpentafeln ist Annahme (OBJ liefert nur Boxen; Tafeln stehen tangential am Boden: alternativ Seitenbleche/Spritzschutz)", "Anzahl 4 Pumpenmodule (OBJ) gegen 4 Pumpen A/B + 2 Siebe (hydraulics.md 3): Siebe ohne Bauteil", "Pumpenfabrikat, Leistung (R07 pausiert); Foerderstrom 12 / 30 l/min nur [E]", "Schrauben der Pumpe auf dem Sockel (4 x M6), Standwinkel-Befestigung nicht modelliert", "Kabel gerade und 150 mm kurz modelliert (real 1,5-3 m); Elektrik/Zufuehrung: Schaltschrank-Klasse", "Kollision Pumpe/Tankkegel: Integrator pruefen"]
d["herkunft_tabelle"] = [r for r in d["herkunft_tabelle"] if not any(w in r[0] for w in ("Kassette", "Filter", "Ein-/Auslass", "Montagelaschen", "Siebeinsatz", "Port-Koordinaten"))]
for r in d["herkunft_tabelle"]:
    if r[0].startswith("Rolle"):
        r[0] = "Rolle: Tafel = Pumpenmodul (die 384er-Kassetten sind Stuetzrippen der Klasse Tank)"
        r[3] = "docs/components.md (Bedeutung Annahme), hydraulics.md (Pumpen); Orchestrator-Entscheidung 29.10. zu den Kassetten"
    if r[0].startswith("Anzahl 4 / 4 / 10"):
        r[0], r[1] = "Anzahl 4 / 4 (Pumpentafeln klein/gross)", "4 / 4"
    if r[0].startswith("Werkstoffe"):
        r[0] = "Werkstoffe: Tafel PP 0,91, Stahl 7,85, PVC-U 1,4, Pumpe Kunststoff 1,5"
        r[1] = "0,91 / 7,85 / 1,4 / 1,5 g/cm3"
        r[3] = "Handbuchwerte; Masse im Modell = Summe je Koerper nach Werkstoff (pumpe_klein 5,3 kg, pumpe_gross 8,5 kg)"
d["herkunft_tabelle"].append(["Port-Koordinaten (Saug-, Druckstutzen, Strom, Standwinkel)", "siehe Ports", "E", "berechnet aus den Parametern (fix_pumpe_blatt.py), Ursprung = Mitte der Standflaeche", "mittel"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pumpe.json (3) gepflegt")
