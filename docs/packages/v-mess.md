# Arbeitspaket V-MESS: Viewer Ebene Messstellen, Plane-Sichtbarkeit, Kennzahlen

**Problem:** Die 22 Halter und Sonden im Modell (`MS_halter_*`, `MS_sonde_*`, je wenige Zentimeter gross) gehen im Gesamtbild unter; die durchsichtige Plane (Hülle) kann man nicht ausblenden oder stärker durchsichtig stellen; die Kennzahlen zeigen den Puffer (0,16 m³) als "0,2" und kennen die Messstellen nicht.
**Intent:** Ben soll Messstellen im Modell sofort finden, ins Innere der Kuppel sehen können und Kennzahlen lesen, die genau aus `data/system-specs.json` und `data/messstellen.json` kommen.
**Goal:** (1) Ebene "Messstellen zeigen": Haken im Menü, Markierkugeln und Leuchtumriss an allen Haltern und Sonden, Zähler "n von 67 geplanten Messstellen haben ein Bauteil"; Kategorie "Messstellen" im Bauteilbaum. (2) Plane: Haken "Plane zeigen" und Schieber Deckkraft, Zustand im `localStorage`. (3) Kennzahlen: Wasseranteile unter 1 m³ mit zwei Nachkommastellen (Puffer 0,16), Abschnitt "Messstellen" aus `data/messstellen.json` und den Instanzen. Nur `viewer/` wird gebaut, kein Vollexport.

## Plan

1. [x] `serve.py`: Route `/messstellen.json`
2. [x] `index.html`: Ebene Messstellen (Haken, Kugeln, Umriss, Baumkategorie)
3. [x] `index.html`: Plane-Haken und Deckkraft-Schieber
4. [x] `index.html`: Kennzahlen (Puffer 0,16, Abschnitt Messstellen)
5. [x] Screenshots Messstellen an/aus, Plane an/aus/durchsichtiger, Kennzahlen; Messung per Browser

## Status

05.11.2026 — Plan angelegt (Roadmap-Eintrag V-MESS). L18 (Viewer-Export unter 40 MB) ist laut Auftrag nicht Teil dieses Schritts: er braucht einen Vollexport.
05.11.2026 — Gebaut und im Browser-Pane gegen den echten Viewer-Ordner gemessen (Testserver ohne Auto-Export, kein Export, nur `viewer/`):
- Ebene Messstellen: Haken "Messstellen zeigen" (Standard aus, `localStorage` `viewer.messstellen`), 7 Markiergruppen (rosa Kugeln mit Leuchtumriss, sichtbar durch andere Koerper), Bauteilbaum bekommt die Kategorie "Messstellen"; `window.messStand()`: 5 Halter und 17 Sonden = 22 Bauteile im Modell, 67 Messstellen im Plan (22 Pflicht, 45 Zusatz). Ohne den Haken "Kleinteile" erscheinen nur Kugeln und die grossen Halterteile.
- Plane: Haken "Plane zeigen" (Standard an) und Schieber "Deckkraft Plane" 0 bis 60 % (Standard 14 %, wie bisher), beides im `localStorage`; aus: 0 sichtbare Plane-Netze (vorher 6), Innenraum frei; 45 %: milchig. Screenshots: Messstellen an, Plane aus, Plane 45 %.
- Kennzahlen: Puffer zeigt jetzt "0,16 m³ (0%)" (Anteile unter 1 m³ mit zwei Nachkommastellen, Quelle `data/system-specs.json` Feld `wasser.teile`), neuer Abschnitt "Messstellen" (Plan aus `data/messstellen.json` ueber `/messstellen.json`, Zaehlung aus den Instanzen).
- Nicht gemacht: L18 (Export unter 40 MB, braucht Vollexport); fest im Code stehen noch "12 m Durchmesser, 2V-Halbkugel, 6 m hoch" und "2 × <W>" Pumpen.

## Definition of Done

Geprueft gegen: Screenshots im Browser-Pane; `window.messStand()` (Zaehlung Halter und Sonden); Kennzahl Puffer in der Seite gegen `data/system-specs.json`
Offen: L18 Exportgroesse; zwei feste Texte im Kennzahlenkopf (Durchmesser, Pumpenzahl) stehen nicht in `system-specs.json`
