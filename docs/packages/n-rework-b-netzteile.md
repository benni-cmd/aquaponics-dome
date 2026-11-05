# Work package: N-REWORK B Fehlende Netz-Bauteile (M02) und Tankdeckel (M11)

**Problem:** Die Netz-Knoten `verteiler_1/2` und `ruecklauf_1/2` haben im Modell kein Bauteil (`docs/model-maengel.md` M02), der Biofilter Drittbecken fehlt, und die Deckeloeffnung der Tanks zeigt im Viewer den Grund (M11).
**Intent:** Die Montage soll S3 (Verteilung, Ruecklauf) ohne Wartezeit verlegen koennen, und Ben soll im Viewer keine scheinbar offenen Tanks sehen.
**Goal:** Fuer jeden der Knoten Verteiler und Ruecklauf gibt es eine gepruefte Komponente mit Ports passend zu den Netz-Kanten; der Biofilter Drittbecken ist geprueft (vorhanden oder Befund mit Grund); fuer `tank_klein`, `tank_gross`, `tank_gross_t3` ist gemessen, ob ein Koerper offen ist, und offene Koerper sind geschlossen oder die Ursache liegt nachweislich im Viewer.
Auftrag: `docs/jobs/start/N-REWORK-folge.md` Abschnitt B (Commit 72dc3d3). Erlaubt: `designs/components/`, `scripts/components/`, `scripts/workshop/`, `docs/parts/`, `data/components/`, `data/parts/`.

## Plan
1. [x] Bestand: `lt_verteiler_d50` existiert (T70-V-50-4, Abgaenge Beete d40, NFT d32, Messkreis d20, Bypass d50; `check_lt_w36.py verteiler` 29/29 laut Blatt). M02 sucht den Netz-Namen `lt_verteiler`: kein Bau, nur Namenshinweis an die Montage.
2. [ ] Ruecklauf-Sammler `lt_sammler_d110` (neu, `scripts/workshop/leitung_w71.py`): Sammelrohr d110 (Formstueck), Auslauf A Muffe d110 zum Pool (K16/K32), Zulaeufe oben als Muffen: NFT d63 (K15/K31), Bypass d50 (K13/K29), Beet-Sumpf d40 (K58/K59); Abgang unten Zapfen d50 Zweitbecken (K33, nur Linie 1; Linie 2 mit `lt_kappe_d50`). Ende geschlossen. Check `check_lt_w71.py`: 1 Koerper, Masse, Ports (Stirnflaechen), Luft zwischen Muffen, Durchfluss-Bilanz je Linie, Schwerkraft-Kapazitaet bei 1 % Gefaelle, Volumen gegen Raster, Interferenz 0 mit Testrohren in den Muffen.
3. [ ] Teiledaten `data/parts/lt_sammler_d110.json` (Ausnahme Katalog: N-STUECKLISTE nimmt den Artikel auf), Blatt-Abschnitt `docs/parts/leitungsteile.md`, `data/components/leitungsteile.json` (Schluessel `w71_teile`), `check_leitungsteile.py` schliesst die Datei aus den 63 Bibliotheksteilen aus.
4. [ ] Biofilter Drittbecken: pruefen, ob eine Komponente existiert; Netz fuehrt ihn als "Empfehlung, nicht im Modell" (37 l Bioballs). Befund hier eintragen; Bau nur mit Masswerten aus Recherche (sonst als offener Punkt).
5. [ ] M11 Tankkoerper: `solidcraft-cli.exe eval` je Tank, Feld `closed` je Koerper; offene Koerper benennen und im Generator `scripts/workshop/tank.py` schliessen, sonst Befund "Viewer".
6. [ ] Messwerte hier eintragen, Commit per Pfad, Push, Kurzmeldung, STOPP.

## Stand
05.11.2026, Werkstatt (Opus 5.5): Plan angelegt, Schritt 1 erledigt.

## DoD
Sammler gebaut und Check Exit 0; Teiledaten `check_parts.py lt_sammler_d110` Exit 0; Biofilter-Befund mit Grund; M11 je Tank gemessen (Koerper offen ja/nein) und gegebenenfalls geschlossen; Commit und Push.
