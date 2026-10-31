# Bauteilblatt T14k becken_dritt_klein (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/becken_dritt_klein.json` und `designs/components/becken_dritt_klein.sc`, nicht von Hand aendern)

**Funktion:** Drittbecken als Quarantaene- und Notbecken fuer Zuchttiere oder Kranke (R37 Befund 10): 0,4 m3 Wasser, eingelassen in den Boden wie Pool und Zweitbecken. Der Pool (346 kg Fisch) laesst sich in keinem Becken auffangen. Eigener Biofilter (37 l Bioballs) und Belueftung sind noetig und liegen ausserhalb dieses Bauteils.

**Datei:** `designs/components/becken_dritt_klein.sc` · **Teilenummer:** T14k · **Revision:** A · **Bezugspunkt:** Mitte der Beckenunterkante (Z 0 = Unterkante Boden); Z hoch; Einbau: Z 0 liegt bei Wasserspiegel Z 515 minus 920 = Z -405 im Modellrahmen

**Anzahl (Instanzen):** 1 Drittbecken (Quelle: D46/D49 (Lage Zwickel Tuer/Station, Platzierung Montage); D66: klein)

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

Gesamt-Box (Messung): X -460.0 bis 460.0, Y -460.0 bis 460.0, Z 0.0 bis 1055.0 mm; Koerper: 2.

**Toleranzen / Spiel:** Rand 135 mm ueber dem Wasserspiegel; 5 mm Luft zwischen Wasserkoerper und Wand.

## Werkstoff und Gewicht

- Werkstoff: Beton (Platzhalter fuer die Ringwand), Dichte 2.4 g/cm3, Farbe #9a9a96 ([A] Wandwerkstoff nicht entschieden (Bestand ohne Material, Standarddichte); Beton als Platzhalter fuer eingelassene Becken)
- Volumen (Messung, `solidcraft-cli eval`): 231314.5 cm3 · Masse leer (ohne Wasser): 555155 g (555.15 kg)
- Gefuellt/in Betrieb: Wasser 392 l ca. 392 kg [E, Dichte 1]

## Querschnitt / Profil

Zylinderwanne: Aussen Ø 920, Hohlraum Ø 800 ab 120 mm ueber der Unterkante, Gesamthoehe 1055 mm (Boden 120 + Wassertiefe 800 + Rand 135). Wasserkoerper Ø 790 x 800.

## Verbindungen und Befestigungen

- Anschluesse und Stutzen sind im Bestand nicht modelliert (gen_dome.py pool_fn erzeugt nur Wanne und Wasser); Zu- und Ablaufstutzen liefert das Leitungsnetz (Montage). Stutzen wie bisher: keine.

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

## Alternative lokale Fertigung

Fertigbecken PE Ø 920 oder Betonring DN 800 mit Bodenplatte; Rand 135 mm ueber dem Wasserspiegel.

## Renders


## Pruefung

- Gauntlet-Urteil: Kein Pruefer-Lauf (Auftrag W34: Selbstcheck).
- scripts/workshop/check_becken_dritt_klein.py (Ergebnis renders/components/becken_dritt_klein/check.txt): Durchmesser, Ring, Tiefe, Volumen 0,4 m3, Grundflaeche 0,66 m2, Rand, Interferenz 0

## Offene Fragen

- Montage: data/params.json pool3_d 800 und pool3_depth 920 setzen (oder die neue Komponente verknuepfen); Lage D49 (Zwickel Tuer/Station) mit dem kleineren Becken neu pruefen (place_m8.py, Laufwegkarte)
- Wandwerkstoff (Beton oder PE) offen; Stutzen, Biofilter 37 l und Belueftung nicht modelliert (Leitungsnetz K35-K41: Montage)
- Wasserwechsel 2 l/min aus der Frischwasserleitung bzw. Zisterne (R37 Befund 9), Frischwasserquelle klaert Ben beim Versorger
