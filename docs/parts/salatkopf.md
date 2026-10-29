# Bauteilblatt T12 salatkopf (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/salatkopf.json` und `designs/components/salatkopf.sc`, nicht von Hand aendern)

**Funktion:** Visuelles Pflanzenbauteil (Kopfsalat) fuer Rinnen und Beete; nur Darstellung, keine Funktion im Wasserkreislauf.

**Datei:** `designs/components/salatkopf.sc` · **Teilenummer:** T12 · **Revision:** A · **Bezugspunkt:** Z=0 = Kragenoberkante des Netztopfs (Mitte Topfoeffnung); Kopf waechst nach +Z, Hals nach -Z in den Topf

**Anzahl (Instanzen):** Aussenbeete 2160 Toepfe, Besatz laut Integrator (Quelle: data/layout.json)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `head_d` | 100 | mm | [A] Standard M (Rosettenbreite ca. 1,05 x head_d, Hoehe ca. 0,7 x head_d); S = 70, L = 130 |
| `leaf_t_f` | 0.035 |  | [A] Blattdicke / head_d (Scheibe) |
| `core_r_f` | 0.14 |  | [A] Kernkugel Radius / head_d |
| `core_h_f` | 0.35 |  | [A] Kernkugel Hoehe / head_d |
| `neck_d` | 16 | mm | [A] Wurzelhals-Durchmesser, steckt im Netztopf (Innen-D oben 47) |
| `neck_len` | 25 | mm | [A] Wurzelhals unter Z=0 im Topf |

Gesamt-Box (Messung): X -51.0 bis 51.0, Y -47.0 bis 47.0, Z -25.0 bis 61.5 mm; Koerper: 34.

**Toleranzen / Spiel:** Hals D16 in Netztopf-Innen-D 47 (oben).

## Werkstoff und Gewicht

- Werkstoff: Pflanze (Kopfsalat), Dichte 0.4 g/cm3, Farbe #58a63f ([A] Bulk-Dichte Naeherung, nur fuer Gewichtsangabe grob; Gewicht eines Kopfes real 150-250 g)
- Volumen (Messung, `solidcraft-cli eval`): 151.7 cm3 · Masse leer: 61 g (0.06 kg)

## Querschnitt / Profil

Rosette aus 33 geneigten Blattscheiben (7 Gruppen, Neigung 8 bis 68 Grad, Blattdicke 3,5 mm) um eine Kernkugel; Wurzelhals D16 x 25 mm nach unten in den Netztopf. Blattscheiben ueberlappen sich gewollt (Pflanze).

## Verbindungen und Befestigungen

- Hals steckt im Netztopf; Instanz wird mit Ursprung auf die Kragenoberkante des Netztopfs gesetzt (Topf-Ursprung + 63 mm).

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Salat als Blattrosette (33 Blaetter, 7 Gruppen) | - | Bild | ref-6 mittlerer Tisch: buschige Kopfsalat-Koepfe; Rosette aus Scheiben ist unsere Vereinfachung (Kritiker R1/R2) | mittel |
| Breite M ca. 115 mm, Hoehe 61 mm | 115 / 61 | Bild + A | ref-6: Kopf ca. 1,5-2 x Topfkragen (64 mm) breit; Proportion 0,5-0,6 (Kritiker widerspruechlich) | niedrig |
| Groessen S 70 / M 100 / L 130 (head_d) | 3 | A | Wachstumsstadien; Konfigurationen, Quelle Ben/cad-standard (Groessenvarianten) | niedrig |
| Wurzelhals D16 x 25 | 16 / 25 | A | steckt in Netztopf-Innen-D 47; ref-6 zeigt es nicht | niedrig |
| Gruen #58a63f | - | Bild | ref-6 Salatgruen | mittel |
| Anzahl | je Pflanzplatz | OBJ | layout.json: 2160 Topfpositionen; Besatz legt der Integrator fest | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: ref-6: Kopf ca. 1,5-2 x Topfkragen (64 mm); Hoehe ca. 0,7 x Breite [A]
- Abweichung zum OBJ: keine OBJ-Vorgabe (Salatkoepfe stammen aus ref-6); Groesse M: Breite ca. 115 mm, Hoehe 61 mm.

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

- Gauntlet-Urteil: Runde 1 und 2: Referenz gewaehlt (A), grosse Luecken Silhouette/Blattstruktur; nach Umbau auf Blattrosette Runde 3 offen
- Konfigurationszeilen S/M/L angelegt (`config.table`), Rosette je Konfiguration ueber head_d skaliert

## Offene Fragen

- Blattraender kreisrund (Ellipsen/Zacken fehlen)
- Konfiguration S/L als Zeile vorhanden, Wirkung auf verknuepfte Instanz im Dom vom Integrator zu pruefen
