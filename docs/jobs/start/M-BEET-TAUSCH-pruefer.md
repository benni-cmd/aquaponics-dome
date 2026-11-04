# Start-Auftrag: Pruefer M-BEET-TAUSCH (14 Beete im Dom, Runde 67)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Pruefer, nur lesen und messen; du hast das Bauteil W40-BEET geprueft, die Montage aber nicht gebaut.

1. Grundlage: `docs/jobs/M-BEET-TAUSCH.md`, Abschnitt "Pruefpunkte (fremd nachmessbar)", Punkte 1 bis 5.
2. Gebaut in den Commits b361159, fa95a9f, 9ddb8b5, 290fe89, b47fc56 (und c0de8d9 fuer die W37-Auflage A5). Stand und Messwerte der Montage: `docs/packages/m-beet-tausch.md`, `docs/loop-state.md` Runde 67.
3. Eigene Pruefung zusaetzlich: (a) Die Montage meldet `check_latte` FAIL L6 (115 Leitungs-Kollisionen M10) als Leitungsthema; pruefe, ob darunter Beet-Koerper sind (dann Beet-Fehler) oder nur Leitungen (dann Altbestand, Vergleich mit Runde 66). (b) Befund Medienschutz Innenbeet (Netztopf 6,5 mm neben der Schutzachse, 5 mm Luft): bewerte, ob das eine Kollision oder nur knapp ist.
4. Fremde, nicht committete Aenderungen im Arbeitsbaum (`becken_dritt.sc`, `erdflaeche.sc`, `fundamentring.sc`, `haut_paneel_BBB.sc`, `pool_zentral.sc`, `schaltschrank.sc`, `strebe_a.sc`, `strebe_b.sc`, `tuer.sc`, `zulaufrohr.sc`, `zweitbecken.sc`, `viewer/extras.json`, `viewer/detail/`, Renders): nicht anfassen, nicht zuruecksetzen. Builds nur in einer Kopie im Scratchpad.
5. Ergebnis: `docs/jobs/pruefung/M-BEET-TAUSCH.md` mit PASS / PASS mit Auflagen / FAIL je Punkt, Messbefehl neben jeder Zahl. Commit nur dieser Datei per Pfad (`git -C . commit -m "..." -- <pfad>`, neue Datei vorher `git add -N`), Push. Danach STOPP.
