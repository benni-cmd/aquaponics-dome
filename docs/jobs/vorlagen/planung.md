# Vorlage Planungssitzung (Planer)

Zweck (Ben 01.11.2026, E18): Der Planer schreibt das Auftragsblatt fuer einen Roadmap-Schritt, kurz BEVOR gebaut wird, mit frischem Kontext und frischer Aktualitaetspruefung. Der Orchestrator liest danach nur das fertige Blatt und die 6-Zeilen-Meldung, nicht mehr alle Recherche-Dateien. Frische Sitzung, nur lesen und ein Blatt schreiben. Empfohlen: Modell Sonnet, Aufwand medium.

**Wann Planer:** fuer jeden Montage- und Werkstatt-Schritt und jede Recherche mit mehr als einer Eingabedatei oder neuen Entscheidungen. **Wann nicht:** kleine Orchestrator-Arbeiten (Netzliste, Roadmap), Wiederanlauf eines schon geplanten Schritts.

**Eingabe (steht im Start-Prompt des Orchestrators):** Schritt-ID, Ziel in zwei bis drei Saetzen, Liste der Eingabedateien (bekannt), bekannte Entscheidungen, Nicht-anfassen-Liste, Rolle der spaeteren Bau-Sitzung.

**Ablauf**
1. Aktualitaetspruefung (Regel W44): Roadmap-Eintrag des Schritts (`data/roadmap.json`, nur diesen Eintrag per Python lesen), `docs/decisions.md` (letzte zehn Eintraege), `git log --oneline -15`, Ergebnisse der Vorgaengerschritte (die genannten Dateien). Ergebnis: **gueltig**, **angepasst** (Plan gilt dann als freigegeben) oder **wesentlich geaendert / obsolet** (dann STOPP, nur Befund melden, kein Blatt).
2. Blatt `docs/jobs/<ID>.md` schreiben, Aufbau wie `docs/jobs/README.md`: Problem · Intent · Ziel in einem Satz · Aktualitaetspruefung · Eingaben mit Datei und Zeilen (nur was gebraucht wird, Zeilen selbst nachsehen) · Schritte (einzeln committbar) · Nicht anfassen · Ergebnis · **Pruefpunkte**: drei bis fuenf messbare Punkte, die eine fremde Sitzung nachmessen kann (Befehl oder Datei plus Sollwert).
3. Am Blattende fuenf Zeilen Start-Hinweis fuer die Bau-Sitzung: Besonderheiten, bekannte Fallen aus den Vorgaengern, Limit-Hinweis.

**Grenzen:** schreibt nur `docs/jobs/<ID>.md` (und einen Mini-Plan in `docs/packages/<paket>.md`, wenn verlangt). Aendert kein Modell, keine Daten, nicht `data/roadmap.json`. Keine Rueckfragen an Ben, keine AskUserQuestion. Fehlt eine Entscheidung: im Blatt als "OFFEN (Ben)" kennzeichnen und die Teile ohne sie trotzdem planen. Nur die Eingaben lesen, die der Schritt wirklich braucht (Token-Limit).

**Kontext- und Limitregeln (Ben 01.11.2026, gelten auch fuer den Pruefer):** (1) Eine Sitzung = ein Arbeitspaket (eine Schritt-ID oder ein Buendel mit denselben Eingaben); ein neues Thema bekommt eine neue Sitzung. (2) Nur die genannten Eingaben lesen; grosse Dateien mit Grep oder Offset und Limit statt ganz; keine Ordner durchsuchen. (3) Ergebnisse stehen in der Datei, die Chat-Meldung hat hoechstens sechs Zeilen. (4) Ab etwa 60 Prozent Kontextfuellung nach dem letzten Commit den Stand ins Blatt schreiben und stoppen; die Fortsetzung macht eine neue Sitzung. (5) Nach der Meldung STOPP, keine Folgeaufgaben.

**Sichern:** `git commit -m "Plan <ID>: Auftragsblatt" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" -- docs/jobs/<ID>.md` (neue Datei vorher `git add -N`), `git push`. Fremde Dateien nie committen.

**Abschluss:** Kurzmeldung, hoechstens sechs Zeilen: Aktualitaet (gueltig/angepasst/obsolet und Grund) · Blattpfad · was Ben noch entscheiden muss · geschaetzte Zahl der Bau-Sitzungen · "Besonderheit: ..." falls etwas auffaellt. Dann STOPP.
