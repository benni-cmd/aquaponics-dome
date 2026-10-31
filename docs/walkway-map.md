# Laufwegkarte (M10 Schritt 0, D54)

Erzeugt von `scripts/check_walkways_voll.py` aus `scripts/dome-script.json` (Raster 50 mm). Weite = 2 x Abstand zum naechsten Hindernis an der Grenze zweier Hindernisse (Voronoi-Kante). Rot < 500 mm, gelb 500-600 mm. Ort als Azimut (Modellrahmen, Grad) / Radius (mm).

## Scheibe knie (0.3 m ueber Boden)

### rot: 1 Engstellen

- Weite ca. 100 mm bei 162 Grad / 158 mm (Laenge ca. 179300 mm): Beet_aussen_800:1 x Beet_aussen_800:2 | Beet_aussen_800:1 x Beet_aussen_800:8

### gelb: 5 Engstellen

- Weite ca. 442 mm bei -87 Grad / 4457 mm (Laenge ca. 700 mm): Beet_aussen_800:4 x Zweitbecken
- Weite ca. 442 mm bei -70 Grad / 5472 mm (Laenge ca. 400 mm): Drittbecken x Wand
- Weite ca. 484 mm bei -39 Grad / 2772 mm (Laenge ca. 2300 mm): Puffer_Station:1 x Tank_klein:2 | Puffer_Station:1 x Tisch_innen:5
- Weite ca. 500 mm bei -88 Grad / 5452 mm (Laenge ca. 500 mm): Beet_aussen_800:4 x Wand
- Weite ca. 500 mm bei -71 Grad / 4712 mm (Laenge ca. 400 mm): Drittbecken x Zweitbecken

### Erreichbarkeit der Bauteile (Zelle mit >= 500 mm Gang <= 450 mm vom Grundriss)

- NICHT erreichbar: Tank_klein:1
- NICHT erreichbar: Tank_klein:2
- NICHT erreichbar: Tank_gross:1
- NICHT erreichbar: Tank_gross_t3:1
- NICHT erreichbar: Pumpe_klein:1
- NICHT erreichbar: Pumpe_klein:2
- NICHT erreichbar: Pumpe_klein:3
- NICHT erreichbar: Pumpe_klein:4
- NICHT erreichbar: Pumpe_gross:1
- NICHT erreichbar: Pumpe_gross:2
- NICHT erreichbar: Pumpe_gross:3
- NICHT erreichbar: Pumpe_gross:4
- NICHT erreichbar: Beet_aussen_800:1
- NICHT erreichbar: Beet_aussen_800:2
- NICHT erreichbar: Beet_aussen_800:3
- NICHT erreichbar: Beet_aussen_800:5
- NICHT erreichbar: Beet_aussen_800:6
- NICHT erreichbar: Beet_aussen_800:7
- NICHT erreichbar: Beet_aussen_800:8
- NICHT erreichbar: Beet_innen_933:1
- NICHT erreichbar: Beet_innen_933:2
- NICHT erreichbar: Beet_innen_933:3
- NICHT erreichbar: Beet_innen_933:4
- NICHT erreichbar: Beet_innen_933:5
- NICHT erreichbar: Beet_innen_933:6
- NICHT erreichbar: Tisch_innen:1
- NICHT erreichbar: Tisch_innen:2
- NICHT erreichbar: Tisch_innen:3
- NICHT erreichbar: Tisch_innen:4
- NICHT erreichbar: Tisch_innen:5
- NICHT erreichbar: Tisch_innen:6
- NICHT erreichbar: Tisch_innen:7
- NICHT erreichbar: Tisch_innen:8
- NICHT erreichbar: Tisch_innen:9
- NICHT erreichbar: Tisch_innen:10
- NICHT erreichbar: Puffer_Station:1
- NICHT erreichbar: Zentralpool
- erreichbar: Zweitbecken
- erreichbar: Drittbecken

## Zusammenfassung

- knie rot: 1 Engstellen
- knie gelb: 5 Engstellen

## Befund und Massnahmen (Montage, 31.10., Runde 53)

**Befund:** In der Kniescheibe ist der Innenraum von der Tuer aus mit 500-mm-Gang NICHT erreichbar: geflutet wird nur der Vorraum vor der Tuer. Selbst bei nur 300 mm Gang kommt man nicht bis zum Zentralpool. Die Tuerachse ist gesperrt, weil das Zweitbecken (D36) auf der Tuerachse steht (die alte Pruefung `check_walkways.py` zaehlte nur Beete/Portale und meldete den Tuer-Gang 2944 mm), rechts schliessen Puffer-Station (Luecke zum Zweitbecken ca. 100 mm) und Drittbecken (Luecke zur Wand 200 mm), links Tank 0/Pumpentafel (Luecke zum Zweitbecken ca. 100 mm; zum Aussenportal 442-484 mm). Kopfscheibe: 5 rote Engstellen, alle am Tuerzwickel (Station/Zweitbecken/Drittbecken/Wand). Alle Bauteile im Innenring (Tanks, Pumpen, Zentralpool) sind damit nicht erreichbar.
Rote 100-mm-Eintraege zwischen Portalen (Beet x Beet, Tisch x Tisch) sind Beruehrung der Rechtecke an den Ecken (Portal = Beet + 115 je Seite), kein Durchgang; zwischen Tank und seiner Pumpentafel Anbau (gleiche Baugruppe).

**Suche:** Simulated Annealing ueber Zweitbecken (r, az), Drittbecken (r, az) und Station (r, az) mit allen Luecken >= 500 mm (Wand 100), Tuergang 900 mm frei, Station Stapel r <= 4000: beste Loesung -126 mm (Ueberlappung), also KEINE Anordnung im Dom, in der Zweitbecken, Drittbecken, Puffer-Station, Tuergang 900 und 500-mm-Gaenge zugleich Platz haben (Bodenflaeche: Tuerkeil 72 Grad ca. 17 m2 gegen ca. 13 m2 Bauteile plus Gaenge).

**Massnahmen (Entscheidung noetig, Montage setzt nach Freigabe um):**
1. Zweitbecken von der Tuerachse nehmen (Tuergang >= 900 laut D29 gilt bis zum Zentralpool) oder die Tuerachse als Gang freihalten: Zweitbecken seitlich auf Azimut ca. -55 (r 3500) schieben; Folge: Station muss weichen.
2. Drittbecken und/oder Puffer-Station ausserhalb der Kuppel (Anbau/Technikvorbau an der Tuerseite) oder als Variante in die 4 freien Mittelring-Sektoren verlegen (dort stehen jetzt die 4 Tanks mit Pumpentafeln).
3. Tank-Abstand D22 (130-150 mm) und Pumpentafeln: Tanks 60-80 mm vom Aussenportal abruecken, damit 442-484 mm auf 500 kommt.
4. check_walkways.py um Zweitbecken/Drittbecken/Station/Tanks erweitern oder durch `check_walkways_voll.py` ersetzen (Hauptprueffall: Flutung von der Tuer).
