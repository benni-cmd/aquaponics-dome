# Sammelblatt Leitungsteile-Bibliothek T70 (erzeugt von `scripts/workshop/fix_lt_blatt.py`, Dateien aus `scripts/workshop/leitung.py`, Pruefung `check_leitungsteile.py` 78/78)

**Funktion:** Normteile des Rohrnetzes als Komponenten mit Ports: Rohr, Kupplung (Doppelmuffe), Bogen 90/45 Grad, T-Stueck, Kugelhahn, Rohrklemme, Schlauch gerade und Bogen, Verteiler. Die Montage-Sitzung verlegt sie nach `data/system.json` (Wegfuehrung gehoert NICHT in diese Klasse). Dateien `designs/components/lt_<teil>_d<groesse>.sc` (49 Stueck).

**Scope-Card:** DRIN Geometrie und Ports je Teil, DN parametrisch, Biegeradius Schlauch >= 5 x AD, Farben nach `docs/hydraulics.md` 5; DRAUSSEN Verlegung, Anschlussreihenfolge, `routing surface/buried`.

## Konvention (Bauteil-Koordinatensystem)

Port A liegt im Ursprung (Rohr-/Schlauchachse +Z, bei Bogen/T in der XZ-Ebene). Alle Maße in mm. Ports (Name, DN, Lage, Richtung der Oeffnung):

| Teil | Port | Lage x, y, z | Richtung (Oeffnung) |
|---|---|---|---|
| Rohr (Laenge L, Standard 1000) | A | 0, 0, 0 | -Z |
| Rohr | B | 0, 0, L | +Z |
| Kupplung (L = 2 x Muffentiefe + 6) | A / B | 0, 0, 0 / 0, 0, L | -Z / +Z |
| Bogen 90 (Radius R, Schenkel = Muffentiefe t) | A | 0, 0, 0 | -Z |
| Bogen 90 | B | R + t, 0, t + R | +X |
| Bogen 45 | B | R(1 - cos 45) + t sin 45, 0, t + R sin 45 + t cos 45 | (sin 45, 0, cos 45) |
| T-Stueck (Arm a = t + OD_f/2) | A / B / C | -a, 0, 0 / +a, 0, 0 / 0, 0, +a | -X / +X / +Z |
| Kugelhahn (L = 50 + 2 t) | A / B | 0, 0, 0 / 0, 0, L | -Z / +Z; Hebel +X (offen = parallel zur Rohrachse) |
| Schlauch (ID16 / ID25, Standard 1000) | A / B | 0, 0, 0 / 0, 0, L | -Z / +Z |
| Schlauchbogen 90 (R = 5 x AD, Schenkel 100) | A / B | 0, 0, 0 / R, 0, 100 + R + 100 | -Z / +X |
| Rohrklemme (Aufnahme Rohr d) | Rohrachse | 0, 0, z = 4 + (d + 6)/2, Achse X | Rohr liegt entlang X; Fuss unten (Z = 0), 2 Schrauben M6x20 |
| Verteiler d32 (n = 2, 3, 4 Abgaenge d25, Teilung 120) | Sammler A / B | 0, 0, 0 / L, 0, 0 (L = 120 n + 120) | -X / +X |
| Verteiler | Abgang k | x_k = 60 + 60 + 120 (k - 1), 0, 66 | +Z |

DN-Naeherung: d25 = DN20, d32 = DN25, d40 = DN32, d50 = DN40, d63 = DN50, d110 = DN100 (PVC-U-Rohr d entspricht dem Nenndurchmesser um etwa eine Stufe kleiner).

## Masse und Gewichte je Groesse (PVC-U, Messung aus den .sc)

| d | DN | Wand | Muffentiefe t | Formstueck-Aussen | Bogenradius R | Rohr 1 m (kg) | Kupplung | Bogen 90 | Bogen 45 | T | Kugelhahn | Klemme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d25 | DN20 | 1.8 | 19 | 32.2 | 32 | 0.18 | 0.021 | 0.040 | 0.029 | 0.046 | 0.127 | 0.099 |
| d32 | DN25 | 1.8 | 22 | 39.6 | 40 | 0.24 | 0.031 | 0.064 | 0.045 | 0.071 | 0.156 | 0.109 |
| d40 | DN32 | 1.9 | 26 | 48.0 | 48 | 0.32 | 0.047 | 0.099 | 0.069 | 0.110 | 0.195 | 0.121 |
| d50 | DN40 | 2.4 | 31 | 58.5 | 60 | 0.50 | 0.072 | 0.158 | 0.111 | 0.177 | 0.258 | 0.143 |
| d63 | DN50 | 3.0 | 37.5 | 72.2 | 76 | 0.79 | 0.115 | 0.263 | 0.183 | 0.297 | 0.354 | 0.176 |
| d110 | DN100 | 5.2 | 61 | 121.5 | 132 | 2.40 | 0.389 | 0.964 | 0.661 | 1.130 | 0.858 | 0.298 |

Schlauch (Standard 1000 mm): ID16 / AD23, hellblau, 0.21 kg, Bogen 90 R = 115 (5 x AD) 0.082 kg; ID25 / AD32, dunkelblau, 0.31 kg, Bogen 90 R = 160 0.141 kg. Verteiler d32: n2 0.103 kg, n3 0.141 kg, n4 0.178 kg.

## Farben nach Funktion (docs/hydraulics.md 5)

Frischwasser hellblau (#7fc4ea, Schlauch ID16), Filterlinie dunkelblau (#2a5da8, Schlauch ID25, Kugelhahn), Ruecklauf grau (#8d9296, PVC-Rohre/Formstuecke, Standard), Luft schwarz oder gruen. Die Montage setzt die Farbe je Leitung per `appearance.assign` auf die Instanz; die Bibliothek liefert grau (Rohre/Formstuecke) und die Standardfarbe der Schlaeuche.

## Verbindungen und Befestigungen

- Rohr und Formstueck: Klebemuffe nach DIN EN 1452 (Muffentiefe t aus der Tabelle, Spiel 0), PVC-U-Kleber; Kugelhahn mit Klebemuffen (Verschraubung als Variante).
- Schlauch: Aufstecken auf Tuelle/Stutzen mit Schlauchschelle (nicht modelliert).
- Rohrklemme: 2 Schrauben M6x20 ISO 4017 in Duebel/Holz; Abstand der Klemmen 0,5-1 m (hydraulics.md 5).

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Rohrgroessen d25/32/40/50/63/110 | d25-d110 | OBJ + Bauteilblaetter | layout.json tanks fittings 30-56; Rinne d32, Tuelle ID16, Tankzulauf d50/d63, Beet Standrohr d25/Tropfrohr d20 (PE), Pumpe d32-d50; Scope-Card nennt DN 25/32/50/110 | mittel |
| Wandstaerke PVC-U PN10 (SDR 21): max(1,8; d/21) | 1,8 - 5,2 mm | A | DIN 8062/EN 1452 Naeherung ohne Tabelle; keine Quelle abgerufen | niedrig |
| Muffentiefe 19/22/26/31/37,5/61 | mm | A | EN 1452-3 Klebemuffen (aus dem Gedaechtnis gerundet, nicht abgerufen) | niedrig |
| Formstueckwand 3 + d/40, Aussen-D = d + 2 x Wand | mm | A | Praxis PVC-U-Formstuecke | niedrig |
| Bogenradius R = max(OD_f, 1,2 d) | mm | A | kompakte Klebebogen; keine Quelle | niedrig |
| Kugelhahn Gehaeuse 50 mm lang, Hebel 110 x d/5 | mm | A | Bauform; keine Quelle | niedrig |
| Schlauch ID16/ID25, Wand 3,5; Biegeradius 5 x AD | ID16 / ID25 | Bauteilblaetter + hydraulics.md 5 | Tuelle ID16 (Rinne), Tankzulauf/Pumpe; Biegeradius >= 5 x Schlauchdurchmesser | mittel |
| Schlauchfarben hellblau/dunkelblau | #7fc4ea / #2a5da8 | Bild + hydraulics.md 5 | ref-6: hellblaue Schlaeuche; Farbe nach Funktion | mittel |
| Rohrklemme: Ring 3 mm, Breite 20, Fuss 4 mm, 2 x M6x20 | M6 | A | Konstruktionspraxis (Klemmen alle 0,5-1 m laut hydraulics.md 5) | niedrig |
| Verteiler d32 mit n Abgaengen d25, Teilung 120 | n = 2-4 | A + Bauteilblatt Tisch | analog Zulaufverteiler des NFT-Tischs; Teilung Annahme | niedrig |
| Werkstoff PVC-U 1,4 g/cm3, Schlauch 1,0 | g/cm3 | Fachwert | Handbuchwerte | mittel |

## Montage (L4)

1. Teile nach der Leitungsliste der Montage zuschneiden (Rohr: Saege, entgraten) und trocken ausrichten.
2. Klebemuffen mit PVC-U-Reiniger anrauen, Kleber auftragen, bis Anschlag einschieben, 1/4 Drehung, Abbinden lassen.
3. Schlaeuche mit Schelle auf Tuellen/Stutzen; Rohrklemmen alle 0,5-1 m.
4. Dichtheitsprobe (Wasser), Kugelhaehne Hebelstellung pruefen.

**Werkzeug:** Rohrschneider/Saege, Entgrater, Kleber, Schluessel M6, Bohrer.

## Stueckliste (Mengen)

Bibliothek: 49 Definitionen = 6 Rohre, 6 Kupplungen, 12 Boegen (90/45), 6 T-Stuecke, 6 Kugelhaehne, 6 Klemmen je Groesse d25-d110, 4 Schlauchteile (ID16/25 gerade und Bogen), 3 Verteiler. Mengen je Anlage ergeben sich aus `data/system.json` (Montage, Graph); jede Instanz ist ein Verknuepfen der Definition (keine Einzelkoerper).

## Alternative lokale Fertigung

PVC-/PE-Rohre und Fittings aus dem Sanitaer-/Bewaesserungshandel; Schlaeuche als PVC-Gewebeschlauch (Gartenbedarf).

## Offene Fragen

- DN-Zuordnung, Wandstaerken und Muffentiefen sind Naeherungen ohne Normtabelle (keine Quelle abgerufen).
- Weitere Teile (Reduzierung, Winkel-T, Flansch, Rueckschlagventil, Schlauchschelle) fehlen; bei Bedarf der Montage nachbauen.
- Rohrlaengen: Standard 1000 mm; Montage setzt Laengen ueber den Parameter `laenge` (Generator `leitung.rohr(d, L)`).
- Verlegung/Weg und `routing surface|buried`: Montage (nicht Klasse).

## Renders

- `renders/components/leitungsteile/lt_bogen45_d50.png`
- `renders/components/leitungsteile/lt_bogen90_d50.png`
- `renders/components/leitungsteile/lt_klemme_d50.png`
- `renders/components/leitungsteile/lt_kugelhahn_d50.png`
- `renders/components/leitungsteile/lt_kupplung_d50.png`
- `renders/components/leitungsteile/lt_rohr_d50.png`
- `renders/components/leitungsteile/lt_schlauchbogen90_id16.png`
- `renders/components/leitungsteile/lt_t_d50.png`
- `renders/components/leitungsteile/lt_verteiler_d32_n3.png`

## Pruefung

- `scripts/workshop/check_leitungsteile.py` (Ergebnis `renders/components/leitungsteile/check.txt`): 49 Dateien, Aussen-D, Laenge, Volumen = Ringflaeche x Mittellinie (Pappus, Rohr/Bogen/Schlauchbogen), Baulaengen, Biegeradius, Verteiler-Abgaenge.
- Kein Bild-Kritiker: Normteile ohne Referenzbild; Spec-Pruefer und Orchestrator-Stichprobe.
