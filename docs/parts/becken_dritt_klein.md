# Bauteilblatt T14k becken_dritt_klein (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/becken_dritt_klein.json` und `designs/components/becken_dritt_klein.sc`, nicht von Hand aendern)

**Funktion:** Drittbecken als Quarantaene- und Notbecken fuer Zuchttiere oder Kranke (R37 Befund 10): 0,4 m3 Wasser, eingelassen in den Boden wie Pool und Zweitbecken. Der Pool (346 kg Fisch) laesst sich in keinem Becken auffangen. Eigener Biofilter (37 l Bioballs) und Belueftung sind noetig und liegen ausserhalb dieses Bauteils.

**Datei:** `designs/components/becken_dritt_klein.sc` · **Teilenummer:** T14k · **Revision:** A · **Bezugspunkt:** Mitte der Beckenunterkante (Z 0 = Unterkante Boden); Z hoch; Einbau: Z 0 liegt bei Wasserspiegel Z 515 minus 920 = Z -405 im Modellrahmen

**Anzahl (Instanzen):** 1 Drittbecken mit 4 Stutzen (Quelle: D46/D49 (Lage Zwickel Tuer/Station, Platzierung Montage); D66: klein)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `wasser_d` | 800 | mm | [E] R37 Befund 10 / Auftrag W34: Wasserdurchmesser (Innendurchmesser) 800 mm; ersetzt pool3_d 1030 |
| `wasser_tiefe` | 800 | mm | [E] R37 Befund 10 / Auftrag W34: Wassertiefe 800 mm (0,4 m3 = Ø 0,8 x 0,8 m); der Bestand pool3_depth 1130 war die Tiefe einschliesslich des 120-mm-Bodens bis zum Wasserspiegel |
| `ring` | 60 | mm | [E] Auftrag W34 / R37 Befund 10: Ring 60 mm (wie Zweitbecken und Drittbecken im Bestand) |
| `boden` | 120 | mm | [E] Bestand gen_dome.py pool_fn: Hohlraum beginnt 120 mm ueber der Unterkante |
| `wasser_spiel` | 10 | mm | [E] Bestand gen_dome.py pool_fn: Wasserkoerper Ø d - 10 (5 mm Luft zur Wand, keine Beruehrung) |
| `rand_ueber_wasser` | 135 | mm | [E] data/params.json pool_rim 650 minus data/layout.json pool2.water_z 515 (Rand Z 650, Wasserspiegel Z 515, wie Pool und Zweitbecken) |
| `pool3_d_neu` | 800 | mm | [R] Wert fuer data/params.json pool3_d (Montage setzt ihn; vorher 1030) |
| `pool3_depth_neu` | 920 | mm | [R] Wert fuer data/params.json pool3_depth (Tiefe bis Wasserspiegel einschliesslich Boden 120: 800 + 120; vorher 1130) |
| `stutzen_h` | 60 | mm | [A] W37-2 Teil 3: Hoehe der Anschlussbloecke auf der Rand-Oberkante (Z 1055 bis 1115); Stutzenachse 30 mm darueber |
| `stutzen_blk_r` | 60 | mm | [E] Blockbreite radial = Ringbreite 60 (liegt auf der ebenen Rand-Oberkante) |
| `stutzen_blk_t` | 90 | mm | [A] Blockbreite tangential |
| `stutzen_len` | 70 | mm | [A] Stutzenrohr ausserhalb des Rings (Muffentiefe d25 = 19, d20 = 16) |
| `winkel_k41` | 0 | deg | [A] Azimut Stutzen K41 (Frischwasser d20); Vielfache von 90 Grad, endgueltige Lage Montage (Biofilter-Seite offen) |
| `winkel_k42` | 90 | deg | [A] Azimut Stutzen K42 (Entnahme zum Biofilter d25) |
| `winkel_k43` | 180 | deg | [A] Azimut Stutzen K43 (Rueckfluss vom Biofilter d25) |
| `winkel_k49` | 270 | deg | [A] Azimut Stutzen K49 (Luftschlauch ID16/AD20, Notstrom) |

Gesamt-Box (Messung): X -530.0 bis 530.0, Y -530.0 bis 530.0, Z 0.0 bis 1115.0 mm; Koerper: 6.

**Toleranzen / Spiel:** Rand 135 mm ueber dem Wasserspiegel; 5 mm Luft zwischen Wasserkoerper und Wand.

## Werkstoff und Gewicht

- Werkstoff: Beton (Platzhalter fuer die Ringwand), Dichte 2.4 g/cm3, Farbe #9a9a96 ([A] Wandwerkstoff nicht entschieden (Bestand ohne Material, Standarddichte); Beton als Platzhalter fuer eingelassene Becken)
- Volumen (Messung, `solidcraft-cli eval`): 232749.4 cm3 · Masse leer (ohne Wasser): 557164 g (557.16 kg)
- Gefuellt/in Betrieb: Wasser 392 l ca. 392 kg [E, Dichte 1]

## Querschnitt / Profil

Zylinderwanne: Aussen Ø 920, Hohlraum Ø 800 ab 120 mm ueber der Unterkante, Gesamthoehe 1055 mm (Boden 120 + Wassertiefe 800 + Rand 135). Wasserkoerper Ø 790 x 800.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| K41 Frischwasser-Zulauf (aus der Aktivkohle-Station) | PVC-U d20 (DN15), Klebemuffe aussen, Einstecktiefe 16 | x 530, y 0, z 1085 (Mitte der Oeffnung) | Oeffnung zeigt +X (Azimut 0 Grad, Parameter winkel_k41); Wasserwechsel 2 l/min |
| K42 Entnahme zum Biofilter | PVC-U d25 (DN20), Klebemuffe aussen, Einstecktiefe 19 | x 0, y 530, z 1085 | Oeffnung zeigt +Y (Azimut 90 Grad, winkel_k42); Umlauf 5 l/min |
| K43 Rueckfluss vom Biofilter | PVC-U d25 (DN20), Klebemuffe aussen, Einstecktiefe 19 | x -530, y 0, z 1085 | Oeffnung zeigt -X (Azimut 180 Grad, winkel_k43); 5 l/min |
| K49 Luftschlauch (Belueftung, Notstrom) | Schlauchtuelle Aussen-Ø 20, Bohrung Ø 16 (Schlauch ID16/AD20) | x 0, y -530, z 1085 | Oeffnung zeigt -Y (Azimut 270 Grad, winkel_k49); Luft 2 l/min, Geblaese in W37-3 |

## Verbindungen und Befestigungen

- Wanne unveraendert (W34). Neu W37-2 Teil 3: vier Anschluss-Stutzen K41, K42, K43, K49 als eigene Koerper (Block 60 x 90 x 60 auf der ebenen Rand-Oberkante, radiales Stutzenrohr 70 mm nach aussen), keine Boolean-Operation an der Ringwand
- Die Stutzen sind Anschlusspunkte aussen am Rand; der Wasserweg ueber die Kante ins Becken (Tauchrohr/Saugkorb fuer K42, Einlauf K41/K43) ist Montage und nicht modelliert
- Ueberlauf/Ablauf des Wechselwassers: Montage, nicht Teil

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Drittbecken 0,4 m3: Wasser Ø 800 x 800 tief | 402 l Nennvolumen | E | R37 Befund 10 (Quarantaene, 31 Fische, 2,4 kg, 37-l-Biofilter); Auftrag W34 | mittel |
| Ring 60 mm, Aussendurchmesser 920 | Ø 920 | E | Auftrag W34; Bestand pool_fn (wall 60) | mittel |
| Grundflaeche mit Ring 0,66 m2 | 0,66 m2 | R | pi x 0,46^2 = 0,665 m2 (R37 Befund 10: 0,66 m2; Bestand 1,04 m2) | hoch |
| Rand 135 mm ueber dem Wasserspiegel | 135 | E | data/params.json pool_rim 650, layout pool2.water_z 515 (wie Pool/Zweitbecken) | hoch |
| Ringwand Beton | 2,4 g/cm3 | A | Wandwerkstoff offen; Bestand ohne Material | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R37.md Befund 10 (0,4 m3 = Ø 0,8 x 0,8 m, 37-l-Biofilter, Grundflaeche 0,66 m2 mit 60-mm-Ring); Bestand: scripts/gen_dome.py pool_fn (Boden 120, Wasser Ø d-10, Wand 60, Rand pool_rim 650, Wasserspiegel water_z 515)
- Abweichung zum OBJ: Bestand: Innen Ø 1030, Wassertiefe 1010 (pool3_depth 1130 bis Wasserspiegel), 825 l Wasser, Grundflaeche 1,04 m2. Neu: Innen Ø 800, Wassertiefe 800, 402 l Nennvolumen, Grundflaeche 0,66 m2. Der Bestand `designs/components/becken_dritt.sc` bleibt unveraendert (Montage-Datei, von gen_dome.py erzeugt).

## Montage (L4)

1. Grube Ø 920, Tiefe 1055 minus 135 Rand ueber Gelaende (Wasserspiegel Z 515, Rand Z 650)
2. Becken einsetzen, Wasserspiegel auf Z 515 einstellen

**Werkzeug:** Bagger oder Spaten, Wasserwaage

## Stueckliste-Zeile

- T14k Drittbecken klein: 1 Wanne Ø 920 x 1055 (Ringwand 60, Boden 120)
- 4 Anschluss-Stutzen (K41 d20, K42 d25, K43 d25 Klebemuffen; K49 Schlauchtuelle ID16) auf dem Rand

## Alternative lokale Fertigung

Fertigbecken PE Ø 920 oder Betonring DN 800 mit Bodenplatte; Rand 135 mm ueber dem Wasserspiegel.

## Renders

- `renders/components/becken_dritt_klein/becken_dritt_klein-01-schraeg.png`
- `renders/components/becken_dritt_klein/becken_dritt_klein-02-schnitt.png`
- `renders/components/becken_dritt_klein/becken_dritt_klein-03-stutzen.png`

## Pruefung

- Gauntlet-Urteil: Pruefer-Lauf: PASS, Befund in docs/jobs/pruefung/W37-2-W37-3.md.
- scripts/workshop/check_becken_dritt_klein.py (Ergebnis renders/components/becken_dritt_klein/check.txt): Durchmesser, Ring, Tiefe, Volumen 0,4 m3, Grundflaeche 0,66 m2, Rand, Wannenvolumen unveraendert, 4 Stutzen mit Ports K41 d20, K42 d25, K43 d25, K49 d20, Interferenz 0

## Offene Fragen

- Montage: data/params.json pool3_d 800 und pool3_depth 920 setzen (oder die neue Komponente verknuepfen); Lage D49 (Zwickel Tuer/Station) mit dem kleineren Becken neu pruefen (place_m8.py, Laufwegkarte)
- Wandwerkstoff (Beton oder PE) offen; Biofilter 37 l und Belueftung nicht modelliert (Leitungsnetz K35-K41: Montage)
- Stutzen: Azimut je Stutzen (winkel_*) vorlaeufig 0/90/180/270 Grad, Biofilter-Seite legt die Montage fest; Wasserweg ueber die Kante, Tauchrohr fuer K42 und Ueberlauf des Wechselwassers: Montage
- Wasserwechsel 2 l/min aus der Frischwasserleitung bzw. Zisterne (R37 Befund 9), Frischwasserquelle klaert Ben beim Versorger
