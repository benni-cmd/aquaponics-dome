# Bauteilblatt T82 puffer_klein (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/puffer_klein.json` und `designs/components/puffer_klein.sc`, nicht von Hand aendern)

**Funktion:** Kleiner Puffer (R37 Option A): 120-l-Fass opak fuer die Stammloesung (Base: KOH/NaHCO3, R37 Befund 8), Messzelle 20 l (Messkreis 3 l/min, 4 Sondenstutzen d25, Ablauf zum Pool), Eisenchelat-Kanister 20 l, zwei Schlauchpumpen (Dosierung Base und Eisen). Der Regalboden traegt Messzelle, Kanister und Pumpen ueber dem Fass; das Fass wird nach vorn herausgezogen. Entchlortes Frischwasser ist eine Quelle (Aktivkohle oder Zisterne), kein Volumen im Dom.

**Datei:** `designs/components/puffer_klein.sc` · **Teilenummer:** T82 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche am Boden (Z 0); X: Messzelle -X, Kanister +X; Y: vorn -Y (Pumpen, Fass wird nach vorn herausgezogen), hinten +Y (Ablauf, Kabel); Z hoch

**Anzahl (Instanzen):** 1 Puffer klein im Dom (Quelle: R37 Option A, D66; Platzierung Montage (Laufwegkarte, place_m8.py))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `fass_d` | 500 | mm | [E] R37 Befund 7: 120-l-Weithals-/Deckelfass HDPE Ø 470-500 x 795-800 mm, 6 kg, lebensmittelecht lt. Haendler (toom/GRAF, Kaufland, denios Ø 496 x 800); Auftrag W34: Ø 500 x 800 |
| `fass_h` | 800 | mm | [E] R37 Befund 7 (795-800 mm), inklusive Deckel |
| `fass_wall` | 3 | mm | [A] Wandstaerke HDPE-Fass (kein Datenblatt gelesen) |
| `fass_floor` | 4 | mm | [A] Bodenstaerke HDPE-Fass |
| `fass_lid_t` | 12 | mm | [A] Deckel mit Spannring, Oberkante = Fasshoehe 800 |
| `fass_nenn_l` | 120 |  | [E] R37 Befund 1/7: Stammloesungsfass 120 l; Fuellmarke 120 l bei Z 630 (Innenzylinder, Rechnung im Check), der modellierte Zylinder fasst bis zum Deckel mehr |
| `fass_cx` | 0 | mm | [A] Fass mittig im Stand (Spiel zu den Pfosten 45 mm je Seite) |
| `fass_cy` | 0 | mm | [A] |
| `entn_z` | 60 | mm | [A] Entnahmestutzen (Kugelhahn-Stutzen R3/4, vereinfacht d25 mit Bohrung d16) seitlich unten, +X; Spitze x 285 |
| `stu_od` | 25 | mm | [A] Stutzen d25 (R37: Sondenhalter d25, Ablauf zum Pool) |
| `stu_id` | 16 | mm | [A] Bohrung der Stutzen (Schlauch ID 16 wie NFT-Verteiler) |
| `einf_od` | 32 | mm | [A] Einfuellstutzen im Deckel (Frischwasser zum Ansetzen der Stammloesung, Quelle: entchlortes Nachfuellwasser R37 Befund 3) |
| `einf_h` | 35 | mm | [A] Einfuellstutzen Hoehe ueber dem Deckel |
| `regal_z` | 898 | mm | [A] Oberkante Regalboden: 98 mm ueber dem Fassdeckel (800) fuer Spannring und Deckelabnahme nach vorn (Fass wird nach vorn herausgezogen, Vorderseite ohne Querriegel) |
| `zelle_ix` | 280 | mm | [R] Messzelle Innenmass 280 x 280 x 255 = 20,0 l (R37 Befund 1: 20 l reichen, 6,7 min Verweilzeit bei 3 l/min) |
| `zelle_iy` | 280 | mm | [R] |
| `zelle_ih` | 255 | mm | [R] |
| `zelle_wall` | 5 | mm | [A] Acryl (PMMA) 5 mm; R37 Befund 6: Acryl hat die beste UV-Beständigkeit (ca. 3 % Durchlassverlust in 10 Jahren); Lebensmittelaussage zu Acryl nicht gefunden |
| `zelle_cx` | -175 | mm | [A] Lage auf dem Regalboden (links hinten) |
| `zelle_cy` | 170 | mm | [A] |
| `zelle_zulauf_z` | 30 | mm | [A] Zulauf Messkreis (Tuelle d20, ID 16) 30 mm ueber dem Zellboden, Seite -X |
| `zelle_ablauf_z` | 235 | mm | [A] Ablauf zum Pool (d25) 235 mm ueber dem Zellboden: Wasserstand bis Unterkante Ablauf 222 mm = 17,4 l = 5,8 min bei 3 l/min (R37: 20 l = 6,7 min bei voller Zelle; Ablaufhoehe ist Annahme), Oberkante Stutzen 248 mm, 7 mm Luft zum Deckel |
| `halter_od` | 25 | mm | [E] R37/Auftrag: Stutzen fuer 4 Sondenhalter d25 im Deckel der Messzelle (Sondenliste liefert R39, W35) |
| `halter_id` | 16 | mm | [A] Bohrung fuer Sonde mit Kabelverschraubung (Sondenfabrikate offen) |
| `halter_h` | 40 | mm | [A] Stutzenhoehe ueber dem Deckel |
| `halter_pitch` | 110 | mm | [A] Raster der 4 Stutzen (2 x 2, +-55 um die Zellmitte) |
| `blende_t` | 3 | mm | [A] Lichtschutz-Blende vorn (PP schwarz), abdeckbar laut R37 Befund 5; Seiten und Rueckseite nicht abgedeckt (offen) |
| `kan_l` | 250 | mm | [A] Kanister 20 l: 250 x 300 x 285 (puffer_station: 250 x 300 x 280); Innenvolumen 244 x 294 x 279 = 20,0 l |
| `kan_w` | 300 | mm | [A] |
| `kan_h` | 285 | mm | [A] |
| `kan_wall` | 3 | mm | [A] Wand HDPE-Kanister |
| `kan_cx` | 190 | mm | [A] Lage auf dem Regalboden (rechts hinten) |
| `kan_cy` | 175 | mm | [A] |
| `kap_d` | 60 | mm | [A] Schraubdeckel des Kanisters |
| `kap_h` | 20 | mm | [A] |
| `pump_l` | 140 | mm | [A] Schlauchpumpe 140 x 120 x 100 (puffer_station, Pumpenmasse Annahme) |
| `pump_w` | 120 | mm | [A] |
| `pump_h` | 100 | mm | [A] |
| `pump_x` | 190 | mm | [A] Pumpen in der vorderen Reihe auf dem Regalboden: Base-Pumpe x -190, Eisen-Pumpe x +190 |
| `pump_y` | -240 | mm | [A] Mitte der vorderen Reihe (Pumpen y -300 bis -180) |
| `tuelle_od` | 12 | mm | [A] Dosierschlauch 6/9 (ID 6, AD 9) auf Tuelle d12 |
| `tuelle_len` | 20 | mm | [A] Tuellenlaenge ab Pumpengehaeuse |
| `stand_w` | 700 | mm | [E] Auftrag W34: max. 0,7 x 0,7 m ohne Mensch; Regalboden und Fussplattenaussenkanten = Grundflaeche |
| `leg_w` | 30 | mm | [A] Pfosten und Riegel Rechteckrohr 30 x 30 x 2 verzinkt (Last auf dem Regal ca. 60 kg, Statik nicht gerechnet) |
| `leg_wall` | 2 | mm | [A] |
| `leg_pos` | 310 | mm | [A] Pfostenmitte x/y +-310: Pfostenaussenkante 325, Innenkante 295 (Fass Ø 500 hat 45 mm Spiel) |
| `foot` | 80 | mm | [A] Fussplatte 80 x 80 x 6, aussen buendig mit 350 |
| `foot_t` | 6 | mm | [A] |
| `rail_z` | 880 | mm | [A] Mitte der oberen Riegel (Oberkante 895 = Unterkante Regalboden) |
| `low_rail_z` | 150 | mm | [A] untere Riegel links, rechts und hinten (Vorderseite frei fuer das Fass) |
| `plate_t` | 3 | mm | [A] Regalboden Stahlblech verzinkt 3 mm, 700 x 700, mit Querriegel y 0 unterstuetzt |
| `rim_h` | 20 | mm | [A] Auffangrand 20 mm, 3 mm stark, rundum auf dem Regalboden (Lauge/Chelat-Leckage) |
| `rim_t` | 3 | mm | [A] |
| `kabel_od` | 20 | mm | [A] Kabelverschraubung M20 (PA schwarz) am hinteren oberen Riegel, nach +Y |
| `hoehe_max` | 1300 | mm | [E] Auftrag W34: Hoehe unter 1,3 m |

Gesamt-Box (Messung): X -350.0 bis 350.0, Y -350.0 bis 350.0, Z -0.0 bis 1203.0 mm; Koerper: 32.

**Toleranzen / Spiel:** Fass 45 mm Spiel zu den Pfosten, 65 mm bis zur Riegel-Unterkante; Fassdeckel 98 mm unter dem Regalboden; Messzelle, Kanister und Pumpen liegen innerhalb des Auffangrands (innen 347 mm); Hoehe gesamt unter 1300 mm.

## Werkstoff und Gewicht

- Werkstoff: Stahl verzinkt (Stand), HDPE (Fass, Kanister), Acryl (Messzelle), Dichte 7.85 g/cm3, Farbe #aeb4b8 ([A]; HDPE opak blau (Algen: R37 Befund 5), Acryl klar)
- Volumen (Messung, `solidcraft-cli eval`): 17749.3 cm3 · Masse leer: 43829 g (43.83 kg)
- Gefuellt/in Betrieb: Fass 120 l, Messzelle 20 l, Kanister 20 l Flüssigkeit: zusammen ca. 160 kg zusaetzlich zur Leermasse [E, Dichte 1]; Regalboden traegt Messzelle + Kanister + Pumpen ca. 45 kg gefuellt [A, Statik nicht gerechnet]

## Querschnitt / Profil

Stand: 4 Pfosten und 8 Riegel Rechteckrohr 30 x 30 x 2 (obere Riegel Z 865-895 an allen Seiten und quer bei y 0, untere Riegel Z 135-165 links, rechts, hinten), Fussplatten 80 x 80 x 6, Regalboden 700 x 700 x 3 mit 20-mm-Auffangrand. Fass Ø 500 x 800 (Wand 3, Boden 4, Deckel 12) steht auf dem Boden. Messzelle Acryl 5 mm (aussen 290 x 290 x 260), Deckel 5 mm, Blende 3 mm vorn. Kanister 250 x 300 x 285 (Wand 3).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Messkreis Zulauf (Messzelle, 3 l/min) | Tuelle d20, ID 16 | x -345, y 170, z 933 | -X |
| Ablauf Messzelle -> Pool | Stutzen d25, ID 16 | x -175, y 340, z 1138 | +Y |
| Sondenstutzen 1 (Deckel Messzelle) | d25, Bohrung 16 (Sondenhalter, Liste R39/W35) | x -230, y 115, z 1203 | +Z |
| Sondenstutzen 2 (Deckel Messzelle) | d25, Bohrung 16 (Sondenhalter, Liste R39/W35) | x -120, y 115, z 1203 | +Z |
| Sondenstutzen 3 (Deckel Messzelle) | d25, Bohrung 16 (Sondenhalter, Liste R39/W35) | x -230, y 225, z 1203 | +Z |
| Sondenstutzen 4 (Deckel Messzelle) | d25, Bohrung 16 (Sondenhalter, Liste R39/W35) | x -120, y 225, z 1203 | +Z |
| Frischwasser / Ansetzen (Einfuellstutzen Fass) | d32, Bohrung 25 | x 0, y -120, z 835 | +Z |
| Entnahme Stammloesung (Fass -> Pumpe Base) | Stutzen d25, ID 16 | x 285, y 0, z 60 | +X |
| Saug Base (Pumpe Base, aus dem Fass) | Tuelle d12 (Schlauch 6/9) | x -190, y -160, z 948 | +Y |
| Dosierleitung Base (Pumpe Base, Druckseite -> Pool) | Tuelle d12 (Schlauch 6/9) | x -190, y -320, z 948 | -Y |
| Saug Eisen (Pumpe Eisen, aus dem Kanister) | Tuelle d12 (Schlauch 6/9) | x 190, y -160, z 948 | +Y |
| Dosierleitung Eisen (Pumpe Eisen, Druckseite -> Pool) | Tuelle d12 (Schlauch 6/9) | x 190, y -320, z 948 | -Y |
| Kabel (Netz 230 V, Sonden, Steuerung) | Kabelverschraubung M20 | x 0, y 345, z 880 | +Y |

## Verbindungen und Befestigungen

- Stand: Pfosten an Fussplatten geschweisst, Riegel an die Pfosten geschweisst, danach verzinkt [A]; Regalboden auf die oberen Riegel geschraubt (nicht modelliert)
- Messzelle: Deckel aufgelegt (Dichtung/Schrauben nicht modelliert), Tuellen und Stutzen angeklebt (Acryl-Klebstoff) [A]; Blende liegt vorn an, Scharnier nicht modelliert
- Fass: Spannringdeckel (nicht modelliert), Entnahmestutzen und Einfuellstutzen angeschweisst bzw. verschraubt [A]; Fass steht frei, Wegrutschen am Regalboden nicht gesichert (offen)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Fass 120 l HDPE opak Ø 500 x 800, Deckel, Entnahmestutzen | Ø 500 x 800 | E | R37 Befund 7 (toom/GRAF, Kaufland, denios); opak wegen Algen (Befund 5) | mittel |
| Messzelle 20 l Acryl, abdeckbar, 4 Sondenstutzen d25 | 280 x 280 x 255 innen | R + E | R37 Befund 1 (20 l, 6,7 min bei 3 l/min), Befund 5/6 (transparent nur Messzelle, abdeckbar; Acryl); Stutzenzahl aus dem Auftrag W34 | mittel |
| Eisenchelat-Kanister 20 l | 250 x 300 x 285 | E + A | R37 Befund 1 (74 g Fe alle 3 Wochen); Mass aus puffer_station (Kanister 250 x 300 x 280) | niedrig |
| 2 Schlauchpumpen 140 x 120 x 100 (Dosierung Base und Eisen) | 2 Stueck | E + A | R37 Befund 8/9; Pumpenmasse Annahme aus puffer_station | niedrig |
| Stand 700 x 700, Hoehe 1203, Regalboden auf Z 898 | 0,49 m2 | E + A | Auftrag W34: Raster max 0,7 x 0,7 m, Hoehe < 1,3 m; R37 Befund 11: etwa 0,4 m2 Raster (Summe der Einzelflaechen 0,39 m2) | mittel |
| Pumpe Strom 11,5 W der Station (A) | 11,5 W | E | R37 Befund 9 (Messkreis 1,5 m Foerderhoehe, Umpumpen entfaellt) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R37.md (Befund 1, 5, 6, 7, 9, 11; Option A), docs/parts/puffer_station.md (Ports, Pumpen- und Kanistermasse)
- Abweichung zum OBJ: Keine OBJ-Vorgabe; Konzept der Werkstatt nach R37 Option A (D66). Gegenueber der Station T81 (2420 x 1920 x 2445 mm, 4,65 m2): 0,49 m2 Grundflaeche, 1,2 m Hoehe; Messplatz und Dosierkonsole der Station entfallen als eigene Gestelle.

## Montage (L4)

1. Stand aufstellen, Fussplatten am Boden verschrauben, Regalboden auflegen und verschrauben
2. Fass von vorn einschieben, Entnahmestutzen nach +X, Einfuellstutzen oben
3. Messzelle, Kanister und die beiden Pumpen auf den Regalboden stellen, Schlaeuche aufstecken, Kabel durch die Verschraubung hinten

**Werkzeug:** Schweissgeraet oder Winkelverbinder, Schluesselsatz, Schlauchschneider, Wasserwaage

## Stueckliste-Zeile

- T82 Puffer klein: Stand (4 Pfosten 30x30x2, 8 Riegel, 4 Fussplatten 80x80x6, Regalboden 700x700x3, Auffangrand), 1 Fass 120 l HDPE mit Deckel, 1 Messzelle 20 l Acryl mit Deckel, Blende und 4 Sondenstutzen, 1 Kanister 20 l mit Schraubdeckel, 2 Schlauchpumpen, 1 Kabelverschraubung M20

## Alternative lokale Fertigung

Stand aus Baustahl-Rechteckrohr (Metallbauer, Kaltverzinken) oder Aluprofil-System; Messzelle aus PMMA-Platten 5 mm geklebt (Kunststoffhandel) oder transparenter Lebensmittelbehaelter 20 l; Fass und Kanister aus dem Handel (R37).

## Renders


## Pruefung

- Gauntlet-Urteil: Kein Pruefer-Lauf (Auftrag W34: Selbstcheck).
- scripts/workshop/check_puffer_klein.py (Ergebnis renders/components/puffer_klein/check.txt): Fass Ø/Hoehe/Masse, Innenvolumen Messzelle 20 l und Kanister 20 l, Grundflaeche <= 700 x 700, Hoehe < 1300, Ports (Lage und Richtung), Interferenz 0

## Offene Fragen

- Statik von Regalboden und Pfosten (ca. 60 kg auf 4 Pfosten 30x30x2, Regalboden 3 mm mit Querriegel) nicht gerechnet [A]
- Lichtschutz der Messzelle: nur Blende vorn modelliert, Seiten und Rueckseite nicht abgedeckt; ob 7 min Verweilzeit ohne Abdeckung reichen, ist Annahme (R37 Befund 5)
- Fass modelliert als Zylinder: Innenvolumen bis zum Deckel groesser als 120 l, Fuellmarke 120 l bei Z 630; reale Fass-Rippen und Spannring nicht modelliert
- Fass und Kanister: Konformitaetserklaerung EU 10/2011 des konkreten Fabrikats fehlt (R37 Befund 7)
- Sondenliste und Sondenmasse liefert R39 (Auftrag W35): die 4 Stutzen d25 sind Ports, keine Sonden modelliert
- Leitungsplan K35-K41 und Platzierung im Dom (Messzelle neben dem Verteiler): Montage; Schlaeuche sind Platzhalter (nur Tuellen modelliert)
- Frischwasserquelle (Aktivkohle oder Zisterne): Versorger fragen (Chlor/Chloramin), Entscheidung Ben (R37)
