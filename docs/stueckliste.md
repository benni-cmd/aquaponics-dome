# Stueckliste (erzeugt, nicht von Hand)

Erzeugt von `scripts/bom.py` aus dem Modellstand (`viewer/instances.json` built 2026-11-11 04:31:07, sc_sha256 8a336512b16ced32). Preise brutto, Richtwerte mit Datum, keine Angebote. Quelle der Preise: `data/beschaffung/*.json`.

## Kopf

1. Zeilen: 345 (Preis fehlt bei 110 platzierten, 154 Zeilen nur in nicht platzierten Komponenten)
2. Summe der Zeilen mit Preis (platziert): 39.097,43 EUR
2b. Nicht platzierte Komponenten (ohne lt_-Bibliothek), je 1 Stueck gerechnet, 42 Zeilen mit Preis: 3.505,02 EUR (nicht in der Summe, Entscheidung offen)
3. Instanzen im Modell: 5335 in 179 Definitionen
4. Unbenannte Koerper (Body<n>) in der Messung: 0, davon per Regel benannt: 0, ungeklaert: 0

## Summe je Typ

| Typ | Bedeutung | Summe |
|---|---|---|
| ARM | Armatur (Kugelhahn, Ventil, Bulkhead, Durchfuehrung) | 3.832,05 EUR |
| BEH | Behaelter und Becken | 3.973,21 EUR |
| BLE | Blech, Platte, Lochblech, Zuschnitt | 6.760,67 EUR |
| ELE | Elektrik (Schaltschrank, Kabel, Hutschiene) | 470,86 EUR |
| FIT | Fitting (Bogen, T, Reduzierung, Kupplung, Stutzen, Kappe) | 1.112,93 EUR |
| FOL | Folie, Plane, Dichtband, Dichtung | 2.331,73 EUR |
| MES | Messtechnik (Sonden, Sensoren) | 1.583,94 EUR |
| PMP | Pumpe und Geblaese | 2.673,70 EUR |
| PRF | Stahlprofil (Rechteck-, Vierkantrohr, Rund- und Vollmaterial) | 6.656,35 EUR |
| ROH | PVC-U-Rohr (Meterware) | 5.504,40 EUR |
| SCH | Schlauch, Schelle, Tuelle | 270,06 EUR |
| SON | Sonderteil (Eigenbau mit Rohmaterial als Kaufteil, Tuer, Haut, Knoten) | 788,59 EUR |
| SRB | Schraube, Mutter, Scheibe, Bolzen | 106,20 EUR |
| TOP | Topf und Substrat | 2.480,60 EUR |
| WNK | Winkel und Flachstahl, Halter | 552,14 EUR |

## Summe je Bauteilgruppe

| Gruppe | Summe |
|---|---|
| Becken und Tanks | 4.567,73 EUR |
| Filter | 140,78 EUR |
| Fundament | 323,20 EUR |
| Huelle | 3.180,29 EUR |
| Kuppel | 8.598,14 EUR |
| Leitungen | 8.851,43 EUR |
| Messtechnik und Elektrik | 2.172,62 EUR |
| Tische und Beete | 11.263,24 EUR |

## Nicht in der Liste (Ausnahmen)

| Grund | Koerper | Masse (kg, mit Instanzen) |
|---|---|---|
| Aushub und Erde (Entscheidung 04.11.2026) | 1 | 1183083.09 |
| Beton nach Menge (Entscheidung 04.11.2026) | 3 | 9048.67 |
| Massfigur, kein Bauteil | 43 | 160.2 |
| Mutter/Scheibe im Schraubensatz enthalten | 492 | 4.01 |
| Pflanze (Salat), nicht kaufbar | 98 | 59.0 |
| Teil eines Hahns (Griff/Spindel/Hebel) im Hahn-Artikel enthalten | 9 | 0.09 |
| Wasserkoerper, kein Bauteil | 8 | 38756.37 |

## PRF Stahlprofil (Rechteck-, Vierkantrohr, Rund- und Vollmaterial)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `PRF-alu-haut-profil` | Alu-Kappenprofil der Haut | nicht platziert (je 1: 3.279) | 0.0 m | 4.39/m | 0,00 EUR | OK |
| `PRF-alu-keilschiene` | Alu-Keilschiene (Kanal 25x15) | nicht platziert (je 1: 3.019) | 0.0 m | 7.32/m | 0,00 EUR | OK |
| `PRF-alu-klemmleiste` | Alu-Klemmleiste Zarge | nicht platziert (je 1: 2.043) | 0.0 m | 3.29/m | 0,00 EUR | OK |
| `PRF-pvcu-rinne-130x100` | NFT-Rinnenprofil PVC-U 130x100 (Meterware, Lagerlaenge offen) | 147.924 m | 154.0 m (22 x 7000 mm) | 7.16/m | 1.102,64 EUR | OK |
| `PRF-st-rr20x40x2.5` | Rechteckrohr 20x40x2.5 mm, Stahl verzinkt | 10.84 m | 12.0 m (2 x 6000 mm) | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-st-rr25x25x2` | Vierkantrohr 25x25x2 mm, Stahl verzinkt | nicht platziert (je 1: 8.82) | 0.0 m | 5.47/m | 0,00 EUR | OK |
| `PRF-st-rr30x30x2` | Vierkantrohr 30x30x2 mm, Stahl verzinkt | 24.876 m | 26.0 m (4 x 6500 mm) | 6.65/m | 172,90 EUR | OK |
| `PRF-st-rr35x600x0.5` | Rechteckrohr 35x600x0.5 mm, Stahl verzinkt | nicht platziert (je 1: 0.6) | 0.0 m | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-st-rr40x40x2` | Vierkantrohr 40x40x2 mm, Stahl verzinkt | nicht platziert (je 1: 14.104) | 0.0 m | 9.04/m | 0,00 EUR | OK |
| `PRF-st-rr40x40x2.5` | Vierkantrohr 40x40x2.5 mm, Stahl verzinkt | 161.888 m | 168.0 m (24 x 7000 mm) | 12.65/m | 2.125,20 EUR | OK |
| `PRF-st-rr40x40x3` | Vierkantrohr 40x40x3 mm, Stahl verzinkt | 40.795 m | 44.0 m (11 x 4000 mm) | 12.65/m | 556,60 EUR | OK |
| `PRF-st-rr40x60x3` | Rechteckrohr 40x60x3 mm, Stahl verzinkt | 29.596 m | 32.5 m (5 x 6500 mm) | 16.26/m | 528,45 EUR | OK |
| `PRF-st-rr41x41x2` | Vierkantrohr 41x41x2 mm, Stahl verzinkt | 21.79 m | 28.0 m (4 x 7000 mm) | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-st-rr42x109x1` | Rechteckrohr 42x109x1 mm, Stahl verzinkt | nicht platziert (je 1: 0.252) | 0.0 m | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-st-rr42x118x1` | Rechteckrohr 42x118x1 mm, Stahl verzinkt | nicht platziert (je 1: 0.502) | 0.0 m | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-st-rr50x50x3` | Vierkantrohr 50x50x3 mm, Stahl verzinkt | 5.076 m | 6.0 m (1 x 6000 mm) | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-st-rr60x60x3` | Vierkantrohr 60x60x3 mm, Stahl verzinkt | nicht platziert (je 1: 10.808) | 0.0 m | 19.76/m | 0,00 EUR | OK |
| `PRF-st-rund20` | Rundstahl 20 mm, Stahl verzinkt | nicht platziert (je 1: 2.35) | 0.0 m | 11.25/m | 0,00 EUR | OK |
| `PRF-st-strebe30x30` | Strebenprofil 30x30 (Kuppelstrebe, Profil und Wand offen: N-STATIK V1/V2c) | 211.446 m | 238.0 m (34 x 7000 mm) | 9.12/m | 2.170,56 EUR | OK |
| `PRF-st-voll40x40` | Vierkant-/Flachstahl voll 40x40 mm, Stahl verzinkt | 30.04 m | 31.5 m (9 x 3500 mm) | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-st-voll6x100` | Vierkant-/Flachstahl voll 6x100 mm, Stahl verzinkt | 3.2 m | 3.5 m (1 x 3500 mm) | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-v2a-voll8x8` | Vierkant-/Flachstahl voll 8x8 mm, Edelstahl 1.4301 | nicht platziert (je 1: 3.384) | 0.0 m | 6.12/m | 0,00 EUR | OK |

## WNK Winkel und Flachstahl, Halter

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `WNK-flach-14x3` | Flachstahl 14x3 (Tuer-Anschlag) | 5.004 m | 6.0 m (1 x 6000 mm) | 2.85/m | 17,10 EUR | OK |
| `WNK-flach-3mm-diagonale` | Flachstahl 3 mm (Diagonalen, Breite aus Modell nicht ableitbar, Zuschnitt) | 110.0 Stk | 110 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (m), Umrechnung offen |
| `WNK-pumpenkonsole` | Pumpenkonsole/Standwinkel (Stahl, Zuschnitt) | nicht platziert (je 1: 6.0) | 0 Stk | 1.25/Stk | 0,00 EUR | OK |
| `WNK-rinnenhalter-25` | Rinnenhalter 25x25 (Stahl, Zuschnitt/Kleinteil) | 304.0 Stk | 304 Stk | 1.56/Stk | 474,24 EUR | OK |
| `WNK-wandlasche-30x30x3` | Wandlasche 30x30x3 | nicht platziert (je 1: 2.0) | 0 Stk | 1.13/Stk | 0,00 EUR | OK |
| `WNK-winkel-36x60x60` | Winkel 36x60x60 (Rinnen-Winkelhalter, Stahl) | 76.0 Stk | 76 Stk | 0.8/Stk | 60,80 EUR | OK |

## BLE Blech, Platte, Lochblech, Zuschnitt

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `BLE-blech-st-10` | Stahlblech 10 mm verzinkt, Zuschnitt 200x200 | 3.0 Stk | 3 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BLE-blech-st-3` | Stahlblech 3 mm verzinkt, Zuschnitt 700x700 | 5.0 Stk | 5 Stk | 35.96/Stk | 179,80 EUR | OK |
| `BLE-blech-st-4` | Stahlblech 4 mm verzinkt, Zuschnitt 40x40 | 31.0 Stk | 31 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BLE-blech-st-5` | Stahlblech 5 mm verzinkt, Zuschnitt 840x400 | nicht platziert (je 1: 2.0) | 0 Stk | 39.99/Stk | 0,00 EUR | OK |
| `BLE-blech-st-6` | Stahlblech 6 mm verzinkt, Zuschnitt 100x100 | 56.0 Stk | 56 Stk | 106.74/Stk | 5.977,44 EUR | OK |
| `BLE-blech-st-8` | Stahlblech 8 mm verzinkt, Zuschnitt 100x40 | 66.0 Stk | 66 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BLE-fussplatte-100x100x6` | Fussplatte Stahl verzinkt 100x100x6 mm | 32.0 Stk | 32 Stk | 4.32/Stk | 138,24 EUR | OK |
| `BLE-fussplatte-150x150x8` | Fussplatte Stahl verzinkt 150x150x8 mm | nicht platziert (je 1: 2.0) | 0 Stk | 4.79/Stk | 0,00 EUR | OK |
| `BLE-fussplatte-200x200x8` | Fussplatte Stahl verzinkt 200x200x8 mm | nicht platziert (je 1: 1.0) | 0 Stk | 8.52/Stk | 0,00 EUR | OK |
| `BLE-fussplatte-70x70x5` | Fussplatte Stahl verzinkt 70x70x5 mm | 76.0 Stk | 76 Stk | 1.65/Stk | 125,40 EUR | OK |
| `BLE-fussplatte-80x80x6` | Fussplatte Stahl verzinkt 80x80x6 mm | 4.0 Stk | 4 Stk | 3.84/Stk | 15,36 EUR | OK |
| `BLE-fussplatte-80x80x8` | Fussplatte Stahl verzinkt 80x80x8 mm | nicht platziert (je 1: 8.0) | 0 Stk | 1.36/Stk | 0,00 EUR | OK |
| `BLE-laser-lochplatte-110x110x8` | Laserteil Lochplatte 110x110x8 mm, Stahl (Knoten Schere) | 52.0 Stk | 52 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BLE-platte-250x250x15` | Ankerplatte 250x250x15 mm, Stahl | 10.0 Stk | 10 Stk | 32.32/Stk | 323,20 EUR | OK |
| `BLE-pp-abtropfgitter-beet` | PP-Abtropfgitter 25 mm (Stegrost, Zuschnitt je Beet) [A] | 14.0 Stk | 14 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BLE-pp-blende-290x260` | PP-Blende 290x260x3 (Messzelle) | 1.0 Stk | 1 Stk | 1.23/Stk | 1,23 EUR | OK |
| `BLE-pp-platte10-210x1125` | PP-Platte 10 mm, Zuschnitt 1125x210 (Trennwand, Pufferzone) | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BLE-pp-platte10-360x1125` | PP-Platte 10 mm, Zuschnitt 1125x360 (Trennwand, Pufferzone) | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BLE-pp-platte30-400x400` | PP-Platte 30 mm, Zuschnitt 400x400 (Pumpensockel) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BLE-pp-tafel-502x345x5` | PP-Montagetafel 502x345x5 (Zuschnitt) | nicht platziert (je 1: 1.0) | 0 Stk | 4.74/Stk | 0,00 EUR | OK |
| `BLE-pp-tafel-693x463x7` | PP-Montagetafel 693x463x7 (Zuschnitt) | nicht platziert (je 1: 1.0) | 0 Stk | 13.94/Stk | 0,00 EUR | OK |
| `BLE-schrankboden-3x500x800` | Stahlblech 3 mm, Zuschnitt 800x500 (Schrankboden) [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BLE-v2a-3mm-korbflansch` | Edelstahlblech 3 mm 1.4301, Zuschnitt 604x414 (Korbflansch) | nicht platziert (je 1: 1.0) | 0 Stk | 94.2/Stk | 0,00 EUR | OK |

## ROH PVC-U-Rohr (Meterware)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `ROH-leerrohr-dn100` | Leerrohr DN100 (Kabelschutz, Meterware) | nicht platziert (je 1: 3.0) | 0.0 m | 3.85/m | 0,00 EUR | OFFEN (E20) |
| `ROH-leerrohr-dn50` | Leerrohr DN50 (Kabelschutz, Meterware) | nicht platziert (je 1: 3.0) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ROH-pvcu-d110` | PVC-U-Druckrohr d110 (Meterware) | 6.286 m | 10.0 m (2 x 5000 mm) | 79.83/m | 798,30 EUR | OFFEN (E20) |
| `ROH-pvcu-d16` | PVC-U-Druckrohr d16 (Meterware) | 2.538 m | 5.0 m (1 x 5000 mm) | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ROH-pvcu-d160` | PVC-U-Druckrohr d160 (Zulaufrohr, Meterware, Laenge aus Bbox [E]) | 4.403 m | 5.0 m (1 x 5000 mm) | 81.47/m | 407,35 EUR | OFFEN (Quelle) |
| `ROH-pvcu-d20` | PVC-U-Druckrohr d20 (Meterware) | 99.9639 m | 105.0 m (21 x 5000 mm) | 4.77/m | 500,85 EUR | OFFEN (E20) |
| `ROH-pvcu-d25` | PVC-U-Druckrohr d25 (Meterware) | 38.133 m | 40.0 m (8 x 5000 mm) | 5.19/m | 207,60 EUR | OFFEN (E20) |
| `ROH-pvcu-d32` | PVC-U-Druckrohr d32 (Meterware) | 1.296 m | 5.0 m (1 x 5000 mm) | 10.22/m | 51,10 EUR | OFFEN (E20) |
| `ROH-pvcu-d40` | PVC-U-Druckrohr d40 (Meterware) | 3.868 m | 5.0 m (1 x 5000 mm) | 15.41/m | 77,05 EUR | OFFEN (E20) |
| `ROH-pvcu-d50` | PVC-U-Druckrohr d50 (Meterware) | 64.185 m | 65.0 m (13 x 5000 mm) | 23.66/m | 1.537,90 EUR | OFFEN (E20) |
| `ROH-pvcu-d63` | PVC-U-Druckrohr d63 (Meterware) | 30.225 m | 35.0 m (7 x 5000 mm) | 35.95/m | 1.258,25 EUR | OFFEN (E20) |
| `ROH-pvcu-d75` | PVC-U-Druckrohr d75 (Meterware) | 13.593 m | 15.0 m (3 x 5000 mm) | 44.4/m | 666,00 EUR | OFFEN (E20) |

## FIT Fitting (Bogen, T, Reduzierung, Kupplung, Stutzen, Kappe)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `FIT-bogen45-d110` | PVC-U-Bogen 45 Grad d110 | nicht platziert (je 1: 1.0) | 0 Stk | 37.52/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d20` | PVC-U-Bogen 45 Grad d20 | nicht platziert (je 1: 1.0) | 0 Stk | 2.38/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d25` | PVC-U-Bogen 45 Grad d25 | nicht platziert (je 1: 1.0) | 0 Stk | 2.38/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d32` | PVC-U-Bogen 45 Grad d32 | nicht platziert (je 1: 1.0) | 0 Stk | 2.63/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d40` | PVC-U-Bogen 45 Grad d40 | nicht platziert (je 1: 1.0) | 0 Stk | 3.69/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d50` | PVC-U-Bogen 45 Grad d50 | nicht platziert (je 1: 1.0) | 0 Stk | 4.76/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d63` | PVC-U-Bogen 45 Grad d63 | nicht platziert (je 1: 1.0) | 0 Stk | 7.29/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d75` | PVC-U-Bogen 45 Grad d75 | nicht platziert (je 1: 1.0) | 0 Stk | 11.91/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen90-d110` | PVC-U-Bogen 90 Grad d110 | nicht platziert (je 1: 1.0) | 0 Stk | 27.77/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen90-d20` | PVC-U-Bogen 90 Grad d20 | 26.0 Stk | 26 Stk | 1.36/Stk | 35,36 EUR | OFFEN (E20) |
| `FIT-bogen90-d25` | PVC-U-Bogen 90 Grad d25 (Beet-Auslass) | 26.0 Stk | 26 Stk | 1.38/Stk | 35,88 EUR | OFFEN (E20) |
| `FIT-bogen90-d32` | PVC-U-Bogen 90 Grad d32 | nicht platziert (je 1: 1.0) | 0 Stk | 1.76/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen90-d40` | PVC-U-Bogen 90 Grad d40 | nicht platziert (je 1: 1.0) | 0 Stk | 3.01/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen90-d50` | PVC-U-Bogen 90 Grad d50 | 16.0 Stk | 16 Stk | 3.94/Stk | 63,04 EUR | OFFEN (E20) |
| `FIT-bogen90-d63` | PVC-U-Bogen 90 Grad d63 | 11.0 Stk | 11 Stk | 6.06/Stk | 66,66 EUR | OFFEN (E20) |
| `FIT-bogen90-d75` | PVC-U-Bogen 90 Grad d75 | nicht platziert (je 1: 1.0) | 0 Stk | 11.95/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-entlueftung-d32` | Entlueftung d32 (PVC-U, mit Insektengitter-Kappe) [A] | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-gewindenippel-edelstahl` | Gewindenippel Edelstahl (Druckmessstelle) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-kappe-d16` | PVC-U-Kappe d16 | 28.0 Stk | 28 Stk | 1.19/Stk | 33,32 EUR | OFFEN (Quelle) |
| `FIT-kappe-d20` | PVC-U-Kappe d20 | 5.0 Stk | 5 Stk | 1.24/Stk | 6,20 EUR | OFFEN (E20) |
| `FIT-kappe-d25` | PVC-U-Endkappe d25 | 24.0 Stk | 24 Stk | 1.33/Stk | 31,92 EUR | OK |
| `FIT-kappe-d32` | PVC-U-Kappe d32 | 2.0 Stk | 2 Stk | 1.4/Stk | 2,80 EUR | OK |
| `FIT-kappe-d50` | PVC-U-Kappe d50 | 24.0 Stk | 24 Stk | 2.92/Stk | 70,08 EUR | OFFEN (E20) |
| `FIT-kupplung-d110` | PVC-U-Kupplung (Muffe) d110 | nicht platziert (je 1: 1.0) | 0 Stk | 19.34/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d20` | PVC-U-Kupplung (Muffe) d20 | nicht platziert (je 1: 1.0) | 0 Stk | 1.19/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d25` | PVC-U-Kupplung (Muffe) d25 | 1.0 Stk | 1 Stk | 1.24/Stk | 1,24 EUR | OFFEN (E20) |
| `FIT-kupplung-d32` | PVC-U-Kupplung (Muffe) d32 | nicht platziert (je 1: 1.0) | 0 Stk | 1.33/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d40` | PVC-U-Kupplung (Muffe) d40 | nicht platziert (je 1: 1.0) | 0 Stk | 1.95/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d50` | PVC-U-Kupplung (Muffe) d50 | nicht platziert (je 1: 1.0) | 0 Stk | 2.38/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d63` | PVC-U-Kupplung (Muffe) d63 | nicht platziert (je 1: 1.0) | 0 Stk | 3.22/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d75` | PVC-U-Kupplung (Muffe) d75 | nicht platziert (je 1: 1.0) | 0 Stk | 8.03/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-leerrohr-bogen45-dn100` | Leerrohr-Bogen 45 Grad dn100 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-bogen45-dn50` | Leerrohr-Bogen 45 Grad dn50 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-bogen90-dn100` | Leerrohr-Bogen 90 Grad dn100 | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-bogen90-dn50` | Leerrohr-Bogen 90 Grad dn50 | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-red-dn100_dn50` | Leerrohr-Reduzierung dn100_dn50 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-t-dn100` | Leerrohr-T-Stueck dn100 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-t-dn50` | Leerrohr-T-Stueck dn50 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-red-d110_d63` | PVC-U-Reduzierung d110_d63 | nicht platziert (je 1: 1.0) | 0 Stk | 10/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d25_d20` | PVC-U-Reduzierung d25_d20 | nicht platziert (je 1: 1.0) | 0 Stk | 0.8/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d32-d25` | PVC-U-Reduzierung d32 auf d25 | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-red-d32_d25` | PVC-U-Reduzierung d32_d25 | nicht platziert (je 1: 1.0) | 0 Stk | 1.38/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d40_d20` | PVC-U-Reduzierung d40_d20 | nicht platziert (je 1: 1.0) | 0 Stk | 1.51/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d40_d32` | PVC-U-Reduzierung d40_d32 | nicht platziert (je 1: 1.0) | 0 Stk | 1.25/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d50-d32` | PVC-U-Reduzierung d50 auf d32 | 24.0 Stk | 24 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-red-d50-d40` | PVC-U-Reduzierung d50 auf d40 | 14.0 Stk | 14 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-red-d50_d32` | PVC-U-Reduzierung d50_d32 | nicht platziert (je 1: 1.0) | 0 Stk | 1.67/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d50_d40` | PVC-U-Reduzierung d50_d40 | nicht platziert (je 1: 1.0) | 0 Stk | 1.73/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d63_d50` | PVC-U-Reduzierung d63_d50 | nicht platziert (je 1: 1.0) | 0 Stk | 2.14/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d75-d50` | PVC-U-Reduzierung d75 auf d50 | 38.0 Stk | 38 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-red-d75_d50` | PVC-U-Reduzierung d75_d50 | nicht platziert (je 1: 1.0) | 0 Stk | 4.09/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d75_d63` | PVC-U-Reduzierung d75_d63 | 10.0 Stk | 10 Stk | 4.09/Stk | 40,90 EUR | OFFEN (E20) |
| `FIT-reduktion-d20` | PVC-U-Reduktion/Huelse d20 | 14.0 Stk | 14 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-ring-ecke-d75` | Ring-Ecke d75 (PE100, Segmentbogen/Formteil fuer den Ring) [A] | 10.0 Stk | 10 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-rinne-kappe-ablauf` | Rinnen-Endkappe Ablauf 130x100 | 76.0 Stk | 76 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-rinne-kappe-zulauf` | Rinnen-Endkappe Zulauf 130x100 | 76.0 Stk | 76 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-sammler-d110` | Sammelleitung (Sammler) d110 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-schlauchanschluss-abzweig` | Schlauchanschluss am Abzweig (Gewinde/Klebe auf Schlauchtuelle) [A] | 38.0 Stk | 38 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-schlauchwinkel-90` | Schlauch-Winkelstueck 90 Grad (PVC, Tuelle-Tuelle) [A] | 31.0 Stk | 31 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-stutzen-d16` | PVC-U-Stutzen d16 (Klebe/Gewinde) | 4.0 Stk | 4 Stk | 1.98/Stk | 7,92 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d20` | PVC-U-Stutzen d20 (Klebe/Gewinde) | 4.0 Stk | 4 Stk | 1.98/Stk | 7,92 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d25` | PVC-U-Stutzen d25 (Klebe/Gewinde) | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-stutzen-d32` | PVC-U-Stutzen d32 (Klebe/Gewinde) | 9.0 Stk | 9 Stk | 2.13/Stk | 19,17 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d40` | PVC-U-Stutzen d40 (Klebe/Gewinde) | 6.0 Stk | 6 Stk | 2.95/Stk | 17,70 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d50` | PVC-U-Stutzen d50 (Klebe/Gewinde) | 6.0 Stk | 6 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-stutzen-d63` | PVC-U-Stutzen d63 (Klebe/Gewinde) | 2.0 Stk | 2 Stk | 5.41/Stk | 10,82 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d75` | PVC-U-Stutzen d75 (Klebe/Gewinde) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-t-d110` | PVC-U-T-Stueck d110 | nicht platziert (je 1: 1.0) | 0 Stk | 35.87/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d20` | PVC-U-T-Stueck d20 | nicht platziert (je 1: 1.0) | 0 Stk | 1.74/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d25` | PVC-U-T-Stueck d25 | 3.0 Stk | 3 Stk | 1.86/Stk | 5,58 EUR | OFFEN (E20) |
| `FIT-t-d32` | PVC-U-T-Stueck d32 | nicht platziert (je 1: 1.0) | 0 Stk | 1.98/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d40` | PVC-U-T-Stueck d40 | nicht platziert (je 1: 1.0) | 0 Stk | 2.92/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d50` | PVC-U-T-Stueck d50 | nicht platziert (je 1: 1.0) | 0 Stk | 4.08/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d63` | PVC-U-T-Stueck d63 | nicht platziert (je 1: 1.0) | 0 Stk | 8.21/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d75` | PVC-U-T-Stueck d75 | 46.0 Stk | 46 Stk | 14.27/Stk | 656,42 EUR | OFFEN (E20) |
| `FIT-uebergang-pe-pvc-pe_pvc_d20` | Uebergang PE auf PVC-U pe_pvc_d20 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-uebergangsnippel-d75-d40` | PVC-U-Uebergangsnippel d75 auf d40 | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-verschraubung-d50` | PVC-U-Verschraubung (Rohrverbinder) | nicht platziert (je 1: 2.0) | 0 Stk | 13.2/Stk | 0,00 EUR | OK |
| `FIT-verschraubung-d75` | PVC-U-Verschraubung (Rohrverbinder) | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-verteiler-d25-nft` | NFT-Verteiler d25 (Zulauf je Rinne, Laenge je Tisch) | 24.0 Stk | 24 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-verteiler-d32_n2` | PVC-U-Verteiler d32_n2 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-verteiler-d32_n3` | PVC-U-Verteiler d32_n3 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-verteiler-d32_n4` | PVC-U-Verteiler d32_n4 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-verteiler-d50` | PVC-U-Verteiler d50 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |

## ARM Armatur (Kugelhahn, Ventil, Bulkhead, Durchfuehrung)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `ARM-anbohrschelle` | Anbohrschelle PVC-U (Messstelle) | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-bulkhead-d20` | PVC-U-Bulkhead d20 | 14.0 Stk | 14 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-bulkhead-d50` | PVC-U-Bulkhead d50 (Tankverbinder, Tankdurchfuehrung) | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-bulkhead-d63` | PVC-U-Bulkhead d63 (Tank-/Behaelterdurchfuehrung) | nicht platziert (je 1: 1.0) | 0 Stk | 49.02/Stk | 0,00 EUR | OFFEN (Quelle) |
| `ARM-bulkhead-pool` | Pool-Durchfuehrung d63 (Stutzen Pool-Wand) | 8.0 Stk | 8 Stk | 49.02/Stk | 392,16 EUR | OFFEN (Quelle) |
| `ARM-durchflussbegrenzer-messing` | Durchflussbegrenzer Messing [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-entlueftungsventil-messing` | Be-/Entlueftungsventil Messing (Rohrleitung, 1 1/2 Zoll) [A] | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-kabeleinfuehrung-dn100` | Kabeleinfuehrung dn100 | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-kabeleinfuehrung-dn50` | Kabeleinfuehrung dn50 | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-kugelhahn-d110` | PVC-U-Kugelhahn d110 | nicht platziert (je 1: 1.0) | 0 Stk | 323.86/Stk | 0,00 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d20` | PVC-U-Kugelhahn d20 | 1.0 Stk | 1 Stk | 23.53/Stk | 23,53 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d25` | PVC-U-Kugelhahn d25 | 42.0 Stk | 42 Stk | 28.04/Stk | 1.177,68 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d32` | PVC-U-Kugelhahn d32 | 24.0 Stk | 24 Stk | 35.34/Stk | 848,16 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d40` | PVC-U-Kugelhahn d40 | 18.0 Stk | 18 Stk | 44.97/Stk | 809,46 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d50` | PVC-U-Kugelhahn d50 | 2.0 Stk | 2 Stk | 53.47/Stk | 106,94 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d63` | PVC-U-Kugelhahn d63 | 6.0 Stk | 6 Stk | 79.02/Stk | 474,12 EUR | OFFEN (E20) |
| `ARM-kugelhahn-feder_d40` | PVC-U-Kugelhahn feder_d40 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-luftstein-notluft` | Luftausstroemer (Luftstein) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-probehahn-messing` | Probierhahn Messing 1/2 Zoll [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-rsv-d20` | PVC-U-Rueckschlagventil d20 | 2.0 Stk | 2 Stk | - | - | OFFEN (E20) - kein Angebot mit Preis in data/beschaffung |
| `ARM-rsv-d25` | PVC-U-Rueckschlagventil d25 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (E20) - kein Angebot mit Preis in data/beschaffung |
| `ARM-rsv-d40` | PVC-U-Rueckschlagventil d40 | nicht platziert (je 1: 3.0) | 0 Stk | - | - | OFFEN (E20) - kein Angebot mit Preis in data/beschaffung |
| `ARM-rsv-d50` | PVC-U-Rueckschlagventil d50 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-rueckschlagventil-d50` | PVC-U-Rueckschlagventil d50 (Klebemuffe) | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-rueckschlagventil-luft` | Rueckschlagventil Luft (Schlauch) | 3.0 Stk | 3 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-schnellkupplung-id19` | Schnellkupplung id19 | 26.0 Stk | 26 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-schnellkupplung-id25` | Schnellkupplung id25 | 12.0 Stk | 12 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-schwimmerschalter-hochstand` | Schwimmerschalter Hochstand (Fabrikat offen) [A] | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-schwimmerventil-nachspeise` | Schwimmerventil 3/4 Zoll (Nachspeisung, Gehaeuse, Wangen, Hebelarm mit Kugel) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-schwimmerventil-pool` | Schwimmerventil Pool (Gehaeuse, Wangen, Hebelarm mit Kugel) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-venturi-mazzei-1583` | Venturi-Injektor | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |

## SCH Schlauch, Schelle, Tuelle

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `SCH-rohrschelle-d110` | Rohrschelle (Klemme, Stahl) d110 | nicht platziert (je 1: 1.0) | 0 Stk | 2.58/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d20` | Rohrschelle (Klemme, Stahl) d20 | 66.0 Stk | 66 Stk | 0.83/Stk | 54,78 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d25` | Rohrschelle (Klemme, Stahl) d25 | 25.0 Stk | 25 Stk | 0.84/Stk | 21,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d32` | Rohrschelle (Klemme, Stahl) d32 | nicht platziert (je 1: 1.0) | 0 Stk | 0.79/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d40` | Rohrschelle (Klemme, Stahl) d40 | nicht platziert (je 1: 1.0) | 0 Stk | 1.13/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d50` | Rohrschelle (Klemme, Stahl) d50 | 49.0 Stk | 49 Stk | 1.27/Stk | 62,23 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d63` | Rohrschelle d63 (Stahl verzinkt, Doppelschelle) | 30.0 Stk | 30 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-rohrschelle-d75` | Rohrschelle (Klemme, Stahl) d75 | 20.0 Stk | 20 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SCH-rohrschelle-d75_ecke` | Rohrschelle (Klemme, Stahl) d75_ecke | 7.0 Stk | 7 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SCH-rohrschelle-d75_stelze` | Rohrschelle (Klemme, Stahl) d75_stelze | 3.0 Stk | 3 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SCH-rohrschelle-vk-vk_d32` | Rohrschelle VK vk_d32 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-rohrschelle-vk-vk_d63` | Rohrschelle VK vk_d63 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauch-d50` | Schlauch D50 (Meterware) | nicht platziert (je 1: 1.0) | 0.0 m | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SCH-schlauch-id16` | Schlauch ID16 (Meterware) | nicht platziert (je 1: 1.1) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauch-id19` | Schlauch ID19 (Meterware, Laenge aus Modellmasse) | 861.0796 m | 875.0 m (35 x 25000 mm) | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SCH-schlauch-id25` | Schlauch ID25 (Meterware) | 321.9333 m | 350.0 m (14 x 25000 mm) | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauch-luft-d12` | Luftschlauch d12 (Meterware) | 3.88 m | 25.0 m (1 x 25000 mm) | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SCH-schlauch-luft-d8` | Luftschlauch d8 (Meterware) | 2.016 m | 25.0 m (1 x 25000 mm) | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SCH-schlauch-rinne-id16` | Schlauch ID16, 110 mm Stueck (Rinne Zulauf) | 76.0 Stk | 76 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauchbogen90-id16` | Schlauchbogen 90 Grad id16 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauchbogen90-id25` | Schlauchbogen 90 Grad id25 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauchschelle-id16` | Schlauchschelle id16 | nicht platziert (je 1: 1.0) | 0 Stk | 0.63/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-schlauchschelle-id25` | Schlauchschelle id25 | nicht platziert (je 1: 1.0) | 0 Stk | 0.65/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-schlauchtuelle-d12` | Schlauchtuelle (PVC) | 15.0 Stk | 15 Stk | 1.33/Stk | 19,95 EUR | OFFEN (Quelle) |
| `SCH-schlauchtuelle-d25` | Schlauchtuelle d25 (PVC) | 38.0 Stk | 38 Stk | 2.95/Stk | 112,10 EUR | OFFEN (Quelle) |

## SRB Schraube, Mutter, Scheibe, Bolzen

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `SRB-gewindestange-m17x110` | Gewindestange M17x110, verzinkt | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SRB-gewindestange-m17x120` | Gewindestange M17x120, verzinkt | 12.0 Stk | 12 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SRB-halter-klein-12x10x20` | Kleinteil am Winkelhalter 12x10x20 (Schraube/Mutter) [A] | 456.0 Stk | 456 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (Satz), Umrechnung offen |
| `SRB-satz-m10x60` | Schraubensatz M10x60 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 128.0 Satz | 128 Satz | 0.2888/Satz | 36,97 EUR | OK |
| `SRB-satz-m12x55` | Schraubensatz M12x55 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 10.0 Satz | 10 Satz | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SRB-satz-m16x300` | Schraubensatz M16x300 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 20.0 Satz | 20 Satz | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SRB-satz-m5x12` | Schraubensatz M5x12 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 304.0 Satz | 304 Satz | 0.0649/Satz | 19,73 EUR | OK |
| `SRB-satz-m6x16` | Schraubensatz M6x16 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | nicht platziert (je 1: 2.0) | 0 Satz | 0.0723/Satz | 0,00 EUR | OK |
| `SRB-satz-m6x20` | Schraubensatz M6x20 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | nicht platziert (je 1: 4.0) | 0 Satz | 0.0747/Satz | 0,00 EUR | OK |
| `SRB-satz-m6x40` | Schraubensatz M6x40 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 112.0 Satz | 112 Satz | 0.0927/Satz | 10,38 EUR | OK |
| `SRB-satz-m6x55` | Schraubensatz M6x55 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | nicht platziert (je 1: 2.0) | 0 Satz | 0.1131/Satz | 0,00 EUR | OK |
| `SRB-satz-m8x30` | Schraubensatz M8x30 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) [A] | 312.0 Satz | 312 Satz | 0.1254/Satz | 39,12 EUR | OK |
| `SRB-satz-m8x65` | Schraubensatz M8x65 (Sechskantschraube + Mutter + 2 Scheiben) [A] | 56.0 Satz | 56 Satz | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |

## BEH Behaelter und Becken

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `BEH-ak-kompositbehaelter-254x790` | Aktivkohle-Druckbehaelter Komposit 254x790 mm mit Steuerkopf [A] | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-ak-sedimentfilter` | Sedimentfilter-Set (Gehaeuse, Kopf, Patrone) [A] | 1.0 Satz | 1 Satz | 20.72/Satz | 20,72 EUR | OK |
| `BEH-becken-dritt` | Drittbecken (Eigenbau/Sonderanfertigung, Masse aus Modell) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-biofilter-dritt-fass` | Biofilter-Fass PE mit Lochplatte (Altbestand-Drittbiofilter) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BEH-drittbecken-klein` | Drittbecken klein (Wanne 920x920x1055) | 1.0 Stk | 1 Stk | 680.68/Stk | 680,68 EUR | OK |
| `BEH-fass-hdpe` | HDPE-Fass 500 mm (Mischfass) | 1.0 Stk | 1 Stk | 43.99/Stk | 43,99 EUR | OK |
| `BEH-feinfilter-pp-630x440x610` | Feinfilter-Behaelter PP 630x440x610 (Eigenbau/Kaufteil offen) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-futterzuchtkiste-pe` | Futterzuchtkiste PE 350x525x800 (Permakultur-Modul) [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BEH-halter-box-gehaeuse` | Anschlussbox PS 200x150x100 mit Acryldeckel | nicht platziert (je 1: 1.0) | 0 Stk | 67.27/Stk | 0,00 EUR | OK |
| `BEH-ibc-1000l` | IBC-Container 1000 l mit Gitterkaefig und Palette (Puffer) | nicht platziert (je 1: 3.0) | 0 Stk | 229.94/Stk | 0,00 EUR | OK |
| `BEH-ibc-beetwanne` | IBC-Beetwanne HDPE (aus IBC geschnitten, Laenge je Beet) | 14.0 Stk | 14 Stk | 229.94/Stk | 3.219,16 EUR | OK |
| `BEH-kanister-hdpe` | HDPE-Kanister (Dosiervorrat) | 1.0 Stk | 1 Stk | 8.66/Stk | 8,66 EUR | OK |
| `BEH-messbecher-pp` | Messbecher PP 160x310 | nicht platziert (je 1: 1.0) | 0 Stk | 13.09/Stk | 0,00 EUR | OK |
| `BEH-messzelle-acryl` | Messzelle Acryl 315x315x260 | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (m2), Umrechnung offen |
| `BEH-pe-schachtaufsatz-600x200` | PE-Schachtaufsatz (Dom) Oe 600 x 200 mm fuer Tank [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-pegelschacht-fass` | Pegelschacht PE-HD-Fass mit Deckel (Altbestand, entfaellt im Modell) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BEH-pool-zentral` | Zentralpool (Eigenbau/Sonderanfertigung, Masse aus Modell) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-regentank-5000` | Regenwassertank 5000 l, stehend, oberirdisch (PE) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-schlammbehaelter-350` | Schlamm-Sammelbehaelter PE rund 350 l mit Deckel (Durchm. 900 x 600) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-580-deckel` | PE-Tankdeckel 580 mm | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-580x865` | PE-Tank 580 mm Durchm., 865 mm hoch (Kegelboden/Absetzer) | nicht platziert (je 1: 1.0) | 0 Stk | 74.99/Stk | 0,00 EUR | OK |
| `BEH-tank-pe-673-deckel` | PE-Tankdeckel 673 mm | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-673x1075` | PE-Tank 673 mm Durchm., 1075 mm hoch (Kegelboden/Absetzer) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-700-deckel` | PE-Tankdeckel 700 mm | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-800x1000` | PE-Tank 800 mm Durchm., 1000 mm hoch (Kegelboden/Absetzer) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-930-deckel` | PE-Tankdeckel 930 mm | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-930x1444` | PE-Tank 930 mm Durchm., 1444 mm hoch (Kegelboden/Absetzer) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-zweitbecken` | Zweitbecken (Eigenbau/Sonderanfertigung, Masse aus Modell) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |

## PMP Pumpe und Geblaese

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `PMP-dosierpumpe` | Dosierpumpe (Schlauchpumpe) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `PMP-geblaese-luft` | Membrangeblaese Luft (Leistung offen, Bauteilblatt geblaese_luft) | 2.0 Stk | 2 Stk | 458.42/Stk | 916,84 EUR | OK |
| `PMP-luftpumpe-notluft` | Notluftpumpe (Membranpumpe, Akku/Netz) [A] | 1.0 Stk | 1 Stk | 120.9/Stk | 120,90 EUR | OK |
| `PMP-pumpe-gross` | Kreiselpumpe gross | nicht platziert (je 1: 1.0) | 0 Stk | 233.79/Stk | 0,00 EUR | OK |
| `PMP-pumpe-klein` | Kreiselpumpe klein | nicht platziert (je 1: 1.0) | 0 Stk | 95.9/Stk | 0,00 EUR | OK |
| `PMP-tauchpumpe-oase-8000` | Tauchpumpe (Klasse Oase AquaMax Eco Premium 8000, Typ offen, siehe Beschaffung) | 4.0 Stk | 4 Stk | 408.99/Stk | 1.635,96 EUR | OK |
| `PMP-teichpumpe-5300` | Teichpumpe 5300 l/h, 60 W, Hmax 2,8 m (Beet-Sumpf, Fabrikat offen) [A] | nicht platziert (je 1: 2.0) | 0 Stk | 220.49/Stk | 0,00 EUR | OK |

## MES Messtechnik (Sonden, Sensoren)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `MES-co2-scd41` | Sonde co2_scd41 (Typ und Fabrikat offen: docs/research/R39) | nicht platziert (je 1: 1.0) | 0 Stk | 30.820999999999998/Stk | 0,00 EUR | OK |
| `MES-do-ind` | Sonde do_ind (Typ und Fabrikat offen: docs/research/R39) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `MES-do-mini` | Sonde do_mini (Typ und Fabrikat offen: docs/research/R39) | 3.0 Stk | 3 Stk | 285.72/Stk | 857,16 EUR | OK |
| `MES-druck-schalter` | Sonde druck_schalter (Typ und Fabrikat offen: docs/research/R39) | nicht platziert (je 1: 1.0) | 0 Stk | 13.79/Stk | 0,00 EUR | OK |
| `MES-ec` | Sonde EC (Stationsmessplatz) | 1.0 Stk | 1 Stk | 195.47/Stk | 195,47 EUR | OK |
| `MES-flow-12` | Sonde flow_12 (Typ und Fabrikat offen: docs/research/R39) | nicht platziert (je 1: 1.0) | 0 Stk | 7.42/Stk | 0,00 EUR | OK |
| `MES-flow-gross` | Sonde flow_gross (Typ und Fabrikat offen: docs/research/R39) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `MES-leck` | Sonde leck (Typ und Fabrikat offen: docs/research/R39) | 3.0 Stk | 3 Stk | 34.9/Stk | 104,70 EUR | OK |
| `MES-level-druck` | Sonde level_druck (Typ und Fabrikat offen: docs/research/R39) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `MES-level-float` | Sonde level_float (Typ und Fabrikat offen: docs/research/R39) | 3.0 Stk | 3 Stk | 44.9/Stk | 134,70 EUR | OK |
| `MES-o2` | Sonde O2 (Stationsmessplatz) | nicht platziert (je 1: 1.0) | 0 Stk | 285.72/Stk | 0,00 EUR | OK |
| `MES-par` | Sonde par (Typ und Fabrikat offen: docs/research/R39) | nicht platziert (je 1: 1.0) | 0 Stk | 605.0/Stk | 0,00 EUR | OK |
| `MES-ph` | Sonde pH (Stationsmessplatz) | 3.0 Stk | 3 Stk | 94.59/Stk | 283,77 EUR | OK |
| `MES-schwimmerschalter` | Schwimmerschalter (Niveau AUS/EIN/ALARM, Fabrikat offen) [A] | nicht platziert (je 1: 3.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `MES-strom-ct` | Sonde strom_ct (Typ und Fabrikat offen: docs/research/R39) | nicht platziert (je 1: 1.0) | 0 Stk | 7.0/Stk | 0,00 EUR | OK |
| `MES-temp-ds` | Sonde temp_ds (Typ und Fabrikat offen: docs/research/R39) | 2.0 Stk | 2 Stk | 4.07/Stk | 8,14 EUR | OK |
| `MES-temperatur` | Sonde Temperatur (Stationsmessplatz) | nicht platziert (je 1: 1.0) | 0 Stk | 4.07/Stk | 0,00 EUR | OK |

## ELE Elektrik (Schaltschrank, Kabel, Hutschiene)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `ELE-hutschiene-35` | Hutschiene 35 mm | nicht platziert (je 1: 1.0) | 0 Stk | 9.01/Stk | 0,00 EUR | OK |
| `ELE-kabelkanal-30x60` | Kabelkanal PVC 30x60 | nicht platziert (je 1: 1.0) | 0.0 m | 9.24/m | 0,00 EUR | OK |
| `ELE-kabelverschraubung-m25` | Kabelverschraubung M25 (PA) | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ELE-kabelverschraubung-pg` | Kabelverschraubung PA (PG/M20) | 1.0 Stk | 1 Stk | 0.89/Stk | 0,89 EUR | OK |
| `ELE-schaltschrank-500x800x1200` | Schaltschrank 500x800x1200 mm (leer, Ausruestung offen) | 1.0 Stk | 1 Stk | 469.97/Stk | 469,97 EUR | OK |

## FOL Folie, Plane, Dichtband, Dichtung

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `FOL-epdm-dichtband-zarge` | EPDM-Dichtband Zarge | nicht platziert (je 1: 2.043) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FOL-epdm-dichtung-630x440` | EPDM-Flachdichtung 630x440x3 | nicht platziert (je 1: 1.0) | 0 Stk | 4.23/Stk | 0,00 EUR | OK |
| `FOL-epdm-schaumband` | EPDM-Schaumband 25x3 | nicht platziert (je 1: 3.019) | 0.0 m | 2.29/m | 0,00 EUR | OK |
| `FOL-epdm-schelleneinlage-d75` | EPDM-Schelleneinlage d75 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FOL-epdm-tuerdichtung` | EPDM-Tuerdichtung | 5.988 m | 25.0 m (1 x 25000 mm) | 1.64/m | 41,00 EUR | OK |
| `FOL-pe-plane` | PE-Planenbahn (Huelle, Zuschnitt je Feld, Flaeche aus Modell) | 1015.8418 m2 | 1117.43 m2 | 2.05/m2 | 2.290,73 EUR | OK |

## GEW Gewebe und Netz

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `GEW-sieb-v2a-2mm` | Edelstahl-Siebgewebe 2 mm (Beetsieb, Flaeche aus Modell) | 25.0701 m2 | 27.58 m2 | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `GEW-v2a-100um` | Edelstahl-Siebgewebe 100 um, 1.4301 (Siebkorb, Flaeche aus Modell) | nicht platziert (je 1: 1.0104) | 0.0 m2 | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `GEW-vlies-pp` | PP-Vlies (Beetboden, Flaeche aus Modell) | 25.0701 m2 | 27.58 m2 | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |

## TOP Topf und Substrat

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `TOP-aktivkohle` | Aktivkohle-Granulat (Behaelterfuellung) | 0.042 m3 | 0.05 m3 | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (Packung/Sack), Umrechnung offen |
| `TOP-biomedium` | Biomedium (Biofilter-Fuellkoerper) | 1.29 m3 | 1.36 m3 | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `TOP-blaehton` | Blaehton-Substrat 8-16 mm (Beetfuellung) | 7.5211 m3 | 7.9 m3 | 314/m3 | 2.480,60 EUR | OK |
| `TOP-netztopf-64` | Netztopf PP 64 mm (Pflanzkorb, Stueckzahl aus Instanzen) | 2222.0 Stk | 2222 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |

## SON Sonderteil (Eigenbau mit Rohmaterial als Kaufteil, Tuer, Haut, Knoten)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `SON-ak-konsole` | Konsole Sedimentfilter (Stahl, Eigenbau) [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-ankergabel-80x140` | Gabelkopf 80x140 (Fundamentanker, Stahl, Zuschnitt) | 20.0 Stk | 20 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-ankerlasche` | Ankerlasche am Knoten (Stahl, Zuschnitt) | nicht platziert (je 1: 11.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-ausstroemer-stab-600` | Ausstroemer-Stab PP 16x600 (Beet-Belueftung) [A] | 14.0 Stk | 14 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-belueftungsgitter-460` | Belueftungsgitter 460x460 (PVC, Tankdeckel) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-bodenrinne-pp-1100` | Bodenrinne PP 120x162x1100 (Laufgang-Entwaesserung, Eigenbau/Zuschnitt) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-bodenrinne-pp-1200` | Bodenrinne PP 120x162x1200 (Laufgang-Entwaesserung, Eigenbau/Zuschnitt) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-federdraht-d2` | Federstahldraht d2 (Keilschiene) | nicht platziert (je 1: 2.979) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-gummifuss-40` | Gummifuss 40x40x15 | 8.0 Stk | 8 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-halter-inline-d32-sensorblock` | Sensorblock (halter_inline_d32, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d32-sieb` | Sieb halter_inline_d32 (Edelstahl) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d32-vorfilter` | Vorfilter (halter_inline_d32, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d50-sensorblock` | Sensorblock (halter_inline_d50, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d50-sieb` | Sieb halter_inline_d50 (Edelstahl) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d50-vorfilter` | Vorfilter (halter_inline_d50, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-zelle-zellkoerper` | Zellkoerper (halter_zelle, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-holz-stuetzrippe` | Stuetzrippe Fichte (Tank-Auflage) | 10.0 Stk | 10 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-knotenarm-23x23x3` | Steckarm 23x23x3 am Knoten (Verbindungsstueck, N-STATIK W43 offen) | nicht platziert (je 1: 145.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-knotenkugel-d100` | Knotenkugel d100, Stahl (Verbindungsstueck, N-STATIK W43 offen) | nicht platziert (je 1: 29.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-korbgriff-v2a` | Korbgriff Edelstahl (Eigenbau) | nicht platziert (je 1: 2.0) | 0 Stk | 13.24/Stk | 0,00 EUR | OK |
| `SON-laser-lasche-30x34x123` | Laserteil Lasche 30x34x123 mm, Stahl (Knoten Schere) | 60.0 Stk | 60 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-laser-lasche-30x34x125` | Laserteil Lasche 30x34x125 mm, Stahl (Knoten Schere) | 60.0 Stk | 60 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-laser-lasche-34x35x122` | Laserteil Lasche 34x35x122 mm, Stahl (Knoten Schere) | 68.0 Stk | 68 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-laser-lasche-34x36x124` | Laserteil Lasche 34x36x124 mm, Stahl (Knoten Schere) | 68.0 Stk | 68 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-luftfilter-ansaug` | Ansaug-Luftfilter fuer den Venturi (PP) [A] | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-luftverteiler-4` | Luftverteiler 4-fach (PVC, Eigenbau) [A] | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-luftverteiler-6` | Luftverteiler 6-fach (PVC, Eigenbau) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-permakultur-kompostbox` | Kompostbox Fichte 525x600x1500 mit Deckel (Permakultur-Modul, Eigenbau) [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-pflanztisch-platte` | Pflanztischplatte (Alt-Modell, nicht verbaut) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-plattform-619x619` | Tankplattform 619x619x73 (Stahl, Eigenbau) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-plattform-821x821` | Tankplattform 821x821x98 (Stahl, Eigenbau) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-polycarbonat-paneel` | Polycarbonat-Paneel 8 mm (Zuschnitt je Feld) | nicht platziert (je 1: 3.0) | 0 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (m2), Umrechnung offen |
| `SON-pp-schwimmerhalter` | Schwimmerhalter PP 40x60x80 (Eigenbau) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-pp-stuetze-60x60` | PP-Stuetze 60x60 (Beetboden, Hoehe je Beet) | 274.0 Stk | 274 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-pp-zonenschild` | Zonenschild PP 2x40x100 (Beschriftung Pufferzone) | 8.0 Stk | 8 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-ruecklaufrinne-v2a-2000` | Ruecklaufrinne Edelstahl 55x103x2000 (Altbestand) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-schacht-kugelhahn-d63` | Schacht fuer Kugelhahn (PE-HD) d63 | nicht platziert (je 1: 3.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-scheibenbelueftung-270` | Scheibenbelueftung d270 (Tragteller, Stuetzfuss, EPDM-Membran) [A] | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-schlauchhalter-pp` | Schlauchhalter PP (Clip) [A] | 27.0 Stk | 27 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-schrankwand-500x800` | Schrankwand 500x800 (Eigenbau, Werkstoff offen) [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-sondenhalter-36` | Sondenhalter 36x36x40 (PVC, Eigenbau/Stuetze) | nicht platziert (je 1: 4.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-spannverschluss-edelstahl` | Spannverschluss Edelstahl (Bock + Hebel) | nicht platziert (je 1: 4.0) | 0 Stk | 23.03/Stk | 0,00 EUR | OK |
| `SON-stahlteil-134x192x230` | Stahlteil 134x192x230 mm (Eigenbau/Zuschnitt, Stahl verzinkt) | 18.0 Stk | 18 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-stahlteil-20x40x42` | Stahlteil 20x40x42 mm (Eigenbau/Zuschnitt, Stahl verzinkt) | 74.0 Stk | 74 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-stahlteil-35x40x40` | Stahlteil 35x40x40 mm (Eigenbau/Zuschnitt, Stahl verzinkt) | 3.0 Stk | 3 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-stahlteil-60x416x416` | Stahlteil 60x416x416 mm (Eigenbau/Zuschnitt, Stahl verzinkt) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-stahlteil-80x118x160` | Stahlteil 80x118x160 mm (Eigenbau/Zuschnitt, Stahl verzinkt) | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `SON-strahlungsschutz-par` | Strahlungsschutz PP weiss (Messmast) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-tanksieb-stahl` | Sieb am Tank (Stahl verzinkt, Zulauf/Auslauf) | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-tauchklemme` | Klemme Tauchrohr (Stahl, Eigenbau) | 3.0 Stk | 3 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-tuer-modellvariante` | Tuer (Alt-Modell, nicht verbaut) T4_Pfosten_L | nicht platziert (je 1: 4.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-tuerblatt-1000x2000` | Tuerblatt Sandwich 1000x2000x40 | 1.0 Stk | 1 Stk | 749/Stk | 749,00 EUR | OK |
| `SON-tuerdruecker` | Tuerdruecker mit Rosette | 2.0 Stk | 2 Stk | 16.06/Stk | 32,12 EUR | OK |
| `SON-tuerscharnier` | Tuerscharnier (Zargenlasche, Blattlasche, Bolzen) | 3.0 Stk | 3 Stk | 2.49/Stk | 7,47 EUR | OK |
| `SON-zarge-aufsatzrahmen` | Alu-Aufsatzrahmen Tuerzarge (Planenausschnitt) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |

## MAT Material nach Menge (Gitterrost, Teichfolie; Zuschnitt oder Flaeche)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `MAT-epdm-teichfolie` | EPDM-Teichfolie 1,5 mm (Grubenauskleidung, Flaeche aus Modell: Boden und vier Waende) | 14.3182 m2 | 15.76 m2 | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `MAT-gitterrost-112x1096` | Gitterrost verzinkt 1096x112x20 mm (Rinnenabdeckung) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `MAT-gitterrost-112x1196` | Gitterrost verzinkt 1196x112x20 mm (Rinnenabdeckung) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `MAT-gitterrost-deckel` | Begehbarer Gitterrost 30/10 feuerverzinkt 1229 x 1026 x 40 mm (Grubendeckel) | 6.0 Stk | 6 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
