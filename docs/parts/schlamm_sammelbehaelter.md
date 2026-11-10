# Bauteilblatt T106 schlamm_sammelbehaelter (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/schlamm_sammelbehaelter.json` und `designs/components/schlamm_sammelbehaelter.sc`, nicht von Hand aendern)

**Funktion:** Nimmt den Feststoffschlamm des Vortex (und eventuell des Biofilters) auf: Zulauf per Schwerkraft ueber den Einlaufstutzen, Ablass nur von Hand ueber den Kugelhahn d40; steht oberirdisch ausserhalb des Wasserkreislaufs, der Schlamm geht von Hand an das Permakultur-Modul, kein Rueckweg (Quelle A11, D104, Designprinzip 8). Steht tiefer als der Schlammstutzen des Vortex.

**Datei:** `designs/components/schlamm_sammelbehaelter.sc` · **Teilenummer:** T106 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche in X und Y, Z 0 = Fussboden (Behaelter-Unterkante); Ablasshahn bei +X, Einlauf in der Deckelmitte

**Anzahl (Instanzen):** 2 (je Linie einer) (Quelle: data/oasis-soll.json sludge_1, sludge_2)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `aussen_d` | 900 | mm | [Q] Zeichnung sludge_1: Radius 450 mm (Fussabdruck der Lage-Probe U1); Behaelter Ø 900 aussen |
| `wand` | 10 | mm | [A] Wand und Boden PE 10 mm |
| `innen_h` | 575 | mm | [E] 350 l = pi x 440^2 x 575 mm (Innen-Ø 880): 349,7 l; Hoehe so gewaehlt, dass der Zulauf unter dem Schlammstutzen des Vortex liegt |
| `deckel_t` | 15 | mm | [A] Deckel PE 15 mm, aufgesetzt |
| `einlauf_l` | 60 | mm | [A] Einlaufstutzen d40 (Klebemuffe, Aussen 46,25 laut leitung.py) 60 hoch auf dem Deckel |
| `ent_d` | 26 | mm | [A] Entlueftungsstutzen Ø 26 x 30 auf dem Deckel (Bohrung 10) |
| `auslauf_z` | 40 | mm | [A] Achse des Ablaufs 40 mm ueber der Behaelter-Unterkante (Restmenge unter dem Ablauf rund 18 l) |
| `hahn_d` | 52 | mm | [A] Kugelhahn d40 PVC-U, Gehaeuse Ø 52 x 70 (Platzhalter, Handelsmaß offen) |
| `vortex_schlammstutzen_z` | 697 | mm | [E] Vortex-Schlammstutzen: Podest 577 + Kugelhahn des tank_klein bei z 120 (data/parts/tank_klein.json 'kugelhahn z 120 bis 160'); der Behaelter muss tiefer stehen, damit der Schlamm abwaerts laeuft |

Gesamt-Box (Messung): X -450.0 bis 524.0, Y -450.0 bis 450.0, Z -0.0 bis 660.0 mm; Koerper: 7.

**Toleranzen / Spiel:** Rohr und Hahn stossen an; Rohr ragt 10 mm in den Behaelter. Restmenge unter dem Ablauf rund 18 l.

## Werkstoff und Gewicht

- Werkstoff: PE-HD (Behaelter, Deckel), PVC-U (Stutzen, Hahn), Dichte 0.95 g/cm3, Farbe #d9d4c0 ([A] PE-Fass oder Rundbehaelter; Wasserkontakt Schlamm, nicht Fisch (D85: Nachweis offen))
- Volumen (Messung, `solidcraft-cli eval`): 32126.3 cm3 · Masse leer: 30589 g (30.59 kg)

## Querschnitt / Profil

PE-Behaelter aussen Ø 900, Wand und Boden 10, innen Ø 880 x 575 (350 l); Deckel 15; Einlaufstutzen d40 (60 hoch, Muffe d40) mittig; Entlueftung Ø 26 x 30; Ablaufrohr d40 durch die Wand bei Z 40 mit Kugelhahn Ø 52 x 70 und Hebel.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Einlauf (Muffe d40) | PVC-U d40, Tiefe 26 | x 0, y 0, Z 600 bis 660 | Oeffnung oben; Rohr d40 vom Schlammstutzen des Vortex |
| Ablass (Kugelhahn d40) | PVC-U d40 | x 454 bis 524, z 40 | Hahn von Hand, Ablass in Eimer oder Karre |

## Verbindungen und Befestigungen

- Einlaufstutzen mit dem Deckel verklebt oder verschweisst
- Ablaufrohr durch die Wand mit Dichtung, Hahn auf das Rohr geklebt
- Deckel lose aufgesetzt

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Inhalt 350 l | Innen Ø 880 x 575 | E | Quelle: 350 l (sludge_1); Rechnung pi x 0,44^2 x 0,575 m | hoch |
| Ø 900 aussen | Zeichnung Radius 450 | Q | data/oasis-soll.json sludge_1 radius_mm 450 | mittel |
| oberirdisch, Ablasshahn von Hand | Hahn d40 bei Z 40 | Q/A | Quelle A11, D104; Hahnmaße Platzhalter | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (sludge_1: Sammelbehaelter 350 l, Ablasshahn von Hand, Stufe 1 nicht festgelegt, Zeichnung Radius 450 mm); docs/research/R61-oasis-wasserkreislauf.md Abschnitt 4 (O5); docs/decisions.md D104
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).

## Montage (L4)

1. Behaelter auf ebenen Fussboden stellen, Standort tiefer als der Schlammstutzen des Vortex
2. Rohr d40 vom Vortex zum Einlaufstutzen mit Gefaelle fuehren
3. Hahn schliessen, Deckel aufsetzen, Entlueftung offen lassen

**Werkzeug:** Lochsaege 40 mm, PVC-Kleber, Wasserwaage

## Renders

- `renders/components/schlamm_sammelbehaelter/schlamm_sammelbehaelter-01-schraeg.png`
- `renders/components/schlamm_sammelbehaelter/schlamm_sammelbehaelter-02-schnitt.png`

## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_schlamm_sammelbehaelter.py

## Offene Fragen

- Fabrikat und Wanddicke des PE-Behaelters offen (Ø 900 x 600 ist Platzhalter nach der Zeichnung); Bezug Europa siehe data/beschaffung/
- Zulauf-Gefaelle ab Vortex-Schlammstutzen: Rohrlaenge und Gefaelle gehoeren zu U6
- Geruch und Schlammverfestigung (Entlueftung, Reinigung) nicht gerechnet
- Bezug Europa und Lebensmittel (D76, D85), Stand 10.11.2026 aus data/beschaffung/u2_wasserkreislauf.json: BEH-schlammbehaelter-350: kein Angebot in Europa gefunden; Lebensmittel: offen fuer 350 l rund (kein Hersteller mit Datenblatt gelesen), Rueckfall: Werit/Buerkle/Plasteo oder Graf nach rundem Behaelter 350 l bzw; Rueckfall: Delta-V 400 l PE-HD lebensmittelecht (rechteckig 1200 x 1000 x 580 mm) laut Suchzusammenfassung [Q-Treffer, https://www.delta-v.de//out/medi
