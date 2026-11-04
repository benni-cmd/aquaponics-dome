# Work package: N-MODELL-KOMPLETT Platzhalter im Gesamtmodell durch genaue Bauteile ersetzen

**Problem:** Streben stehen im Modell als Rundstab (`strut_r` 45, Quelle "Platzhalter"), die Einkaufsliste fuehrt Vierkantrohr 30 x 30 (`PRF-st-strebe30x30`); Bauteile tragen Werkstoff `Default`. Die Tuer-Klinke fehlt im Viewer, obwohl `tuer_komplett` (27 Koerper) eingebaut ist: Kleinteile unter `MIN_DIAG` 150 werden nicht exportiert (12 von 27 Koerpern in der OBJ).
**Intent:** Alle Bauteile genau im Modell, damit Detailansicht, Einkaufsliste und das gemeinsame Ausfuell-Artefakt (W65) auf dem echten Modell stehen (Ben, W63).
**Goal:** Streben als Vierkantrohr 30 x 30 x 3 mit Rollwinkel zu den Steckarmen, Achsen/Knoten/Folie/Tuer unveraendert; Tuer mit Klinke im Viewer; kein eingesetztes Bauteil mit Werkstoff `Default`; Einkaufsliste ohne `platzhalterkoerper`. Blatt: `docs/jobs/N-MODELL-KOMPLETT.md`

## Plan
1. [x] Werkstatt A (04.11., a2efae2): Inventur-Skript `scripts/model_inventar.py`, `docs/model-inventar.md`
2. [ ] Werkstatt B: Strebe als Vierkantrohr (`scripts/components/strebe.py`, Parameter, Bauteilblatt, `data/parts`)
3. [ ] Montage (nach M10-S5-LUFT, einzige Modell-Schreibsitzung): `place_struts` mit Rollwinkel, `strut_r` aus Basisringhoehe entkoppeln, `dome.sc` neu bauen
4. [~] Werkstatt C (04.11.): `tuer.sc` gekennzeichnet (erledigt); Werkstoffe: Skript `scripts/workshop/default_werkstoffe.py` fertig und auf Kopien geprueft, Anwendung nach Modell-Build durch Montage, `check_parts.py`
5. [ ] Viewer: Kleinteil-Ausnahme in `export_model.py`, Screenshot Tuer und Strebe
6. [ ] `bom.py` und `check_bom.py` nachziehen
7. [ ] Pruefer: `docs/jobs/pruefung/N-MODELL-KOMPLETT.md` nach fuenf Pruefpunkten
8. [ ] Orchestrator: Roadmap nachfuehren, W65 (Ausfuell-Artefakt) freigeben

Reihenfolge: 2 und 5 duerfen vor Schritt 3 laufen (kein `dome.sc`-Neubau); 3 nach M10-S5-LUFT; 6 nach 3 und 4; 7 zuletzt.

## Stand
04.11.2026, Planer (Sonnet 5.5): Blatt geschrieben, Aktualitaet **angepasst**. Zwei Korrekturen am Auftragstext: (1) die genaue Tuer ist schon eingebaut, die Klinke fehlt nur im Export (`export_model.py:14`); (2) Strebenumbau hat Zusatzfolgen: Rollwinkel und `strut_r` in `gen_dome.py:250` (Basisring sonst 30 mm tiefer). Werkstoff-Zahl 39 nicht reproduziert, Schritt 4 misst neu. OFFEN (Ben): Wandstaerke 3 mm bis N-STATIK (Empfehlung 3 jetzt); `tuer.sc` loeschen oder kennzeichnen (Empfehlung kennzeichnen).

## Stand 04.11.2026 Werkstatt A+C (Schritte 1 und 4)
- **Schritt 1 erledigt:** `python -X utf8 scripts/model_inventar.py` Exit 0 (Lauf ca. 50 Min, eval einzeln mit 90-s-Grenze, Zwischenspeicher in `%TEMP%`). `docs/model-inventar.md`: 164 Definitionen, 4914 Instanzen, 316 `.sc`, davon 152 ohne Instanz. Nicht ausgewertet (eval ueber 90 s): `nft_tisch_aussen`, `nft_tisch_mitte`, `tank_gross`, `tank_gross_t3`, `ibc_beet_aussen_993`, `luftverteiler_6`.
- **Tuer:** `tuer` (T4) als abgeloest gekennzeichnet (`docs/parts/tuer.md`, `data/parts/tuer.json` Feld `abgeloest`); Einkaufsliste zaehlt sie nicht (`SON-tuer-modellvariante` Bedarf 0, `nicht_platziert`, Hinweis `altmodell`); `check_parts.py tuer` 21/21.
- **Werkstoffe, gemessen:** eingesetzte Komponenten mit `Default` ausser Ausnahmeliste: **8** (Messbefehl: `python -X utf8 scripts/model_inventar.py`, letzte Zeilen): `fundamentring`, `pool_zentral`, `zweitbecken`, `zulaufrohr`, `schaltschrank` (alle in `scripts/gen_dome.py` inline gebaut, `component_file` setzt keinen Werkstoff), `strebe_a`, `strebe_b` (Schritt 2, `scripts/components/strebe.py`), `nft_tisch_innen` (6 Koerper Rinnenprofil/Kappen; Tische-Sitzung, `scripts/workshop/nft_tisch.py`). Die Zahl 39 des Auftrags ist damit ersetzt durch 8 (plus 6 Komponenten nicht ausgewertet).
- **Nicht erreicht:** Soll 0. Grund: Die fuenf inline-Komponenten werden bei jedem Build von `gen_dome.py` neu geschrieben und tragen dort keinen Werkstoff; `gen_dome.py`, `build.sh` und die fremd geaenderten `.sc` sind laut Auftrag tabu. Loesung bereit: `python -X utf8 scripts/workshop/default_werkstoffe.py --apply` weist Beton, PE Tank [A], PVC grau [A], Wasser, Stahl verzinkt [A] zu (auf Kopien geprueft, alle Koerper danach ohne Default). Die Montage ruft es nach `gen_dome.py` auf (oder uebernimmt die Zuordnung in `component_file`). Pool-/Zweitbeckenwerkstoff PE ist Platzhalter bis R32.
- **check_parts, gemessen 04.11. 12:35:** `python -X utf8 scripts/workshop/check_parts.py` Exit 0, 308 Komponenten, 0 FAIL, Teile offen fuer 5a: 43 (fremde Gruppen).
- **Folgen fuer andere Sitzungen:** Strebe (Schritt 2) setzt `Stahl verzinkt` selbst; Tische-Sitzung setzt Werkstoff fuer `nft_tisch_innen` Rinnenprofil/Kappen (Katalog: `PVC grau Beet`) und prueft die Tische aussen/mitte.

## DoD
Dateien aus dem Blatt vorhanden; fuenf Pruefpunkte vom Pruefer gemessen; Screenshot Tuer mit Klinke und Streben-Nahansicht gegen `docs/ui-standard.md`; Vorher/Nachher-Werte (Basisknoten-Z, defs-Summe) im Paket; Entscheidungen in `docs/decisions.md`; Commit und Push je Teilschritt.
