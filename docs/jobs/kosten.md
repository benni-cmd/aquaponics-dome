# Sitzungskosten (Messtabelle, Regel D74 Nr. 8)

Zweck: Schwellen der Kontextregeln aus Daten statt aus Schaetzung nachschaerfen (`docs/arbeitsweise-sitzungen.md` Abschnitt 4). Kontext-Formel [A, aus W39 gemessen]: Tokens ungefaehr 71.000 + 440 x Nachrichten; Prozent von 1 Mio. Fenster. "gemessen" = `get_usage` mit `session_id` waehrend des Laufs, "Formel" = aus der Nachrichtenzahl (`list_events`, limit 1) gerechnet. Fenster- und Wochenwerte sind Kontosummen und lassen sich nicht einer Sitzung zuordnen; deshalb vor und nach jeder Sitzung eintragen.

| Datum | Sitzung | Art | Nachrichten | Kontext | Art der Zahl | Woche vorher -> nachher | Bemerkung |
|---|---|---|---|---|---|---|---|
| 01.11. | R45 Hydraulik und Schlamm | Fachrecherche | 573 | etwa 33 % | Formel | 71 -> 75 (mit Werkstatt A und Orchestrator) | 6 Fragen, 75 Zuege, Web-Recherche |
| 01.11. | Werkstatt A (W36, 6 Teile) | Werkstatt | 609 | etwa 34 % | Formel | siehe oben | 2 Zuege (Teile liefen in grossen Zuegen) |
| 01.11. | Montage M10-S2R | Montage | 589 | etwa 33 % | Formel | 75 -> 77 | Build 66, 21 Zuege |
| 01.11. | Planer W37/W39 | Planer | 159 | etwa 14 % | Formel | 75 -> 77 | 4 Blaetter, 22 Zuege |
| 01.11. | Pruefer M10-S2R | Pruefer | 102 | etwa 12 % | Formel | 77 -> 77 | PASS mit Auflagen, fand 2 zu optimistische Aussagen |
| 01.11. | Werkstatt A2 (W39) | Werkstatt | 328 (laufend) | 21 % (214.584 Tokens) | gemessen | 77 -> 79 (mit Orchestrator) | laeuft noch |

Konto am 01.11. spaet: 5-Stunden-Fenster von 4 % auf 75 %, Woche von 71 % auf 79 % in etwa fuenf Stunden mit sieben Sub-Sitzungen und dem Orchestrator.
