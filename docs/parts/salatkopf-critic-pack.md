# Kontextpaket Kritiker: salatkopf (Werkstatt, 29.10.2026, Rev. B)

## 1. Scope-Card (aus `docs/scope-cards.md`)
- **DRIN:** EIN Bauteil, wenige Facetten, Varianten S/M/L (Konfiguration `head_d` 70/100/130; Groesse per Skalierung des ganzen Kopfes).
- **DRAUSSEN:** Topf, Beet, Anzahl/Platzierung (Instanzen aus Tisch/Layout), NFT-Rinne.

## 2. System in fuenf Zeilen
Geodaetische Aquaponik-Kuppel (12 m). Salatkoepfe sitzen in Netztoepfen in den Topfloechern der NFT-Rinnen und in den Substratbeeten. Das Bauteil wird hundertfach instanziert und muss deshalb mit wenigen Flaechen auskommen (Tesselierung, Exportgroesse). Es ist reine Darstellung der Pflanze (keine Funktion im Wasserkreislauf). Hierarchie: Ring > Tisch > Rinne > Netztopf > Salatkopf.

## 3. Bilder (`renders/components/salatkopf/critic/` und `renders/components/salatkopf/`)
- `critic/k2-referenz-ausschnitt-salat-ref6.png` und `k2b-referenz-ausschnitt-salat-ref6-links.png`: Referenzausschnitte der Salatkoepfe auf den Tischen (ref-6): flache, breite, dichte, fransige Huegel.
- `salatkopf-02.png` (3/4-Ansicht), `salatkopf-03.png` (Seitenansicht), `salatkopf-04.png` (von oben): Modell Rev. B, Groesse M.
- `critic/k4-modell-im-eltern-kontext-rinne.png`: drei Koepfe (verschieden gedreht) in einer Rinne (zeigt den Sitz im Topfloch, der Topf ist unter dem Kopf verdeckt).

## 4. Messwerte (`scripts/workshop/check_pflanze.py`: 17/17 PASS)
96 kleine polygonale Blaetter (12-Eck, unregelmaessig, 2 mm dick, je Blatt eigener Koerper) in Fibonacci-Verteilung auf einem Halbellipsoid-Huegel (a 34, b 34 mm), Anstellwinkel steigt mit der Hoehe (Saum flach, Herz steil), Azimut/Roll/Laenge/Breite zufaellig mit festem Seed; dazu ein niedriges Achteck-Prisma als Herz und der Hals D16 x 25 im Topf. 98 Koerper, 1357 Flaechen gesamt, jeder Koerper <= 14 Flaechen (Rev. B2 nach Runde 5: mehr, kleinere Blaetter, flacherer Herzwinkel; OBJ-Export 8756 Dreiecke statt vorher 69 k). Groesse M: Breite ca. 102 mm, Hoehe ca. 51,5 mm ueber dem Topfrand (Verhaeltnis 0,50). S/M/L durch Skalierung des ganzen Kopfes (Breite 0,7 / 1,0 / 1,3 x M).

## 5. Soll
Keine OBJ-Vorgabe. ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite, Breite ca. 1,5-2 x Topfkragen (64 mm).

## 6. Bekannte Fehlinterpretationen (`docs/review-lessons.md`)
Kritiker widersprachen sich frueher bei der Proportion (flacher / hoeher): hier gilt die Zahl oben. Die Blaetter sind flache Plaettchen, die sich ueberlappen (gewollt; je Blatt eigener Koerper, die Vereinigung flacher Koerper scheitert im Kernel; gekraeuselte Blaetter sprengen das Facettenbudget bei 2716 Instanzen). Gleiche Drehung aller Instanzen im Kontextbild ist Sache des Layouts (andere Klasse). Rendering-Stil (glatt, Kantenlinien) ignorieren.

## 7. Frage und Antwortformat
Siehe `docs/review-protocol.md` Abschnitt 4: Referenz oder Modell, hoechstens fuenf Luecken, je gross/klein, Bezug, Sicherheit.
