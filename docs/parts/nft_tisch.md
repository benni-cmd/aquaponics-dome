# Bauteilblatt T22 nft_tisch (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/nft_tisch.json` und `designs/components/nft_tisch.sc`, nicht von Hand aendern)

**Funktion:** Tragt n NFT-Rinnen mit 1,5 % Gefaelle (Zulauf hoch bei -X), verteilt Wasser ueber Zulaufverteiler und Schlaeuche (ein Schlauch je Rinne) und sammelt den Ablauf im Sammelrohr; Zickzack der Pflanzen durch Phase A/B benachbarter Rinnen (pitch/2).

**Datei:** `designs/components/nft_tisch.sc` · **Teilenummer:** T22 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche (Z=0 Boden), X Laengsachse (Zulauf bei -X), Y quer

**Anzahl (Instanzen):** innen 10, Mitte 6, aussen 8 (Quelle: docs/scope-cards.md nft_tisch, data/layout.json hydro_tables)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `slope_pct` | 1.5 |  | R06 (docs/research/R06.md): Gefaelle laut zwei Quellen 1,3-3 % (Morgan 1:50-1:75, Greenhouse Management 1,2-3 %), nur FarmHub 1 % -> 1,5 % = 15 mm/m = 0,86 Grad; Durchfluss je Rinne 0,5 l/min (Port-Attribut) |
| `leg_w` | 30 | mm | OBJ-Analyse: Beine 30 x 30 (Tanks); Tischbeine in ref-6 flache Winkelprofile, hier Rechteckrohr 30 x 30 x 2 [A] |
| `leg_wall` | 2 | mm | [A] Rechteckrohr verzinkt |
| `holm_w` | 40 | mm | [A] Querholm 40 x 30 x 2 (Rinne liegt auf) |
| `holm_h` | 30 | mm | [A] |
| `holm_overhang` | 30 | mm | [A] Holm steht je Seite 30 mm ueber die Beine |
| `bock_inset` | 250 | mm | [A] Abstand Bock zur Rinnenstirn (Ueberstand 250) |
| `leg_inset` | 25 | mm | [A] Beinmitte um 25 mm nach innen von der Holmkante |
| `strut_z` | 250 | mm | [A] Querstrebe/Laengsstrebe auf Hoehe 250 ueber Boden |
| `foot_plate` | 80 | mm | [A] Fussplatte 80 x 80 x 5 |
| `foot_t` | 5 | mm | [A] |
| `foot_hole` | 9 | mm | [E] Durchgangsloch fuer M8 (ISO 273 mittel 9) |
| `clip_t` | 3 | mm | [A] Rinnenhalter aus 3-mm-Blech, 25 breit, 25 hoch |
| `clip_len` | 25 | mm | [A] |
| `hdr_od` | 25 | mm | [A] Zulaufverteiler d25 (entspricht etwa DN20), Wand 3 |
| `hdr_wall` | 3 | mm | [A] |
| `hose_od` | 20 | mm | [A] Schlauch ID 16 / AD 20 ueber Tuelle D16 und Verteilerstutzen |
| `hose_gap` | 70 | mm | [A] freier Abstand zwischen Tuelle und Verteilerstutzen |
| `col_od` | 50 | mm | [A] Sammelrohr d50 (Aussen 50, Wand 3; entspricht etwa DN40, Muffen d40/d32) |
| `col_wall` | 3 | mm | [A] |

| Typ | Rinnen | Abstand | Rinne | Z Rinnenmitte | Laenge | Herkunft |
|---|---|---|---|---|---|---|
| aussen | 3 | 288 | l | 1300 | 3232 | layout.json hydro_tables r 4888/5176, Rinnen-Unterkante Z 1291-1325 (Mittel 1308, gerundet auf 1300 = -8 mm); 3 Rinnen: Ben (OBJ/Bild zeigen nur 2, oasis-obj-analysis) + A (3 nach Beetbreite) |
| mitte | 4 | 263 | m | 1300 | 1983 | layout.json hydro_tables r 2987-3775, Rinnen-Unterkante Z 1280-1330 (Mittel 1307, gerundet 1300 = -7 mm), Abstand 263 |
| innen | 2 | 262 | k | 840 | 1304 | layout.json hydro_tables r 1733/1995, Rinnen-Unterkante Z 819-858 (Mittel 838,5, gerundet 840 = +1,5 mm), Abstand 262 |

Gesamt-Box (Messung): X -1785.0 bis 1695.0, Y -413.0 bis 413.0, Z -25.0 bis 1424.3 mm; Koerper: 82.

**Toleranzen / Spiel:** Rinnenunterkante = Holmoberkante an jedem Bock (Pruefung +-1 mm); Gefaelle 1,5 % +-0,03 %; Rinnenhoehe Z +-1,5 mm. Gewichte: Summe je Koerper nach Werkstoff (Stahl 7,85, PVC 1,4 g/cm3; die Messung am .sc enthaelt auch die verknuepften Rinnen).

## Werkstoff und Gewicht

- Werkstoff: Stahl verzinkt (Boecke), PVC/PE (Rohre, Schlaeuche), Dichte 7.85 g/cm3, Farbe #aeb4b8 (ref-6: graue/verzinkte Beine mit Halterungen)
- Volumen (Messung, `solidcraft-cli eval`): 15969.3 cm3 · Masse leer: 42880 g (42.88 kg)
- Variante `nft_tisch_aussen`: 42.88 kg leer
- Variante `nft_tisch_mitte`: 38.32 kg leer
- Variante `nft_tisch_innen`: 18.22 kg leer
- Gefuellt/in Betrieb: Wasserfuellung der Rinnen (Film 10 mm, 1 l = 1 kg): aussen 3 x 4,0 = 12 kg, Mitte 4 x 2,5 = 10 kg, innen 2 x 1,6 = 3,2 kg [E]; Verteiler d25 und Sammelrohr d50 gefuellt je ca. 0,3-1,6 kg [E]

## Querschnitt / Profil

Boecke: Beine, Querholm, Querstrebe aus Rechteckrohr verzinkt 30x30x2 bzw. 40x30x2; Diagonalen Flachstahl 25x3 gekreuzt; Fussplatten 80x80x5. Rinnen: Instanzen nft_rinne_<l|m|k>_<a|b>, Phase abwechselnd.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| aussen: Zulauf Tisch (Verteilerrohr D25 offen, +Y-Ende) | Rohr d25, Wand 3 (Anschluss Rohr/Schlauch) | x -1772, y 413, z 1394 | Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y); Rohr d25 (etwa DN20) |
| aussen: Ablauf Tisch (Sammelrohr d50 offen, +Y-Ende) | Rohr d50, Wand 3 (etwa DN40) | x 1670, y 413, z 1296 | Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal) |
| aussen: Verteiler-Stutzen je Rinne (n=3) | Schlauch ID 16, Durchfluss je Rinne 0,5 l/min (R06) | x -1715, y = Rinnenmitte, z 1394 | aus Verteiler, Richtung +X |
| aussen: Fussplatten-Anker | M8, 2 Schrauben je Platte, Loch D9, Diagonalversatz +-25 | Fusspunkte z 5; aussen: Beinabstand y 596, Bockabstand x 2732; mitte: Beinabstand y 809, Bockabstand x 1483; innen: Beinabstand y 282, Bockabstand x 804 (je Bock zwei Fuesse bei y = +-Beinabstand/2) | Befestigung auf Boden/Betonpunkt, Richtung -Z |
| mitte: Zulauf Tisch (Verteilerrohr D25 offen, +Y-Ende) | Rohr d25, Wand 3 (Anschluss Rohr/Schlauch) | x -1148, y 520, z 1385 | Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y); Rohr d25 (etwa DN20) |
| mitte: Ablauf Tisch (Sammelrohr d50 offen, +Y-Ende) | Rohr d50, Wand 3 (etwa DN40) | x 1046, y 520, z 1305 | Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal) |
| mitte: Verteiler-Stutzen je Rinne (n=4) | Schlauch ID 16, Durchfluss je Rinne 0,5 l/min (R06) | x -1090, y = Rinnenmitte, z 1385 | aus Verteiler, Richtung +X |
| mitte: Fussplatten-Anker | M8, 2 Schrauben je Platte, Loch D9, Diagonalversatz +-25 | Fusspunkte z 5; aussen: Beinabstand y 596, Bockabstand x 2732; mitte: Beinabstand y 809, Bockabstand x 1483; innen: Beinabstand y 282, Bockabstand x 804 (je Bock zwei Fuesse bei y = +-Beinabstand/2) | Befestigung auf Boden/Betonpunkt, Richtung -Z |
| innen: Zulauf Tisch (Verteilerrohr D25 offen, +Y-Ende) | Rohr d25, Wand 3 (Anschluss Rohr/Schlauch) | x -808, y 256, z 920 | Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y); Rohr d25 (etwa DN20) |
| innen: Ablauf Tisch (Sammelrohr d50 offen, +Y-Ende) | Rohr d50, Wand 3 (etwa DN40) | x 706, y 256, z 850 | Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal) |
| innen: Verteiler-Stutzen je Rinne (n=2) | Schlauch ID 16, Durchfluss je Rinne 0,5 l/min (R06) | x -751, y = Rinnenmitte, z 920 | aus Verteiler, Richtung +X |
| innen: Fussplatten-Anker | M8, 2 Schrauben je Platte, Loch D9, Diagonalversatz +-25 | Fusspunkte z 5; aussen: Beinabstand y 596, Bockabstand x 2732; mitte: Beinabstand y 809, Bockabstand x 1483; innen: Beinabstand y 282, Bockabstand x 804 (je Bock zwei Fuesse bei y = +-Beinabstand/2) | Befestigung auf Boden/Betonpunkt, Richtung -Z |

## Verbindungen und Befestigungen

- Beine an Fussplatte und Querholm: geschweisst (MAG), danach verzinkt [A]
- Fussplatten: 2 Schrauben M8x30 (hex_bolt) je Platte in den Boden/Betonpunkt, Loch D9
- Diagonalen: je Ende Schraube M6x40 mit Mutter durch das Bein
- Rinnenhalter: L-Blech 3 mm, 25 x 25 x 25, je Rinnenseite und Bock, Schraube M5x12
- Verteiler: Rohr d25 mit Stutzen D16 (Verklebung/Schweissen), Schlaeuche ID 16 auf Tuelle und Stutzen, Sammelrohr d50 mit Muffen d40/d32 auf den Ablaufstutzen

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Rinnenzahl 2 / 4 / 3 | 2/4/3 | OBJ + Ben + A | layout.json hydro_tables (2 innen, 4 Mitte, 2 aussen im OBJ/Bild); aussen 3: Ben (Bild/OBJ zeigen nur 2, oasis-obj-analysis) + A Anzahl nach Beetbreite 933-993 | mittel |
| Rinnenabstand 262 / 263 / 288 | 262 / 263 / 288 mm | OBJ | layout.json hydro_tables (Abstand der Rinnen) | hoch |
| Rinnenlaenge 1304 / 1983 / 3232 | 1304 / 1983 / 3232 mm | OBJ | layout.json hydro_tables | hoch |
| Hoehe Rinnenunterkante (Boden) bei x=0: Z 840 / 1300 / 1300 | 840 / 1300 / 1300 | OBJ | layout.json hydro_tables Z (Unterkanten 819-858, 1280-1330, 1291-1325), Mittel 838,5 / 1307 / 1308 gerundet (Abweichung <= 8 mm) | mittel |
| Zickzack Versatz pitch/2 = 125 | 125 mm | Bild | ref-6 mittlerer Tisch (zwei versetzte Reihen zwischen Nachbarrinnen); Scope-Card nft_tisch | hoch |
| Gefaelle 1,5 % (0,86 Grad) | 1,5 % (0,86 Grad) | R06 | docs/research/R06.md: 1,3-3 % (Morgan, Greenhouse Mgmt), FarmHub 1 % | mittel |
| Zwei Boecke = 4 Beine, Abstand zur Rinnenstirn 250 | 2 Boecke (4 Beine) | Scope-Card + A | docs/scope-cards.md nft_tisch: 4 Beine mit Querstreben, Diagonalen; ref-6: zwei Beinpaare je Tisch (Bild-Kritiker: keine Mittelbeine); Abstand 250 geschaetzt | mittel |
| Rechteckrohr 30x30x2 / 40x30x2 | 30x30x2; 40x30x2 | A + OBJ | Beine 30x30 aus OBJ-Analyse (Tank); ref-6 zeigt flache Beine/Winkel mit Halterungen | niedrig |
| Gekreuzte Diagonalen Flachstahl 25x3 | 2 je Bock | Bild + A | ref-6: schraege Stuetzen an den Beinen; Scope-Card verlangt Diagonalen | mittel |
| Fussplatten 80x80x5, M8 | 80x80x5 | A | Standard-Fusspaltte; ref-6 zeigt Winkelfuesse | niedrig |
| Rinnenhalter L-Blech 25x25x3, M5 | 25x25x25 x 3 mm, M5x12 | Bild + A | ref-6: kleine Befestigungspunkte an der Rinnenseitenwand (Bild-Kritiker B3) | niedrig |
| Zulaufverteiler d25 mit n Stutzen, Schlauch ID 16 / AD 20 (hellblau) | d25; Schlauch ID16/AD20 | Bild + A | ref-6: hellblaue Schlaeuche am Tischende, ein Schlauch je Rinne; Masse A | mittel |
| Sammelrohr d50 mit Muffen | d50, Muffen d40/d32 | A | Scope-Card: Sammelablauf; Mass A (keine Quelle) | niedrig |
| Durchfluss je Rinne 0,5 l/min | 0,5 l/min je Rinne | R06 | docs/research/R06.md | mittel |
| Anzahl Tische 10 / 6 / 8 | 10 / 6 / 8 | OBJ + Ben | components.md NFT-Ringe (Sektoren je Ring) | mittel |
| Laengsstreben 30x30x2 auf Hoehe 250 (Bodenrahmen) | 30x30x2, z 250 | A | statisch noetig (Aussteifung der zwei Boecke); in ref-6 durch Beete verdeckt (Bild-Kritiker vermutet: nicht sichtbar) | niedrig |
| Zulaufverteiler: Achse auf Hoehe der Tuellenachse (+70 mm), freier Schlauchabschnitt 70 mm (hose_gap) | 70 / 70 | E + A | Rinne: Tuelle z 70 (nft_rinne.json); hose_gap Annahme | niedrig |
| Sammelrohr: Achse auf Hoehe der Ablaufachse der Rinne (+20 mm ueber dem tiefen Rinnenende) | 20 | E | Rinne: Ablaufstutzen z 20 (nft_rinne.json) | mittel |
| Holmueberstand 30 mm, Beineinzug 25 mm | 30 / 25 | A | Konstruktionspraxis (Holm ragt je Seite 30 mm ueber die Beine) | niedrig |
| Diagonalenschrauben M6x40 mit Mutter | M6x40 | A + Normteil | SolidCraft parts.insert hex_bolt/hex_nut M6 | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg (Tisch: Platte aus Rinnen auf Boecken, Schlaeuche am Tischende hellblau); reference/ref-4 und ref-5 (Ringanordnung)
- Quelle der Masse: docs/components.md und data/layout.json hydro_tables (Hoehe Z, Rinnenabstand, Laenge); ref-6: weisse Platte aus Rinnen auf Boecken, Verteilerschlaeuche hellblau am Tischende
- Abweichung zum OBJ: OBJ: hydro_tables je Ring nur ein Beispiel (2 Rinnen aussen, Platten ohne Beine); Hoehe Z (Rinnenmitte) innen 840, Mitte/aussen 1300 als Mittel der OBJ-Werte (819-858, 1280-1330, 1291-1325); die Ringlage (Azimut, Apothem) kommt vom Integrator.

## Montage (L4)

1. Boecke am Boden ausrichten, Fussplatten mit M8 verschrauben
2. Querstreben und Laengsstreben einsetzen, Diagonalen verschrauben
3. Rinnen auf die Querholme legen (Zulaufende hoeher), Halteclips M5 setzen
4. Zulaufverteiler an die Boecke haengen, Schlaeuche ID 16 auf Stutzen und Tuellen
5. Sammelrohr mit Muffen auf die Ablaufstutzen stecken, Gefaelle kontrollieren (1,5 %)

**Werkzeug:** Wasserwaage/Gefaellelatte, Akkuschrauber, Schluessel M5/M6/M8, Bohrmaschine, Schweissgeraet (oder Winkelverbinder)

## Stueckliste-Zeile

- Pro Tisch je Typ (Laengen in mm):
-   aussen: Beine 4 x 30x30x2: Laenge 1285 (Zulauf-Bock) / 1245 (Ablauf-Bock), Beinabstand y 596; Holm 40x30x2 x 2: Laenge 766; Querstrebe 30x30x2 x 2: Laenge 566; Laengsstreben 30x30x2 x 2: Laenge 2702; Diagonalen 25x3 x 4: Laenge 1165/1130; Fussplatten 80x80x5 x 4; Rinnen 3 x nft_rinne_l (Laenge 3232); Verteiler d25: Laenge 826, 3 Stutzen d16; Sammelrohr d50: Laenge 826; Schlaeuche 3 x ID16/AD20 x 110
-   mitte: Beine 4 x 30x30x2: Laenge 1276 (Zulauf-Bock) / 1254 (Ablauf-Bock), Beinabstand y 809; Holm 40x30x2 x 2: Laenge 979; Querstrebe 30x30x2 x 2: Laenge 779; Laengsstreben 30x30x2 x 2: Laenge 1453; Diagonalen 25x3 x 4: Laenge 1279/1262; Fussplatten 80x80x5 x 4; Rinnen 4 x nft_rinne_m (Laenge 1983); Verteiler d25: Laenge 1039, 4 Stutzen d16; Sammelrohr d50: Laenge 1039; Schlaeuche 4 x ID16/AD20 x 110
-   innen: Beine 4 x 30x30x2: Laenge 811 (Zulauf-Bock) / 799 (Ablauf-Bock), Beinabstand y 282; Holm 40x30x2 x 2: Laenge 452; Querstrebe 30x30x2 x 2: Laenge 252; Laengsstreben 30x30x2 x 2: Laenge 774; Diagonalen 25x3 x 4: Laenge 597/586; Fussplatten 80x80x5 x 4; Rinnen 2 x nft_rinne_k (Laenge 1304); Verteiler d25: Laenge 512, 2 Stutzen d16; Sammelrohr d50: Laenge 512; Schlaeuche 2 x ID16/AD20 x 110
- Je Bock: 2 Beine, 1 Holm, 1 Querstrebe, 2 Diagonalen, 2 Fussplatten, 4 Schrauben M8x30 (Fussplatten, 2 je Platte), 4 Schrauben M6x40 + 4 Muttern M6 (Diagonalen, 1 je Ende), 2 Rinnenhalter je Rinne (je Rinnenseite 1) mit Schraube M5x12; Bock-Anzahl je Tisch 2, Tische gesamt 10 / 6 / 8 (Boecke gesamt 48)
- Dabei: 4 Duebel/Anker M8 je Bock (Boden), je 1 Endstopfen d25 und d50 je Tisch (-Y-Rohrende)

## Alternative lokale Fertigung

Rahmen aus Baustahl-Rechteckrohr (Metallbauer, Kaltverzinken) oder Aluprofil-Systemprofil mit Winkelverbindern; Rinnenhalter aus Streifen 25x3 selbst gebogen.

## Renders


## Pruefung

- Gauntlet-Urteil: Bild-Kritiker: Referenz (Luecken trianguliert); Spec-Pruefer: FAIL behoben, Beinstandort offen (Orchestrator)
- scripts/workshop/check_nft_tisch.py (Ergebnis renders/components/nft_tisch_aussen/check.txt): Rinnenzahl, Abstand, Zickzack pitch/2, Gefaelle, Hoehe, Auflage, Boecke, Verteiler/Sammelrohr
- Triage in docs/workshop-log.md
- Bild-Kritiker (Kontextpaket): Referenz; grosse Luecken vermutet (Bockzahl, Rinnenbreite) -> Triage im Log; Bockzahl auf Scope-Card (4 Beine) umgestellt

## Offene Fragen

- Aufhaengung des Verteilers an den Boecken (Rohrschellen) nicht modelliert
- Eckengehrung/Zehneck-Lage und Azimut vom Integrator (Ring)
- Halteclips und Verteiler sind Annahmen [A]; Statik des Tisches nicht nachgewiesen
- Aussen 3 Rinnen (OBJ 2) als Annahme
- Rinnenabstand 262-288 (OBJ) bei Rinnenbreite 130 laesst 132-158 mm Luecken; ref-6 zeigt fast buendige Rinnen: Widerspruch OBJ/Bild, OBJ gilt (provenance), beim Orchestrator/Ben nachfragen
- Schlaeuche gerade statt gebogen (Zwischenbauteil, Montage-Sitzung), Kopfplatten/Winkelhalter an den Beinkoepfen nicht modelliert
- STANDORT DER BEINE (components.md Z.44): Fusspunkte liegen auf Z=0 des Bauteils; die Innentische (Apothem 1733-1995) liegen ueber dem Pool (Wasserradius 1945): ihre Beine stuenden im Wasser -> Stuetzung des Innenrings (Ausleger/Konsole am Beckenrand oder Beine ausserhalb) ist OFFEN, Entscheidung beim Orchestrator/Integrator; Aussen/Mitte: Beine neben den Beeten auf dem Boden (Beinabstand siehe Ports), Kollision mit den Beeten vom Integrator zu pruefen
- Gefaelle: detail-standard.md und Scope-Card nennen noch 1 cm/m, gebaut 1,5 % nach R06 (Orchestrator-Vorgabe)
- Wasserfilm 10 mm ist ein Rinnenmerkmal (Blatt nft_rinne)
