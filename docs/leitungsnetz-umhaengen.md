# Netzliste umhaengen: Linie 1 = Ost, Linie 2 = West (M10, Stand 01.11.2026)

Rolle Montage, Schritt M10-S0. Die Netzliste `data/leitungsnetz.json` (Version 2) gehoert dem Orchestrator und bleibt unveraendert; diese Liste sagt nur, welches Netz-Etikett an welche Modell-Instanz gehaengt wird (Entscheidung E2 im Freigabe-Abschnitt von `docs/jobs/M10-leitungen.md`, Plan `docs/packages/m10-leitungen.md` Abschnitt 3).

## Problem
Die Netzliste fuehrt `absetzer_1` und `pumpe_klein_1`/`_2` zu Linie 1 und `absetzer_2` und `pumpe_klein_3`/`_4` zu Linie 2. Im Modell steht aber der erste Absetzer samt seinen zwei kleinen Pumpen in der West-Haelfte, der zweite in der Ost-Haelfte. Wer die Etiketten nach Instanznummer verbindet, schliesst Pool-Bodenablauf, Absetzer und Pumpen der falschen Seite an.

## Regel fuer Ost und West
Die Tuerachse (Az -54 / 126, `data/params.json` `door_az`) teilt die Kuppel. **Ost = Linie 1** liegt von Az -54 gegen den Uhrzeigersinn bis 126 (Sektoren Az -35,7 / 0,3 / 36,3 / 72,3 / 108,3), **West = Linie 2** von 126 bis 306 (Sektoren 144,3 / -179,7 / -143,7 / -107,7 / -71,7). Das Mass `rel` unten ist `(Az + 54) mod 360`; 0 bis 180 heisst Ost.

## Zuordnung (Instanz-Lagen aus `scripts/dome-script.json`, `occurrence.move`)
| Modell-Instanz | x / y mm | Az / r | rel | Seite | Netz-Knoten (neu) | Hinweis |
|---|---|---|---|---|---|---|
| Tank_gross:1 | 3372 / -300 | -5,1 / 3385 | 49 | Ost | biofilter_1 | stimmt schon (`mk_l1` Bauteil Tank_gross:1) |
| Tank_gross_t3:1 | -458 / -3334 | -97,8 / 3365 | 316 | West | biofilter_2 | stimmt schon (`mk_l2` Bauteil Tank_gross_t3:1) |
| Pumpe_gross:1 | 3373 / -765 | -12,8 / 3458 | 41 | Ost | pumpe_gross_1 | stimmt schon |
| Pumpe_gross:2 | 3371 / 166 | 2,8 / 3375 | 57 | Ost | pumpe_gross_2 | stimmt schon |
| Pumpe_gross:3 | -313 / -2891 | -96,2 / 2908 | 318 | West | pumpe_gross_3 | stimmt schon |
| Pumpe_gross:4 | -601 / -3776 | -99,0 / 3824 | 315 | West | pumpe_gross_4 | stimmt schon |
| **Tank_klein:2** | 2842 / -1652 | -30,2 / 3287 | 24 | Ost | **absetzer_1** | Netz-Linie 1 (Ost); Modell-Instanz :2 steht in Ost, nicht :1 |
| **Tank_klein:1** | 906 / -3944 | -77,1 / 4047 | 337 | West | **absetzer_2** | Netz-Linie 2 (West); Instanz :1 steht in West |
| **Pumpe_klein:3** | 2844 / -1287 | -24,4 / 3121 | 30 | Ost | **pumpe_klein_1** | Linie 1; Zulauf-Pumpe der Kanten K03/K04 |
| **Pumpe_klein:4** | 2840 / -2016 | -35,4 / 3483 | 19 | Ost | **pumpe_klein_2** | Linie 1, Reserve |
| **Pumpe_klein:1** | 1019 / -3598 | -74,2 / 3740 | 340 | West | **pumpe_klein_3** | Linie 2; Zulauf-Pumpe der Kanten K19/K20 |
| **Pumpe_klein:2** | 793 / -4291 | -79,5 / 4363 | 334 | West | **pumpe_klein_4** | Linie 2, Reserve |

Fett = muss umgehaengt werden: die Netz-Knoten behalten ihre Namen und Linien, aber wer sie nach Instanznummer ans Modell haengt (absetzer_1 = Tank_klein:1 usw.) trifft die falsche Seite. Richtig ist die Zuordnung der Tabelle, also absetzer_1 und pumpe_klein_1/2 nach Ost, absetzer_2 und pumpe_klein_3/4 nach West. Die zwei grossen Tanks und alle vier Pumpe_gross stehen schon richtig.

## Kurzliste fuer den Orchestrator
- `absetzer_1` -> Modell `Tank_klein:2` (Ost, Linie 1); `absetzer_2` -> `Tank_klein:1` (West, Linie 2).
- `pumpe_klein_1`, `pumpe_klein_2` -> `Pumpe_klein:3`, `Pumpe_klein:4` (Ost); `pumpe_klein_3`, `pumpe_klein_4` -> `Pumpe_klein:1`, `Pumpe_klein:2` (West).
- `biofilter_1` -> `Tank_gross:1`, `biofilter_2` -> `Tank_gross_t3:1`, `pumpe_gross_1..4` -> `Pumpe_gross:1..4`: unveraendert.
- Die Paarung innerhalb einer Linie (welche von zwei gleichen Pumpen als 1 oder 2 gilt, z. B. Pumpe_klein:3 oder :4 als pumpe_klein_1) folgt hier der Instanznummer-Reihenfolge; sie ist frei und wird in S2 nach der kuerzeren Trasse nachgezogen (nur Namen).

## Nicht in der Netzliste umzuhaengen (Hinweise)
- **Feinfilter** `feinfilter_1`/`_2` haben noch keine Modell-Instanz (S1 setzt sie): Ost A (x 3925 / y 825, Linie 1) und West B (x -1575 / y -3175, Linie 2) nach D72.
- **Puffer klein** `Puffer_Klein:1` (x 1739 / y -2147, Az -51, rel 3) liegt auf der Ost-Seite, nur 3 Grad neben der Tuerachse. Die Netzliste haengt ihn an `verteiler_1` (K35, Linie 1), das passt zu Ost. Wegen der Lage am Tuergang ist jede Trasse dorthin in S5 einzeln gegen die Gangkarte zu pruefen.
- **Zweitbecken** (Az -54, auf der Tuerachse) haengt per K33 an `ruecklauf_1` (Linie 1, Ost); **Drittbecken** `Becken_Dritt:1` (Az -30, rel 24) liegt in Ost. Keine Aenderung.

Geprueft gegen: `scripts/dome-script.json` (occurrence.move aller Tank-, Pumpen- und Puffer-Instanzen, Azimute mit atan2 und Tuerachse -54 gerechnet), `data/leitungsnetz.json` Version 2 (Knoten `linie`, Kanten K03/K04/K19/K20), `data/messstellen.json` (`mk_l1`/`mk_l2`), `docs/packages/m10-leitungen.md` Abschnitt 3 · Offen: Orchestrator uebernimmt die Umhaengung in die Netzliste (E2); Paarung innerhalb der Linie in S2.
