# Arbeitspaket R39: Messstellenkonzept — wichtige Werte an mehreren kritischen Stellen des Kreislaufs

**Problem:** Gemessen wird heute nur in der Puffer-Station (4 Sonden: pH, EC, Temperatur, O2); die Alarmkette `steuerung_alarm` ist ein Platzhalter. Ein einziger Messpunkt sagt nicht, WO im Kreislauf etwas kippt (Fischbecken, Biofilter, Rinnenende, Luft, Strom). Ben (D65, 31.10.): an mehreren kritischen Stellen messen.
**Intent:** Fischtod und Anlagenschaden fruehzeitig erkennen und melden; Prozesswerte (pH, EC, Stickstoff) dort messen, wo sie sich aendern; die Stellen als Bauteile ins Modell bringen, damit Stueckliste, Kabel und Zugang (Laufwege >= 500 mm) stimmen.
**Goal:** `docs/research/R39.md` (Messstellenplan, Alarmgrenzen, Quellen, Konfidenz), `data/messstellen.json` (maschinenlesbar, Orte als Netzlisten-Knoten/-Kanten), `scripts/messstellen_plan.py` (Pruefung der Pflichtliste gegen `data/leitungsnetz.json`, Zaehlung je Sondentyp, Zugang gegen Laufwegkarte). Modell und Netzliste bleiben unveraendert.

## Plan

1. [x] Auftrag, R27, Werte-Tabelle, Puffer-Station, Filterkonzept, Netzliste, Laufwegkarte gelesen
2. [x] Web: Messgroessen/Alarme (SRAC 452 Volltext, Global-Seafood-Artikel), Sonden (Atlas pH/DO/EC/Durchfluss), Strom-/Pegel-/CO2-Sensorik
3. [x] `data/messstellen.json` (Sondentypen, Messknoten, Messstellen, Alarmgrenzen, Pflichtliste)
4. [x] `scripts/messstellen_plan.py` (Pruefung, Zaehlung, Zugang), Negativtest: fehlende Pflichtstelle und fehlender Netzknoten werden gemeldet
5. [x] `docs/research/R39.md` geschrieben
6. [x] Committen mit Pfad, pushen

## Status

31.10.2026 — alle Schritte erledigt; 67 Messstellen (22 Pflicht, 45 Zusatz), Skript Exit 0. Folge: Werkstatt W35 (Halter `H_*`), Montage-Platzierung nach R37/W34, Leitungsplan M10 (Trunk + Stichleitungen je Messknoten).

## Definition of Done

Geprueft gegen: `python scripts/messstellen_plan.py` (Exit 0, 26/26 Pflichtlisten-Eintraege, alle Netzlisten-Knoten abgedeckt oder begruendet), Negativtest, `data/leitungsnetz.json`, `docs/walkway-map.md` (Runde 57), SRAC 452 Volltext, Atlas-Herstellerseiten
Offen: Notluft-/Notstrom-Auslegung (Ben waehlt Variante a/b/c, danach eigener Auftrag); Online-Verfahren fuer Ammonium/Nitrit/Nitrat nicht belegt (Handmessung); Durchflussmesser fuer 110 l/min Typ offen; Zugang von 28 Messstellen nicht pruefbar (Karte kennt Beete, Tische, Verteiler, Feinfilter, Station nicht)
