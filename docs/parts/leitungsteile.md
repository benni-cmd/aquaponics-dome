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
