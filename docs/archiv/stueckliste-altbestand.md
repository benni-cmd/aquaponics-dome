# Stueckliste (erzeugt, nicht von Hand)

Erzeugt von `scripts/bom.py` aus dem Modellstand (`viewer/instances.json` built 2026-11-05 02:12:59, sc_sha256 4aef15a1929b9af1). Preise brutto, Richtwerte mit Datum, keine Angebote. Quelle der Preise: `data/beschaffung/*.json`.

**Drift:** die `.sc` haben sich seit der Koerpermessung geaendert (aktuell 938f5a09625e8abb). Nachmessen: `python -X utf8 scripts/bom_artikel.py --ergaenzen`.

## Kopf

1. Zeilen: 273 (Preis fehlt bei 43 platzierten, 137 Zeilen nur in nicht platzierten Komponenten)
2. Summe der Zeilen mit Preis (platziert): 26.870,92 EUR
2b. Nicht platzierte Komponenten (ohne lt_-Bibliothek), je 1 Stueck gerechnet, 35 Zeilen mit Preis: 3.040,82 EUR (nicht in der Summe, Entscheidung offen)
3. Instanzen im Modell: 4914 in 164 Definitionen
4. Unbenannte Koerper (Body<n>) in der Messung: 0, davon per Regel benannt: 0, ungeklaert: 0

## Summe je Typ

| Typ | Bedeutung | Summe |
|---|---|---|
| ARM | Armatur (Kugelhahn, Ventil, Bulkhead, Durchfuehrung) | 1.442,90 EUR |
| BEH | Behaelter und Becken | 3.952,49 EUR |
| BLE | Blech, Platte, Lochblech, Zuschnitt | 1.153,83 EUR |
| ELE | Elektrik (Schaltschrank, Kabel, Hutschiene) | 470,45 EUR |
| FIT | Fitting (Bogen, T, Reduzierung, Kupplung, Stutzen, Kappe) | 714,55 EUR |
| FOL | Folie, Plane, Dichtband, Dichtung | 2.340,19 EUR |
| MES | Messtechnik (Sonden, Sensoren) | 1.583,94 EUR |
| PMP | Pumpe und Geblaese | 1.318,76 EUR |
| PRF | Stahlprofil (Rechteck-, Vierkantrohr, Rund- und Vollmaterial) | 6.284,12 EUR |
| ROH | PVC-U-Rohr (Meterware) | 3.418,30 EUR |
| SCH | Schlauch, Schelle, Tuelle | 11,80 EUR |
| SON | Sonderteil (Eigenbau mit Rohmaterial als Kaufteil, Tuer, Haut, Knoten) | 1.025,79 EUR |
| SRB | Schraube, Mutter, Scheibe, Bolzen | 91,06 EUR |
| TOP | Topf und Substrat | 2.480,60 EUR |
| WNK | Winkel und Flachstahl, Halter | 582,14 EUR |

## Summe je Bauteilgruppe

| Gruppe | Summe |
|---|---|
| Becken und Tanks | 4.004,51 EUR |
| Filter | 958,01 EUR |
| Fundament | 323,20 EUR |
| Huelle | 3.180,29 EUR |
| Kuppel | 2.080,58 EUR |
| Leitungen | 2.089,35 EUR |
| Messtechnik und Elektrik | 2.173,74 EUR |
| Tische und Beete | 12.061,24 EUR |

## Nicht in der Liste (Ausnahmen)

| Grund | Koerper | Masse (kg, mit Instanzen) |
|---|---|---|
| Aushub und Erde (Entscheidung 04.11.2026) | 1 | 701782.1 |
| Beton nach Menge (Entscheidung 04.11.2026) | 2 | 5111.19 |
| Massfigur, kein Bauteil | 43 | 160.2 |
| Mutter/Scheibe im Schraubensatz enthalten | 462 | 2.95 |
| Pflanze (Salat), nicht kaufbar | 98 | 59.0 |
| Teil eines Hahns (Griff/Spindel/Hebel) im Hahn-Artikel enthalten | 9 | 0.0 |
| Wasserkoerper, kein Bauteil | 7 | 36335.16 |

## PRF Stahlprofil (Rechteck-, Vierkantrohr, Rund- und Vollmaterial)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `PRF-alu-haut-profil` | Alu-Kappenprofil der Haut | nicht platziert (je 1: 3.279) | 0.0 m | 4.39/m | 0,00 EUR | OK |
| `PRF-alu-keilschiene` | Alu-Keilschiene (Kanal 25x15) | nicht platziert (je 1: 3.019) | 0.0 m | 7.32/m | 0,00 EUR | OK |
| `PRF-alu-klemmleiste` | Alu-Klemmleiste Zarge | nicht platziert (je 1: 2.043) | 0.0 m | 3.29/m | 0,00 EUR | OK |
| `PRF-pvcu-rinne-130x100` | NFT-Rinnenprofil PVC-U 130x100 (Meterware, Lagerlaenge offen) | 147.924 m | 154.0 m (22 x 7000 mm) | 7.16/m | 1.102,64 EUR | OK |
| `PRF-st-rr25x25x2` | Vierkantrohr 25x25x2 mm, Stahl verzinkt | nicht platziert (je 1: 8.82) | 0.0 m | 5.47/m | 0,00 EUR | OK |
| `PRF-st-rr30x30x2` | Vierkantrohr 30x30x2 mm, Stahl verzinkt | 24.876 m | 26.0 m (4 x 6500 mm) | 6.65/m | 172,90 EUR | OK |
| `PRF-st-rr35x600x0.5` | Rechteckrohr 35x600x0.5 mm, Stahl verzinkt | nicht platziert (je 1: 0.6) | 0.0 m | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `PRF-st-rr40x40x2` | Vierkantrohr 40x40x2 mm, Stahl verzinkt | nicht platziert (je 1: 14.104) | 0.0 m | 9.04/m | 0,00 EUR | OK |
| `PRF-st-rr40x40x2.5` | Vierkantrohr 40x40x2.5 mm, Stahl verzinkt | 158.408 m | 162.5 m (25 x 6500 mm) | 12.65/m | 2.055,62 EUR | OK |
| `PRF-st-rr40x40x3` | Vierkantrohr 40x40x3 mm, Stahl verzinkt | 10.672 m | 12.0 m (2 x 6000 mm) | 12.65/m | 151,80 EUR | OK |
| `PRF-st-rr40x60x3` | Rechteckrohr 40x60x3 mm, Stahl verzinkt | 40.436 m | 44.0 m (11 x 4000 mm) | 16.26/m | 715,44 EUR | OK |
| `PRF-st-rr60x60x3` | Vierkantrohr 60x60x3 mm, Stahl verzinkt | nicht platziert (je 1: 10.808) | 0.0 m | 19.76/m | 0,00 EUR | OK |
| `PRF-st-rund20` | Rundstahl 20 mm, Stahl verzinkt | nicht platziert (je 1: 2.35) | 0.0 m | 11.25/m | 0,00 EUR | OK |
| `PRF-st-strebe30x30` | Strebenprofil 30x30 (Kuppelstrebe, Profil und Wand offen: N-STATIK V1/V2c) | 209.082 m | 224.0 m (32 x 7000 mm) | 9.12/m | 2.042,88 EUR | OK |
| `PRF-v2a-voll8x8` | Vierkant-/Flachstahl voll 8x8 mm, Edelstahl 1.4301 | 6.768 m | 7.0 m (1 x 7000 mm) | 6.12/m | 42,84 EUR | OK |

## WNK Winkel und Flachstahl, Halter

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `WNK-flach-14x3` | Flachstahl 14x3 (Tuer-Anschlag) | 5.004 m | 6.0 m (1 x 6000 mm) | 2.85/m | 17,10 EUR | OK |
| `WNK-flach-3mm-diagonale` | Flachstahl 3 mm (Diagonalen, Breite aus Modell nicht ableitbar, Zuschnitt) | 110.0 Stk | 110 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (m), Umrechnung offen |
| `WNK-pumpenkonsole` | Pumpenkonsole/Standwinkel (Stahl, Zuschnitt) | 24.0 Stk | 24 Stk | 1.25/Stk | 30,00 EUR | OK |
| `WNK-rinnenhalter-25` | Rinnenhalter 25x25 (Stahl, Zuschnitt/Kleinteil) | 304.0 Stk | 304 Stk | 1.56/Stk | 474,24 EUR | OK |
| `WNK-wandlasche-30x30x3` | Wandlasche 30x30x3 | nicht platziert (je 1: 2.0) | 0 Stk | 1.13/Stk | 0,00 EUR | OK |
| `WNK-winkel-36x60x60` | Winkel 36x60x60 (Rinnen-Winkelhalter, Stahl) | 76.0 Stk | 76 Stk | 0.8/Stk | 60,80 EUR | OK |

## BLE Blech, Platte, Lochblech, Zuschnitt

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `BLE-blech-st-3` | Stahlblech 3 mm verzinkt, Zuschnitt 700x700 | 5.0 Stk | 5 Stk | 35.96/Stk | 179,80 EUR | OK |
| `BLE-blech-st-5` | Stahlblech 5 mm verzinkt, Zuschnitt 840x400 | nicht platziert (je 1: 2.0) | 0 Stk | 39.99/Stk | 0,00 EUR | OK |
| `BLE-blech-st-6` | Stahlblech 6 mm verzinkt, Zuschnitt 1360x580 | nicht platziert (je 1: 1.0) | 0 Stk | 106.74/Stk | 0,00 EUR | OK |
| `BLE-fussplatte-100x100x6` | Fussplatte Stahl verzinkt 100x100x6 mm | 16.0 Stk | 16 Stk | 4.32/Stk | 69,12 EUR | OK |
| `BLE-fussplatte-150x150x8` | Fussplatte Stahl verzinkt 150x150x8 mm | nicht platziert (je 1: 2.0) | 0 Stk | 4.79/Stk | 0,00 EUR | OK |
| `BLE-fussplatte-200x200x8` | Fussplatte Stahl verzinkt 200x200x8 mm | nicht platziert (je 1: 1.0) | 0 Stk | 8.52/Stk | 0,00 EUR | OK |
| `BLE-fussplatte-70x70x5` | Fussplatte Stahl verzinkt 70x70x5 mm | 76.0 Stk | 76 Stk | 1.65/Stk | 125,40 EUR | OK |
| `BLE-fussplatte-80x80x6` | Fussplatte Stahl verzinkt 80x80x6 mm | 12.0 Stk | 12 Stk | 3.84/Stk | 46,08 EUR | OK |
| `BLE-fussplatte-80x80x8` | Fussplatte Stahl verzinkt 80x80x8 mm | nicht platziert (je 1: 8.0) | 0 Stk | 1.36/Stk | 0,00 EUR | OK |
| `BLE-platte-250x250x15` | Ankerplatte 250x250x15 mm, Stahl | 10.0 Stk | 10 Stk | 32.32/Stk | 323,20 EUR | OK |
| `BLE-pp-blende-290x260` | PP-Blende 290x260x3 (Messzelle) | 1.0 Stk | 1 Stk | 1.23/Stk | 1,23 EUR | OK |
| `BLE-pp-siebboden-beet` | PP-Siebboden 8 mm (Zuschnitt je Beet) | 14.0 Stk | 14 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (m2), Umrechnung offen |
| `BLE-pp-tafel-502x345x5` | PP-Montagetafel 502x345x5 (Zuschnitt) | 4.0 Stk | 4 Stk | 4.74/Stk | 18,96 EUR | OK |
| `BLE-pp-tafel-693x463x7` | PP-Montagetafel 693x463x7 (Zuschnitt) | 4.0 Stk | 4 Stk | 13.94/Stk | 55,76 EUR | OK |
| `BLE-schrankboden-3x500x800` | Stahlblech 3 mm, Zuschnitt 800x500 (Schrankboden) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BLE-v2a-3mm-korbflansch` | Edelstahlblech 3 mm 1.4301, Zuschnitt 604x414 (Korbflansch) | 2.0 Stk | 2 Stk | 94.2/Stk | 188,40 EUR | OK |
| `BLE-v2a-lochblech-medienschutz` | Edelstahl-Lochblech 1,5 mm RV5-8, Medienschutz-Zylinder 110x320 | 14.0 Stk | 14 Stk | 10.42/Stk | 145,88 EUR | OK |

## ROH PVC-U-Rohr (Meterware)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `ROH-leerrohr-dn100` | Leerrohr DN100 (Kabelschutz, Meterware) | nicht platziert (je 1: 3.0) | 0.0 m | 3.85/m | 0,00 EUR | OFFEN (E20) |
| `ROH-leerrohr-dn50` | Leerrohr DN50 (Kabelschutz, Meterware) | nicht platziert (je 1: 3.0) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ROH-pvcu-d110` | PVC-U-Druckrohr d110 (Meterware) | 6.286 m | 10.0 m (2 x 5000 mm) | 79.83/m | 798,30 EUR | OFFEN (E20) |
| `ROH-pvcu-d16` | PVC-U-Druckrohr d16 (Meterware) | 2.538 m | 5.0 m (1 x 5000 mm) | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ROH-pvcu-d160` | PVC-U-Druckrohr d160 (Zulaufrohr, Meterware, Laenge aus Bbox [E]) | 4.403 m | 5.0 m (1 x 5000 mm) | 81.47/m | 407,35 EUR | OFFEN (Quelle) |
| `ROH-pvcu-d20` | PVC-U-Druckrohr d20 (Meterware) | 28.334 m | 30.0 m (6 x 5000 mm) | 4.77/m | 143,10 EUR | OFFEN (E20) |
| `ROH-pvcu-d25` | PVC-U-Druckrohr d25 (Meterware) | 25.971 m | 30.0 m (6 x 5000 mm) | 5.19/m | 155,70 EUR | OFFEN (E20) |
| `ROH-pvcu-d32` | PVC-U-Druckrohr d32 (Meterware) | 2.487 m | 5.0 m (1 x 5000 mm) | 10.22/m | 51,10 EUR | OFFEN (E20) |
| `ROH-pvcu-d40` | PVC-U-Druckrohr d40 (Meterware) | 12.525 m | 15.0 m (3 x 5000 mm) | 15.41/m | 231,15 EUR | OFFEN (E20) |
| `ROH-pvcu-d50` | PVC-U-Druckrohr d50 (Meterware) | 33.415 m | 35.0 m (7 x 5000 mm) | 23.66/m | 828,10 EUR | OFFEN (E20) |
| `ROH-pvcu-d63` | PVC-U-Druckrohr d63 (Meterware) | 7.778 m | 10.0 m (2 x 5000 mm) | 35.95/m | 359,50 EUR | OFFEN (E20) |
| `ROH-pvcu-d75` | PVC-U-Druckrohr d75 (Meterware) | 8.184 m | 10.0 m (2 x 5000 mm) | 44.4/m | 444,00 EUR | OFFEN (E20) |

## FIT Fitting (Bogen, T, Reduzierung, Kupplung, Stutzen, Kappe)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `FIT-bogen45-d110` | PVC-U-Bogen 45 Grad d110 | nicht platziert (je 1: 1.0) | 0 Stk | 37.52/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d20` | PVC-U-Bogen 45 Grad d20 | nicht platziert (je 1: 1.0) | 0 Stk | 2.38/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d25` | PVC-U-Bogen 45 Grad d25 | nicht platziert (je 1: 1.0) | 0 Stk | 2.38/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d32` | PVC-U-Bogen 45 Grad d32 | nicht platziert (je 1: 1.0) | 0 Stk | 2.63/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d40` | PVC-U-Bogen 45 Grad d40 | nicht platziert (je 1: 1.0) | 0 Stk | 3.69/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen45-d50` | PVC-U-Bogen 45 Grad d50 | 3.0 Stk | 3 Stk | 4.76/Stk | 14,28 EUR | OFFEN (E20) |
| `FIT-bogen45-d63` | PVC-U-Bogen 45 Grad d63 | 4.0 Stk | 4 Stk | 7.29/Stk | 29,16 EUR | OFFEN (E20) |
| `FIT-bogen45-d75` | PVC-U-Bogen 45 Grad d75 | nicht platziert (je 1: 1.0) | 0 Stk | 11.91/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen90-d110` | PVC-U-Bogen 90 Grad d110 | nicht platziert (je 1: 1.0) | 0 Stk | 27.77/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen90-d20` | PVC-U-Bogen 90 Grad d20 | nicht platziert (je 1: 1.0) | 0 Stk | 1.36/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-bogen90-d25` | PVC-U-Bogen 90 Grad d25 | 16.0 Stk | 16 Stk | 1.38/Stk | 22,08 EUR | OFFEN (E20) |
| `FIT-bogen90-d32` | PVC-U-Bogen 90 Grad d32 | 8.0 Stk | 8 Stk | 1.76/Stk | 14,08 EUR | OFFEN (E20) |
| `FIT-bogen90-d40` | PVC-U-Bogen 90 Grad d40 | 14.0 Stk | 14 Stk | 3.01/Stk | 42,14 EUR | OFFEN (E20) |
| `FIT-bogen90-d50` | PVC-U-Bogen 90 Grad d50 | 19.0 Stk | 19 Stk | 3.94/Stk | 74,86 EUR | OFFEN (E20) |
| `FIT-bogen90-d63` | PVC-U-Bogen 90 Grad d63 | 7.0 Stk | 7 Stk | 6.06/Stk | 42,42 EUR | OFFEN (E20) |
| `FIT-bogen90-d75` | PVC-U-Bogen 90 Grad d75 | 8.0 Stk | 8 Stk | 11.95/Stk | 95,60 EUR | OFFEN (E20) |
| `FIT-entlueftung-d32` | Entlueftung d32 (PVC-U, mit Insektengitter-Kappe) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-gewindenippel-edelstahl` | Gewindenippel Edelstahl (Druckmessstelle) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-kappe-d16` | PVC-U-Kappe d16 | 42.0 Stk | 42 Stk | 1.19/Stk | 49,98 EUR | OFFEN (Quelle) |
| `FIT-kappe-d20` | PVC-U-Kappe d20 | 5.0 Stk | 5 Stk | 1.24/Stk | 6,20 EUR | OFFEN (E20) |
| `FIT-kappe-d25` | PVC-U-Endkappe d25 | 24.0 Stk | 24 Stk | 1.33/Stk | 31,92 EUR | OK |
| `FIT-kappe-d32` | PVC-U-Kappe d32 | 2.0 Stk | 2 Stk | 1.4/Stk | 2,80 EUR | OK |
| `FIT-kappe-d50` | PVC-U-Kappe d50 | 24.0 Stk | 24 Stk | 2.92/Stk | 70,08 EUR | OFFEN (E20) |
| `FIT-kupplung-d110` | PVC-U-Kupplung (Muffe) d110 | nicht platziert (je 1: 1.0) | 0 Stk | 19.34/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d20` | PVC-U-Kupplung (Muffe) d20 | nicht platziert (je 1: 1.0) | 0 Stk | 1.19/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d25` | PVC-U-Kupplung (Muffe) d25 | nicht platziert (je 1: 1.0) | 0 Stk | 1.24/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d32` | PVC-U-Kupplung (Muffe) d32 | nicht platziert (je 1: 1.0) | 0 Stk | 1.33/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d40` | PVC-U-Kupplung (Muffe) d40 | 2.0 Stk | 2 Stk | 1.95/Stk | 3,90 EUR | OFFEN (E20) |
| `FIT-kupplung-d50` | PVC-U-Kupplung (Muffe) d50 | 7.0 Stk | 7 Stk | 2.38/Stk | 16,66 EUR | OFFEN (E20) |
| `FIT-kupplung-d63` | PVC-U-Kupplung (Muffe) d63 | nicht platziert (je 1: 1.0) | 0 Stk | 3.22/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-kupplung-d75` | PVC-U-Kupplung (Muffe) d75 | nicht platziert (je 1: 1.0) | 0 Stk | 8.03/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-leerrohr-bogen45-dn100` | Leerrohr-Bogen 45 Grad dn100 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-bogen45-dn50` | Leerrohr-Bogen 45 Grad dn50 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-bogen90-dn100` | Leerrohr-Bogen 90 Grad dn100 | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-bogen90-dn50` | Leerrohr-Bogen 90 Grad dn50 | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-red-dn100_dn50` | Leerrohr-Reduzierung dn100_dn50 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-t-dn100` | Leerrohr-T-Stueck dn100 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-leerrohr-t-dn50` | Leerrohr-T-Stueck dn50 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-red-d110_d63` | PVC-U-Reduzierung d110_d63 | nicht platziert (je 1: 1.0) | 0 Stk | 10/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d25_d20` | PVC-U-Reduzierung d25_d20 | nicht platziert (je 1: 1.0) | 0 Stk | 0.8/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d32-d25` | PVC-U-Reduzierung d32 auf d25 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-red-d32_d25` | PVC-U-Reduzierung d32_d25 | nicht platziert (je 1: 1.0) | 0 Stk | 1.38/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d40_d20` | PVC-U-Reduzierung d40_d20 | nicht platziert (je 1: 1.0) | 0 Stk | 1.51/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d40_d32` | PVC-U-Reduzierung d40_d32 | nicht platziert (je 1: 1.0) | 0 Stk | 1.25/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-red-d50_d32` | PVC-U-Reduzierung d50_d32 | 2.0 Stk | 2 Stk | 1.67/Stk | 3,34 EUR | OFFEN (E20) |
| `FIT-red-d50_d40` | PVC-U-Reduzierung d50_d40 | 6.0 Stk | 6 Stk | 1.73/Stk | 10,38 EUR | OFFEN (E20) |
| `FIT-red-d63_d50` | PVC-U-Reduzierung d63_d50 | 8.0 Stk | 8 Stk | 2.14/Stk | 17,12 EUR | OFFEN (E20) |
| `FIT-red-d75_d50` | PVC-U-Reduzierung d75_d50 | 2.0 Stk | 2 Stk | 4.09/Stk | 8,18 EUR | OFFEN (E20) |
| `FIT-red-d75_d63` | PVC-U-Reduzierung d75_d63 | 6.0 Stk | 6 Stk | 4.09/Stk | 24,54 EUR | OFFEN (E20) |
| `FIT-reduktion-d16` | PVC-U-Reduktion/Huelse d16 | 28.0 Stk | 28 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-reduktion-d32` | PVC-U-Reduktion/Huelse d32 | 14.0 Stk | 14 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-reduktion-d50` | PVC-U-Reduktion/Huelse d50 | 14.0 Stk | 14 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-rinne-kappe-ablauf` | Rinnen-Endkappe Ablauf 130x100 | 76.0 Stk | 76 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-rinne-kappe-zulauf` | Rinnen-Endkappe Zulauf 130x100 | 76.0 Stk | 76 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FIT-stutzen-d16` | PVC-U-Stutzen d16 (Klebe/Gewinde) | 4.0 Stk | 4 Stk | 1.98/Stk | 7,92 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d20` | PVC-U-Stutzen d20 (Klebe/Gewinde) | nicht platziert (je 1: 3.0) | 0 Stk | 1.98/Stk | 0,00 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d25` | PVC-U-Stutzen d25 (Klebe/Gewinde) | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-stutzen-d32` | PVC-U-Stutzen d32 (Klebe/Gewinde) | 1.0 Stk | 1 Stk | 2.13/Stk | 2,13 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d40` | PVC-U-Stutzen d40 (Klebe/Gewinde) | 4.0 Stk | 4 Stk | 2.95/Stk | 11,80 EUR | OFFEN (Quelle) |
| `FIT-stutzen-d50` | PVC-U-Stutzen d50 (Klebe/Gewinde) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `FIT-stutzen-d63` | PVC-U-Stutzen d63 (Klebe/Gewinde) | 2.0 Stk | 2 Stk | 5.41/Stk | 10,82 EUR | OFFEN (Quelle) |
| `FIT-t-d110` | PVC-U-T-Stueck d110 | nicht platziert (je 1: 1.0) | 0 Stk | 35.87/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d20` | PVC-U-T-Stueck d20 | nicht platziert (je 1: 1.0) | 0 Stk | 1.74/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d25` | PVC-U-T-Stueck d25 | nicht platziert (je 1: 4.0) | 0 Stk | 1.86/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d32` | PVC-U-T-Stueck d32 | nicht platziert (je 1: 1.0) | 0 Stk | 1.98/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d40` | PVC-U-T-Stueck d40 | nicht platziert (je 1: 1.0) | 0 Stk | 2.92/Stk | 0,00 EUR | OFFEN (E20) |
| `FIT-t-d50` | PVC-U-T-Stueck d50 | 3.0 Stk | 3 Stk | 4.08/Stk | 12,24 EUR | OFFEN (E20) |
| `FIT-t-d63` | PVC-U-T-Stueck d63 | 4.0 Stk | 4 Stk | 8.21/Stk | 32,84 EUR | OFFEN (E20) |
| `FIT-t-d75` | PVC-U-T-Stueck d75 | 4.0 Stk | 4 Stk | 14.27/Stk | 57,08 EUR | OFFEN (E20) |
| `FIT-uebergang-pe-pvc-pe_pvc_d20` | Uebergang PE auf PVC-U pe_pvc_d20 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
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
| `ARM-bulkhead-d40` | PVC-U-Bulkhead d40 | 14.0 Stk | 14 Stk | 35.77/Stk | 500,78 EUR | OFFEN (Quelle) |
| `ARM-bulkhead-d50` | PVC-U-Bulkhead d50 (Tankverbinder, Tankdurchfuehrung) | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-bulkhead-d63` | PVC-U-Bulkhead d63 (Tank-/Behaelterdurchfuehrung) | 2.0 Stk | 2 Stk | 49.02/Stk | 98,04 EUR | OFFEN (Quelle) |
| `ARM-bulkhead-pool` | Pool-Durchfuehrung d63 (Stutzen Pool-Wand) | 7.0 Stk | 7 Stk | 49.02/Stk | 343,14 EUR | OFFEN (Quelle) |
| `ARM-durchflussbegrenzer-messing` | Durchflussbegrenzer Messing [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-kabeleinfuehrung-dn100` | Kabeleinfuehrung dn100 | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-kabeleinfuehrung-dn50` | Kabeleinfuehrung dn50 | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `ARM-kugelhahn-d110` | PVC-U-Kugelhahn d110 | nicht platziert (je 1: 1.0) | 0 Stk | 323.86/Stk | 0,00 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d20` | PVC-U-Kugelhahn d20 | nicht platziert (je 1: 4.0) | 0 Stk | 23.53/Stk | 0,00 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d25` | PVC-U-Kugelhahn d25 | 2.0 Stk | 2 Stk | 28.04/Stk | 56,08 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d32` | PVC-U-Kugelhahn d32 | nicht platziert (je 1: 1.0) | 0 Stk | 35.34/Stk | 0,00 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d40` | PVC-U-Kugelhahn d40 | 4.0 Stk | 4 Stk | 44.97/Stk | 179,88 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d50` | PVC-U-Kugelhahn d50 | 2.0 Stk | 2 Stk | 53.47/Stk | 106,94 EUR | OFFEN (E20) |
| `ARM-kugelhahn-d63` | PVC-U-Kugelhahn d63 | 2.0 Stk | 2 Stk | 79.02/Stk | 158,04 EUR | OFFEN (E20) |
| `ARM-kugelhahn-feder_d40` | PVC-U-Kugelhahn feder_d40 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-probehahn-messing` | Probierhahn Messing 1/2 Zoll [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `ARM-rsv-d20` | PVC-U-Rueckschlagventil d20 | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (E20) - kein Angebot mit Preis in data/beschaffung |
| `ARM-rsv-d25` | PVC-U-Rueckschlagventil d25 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (E20) - kein Angebot mit Preis in data/beschaffung |
| `ARM-rsv-d40` | PVC-U-Rueckschlagventil d40 | nicht platziert (je 1: 3.0) | 0 Stk | - | - | OFFEN (E20) - kein Angebot mit Preis in data/beschaffung |
| `ARM-schwimmerventil-pool` | Schwimmerventil Pool (Gehaeuse, Wangen, Hebelarm mit Kugel) [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |

## SCH Schlauch, Schelle, Tuelle

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `SCH-rohrschelle-d110` | Rohrschelle (Klemme, Stahl) d110 | nicht platziert (je 1: 1.0) | 0 Stk | 2.58/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d20` | Rohrschelle (Klemme, Stahl) d20 | nicht platziert (je 1: 1.0) | 0 Stk | 0.83/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d25` | Rohrschelle (Klemme, Stahl) d25 | nicht platziert (je 1: 1.0) | 0 Stk | 0.84/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d32` | Rohrschelle (Klemme, Stahl) d32 | nicht platziert (je 1: 1.0) | 0 Stk | 0.79/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d40` | Rohrschelle (Klemme, Stahl) d40 | nicht platziert (je 1: 1.0) | 0 Stk | 1.13/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d50` | Rohrschelle (Klemme, Stahl) d50 | nicht platziert (je 1: 1.0) | 0 Stk | 1.27/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-rohrschelle-d63` | Rohrschelle d63 (Stahl verzinkt, Doppelschelle) | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-rohrschelle-vk-vk_d32` | Rohrschelle VK vk_d32 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-rohrschelle-vk-vk_d63` | Rohrschelle VK vk_d63 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauch-id16` | Schlauch ID16 (Meterware) | nicht platziert (je 1: 1.1) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauch-id25` | Schlauch ID25 (Meterware) | nicht platziert (je 1: 1.0) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauch-rinne-id16` | Schlauch ID16, 110 mm Stueck (Rinne Zulauf) | 76.0 Stk | 76 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauchbogen90-id16` | Schlauchbogen 90 Grad id16 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauchbogen90-id25` | Schlauchbogen 90 Grad id25 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SCH-schlauchschelle-id16` | Schlauchschelle id16 | nicht platziert (je 1: 1.0) | 0 Stk | 0.63/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-schlauchschelle-id25` | Schlauchschelle id25 | nicht platziert (je 1: 1.0) | 0 Stk | 0.65/Stk | 0,00 EUR | OFFEN (E20) |
| `SCH-schlauchtuelle-d12` | Schlauchtuelle (PVC) | nicht platziert (je 1: 1.0) | 0 Stk | 1.33/Stk | 0,00 EUR | OFFEN (Quelle) |
| `SCH-schlauchtuelle-d25` | Schlauchtuelle d25 (PVC) | 4.0 Stk | 4 Stk | 2.95/Stk | 11,80 EUR | OFFEN (Quelle) |

## SRB Schraube, Mutter, Scheibe, Bolzen

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `SRB-halter-klein-12x10x20` | Kleinteil am Winkelhalter 12x10x20 (Schraube/Mutter) [A] | 456.0 Stk | 456 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (Satz), Umrechnung offen |
| `SRB-satz-m10x60` | Schraubensatz M10x60 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 130.0 Satz | 130 Satz | 0.29/Satz | 37,70 EUR | OK |
| `SRB-satz-m12x55` | Schraubensatz M12x55 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 10.0 Satz | 10 Satz | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SRB-satz-m16x300` | Schraubensatz M16x300 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 20.0 Satz | 20 Satz | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SRB-satz-m5x12` | Schraubensatz M5x12 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 304.0 Satz | 304 Satz | 0.06/Satz | 18,24 EUR | OK |
| `SRB-satz-m6x16` | Schraubensatz M6x16 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | nicht platziert (je 1: 2.0) | 0 Satz | 0.07/Satz | 0,00 EUR | OK |
| `SRB-satz-m6x20` | Schraubensatz M6x20 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 16.0 Satz | 16 Satz | 0.07/Satz | 1,12 EUR | OK |
| `SRB-satz-m6x40` | Schraubensatz M6x40 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 112.0 Satz | 112 Satz | 0.09/Satz | 10,08 EUR | OK |
| `SRB-satz-m6x55` | Schraubensatz M6x55 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | nicht platziert (je 1: 2.0) | 0 Satz | 0.11/Satz | 0,00 EUR | OK |
| `SRB-satz-m8x30` | Schraubensatz M8x30 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) | 184.0 Satz | 184 Satz | 0.13/Satz | 23,92 EUR | OK |

## BEH Behaelter und Becken

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `BEH-ak-kompositbehaelter-254x790` | Aktivkohle-Druckbehaelter Komposit 254x790 mm mit Steuerkopf [A] | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-ak-sedimentfilter` | Sedimentfilter-Set (Gehaeuse, Kopf, Patrone) [A] | nicht platziert (je 1: 1.0) | 0 Satz | 20.72/Satz | 0,00 EUR | OK |
| `BEH-becken-dritt` | Drittbecken (Eigenbau/Sonderanfertigung, Masse aus Modell) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-drittbecken-klein` | Drittbecken klein (Wanne 920x920x1055) | 1.0 Stk | 1 Stk | 680.68/Stk | 680,68 EUR | OK |
| `BEH-fass-hdpe` | HDPE-Fass 500 mm (Mischfass) | 1.0 Stk | 1 Stk | 43.99/Stk | 43,99 EUR | OK |
| `BEH-feinfilter-pp-630x440x610` | Feinfilter-Behaelter PP 630x440x610 (Eigenbau/Kaufteil offen) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-halter-box-gehaeuse` | Anschlussbox PS 200x150x100 mit Acryldeckel | nicht platziert (je 1: 1.0) | 0 Stk | 67.27/Stk | 0,00 EUR | OK |
| `BEH-ibc-1000l` | IBC-Container 1000 l mit Gitterkaefig und Palette (Puffer) | nicht platziert (je 1: 3.0) | 0 Stk | 229.94/Stk | 0,00 EUR | OK |
| `BEH-ibc-beetwanne` | IBC-Beetwanne HDPE (aus IBC geschnitten, Laenge je Beet) | 14.0 Stk | 14 Stk | 229.94/Stk | 3.219,16 EUR | OK |
| `BEH-kanister-hdpe` | HDPE-Kanister (Dosiervorrat) | 1.0 Stk | 1 Stk | 8.66/Stk | 8,66 EUR | OK |
| `BEH-messbecher-pp` | Messbecher PP 160x310 | nicht platziert (je 1: 1.0) | 0 Stk | 13.09/Stk | 0,00 EUR | OK |
| `BEH-messzelle-acryl` | Messzelle Acryl 315x315x260 | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (m2), Umrechnung offen |
| `BEH-pe-schachtaufsatz-600x200` | PE-Schachtaufsatz (Dom) Oe 600 x 200 mm fuer Tank [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BEH-pool-zentral` | Zentralpool (Eigenbau/Sonderanfertigung, Masse aus Modell) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-580-deckel` | PE-Tankdeckel 580 mm | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BEH-tank-pe-580x865` | PE-Tank 580 mm Durchm., 865 mm hoch (Kegelboden/Absetzer) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BEH-tank-pe-673-deckel` | PE-Tankdeckel 673 mm | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-673x1075` | PE-Tank 673 mm Durchm., 1075 mm hoch (Kegelboden/Absetzer) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-700-deckel` | PE-Tankdeckel 700 mm | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BEH-tank-pe-800x1000` | PE-Tank 800 mm Durchm., 1000 mm hoch (Kegelboden/Absetzer) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |
| `BEH-tank-pe-930-deckel` | PE-Tankdeckel 930 mm | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-tank-pe-930x1444` | PE-Tank 930 mm Durchm., 1444 mm hoch (Kegelboden/Absetzer) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `BEH-zweitbecken` | Zweitbecken (Eigenbau/Sonderanfertigung, Masse aus Modell) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |

## PMP Pumpe und Geblaese

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `PMP-dosierpumpe` | Dosierpumpe (Schlauchpumpe) | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `PMP-geblaese-luft` | Membrangeblaese Luft (Leistung offen, Bauteilblatt geblaese_luft) | nicht platziert (je 1: 1.0) | 0 Stk | 458.42/Stk | 0,00 EUR | OK |
| `PMP-pumpe-gross` | Kreiselpumpe gross | 4.0 Stk | 4 Stk | 233.79/Stk | 935,16 EUR | OK |
| `PMP-pumpe-klein` | Kreiselpumpe klein | 4.0 Stk | 4 Stk | 95.9/Stk | 383,60 EUR | OK |
| `PMP-teichpumpe-5300` | Teichpumpe 5300 l/h, 60 W, Hmax 2,8 m (Beet-Sumpf, Fabrikat offen) [A] | nicht platziert (je 1: 2.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Eintrag in data/beschaffung |

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
| `ELE-kabelverschraubung-pg` | Kabelverschraubung PA (PG/M20) | 1.0 Stk | 1 Stk | 0.485/Stk | 0,48 EUR | OK |
| `ELE-schaltschrank-500x800x1200` | Schaltschrank 500x800x1200 mm (leer, Ausruestung offen) | 1.0 Stk | 1 Stk | 469.97/Stk | 469,97 EUR | OK |

## FOL Folie, Plane, Dichtband, Dichtung

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `FOL-epdm-dichtband-zarge` | EPDM-Dichtband Zarge | nicht platziert (je 1: 2.043) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `FOL-epdm-dichtung-630x440` | EPDM-Flachdichtung 630x440x3 | 2.0 Stk | 2 Stk | 4.23/Stk | 8,46 EUR | OK |
| `FOL-epdm-schaumband` | EPDM-Schaumband 25x3 | nicht platziert (je 1: 3.019) | 0.0 m | 2.29/m | 0,00 EUR | OK |
| `FOL-epdm-tuerdichtung` | EPDM-Tuerdichtung | 5.988 m | 25.0 m (1 x 25000 mm) | 1.64/m | 41,00 EUR | OK |
| `FOL-pe-plane` | PE-Planenbahn (Huelle, Zuschnitt je Feld, Flaeche aus Modell) | 1015.8418 m2 | 1117.43 m2 | 2.05/m2 | 2.290,73 EUR | OK |

## GEW Gewebe und Netz

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `GEW-v2a-100um` | Edelstahl-Siebgewebe 100 um, 1.4301 (Siebkorb, Flaeche aus Modell) | 2.0208 m2 | 2.23 m2 | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |

## TOP Topf und Substrat

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `TOP-aktivkohle` | Aktivkohle-Granulat (Behaelterfuellung) | nicht platziert (je 1: 0.042) | 0.0 m3 | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (Packung/Sack), Umrechnung offen |
| `TOP-biomedium` | Biomedium (Biofilter-Fuellkoerper) | 1.29 m3 | 1.36 m3 | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `TOP-blaehton` | Blaehton-Substrat 8-16 mm (Beetfuellung) | 7.5211 m3 | 7.9 m3 | 314/m3 | 2.480,60 EUR | OK |
| `TOP-netztopf-64` | Netztopf PP 64 mm (Pflanzkorb, Stueckzahl aus Instanzen) | 2222.0 Stk | 2222 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |

## SON Sonderteil (Eigenbau mit Rohmaterial als Kaufteil, Tuer, Haut, Knoten)

| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |
|---|---|---|---|---|---|---|
| `SON-ak-konsole` | Konsole Sedimentfilter (Stahl, Eigenbau) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-ankergabel-80x140` | Gabelkopf 80x140 (Fundamentanker, Stahl, Zuschnitt) | 20.0 Stk | 20 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-ankerlasche` | Ankerlasche am Knoten (Stahl, Zuschnitt) | 10.0 Stk | 10 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-belueftungsgitter-460` | Belueftungsgitter 460x460 (PVC, Tankdeckel) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-federdraht-d2` | Federstahldraht d2 (Keilschiene) | nicht platziert (je 1: 2.979) | 0.0 m | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-gummifuss-40` | Gummifuss 40x40x15 | nicht platziert (je 1: 4.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-halter-inline-d32-sensorblock` | Sensorblock (halter_inline_d32, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d32-sieb` | Sieb halter_inline_d32 (Edelstahl) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d32-vorfilter` | Vorfilter (halter_inline_d32, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d50-sensorblock` | Sensorblock (halter_inline_d50, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d50-sieb` | Sieb halter_inline_d50 (Edelstahl) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-inline-d50-vorfilter` | Vorfilter (halter_inline_d50, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-halter-zelle-zellkoerper` | Zellkoerper (halter_zelle, Eigenbau aus PVC-U) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-holz-stuetzrippe` | Stuetzrippe Fichte (Tank-Auflage) | 10.0 Stk | 10 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-knotenarm-23x23x3` | Steckarm 23x23x3 am Knoten (Verbindungsstueck, N-STATIK W43 offen) | 130.0 Stk | 130 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-knotenkugel-d100` | Knotenkugel d100, Stahl (Verbindungsstueck, N-STATIK W43 offen) | 26.0 Stk | 26 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-korbgriff-v2a` | Korbgriff Edelstahl (Eigenbau) | 4.0 Stk | 4 Stk | 13.24/Stk | 52,96 EUR | OK |
| `SON-luftverteiler-4` | Luftverteiler 4-fach (PVC, Eigenbau) [A] | 1.0 Stk | 1 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-luftverteiler-6` | Luftverteiler 6-fach (PVC, Eigenbau) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-pflanztisch-platte` | Pflanztischplatte (Alt-Modell, nicht verbaut) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-plattform-619x619` | Tankplattform 619x619x73 (Stahl, Eigenbau) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-plattform-821x821` | Tankplattform 821x821x98 (Stahl, Eigenbau) | 2.0 Stk | 2 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-polycarbonat-paneel` | Polycarbonat-Paneel 8 mm (Zuschnitt je Feld) | nicht platziert (je 1: 3.0) | 0 Stk | - | - | OFFEN (Quelle) - Angebote in anderer Bezugseinheit (m2), Umrechnung offen |
| `SON-pp-stuetze-60x60` | PP-Stuetze 60x60 (Beetboden, Hoehe je Beet) | 282.0 Stk | 282 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-schacht-kugelhahn-d63` | Schacht fuer Kugelhahn (PE-HD) d63 | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-scheibenbelueftung-270` | Scheibenbelueftung d270 (Tragteller, Stuetzfuss, EPDM-Membran) [A] | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-schrankwand-500x800` | Schrankwand 500x800 (Eigenbau, Werkstoff offen) [A] | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung; Eigenbau, Rohmaterial in anderen Zeilen |
| `SON-sondenhalter-36` | Sondenhalter 36x36x40 (PVC, Eigenbau/Stuetze) | nicht platziert (je 1: 4.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-spannverschluss-edelstahl` | Spannverschluss Edelstahl (Bock + Hebel) | 8.0 Stk | 8 Stk | 23.03/Stk | 184,24 EUR | OK |
| `SON-strahlungsschutz-par` | Strahlungsschutz PP weiss (Messmast) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-tanksieb-stahl` | Sieb am Tank (Stahl verzinkt, Zulauf/Auslauf) | 4.0 Stk | 4 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-tauchklemme` | Klemme Tauchrohr (Stahl, Eigenbau) | 3.0 Stk | 3 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
| `SON-tuer-modellvariante` | Tuer (Alt-Modell, nicht verbaut) T4_Pfosten_L | nicht platziert (je 1: 4.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot mit Preis in data/beschaffung |
| `SON-tuerblatt-1000x2000` | Tuerblatt Sandwich 1000x2000x40 | 1.0 Stk | 1 Stk | 749/Stk | 749,00 EUR | OK |
| `SON-tuerdruecker` | Tuerdruecker mit Rosette | 2.0 Stk | 2 Stk | 16.06/Stk | 32,12 EUR | OK |
| `SON-tuerscharnier` | Tuerscharnier (Zargenlasche, Blattlasche, Bolzen) | 3.0 Stk | 3 Stk | 2.49/Stk | 7,47 EUR | OK |
| `SON-zarge-aufsatzrahmen` | Alu-Aufsatzrahmen Tuerzarge (Planenausschnitt) | nicht platziert (je 1: 1.0) | 0 Stk | - | - | OFFEN (Quelle) - kein Angebot in Europa mit bekanntem Land |
