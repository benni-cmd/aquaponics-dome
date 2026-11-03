# R52 — Europa-Bezug der Kaufteile aus R50 und R51 (D76)

**Art:** Recherche und Rechnung, KEIN Bau, kein Modell-Umbau. Auftrag Ben 03.11.2026: „Schau, dass wir die Bauteile mindestens in Europa auch bekommen.“

## Problem
R50 fand den Kegelboden-Tank für den Absetzer (`tank_klein`) nur bei US-Händlern; auch andere Kaufteile aus R50 und R51 (Beutelgehäuse, Siphon-Kits, Siebgewebe) waren teils nur über US-Quellen belegt. Nach D76 gilt ein Teil, das nur bei US-Händlern gefunden wurde, als nicht beschaffbar.

## Intent
Ben soll wissen, welche Kaufteile in Europa bestellbar sind, wo eine Quelle fehlt und was das Bauteil `tank_klein` bei einem europäischen Standardtank ändern würde, bevor er entscheidet.

## Goal
Ein Bericht `docs/research/R52-europa-bezug.md` mit Antwort zuerst (höchstens fünf Punkte), mindestens drei realen Kegelboden-Tank-Produkten mit Maßen, Anschlüssen, Link und Lieferland und Vergleich mit `tank_klein`, einer Tabelle aller weiteren Kaufteile (Quelle 1, Quelle 2, Status), einer Liste der Stellen in Dokumenten und Bauteilblättern, die wegen D76 anzupassen sind (Datei und Zeile), Empfehlung je Teil mit Bens offenen Entscheidungen; Herkunftsmarken Q, Q-Treffer, E, A; Rechenskript `scripts/r52_rechnung.py`.

## Grenzen
Kein Umbau, `gen_dome.py`, `data/*`, Netzliste und Roadmap unverändert; keine Kostenrechnung (D69, Preise nur grobe Orientierung); keine fremden Dateien angefasst (`designs/components/*`, `viewer/extras.json`, `renders/*`); Nachrichten an andere Sitzungen gesperrt. Kontextgrenzen nach `docs/arbeitsweise-sitzungen.md` Abschnitt 4.

## Stand (03.11.2026, Fachrecherche)
- **Fertig:** `docs/research/R52-europa-bezug.md` (5 Abschnitte, 3 Tank-Produkte, 14 Kaufteil-Zeilen, Stellenliste mit Datei und Zeile) und `scripts/r52_rechnung.py`. Nichts am Modell, an der Netzliste, an der Roadmap geändert.
- **Ergebnis:** Kegelboden-Tank: Enduramaxx 250 l, 45°, Ø609 × H1257, 2″-Auslauf (UK) passt fast genau zu `tank_klein` (20,0 gegen 20,3 min Verweilzeit); EU-Quelle CGK (NL) 300 l auf Anfrage, Kegelwinkel unbekannt; tanksdirekt.de 200 l nur als Notlösung. Weitere Kaufteile: 10 von 14 Zeilen mit zwei europäischen Quellen; nur eine Quelle: Beutelgehäuse Größe 2, Siphon-Kit; **nicht beschaffbar: fertiger 100-µm-Siebkorb 560 × 370 × 400** (Ersatz: Korb aus Gewebe 100 µm und Rahmen, Selbstbau). R50 Zeile 27 und 85 korrigieren (Aquagart nur 300 µm).
- **Grenzen der Belege:** EU-Festland-Versand und Zoll für Enduramaxx und CGK nicht belegt; Kegelwinkel und Wandstärke CGK offen; Kugelhahn-PN d75, Datenblätter von Bevo, GF, Wilo und Pumpen nicht gelesen; Riffert, Weinmann-Schanz und Hennlich beim Abruf nicht erreichbar (Zertifikatsfehler, 404), Inhalt aus der Suchzusammenfassung.
- **Offen:** DEINE ENTSCHEIDUNG: UK als „Europa“ zulassen; Enduramaxx oder CGK; Hersteller-Gestell. DEINE HANDLUNG: CGK und einen UK-Händler nach Versand, Zoll, Kegelwinkel, Wandstärke und Preis fragen; Gewebe-Muster bestellen. ICH: Werkstatt-Folge am Bauteil nach Bens Wahl, Datenblätter lesen, N-BESCHAFFUNG.
