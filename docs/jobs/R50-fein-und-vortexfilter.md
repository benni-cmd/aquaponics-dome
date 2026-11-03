# R50 — Fein- und Vortexfilter: Funktion, Kaufgeraete, Selbstbau

**Art:** Recherche und Rechnung, KEIN Bau, kein Modell-Umbau. Auftrag Ben 03.11.2026.

## Problem
Ben kann die beiden Filterarten (Feinfilter im Hauptstrom, Vortex/Absetzer im Teilstrom) nicht beurteilen, bevor der Subtank-Umbau M10-S2V (geparkt) freigegeben wird. Es ist unklar, was jeder Filter leistet, ob es kaufbare Standardgeraete gibt und ob Selbstbau super simpel waere.

## Intent
Ben soll Funktion und Kauf-Alternativen beider Filter beurteilen koennen; Standardgeraete bevorzugt, Selbstbau nur wenn super simpel; die Geraete sollen spaeter als Bauteile nachgebaut werden koennen.

## Goal
Ein Bericht `docs/research/R50-fein-und-vortexfilter.md` mit Antwort zuerst, Wirkprinzip und Bauarten beider Filter, Katalog mit mindestens drei realen Produkten je Art (Maße, Anschluesse, Durchsatz, Quelle), Selbstbau-Bewertung, Empfehlung je Art mit Folgen fuer D71/D75 und Modellier-Spezifikation je empfohlenem Geraet. Herkunftsmarken Q/E/A, Zwei-Quellen-Regel, Rechenskript `scripts/r50_rechnung.py`.

## Grenzen
Kein Umbau, `gen_dome.py`, `data/*`, Netzliste und Roadmap unveraendert; keine Kostenrechnung (D69). Kontextgrenzen nach `docs/arbeitsweise-sitzungen.md` Abschnitt 4.

## Stand (03.11.2026, Fachrecherche)
- **Fertig:** `docs/research/R50-fein-und-vortexfilter.md` (7 Abschnitte, Katalog 8 Feinfilter-Zeilen und 10 Vortex/Tank-Zeilen, Spezifikationen 6.1 bis 6.3) und `scripts/r50_rechnung.py`. Kein Bau, nichts an Modell, Netzliste, Roadmap geaendert.
- **Ergebnis:** Kein Kaufgeraet erfuellt beim Feinfilter 100 µm, 110 l/min im Schwerkraftzulauf (85 mm Reserve) und die Netz-Anschluesse zugleich. Trommelfilter (Entry 25 mit 120 µm und 160 mm Ueberstand, ATF-1 mit 60 µm, FIAP mit 100 µm) sind 3,8- bis 15,6-fach zu gross. Bogensiebe 300 µm, Beutelgehaeuse sind Druckbehaelter. Der Feinfilter hat nur Schutzfunktion (100 µm haelt 21 % der Masse). Vortex: Teich-Vortex ab 10 m³/h, im Teilstrom 0,75 m³/h nur Becken; Standardteil ist der Kegelboden-Tank (in Europa nicht gefunden), Einbauten selbst aus PVC.
- **Empfehlung:** Absetzer behalten (D71), Tank als Standard-Kegelboden-Tank; Siebkorb behalten und vereinfachen (auch im Subtank, D75), Rueckstausicherung ergaenzen; Trommelfilter nur als Option B mit Heber d90/d110.
- **Grenzen der Belege:** Pentair Radial Flow Settler und Oase-BioTec-Datenblatt nicht gelesen; Maße/Anschlusslage Entry 25 beim Hersteller offen; Heber-Aufweitung nur gerechnet, nicht gemessen; 130 g/Tag Feststofffracht des Auftrags in den gelesenen Dateien nur als TAN gefunden (gerechnet 200 bis 400 g/Tag je Linie).
- **Offen:** Entscheidung Ben (Siebkorb behalten oder Trommelfilter Option B; Standard-Kegelboden-Tank; Radial-Flow-Absetzer pruefen); Montage: Heber-Messung und Rueckstausicherung vor M10-S2V.
