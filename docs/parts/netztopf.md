# Bauteilblatt T10 netztopf (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/netztopf.json` und `designs/components/netztopf.sc`, nicht von Hand aendern)

**Funktion:** Haelt die Pflanze im Beet (Kies/Blaehton, 288 je Aussenbeet) und in den NFT-Rinnen; Wurzeln wachsen durch die Schlitze.

**Datei:** `designs/components/netztopf.sc` · **Teilenummer:** T10 · **Revision:** A · **Bezugspunkt:** Mitte Boden (Z=0), Achse Z; Kragenoberkante bei Z=cup_h

**Anzahl (Instanzen):** Beete 2160 (OBJ) + Rinnen 556 (E) = 2716 (Quelle: data/layout.json pots.total (7 x 288 + 144) und docs/parts/nft_rinne.md (20 Rinnen x 5 + 24 x 7 + 24 x 12 Loecher))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `cup_h` | 63 | mm | OBJ: 63 Hoehe (docs/components.md) |
| `flange_d` | 64 | mm | OBJ: 64 groesste Breite = Kragen |
| `flange_t` | 3.5 | mm | [A] Kragen-Dicke |
| `rim_d` | 50 | mm | OBJ: 50 = Korpus-Durchmesser oben unter dem Kragen |
| `base_d` | 34 | mm | [A] Aussen-Durchmesser am Boden (Konus) |
| `wall` | 1.5 | mm | [A] Wandstaerke PP Spritzguss 1,2-1,6 |
| `floor_t` | 1.5 | mm | [A] Bodenstaerke |
| `slot_count` | 8 |  | [A] Schlitze am Umfang |
| `slot_w` | 3 | mm | [A] Schlitzbreite (Wurzeldurchtritt) |
| `slot_h` | 38 | mm | [A] Schlitzhoehe |
| `slot_z0` | 8 | mm | [A] Schlitzbeginn ab Boden |

Gesamt-Box (Messung): X -32.0 bis 32.0, Y -32.0 bis 32.0, Z -0.0 bis 63.0 mm; Koerper: 1.

**Toleranzen / Spiel:** Topfloch der NFT-Rinne D52 (Korpus 50 + 2 mm Spiel); Kragen D64 liegt auf der Deckelflaeche auf.

## Werkstoff und Gewicht

- Werkstoff: PP (Polypropylen), Dichte 0.91 g/cm3, Farbe #2b2b2b ([E] Standardwerkstoff Netztopf; Farbe schwarz wie ref-6 (dunkle Toepfe unter dem Kopf nicht sichtbar) [A])
- Volumen (Messung, `solidcraft-cli eval`): 18.4 cm3 · Masse leer: 17 g (0.02 kg)

## Querschnitt / Profil

Rotationskoerper: konischer Korpus (Aussen-D 34 unten, 50 oben), Wand 1,5 mm, Boden 1,5 mm mit Loch D10, Kragen D64 x 3,5 mm; 8 Schlitze 3 x 38 mm ab 8 mm ueber dem Boden.

## Verbindungen und Befestigungen

- Steckt lose im Topfloch der NFT-Rinne (Kragen liegt auf) bzw. im Medium des IBC-Beets; keine Schrauben.

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Hoehe 63 mm | 63 | OBJ | layout.json pots.size_mm (50 x 64 x 63) | hoch |
| Korpus-D oben 50 mm | 50 | OBJ | layout.json pots.size_mm (50) | hoch |
| Kragen D64 x 3,5 mm | 64 / 3,5 | OBJ + A | OBJ-Box 64 = Kragen (groesste Breite); Kragendicke Annahme | mittel |
| Boden-D 34 (Konus) | 34 | A | Standard-Netztopf konisch; im OBJ nur Box 'potplant_dxf' ohne Profil | niedrig |
| Wand 1,5 mm, Boden 1,5 mm, Bodenloch D10 | 1,5 | A | PP-Spritzguss typisch 1,2-1,6; OBJ ohne Wand | niedrig |
| 8 Schlitze 3 x 38 mm | 8 | A | Netztoepfe haben Schlitze fuer Wurzeln; Zahl geschaetzt | niedrig |
| Werkstoff PP schwarz | 0,91 g/cm3 | A | Standard; ref-6 zeigt den Topf nicht (vom Salat verdeckt) | niedrig |
| Anzahl 2160 | 2160 | OBJ | layout.json pots.total (7 Beete x 288 + 144); Topfzahl der Rinnen kommt aus dem Tisch | hoch |
| Schlitze 3 x 38 mm, 8 Stueck, ab 8 mm ueber dem Boden | 3 x 38 mm, 8 St. | A | Netztoepfe haben Schlitze fuer den Wurzeldurchtritt; Mass geschaetzt | niedrig |
| Bodenloch D10 | D10 | A | Standard-Netztopf; OBJ hat nur eine Box | niedrig |
| Konischer Korpus 34 -> 50 mm, Innenwand parallel | D34 / D50 | A | Standard-Netztopf konisch; Aussen-D oben 50 = OBJ | niedrig |
| Gesamtzahl 2716 = 2160 (Beete) + 556 (Rinnen) | 2716 | OBJ + E | layout.json pots.total + Rinnen-Blatt (Loecher 5/7/12 je Rinne) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/components.md: 50 x 64 x 63 mm aus dem OBJ (Pflanztopf, 2160 Stueck); Innenprofil [A]
- Abweichung zum OBJ: OBJ-Box 50 x 64 x 63: Modell Korpus 50, Kragen 64, Hoehe 63 (Abweichung 0 mm); Innenprofil und Schlitze sind Annahmen.

## Montage (L4)

1. Topf in das Loch der Rinne bzw. in die Kiesschicht druecken, bis der Kragen aufliegt
2. Setzling mit Mineralwolle/Blaehton-Substrat in den Topf setzen

**Werkzeug:** keines

## Stueckliste-Zeile

- T10 Netztopf 50/64 x 63, PP schwarz: Beete 2160 (OBJ: 7 Aussenbeete x 288 + 144 im Beet bei Azimut 113) + Rinnen 556 (20 Rinnen K x 5 Loecher + 24 Rinnen M x 7 + 24 Rinnen L x 12; Auslegung E) = 2716 gesamt; Ob Rinnen UND Beete bepflanzt werden (Tische stehen ueber den Beeten, decisions D04), entscheidet der Orchestrator/Integrator

## Alternative lokale Fertigung

Netztoepfe 50 mm sind Massenware (Gartenbedarf/Hydroponik, ca. 0,05-0,10 EUR/Stueck, [A] nicht recherchiert).

## Renders

- `renders/components/netztopf/netztopf-01-iso.png`
- `renders/components/netztopf/netztopf-02-schnitt.png`
- `renders/components/netztopf/netztopf-03-seite.png`

## Pruefung

- Gauntlet-Urteil: Bild-Kritiker (Salatkopf): vier Runden, Referenz; Spec-Pruefer: Netztopf FAIL behoben, Salatkopf PASS mit Hinweisen
- scripts/workshop/check_pflanze.py (14/14 PASS): Masse 50 x 64 x 63 (OBJ), Kragen D64, Bezugspunkt Z=0, 8 Schlitze, Material PP
- Schnitt `renders/components/netztopf/netztopf-02-schnitt.png` zeigt Wand, Kragen, Schlitze und Bodenloch; Sitz im Topfloch: `renders/components/nft_rinne/nft_rinne-06-schnitt-zulauf.png`
- Kein Bild-Kritiker: der Netztopf ist in keiner Referenz sichtbar (vom Salat bzw. der Erde verdeckt); Spec-Pruefer (Runde 1: FAIL -> behoben)

## Offene Fragen

- Farbe schwarz oder weiss (nicht sichtbar in ref-6)
- Topfhoehe 63 laut OBJ; Standardware ist oft 50 mm
- Scope-Card netztopf/salatkopf ist nur eine Zeile (ohne Format nach review-protocol 1): Orchestrator ergaenzen (Anzahl je Eltern, Referenz, Pruefzahlen)
- Anzahl gesamt 2716 gegen Board 'Salatkopf ca. 240+': Orchestrator klaeren
- Beet-Raster 288 je Beet (24 x 12) gegen layout.json distinct_along 64 / distinct_across 39: Integrator
