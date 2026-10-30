# Bauteilblatt T12 salatkopf (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/salatkopf.json` und `designs/components/salatkopf.sc`, nicht von Hand aendern)

**Funktion:** Visuelles Pflanzenbauteil (Kopfsalat) fuer Rinnen und Beete; nur Darstellung, keine Funktion im Wasserkreislauf.

**Datei:** `designs/components/salatkopf.sc` · **Teilenummer:** T12 · **Revision:** B · **Bezugspunkt:** Z=0 = Kragenoberkante des Netztopfs (Mitte Topfoeffnung); Kopf waechst nach +Z, Hals nach -Z in den Topf

**Anzahl (Instanzen):** Aussenbeete 2160 Toepfe, Besatz laut Integrator (Quelle: data/layout.json)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `head_d` | 100 | mm | [A] Standard M: Breite ca. 1,05 x head_d, Hoehe ca. 0,55 x head_d (ref-6: flacher, breiter Huegel, Hoehe etwa halbe Breite); S = 70, L = 130; wirkt als solid.scale-Faktor head_d/100 auf alle Blaetter und das Herz (Hals bleibt D16) |
| `neck_d` | 16 | mm | [A] Wurzelhals-Durchmesser, steckt im Netztopf (Innen-D oben 47) |
| `neck_len` | 25 | mm | [A] Wurzelhals unter Z=0 im Topf |

Gesamt-Box (Messung): X -50.6 bis 51.4, Y -51.9 bis 50.1, Z -25.0 bis 51.5 mm; Koerper: 98.

**Toleranzen / Spiel:** Hals D16 in Netztopf-Innen-D 47 (oben).

## Werkstoff und Gewicht

- Werkstoff: Pflanze (Kopfsalat), Dichte 0.4 g/cm3, Farbe #58a63f ([A] Bulk-Dichte Naeherung nur fuer die Gewichtsangabe; Frischmasse eines Kopfes real 150-250 g (Blatt: Modellmasse ist die Frischmasse-Naeherung))
- Volumen (Messung, `solidcraft-cli eval`): 66.4 cm3 · Masse leer: 27 g (0.03 kg)

## Querschnitt / Profil

Blattrosette: 96 kleine, ebene Polygonblaetter (12-Eck, unregelmaessiger Umriss, 2 mm dick, je Blatt eigener Koerper, <= 14 Flaechen) auf einem Halbellipsoid (a 34, b 34 mm bei head_d 100), Anstellwinkel steigt von flach am Saum bis steil im Herzen, Azimut, Roll, Laenge und Breite zufaellig (fester Seed); Herz = niedriges Achteck-Prisma, Wurzelhals D16 x 25 mm nach unten in den Netztopf. Groesse M: Breite 102 mm, Hoehe 52 mm ueber dem Topfrand; S/L entstehen durch Skalierung (0,7 / 1,3). Blaetter ueberlappen sich gewollt; die Vereinigung flacher Koerper scheitert im Kernel, daher keine Booleans.

## Verbindungen und Befestigungen

- Hals steckt im Netztopf; Instanz wird mit Ursprung auf die Kragenoberkante des Netztopfs gesetzt (Topf-Ursprung + 63 mm).

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Groessen S 70 / M 100 / L 130 (head_d) | 3 | A | Wachstumsstadien; Konfigurationen, Quelle Ben/cad-standard (Groessenvarianten) | niedrig |
| Wurzelhals D16 x 25 | 16 / 25 | A | steckt in Netztopf-Innen-D 47; ref-6 zeigt es nicht | niedrig |
| Gruen #58a63f | #58a63f | Bild | ref-6 Salatgruen | mittel |
| Anzahl | je Pflanzplatz | OBJ | layout.json: 2160 Topfpositionen; Besatz legt der Integrator fest | mittel |
| Salat als buschige Blattrosette (96 Polygonblaetter auf Halbellipsoid) | - | Bild | ref-6 mittlerer Tisch: buschige, dichte Kopfsalat-Koepfe; Polygonblaetter sind unsere Vereinfachung (Kritiker R1-R4) | mittel |
| Breite M ca. 102 mm, Hoehe 52 mm | 102 / 52 mm | Bild + A | ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite; Kopf ca. 1,5-2 x Topfkragen (64 mm) | niedrig |
| Huegel Halbellipsoid a 34 / b 34 mm, Fibonacci-Verteilung der Blaetter | 34 / 34 mm | A | gleichmaessige Flaechenbelegung ohne Muster (Kritiker R4: gestapelte Scheiben) | niedrig |
| Blatt 12-Eck 19 x 15.5 mm, 2 mm dick, Streuung Laenge 14 %, Breite 12 % | 19 x 15.5 x 2 mm | A + Bild | ref-6: fransige Silhouette; wenige Flaechen je Koerper (12-Eck-Prisma = 14 Flaechen) | niedrig |
| Anstellwinkel 16 Grad + 0.5 x Hoehenwinkel, Streuung +-13 Grad; Azimut +-50 Grad, Roll +-50 Grad | Seed sin(i*12,9898) | A | Saum flach/haengend, Herz aufrecht (ref-6, Kritiker R3); deterministisch fuer reproduzierbare .sc | niedrig |
| Herz: Achteck-Prisma r 17, h 20, ab z 8 | r 17 / h 20 mm | A | dunkler Kern unter den Blaettern, verdeckt Luecken | niedrig |
| S/M/L per solid.scale (head_d / 100 mm) | 0,7 / 1,0 / 1,3 | A | Facetten bleiben gleich; Hals D16 bleibt (steckt im Topf) | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: ref-6: Kopf ca. 1,5-2 x Topfkragen (64 mm) breit, flacher dichter Huegel (Hoehe ca. 0,5 x Breite) [A]
- Abweichung zum OBJ: keine OBJ-Vorgabe (Salatkoepfe stammen aus ref-6); Groesse M: Breite 102 mm, Hoehe 52 mm (Verhaeltnis 0.51; ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite).

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

- Gauntlet-Urteil: Bild-Kritiker Runde 5 (Rev. B, 29.10.): Urteil Referenz; Luecken in Sache umgesetzt (Rev. B2, mehr/kleinere Blaetter, flacherer Herzwinkel), kein zweiter Lauf (Pruefer-Budget)
- scripts/workshop/check_pflanze.py (18/18 PASS, davon 9 Salatkopf): 96 Blaetter, Breite M 95-125, Hoehe 50-70, Hals im Topf, Flaechenbudget, Konfigurationen S/M/L, Breite S/L = 0,7/1,3 x M
- Facetten: 98 Koerper, 1357 Flaechen gesamt, OBJ-Export 8756 Dreiecke (solidcraft-cli run salatkopf.sc --out x.obj; vorher 69 k)

## Offene Fragen

- Blattraender eben und kantig (keine Kraeuselung): gekraeuselte Blaetter brauchen viele Flaechen, Budget bei 2730 Instanzen
- Konfigurationen S/L wirken auf verknuepfte Instanzen im Dom: Integrator pruefen
- Instanzvariation (zufaellige Drehung um Z, S/M/L gemischt) ist Sache des Layouts/Tisches
