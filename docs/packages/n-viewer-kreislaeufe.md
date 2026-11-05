# N-VIEWER-KREISLAEUFE: Ebenen-Schalter für Wasser, Luft und Strom im Viewer

Stand 05.11.2026, Viewer-Sitzung. Wunsch W87 (`docs/packages/wunschbuch-ben.md`). Status: gebaut und belegt; Deploy wartet auf den Orchestrator.

## PIG
- **Problem:** Im Viewer liegen Wasserleitungen, Luftschläuche und Kabel dicht beieinander. Ben und Leon können einen Kreislauf nicht einzeln verfolgen. Es gibt nur den einen Schalter "Messstellen zeigen".
- **Intent:** Ben und Leon prüfen im Viewer (lokal und auf Vercel), wo jedes Wasser-, Luft- und Stromsystem läuft, ohne die anderen Teile im Weg zu haben.
- **Goal:** Im Menü stehen drei kombinierbare Schalter "Wasserkreislauf", "Luftkreislauf" und "Stromkreislauf". Ein eingeschalteter Schalter hebt die Leitungen, Schläuche, Kabel und die zugehörigen Teile farbig hervor, alle anderen Teile werden blass. Die Zuordnung jedes Teils kommt aus den Daten (`viewer/ansicht.json`, `data/leitungsnetz.json`, `data/leitungstrassen.json`, `data/parts`), nicht aus einer Handliste im Viewer. Das gilt für A+ und Ring B2. Die Desktopansicht ist sonst unverändert; mobil gibt es die Schalter einfach im Menü.

## Entwurf
1. **Datenquelle:** `viewer/export_ansicht.py` schreibt in `ansicht.json` ein neues Feld `kreislauf`. Jede Variante bekommt es beim eigenen Export (`export_model.py` und `serve.py` rufen das Skript schon auf). Der Viewer liest nur dieses Feld.
2. **Zuordnung je Teil, in dieser Reihenfolge:**
   - Rohre, Bögen, Hähne und Co. (`lt_*`): die Leitungsart der Instanz aus `leitungsart` (Zulauf, Rücklauf, Frischwasser = Wasser; Luft = Luft). Fehlt sie (Abstand zur Trasse über 150 mm), entscheidet das Feld `linie` des nächsten Eintrags in `leitungstrassen.json` (`teile`): `luft` und `luft_b` = Luft, Zahl = Wasser, `frisch` = Wasser.
   - Tanks, Pumpen, Filter und andere Bauteile: die Knoten in `leitungsnetz.json` (`bauteil` oder `id` passt zum Teilenamen). Hängt der Knoten an einer Kante mit Medium Wasser, ist das Teil Wasser; bei Medium Luft zählt nur der Quellknoten (Gebläse), die belüfteten Becken bleiben Wasser.
   - Strom: die Kabelliste in `leitungsnetz.json` (Medium Strom: Schaltschrank, Pumpen, Gebläse, Puffer, Steuerung) und im Teile-Datensatz jeder Körper mit Werkstoff `kabel_pvc` oder Namen "Kabel", "Netzkabel", "Stecker" (Pumpenkabel sind einzelne Körper).
3. **Darstellung:** Schalter an, dann bekommen alle Körper ein blasses, durchsichtiges Material. Die Teile des gewählten Kreislaufs liegen als farbige Kopie darüber (Wasser blau, Luft hellgelb, Strom orangerot (W87a)), Tiefentest an, damit Formen lesbar bleiben. Mehrere Schalter ergeben die Vereinigung. Bauteilbaum, Auswahl und Schnitt-Regler wirken weiter (versteckte Teile bleiben versteckt, der Schnitt gilt auch für die Kopie).
4. **Mobil:** die drei Schalter stehen im Menü (einfache Kontrollkästchen), kein Zusatzaufwand.
5. **Grenzen, ehrlich:** Messstellen-Halter und Sonden gehören zu keinem der drei Kreisläufe (sie haben ihre eigene Ebene). Teile ohne Datenbezug (Fundament, Kuppel, Hülle, Pflanzen, Tische) gehören zu keinem Kreislauf und sind bei jedem Schalter blass.

## Plan
1. [x] Bestand lesen (`viewer/index.html`, `export_ansicht.py`, `leitungsnetz.json`, `leitungstrassen.json`, `data/parts`)
2. [x] Paket anlegen
3. [x] `export_ansicht.py`: Feld `kreislauf` je Variante, Zählung ausgeben
4. [x] `ansicht.json` beider Varianten neu schreiben, Zählung gegen die Daten prüfen
5. [x] Viewer: drei Schalter, blasse Welt, farbige Ebene, Zähler und Kurzinfo
6. [x] Mobil: Schalter bleiben im Menü
7. [x] Screenshot je Schalter (Wasser, Luft, Strom, kombiniert) im Browser-Pane, A+ und Ring B2, gegen `docs/ui-standard.md`
8. [x] `python -X utf8 scripts/viewer_dist.py` laufen lassen und die statische Ausgabe testen
9. [x] Paket nachführen, Wunschbuch W87 auf "gebaut" setzen, Commit per Pfad, Push

## Nachtrag W87b (05.11.2026): Tische und Beete nicht im Wasserkreislauf
Der Wasserschalter hebt die NFT-Tische (`nft_tisch_*`) und Substratbeete (`ibc_beet_*`) selbst nicht mehr hervor, nur ihre Zuläufe, Abläufe und Siphons. Regel in `export_ansicht.py`: Für Teile der Bauteilgruppe "Tische und Beete" gilt Wasser nur für einzelne Körper, nämlich Werkstoff `pvc_u` oder `pvc_p_schlauch` oder ein Name mit zulauf, ablauf, siphon, glocke, standrohr, bulkhead, sammelrohr, verteiler, tropfrohr. Beispiele: Verteiler, Schläuche, Sammelrohr, KappeZulauf, KappeAblauf (Tische); Bulkhead, Standrohr, Glocke, Tropfrohr (Beete). Wanne, Siebboden, Medium, Stützen, Rinnenprofil, Beine bleiben blass. Der Viewer liest dafür das Feld `koerper` mit Kreislauf-Liste (vorher nur Strom). Beleg: Screenshot Draufsicht A+ nur Wasser, Tische und Beete blass; `koerper` enthält 5 Definitionen, `stamm` Wasser nur noch 13 statt 18 (`python -X utf8 viewer/export_ansicht.py`).

## Messung (Browser-Pane, lokaler Server `viewer/serve.py 4431 --kein-export` und statische Ausgabe auf Port 4432, 05.11.2026)
Alle Zahlen kommen aus `python -X utf8 viewer/export_ansicht.py [--variante ring_b2]` (Zeile `kreislauf:`) und aus `window.kreisStand()` im Viewer; beide stimmen überein.

| Größe | A+ | Ring B2 |
|---|---|---|
| Wasserteile (Rohre, Tanks, Pumpen, Filter, Tische, Beete) | 451 (mit Kleinteilen; 291 ohne, 160 Teile unter 15 cm sind erst mit dem Haken geladen) | 388 |
| Luftteile (Schläuche, Verteiler, Belüfter, Gebläse) | 154 (66 ohne Kleinteile) | 154 |
| Stromteile (Schaltschrank, Pumpen, Gebläse, Puffer, Schrankeinführung) | 13 | 17 |
| Rohrteile ohne Zuordnung | 6 | 183 |
| Definitionen mit fester Zuordnung (`stamm`) | 21 | 21 |

- Hervorgehoben werden nur die Teile des Kreislaufs, alle 692 (A+) oder 1037 (Ring) Körper werden blass (`kreisStand().blass`).
- Der Baum wirkt weiter: "Tanks und Pumpen" ausblenden senkt die farbigen Kopien von 460 auf 366, Einblenden bringt 460 zurück.
- Der Haken "Kleinteile" lädt die Teile unter 15 cm nach; die Wasserzählung steigt dann von 291 auf 451 und der Hinweis verschwindet.
- Der Zustand der drei Schalter bleibt nach dem Neuladen erhalten (`localStorage`, Schlüssel `viewer.kreis.*`).

## Belege
- Screenshots im Browser-Pane (Desktop, Draufsicht, A+): Wasser allein (Pool, Tanks, Tische, Beete, Rohre blau, Rest blass), Luft allein (hellgelbe Schläuche, vier Belüfter, Gebläse), Strom allein (orangerote Schaltschrank, Pumpen, Puffer, Gebläse), alle drei zusammen.
- Screenshot Ring B2 mit allen drei Schaltern: gleiche Farben, Ring-Pool und Ring-Schaltschrank werden erkannt.
- Screenshot Mobil (375x812, `?mobil=1`): die drei Schalter stehen im Menü, der Satz zur Hervorhebung ist lesbar, kein Bauteilbaum.
- Statische Ausgabe: `python -X utf8 scripts/viewer_dist.py` lief durch (906 OBJ-Dateien, 182,8 MB, 1553 Dateien, 165 s). `viewer/dist/index.html` enthält die Schalter, beide `ansicht.json` das Feld `kreislauf`. Im statischen Viewer (Python-Server auf `viewer/dist`) laden 273 Definitionen in 15 s, alle drei Schalter arbeiten.
- `git diff --stat viewer/index.html`: 73 Einfügungen, 6 Löschungen, nur die Ebene und ihre Anbindung. Der Desktop-Aufbau ist sonst unverändert.
- `docs/ui-standard.md`: Sätze statt Fragmenten (Hinweis unter den Schaltern), kein Unicode-Symbol, keine verbotenen Wörter, optische Abnahme per Screenshot. Die Dashboard-Bausteine `HD.*` gelten für das Dashboard, nicht für den Viewer.

## Grenzen
- Ring B2: 183 Rohrteile (zum Beispiel `lt_klemme_d75`, `lt_bogen90_d50`) haben noch keine Trasse in `leitungstrassen.json` und bleiben bei jedem Schalter blass. Ring-Formteile (`ring_ecke_d75`, `ringstuetze_d75_b`, `ring_abzweig_d40`) haben keine Bauteilgruppe in `data/parts`; sie bekommen ihre Zuordnung, sobald die Montage ihre Trassen schreibt, ein neuer Export (`export_model.py` ruft `export_ansicht.py`) reicht.
- A+: 6 Rohrteile (`lt_kugelhahn_d50` 2, `lt_rohr_d50_L72` 4) liegen weiter als 150 mm von jeder Trasse und haben keinen Eintrag in `teile`.
- Strom: Kabel sind im Modell nur als Pumpenkabel und Netzkabel vorhanden, keine verlegten Kabeltrassen. Der Stromkreislauf zeigt deshalb die Verbraucher (Schaltschrank, Pumpen, Gebläse, Puffer), nicht den Kabelweg. Die Kabelliste in `leitungsnetz.json` hat keine Geometrie.
- Teile ohne Datenbezug sind bei jedem Schalter blass: Schwimmerventil im Pool, Fundament, Kuppel, Hülle, Pflanzen, Messstellen-Halter und Sonden (eigene Ebene).
- Das Gebläse und die Pumpen gehören zu zwei Kreisläufen; bei mehreren Schaltern gewinnt die seltenere Farbe (Strom vor Luft vor Wasser), gezählt wird jedes Teil in beiden.
- Nicht auf einem echten Handy geprüft, nur im Pane (375x812).

## Status
05.11.2026: gebaut, lokal und statisch belegt. Geändert: `viewer/index.html` (Schalter, blasse Welt, farbige Ebene), `viewer/export_ansicht.py` (Feld `kreislauf`), dieses Paket, Wunschbuch W87. `ansicht.json` ist nicht im Repo (`.gitignore`); `serve.py` und `export_model.py` erzeugen sie beim nächsten Export neu. Deploy: gehört dem Orchestrator, `viewer/dist` ist frisch gebaut.

## Definition of Done
Geprueft gegen: Screenshots der drei Schalter einzeln und kombiniert (A+ und Ring B2, Mobil), Zählung je Kreislauf aus `window.kreisStand()` gleich der Ausgabe von `export_ansicht.py`, `python -X utf8 scripts/viewer_dist.py` (statische Ausgabe getestet), `git diff --stat viewer/index.html`
Offen:
1. Deploy auf Vercel — Orchestrator
2. Ring B2: 183 Rohrteile ohne Trasse, Ring-Formteile ohne Gruppe — Montage Ring (neuer Export genügt)
3. Stromkreislauf zeigt Verbraucher, keinen Kabelweg (keine Kabelgeometrie im Modell) — DEINE ENTSCHEIDUNG, ob Kabeltrassen modelliert werden sollen
