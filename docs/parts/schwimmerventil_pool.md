# Bauteilblatt T84 schwimmerventil_pool (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/schwimmerventil_pool.json` und `designs/components/schwimmerventil_pool.sc`, nicht von Hand aendern)

**Funktion:** Haelt den Wasserspiegel im Pool auf Z 515: sinkt der Spiegel (Verdunstung, Wasserwechsel), kippt die Schwimmerkugel nach unten, das Ventil oeffnet und das entchlorte Frischwasser aus der Aktivkohle-Station (K40, Spitze 10 l/min, Mittel 0,47 l/min) laeuft nach; steigt der Spiegel, schliesst es. Handelsteil, keine Eigenkonstruktion. Zulauf OFFEN (E20): In Variante B speist der Ring (d90, Z 2100/2245) auch das Becken-Frischwasser (R47 Definition B); ob K40 dann aus dem Ring statt aus der Filterstation kommt, ist OFFEN (E20). Das Bauteil selbst gilt in jeder Variante, die Aktivkohle-Station bleibt davor.

**Datei:** `designs/components/schwimmerventil_pool.sc` · **Teilenummer:** T84 · **Revision:** A · **Bezugspunkt:** Port A (Mitte der Muffenoeffnung) im Ursprung; Rohrachse +X (Zulauf kommt aus -X), Z hoch, Hebelarm zeigt nach unten zum Wasser; Einbau: Rohrachse bei Z 710 im Modellrahmen (Spiegel 515 + 195)

**Anzahl (Instanzen):** 1 Schwimmerventil am Pool (Zweitbecken: eigenes, Montage) (Quelle: Netz Version 3: K40 nach pool; R45 Abschnitt 5)

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
| `ventil_h` | 195 | mm | [E] Rohrachse ueber dem Wasserspiegel: Rand Z 650 minus Spiegel Z 515 = 135, plus 60 Montagehoehe ueber dem Rand [A] |
| `kugel_auf` | 20 | mm | [A] Kugelmitte liegt 20 mm ueber dem Wasserspiegel (Kugel schwimmt zu ca. 60 Prozent eingetaucht, Ventil geschlossen) |
| `water_z` | 515 | mm | [E] data/layout.json pool2.water_z (nur gelesen); Einbau: Rohrachse bei Z 515 + ventil_h = 710 |

Gesamt-Box (Messung): X -0.0 bis 415.0, Y -55.0 bis 55.0, Z -230.0 bis 19.0 mm; Koerper: 5.

**Toleranzen / Spiel:** Hebelarm und Kugel sind ein Koerper (Arm 5 mm in die Kugel gesteckt); Maße Platzhalter.

## Werkstoff und Gewicht

- Werkstoff: Kunststoff PP (Gehaeuse, Hebelarm, Kugel), PVC-U (Uebergang), Dichte 0.91 g/cm3, Farbe #e8e5d8 ([A] Handelsteil, Werkstoff nach Katalog offen)
- Volumen (Messung, `solidcraft-cli eval`): 821.6 cm3 · Masse leer: 360 g (0.36 kg)
- Gefuellt/in Betrieb: Kugel zu 60 Prozent eingetaucht schwimmt auf; Masse leer siehe Messung

## Querschnitt / Profil

Klebemuffe d25 (Aussen 32,25, Tiefe 19) mit Gewindeteil, Ventilgehaeuse Ø 38 x 80 liegend, Hebelarm Ø 8 mit Wangenhalter, Schwimmerkugel Ø 110; Hebelarm 260 mm horizontal, Kugelmitte 175 mm unter der Rohrachse.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| A Zulauf K40 (Muffe) | PVC-U d25 (DN20), Klebemuffe, Einstecktiefe 19 | x 0, y 0, z 0 (Mitte der Oeffnung) | Oeffnung zeigt -X; das Rohr d25 von der Aktivkohle-Station wird eingesteckt. Zulauf OFFEN (E20) |

## Verbindungen und Befestigungen

- Port A: Rohr d25 in die Klebemuffe
- Befestigung des Ventils am Beckenrand: Halter nicht modelliert (Montage)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Schwimmerventil 3/4 Zoll, Spitze 10 l/min | Ventilgehaeuse Ø 38 x 80 | A | R53 Abschnitt Europa-Teileliste: R+M Suttner Art. 701403 (Kunststoff, max. 22 l/min, Q), Pegler Yorkshire 3/4 Messing; Katalog offen, N-BESCHAFFUNG | niedrig |
| Rohrachse ueber dem Wasserspiegel | 195 mm | E | data/params.json pool_rim 650 minus layout pool2.water_z 515 = 135, plus 60 [A] | mittel |
| Schwimmerkugel auf Spiegel | Mitte 20 mm ueber Z 515 | A | Schwimmerventil-Praxis; Kugel Ø 110 | niedrig |
| Schliessdruck mit Drossel | offen | offen | R45 offener Punkt 4: Verhalten des Durchflussbegrenzers (4 l/min) mit Schwimmerventil, Fabrikat offen | - |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R45-hydraulik-auslegung.md Abschnitt 5 (Spitze 10 l/min, offener Punkt 4: Schliessdruck); docs/research/R53-europa-frischwasser-luft.md (Schwimmerventil 3/4: R+M Suttner 701403, Pegler Yorkshire; Q); data/layout.json pool2.water_z 515 (nur gelesen), data/params.json pool_rim 650
- Abweichung zum OBJ: Kein OBJ-Bestand.

## Montage (L4)

1. Ventil so ans Rohrende kleben, dass die Rohrachse 195 mm ueber dem Spiegel liegt (Z 710)
2. Hebelarm einstellen: Ventil schliesst bei Kugelmitte Z 535, Wasserspiegel Z 515
3. Aktivkohle-Station liegt vor dem Ventil; Begrenzer 4 l/min vor dem Ventil pruefen (Schliessdruck offen)

**Werkzeug:** Rohrschneider, Klebstoff PVC

## Stueckliste-Zeile

- 1 Schwimmerventil 3/4 Zoll mit Hebelarm und Kugel (z. B. Kunststoff)
- 1 Uebergang Klebemuffe d25 auf 3/4 Zoll Aussengewinde

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| Schwimmerventil 3/4 Zoll | Spitze 10 l/min, max. 22 l/min | R+M Suttner Art. 701403, Kunststoff (DE) [Q]; Pegler Yorkshire 3/4 Messing, RS Art. 0197867 (UK-Marke) [Q-Treffer] | beschaffbar (zwei Quellen); Schliessdruck mit Drossel offen; Zulauf OFFEN (E20) |
| Uebergang Klebemuffe d25 auf 3/4 Zoll | PVC-U | Katalog offen, N-BESCHAFFUNG (W47) | offen |

## Alternative lokale Fertigung

Handelsteil (Sanitaer/Garten, Schwimmerventil 3/4 Zoll, max. 22 l/min).

## Renders

- `renders/components/schwimmerventil_pool/schwimmerventil_pool-01-schraeg.png`
- `renders/components/schwimmerventil_pool/schwimmerventil_pool-02-seite.png`

## Pruefung

- Gauntlet-Urteil: Kein Pruefer-Lauf (Auftrag W37-2: Selbstcheck; Pruefer folgt).
- scripts/workshop/check_schwimmerventil_pool.py (Ergebnis renders/components/schwimmerventil_pool/check.txt): Masse, Port, Kugelmitte auf Spiegelhoehe, Interferenz 0

## Offene Fragen

- Zulauf OFFEN (E20): Variante B kann K40 aus dem Ring speisen (R47 Definition B); entschieden wird am 05.11.2026
- Fabrikat und Schliessdruck mit Drossel (R45 offener Punkt 4): Katalog offen, N-BESCHAFFUNG
- Befestigung am Beckenrand und Hoehe ueber dem Rand: Montage
- Schwimmerventil am Zweitbecken: eigenes Bauteil Montage (nicht Teil dieses Auftrags)
