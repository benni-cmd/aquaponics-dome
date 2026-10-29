# Sauberer Stopp (nach dem Muster "sanfter Stopp" aus smalltalk-languages, 22.10.2026)

Ausloeser: Ben schreibt "stopp" (sanfter Stopp: laufende Arbeit sauber beenden) oder nennt einen geplanten Stopp ("mach X fertig, dann stopp"; Ziel steht dann in `docs/orchestrator-state.md`, bei Erfuellung beginnt dieser Ablauf). Ergaenzungen oder neue Auftraege von Ben sind KEIN Stopp, sie werden eingereiht. Eine neue Phase von Ben beendet den bisherigen Endlos-Modus ebenfalls (Ablauf unten, danach neue Phase).

## Ablauf (Orchestrator fuehrt ihn aus, in dieser Reihenfolge)

1. **Stopp-Nachricht an beide Bau-Sitzungen** (`SendMessage`): aktuellen kleinen Schritt zu Ende bringen, nichts Neues beginnen, laufende Kritiker-Agenten beenden lassen, Checks laufen lassen, committen mit Pfad, pushen, Checkpoint mit Zeile "Stand beim Stopp" (was ist fertig, was angefangen, was offen mit Besitzer), Abschluss in hoechstens fuenf Zeilen.
2. **Zeile in `docs/loop-state.md` eintragen: `STOPP von Ben <Datum Uhrzeit>`** (frische geplante Laeufe beenden sich daran selbst).
3. **Automatik abschalten:** meinen Anstoss-Cron loeschen (`CronDelete`), die dauerhaften Auftraege `dome-loop-hourly-fallback` und `dome-loop-restart-0715` per `update_scheduled_task` auf `enabled: false` setzen (nicht loeschen, damit Ben sie wieder einschalten kann). Viewer-Server beenden (`python viewer/serve.py` Prozess), Port 4410 frei.
4. **Warten bis alles ruht:** `ListAgents` zeigt beide Bau-Sitzungen `idle`, kein Kritiker laeuft. Haelt sich eine Sitzung nicht daran, nach 10 Minuten per `stop_session` beenden und ihren letzten Commit pruefen.
5. **Sichern und belegen:** `git -C <repo> status` ohne eigene offene Aenderungen (offene Aenderungen anderer Rolle pruefen und mit Pfad committen), `git log origin/main..HEAD` leer (alles gepusht), `gh repo view` bestaetigt den Stand; Werkbank-Repo `keel-harness` ebenfalls (`CLAUDE.md`-Eintrag des Projekts, Skill gauntlet-loop) gepusht.
6. **Abschlusspruefung:** alle Pruefskripte laufen lassen (`check_latte.py`, `check_components.py`, soweit vorhanden `check_hydraulics.py`, `check_fidelity.py`) und die Zahlen mit Befehl notieren; letzte Renders aus `cam_ref4`, `cam_ref5`, `cam_ref1`, Schnitt ansehen; Skill `completeness` fuer das Audit (Coverage: alles adressiert? Fulfillment: Ziel erfuellt?).
7. **`docs/morning-report.md` zur Gesamtzusammenfassung fertigstellen** (eine Seite, Details verlinkt): Bilder, was gebaut ist (Board `docs/integration-board.md`), gemessene Zahlen mit Befehl, alle autonomen Entscheidungen (`docs/decisions.md`), Recherchen (`docs/research-queue.md`), offene Fragen an Ben mit Besitzer (Standort, Fischart, Tuerrichtung, Windfang, Pooltiefe, Hub-Variante), bekannte Risiken (Statik 30x30, Gewicht 25-30 t, Quellenluecken), "Wartet auf Ben", wie man das Modell ansieht (`python viewer/serve.py 4410`, oder `designs/dome.sc` in der SolidCraft-App), wie es weitergeht (`docs/resume.md`).
8. **Stand beim Stopp** als Eintrag in `docs/orchestrator-state.md` und `docs/loop-state.md`; Commit, Push, Verifikation.
9. **Eine einzige Gesamtzusammenfassung an Ben im Chat** (kurz, Antwort zuerst), Abschluss "Geprueft gegen / Offen" mit Besitzer je Punkt und der empfohlenen naechsten Handlung.

## Geplanter Stopp

Nennt Ben ein Ziel ("mach NFT, Tanks und Beete fertig, dann stopp"), trage es in `docs/orchestrator-state.md` ein (Zeile "Geplanter Stopp: ..."), schliesse nur diese Punkte ab (Board-Status `eingebaut` plus Checks PASS plus Abnahme), nichts Neues beginnen, dann Ablauf oben ab Schritt 1.

## Wiederaufnahme

`docs/resume.md`: Prompts zum Starten neuer Sitzungen je Rolle und Befehle zum Wiedereinschalten der Automatik.
