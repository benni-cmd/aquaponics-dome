# Auswertung `Project_Oasis_Layout.obj` (Wahrheitsquelle, 29.10.2026)

Quelle: `C:\Users\benkn\Downloads\Project_Oasis_Layout.obj` (SketchUp-Export, 53 MB, Meter, Y = oben; nicht im Repo, zu gross).
Reproduzierbar mit `python scripts/analyze_oasis_obj.py`. Der OBJ ist die genauere Quelle als die Blender-Bilder
(Ben, 29.10.2026: in den Bildern sind einzelne Bauteile falsch, z. B. nur 2 Rohre je NFT-System aussen, nur ein Beispiel je NFT-Typ).
Rangfolge der Quellen: Ben-Aussagen > OBJ > Blender-Bilder.

Kuppelmitte im OBJ: x = 24,63, z = 63,34 (alle Radien/Azimute unten relativ dazu; Azimut = atan2(z, x)).

## Kuppel T1
- Gruppenname `Acidome_*_Cone_D0_2V_R6_beams_30x30`: 2V, Radius 6 m (= 12 m), Balken 30 x 30 mm (quadratisch, nicht rund).
- 65 Strebengruppen (64 + 1 Sonderstueck), Strebenlaenge ca. 3,08 m. Scheitel y = 6,99 m ueber Szenen-Nullpunkt; Boden/Tankfuesse liegen bei y = 1,00, die Kuppel ist also 6 m ueber einem Boden bei y = 1,0 (Sockelhoehe pruefen).

## Zentraltank T5
- Wasserscheibe 3,89 m Durchmesser, Mittelpunkt im Kuppelzentrum (r = 0,04 m), Wasserspiegel y = 1,51.
- Unser Modell setzt ihn 0,45 m aus der Mitte: korrigieren auf zentriert.

## Pflanztoepfe / NFT-Systeme (T8)
- 2160 Toepfe (`potplant_dxf`), je 0,05 x 0,06 x 0,06 m, 204 Eckpunkte, ALLE aussen am Kuppelrand: Radius 4,78 bis 5,78 m (1693 bei ca. 5 m, 467 bei ca. 6 m), Hoehe y = 1,41 bis 1,54.
- Azimutbelegung: 0-150 Grad und 240-360 Grad belegt, Luecke 150-240 Grad (Tuerseite). Etwa 230 Toepfe je 30-Grad-Sektor.
- Toepfe liegen auf zwei Hoehenstufen (1,4 und 1,5) = geneigte NFT-Rohre (Gefaelle ca. 0,13 m).
- Folgerung: Die NFT-Anlage ist ein durchgehender Ring langer Rohre aussen entlang der Kuppelwand mit Tuerlucke, nicht 10 einzelne Tische. Die Blender-Bilder zeigen nur ein Beispiel.
- Erhoehte Hydroponik-Tische `Hidrtoponia_Mixta` / `Diferencia` (Platten mit Loechern): 3,02 x 1,39 m (2 Stueck, r 4,9-5,2, Hoehe y 2,3), 1,96 x 0,57 m (4 Stueck, r 3,0-3,8, y 2,3, Azimut 283), 1,30 x 0,40 m (2 Stueck, r 1,7-2,0, y 1,85). Netztopf 0,03 x 0,11 x 0,13 m.

## Substratbeete T9 (IBC halb geschnitten, `IBC_Open_Top`)
- 14 Stueck, Hoehe 0,64 m, Mitte y = 1,0.
- 8 aussen, r ca. 5,2 m, Azimute 355, 319, 247, 31, 140, 67, 283, 103, Laenge ca. 3,0 m.
- 6 innen, r ca. 3,3 m, Azimute 318, 103, 283, 67, 30, 354, Laenge ca. 1,2-2,0 m.

## Tanks T7 / Vortexfilter
- Nur 4 Tanks (`1000_plastic_tank`), alle auf der Tuerseite, r ca. 3,3-3,4 m: Azimut 237 und 147 (0,67 m Durchmesser, 1,08 m hoch), Azimut 131 und 252 (0,93 m, 1,44 m hoch).
- Je Tank: Plattform 0,71 x 0,07 x 0,71 m auf Beinen (0,03 x 0,75 bzw. 0,04 x 1,01 m), Pumpen-/Filtermodule 0,46 x 0,35 x 0,20 m, Rohrfittings (PVC Bulkhead mit Dichtung, ca. 0,04-0,06 m) nahe dem Tankboden (y ca. 1,2). `Base_of_tank`: 108 Einzelteile gesamt.
- Unser Modell hat 6 Fasstanks mit 1,1 m Durchmesser: falsch, auf 4 Tanks mit diesen Massen aendern.

## Offene Fragen (Sitzung klaeren, in Paket vermerken)
1. Bodenhoehe: Stehen Boden/Sockel bei y = 1,0 (1 m hoher Unterbau?) oder ist y = 1,0 nur die Fusshoehe der Tankplattformen? Strebenknoten niedrigste y ermitteln.
2. Genaue Rohrgeometrie der NFT-Ringe (Rohrdurchmesser, Abstand, Anzahl Reihen): aus den Topfpositionen ableiten (Hoehen- und Radienstufen).
3. Wo die Zulaufrohre, Pumpen und Schlauchfuehrung liegen: Gruppen `Group#`/`Component#` im OBJ lesen.
