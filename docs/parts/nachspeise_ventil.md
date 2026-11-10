# Bauteilblatt T108 nachspeise_ventil (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/nachspeise_ventil.json` und `designs/components/nachspeise_ventil.sc`, nicht von Hand aendern)

**Funktion:** Haelt den Wasserspiegel im Fischtank bei 750 mm: sinkt er (Verdunstung, Wasserwechsel), oeffnet zuerst das Regenwasser-Ventil (Eingang A, Regenwassertank 5 m3, erste Wahl, salz- und chlorfrei); laeuft kein Regenwasser nach, sinkt der Spiegel um weitere 30 mm und das Frischwasser-Ventil (Eingang B, ueber die Aktivkohle-Station entchlort) oeffnet. Steigt der Spiegel, schliessen beide: Schutz vor Ueberfuellen. Mechanisch, ohne Strom (Designprinzip 1). Auslauf frei ueber dem Rand: kein Rueckfluss in die Leitungen.

**Datei:** `designs/components/nachspeise_ventil.sc` · **Teilenummer:** T108 · **Revision:** A · **Bezugspunkt:** Port A Regenwasser (Mitte Muffenoeffnung) im Ursprung, Port B Frischwasser bei y 120; Rohrachse +X (Zulauf aus -X), Z hoch, Hebelarme nach unten; Einbau: Rohrachse Modell-Z 1660 (Spiegel 1150 + 510)

**Anzahl (Instanzen):** 1 (Nachspeise-Ventil am Fischtank) (Quelle: data/oasis-soll.json nachspeise (anzahl 1))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `pipe_d` | 25 | mm | [E] Netz K40: Zulauf d25 |
| `uebergang_l` | 40 | mm | [A] Klebemuffe d25 (Tiefe 19) plus Gewindeteil 3/4 Zoll; Platzhalter |
| `ventil_d` | 38 | mm | [A] Ventilgehaeuse 3/4 Zoll Kunststoff (R+M Suttner 701403, R53; Maß nicht aus dem Datenblatt gelesen) |
| `ventil_l` | 80 | mm | [A] Ventilgehaeuse Laenge (Platzhalter) |
| `hebel_x` | 100 | mm | [A] Lage des Drehpunkts hinter dem Uebergang |
| `wange_t` | 4 | mm | [A] Wange der Hebelaufnahme (zwei Wangen links und rechts des Arms) |
| `arm_d` | 8 | mm | [A] Hebelarm Ø 8 |
| `arm_dx` | 260 | mm | [A] Horizontaler Abstand Drehpunkt bis Kugelmitte |
| `kugel_d` | 110 | mm | [A] Schwimmerkugel Ø 110 (PE, Handelsmass offen) |
| `kugel_auf` | 20 | mm | [A] Kugelmitte liegt 20 mm ueber dem Wasserspiegel (Kugel schwimmt zu ca. 60 Prozent eingetaucht, Ventil geschlossen) |
| `ventil_h` | 510 | mm | [E] Rohrachse ueber dem Spiegel des Fischtanks: Rand 1200 minus Wsp 750 = 450 (data/oasis-soll.json fish) plus 60 mm ueber dem Rand (freier Auslauf wie T84); Lage Modell-Z 1150 + 510 |
| `spiegel` | 750 | mm | [Q] data/oasis-soll.json fish wsp_ueber_fussboden_mm 750 (Fussboden-Bezug; Modell-Z 1150) |
| `staffel` | 30 | mm | [A] Staffelung: das Frischwasser-Ventil schliesst 30 mm tiefer als das Regenwasser-Ventil; so oeffnet Frischwasser erst, wenn Regenwasser nicht mehr nachlaeuft (D114) |
| `abstand_y` | 120 | mm | [A] Abstand der beiden Ventilachsen (Regenwasser y 0, Frischwasser y 120): groesser als die Kugel Ø 110 |

Gesamt-Box (Messung): X -0.0 bis 415.0, Y -55.0 bis 175.0, Z -575.0 bis 19.0 mm; Koerper: 10.

**Toleranzen / Spiel:** Hebelarm und Kugel je ein Koerper; Maße Platzhalter wie T84; Schliessdruck mit Drossel offen.

## Werkstoff und Gewicht

- Werkstoff: Kunststoff PP (Gehaeuse, Hebelarm, Kugel), PVC-U (Uebergang), Dichte 0.91 g/cm3, Farbe #e8e5d8 ([A] Handelsteil, Werkstoff nach Katalog offen)
- Volumen (Messung, `solidcraft-cli eval`): 1667.7 cm3 · Masse leer: 728 g (0.73 kg)

## Querschnitt / Profil

Je Ventil: Klebemuffe d25 (Aussen 32,25, Tiefe 19) mit Gewindeteil 40 lang, Ventilgehaeuse Ø 38 x 80, zwei Wangen, Hebelarm Ø 8 mit Schwimmerkugel Ø 110 (PP); Achsabstand 120; Frischwasser-Kugel 30 mm tiefer als die Regenwasser-Kugel.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| A Regenwasser (Muffe) | PVC-U d25, Klebemuffe, Tiefe 19 | x 0, y 0, z 0 | Oeffnung zeigt -X; Rohr d25 vom Regenwassertank |
| B Frischwasser (Muffe) | PVC-U d25, Klebemuffe, Tiefe 19 | x 0, y 120, z 0 | Oeffnung zeigt -X; Rohr d25 von der Aktivkohle-Station |

## Verbindungen und Befestigungen

- Beide Rohre d25 in die Klebemuffen
- Befestigung am Rand des Fischtanks: Halter nicht modelliert (Montage)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Ventil 3/4 Zoll, Handelsteil | zwei Gehaeuse Ø 38 x 80 | A | T84 (R53: R+M Suttner 701403); Maße aus dem Blatt T84, nicht aus einem Datenblatt | niedrig |
| Regenwasser zuerst | Frischwasser-Kugel 30 mm tiefer | A | D114: mechanische Staffelung statt zweitem Mechanismus; Quelle A8 nennt nur die Reihenfolge | mittel |
| Rohrachse 510 ueber dem Spiegel | Rand 450 + 60 | E | data/oasis-soll.json fish: Rand 1200, Wsp 750; freier Auslauf 60 mm ueber dem Rand (EN 1717 sinngemaess) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (nachspeise: mechanisches Schwimmerventil am Fischtank, Regenwasser zuerst, Frischwasser nachrangig; fish: Rand 1200, Wsp 750); docs/decisions.md D107; data/components/schwimmerventil_pool.json (T84, Maße und Herkunft des Ventils); docs/research/R53-europa-frischwasser-luft.md
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ersetzt T84 am Fischtank).

## Montage (L4)

1. Ventile so ans Rohrende kleben, dass die Rohrachse 510 ueber dem Spiegel liegt (Modell-Z 1660)
2. Hebelarme einstellen: Regenwasser schliesst bei Spiegel 750, Frischwasser bei Spiegel 720
3. Regenwassertank an A, Aktivkohle-Station an B; Begrenzer 4 l/min vor dem Frischwasser-Ventil pruefen

**Werkzeug:** Saege, PVC-Kleber nach DIN EN 14814, Wasserwaage

## Renders

- `renders/components/nachspeise_ventil/nachspeise_ventil-01-schraeg.png`
- `renders/components/nachspeise_ventil/nachspeise_ventil-02-seite.png`

## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_nachspeise_ventil.py

## Offene Fragen

- Zwei Ventile mit gestaffelter Kugelhoehe sind eine Annahme (D114); die Quelle nennt ein Ventil mit Regenwasser zuerst. Rueckfall: ein Mehrwege-Schwimmerventil oder die Frischwasser-Nachspeisung im Regentank
- Handelsteil, Fabrikat und Schliessdruck mit Drossel offen (wie T84); Bezug Europa und Lebensmittelnachweis (D85) siehe data/beschaffung/
- Der Bestand T84 (schwimmerventil_pool) wird in U3/U5 durch dieses Teil ersetzt; T84 bleibt bis dahin unberuehrt
- Bezug Europa und Lebensmittel (D76, D85), Stand 10.11.2026 aus data/beschaffung/u2_wasserkreislauf.json: ARM-schwimmerventil-nachspeise: R+M Suttner (Online-Shop) (DE), Konfidenz Q; Lebensmittel: offen fuer 701403 (kein Herstellernachweis gefunden), Rueckfall: 701408 mit Trinkwasser-Hinweis (Flyer https://shop; Rueckfall: R+M Suttner 701408 (3/4 Zoll AG mit Kugel, Trinkwasser-Flyer) [Q-Treffer, https://shop.rm-suttner.com/en/low-pressure-equipment/valves/float
