# Bauteilblatt T20 nft_rinne (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/nft_rinne.json` und `designs/components/nft_rinne.sc`, nicht von Hand aendern)

**Funktion:** Fuehrt den Naehrloesungsfilm an den Wurzeln der Pflanzen vorbei (NFT); Zulauf am hoeheren Ende (-X), Ablauf am tieferen Ende (+X).

**Datei:** `designs/components/nft_rinne.sc` · **Teilenummer:** T20 · **Revision:** A · **Bezugspunkt:** Mitte der Rinnenlaenge, Mitte Breite, Rinnenboden Z=0; Zulaufende bei -X (hoeheres Ende), Ablaufende bei +X; Rinne selbst gerade, Gefaelle entsteht im Tisch

**Anzahl (Instanzen):** Tisch innen 10 x 2, Mitte 6 x 4, aussen 8 x 2-3 (docs/components.md) (Quelle: data/layout.json hydro_tables)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `len_l` | 3232 | mm | layout.json: Laenge Aussentisch; Konfigurationen K 1304 (innen), M 1983 (Mitte), L 3232 (aussen) |
| `ch_w` | 130 | mm | OBJ: 129-130 |
| `ch_h` | 100 | mm | OBJ: 102-103 (Hoehe inkl. Rippen); Normmass 100 |
| `wall` | 2.5 | mm | [A] Strangpress-/Extrusionsprofil PVC-U oder PP, 2-3 mm |
| `rib_h` | 5 | mm | [A] Rippenhoehe, ref-6 |
| `rib_w` | 8 | mm | [A] |
| `rib_y` | 40 | mm | [A] Rippen-Mittellinie von der Rinnenmitte; innen 36 mm > Netztopf-Kragenradius 32 |
| `hole_d` | 52 | mm | [E] Netztopf-Korpus 50 + 2 mm Spiel; Kragen 64 liegt auf |
| `pitch` | 200 | mm | [A] Pflanzabstand Blattsalat im NFT 150-250 mm (FarmHub 2.4 allgemein) |
| `margin` | 110 | mm | [A] Abstand erstes Loch vom Rinnenende |
| `n_holes` | 15 |  | [E] = floor((len_l - 2 margin)/pitch) + 1; K 6, M 9, L 15 |
| `cap_t` | 4 | mm | [A] Endkappe Plattenstaerke |
| `plug_len` | 14 | mm | [A] Steckzapfen-Tiefe |
| `fit` | 0.5 | mm | [A] Spiel je Seite Zapfen/Profil |
| `inlet_od` | 16 | mm | [A] Zulauf-Tuelle fuer 16-mm-Schlauch (PE-Verteilerrohr) |
| `inlet_id` | 12 | mm | [A] |
| `inlet_len` | 25 | mm | [A] |
| `inlet_z` | 70 | mm | [A] Hoehe Zulaufachse ueber Rinnenboden |
| `drain_od` | 32 | mm | [A] Ablaufstutzen DN32 (Aussen 32, PVC-Klebemuffe 32) |
| `drain_id` | 28 | mm | [A] |
| `drain_len` | 30 | mm | [A] |
| `drain_z` | 25 | mm | [A] Hoehe Ablaufachse ueber Rinnenboden |
| `slope_pct` | 1.0 |  | docs/hydraulics.md 2.5: Vorschlag 1 % = 1 cm/m (FarmHub 2.4); im Tisch durch Neigung der Rinne um atan(0,01) = 0,573 Grad umgesetzt |

Gesamt-Box (Messung): X -1645.0 bis 1650.0, Y -65.0 bis 65.0, Z -0.0 bis 100.0 mm; Koerper: 3.

**Toleranzen / Spiel:** Endkappen-Zapfen mit 0,5 mm Spiel je Seite zum Innenmass 125 x 90; Topfloch +2 mm zum Topf.

## Werkstoff und Gewicht

- Werkstoff: PVC-U weiss, UV-stabilisiert (alternativ PP), Dichte 1.4 g/cm3, Farbe #f2f2ee ([A] ref-6 weisse Rinne)
- Volumen (Messung, `solidcraft-cli eval`): 3889.2 cm3 · Masse leer: 5445 g (5.44 kg)

## Querschnitt / Profil

Geschlossenes Rechteckprofil 130 x 95 mm, Wand 2,5 mm, plus zwei Rippen 8 x 5 mm auf der Oberseite (y = +-40): Gesamthoehe 100; Topfloecher D52, Raster 200 mm, erstes Loch 110 mm vom Ende (K 6, M 9, L 15 Loecher).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Zulauf | Tuelle D16 (innen 12) fuer 16-mm-Schlauch | x = -len_l/2 - 29, y 0, z 70 | in, Richtung -X |
| Ablauf | Stutzen D32 (innen 28), 30 mm lang, PVC-Klebemuffe DN32 | x = +len_l/2 + 34, y 0, z 25 | aus, Richtung +X |

## Verbindungen und Befestigungen

- Endkappen als Stopfen 14 mm tief in das Profil gesteckt, 4 mm Plattenstaerke (Verklebung/Silikon, Schrauben nicht modelliert)
- Auflage auf den Querholmen des NFT-Tischs (Halteclips: im Tisch)

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/components.md und data/layout.json hydro_tables: Breite 130, Hoehe 100, Laengen 1304 / 1983 / 3232; ref-6: weisse Rinnen mit Rippen
- Abweichung zum OBJ: OBJ-Rinnen 129/130 x 102/103 mm, Laenge 1304/1983/3232: Modell Breite 130, Hoehe 100, Laenge ueber len_l (Abweichung <= 3 %). Die OBJ-Hoehe 102-103 enthaelt vermutlich Plattenreste/Rippen [A].

## Montage (L4)

1. Profil auf Laenge sagen (len_l)
2. Endkappen mit PVC-Kleber/Silikon einsetzen
3. Rinne auf Tisch-Querholme legen, mit Clips fixieren, Gefaelle 1 % einstellen (Zulaufende hoeher)
4. Zulaufschlauch D16 auf die Tuelle, Ablauf DN32 an Sammelrohr

**Werkzeug:** Gehrungs-/Kappsaege, Silikonpistole, Bohrer-Dosensaege D52 fuer Topfloecher (falls kein Extrusionsprofil mit Loechern)

## Stueckliste-Zeile

- T20a Rinnenprofil 130x95x2,5 + Rippen, PVC-U weiss, Laenge len_l (1304 / 1983 / 3232)
- T20b Endkappe Zulauf mit Tuelle D16
- T20c Endkappe Ablauf mit Stutzen DN32

## Alternative lokale Fertigung

Statt Spezialprofil: PVC-Rechteckrohr/Kabelkanal-aehnliche Profile oder PP-Rinne aus dem Gewaechshausbedarf; Loecher mit Dosensaege D52, Endkappen aus 4-mm-PVC-Platte plus Dichtleiste.

## Renders

- `renders/components/nft_rinne/nft_rinne-02-zulauf-ende.png`
- `renders/components/nft_rinne/nft_rinne-03-ablauf-ende.png`
- `renders/components/nft_rinne/nft_rinne-04-oberseite-toepfe.png`
- `renders/components/nft_rinne/nft_rinne-05-ueberblick.png`
- `renders/components/nft_rinne/nft_rinne-06-schnitt-zulauf.png`
- `renders/components/nft_rinne/nft_rinne-07-querschnitt.png`

## Pruefung

- Gauntlet-Urteil: offen
- `solidcraft-cli eval`: Boxen und Massen; Schnitt `nft_rinne-06-schnitt-zulauf.png`, Querschnitt `nft_rinne-07-querschnitt.png`
- Gefaelle: wird im Tisch gebaut (Neigung 0,573 Grad)

## Offene Fragen

- Rippenprofil und Wandstaerke sind Annahmen [A]
- Topfzahl je Rinne ist unsere Auslegung (Raster 200 mm)
- Rinne 1304 mm innen: Eckengehrung am Zehneck-Ring klaeren (docs/components.md)
