# Arbeitspaket N-VIEWER-LADEN (W66)

**Problem:** `viewer/index.html` `load()` holt 152 Definitionen (312 MB in `viewer/defs`, `du -sh viewer/defs`) ohne jede Anzeige; Ben sieht nicht, ob der Viewer arbeitet oder haengt. `viewer/export_model.py` wirft Koerper unter 15 cm Diagonale (`MIN_DIAG = 150`) ganz weg: Tuerklinke, Scharniere und Schrauben fehlen (`tuer_komplett.obj` zeigt 12 von 27 Koerpern). Die Seitentexte nennen alte Topfzahlen (2834 gesamt, 2160 Beete, 1634 im Board) statt der Modellzahl.
**Intent:** Ben soll beim Laden sehen, was passiert (und wann etwas haengt), und Kleinteile bei Bedarf einschalten koennen, ohne dass der Standardstart schwerer wird.
**Goal:** (1) Balken mit Text "Definition x von N, y MB von z MB, aktuelle Datei, vergangene Zeit", Phasen Laden/Aufbauen/fertig, Haenger-Hinweis nach 20 s, Fehler je Datei sichtbar; gilt auch fuer Auto-Update und Kleinteile-Nachladen. (2) Checkbox "Kleinteile unter 15 cm zeigen" (Standard aus, localStorage); Export schreibt `defs/<stem>.klein.obj`, Viewer laedt sie erst beim Einschalten; mit Haken zeigt `tuer_komplett` alle 27 Koerper. (3) Topfzahlen im Viewer aus dem Modell abgeleitet (2222 gesamt, 1548 Beet-Toepfe). (4) Screenshots und Messwerte (Ladezeit ohne/mit Kleinteilen, Groesse `viewer/defs` vorher/nachher).

## Plan

1. [x] `export_model.py`: Kleinteile in `<stem>.klein.obj`, Cache-Schluessel erweitert, `instances.json` traegt `klein_kb`; Test am Muster in einer Scratchpad-Kopie (Exit 0), 27 Koerper bei `tuer_komplett`
2. [x] `index.html`: Lade-Fortschritt (Balken, Text, Phasen, 20-s-Hinweis, Dateifehler) in `load()` und im Nachladen
3. [x] `index.html`: Kleinteile-Schalter (localStorage, Nachladen, Ausblenden)
4. [x] Topfzahlen aus dem Modell ableiten (SPEC und DESC)
5. [x] Screenshots im Browser-Pane gegen `docs/ui-standard.md`, Messwerte
6. [x] Voller Export erst nach "Montage fertig" des Orchestrators, dann `export_model.py` und Viewer-Dateien committen

## Status

04.11.2026 — Paket angelegt, Plan steht. Montage von `designs/dome.sc` laeuft parallel; voller Export erst nach "Montage fertig".
04.11.2026 — Punkte 1 bis 5 gebaut und am Muster gemessen (Scratchpad-Kopie, 5 Definitionen, `export_model.py` Exit 0, 18 s):
- Export: `tuer_komplett.obj` 12 Koerper + `tuer_komplett.klein.obj` 15 Koerper = 27 (`grep -c "^[go] "` je Datei); Cache-Schluessel `mtime|min_diag|v2`; `instances.json` traegt `klein_kb` je Definition.
- Viewer: Balken mit "Definition x von N, y MB von z MB, aktuell <Datei>, t s", Schritte Laden/Aufbauen/fertig, Hinweis nach 20 s ohne Daten ("Keine Antwort seit ... bei <Datei>", mit Schwelle 3 s in einer Testkopie vorgefuehrt), Fehler je Datei als rote Liste (404 einer Definition in der Testkopie sichtbar, restliches Modell laedt weiter). Gilt fuer Erstladen, Auto-Update und Kleinteile-Nachladen (eine gemeinsame `Lade`-Anzeige).
- Kleinteile-Schalter: Standard aus, `localStorage` `viewer.kleinteile` (try/catch), Reload merkt den Haken; mit Haken `window.viewerStand()` meldet `tuer_komplett` 12 + 15 = 27 sichtbare Koerper, ohne Haken 12 + 0; Wiedereinschalten ohne neues Laden.
- Topfzahlen: Viewer leitet sie aus `netztopf`-Instanzen ab (groesste Hoehenluecke trennt Beet und NFT): Seite zeigt 2.222 gesamt, 1.548 / 674; keine Handzahl im Code.
- Baseline (alte Definitionen, kein Kleinteile-Export, echter Viewer-Ordner, Testserver ohne Auto-Export): 164 Definitionen, 282,1 MB, Laden + Aufbauen 19 s (`Fertig`-Zeile der Seite); `du -sh viewer/defs` 312 MB vor dem Neuexport.
04.11.2026 — Voller Export nach "Montage fertig" (dome.sc 10:33): `python -X utf8 viewer/export_model.py` Exit 0, 1686 s, 164 Definitionen alle neu, 4914 Instanzen, 256,0 MB Hauptdateien + 198,9 MB Kleinteile in 78 `*.klein.obj`; `du -sh viewer/defs` 312 MB vorher, 485 MB nachher (alte Dateien ohne Kleinteile waren 282 MB laut Seite). Hinweis statt Stille eingebaut (0410a20): ohne Kleinteile-Dateien nennt der Viewer den Grund und den Befehl.
- Messung im Browser (Testserver ohne Auto-Export): Laden + Aufbauen ohne Kleinteile 12,7 s (vorher 19 s mit den alten Dateien); Kleinteile nachladen 78 Dateien, 198,9 MB, 8 s (Server lokal); `tuer_komplett` 12 + 15 = 27 sichtbare Koerper mit Haken. Screenshot beim Nachladen: "Kleinteile, Schritt 1 von 3: Laden, Datei 5 von 78, 23,0 MB von 198,9 MB, aktuell knoten_6_n01.klein.obj".
- `viewer/defs/` und `viewer/instances.json` sind in `.gitignore`: sie liegen nur lokal. Wer `serve.py` startet, bekommt den Export beim naechsten Speichern von `dome.sc` selbst.

04.11.2026 — Nachbesserung "Failed to fetch" (Seite lud waehrend eines laufenden Exports): `export_model.py` schreibt `instances.json`, `extras.json` und `.cache.json` jetzt per Temp-Datei und `os.replace`, `instances.json` zuletzt (OBJ-Dateien waren schon so); `serve.py` exportiert beim Start nur, wenn `dome.sc` neuer ist als `viewer/instances.json`; der Viewer laedt nicht, solange `/api/state` `busy` meldet, und zeigt "Export laeuft, das Modell wird danach automatisch neu geladen"; fehlgeschlagene Dateien werden bis zu zweimal wiederholt (0,8 s und 1,6 s Pause), `instances.json` und `extras.json` ebenso, erst danach Fehlerzeile "nach 3 Versuchen". Grenze: Windows kann eine Datei, die der Server gerade liest, nicht atomar ersetzen; die Wiederholung faengt diesen Rest ab.
- Gemessen am Muster (Scratchpad-Kopie, Port 4469): Start mit aelterer `dome.sc`: `busy` false, kein Export; `dome.sc` anfassen: Export laeuft (`busy` true), Seite zeigt den Hinweis (Screenshot), nach dem Export laedt sie selbst, 0 Fehlerzeilen; Datei `tuer_komplett.klein.obj` 3 s entfernt: Meldungen "Wiederholung 1 von 2" und "2 von 2", dritter Versuch gelingt, `tuer_komplett` 12 + 15 Koerper, 0 Fehlerzeilen.
- Hinweis: Ein laufender `serve.py` (Port 4410) hat den alten Code im Speicher; neu starten, damit der Start ohne Export und der Export mit atomaren JSON-Dateien gelten.

05.11.2026 — M12 Anschlussteile immer sichtbar (Befund `docs/model-maengel.md` M12, Auftrag `N-REWORK-folge.md` C): `viewer/anschluesse.json` listet Namensmuster (Stutzen, Muffen, Kugelhaehne, Abgaenge, Bulkhead, Flansche, Tuellen, Huelsen, Reduktionen, Auslauf/Ablauf/Zulauf, Endstopfen, Kabelverschraubung ...); `export_model.py` haelt passende Koerper im Hauptexport, auch unter 15 cm Diagonale (Cache-Schluessel `v3` plus Kennung der Liste, `instances.json` traegt `anschluss_immer_sichtbar`), der Viewer sagt es im Hinweis unter dem Haken. Am Muster (Scratchpad-Kopie mit 5 Definitionen, `export_model.py` Exit 0): Absetzer `tank_klein` 19 Koerper vorher, 21 nachher ohne Haken (Ablaufstutzen und Schlammstutzen dazu, Schlammstutzen jetzt an der Kegelspitze sichtbar), `feinfilter` 42 von 55 statt 31, `pumpe_gross` 7 von 15. Screenshots vorher (echter Export) und nachher (Muster) mit gleicher Kamera. Der volle Export folgt mit der naechsten Montage (`python -X utf8 viewer/export_model.py`, rund 30 Minuten).
- Messhaken `window.kamera(pos, ziel)` fuer Bildvergleiche; Muster ohne `data/parts` meldet `ansicht.json` als nicht lesbar (Rueckfall greift), im echten Ordner nicht.

## Definition of Done

Geprueft gegen: Screenshots Balken/Menue/Tuer mit Klinke; `du -sh viewer/defs` vorher/nachher; Ladezeit ohne/mit Kleinteilen; `export_model.py` Exit 0 am Muster; Koerperzahl `tuer_komplett` 27
Offen: Screenshot der Tuer mit Klinke (Koerperzahl belegt, Bild fehlt); Beschreibungstexte in `data/descriptions.json` und `data/system-specs.json` nennen weitere von 2160 abgeleitete Werte (79 je m2, 24 %), die der Viewer nicht umschreibt
