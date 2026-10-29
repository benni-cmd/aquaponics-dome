# Modellbeschreibung: Aquaponik-Kuppel (lebendes Dokument)

Besitzer: Orchestrator. Waechst mit jeder Abnahme und wird dabei genauer. Zweck: anderen zeigen koennen, was das Modell berücksichtigt, wie genau es ist, was wir daraus gelernt haben und wo seine Grenzen liegen. Kennzahlen kommen aus dem Repo (`python scripts/build_model_description.py`), alles andere pflegt der Orchestrator mit Datum und Beleg.

## 1. Kennzahlen (automatisch)
<!-- KENNZAHLEN-START -->
| Kennzahl | Wert |
|---|---|
| Stand | 29.10.2026 21:36 |
| Komponenten-Definitionen (`designs/components/*.sc`) | 134 |
| Bauteilklassen (grob nach Dateiname) | 35 |
| Bauteilblaetter mit Herkunftstabelle (`docs/parts/*.md`) | 17 |
| Entscheidungen (`docs/decisions.md`) | 31 |
| Recherchen (`docs/research/R*.md`) | 7 |
| Pruefskripte (`scripts/check_*.py`, `scripts/workshop/check_*.py`) | 13 |
| Pruefbilder im Verlauf (`renders/history`) | 180 |
| Commits | 157 |
| Erster / letzter Commit | 29.10.2026 01:04 / 29.10.2026 21:36 |
<!-- KENNZAHLEN-ENDE -->

## 2. Was gebaut wird
Ein parametrisches SolidCraft-Modell einer Geodaetischen Kuppel (12 m Durchmesser, 2V-Halbkugel, hoechster Punkt 6 m) mit einem Aquaponik-System im Inneren: Fischbecken (Pool), zwei Ringe Substratbeete, drei Ringe NFT-Rinnen ueber den Beeten, vier Tanks mit Pumpen, Tuer, Rohre und Schlaeuche. Phase **reines Modell**: nur Geometrie, Anzahlen, Masse und Verbindungen; Fischart, Standort, Biologie, Elektrik, Betrieb, Preise und Statik sind bewusst noch nicht Teil (Ben, 29.10.).
Jedes wiederkehrende Bauteil ist eine **Komponente**: eine Definition, viele Instanzen. Eine Aenderung an der Definition wirkt ueberall.

## 3. Quellen und ihre Rangfolge
1. **Ben** (Aussagen im Chat, seine Tabelle `reference/Kuppelberechnung-neu-2.xlsx`).
2. **OBJ-Zahlen** aus Bens SketchUp-Layout (`data/layout.json`, 14 Beete, 4 Tanks, Pool, Tische, 2160 Toepfe).
3. **Bilder** (`reference/ref-4-dome-clean.jpg` als Hauptbild fuer das Aussehen).
4. Recherche mit mindestens zwei unabhaengigen Quellen, sonst als Annahme markiert.
Jede Zahl im Bauteilblatt traegt eine Herkunftsmarke: **Q** (Quelle), **E** (aus OBJ/Messung abgeleitet), **A** (Annahme). Annahmen sind sichtbar und umkehrbar (`docs/decisions.md`, Spalte Rueckgaengig).

## 4. Geometrie-Grundlagen
- Kuppel 2V, Radius 6000: Streben A 3279 mm (0,5465 R, 30 Stueck), B 3708 mm (0,618 R, 35), Profil 30 x 30 (OBJ-Treue; die Statik wuerde ein groesseres Profil verlangen, D09). Knoten als Kugel mit 4/5/6 Steckarmen (D15, Recherche R02), Fundamentanker an den 10 Basisknoten.
- Boden: kein fester Boden, Erdoberflaeche mit eingelassenem Pool und eingelassenen Beeten (D13).
- Tuer: Normtuer 1000 x 2000, im Basisdreieck mit Scheitel Z 3150 (R13); Azimut 167 im OBJ (D02).
- Die drei NFT-Ringe sind regelmaessige Zehnecke (Seite = 2 x Apothem x tan 18 Grad); das OBJ zeigt je Ring nur ein Beispiel, die Ringe sind daraus abgeleitet (D04).

## 5. Bauteile und Pruefstand (von Hand, mit Datum)
| Klasse | Stand | Pruefung | Datum |
|---|---|---|---|
| Netztopf, Salatkopf | Salatkopf Rev. B2 (96 Blaetter, ca. 8,8k Dreiecke statt 69k) | check_pflanze 18/18, Bild-Kritiker Runde 5 | 29.10. 21:30 |
| NFT-Rinne (3 Laengen + Reihenvarianten) | abgenommen | Vorpruefung 93/93 | 29.10. |
| NFT-Tisch innen/mitte/aussen | Rev. C (W17): Radialbudget, `corner_gap` 60 (Annahme der Werkstatt), 586 Rinnenpflanzen bei Lochabstand 200 mm (D32/D33, W18), Winkelhalter (W11) | check_nft_fit 42/42 (selbst nachgemessen, inkl. Laufweg A >= 500), check_nft_tisch 196/196; Spec-Pruefer W17+W18 gelaufen, Befunde eingearbeitet | 30.10. 00:10 |
| IBC-Beet aussen/innen | Aussenbeet 800 breit (D29, W17), Innenbeet 933 | Vorpruefung 66/66 (alt), neue Parameter in check_nft_fit | 29.10. 21:30 |
| Tank klein (Vortex), gross (Biofilter) | abgenommen, 45-Grad-Kegel ab Plattform (R09) | check_tank 60/60 | 29.10. |
| Pumpe (4 Tafeln) | abgenommen nach 4 Pruefrunden | check_pumpe 34/34 | 29.10. |
| Knoten 4/5/6 (26 Dateien), Fundamentanker | abgenommen | 135/135 bzw. 15/15 | 29.10. |
| Leitungsteile (Rohr, Bogen, T, Kugelhahn, Schlauch, Verteiler, 63 Dateien) | gebaut, Sammelblatt | check_leitungsteile 231/231 (Volumen nach Pappus) | 29.10. |
| Gesamtmodell `designs/dome.sc` | Beete, Tanks, Pumpen, Knoten, Anker, 24 Tische, Toepfe als Instanzen; M7 Radialbudget als WIP (D30, D31) | check_latte Runde 39: 21/24 (WIP), check_walkways: Laufweg B 476 mm gegen Ziel 600 (Minimum 500) | 29.10. 21:35 |
| Haut-Paneele (T40) | 40 Dreiecke, 2 Typen (AAB, BBB), Doppelstegplatte 8 mm, Rand 15 mm vor der Strebenachse, Alu-Kappe 30 x 8 als Randprofil (W19, noch nicht im Gesamtmodell) | check_haut 27/27 (nachgemessen), Spec-Pruefer und Bild-Kritiker fehlen | 30.10. 00:00 |
| Tuer, Rohrnetz | offen | - | - |

## 6. Wie genau ist das Modell?
- **Anzahlen** stimmen mit Bens OBJ und Tabelle ueberein: 14 Beete (8 x 2953, 6 x 1865), 4 Tanks, 24 NFT-Tische, 2160 Beetpflanzen (Tabelle verlangt mindestens 152) und 586 Rinnenpflanzen (Tabelle verlangt mindestens 459). Die NFT-Mindestzahl ist die bindende Grenze.
- **Positionen** folgen dem OBJ; dessen Beetlage ist nur auf etwa 100 mm genau (D21), Tankplattformen ueberlappen dort teils (D22).
- **Bauteile** sind nach Herkunftstabelle gebaut, Volumina per Pappus und Port-Stirnflaechen geprueft; jede Klasse lief durch einen Bild-Kritiker und einen Spec-Pruefer mit getrennten Rollen, nicht durch den Bauer selbst.
- **Grenzen:** keine Statik, keine Hydraulik-Rechnung, keine Bewegungs-/Erreichbarkeitssimulation; Erreichbarkeit nur mit einfachen Regeln (D29). Annahmen (A) sind im Blatt gekennzeichnet.

## 7. Was berücksichtigt wurde (Auswahl)
Wiederkehrende Teile als Komponenten (D12) · Zickzack-Pflanzmuster (Phase A/B der Rinnen) und Rinnengefaelle 1,5 % (R06) · Kegelboeden und Anschluesse der Tanks (R09, Fittings als Ports) · Rohre vergraben oder auf der Erde (D14) · Kollisionsfreiheit zwischen Instanzen (Prüfskript, Bens Fund) · Laufwege mindestens 600 mm, Tuer-Gang 900 mm, Erreichbarkeit (D28, D29) · Mindestzahl Pflanzen aus Bens Tabelle (D27) · Pool nach Bens Tabelle Ø4,0 x 2,2 m (D26) · Viewer-Export ohne Datenflut (31 MB statt 320 MB).

## 8. Was wir daraus gelernt haben
- **Einzelpruefung reicht nicht.** Jede Komponente war fuer sich in Ordnung, erst das Zusammenstellen zeigte Kollisionen: Rinnen laenger als die Zehneck-Seite (4 von 6 Reihen), Tischbeine im Substrat, Beete an der Domwand ohne Platz fuer Tischboecke, Tankplattformen die sich ueberlappen. Bens Blick auf ein Bild fand, was die Pruefungen nicht fanden; seither prueft die Latte Instanzen gegeneinander.
- **Ein Beispiel im OBJ ist kein Ring.** Das OBJ zeigt je NFT-Typ ein Muster; erst die Zehneck-Rechnung machte daraus Ringe.
- **Zahlen aus Bens Tabelle schlagen eigene Ableitungen** (Pool 2,2 statt 2,34 m).
- **Raum ist das knappe Gut:** Vom Beckenrand bis zur Domwand sind es 3611 mm; zwei Beetportale, zwei Laufwege und Wandluft fuellen sie fast voll (D28/D29).
- **Prozess:** getrennte Rollen (Bauen, Montieren, Pruefen), kleine Auftragsblaetter statt langer Leselisten, Zustand im Repo statt im Kopf, Kontext sparen durch Leeren nach sauberem Abschluss, Limit-Regeln. Genaue Messwerte: Viewer-Modell 320 MB auf 32 MB; Leseliste der Werkstatt 73 KB auf ein Blatt.

## 9. Offen und naechste Praezisierungen
Tuer komplett (M3) · Rohrnetz aus dem Wasserweg-Graphen (M4, M5) · Laufwege-Umbau (M7, W17) · Haut/Paneele (R11) · vollstaendige Kollisionspruefung · Pflanzenartmodelle (7 Arten laut Tabelle, bewusst hinten) · Fragen an Ben: Innenring 6 oder 10 Tische, Zuchtbecken gleich zweites Becken, 2 oder 4 Pumpen, 2 oder 3 Rinnen je Aussentisch.

## 10. Verlauf (neueste zuerst)
- 30.10. 00:00 Werkstatt W19: Kuppelhaut als Komponenten (40 Dreiecke, 2 Typen, Randprofil), Recherche R11; Becken wird zentriert, Zickzack bleibt (D35).
- 29.10. 23:55 Werkstatt: gemeinsamer Pruefer W17+W18, Laufweg A am Innenpfosten von 486 auf >= 500 mm (Parameter `leg_clearance_innen`), check_nft_fit 42/42.
- 29.10. 22:40 Werkstatt W18: Lochabstand der NFT-Rinnen 250 auf 200 mm (Recherche R16), Rinnenpflanzen 462 auf 586, Gesamt 2746 Pflanzen-Toepfe; check_nft_fit 40/40.
- 29.10. 22:20 Viewer: Bauteile als einklappbare Gruppenliste mit Zaehlern (24 NFT-Tische, 5252 Pflanzenteile, ...), Ein-/Ausblenden je Gruppe und Einzelteil, Hover und Klick leuchten durch andere Koerper (`viewer/index.html`).
- 29.10. 21:35 Auslaufen wegen Wochenlimit (93 %): W07, W11, W17 gepusht, M7 als WIP gepusht; Arbeitsbaum sauber, alles auf GitHub (Commit 8eebd21). Offen: Laufweg B 476 mm statt 600, Spec-Pruefer W17, Tuer, Rohrnetz.
- 29.10. 20:30 Beschreibung angelegt. Stand: 133 Komponentendateien, Bens Tabelle ausgewertet (R15), Laufwege-Regeln D28/D29, Wochenlimit-Regel.
- 29.10. 19:20 Montage M1.4: 24 Tische Rev. B und 466 Rinnenpflanzen im Gesamtmodell.
- 29.10. 17:15 Werkstatt W16 NFT-Tisch-Passung nach Bens Kollisionsfund; Viewer von 320 auf 32 MB.
- 29.10. 12:30 Montage M1.1/M1.2: Beete, Tanks und Pumpen als Instanzen.
- 29.10. 01:04 Projekt angelegt, erste Kuppel aus Referenzbildern, OBJ-Auswertung.
