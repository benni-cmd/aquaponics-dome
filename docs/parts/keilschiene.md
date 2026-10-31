# Bauteilblatt T43 keilschiene (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/keilschiene.json` und `designs/components/keilschiene.sc`, nicht von Hand aendern)

**Funktion:** Befestigung der Planen-Huelle (D39, R24): Die Schiene sitzt auf einer Strebe (Schaumband dazwischen); die Folienkante wird mit dem Federdraht in den Kanal gedrueckt und haelt dort durch Klemmung. So braucht die Folie keine Tacker oder Schrauben und laesst sich beim Austausch (UV-PE ca. 4 Jahre) loesen. Je Strebe eine Schiene, Laenge = Knotenabstand minus 2 x 130 mm Knotenfreiraum, damit die Knotennabe und ihre Schrauben frei bleiben.

**Datei:** `designs/components/keilschiene.sc` · **Teilenummer:** T43 · **Revision:** A · **Bezugspunkt:** Mitte der Laenge, X Laengsrichtung, Z 0 = Unterkante Schaumband (Kontaktflaeche auf der Strebe), Y quer; Kanal oeffnet nach +Z (aussen)

**Anzahl (Instanzen):** 65 (30 Typ A + 35 Typ B) (Quelle: data/layout.json dome.struts 65; die Basisstrebe 24-22 am Tuerfeld wird von der Schwelle ersetzt (tuer_komplett: Reststrecken 1316 mm je Seite): Montage kuerzt dort die Schiene)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `len` | 3019 | mm | [E] Typ A = Knotenabstand 3279 - 2 x node_clear 130; Typ B ueber Konfiguration 3448 (3708 - 260) |
| `node_clear` | 130 | mm | [A] Knotenfreiraum je Ende: 120 mm Strebenendversatz (params.json strut_end_offset, Steckarm der Knotennabe) + 10 mm Luft; die Nabe bleibt frei fuer Schrauben |
| `ch_w` | 25 | mm | [A] R24: Alu-Kanal ca. 25 x 15 (Lock Channel, Haendlermass) |
| `ch_h` | 15 | mm | [A] R24 |
| `ch_wall` | 1.5 | mm | [A] Strangpressprofil Aluminium 1,5 mm |
| `ch_lip` | 4 | mm | [A] Lippe 4 mm je Seite, Maulweite 17 mm (Folie + Federdraht passen hindurch) |
| `foam_w` | 25 | mm | [A] Schaumband auf der Strebenkante (R24), gleich breit wie der Kanal |
| `foam_t` | 3 | mm | [A] R24: Schaumband auf der Strebenkante |
| `foam_density` | 0.25 | g/cm3 | [A] EPDM-Zellkautschuk |
| `wire_d` | 2 | mm | [Q] Auftrag W27: Federdraht D 2 mm |
| `wire_gap` | 0.5 | mm | [A] Luft zwischen Federdraht und Kanalgrund (kein Kontakt im Modell) |
| `wire_clear` | 20 | mm | [A] Federdraht endet 20 mm vor jedem Kanalende (Einziehhilfe) |

| Typ | len | anzahl | knotenabstand |
|---|---|---|---|
| A | 3019 | 30 | 3279 |
| B | 3448 | 35 | 3708 |

Gesamt-Box (Messung): X -1509.5 bis 1509.5, Y -12.5 bis 12.5, Z 0.0 bis 18.0 mm; Koerper: 3.

**Toleranzen / Spiel:** Maulweite 17 mm gegen Federdraht 2 mm plus zwei Folienlagen (2 x 0,15 mm) mit Reserve; Federdraht 0,5 mm ueber dem Kanalgrund, endet 20 mm vor den Kanalenden (Einziehen); Pruefung check_huelle.py keilschiene (Volumen gegen Profilflaeche +-20 mm3).

## Werkstoff und Gewicht

- Werkstoff: Aluminium EN AW-6060 (Kanal), Federstahl (Draht), EPDM-Zellkautschuk (Schaumband), Dichte 2.7 g/cm3, Farbe #c4c9ce (Handbuchwerte, Annahme)
- Volumen (Messung, `solidcraft-cli eval`): 492.9 cm3 · Masse leer: 819 g (0.82 kg)
- Gefuellt/in Betrieb: nicht zutreffend (kein Fuellvolumen)

## Querschnitt / Profil

U-Profil Aluminium 25 x 15, Wand 1,5 mm, Lippen 4 mm je Seite (Maulweite 17 mm); darunter Schaumband EPDM 25 x 3; im Kanalgrund Federdraht D2 (gerade modelliert, real eine Zickzack-Feder).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Auflage auf der Strebe (Schaumband-Unterkante) | Strebe D90 (Rohr), Schaumband 25 breit | z 0 (Bezug), Mitte Y 0, ueber die ganze Laenge | liegt oben auf der Strebe, Richtung -Z |
| Befestigung an der Strebe | 2 Blechschrauben oder Schellbaender je 600 mm [A, nicht modelliert] | Raster 600 mm entlang x | Schiene gegen die Strebe, Richtung -Z |
| Folieneinlass (Maul) | 17 mm | z 18 (Oberkante), Mitte Y 0 | Folie wird von +Z in das Maul gedrueckt, Federdraht klemmt |

## Verbindungen und Befestigungen

- Schiene an der Strebe: Edelstahl-Blechschrauben 4,8 x 19 (DIN 7981) im Raster 600 mm oder Kabelbinder/Schellbaender um die Strebe [A, nicht modelliert]; ca. 6 Stueck je Strebe
- Federdraht: in den Kanal gedrueckt, haelt die Folienkante durch Federkraft (Haendler-Systeme Lock Channel, R24)
- Stoss: keine Stoesse, ein Stueck je Strebe; an den Knoten 130 mm Freiraum je Ende

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Befestigung Alu-Keilschiene + Federdraht auf allen 65 Streben | 65 Stueck | Q | docs/research/R24.md Empfehlung 2 (Domerama, Haendler, Northern Homestead) | mittel |
| Kanal 25 x 15 | 25 x 15 mm | A | R24: Alu-Kanal ca. 25 x 15 [A] | niedrig |
| Federdraht D2 | 2 mm | Q | Auftrag W27 (Blatt) | mittel |
| Laenge Typ A / B = Knotenabstand minus 2 x 130 | 3019 / 3448 mm | E | data/layout.json dome.strut_len_mm 3279 / 3708; params.json strut_end_offset 120 + 10 | mittel |
| Anzahl 30 A + 35 B | 30 + 35 | Q | data/layout.json dome.struts 65; R24 Zahlen (30 x 3,279 + 35 x 3,708) | hoch |
| Wand 1,5, Lippe 4, Maul 17 | mm | A | Strangpressprofil-Praxis | niedrig |
| Schaumband EPDM 25 x 3, Dichte 0,25 | 25 x 3 mm | A | R24: Schaumband auf der Strebenkante | niedrig |
| Dichten Aluminium 2,7 / Federstahl 7,85 | g/cm3 | A | Handbuchwerte | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: docs/research/R24.md (Befestigung: Alu-Keilschiene + Federdraht); kein Referenzbild
- Quelle der Masse: docs/research/R24.md (Befestigung: Aluminium-Keilschiene mit Federdraht auf allen 65 Streben, ca. 228 m; Kanal ca. 25 x 15 [A]); data/layout.json dome.strut_len_mm 3279 / 3708, 30 x A + 35 x B = 65; data/params.json strut_end_offset 120
- Abweichung zum OBJ: Das Bauteil kommt nicht aus dem OBJ (die Huelle ist Plane, D39). R24 rechnet 228 m aus dem Knotenabstand; mit 130 mm Freiraum je Ende ergeben sich 30 x 3,019 + 35 x 3,448 = 211,3 m (-7 %). Die Basisstrebe 24-22 am Tuerfeld wird von der Schwelle ersetzt (tuer_komplett: Reststrecken 1316 mm je Seite): die Montage kuerzt dort die Schiene.

## Montage (L4)

1. Strebenkante reinigen, Schaumband auf die Strebe kleben
2. Kanal auf das Schaumband setzen und am Raster 600 mm festschrauben oder festklemmen
3. Folie ueber die Strebe legen, Federdraht abschnittsweise einziehen und die Folie dabei in den Kanal druecken
4. Folie am Ueberstand beschneiden und mit der Nachbarbahn ziegelartig ueberlappen (huelle_folie)

**Werkzeug:** Akkuschrauber, Federdrahtroller oder Schraubendreher, Cuttermesser

## Stueckliste-Zeile

- Keilschiene Typ A (Alu-Kanal 25 x 15 x 1,5, Laenge 3019) mit Schaumband EPDM 25 x 3 und Federdraht D2 x 2979: 30 Stueck
- Keilschiene Typ B (Laenge 3448, Federdraht 3408): 35 Stueck
- Befestigungsschrauben 4,8 x 19 oder Schellbaender: ca. 6 je Strebe, 390 gesamt [A, nicht modelliert]
- Gesamtlaenge Kanal 211,3 m, Federdraht ca. 209 m (Handel: Rolle 30 m Federdraht + Schiene in 3-m-Staeben, Zuschnitt vor Ort)

## Alternative lokale Fertigung

Handelsueblich: Lock-Channel-Profile (Alu oder verzinkt) mit Wiggle Wire fuer Gewaechshausfolie, Staebe 3 m; Zuschnitt auf der Baustelle mit Metallsaege.

## Renders

- `renders/components/keilschiene/keilschiene-01-iso.png`
- `renders/components/keilschiene/keilschiene-02-querschnitt.png`

## Pruefung

- Gauntlet-Urteil: kein Pruefer-Lauf (Auftrag W27: Selbstcheck)
- scripts/workshop/check_huelle.py keilschiene: Ergebnis in renders/components/keilschiene/check.txt (Profilflaeche, Laengen A/B gegen layout.json, Federdraht im Kanal, Konfiguration B, Interferenz 0)
- Kein Bild-Kritiker und kein Spec-Pruefer (Auftrag W27)

## Offene Fragen

- Kanalmass 25 x 15 ist Haendlerangabe (R24 [A]); Wandstaerke, Lippe und Maulweite sind Annahmen; Hersteller offen
- Federdraht gerade modelliert; die reale Zickzack-Feder (Wiggle Wire) ist eine Huellform
- Knotenfreiraum 130 mm: die Montage prueft gegen die Knotenarme (knoten_arme) und passt node_clear an
- Basisstrebe am Tuerfeld wird gekuerzt (Schwelle ersetzt das Mittelstueck): Montage
- Befestigung an der Strebe (Schrauben oder Schellbaender) nicht modelliert
- Winkel- und Kruemmungsfreiheit: die Schiene ist gerade, die Strebe ist es auch (Rohr); keine Kruemmung noetig
