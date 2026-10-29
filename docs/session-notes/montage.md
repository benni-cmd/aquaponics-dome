
## 2026-10-29 — von Orchestrator
M1.1 gesehen (442565e, check_latte 18/19) — weiter mit den 8 Kollisionen Beet gegen Strebe/Sockel, dann Tanks, NFT-Tische, Pflanzen als Instanzen.
Beleg: docs/next-steps-montage.md M1, docs/integration-board.md.
Zu tun: Kollisionen klaeren (Rangfolge Ben > OBJ-Zahlen > Bilder, Annahmen in docs/decisions.md), Pruefbild per scripts/archive_render.py in renders/history, Commit mit Pfad + Push, bei Kontext ueber 50 % clear_session self.

## 2026-10-29 — von Werkstatt
Leitungsteile-Bibliothek fertig (63 Teile `designs/components/lt_*.sc`, d20-d110, Reduziermuffen, Schlauch ID16/25, Verteiler d32) — fuer dich: Ports mit Art/DN/Lage maschinenlesbar in `scripts/workshop/leitung.ports(fname)`, Menschentabelle im Blatt.
Beleg: docs/parts/leitungsteile.md (Abschnitt Konvention, Port-Tabelle), check_leitungsteile.py 231/231.
Zu tun: Rohrnetz (M5) mit diesen Instanzen verlegen; Tisch-Verteiler d25/D16 bringt die Tisch-Klasse selbst mit.
