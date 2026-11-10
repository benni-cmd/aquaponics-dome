# Paket N-UNIFY-AUTOBAHN: ein Wasserkreislauf, exakt nach Leons Oasis-Showcase

**Problem:** Das Modell hat zwei Wasserkreisläufe (A+ mit Zielbild S und Ring B2 als Wasserautobahn), umschaltbar in
Skripten, Modell und Viewer. Leon hat den Kreislauf im Oasis-Showcase ausgearbeitet (Bauteile, Draufsicht,
Seitenprofil, Höhenschnitt, Höhenstufen 0 bis 5, Wasserspiegel über Fußboden, Wasserwege). Modell und Quelle stimmen
nicht überein, und wir sind uns über den Kreislauf nicht einig.
**Intent:** Ein einziger, richtiger Wasserkreislauf, auf den sich Ben und Leon einigen, der Schwerkraft nutzt und
im 3D-Modell, in Teileliste, Bestellliste und Bauteilbeschreibungen einheitlich und vollständig steht.
**Goal (prüfbar):** Jede Wasser-Komponente und jeder Wasserweg der Quelle ist im Gesamtmodell an der Stelle und Höhe
der Quelle gebaut (Abweichung je Wasserspiegel höchstens ±50 mm zum Wert der Quelle, Stufenreihenfolge 0 bis 5 exakt),
es gibt nur noch eine Variante, Teileliste/Bestellliste/Beschreibungen decken jedes neue Teil ab,
`check_latte` zeigt keine neuen Kollisionen durch den Kreislauf, und ein fremder Prüfer bestätigt das gegen eine
Soll-Ist-Tabelle aller Quell-Bauteile.

**Quelle:** `docs/quellen/oasis-showcase-2026-11-10/` (Commit f11a92d, SHA256 im README). Entscheidung D93, Wunsch W89.
**Arbeitsweise:** Agent-SDK-Runner auf API-Guthaben (`tools/agent-sdk-runner` der Werkbank), Sonnet 5.5, einfache
Aufgaben Haiku 5.5, kein Opus. Phasen wie bisher: Planer → Bau (Werkstatt, Montage, Daten, Viewer) → fremder Prüfer.
Ein Lauf zur Zeit (das Gesamtmodell baut immer nur einer). Der Orchestrator legt die Läufe in die Warteschlange,
liest Ergebnis und Verbrauch und meldet Ben Zwischenstände.

## Plan
| Phase | Lauf | Inhalt | Budget | Stand |
|---|---|---|---|---|
| P0 | im Planer-Lauf | WIP-Stand Ring B2 sichten und sichern (16 ungesicherte Dateien seit 05.11.) | – | offen |
| P1 | `docs/jobs/api/unify-1-planer.md` | Quelle auswerten → `data/oasis-soll.json` + R61; Soll-Ist-Abgleich; Bauplan in Runden U1…Un; Abweichungen zu Altbestand | 12 USD | offen |
| P2…n | je Runde ein Lauf (vom Planer festgelegt) | Werkstatt/Montage/Daten/Viewer je Runde, `build.sh`, `check_latte` in Kopie | je Runde laut Planer | offen |
| P-Prüf | eigener Lauf, nicht der Bauer | Soll-Ist-Tabelle aller Quell-Bauteile, Kollisionen, Listen | 8 USD | offen |

## Stand
- 10.11.2026: Quelle gesichert (f11a92d), D93 und W89 eingetragen, Planer-Auftrag geschrieben.

## Verbrauch (aus `tools/agent-sdk-runner/usage.jsonl`, je Lauf)
| Lauf | Modell | USD | Token Eingabe/Ausgabe/Cache gelesen/geschrieben |
|---|---|---|---|

## DoD
- [ ] Soll-Ist-Tabelle: alle Wasser-Bauteile und -Wege der Quelle gebaut, Wasserspiegel ±50 mm, Stufen exakt
- [ ] Nur noch eine Variante in Skripten, Modell, Viewer (A+/Ring-B2-Schalter entfernt oder auf eine Variante gesetzt)
- [ ] Teileliste, Bestellliste (Europa, Link, lebensmittelecht D85), Bauteilbeschreibungen für jedes neue Teil
- [ ] `check_latte`: keine neue Kollision durch den Kreislauf
- [ ] Fremder Prüfer PASS
- [ ] Abweichungen Altbestand ↔ Quelle vollständig notiert, Annahmen in `docs/decisions.md`
