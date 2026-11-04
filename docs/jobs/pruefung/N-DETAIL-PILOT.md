# Pruefung N-DETAIL-PILOT (Pruefer, 04.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md`. Gegenstand: Blatt `docs/jobs/N-DETAIL-PILOT.md`, Paket `docs/packages/n-detail-pilot.md`, Commits 8e16da5 bis 89237cd. Ein frueherer Pruefer hatte keinen Befund hinterlassen, daher vollstaendig neu. Die Selbstauskunft im Paket wurde als Behauptung behandelt und nachgemessen. Viewer auf eigenem Testport 4431 (der alte Server auf 4410 blieb unberuehrt), echte Klicks im Browser-Pane (Rechtsklick, Menue, Schieber ziehen, Zeilenklick, Zurueck), Dritt-Datei-Probe in einer Kopie unter dem Scratchpad (Repo unberuehrt).

## Urteil: PASS mit Auflagen

Alle fuenf Pruefpunkte des Blatts sind erfuellt und nachgemessen. Die Auflagen betreffen nur die Anzeigetexte (Register-Kuerzel und Parameternamen in Saetzen, ein Grammatikfehler) und die Kameraeinstellung bei Schieber 1; keine davon bricht ein Soll des Blatts.

## Pruefpunkte

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | Exit 0; 55 und 33 Koerper; jeder Koerper genau einmal; kein `Body<Zahl>`; Pflichtfelder gefuellt | `python -X utf8 scripts/workshop/check_parts.py feinfilter tank_klein` | Exit 0; feinfilter 55/55 Koerper, 19/19 PASS; tank_klein 33/33, 19/19 PASS; `Body<Zahl>` Ist 0. Gegenprobe: `check_tank.py klein` 34/34 PASS, `check_feinfilter.py` 54/54 PASS (Interferenzen 0) | PASS |
| 2 | defs 316,4 MB +- 1 %; 152 Definitionen; 4880 Instanzen; Detail-OBJ nur in `viewer/detail/`, je hoechstens 10 MB | `python -c "import os;print(sum(os.path.getsize('viewer/defs/'+f) for f in os.listdir('viewer/defs'))/1e6)"`; `instances.json` gelesen; `ls -la viewer/detail` | Erste Messung 316,42 MB (nur `.obj` 316,415). Spaeter 317,60 MB (+0,37 %), weil der alte Server auf 4410 nach einer Aenderung anderer Sitzungen am Modell neu exportiert hat (`built` 01:33:42); innerhalb der Toleranz und nicht dem Piloten zuzurechnen. 152 Definitionen, 4880 Instanzen. Detail-OBJ feinfilter 6,78 MB, tank_klein 8,22 MB; `viewer/detail/` ist unversioniert (`git status`: `??`) | PASS |
| 3 | Vor dem Klick kein Request auf `detail/` oder `/parts/`; danach je eine `.obj`, `.json`, `/parts/<def>.json`; `grep -c "^o "` 55 / 33 | `read_network_requests` im Browser; `grep -c "^o " viewer/detail/*.obj` | Vor dem Klick 0 Requests auf `detail/` und `/parts/` (nur `/defs/`). Absetzer: genau `/parts/tank_klein.json`, `/detail/tank_klein.json`, `/detail/tank_klein.obj`. Feinfilter: genau `/parts/feinfilter.json`, `/detail/feinfilter.json`, `/detail/feinfilter.obj`. `grep -c`: feinfilter 55, tank_klein 33. Nebenbefund: `/katalog.json` wird zusaetzlich geladen (auch bei Bauteilen ohne Teiledaten); das Blatt verbietet nur `detail/` und `/parts/` | PASS |
| 4 | Box bei Schieber 0 = `.sc`-Box +-1 mm; Schieber 1: Siebkorb ueber Deckel, `folgt`-Teile ueber Bezugsteil; Zeile "Siebgewebe" zeigt Werkstoff, Funktion, Norm, Lebensmittelkontakt als Worte; Zurueck stellt Kamera +-1 mm her; vier Screenshots | `window.detailState()`; unabhaengige Box aus `solidcraft-cli.exe eval` je `.sc`; Explosionsrechnung aus `data/parts/feinfilter.json` und `viewer/detail/feinfilter.json`; Screenshots mit dem Read-Werkzeug angesehen | Box feinfilter Viewer [-375,-340,0]/[385,325,903] = `.sc` [-375,-340,0]/[385,325,903]; tank_klein Viewer [-344,5,-351,2479,-24]/[441,5,344,5,1323] = `.sc` (Abweichung unter 0,001 mm). Schieber 1: Box -250..1919,97 = gerechnet 1920; Siebkorb Unterkante z 1315 ueber Deckelgriff Oberkante z 1243; `kugelhahn_hebel` (folgt Kugelhahn) Offset 0/-200/60 = Bezugsteil plus Eigenabstand. Zeile "Siebgewebe des Korbs": Werkstoff "Edelstahl-Drahtgewebe, Maschenweite 100 Mikrometer", Funktion als Satz, Norm DIN ISO 9044 [A] (angenommen), Lebensmittelkontakt "Ja (angenommen)", Belegstand "gerechnet". Zurueck: mit Standardkamera Abweichung 0; mit von Hand gedrehter, beruhigter Kamera Abweichung 0 / 0 / 0 (Kamera und Ziel). Screenshots: Absetzer zusammen, Absetzer gesprengt, Absetzer Infokarte Kugelhahn, Feinfilter zusammen, Feinfilter gesprengt mit Infokarte Siebgewebe, Gesamtansicht mit Rechtsklick-Menue (6 Bilder gegen `ui-standard.md`, siehe Optik) | PASS |
| 5 | Kein Komponentenname im Viewer-Code; dritte `data/parts`-Datei ohne Viewer-Aenderung ladbar | `grep -nE "feinfilter\|tank_klein" viewer/index.html`; Probe in Kopie unter dem Scratchpad (nicht im Repo): neue `data/parts/zulaufrohr.json` mit einem Koerper, `export_detail.py zulaufrohr`, unveraenderte `index.html` | grep 0 Treffer. Probe: Detailansicht "Zulaufrohr (Pruefsonde)" oeffnet, 1 Koerper, Teileliste und Schieber vorhanden; Kopie und Probe-Server danach entfernt bzw. beendet, im Repo nichts angelegt | PASS |

## Stichproben ausserhalb der Pruefpunkte

1. Zahl aus der Kurzmeldung gegen die Datei: "7 Werkstoffe, 2 Profile, 5 Rohre, 3 Normteile" gegen `data/katalog.json` = 7 / 2 / 5 / 3, `stand: pilot`. PASS.
2. Teil gegen sein Blatt: Siebgewebe "560 x 370 x 400 (Parameter basket_l, basket_w, basket_d)" gegen `data/components/feinfilter.json` (`basket_l` 560, `basket_w` 370, `basket_d` 400). PASS. Schraubenmasse 17,92 g je Schraube (Stahl verzinkt), Gesamtmasse Absetzer aus dem Detailmodell 37,357 kg = 37,24 + 0,12 wie gemeldet. PASS.
3. Commit gegen `git diff`: `git diff 8e16da5^ 89237cd --name-only` nennt neben den Pilotdateien auch `data/roadmap.json`, `docs/orchestrator-state.md`, `roadmap/index.html`; das stammt aus den zwei Orchestrator-Commits 6d44a35 und c7c4f07 im Bereich, nicht aus den Pilot-Commits. Die Pilot-Commits selbst beruehren nur ihre genannten Pfade (`git log --stat`); `export_model.py`, `dome.sc` und andere `components/*.sc` ausser `tank_klein.sc` sind unveraendert, `serve.py` +4 Zeilen (zwei Durchreichen). PASS.

## Nicht belegte oder nicht nachgemessene Behauptungen

1. Hover auf einer Zeile hebt die Koerper im Modell gelb hervor, und Klick auf einen Koerper im Modell waehlt die Zeile: nicht nachgemessen (kein Pruefpunkt des Blatts); Zeilenklick mit Cyan-Hervorhebung im Modell wurde gesehen.
2. "Bezugsteile standardmaessig durchsichtig": Haken ist gesetzt und das Verhalten im Bild sichtbar, aber nicht numerisch nachgemessen.
3. Normverweise sind laut Paket `angenommen`; nur DIN 8062/EN 1452, EN 10088-2, DIN ISO 9044, ISO 4017 stehen im Repo. Nicht nachgeprueft, die Infokarte zeigt das Wort "angenommen" und einen Hinweis.

## Optik gegen `docs/ui-standard.md` (sieben Punkte)

1. Saetze statt Fragmente: Funktion und Eigenschaften sind ausgeschriebene Saetze. Die Tabellenzeile "Masse" enthaelt Kurzformen ("Gehaeuse etwa 56 breit, 40 lang (z 120 bis 160)") mit Parameternamen in Klammern. Auflage A1.
2. Ein Vokabular: Infokarte benutzt vorhandene Klassen (Badges, Notiz, Quellzeile); keine neue Mischung gesehen. PASS.
3. Status als Wort: Konfidenz, Belegstand und Lebensmittelkontakt stehen als Wort ("angenommen", "gerechnet", "Ja (angenommen)"). PASS.
4. Etablierte Bausteine: bestehendes Infofeld und Baum-Stil, Teileliste in der linken Spalte. PASS.
5. Kein Unicode-Symbol statt Icon: "Zurueck zum Gesamtmodell" ist reiner Text; im Detailcode nur das Faltzeichen der Teileliste (`▸`, wie im vorhandenen Baum) und das Malzeichen in "4 ×". Hinweis, kein Befund.
6. Verbotene Woerter: in Detailcode und Anzeigetexten beider `parts`-Dateien kein Treffer (Brett, Posten, Rubrik, Marke, Kennung, Waechter und die uebrigen der Liste). PASS.
7. Screenshots im Browser: gemacht und angesehen (siehe Pruefpunkt 4). Optisch sauber: Teileliste, Schieber, Infokarte lesbar, gelbe Hinweiskarte klar abgesetzt.

## Auflagen

1. **A1, Register-Kuerzel und Parameternamen im Anzeigetext:** Gemessen (`re` ueber alle Anzeigefelder beider `parts`-Dateien): 30 Stellen mit R09/R31/R50/R52/D76/B6 und 37 Stellen "Parameter <name>" (z. B. "Parameter valve_len, valve_d", "Regel D76"). Ben liest das als Fragment; in Klartext umformulieren (Folgeschritt `N-DETAIL-R50`, nur Daten, kein Viewer-Code).
2. **A2, Grammatik:** Kopfzeile zeigt "1 Teile, 1 Koerper" (Probe) bzw. "14 Teile, 33 Koerper"; Singular fehlt bei 1. Kleine Viewer-Aenderung (`viewer/index.html`), gleiche Datei wie V-MESS, daher dort mitnehmen.
3. **A3, Kamera bei Schieber 1:** Beim Absetzer ist der Deckel oben aus dem Bild geschnitten, solange man nicht "Ansicht einpassen" drueckt (Schaltflaeche ist da). Vorschlag: beim Ziehen auf Schieber 1 einmal selbst einpassen. Kein Soll des Blatts.

## Hinweise (keine Auflage)

- Bauteile ohne Teiledaten (Biofilter) zeigen im Rechtsklick-Menue den normalen Eintrag "Detailansicht"; erst nach dem Klick erscheint ein kurzer Hinweis mit dem Befehl. Das ist die im Paket dokumentierte Abweichung vom grauen Menue; der Hinweis ist nur wenige Sekunden zu sehen.
- Rechtsklick auf einen Absetzer trifft bei verdeckter Lage zuerst die davorstehende Strebe (Treffer = naechstes undurchsichtiges Objekt); der Weg ueber den Baum plus Schaltflaeche "Detailansicht" funktioniert.
- Die Kamerapruefung braucht eine beruhigte Kamera: direkt nach dem Ziehen laeuft die Daempfung noch nach (erste Messung 14 m daneben, nach Beruhigung 0). Kein Fehler des Viewers.
- Stand der Selbstauskunft insgesamt: alle gemessenen Zahlen stimmen mit dem Paket ueberein.

Geprueft gegen: check_parts 19/19 je Komponente, check_tank klein 34/34, check_feinfilter 54/54, Summe `viewer/defs` (316,42 und 317,60 MB), Netzwerklog im Browser, `grep -c "^o "`, `solidcraft-cli eval` je `.sc`, `window.detailState()`, 6 Screenshots, Dritt-Datei-Probe, `git log --stat` und `git diff --name-only`.
Offen: A1 bis A3 (Folgeschritt, Orchestrator); nicht nachgemessen: Hover und Modellklick (siehe oben).
