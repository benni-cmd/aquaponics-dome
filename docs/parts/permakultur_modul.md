# Bauteilblatt T111 permakultur_modul (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/permakultur_modul.json` und `designs/components/permakultur_modul.sc`, nicht von Hand aendern)

**Funktion:** Nimmt den Schlamm aus den Sammelbehaeltern von Hand auf (Kompost, Wuermer, Futterzucht); keine Rueckleitung ins Wasser, getrennt vom Lebendfutterbecken (Quelle). Einfacher Platzhalter fuer die Schlamm-Senke ausserhalb der Kuppel; die Permakultur um den Dom ist nicht modelliert.

**Datei:** `designs/components/permakultur_modul.sc` · **Teilenummer:** T111 · **Revision:** A · **Bezugspunkt:** Mitte der Kompostbox in X und Y, Z 0 = Fussboden; Futterzuchtkiste bei +X neben der Kompostbox

**Anzahl (Instanzen):** 1 (Permakultur-Modul) (Quelle: data/oasis-soll.json permakultur (anzahl 1))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `kompost_l` | 1500 | mm | [Q] Zeichnung permakultur: Rechteck 1500 mm breit |
| `kompost_b` | 525 | mm | [Q] Zeichnung permakultur: Rechteck 525 mm tief |
| `kompost_h` | 600 | mm | [A] Hoehe Kompostbox (Quelle: Hoehe nicht festgelegt) |
| `holz_t` | 25 | mm | [A] Fichte 25 mm (Wand, Boden, Deckel) |
| `kiste_l` | 800 | mm | [A] Futterzuchtkiste PE 800 x 525 x 350 (Wuermer) |
| `kiste_h` | 350 | mm | [A] Hoehe der Futterzuchtkiste |
| `kiste_wand` | 6 | mm | [A] PE-Kiste Wand und Boden 6 mm |
| `abstand` | 50 | mm | [A] Abstand der Kiste neben der Kompostbox |

Gesamt-Box (Messung): X -750.0 bis 1600.0, Y -262.5 bis 262.5, Z 0.0 bis 625.0 mm; Koerper: 3.

**Toleranzen / Spiel:** Platzhalter; Kiste steht 50 mm neben der Box.

## Werkstoff und Gewicht

- Werkstoff: Fichtenholz (Kompostbox), PE (Futterzuchtkiste), Dichte 0.45 g/cm3, Farbe #c8a878 ([A] einfacher Platzhalter; kein Kontakt zu Wasser, Fisch oder Pflanzen des Kreislaufs (D85 greift nicht))
- Volumen (Messung, `solidcraft-cli eval`): 104096.3 cm3 · Masse leer: 50813 g (50.81 kg)

## Querschnitt / Profil

Kompostbox Fichte 25 mm, aussen 1500 x 525 x 600, offen, mit Deckel 25 mm; Futterzuchtkiste PE 800 x 525 x 350, Wand 6 mm.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Schlammannahme | offen von oben | Oberkante Kompostbox Z 600 | Schlamm von Hand einfuellen |

## Verbindungen und Befestigungen

- Holz verschraubt (Normteile nicht modelliert)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Rechteck 1500 x 525 | Kompostbox | Q | data/oasis-soll.json permakultur zeichnung_rect | mittel |
| Hoehen und Futterzuchtkiste | Annahme | A | Quelle legt Hoehe nicht fest; D104/D107: einfacher Platzhalter | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (permakultur: Schlamm-Senke, Zeichnung Rechteck 1500 x 525 mm, Hoehe nicht festgelegt; Beschreibung 'Permakultur um den Dom und Futterzucht (Wuermer, Kompostbox, Soldatenfliegen)'); docs/decisions.md D104, D107
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).

## Montage (L4)

1. Box auf ebenem Grund stellen
2. Schlamm aus dem Sammelbehaelter von Hand einfuellen, mit Laub abdecken

**Werkzeug:** Schaufel, Karre

## Renders

- `renders/components/permakultur_modul/permakultur_modul-01-schraeg.png`

## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_permakultur_modul.py

## Offene Fragen

- Maße und Aufbau sind Annahme (Quelle nennt nur Rechteck und Stichworte); Permakultur um den Dom, Soldatenfliegen und Wuermer-Besatz nicht modelliert
- Eigener Baustein ausserhalb der zehn Namen des Auftrags: das Soll-Bauteil `permakultur` hat sonst keine Komponente (D112 Zusatz)
