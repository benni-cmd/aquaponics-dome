# Arbeitspaket R39: Messstellenkonzept — wichtige Werte an mehreren kritischen Stellen des Kreislaufs

**Problem:** Gemessen wird heute nur in der Puffer-Station (4 Sonden: pH, EC, Temperatur, O2); die Alarmkette `steuerung_alarm` ist ein Platzhalter. Ein einziger Messpunkt sagt nicht, WO im Kreislauf etwas kippt (Fischbecken, Biofilter, Rinnenende, Luft, Strom). Ben (D65, 31.10.): an mehreren kritischen Stellen messen.
**Intent:** Fischtod und Anlagenschaden fruehzeitig erkennen und melden; Prozesswerte (pH, EC, Stickstoff) dort messen, wo sie sich aendern; die Stellen als Bauteile ins Modell bringen, damit Stueckliste, Kabel und Zugang (Laufwege >= 500 mm) stimmen.
**Goal:** `docs/research/R39.md` (Messstellenplan, Alarmgrenzen, Quellen, Konfidenz), `data/messstellen.json` (maschinenlesbar, Orte als Netzlisten-Knoten/-Kanten), `scripts/messstellen_plan.py` (Pruefung der Pflichtliste gegen `data/leitungsnetz.json`, Zaehlung je Sondentyp, Zugang gegen Laufwegkarte). Modell und Netzliste bleiben unveraendert.

## Plan

1. [x] Auftrag, R27, Werte-Tabelle, Puffer-Station, Filterkonzept, Netzliste, Laufwegkarte gelesen
2. [x] Web: Messgroessen/Alarme (SRAC 452 Volltext, Global-Seafood-Artikel), Sonden (Atlas pH/DO/EC/Durchfluss), Strom-/Pegel-/CO2-Sensorik
3. [ ] `data/messstellen.json` (Sondentypen, Messknoten, Messstellen, Alarmgrenzen, Pflichtliste)
4. [ ] `scripts/messstellen_plan.py` (Pruefung, Zaehlung, Zugang) laufen lassen
5. [ ] `docs/research/R39.md` schreiben
6. [ ] Committen mit Pfad, pushen

## Status

31.10.2026 — Schritte 1 und 2 erledigt.

## Definition of Done

Geprueft gegen: (wird beim Abschluss nachgefuehrt)
Offen: (wird beim Abschluss nachgefuehrt)
