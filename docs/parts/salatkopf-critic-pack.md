# Kontextpaket Kritiker: salatkopf (Werkstatt, 29.10.2026)

## 1. Scope-Card (aus `docs/scope-cards.md`)
- **DRIN:** EIN Bauteil, wenige Facetten, Varianten S/M/L (Konfiguration `head_d` 70/100/130).
- **DRAUSSEN:** Topf, Beet, Anzahl/Platzierung (Instanzen aus Tisch/Layout), NFT-Rinne.

## 2. System in fuenf Zeilen
Geodaetische Aquaponik-Kuppel (12 m). Salatkoepfe sitzen in Netztoepfen in den Topfloechern der NFT-Rinnen und in den Substratbeeten. Das Bauteil wird hundertfach instanziert und muss deshalb mit wenigen Flaechen auskommen (Tesselierung, Exportgroesse). Es ist reine Darstellung der Pflanze (keine Funktion im Wasserkreislauf). Hierarchie: Ring > Tisch > Rinne > Netztopf > Salatkopf.

## 3. Bilder (`renders/components/salatkopf/critic/` und `renders/components/salatkopf/`)
- `critic/k2-referenz-ausschnitt-salat-ref6.png` und `k2b-referenz-ausschnitt-salat-ref6-links.png`: Referenzausschnitte der Salatkoepfe auf den Tischen (ref-6): flache, breite, fransige Huegel.
- `salatkopf-02.png` (3/4-Ansicht), `salatkopf-03.png` (Seitenansicht), `salatkopf-04.png` (von oben): Modell, Groesse M.
- `critic/k4-modell-im-eltern-kontext-rinne.png`: drei Koepfe in einer Rinne (zeigt den Sitz im Topfloch, der Topf ist unter dem Kopf verdeckt).

## 4. Messwerte (`scripts/workshop/check_pflanze.py`, `renders/components/netztopf/check.txt`: 14/14 PASS)
36 Blattscheiben (einzeln, mit Zufallsversatz fester Seed) + Kuppelkoerper + Hals, jeder Koerper < 8 Flaechen, Breite M ca. 108 mm, Hoehe ca. 55 mm ueber dem Topfrand (Verhaeltnis 0,51), Hals D16 x 25 im Topf, Konfigurationen S/M/L.

## 5. Soll
Keine OBJ-Vorgabe. ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite, Breite ca. 1,5-2 x Topfkragen (64 mm).

## 6. Bekannte Fehlinterpretationen (`docs/review-lessons.md`)
Kritiker widersprachen sich frueher bei der Proportion (flacher / hoeher): hier gilt die Zahl oben. Die Blaetter sind Scheiben, die sich ueberlappen (gewollt; je Gruppe eigener Koerper, weil die Vereinigung flacher Scheiben im Kernel scheitert). Rendering-Stil (glatt, Kantenlinien) ignorieren.

## 7. Frage und Antwortformat
Siehe `docs/review-protocol.md` Abschnitt 4: Referenz oder Modell, hoechstens fuenf Luecken, je gross/klein, Bezug, Sicherheit.
