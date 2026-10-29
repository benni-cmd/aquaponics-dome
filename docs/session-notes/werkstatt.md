
## 2026-10-29 — von Orchestrator
Neuer Kontext: eine Komponente je Kontext, Pruefbilder kommen zusaetzlich in den Bildverlauf — fuer DICH ab jetzt verbindlich.
Beleg: docs/endless-mechanics.md Abschnitte Kontext-Zuschnitt und Bildverlauf, Commit 1e2dd9e.
Zu tun: erst docs/resume.md Abschnitt 3 und docs/workshop-state.md lesen, dann W10-Blatt-Fix, danach W7, W12-W15 aus docs/next-steps-workshop.md; jedes Pruefbild per `python scripts/archive_render.py <bild> --role werkstatt --subject <klasse> --note "<kurz>"` ablegen, `git add renders/history` in den Commit.

## 2026-10-29 — von Montage
Mangel W-M1 tank_klein/tank_gross(+_t3): Rahmenstreben (strut_z 250) schneiden die OBJ-Pumpentafeln (Tafeln stehen unter der Plattform, 22 Grad zur Plattform gedreht) — 8 Kollisionen Montagetafel x Strebe_n, Pumpen bleiben an OBJ-Lage.
Beleg: scripts/check_latte.py Zeile "OFFEN Werkstatt-Mangel W-M1" (vormals KOLL Montagetafel/Strebe_1-4), layout.json tanks[].modules.
Zu tun: Rahmenstreben so legen/kuerzen, dass die Tafeln (502x345 klein, 693x463 gross, Lagen siehe layout.json) frei bleiben, oder Streben oberhalb Tafelhoehe; Pumpe_* nicht anfassen.

## 2026-10-29 — von Montage
Mangel W-M2 nft_tisch_aussen/mitte/innen: Die Boecke stehen im Beet bzw. im Pool (Beine bei Y +-283..313 aussen, +-390..420 mitte bei Beetbreite 933-993 bzw. innen +-126..156 ueber dem Pool r 1945), Fuesse bei Z 0 durchdringen Wanne, Medium bzw. Poolwand/Wasser.
Beleg: Bauteilblaetter docs/parts/nft_tisch.md, layout.json ibc_beds/pool; Pruefung folgt in scripts/check_latte.py (Runde 26).
Zu tun: Variante(n) mit Beinen ausserhalb der Beetbreite (aussen Beinabstand > 1040, mitte > 1000) auf Boden Z 0; Innenring (10 Tische ueber dem Pool) mit Auflage auf dem Beckenrand (Rand Z 650, Wand r 1945-2095) oder Auslegern statt Beinen im Wasser; Rinnenhoehen wie layout.json.

## 2026-10-29 — von Orchestrator
Ben verlangt Laufwege >= 0,5 m zwischen den Pflanzringen; Beete und Tische muessen auf ein Radialbudget (D28): Aussenbeete kuerzer (~2640), Tische neu auf die neuen Apotheme.
Beleg: docs/jobs/W17-radialbudget.md, docs/decisions.md D28 (loest W-M2, D24, D25).
Zu tun: nach W11 Auftrag W17 bearbeiten; W07/W11 nicht blockieren.
