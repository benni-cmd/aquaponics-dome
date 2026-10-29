# Bauteilblatt T23 winkelhalter (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/winkelhalter.json` und `designs/components/winkelhalter.sc`, nicht von Hand aendern)

**Funktion:** Steift den Beinkopf der NFT-Tische gegen Kippen des Holms bzw. Kragarms: Eckwinkel zwischen Beininnenflaeche und Holmunterkante (bisher lag der Holm nur auf, ohne Verbindung).

**Datei:** `designs/components/winkelhalter.sc` · **Teilenummer:** T23 · **Revision:** A · **Bezugspunkt:** Ecke aus Beininnenflaeche (Y=0) und Holmunterkante (Z=0), Mitte der Winkelbreite (X=0); Y = vom Bein weg unter den Holm, Z = hoch; senkrechter Flansch nach -Z am Bein

**Anzahl (Instanzen):** je Bein einer: innen 20, mitte 24, aussen 32 = 76 (Quelle: docs/scope-cards.md winkelhalter; Tische 10/6/8 laut data/layout.json hydro_tables, Beine 2/4/4 je Tisch (tisch_geom.py))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `wh_w` | 36 | mm | [A] Winkelbreite 36, 2 mm schmaler als Bein/Holm (40), damit die Diagonalen (ausserhalb der Beinflaeche) frei bleiben |
| `wh_t` | 4 | mm | [A] Blechdicke Stahlwinkel |
| `wh_lv` | 60 | mm | [A] senkrechter Flansch (am Bein) |
| `wh_lh` | 60 | mm | [A] waagerechter Flansch (unter dem Holm) |
| `wh_hole` | 6.6 | mm | [E] Durchgangsloch M6 mittel (ISO 273) |
| `wh_pitch` | 25 | mm | [A] Lochabstand je Flansch |
| `wh_edge` | 20 | mm | [A] erstes Loch ab Winkelkante bzw. Holmunterkante |
| `leg_w` | 40 | mm | nft_tisch leg_w (Bein 40 x 40 x 3) |

Gesamt-Box (Messung): X -18.0 bis 18.0, Y -46.0 bis 60.0, Z -60.0 bis 12.0 mm; Koerper: 7.

**Toleranzen / Spiel:** Loch D6,6 fuer M6 (ISO 273 mittel); Winkelbreite 36 gegen Bein 40 (2 mm Luft je Seite).

## Werkstoff und Gewicht

- Werkstoff: Stahl S235 feuerverzinkt, Dichte 7.85 g/cm3, Farbe #aeb4b8 ([A] Standard-Eckwinkel; Normteile Stahl 8.8 verzinkt)
- Volumen (Messung, `solidcraft-cli eval`): 21.9 cm3 · Masse leer: 172 g (0.17 kg)

## Querschnitt / Profil

L-Winkel 36 breit, 4 mm dick, Schenkel 60 + 60 mm; je Schenkel 2 Loecher D6,6 im Abstand 25 (erstes Loch 20 mm von der Kante).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Anlage Bein | senkrechter Flansch 36 x 60 x 4 | y 0..4, z -60..0 (Bezug = Ecke) | liegt an der Innenflaeche des Beins (Rechteckrohr 40 x 40 x 3), 2 x M6x50 mit Mutter auf der Aussenseite |
| Anlage Holm | waagerechter Flansch 36 x 60 x 4 | y 0..60, z -4..0 | liegt an der Unterseite von Querholm bzw. Kragarm (40 x 60 x 3), 2 x M6x16 in Blindnietmuttern M6 (nicht modelliert, A) |
| Ausrichtung je Bein | Y vom Bein weg, unter den Holm | Bein mit ly < 0: Drehung 0, Bein mit ly > 0: Drehung 180 Grad um Z | Platzierung durch nft_tisch.py je Bein |

## Verbindungen und Befestigungen

- Senkrechter Flansch: 2 x Sechskantschraube M6x50 ISO 4017 und Mutter ISO 4032 durch beide Rohrwaende des Beins (Huelse gegen Quetschen nicht modelliert, A); Kopf auf der Winkelseite
- Waagerechter Flansch: 2 x M6x16 ISO 4017 von unten in Blindnietmuttern M6 im Holm (nicht modelliert, A)
- Scheiben ISO 7089 nicht modelliert (A)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Winkel 36 x 60 x 60 x 4 | 36 / 60 / 4 mm | A | Baumarkt-Eckwinkel; Breite 2 mm kleiner als Bein/Holm | niedrig |
| Loecher D6,6, 2 je Flansch, Abstand 25 | D6,6 / 25 mm | E + A | ISO 273 mittel fuer M6; Anzahl/Abstand Annahme | niedrig |
| Beinmass 40 x 40 x 3, Holm 40 x 60 x 3 | 40 / 60 | nft_tisch | data/components/nft_tisch.json leg_w, holm_w, holm_h | mittel |
| Bein M6x50 / Holm M6x16 | 50 / 16 mm | E | Klemmlaenge Flansch 4 + Bein 40 + Mutter 5 = 49 -> 50; Flansch 4 + Holmwand 3 = 7 -> 16 in Blindnietmutter | niedrig |
| Anzahl 76 | 76 | OBJ + E | layout.json hydro_tables 10/6/8, Beine 2/4/4 je Tisch (tisch_geom.py) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/scope-cards.md winkelhalter und nft_tisch (Bein 40 x 40 x 3, Holm 40 x 60 x 3); Winkelmasse Annahme A (Baumarkt-Eckwinkel)
- Abweichung zum OBJ: keine OBJ-Vorgabe (Beinkoepfe in ref-6 nicht aufgeloest); Ausfuehrung Annahme A.

## Montage (L4)

1. Winkel an die Holmunterkante legen, 2 Blindnietmuttern M6 setzen, Winkel mit 2 x M6x16 anschrauben
2. Bein unter den Holm stellen, Winkel am Bein anbohren (D6,6) und 2 x M6x50 mit Muttern festziehen

**Werkzeug:** Bohrmaschine, Nietmutternzange M6, Schluessel 10

## Stueckliste-Zeile

- T23 Winkelhalter 36 x 60 x 60 x 4, S235 verzinkt, mit 2 x M6x50 + Mutter und 2 x M6x16: 76 Stueck gesamt (innen 20, mitte 24, aussen 32)

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

- Gauntlet-Urteil: Spec-Pruefer Runde 1 laeuft
- scripts/workshop/check_nft_tisch.py (160/160 PASS): je Tisch Winkelzahl = Beinzahl (innen 2, mitte 4, aussen 4), 6 Normteile je Winkel, Anlage an der Beininnenflaeche (Abstand 0), Oberkante = Beinoberkante = Holmunterkante, Schenkel 60 x 60
- Bilder `renders/components/winkelhalter/` 01-03 (Einzelteil), 04-05 (Winkel am Beinkopf mitte, Ecke und Gegenseite), 06 (Querschnitt Bock); Winkel liegt an Holmunterkante, Diagonalen (Flachstahl ausserhalb der Beinflaeche) kollidieren nicht (Winkelbreite 36 < 40)

## Offene Fragen

- Statik der Verbindung (Kippmoment Ausleger innen) nicht nachgewiesen
- Blindnietmuttern M6 nicht modelliert (Stueckliste)
- Huelsen gegen Quetschen der Beinrohre nicht modelliert
