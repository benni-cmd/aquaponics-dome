# Start-Auftrag: Werkstatt-Vorlauf und Montage M-BEET-TAUSCH (Orchestrator, 04.11.2026 nachts)

Weckruf statt neuer Sitzung (App-Grenze, siehe `docs/orchestrator-state.md`). Rolle: zuerst Werkstatt-Vorlauf, dann Montage. Du bist jetzt die EINE schreibende Bau-Sitzung.

1. Blatt `docs/jobs/M-BEET-TAUSCH.md` und Mini-Plan `docs/packages/m-beet-tausch.md` (2ef4f20) ganz lesen, Aktualitaetspruefung kurz (`git log --oneline -15`, `git status --short`).
2. Werkstatt-Vorlauf laut Blatt Schritt 0 (W40-Auflagen 3 und 4) und Schritt 1 (Auflage 5). Zusaetzlich W37-Auflage A5 aus `docs/jobs/pruefung/W37-2-W37-3.md`: in den acht Bauteilblaettern von W37-2/W37-3 den Satz "Kein Pruefer-Lauf ... Pruefer folgt" auf den Verweis `docs/jobs/pruefung/W37-2-W37-3.md` umstellen und im Paket `docs/packages/w37-2-3-frischwasser-luft.md` Punkt 11 abhaken.
3. Montage laut Blatt Schritt 2: Dom neu bauen, Kollision und Gaenge pruefen, Viewer-Export. Alles mit Bezug zur Kreislaufvariante (K14/K30, Beet-Sumpf) bleibt OFFEN (E20).
4. Checks seriell starten, nie mehrere parallel (W37-Auflage A4: gemeinsamer TMP-Ordner in `scripts/workshop/sc.py`).
Nicht anfassen: fremde unversionierte `.sc` (Liste in `git status`), `data/beschaffung/`, `data/katalog.json`, `docs/einkaufsliste.html`, `scripts/bom*.py` (parallel baut eine andere Sitzung die Einkaufsliste).
Sichern: Pfad-Commits `git commit -m "M-BEET-TAUSCH: ..." -- <pfade>`, `git push`, WIP-Commit spaetestens alle 20 Minuten. Abschluss: Paket nachfuehren, hoechstens sechs Zeilen, dann STOPP.
