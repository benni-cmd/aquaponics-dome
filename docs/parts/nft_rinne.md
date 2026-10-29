# Bauteilblatt T20 nft_rinne (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/nft_rinne.json` und `designs/components/nft_rinne.sc`, nicht von Hand aendern)

**Funktion:** Fuehrt den Naehrloesungsfilm an den Wurzeln der Pflanzen vorbei (NFT); Zulauf am hoeheren Ende (-X), Ablauf am tieferen Ende (+X).

**Datei:** `designs/components/nft_rinne.sc` · **Teilenummer:** T20 · **Revision:** A · **Bezugspunkt:** Mitte der Rinnenlaenge, Mitte Breite, Rinnenboden Z=0; Zulaufende bei -X, Ablaufende bei +X; Rinne selbst gerade (Neigung/Gefaelle ist Sache des Tisches)

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
| `inlet_od` | 16 | mm | [A] Tuelle D16 fuer Schlauch ID 16 mm (5/8 Zoll PVC-Gewebeschlauch); NICHT PE-Rohr 16 mm (Innen-D ca. 13) |
| `inlet_id` | 10 | mm | [A] Tuelle Wand 3 mm (Kritiker Runde 1) |
| `inlet_len` | 25 | mm | [A] |
| `inlet_z` | 70 | mm | [A] Hoehe Zulaufachse ueber Rinnenboden |
| `drain_od` | 32 | mm | [A] Ablaufstutzen d32 (PVC-U Rohr d32 fuer Klebemuffe, entspricht etwa DN25); Aussen 32, Innen 28 |
| `drain_id` | 28 | mm | [A] |
| `drain_len` | 30 | mm | [A] |
| `drain_z` | 20 | mm | [A] Ablaufachse 20 mm ueber Rinnenboden: Unterkante Bohrung 6 mm, Restfilm 3,5 mm ueber Innenboden (Kritiker: 16 mm ueber Innenboden) |
| `rib_w` | 5 | mm | [A] Rippenbreite (ref-6: gerippte Oberseite) |
| `rib_y1` | 38 | mm | [A] innere Rippen bei y = +-38: innen 35,5 > Netztopf-Kragenradius 32 |
| `rib_y2` | 52 | mm | [A] aeussere Rippen bei y = +-52 |
| `rib_end` | 20 | mm | [A] Rippen enden 20 mm vor der Endkappe |
| `pitch` | 250 | mm | [A] Lochabstand EINER Reihe in der Mittellinie (Scope-Card nft_rinne); ref-6: Abstand der Pflanzen je Reihe ca. 3-4 Kragenbreiten = 200-250 mm geschaetzt; Blattsalat NFT 150-250 mm (FarmHub 2.4); Zickzack zu Nachbarrinnen = pitch/2 im Tisch |
| `n_holes` | 12 |  | [E] = floor(len_l / pitch): L 12, M 7, K 5 (Pruefzahl Scope-Card: Lochzahl = Laenge/pitch abgerundet; Lochreihen = 1) |
| `shift` | -62.5 | mm | [E] Phase der Lochreihe: Variante A -pitch/4, Variante B +pitch/4 -> benachbarte Rinnen im Tisch um pitch/2 versetzt (Zickzack) |

Gesamt-Box (Messung): X -1645.0 bis 1650.0, Y -65.0 bis 65.0, Z 0.0 bis 100.0 mm; Koerper: 3.

**Toleranzen / Spiel:** Endkappen-Zapfen mit 0,5 mm Spiel je Seite zum Innenmass 125 x 90 (Klebespalt, Fuge mit PVC-Kleber/Silikon 2 mm Kehlnaht, nicht als Koerper modelliert); Topfloch +2 mm zum Topf; Kragen R32 laesst 3,5 mm bis zur inneren Rippe.

## Werkstoff und Gewicht

- Werkstoff: PVC-U weiss, UV-stabilisiert (alternativ PP), Dichte 1.4 g/cm3, Farbe #f2f2ee ([A] ref-6 weisse Rinne)
- Volumen (Messung, `solidcraft-cli eval`): 3966.7 cm3 · Masse leer: 5553 g (5.55 kg)
- Variante `nft_rinne_l_a`: 5.55 kg leer
- Variante `nft_rinne_l_b`: 5.55 kg leer
- Variante `nft_rinne_m_a`: 3.49 kg leer
- Variante `nft_rinne_m_b`: 3.49 kg leer
- Variante `nft_rinne_k_a`: 2.37 kg leer
- Variante `nft_rinne_k_b`: 2.37 kg leer
- Gefuellt/in Betrieb: Betriebsfuellung Naehrloesungsfilm 10 mm Tiefe x 125 mm Innenbreite x Laenge: L 4,0 l, M 2,5 l, K 1,6 l [E]; Betrieb ca. +4,0 / +2,5 / +1,6 kg zum Leergewicht der Variante

## Querschnitt / Profil

Geschlossenes Rechteckprofil 130 x 95 mm, Wand 2,5 mm, vier Rippen 5 x 5 mm auf der Oberseite (y = +-38 und +-52, enden 20 mm vor den Kappen): Gesamthoehe 100; EINE Reihe Topfloecher D52 in der Mittellinie, Teilung 250 (L 12, M 7, K 5 Loecher), Reihe um shift = +-62,5 verschoben (Phase A/B fuer den Zickzack im Tisch).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Zulauf | Tuelle D16 (innen 10, Wand 3) fuer Schlauch ID 16 mm | Spitze bei x = -len_l/2 - 29, y 0, z 70 (Kappenflaeche bei -len_l/2 - 4) | in, Richtung -X |
| Ablauf | Stutzen d32 (innen 28), 30 mm lang, PVC-Klebemuffe d32 (etwa DN25) | Spitze bei x = +len_l/2 + 34, y 0, z 20 (Kappenflaeche bei +len_l/2 + 4) | aus, Richtung +X |

## Verbindungen und Befestigungen

- Endkappen als Stopfen 14 mm tief in das Profil gesteckt, 4 mm Plattenstaerke (Verklebung/Silikon, Schrauben nicht modelliert)
- Auflage auf den Querholmen des NFT-Tischs (Halteclips: im Tisch)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Profil Breite 130 | 130 mm | OBJ | layout.json hydro_tables (Breite 129/130) | hoch |
| Profil Hoehe 100 (inkl. Rippen) | 100 mm | OBJ | layout.json hydro_tables (Hoehe 102/103, gerundet auf Normmass) | mittel |
| Laenge 1304 / 1983 / 3232 | 3 Varianten | OBJ | layout.json hydro_tables (Laenge je Ring); passt auf Zehneck-Seite (components.md) | hoch |
| Wandstaerke 2,5 mm | 2,5 mm | A | OBJ hat Plattenkoerper ohne Wand; Extrusionsprofil PVC-U 2-3 mm typisch | niedrig |
| geschlossenes Rechteckprofil (Hohlkammer) | - | Bild + A | ref-6: Rinnen wirken als weisse geschlossene Platten mit Loechern; Hohlkammer aus NFT-Praxis (FarmHub 2.4) | mittel |
| vier Rippen 5 x 5 mm auf der Oberseite | y +-38, +-52 | Bild + A | ref-6 mittlerer Tisch: laengs verlaufende Ruecken auf der Oberseite; Mass geschaetzt | niedrig |
| EINE Lochreihe in der Mittellinie | 1 Reihe | Bild | ref-6 mittlerer Tisch (je Rinne eine Reihe, Zickzack zwischen Nachbarrinnen); Scope-Card nft_rinne | hoch |
| Lochabstand 250 mm, 12/7/5 Loecher | 250 mm | A | ref-6 zeigt Raster ohne Mass (ca. 2 Topfbreiten); Blattsalat NFT 150-250 mm (FarmHub 2.4, hydraulics.md 2.5) | niedrig |
| Loch D52 | 52 mm | E | Netztopf-Korpus 50 (OBJ potplant_dxf 50 x 64 x 63) + 2 mm Spiel | mittel |
| Endkappen mit Stopfen 14 mm, Spiel 0,5 | - | A | Konstruktionspraxis fuer Steckkappen; ref-6 zeigt Kappen am Tischende nur angedeutet | niedrig |
| Zulauf-Tuelle D16 (Wand 3), z 70 | 16 mm | Bild + A | ref-6: hellblaue Schlaeuche am Tischende, ein Schlauch je Rinne; 16-mm-PE-Rohr ist Standard der Tropfbewaesserung | mittel |
| Ablaufstutzen DN32, z 20, mittig unten | 32 mm | A | Scope-Card: Ablauf mittig unten; DN32 Standard-PVC-Klebemuffe; Hoehe so, dass 3,5 mm Restfilm bleiben | niedrig |
| Gefaelle 1 cm/m | 1 % | R / hydraulics.md | FarmHub 2.4 (1 cm/m) bis Greenhouse Mgmt 1,2-3 %; Quellen widersprechen sich; im Tisch gebaut | mittel |
| Werkstoff PVC-U weiss | 1,4 g/cm3 | Bild + A | ref-6 weisse Oberflaeche; Werkstoff ungeprueft | niedrig |
| Lochphase A/B (shift +-pitch/4) | +-62,5 mm | E | Scope-Card nft_tisch: Versatz benachbarter Rinnen pitch/2; die Rinne stellt beide Phasen bereit | mittel |
| Rippen enden 20 mm vor Kappe (rib_end) | 20 mm | A | Kritiker Runde 1 (Rippenenden auslaufen lassen), Konstruktionspraxis | niedrig |
| Tuelle Laenge 25 mm, Ablaufstutzen 30 mm | 25 / 30 | A | Aufsteckbarkeit Schlauch/Muffe; ref-6 zeigt Laenge nicht | niedrig |
| Rinnen je Tisch 2 / 4 / 2-3 | - | OBJ + A | layout.json hydro_tables (2/4/2), components.md: aussen 3 nach Beetbreite 933-993 [A] | mittel |
| Anzahl Rinnen gesamt 68 | 68 | E | 10 x 2 + 6 x 4 + 8 x 3 (innen/mitte/aussen) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/components.md und data/layout.json hydro_tables: Breite 130, Hoehe 100, Laengen 1304 / 1983 / 3232; ref-6: weisse Rinnen mit Rippen
- Abweichung zum OBJ: OBJ-Rinnen 129/130 x 102/103 mm, Laenge 1304/1983/3232: Modell Breite 130, Hoehe 100, Laenge ueber len_l (Abweichung <= 3 %). Die OBJ zeigt keine Topfloecher in den Rinnen (Platten mit Loechern, Hidrtoponia): Lochreihe nach ref-6 und Scope-Card.

## Montage (L4)

1. Profil auf Laenge saegen (len_l)
2. Endkappen mit PVC-U-Kleber (nach DIN EN 14814) einkleben, Fuge 2 mm Kehlnaht
3. Rinne im Tisch auf die Querholme legen und mit Halteclips fixieren (Gefaelle und Phase A/B kommen vom Tisch)
4. Zulaufschlauch ID 16 auf die Tuelle, Ablauf mit Muffe d32 an das Sammelrohr

**Werkzeug:** Gehrungs-/Kappsaege, Silikonpistole, Bohrer-Dosensaege D52 fuer Topfloecher (falls kein Extrusionsprofil mit Loechern)

## Stueckliste-Zeile

- T20a Rinnenprofil 130x95x2,5 + 4 Rippen 5x5, PVC-U weiss: 1 je Rinne, Laenge 1304 / 1983 / 3232 (Rinnen gesamt 68: 20 + 24 + 24)
- T20b Endkappe Zulauf mit Tuelle D16: 1 je Rinne (68)
- T20c Endkappe Ablauf mit Stutzen d32: 1 je Rinne (68)
- PVC-U-Kleber DIN EN 14814: ca. 20 g je Kappe, 1 Kartusche je ca. 20 Rinnen [A]

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
- Scope-Card nft_rinne: Lochreihen je Rinne = 1, Loecher = floor(Laenge/pitch) (L 12, M 7, K 5), Breite 130, Hoehe 100 (check_nft_rinne.py, check.txt)
- Bild-Kritiker Runde 3 (Kontextpaket): Modell gewaehlt, keine grosse Luecke; Spec-Pruefer: FAIL (Herkunft im Blatt, Eltern-Merkmale) -> behoben in Runde 4
- Triage in `docs/workshop-log.md`

## Offene Fragen

- Rippenprofil (vier Rippen 5x5) und Wandstaerke sind Annahmen [A]
- Lochabstand 250 ist unsere Auslegung, ref-6 gibt kein Mass
- Rinne 1304 mm innen: Eckengehrung am Zehneck-Ring klaeren (docs/components.md)
- Klebefuge der Endkappen nicht als Koerper modelliert
- Zickzack = Versatz benachbarter Rinnen im Tisch; die Rinne liefert nur die Lochphase A/B (Konfiguration shift +-pitch/4, Dateien nft_rinne_<l|m|k>_<a|b>.sc) - Scope-Card nft_rinne vom Orchestrator zu ergaenzen
- Anzahl Rinnen je Aussentisch: layout.json 2, components.md 3 -> 3 als Annahme A (Beetbreite 933-993)
