# Pruefung M-BEET-TAUSCH (Pruefer, 04.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md` und `docs/jobs/start/M-BEET-TAUSCH-pruefer.md`. Gegenstand: Blatt `docs/jobs/M-BEET-TAUSCH.md` (Pruefpunkte 1 bis 5), Paket `docs/packages/m-beet-tausch.md`, Commits b361159, fa95a9f, 9ddb8b5, 290fe89, b47fc56, c0de8d9, `docs/loop-state.md` Runde 67. Die Selbstauskunft wurde als Behauptung behandelt. Gemessen in einer Kopie im Scratchpad (`scratchpad/mb`: `scripts/`, `data/`, `designs/`, `docs/` kopiert; Repo und fremde Aenderungen im Arbeitsbaum unberuehrt); Viewer auf eigenem Port 4432 (danach beendet).

## Urteil (Stand Runde 67, Erstpruefung): FAIL (Punkt 3), Punkte 1, 2, 4, 5 PASS

**Neues Urteil nach Nachpruefung Runde 68: PASS mit Auflagen** (Abschnitt "Nachpruefung Runde 68" am Ende). Der Text dazwischen ist der Erstbefund und bleibt als Beleg stehen.

Die Montage ist sauber gebaut und die Gaenge, Zaehlungen und der Schacht-Abstand stimmen. Aber: Im Aussenbeet schneidet das Topfraster den Medienschutz und seine Kappe. Das Blatt-Ziel "keine echte Kollision der Beete" ist damit in 8 von 14 Beeten nicht erfuellt, und die Montage hat es als "aussen_800 ohne Treffer" gemeldet, ohne es zu messen (`check_latte` nimmt Pflanzen aus, die Abstandszeile `check_ibc_beet.py` prueft nur den Schacht, nicht den Medienschutz). Die Behebung ist klein (siehe Auflagen), danach Punkt 3 neu messen.

## Pruefpunkte

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | Bau Exit 0; 8 `Beet_aussen_800`, 6 `Beet_innen_933`; Netztoepfe 2222; Salatkoepfe 2626 | `python scripts/gen_dome.py 5 <kopie>/dome-script.json` (26 s), danach Pfad-normalisierter Vergleich mit `scripts/dome-script.json`; Zaehlung der `occurrence.copy`/`insert_design` in der JSON | Skript neu erzeugt: 10098 Befehle, **nach Pfad-Normalisierung byte-identisch** zum committeten Skript. Beete: 1 + 7 Kopien `Beet_aussen_800` = 8, 1 + 5 = 6 `Beet_innen_933`; Netztopf 1 + 2221 = **2222**; Salatkopf 1 + 2221 = **2222**. Der Sollwert 2626 im Blatt ist der Stand von Runde 36 (loop-state Zeile 11); gueltig ist 2222 (D52, Runde 52, Zeile 30 und 43). Build mit CAD-Kern (`sh scripts/build.sh 5 67`, Exit 0) nicht neu gelaufen; stattdessen: `designs/dome.sc` (03:52) ist neuer als die Bauteile `ibc_beet_*.sc` (03:38/03:39), und `check_latte` auf dieser Datei reproduziert die Montage-Ausgabe (Punkt 3) | PASS (Soll 2626 im Blatt veraltet, Auflage 5) |
| 2 | `check_walkways.py` PASS: A 700, B 600, Wandluft 110, Nachbarportale 307, Tuer-Gang 3177 | `python -X utf8 scripts/check_walkways.py` in der Kopie | Exit 0; A 700, B 600, Wandluft 110, Nachbarportale 307, Tuer-Gang 3177 (jeweils PASS); Radialbudget Rand 2095. Gleich Runde 62/66; `check_walkways_voll` (60/82/2/4, `docs/walkway-map.md`) nicht neu gelaufen, Skript und Matrizen unveraendert | PASS |
| 3 | `check_latte`: echte Kollisionen 0; Netztopf x Reinigungsschacht/Medienschutz 0; `check_ibc_beet.py` Exit 0 mit 190 + neuen Zeilen | `python scripts/check_latte.py 67` in der Kopie (ca. 67 min); `python -X utf8 scripts/workshop/check_ibc_beet.py` (voll mit Interferenz); eigene Abstandsmessung aus Instanzmatrizen; CAD-Interferenzprobe (unten) | `check_latte`: Exit 1, 29/31, FAIL L6 Kollisionen **115**, FAIL L6 vollstaendig **71** = Montage-Zahlen; die 115 KOLL-Zeilen sind **identisch** zu `renders/check_latte-67.txt` (sortierter Vergleich). `check_ibc_beet`: Exit 0, **194/194** (190 + 4 Zeilen Abstand Schachtachse zu Netztopf 91,9 mm >= 87, eine je Typ). Netztopf x Schacht aus Matrizen: alle 14 Beete 91,9 mm (Soll >= 87): PASS. **Netztopf x Medienschutz: nicht von `check_latte` und nicht vom Check erfasst; eigene Messung: FAIL**, siehe Abschnitt 3a | **FAIL** (Medienschutz aussen_800; Schacht-Zeile PASS) |
| 4 | `export_model.py` Exit 0; `viewer/defs/ibc_beet_aussen_800*.obj` und `innen_933*.obj` neuer als der Build; `instances.json` 14 Beet-Instanzen; Screenshot zeigt Schachtkappe am Beetende | `ls -l --time-style=full-iso viewer/defs/ibc_beet_*.obj designs/dome.sc`; `viewer/instances.json` gelesen; `python viewer/serve.py 4432` und Browser-Pane | `ibc_beet_aussen_800.obj` 05:17:33, `ibc_beet_innen_933.obj` 05:18:08, beide neuer als `dome.sc` (03:52:45). `instances.json`: 14 Beet-Instanzen (`ibc_beet_aussen_800` 8, `ibc_beet_innen_933` 6), 4880 Instanzen, "Modell gespeichert 03:52:45". Viewer-Bild, nur Beete eingeblendet (Draufsicht): 14 Beete, je zwei runde Kappen nahe den Beetenden; welche die Schachtkappe ist, ist im Bild nicht beschriftet und nicht per Hover geprueft. `export_model.py` selbst nicht neu gelaufen (`viewer/` ist ausserhalb meines Schreibrechts) | PASS (Schachtkappe nicht eindeutig benannt im Bild) |
| 5 | Bauteilblatt Rohr-DN100-Zeile mit Artikel oder "Artikel nicht nachgewiesen", Dichtband "nicht beschafft (Mass offen)"; `grep -n "346"` ohne Treffer; Paket Abschnitt "Auflage 5" mit Messwerten und zwei Quellen; Bilanz-Dateiliste mit Eigentuemer; keine Bilanz-Datei von der Montage geaendert | `grep -n "Reinigungsschacht d110\|Dichtband Plattenrand" docs/parts/ibc_beet.md`; `grep -c 346 scripts/workshop/check_ibc_beet.py`; Paket gelesen; `git log --oneline b361159^..HEAD -- docs/system-concept.md data/system-specs.json docs/filter-konzept.md`; `git show --name-only` der sechs Commits | Zeile 181 "Artikel nicht nachgewiesen", Zeile 184 "nicht beschafft (Mass offen)"; `grep -c 346` = 0; Paket "Auflage 5": Tabelle mit Modellmass gegen Quelle (22 mm Bevo 7002656 und GF-Reduzierstueck, beide nur Katalogzeile, ausdruecklich "kein Datenblatt gelesen, [A]"); Bilanz-Liste in `M-BEET-TAUSCH.md` Zeilen 46 bis 52, Eigentuemer Orchestrator; `git log` leer (kein Commit an den drei Bilanz-Dateien); die sechs Commits beruehren nur Beet-, Paket-, Doku-, Render- und Check-Pfade (c0de8d9 nur Bauteilblaetter der W37-Teile) | PASS |

### 3a Eigene Pruefung (a): sind unter den 115 Kollisionen Beet-Koerper?

Nein. `grep "^KOLL" renders/check_latte-67.txt` aufgeschluesselt nach Komponentenpfad: 86 nur `08_Leitungen`, 7 `08_Leitungen` x `09_Technik`, 4 nur `09_Technik`, 3 `07_Tanks`, 15 ohne Pfad (Namen `Bogen`, `Rohr`, `Reduzierung`, `Kupplung`, `Saugstutzen`, `Montagetafel`, dazu `T10_Zulaufrohr x T3_Sockel`). Treffer mit `Beet`, `ibc`, `Schacht`, `Siphon`, `Medienschutz`: 0. Die Beete untereinander: kleinste Luecke 94 mm (PASS). **Altbestand:** `scripts/gen_dome.py` wurde zuletzt am 01.11.2026 16:36 geaendert (vor dem Tausch), der Tausch wirkt nur ueber die zwei Bauteil-`.sc`; ein direkter Vergleichslauf auf der Runde-66-Datei (`git show 9ddb8b5^:designs/dome.sc`) wurde nicht gemacht (zweiter 67-Minuten-Lauf), die Montage selbst nennt, dass Runde 62 bis 66 ohne vollen Lauf liefen. Urteil: Leitungsthema, kein Beet-Fehler; Altbestand nur begruendet, nicht gemessen.

### 3b Eigene Pruefung (b): Medienschutz im Innenbeet, Kollision oder nur knapp?

Gemessen aus den Instanzmatrizen (Topfmatrizen mit Z 805, 1548 Stueck): Innenbeet, naechster Topf zur Schutzachse **6,4 bis 6,5 mm** (alle 6 Beete). Netztopf-Boden Z 805, Schutzkappe-Oberkante Z 800: **5 mm Luft**. CAD-Probe (Bauteil `ibc_beet_innen_933.sc` plus ein `netztopf.sc` an der Stelle des naechsten Topfs, `inspect.interference`): **0 Paare**. Im Modell also keine Kollision, nur knapp.

Aber: Der Befund ist ein Zufallsprodukt. Der Topf steht im Innenbeet 40 mm ueber dem Medium (Medium-Oberkante abs. 765, Topf-Boden 805), weil `gen_dome.py` `pots()` die Topfhoehe `fz + pot_base_z` fuer alle Beete gleich setzt. Wuerde der Topf auf dem Medium stehen (Z 765): dieselbe CAD-Probe mit Topf bei Z lokal 574 liefert **1 Paar: Netztopf x Schutzkappe, 3837 mm2**. Bewertung: im Modell nur knapp, im realen Beet eine Kollision. Die Loesung wie bei Schritt 0c (Rasterzellmitte) gilt hier auch.

### 3c Neuer Befund: Aussenbeet, Netztopf x Medienschutz und Schutzkappe (8 von 8 Beeten)

Die Montage meldet "aussen_800 ohne Treffer". Gemessen (Matrizen der 1548 Beet-Topfmatrizen, Abstand lokal zur Schutzachse x 1096, y 0): kleinster Abstand **65,6 mm in allen 8 Aussenbeeten** (Topf lokal x 1105, y -65). Der Schutzrohr-Radius ist 55, der Topf-Radius am Boden 17 (Konus 34 auf 50 mm, `data/components/netztopf.json`). CAD-Probe (Bauteil `ibc_beet_aussen_800.sc` plus ein `netztopf.sc` an dieser Stelle, Z 805, `inspect.interference`): **2 Paare**, **Netztopf x Medienschutz 350 mm2** und **Netztopf x Schutzkappe 1058 mm2**. Das ist eine echte Ueberschneidung der Beet-Koerper mit der Bepflanzung. Der Befehl der CAD-Proben: `solidcraft-cli.exe run <probe.json> --in designs/components/ibc_beet_aussen_800.sc --results --json-out ...` mit den Befehlen `component.insert_design` (netztopf.sc), `occurrence.move` (Matrix x 1105, y -65, z 567), `inspect.interference`.

Warum entgangen: (1) `check_latte` nimmt Pflanzen aus (219 978 Koerper, Montage-Eintrag Zeile 86); (2) die in Schritt 0c ergaenzte Zeile "Abstand >= 87 mm" (`check_ibc_beet.py` Zeile 113) prueft nur die Schachtachse, der Medienschutz hat denselben Radius 55 und braucht dieselbe Pruefung; (3) die Montage hat nur die Schachtachse aus den Matrizen gemessen.

## Stichproben ausserhalb der Pruefpunkte

1. Zahl der Kurzmeldung gegen die Datei: "check_ibc_beet 194/194" (Paket, loop-state) gegen eigenen Lauf **194/194 PASS**, Exit 0. PASS. "Abstand 91,9 mm" gegen eigene Matrizenmessung 91,9 mm (alle 14). PASS. "Salatkoepfe 2222" gegen Skript 2222. PASS.
2. Teil gegen sein Blatt: Schacht lokal aussen_800 x -1040, innen_933 x -650, y 65 (aus `eval` der Bauteil-`.sc`, Bounding-Box-Mitte) gegen Paket "Schacht auf Rasterzellmitte (91,9 mm)": stimmt. Reduzierhuelse Baulaenge 22 mm gegen Modell 15 und 39 mm: im Paket als offen ausgewiesen, nicht bewertet.
3. Commit gegen `git diff`: `git show --name-only` der sechs Commits: nur Beet-, Paket-, Doku-, Render-, Check- und (c0de8d9) 8 Bauteilblaetter der W37-Teile; keine fremden `designs/components/*.sc`, kein `data/roadmap.json`, keine Bilanz-Datei. PASS. Der Arbeitsbaum enthaelt weiterhin die genannten fremden Aenderungen, unberuehrt.

## Nicht belegte oder nicht nachgemessene Behauptungen

1. "`sh scripts/build.sh 5 67` Exit 0": der CAD-Lauf wurde nicht wiederholt (nur Skript neu erzeugt und `dome.sc` ueber `check_latte` gemessen).
2. "`check_walkways_voll` unveraendert 60/82/2/4": nicht neu gelaufen (7,5 min), nur `check_walkways`.
3. "`export_model.py` Exit 0": nicht neu gelaufen; Ergebnisdateien und Zeitstempel gemessen.
4. Schachtkappe im Viewer: zwei runde Kappen je Beet gesehen, die Zuordnung (Schacht gegen Schutz) nicht per Hover belegt.
5. Altbestand der 115 Leitungs-Kollisionen gegen Runde 66: nur ueber den Generator-Stand begruendet, nicht gemessen.
6. Viewer-Seitentext "Netztopf 1634 (960 Aussenbeete + 674 NFT)", "Salatkopf 1634", "Beete / NFT 2.160 / 674, Toepfe gesamt 2.834": passt nicht zum Modell (1548 Beet-Toepfe, 2222 gesamt); Textstand 31.10./`viewer/extras.json` (fremde, nicht committete Aenderung), nicht von der Montage.
7. Anspringen und Dichtheit am Muster, Kaufteil-Datenblaetter: unveraendert nicht pruefbar.

## Auflagen

1. **Medienschutz freiraeumen, Aussen- und Innenbeet (Blocker fuer PASS).** Schutzachse wie in 0c auf Rasterzellmitte legen oder den betroffenen Topf je Beet streichen; Abstandsbedingung gegen Rohr plus Kappe: >= 55 + Topfradius (bei Kappenhoehe Z 835 etwa 21 mm, Kragen 32 mm als sichere Grenze 87 mm). `check_ibc_beet.py` um eine Zeile "Abstand Schutzachse zu jedem Netztopf" ergaenzen, alle vier Typen. Owner: Werkstatt; dann Montage-Neubau nur der Beet-Instanzen und `check_latte` neu. Hinweis: die Rasterzellmitten fuer Schacht und Schutz muessen zusammen aufgehen (Schacht x -1040 bzw. -650, Schutz x 1096 bzw. 708,5 sind heute nicht auf Zellmitte; Topfzahl 2222 bleibt das Ziel, ersatzweise Topfzahl als Entscheidung an Ben).
2. **Topfhoehe je Beet.** `gen_dome.py` `pots()` setzt `zb = fz + pot_base_z` fuer alle Beete; Innenbeete stehen 40 mm ueber dem Medium (765 gegen 805), Aussenbeete 5 mm darueber (800 gegen 805). Entscheidung, ob die Hoehe je Beet aus der Medienoberkante folgt (dann entsteht die Kollision aus 3b im Modell sichtbar und Auflage 1 muss sie abdecken). Owner: Montage/Orchestrator.
3. **`check_latte` um Pflanzen-Teilpruefung ergaenzen oder den Check `check_ibc_beet.py` als Pflicht fuer "Beet x Pflanze" fuehren**, damit ein Pflanzen-Fehler nicht wieder unsichtbar bleibt. Owner: Orchestrator.
4. **Sollwert im Blatt `M-BEET-TAUSCH.md` korrigieren:** Salatkoepfe 2222 statt 2626 (Stand Runde 36). Owner: Orchestrator.
5. **Viewer-Textstand** (`viewer/extras.json`: Netztopf/Salatkopf 1634, Toepfe 2834, Beete 2160) an das Modell (1548 Beet-Toepfe, 2222 gesamt) angleichen, sobald die fremde Aenderung an der Datei gesichert ist. Owner: Orchestrator.
6. Offen aus dem Paket, nicht Gegenstand dieser Pruefung: Datenblaetter Reduzierhuelse und Tankverbinder (Ben/N-BESCHAFFUNG), Dichtband-Mass, Metallbauer-Anfrage, E20 (Ablaufleitungen, Beet-Sumpf), Bilanz-Dateien nachfuehren (6280 l).

Geprueft gegen: `python scripts/gen_dome.py 5` (identisch nach Pfad-Normalisierung), `python -X utf8 scripts/check_walkways.py` (Exit 0), `python scripts/check_latte.py 67` in der Kopie (Exit 1, 29/31, 115 und 71, KOLL-Liste identisch), `python -X utf8 scripts/workshop/check_ibc_beet.py` (Exit 0, 194/194), Instanzmatrizen aus `scripts/dome-script.json`, `solidcraft-cli.exe eval` und `run` mit `inspect.interference` (Netztopf-Proben), `viewer/instances.json`, Viewer-Bild Port 4432, `git show --name-only` der sechs Commits.
Offen: Auflagen 1 bis 5 (Owner je Auflage genannt; Auflage 1 ist die einzige, die das Urteil ändert); nicht gemessen: CAD-Neubau Exit 0, `check_walkways_voll`, `export_model.py`, Vergleichslauf Runde 66, Schachtkappe-Zuordnung im Viewer.

## Nachpruefung Runde 68 (Pruefer, 04.11.2026)

Gegenstand: Commits 7ddff23, 3fbcc3e, fa99e8f, 089bc33 (D79: Medienschutz auf Rasterzellmitte, Topf auf Medienoberkante je Beet). Alle Messungen in dieser Sitzung neu, in einer Kopie des Stands 089bc33 (`git archive 089bc33` im Scratchpad); der Arbeitsbaum des Repos blieb unberuehrt, geschrieben ist nur diese Datei.

### Urteil: PASS mit Auflagen

Der Fehler aus Punkt 3 ist behoben: In allen 14 Beeten liegt der naechste Netztopf 91,9 mm von Schutz- und Schachtachse (Soll >= 87); die CAD-Probe auf der neuen Topfhoehe findet 0 Kollisionen, die Gegenprobe mit dem alten Abstand findet sie. `check_latte` 68 zeigt keine neue Kollision. Auflagen betreffen nur noch Nebenpunkte (unten).

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | 8 aussen_800 + 6 innen_933, 2222 Netztoepfe, 2222 Salatkoepfe | `python scripts/components/strebe.py; python scripts/gen_dome.py 5 scripts/dome-script.json`; Zaehlung der `occurrence.move` je Namensanfang (eigenes Skript, Scratchpad `m68_geo.py`); `check_latte.py 68` Zeilen "Netztoepfe" | 14 Beet-Verschiebungen (8 + 6), 2222 Netztopf-, 2222 Salatkopf-Verschiebungen, 10098 Befehle; davon 1548 Beet-Toepfe (8 x 120 + 6 x 98) + 674 Rinnen; `check_latte` PASS "Netztoepfe 2222" und "Erwartung (960, 588, 674, 2222)" | PASS |
| 2 | `check_walkways` unveraendert | `python -X utf8 scripts/check_walkways.py` (Kopie); `python -X utf8 scripts/check_walkways_voll.py` (Kopie) | A 700 / B 600 / Wandluft 110 / Nachbarportale 307 / Tuer-Gang 3177, alle PASS (gleich Runde 67); voll: knie rot 60 / gelb 82, kopf rot 2 / gelb 4, erzeugte `docs/walkway-map.md` per `diff` gleich der im Repo | PASS |
| 3 | Netztopf x Medienschutz und Schacht, aussen und innen, auf der NEUEN Topfhoehe, 0 echte Kollisionen | Instanzmatrizen: `dome-script.json` -> Topf-Mitte in Beet-Koordinaten (Rueckrechnung ueber die Beet-Matrix), Abstand zu Schutz- und Schachtachse (aus `solidcraft-cli.exe eval ibc_beet_<typ>.sc` gemessen: aussen x +-1040 / y 0, innen x +-650 / y 65). CAD: `solidcraft-cli.exe run n68_<x>.json --in designs/components/ibc_beet_<typ>.sc --results` mit eingesetztem `netztopf.sc` am naechstgelegenen Raster-Topf je Achse (4 Proben) plus `inspect.interference` | Abstand aussen und innen in allen 14 Beeten 91,9 mm (Soll >= 87). Topfhoehe: Topf-Boden lokal z 562 (aussen) bzw. 574 (innen) = Oberkante `Medium` (eval: 562 / 574), also Luft 0 statt 40 mm; gilt fuer alle 14 Beete (Beet-z0 innen 191 bis 230, Topf folgt). CAD: 4 von 4 Proben `count 0` (checked 41 bzw. 32 Paare); Kontrollprobe mit dem alten Abstand (65,6 mm, gleiche Topfhoehe aussen): 1 Treffer Netztopf x Schutzkappe 1062 mm2, die Probe erkennt den Fehler also | PASS |
| 4 | Viewer-Export Runde 68 | `export_model.py` nicht gelaufen | nicht gebaut, Berechtigungssystem lehnte ab, Ben entscheidet (laut Start-Auftrag) | offen, nicht Fehlerpunkt |
| 5 | Bauteil-Check und Nachfuehrung | `python -X utf8 scripts/workshop/check_ibc_beet.py` (Kopie) | Exit 0, Schlusszeile "== ibc_beet: 210/210 PASS", 0 Zeilen ohne PASS; je Typ neue Zeile "Abstand Medienschutz-Achse zu jedem Netztopf" 91,9 mm (8 Zeilen Abstand, 4 Typen); Interferenz Ist 0 und "alle Koerper benannt" in 4 von 4 | PASS (Zahl siehe Auflage 1) |

### Zusatzmessungen (Wunsch des Start-Auftrags)

1. `check_latte.py 68` in der Kopie auf dem committeten `designs/dome.sc`: 29/31, 115 KOLL, 71 Paare nicht vollstaendig. Die sortierte KOLL-Liste ist Zeile fuer Zeile gleich `renders/check_latte-67.txt` (115 = 115, `sorted(a)==sorted(b)`); 0 Zeilen mit Beet, Schacht, Siphon, Medienschutz, Netztopf, Salat, Reduktion oder Erde; "EXAKT Erde 542 Koerper, noch offen 0". Der Befund "Leitungs-Altbestand, kein Beet-Thema" ist damit durch einen Vergleichslauf belegt (in der Erstpruefung nur ueber den Generatorstand).
2. `check_walkways_voll` siehe Punkt 2.
3. `designs/dome.sc` wurde in fa99e8f geaendert (15 625 398 -> 15 595 090 Byte) und ist im Arbeitsbaum unveraendert (`git diff HEAD --stat -- designs/dome.sc` leer).

### Nicht gemessen

1. CAD-Neubau selbst (`build.sh 5 68`, Exit 0): nicht neu gebaut; die Aussage "Exit 0" stuetzt sich auf das committete `dome.sc`, das `check_latte` fehlerfrei einliest, und auf das identisch regenerierte `dome-script.json`. Schliesst einen Build-Fehler nicht formal aus.
2. Pflanzen in `check_latte`: weiter ausgenommen (219 978 Koerper); Topf x Beet ruht auf der CAD-Probe und der Matrixrechnung oben, nicht auf `check_latte`. Probe deckt nur Topf gegen das Beet-Bauteil, nicht Topf/Salatkopf gegen Portale, Tische oder Streben.
3. Das Paar Medium x Medienschutz bleibt in `inspect.interference` "unchecked" (Boolean liefert kein Ergebnis); trat auch im Erstbefund auf und betrifft nicht den Topf.
4. Viewer-Export Runde 68 und Viewer-Texte (Auflage 5 der Erstpruefung).

### Auflagen (neu geordnet)

1. Paket und Commit 3fbcc3e nennen "211 PASS"; gemessen 210/210 (die 211 entsteht, wenn die Schlusszeile mitgezaehlt wird, gleicher Fehler wie in W40-BEET Auflage 1). Zahl in `docs/packages/m-beet-tausch.md` und `docs/loop-state.md` auf 210 korrigieren. Owner: Werkstatt/Orchestrator.
2. `check_latte` um eine Pflanzen-Teilpruefung ergaenzen oder `check_ibc_beet.py` ausdruecklich als Pflicht fuer "Beet x Pflanze" fuehren (Auflage 3 der Erstpruefung, unveraendert offen). Owner: Orchestrator.
3. Viewer-Export Runde 68 und Texte in `viewer/extras.json` (Netztopf/Salatkopf 1634, Toepfe 2834, Beete 2160 gegen 2222) nachziehen. Owner: Ben (Entscheidung zur fremden Aenderung an der Datei).
4. Ablaufport der Beete wandert (aussen_800 x -56 mm, innen_933 y +65 mm, Angabe des Pakets, nicht nachgemessen): beim Anschluss K14/K30 (E20) beachten. Owner: Planer.
5. Der Sollwert Salatkoepfe 2222 steht im Blatt jetzt richtig (Zeile 39); keine Handlung.

Geprueft gegen: `gen_dome.py 5` (Zaehlung 14 Beete / 2222 / 2222), `check_walkways.py`, `check_walkways_voll.py` (`diff` gleich Repo), `check_ibc_beet.py` (210/210), `check_latte.py 68` (115 KOLL identisch zu Runde 67), Rueckrechnung aller Topf-Mitten auf Beet-Koordinaten, 4 CAD-Interferenzproben plus Kontrollprobe, `eval` der Beet-Bauteile, `git show --stat` der Commits.
Offen: Auflagen 1 bis 4; nicht gemessen: CAD-Neubau Exit 0, Topf/Salatkopf gegen Portale/Tische/Streben, Viewer-Export (Ben).

