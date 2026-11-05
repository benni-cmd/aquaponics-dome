# Start-Auftrag R60: Stärkere Wasserpumpe mit Venturi statt Gebläse und Luftleitungen?

**Rolle:** Fachrecherche (nur lesen und schreiben). Kein Modellbau, keine SolidCraft-Läufe, keine Käufe, keine Anmeldungen, keine Formulare. Der PC soll entlastet bleiben (Ben 05.11. abends).
**Ergebnis:** `docs/research/R60-pumpe-statt-geblaese.md` im Format wie R54 und R55, danach commit und push (nur Pfad-Commits: `git commit -m "..." -- <pfad>`).

## Problem, Intent, Goal
- **Problem:** Ben schlägt vor (05.11.2026): eine stärkere Wasserpumpe nehmen, die im Normalbetrieb mit niedriger Grundlast läuft und genug Druck für Venturi-Injektoren hat. Dann entfallen Luftkompressoren (Linear-Membranpumpen), Luftverteiler und Luftleitungen. R54 und R55 haben Venturi abgelehnt, weil der heutige Pumpendruck (0,2 bis 0,4 bar) zu klein ist und Luft mit der Pumpe ausfällt.
- **Intent:** Weniger Teile und weniger Leitungen (Designprinzip 3), ohne die Fische zu gefährden (Designprinzip 9).
- **Goal:** Eine belegte Gegenüberstellung "Gebläse + Scheiben (heute)" gegen "stärkere Pumpe + Venturi" mit Strom pro Jahr, Teilezahl, Kosten, Sauerstoffbilanz (46 bis 71 g O2/h), Ausfallsicherheit und einer Entscheidungsfrage an Ben.

## Fragen
1. Welche Pumpe (lebensmittelecht/fischtauglich, in Europa bestellbar, Link) liefert 220 l/min Umlauf plus Injektor-Druckdifferenz 0,7 bis 1,4 bar? Leistungsaufnahme bei Volllast und bei gedrosselter Grundlast (Frequenzumrichter/ECM, Affinitätsgesetze), Wirkungsgrad.
2. Wie viel Luft (l/min) und Sauerstoff (g/h) bringen konkrete Injektoren (Mazzei 584/784/1078 oder EU-Gleichwertige) bei diesem Druck und Durchfluss? Datenblatt lesen, nicht schätzen. Reicht das für 71 g O2/h bei 2,17 m Pooltiefe und 28 °C?
3. Strom pro Jahr: Pumpe + Venturi gegen heutige Pumpen (288 W) + Gebläse (204 W). Gilt "niedrige Grundlast", wenn das Venturi dauernd Druck braucht?
4. Ausfall: Pumpe weg = Wasser und Luft weg. Welche Notluft bleibt nötig (Akku-Notpumpe 12 V, Reservepumpe N+1)? Wie viele Teile entfallen dann netto wirklich?
5. Verstopfung, Lärm, Wartung, CO2-Entgasung, Gasübersättigung (Druck-Injektion) — je mit Quelle oder als Lücke.

## Regeln
- Jede Aussage zwei unabhängige Quellen, sonst als [Q-Treffer] oder Lücke markieren; jede Rechnung mit Befehl (`python -X utf8 -I -c ...`).
- Pflicht-Check `docs/designprinzipien.md` (alle 10 Punkte) am Ende.
- Eingaben: `docs/research/R54-venturi-belueftung.md`, `docs/research/R55-wasserquelle-venturi.md`, `docs/research/R45-hydraulik-auslegung.md` Abschnitt 4, `docs/research/R59-tauchpumpe.md`, `data/system-specs.json`.
- Kein Parameter in `data/` ändern; Empfehlung nur als Entscheidungsfrage.
