# Bauteilblatt T12 salatkopf (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/salatkopf.json` und `designs/components/salatkopf.sc`, nicht von Hand aendern)

**Funktion:** Visuelles Pflanzenbauteil (Kopfsalat) fuer Rinnen und Beete; nur Darstellung, keine Funktion im Wasserkreislauf.

**Datei:** `designs/components/salatkopf.sc` · **Teilenummer:** T12 · **Revision:** A · **Bezugspunkt:** Z=0 = Kragenoberkante des Netztopfs (Mitte Topfoeffnung); Kopf waechst nach +Z, Hals nach -Z in den Topf

**Anzahl (Instanzen):** Aussenbeete 2160 Toepfe, Besatz laut Integrator (Quelle: data/layout.json)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `head_d` | 100 | mm | [A] Standard M: Breite ca. 1,15 x head_d, Hoehe ca. 0,5 x head_d (ref-6: flacher, breiter Hügel, Hoehe etwa halbe Breite); S = 70, L = 130 |
| `leaf_t_f` | 0.045 |  | [A] Blattdicke / head_d (Scheibe) |
| `core_r_f` | 0.27 |  | [A] Kuppelkoerper Radius / head_d (klein gehalten, damit die Blattmasse das Bild bestimmt; Kritiker R3: Kern zu glatt) |
| `core_h_f` | 0.2 |  | [A] Kernkugel Hoehe / head_d |
| `neck_d` | 16 | mm | [A] Wurzelhals-Durchmesser, steckt im Netztopf (Innen-D oben 47) |
| `neck_len` | 25 | mm | [A] Wurzelhals unter Z=0 im Topf |

Gesamt-Box (Messung): X -52.2 bis 56.4, Y -54.2 bis 54.4, Z -25.0 bis 54.9 mm; Koerper: 37.

**Toleranzen / Spiel:** Hals D16 in Netztopf-Innen-D 47 (oben).

## Werkstoff und Gewicht

- Werkstoff: Pflanze (Kopfsalat), Dichte 0.4 g/cm3, Farbe #58a63f ([A] Bulk-Dichte Naeherung nur fuer die Gewichtsangabe; Frischmasse eines Kopfes real 150-250 g (Blatt: Modellmasse ist die Frischmasse-Naeherung))
- Volumen (Messung, `solidcraft-cli eval`): 285.5 cm3 · Masse leer: 114 g (0.11 kg)

## Querschnitt / Profil

Blattrosette: Kuppelkoerper (Kugel) mit 36 geneigten Blattscheiben in 7 Gruppen (Neigung -14 bis 64 Grad, Blattdicke 4,5 mm), Wurzelhals D16 x 25 mm nach unten in den Netztopf; Groesse M: Breite 109 mm, Hoehe 55 mm ueber dem Topfrand. Blattscheiben ueberlappen sich gewollt (Pflanze); Vereinigung flacher Scheiben scheitert im Kernel, daher je Gruppe eigene Koerper.

## Verbindungen und Befestigungen

- Hals steckt im Netztopf; Instanz wird mit Ursprung auf die Kragenoberkante des Netztopfs gesetzt (Topf-Ursprung + 63 mm).

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Salat als buschige Blattrosette (33 Blaetter, 7 Gruppen, Kuppelkoerper) | - | Bild | ref-6 mittlerer Tisch: buschige Kopfsalat-Koepfe; Rosette aus Scheiben ist unsere Vereinfachung (Kritiker R1/R2) | mittel |
| Breite M ca. 109 mm, Hoehe 55 mm | 109 / 55 mm | Bild + A | ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite; Kopf ca. 1,5-2 x Topfkragen (64 mm) | niedrig |
| Groessen S 70 / M 100 / L 130 (head_d) | 3 | A | Wachstumsstadien; Konfigurationen, Quelle Ben/cad-standard (Groessenvarianten) | niedrig |
| Wurzelhals D16 x 25 | 16 / 25 | A | steckt in Netztopf-Innen-D 47; ref-6 zeigt es nicht | niedrig |
| Gruen #58a63f | #58a63f | Bild | ref-6 Salatgruen | mittel |
| Anzahl | je Pflanzplatz | OBJ | layout.json: 2160 Topfpositionen; Besatz legt der Integrator fest | mittel |
| Kuppelkoerper Radius 0,27 x head_d, Hoehe 0,20 x head_d | 0,27 / 0,20 x head_d | A | Kritiker R3: Kern klein halten, Blattmasse bestimmt das Bild | niedrig |
| Blattdicke 0,045 x head_d (4,5 mm bei M) | 0,045 x head_d | A | Scheibenblatt; Mindestdicke fuer stabile Geometrie | niedrig |
| 7 Blattgruppen (Saum haengt -14 Grad, Herz 56-64 Grad) | 36 Blaetter | A + Bild | ref-6: Randblaetter haengen nach unten (Kritiker R3), Herzblaetter aufrecht | niedrig |
| Zufallsversatz je Blatt (Azimut +-8 Grad, Radius +-14 %, Neigung +-4,5 Grad, Hoehe, Abstand) | Seed sin(i*12,9898) | A | Kritiker R3/R4: unregelmaessige Silhouette; deterministisch fuer reproduzierbare .sc | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: ref-6: Kopf ca. 1,5-2 x Topfkragen (64 mm) breit, flacher Huegel (Hoehe ca. 0,5 x Breite) [A]
- Abweichung zum OBJ: keine OBJ-Vorgabe (Salatkoepfe stammen aus ref-6); Groesse M: Breite 109 mm, Hoehe 55 mm (Verhaeltnis 0.51; ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite).

## Montage (L4)

1. Instanz auf den Topf setzen (Pattern oder `occurrence.copy`)
2. Groesse ueber Konfiguration S (70) / M (100) / L (130) waehlen

**Werkzeug:** keines

## Stueckliste-Zeile

- T12 Salatkopf, Konfigurationen S/M/L, nur Darstellung (keine Beschaffung)

## Renders

- `renders/components/salatkopf/salatkopf-01.png`
- `renders/components/salatkopf/salatkopf-02.png`
- `renders/components/salatkopf/salatkopf-03.png`
- `renders/components/salatkopf/salatkopf-04.png`

## Pruefung

- Gauntlet-Urteil: Bild-Kritiker (Salatkopf): vier Runden, Referenz; Spec-Pruefer: Netztopf FAIL behoben, Salatkopf PASS mit Hinweisen
- Konfigurationszeilen S/M/L angelegt (`config.table`), Rosette je Konfiguration ueber head_d skaliert

## Offene Fragen

- Blattraender kreisrund (Ellipsen/Zacken fehlen)
- Konfiguration S/L als Zeile vorhanden, Wirkung auf verknuepfte Instanz im Dom vom Integrator zu pruefen
- Konfigurationen S/L wirken auf verknuepfte Instanzen im Dom: Integrator pruefen
- Instanzvariation (zufaellige Drehung um Z, S/M/L gemischt) ist Sache des Layouts/Tisches (Kritiker R3/R4 Hinweis)
- Bild-Kritiker: vier Runden, Referenz gewaehlt (Stilunterschied CAD gegen Raytracing; gekraeuselte Blaetter mit < 8 Flaechen je Koerper nicht erreichbar); Restluecken: Blattraender kreisrund, glatte Scheiben
