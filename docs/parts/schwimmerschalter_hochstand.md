# Bauteilblatt T105 schwimmerschalter_hochstand (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/schwimmerschalter_hochstand.json` und `designs/components/schwimmerschalter_hochstand.sc`, nicht von Hand aendern)

**Funktion:** Meldet dem Schaltschrank den Hochstand im Sumpftank (-110 mm). Steigt der Pegel zu hoch (zum Beispiel weil die Pumpe am Sumpf ausfaellt), schaltet die Steuerung die Pumpe Fischtank zu Filter der eigenen Linie ab, damit der Sumpf nicht ueberlaeuft (A20, A31). Schutz gegen Ueberlauf, Designprinzip 9. Die Pumpe am Sumpf bekommt den mechanischen Trockenlaufschutz ueber ein Schwimmerventil (Quelle sump_1.t1, gehoert zu Pumpe und Sumpf, nicht zu diesem Teil).

**Datei:** `designs/components/schwimmerschalter_hochstand.sc` · **Teilenummer:** T105 · **Revision:** A · **Bezugspunkt:** Mitte des Schwimmers im Ursprung = Schaltpunkt (Sumpf: Fussboden-Z -110); Kabel und Klemme nach oben (+Z); Einbau: Klemme in der Aufnahme des sumpftank (Z -75 bis -45 im Sumpf)

**Anzahl (Instanzen):** 2 (Schwimmerschalter 1 und 2, je Sumpftank einer) (Quelle: data/oasis-soll.json schwimmer_1, schwimmer_2)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `schwimmer_d` | 70 | mm | [A] Schwimmer Ø 70 (handelsueblicher Kabel-Schwimmerschalter fuer Pumpen, Maß je Fabrikat offen) |
| `klemme_s` | 30 | mm | [A] Kabelklemme 30 x 30 x 30 (PA) |
| `kabel_d` | 7 | mm | [A] Kabel Ø 7 (Steuerleitung, PVC-Mantel) |
| `kabel_l` | 400 | mm | [A] Kabelstueck im Modell (Ausschnitt); die Meldeleitung zur Steuerung wird laenger, Laenge nach Einbauort (U5/U6) |
| `schaltpunkt` | -110 | mm | [Q] data/oasis-soll.json sump_1 hochstand_ueber_fussboden_mm; Mitte des Schwimmers im Ursprung = Schaltpunkt (Fussboden-Bezug) |
| `wiederein` | -180 | mm | [A] D105: Wiedereinschalten bei -180 mm (Schaltdifferenz 70 mm), im Modell zaehlt der Hochstand; Schaltdifferenz des Fabrikats offen |

Gesamt-Box (Messung): X -35.0 bis 35.0, Y -35.0 bis 35.0, Z -35.0 bis 435.0 mm; Koerper: 3.

**Toleranzen / Spiel:** Schwimmer und Kabel beruehren sich nur im Pol (keine Durchdringung); Kabel sitzt passgenau in der Klemmenbohrung.

## Werkstoff und Gewicht

- Werkstoff: PP (Schwimmer), PA (Klemme), PVC (Kabelmantel), Dichte 0.91 g/cm3, Farbe #e07a2f ([A] Kabel-Schwimmerschalter, Werkstoff je Hersteller; Wasserkontakt: Schwimmer und Kabel (D85: Nachweis offen))
- Volumen (Messung, `solidcraft-cli eval`): 220.8 cm3 · Masse leer: 211 g (0.21 kg)

## Querschnitt / Profil

Schwimmer Kugel Ø 70 mit Mitte im Ursprung; Kabelklemme 30 x 30 x 30 von Z 35 bis 65 mit Bohrung Ø 7; Kabel Ø 7 von Z 35 bis 435 durch die Klemme.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Meldeleitung | Kabel Ø 7, Ausschnitt 400 | x 0, y 0, z 435 | Kabelende nach oben, weiter zur Steuerung (Schaltschrank) |

## Verbindungen und Befestigungen

- Kabelklemme in der Aufnahme des sumpftank (Schwimmerhalter an der +X-Wand)
- Kabel ueber die Deckelfuge zum Schaltschrank, Steuerung schaltet die Pumpe Fischtank zu Filter ab

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Schaltpunkt -110 mm | Schwimmermitte = Ursprung | Q | data/oasis-soll.json sump_1/schwimmer_1, A20 | hoch |
| Wiedereinschalten -180 mm | 70 mm Schaltdifferenz | A | D105; Quelle laesst es offen (A20) | niedrig |
| Schwimmer Ø 70, Klemme 30, Kabel Ø 7 | Platzhalter | A | handelsueblicher Pumpen-Schwimmerschalter; Maße nicht aus einem Datenblatt gelesen | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (schwimmer_1: Hochstand-Schwimmerschalter, Meldeleitung zur Steuerung, Schaltpunkt offen A20; sump_1 hochstand_ueber_fussboden_mm -110); docs/decisions.md D105 (Wiedereinschalten bei -180 mm Annahme); docs/research/R61-oasis-wasserkreislauf.md Abschnitt 4 (O4)
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).

## Montage (L4)

1. Klemme in der Halteraufnahme befestigen, Schwimmer in die Hochstand-Lage bringen (Mitte bei -110 mm)
2. Kabel zur Steuerung fuehren
3. Probe: Wasser auf -110 anheben, Steuerung muss die Pumpe abschalten

**Werkzeug:** Schraubendreher, Wasserwaage, Maßband

## Renders

- `renders/components/schwimmerschalter_hochstand/schwimmerschalter_hochstand-01-schraeg.png`

## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_schwimmerschalter_hochstand.py

## Offene Fragen

- Fabrikat und Schaltdifferenz (Wiedereinschaltpunkt -180 mm ist Annahme D105); Bezug Europa je Haendler siehe data/beschaffung/
- Lebensmitteleignung von Schwimmer und Kabel (D85) ohne Herstellernachweis; Rueckfall: Schwimmerschalter mit Edelstahl-Schwimmer oder berührungsloser Fuellstandsschalter
- Die Steuerung (Verdrahtung, Abschalten der Pumpe) gehoert zu U6 und zum Schaltschrank, nicht zu diesem Teil
- Bezug Europa und Lebensmittel (D76, D85), Stand 10.11.2026 aus data/beschaffung/u2_wasserkreislauf.json: ARM-schwimmerschalter-hochstand: Finder (Hersteller-Datenblatt Serie 72) (unbekannt), Konfidenz Q-Treffer; Lebensmittel: offen (kein selbst gelesener Herstellernachweis), Rueckfall: Findernet 72; Rueckfall: Eaton SW Schwimmerschalter (Conrad-Datenblatt, Trinkwasser 'ja', IP65) [Q-Treffer, https://asset.conrad.com/media10/add/160267/c1/-/de/00213
