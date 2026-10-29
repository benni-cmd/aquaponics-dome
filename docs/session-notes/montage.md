
## 2026-10-29 — von Orchestrator
M1.1 gesehen (442565e, check_latte 18/19) — weiter mit den 8 Kollisionen Beet gegen Strebe/Sockel, dann Tanks, NFT-Tische, Pflanzen als Instanzen.
Beleg: docs/next-steps-montage.md M1, docs/integration-board.md.
Zu tun: Kollisionen klaeren (Rangfolge Ben > OBJ-Zahlen > Bilder, Annahmen in docs/decisions.md), Pruefbild per scripts/archive_render.py in renders/history, Commit mit Pfad + Push, bei Kontext ueber 50 % clear_session self.

## 2026-10-29 — von Werkstatt
Leitungsteile-Bibliothek fertig (63 Teile `designs/components/lt_*.sc`, d20-d110, Reduziermuffen, Schlauch ID16/25, Verteiler d32) — fuer dich: Ports mit Art/DN/Lage maschinenlesbar in `scripts/workshop/leitung.ports(fname)`, Menschentabelle im Blatt.
Beleg: docs/parts/leitungsteile.md (Abschnitt Konvention, Port-Tabelle), check_leitungsteile.py 231/231.
Zu tun: Rohrnetz (M5) mit diesen Instanzen verlegen; Tisch-Verteiler d25/D16 bringt die Tisch-Klasse selbst mit.

## 2026-10-29 — von Orchestrator
Ben sieht NFT-Tische ineinander kollidieren und Tischbeine in den Substratbeeten — in `check_latte` fehlen diese Pruefungen; die Werkstatt baut Passungsvarianten (Auftrag W16, Entscheidung D18, Portalrahmen, Rinnenlaenge je Reihe).
Beleg: docs/decisions.md D18, docs/jobs/W16-nft-tisch-passung.md.
Zu tun: in `scripts/check_latte.py` Pruefungen Tisch/Tisch (Footprints je Ring, Abstand >= 100 mm) und Tischbein/Beet (Bein ausserhalb der Beet-Rechtecke) ergaenzen; NFT-Tische erst mit den W16-Varianten als Instanzen setzen, nicht mit den alten.

## 2026-10-29 — von Orchestrator
Bens Tabelle (reference/Kuppelberechnung-neu-2.xlsx) bestaetigt die Zahlen; Pool-Tiefe wird 2200 statt 2340 (D26); Pflanzenartmodelle hinten, Technik/Rohre/Schlaeuche haben Vorrang (D27).
Beleg: docs/research/R15.md, docs/decisions.md D26 D27.
Zu tun: `pool_depth_total` auf 2200 setzen (Pool-Wanne/Erdtasche), dann M4/M5 (Wasserweg, Rohre, Schlaeuche) vor weiteren Pflanzenarbeiten.

## 2026-10-29 — von Orchestrator
Ben verlangt Laufwege >= 0,5 m zwischen den Pflanzringen und kluge Platznutzung — das ersetzt D24/D25 durch ein Radialbudget (D28); neuer Schritt M7 vor M3.
Beleg: docs/next-steps-montage.md M7, docs/decisions.md D28, docs/jobs/W17-radialbudget.md.
Zu tun: M7 abarbeiten (Radien setzen, scripts/check_walkways.py, Tuer-Gang >= 900); die Werkstatt baut dazu kuerzere Aussenbeete und neu angepasste Tische (W17).

## 2026-10-29 — von Orchestrator
M7 ist praezisiert (D29): Laufwege >= 600 (nie < 500), Aussenbeete 800 breit, Tuer-Gang >= 900, alles erreichbar (nicht zu tief pruefen); NFT-Mindestzahl 459 bleibt bindend.
Beleg: docs/next-steps-montage.md M7, docs/decisions.md D29, docs/jobs/W17-radialbudget.md.
Zu tun: M7 nach den Budgetzahlen umsetzen; aktuell liegen die Aussentische (D25, 497 nach innen) im Laufweg B, das ist der Grund fuer "zu eng".
