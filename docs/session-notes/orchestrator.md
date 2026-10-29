
## 2026-10-29 — von Werkstatt
W10 fertig (Leitungsteile-Bibliothek, 63 `lt_*.sc`, check 231/231 PASS, Spec-Pruefer Runde 3 PASS knapp, 4 kleine Befunde eingearbeitet) — fuer dich offen: (1) Wandstaerken der Klassenblaetter (Tank/Pumpe/Tisch/Beet 2-3 mm) gegen SDR 21 der Bibliothek, (2) Farbzuordnung Schlauch-ID16/ID25 (Annahme hellblau/dunkelblau), (3) Scope-Card "Kupplung per parts.insert" nicht eingehalten, (4) Tisch-Verteiler d25/D16 bleibt Tisch-Klasse, (5) tank.md 73 "d40 = DN30" statt DN32.
Beleg: docs/parts/leitungsteile.md (Abschnitte Offene Fragen, Herkunft), docs/workshop-log.md Runden 1-3.
Zu tun: Punkte 1-3 entscheiden; keine vierte Pruefrunde gelaufen (Runde-3-Befunde nur Text/Herkunft).

## 2026-10-29 — von Werkstatt
W12 Pumpe fertig (4 Spec-Runden, Runde 4 PASS knapp, check_pumpe 34/34, Bilder im Verlauf) — fuer dich offen: (1) D16-Reste in scope-cards.md 34/37, components.md 22, detail-standard.md 28/40, hydraulics.md 51/61 ("Filtermodul"), (2) 8 Pumpenmodule (OBJ) gegen 4 Pumpen A/B + 2 Siebe in hydraulics.md, (3) Untergrund der Standwinkel (Boden ist Erde), (4) Modellfix: Sockel jetzt 11 mm (Kopf ragte in die Konsole), Konsole als Winkel; Ports unveraendert.
Beleg: docs/parts/pumpe.md (Offene Fragen), docs/workshop-log.md Runden 2-4.
Zu tun: Punkte 1-2 entscheiden/bereinigen; W07-salatkopf laeuft als Naechstes.

## 2026-10-29 — von Werkstatt
W16 NFT-Tische Rev. B fertig (D18/D20): Rinnenlaenge je Reihe, Portal-/Auslegerbock, schraege Rohre, 466 Topfloecher, check_nft_tisch 124/124, check_nft_fit 36/36 (Ecken-Luft 171-190 mm), Bild-Kritiker PASS, Spec-Pruefer FAIL -> 5 Befunde eingearbeitet (nicht erneut geprueft, nur Text/Herkunft) — fuer Integrator/Montage: Platzierung yaw = Azimut + 90 Grad in vollen 360 Grad (layout.json yaw nur modulo 180: aussen Sektor 3, 6-9 und Mitte/innen 7-9 liegen dort bei az - 90, dort Tisch um 180 Grad gedreht setzen); Tischmitte = Beetmitte (Radius ibc_beds), Y radial nach innen.
Beleg: docs/parts/nft_tisch.md (Abweichung, Offene Fragen), docs/workshop-log.md (Runden 1-2), renders/components/nft_passung/.
Zu tun: Orchestrator: Statik Ausleger/Fundament (Boden Erde), Pool-Wand 150 (Platzhalter) und Durchgangsbreite Gehweg klaeren; Montage: Tische mit den 9 Rinnenvarianten nft_rinne_<typ>_r<k>.sc und neuer Lage platzieren.
