# Bauteil-Spezifikation (aus dem OASIS-OBJ abgeleitet, Maße in mm)

Rohzahlen: `data/layout.json`, Tabellen: `docs/layout.md` (beide erzeugt von `scripts/extract_layout.py`). Rangfolge: Ben > OBJ-Zahlen > Bilder (Look). Koordinaten: Ursprung Kuppelmitte am Boden, Z nach oben, Azimut gegen den Uhrzeigersinn.
**Drehung:** Im OBJ liegt die Tuer bei Azimut ca. 167 Grad (Mitte der Luecke zwischen den Aussenbeeten bei 149 und 185 Grad; das zweite Becken liegt direkt davor). Unser Modell hat die Tuer bei `door_az` = -54. Das ganze Layout wird um `layout_rot = door_az - 167` um Z gedreht (Parameter in `P`), damit die Tuer wie in ref-4 vorne rechts liegt.

## Sektoren-Prinzip
Der Sockel ist ein Zehneck: 10 Sektoren zu je 36 Grad, Mitte der Aussenbeete bei Azimut 5,3 + 36 k. In 8 Sektoren steht ein Aussenbeet (k = 0-3 und 5-8 ohne die zwei Tuersektoren bei 149 und 185 Grad), in 6 Sektoren ein Innenbeet. Je Sektor: Beet unten, NFT-Rinnen darueber. Die vier Tanks stehen in den Sektoren um 108-123 Grad und 213-229 Grad.

## Wiederkehrende Bauteile (jedes EINMAL definieren, per Tabelle platzieren)

| Bauteil | Anzahl | Maße | Lage / Besonderheit |
|---|---|---|---|
| Strebe A | 30 | Laenge 3279 (= 0,5465 R), Profil 30 x 30 | 2V, R = 6000 |
| Strebe B | 35 | Laenge 3708 (= 0,6180 R), Profil 30 x 30 | 2V, R = 6000 |
| Knoten | 26 | 6 fuenfwertig (Apex + 5), 10 sechswertig, 10 vierwertig (Basis) | Positionen in `layout.json` `dome.nodes_list`; Scheitel Z = 5986 |
| Aussenbeet (halber IBC) | 8 | 2953 x 933..993 x 637, Oberkante Z ca. 475 | r ca. 5200, tangential; Unterkante laut OBJ -160..-210 (Beet eingelassen); Pflanztoepfe in Reihen: 288 je Beet (Beet am Azimut 113: 144) |
| Innenbeet (halber IBC) | 6 | 1865 x 933 x 649 | r ca. 3340, tangential; ohne Pflanzen im OBJ |
| Pflanztopf/Netztopf | 2160 | 50 x 64 x 63 | Z 407..506 im Aussenbeet; Raster aus den Topfpositionen in `layout.json` ableiten (288 = z. B. 24 x 12) |
| NFT-Rinne | siehe Zeile | Breite 130, Tiefe 100, Laenge je Tisch 3232 / 1983 / 1304 | Rinnenabstand 263-288; Aussentisch r 4888 und 5176 (Z 1291-1325) ueber dem Aussenbeet; Mitteltisch 4 Rinnen r 2987-3775 (Z 1280-1330) ueber dem Innenbeet; Innentisch 2 Rinnen r 1733 und 1995 (Z 819-858). Das OBJ zeigt je Typ nur EIN Beispiel: je Beet die Rinnenzahl so waehlen, dass die Beetbreite abgedeckt ist (Aussen 3 Rinnen, Mitte 4, Abstand 263-288), in allen Sektoren wiederholen |
| Vortexfilter (kleiner Tank) | 2 | Durchmesser 673, Hoehe 1075 inkl. Kegelboden, Kegelspitze Z ca. 170, Plattform 706 x 707 x 73 auf Z 428, 4 Beine 30 x 30 x 751 | Azimut 123 (r 3420) und 213 (r 3319); Ablauf-Fittings (PVC Bulkhead 30-40) an der Kegelspitze |
| Grosser Tank (Biofilter/Sump) | 2 | Durchmesser 930, Hoehe 1444 inkl. Kegelboden, Spitze Z ca. 228, Plattform 977 x 976 x 98 auf Z 570, 4 Beine 40 x 40 x 1008 | Azimut 108 (r 3391) und 229 (r 3346); Fittings 41-56 an der Spitze |
| Pump-/Filtermodule | je Tank 4-8 | 502 x 345 (klein), 384 x 419 (gross), Platten 693 x 463 | Positionen je Tank in `layout.json` `tanks[].modules`; Bedeutung noch Annahme |
| Pool | 1 | Durchmesser 3890, Wasserspiegel Z 515, Mitte (-36, 20) | Wasserspiegel gleich im zweiten Becken |
| Zweites Becken | 1 | Durchmesser 1747, Wasserspiegel Z 515, r 3017, Azimut 166 | direkt vor der Tuer (der flache Rundtank aus ref-4) |
| Tuer | 1 | 1000 x 2000 | Normtuer, Azimut 167 im OBJ |

## Bauvorgaben fuer die Modell-Sitzung
1. Pro wiederkehrendem Bauteil EINE Definition mit Parametern (Datei `scripts/components/<name>.py` oder SolidCraft-Komponente), die Platzierungen stehen als Tabelle aus `data/layout.json` (Mitte, Azimut/Radius, yaw, Z). Das Dom-Skript liest `layout.json`, keine Zahlen im Skript wiederholen.
2. Aussehen kommt aus ref-4 bis ref-6 (Farben, Rinnen mit Rippen, Beine, Schlaeuche); Anzahl, Lage und Maße aus dieser Tabelle. Widerspruch: OBJ gewinnt bei Maßen, Bild bei Material.
3. `scripts/check_fidelity.py` vergleicht das Modell je Klasse mit `layout.json` (Anzahl, mittlere Positionsabweichung nach `layout_rot`).
4. Kegelboeden der Tanks beachten: Zylinder oberhalb der Plattform, Kegel darunter bis zur Fitting-Spitze. Fittings sind die Anschluss-Ports fuer den Wasserkreislauf (`data/system.json`).
5. NFT-Rinnen mit leichtem Gefaelle (Wasser soll laufen); Hoehe und Gefaelle in `docs/hydraulics.md` festlegen. Die Z-Werte im OBJ sind Unterkanten der ganzen Rinne.

## NFT-Ringe: drei Zehneck-Ringe (Auswertung 29.10.2026, nach Bens Hinweis auf den inneren Ring ueber dem Pool)

Das OBJ zeigt je Ring nur EIN Beispiel (Azimut ca. 78 bzw. 113 Grad). Die Rinnenlaengen passen exakt auf regelmaessige Zehnecke (Seite = 2 x Apothem x tan 18 Grad), also sind es durchgehende Ringe mit je einem Tisch je 36-Grad-Sektor, gleiche Sektor-Azimute wie die Beete (5,3 + 36 k im OBJ-Koordinatensystem, im Modell um `layout_rot` gedreht):

| Ring | Apothem der Rinnen (mm) | Rinnen je Tisch | Rinnenlaenge | Pruefung (2 x Apothem x tan 18) | Z (Unterkante) | Tische |
|---|---|---|---|---|---|---|
| Innen, ueber dem Pool | 1733 und 1995 (Abstand 262) | 2 | 1304 | 2 x 1995 x 0,3249 = 1296 | 819 und 858 | 10 (voller Ring; Tuerseite pruefen) |
| Mitte, ueber den Innenbeeten | 2987, 3248, 3514, 3775 (Abstand ca. 263) | 4 | 1983 | Seite bei Apothem 3,4 m = 2210, Tisch kuerzer, also einzelne Tische mit Luecke | 1280-1330 | 6 (Sektoren der Innenbeete) |
| Aussen, ueber den Aussenbeeten | 4888 und 5176 (Abstand 288) | 2 (im OBJ; je Beet nach Beetbreite 3) | 3232 | 2 x 5000 x 0,3249 = 3249 | 1291-1325 | 8 (Sektoren der Aussenbeete) |

Der innere Ring haengt ueber dem Pool: Pool-Wasserradius 1945 mm, Beckenrand Z ca. 650, Rinnen auf Z 819-858 darueber, also etwa 170-210 mm ueber dem Rand. Die innere Rinne (Apothem 1733) ist als Zehneck mit Seite 1126 mm kuerzer als die Rinnenlaenge 1304: Gehrung/Ueberlappung an den Ecken klaeren oder Rinnen entsprechend kuerzen. Das zweite Becken liegt bei Azimut 166, r 3017, Radius 873: sein inneres Ende bei r 2144 liegt knapp ausserhalb der aeusseren inneren Rinne (1995 plus halbe Rinnenbreite 65 = 2060). Aufhaengung/Stuetzen des inneren Rings (ausserhalb des Pools auf Beinen oder Ausleger vom Beckenrand) aus dem Bild ref-4 und der OBJ-Geometrie ableiten und im Bauteilblatt festhalten.
Dome-Pruefung: Basis-Zehneck mit Umkreisradius 6000 hat Seitenlaenge 2 x 6000 x sin 18 = 3708 mm = Strebe B; Apothem 5706 mm. Die aeussere Rinne (Apothem 5176 + 65) liegt damit gut 0,4 m innerhalb der Kuppelwand.
