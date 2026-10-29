# Bauteilblatt T23 winkelhalter (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/winkelhalter.json` und `designs/components/winkelhalter.sc`, nicht von Hand aendern)

**Funktion:** Verbindet Bein und Querholm/Kragarm der NFT-Tische als loesbare Schraubverbindung (Eckwinkel zwischen Beininnenflaeche und Holmunterkante): Holm/Kragarm wird nicht mehr geschweisst, sondern ueber den Winkelhalter am Beinkopf gesichert (Job W11).

**Datei:** `designs/components/winkelhalter.sc` · **Teilenummer:** T23 · **Revision:** A · **Bezugspunkt:** Ecke aus Beininnenflaeche (Y=0) und Holmunterkante (Z=0), Mitte der Winkelbreite (X=0); Y = vom Bein weg unter den Holm, Z = hoch; senkrechter Flansch nach -Z am Bein

**Anzahl (Instanzen):** je Bein einer: innen 20, mitte 24, aussen 32 = 76 (Quelle: docs/scope-cards.md winkelhalter; Tischzahlen 10/6/8 aus docs/components.md (Zehneck-Sockel: 10 Sektoren, 8 Aussen-, 6 Innenbeete; layout.json hydro_tables ist nur eine Beispielliste), Beine 2/4/4 je Tisch (tisch_geom.py))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `wh_w` | 36 | mm | [A] Winkelbreite 36, 2 mm schmaler als Bein/Holm (40), damit die Diagonalen (ausserhalb der Beinflaeche) frei bleiben |
| `wh_t` | 4 | mm | [A] Blechdicke Stahlwinkel |
| `wh_lv` | 60 | mm | [A] senkrechter Flansch (am Bein) |
| `wh_lh` | 60 | mm | [A] waagerechter Flansch (unter dem Holm) |
| `wh_hole` | 6.6 | mm | [E] Durchgangsloch M6 mittel (ISO 273) |
| `wh_pitch` | 25 | mm | [A] Lochabstand im waagerechten Flansch |
| `wh_edge` | 20 | mm | [A] erstes Loch im waagerechten Flansch ab Winkelkante (Holmunterkante, vom Bein weg gemessen ab Flanschdicke) |
| `leg_w` | 40 | mm | [A] uebernommen aus data/components/nft_tisch.json (Bein 40 x 40 x 3) |
| `wh_edge_v` | 10 | mm | [A] erstes Loch im senkrechten Flansch ab Holmunterkante; hoch gesetzt, damit Mutter/Schraube nicht in die Diagonalen- und Laengsdiagonalenschrauben (z -40 / -45) laufen (Spec-Pruefer W11: Durchdringung) |
| `wh_pitch_v` | 16 | mm | [A] Lochabstand im senkrechten Flansch (zweites Loch bei z -26, Mutter bis z -31,8; Laengsdiagonale endet bei z ca. -34) |
| `wh_bolt_v` | 55 | mm | [E] M6x55 ISO 4017: Flansch 4 + Bein 40 + Mutter 5,2 = 49,2; mit 2 Scheiben ISO 7089 (nicht modelliert) 52,4; Standardlaenge 55 |
| `wh_bolt_h` | 16 | mm | [E] M6x16 ISO 4017: Flansch 4 + Holmwand 3 = 7, Rest in der Blindnietmutter |

Gesamt-Box (Messung): X -18.0 bis 18.0, Y -51.0 bis 60.0, Z -60.0 bis 12.0 mm; Koerper: 7.

**Toleranzen / Spiel:** Loch D6,6 fuer M6 (ISO 273 mittel); Winkelbreite 36 gegen Bein 40 (2 mm Luft je Seite).

## Werkstoff und Gewicht

- Werkstoff: Stahl S235 feuerverzinkt, Dichte 7.85 g/cm3, Farbe #aeb4b8 ([A] Standard-Eckwinkel; Normteile Stahl 8.8 verzinkt)
- Volumen (Messung, `solidcraft-cli eval`): 22.2 cm3 · Masse leer: 174 g (0.17 kg)

## Querschnitt / Profil

L-Winkel 36 breit, 4 mm dick, Schenkel 60 + 60 mm; waagerechter Flansch 2 Loecher D6,6 (y 24 / 49), senkrechter Flansch 2 Loecher D6,6 (z -10 / -26). Masse Winkel allein 127 g (16,2 cm3), mit den 6 Normteilen 172 g (21,9 cm3).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Anlage Bein | senkrechter Flansch 36 x 60 x 4 | y 0..4, z -60..0 (Bezug = Ecke) | liegt an der Innenflaeche des Beins (Rechteckrohr 40 x 40 x 3), 2 x M6x55 mit Mutter auf der Aussenseite; Loecher z -10 / -26 |
| Anlage Holm | waagerechter Flansch 36 x 60 x 4 | y 0..60, z -4..0 | liegt an der Unterseite von Querholm bzw. Kragarm (40 x 60 x 3), 2 x M6x16 in Blindnietmuttern M6 (nicht modelliert, A) |
| Ausrichtung je Bein | Y vom Bein weg, unter den Holm | Bein mit ly < 0: Drehung 0, Bein mit ly > 0: Drehung 180 Grad um Z | Platzierung durch nft_tisch.py je Bein |

## Verbindungen und Befestigungen

- Senkrechter Flansch: 2 x Sechskantschraube M6x55 ISO 4017 und Mutter ISO 4032 durch beide Rohrwaende des Beins (Bohrungen im Bein und Huelse gegen Quetschen nicht modelliert, A); Kopf auf der Winkelseite
- Waagerechter Flansch: 2 x M6x16 ISO 4017 von unten in Blindnietmuttern M6 im Holm (Loecher im Holm und Blindnietmuttern nicht modelliert, A)
- Scheiben ISO 7089 nicht modelliert (A); im Modell durchdringen die Normteile die Rohrwaende von Bein und Holm (vereinfacht, kein Loch)
- Bein-Fussplatte bleibt geschweisst (MAG); Holm/Kragarm sitzt NICHT geschweisst auf dem Bein, sondern ist ueber T23 geschraubt (Loecher vor dem Feuerverzinken bohren)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Winkel 36 x 60 x 60 x 4 | 36 / 60 / 4 mm | A | Baumarkt-Eckwinkel; Breite 2 mm kleiner als Bein/Holm | niedrig |
| Loecher D6,6, 2 je Flansch, Abstand 25 | D6,6 / 25 mm | E + A | ISO 273 mittel fuer M6; Anzahl/Abstand Annahme | niedrig |
| Beinmass 40 x 40 x 3, Holm 40 x 60 x 3 | 40 / 60 | A | Wert uebernommen aus data/components/nft_tisch.json (leg_w, holm_w, holm_h) | mittel |
| Bein M6x55 / Holm M6x16 | 55 / 16 mm | E | [E] M6x55 ISO 4017: Flansch 4 + Bein 40 + Mutter 5,2 = 49,2; mit 2 Scheiben ISO 7089 (nicht modelliert) 52,4; Standardlaenge 55; Holm: [E] M6x16 ISO 4017: Flansch 4 + Holmwand 3 = 7, Rest in der Blindnietmutter | niedrig |
| Anzahl 76 | 76 | OBJ + E | docs/components.md (10 Sektoren, 8 Aussen-/6 Innenbeete), Beine 2/4/4 je Tisch (tisch_geom.py) | mittel |
| Lochlage senkrechter Flansch z -10 / -26 | 10 / 16 mm | A | frei von den Diagonalen-Schrauben (z -40) und der Laengsdiagonale (Ende z ca. -34): Spec-Pruefer W11 fand die Durchdringung bei z -20 / -45 | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/scope-cards.md winkelhalter und nft_tisch (Bein 40 x 40 x 3, Holm 40 x 60 x 3); Winkelmasse Annahme A (Baumarkt-Eckwinkel)
- Abweichung zum OBJ: keine OBJ-Vorgabe (Beinkoepfe in ref-6 nicht aufgeloest); Ausfuehrung Annahme A.

## Montage (L4)

1. Winkel und Rohre vor dem Feuerverzinken bohren (D6,6 in Winkel und Bein, D8 fuer Blindnietmuttern im Holm), danach verzinken
2. Blindnietmuttern M6 in die Holmunterseite setzen, Winkel mit 2 x M6x16 anschrauben
3. Bein unter den Holm stellen und den Winkel mit 2 x M6x55 und Muttern am Bein festziehen

**Werkzeug:** Bohrmaschine, Nietmutternzange M6, Schluessel 10

## Stueckliste-Zeile

- T23 Winkelhalter 36 x 60 x 60 x 4, S235 verzinkt, mit 2 x M6x55 + Mutter und 2 x M6x16 (+ 2 Blindnietmuttern M6): 76 Stueck gesamt (innen 20, mitte 24, aussen 32)

## Alternative lokale Fertigung

Eckwinkel 60 x 60 x 4 gibt es als Baumarktware (Lochwinkel, ca. 1-2 EUR/Stueck, [A] nicht recherchiert); Breite 36 durch Zuschnitt aus 40er Winkel.

## Renders

- `renders/components/winkelhalter/winkelhalter-01-iso.png`
- `renders/components/winkelhalter/winkelhalter-02-unten.png`
- `renders/components/winkelhalter/winkelhalter-03-seite.png`
- `renders/components/winkelhalter/winkelhalter-04-im-tisch-mitte-ecke.png`
- `renders/components/winkelhalter/winkelhalter-05-im-tisch-mitte-gegenseite.png`
- `renders/components/winkelhalter/winkelhalter-06-querschnitt-bock.png`

## Pruefung

- Gauntlet-Urteil: Spec-Pruefer Runde 1 (29.10.) FAIL -> behoben (kein zweiter Lauf, Pruefer-Budget); kein Bild-Kritiker (Beinkopf in keiner Referenz sichtbar)
- scripts/workshop/check_nft_tisch.py (196/196 PASS): je Tisch Winkelzahl = Beinzahl (innen 2, mitte 4, aussen 4), 6 Normteile je Winkel, Anlage an der Beininnenflaeche (aus der Bein-bbox), Oberkante = Unterkante Holm/Kragarm = Beinoberkante, Breite 36, Schenkel 60 x 60, Masse 126,8 g, inspect.interference: 0 Treffer ausser Bein/Holm/Kragarm
- Bilder `renders/components/winkelhalter/` 01-03 (Einzelteil), 04-05 (Winkel am Beinkopf mitte), 06 (Querschnitt Bock); Spec-Pruefer Runde 1: FAIL (zwei Schraubendurchdringungen, Widerspruch Schweissung, Check), Befunde behoben (Loecher z -10 / -26, M6x55, Konzept geschraubt, Interferenzcheck)

## Offene Fragen

- Statik der Verbindung (Kippmoment Ausleger innen: der Winkel sitzt an der Pfosteninnenseite, nahe dem Drehpunkt des Kragarms; Abheben am Aussenrand nicht nachgewiesen) nicht nachgewiesen
- Blindnietmuttern M6, Scheiben und Huelsen gegen Quetschen der Beinrohre nicht modelliert; Bein/Holm ohne Bohrungen
- Beckenrand Z 650 und Wand 150 (Annahme A) bestimmen die 69 mm Hoehenluft und 30 mm Radialluft des Winkels beim Auslegerbock innen
