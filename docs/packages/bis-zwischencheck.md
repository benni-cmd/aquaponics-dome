# Paket: Bis zum Zwischencheck (Ben 05.11.2026, D81)

**Problem:** Viele Roadmap-Schritte vor dem Zwischencheck warten auf Bens Entscheidungen (E20, E13, E19 und weitere).
**Intent:** Ben will beim Zwischencheck ein moeglichst vollstaendiges Modell sehen; fehlende Entscheidungen werden als Annahme getroffen und dort bestaetigt.
**Goal:** Alle Roadmap-Schritte mit Phase `vor_zwischencheck` sind erledigt oder ausdruecklich benannt geparkt; jede Annahme steht in D81 und im Zwischencheck-Bericht.

## Plan (Wellen; Gesamtmodell baut nur eine Sitzung zugleich, sonst bis 7 parallel, D80)
1. Modell-Kette (nacheinander): check_latte 69 -> Pruefer Luft A -> Montage Strebe + Werkstoffe -> Montage Luft Teil B (E13-Annahme) -> M10-S2N -> M10-S3 -> M10-S4 (mit Beet-Sumpf) -> M10-S5 Rest -> M10-S6 -> M10-S7 -> CHECK; je Montage ein fremder Pruefer.
2. Parallel dazu: Planer-Buendel M10 nach A+ (Blaetter S2N bis S7 auf A+ und D81), Werkstatt W37-1 Beet-Sumpf/Schlammfass, SPECS-R45 + HEBER-SKRIPT, N-PREIS-PRUEF (Recherche -> Werkstatt -> Pruefer), Auflagen Detailansicht.
3. Danach: V-MESS (Viewer Messstellen, Export kleiner), W65-Tabelle, Zwischencheck-Bericht mit allen Annahmen.
4. Geparkt: M10-S2V Subtank (Ben), E16/E17, R46 nach dem Zwischencheck.

## Stand
- 05.11. ~01:00: Paket angelegt, Annahmen D81, Welle 2 startet.

## DoD
Roadmap `vor_zwischencheck` ohne offene Bauschritte; Pruefer-Befunde je Montage; Zwischencheck-Bericht mit Annahmen-Liste; Commit und Push je Schritt.
