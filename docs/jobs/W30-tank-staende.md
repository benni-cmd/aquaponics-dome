# W30 Tank-Staende verkleinern (Ben 31.10., D50)
Problem: Die Plattformen/Staende unter den Filtertanks wirken zu gross (Bens Screenshot): gross 977 x 976 x 98 bei Tank D 930, klein 706 x 707 x 73 bei D 673. Der Konus des Tanks ist auf Plattformhoehe viel schmaler (gross: Radius 570 - 226 = 344 mm, klein: 428 - 172 = 256 mm).
Ziel: Stand passt zum Tank: Plattform = Konusdurchmesser auf Plattformhoehe + 2 x 60 mm Rand (gross ca. 810, klein ca. 632); Beine, Querstreben, Fussplatten und Pumpentafel-Rippen passend verkleinert. Tank bleibt unveraendert, die Pumpentafeln (502 x 345 und 693 x 463) muessen noch passen und erreichbar bleiben.
Eingaben: `data/components/tank.json` (typen klein/gross/gross_t3: plat_l, plat_w, plat_t, plat_z0, leg_w, leg_h; Parameter rib_r_out 440, foot_plate 100, rib_*), `docs/parts/tank.md`, `scripts/workshop/check_tank.py`, Bens Bild. Nur diese Dateien lesen.
Schritte (einzeln committen):
1. Neue Plattformmasse als Parameter (`plat_margin` 60; Plattform aus Konusdurchmesser berechnet, nicht hart), Rippenradius `rib_r_out` und Beine mitziehen.
2. Pumpentafel/Kassette auf den Rippen pruefen (ist die Tafel breiter als die Plattform: Kassette seitlich am Stand statt unter der Plattform).
3. `check_tank.py` anpassen (Mass, Interferenz, Tafel passt), Blatt `docs/parts/tank.md` nachziehen, Render Seitenansicht und Schnitt per `scripts/archive_render.py --role werkstatt`.
Folge fuer die Montage: Fussabdruck wird kleiner (mehr Luft zu Nachbarn); Tank-Mittelpunkte bleiben, `tank_offsets` nur pruefen.
Nicht anfassen: `dome.sc`, Layout, andere Komponenten. Kein Pruefer-Lauf (Selbstcheck genuegt).
Ergebnis: Komponente, Blatt, Check, Bild, WIP-Commit je Schritt, Push, Zeile in `docs/workshop-state.md`.
