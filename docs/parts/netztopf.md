# Bauteilblatt T10 netztopf (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/netztopf.json` und `designs/components/netztopf.sc`, nicht von Hand aendern)

**Funktion:** Haelt die Pflanze im Beet (Kies/Blaehton, 288 je Aussenbeet) und in den NFT-Rinnen; Wurzeln wachsen durch die Schlitze.

**Datei:** `designs/components/netztopf.sc` · **Teilenummer:** T10 · **Revision:** A · **Bezugspunkt:** Mitte Boden (Z=0), Achse Z; Kragenoberkante bei Z=cup_h

**Anzahl (Instanzen):** 2160 (Quelle: data/layout.json (OBJ potplant_dxf))

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

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/components.md: 50 x 64 x 63 mm aus dem OBJ (Pflanztopf, 2160 Stueck); Innenprofil [A]
- Abweichung zum OBJ: OBJ-Box 50 x 64 x 63: Modell Korpus 50, Kragen 64, Hoehe 63 (Abweichung 0 mm); Innenprofil und Schlitze sind Annahmen.

## Montage (L4)

1. Topf in das Loch der Rinne bzw. in die Kiesschicht druecken, bis der Kragen aufliegt
2. Setzling mit Mineralwolle/Blaehton-Substrat in den Topf setzen

**Werkzeug:** keines

## Stueckliste-Zeile

- T10 Netztopf 50/64 x 63, PP schwarz, Menge laut layout.json: 2160 (Beete) plus Rinnen (3 Typen, siehe NFT-Rinne)

## Alternative lokale Fertigung

Netztoepfe 50 mm sind Massenware (Gartenbedarf/Hydroponik, ca. 0,05-0,10 EUR/Stueck, [A] nicht recherchiert).

## Renders

- `renders/components/netztopf/netztopf-01.png`

## Pruefung

- Gauntlet-Urteil: offen
- Masse und Volumen aus `solidcraft-cli eval`; Schnittbild `renders/components/nft_rinne/nft_rinne-06-schnitt-zulauf.png` zeigt den Topf im Topfloch

## Offene Fragen

- Farbe schwarz oder weiss (nicht sichtbar in ref-6)
- Topfhoehe 63 laut OBJ; Standardware ist oft 50 mm
