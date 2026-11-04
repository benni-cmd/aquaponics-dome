# Start-Auftrag: Planer M10-S5-LUFT (Orchestrator, 04.11.2026 nachts)

Grund fuer diese Datei: Die App startet seit Bens letzter Nachricht keine neuen Sitzungen mehr (Grenze 10). Der Auftrag geht deshalb per Weckruf an eine warme, verwandte Sitzung; der Inhalt steht hier.

Rolle: Planer nach `docs/jobs/vorlagen/planung.md` (nur lesen und ein Blatt schreiben, kein Modell, kein `data/`).

Frage zuerst (Aktualitaetspruefung): Lassen sich die neuen Bauteile aus W37-2 (Aktivkohle-Station, Schwimmerventil, Stutzen Drittbecken, 83d15c0) und W37-3 (Luftpumpen N+1, Verteiler, Scheibenbelueftung, 854276e) im Dom setzen und die Luftkanten K44 bis K51 sowie die Frischwasserkanten K39 bis K43 und K52 verlegen, OHNE die Kreislaufvariante E20 (Entscheidung Ben 05.11.)?

Eingaben: Roadmap-Eintrag M10-S5 (per Python aus `data/roadmap.json`), `data/leitungsnetz.json` (diese Kanten), Befund in `docs/packages/w37-2-3-frischwasser-luft.md`, `docs/loop-state.md` (Montage-Stand), `scripts/gen_dome.py` und `scripts/leitungen.py` per Grep.

Wenn ja: Blatt `docs/jobs/M10-S5-LUFT.md` (abgetrennter Teil von M10-S5, nur variantenunabhaengige Kanten und Bauteile; alles mit E20- oder E13-Bezug als "OFFEN (E20)"/"OFFEN (E13)"), Mini-Plan `docs/packages/m10-s5-luft.md`, drei bis fuenf fremd messbare Pruefpunkte, Start-Hinweis fuer die Montage. Wenn nein: nur Befund mit Grund in den Mini-Plan, kein Blatt.

Nicht anfassen: Modell, `data/`, `viewer/`, fremde Dateien. Parallel baut die Werkstatt N-STUECKLISTE 1b bis 1d.
Sichern: `git commit -m "Plan M10-S5-LUFT: ..." -- <pfade>`, `git push`. Abschluss: hoechstens sechs Zeilen, dann STOPP.
