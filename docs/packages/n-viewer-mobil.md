# N-VIEWER-MOBIL: einfache Mobilansicht für den öffentlichen Viewer

Stand 05.11.2026, Viewer-Sitzung. Status: gebaut und lokal belegt; Deploy wartet auf den Orchestrator (Berechtigungssystem hat `vercel deploy --prod` abgelehnt).

## PIG
- **Problem:** Der öffentliche Viewer (https://aquaponics-dome-viewer.vercel.app) ist für den Desktop gebaut: ein 330 px breites Bedienfeld verdeckt auf dem Handy das Modell, FPV lässt sich nur mit Tastatur und Maus steuern, und der Start lädt 317 MB entpackte Geometrie.
- **Intent:** Ben und Leon sehen das Modell unterwegs auf dem Handy, drehen es mit dem Finger und laufen im Ego-Blick (FPV) durch die Kuppel.
- **Goal:** Auf einem Touch-Gerät mit schmalem Bildschirm zeigt der Viewer ein kleines, einklappbares Menü, bewegt das Modell per Touch (drehen, zoomen, verschieben) und steuert FPV mit virtuellem Joystick (Laufen) und Wischen (Umschauen). Kleinteile laden mobil standardmäßig nicht. Die Desktopansicht bleibt unverändert; das ist per Screenshot und gleicher Ladestatistik belegt.

## Entwurf
1. **Weiche:** `html.mobil` wird früh im `<head>` gesetzt, nur wenn das Gerät Touch hat (Berührungspunkte, grober Zeiger oder mobile Browser-Kennung) und die kleinere Fensterseite höchstens 600 px misst. `?mobil=1` erzwingt, `?mobil=0` schaltet ab. Grund: der Browser-Pane meldet 0 Berührungspunkte, deshalb die Kennung und der Schalter. Ohne diese Klasse greift keine Mobil-Regel.
2. **CSS:** alle Mobil-Regeln stehen unter `.mobil`. Das Desktop-CSS wird nicht geändert.
3. **JS:** ein eigener Abschnitt am Ende des Modul-Skripts, nur bei `MOBIL`. Er legt Menü-Knopf, Joystick und Wisch-Blick an. Er nutzt die vorhandenen FPV-Funktionen (`fpvEnter`, `fpvLook`, `fpvApply`); der FPV-Code selbst bleibt unverändert.
4. **Zwei Einzeiler im Desktop-Pfad**, beide mit `MOBIL` abgesichert (Desktop führt dieselben Anweisungen wie vorher aus): Kleinteile aus dem lokalen Speicher ignorieren, und den Text-Zwischenspeicher `defCache` nach dem Aufbau leeren (spart Speicher auf dem Handy).
5. **Menü mobil:** Kamera-Knöpfe, FPV, Ansicht Visuell/Technisch, Plane, Kleinteile (mit Datenhinweis), Schnitt-Regler. Ausgeblendet (mobil, auch Kreislauf-Etikett): Bauteilbaum, Infopanel, Kontextmenü, Drahtgitter, Messstellen, Deckkraft, Kreislauf-Schalter, Detailansicht.
6. **Ladeanzeige** zieht mobil aus dem Menü an den unteren Rand, damit der Fortschritt bei geschlossenem Menü sichtbar bleibt.

## Plan
1. [x] Bestand lesen (`viewer/index.html`, V01, Hosting-Paket, `scripts/viewer_dist.py`)
2. [x] Paket anlegen
3. [x] Mobil-Schicht bauen
4. [x] Lokal testen (`viewer/dist` über `python -m http.server`), Screenshots mobil: Modellansicht, FPV mit Steuerelementen
5. [x] Screenshot Desktop (Preset desktop) als Beleg, dass Desktop gleich ist
6. [x] Ladezeit und Datenmenge mobil messen
7. [x] `viewer_dist.py` neu gelaufen; Deploy abgelehnt, an den Orchestrator übergeben
8. [x] Commit per Pfad, Push

## Messung (Browser-Pane, Preset mobile 375x812, lokaler Server auf `viewer/dist`, 05.11.2026)
| Größe | Wert | Befehl |
|---|---|---|
| Übertragen mobil (ohne Kleinteile) | 39,9 MB gzip, 250 Anfragen | `performance.getEntriesByType('resource')`, Summe `encodedBodySize` |
| Entpackte Geometrie mobil | 317,2 MB (296 Definitionen) | Ladeanzeige "Fertig: 296 Definitionen, 317,2 MB" |
| Ladezeit mobil, warmer Cache | 14 s | Ladeanzeige, zweiter Lauf |
| Ladezeit mobil, erster Lauf | 34 s (Pane teilweise im Hintergrund) | Ladeanzeige |
| Kleinteile (optional, mobil aus) | 29,5 MB gzip zusätzlich, 221 MB entpackt | Summe `dist/defs/*.klein.obj.gz` und `viewer/instances.json` (`klein_kb`) |
| Rohtext im Speicher nach dem Aufbau | 0 Einträge (`defCache.size`) | `window.mobilStand()` |
| `viewer/dist` gesamt | 173,6 MB, 1475 Dateien | `python -X utf8 scripts/viewer_dist.py` |

Ehrlich: Das ist der Pane (Desktop-Rechner, lokal), kein echtes Handy und kein Mobilfunk. Auf dem Handy sind 40 MB Übertragung und 317 MB Textverarbeitung die Risiken; ob der Speicher reicht, ist nicht gemessen (siehe Offen).

## Belege
- Mobil, Modellansicht: Kuppel passt ins Hochformat, Menü-Knopf oben links, Ladebalken unten (Screenshot im Browser-Pane, 05.11.2026).
- Mobil, Menü offen: Kamera-Knöpfe, FPV, Visuell/Technisch, Plane, Kleinteile mit Datenhinweis, Schnitt-Regler; Bauteilbaum, Infopanel und Kontextmenü fehlen mobil.
- Mobil, FPV: Joystick "Laufen" unten links, X oben rechts. Joystick voll nach oben bewegt die Kamera 2,1 m in 1,5 s (1,4 m/s wie Desktop); Wischen dreht den Blick (200 px nach rechts: Yaw 1,885 auf 1,185 rad); X beendet FPV und stellt Menü-Knopf wieder her.
- Desktop, unverändert: `git diff --stat viewer/index.html` zeigt 92 Einfügungen, 0 Löschungen. Im Desktop-Fenster: Klasse `statik` ohne `mobil`, Panel 330 px, Infopanel 410 px, 1065 Baumknoten, 5225 Instanzen, 296 Definitionen, `#mbtn` und `#mjoy` existieren nicht, `window.mobilStand` nicht definiert.
- `docs/ui-standard.md`: Sätze statt Fragmente (Datenhinweis "Lädt zusätzlich etwa 30 MB und braucht viel Speicher."), keine Unicode-Symbole, keine verbotenen Wörter, optische Abnahme per Screenshot gemacht. Punkte 3 bis 5 (Dashboard-Bausteine `HD.*`) gelten für das Dashboard, nicht für diesen Viewer.

## Stand
05.11.2026: Mobil-Schicht in `viewer/index.html` gebaut, `viewer/dist` neu gebaut (173,6 MB), lokal im Pane belegt (mobil Modell, mobil FPV, Desktop unverändert). Deploy: `npx.cmd --yes vercel@59.5.0 deploy --prod --yes` in `viewer/dist` wurde vom Berechtigungssystem abgelehnt ("Production Deploy"), nicht umgangen. Der Orchestrator deployt. Hinweis zum Bau: `viewer/dist` war durch einen fremden Prozess gesperrt (alter Testserver `http.server 4425` aus dem Hosting-Paket, beendet; danach hielt weiterhin ein Prozess den Ordner). Das Bau-Skript lief mit abgefangenem Löschfehler, Ergebnis gleich; das Skript selbst ist unverändert.

Weiche: `?mobil=1` erzwingt die Mobilansicht, `?mobil=0` schaltet sie ab.

## DoD
- [x] Deploy an den Orchestrator übergeben (Mobilansicht noch nicht online)
- [x] Screenshot Modellansicht mobil
- [x] Screenshot FPV mobil mit Joystick und X
- [x] Screenshot Desktop gegen `docs/ui-standard.md`, Desktop unverändert
- [x] Ladezeit und Datenmenge mobil mit Befehl im Paket
- [x] Paket nachgeführt, Commit und Push
- [ ] Mobilansicht online (Orchestrator)
- [ ] Test auf echtem Handy (Ben oder Leon): Speicher, Touch-Gefühl, Mobilfunk-Ladezeit
