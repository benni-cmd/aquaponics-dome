# Sammelblatt Messstellen-Bauteile T90/T91 (erzeugt von `scripts/workshop/fix_w35_blatt.py` aus `scripts/workshop/messstellen.py`, `data/messstellen.json` und den gebauten Dateien, nicht von Hand aendern)

**Funktion:** Halter und Sonden-Platzhalter fuer die 67 Messstellen der Fachrecherche R39 (22 Pflicht, 45 Zusatz). Die Montage setzt sie an den Messstellen (`data/messstellen.json`: `halter`, `sonden`); jede Komponente hat Ports (Lage der Spitze im Bauteil-KS, Richtung), die Teile-Zeilen entsprechen 1:1 den Koerpern der Datei (Roadmap B1).

**Scope:** DRIN: 8 Halter (H_INLINE in zwei Groessen) = 9 Dateien `halter_*.sc`, 14 Sonden-Platzhalter `sonde_*.sc` (je ein Koerper). DRAUSSEN: Alarmwaehler, Spannungswaechter, Batteriemonitor (Schaltschrank, kein Bauteil), `hahn_probe` (= H_HAHN), Messrechner/Platinen, Kabelwege (M10).

**Herkunft-Kuerzel:** Q = aus gelesener Quelle (R39, `messstellen.json`), E = Handelsmass/Norm/eigene Rechnung, R = Rechenwert aus anderen Parametern, A = Annahme. **Alle Sondenmasse sind A:** `data/messstellen.json` enthaelt keine Abmessungen und die Hersteller-Datenblaetter sind nicht gelesen; Farbe nach vermuteter Hersteller-Erscheinung.

## Uebersicht

| Datei | Bauteil | Teilenummer | Koerper | Masse leer | Gesamt-Box (mm) | Stueck laut R39 |
|---|---|---|---|---|---|---|
| `halter_tauch.sc` | H_TAUCH Beckenrand-Tauchhalter | T90a | 3 | 1766 g | 242 x 52 x 1020 | 5 |
| `halter_beruhig.sc` | H_BERUHIG Beruhigungsrohr fuer Schwimmerschalter | T90b | 5 | 1173 g | 105 x 75 x 650 | 14 |
| `halter_zelle.sc` | H_ZELLE Durchflusszelle mit 3 Sondenstutzen | T90c | 4 | 490 g | 320 x 70 x 74 | 2 |
| `halter_inline_d32.sc` | H_INLINE d32 Einbaustueck Durchflussmesser d32 mit Vorfilter | T90d | 6 | 1392 g | 470 x 54 x 117 | 7 |
| `halter_inline_d50.sc` | H_INLINE d50 Einbaustueck Durchflussmesser d50 mit Vorfilter | T90e | 6 | 2196 g | 470 x 72 x 135 | 2 |
| `halter_hahn.sc` | H_HAHN Probenahmehahn | T90f | 3 | 141 g | 95 x 50 x 89 | 5 |
| `halter_druck.sc` | H_DRUCK Druckschalter-Stutzen R1/4 | T90g | 2 | 128 g | 60 x 50 x 67 | 6 |
| `halter_mast.sc` | H_MAST Sensor-Mast Kuppel | T90h | 3 | 936 g | 100 x 100 x 1736 | 5 |
| `halter_box.sc` | H_BOX Messknoten-Gehaeuse IP65 | T90i | 9 | 906 g | 260 x 150 x 116 | 7 |
| `sonde_do_ind.sc` | do_ind  | T91-do_ind | 1 | 133 g | 25 x 25 x 170 | 1 |
| `sonde_do_mini.sc` | do_mini  | T91-do_mini | 1 | 20 g | 12 x 12 x 110 | 5 |
| `sonde_ph.sc` | ph  | T91-ph | 1 | 27 g | 12 x 12 x 150 | 5 |
| `sonde_ec.sc` | ec  | T91-ec | 1 | 27 g | 12 x 12 x 150 | 3 |
| `sonde_temp_ds.sc` | temp_ds  | T91-temp_ds | 1 | 11 g | 6 x 6 x 50 | 6 |
| `sonde_level_float.sc` | level_float  | T91-level_float | 1 | 23 g | 30 x 30 x 55 | 17 |
| `sonde_level_druck.sc` | level_druck  | T91-level_druck | 1 | 347 g | 20 x 20 x 140 | 2 |
| `sonde_flow_12.sc` | flow_12  | T91-flow_12 | 1 | 192 g | 50 x 40 x 80 | 7 |
| `sonde_flow_gross.sc` | flow_gross  | T91-flow_gross | 1 | 288 g | 100 x 60 x 40 | 2 |
| `sonde_druck_schalter.sc` | druck_schalter  | T91-druck_schalter | 1 | 349 g | 32 x 32 x 55 | 6 |
| `sonde_strom_ct.sc` | strom_ct  | T91-strom_ct | 1 | 17 g | 36 x 13 x 30 | 10 |
| `sonde_co2_scd41.sc` | co2_scd41  | T91-co2_scd41 | 1 | 8 g | 25 x 17 x 10 | 3 |
| `sonde_par.sc` | par  | T91-par | 1 | 42 g | 30 x 30 x 37 | 2 |
| `sonde_leck.sc` | leck  | T91-leck | 1 | 8 g | 50 x 20 x 6 | 3 |

Gesamt: 53 Halter und 72 Sonden (Summe Stueck x Masse leer: 58.8 kg); H_BOX = 7 Messknoten.

## Halter

### H_TAUCH Beckenrand-Tauchhalter (`halter_tauch.sc`, T90a)

**Funktion:** Rohr d40 mit Klemme am Beckenrand, 0,3-0,7 m Eintauchtiefe, Sonde ohne Werkzeug herausziehbar (R39 H_TAUCH, 5 Stueck)

**Bauteil-KS:** Z hoch; Ursprung = Mitte der unteren Rohrkante (Tauchende); +X zeigt vom Rohr ueber den Beckenrand. **Gesamt-Box:** X -26.0 bis 216.0, Y -26.0 bis 26.0, Z 0.0 bis 1020.0 mm. **Masse leer:** 1766 g. **Stueck:** 5 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `laenge` | 1000 | mm | [E] Rohrlaenge: Klemme bei 640 mm, Beckenrand Z 650 minus Spiegel 515 = 135 mm Freibord, Eintauchtiefe 505 mm (R39: 0,3-0,7 m) |
| `rohr_d` | 40 | mm | [E] Rohr PVC-U d40 (R39 H_TAUCH; Bibliothek T70) |
| `rohr_wall` | 1.9 | mm | [E] PVC-U SDR 21 (leitung.wall_p) |
| `bohr_d` | 10 | mm | [A] zwei Querbohrungen d10 am Tauchende (Wasserzutritt, Z 30 und 70) |
| `kappe_d` | 44 | mm | [A] Kappe PA schwarz |
| `kappe_h` | 20 | mm | [A] |
| `kabel_d` | 8 | mm | [A] Kabelbohrung d8 (Atlas-Kabel 1-3 m) |
| `schelle_z` | 640 | mm | [E] Unterkante Klemmarm = Beckenrand-Auflage (Rand Z 650: Eintauchtiefe 505) |
| `schelle_od` | 52 | mm | [A] Klemmring Stahl, Wand 6 |
| `schelle_h` | 20 | mm | [A] |
| `arm_len` | 190 | mm | [A] Arm ueber den Rand (Beckenwand 150 mm + 40 Luft) |
| `arm_w` | 30 | mm | [A] |
| `haken_h` | 80 | mm | [A] Haken aussen am Rand |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Tauchrohr` | PVC-U d40 x 1,9, 1000 lang, 2 Querbohrungen d10 | PVC grau | E | 318 g |
| 2 | `Kappe` | Kappe d44 x 20 mit Kabelbohrung d8 | PA schwarz | A | 34 g |
| 3 | `Klemme` | Klemmring d52 mit Arm 190 x 30 und Haken 80 (ein Stahlteil) | Stahl verzinkt | A | 1415 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Kabeldurchfuehrung (Kappe, Sonde haengt im Rohr d40) | Bohrung d8 | x 0, y 0, z 1020 | (0, 0, 1) | `Kappe` |
| Beckenrand-Anlage (Unterkante Klemmarm auf dem Rand) | Arm 30 breit, Haken 80 | x 126, y 0, z 640 | (0, 0, -1) | `Klemme` |

**Lebensmittel-/Wasserkontakt:** PVC-U-Rohr im Wasser (EN 1452, handelsueblich fuer Trinkwasser; Zulassung des Fabrikats pruefen [A]); Klemme (Stahl) ausserhalb des Wassers.

### H_BERUHIG Beruhigungsrohr fuer Schwimmerschalter (`halter_beruhig.sc`, T90b)

**Funktion:** PVC-U d63 senkrecht, geschlitzt, 2 Schwimmerschalter (Niedrig/Hoch) (R39 H_BERUHIG, 14 Stueck)

**Bauteil-KS:** Z hoch; Ursprung = Mitte der Rohrunterkante (Boden des Rohrs, Bodenkappe darunter); +X zur Wand. **Gesamt-Box:** X -37.5 bis 67.5, Y -37.5 bis 37.5, Z -20.0 bis 630.0 mm. **Masse leer:** 1173 g. **Stueck:** 14 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `laenge` | 600 | mm | [A] Rohrlaenge: zwei Schwimmer im Abstand bis 300 mm im geschlitzten Bereich |
| `rohr_d` | 63 | mm | [E] Rohr PVC-U d63 (R39) |
| `rohr_wall` | 3.0 | mm | [E] PVC-U SDR 21 |
| `schlitz_l` | 360 | mm | [A] Schlitzlaenge, mittig |
| `schlitz_w` | 8 | mm | [A] Schlitzbreite, 4 Schlitze (je 2 durch das Rohr) |
| `kappe_d` | 70 | mm | [A] Bodenkappe |
| `kappe_h` | 20 | mm | [A] |
| `dkappe_h` | 30 | mm | [A] Deckelkappe |
| `kabel_d` | 12 | mm | [A] 2 Kabelbohrungen d12 |
| `kabel_abst` | 24 | mm | [A] |
| `schelle_z1` | 100 | mm | [A] untere Rohrschelle |
| `schelle_z2` | 480 | mm | [A] obere Rohrschelle |
| `schelle_od` | 75 | mm | [A] Rohrschelle Stahl 6 mm Wand |
| `schelle_h` | 15 | mm | [A] |
| `ohr_len` | 30 | mm | [A] Befestigungsohr |
| `ohr_w` | 25 | mm | [A] |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Rohr` | PVC-U d63 x 3,0, 600 lang, 4 Schlitze 8 x 360 | PVC grau | E | 426 g |
| 2 | `Bodenkappe` | Kappe d70 x 20, geschlossen | PVC grau | A | 108 g |
| 3 | `Deckelkappe` | Kappe d70 x 30 mit 2 Kabelbohrungen d12 | PVC grau | A | 152 g |
| 4 | `Schelle_1` | Rohrschelle d75 x 15 mit Ohr (unten) | Stahl verzinkt | A | 244 g |
| 5 | `Schelle_2` | Rohrschelle d75 x 15 mit Ohr (oben) | Stahl verzinkt | A | 244 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Kabeldurchfuehrung 1 (Deckelkappe, Schwimmerkabel) | Bohrung d12 | x -12, y 0, z 630 | (0, 0, 1) | `Deckelkappe` |
| Kabeldurchfuehrung 2 (Deckelkappe, Schwimmerkabel) | Bohrung d12 | x 12, y 0, z 630 | (0, 0, 1) | `Deckelkappe` |
| Wandbefestigung 1 (Ohr der Rohrschelle) | Ohr 25 breit | x 67.5, y 0, z 107.5 | (1, 0, 0) | `Schelle_1` |
| Wandbefestigung 2 (Ohr der Rohrschelle) | Ohr 25 breit | x 67.5, y 0, z 487.5 | (1, 0, 0) | `Schelle_2` |

**Lebensmittel-/Wasserkontakt:** PVC-U im Wasser (wie H_TAUCH); Schelle ausserhalb.

### H_ZELLE Durchflusszelle mit 3 Sondenstutzen (`halter_zelle.sc`, T90c)

**Funktion:** Durchflusszelle am Abzweig d20 des Sammelrohrs mit 3 Sondenstutzen (pH, EC, Temperatur) und Absperrhahn (R39 H_ZELLE, 2 Stueck: MS40, MS41)

**Bauteil-KS:** X = Strommrichtung (Zulauf -X, Ablauf +X), Z hoch; Ursprung = Mitte der Zulaufseite des Zellkoerpers. **Gesamt-Box:** X -30.0 bis 290.0, Y -35.0 bis 35.0, Z -22.0 bis 52.0 mm. **Masse leer:** 490 g. **Stueck:** 2 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `laenge` | 220 | mm | [A] Zellkoerper PVC-Block 220 x 44 x 44 |
| `breite` | 44 | mm | [A] |
| `hoehe` | 44 | mm | [A] |
| `bohr_d` | 28 | mm | [A] Durchgangsbohrung d28 (Zellvolumen ca. 0,13 l) |
| `stutzen_x` | [40, 110, 180] | mm | [A] Lage der Sondenstutzen (pH, EC, Temperatur) |
| `stutzen_d` | 25 | mm | [E] Stutzen d25 wie die Sondenstutzen im Deckel der Messzelle (puffer_klein) |
| `stutzen_id` | 16 | mm | [A] Bohrung fuer Sonde mit Kabelverschraubung |
| `stutzen_h` | 30 | mm | [A] |
| `anschl_d` | 20 | mm | [E] Anschlussstutzen d20 (R39) |
| `anschl_id` | 14 | mm | [A] |
| `anschl_l` | 30 | mm | [A] |
| `hahn_l` | 40 | mm | [A] Absperrhahn Gehaeuse 40 x 28 x 28 |
| `hahn_b` | 28 | mm | [A] |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Zellkoerper` | PVC-Block 220 x 44 x 44, Bohrung d28, 3 Stutzen d25 mit Bohrung d16 | PVC grau | A | 436 g |
| 2 | `Anschluss_Zulauf` | Stutzen d20 x 30, ID 14 | PVC grau | E | 7 g |
| 3 | `Anschluss_Ablauf` | Stutzen d20 x 30, ID 14 | PVC grau | E | 7 g |
| 4 | `Absperrhahn` | Kugelhahn d20 (Block 40 x 28 x 28) mit Spindel und Hebel | PVC blau | E | 41 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Zulauf (Anschluss d20, Abzweig Sammelrohr) | Stutzen d20, ID 14 | x -30, y 0, z 0 | (-1, 0, 0) | `Anschluss_Zulauf` |
| Ablauf (hinter dem Absperrhahn) | Hahn d20, ID 14 | x 290, y 0, z 0 | (1, 0, 0) | `Absperrhahn` |
| Sondenstutzen 1 (pH) | d25, Bohrung 16 | x 40, y 0, z 52 | (0, 0, 1) | `Zellkoerper` |
| Sondenstutzen 2 (EC) | d25, Bohrung 16 | x 110, y 0, z 52 | (0, 0, 1) | `Zellkoerper` |
| Sondenstutzen 3 (Temperatur) | d25, Bohrung 16 | x 180, y 0, z 52 | (0, 0, 1) | `Zellkoerper` |

**Lebensmittel-/Wasserkontakt:** PVC-U/PVC-Armatur im Wasser; Zulassung des Fabrikats pruefen [A].

### H_INLINE d32 Einbaustueck Durchflussmesser d32 mit Vorfilter (`halter_inline_d32.sc`, T90d)

**Funktion:** Rohrstueck mit Verschraubung, 20 cm gerade Strecke vor dem Messer und Vorfilter >= 80 um (R39 H_INLINE, 9 Stueck: MS12/13, MS34-39, MS50), Groesse d32 (flow_12)

**Bauteil-KS:** X = Stroemungsrichtung (Zulauf -X), Z hoch; Ursprung = Achse an der Vorfilter-Eintrittsseite. **Gesamt-Box:** X -30.0 bis 440.0, Y -27.0 bis 27.0, Z -66.0 bis 51.0 mm. **Masse leer:** 1392 g. **Stueck:** 7 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `d` | 32 | mm | [E] Rohr-Aussendurchmesser PVC-U (R39 H_INLINE; flow_12 an d32, flow_gross an d50, K10/K26) |
| `wand` | 1.8 | mm | [E] PVC-U SDR 21 |
| `block` | 52 | mm | [A] Vierkantblock d + 20 (Messstueck und Vorfilter aus PVC-Block gebohrt) |
| `nut_l` | 30 | mm | [A] Verschraubung (Union) 30 lang, Aussen d + 22 |
| `filter_l` | 110 | mm | [A] Vorfilterblock |
| `strecke_l` | 200 | mm | [R] 20 cm gerade Strecke vor dem Messer (R39 H_INLINE: Herstellervorgabe Paddelrad) |
| `sensor_l` | 100 | mm | [A] Messblock mit Sensorsitz |
| `x_end` | 410 | mm | [R] Ende des Messblocks = filter_l + strecke_l + sensor_l |
| `kappe_d` | 36 | mm | [A] Filterkappe 0,7 x Block |
| `kappe_h` | 40 | mm | [A] Kappe unter dem Block; Sieb >= 80 um (R39) Edelstahlgewebe, Maschenweite nicht modelliert |
| `sitz_d` | 30 | mm | [A] Sensorsitz (Gewindestutzen fuer Atlas-Paddelrad 1/2 Zoll, Hersteller-Datenblatt nicht gelesen) |
| `sitz_id` | 22 | mm | [A] Bohrung Sensorsitz |
| `sitz_h` | 25 | mm | [A] |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Verschraubung_A` | Union d54 x 30 (Zulauf), Rohr d32 | PVC blau | A | 70 g |
| 2 | `Vorfilter` | Block 52 x 52 x 110 mit Filterkappe d36 x 40 | PVC grau | A | 337 g |
| 3 | `Sieb` | Siebkorb Edelstahl d26 x 30 (>= 80 um, Gewebe nicht modelliert) | Edelstahl | A | 42 g |
| 4 | `Beruhigungsstrecke` | Block 52 x 52 x 200, Bohrung = Rohr-ID (20 cm gerade Strecke) | PVC grau | R | 580 g |
| 5 | `Sensorblock` | Block 52 x 52 x 100 mit Sensorsitz d30 x 25 | PVC grau | A | 294 g |
| 6 | `Verschraubung_B` | Union d54 x 30 (Ablauf), Rohr d32 | PVC blau | A | 70 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Zulauf (Verschraubung, Rohr d32) | Rohr d32 | x -30, y 0, z 0 | (-1, 0, 0) | `Verschraubung_A` |
| Ablauf (Verschraubung, Rohr d32) | Rohr d32 | x 440, y 0, z 0 | (1, 0, 0) | `Verschraubung_B` |
| Sensorsitz (Paddelrad / Ultraschall, Bohrung d22) | d30 | x 360, y 0, z 51 | (0, 0, 1) | `Sensorblock` |
| Filterwechsel / Entleerung (Kappe unten) | Kappe d36 | x 55, y 0, z -66 | (0, 0, -1) | `Vorfilter` |

**Lebensmittel-/Wasserkontakt:** PVC-U-Bloecke, Union-Verschraubung PVC; Sieb Edelstahl; Zulassung des Fabrikats pruefen [A].

### H_INLINE d50 Einbaustueck Durchflussmesser d50 mit Vorfilter (`halter_inline_d50.sc`, T90e)

**Funktion:** wie H_INLINE d32, Groesse d50 fuer die Hauptleitungen K10/K26 (110 l/min, flow_gross)

**Bauteil-KS:** X = Stroemungsrichtung (Zulauf -X), Z hoch; Ursprung = Achse an der Vorfilter-Eintrittsseite. **Gesamt-Box:** X -30.0 bis 440.0, Y -36.0 bis 36.0, Z -75.0 bis 60.0 mm. **Masse leer:** 2196 g. **Stueck:** 2 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `d` | 50 | mm | [E] Rohr-Aussendurchmesser PVC-U (R39 H_INLINE; flow_12 an d32, flow_gross an d50, K10/K26) |
| `wand` | 2.4 | mm | [E] PVC-U SDR 21 |
| `block` | 70 | mm | [A] Vierkantblock d + 20 (Messstueck und Vorfilter aus PVC-Block gebohrt) |
| `nut_l` | 30 | mm | [A] Verschraubung (Union) 30 lang, Aussen d + 22 |
| `filter_l` | 110 | mm | [A] Vorfilterblock |
| `strecke_l` | 200 | mm | [R] 20 cm gerade Strecke vor dem Messer (R39 H_INLINE: Herstellervorgabe Paddelrad) |
| `sensor_l` | 100 | mm | [A] Messblock mit Sensorsitz |
| `x_end` | 410 | mm | [R] Ende des Messblocks = filter_l + strecke_l + sensor_l |
| `kappe_d` | 49 | mm | [A] Filterkappe 0,7 x Block |
| `kappe_h` | 40 | mm | [A] Kappe unter dem Block; Sieb >= 80 um (R39) Edelstahlgewebe, Maschenweite nicht modelliert |
| `sitz_d` | 30 | mm | [A] Sensorsitz (Gewindestutzen fuer Atlas-Paddelrad 1/2 Zoll, Hersteller-Datenblatt nicht gelesen) |
| `sitz_id` | 22 | mm | [A] Bohrung Sensorsitz |
| `sitz_h` | 25 | mm | [A] |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Verschraubung_A` | Union d72 x 30 (Zulauf), Rohr d50 | PVC blau | A | 104 g |
| 2 | `Vorfilter` | Block 70 x 70 x 110 mit Filterkappe d49 x 40 | PVC grau | A | 530 g |
| 3 | `Sieb` | Siebkorb Edelstahl d39 x 30 (>= 80 um, Gewebe nicht modelliert) | Edelstahl | A | 70 g |
| 4 | `Beruhigungsstrecke` | Block 70 x 70 x 200, Bohrung = Rohr-ID (20 cm gerade Strecke) | PVC grau | R | 923 g |
| 5 | `Sensorblock` | Block 70 x 70 x 100 mit Sensorsitz d30 x 25 | PVC grau | A | 466 g |
| 6 | `Verschraubung_B` | Union d72 x 30 (Ablauf), Rohr d50 | PVC blau | A | 104 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Zulauf (Verschraubung, Rohr d50) | Rohr d50 | x -30, y 0, z 0 | (-1, 0, 0) | `Verschraubung_A` |
| Ablauf (Verschraubung, Rohr d50) | Rohr d50 | x 440, y 0, z 0 | (1, 0, 0) | `Verschraubung_B` |
| Sensorsitz (Paddelrad / Ultraschall, Bohrung d22) | d30 | x 360, y 0, z 60 | (0, 0, 1) | `Sensorblock` |
| Filterwechsel / Entleerung (Kappe unten) | Kappe d49 | x 55, y 0, z -75 | (0, 0, -1) | `Vorfilter` |

**Lebensmittel-/Wasserkontakt:** PVC-U-Bloecke, Union-Verschraubung PVC; Sieb Edelstahl; Zulassung des Fabrikats pruefen [A].

### H_HAHN Probenahmehahn (`halter_hahn.sc`, T90f)

**Funktion:** Kugelhahn d16/d20 mit Schlauchtuelle an einer Anbohrschelle, Handmessung mit Tropfentest oder Photometer (R39 H_HAHN, 5 Stueck)

**Bauteil-KS:** Z hoch; Ursprung = Mitte der Unterseite der Anbohrschelle (Anlage am Rohr); Tuelle zeigt nach +X. **Gesamt-Box:** X -30.0 bis 65.0, Y -25.0 bis 25.0, Z 0.0 bis 89.0 mm. **Masse leer:** 141 g. **Stueck:** 5 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `sattel_l` | 60 | mm | [A] Anbohrschelle 60 x 50 x 20 (flache Platte statt Rohrsattel; Rohr d20-d63) |
| `sattel_b` | 50 | mm | [A] |
| `sattel_h` | 20 | mm | [A] |
| `stutzen_d` | 25 | mm | [A] Stutzen d25 (R3/4) |
| `stutzen_h` | 20 | mm | [A] |
| `bohr_d` | 12 | mm | [A] Durchgang d12 |
| `hahn_b` | 30 | mm | [A] Kugelhahn d16/d20 Gehaeuse 30 x 30 x 36 (R39 hahn_probe) |
| `hahn_h` | 36 | mm | [A] |
| `hebel_l` | 65 | mm | [A] Hebel 70 lang, 8 breit |
| `tuelle_d` | 14 | mm | [A] Schlauchtuelle d14 fuer Schlauch ID 12 (Probenahme per Hand) |
| `tuelle_id` | 8 | mm | [A] |
| `tuelle_l` | 40 | mm | [A] |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Anbohrschelle` | Platte 60 x 50 x 20 mit Stutzen d25 x 20 | PVC grau | A | 91 g |
| 2 | `Kugelhahn` | Gehaeuse 30 x 30 x 36 mit Spindel und Hebel | PVC blau | A | 44 g |
| 3 | `Schlauchtuelle` | Tuelle d14 x 40 mit Bohrung d8 | PVC grau | A | 6 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Rohr-Anlage (Unterkante Anbohrschelle auf dem Rohr) | Anbohrschelle d20-d63 | x 0, y 0, z 0 | (0, 0, -1) | `Anbohrschelle` |
| Probenahme (Schlauchtuelle) | Tuelle d14 | x 55, y 0, z 58 | (1, 0, 0) | `Schlauchtuelle` |

**Lebensmittel-/Wasserkontakt:** PVC-Hahn und -Tuelle im Wasser; Zulassung pruefen [A].

### H_DRUCK Druckschalter-Stutzen R1/4 (`halter_druck.sc`, T90g)

**Funktion:** Anschlussstutzen R1/4 am Rohr bzw. an der Luftleitung fuer den Druckschalter (R39 H_DRUCK, 6 Stueck)

**Bauteil-KS:** Z hoch; Ursprung = Mitte der Unterseite der Anbohrschelle; Gewinde zeigt nach +Z. **Gesamt-Box:** X -30.0 bis 30.0, Y -25.0 bis 25.0, Z 0.0 bis 67.0 mm. **Masse leer:** 128 g. **Stueck:** 6 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `sattel_l` | 60 | mm | [A] Anbohrschelle 60 x 50 x 20 (flache Platte statt Rohrsattel; Rohr d20-d63) |
| `sattel_b` | 50 | mm | [A] |
| `sattel_h` | 20 | mm | [A] |
| `stutzen_d` | 25 | mm | [A] Stutzen d25 (R3/4) |
| `stutzen_h` | 20 | mm | [A] |
| `bohr_d` | 12 | mm | [A] Durchgang d12 |
| `sechs_d` | 19 | mm | [A] Sechskantteil des Nippels (Schluesselweite 19, als Zylinder) |
| `sechs_h` | 12 | mm | [A] |
| `gewinde_d` | 13.2 | mm | [E] Gewinde R1/4 Aussen 13,157 mm (DIN EN 10226) |
| `gewinde_h` | 15 | mm | [A] Gewindelaenge |
| `nippel_id` | 6 | mm | [A] Durchgang d6 |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Anbohrschelle` | Platte 60 x 50 x 20 mit Stutzen d25 x 20 | PVC grau | A | 91 g |
| 2 | `Gewindenippel` | Edelstahl, Sechskant d19 x 12 mit Gewinde R1/4 x 15, Durchgang d6 (kein Messing: Kupfer ist fuer Fische giftig) | Edelstahl | E | 37 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Rohr-Anlage (Unterkante Anbohrschelle auf Rohr oder Luftleitung) | Anbohrschelle d20-d63 | x 0, y 0, z 0 | (0, 0, -1) | `Anbohrschelle` |
| Druckanschluss R1/4 (Druckschalter) | R1/4 aussen | x 0, y 0, z 67 | (0, 0, 1) | `Gewindenippel` |

**Lebensmittel-/Wasserkontakt:** PVC-Anbohrschelle; Nippel Edelstahl (nicht Messing).

### H_MAST Sensor-Mast Kuppel (`halter_mast.sc`, T90h)

**Funktion:** Rohr d32 mit Strahlungsschutz, Hoehe 1,7 m (Kopfhoehe) bzw. am Scheitel (R39 H_MAST, 5 Stueck: MS59-MS62)

**Bauteil-KS:** Z hoch; Ursprung = Mitte der Unterseite der Fussplatte (Boden). **Gesamt-Box:** X -50.0 bis 50.0, Y -50.0 bis 50.0, Z 0.0 bis 1736.0 mm. **Masse leer:** 936 g. **Stueck:** 5 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `hoehe` | 1700 | mm | [E] Kopfhoehe 1,7 m (R39 H_MAST), Oberkante Mastrohr |
| `rohr_d` | 32 | mm | [E] Rohr PVC-U d32 (R39) |
| `rohr_wall` | 1.8 | mm | [E] PVC-U SDR 21 |
| `platte` | 100 | mm | [A] Fussplatte Stahl 100 x 100 x 6, 4 Duebel (nicht modelliert) |
| `platte_t` | 6 | mm | [A] |
| `spindel_d` | 20 | mm | [A] Strahlungsschutz Spindel |
| `schirm_d` | 90 | mm | [A] Lamellenscheiben d90, 3 Stueck im Abstand 14 |
| `schirm_h` | 36 | mm | [A] Hoehe des Strahlungsschutzes |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Fussplatte` | Stahl 100 x 100 x 6 | Stahl verzinkt | A | 471 g |
| 2 | `Mastrohr` | PVC-U d32 x 1,5, Oberkante Z 1700 | PVC grau | E | 405 g |
| 3 | `Strahlungsschutz` | Spindel d20 mit 3 Lamellenscheiben d90 (weiss) | PP weiss | A | 60 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Fuss (Unterkante Fussplatte auf dem Boden) | Platte 100 x 100 | x 0, y 0, z 0 | (0, 0, -1) | `Fussplatte` |
| Sensoraufnahme (Strahlungsschutz oben) | Spindel d20, SCD41-Platine / PAR-Sensor | x 0, y 0, z 1736 | (0, 0, 1) | `Strahlungsschutz` |

**Lebensmittel-/Wasserkontakt:** Luft, kein Wasserkontakt.

### H_BOX Messknoten-Gehaeuse IP65 (`halter_box.sc`, T90i)

**Funktion:** Messknoten-Gehaeuse IP65 mit Hutschiene (ESP32/Rechner, EZO-Schaltkreise, Isolatoren) neben dem Halter (R39 H_BOX, 7 Stueck, Messknoten mk_*)

**Bauteil-KS:** Z hoch; Ursprung = Mitte der Gehaeuse-Unterseite; Verschraubungen zeigen nach -Z (Kabel nach unten), Laschen +-X. **Gesamt-Box:** X -130.0 bis 130.0, Y -75.0 bis 75.0, Z -12.0 bis 104.0 mm. **Masse leer:** 906 g. **Stueck:** 7 (R39).

**Parameter:**

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `l` | 200 | mm | [A] IP65-Gehaeuse 200 x 150 x 100 (ESP32/Rechner, EZO-Schaltkreise, Isolatoren, R39 H_BOX; Handelsmass ueblich) |
| `w` | 150 | mm | [A] |
| `h` | 100 | mm | [A] |
| `wand` | 4 | mm | [A] Wand PS |
| `deckel_t` | 4 | mm | [A] Klardeckel Acryl |
| `schiene_l` | 150 | mm | [E] Hutschiene TS35 35 x 7,5 (DIN EN 60715), 150 lang |
| `kabel_x` | [-60, -20, 20, 60] | mm | [A] 4 Kabelverschraubungen M16 in der Bodenwand |
| `kabel_y` | -50 | mm | [A] |
| `kabel_d` | 20 | mm | [A] Verschraubung M16 aussen d20 |
| `kabel_id` | 10 | mm | [A] Durchgang d10 (Atlas-Koaxkabel, Bus 4 Adern + 24 V) |
| `kabel_l` | 12 | mm | [A] |
| `lasche_l` | 30 | mm | [A] Wandlasche 30 x 30 x 3 |
| `lasche_t` | 3 | mm | [A] |
| `lasche_z` | 40 | mm | [A] |

**Teile (Zeile = Koerper der Datei):**

| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |
|---|---|---|---|---|---|
| 1 | `Gehaeuse` | PS 200 x 150 x 100, Wand 4, 4 Durchgaenge d10 | PS grau | A | 400 g |
| 2 | `Deckel` | Klardeckel Acryl 200 x 150 x 4 | Acryl klar | A | 143 g |
| 3 | `Hutschiene` | TS35 35 x 7,5 x 150 | Stahl verzinkt | E | 309 g |
| 4 | `Verschraubung_1` | Kabelverschraubung M16 (Trunk) | PA schwarz | A | 3 g |
| 5 | `Verschraubung_2` | Kabelverschraubung M16 (Sonde 1) | PA schwarz | A | 3 g |
| 6 | `Verschraubung_3` | Kabelverschraubung M16 (Sonde 2) | PA schwarz | A | 3 g |
| 7 | `Verschraubung_4` | Kabelverschraubung M16 (Sonde 3) | PA schwarz | A | 3 g |
| 8 | `Wandlasche_1` | Stahl 30 x 30 x 3, Loch d6 | Stahl verzinkt | A | 21 g |
| 9 | `Wandlasche_2` | Stahl 30 x 30 x 3, Loch d6 | Stahl verzinkt | A | 21 g |

**Ports:**

| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |
|---|---|---|---|---|
| Trunk (RS-485 4 Adern + 24 V DC 2 Adern) | Verschraubung M16 | x -60, y -50, z -12 | (0, 0, -1) | `Verschraubung_1` |
| Sondenanschluss 1 (Koax / Kabel) | Verschraubung M16 | x -20, y -50, z -12 | (0, 0, -1) | `Verschraubung_2` |
| Sondenanschluss 2 (Koax / Kabel) | Verschraubung M16 | x 20, y -50, z -12 | (0, 0, -1) | `Verschraubung_3` |
| Sondenanschluss 3 (Koax / Kabel) | Verschraubung M16 | x 60, y -50, z -12 | (0, 0, -1) | `Verschraubung_4` |
| Wandbefestigung 1 | Lasche 30 x 30 x 3, Loch d6 | x -130, y 0, z 41.5 | (-1, 0, 0) | `Wandlasche_1` |
| Wandbefestigung 2 | Lasche 30 x 30 x 3, Loch d6 | x 130, y 0, z 41.5 | (1, 0, 0) | `Wandlasche_2` |

**Lebensmittel-/Wasserkontakt:** Luft, kein Wasserkontakt (IP65).

## Sonden-Platzhalter (ein Koerper je Typ, Masse Annahme)

| Datei | Typ / Produkt (R39) | Platzhalter (Teile-Zeile = 1 Koerper) | Masse | Stueck (Pflicht/Zusatz) | Preis (R39) | Kalibrierung | Wartung / Standzeit | Kabel | Konfidenz R39 |
|---|---|---|---|---|---|---|---|---|---|
| `sonde_do_ind.sc` | `do_ind`: Gel/galvanische DO-Sonde industriell mit PT-1000 (Atlas ENV-50-DO) | Tauchsonde industriell Ø 25 x 170 (Atlas ENV-50-DO) (Platzhalter, Masse Annahme) (Sonde blau, A) | 133 g | 1 (1/0) | 349.99 USD (gelesen) | ca. 1 Jahr (Hersteller), Ein-Punkt in Luft | ca. 18 Monate; ca. 4 Jahre | koax_sma, 1 Adern, 5 V | mittel |
| `sonde_do_mini.sc` | `do_mini`: Mini-DO-Sonde (Atlas ENV-20-DOX) | Mini-Tauchsonde Ø 12 x 110 (Atlas ENV-20-DOX) (Platzhalter, Masse Annahme) (Sonde blau, A) | 20 g | 5 (3/2) | 199.99 USD (Haendlerliste) | ca. 6 Monate (Haendlerangabe) | ca. 6 Monate; ca. 2,5 Jahre | koax_sma, 1 Adern, 5 V | niedrig-mittel |
| `sonde_ph.sc` | `ph`: pH-Sonde Doppelelektrolyt Ag/AgCl (Atlas ENV-40-pH) | pH-Sonde Ø 12 x 150 (Atlas ENV-40-pH) (Platzhalter, Masse Annahme) (Sonde grau, A) | 27 g | 5 (1/4) | 99.99 USD (gelesen) | Hersteller ca. 1 Jahr; im Dauerbetrieb im Fischwasser erst monatlich pruefen [A] | Reinigen/Auffrischen nach Bedarf; ca. 2,5 Jahre | koax_bnc, 1 Adern, 5 V | mittel |
| `sonde_ec.sc` | `ec`: Leitfaehigkeitssonde K 0,1 (Atlas) | Leitfaehigkeitssonde K 0,1 Ø 12 x 150 (Atlas) (Platzhalter, Masse Annahme) (Sonde grau, A) | 27 g | 3 (1/2) | 177.99 USD (gelesen) | bei Einbau, danach Hersteller ca. 10 Jahre; Kontrolle mit Standard jaehrlich [A] | Reinigen bei Belag; ca. 10 Jahre | koax_bnc, 1 Adern, 5 V | mittel |
| `sonde_temp_ds.sc` | `temp_ds`: Temperaturfuehler DS18B20 wasserdicht | Temperaturfuehler DS18B20, Edelstahlhuelse Ø 6 x 50 (Platzhalter, Masse Annahme) (Edelstahl, A) | 11 g | 6 (2/4) | 3-10 USD (Annahme) | Vergleichsmessung jaehrlich [A] | keine; Jahre [A] | onewire_3ader, 3 Adern, 3,3-5 V | mittel (Technik) / niedrig (Preis) |
| `sonde_level_float.sc` | `level_float`: Schwimmerschalter (Niedrig/Hoch) | Schwimmerschalter Ø 30 x 55 (Niedrig/Hoch, Kontakt) (Platzhalter, Masse Annahme) (Schwimmer orange, A) | 23 g | 17 (4/13) | 10-20 USD (gelesen) | Funktionstest monatlich | Reinigen von Belag; Jahre [A] | kontakt_2ader, 2 Adern, keine (Kontakt) | mittel |
| `sonde_level_druck.sc` | `level_druck`: Tauchdrucksonde 4-20 mA | Tauchdrucksonde 4-20 mA Ø 20 x 140 (Platzhalter, Masse Annahme) (Edelstahl, A) | 347 g | 2 (0/2) | 300-500 USD (Herstellerblog) | Nullpunkt jaehrlich [A] | Sediment/Biofilm abwischen; Jahre [A] | strom_4_20mA_2ader, 2 Adern, 12-24 V | niedrig-mittel |
| `sonde_flow_12.sc` | `flow_12`: Paddelrad-Durchflussmesser 1/2 Zoll (Atlas) | Paddelrad-Durchflussmesser 1/2 Zoll 50 x 40 x 80 (Atlas) (Platzhalter, Masse Annahme) (Sonde schwarz, A) | 192 g | 7 (0/7) | 145.99 USD (gelesen) | nicht noetig, Plausibilitaet gegen Pumpen-Soll | Vorfilter, Schmutz in den Schaufeln; ca. 10 Jahre | impuls_3ader, 3 Adern, 5 V | mittel |
| `sonde_flow_gross.sc` | `flow_gross`: Durchflussmesser fuer 110 l/min (1 Zoll oder Ultraschall-Clamp-on, Typ offen) | Durchflussmesser fuer 110 l/min (Ultraschall-Clamp-on, Typ offen) 100 x 60 x 40 (Platzhalter, Masse Annahme) (Sonde schwarz, A) | 288 g | 2 (2/0) | 266-500 USD (Annahme) | nicht noetig | Vorfilter; Jahre [A] | impuls_3ader, 3 Adern, 5-24 V | niedrig |
| `sonde_druck_schalter.sc` | `druck_schalter`: Druckschalter mit Relais (Luft oder Wasser) | Druckschalter mit Relais-Ausgang Ø 32 x 55, Anschluss R1/4 (Platzhalter, Masse Annahme) (Edelstahl, A) | 349 g | 6 (1/5) | 30 USD (gelesen (Luft)) | Funktionstest monatlich (Gebläse abschalten) | keine; Jahre [A] | kontakt_2ader, 2 Adern, keine (Kontakt) | mittel |
| `sonde_strom_ct.sc` | `strom_ct`: Stromwandler SCT-013 (Klemm-CT) je Verbraucher | Klemm-Stromwandler SCT-013 36 x 13 x 30 (Platzhalter, Masse Annahme) (Sonde schwarz, A) | 17 g | 10 (4/6) | 17-21 EUR (Haendlerliste) | Sollstrom bei Inbetriebnahme einlernen | keine; Jahre [A] | ct_2ader, 2 Adern, keine | mittel |
| `sonde_co2_scd41.sc` | `co2_scd41`: CO2/Temperatur/Feuchte-Modul SCD41 | CO2-Modul SCD41 auf Platine 25 x 17 x 10 (Chip 10 x 10 x 6,5) (Platzhalter, Masse Annahme) (Platine gruen, A) | 8 g | 3 (0/3) | 14-19 GBP (Haendlerliste (nur Chip)) | Selbstkalibrierung, Frischluft-Abgleich jaehrlich [A] | keine; Jahre [A] | i2c_4ader, 4 Adern, 3,3-5 V | mittel |
| `sonde_par.sc` | `par`: Quantensensor PAR (z. B. Apogee SQ-500) oder Lux-Platine | Quantensensor PAR Ø 30 x 37 (z. B. Apogee SQ-500) (Platzhalter, Masse Annahme) (Sonde gelb, A) | 42 g | 2 (0/2) | offen (offen) | Herstellerkalibrierung, 4 Jahre Garantie; Intervall nicht gelesen | Diffusor reinigen; Jahre [A] | analog_3ader, 3 Adern, 5-24 V | niedrig |
| `sonde_leck.sc` | `leck`: Leckagesonde (Kontakt am Boden) | Leckagesonde, Kontaktflaeche 50 x 20 x 6 (Platzhalter, Masse Annahme) (Kontakt rot, A) | 8 g | 3 (0/3) | 45 GBP (Haendlerliste) | Nassprobe halbjaehrlich | trocken halten; Jahre [A] | kontakt_2ader, 2 Adern, 5 V | niedrig-mittel |

**Ports aller Sonden:** Messspitze/Anlage unten (x 0, y 0, z 0, -Z) und Kabel am oberen Ende (x 0, y 0, z = Hoehe, +Z) mit Adernzahl und Versorgung aus `messstellen.json`.

**Lebensmittel-/Wasserkontakt und Alarm je Sonde:**

| Typ | Wasser-/Lebensmittelkontakt | Alarmgrenzen (R39, aus den Messstellen) |
|---|---|---|
| `do_ind` | Wasserkontakt ja (Fischwasser); Gehaeusewerkstoff des Herstellers nicht belegt [A], Konformitaet fuer Lebensmittelkontakt ungeprueft | AL01 O2 Fischbecken: Warnung < 5,0, Alarm < 4,0, Notfall < 3,0 (Notluft sofort); AL03 Temperatur Fischbecken/Heizung: Warnung < 25 oder > 31, Alarm < 20 oder > 34 [A] oder Sprung > 2,8 K in 1 h |
| `do_mini` | wie do_ind | AL01 O2 Fischbecken: Warnung < 5,0, Alarm < 4,0, Notfall < 3,0 (Notluft sofort); AL02 O2 Biofilter-Auslass: Warnung < 3,0, Alarm < 2,0; AL03 Temperatur Fischbecken/Heizung: Warnung < 25 oder > 31, Alarm < 20 oder > 34 [A] oder Sprung > 2,8 K in 1 h |
| `ph` | wie do_ind (Glas/Epoxid-Gehaeuse laut Hersteller-Erscheinung [A]) | AL01 O2 Fischbecken: Warnung < 5,0, Alarm < 4,0, Notfall < 3,0 (Notluft sofort); AL03 Temperatur Fischbecken/Heizung: Warnung < 25 oder > 31, Alarm < 20 oder > 34 [A] oder Sprung > 2,8 K in 1 h; AL04 pH Kreislauf: Warnung < 6,8 oder > 7,8, Alarm < 6,5 oder > 8,5 [A] oder Sprung >= 0,5 in 1 h [A] |
| `ec` | wie do_ind | AL01 O2 Fischbecken: Warnung < 5,0, Alarm < 4,0, Notfall < 3,0 (Notluft sofort); AL03 Temperatur Fischbecken/Heizung: Warnung < 25 oder > 31, Alarm < 20 oder > 34 [A] oder Sprung > 2,8 K in 1 h; AL04 pH Kreislauf: Warnung < 6,8 oder > 7,8, Alarm < 6,5 oder > 8,5 [A] oder Sprung >= 0,5 in 1 h [A] |
| `temp_ds` | Wasserkontakt ja; Edelstahlhuelse (Handelsware) | AL01 O2 Fischbecken: Warnung < 5,0, Alarm < 4,0, Notfall < 3,0 (Notluft sofort); AL03 Temperatur Fischbecken/Heizung: Warnung < 25 oder > 31, Alarm < 20 oder > 34 [A] oder Sprung > 2,8 K in 1 h; AL04 pH Kreislauf: Warnung < 6,8 oder > 7,8, Alarm < 6,5 oder > 8,5 [A] oder Sprung >= 0,5 in 1 h [A] |
| `level_float` | Wasserkontakt ja; Kunststoff, Konformitaet offen [A] | AL10 Wasserstand Pool (Soll Z 515): Warnung -30 / +30, Alarm -50 / +50 (Heizung und Pumpen sperren) |
| `level_druck` | Wasserkontakt ja; Edelstahl/Keramik (Herstellerblog), Konformitaet offen | AL10 Wasserstand Pool (Soll Z 515): Warnung -30 / +30, Alarm -50 / +50 (Heizung und Pumpen sperren); AL20 Reserve Frischwasser Puffer unten: Warnung < 0,7 (1 Tag), Alarm < 0,35 (0,5 Tag) |
| `flow_12` | Wasserkontakt ja (Paddelrad im Strom); Werkstoff nicht belegt [A] | AL11 Durchfluss Linie, Abgaenge: Warnung < 82 % Soll, Alarm < 64 % Soll laenger als 60 s [A]; AL20 Reserve Frischwasser Puffer unten: Warnung < 0,7 (1 Tag), Alarm < 0,35 (0,5 Tag) |
| `flow_gross` | Clamp-on: kein Wasserkontakt; Inline-Typ: ja, offen | AL11 Durchfluss Linie, Abgaenge: Warnung < 82 % Soll, Alarm < 64 % Soll laenger als 60 s [A] |
| `druck_schalter` | Wasser- bzw. Luftkontakt; Edelstahl-Anschluss statt Messing (Kupfer ist fuer Fische giftig) [A] | AL12 Pumpenstrom Pumpen, Gebläse: Warnung < 70 oder > 120, Alarm < 50 laenger als 5 s oder > 130 [A]; AL13 Luftdruck Belueftung, Luftpolster: Warnung -, Alarm faellt unter 50 % des Betriebsdrucks [A] (sofort), Notfall Notluft sofort |
| `strom_ct` | kein Wasserkontakt (Schaltschrank) | AL12 Pumpenstrom Pumpen, Gebläse: Warnung < 70 oder > 120, Alarm < 50 laenger als 5 s oder > 130 [A] |
| `co2_scd41` | kein Wasserkontakt (Kuppelluft), Strahlungsschutz | AL16 CO2 Raumluft Kuppel: Warnung > 1000, Alarm > 2000 (lueften), > 5000 (Raum verlassen); AL17 Luftfeuchte Kuppel: Warnung > 85 [A], Alarm - |
| `par` | kein Wasserkontakt (Kuppelluft) | kein eigener Alarm (Signal fuer Verknuepfungen) |
| `leck` | kein Lebensmittelkontakt (Boden, Kontaktflaeche trocken bis zur Leckage) | AL19 Leckage Technikbereich: Warnung -, Alarm nass |

## Passung Sonde und Halter (Check)

do_ind (d25) im Tauchrohr d40 (ID 36,2); ph, ec, temp_ds, do_mini in den Sondenstutzen d25/Bohrung 16 (H_ZELLE und Messzelle puffer_klein); level_float (d30) im Beruhigungsrohr d63 (ID 57); flow_12 deckt den Sensorsitz d30 ab; druck_schalter auf dem R1/4-Nippel; par (d30) und SCD41-Platine unter den Strahlungsschutz d90; Details in `scripts/workshop/check_messstellen.py` (`fit_checks`).

## Montage (L4)

1. Halter an der Messstelle setzen (Beckenrand, Rohr, Wand, Boden), Anbohrschellen auf das Rohr; 2. Sonden einsetzen, Kabel ins Messknoten-Gehaeuse (H_BOX) fuehren; 3. Messknoten per Trunk (RS-485 + 24 V) an die Zentrale; 4. Sonden kalibrieren (Intervalle oben), Alarmgrenzen einstellen (R39).

**Werkzeug:** Akkuschrauber, Rohrschneider, PVC-Kleber, Bohrer, Klemmen; Kalibrierloesungen pH 4/7/10, EC-Standard, Luft fuer DO-Ein-Punkt.

## Stueckliste-Zeile

- Messstellen-Bauteile: 5 x H_TAUCH, 14 x H_BERUHIG, 2 x H_ZELLE, 7 x H_INLINE d32, 2 x H_INLINE d50, 5 x H_HAHN, 6 x H_DRUCK, 5 x H_MAST, 7 x H_BOX; Sonden: 1 x do_ind, 5 x do_mini, 5 x ph, 3 x ec, 6 x temp_ds, 17 x level_float, 2 x level_druck, 7 x flow_12, 2 x flow_gross, 6 x druck_schalter, 10 x strom_ct, 3 x co2_scd41, 2 x par, 3 x leck.

## Alternative lokale Fertigung

Halter aus PVC-U-Rohr und Bloecken (Kunststoffhandel) selbst gebohrt und geklebt; Klemmen und Laschen aus Flachstahl 25 x 3 gebogen; Messknoten-Gehaeuse als Standard-IP65-Verteilerkasten; Sonden nach R39-Produktliste (Atlas Scientific) oder gleichwertig.

## Pruefung

- `scripts/workshop/check_messstellen.py` (alle 23 Komponenten, Ergebnis `renders/components/messstellen/check.txt`): Koerper = Teile-Zeilen, Namen, Masse > 0, Ports an den Koerpern mit Spitzen am Rand, Mass-/Volumenpruefungen je Halter, Sondenmasse = Volumen x Dichte, Passung Sonde/Halter, Abdeckung der Sondentypen, Interferenz 0.
- Kein Pruefer-Lauf (Auftrag W35: Selbstcheck).

## Offene Fragen

- Hersteller-Abmessungen und -Werkstoffe der Sonden (Atlas-Datenblaetter, SCT-013, SCD41-Modul, PAR-Sensor) nicht gelesen: alle Sondenmasse und Farben Annahme; vor der Bestellung gegen Datenblatt pruefen
- Konformitaet fuer Lebensmittelkontakt: Rohre, Armaturen und Sondengehaeuse nur als Handelsware angenommen, keine Zulassung belegt
- H_INLINE: Rohrdurchmesser je Kante stehen nur in `leitungsnetz.json` (R40, nicht anfassen): d32 fuer flow_12 angenommen, d50 fuer flow_gross; Kanten d40/d25 brauchen Reduzierung (Bibliothek T70)
- Anbohrschelle (H_HAHN, H_DRUCK) als flache Platte: Rohrsattel und Dichtung nicht modelliert; Sattelform je Rohr-d offen
- Siebfeinheit >= 80 um (H_INLINE) und Schlitzbreite (H_BERUHIG) sind Masse, keine gepruefte Filterleistung
- Kabelwege und Kabellaengen der Sonden (Atlas-Kabel 1-3 m) liegen bei der Montage (M10); Verlaengerung nicht gelesen (R39)
- Statik des Sensor-Masts (1,7 m PVC d32 auf 100 x 100 Platte) nicht gerechnet; Wind und Berührung nicht betrachtet
- Messzelle puffer_klein: Sondenstutzen d25 passen zu ph, ec, do_mini, temp_ds (Bohrung 16); die endgueltige Belegung der 4 Stutzen liegt bei der Montage
