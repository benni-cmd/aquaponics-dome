# Sitzungskosten (Messtabelle, Regel D74 Nr. 8)

Zweck: Schwellen der Kontextregeln aus Daten statt aus Schaetzung nachschaerfen (`docs/arbeitsweise-sitzungen.md` Abschnitt 4). Kontext-Formel [A, aus W39 gemessen]: Tokens ungefaehr 71.000 + 440 x Nachrichten; Prozent von 1 Mio. Fenster. "gemessen" = `get_usage` mit `session_id` waehrend des Laufs, "Formel" = aus der Nachrichtenzahl (`list_events`, limit 1) gerechnet. Fenster- und Wochenwerte sind Kontosummen und lassen sich nicht einer Sitzung zuordnen; deshalb vor und nach jeder Sitzung eintragen.

| Datum | Sitzung | Art | Nachrichten | Kontext | Art der Zahl | Woche vorher -> nachher | Bemerkung |
|---|---|---|---|---|---|---|---|
| 01.11. | R45 Hydraulik und Schlamm | Fachrecherche | 573 | etwa 33 % | Formel | 71 -> 75 (mit Werkstatt A und Orchestrator) | 6 Fragen, 75 Zuege, Web-Recherche |
| 01.11. | Werkstatt A (W36, 6 Teile) | Werkstatt | 609 | etwa 34 % | Formel | siehe oben | 2 Zuege (Teile liefen in grossen Zuegen) |
| 01.11. | Montage M10-S2R | Montage | 589 | etwa 33 % | Formel | 75 -> 77 | Build 66, 21 Zuege |
| 01.11. | Planer W37/W39 | Planer | 159 | etwa 14 % | Formel | 75 -> 77 | 4 Blaetter, 22 Zuege |
| 01.11. | Pruefer M10-S2R | Pruefer | 102 | etwa 12 % | Formel | 77 -> 77 | PASS mit Auflagen, fand 2 zu optimistische Aussagen |
| 01.11. | Werkstatt A2 (W39) | Werkstatt | 557 (Ende) | 21 % bei 328 Nachrichten, 31 % bei etwa 460 (gemessen), Ende etwa 33 % | gemessen und Formel | 77 -> 80 (mit Orchestrator) | 9 Teilgruppen in 15 Dateien, rund 1 Stunde 40 Minuten |
| 01.11./02.11. | Orchestrator (diese Sitzung) | Orchestrator | etwa 1.100 | 56 % (564.031 Tokens gemessen) | gemessen | 71 -> 80 | Wechsel an eine frische Orchestrator-Sitzung empfohlen (Regel D74 Nr. 7: ab etwa 50 %) |

Konto am 01.11. spaet: 5-Stunden-Fenster von 4 % auf 75 %, Woche von 71 % auf 79 % in etwa fuenf Stunden mit sieben Sub-Sitzungen und dem Orchestrator.

## Zwischenspeicher-Messung (01.11.2026, `scripts/messung_sitzungs_cache.py`)
| Abstand zum vorigen Aufruf | Aufrufe | gelesen aus dem Zwischenspeicher | neu geschrieben je Aufruf |
|---|---|---|---|
| unter 5 min | 6.370 | 99,2 % | 2.648 |
| 5 bis 30 min | 373 | 98,1 % | 6.459 |
| 30 bis 60 min | 45 | 79,1 % (unter 60 min warm, ab 68 min kalt) | 47.877 |
| ueber 60 min | 81 | 8,8 % | 281.446 |
Schluss: Der Zwischenspeicher haelt etwa eine Stunde. Wecken nach laengerer Pause (Nacht) kostet einmalig den ganzen Kontext; Regel D74 Nr. 1 (d).
