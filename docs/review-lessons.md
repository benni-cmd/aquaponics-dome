# Lernprotokoll der Pruefung (Besitzer: Orchestrator; Werkstatt und Integrator duerfen anhaengen)

| Datum | Klasse | Was schiefging | Ursache | Neue Regel |
|---|---|---|---|---|
| 29.10. 03:55 | nft_rinne | Rinne bekam zwei versetzte Lochreihen (y = +-30), Mittelrippe, Salatkoepfe standen neben den Loechern | Kritiker bekam Referenzausschnitt mit mehreren Rinnen; Zickzack zwischen Nachbarrinnen wurde der Einzelrinne zugeschrieben; Umsetzung ohne Triage | Merkmale, die erst mehrere gleiche Teile ergeben (Versatz, Abstand, Zickzack), gehoeren zur Elternklasse; Referenzausschnitt nur der Einzelklasse; Kontextpaket; Triage vor jedem Umbau; Vorpruefung (Lochreihen je Rinne = 1) |
| 29.10. 03:57 | nft_rinne | Pflanzen sassen nicht in den Topfloechern | Plazierung der Pflanzen ohne Bezug zu den Lochpositionen | Pflanze/Netztopf sitzt im Loch (Position aus Lochraster), Pruefzahl: Abstand Pflanzenmitte zu Lochmitte = 0 |
| 29.10. 04:50 | nft_rinne | (Werkstatt) Vorpruefung fehlte: Loechermodell (zwei Halbzylinder je Bohrung) zaehlt doppelt, wenn man Flaechen statt Mittelpunkte zaehlt | Erste Fassung des Pruefskripts zaehlte Zylinderflaechen | Bohrungen ueber distinct Achs-Ursprung zaehlen (`check_nft_rinne.py`) |
| 29.10. 04:50 | salatkopf | Kritiker widersprachen sich in Runde 1 und 2 (flacher / hoeher) | Referenzbild zeigt Salat von der Seite verdeckt, Kritiker schaetzt Proportion | Proportion nur ueber Zahl im Kontextpaket vorgeben (Breite 110-120, Hoehe 55-65 bei M) |
