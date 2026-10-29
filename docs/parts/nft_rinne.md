# Bauteilblatt T20 nft_rinne (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/nft_rinne.json` und `designs/components/nft_rinne.sc`, nicht von Hand aendern)

**Funktion:** Fuehrt den Naehrloesungsfilm an den Wurzeln der Pflanzen vorbei (NFT); Zulauf am hoeheren Ende (-X), Ablauf am tieferen Ende (+X).

**Datei:** `designs/components/nft_rinne.sc` · **Teilenummer:** T20 · **Revision:** A · **Bezugspunkt:** Mitte der Rinnenlaenge, Mitte Breite, Rinnenboden Z=0; Zulaufende bei -X (hoeheres Ende), Ablaufende bei +X; Rinne selbst gerade, Gefaelle entsteht im Tisch

**Anzahl (Instanzen):** Tisch innen 10 x 2, Mitte 6 x 4, aussen 8 x 2-3 (docs/components.md) (Quelle: data/layout.json hydro_tables)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `len_l` | 3232 | mm | layout.json: Laenge Aussentisch; Konfigurationszeilen L 3232 (aussen), M 1983 (Mitte), K 1304 (innen), je Phase A/B |
| `ch_w` | 130 | mm | OBJ: 129-130 |
| `ch_h` | 100 | mm | OBJ: 102-103 (Hoehe inkl. Rippen); Normmass 100 |
| `wall` | 2.5 | mm | [A] Strangpress-/Extrusionsprofil PVC-U oder PP, 2-3 mm |
| `rib_h` | 5 | mm | [A] Rippenhoehe, ref-6 |
| `hole_d` | 52 | mm | [E] Netztopf-Korpus 50 + 2 mm Spiel; Kragen 64 liegt auf |
| `cap_t` | 4 | mm | [A] Endkappe Plattenstaerke |
| `plug_len` | 14 | mm | [A] Steckzapfen-Tiefe |
| `fit` | 0.5 | mm | [A] Spiel je Seite Zapfen/Profil |
| `inlet_od` | 16 | mm | [A] Zulauf-Tuelle fuer 16-mm-Schlauch (PE-Verteilerrohr) |
| `inlet_id` | 10 | mm | [A] Tuelle Wand 3 mm (Kritiker Runde 1) |
| `inlet_len` | 25 | mm | [A] |
| `inlet_z` | 70 | mm | [A] Hoehe Zulaufachse ueber Rinnenboden |
| `drain_od` | 32 | mm | [A] Ablaufstutzen DN32 (Aussen 32, PVC-Klebemuffe 32) |
| `drain_id` | 28 | mm | [A] |
| `drain_len` | 30 | mm | [A] |
| `drain_z` | 20 | mm | [A] Ablaufachse 20 mm ueber Rinnenboden: Unterkante Bohrung 6 mm, Restfilm 3,5 mm ueber Innenboden (Kritiker: 16 mm ueber Innenboden) |
| `slope_pct` | 1.0 |  | docs/hydraulics.md 2.5: Vorschlag 1 % = 1 cm/m (FarmHub 2.4); im Tisch durch Neigung der Rinne um atan(0,01) = 0,573 Grad umgesetzt |
| `rib_w` | 5 | mm | [A] Rippenbreite (ref-6: gerippte Oberseite) |
| `rib_y1` | 38 | mm | [A] innere Rippen bei y = +-38: innen 35,5 > Netztopf-Kragenradius 32 |
| `rib_y2` | 52 | mm | [A] aeussere Rippen bei y = +-52 |
| `rib_end` | 20 | mm | [A] Rippen enden 20 mm vor der Endkappe |
| `pitch` | 250 | mm | [A] Lochabstand EINER Reihe in der Mittellinie (Scope-Card nft_rinne); Blattsalat NFT 150-250 mm (FarmHub 2.4 allgemein); Zickzack zu Nachbarrinnen = pitch/2 im Tisch |
| `n_holes` | 12 |  | [E] = floor(len_l / pitch): L 12, M 7, K 5 (Pruefzahl Scope-Card: Lochzahl = Laenge/pitch abgerundet; Lochreihen = 1) |
| `shift` | -62.5 | mm | [E] Phase der Lochreihe: Variante A -pitch/4, Variante B +pitch/4 -> benachbarte Rinnen im Tisch um pitch/2 versetzt (Zickzack) |

Gesamt-Box (Messung): X -1645.0 bis 1650.0, Y -65.0 bis 65.0, Z 0.0 bis 100.0 mm; Koerper: 3.

**Toleranzen / Spiel:** Endkappen-Zapfen mit 0,5 mm Spiel je Seite zum Innenmass 125 x 90 (Klebespalt, Fuge mit PVC-Kleber/Silikon 2 mm Kehlnaht, nicht als Koerper modelliert); Topfloch +2 mm zum Topf; Kragen R32 laesst 3,5 mm bis zur inneren Rippe.

## Werkstoff und Gewicht

- Werkstoff: PVC-U weiss, UV-stabilisiert (alternativ PP), Dichte 1.4 g/cm3, Farbe #f2f2ee ([A] ref-6 weisse Rinne)
- Volumen (Messung, `solidcraft-cli eval`): 3966.7 cm3 · Masse leer: 5553 g (5.55 kg)

## Querschnitt / Profil

Geschlossenes Rechteckprofil 130 x 95 mm, Wand 2,5 mm, vier Rippen 5 x 5 mm auf der Oberseite (y = +-38 und +-52, enden 20 mm vor den Kappen): Gesamthoehe 100; EINE Reihe Topfloecher D52 in der Mittellinie, Teilung 250 (L 12, M 7, K 5 Loecher), Reihe um shift = +-62,5 verschoben (Phase A/B fuer den Zickzack im Tisch).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Zulauf | Tuelle D16 (innen 10, Wand 3) fuer 16-mm-Schlauch | x = -len_l/2 - 29, y 0, z 70 | in, Richtung -X |
| Ablauf | Stutzen D32 (innen 28), 30 mm lang, PVC-Klebemuffe DN32 | x = +len_l/2 + 34, y 0, z 20 | aus, Richtung +X |

## Verbindungen und Befestigungen

- Endkappen als Stopfen 14 mm tief in das Profil gesteckt, 4 mm Plattenstaerke (Verklebung/Silikon, Schrauben nicht modelliert)
- Auflage auf den Querholmen des NFT-Tischs (Halteclips: im Tisch)

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/components.md und data/layout.json hydro_tables: Breite 130, Hoehe 100, Laengen 1304 / 1983 / 3232; ref-6: weisse Rinnen mit Rippen
- Abweichung zum OBJ: OBJ-Rinnen 129/130 x 102/103 mm, Laenge 1304/1983/3232: Modell Breite 130, Hoehe 100, Laenge ueber len_l (Abweichung <= 3 %). Die OBJ zeigt keine Topfloecher in den Rinnen (Platten mit Loechern, Hidrtoponia): Lochreihe nach ref-6 und Scope-Card.

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
- Scope-Card nft_rinne: Lochreihen je Rinne = 1, Loecher = floor(Laenge/pitch) (L 12, M 7, K 5), Breite 130
- Triage der Kritiker-Luecken Runde 1 und 2 in `docs/workshop-log.md`

## Offene Fragen

- Rippenprofil (vier Rippen 5x5) und Wandstaerke sind Annahmen [A]
- Lochabstand 250 ist unsere Auslegung, ref-6 gibt kein Mass
- Rinne 1304 mm innen: Eckengehrung am Zehneck-Ring klaeren (docs/components.md)
- Klebefuge der Endkappen nicht als Koerper modelliert
- Zickzack (Phase A/B) wird im Tisch gebaut, Varianten nft_rinne_<l|m|k>_<a|b>.sc
