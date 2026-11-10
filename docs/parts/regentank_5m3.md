# Bauteilblatt T107 regentank_5m3 (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/regentank_5m3.json` und `designs/components/regentank_5m3.sc`, nicht von Hand aendern)

**Funktion:** Sammelt Regenwasser (salz- und chlorfrei, erste Wahl der Nachspeisung) und gibt es ueber den Auslaufstutzen d25 an das Nachspeise-Ventil am Fischtank ab; der Ueberlaufstutzen d63 leitet bei Fuellung zum Versickern oder in die Permakultur. Einfacher Platzhalter ausserhalb der Kuppel (Quelle A16, D107, Designprinzip 4 Ausnahme).

**Datei:** `designs/components/regentank_5m3.sc` · **Teilenummer:** T107 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche in X und Y, Z 0 = Fussboden; Stutzen bei +X, Dom oben mittig

**Anzahl (Instanzen):** 1 (Regenwassertank) (Quelle: data/oasis-soll.json rain (anzahl 1))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `aussen_d` | 1700 | mm | [A] Platzhalter: stehender PE-Tank Ø 1700 (die Zeichnung zeigt nur ein Rechteck 1625 x 500, schematisch A16) |
| `wand` | 15 | mm | [A] Wand, Boden und Deckel PE 15 mm |
| `h` | 2300 | mm | [E] 5 m3 = pi x 0,835^2 x 2,27 m = 4,97 m3 (Innen-Ø 1670, Innenhoehe 2270) |
| `dom_d` | 500 | mm | [A] Domschacht Ø 500 aussen, Bohrung Ø 440 |
| `dom_h` | 150 | mm | [A] Domschacht 150 hoch |
| `domdeckel_d` | 520 | mm | [A] Domdeckel Ø 520 x 30 |
| `auslauf_z` | 150 | mm | [A] Auslauf d25 (Klebemuffe, Aussen 32,25) 150 mm ueber dem Boden (Bodensatz bleibt im Tank) |
| `ueberlauf_z` | 2150 | mm | [A] Ueberlauf d63 (Aussen 72,15) 150 mm unter dem Rand |
| `stutzen_l` | 100 | mm | [A] Stutzen ragen 100 mm aus der Wand |
| `volumen_l` | 5000 |  | [Q] Quelle: Tank-Kapazitaet 5,0 m3 (5000 Liter) |

Gesamt-Box (Messung): X -850.0 bis 950.0, Y -850.0 bis 850.0, Z -0.0 bis 2480.0 mm; Koerper: 5.

**Toleranzen / Spiel:** Platzhalter: Maße aus Annahme; Stutzen durch die Wand in Passbohrung.

## Werkstoff und Gewicht

- Werkstoff: PE-HD (Tank, Dom, Deckel), PVC-U (Stutzen), Dichte 0.95 g/cm3, Farbe #d9d4c0 ([A] Platzhalter; Regenwasser mit Fischkontakt (Nachspeisung): Tankwerkstoff lebensmittelecht, Nachweis offen (D85))
- Volumen (Messung, `solidcraft-cli eval`): 259231.2 cm3 · Masse leer: 246374 g (246.37 kg)

## Querschnitt / Profil

PE-Tank aussen Ø 1700 x 2300, Wand 15; Innen 1670 x 2270; Domschacht Ø 500 x 150 mit Bohrung Ø 440; Domdeckel Ø 520 x 30; Auslaufstutzen d25 bei Z 150, Ueberlaufstutzen d63 bei Z 2150.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Auslauf (Muffe d25) | PVC-U d25, Tiefe 19 | x 850 bis 950, z 150 | waagerecht zum Nachspeise-Ventil (Rohr d25, Eingang A) |
| Ueberlauf (Muffe d63) | PVC-U d63, Tiefe 37,5 | x 850 bis 950, z 2150 | waagerecht, Wasser zum Versickern |

## Verbindungen und Befestigungen

- Stutzen mit Dichtung durch die Wand
- Domdeckel lose, gegen Kinder gesichert

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| 5 m3 | Innen Ø 1670 x 2270 = 4,97 m3 | E/Q | Quelle rain 5,0 m3; Rechnung pi x 0,835^2 x 2,27 | hoch |
| Maße Ø 1700 x 2300 | Platzhalter | A | Quelle legt Hoehe und Lage nicht fest (rain: stufe_status ohne Hoehenangabe) | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (rain: Regenwassertank 5 m3, Salzgehalt < 12 mg/l, freies Chlor 0; Hoehe nicht festgelegt; Zeichnung Rechteck 1625 x 500 schematisch); docs/decisions.md D107
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).

## Montage (L4)

1. Tank auf tragfaehigen, ebenen Grund stellen (5 t Last)
2. Zulauf vom Kuppeldach (Regenrinne) an den Dom, Auslauf d25 zum Nachspeise-Ventil
3. Ueberlauf ableiten

**Werkzeug:** Wasserwaage, Lochsaege

## Renders


## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_regentank_5m3.py

## Offene Fragen

- Maße, Lage und Typ (stehend/liegend) vom Orchestrator angenommen, weil die Quelle sie nicht festlegt (D107); Fabrikat und Bezug Europa siehe data/beschaffung/
- Fundament und Statik fuer 5 t Wasser: N-STATIK
- Regenwasserfuehrung von der Kuppelhaut (Rinne, Filter) ist nicht modelliert
- Bezug Europa und Lebensmittel (D76, D85), Stand 10.11.2026 aus data/beschaffung/u2_wasserkreislauf.json: BEH-regentank-5000: tbs-online.de (DE), Konfidenz Q-Treffer; Lebensmittel: offen (kein Herstellernachweis gefunden), Rueckfall: Hersteller (Graf, Roth, Kingspan, 4rain) nach Datenblatt des oberirdischen Rundtanks 5000 l mit KTW/W270 oder DIN-Angabe fragen; Rueckfall: Zwei kleinere stehende Tanks oder Erdtank-Bauform (Hornbach 4rain Mono 5000 l, https://www.hornbach.de/p/erdtank-4rain-mono-5000-l/10356804 
