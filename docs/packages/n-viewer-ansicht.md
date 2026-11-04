# Arbeitspaket N-VIEWER-ANSICHT (W68)

**Problem:** `viewer/index.html` `colorFor()` faerbt nach Namensvorsilben (T1_ bis T13_) und einer kleinen Tabelle; viele Teile wirken einheitlich grau, Werkstoffe sind nicht sichtbar. Die Referenzfiguren (`mensch_referenz_arbeiten`, `mensch_referenz_messen`) stehen immer im Bild.
**Intent:** Ben soll im Viewer wahlweise ein glaubhaftes Bild nach Werkstoff sehen (Visuell) oder eine technische Sicht nach Bauteilgruppe ohne Figuren (Technisch), ohne dass die Geometrie neu laedt.
**Goal:** Schalter "Ansicht: Visuell / Technisch" im linken Menue (Standard Visuell, `localStorage` merkt den Zustand); Visuell faerbt je Koerper nach Werkstoff aus `data/parts/<komp>.json` mit Farbtabelle `viewer/farben.json`, Rueckfall auf die heutigen Regeln; Technisch blendet die Figuren aus, faerbt nach Bauteilgruppe (Leitungen nach Nennweite), Wasser und Folie bleiben durchsichtig, kleine Legende; Umschalten tauscht nur Materialien und Sichtbarkeit.

## Plan

1. [x] `viewer/farben.json`: 31 Werkstoff-Regeln, Rueckfall Erde, Gruppenfarben, Nennweiten-Farben
2. [x] `index.html`: Teiledaten laden (`/parts/<stem>.json`: Werkstoff je Koerper, Bauteilgruppe), Materialien je Koerper (`vis`/`tech`), `applyAnsicht()`, Schalter, Legende
3. [x] Screenshots beider Ansichten (Gesamtansicht und Nahansicht Pool), Zaehlung per `window.ansichtStand()`

## Status

04.11.2026 — gebaut und im Browser-Pane belegt (Testserver auf dem echten Viewer-Ordner ohne Auto-Export, 164 Definitionen, 685 Koerper-Meshes):
- Zuordnung: 680 von 685 Meshes haben einen Werkstoff aus `data/parts` (99,3 %), die uebrigen 5 fallen auf die alten Regeln zurueck; Visuell zeigt 30 verschiedene Farben, Technisch 16.
- Technisch: 656 von 685 Meshes sichtbar, die 29 Meshes der Menschfiguren sind ausgeblendet; Visuell: alle 685 sichtbar. Umschalten ohne Neuladen (kein Ladebalken).
- Screenshots: Visuell Gesamt und Pool (Stahl silbergrau, Tanks hell, Holztuer, Wasser blau durchsichtig, Pflanzen gruen, Figuren in Weste), Technisch Gesamt und Pool (Gruppenfarben mit Legende, Leitungen nach Nennweite, Figuren weg, Huelle und Wasser durchsichtig).
- Abweichung vom Blatt: Das Blatt nennt "fuenf Gruppen der Einkaufsliste plus Leitungen nach Linie". Die Einkaufsliste hat acht Gruppen (ohne Massfigur) und `data/parts` kennt sie alle; die Zuordnung Leitung zu Linie (Hauptstrom, Tank 1+2, Tank 3+4, Luft) gibt es im Viewer nicht (kein Linienfeld je Rohrteil), daher faerbt Technisch Leitungen nach Nennweite (d25 bis d110). Eine Linienfaerbung braucht ein Linienfeld je Leitungsbauteil in `data/parts`.
- Kein Export noetig: Werkstoff und Gruppe kommen ueber `/parts/<komp>.json` (serve.py liefert sie schon). `designs/`, `scripts/`, `data/` unberuehrt.

## Definition of Done

Geprueft gegen: Screenshots Visuell und Technisch (Gesamt, Pool); `window.ansichtStand()` (Koerper, Werkstoff, sichtbar, Figuren, Farbzahl); `localStorage` `viewer.ansicht`; `viewer/farben.json` als einzige Farbtabelle
Offen: Leitungen nach Linie statt Nennweite (braucht Linienfeld je Leitungsbauteil, DEINE ENTSCHEIDUNG); 5 Meshes ohne Werkstoff in `data/parts`
