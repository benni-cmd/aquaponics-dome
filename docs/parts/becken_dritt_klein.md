# Bauteilblatt T14k becken_dritt_klein (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/becken_dritt_klein.json` und `designs/components/becken_dritt_klein.sc`, nicht von Hand aendern)

**Funktion:** Lebendfutterbecken (Quelle: Algen- oder Wasserflohzucht, gespeist mit gereinigtem Biofilterwasser aus Biofilter 1, Weg e62; Ueberlauf in das Anzuchtbecken, Weg e63): 0,57 m3 Wasser, steht auf dem Boden. Die Quarantaene-Funktion des bisherigen Drittbeckens (D46) entfaellt (D96). Eigener Biofilter und Belueftung liegen ausserhalb dieses Bauteils.

**Datei:** `designs/components/becken_dritt_klein.sc` · **Teilenummer:** T14k · **Revision:** B · **Bezugspunkt:** Mitte der Beckenunterkante (Z 0 = Unterkante Boden = Standflaeche); Z hoch; Einbau: Z 0 liegt auf dem Fussboden (Modell-Z 400), Wasserspiegel dann bei Z 1250; Einbau ohne Drehung (yaw 0), sonst dreht die Ueberlauf-Tuelle mit

**Anzahl (Instanzen):** 1 Lebendfutterbecken mit Ueberlauf-Tuelle d63 und 4 Stutzen (Quelle: D93, data/oasis-soll.json feed, Weg e63; Lage D110 (Bauplatz U1))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `wasser_d` | 1000 | mm | [Q] data/oasis-soll.json feed masse_text_mm.durchmesser 1000 (Innendurchmesser, D118) = data/params.json pool3_d (varianten_werte ring_b2) || UEBERHOLT (U3, D118): [E] R37 Befund 10 / Auftrag W34: Wasserdurchmesser (Innendurchmesser) 800 mm; ersetzt pool3_d 1030 |
| `wasser_tiefe` | 730 | mm | [E] Wasserspiegel 850 minus Boden 120 = 730 (data/oasis-soll.json feed wsp 850; steht auf dem Fussboden, Standflaeche 0) || UEBERHOLT (U3, D118): [E] R37 Befund 10 / Auftrag W34: Wassertiefe 800 mm (0,4 m3 = Ø 0,8 x 0,8 m); der Bestand pool3_depth 1130 war die Tiefe einschliesslich des 120-mm-Bodens bis zum Wasserspiegel |
| `ring` | 60 | mm | [E] Auftrag W34 / R37 Befund 10: Ring 60 mm (wie Zweitbecken und Drittbecken im Bestand) |
| `boden` | 120 | mm | [E] Bestand gen_dome.py pool_fn: Hohlraum beginnt 120 mm ueber der Unterkante |
| `wasser_spiel` | 10 | mm | [E] Bestand gen_dome.py pool_fn: Wasserkoerper Ø d - 10 (5 mm Luft zur Wand, keine Beruehrung) |
| `ue_dn` | 63 | mm | [A] D106: Ueberlaeufe der Becken d63 (Leitungsbibliothek lt_*, EN 1452); Weg e63 Lebendfutter -> Anzucht |
| `ue_id` | 57 | mm | [E] PVC-U 63 x 3,0 PN10: Innendurchmesser 57; Rohr-Innenunterkante = Wasserspiegel (D120) |
| `fussboden_z` | 0 | mm | [E] lokaler Rahmen: Z 0 = Unterkante; das Becken steht auf dem Fussboden, Einbau bei Z 400 (D94, D118) |
| `rand_ueber_wasser` | 150 | mm | [Q] data/oasis-soll.json feed rand 1000 minus wsp 850 = 150 (= data/params.json pool3_rim minus pool3_wsp) || UEBERHOLT (U3, D118): [E] data/params.json pool_rim 650 minus data/layout.json pool2.water_z 515 (Rand Z 650, Wasserspiegel Z 515, wie Pool und Zweitbecken) |
| `pool3_d_neu` | 1000 | mm | [R] Wert fuer data/params.json pool3_d, Soll-Wert steht dort als varianten_werte ring_b2 (D119) || UEBERHOLT (U3, D118): [R] Wert fuer data/params.json pool3_d (Montage setzt ihn; vorher 1030) |
| `pool3_depth_neu` | 850 | mm | [R] Wert fuer data/params.json pool3_depth = Wasserspiegel 850 minus Standflaeche 0 (varianten_werte ring_b2, D118) || UEBERHOLT (U3, D118): [R] Wert fuer data/params.json pool3_depth (Tiefe bis Wasserspiegel einschliesslich Boden 120: 800 + 120; vorher 1130) |
| `stutzen_h` | 60 | mm | [A] W37-2 Teil 3: Hoehe der Anschlussbloecke auf der Rand-Oberkante (Z 1055 bis 1115); Stutzenachse 30 mm darueber |
| `stutzen_blk_r` | 60 | mm | [E] Blockbreite radial = Ringbreite 60 (liegt auf der ebenen Rand-Oberkante) |
| `stutzen_blk_t` | 90 | mm | [A] Blockbreite tangential |
| `stutzen_len` | 70 | mm | [A] Stutzenrohr ausserhalb des Rings (Muffentiefe d25 = 19, d20 = 16) |
| `winkel_k41` | 0 | deg | [A] Azimut Stutzen K41 (Frischwasser d20); Vielfache von 90 Grad, endgueltige Lage Montage (Biofilter-Seite offen) |
| `winkel_k42` | 90 | deg | [A] Azimut Stutzen K42 (Entnahme zum Biofilter d25) |
| `winkel_k43` | 180 | deg | [A] Azimut Stutzen K43 (Rueckfluss vom Biofilter d25) |
| `winkel_k49` | 270 | deg | [A] Azimut Stutzen K49 (Luftschlauch ID16/AD20, Notstrom) |

Gesamt-Box (Messung): X -630.0 bis 630.0, Y -630.0 bis 630.0, Z 0.0 bis 1060.0 mm; Koerper: 7.

**Toleranzen / Spiel:** Rand 150 mm ueber dem Wasserspiegel; 5 mm Luft zwischen Wasserkoerper und Wand; Rohr-Innenunterkante der Ueberlauf-Tuelle = Wasserspiegel.

## Werkstoff und Gewicht

- Werkstoff: Beton (Platzhalter fuer die Ringwand), Dichte 2.4 g/cm3, Farbe #9a9a96 ([A] Wandwerkstoff nicht entschieden (Bestand ohne Material, Standarddichte); Beton als Platzhalter fuer eingelassene Becken)
- Volumen (Messung, `solidcraft-cli eval`): 295419.1 cm3 · Masse leer (ohne Wasser): 707392 g (707.39 kg)
- Gefuellt/in Betrieb: Wasser 573 l ca. 573 kg [E, Dichte 1]

## Querschnitt / Profil

Zylinderwanne: Aussen Ø 1120, Hohlraum Ø 1000 ab 120 mm ueber der Unterkante, Gesamthoehe 1000 mm (Boden 120 + Wassertiefe 730 + Rand 150). Wasserkoerper Ø 990 x 730.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| K41 Frischwasser-Zulauf (aus der Aktivkohle-Station) | PVC-U d20 (DN15), Klebemuffe aussen, Einstecktiefe 16 | x 630, y 0, z 1030 (Mitte der Oeffnung) | Oeffnung zeigt +X (Azimut 0 Grad, Parameter winkel_k41); Wasserwechsel 2 l/min |
| K42 Entnahme zum Biofilter | PVC-U d25 (DN20), Klebemuffe aussen, Einstecktiefe 19 | x 0, y 630, z 1030 | Oeffnung zeigt +Y (Azimut 90 Grad, winkel_k42); Umlauf 5 l/min |
| K43 Rueckfluss vom Biofilter | PVC-U d25 (DN20), Klebemuffe aussen, Einstecktiefe 19 | x -630, y 0, z 1030 | Oeffnung zeigt -X (Azimut 180 Grad, winkel_k43); 5 l/min |
| K49 Luftschlauch (Belueftung, Notstrom) | Schlauchtuelle Aussen-Ø 20, Bohrung Ø 16 (Schlauch ID16/AD20) | x 0, y -630, z 1030 | Oeffnung zeigt -Y (Azimut 270 Grad, winkel_k49); Luft 2 l/min, Geblaese in W37-3 |
| Ueberlauf zum Anzuchtbecken (Weg e63) | PVC-U d63 (DN50), Klebemuffe aussen, Einstecktiefe 37,5; Rohr-Innenunterkante = Wasserspiegel 850 | Aussenende Radius 630, Achse Z 878,5, Azimut 12,5 Grad zum Anzuchtbecken (Bauplatz data/oasis-lage.json) | freier Auslauf ins Anzuchtbecken (Wasserspiegel 800, 50 mm tiefer); Einbau ohne Drehung |

## Verbindungen und Befestigungen

- Wanne wie W34, ein Wandloch nur fuer die Ueberlauf-Tuelle (U3). Neu W37-2 Teil 3: vier Anschluss-Stutzen K41, K42, K43, K49 als eigene Koerper (Block 60 x 90 x 60 auf der ebenen Rand-Oberkante, radiales Stutzenrohr 70 mm nach aussen)
- Die Stutzen sind Anschlusspunkte aussen am Rand; der Wasserweg ueber die Kante ins Becken (Tauchrohr/Saugkorb fuer K42, Einlauf K41/K43) ist Montage und nicht modelliert
- Ueberlauf/Ablauf des Wechselwassers: Montage, nicht Teil
- Neu U3: Ueberlauf-Tuelle d63 als eigener Koerper T14k_Ueberlauf (Stutzen mit Bohrung ID 57 und Muffe d63) in einem Wandloch auf Wasserspiegelhoehe

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Lebendfutterbecken 0,57 m3: Wasser Ø 1000 x 730 tief | 573 l Nennvolumen | Q | data/oasis-soll.json feed (Ø 1000, Wsp 850, Rand 1000, steht auf dem Boden); Boden 120 wie Bestand | hoch |
| Ring 60 mm, Aussendurchmesser 1120 | Ø 1120 | E | Bestand pool_fn (wall 60) | mittel |
| Grundflaeche mit Ring 0,99 m2 | 0,99 m2 | R | pi x 0,56^2 = 0,985 m2 | hoch |
| Rand 150 mm ueber dem Wasserspiegel | 150 | Q | data/oasis-soll.json feed: Rand 1000 minus Wsp 850 | hoch |
| Ueberlauf-Tuelle d63 auf Wasserspiegelhoehe | d63, Achse 878,5 | A | D120, D106; Quelle Weg e63 Ueberlauf Lebendfutter -> Anzucht (50 mm tiefer, A13) | mittel |
| Ringwand Beton | 2,4 g/cm3 | A | Wandwerkstoff offen; Bestand ohne Material | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: data/oasis-soll.json feed (A13, A26: Ø 1 m, steht auf dem Boden, Wsp 850, Rand 1000); Bestand: scripts/gen_dome.py pool_fn (Boden 120, Wand 60, Wasserkoerper Ø d-10); Bauplatz data/oasis-lage.json feed (U1, D110)
- Abweichung zum OBJ: Bestand (A+): Innen Ø 800, Wassertiefe 800, in den Boden eingelassen (Wasserspiegel +515, Rand +650). Neu (D118): Innen Ø 1000, Standflaeche auf dem Fussboden, Wasserspiegel 850, Rand 1000, Wassertiefe 730, 573 l Nennvolumen. Die Stutzen K41/K42/K43/K49 bleiben, neu ist die Ueberlauf-Tuelle d63. Der Bestand `designs/components/becken_dritt.sc` bleibt unveraendert.

## Montage (L4)

1. Aufstellen auf dem Fussboden (Modell-Z 400), keine Grube; Wasserspiegel auf Z 1250 (850 ueber dem Fussboden) einstellen
2. Ueberlauf-Tuelle d63 zeigt zum Anzuchtbecken, freier Auslauf

**Werkzeug:** Wasserwaage

## Stueckliste-Zeile

- T14k Lebendfutterbecken: 1 Wanne Ø 1120 x 1000 (Ringwand 60, Boden 120)
- 1 Ueberlauf-Tuelle d63 (Wanddurchfuehrung mit Muffe)
- 4 Anschluss-Stutzen (K41 d20, K42 d25, K43 d25 Klebemuffen; K49 Schlauchtuelle ID16) auf dem Rand

## Alternative lokale Fertigung

Fertigbecken PE Ø 1120 mit Standfuss oder Betonring DN 1000 mit Bodenplatte; Rand 150 mm ueber dem Wasserspiegel; Tankdurchfuehrung d63 fuer den Ueberlauf.

## Renders

- `renders/components/becken_dritt_klein/becken_dritt_klein-01-schraeg.png`
- `renders/components/becken_dritt_klein/becken_dritt_klein-02-schnitt.png`
- `renders/components/becken_dritt_klein/becken_dritt_klein-03-stutzen.png`

## Pruefung

- Gauntlet-Urteil: Pruefer-Lauf: PASS, Befund in docs/jobs/pruefung/W37-2-W37-3.md.
- scripts/workshop/check_becken_dritt_klein.py (Ergebnis renders/components/becken_dritt_klein/check.txt): Durchmesser, Ring, Hoehe, Wassertiefe, Nennvolumen 0,57 m3, Rand, Wannenvolumen, 4 Stutzen, Ueberlauf-Tuelle d63, Interferenz 0; Soll aus data/oasis-soll.json (feed)

## Offene Fragen

- Montage U4: Bauplatz aus data/oasis-lage.json (feed, ANNAHME D110), Einbau ohne Drehung auf dem Fussboden; Parameter pool3_d und pool3_depth aus data/params.json (varianten_werte ring_b2)
- Wandwerkstoff (Beton oder PE) offen; Biofilter 37 l und Belueftung nicht modelliert (Leitungsnetz K35-K41: Montage)
- Stutzen: Azimut je Stutzen (winkel_*) vorlaeufig 0/90/180/270 Grad, Biofilter-Seite legt die Montage fest; Wasserweg ueber die Kante, Tauchrohr fuer K42 und Ueberlauf des Wechselwassers: Montage
- Wasserwechsel 2 l/min aus der Frischwasserleitung bzw. Zisterne (R37 Befund 9), Frischwasserquelle klaert Ben beim Versorger
