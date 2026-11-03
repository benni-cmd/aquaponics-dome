# R52: Europa-Bezug der Kaufteile aus R50 und R51 (D76)

**Auftrag:** `docs/jobs/R52-europa-bezug.md` · **Bearbeitet:** 03.11.2026 · **Rolle:** Fachrecherche, nur lesen, im Netz suchen, rechnen, schreiben; nichts umgebaut, `gen_dome.py`, `data/*`, Netzliste und Roadmap unverändert.
**Regel D76:** Jedes Kaufteil muss mindestens in Europa bestellbar sein; ein Teil, das nur bei US-Händlern gefunden wurde, gilt als nicht beschaffbar.
**Herkunft:** [Q] Quelle selbst geöffnet (Seite oder Datenblatt gelesen) · [Q-Treffer] nur Suchergebnis oder Händlerseite, nicht selbst geöffnet · [E] eigene Rechnung (`python -X utf8 -I scripts/r52_rechnung.py`) · [A] Annahme. **Status:** *beschaffbar* = mindestens zwei europäische Quellen; *nur eine Quelle* = eine europäische Quelle; *nicht beschaffbar* = keine europäische Quelle gefunden. „Europa“ schließt hier das Vereinigte Königreich ein (Ort, nicht EU); ob das für Ben reicht, steht in Abschnitt 4. Preise: grobe Orientierung (Scope D69).

## 0. Antwort (fünf Punkte)

1. **Kegelboden-Tank: Es gibt in Europa einen fast passgenauen Standardtank, aber nur im Vereinigten Königreich.** Enduramaxx 250 l, 45°-Kegel, Ø609 × H1257, Auslauf 2″ BSP, Deckel Ø355 (Lincolnshire) [Q]. Unser `tank_klein` hat Körper-Ø623, 254 l, Kegel 48,7° (Bauteilblatt) [Q]; die Hydraulik bleibt gleich (20,0 statt 20,3 min Verweilzeit, 2,57 statt 2,46 m/h Beschickung) [E]. Die Händlerseite von Kingfisher Direct nennt die Republik Irland als Lieferziel mit Zuschlag; Versand in die EU-Festlandländer und Zoll nach dem Brexit sind **nicht geprüft** [Q].
2. **EU-Gegenstück: CGK (Niederlande), „offener runder Tank mit Konusboden“ 300 l, Typ TCO3/L, 695 × 695 × 1360 mm, Metallgestell, Gewinde oder Flansch 1″ bis 3″** [Q]. Kegelwinkel und Preis stehen nicht auf der Seite (nur Anfrage). Dritter Fund tanksdirekt.de (liefert u. a. nach DE, AT, FR, IT, PL): 200 l, „konischer Boden, vollständige Entleerung“, aber 1″-Auslauf und 16 min Verweilzeit, also nur Notlösung [Q]. D76-Status für den Tank: **nur eine EU-Quelle (CGK, Anfrage) plus eine UK-Quelle**.
3. **Alle anderen Kaufteile sind in Europa bestellbar** (Tabelle in Abschnitt 2): Siebgewebe 100 µm, Lochblech RV 5-8, Reduktion 40 × 25, Kugelhähne d40/d63/d75, Bulkheads, Schwimmerschalter, Tauchpumpen 5000 bis 6000 l/h, Beutelgehäuse und -beutel. **Nicht beschaffbar in Europa: ein fertiger 100-µm-Siebkorb in der Größe 560 × 370 × 400**; Ersatz ist der Korb aus Gewebe und Rahmen (Selbstbau).
4. **Zwei Stellen in R50 sind zu korrigieren:** Aquagart-Edelstahlgewebe ist nur mit 300 µm belegt, nicht mit 100 µm (R50 Zeile 27 und 85); die US-Beutelgehäuse (PRM, Shelco, Zoro, Pentair-NPT) fallen unter D76 weg, Ersatz Hennlich (AT) und Eaton (Abschnitt 2). Liste mit Datei und Zeile in Abschnitt 3.
5. **Ben muss entscheiden:** UK als „Europa“ akzeptieren, oder nur EU? Und: Enduramaxx (passt, UK) gegen CGK 300 l (EU, größer, Anfrage). Ich ändere am Bauteil nichts (Abschnitt 4).

## 1. Kegelboden-Tank (Absetzer `tank_klein`)

### 1.1 Gesucht und gefunden
Gesucht in Deutsch, Niederländisch, Polnisch, Italienisch, Spanisch, Französisch und Englisch (Spitzbodentank, Konustank, Trichterboden, conische tank, zbiornik stożkowy, serbatoio conico, depósito cónico, cuve conique). Die meisten Treffer sind US-Tanks in Gallonen (300 gal ≈ 1136 l, nicht 300 l); eine europäische Produktlinie mit Kegelboden im Bereich 200 bis 300 l gibt es nur bei den drei folgenden Herstellern bzw. Händlern.

| # | Hersteller / Händler, Modell | Maße, Volumen | Kegel, Anschlüsse | Sonstiges | Lieferland, Link | Herkunft |
|---|---|---|---|---|---|---|
| 1 | **Enduramaxx** (Lincolnshire, UK), 250 Litre 45° Closed Top Cone Tank, SKU 17520145 | Ø609 × 1257 (ohne Gestell), 1562 mit Gestell; 250 l | **45°**; Bodenauslauf **2″ BSP** (Teilecode 178020-BDV 3.5); Deckel Ø355, belüftet oder nicht | HDPE, UV-stabilisiert, lebensmittelecht; Gestell als Option (Stahl verzinkt, „speziell für diesen Tank“); Wandstärke nicht genannt; UK-Listenpreis 344 £ ohne MwSt (Händler) | UK; Händler Kingfisher Direct nennt Irland als Zuschlagsgebiet; EU-Festland nicht genannt. [Hersteller](https://www.enduramaxx.co.uk/enduramaxx/250-litre-45-cone-tank/), [Händler](https://kingfisherdirect.co.uk/enduramaxx-250-litre-45-degree-cone-tank) | [Q] beide Seiten gelesen |
| 2 | **CGK Chemical Process Solutions** (NL), offener runder Tank mit Konusboden 300 l, Typ TCO3/L, Art. 56.342.01.01 | 695 × 695 × 1360; 300 l | Kegelwinkel **nicht genannt**; Anschluss Gewinde oder Flansch **1″ bis 3″** wählbar; Schraubdeckel Ø200 belüftet | lineares PE, FDA, UV; „stabiles Metallgestell“ lackiert, verzinkt oder Edelstahl; weiß, schwarz oder grau; Preis nur auf Anfrage; „schnelle Lieferung dank Standardgrößen“ ohne Länderangabe | NL; [Produktseite](https://cgk-group.com/en/chemicals/solutions/storage-of-chemicals-hazardous-materials/kunststof-opslagtanks/silos-and-conical-tanks/silos-for-liquids/gesloten-ronde-procestanks/gesloten-rechthoekige-tank-met-conische-bodem-115-l-6-3-2-2-3-2-3-2-2-2-2-2-2-2-2-7-6); gleiche Reihe 190 l und 500 l | [Q] Produktseite gelesen; Hersteller hinter der Marke nicht genannt |
| 3 | **tanksdirekt.de** (Rotterdam-Plastics-Gruppe), 200 Litre Conical Water Tank | 568 × 568 × 975 (1015 mit Deckel); 200 l; Wand 6 bis 7 mm; 17,5 kg | „conical base, complete drainage“; **1″ BSP** (Messing, eingeformt, offen oder ungebohrt); Schraubdeckel Ø200, Revision Ø189 | Naturfarben/PE; Lieferländer laut Seite u. a. DE, AT, BE, NL, FR, IT, PL, ES, CZ, DK, SE; ob Kegelspitze oder Kegelstumpf mit Flachboden: nicht eindeutig | [Produktseite](https://tanksdirekt.de/en/200-litre-conical-watertank) | [Q] Seite gelesen |

**Gefunden, aber ungeeignet:** Cemo GFK-Großbehälter 200 l „konisch“ (Art. 203892): trichterförmiger, ineinanderstellbarer GFK-Behälter mit Fußgestell, kein Kegelbodentank mit Auslauf, laut Händlerseite nicht lebensmittelgeeignet [Q-Treffer, Mercateo-Datenblatt]. Colasit AG (Spiez, CH) und AGK Kronawitter (DE) fertigen PE-HD-Fischzuchtbecken nach Kundenwunsch, ohne Standardmaße im Bereich 200 bis 300 l [Q-Treffer]. Die US-Tanks aus R50 (Norwesco, Chemical Containers, Tanks Supply Direct) entfallen nach D76. Denios, Delta-V und Rotterdam Plastics: keine Kegelboden-Tanks in 200 bis 300 l gefunden (Seite von Rotterdam Plastics war nicht abrufbar, 429).

### 1.2 Vergleich mit `tank_klein` (Maße aus `docs/parts/tank.md`, Rechnung `scripts/r52_rechnung.py`)

| Größe | `tank_klein` (T40) | Enduramaxx 250 l | CGK TCO3/L 300 l | tanksdirekt 200 l |
|---|---|---|---|---|
| Körper-Ø (mm) | 623 (Außen 673 mit Randwulst 25) | 609 | 695 × 695 (Grundfläche, mit Gestell?) | 568 |
| Gesamthöhe Rand bis Spitze (mm) | 1075 | 1257 (+182) | 1360 (mit Gestell?) | 975 (1015 mit Deckel) |
| Kegelwinkel | 48,7° (Bauteil; aus Spitze Z 172 und Ende Z 501 gerechnet 46,6° [E], Abweichung offen) | **45°** | unbekannt | unbekannt („konisch“) |
| Volumen (l) | 254 bis Rand | 250 nominal | 300 | 200 |
| Beschickung bei 12,5 l/min [E] | 2,46 m/h | 2,57 m/h | 1,98 m/h | 2,96 m/h |
| Verweilzeit [E] | 20,3 min | **20,0 min** | 24,0 min | **16,0 min** |
| Bodenauslauf | Kugelhahn d40 (Netz K07) | 2″ BSP | 1″ bis 3″ frei | 1″ BSP |
| Deckel | 6 mm, Revision Ø200 | Ø355 | Schraubdeckel Ø200 | Schraubdeckel Ø200 |
| Standfuß | Plattform + 4 Beine (Selbstbau, Kegelsitz) | Stahlgestell optional | Metallgestell (3 Ausführungen) | keiner |

Zur Einordnung der Rechnung: R50 nennt 2,17 m/h, weil es mit der Außenfläche (Ø673) rechnet; hier gilt die Körperfläche (Ø623), deshalb 2,46 m/h. Bewertungsgrenzen aus R50: Verweilzeit 15 bis 30 min (SRAC 453), Richtwert mindestens 20 min (Aquaponics411). **Enduramaxx liegt auf dem Bauteilmaß; CGK ist 46 l größer, besser in Verweilzeit und Beschickung, aber Kegelwinkel und Höhe ohne Anfrage unbekannt; tanksdirekt 200 l unterschreitet die 20 min.**

### 1.3 Folgen, wenn Enduramaxx statt `tank_klein` gewählt wird (nur Liste, nichts geändert)
- Höhe Rand bis Spitze 1257 statt 1075 (+182 mm; berechnet reicht 250 l bis 1061 mm, der Rest ≈ 196 mm ist Hals und Deckel [E]): Zulauf (250 mm unter Rand), Auslauf (100 mm unter Rand), Leitrohr (420 mm unter Deckel) und Gesamthöhe über Plattform neu setzen.
- Kegel 45° (statt 48,7°) und Körper-Ø 609 (statt 623): Kegelsitz der Plattform und das Plattformmaß (619 = 2 × (Konusradius 247 + 2 + 60), W30/D50) neu rechnen; Randwulst: Hersteller nennt keinen, das Bauteil hat 25 × 40.
- Auslauf 2″ BSP statt d40: Übergang 2″ Außengewinde auf d63 Klebemuffe, Kugelhahn d63 und Reduktion auf d40 (alles Katalogteile, Abschnitt 2), oder 2″-Hahn mit Gewinde. Netz K07 (d40) und Bauteil-Port ändern sich.
- Deckel Ø355 (statt Revision Ø200): gut für das Leitrohr d110, aber das Bauteil hat einen Deckel 6 mm mit Revisionsloch.
- Zulauf und Auslauf d50 durch die Tankwand: Lochsäge und Bulkhead (Abschnitt 2); Wandstärke nicht genannt [offen, beim Hersteller erfragen].
- Optional das Enduramaxx-Gestell statt Plattform und Beinen (spart Selbstbau, Preis auf Anfrage, Höhenlage des Kegels offen): wäre eine Vereinfachung, aber eigene Entscheidung.
- Wenn CGK 300 l: Kegelwinkel, Höhe ohne Gestell und Gestellmaß anfragen; Grundfläche 695 liegt über der Plattform 619.

## 2. Alle weiteren Kaufteile aus R50 und R51

| Teil | Verwendung | Europa-Quelle 1 | Quelle 2 | Status | Hinweis |
|---|---|---|---|---|---|
| Edelstahl-Siebgewebe 100 µm, Meterware | Korb Feinfilter T55, Subtank (D75) | [Metallwaren-Riffert (AT)](https://www.metallwaren-riffert.at/siebgewebe.htm): MW-0,10, 1.4301, Leinwand, Draht 0,065 mm, rund 36 % offen [Q-Treffer, Seite nicht abrufbar: Zertifikatsfehler] | eBay.de-Händler: Edelstahlgewebe 0,100 mm (V4A 1.4401), Zuschnitte bis 200 × 60 cm; Beissermetall (DE, Stuttgart) und Teichhansel (DE) fertigen oder beschaffen auf Anfrage [Q-Treffer] | **beschaffbar** | Aquagart (Galaxus CH, R50) ist nur mit 300 µm belegt, **nicht 100 µm**. Rolle 1000 mm breit nur auf Anfrage; Stücke bis 600 mm Breite im Handel. Offene Fläche rund 36 % deckt sich mit der Annahme 35 % in R50 1.1; Fabrikat und Draht bei Anfrage festlegen |
| Edelstahl-Lochblech 1,5 mm, 1.4301, RV 5-8 (Rundloch 5, Teilung 8 versetzt) | Medienschutz S-A im Beet (R51), Stützkorb | [ehorst.de (DE)](https://www.ehorst.de/Lochblech-Edelstahl-1-4301-RV-5-8-1-50-1000-2000-mm-beids-K240-Folie-DIN24041-1003438.html), Art. 1003438, Tafel 1000 × 2000, geschliffen mit Folie, „sofort lieferbar“, Preis nach Login [Q] | Preissuchmaschine listet RV 5-8 V2A roh 1,5 mm als Zuschnitt; BUCHERT Stahl (eBay.de) RV 5-8 VA **2 mm** als Zuschnitt [Q-Treffer] | **beschaffbar** | Die Seite von ehorst nennt das Lochmaß nicht; „RV“ = Rundlochung versetzt nach DIN 24041, 5-8 = Loch 5, Teilung 8 [Q-Treffer DIN, A]. Zuschnitt kleiner als eine Tafel über die Zuschnittshändler; Rollen zum Zylinder beim Metallbauer |
| PVC-U-Klebefitting Reduktion kurz 40 × 25 | Beet-Auslauf (L03, R51) | [Weinmann-Schanz (DE) 93 049 64](https://weinmann-schanz.de/de/de/Installation/Rohrsysteme/Klebefittinge-aus-PVC-U/PVC-U-Klebfittings/PVC-U-Klebefitting-Reduktion-kurz/PVC-U-Klebefitting-Reduktion-kurz-40-x-25-mm-mit-Klebstutzen-u-Klebmuffe-sid313937.html), Bänninger, Länge 26 mm [Q-Treffer] | [Vanmarcke](https://blue.vanmarcke.com/de_CH/p/20020205) (Shops BE, FR, LU, CH): Georg Fischer D40AG-D25IG, Hersteller-Ref. RV0RCI40C, Bestand und Preis nach Login [Q]; RS Components (BE, UK): Georg Fischer 40 × 25, 26 mm [Q-Treffer] | **beschaffbar** | Baulänge etwa 26 mm (R51 nahm 50 mm [A]); PN nicht geprüft |
| PVC-U-Kugelhahn Klebemuffe d40 | Schlammhahn Absetzer (K07), Ablass Feinfilter | Bevo (NL) VDL Typ EIL d40 DN32 16 bar ([Seite](https://www.bevo.com/en/vdl-ball-valve-pvc-u-40-mm-glue-socket-16bar-dn32-grey-type-eil-7018363?fs=1)) [Q-Treffer] | Bevo Profec Typ 2000 d40 10/16 bar; Profec Safe 600 [Q-Treffer] | **beschaffbar** | Federrückzug (Netz K07) nicht geprüft; Bauteil-Gehäuse D56 gegen Fabrikat prüfen |
| PVC-U-Kugelhahn d63 | Absetzer-Zulauf d63, Auslauf Feinfilter | Bevo (NL) VDL EIL d63 DN50 16 bar ([Seite](https://www.bevo.com/en/vdl-ball-valve-pvc-u-63-mm-glue-socket-16bar-dn50-grey-type-eil-7018365)) [Q-Treffer] | Georg Fischer Typ 546 PRO d63 DN50 PN16 EPDM (eBay.de-Händler) [Q-Treffer] | **beschaffbar** | – |
| PVC-U-Kugelhahn d75 | Heber (K01), Hahn zum Hochschalter (R48) | Bevo (NL) Profec Typ 2000 d75 DN65 10 bar ([Seite](https://www.bevo.com/en/profec-ball-valve-pvc-u-75-mm-glue-socket-10bar-dn65-grey-type-2000-0111382?fs=1)); Praher S6 d75 16 bar [Q-Treffer] | Georg Fischer Typ 546 d75 DN65 (Art. 161 546 108 PN10 laut Datenblatt-Suche; PN-Angaben der Treffer widersprechen sich, 163 546 108 PN16) [Q-Treffer]; R+A (DE) DN65 PN16 [Q-Treffer] | **beschaffbar** | PN vor der Bestellung prüfen; d75 ist bei Bevo nur PN10 belegt |
| Bulkhead-Durchführung PVC-U (Tankanschluss) | Tank-Wand, Beet-Standrohr (D36 im Bauteil), Subtank | [Bevo (NL) VDL Bulkhead 0100543 (40/50 × 1¾″), 0100819 (50/63 × 2″), 7026182 (63/75 × 2½″), 7026183 (75/90 × 3″), 7026181 (20/25 × ¾″)](https://www.bevo.com/en/bulkhead-fitting-pvc-u-40-50-mm-x-1-3-4-glue-socket-glue-spigot-x-male-thread-10bar-grey-0100543), PVC-U, 10 bar, Klebemuffe/Klebestutzen × Außengewinde; 224 Stück im europäischen Zentrallager, Lieferzeit ab 2 Arbeitstage [Q] | Royal Brinkman (NL) Tank-Verschraubung 63 mm × 2¾″; Koi-Breeder PVC-U Teichdurchführung (Galaxus CH); tanksdirekt.de Tankanschluss-Set 63 mm [Q-Treffer] | **beschaffbar** | Dichtung (EPDM) und Wandstärkenbereich stehen nicht auf der Seite; das Beet-Standrohr d25 durch eine Bohrung D36 passt am ehesten zu 25/32 × 1″ (Gewinde rund 33 mm) [A]. Bulkhead d40/d50 für die Absetzer-Einbauten 0100543 bzw. 0100819 |
| Schwimmerschalter | Hoch-Schwimmer Rückstausicherung (R48 4.7, R50), Subtank | Wilo (DE) MS1 mit 10 m Kabel, Datenblatt über solarics.de [Q-Treffer] | Doepke Champ 2 3 m, Leeren/Füllen (elektro-wandelt.de, DE); Wiltec Wechsler 10 m (Kaufland AT) [Q-Treffer] | **beschaffbar** | Kontaktart (Öffner/Schließer/Wechsler), Spannung und Kabellänge hängen an der Steuerung (Netz); Datenblätter nicht gelesen |
| Tauchpumpe 5000 bis 6000 l/h | Subtank M10-S2V (geparkt), kleine Pumpen | Oase (DE) AquaMax Eco Classic 5500: 5300 l/h, 60 W, 2,8 m Förderhöhe [Q-Treffer]; Heissner (DE) Smartline Jet Eco HSP5000-00: 5000 l/h [Q-Treffer] | SunSun CHJ-5000 Eco, 80 W (wiltec.de, DE) und CDF-6000 24 V DC, 40 W (teichtip.de, DE) [Q-Treffer] | **beschaffbar** | Förderhöhe und Feststoffgröße je Fabrikat gegen den Subtank prüfen (M10-S2V); Datenblätter nicht gelesen. Die Pumpenwahl ist nicht Teil von R52 |
| Beutelfilter-Gehäuse (Größe 2, nur Option hinter den Pumpen) | Option Druckseite (R50 1.2) | [Hennlich (AT) Beutelfilter-Gehäuse BFBE](https://www.hennlich.at/fileadmin/user_upload/KATEGORIEN/Beutelfiltergehaeuse/Doppelfilter_LT-BFBES/de_HENNLICH_FestFluessigTrennung_Beutelfiltergehaeuse_BFBE.pdf): Größe 2, AISI 304 oder 316L, DN65, 10 bar [Q-Treffer, Link beim Abruf 404] | Eaton ECOLINE (DE): Größe 04, DN40 BSP; Pentair/Pentek 2″ NPT nur bei eBay (US-Norm) [Q-Treffer] | **nur eine Quelle** (Größe 2) | Die US-Gehäuse aus R50 (PRM, Shelco, Zoro) gelten nach D76 nicht. PP-Gehäuse Größe 2 mit 2″ nicht in Europa gefunden; Edelstahl ersatzweise |
| Filterbeutel PP Größe 2, 100 µm | Option Druckseite; Siebbeutel | Eaton HAYFLOW (DE): PP, 100 µm nominal, 180 × 700 mm; Nordic Filtration: PP Größe 2 ab 7 € [Q-Treffer] | monopoel.de Siebbeutel 100 µm 15 × 25 cm (R50; hier nicht erneut belegt) [Q-Treffer] | **beschaffbar** | Nur nötig, wenn Ben die Druckseiten-Option wählt |
| Fertiger Siebkorb 100 µm, Teichtechnik, 560 × 370 × 400 mm | Feinfilter T55, Subtank D75 | – | – | **nicht beschaffbar in Europa** | Gefunden: Siebkörbe für Beutelgehäuse (AmazonFilters) und Laborsiebe, keine für 560 × 370 × 400; Teich-Bogensiebgewebe nur 300 µm (Aquagart). **Ersatz:** Korb aus Gewebe 100 µm (siehe Zeile 1) auf einem Rahmen aus Lochblech oder Flachstahl (Selbstbau, R50 6.1; „einfache Form“ bleibt) |
| Beet-Siphon-Kit (R51) | Standrohr + Glocke | Ofera (AT), Bell Siphon Kit [Q-Treffer, Seite nicht abrufbar] | – | **nur eine Quelle** (nicht geprüft) | Kein Kauf empfohlen (R51: Selbstbau aus Standardrohren d25/d75); die US-Kits (Aquaponic Source, Desert Aquaponics, Practical Aquaponics AU) entfallen nach D76 |
| PVC-U-Rohre und -Kappen d25, d40, d50, d75, d110 (Standrohr, Glocke, Reinigungsschacht, Leitrohr) | Beet, Absetzer | PVC-U- und KG-Rohre sind Standardkatalog bei Bevo, Weinmann-Schanz und Baumärkten [A, einzeln nicht geöffnet] | – | **beschaffbar** [A] | Nicht Gegenstand der Recherche; Nachweis folgt in N-BESCHAFFUNG (W47) |

**Zählung (von Hand über die Statusspalte, 03.11.2026):** 14 Zeilen; 10 beschaffbar, 2 nur eine Quelle (Beutelgehäuse, Siphon-Kit), 1 nicht beschaffbar (fertiger Siebkorb), 1 beschaffbar nur nach Annahme (Standardrohre). Der Kegelboden-Tank aus Abschnitt 1 ist als 15. Teil **nur eine EU-Quelle** (CGK, Anfrage), dazu eine UK-Quelle (Enduramaxx).

## 3. Stellen, die wegen D76 angepasst werden müssen (nur Liste, nichts geändert)

**R50 (`docs/research/R50-fein-und-vortexfilter.md`)**
- Zeile 12 und 14: „Standardteil ist der Kegelboden-Tank … nur bei US-Händlern“, „Tank als Standard-Kegelboden-Tank beschaffen“: Europa-Quellen (Enduramaxx, CGK) und Status eintragen.
- Zeile 27 und 85: „Gewebe 100 µm Meterware: Aquagart Edelstahlgewebe“: Aquagart nur 300 µm belegt; Riffert, Beissermetall, Teichhansel ergänzen.
- Zeile 28 und 82 bis 83: Beutelgehäuse PRM, Shelco, Zoro (US) entfallen nach D76; Hennlich (AT) und Eaton ergänzen.
- Zeile 96 bis 98: Norwesco 43161, Cone-Bottom 100 gal (Protank, Chemical Containers), Tanks Supply Direct 100-OTCB: US-Zeilen als nicht beschaffbar markieren, europäische Zeilen (Abschnitt 1.1) einfügen.
- Zeile 103 bis 104: „Für Europa fand die Suche keinen Kegelboden-Tank“: durch das Ergebnis aus R52 ersetzen.
- Zeile 124 bis 125: Empfehlung „Kegelboden-Tank PE (100 bis 125 gal)“, „Tank Standard“: Gallonen durch europäische Größen (250 bis 300 l) ersetzen.
- Zeile 158 bis 170 (Spezifikation 6.3, besonders 169): „Alternative Standard-Tank statt Sondermaß“ nennt Tanks Supply Direct 100-OTCB (US) als Alternative; Enduramaxx/CGK-Folge aus Abschnitt 1.3 einfügen; Zeile 170 „Beschaffbarkeit“ mit Quelle.
- Zeile 183 (Belegstand „Kegel-Tanks PE (Norwesco, Chemical Containers)“) und Zeile 191 („Offen: europäischer Kegelboden-Tank-Händler“): schließen.

**R51 (`docs/research/R51-beet-siphon-und-schutz.md`)**
- Zeile 52 bis 62 (Standardsiphon-Tabelle, 4 von 5 Zeilen US/AU), 129: Hinweis „entfallen nach D76“ ergänzen; Zeile 60 (Ofera, AT) bleibt einzige EU-Zeile.
- Zeile 73: Reduktion 40 × 25: Baulänge 26 mm statt R51 Zeile 148 „etwa 50 mm [A]“ (Zeile 148, Tabelle T30e-3).
- Zeile 91 bis 92: Hornbach (DE) ist europäisch; kein Eingriff, nur Quelle prüfen (Suchtreffer).
- Zeile 100: ehorst.de bleibt gültig (europäisch); Lochmaß auf der Seite nicht genannt.

**Bauteilblätter und Doku**
- `docs/parts/tank.md` Zeile 152 („Alternative lokale Fertigung: handelsüblicher Konus-Boden-Tank (Kunststoff, 500-1000 l)“): für den Absetzer 250 bis 300 l; Zeilen 52 und 80 bis 82 (Maße, Ports, Schlammablass d40) und 188 (Plattform/Kegelsitz) betroffen, falls Enduramaxx oder CGK gewählt wird. Das Blatt wird vom Skript `partsheet.py` erzeugt: Änderung an der Quelle `data/components/tank.json`, nicht am Blatt.
- `docs/parts/feinfilter.md` Zeile 163 („Alternative lokale Fertigung: Beutel-/Taschenfilter-Gehäuse oder Siebkorbfilter für Teichtechnik (Edelstahl, 100 Mikrometer Filterbeutel)“): fertiger Siebkorb nicht beschaffbar; Zeile 41, 111, 113 („Fabrikat offen“): Spannverschluss, Durchführungen und Hersteller offen.
- `docs/jobs/M10-S2V.md` Zeile 71 bis 73 („Beschaffbarkeit der neuen Teile“: Siebkorb „Handel: Edelstahl-Siebkorb/Beutelfilter der Teichtechnik (100 um)“): fertiger Korb nicht beschaffbar, Selbstbau aus Gewebe; Subtank PE-Rundtank 500 l: Europa-Nachweis fehlt (nicht Teil von R52).
- `docs/jobs/R50-fein-und-vortexfilter.md` Zeile 19, 20 und 22 (Ergebnis „Standard-Kegelboden-Tank (in Europa nicht gefunden)“, Empfehlung, Offen).
- `docs/jobs/R51-beet-siphon-und-schutz.md` Zeile 19 und 21 (Kits, Ofera/Perth).
- `docs/orchestrator-state.md` Zeile 154 („Absetzer behalten (Kegelboden-Tank als Standardteil)“).
- `docs/pitch-besonderheiten.md` Zeile 21 (B12 „Standard-Kits aus dem Netz sind US-Zoll“): richtig; kein Eingriff, aber B11 (Zeile 20) nennt den Kegelboden-Tank nicht, bleibt gültig.
- `data/roadmap.json` Zeile 1076 („Kegelboden-Tank als Standardteil“), 1098 bis 1103 (der R52-Eintrag selbst): Eigentümer ist der Orchestrator, hier nur gemeldet.
- `docs/hydraulics.md` Zeile 14 und `docs/components.md` Zeile 20: nennen nur Maße aus dem OBJ; Änderung nur, wenn Ben einen Tank wählt.

## 4. Empfehlung und Entscheidungen

| Teil | Empfehlung | Offen |
|---|---|---|
| **Kegelboden-Tank (Absetzer)** | **Enduramaxx 250 l 45° (UK)** als Bezugsquelle, wenn Ben das UK als Europa akzeptiert: Maße und Hydraulik decken sich mit `tank_klein`. Als EU-Quelle daneben **CGK 300 l** anfragen (Kegelwinkel, Höhe, Gestellmaß, Preis). tanksdirekt 200 l nur als Notlösung (1″-Auslauf, 16 min). Beim Bauteil nichts ändern, bis Ben entschieden hat. | DEINE ENTSCHEIDUNG: UK zählt als Europa? Enduramaxx oder CGK? Gestell des Herstellers statt Plattform und Beinen? |
| Siebgewebe 100 µm | Riffert (AT) oder Beissermetall (DE, Anfertigung); Aquagart nur 300 µm | DEINE HANDLUNG: Muster 100 µm bestellen, Rollenbreite klären |
| Lochblech RV 5-8, 1,5 mm | ehorst.de (DE) Tafel oder Zuschnitt | DEINE HANDLUNG: Preis und Lochmaß beim Händler bestätigen |
| Reduktion 40 × 25 | Weinmann-Schanz oder GF über Vanmarcke | ICH: Baulänge 26 mm im Bauteil nachziehen (Werkstatt, nicht hier) |
| Kugelhähne, Bulkheads | Bevo (NL) für d40, d63, d75 und Bulkheads | ICH: Datenblätter lesen (PN, Dichtung, Wandstärke) vor N-BESCHAFFUNG |
| Schwimmer, Pumpen | Wilo oder Doepke; Oase, Heissner oder SunSun | Entscheidung hängt an M10-S2V (geparkt) |
| Fertiger Siebkorb 100 µm | nicht beschaffbar: Korb aus Gewebe und Rahmen selbst bauen (bleibt „einfache Form“, R50) | DEINE ENTSCHEIDUNG: nur falls Ben einen fertigen Teichfilter will (Trommelfilter, R50 Option B) |
| Beutelgehäuse | nur Option; Hennlich (AT) Edelstahl | keine, solange Option B nicht gewählt |

## 5. Belegstand und Grenzen
- Selbst gelesen [Q]: Enduramaxx Herstellerseite und Kingfisher-Seite, CGK 300 l, tanksdirekt 200 l, ehorst Lochblech (Lochmaß dort nicht angegeben), Vanmarcke GF 40 × 25, Bevo Bulkhead-Seite.
- Nur Suchergebnis [Q-Treffer]: Riffert-Seite (Zertifikatsfehler beim Abruf), Kugelhähne (Bevo, GF-Datenblatt-PDF war nicht lesbar), Weinmann-Schanz 93 049 64 (Seite beim Abruf 404, Inhalt aus der Suchzusammenfassung), Hennlich (Link beim Abruf 404), Pumpen und Schwimmerschalter (Datenblätter nicht gelesen), Oase-Seite nicht geöffnet. Preise: keine erhoben, nur der UK-Listenpreis des Tanks (344 £ ohne MwSt, Händler).
- **Nicht belegt:** ob Enduramaxx oder CGK in EU-Festlandländer liefern und zu welchen Bedingungen; Kegelwinkel und Wandstärke von CGK; Wandstärke von Enduramaxx; Randwulst; ob die 1000-mm-Gewebrolle 100 µm lieferbar ist; PN der Kugelhähne d75.
- Suchwerkzeug: nur die Websuche des Werkzeugs (Treffer teils US-lastig); Händlerseiten in Polen, Italien, Spanien, Frankreich lieferten für Kegelboden-Tanks 200 bis 300 l keinen Treffer.

**Geprüft gegen:** `docs/research/R50-fein-und-vortexfilter.md` (0, 2, 3, 6), `docs/research/R51-beet-siphon-und-schutz.md` (Teileliste, Spezifikation), `docs/parts/tank.md`, `docs/parts/feinfilter.md`, `docs/decisions.md` D76, `docs/arbeitsweise-sitzungen.md` Abschnitt 4; Herstellerseite Enduramaxx, Händlerseiten Kingfisher Direct, CGK, tanksdirekt.de, ehorst.de, Vanmarcke, Bevo; Rechnung `scripts/r52_rechnung.py`.
**Offen:** (DEINE ENTSCHEIDUNG) UK als Europa zulassen; Enduramaxx 250 l oder CGK 300 l für den Absetzer; Gestell des Herstellers; (DEINE HANDLUNG) CGK und einen UK-Händler fragen (Versand nach Deutschland, Zoll, Kegelwinkel, Wandstärke, Preis); Gewebe-Muster 100 µm und Lochblech beim Händler bestätigen; (ICH) Datenblätter Bevo, Wilo und GF lesen, Werkstatt-Folge am Bauteil nach Bens Wahl, Beschaffbarkeits-Nachweis N-BESCHAFFUNG.
