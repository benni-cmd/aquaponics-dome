# Work package: system-logic

**Problem:** Das Modell sieht teilweise passend aus, ist aber technisch nicht belegt: Es gibt keinen Wasserweg, keine Pumpen- und Filterrollen, keine Verteiler, keine Kuppel-Knoten, keine Stueckliste, und "naeher am Original" ist nicht gemessen.
**Intent:** Ein NGO-Projekt in entfernten Regionen soll aus dem Modell bauen koennen, teils mit lokalen Ressourcen: also ein Modell, dessen Wasserkreislauf, Bauteile und Kosten logisch stimmen und das so einfach und guenstig wie moeglich zu bauen ist.
**Goal:** (1) `data/system.json` beschreibt den Wasserkreislauf als Graph (Bauteile mit Anschlussports, Rohre als Kanten); `scripts/check_hydraulics.py` besteht; (2) die 3D-Rohre, Schlaeuche, Verteiler, Pumpen und Ventile entstehen aus diesem Graphen; (3) die Kuppel hat Knoten (Hubs) in einer begruendeten, einfach und guenstig baubaren Variante; (4) `scripts/check_fidelity.py` misst die Naehe zum OBJ je Bauteilklasse, Score steigt Runde fuer Runde; (5) `docs/bom.md` (Stueckliste mit Mengen) wird aus dem Modell erzeugt.

## Quellen (Rangfolge: Ben > OBJ-Zahlen > Bilder; siehe `reference/oasis-obj-analysis.md`)

1. Ben: Aquaponik mit Fischtank, Vortexfiltern, NFT-Systemen, Substratbeeten, Pumpen, Schlaeuchen; NGO-Projekt, lokale Ressourcen, Kosten zaehlen.
2. OBJ: 4 Tanks mit Plattformen, Pump-/Filtermodulen und PVC-Fittings (Bulkheads) nahe dem Boden; 14 IBC-Beete; 2160 NFT-Toepfe im Aussenring; Pool 3,89 m zentral.
3. Bilder `reference/ref-1` bis `ref-6`: Look und Komposition (Ziel).

## Annahmen zum Kreislauf (aus OBJ abgeleitet; Ben nicht bestaetigt, in `data/system.json` je Eintrag `assumption: true`)

Fischpool (T5) -> Bodenablauf/Skimmer -> Vortexfilter (die zwei kleinen Tanks, 0,67 x 1,08 m) -> Biofilter/Sump (die zwei grossen Tanks, 0,93 x 1,44 m) -> Pumpen (Module 0,46 x 0,35 x 0,20 m an den Tanks) -> Verteiler -> NFT-Ringrohre (parallel, Gefaelle 1-2 %) und erhoehte Tische -> Sammelrinne -> Substratbeete (IBC, Flut-und-Ablauf mit Glockensiphon) -> Schwerkraft-Ruecklauf zum Pool. Dazu: Belueftung (Luftpumpe, Ausstroemer in Pool und Biofilter), Notueberlauf, Ablassventile an den Tiefpunkten, Frischwasser-Zulauf mit Schwimmerventil (das blaue Zulaufrohr von aussen), Strom aus dem Schaltschrank (Solar spaeter).

## Plan (Reihenfolge, jede Phase = sichtbarer Commit)

1. [ ] **Systemgraph** `data/system.json`: Bauteile (id, Typ, Position, Hoehe, Ports mit 3D-Koordinate und Richtung ein/aus), Rohre (von-Port, nach-Port, DN, Art: Druck/Schwerkraft/Schlauch). Lesbares Schema in `docs/hydraulics.md` mit Fliessbild (Mermaid) und je Verbindung einer Zeile Begruendung. Rollen der 4 Tanks aus den OBJ-Fittings (Lage der Bulkheads) ableiten, nicht raten; Unsicheres als Annahme markieren.
2. [ ] **Hydraulik-Dimensionierung** in `docs/hydraulics.md`: Umlaufmenge Pool (mindestens 1 Volumen/h, Poolvolumen aus 3,89 m und Wassertiefe), NFT-Durchfluss je Rohr (ca. 1-2 l/min), Pumpenhoehe (statisch plus Reibung plus 20 % Reserve), Rohr-DN (Druckseite Fliessgeschwindigkeit <= 1,5 m/s, Schwerkraft DN >= 50 mit Gefaelle >= 1 %), Pumpenwahl (Fabrikatsneutral, Daten). Rechnung nachvollziehbar, Quellen fuer Richtwerte (zwei unabhaengige).
3. [ ] **`scripts/check_hydraulics.py`** (PASS/FAIL je Pruefung): Graph zusammenhaengend und geschlossener Kreislauf; jeder Port genau einmal verbunden, Rohr-Enden liegen auf den Port-Koordinaten (Toleranz 20 mm); Druckleitungen steigen, Schwerkraftleitungen fallen (Gefaelle >= 1 %); Durchflussbilanz je Knoten; Geschwindigkeit je Rohr im Grenzwert; Pumpenhoehe >= noetig; Sicherheit: kein Auslass unter dem Poolwasserspiegel ohne Siphonbrecher oder Ventil (Pool kann nicht leerlaufen), Notueberlauf vorhanden; Tuerzugang 1,0 m frei von Rohren.
4. [ ] **3D aus dem Graphen**: Skript erzeugt Rohre (gerade Stuecke, Boegen), Schlaeuche, Verteiler, T-Stuecke, Ventile, Pumpen, Bulkheads als wiederverwendbare Bauteile (`scripts/components/`), farbig nach Funktion (sauber / Filter / Ruecklauf / Luft / Frischwasser); Rohrverlauf rechtwinklig oder als kurzer Schlauch, ohne Durchdringungen mit Beeten und Streben.
5. [ ] **Kuppel-Knoten und Streben** (`docs/hubs.md`): Knoten des 2V-Gitters zaehlen (Apex 5-wertig, Rest 6-wertig, Basis 4-/5-wertig, Strebenlaengen-Gruppen). Optionen mit Entscheidungsmatrix (Kosten je Knoten, Werkzeug, Fachkenntnis, lokal beschaffbar, Winkelgenauigkeit, Wind-/Schneelast, Haltbarkeit, Montage ohne Kran): A) flachgedrueckte Rohrenden mit Schraube (Conduit-Dome), B) geschweisste Stahl-Hubs mit Rohrstutzen, C) Holzlatten mit Stahlblech-Knotenplatten und Schrauben (Holz lokal), D) Bambus mit Gusset und Seil (low-tech, geringe Festigkeit), E) HDPE/PVC (nur Last gering). Empfehlung begruenden (guenstigste baubare Variante, die die Last traegt), je Variante Parameter; die gewaehlte Variante als Bauteil `Knoten` modellieren (Hub je Knoten, Strebenanschluss). Hinweis aufnehmen: Profil 30 x 30 mm bei 12 m Spannweite ist statisch ungeprueft, ein statischer Nachweis durch eine Fachperson ist noetig; hier nur Plausibilitaet. Preise nur mit Quelle und Datum, sonst als Schaetzung kennzeichnen.
6. [ ] **Stueckliste** `scripts/bom.py` -> `docs/bom.md`: Streben nach Laenge und Stueckzahl, Knoten nach Typ, Rohre nach DN und Laenge, Formstuecke, Ventile, Pumpen, Tanks, IBC, Toepfe, Pflanzen; Summen. Wird aus dem Modell und dem Graphen berechnet, nie von Hand geschrieben.
7. [ ] **OBJ-Abgleich** `scripts/check_fidelity.py`: je Bauteilklasse (Pool, Tanks, IBC-Beete, NFT-Rohre/Toepfe, Hydroponik-Tische, Streben, Fittings) Anzahl und mittlere Positionsabweichung gegen das OBJ (Kuppelmitte als Ursprung, Azimut/Radius), Score je Klasse und gesamt in `renders/fidelity.json`. Schlechteste Klasse zuerst verbessern.
8. [ ] **Bauteil-Verfeinerung** laufend (wie `dome-build.md`): NFT-Rohr mit Toepfen, Salatkopf, Tank mit Fittings, Pool mit Rand und Skimmer, IBC-Beet mit Kies/Glockensiphon, Pumpe, Filter, Tuer, Haut.
9. [ ] **Foto-Render** mit ControlNet (`solidcraft-playground/comfyui/generate.py --control`) nach groesseren Schritten, Ergebnis in `renders/photoreal-*.png`; ComfyUI danach beenden.

## Loop v4 (Endlos, schlank)

Je Durchlauf: `check_hydraulics.py`, `check_latte.py`, `check_fidelity.py` laufen lassen -> den schlechtesten Punkt waehlen (FAIL zuerst, dann niedrigster Fidelity-Wert, dann naechste Phase) -> EINEN Schritt umsetzen -> Checks wieder laufen lassen (keine Verschlechterung committen) -> Screenshot mit `compare.py` ansehen -> Commit+Push -> eine Zeile in `docs/loop-log.md`. Checkpoint vor jedem Schritt in `docs/loop-state.md` (max. 8 Zeilen). Kein Ende ausser Bens "stopp": sind alle Checks gruen, naechster Verfeinerungspunkt aus Phase 8.

## Status

29.10.2026 — Plan angelegt. Phasen 1-9 offen.

## Definition of Done (je Phase)

Geprueft gegen: Check-Skripte (PASS), Screenshot gegen Referenz, `git log`
Offen: Phasen 1-9; Rollen der 4 Tanks und Pumpenlage (DEINE ENTSCHEIDUNG, nur falls Ben sie kennt, sonst Annahme)
