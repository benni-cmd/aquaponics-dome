# W24 Aussentisch mit 4 statt 3 Rinnen pruefen (Ben 30.10.)
Problem: Ben will mehr Pflanzflaeche, damit die Fischmenge naeher an Bens Tabelle kommt (Pflanzflaeche ist der Engpass, aquaponik-empfehlung.md). Idee: Aussenring 4 Rinnen je Tisch statt 3 (Mitte hat schon 4, Innen 2).
Ziel: Machbarkeit am Radialbudget (D28/D29) mit Zahlen: passt eine 4. Rinne, ohne Laufweg B < 600 (nie < 500), ohne Beet-Erreichbarkeit > 800 (einseitig) und ohne Kollision?
Eingaben: `docs/jobs/W17-radialbudget.md`, `W18-lochabstand.md`; `data/components/nft_tisch.json` (aussen: n 3, rinnen_abstand 288, Laengen 3051/2864/2676, Tischmitte ap_c 4973); `scripts/workshop/tisch_geom.py`, `check_nft_fit.py`; D28-D34.
Rechne: Rinnenabstand 288 mit 4 Reihen = zu breit (864 mm Mitte-Mitte plus Rinne); Variante Abstand 230-240 (4 Reihen ~700-740 mm + Rinne) pruefen: Topfabstand quer zu Nachbarrinne, Erreichbarkeit der inneren Reihe von der Laufwegseite (Tisch 1,3 m hoch), Tischbreite gegen Aussenportal 1030. Neue 4. Reihenlaenge aus den Apothemen (ca. 2490 mm), Topfzahl bei Lochabstand 200, Rinnenzahl 68 -> 76, Rinnenlaenge gesamt.
Ergebnis: `nft_tisch.json` bekommt die Variante `aussen4` als PARAMETER-Konfiguration (Standard bleibt aussen mit 3 bis Ben/Orchestrator entscheidet); `check_nft_fit` rechnet beide Varianten; Kurzbericht mit Zahlen: Topfzahl, Rinnenlaenge, Tischbreite, Laufweg B, Erreichbarkeit, Statik (Holm/Beine ausreichend?). KEINE Platzierung in dome.sc (Montage).
Nicht anfassen: dome.sc, Layout-Radien, Beete.
Pruefung: check_nft_fit beide Varianten, ein Render Querschnitt Wand-Beet-Tisch-Weg per archive_render.py. WIP-Commit mit Pfad, Push.
Danach: W25 Pumpen-Blatt (D38).
