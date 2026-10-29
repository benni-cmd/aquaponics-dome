# Plan fuer den Plan: wie geplant, recherchiert und gebaut wird (Prozess, v1, 29.10.2026)

**Problem:** Der Plan (Konzept-Atlas, Hydraulik, Statik, Biologie ...) wird WAEHREND des Baus verfeinert. Ohne festen Prozess driften Dokumente, Zahlen stehen doppelt, Recherchen sind nicht nachvollziehbar, Entscheidungen gehen verloren.
**Intent:** Planen, Recherchieren, Entscheiden und Bauen laufen parallel, aber jeder Schritt ist wiederholbar, belegt und im Repo sichtbar; eine neue Sitzung ohne Gespraechsverlauf kann ohne Rueckfrage weitermachen. Ben schlaeft, es gibt keine Rueckfragen.
**Goal:** Morgen liegt ein schoenes, plausibles Modell vor (Meilenstein unten), und jedes Dokument sagt, wie reif es ist, woher die Zahlen kommen und was noch offen ist.

## 0. AKTUELLE PHASE: reines Modell (Ben, 29.10.2026, bis er etwas anderes sagt)

Es geht NUR darum, das Modell und seine Bauteile besser, logischer und geprueft zu machen. Fischart, Standort, Klima, Biologie-Bilanz, Elektrik/Solar, Betrieb und Preise ruhen. Aktiv sind: wiederkehrende Bauteile als Komponenten, Layout nach `layout.json`, Geometrie und Details (Knoten, Beete mit Kies, NFT-Rinnen, Tanks mit Kegel, Pool, Rohre/Schlaeuche aus dem Graphen, Farben/Materialien), Wasserweg als Graph (Logik des Modells), geometrische Pruefungen (Kollisionen, Anschluesse, Gefaelle, Massabgleich mit dem OBJ), Gauntlet je Bauteil. Recherche nur fuer Modellgeometrie: R02 Hub, R03 Kiestiefe/Beetaufbau, R06 NFT-Geometrie, R09 Vortex-Tank-Geometrie, R11 Haut. Alle anderen R-Auftraege stehen auf `pausiert`. Die Abschnitte unten gelten sonst unveraendert; die Etappen E4 (Fachlich) und E5 (Betrieb) ruhen bis Ben sie freigibt. Statik bleibt als Hinweis im Morgenbericht (30x30-Profil), wird aber jetzt nicht ausgebaut.

## 1. Artefakte und ihre Rolle (eine Quelle der Wahrheit je Frage)

| Frage | Quelle der Wahrheit | Verbraucher |
|---|---|---|
| Wie viele, wie gross, wo (Original)? | `data/layout.json` (aus OBJ, erzeugt von `scripts/extract_layout.py`) | Baukript, `check_fidelity.py` |
| Welche Zahl gilt (Mass, Annahme, Grenzwert)? | `data/params.json` (je Parameter: Wert, Einheit, Herkunft `Q/E/A`, Quelle/R-ID, Reife, Fachbereich, verwendet von) | Baukript, alle `check_*.py`, Fachdokumente |
| Wie fliesst das Wasser? | `data/system.json` (Graph) | `check_hydraulics.py`, 3D-Rohre |
| Was ist offen zu klaeren? | `docs/research-queue.md` (R-Auftraege) | Rechercheschritt |
| Was wurde herausgefunden? | `docs/research/<R-ID>.md` | Fachdokumente |
| Wer hat wann was entschieden? | `docs/decisions.md` (D-Eintraege) | alle |
| Wie sieht es aus, wie gut? | `renders/`, `renders/gauntlet/`, `docs/loop-log.md` | Ben, Kritiker |
| Wo stehen wir? | `docs/loop-state.md` (max. 8 Zeilen) | frische Sitzung |
Regel: Zahlen stehen genau EINMAL (`params.json` oder `layout.json`); Dokumente und Skripte lesen sie, wiederholen sie nicht.

## 2. Reife-Stufen je Fachdokument (Kopfzeile `Reife: ...`)

0 Entwurf (Annahmen) -> 1 recherchiert (je Wert zwei unabhaengige Quellen oder als [E]/[A] markiert) -> 2 kritisiert (Fachkritiker hat Luecken benannt, behoben) -> 3 freigegeben fuer Bau (Modell darf sich darauf stuetzen). Das Modell nutzt auch Reife 0, aber der Morgenbericht nennt, was auf welcher Stufe steht.

## 3. Der Zyklus (wiederholbar, ein Agent zur Zeit)

1. **Bedarf finden:** Das Bauen erzeugt Fragen ("welche Kiestiefe?"). Jede Frage wird ein R-Auftrag in `research-queue.md` mit: ID, Frage, Warum (welcher Bauschritt haengt dran), Prioritaet (blockiert den Bau = hoch), Akzeptanz (zwei unabhaengige Quellen oder eigene Rechnung mit Quelle der Eingaben), Zielparameter in `params.json`.
2. **Recherche vor Urteil, Annahme nur als Platzhalter (Ben, 29.10.2026):** Entscheidungen stuetzen sich auf strukturierte Recherche, nicht nur auf eigenes Wissen. Bei einer Frage zuerst recherchieren (Abschnitt 3a). Kann der Bau nicht warten, ist eine Annahme (`A`) nur ein vorlaeufiger Platzhalter, und es MUSS ein R-Auftrag dazu existieren (Annahme ohne R-Auftrag ist verboten). Frist: der R-Auftrag wird innerhalb der naechsten zwei Baurunden bearbeitet, Prioritaet H vor jedem neuen Bauteil. Eintrag in `decisions.md` (Optionen, Wahl, Grund, Verweis auf R-ID, wie rueckgaengig). Danach weiterbauen; trifft die Recherche eine andere Aussage, wird die Entscheidung revidiert (Status `revidiert`) und das Modell folgt.
3. **Recherchieren just in time:** Hoechste Prioritaet zuerst, hoechstens ein Auftrag je Baurunde, ein Recherche-Agent zur Zeit. Suche -> Quelle oeffnen und lesen (nicht nur Suchtreffer) -> mindestens zwei unabhaengige Quellen -> Widersprueche notieren statt glaetten -> Ergebnis in `docs/research/<R-ID>.md` (Befund, Zahlen, Quellen mit URL und Datum, Konfidenz, Luecken) -> Parameter in `params.json` auf `Q` setzen -> Fachdokument und Modell folgen.
4. **Aenderung wirken lassen:** `params.json` geaendert -> `scripts/run_all.sh` (Neubau, alle Checks, Render) -> Vergleich mit Vorstand -> nur committen, wenn kein Check schlechter wurde.
5. **Kritik:** Bauteile durch den Gauntlet (Bildkritiker), Fachdokumente durch den Fachkritiker (Statik, Biologie, Technik); Luecken werden R-Auftraege oder Bauaufgaben.
6. **Protokoll:** eine Zeile je Runde in `loop-log.md`, `plan-changelog` unten, Commit+Push, Checkpoint.

## 3a. Recherche-Protokoll (strukturiert, wiederholbar)

1. **Suchplan** vorab im R-Dokument: Fragestellung in einem Satz, 3-5 Suchanfragen (deutsch und englisch), Quellenarten in Rangfolge: a) Normen und Regelwerke (Eurocode, IEC, EN), b) Fachbehoerden und Organisationen (FAO, SRAC, Universitaets-Extension), c) Hersteller-Datenblaetter, d) Fachbuecher und Handbuecher, e) Praxisberichte und Foren (nur zur Gegenpruefung, nie allein).
2. **Quellen lesen**, nicht nur Treffer: Seite oeffnen (WebFetch) oder, wenn gesperrt (z. B. FAO-PDF HTTP 403), ueber Spiegel/Kapitelseiten oder Zweitquelle; Zahl, Einheit, Randbedingung und Fundstelle notieren, kurzes Zitat (unter 15 Woerter) nur mit Quelle.
3. **Zwei unabhaengige Quellen** je Wert (nicht voneinander abgeschrieben); Primaerquelle bevorzugt. Gibt es nur eine, bleibt die Konfidenz `niedrig` und der Wert `Q1`.
4. **Widersprueche** in einer Tabelle (Quelle A sagt x, Quelle B sagt y, moegliche Ursache); nie glaetten. Entscheidung dann mit der konservativen Seite (bei Sicherheit/Statik die ungünstigere Zahl).
5. **Ergebnis** nach `docs/research/<R-ID>.md` (Vorlage `docs/research/TEMPLATE.md`): Frage, Suchplan, Befund, Zahlen mit Einheit, Quellen (URL, Abrufdatum, Art, Qualitaet), Widersprueche, Konfidenz (hoch/mittel/niedrig), Folge fuer Parameter und Modell, Luecken.
6. **Uebernahme:** `params.json` (Herkunft `Q`, R-ID), Fachdokument (Marke [Q]), `decisions.md` (Verweis).
7. **Recherche-Kritiker** (getrennter Agent, frischer Kontext) bei Prioritaet H oder bei Sicherheitswerten: liest nur das R-Dokument, prueft Unabhaengigkeit der Quellen, ob die Zahl wirklich in der Quelle steht, und ob Widersprueche ehrlich stehen. Meldet hoechstens fuenf Luecken.
8. **Anteil:** Mindestens ein Rechercheauftrag je zwei Baurunden wird abgeschlossen, solange offene H-Auftraege existieren; Statik (R01), Hub (R02), Kiestiefe (R03) vor allem anderen Detail.

## 4. Wiederholbarkeit (jeder kann es nachbauen)

- `scripts/run_all.sh` baut aus `layout.json` und `params.json` das Modell neu, fuehrt alle `check_*.py` aus, rendert die Standardkameras (cam_ref4, cam_ref5, cam_ref1), schreibt `renders/` und `renders/summary.json`. Ein Befehl, gleiches Ergebnis.
- `docs/environment.md`: Versionen (SolidCraft 0.25.1, ComfyUI 0.43.0, SDXL Base und ControlNet-Canny-Datei mit SHA256, Python), Aufrufe, Kamera-Parameter, Seeds.
- Skripte sind deterministisch; Zufall nur mit festem Seed (Foto-Render).
- Jede Zahl im Modell fuehrt ueber `params.json` zu einer Herkunft; ohne Herkunft gilt sie als offen.

## 5. Plan des Plans, in Etappen (Reihenfolge = Prioritaet, sichtbare Gewinne zuerst)

E1 Grundlage (sofort): `data/params.json` aus der Parameter-Tabelle `P` erzeugen, `run_all.sh`, `environment.md`, `decisions.md`, `research-queue.md` (dieses Dokument legt sie an).
E2 Sichtbar: Bauteil-Bibliothek, Aussenbeet mit Kies und Toepfen, NFT-Rinnen ueber den Beeten, Tanks mit Kegel und Plattform, Pool mit Rand, Farben/Materialien, Streben und Knoten.
E3 Technisch: `system.json`, `check_hydraulics.py`, Rohre und Schlaeuche aus dem Graphen, Pumpen, Filter.
E4 Fachlich: `statics.md` + `check_statics.py`, `biology.md` + `check_biology.py`, `electrical.md`, `bom.md`.
E5 Betrieb: `operations.md`, `assembly.md`.
E6 Schlussglanz: ControlNet-Foto-Render, Morgenbericht.
Etappen laufen verschraenkt: je Runde ein Bauschritt (E2/E3) und, wenn Limit und Zeit es erlauben, ein Rechercheschritt (E4). Beginne E4 frueh genug, damit die Statik das Profil beeinflussen kann, bevor die Streben endgueltig modelliert werden.

## 6. Meilenstein "Morgen-Demo" (Ben schlaeft, Ziel: ein cooles Modell)

Bis morgen mindestens: (a) saubere Gesamtansicht aus drei Kameras, farbig, ohne Fremdkoerper (kein blauer Stab im Inneren); (b) 14 Beete mit Kies und Pflanzen, NFT-Rinnen mit Toepfen ueber den Beeten, 4 Tanks mit Kegelboden und Plattform, Pool und zweites Becken mit Wasserflaeche; (c) Streben mit Knoten; (d) erste Rohre und Schlaeuche aus dem Graphen; (e) ein ControlNet-Foto-Render; (f) `docs/morning-report.md` mit: Bildern, was gebaut wurde, was berechnet ist (Statik-Warnung zuerst), alle autonomen Entscheidungen aus `decisions.md`, offene Fragen an Ben (Standort, Fischart, Pooltiefe), naechste Schritte. Der Morgenbericht ist kurz (eine Bildschirmseite), Details verlinkt.

## 7. Grenzen der Autonomie (nachts ohne Ben)

Erlaubt: Bauen, Rechnen, Recherchieren (lesend), committen und pushen im Repo `aquaponics-dome`, Render mit der lokalen ComfyUI-Installation. Nicht erlaubt: Kaeufe, Installationen oder Downloads ausser Lesen von Webseiten, Aenderungen an Einstellungen/Berechtigungen, Pushes in andere Repos, Loeschen fremder Dateien. Wird eine Aktion abgelehnt, nicht umgehen: im Checkpoint vermerken, mit etwas anderem weitermachen. Bei Zweifeln zwischen zwei Optionen die reversible waehlen und in `decisions.md` festhalten.

## 8. Limit und Neustart

Limit voll nutzen, aber ab 85 % ein Bauteil je Schritt, Checkpoint VOR jedem Schritt, Commit+Push NACH jedem Schritt. Neustarts: geplanter Lauf 07:15 und stuendlicher Auffang (Waechter: letzter Commit juenger als 20 min = laeuft schon) lesen `loop-state.md`, `plan-process.md`, `research-queue.md`.

## 9. Plan-Changelog

- 29.10.2026 v1: Prozess angelegt (Artefakte, Zyklus, Reife-Stufen, Morgen-Demo, Autonomiegrenzen).
