# Sammelblatt Leitungsteile-Bibliothek T70 (erzeugt von `scripts/workshop/fix_lt_blatt.py`, Dateien aus `scripts/workshop/leitung.py`, Pruefung `check_leitungsteile.py` 231/231 PASS)

**Funktion:** Normteile des Rohrnetzes als Komponenten mit Ports: Rohr, Kupplung (Doppelmuffe), Bogen 90/45 Grad, T-Stueck, Kugelhahn, Rohrklemme, Schlauch gerade und Bogen, Reduziermuffe (7 Paarungen), Verteiler. Die Montage-Sitzung verlegt sie nach `data/system.json` (Wegfuehrung gehoert NICHT in diese Klasse). Dateien `designs/components/lt_<teil>_d<groesse>.sc` (63 Stueck: 7 Groessen d20-d110 x 7 Teile = 49, 7 Reduzierungen, 4 Schlauchteile, 3 Verteiler).

**Scope-Card:** DRIN Geometrie und Ports je Teil, Rohr-Aussen-d parametrisch (die Scope-Card schreibt 'DN 25/32/50/110' und meint d-Werte; erweitert um d20, d40, d63), Biegeradius Schlauch >= 5 x AD (ID16/AD20: 100 mm; ID25/AD29: 145 mm), Farben nach `docs/hydraulics.md` 5; DRAUSSEN Verlegung, Anschlussreihenfolge, `routing surface/buried`.

## Konvention (Bauteil-Koordinatensystem)

Alle Masse in mm. Regel: Port A liegt im Ursprung (Rohr-/Schlauchachse +Z, bei Bogen in der XZ-Ebene), AUSSER bei der **Rohrklemme** (einziger Port 'Rohrachse' liegt bei z = 4 + (d + 6)/2 auf der Achse X), beim **T-Stueck** (Ursprung = Kreuzungspunkt der Achsen, A bei -a) und bei den **Verteiler-Abgaengen** (Ursprung = Sammler-Anfang, Abgang k bei x = 120 k). Port-Art: **Muffe** = Klebemuffe, das Gegenrohr wird um die Einstecktiefe t (Spalte `Muffentiefe t` unten) bis zum Anschlag eingeschoben; **Zapfen** = glattes Rohrende (wird in eine Muffe gesteckt, Einstecktiefe t der Gegenmuffe); **Schlauchende** = Aufstecken auf Tuelle/Stutzen mit Schlauchschelle; **Aufnahme** = Klemme. Lage = Mittelpunkt der Oeffnungsebene, Richtung = nach aussen aus dem Teil. DN siehe Naeherung unten; bei der Reduziermuffe hat A (gross) und B (klein) je eigenen DN.

**Lagen als Formel** (Muffentiefe t, Formstueck-Aussen OD_f, Radius R aus der Groessentabelle):

| Teil | Port (Art) | Lage x, y, z | Richtung (Oeffnung) |
|---|---|---|---|
| Rohr (Laenge L, Standard 1000) | A, B (Zapfen) | 0, 0, 0 / 0, 0, L | -Z / +Z |
| Kupplung (L = 2 t + 6) | A, B (Muffe) | 0, 0, 0 / 0, 0, L | -Z / +Z |
| Reduziermuffe d_g auf d_k (L = t_g + t_k + 6) | A gross (Muffe d_g), B klein (Muffe d_k) | 0, 0, 0 / 0, 0, L | -Z / +Z |
| Bogen 90 (Radius R, Schenkel t) | A (Muffe) | 0, 0, 0 | -Z |
| Bogen 90 | B (Muffe) | R + t, 0, t + R | +X |
| Bogen 45 | B (Muffe) | R(1 - cos 45) + t sin 45, 0, t + R sin 45 + t cos 45 | (sin 45, 0, cos 45) |
| T-Stueck (Arm a = t + OD_f/2; Ursprung = Kreuzung) | A / B / C (Muffe) | -a, 0, 0 / +a, 0, 0 / 0, 0, +a | -X / +X / +Z |
| Kugelhahn (L = 50 + 2 t) | A / B (Muffe) | 0, 0, 0 / 0, 0, L | -Z / +Z; Hebel +X (offen = parallel zur Rohrachse) |
| Schlauch (ID16/AD20, ID25/AD29, Standard 1000) | A / B (Schlauchende) | 0, 0, 0 / 0, 0, L | -Z / +Z |
| Schlauchbogen 90 (R = 5 x AD: 100 bzw. 145; Schenkel 100) | A / B (Schlauchende) | 0, 0, 0 / R + 100, 0, 100 + R | -Z / +X |
| Rohrklemme (Aufnahme Rohr d) | Rohrachse (Aufnahme) | 0, 0, z = 4 + (d + 6)/2, Achse X | Rohr liegt entlang X; Fuss unten (Z = 0), 2 Schrauben M6x20 |
| Verteiler d32 (n = 2, 3, 4 Abgaenge d25, Teilung 120) | Sammler A / B (Zapfen DN25) | 0, 0, 0 / L, 0, 0 (L = 120 n + 120) | -X / +X |
| Verteiler | Abgang k (Zapfen DN20) | x_k = 120 k, 0, 66 | +Z |

**Beispielwerte (aus `leitung.ports()`, d32 bzw. repraesentative Teile)** — die Funktion ist die maschinenlesbare Quelle der Montage:

| Datei | Port | DN | Art | Lage x, y, z (mm) | Richtung |
|---|---|---|---|---|---|
| `lt_rohr_d32` | A | DN25 | Zapfen | 0.0, 0.0, 0.0 | 0.00, 0.00, -1.00 |
| `lt_rohr_d32` | B | DN25 | Zapfen | 0.0, 0.0, 1000.0 | 0.00, 0.00, 1.00 |
| `lt_kupplung_d32` | A | DN25 | Muffe | 0.0, 0.0, 0.0 | 0.00, 0.00, -1.00 |
| `lt_kupplung_d32` | B | DN25 | Muffe | 0.0, 0.0, 50.0 | 0.00, 0.00, 1.00 |
| `lt_bogen90_d32` | A | DN25 | Muffe | 0.0, 0.0, 0.0 | 0.00, 0.00, -1.00 |
| `lt_bogen90_d32` | B | DN25 | Muffe | 61.6, 0.0, 61.6 | 1.00, 0.00, 0.00 |
| `lt_bogen45_d32` | A | DN25 | Muffe | 0.0, 0.0, 0.0 | 0.00, 0.00, -1.00 |
| `lt_bogen45_d32` | B | DN25 | Muffe | 27.2, 0.0, 65.6 | 0.71, 0.00, 0.71 |
| `lt_t_d32` | A | DN25 | Muffe | -41.8, 0.0, 0.0 | -1.00, 0.00, 0.00 |
| `lt_t_d32` | B | DN25 | Muffe | 41.8, 0.0, 0.0 | 1.00, 0.00, 0.00 |
| `lt_t_d32` | C | DN25 | Muffe | 0.0, 0.0, 41.8 | 0.00, 0.00, 1.00 |
| `lt_kugelhahn_d32` | A | DN25 | Muffe | 0.0, 0.0, 0.0 | 0.00, 0.00, -1.00 |
| `lt_kugelhahn_d32` | B | DN25 | Muffe | 0.0, 0.0, 94.0 | 0.00, 0.00, 1.00 |
| `lt_klemme_d32` | Rohrachse | DN25 | Aufnahme | 0.0, 0.0, 23.0 | 1.00, 0.00, 0.00 |
| `lt_reduzierung_d40_d32` | A (gross) | DN32 | Muffe | 0.0, 0.0, 0.0 | 0.00, 0.00, -1.00 |
| `lt_reduzierung_d40_d32` | B (klein) | DN25 | Muffe | 0.0, 0.0, 54.0 | 0.00, 0.00, 1.00 |
| `lt_schlauch_id16` | A | ID16 | Schlauchende | 0.0, 0.0, 0.0 | 0.00, 0.00, -1.00 |
| `lt_schlauch_id16` | B | ID16 | Schlauchende | 0.0, 0.0, 1000.0 | 0.00, 0.00, 1.00 |
| `lt_schlauchbogen90_id16` | A | ID16 | Schlauchende | 0.0, 0.0, 0.0 | 0.00, 0.00, -1.00 |
| `lt_schlauchbogen90_id16` | B | ID16 | Schlauchende | 200.0, 0.0, 200.0 | 1.00, 0.00, 0.00 |
| `lt_verteiler_d32_n3` | A | DN25 | Zapfen | 0.0, 0.0, 0.0 | -1.00, 0.00, 0.00 |
| `lt_verteiler_d32_n3` | B | DN25 | Zapfen | 480.0, 0.0, 0.0 | 1.00, 0.00, 0.00 |
| `lt_verteiler_d32_n3` | Abgang 1 | DN20 | Zapfen | 120.0, 0.0, 66.0 | 0.00, 0.00, 1.00 |
| `lt_verteiler_d32_n3` | Abgang 2 | DN20 | Zapfen | 240.0, 0.0, 66.0 | 0.00, 0.00, 1.00 |
| `lt_verteiler_d32_n3` | Abgang 3 | DN20 | Zapfen | 360.0, 0.0, 66.0 | 0.00, 0.00, 1.00 |

DN-Naeherung: d20 = DN15 (PE-Tropfrohr des Beets), d25 = DN20, d32 = DN25, d40 = DN32, d50 = DN40, d63 = DN50, d110 = DN100 (PVC-U-Rohr d entspricht dem Nenndurchmesser um etwa eine Stufe kleiner).

## Masse und Gewichte je Groesse (PVC-U, Messung aus den .sc)

| d | DN | Wand | Muffentiefe t | Formstueck-Aussen | Bogenradius R | Rohr 1 m (kg) | Kupplung | Bogen 90 | Bogen 45 | T | Kugelhahn | Klemme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d20 | DN15 | 1.8 | 16 | 27.0 | 27 | 0.14 | 0.015 | 0.027 | 0.019 | 0.031 | 0.108 | 0.122 |
| d25 | DN20 | 1.8 | 19 | 32.2 | 32 | 0.18 | 0.021 | 0.040 | 0.029 | 0.046 | 0.128 | 0.136 |
| d32 | DN25 | 1.8 | 22 | 39.6 | 40 | 0.24 | 0.031 | 0.064 | 0.045 | 0.071 | 0.158 | 0.156 |
| d40 | DN32 | 1.9 | 26 | 48.0 | 48 | 0.32 | 0.047 | 0.099 | 0.069 | 0.110 | 0.196 | 0.179 |
| d50 | DN40 | 2.4 | 31 | 58.5 | 60 | 0.50 | 0.072 | 0.158 | 0.111 | 0.177 | 0.259 | 0.208 |
| d63 | DN50 | 3.0 | 37.5 | 72.2 | 76 | 0.79 | 0.115 | 0.263 | 0.183 | 0.297 | 0.355 | 0.245 |
| d110 | DN100 | 5.2 | 61 | 121.5 | 132 | 2.40 | 0.389 | 0.964 | 0.661 | 1.130 | 0.860 | 0.380 |

**Reduziermuffen** (Doppelmuffe, grosse Muffe an Port A, kleine an Port B; Aussen-D = Formstueck der grossen Seite):

| d_gross / d_klein | DN | Muffentiefe t_g / t_k | Baulaenge L | Aussen-D | Masse (kg) |
|---|---|---|---|---|---|
| d110 / d63 | DN100 / DN50 | 61 / 37.5 | 104.5 | 121.5 | 0.699 |
| d63 / d50 | DN50 / DN40 | 37.5 / 31 | 74.5 | 72.2 | 0.164 |
| d50 / d40 | DN40 / DN32 | 31 / 26 | 63.0 | 58.5 | 0.097 |
| d50 / d32 | DN40 / DN25 | 31 / 22 | 59.0 | 58.5 | 0.107 |
| d40 / d32 | DN32 / DN25 | 26 / 22 | 54.0 | 48.0 | 0.061 |
| d32 / d25 | DN25 / DN20 | 22 / 19 | 47.0 | 39.6 | 0.040 |
| d25 / d20 | DN20 / DN15 | 19 / 16 | 41.0 | 32.2 | 0.025 |

Schlauch (Standard 1000 mm, Wand 2 [A]): ID16 / AD20, hellblau, 0.11 kg, Bogen 90 R = 100 (5 x AD) 0.040 kg; ID25 / AD29, dunkelblau, 0.17 kg, Bogen 90 R = 145 0.073 kg. Der Schlauch-AD 20 stimmt mit dem Tisch-Blatt ueberein (`docs/parts/nft_tisch.md`, `hose_od` = 20 fuer Schlauch ID16). Verteiler d32: n2 0.103 kg, n3 0.141 kg, n4 0.178 kg.

## Wasser je Meter (gefuellt) und Verbraucher

Fuellung mit Wasser 1 kg/l, Innen-D = d - 2 x Wand; Gewicht = Messung aus dem .sc plus Wasser:

| Teil | Innen-D (mm) | Wasser (l/m) | Leer (kg/m) | Gefuellt (kg/m) |
|---|---|---|---|---|
| Rohr d20 (DN15) | 16.4 | 0.211 | 0.14 | 0.36 |
| Rohr d25 (DN20) | 21.4 | 0.360 | 0.18 | 0.54 |
| Rohr d32 (DN25) | 28.4 | 0.633 | 0.24 | 0.87 |
| Rohr d40 (DN32) | 36.2 | 1.029 | 0.32 | 1.35 |
| Rohr d50 (DN40) | 45.2 | 1.605 | 0.50 | 2.11 |
| Rohr d63 (DN50) | 57.0 | 2.552 | 0.79 | 3.34 |
| Rohr d110 (DN100) | 99.6 | 7.791 | 2.40 | 10.19 |
| Schlauch ID16 / AD20 | 16 | 0.201 | 0.11 | 0.31 |
| Schlauch ID25 / AD29 | 25 | 0.491 | 0.17 | 0.66 |

**Verbraucher** (Hinweis fuer die Montage; verbindlich sind die Port-Tabellen der Klassenblaetter, diese Tabelle ist nur ein Wegweiser und kann veralten):

| Verbraucher | Anschluss | Bibliotheksteil | Quelle |
|---|---|---|---|
| NFT-Rinne | Zulauf Tuelle D16, Ablauf Stutzen d32 | Schlauch ID16 (Zulauf), Muffe d32 (Ablauf) | `docs/parts/nft_rinne.md` |
| NFT-Tisch | Zulaufverteiler d25 mit Stutzen D16 (eigenes Bauteil der Tisch-Klasse, Teilung 262-288), Sammelrohr d50 | Verteiler NICHT aus der Bibliothek (der Bibliotheks-Verteiler d32 hat Teilung 120 und Abgang d25); Zulaufschlauch ID16, Sammelrohr/Anschluss Rohr d50 | `docs/parts/nft_tisch.md` |
| Tank klein | Zulauf d50, Auslauf/Ueberlauf d50 (siehe Blatt), Schlammablass d40 + Kugelhahn, Leitrohr d110 (nur im Absetzer) | Rohr d50, Kugelhahn d40, Rohr d110 | `docs/parts/tank.md` |
| Tank gross | Zulauf d63, Auslauf d63 (siehe Blatt), Schlammablass d50 + Kugelhahn; KEIN Leitrohr im Biofilter; Belueftung d16 (Luftschlauch, nicht Bibliothek) | Rohr d63, Kugelhahn d50 | `docs/parts/tank.md` |
| Pumpe klein | Saug d40, Druck d32 | Rohr d40, Rohr d32 | `docs/parts/pumpe.md` |
| Pumpe gross | Saug d50, Druck d40 | Rohr d50, Rohr d40 | `docs/parts/pumpe.md` |
| IBC-Beet | Ablauf d25, Zulauf PE-Tropfrohr d20 | Rohr d25; d20-Teile der Bibliothek sind PVC-U-Platzhalter (Tropfrohr ist PE, Dichte 0,95: Gewicht d20 um etwa ein Drittel ueberschaetzt) | `docs/parts/ibc_beet.md` |

**Wandstaerken-Abweichung zu den Bauteilblaettern (gemessen am Blatttext):** die Bibliothek nutzt SDR 21 (d20 1,8 · d25 1,8 · d32 1,8 · d40 1,9 · d50 2,4 · d63 3,0 · d110 5,2 mm); die Klassenblaetter rechnen anders: Tank-Leitrohr d110 Wand 3 (`tank.md`, 2,2 mm weniger), Tank-Zu-/Ablauf d50/d63 Wand 3 (+0,6 / 0), Pumpe klein d40/d32 Wand 3 (+1,1 / +1,2), Pumpe gross d50/d40 Wand 3 (+0,6 / +1,1), NFT-Tisch Verteiler d25 und Sammelrohr d50 Wand 3 (+1,2 / +0,6), NFT-Rinne Ablaufstutzen d32 Wand 2 (+0,2), Beet-Standrohr d25 Wand 2 (+0,2), Beet-Tropfrohr d20 PE Wand 2 (+0,2). Beim Gewichtsvergleich der Montage zaehlt die Klassendatei; die Bibliothek ist die Normteil-Naeherung. Abgleich beim Orchestrator offen.

## Farben nach Funktion (docs/hydraulics.md 5)

Frischwasser hellblau (#7fc4ea, Schlauch ID16), Filterlinie dunkelblau (#2a5da8, Schlauch ID25, Kugelhahn), Ruecklauf grau (#8d9296, PVC-Rohre/Formstuecke, Standard), Luft schwarz oder gruen. Die Montage setzt die Farbe je Leitung per `appearance.assign` auf die Instanz; die Bibliothek liefert grau (Rohre/Formstuecke) und die Standardfarbe der Schlaeuche.

**Annahme [A], Entscheidung beim Orchestrator:** `docs/hydraulics.md` Abschnitt 5 faerbt nur nach Funktion (Frischwasser hellblau, Filterlinie dunkelblau) und ordnet keinen Schlauch-ID einer Funktion zu. Die Bibliothek nimmt ID16 = hellblau (ref-6: hellblaue Schlaeuche am Tischende) und ID25 = dunkelblau an; die Montage faerbt je Leitung per `appearance.assign` nach ihrer Funktion um.

## Verbindungen und Befestigungen

- Rohr und Formstueck: Klebemuffe nach DIN EN 1452 (Muffentiefe t aus der Tabelle, Spiel 0), PVC-U-Kleber; Kugelhahn mit Klebemuffen (Verschraubung als Variante).
- Schlauch: Aufstecken auf Tuelle/Stutzen mit Schlauchschelle (nicht modelliert).
- Rohrklemme: 2 Schrauben M6x20 ISO 4017 in Duebel/Holz; Abstand der Klemmen 0,5-1 m (hydraulics.md 5).

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Rohrgroessen d20/25/32/40/50/63/110 | d20-d110 | OBJ | layout.json tanks fittings 30-56 (Marke OBJ); zusaetzlich aus den Klassenblaettern (A dort): Rinne d32, Tuelle ID16, Tankzulauf d50/d63, Beet Standrohr d25 / Tropfrohr d20 (PE), Pumpe d32-d50; die Scope-Card schreibt 'DN 25/32/50/110' und meint damit d-Werte (Aussendurchmesser), nicht DN | mittel |
| Wandstaerke PVC-U SDR 21 (PN10 oder PN12,5 je nach Tabelle/Spannung): max(1,8; d/21) | 1,8 - 5,2 mm | A | EN 1452-2 Reihe SDR 21 aus dem Gedaechtnis; Normtabellen runden d110 auf 5,3, d63 auf 3,0; keine Quelle abgerufen | niedrig |
| Muffentiefe 16/19/22/26/31/37,5/61 | mm | A | EN 1452-3 Klebemuffen (aus dem Gedaechtnis gerundet, nicht abgerufen); d20 analog | niedrig |
| Formstueckwand 3 + d/40, Aussen-D = d + 2 x Wand | mm | A | Praxis PVC-U-Formstuecke | niedrig |
| Bogenradius R = max(OD_f, 1,2 d) | mm | A | kompakte Klebebogen; keine Quelle | niedrig |
| Kugelhahn Gehaeuse 50 mm lang, Hebel 110 x d/5 | mm | A | Bauform; keine Quelle | niedrig |
| Reduziermuffe: L = t_g + t_k + 6, Aussen-D der grossen Seite, 7 Paarungen (110/63, 63/50, 50/40, 50/32, 40/32, 32/25, 25/20) | mm | A | Paarungen aus den Uebergaengen Tank d63/d50, Pumpe d50/d40/d32, Rinne d32, Beet d25/d20; Muffentiefen aus der Tabelle | niedrig |
| Schlauch ID16/ID25, Wand 2 mm, AD20/AD29 | ID16/AD20, ID25/AD29 | A | AD20 gleich `hose_od` im Tisch-Blatt (ID16 ueber Tuelle D16); ID25 analog, Wand 2 geschaetzt | niedrig |
| Schlauch-Biegeradius 5 x AD (100 / 145) | mm | A | hydraulics.md 5 (abgeleitete Festlegung): 'Biegeradius mindestens fuenf Schlauchdurchmesser' | mittel |
| Schlauchfarben hellblau (ID16) / dunkelblau (ID25) | #7fc4ea / #2a5da8 | Bild | ref-6 (Ausschnitt Tischende; hydraulics.md 5 faerbt nur nach Funktion): hellblaue Schlaeuche am Tischende; Filterlinie dunkelblau laut hydraulics 5 — die Zuordnung ID16 = Frischwasser, ID25 = Filterlinie ist eine Annahme dieses Blatts, siehe Abschnitt Farben | mittel |
| Rohrklemme: Ring 3 mm, Breite 20, Fuss 4 mm, 2 x M6x20 | M6 | A | Konstruktionspraxis (Klemmen alle 0,5-1 m laut hydraulics.md 5) | niedrig |
| Verteiler d32 mit n Abgaengen d25, Teilung 120 | n = 2-4 | A | Bauteilblatt Tisch (`nft_tisch.md`) als Vorbild: analog Zulaufverteiler des NFT-Tischs; Teilung Annahme | niedrig |
| Kupplung: Mittelsteg 6 mm (L = 2 t + 6) | 6 mm | A | Anschlagsteg zwischen den Muffen; keine Quelle | niedrig |
| T-Stueck: Arm a = t + OD_f/2; Bogenschenkel = t | mm | E + A | Arm bis Muffenende, Schenkel gleich Muffentiefe; Bauform ohne Quelle | niedrig |
| Kugelhahn: Gehaeuse-Aussen-D = OD_f + 12, Spindel D14, Hebel PVC-U | mm | A | Bauform; Spindel/Hebel wie das Gehaeuse in Material 'hahn' (PVC-U, Dichte 1,4); der Generator-Kommentar 'Schweissverbindung' meint nur 3 mm Einschub Spindel/Hebel, keine Metallteile | niedrig |
| Verteiler: Abgang ragt 50 mm ueber den Sammler (Oberkante z = d/2 + 50 = 66) | mm | A | Zapfen zum Aufstecken/Verkleben; Bauform ohne Quelle | niedrig |
| Farbe Kugelhahn dunkelblau, Rohre/Formstuecke grau | #2a5da8 / #8d9296 | A | Hahn als Funktionsteil hervorgehoben; Ruecklauf grau laut hydraulics 5 | niedrig |
| d20 als PVC-U-Teil (Rohr, Kupplung, Reduzierung 25/20) | d20 | A | Beet-Tropfrohr ist PE (`ibc_beet.md`); die Bibliothek bildet nur die Geometrie ab, Werkstoff und Dichte (0,95) sind abweichend | niedrig |
| Schlauchbogen: gerade Schenkel 100 mm, Wand 2 mm (AD = ID + 4) | mm | A | Bauform; Schenkel fuer Tuelle/Schelle; keine Quelle | niedrig |
| Standardlaenge Rohr und Schlauch 1000 mm (Parameter `laenge`) | mm | A | Handelsueblich 1 m; die Montage setzt die Laenge je Leitung | niedrig |
| DN-Zuordnung d20=DN15, d25=DN20, d32=DN25, d40=DN32, d50=DN40, d63=DN50, d110=DN100 | DN | A | Rohr-d entspricht dem Nenndurchmesser etwa eine Stufe kleiner; Klassenblaetter nutzen dieselbe Zuordnung (Ausnahme tank.md d40 'DN30') | niedrig |
| Port-Art (Muffe/Zapfen/Schlauchende) und Einstecktiefe t | siehe Port-Tabelle | A | Klebemuffe nimmt Rohr bis Anschlag auf; t = Muffentiefe | niedrig |
| Dichte PVC-U 1,4 g/cm3, Schlauch/Wasser 1,0 g/cm3, Stahl 7,85 | g/cm3 | A | Handbuchwerte, keine Quelle abgerufen | niedrig |
| Wasser je Meter = pi/4 x Innen-D^2 | l/m | E | Formel; Innen-D = d - 2 x Wand (Rohr) bzw. ID (Schlauch) | hoch |

## Montage (L4)

1. Teile nach der Leitungsliste der Montage zuschneiden (Rohr: Saege, entgraten) und trocken ausrichten.
2. Klebemuffen mit PVC-U-Reiniger anrauen, Kleber auftragen, bis Anschlag einschieben, 1/4 Drehung, Abbinden lassen.
3. Schlaeuche mit Schelle auf Tuellen/Stutzen; Rohrklemmen alle 0,5-1 m.
4. Dichtheitsprobe (Wasser), Kugelhaehne Hebelstellung pruefen.

**Werkzeug:** Rohrschneider/Saege, Entgrater, Kleber, Schluessel M6, Bohrer.

## Stueckliste (Mengen)

Bibliothek: 63 Definitionen = je 7 Rohre, Kupplungen, T-Stuecke, Kugelhaehne, Klemmen (Groessen d20-d110), 14 Boegen (90/45), 7 Reduziermuffen, 4 Schlauchteile (ID16/25 gerade und Bogen), 3 Verteiler. Mengen je Anlage ergeben sich aus `data/system.json` (Montage, Graph); jede Instanz ist ein Verknuepfen der Definition (keine Einzelkoerper).

## Alternative lokale Fertigung

PVC-/PE-Rohre und Fittings aus dem Sanitaer-/Bewaesserungshandel; Schlaeuche als PVC-Gewebeschlauch (Gartenbedarf).

## Offene Fragen

- DN-Zuordnung, Wandstaerken und Muffentiefen sind Naeherungen ohne Normtabelle (keine Quelle abgerufen).
- Weitere Teile (Winkel-T, Flansch, Rueckschlagventil, Schlauchschelle) fehlen; bei Bedarf der Montage nachbauen.
- Wandstaerken der Klassenblaetter weichen von SDR 21 ab (Zahlen im Abschnitt Masse/Wasser); Abgleich beim Orchestrator.
- Zuordnung Schlauch-ID zu Funktion/Farbe fehlt in `hydraulics.md` 5 (Annahme dieses Blatts: ID16 hellblau, ID25 dunkelblau); Entscheidung beim Orchestrator.
- Scope-Card nennt 'Kupplungen als Normteil (`parts.insert`)': die Kupplung ist stattdessen selbst modelliert (Doppelmuffe mit parametrischem DN); ob `parts.insert` eine passende Klebemuffen-Familie hat, wurde nicht geprueft.
- Der Zulaufverteiler des NFT-Tischs (d25, Stutzen D16, Teilung 262-288) liegt bei der Tisch-Klasse; die Bibliothek hat keinen Verteiler d25 mit Abgang D16.
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

- `scripts/workshop/check_leitungsteile.py` (Ergebnis `renders/components/leitungsteile/check.txt`): 63 Dateien (Soll 63, davon 7 Reduzierungen, 4 Schlauchteile, 3 Verteiler), Aussen-D, Laenge, Volumen = Ringflaeche x Mittellinie (Pappus, Rohr/Bogen/Schlauchbogen), Baulaengen, Biegeradius, Verteiler-Abgaenge und alle Port-Stirnflaechen (231 Pruefungen).
- Kein Bild-Kritiker: Normteile ohne Referenzbild; Spec-Pruefer Runde 1 (FAIL, 5 Befunde), Runde 2 (FAIL knapp, 5 Befunde) und Runde 3 (PASS knapp, 4 kleine Befunde, hier eingearbeitet); Triage in `docs/workshop-log.md`; Orchestrator-Stichprobe steht aus.

## Pool-Anschluesse am Zentralpool (M10-S1b, Montage, Runde 62)

Ein eigenes Bauteilblatt fuer den Pool gibt es unter `docs/parts/` nicht; die Ports stehen deshalb hier. Sie entstehen im Pool-Bauteil `designs/components/pool_zentral.sc` (Build, `pool_ports()` / `pool_stutzen()` in `scripts/gen_dome.py`), nicht von Hand. Je Port ein Loch in Wand bzw. Bodenplatte (Aussen-d) und ein Rohrstueck `T5_Stutzen_<Name>` (eigener Koerper, Bohrung Innen-d, Farbe blau) von der Muendung bis zum offenen Ende; Wasser fliesst aus dem Pool nach aussen. Parameter `pool_sd_*`, `pool_bd_*`, `pool_ueberstand` in `data/params.json`. Koordinaten Modellrahmen (Pool-Mitte 0/0), mm, Z absolut = Netz-Z relativ + 400 (sock_h).

| Port | Netz | DN (Aussen-d / Wand) | Muendung innen x / y / z | offenes Ende x / y / z | Richtung | Kommentar |
|---|---|---|---|---|---|---|
| SA_Ost_A | K01 (Linie 1) | d63 / 3,0 | 1903,2 / 401,1 / 740 | 2196,8 / 462,9 / 740 | radial nach aussen, Az 11,9 | Seitenablauf Z 340 rel., zum Feinfilter Ost A (x 3925 / y 825) |
| SA_West_B | K17 (Linie 2) | d63 / 3,0 | -864,8 / -1742,2 / 740 | -998,2 / -2010,9 / 740 | radial nach aussen, Az -116,4 | Seitenablauf Z 340 rel., zum Feinfilter West B (x -1575 / y -3175) |
| BA_Mitte | K03 + K19 | d50 / 2,4 | 0 / 0 / -1305 | 0 / 0 / -1575 | senkrecht nach unten | ein gemeinsamer Bodenablauf in der Poolmitte; Teilung auf d40 zu Pumpe_klein_1 und _3 folgt in S2 |

- Ueberstand: Seitenstutzen 150 mm ueber der Aussenflaeche der Wand (Radius 2095, Ende bei Radius 2245), Bodenstutzen 150 mm unter der Unterseite der Bodenplatte (Z -1425, Ende -1575); die Muendungen schliessen buendig mit Innenwand bzw. Innenboden ab (kein Ueberstand ins Wasser).
- Azimute: aus der Lage der Feinfilter im Modellrahmen gerechnet (`atan2(ff_a_y, ff_a_x)` = 11,87 Grad, `atan2(ff_b_y, ff_b_x)` = -116,40 Grad), nicht aus den Plan-Rundwerten 12 / -116; Pool-Mitte ist 0/0 (D35).
- Hoehe Seitenablauf: Z 740 absolut (= 340 relativ); Wasserspiegel 915, Ueberdeckung der Achse 175 mm (Plan F2 [A]).
- Bodenablauf-Z: Innenboden des Modells liegt bei Z -1305 absolut = -1705 relativ, das Netz nennt -1685 (20 mm darueber); Modellwert gilt, Abweichung im Rahmen der Netz-Rundung (siehe Hoehenprobe in `scripts/check_leitungen.py`).
- Bodenstutzen reicht 150 mm in den Erdboden (`T13_Erde` ist unter dem Pool nicht ausgespart); der Graben dafuer entsteht mit der Unterflur-Verlegung in S2, nicht in S1b.
- Nicht Teil von S1b: Ringsammler-Einlaeufe (S4), Zweit- und Drittbecken-Ports, Rohre, Pumpentafeln, Feinfilter.

# Ergaenzung W36 (01.11.2026, Werkstatt A): Teile ausserhalb der 63er-Bibliothek

Auftrag `docs/jobs/W36-verteiler-d50.md`. Generator `scripts/workshop/leitung_w36.py` (nutzt die Helfer aus `leitung.py`, `leitung.ports()` fragt ihn per Fallback), Pruefung `scripts/workshop/check_lt_w36.py` (Ergebnis `renders/components/leitungsteile/check_w36.txt`), maschinenlesbar unter `w36_teile` in `data/components/leitungsteile.json`. Die 63er-Pruefung `check_leitungsteile.py` zaehlt die W36-Dateien nicht mit (Liste `leitung_w36.FILES`).

## Verteiler d50 `lt_verteiler_d50` (T70-V-50-4)

**Mini-Plan.** Problem: Beide Linien enden offen am Biofilter-Ueberlauf (K10/K26), ein Verteiler d50 fehlt, S3 ist blockiert. Intent: Hauptstrom 110 l/min auf Beete, NFT, Bypass und Messkreis verteilen. Goal: eine Komponente mit Muffe A fuer das Rohr d50 und vier Abgaengen, Ports im Bibliotheksformat, Check gruen, Interferenz 0. Bau: Verteilerkoerper als Formstueck (Aussen 58,5 wie ein T d50) statt blankes Rohr, damit der Abgang d50 nicht deckungsgleich auf einem Rohr d50 sitzt und die Muffe A das Rohr aufnimmt; Abgaenge als Zapfen d40/d32/d20/d50 mit 50 mm Ueberstand, Teilung 120 wie der Bibliotheks-Verteiler.

**Funktion:** Sammelrohr d50 am Ende der Hauptleitung einer Linie. Fliessrichtung +X; vom Einlauf aus Beete (grosser Strom zuerst), NFT, Messkreis, Bypass (zuletzt, Drossel am Abgang). Gilt fuer Linie 1 (Verteilerplatz) und Linie 2; bei Linie 2 bleibt Abgang 3 (Messkreis) unbenutzt.

| Merkmal | Wert |
|---|---|
| Sammler | d50 x 2,4 (SDR 21 der Bibliothek), Innen-D 45,2, Aussen-D Koerper 58,5, Laenge 490 |
| Einlauf A | Muffe d50, Tiefe 31 (Rohr `lt_rohr_d50` Port B steckt direkt hinein) |
| Ende B | geschlossen, integrierte Kappe 10 mm (kein Port) |
| Abgaenge | 4 Zapfen, Ueberstand 50 mm ueber dem Koerper, Oberkante z = 79,25, Teilung 120 |
| Werkstoff, Farbe | PVC-U (1,4 g/cm3), dunkelblau #2a5da8 (Filterlinie) |
| Masse | 556 440 mm3 = 0,779 kg leer [E aus Volumen]; Wasser ca. 1,0 l (Sammler 0,72 l + Abgangsbohrungen ca. 0,27 l), gefuellt ca. 1,8 kg [E] |

**Ports** (Bauteil-KS, mm; Ursprung = Mitte der Muffenoeffnung A, Sammler-Achse +X):

| Port | DN | Art | Lage x, y, z | Richtung | Netz-Kante | Soll (l/min) | v im Abgang |
|---|---|---|---|---|---|---|---|
| A (Einlauf) | DN40 (d50) | Muffe | 0, 0, 0 | -X | K10 / K26 | 110 | 1,14 m/s im Sammler |
| Abgang 1 Beete | DN32 (d40) | Zapfen | 75, 0, 79,25 | +Z | K11 / K27 | 54,5 | 0,88 |
| Abgang 2 NFT | DN25 (d32) | Zapfen | 195, 0, 79,25 | +Z | K12 / K28 | 38 | 1,00 |
| Abgang 3 Messkreis | DN15 (d20) | Zapfen | 315, 0, 79,25 | +Z | K35 (nur Linie 1) | 3 | 0,24 |
| Abgang 4 Bypass | DN40 (d50) | Zapfen | 435, 0, 79,25 | +Z | K13 / K29 | 14,5 (L1) / 17,5 (L2) | 0,15 |

Geschwindigkeiten gerechnet aus den Innendurchmessern der Bibliothek (Wand SDR 21); die Netzliste nennt 0,94 / 1,03 / 0,25 / 0,16 mit etwas anderen Innen-D. Sammler 1,14 m/s liegt unter der Grenze 1,5 m/s (Druckseite). Der Strom nimmt nach jedem Abgang ab; der Einlauf ist die Spitze.

**Kollisionsfreiheit (Abgaenge mit Muffen und Kugelhahn):** Teilung 120 laesst zwischen den Muffen (Aussen-D 48 / 39,6 / 27 / 58,5) 76 bis 87 mm Luft, zwischen den Kugelhahn-Gehaeusen (Aussen-D = Formstueck + 12, L = 50 + 2 t) 64 bis 75 mm, und der Hebel (offen, +X) bleibt 23 bis 34 mm vom Nachbargehaeuse entfernt. Die Hahnhoehe beginnt bei z = 79,25 ueber dem Zapfen (Muffe der Hahn-Gegenseite steckt auf dem Zapfen, Einstecktiefe t <= 31 < 50).

**Verbindungen:** Klebemuffe nach DIN EN 1452, PVC-U-Kleber; Abgaenge werden mit Kugelhahn bzw. Rohr in die Muffe der Gegenseite gesteckt (Zapfen = glattes Rohrende, wie die Bibliotheks-Verteiler). Abgang 3 bei Linie 2 oder bei abgesperrten Linien braucht Stopfen/Kappe (fehlt, siehe Offene Fragen).

**Herkunft:**

| Merkmal | Wert | Herkunft | Konfidenz |
|---|---|---|---|
| Sammler d50, Abgaenge d40/d32/d50/d20 | DN-Reihe des Netzes | `data/leitungsnetz.json` K10-K13, K35 (Python gelesen) | hoch |
| Wand, Muffentiefe, Formstueck-Aussen 58,5 | SDR 21 / EN 1452 gerundet | A, aus der Bibliothek | niedrig |
| Teilung 120, Ueberstand 50, Endkappe 10, Abgang 1 bei x = 75 | mm | A, wie Bibliotheks-Verteiler; x = 75 = 31 + 25 + 19 Luft zur Muffe A | niedrig |
| Reihenfolge Beete, NFT, Messkreis, Bypass | Gross zuerst, Bypass am Ende (Drossel) | A | niedrig |
| Ende B geschlossen | statt offenem Zapfen | A (spart ein Kappenteil; ein Totende ist hydraulisch ueblich) | niedrig |

**Montage (L4):** Rohr d50 des Biofilter-Ueberlaufs bis Anschlag in Muffe A kleben; je Abgang Kugelhahn bzw. Rohr in die Muffe stecken (Zapfen in Muffe); Hebel der Haehne so ausrichten, dass sie nicht auf Nachbarhaehne zeigen; Dichtheitsprobe. Verteiler waagerecht auf Rohrschellen/Konsole (Schelle fuer Rundrohr: `lt_klemme_d50`). Werkzeug: Saege, Entgrater, Kleber. Alternative lokale Fertigung: Handelsteile (T-Stuecke d50 plus Reduzierungen) zusammenkleben; das Bauteil ist eine Naeherung eines Sammlers aus T-Stuecken.

**Pruefung:** `check_lt_w36.py verteiler` 29/29 PASS: ein Koerper (Interferenz 0), Laenge, Aussen-D, Zapfenhoehe, je Abgang Zapfen- und Bohrungs-Zylinder, 5 Port-Stirnflaechen, Geschwindigkeit beider Linien, 9 Luft-Pruefungen, Volumen gegen unabhaengiges CSG-Raster (Abweichung 0,006 %).

**Bild:** `renders/components/leitungsteile/lt_verteiler_d50.png`.

**Offene Fragen:** (1) Stopfen/Kappe d20 und d50 fehlen in der Bibliothek (Linie 2 ohne Messkreis, Reserve): melden, nicht gebaut. (2) Abgang d40 (Beete) gegen Beet-Port d25: Klaerung in R45, hier unveraendert nach Netz. (3) Abstand der Haehne an Linie 1 (Verteilerplatz) gegen die Umgebung wird erst bei der Platzierung (S3) geprueft.

## Rohrschelle fuer Vierkant-Tischbein `lt_schelle_vk_d32`, `lt_schelle_vk_d63` (T70-SVK-32 / T70-SVK-63)

**Mini-Plan.** Problem: Die Bibliotheksklemme `lt_klemme_d*` ist eine Fuss-Klemme (Fuss mit 2 Schrauben M6 in Holz/Duebel) und sitzt nicht an einem Vierkantprofil; der NFT-Strang d32 (K12) und die Rohre d63 muessen aber an den Tischbeinen gehalten werden (Plan `m10-leitungen.md` Abschnitt 4 Regel 7: Befestigung nur an Tischbeinen, nie an Streben). Intent: Rohr d32 und d63 mit einer Standard-Rohrschelle am Rechteckrohr 40 x 40 x 3 befestigen (`nft_tisch.md`, `leg_w`). Goal: zwei Komponenten (d32, d63) mit Ports Rohrachse und Bein, Check gruen, Interferenz 0 gegen Bein und Rohr. Bau: zwei Halbschalen (Ring 3 mm, Breite 20, Teilungsebene durch die Rohrachse, Ohren mit Schrauben M6x16 und Mutter), die hintere Halbschale traegt einen Steg und eine Rueckenplatte 74 x 20 x 4; ein Spannband 20 x 3 (Spiel 0,5 mm) umfasst das Bein und zieht die Platte mit zwei Schrauben M6x16 an. Der Steg haelt die Platte 14 mm vom Rohr entfernt (Mutter 5,2 + Schraubenende 3,8 + Luft); eine erste Fassung mit 4 mm Abstand hatte Muttern im Rohr (Interferenz-Test 6 Treffer) und wurde verworfen.

**Funktion:** haelt ein waagerechtes Rohr (Achse X) im Abstand an einem senkrechten Bein (Achse Z). Ein Bein, ein Rohr je Schelle; Klemmabstand 0,5 bis 1 m (`hydraulics.md` 5). Befestigung nur an Tischbeinen, nie an Streben, Knoten, Haut oder Plane.

| Merkmal | d32 | d63 |
|---|---|---|
| Rohr-Aussen-d / DN | 32 / DN25 | 63 / DN50 |
| Ring (Aussenradius ro) | 19,0 | 34,5 |
| Ohren (z, Schraube M6x16) | +-26 | +-41,5 |
| Rueckenplatte | 74 x 20 x 4, Vorderseite 14 mm vor der Rohroberflaeche | gleich |
| Anlageflaeche am Bein, y | -34 | -49,5 |
| Beinachse, y | -54 | -69,5 |
| Spannband | 20 x 3, Innenweite 41 (Bein 40 + 2 x 0,5), Laschen 14, Schrauben x = +-30 | gleich |
| Masse (Stahl 7,85, Messung) | 270 g | 315 g |
| Normteile | 4 Schrauben M6x16 ISO 4017, 4 Muttern M6 | gleich |

**Ports** (Bauteil-KS, mm; Ursprung = Rohrachse, Rohr liegt entlang X, Bein senkrecht dahinter bei -Y):

| Port | DN | Art | Lage x, y, z | Richtung |
|---|---|---|---|---|
| Rohrachse | DN25 (d32) bzw. DN50 (d63) | Aufnahme | 0, 0, 0 | +X |
| Bein | Vierkant 40x40 | Aufnahme | 0, -54 (d32) bzw. -69,5 (d63), 0 | +Z (Beinachse) |

Montage: Port Bein auf die Beinachse des Tischs legen (Beinmitte = Mitte der Anlageflaeche + 20 mm in -Y), Port Rohrachse liegt dann 54 bzw. 69,5 mm vor der Beinmitte in +Y; Position entlang des Beins = Z der Schelle. Bei Beinen mit anderer Orientierung die Instanz um Z drehen (yaw).

**Verbindungen:** Halbschalen: 2 x M6x16 + Mutter (Kopf vorn, Mutter hinten). Platte am Bein: Spannband mit 2 x M6x16 + Mutter, Kopf auf der Bandlasche, Mutter vor der Platte; Anzugsmoment nach Schraubenklasse (ca. 8 Nm, [A]). Verzinkt wie die Tischbeine (`nft_tisch.md`: Stahl verzinkt, Farbe #aeb4b8).

**Herkunft:**

| Merkmal | Wert | Herkunft | Konfidenz |
|---|---|---|---|
| Beinprofil 40 x 40 x 3 | mm | `docs/parts/nft_tisch.md` (`leg_w` 40, `leg_wall` 3), Quelle dort [A] | mittel |
| Ring 3 mm, Breite 20, Ohren und Schrauben M6x16 | mm | A, wie `lt_klemme` (Ring 3, Breite 20, M6) | niedrig |
| Rueckenplatte 74 x 20 x 4, Steg 14, Spannband 20 x 3 mit Spiel 0,5 | mm | A, Konstruktionspraxis (Bandschelle am Vierkant); keine Fabrikat-Vorlage | niedrig |
| Standardmasse d32 und d63 | Rohr-d der Bibliothek | E | hoch |

**Montage (L4):** (1) Halbschale hinten am Bein anlegen, Spannband um das Bein legen, Laschen auf die Plattenrueckseite schrauben (2 x M6x16, Mutter vor der Platte). (2) Rohr einlegen, Halbschale vorn aufsetzen, 2 x M6x16 mit Mutter anziehen. (3) Abstand 0,5 bis 1 m einhalten; bei Rohr d63 nachkontrollieren, dass die Ohren (z +-41,5) nicht am Querholm des Tisches anliegen. Werkzeug: Schluessel SW10, Maulschluessel/Nuss. Alternative lokale Fertigung: Handelsschelle (Rohrschelle mit Gummieinlage, DIN 3016) plus Winkel und Bandschelle fuer Vierkant.

**Pruefung:** `check_lt_w36.py schelle` 30/30 PASS (beide Groessen): 11 Koerper (3 Blechteile + 8 Normteile), Aussenradius, Ohr, Ringbreite, Plattenbreite, Anlageflaeche, Bandspiel, Bandbreite, Rohrbohrung d, Port Bein (Anlageflaeche), Port Rohrachse (Bohrungsachse), Abstand Platte-Rohr >= 12, Interferenz 0 gegen Bein 40 x 40 und Rohr d (inspect.interference, 13 Koerper). Bild mit Bein und Rohr (durchsichtig): `renders/components/leitungsteile/lt_schelle_vk_d32.png`, `lt_schelle_vk_d63.png`.

**Offene Fragen:** (1) Bandschelle und Rohrschelle sind Bauformen ohne Fabrikat; Anzugsmoment [A]. (2) Kollision mit Winkelhalter T23, Querholm und Diagonalen am Tischbein wird erst bei der Platzierung (S3/S6) geprueft; die Schelle belegt z +-10 (Platte und Band) bzw. +-41,5 (Ohren d63) um ihre Mitte. (3) Beinprofil gilt fuer Mitte/aussen und innen (40 x 40); die Querholme 40 x 60 sind keine Aufnahme.

## Leerrohr DN50 und DN100 mit Bogen 90 und 45 Grad `lt_leerrohr_dn50/dn100`, `lt_leerrohr_bogen90_dn*`, `lt_leerrohr_bogen45_dn*` (T70-LR-*, T70-LRB90-*, T70-LRB45-*)

**Mini-Plan.** Problem: S6 verlegt Kabel unterflur vom Schaltschrank zu Ost- und West-Gruppe in Leerrohren (Plan Abschnitt 4 Regel 9); in der Bibliothek gibt es nur Wasserrohre mit Klebemuffen und kleinen Bogenradien. Intent: Kabelschutzrohre mit Kabel-Bogenradius als Normteil, damit die Montage Rohr, Bogen und Anschluss an Schaltschrank und Technikgruppe aus Teilen legt; 230-V- und Signalkabel getrennt (eigene Rohre oder >= 200 mm Abstand). Goal: sechs Dateien (2 Groessen x gerade, 90, 45) mit Ports, Check gruen. Bau: Kabelschutzrohr PVC-U glatt mit Steckmuffe: gerade Stange 3000 mm (Muffe an B, in der Laenge enthalten, Zapfen an A); Bogen mit Muffe an A und glattem Ende B, damit sich Zapfen-in-Muffe durch die ganze Kette fortsetzt (Rohr.A in Bogen.A, Bogen.B in die Muffe des naechsten Rohrs). Kein Sweep-Bauteil fuer Kabel (bleibt in S6).

| Merkmal | DN50 | DN100 |
|---|---|---|
| Aussen-d x Wand (PVC-U, Katalogwert [A]) | 50 x 1,8, innen 46,4 | 110 x 3,2 (EN 1401 SN4), innen 103,6 |
| Muffe (Aussen / Tiefe) | 56 / 40 | 123 / 64 |
| Stange | 3000 (Muffe eingerechnet), Parameter `laenge` fuer 1000/2000/5000 | gleich |
| Bogenradius R (Mittellinie), Schenkel = t + 20 | 300 (Schenkel 60) | 500 (Schenkel 84) |
| Masse Stange / Bogen 90 / Bogen 45 | 1,16 / 0,24 / 0,15 kg | 4,63 / 1,55 / 0,96 kg |
| Werkstoff, Farbe | PVC-U 1,4 g/cm3, orange #c9742a (Elektro) | gleich |
| Routing | `buried` (Z -100 bis -400 relativ) | gleich |

**Bogenradius:** 300 mm erlaubt Kabel bis etwa 20 mm Aussen-d (Mindestradius 15 x Kabel-d, NYY 5 x 6 mm2 ca. 17 mm), 500 mm bis etwa 33 mm (NYY 4 x 35 mm2); gilt fuer 230-V-Pumpenkabel. Die Signal-Trunks (4 Adern RS-485 + 2 Adern 24 V, Herstellerkabel) sind duenner und laufen in DN50.

**Ports** (Bauteil-KS, mm; Port A im Ursprung):

| Teil | Port | Art | Lage x, y, z | Richtung |
|---|---|---|---|---|
| Stange (DN50 / DN100) | A | Zapfen | 0, 0, 0 | -Z |
| | B | Muffe | 0, 0, 3000 | +Z |
| Bogen 90 DN50 | A / B | Muffe / Zapfen | 0, 0, 0 / 360, 0, 360 | -Z / +X |
| Bogen 45 DN50 | A / B | Muffe / Zapfen | 0, 0, 0 / 130,29, 0, 314,56 | -Z / (0,707, 0, 0,707) |
| Bogen 90 DN100 | A / B | Muffe / Zapfen | 0, 0, 0 / 584, 0, 584 | -Z / +X |
| Bogen 45 DN100 | A / B | Muffe / Zapfen | 0, 0, 0 / 205,84, 0, 496,95 | -Z / (0,707, 0, 0,707) |

Einstecktiefe: ein Zapfen wird bis zum Anschlag um die Muffentiefe (40 / 64 mm) in die Muffe geschoben (wie die Klebemuffen der Bibliothek, hier Steckmuffe mit Lippendichtung, nicht modelliert).

**Herkunft:**

| Merkmal | Wert | Herkunft | Konfidenz |
|---|---|---|---|
| AD 50 x 1,8 / 110 x 3,2, Muffe 56 / 123 x 40 / 64 | mm | A: Katalogwerte HT/KG-Rohr und Kabelschutzrohr aus dem Gedaechtnis gerundet, nicht abgerufen | niedrig |
| Stangenlaenge 3000 | mm | A: handelsueblich 1/2/3/5 m | niedrig |
| Bogenradius 300 / 500, Schenkel t + 20 | mm | A: Kabel-Mindestradius 15 x Kabel-d; Handelsbogen haben oft R 300 bis 1000 | niedrig |
| Zapfen A + Muffe B je Stange, Muffe A + Zapfen B je Bogen | | A: eine Muffe je Verbindung, durchgehende Kette | mittel |

**Montage (L4):** Stangen im Graben auslegen (Muffe in Verlegerichtung gegen Gefaelle nach oben), Zapfen entgraten, anfasen, Gleitmittel auftragen, bis zur Einstecktiefe in die Muffe schieben; Gefaelle 1 % zum Schacht, damit Kondenswasser ablaeuft; Zugdraht einziehen; Enden mit Kabeleinfuehrung oder Schaumdichtung schliessen. Werkzeug: Saege, Anfasgeraet, Gleitmittel, Wasserwaage. Alternative lokale Fertigung: gelbes oder oranges Kabelschutzrohr (Baumarkt, Elektrogrosshandel), Handelsboegen.

**Pruefung:** `check_lt_w36.py leerrohr` 36/36 PASS: Koerperzahl, Laenge, Muffen-Aussen-D, Volumen Stange gegen Ringflaeche x Laenge + Muffe (Abweichung 0,05 %), Bogen-Volumen per Pappus (0,01 %), Innen-D, Bogenradius, alle 12 Port-Stirnflaechen. Bilder: `renders/components/leitungsteile/lt_leerrohr_bogen90_dn100.png`, `lt_leerrohr_dn50.png`.

**Offene Fragen:** (1) Maße nur Katalog-Naeherung, keine abgerufene Norm. (2) Kabelzahl und -durchmesser je Rohr (230 V je Pumpe, Trunks) legt S6 fest; hier nur DN50 und DN100. (3) Fehlt fuer S6: Kabeleinfuehrung/Endverschluss, Schaltschrank-Einfuehrung, Zugschacht (Teil 4 liefert nur den Ventilschacht), Reduzierstueck DN100/DN50, T-Abzweig.

## Schacht mit Deckel fuer Kugelhahn d63 `lt_schacht_kugelhahn_d63` (T70-SCH-KH63)

**Mini-Plan.** Problem: Der Notbypass K56/K57 (Kugelhahn d63 im Normalbetrieb zu, nur im Stoerfall auf; `docs/loop-state.md` M10-S2b/S2c) liegt in der Tiefleitung bei Z -159 im Graben; ohne Schacht ist der Hahn nicht erreichbar. Intent: Hahn von oben bedienen und warten, ohne zu graben. Goal: ein Schacht mit Deckel als Komponente, in den Kugelhahn d63 der Bibliothek (L = 125, Gehaeuse 84,15, Spindel + Hebel) und das Rohr d63 passen, Hebel in beiden Stellungen frei, Interferenz 0. Bau: Wanne PE-HD, Innen 400 x 400 (Hebel 110 + je 100 Hand, Ellbogenraum), Wand 8, Boden 15, Rohrachse 160 mm unter der Erdoberflaeche (K56 liegt bei Z -159), 150 mm Raum unter der Achse, zwei Wanddurchfuehrungen d70 mit EPDM-Dichtung fuer Rohr d63, Deckel 420 x 420 x 30 mit zwei Griffmulden, Deckelunterkante 47 mm ueber der Hebeloberkante.

| Merkmal | Wert |
|---|---|
| Wanne | PE-HD (0,95 g/cm3), Aussen 416 x 416, Hoehe 295 (z -165 bis 130), Innen 400 x 400 x 280, Wand 8, Boden 15 |
| Deckel | 420 x 420 x 30 (z 130 bis 160), 2 Griffmulden 100 x 30 x 15, liegt auf der Wand, Oberkante = Erdoberflaeche |
| Dichtung | 2 x EPDM-Manschette Aussen 70, Bohrung 63, Laenge 14 (ragt 3 mm innen und aussen) |
| Masse | Wanne 5,88 kg, Deckel 4,94 kg, Dichtungen 2 x 0,011 kg, gesamt 10,84 kg [E aus Volumen] |
| Hahn im Schacht | Hahnmitte im Ursprung, Rohrachse X, Spindel nach +Z; Hebeloberkante z = 83,1, Gehaeuseunterkante z = -42,1, Boden z = -150 |

**Ports** (Bauteil-KS, mm; Ursprung = Rohrachse in der Schachtmitte):

| Port | DN | Art | Lage x, y, z | Richtung |
|---|---|---|---|---|
| Durchfuehrung A | DN50 (d63) | Durchfuehrung (Dichtung) | -208, 0, 0 | -X |
| Durchfuehrung B | DN50 (d63) | Durchfuehrung (Dichtung) | +208, 0, 0 | +X |
| Deckel | 400 x 400 | Oeffnung / Erdoberflaeche | 0, 0, 160 | +Z |

Montage: Schachtmitte auf die Hahnposition der Tiefleitung legen, Rohrachse = Achse X (Instanz um Z drehen, bis die Leitung durch beide Durchfuehrungen laeuft); der Hahn aus der Bibliothek (`lt_kugelhahn_d63`) wird so gedreht, dass seine Spindel (Bauteil +X) nach oben zeigt, Hahnachse (Bauteil Z) = Rohrachse, Hahnmitte im Schachtmittelpunkt (Hahnursprung A liegt dann 62,5 mm vor der Mitte). Hebel offen = laengs zum Rohr, zu = quer; beide Stellungen frei.

**Befund fuer die Montage (K57/K56 unter dem Filterkasten):** Die Tiefleitung K57 liegt bei Z -159, die Filterkasten-Unterkante bei Z -96 (31 mm Luft, `loop-state.md` M10-S2c Befund 2). Ein Schacht mit Deckel an der Erdoberflaeche (Z 0 bis 1) kann nicht unter dem Filterkasten stehen, er wuerde den Kasten durchstossen. Der Hahn muss ausserhalb des Kasten-Grundrisses sitzen; die Leitung ist dafuer an eine Stelle neben dem Kasten zu fuehren (Schacht dort, Hahn im Schacht). Der Grundriss des Filterkastens wurde nicht gelesen; die Lage entscheidet S2b/S2c oder S6. Der Schacht selbst bleibt unveraendert und hat Platz fuer Hahn und Rohr d63.

**Herkunft:**

| Merkmal | Wert | Herkunft | Konfidenz |
|---|---|---|---|
| Hahn d63: L 125, Gehaeuse 84,15, Spindel, Hebel 110 x 12,6 x 14 bei x = 76,1 | mm | E aus `leitung.kugelhahn(63)` (Bibliothek, Bauform ohne Quelle) | niedrig |
| Rohrachse 160 unter Oberflaeche | mm | E aus K56 Z -159 (`loop-state.md`) | mittel |
| Innen 400 x 400, Wand 8, Boden 15, Deckel 30, 150 Raum unter der Achse | mm | A: Handbreite + Hebel 110, Standard-Ventilschacht (PE-HD, Handelsmasse nicht abgerufen) | niedrig |
| Werkstoffe PE-HD 0,95, EPDM 1,1 | g/cm3 | A: Handbuchwerte | niedrig |

**Montage (L4):** Graben ausheben (Sohle 40 cm unter der Achse, 10 cm Sandbett), Wanne einsetzen, waagerecht ausrichten; Rohr d63 durch die Dichtungen schieben, Hahn mit Klebemuffen ankleben; Wanne mit Sand/Kies verfuellen, Deckel bundig zur Erdoberflaeche auflegen. Nach dem Einbau Kugelhahn pruefen (Hebel parallel = offen). Werkzeug: Spaten, Wasserwaage, Kleber. Alternative lokale Fertigung: Handels-Schachtring oder Kontrollschacht Kunststoff DN400 mit Abdeckung; Wanddurchfuehrung per Kernbohrung oder Dichtmanschette.

**Pruefung:** `check_lt_w36.py schacht` 17/17 PASS: 4 Koerper, Aussenmasse, Wannen- und Deckelvolumen gegen Rechnung (0,0003 %), Deckel liegt auf der Wand, Oberkante = Erdoberflaeche, Durchfuehrung d70, Dichtungsbohrung d63, Ports, Luft Hebel-Deckel >= 30 (Ist 47), Oeffnung >= Hebel + 200, Platz unter dem Hahn >= 90 (Ist 108), Interferenz 0 gegen Rohr d63 und Kugelhahn d63 (Gehaeuse, Muffen, Spindel, Hebel) in beiden Hebelstellungen. Bild (Schnitt durch die Mitte, Deckel durchsichtig): `renders/components/leitungsteile/lt_schacht_kugelhahn_d63.png`.

**Offene Fragen:** (1) Lage des Schachts gegen den Filterkasten (Befund oben, Entscheidung bei der Montage/Orchestrator). (2) Entwaesserung des Schachts (Grundwasser, Sickerung) fehlt, keine Angabe zu Grundwasser im Plan [A]; Boden hat keine Ablaufbohrung. (3) Magnetventil statt Hand-Kugelhahn (K56: Hand-/Magnetventil) braucht ggf. Kabeldurchfuehrung; hier nur Handhahn. (4) Der Schacht ist auch fuer Hahn d50 (Tank gross, Schlammablass) nutzbar, aber nicht darauf ausgelegt.

## Pruefung Tropfrohr d20 je Beet und Schlauch ID16/AD20 je Rinne (W36 Teil 5, nur Bericht, kein Bau)

**Ergebnis in einem Satz:** Der Schlauch je Rinne reicht (bis auf eine kurze Laengenvariante und die Schelle), das Tropfrohr je Beet reicht nicht ganz: es fehlen ein direkter Uebergang d40 auf d20 und ein PE-PVC-Verbinder; dazu zwei kleinere Teile.

**Lastfall:** 14 Beete (`detail-standard.md` 5), je Linie 7 [A: gleichmaessig]; K11/K27 liefert 54,5 l/min, also 7,8 l/min = 467 l/h je Beet (Band R03 200 bis 500 l/h; Rohr d20 PE, innen 16, 0,62 m/s). NFT: 38 Rinnen je Linie, K12/K28 liefert 38 l/min; je Rinne 1 l/min laut Netzliste, aber 0,5 l/min laut `nft_tisch.md` (R06): bei 0,5 l/min waeren es nur 19 l/min. Der Widerspruch bleibt offen (Netzliste gegen Tisch-Blatt); beide Werte passen in Schlauch ID16 (0,08 m/s).

**Schlauch ID16/AD20 je Rinne:** `lt_schlauch_id16` (Port Schlauchende, Aufstecken auf Tuelle D16) und `lt_schlauchbogen90_id16` (R 100) decken den Zulauf ab; Zulaufverteiler d25 mit Stutzen D16 und Tuelle D16 gehoeren zur Tisch-Klasse. Luecken: (1) kurze Variante, der freie Schlauchabschnitt zwischen Stutzen und Tuelle ist 70 mm (`hose_gap`), mit Aufsteckenden ca. 100 mm; die Bibliotheksdatei ist 1000 lang, eine Variante `lt_schlauch_id16` mit `laenge` 100 (Generator `leitung.schlauch(16, 100)`) fehlt, 76 Stueck (38 je Linie, zwei Linien); (2) Schlauchschelle ID16 (nicht modelliert, laut Bibliothek: 2 je Schlauch = 152 Stueck als Stuecklistenzeile genuegen).

**Tropfrohr d20 je Beet:** Das gelochte Tropfrohr im Beet (Loch 4, Teilung 200, ab 150 mm, Endstopfen, Durchfuehrung D22 mit Tuelle) gehoert zur Beet-Klasse (`ibc_beet.md`). Anschluss davor aus der Bibliothek: T d40 (Beete-Strang), Kugelhahn d20 (Drossel je Beet), Rohr d20, Bogen d20. Fehlt: (1) Reduzierung direkt d40 auf d20 (oder Reduzier-T d40/d20): sonst Kette Reduziermuffe d40/d32 + d32/d25 + d25/d20, zusammen 142 mm Baulaenge und drei Klebestellen je Beet (14 Beete); (2) PE-PVC-Verbinder d20 (Klemm- oder Steckverbinder): das Tropfrohr ist PE (nicht klebbar), die Bibliotheksteile d20 sind PVC-U-Platzhalter (Gewicht um etwa ein Drittel zu hoch); (3) Stopfen/Kappe d20 und d50 (Messkreis-Abgang Linie 2, Reserveabgaenge); (4) Werkstoff-Variante PE d20 (Dichte 0,95, Wand 2) ueber den Parameter statt der PVC-U-Annahme.

**Liste fehlender Teile (Prioritaet):** 1. Reduzierung d40/d20 oder Reduzier-T (14 Beete). 2. PE-PVC-Verbinder d20 (14 Beete). 3. Schlauch ID16 kurz, 100 mm (76 Stueck). 4. Stopfen/Kappe d20, d50 (mindestens 1 je Linie 2 fuer den Messkreis-Abgang). 5. Schlauchschelle ID16 (152 Stueck, Stuecklistenzeile). Teil 4 (Schacht) und Teil 3 (Leerrohr) lieferten weitere Lueckenhinweise: Reduzierstueck DN100/DN50, Leerrohr-T, Kabeleinfuehrung. Keines davon wurde gebaut (Auftrag: nur melden).

## Rohrbibliothek d75 (W36 Teil 6, Entscheidung E14: Heber K01/K17 auf d75) `lt_rohr_d75`, `lt_kupplung_d75`, `lt_bogen90_d75`, `lt_bogen45_d75`, `lt_t_d75`, `lt_reduzierung_d75_d63`, `lt_reduzierung_d75_d50`

**Mini-Plan.** Problem: Ben hat E14 = d75 fuer die Heber K01/K17 entschieden (`R45-hydraulik-auslegung.md` Abschnitt 2); die Bibliothek hat nur d20 bis d110. Intent: Heberleitungen aus Normteilen d75 legen. Goal: sieben Komponenten mit Ports im Bibliotheksformat, gleiche Bauweise (`leitung.rohr/kupplung/bogen/t_stueck/reduzierung`, Aufruf mit d = 75), Check gruen. Mischtees der Montage (K05: d75 mit Abgang d50, K56: d75 mit Abgang d63) = T d75 plus Reduziermuffe, keine eigenen Teile; kein Kugelhahn und keine Klemme d75. d75 steht in `leitung.DEPTH` und `leitung.DN`, aber nicht in `SIZES`, damit der Aufruf der 63er-Bibliothek diese Dateien nicht neu schreibt.

| Merkmal | Wert | Herkunft |
|---|---|---|
| Rohr d75 x 3,6 (SDR 21), Innen 67,8, DN65 | `wall_p(75)` = max(1,8; 75/21) | E nach Auftrag (Rohr d75 x 3,6) |
| Muffentiefe t | 44 mm | A, zwischen d63 (37,5) und d110 (61) gerundet, Katalog offen (N-BESCHAFFUNG) |
| Formstueck-Aussen 84,75 (3 + d/40 Wand je Seite) | mm | A, nach der Formel der Bibliothek; Graben prueft damit |
| Bogenradius R | 90 = max(84,75; 1,2 d) | A |
| Rohr 1 m | 1,13 kg, 4,0 l/m Wasser (Innen 67,8 mm) | E aus Volumen |
| Kupplung L = 2 t + 6 = 94 | 0,168 kg | E |
| Bogen 90 / 45 | 0,393 / 0,272 kg | E |
| T-Stueck, Arm a = t + OD_f/2 = 86,4 | 0,449 kg | E |
| Reduziermuffe d75/d63, L = t_g + t_k + 6 | 87,5, 0,234 kg | E |
| Reduziermuffe d75/d50 | 81, 0,269 kg | E |

**Ports** (Konvention der Bibliothek): Rohr A, B (Zapfen DN65) bei z = 0 und 1000; Kupplung A, B (Muffe) bei z = 0 und 94; Bogen 90: B bei (134, 0, 134) Richtung +X; Bogen 45: B bei (57,5, 0, 138,8) Richtung (0,707, 0, 0,707); T: A (-86,4, 0, 0), B (+86,4, 0, 0), C (0, 0, 86,4) Muffe DN65; Reduzierungen: A (gross, Muffe DN65) bei z = 0, B (klein, Muffe DN50 bzw. DN40) bei z = 87,5 bzw. 81.

**Besonderheit:** (1) Die Formstuecke sind 84,75 mm dick (Rohr 75): fuer den Graben zaehlt dieser Wert, nicht d75. (2) Der Mischtee d75/d50 ist kein einzelnes Teil: T d75 (Arm 86,4) plus Reduziermuffe d75/d50 (L 81) macht den d50-Abgang rund 123 mm lang (86,4 - 44 + 81) bis zur Muffenoeffnung des d50-Rohrs; die Montage rechnet mit den Ports. (3) Muffentiefe 44 ist keine Norm-Angabe (d75 steht nicht in der urspruenglichen Tabelle). (4) Nach der Bibliotheks-Bauart ist der Bogenradius 90 nur etwas groesser als das Rohr d75; er ist klein fuer einen Heber (Verlustbeiwert hoeher als bei R >= 2 d); die Hydraulik bleibt bei R45.

**Pruefung:** `check_lt_w36.py d75` 36/36 PASS: Rohr Aussen-D, Laenge, Innen-D 67,8, Volumen, Kupplung, Bogen 90/45 (Pappus), T, beide Reduzierungen, je Teil ein Koerper (Interferenz 0), 20 Port-Stirnflaechen. Bild: `renders/components/leitungsteile/lt_t_d75.png`.

**Offene Fragen:** Katalogmasse d75 (Muffentiefe, Formstueck-Aussen) nach N-BESCHAFFUNG nachweisen; Bogen-Radius fuer Heber mit R45 abstimmen.

# Ergaenzung W39 (01.11.2026, Werkstatt A2): Kleinteile der Leitungsbibliothek

Auftrag `docs/jobs/W39-kleinteile.md`. Generator `scripts/workshop/leitung_w39.py` (nutzt die Helfer aus `leitung.py`; `leitung_w39.ports()` liefert die W39-Ports und fragt sonst `leitung.ports()`), Pruefung `scripts/workshop/check_lt_w39.py` (Ergebnis `renders/components/leitungsteile/check_w39.txt`), maschinenlesbar unter `w39_teile` in `data/components/leitungsteile.json`. Teilenummern T70 fortgefuehrt. Die 63er-Pruefung `check_leitungsteile.py` zaehlt die W39-Dateien nicht mit (Liste `leitung_w39.FILES`). Alle Handelsteil-Masse (Klemmverbinder, Schelle, Rueckschlagventil, Kabeleinfuehrung) sind Annahmen [A]: Katalog offen, Nachweis N-BESCHAFFUNG (L21).

## Reduzierung d40 auf d20 `lt_reduzierung_d40_d20` (T70-RED-40-20)

**Mini-Plan.** Problem: Jedes der 14 Beete braucht den Uebergang vom Beete-Strang d40 auf das Anschlussrohr d20; die Bibliothek hat nur die Kette 40/32, 32/25, 25/20 (142 mm, drei Teile, sechs Klebestellen je Beet). Intent: ein Handelsteil (Reduziermuffe 40/20) statt drei. Goal: eine Komponente mit Muffe A d40 und Muffe B d20, Baulaenge t40 + t20 + 6, Ports im Bibliotheksformat, Check gruen. Bau: `leitung.reduzierung(40, 20)` unveraendert, nur neue Datei; die Ports liefert die vorhandene Regel in `leitung.ports()`.

**Funktion:** Reduziermuffe fuer den Uebergang vom Beete-Strang (T d40 am Verteiler d50, Abgang 1 `lt_verteiler_d50`) auf das Anschlussrohr d20 je Beet (Kugelhahn d20 als Drossel, dann Uebergang PE-PVC, Teil 2). 14 Stueck (7 je Linie).

| Merkmal | Wert |
|---|---|
| Baulaenge | 48 mm = t40 (26) + t20 (16) + 6; Kette 40/32 + 32/25 + 25/20 = 54 + 47 + 41 = 142 mm, also 94 mm kuerzer |
| Aussen-D | 48 (Formstueck d40) |
| Muffe A / B | d40, Tiefe 26 / d20, Tiefe 16 |
| Durchgang | d16,4 (Wand 1,8 des Rohrs d20), 6 mm Steg zwischen den Muffen |
| Klebestellen je Beet | 2 statt 6 |
| Werkstoff, Masse | PVC-U 1,4 g/cm3, 67 g [E aus Volumen] |

**Ports** (Bauteil-KS, mm; Port A im Ursprung, Achse +Z; aus `leitung.ports()`, Regel `lt_reduzierung_d<g>_d<k>`):

| Port | DN | Art | Lage x, y, z | Richtung |
|---|---|---|---|---|
| A (gross) | DN32 (d40) | Muffe | 0, 0, 0 | -Z |
| B (klein) | DN15 (d20) | Muffe | 0, 0, 48 | +Z |

**Herkunft:**

| Merkmal | Wert | Herkunft | Konfidenz |
|---|---|---|---|
| Bauweise (Aussen = Formstueck der grossen Seite, Muffen, Durchgang) | | belegt: `leitung.reduzierung`, Bibliothek | mittel |
| Muffentiefen 26 / 16, Formstueck-Aussen 48 | mm | A, EN 1452-3 gerundet (Bibliothek) | niedrig |
| Baulaenge 48 | mm | E aus t40 + t20 + 6 | hoch |
| Handelsteil Reduziermuffe 40/20 | | im Katalog ueblich [A], Nachweis N-BESCHAFFUNG | niedrig |

**Montage (L4):** Rohr d20 und d40 bis Anschlag einkleben (Klebestelle je Seite). Werkzeug: Saege, Entgrater, Kleber. Alternative lokale Fertigung: die Kette aus drei Reduziermuffen (teurer, laenger, sechs Klebestellen).

**Pruefung:** `check_lt_w39.py red` 10/10 PASS: ein Koerper (Interferenz 0), Baulaenge 48, Aussen-D 48, kuerzer als die Kette, Portabstand, Volumen gegen Rechnung (0,002 %), beide Muffen-Zylinder, 2 Port-Stirnflaechen. **Bild:** `renders/components/leitungsteile/lt_reduzierung_d40_d20.png`.

**Offene Fragen:** Handelsteil im Katalog offen (N-BESCHAFFUNG); das Netz (`leitungsnetz.json`, R40) nennt je Beet d25/d20 am Beet-Port, die Montage entscheidet, ob d40/d20 direkt gesetzt wird.

## Uebergang PE-Rohr d20 auf Klebemuffe `lt_uebergang_pe_pvc_d20` (T70-UEB-PE20)

**Mini-Plan.** Problem: Das Tropfrohr im Beet ist PE und nicht klebbar, das Netz davor ist geklebtes PVC-U; ein Uebergang fehlt (14 Beete). Intent: ein Handelsteil Klemmverbinder PE-PVC (Mutter, Klemmring, Klebemuffe) statt eines Eigenbaus. Goal: eine Komponente mit Port A Klemme PE d20 (Einstecktiefe 30) und Port B Klebemuffe d20, Mutter und Klemmring sichtbar, Check gruen, Interferenz 0 gegen das eingesteckte PE-Rohr. Bau: drei Koerper: Koerper (Kragen 30, Gewindehals 24,6, Klebemuffe d20), Ueberwurfmutter 32 x 18 mit Gegenbohrung 25, Klemmring POM 24,8 x 5; Stueckliste aus Handelsteilen, keine Fabrikat-Angabe.

**Funktion:** Verbindet das PE-Tropfrohr d20 des Beets (nicht klebbar) mit dem geklebten PVC-U-Netz: PE-Rohr bis Anschlag (30 mm) einstecken, Ueberwurfmutter anziehen (Klemmring spannt), PVC-Rohr d20 in die Klebemuffe kleben. 14 Stueck (ein Uebergang je Beet).

| Merkmal | Wert |
|---|---|
| Baulaenge | 50 (Mutter z 0 bis 18, Kragen 18 bis 30, Klebemuffe bis 50) |
| Klemmseite | Mutter Aussen 32 x 18, Loch 20,4, Gegenbohrung 25; Gewindehals 24,6 (6 mm im Eingriff); Klemmring POM 24,8 x 5 (z 7 bis 12) |
| Aufnahme PE | d20, Einstecktiefe 30, Anschlag bei z = 30 |
| Klebemuffe B | d20, Tiefe 16, Aussen 27 (Formstueck d20), 4 mm Steg zum Anschlag |
| Durchgang | d16,4 |
| Werkstoff, Masse | PP (0,91) Koerper und Mutter, POM (1,41) Klemmring, 17,0 g [E aus Volumen] |

**Ports** (Bauteil-KS, mm; Port A im Ursprung, Achse +Z):

| Port | DN | Art | Lage x, y, z | Richtung |
|---|---|---|---|---|
| A | PE d20 | Klemme (PE-Rohr einstecken, Mutter anziehen) | 0, 0, 0 | -Z |
| B | DN15 (d20) | Muffe (Klebemuffe) | 0, 0, 50 | +Z |

**Herkunft:**

| Merkmal | Wert | Herkunft | Konfidenz |
|---|---|---|---|
| Bauform Klemmverbinder PE-PVC (Mutter, Klemmring, Klebemuffe) | | A, Handelsteil; kein Katalog gelesen, kein Fabrikat | niedrig |
| Einstecktiefe 30, Mutter 32 x 18, Kragen 30 x 12, Klemmring 24,8 x 5, Hals 24,6 | mm | A, Konstruktionspraxis | niedrig |
| Klebemuffe d20 (Tiefe 16, Aussen 27) | mm | E aus der Bibliothek (`leitung.DEPTH`, `od_f`) | mittel |
| Tropfrohr ist PE, nicht klebbar | | belegt: `docs/parts/leitungsteile.md` Pruefung W36 Teil 5 | hoch |

**Montage (L4):** PE-Rohr rechtwinklig abschneiden, entgraten, bis Anschlag (30 mm, Markierung) durch Mutter und Klemmring stecken, Mutter handfest anziehen; PVC-Rohr d20 in die Klebemuffe kleben (Klebstoff PVC-U). Werkzeug: Rohrschneider, Entgrater, Kleber. Alternative lokale Fertigung: Handelsverbinder "Klemmverbinder PE auf Klebemuffe" (Bewaesserungs-/Poolbedarf).

**Pruefung:** `check_lt_w39.py pe` 14/14 PASS: 3 Koerper, Baulaenge 50, Mutter-Aussen, Volumen je Koerper gegen Rechnung (0,01 %), Anschlag bei z = 30, Eingriff, Gegenbohrung gross genug, Klebemuffen-Zylinder, 2 Port-Stirnflaechen, Interferenz 0 (Koerper, Mutter, Klemmring und ein eingestecktes PE-Rohr d20). **Bild** (Schnitt XZ): `renders/components/leitungsteile/lt_uebergang_pe_pvc_d20.png`.

**Offene Fragen:** Handelsteil, Gewinde (hier nur Hals und Gegenbohrung, kein Gewindeprofil) und Fabrikat offen (N-BESCHAFFUNG); die Klemmverbindung fuer PE d20 gibt es auch als Steckverbinder (Push-Fit), Montage waehlt.

## Schlauch ID16 kurz `lt_schlauch_id16_L100` (T70-SCH-16, Laengenvariante)

**Mini-Plan.** Problem: Je NFT-Rinne liegt zwischen Verteilerstutzen und Tuelle nur ein freier Schlauchabschnitt von 70 mm (`hose_gap` im Tisch-Blatt); die Bibliotheksdatei `lt_schlauch_id16` ist 1000 mm lang (W36 Teil 5). Intent: 76 kurze Schlauchstuecke (38 Rinnen x 2 Linien) als eigenes Bauteil statt zugeschnittener 1000er. Goal: eine Komponente, Schlauch ID16/AD20, Laenge 100 (70 plus Aufsteckenden), Ports wie die Bibliothek, Check gruen. Bau: `leitung.schlauch(16, 100)` unveraendert; der 63er-Check ignoriert Laengenvarianten (Commit 80b61d3), Ports in `leitung_w39.ports()` (die Regel in `leitung.ports()` kennt nur `lt_schlauch_id<n>`).

**Funktion:** kurzes Schlauchstueck fuer den Zulauf je NFT-Rinne (Verteilerstutzen D16 bis Tuelle D16 der Rinne). 76 Stueck (38 Rinnen je Linie, zwei Linien). Die Datei `lt_schlauch_id16` (1000 mm) bleibt unveraendert.

| Merkmal | Wert |
|---|---|
| Innen / Aussen | 16 / 20 (Wand 2) |
| Laenge | 100 (freier Abschnitt 70 plus je 15 Aufsteckende) |
| Farbe | hellblau (Frischwasser, `hydraulics.md` 5) |
| Masse | 11,3 g [E aus Volumen, Dichte 1,0] |

**Ports** (Bauteil-KS, mm; Port A im Ursprung, Achse +Z): A Schlauchende ID16 bei 0, 0, 0 Richtung -Z; B Schlauchende ID16 bei 0, 0, 100 Richtung +Z.

**Herkunft:**

| Merkmal | Wert | Herkunft | Konfidenz |
|---|---|---|---|
| freier Abschnitt 70 | mm | belegt: Tisch-Blatt `hose_gap` (`docs/parts/nft_tisch.md`) | mittel |
| Aufsteckenden 2 x 15, Laenge 100 | mm | A | niedrig |
| Wand 2, ID16/AD20 | mm | Bibliothek (`leitung.schlauch`) | mittel |
| 76 Stueck | | E: 38 Rinnen x 2 Linien (Netzliste K12/K28) | mittel |

**Montage (L4):** beide Enden auf Tuelle D16 stecken, je eine Schlauchschelle (Teil 5). Werkzeug: Schlauchschere. **Pruefung:** `check_lt_w39.py hose` 7/7 PASS (Koerper, Laenge, AD, Volumen gegen Ringflaeche 0,008 %, Innenzylinder r 8, beide Port-Stirnflaechen). **Bild:** `renders/components/leitungsteile/lt_schlauch_id16_L100.png`. **Offene Fragen:** genaue Laenge entscheidet die Montage (Tuellenabstand je Rinne); kein Katalog offen, da zuschneidbarer Meterschlauch.

## Kappe d20 und d50 `lt_kappe_d20`, `lt_kappe_d50` (T70-KAP-20, T70-KAP-50)

**Mini-Plan.** Problem: Der Verteiler d50 hat am Messkreis-Abgang d20 (Linie 2 ohne Messkreis) und am Reserveabgang d50 offene Zapfen; die Bibliothek hat keine Kappe (W36 Teil 5). Intent: Abgaenge mit einem Normteil verschliessen. Goal: zwei Dateien mit einem Port Muffe (Richtung -Z), Boden 3 mm geschlossen, Aussen wie das Formstueck `od_f(d)`, Check gruen, Kappe steckt ohne Ueberlappung (ausser Einstecktiefe) auf dem Zapfen von `lt_verteiler_d50`. Bau: eine parametrische Funktion `kappe(d)`: Zylinder Aussen od_f(d), Hoehe Muffentiefe + 3, Muffe d von unten.

**Funktion:** Aufsteck-Kappe mit geschlossenem Boden; verschliesst einen Zapfen oder ein Rohrende (Klebemuffe). `kappe(d)` fuer d20 und d50. Bedarf laut Netz: d20 mindestens 1 je Linie 2 (Messkreis-Abgang 3 des Verteilers d50 bleibt unbenutzt), d50 fuer Reserveabgaenge; Stueckzahl entscheidet die Montage.

| Merkmal | d20 | d50 |
|---|---|---|
| Muffe (Tiefe) | d20 (16) | d50 (31) |
| Boden | 3 | 3 |
| Hoehe gesamt | 19 | 34 |
| Aussen-D (Formstueck od_f) | 27 | 58,5 |
| Masse (PVC-U 1,4) | 8,2 g | 42,7 g |

**Ports** (Bauteil-KS, mm; Oeffnung im Ursprung, Kappe waechst nach +Z): A (Muffe, DN15 bzw. DN40) bei 0, 0, 0, Richtung -Z. Sitz auf dem Zapfen: Kappenursprung = Zapfenoberkante minus Muffentiefe; am Verteiler d50 (Zapfenoberkante z = 79,25) also Kappe d20 bei z = 63,25 und Kappe d50 bei z = 48,25.

**Herkunft:** Bauweise SDR-21-Naeherung der Bibliothek (A, niedrig); Boden 3 mm Annahme; Aussen-D gerechnet `od_f(d)` (mittel); Handelsteil "Kappe/Stopfen" im Katalog ueblich, Nachweis N-BESCHAFFUNG.

**Montage (L4):** Zapfen entgraten, Kappe aufkleben bis Anschlag; ein verschlossener Abgang braucht keinen Kugelhahn. Werkzeug: Entgrater, Kleber.

**Pruefung:** `check_lt_w39.py kappe` 22/22 PASS: je Groesse Koerper, Hoehe, Aussen-D, Volumen (0,01 %), Boden geschlossen, Anschlag, Port, Interferenz 0 gegen Testzapfen; zusaetzlich fuer Abgang 3 (d20) und Abgang 4 (d50) des echten `lt_verteiler_d50`: Zapfen-Zylinder mit Radius = Muffenradius der Kappe und Zapfenoberkante z = 79,25 = Kappenursprung + Muffentiefe (Passung, nur Einstecktiefe ueberlappt). Ein Boolean-Interferenztest Kappe gegen den ganzen Verteiler scheitert in SolidCraft (114 s, "boolean Intersect: no result") und ist deshalb durch diese Mass-Pruefung ersetzt. **Bild:** `renders/components/leitungsteile/lt_kappe_d20.png`, `lt_kappe_d50.png`. **Offene Fragen:** Handelsteil Kappe oder Stopfen (Stopfen = innen steckend) im Katalog offen.
