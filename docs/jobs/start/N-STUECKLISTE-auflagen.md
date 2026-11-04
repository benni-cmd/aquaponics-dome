# Start-Auftrag: Werkstatt N-STUECKLISTE, Pruefer-Auflagen A1 bis A4 und Neuerzeugung

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Werkstatt (du hast Skript und Seite gebaut).

1. Grundlage: `docs/jobs/pruefung/N-STUECKLISTE.md` (ff27b81), Abschnitt "Auflagen".
2. A1 Links: (a) `GEW-v2a-100um` Angebot mit 100 Mikrometer suchen, sonst Konfidenz `E`; (b) `SON-federdraht-d2` Quelle ersetzen oder Konfidenz `A` in Feld und Zeile; (c) `ARM-kugelhahn-d25` Link der 25-mm-Variante. Zwei unabhaengige europaeische Seiten selbst oeffnen; kein Kauf, keine Anmeldung, keine Formulare.
3. A2 `check_bom.py` Pruefung 12: Determinismus nur in einer Kopie (`BOM_ROOT`) pruefen, Drift-Stempel `modell_aktuell` aus dem Hash nehmen; das Skript darf die Repo-Dateien nicht mehr schreiben.
4. A3: `FOL-pe-plane` und `MES-ph` mit dem Land des Lagers statt `EU`; die 29 Zeilen `lieferung_de: unbekannt` so weit klaeren, wie es mit geoeffneter Seite geht, Rest bleibt `unbekannt` mit Grund.
5. A4: Anzeigetexte der Seite mit echten Umlauten ("Hülle"); Coding-Namen bleiben ASCII.
6. Danach die Liste neu erzeugen (`python -X utf8 scripts/bom.py`), weil die Montage der Beete (Runde 67, 290fe89) das Modell geaendert hat; Summen alt/neu im Paket `docs/packages/n-stueckliste.md` nennen. `check_bom.py` muss Exit 0 haben.
7. A5 (Desktop-Verknuepfung) ist entschieden: sie bleibt, Ben hat sie gewuenscht (Wunschbuch W59). Nichts tun.
8. Nicht anfassen: `designs/`, `viewer/`, `data/leitungsnetz.json` und die fremden, nicht committeten Aenderungen im Arbeitsbaum. Commits nur per Pfad, je Teilschritt, Push. Danach STOPP.
