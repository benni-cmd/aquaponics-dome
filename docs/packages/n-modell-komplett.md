# Work package: N-MODELL-KOMPLETT Platzhalter im Gesamtmodell durch genaue Bauteile ersetzen

**Problem:** Streben stehen im Modell als Rundstab (`strut_r` 45, Quelle "Platzhalter"), die Einkaufsliste fuehrt Vierkantrohr 30 x 30 (`PRF-st-strebe30x30`); Bauteile tragen Werkstoff `Default`. Die Tuer-Klinke fehlt im Viewer, obwohl `tuer_komplett` (27 Koerper) eingebaut ist: Kleinteile unter `MIN_DIAG` 150 werden nicht exportiert (12 von 27 Koerpern in der OBJ).
**Intent:** Alle Bauteile genau im Modell, damit Detailansicht, Einkaufsliste und das gemeinsame Ausfuell-Artefakt (W65) auf dem echten Modell stehen (Ben, W63).
**Goal:** Streben als Vierkantrohr 30 x 30 x 3 mit Rollwinkel zu den Steckarmen, Achsen/Knoten/Folie/Tuer unveraendert; Tuer mit Klinke im Viewer; kein eingesetztes Bauteil mit Werkstoff `Default`; Einkaufsliste ohne `platzhalterkoerper`. Blatt: `docs/jobs/N-MODELL-KOMPLETT.md`

## Plan
1. [ ] Werkstatt A: Inventur-Skript `scripts/model_inventar.py`, `docs/model-inventar.md`
2. [ ] Werkstatt B: Strebe als Vierkantrohr (`scripts/components/strebe.py`, Parameter, Bauteilblatt, `data/parts`)
3. [ ] Montage (nach M10-S5-LUFT, einzige Modell-Schreibsitzung): `place_struts` mit Rollwinkel, `strut_r` aus Basisringhoehe entkoppeln, `dome.sc` neu bauen
4. [ ] Werkstatt C: `tuer.sc` kennzeichnen, Werkstoffe auf Katalog, `check_parts.py`
5. [ ] Viewer: Kleinteil-Ausnahme in `export_model.py`, Screenshot Tuer und Strebe
6. [ ] `bom.py` und `check_bom.py` nachziehen
7. [ ] Pruefer: `docs/jobs/pruefung/N-MODELL-KOMPLETT.md` nach fuenf Pruefpunkten
8. [ ] Orchestrator: Roadmap nachfuehren, W65 (Ausfuell-Artefakt) freigeben

Reihenfolge: 2 und 5 duerfen vor Schritt 3 laufen (kein `dome.sc`-Neubau); 3 nach M10-S5-LUFT; 6 nach 3 und 4; 7 zuletzt.

## Stand
04.11.2026, Planer (Sonnet 5.5): Blatt geschrieben, Aktualitaet **angepasst**. Zwei Korrekturen am Auftragstext: (1) die genaue Tuer ist schon eingebaut, die Klinke fehlt nur im Export (`export_model.py:14`); (2) Strebenumbau hat Zusatzfolgen: Rollwinkel und `strut_r` in `gen_dome.py:250` (Basisring sonst 30 mm tiefer). Werkstoff-Zahl 39 nicht reproduziert, Schritt 4 misst neu. OFFEN (Ben): Wandstaerke 3 mm bis N-STATIK (Empfehlung 3 jetzt); `tuer.sc` loeschen oder kennzeichnen (Empfehlung kennzeichnen).

## DoD
Dateien aus dem Blatt vorhanden; fuenf Pruefpunkte vom Pruefer gemessen; Screenshot Tuer mit Klinke und Streben-Nahansicht gegen `docs/ui-standard.md`; Vorher/Nachher-Werte (Basisknoten-Z, defs-Summe) im Paket; Entscheidungen in `docs/decisions.md`; Commit und Push je Teilschritt.
