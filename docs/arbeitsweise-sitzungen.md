# Arbeitsweise: Sitzungsarten, Ablauf und Regeln (aquaponics-dome)

Stand 01.11.2026, Orchestrator. Quelle der Regeln: Entscheidungen von Ben (E18, W44, W47 bis W50, siehe `docs/decisions.md` D73 und D74 und `docs/packages/wunschbuch-ben.md`). Dieses Dokument ist die EINE Stelle, an der die Arbeitsweise steht; `docs/jobs/README.md` und die Vorlagen verweisen hierher. Was nicht belegt ist, ist als [A] (Annahme) markiert.

## 1. Sitzungsarten
| Art | Aufgabe | Schreibt | Modell und Aufwand | Vorlage oder Blatt |
|---|---|---|---|---|
| Orchestrator | koordiniert, entscheidet innerhalb von Bens Vorgaben, pflegt Roadmap, Wunschbuch, Pitch-Register, Netzliste, Entscheidungen, Zustand | `data/roadmap.json`, `roadmap/`, `data/leitungsnetz.json`, `docs/decisions.md`, `docs/orchestrator-state.md`, Wunschbuch, Pitch-Register | Sonnet, hoch | `docs/orchestrator-state.md` (Wiederanlauf) |
| Planer | schreibt das Auftragsblatt eines Schritts, macht die Aktualitaetspruefung, baut nichts | `docs/jobs/<ID>.md` | Sonnet, mittel | `docs/jobs/vorlagen/planung.md` |
| Fachrecherche | liest Quellen, rechnet, liefert Empfehlungen mit Belegstand | `docs/research/<ID>.md`, eigene Rechenskripte `scripts/r<nr>_*.py` | Sonnet, mittel bis hoch | Blatt `docs/jobs/<ID>.md` |
| Werkstatt | baut Bauteile als Komponenten (`.sc`) mit Check, Bauteilblatt, Bild | `designs/components/`, `scripts/workshop/`, `docs/parts/`, `data/components/`, `data/descriptions.json` | Sonnet, hoch | Blatt `docs/jobs/W<nr>-*.md` |
| Montage | setzt Bauteile ins Modell, verlegt Leitungen, baut Runden, prueft Gaenge und Kollision | `scripts/gen_dome.py`, `scripts/leitungen.py`, `data/leitungstrassen.json`, `designs/dome.sc`, Bilder, `docs/loop-state.md` | Sonnet, hoch | Blatt `docs/jobs/M10-*.md` |
| Pruefer | Gegenleser: misst nach, liest die Selbstauskunft nie als Beweis | `docs/jobs/pruefung/<ID>.md` | Sonnet, mittel | `docs/jobs/vorlagen/pruefung.md` |
| Viewer-Sitzung | Browser-Viewer und Uebersichten | `viewer/` | Sonnet, mittel | Blatt oder Auftrag des Orchestrators |

Nur eine SCHREIBENDE Bau-Sitzung (Werkstatt oder Montage) gleichzeitig, weil alle im selben Arbeitsordner und Index arbeiten. Planer, Pruefer und Recherche lesen und schreiben je eine eigene Datei und duerfen parallel laufen.

## 2. Ablauf je Roadmap-Schritt
1. **Aktualitaetspruefung** (Regel W44): vor jedem Start Blatt und Roadmap-Eintrag gegen die Aenderungen der Vorgaenger und neue Entscheidungen lesen; Ergebnis gueltig, angepasst (Plan gilt als freigegeben) oder obsolet (dann erst Ben fragen).
2. **Planer** schreibt das Blatt mit drei bis fuenf messbaren Pruefpunkten (Bundel mit gleichen Eingaben in einer Sitzung). Entfaellt bei kleinen Orchestrator-Arbeiten und beim Wiederanlauf.
3. **Orchestrator** liest nur Blatt und Kurzmeldung und gibt frei, setzt die Roadmap auf "laeuft".
4. **Bau** (Werkstatt, Montage oder Recherche), je Teil ein Pfad-Commit.
5. **Pruefer** misst nach, Urteil PASS, PASS mit Auflagen oder FAIL, Befund in `docs/jobs/pruefung/<ID>.md`. Auflagen werden Roadmap-Schritte oder Luecken.
6. **Orchestrator** schliesst den Schritt in der Roadmap erst bei PASS und meldet Ben die Folgen, Fragen und Besonderheiten.

## 3. Start einer Sitzung
- Der Start-Prompt beginnt mit `PROJEKT: aquaponics-dome (user-projects/aquaponics-dome)`, dann cd in den Projektordner, dann "nicht per AskUserQuestion nachfragen". Der Hook `.claude/project-context.js` fragt bei der ERSTEN Nachricht nach dem Projekt-Kontext und bleibt bei `PROJEKT:` stumm; Rueckfall ist die Marke `keel-subsession-marker.json` im Temp-Ordner (10 Minuten).
- Aufbau des Prompts: Auftrag (Blatt und Schritt), Aktualitaetspruefung, Arbeitsweise (Python-Pfad, Skripte per Write), Sichern (nur Pfad-Commits), Abschluss (Kurzmeldung, STOPP). Die Vorlagen enthalten den festen Teil; der Brief hat hoechstens fuenfzehn Zeilen. Planer und Pruefer starten mit Aufwand medium.
- Die ersten Zuege jeder Sitzung enthalten eine Bestaetigung des Kommunikationsmodus (Skill `i-have-adhd`, vom Hook `session-roles.js`); der Start-Prompt sagt, dass sie danach sofort mit dem Auftrag beginnt.
- Nachrichten ZWISCHEN Sitzungen sind gesperrt (`sessionpost-guard.js`); erlaubt ist nur das Weckformat `WIEDERANLAUF aquaponics-dome: Fakt: ... Beleg: ... Zu tun: ...` (hoechstens 300 Zeichen), das auf ein Blatt verweist. Inhalte stehen in Dateien, nicht in Nachrichten.

## 4. Kontext- und Limitregeln (D74)
**Messwerte aus diesem Projekt (01.11.2026, `get_usage` und `list_events`):** Grundlast einer Sub-Sitzung etwa 71.000 Tokens (Werkzeuge, Systemtext, Skills, Gedaechtnis); jede Nachricht (mit Werkzeugergebnissen) im Mittel etwa 440 Tokens. Daraus: Kontext ungefaehr 71.000 + 440 x Nachrichten (W39 gemessen: 328 Nachrichten = 214.584 Tokens = 21 Prozent von 1 Mio.). Ein Bau-Lauf endet bei etwa 600 Nachrichten (Recherche R45 573, Werkstatt A 609, Montage S2R 589) = ungefaehr 35 Prozent; Planer 159 = etwa 14, Pruefer 102 = etwa 12 Prozent. Bei laufenden Sitzungen zeigt `get_usage` mit `session_id` den echten Wert, bei untaetigen nicht (dann die Formel).
**Warum diese Regeln [A]:** Jeder Zug liest den ganzen Kontext erneut; zwischengespeicherte Tokens kosten wahrscheinlich nur einen Bruchteil, wie der Tarif sie zaehlt ist nicht belegt. Ein Neustart kostet die Grundlast plus das erneute Lesen der Eingaben, eine wiederverwendete Sitzung traegt dagegen alten Kontext mit. Die Rechnung kippt bei etwa zehn bis fuenfzehn Zuegen.
1. **Wiederverwenden statt neu starten** (Wunsch Ben 01.11.), wenn ALLE drei stimmen: (a) das neue Paket ist fachlich verwandt (gleiche Dateien, Bibliothek oder Skripte wie die Sitzung schon kennt), (b) es ist KURZ (hoechstens etwa zehn Zuege), (c) die untaetige Sitzung steht bei hoechstens 25 Prozent (etwa 400 Nachrichten) und ihr letzter Zug liegt hoechstens 60 Minuten zurueck (warmer Zwischenspeicher [A]). Dann weckt der Orchestrator sie per Weckformat mit Verweis auf das Blatt.
2. **Neue Sitzung** bei einem neuen, unverwandten oder langen Thema (mehr als etwa fuenfzehn Zuege) oder wenn die Sitzung ueber 25 Prozent steht. Der Pruefer darf nie die Sitzung sein, die das Gepruefte gebaut hat.
3. **Grenzen einer Sitzung:** weiche Grenze 30 Prozent (etwa 520 Nachrichten): kein neues Paket mehr annehmen, das laufende zu Ende bringen. Harte Grenze 45 Prozent (etwa 860 Nachrichten): nach dem letzten Commit den Stand ins Blatt oder in den Zustand schreiben und stoppen; die Fortsetzung macht eine neue Sitzung.
4. **Buendeln:** Ein Planer schreibt mehrere Blaetter mit denselben Eingaben (Pilot W37 und W39: 4 Blaetter in einer Sitzung). Ein Pruefer prueft zwei bis drei zusammengehoerige Schritte mit denselben Skripten an einem Meilenstein.
5. **Eingaben lesen:** nur die im Blatt genannten Dateien; grosse Dateien mit Grep oder Offset und Limit; keine Ordner durchsuchen; Bilder nur, wenn ein Pruefpunkt sie nennt.
6. **Ergebnisse in Dateien**, Chat-Meldung hoechstens sechs Zeilen, danach STOPP und keine Folgeaufgaben.
7. **Orchestrator:** liest Blatt, Befund und Kurzmeldung, nicht die Recherche-Volltexte; ein Thema mit mehr als wenigen Aufrufen geht an eine Sitzung. Bei etwa 50 Prozent eigenem Kontext uebergibt er an eine frische Orchestrator-Sitzung ueber `docs/orchestrator-state.md`.
8. **Messen:** vor und nach jeder Sitzung die Werte aus `get_usage` und die Nachrichtenzahl in `docs/jobs/kosten.md` eintragen; nach etwa sechs Eintraegen die Schwellen aus den Daten nachschaerfen.

## 5. Sichern und Fremdes
- Commits nur mit Pfad: `git commit -m "..." -- <pfade>`, neue Dateien vorher `git add -N`, nie `git add -A` oder `commit -a`; danach `git push`. Im Workspace-Repo und im Projekt-Repo je mit `git -C <repo>`.
- Fremde unversionierte Dateien (`viewer/extras.json`, erzeugte `designs/components/*.sc`, `designs/dome.sc` von Builds anderer Sitzungen) nie mitcommitten.
- Die Netzliste `data/leitungsnetz.json` und `data/roadmap.json` gehoeren dem Orchestrator; Sitzungen melden Aenderungswuensche in der Kurzmeldung.

## 6. Laufende Pflege durch den Orchestrator
- **Roadmap** (`data/roadmap.json` -> `scripts/build_roadmap.py` -> `roadmap/index.html`, Desktop-Verknuepfung "Kuppel Roadmap"): Fragen und Handlungen fuer Ben stehen ganz oben ("Von dir gebraucht"), dann laufend, naechste Schritte, nach dem Zwischencheck, Luecken. Nach jedem Bau Exit-Code und HTML pruefen; neue Arbeit sofort eintragen.
- **Luecken** (L01 ff.) werden nie nur im Chat gefuehrt; jede traegt vorn, wo sie geschlossen wird.
- **Wunschbuch** (`docs/packages/wunschbuch-ben.md`): jeder Wunsch von Ben lueckenlos, Konflikte als Entscheidung.
- **Pitch-Register** (`docs/pitch-besonderheiten.md`): Sitzungen melden "Besonderheit: ..." in der Kurzmeldung; Eintrag mit ehrlichem Belegstand und dem, was man NICHT behaupten darf.
- **Entscheidungen** (`docs/decisions.md`), **Zustand** (`docs/orchestrator-state.md`), Gedaechtnis des Orchestrators (Memory-Dateien).
- **Umfang (D69):** keine Ertrags-, Kosten-, Standort- oder Verschattungsrechnung; Standardmasse bevorzugen (W43); Teileliste per Skript aus dem Modell (W45); Beschaffbarkeits-Nachweis spaeter (W47, N-BESCHAFFUNG).
- **Berichte an Ben:** Antwort zuerst, Antwortart benennen, Listen hoechstens fuenf Punkte, Schluss "Geprueft gegen" und "Offen" mit Besitzer ICH, DEINE ENTSCHEIDUNG oder DEINE HANDLUNG.

## 7. Offene Punkte der Arbeitsweise
1. Kosten je Sitzungsart sind noch nicht gemessen (nur Summen); `docs/jobs/kosten.md` wird gefuellt.
2. Zaehlung zwischengespeicherter Tokens im Pro-Tarif und Lebensdauer des Zwischenspeichers der Sub-Sitzungen unbekannt [A].
3. Der Hook `project-context.js`: Beleg fuer die stumme `PROJEKT:`-Seite in einer echten Subsession steht aus.
4. Sechs vorbestehende Fehler in `dashboard/test/hooks-detail.test.js` (nicht Teil dieses Projekts, nicht behoben).
