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

## Definition of Done

Geprueft gegen: Screenshots Balken/Menue/Tuer mit Klinke; `du -sh viewer/defs` vorher/nachher; Ladezeit ohne/mit Kleinteilen; `export_model.py` Exit 0 am Muster; Koerperzahl `tuer_komplett` 27
Offen: Screenshot der Tuer mit Klinke (Koerperzahl belegt, Bild fehlt); Beschreibungstexte in `data/descriptions.json` und `data/system-specs.json` nennen weitere von 2160 abgeleitete Werte (79 je m2, 24 %), die der Viewer nicht umschreibt
