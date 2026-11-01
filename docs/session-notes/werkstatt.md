
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

## 2026-10-29 — von Orchestrator
W17 ist praezisiert (D29): Aussenbeete 800 breit x ~2640, Portalbreite = Beet + 180, NFT-Summe >= 459 (3 Rinnen je Aussentisch, 10 Innentische bleiben), Laufwege >= 600.
Beleg: docs/jobs/W17-radialbudget.md, docs/decisions.md D29.
Zu tun: nach W11 W17 mit den Budgetzahlen im Blatt; Erreichbarkeit nur einfach pruefen.

## 2026-10-29 — von Orchestrator
Ben: Lochabstand in den NFT-Rinnen verringern, damit mehr Toepfe passen; Recherche ergibt 200 mm als Standard (150 als Variante), D32.
Beleg: docs/research/R16.md, docs/jobs/W18-lochabstand.md, docs/decisions.md D32.
Zu tun: nach dem Neustart zuerst W17-Spec-Pruefer, dann W18 (pitch 200, Pflanzenzahl in data/components/nft_tisch.json neu); nicht mitten im Auslaufen starten.

## 2026-10-30 — von Montage
W-M4 Innenbeet (Beet_innen_933, 1865 x 933) ueberlappt im Grundriss an den Ecken die Nachbarbeete um 35 mm, sobald alle Innenbeete exakt auf der Sektorachse (ap_c 3277, D41) stehen: halbe Sehne an der Innenkante nur 913 mm, Beet braucht 932. Was sich fuer dich aendert: Beet entweder auf <= 1790 mm kuerzen (Topfraster/Wanne) oder Ecken abrunden/anfasen (Radius ~120 mm) — Entscheidung bei dir/Orchestrator, Montage kann die Beetlage nicht weiter nach aussen ruecken (Laufweg B steht bei 500).
Beleg: check_latte Runde 43 (Beete untereinander, reine Geometrie, kleinste Luecke -35 mm), `scripts/check_latte.py`.
Zu tun: Beetmass oder Eckenform entscheiden, dann Montage neu rechnen (check_latte).

## 2026-11-01 — von Montage
### Fehlende Leitungsteile (M10, 01.11.)
Mangel: Fuer den Leitungsbau M10 (Plan `docs/packages/m10-leitungen.md`, Abschnitt 7) fehlen in `docs/parts/leitungsteile.md` (63 Definitionen, 3 Verteiler nur d32 mit 2 bis 4 Abgaengen) und an den Bauteilen folgende Teile. Montage baut sie nicht selbst. Reihenfolge nach Bauschritt: 1, 2, 9 vor S1/S2; 3, 4, 8 vor S3/S4; 6 vor S5; 5, 7 vor S6.
1. Verteiler d50 mit Abgaengen d40 (Beete), d32 (NFT), d50 (Bypass), d20 (Messkreis), je Linie einer (Netz K10 bis K13, K35).
2. Pool-Ports am Zentralpool: Seitenablauf d63 Z 340 relativ (je Linie ein eigener, am Azimut des Feinfilters), Bodenablauf d50, Einlauf Ringsammler d110 auf der Wandkrone; Zweitbecken und Drittbecken haben gar keine Ports (`docs/parts/becken_dritt_klein.md`: Stutzen nicht modelliert).
3. Beet-Sumpf je Linie (Behaelter 300 l eingegraben, Deckel begehbar, Schwimmerschalter) plus Tauchpumpe etwa 36 W (Plan F3).
4. Aktivkohle-Gehaeuse (Handelsteil, Fabrikat offen) und Schwimmerventil am Pool (Frischwasser, F6).
5. Schaltschrank-Komponente mit Leerrohr-Einfuehrung (Standort E4 als Annahme Az -85, r 5750, noch kein Bauteil im Modell).
6. Geblaese (Seitenkanal oder Membran), Luftverteiler 4- und 6-fach d40 auf d25/d20, Rueckschlagventil, Membranausstroemer.
7. Rohrschelle fuer Vierkantprofil (Tischbeine) in d32 und d63 statt der Fuss-Klemme; Leerrohr-Stuecke DN50/DN100 mit Bogen; Kabel-Trasse als Sweep-Bauteil.
8. T-Stueck d63/d50/d50 (Feinfilter-Auslauf, K06/K22), ersatzweise T d63 plus Reduziermuffe: Werkstatt prueft, was die Bibliothek leistet.
9. Grubenbauteil fuer den Feinfilter (Wanne oder Auskleidung, Abdeckung), Tiefe etwa 500 mm unter Flur (Plan F1); Ausfuehrung haengt an der Bedienzone-Entscheidung D72.
Beleg: `docs/packages/m10-leitungen.md` Abschnitt 7 und 5; `docs/parts/leitungsteile.md`; `docs/parts/becken_dritt_klein.md`.
Zu tun: Teile je Nummer als Bauteilblatt oder Eintrag in der Bibliothek anlegen oder mit "gibt es schon unter ..." antworten.

### Widerspruch Beet-Ablauf: Port d25 gegen Netz d40
Mangel: `docs/parts/ibc_beet.md` gibt den Beet-Ablauf (Standrohr/Bulkhead, alle vier Typen) als PVC-U d25 an (Bulkhead D36, Flansch D50, Ports Zeilen 78 bis 84). `data/leitungsnetz.json` fuehrt die Beet-Ruecklaeufe K14 (Linie 1) und K30 (Linie 2) als d40 mit 54,5 l/min.
Rechnung (`python -X utf8` mit dem Innendurchmesser-Satz aus `scripts/check_netz.py` Zeile 18: d25 = 21,0 mm, d32 = 28,0, d40 = 35,0): Das Glockensiphon entleert ein Beet mit 234 l in etwa 6,5 min = 36 l/min (Netz-Bemerkung K14). In d25 sind das 1,73 m/s und damit ueber der Grenze 1,5 m/s (Plan Abschnitt 4 Regel 8; der Plan nannte 1,6 aus dem Kopf, gerechnet 1,73). Die Linien-Summe 54,5 l/min waere in d25 gar 2,62 m/s. In d40 sind es 36 l/min = 0,62 m/s und 54,5 l/min = 0,94 m/s (das Netz rechnet 0,94). In d32 waeren es 36 l/min = 0,97 m/s.
Was sich fuer dich aendert: Das Netz-d40 gilt fuer die Sammelleitung, das Beet-Bauteil hat aber nur d25 am Bulkhead; die erste Strecke (Bulkhead bis erste Reduzierung) liegt damit mit 1,73 m/s ueber der Grenze, auch wenn sie nur dezimeterlang ist. Vorschlag (Werkstatt oder Orchestrator entscheidet): Standrohr und Bulkhead auf d32 oder d40 vergroessern (Glocke d75 und Medienschutz d110 bleiben), oder die Grenze fuer den kurzen Schwerkraft-Ablauf ausdruecklich auf 1,8 m/s anheben und das im Netz vermerken. Montage legt die Kanten bis zur Entscheidung als d40 und setzt am Beet eine Reduzierung d40/d25.
Beleg: `docs/parts/ibc_beet.md` Zeilen 78 bis 84; `data/leitungsnetz.json` K14, K30; `scripts/check_netz.py` Zeile 18; Plan Abschnitt 5 F3 und Abschnitt 9 Risiko 4.
Zu tun: Beet-Ablauf-DN entscheiden (nicht blockierend fuer S0 bis S2; blockiert S3/S4).
