# R47: Wasserkreislauf und Verteilung neu denken — Machbarkeitsprüfung (Wunsch W51)

**Auftrag:** `docs/jobs/R47-wasserkreislauf-neu.md` · **Bearbeitet:** 02.11.2026 · **Rolle:** Fachrecherche, nur lesen/rechnen/schreiben; nichts umgesetzt, kein Modell, keine Netzliste, kein Roadmap-Eintrag geändert.
**Herkunft:** [Q] Quelle · [E] eigene Rechnung (`python -X utf8 scripts/r47_rechnung.py`, liest `data/leitungsnetz.json`) · [A] Annahme. Z-Werte relativ zum Innenboden (Skript-Z minus 400). Schwache Belege sind als „Kandidat“ oder „offen“ markiert.

**Problem/Intent/Goal:** Ben will vor dem Weiterbau wissen, ob eine hängende Ringleitung, Anlagenteile näher am Kreislauf, mehr Schwerkraft und ein verstopfungssicheres Flood-and-Drain besser sind als der heutige Plan (Verteiler d50 je Linie, Beete d40, NFT d32, Rücklauf über Halbringe d110 und Sektorsammler d63). Ziel: Einschätzung je Idee, Zahlenvergleich A/B/C, Empfehlung, Folgen für M10 S3–S7 und W37.

## Gesamturteil (zehn Zeilen)

1. **Empfehlung: Variante A (heutiger Plan, gestrafft). Variante B (ein Ring für alles) nicht bauen. Variante C (Ring nur für Beete) nur, wenn die Gräben für K11 zum Problem werden.**
2. **Hängender Ring: teilweise machbar.** Statisch einfach (Ring d90 voll 6,8 kg/m, 146 kg gesamt, 12 Stützen, Durchhang 3–9 mm), hydraulisch ein Rückschritt: Der Biofilter-Überlauf (Z 1570) liegt 530 mm **unter** der Ring-Unterkante (Z 2100). Schwerkraftspeisung braucht den Biofilter 725 mm höher; Druckspeisung hebt die Pumpenhöhe von 2,0 auf 2,83 m.
3. **Zahlen (A / B / C):** Pumpen elektrisch 430 / 548 / 503 W; Zulauf-Verteilrohr 80 / 109 / 81 m; Formteile+Armaturen 214 / 220 / 232; Pumpstufen 2 / 2 / 3; Gangkreuzungen Zulauf (Gräben) ≈ 1 je Außenbeet / 0 / 0 [E, A].
4. **Der Ring spart keine Teile:** 38 Abnehmer (14 Beete, 24 Tische) brauchen jeder ein T, Bögen, Hahn, Reduzierung. Der Ring ersetzt nur die zwei Verteilstränge je Linie und kostet 28 m mehr Rohr.
5. **Der einzige echte Gewinn des Rings:** Beete ohne Graben über die Gänge erreichen. Das lässt sich billiger lösen (Abschnitt 2 und 5).
6. **Teile nah am Kreislauf:** Der Hauptkreislauf ist bereits kurz (eine Pumpstufe, dann alles frei). Größte offene Rohrmenge ist der Rücklauf der Beete (K14, ca. 59 m d50 [E]); Beet-Sumpf im Beet-Schwerpunkt spart rechnerisch 14,5 m. „Sumpf als Saugsumpf der Hauptpumpen“ ist verworfen (Saughöhe).
7. **Schwerkraft:** wird heute schon genutzt (Heber Pool→Filter, Biofilter→Verteiler→Beete/NFT→Pool frei). Gepumpt wird nur zweimal: Hauptpumpen (2,0 m) und Beet-Sumpf (1,47 m), Letzteres zwingend, weil der Beetablauf (Z −100) 615 mm unter dem Spiegel (Z 515) liegt.
8. **Flood-and-Drain:** Bens Wunsch ist im Bauteil `ibc_beet` **schon erfüllt** (Siebboden 8 mm auf 60-mm-Klötzen, 640 l Wasserraum darunter, Siphon leert bis zum Boden). Zu ändern sind nur drei Kleinigkeiten: Medienschutz-Löcher 12 mm gegen Korn ab 8 mm, Reinigungszugang, Korn ≥ 12 mm festlegen.
9. **Folgen:** M10 S3–S7 und W37 können mit A **unverändert** weiterlaufen; W37 (Beet-Sumpf, Schlammfass) bleibt. Bei B/C entfielen K11/K12 als Rohrstränge, es kämen Biofilter-Anhebung oder Booster-Pumpe, Stützen und ein neues Bauteil „Ringstück“ dazu.
10. **Offen:** Stützen-Statik (Kragarm 2,2 m), Gangkarte für Stützenstandorte (nicht gerechnet), Pumpenkennlinien, Frost bei Heizungsausfall (Standort offen). Entscheidung liegt bei Ben.

<!-- ENDE -->
