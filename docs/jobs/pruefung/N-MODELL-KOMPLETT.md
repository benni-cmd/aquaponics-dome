# Pruefung N-MODELL-KOMPLETT (Runde 70) — Befund

Pruefer: frische Sitzung, hat nichts davon gebaut. 05.11.2026. Start-Auftrag `docs/jobs/start/N-MODELL-KOMPLETT-pruefer.md` (90a3cf2), Blatt `docs/jobs/N-MODELL-KOMPLETT.md` Pruefpunkte 1 bis 5.
Gegenstand: Commits bdaccb4, de85faf, 24a5ee8, 5c8baef; Viewer-Kleinteile aus `docs/packages/n-viewer-laden.md`.
`check_latte.py` nicht gestartet (laeuft separat, Auftrag Punkt 2). Nur die Befund-Datei geschrieben; Modell, Daten, Blatt, Roadmap unveraendert.
Aenderungen im Arbeitsbaum, die nicht von mir stammen: viele `M`-Dateien (`data/stueckliste.json`, `data/parts/*.json` u. a.) — andere Sitzungen laufen parallel; mein `bom.py`-Lauf (Punkt 5) schreibt `data/stueckliste.json` neu, ich committe sie nicht.

## Urteil

| Punkt | Gegenstand | Urteil | Begruendung |
|---|---|---|---|
| 1 | Strebe als Vierkant | **PASS** | bbox, Volumen, Masse, Werkstoff, Instanzzahl alle im Soll |
| 2 | Lage und Passung | **PASS mit Auflagen** | Rollwinkel 0,002 Grad an allen 64; Basisknoten-Z 475,0; CAD-Probe: Strebe gegen Steckarm und Knotenkugel 0 Treffer. Schrauben und Scheiben durchstossen die Rohrwand (Querbohrung fehlt, schon beim Rundstab so); `check_latte`/`interf.py` laut Auftrag nicht gelaufen |
| 3 | Tuer mit Klinke | **PASS mit Auflagen** | 27 Koerper belegt (12 + 15 Kleinteile), `tuer` nicht in `instances.json`; aber Wortlaut-Soll `tuer_komplett.obj` = 27 gilt nicht mehr (12), Standard zeigt die Klinke nicht, Screenshot nicht gelungen, Infotext veraltet |
| 4 | Werkstoffe | **PASS mit Auflagen** | die 8 genannten Komponenten gemessen: nur `nft_tisch_innen` hat 6 Koerper `Default` (bekannt offen, Auftrag Punkt 3); `check_parts.py` ueber alle Komponenten nicht zu Ende gelaufen |
| 5 | Folgen sauber | **FAIL** | Hinweis `platzhalterkoerper` steht weiter an `PRF-st-strebe30x30` (`scripts/bom_artikel.py:237`); Paket-Schritt 6 ist offen. Menge, `bom.py`, `check_bom.py`, `check_huelle.py` im Soll |
| **Gesamt** | | **FAIL nur wegen Punkt 5** (Einzeiler); 1 bis 4 PASS bzw. PASS mit Auflagen | W65 erst nach A1 |

## Messung je Pruefpunkt

Alle Befehle aus `user-projects/aquaponics-dome`. Messdateien liegen im Session-Scratchpad.

### Punkt 1 Strebe als Vierkant

| Messung | Befehl | Messwert | Soll | Ergebnis |
|---|---|---|---|---|
| `strebe_a` | `solidcraft-cli.exe eval designs/components/strebe_a.sc --json-out <datei>` | 1 Koerper `T1_Strebe_A`; bbox 30 x 30 x 3039; Volumen 984 636 mm3; Masse 7729 g; closed wahr; Material `Stahl verzinkt` | 1 Koerper, 30 x 30 x 3039, 984 636 mm3 +-1 %, 7,73 kg +-1 %, hohl, Katalogname | PASS |
| `strebe_b` | dito `strebe_b.sc` | 1 Koerper; 30 x 30 x 3468; 1 123 632 mm3; 8821 g; closed; `Stahl verzinkt` | 30 x 30 x 3468, 8,82 kg | PASS |
| Rechnung | `python -X utf8 -I -c "print(324*3039, 324*3039*7.85e-6, 324*3468*7.85e-6, 30*3.039+34*3.468)"` | 984 636; 7,729 kg; 8,821 kg; 209,082 m | gleiche Werte | PASS |
| Instanzen | `python -X utf8 -I -c "import json,collections;c=collections.Counter(x['d'] for x in json.load(open('viewer/instances.json',encoding='utf-8'))['instances']);print(c['strebe_a'],c['strebe_b'],c['tuer'],c['tuer_komplett'])"` | 30, 34, 0, 1 | 30, 34 | PASS |
| Viewer-Definition | Ecken aus `viewer/defs/strebe_a.obj` gelesen | 16 Ecken, Ausdehnung 30,0 x 30,0 x 3039,0 (hohles Rohr) | 30 x 30 x 3039 | PASS |

### Punkt 2 Lage und Passung

| Messung | Befehl | Messwert | Soll | Ergebnis |
|---|---|---|---|---|
| Rollwinkel, unabhaengig aus den gebauten Matrizen | eigenes Skript (`roll.py`, Scratchpad): je Strebe aus `viewer/instances.json` die lokale Y-Achse gegen die `bolzenachse` des Steckarms aus `data/components/knoten_arme.json` (um `door_az - 167` gedreht), Knoten ueber xy-Naehe zugeordnet, an beiden Enden | 64 Streben, 128 Enden, groesster Winkel 0,0018 Grad; Orthogonalitaet der Matrizen 1,2e-9 | unter 1 Grad am Muster von 5 Streben | PASS (alle 64 statt 5) |
| Endabstand | dasselbe Skript, Strebenende gegen Knoten | xy-Abstand hoechstens 136,7 mm; im CAD-Probelauf 3D-Abstand 120 mm an allen 10 Enden = `strut_end_offset` 120, Strebenlaenge 3039 stimmt | 120 mm | PASS |
| Basisknoten-Z | `python -c "import json;s=json.load(open('scripts/.segs.json'));print(len(s),min(p[2] for g in s for p in g))"` | 64 Segmente, kleinstes Z 475,0 | 475,0 (Vorher-Wert Runde 69 laut Paket) | PASS gegen den Wert des Pakets; der Runde-69-Stand selbst ist nicht mehr beschaffbar (`scripts/.segs.json` nicht in Git) |
| Parameter | `git diff de85faf~1 de85faf -- scripts/gen_dome.py data/params.json` | `cz = sock_z + base_axis_h` mit `base_axis_h` 75 (= 45 + 30); `strut_r` nur noch in `check_latte.py`, `place_m8.py`, `check_huelle.py` | Achshoehe entkoppelt, Wert 75 | PASS |
| Tuerlage | nicht neu vermessen; `git diff de85faf~1 de85faf -- scripts/gen_dome.py` aendert nur `place_struts` und die Zeile `cz`, keinen Tuer-Code | | Differenz 0,0 mm | nicht belegt (nur mittelbar, `cz` bleibt 475,0) |
| CAD-Probe Interferenz | Scratchpad-Kopie: `strebe_a.sc` mit den Matrizen aus `instances.json` fuer `Strebe_A:1` bis `:5` plus die 6 anliegenden Knoten (`knoten_n01/02/03/07/22/23`), `solidcraft-cli.exe run ... --save`, dann `inspect.interference` mit `budget_s` 240 | 168 Paare geprueft, 26 Treffer: Strebe gegen Schraube 10 (je 471 mm3 = Ø 10 mal 2 Wandstaerken 3 mm) und gegen Scheibe 10 (53 bis 105 mm3); **Strebe gegen Steckarm, Knotenkugel oder Mutter: 0**; 0 ungepruefte Paare mit Strebe; Rest-Treffer sind Knoten-intern (Kugel/Arm 591 mm3, Schraube/Mutter 0 mm3), 103 Knoten-interne Paare wegen Zeitbudget ungeprueft | keine Interferenz Strebe/Knoten | PASS fuer die Passung; Schraubentreffer siehe A2 |
| Gegenprobe alter Rundstab | dieselbe Probe mit `git show bdaccb4~1:designs/components/strebe_a.sc` | Strebe gegen Schraube 10 und gegen Mutter 10, 20 Strebe-Paare ungeprueft | Schraubentreffer neu? | die Treffer bestanden schon vorher (keine neue Interferenzklasse; Mutter-Treffer entfallen) |
| `check_latte.py`, `interf.py` | nicht gestartet (Auftrag) | | | nicht geprueft |

### Punkt 3 Tuer mit Klinke

| Messung | Befehl | Messwert | Soll | Ergebnis |
|---|---|---|---|---|
| Hauptdefinition | `grep -c "^o " viewer/defs/tuer_komplett.obj` | 12 | blatt: 27 | nach Wortlaut FAIL, **Soll durch W66 ueberholt** (Kleinteile gehen in eine eigene Datei) |
| Kleinteile | `grep -c "^o " viewer/defs/tuer_komplett.klein.obj`; `grep -n "^o "` | 15: `Scharnier1..3` je Zargenlasche, Blattlasche, Bolzen (9), `Rosette_aussen/innen`, `Druecker_Hals_aussen/innen`, `Druecker_Hebel_aussen/innen` | 15 Kleinteile | PASS |
| Summe | 12 + 15 | 27 | 27 | PASS |
| Im Viewer | `viewer/serve.py 4521` (eigener Port, kein Export: `dome.sc` 02:06 aelter als `instances.json` 02:12), Haken "Kleinteile unter 15 cm zeigen" gesetzt, `window.viewerStand()` | `tuer_komplett`: `koerper` 12, `kleinteile` 15; ohne Haken zuvor 12 + 0 | 27 sichtbar mit Haken | PASS |
| `tuer` nicht im Modell | siehe Punkt 1, Zaehler `tuer` | 0 | 0 | PASS |
| Screenshot Tuer mit Klinke / Strebe-Nahansicht | Browser-Pane, Viewport 1600 x 900 | **nicht gelungen**: der Viewer legt keine Kamera-API offen, die Tuer liegt hinter der Huelle, die Listenauswahl der Instanz `Tuer Komplett:1` schlug in dieser Sitzung fehl; es liegen nur Gesamtansichten vor (Ansicht ref-4 und Oben, Kleinteile an, Auf-einen-Blick-Seite rechts, keine ueberlappenden Bedienelemente bei 1600 x 900) | Nahaufnahme gegen `docs/ui-standard.md` | nicht belegt (A3) |

### Punkt 4 Werkstoffe

| Messung | Befehl | Messwert | Soll | Ergebnis |
|---|---|---|---|---|
| 9 Komponenten | `solidcraft-cli.exe eval designs/components/<name>.sc` je Name, Werkstoffe je Koerper gezaehlt (Skript `mat.py`) | `strebe_a/b` Stahl verzinkt; `fundamentring` Beton; `pool_zentral` PE Tank 1, PVC grau 3, Wasser 1; `zweitbecken` PE Tank, Wasser; `zulaufrohr` PVC grau; `schaltschrank` Stahl verzinkt; `tuer_komplett` 22 Stahl verzinkt, 1 Tuerblatt Sandwich, 4 EPDM schwarz; `nft_tisch_innen` **6 von 54 `Default`** (42 Stahl, je 2 PVC blau, Schlauch hellblau, PVC grau) | 0 `Default` ausser Ausnahmeliste | PASS ausser `nft_tisch_innen` (bekannt, Auftrag Punkt 3) |
| ganzer Bestand | `python -X utf8 scripts/workshop/check_parts.py` (ca. 25 Minuten gelaufen, 9 von rund 308 Komponenten, dann von mir abgebrochen) | kein Exit-Code | Exit 0 | **nicht belegt**; der Paket-Wert "Exit 0, 308 Komponenten" (04.11. 12:35) ist nicht nachgemessen |
| `model_inventar.py` | nicht gestartet (rund 50 Minuten) | | Zahl `Default` unter eingesetzten Komponenten | nicht belegt |

### Punkt 5 Folgen

| Messung | Befehl | Messwert | Soll | Ergebnis |
|---|---|---|---|---|
| `bom.py` | `python -X utf8 scripts/bom.py` | Exit 0 | Exit 0 | PASS |
| `check_bom.py` | `python -X utf8 scripts/check_bom.py` | 2 Laeufe: der erste lieferte "13 von 14 Pruefungen PASS" (Exit 0), der zweite "14 von 14 PASS" (Exit 0). Die fehlende Zeile des ersten Laufs habe ich nicht festgehalten; moeglicher Zusammenhang mit gleichzeitig schreibenden Sitzungen, nicht bewiesen | Exit 0 | PASS, Instabilitaet siehe A5 |
| Menge | `python -X utf8 -I -c` auf `data/stueckliste.json`, Artikel `PRF-st-strebe30x30` | `bedarf` 209,082 m; `gekauft_m` 224,0 (32 Stangen zu 7 m); Verschnitt 6,66 % | 209,082 m | PASS |
| Hinweis `platzhalterkoerper` | `grep -rn "platzhalterkoerper" scripts/*.py`; Artikel in `data/stueckliste.json` | `scripts/bom_artikel.py:237` setzt `flag="platzhalterkoerper"` fest; der Artikel traegt `"hinweise": ["platzhalterkoerper"]` | Hinweis weg | **FAIL** |
| `check_huelle.py` | `python -X utf8 scripts/workshop/check_huelle.py` | 68/68 PASS, Exit 0 | Exit 0 | PASS |
| Summe `viewer/defs/*.obj` | `du -cb viewer/defs/*.obj` | 507 451 353 Byte (davon ohne `*.klein.obj` 289 602 681) | hoechstens +2 % gegen den Wert vor Schritt 5 | Wert reproduziert (= Paket); der Vorher-Wert wurde nicht gesichert (`viewer/defs/` ist in `.gitignore`), Wachstum nicht pruefbar |

## Drei Stichproben ausserhalb der Pruefpunkte

1. **Zahl aus der Kurzmeldung gegen Datei:** Commit-Text 24a5ee8 "Basisknoten-Z 475,0, 64/64 Rollwinkel 0,0 Grad, check_huelle 68/68": gemessen 475,0 / 0,0018 Grad (alle 64) / 68/68 = PASS.
2. **Teil gegen sein Blatt:** Bauteilblatt `docs/parts/strebe.md` und Paket-Wert "Steckarm 23 x 23 x 3 in Innenmass 24, 0 Interferenzen": CAD-Probe zeigt gegen den echten Knoten 0 Treffer Strebe/Arm = PASS.
3. **Commit gegen `git diff`:** `git show --stat 24a5ee8` nennt `fundamentring/pool_zentral/schaltschrank/strebe_a/strebe_b/zulaufrohr/zweitbecken.sc`, `designs/dome.sc`, `docs/loop-state.md`, Paket, `viewer/extras.json`; `git diff de85faf~1 de85faf -- scripts/gen_dome.py` betrifft nur `place_struts` und die Zeile `cz`. Nichts Fremdes. Der Commit-Text "7 Komponenten ohne Default" passt zu den 7 geaenderten `.sc` (in Punkt 4 gemessen: 0 `Default`) = PASS.

## Behauptungen, die sich nicht belegen lassen

1. "`check_parts.py` Exit 0, 308 Komponenten, 0 FAIL" (Paket 04.11. 12:35): in dieser Sitzung nach 9 Komponenten abgebrochen; nicht nachgemessen.
2. "Summe `viewer/defs/*.obj` 507 451 353 vor und nach dem Export": die Zahl stimmt heute, aber ein unveraenderter Wert nach dem Austausch von Rundstab (Ausdehnung 90) durch das hohle Rohr (16 Ecken, 889 Byte) ist ohne Vorher-Messung nicht nachvollziehbar.
3. "Tuerlage unveraendert (Differenz 0,0 mm)": nur fuer die Streben und Knoten belegt (Z 475,0); die Tuer selbst nicht neu vermessen.
4. "Viewer-Screenshot Tuer mit Klinke": im Paket als offen gefuehrt, hier nicht herstellbar.
5. **Fulfillment-Frage, Ben-Ziel "Ben sieht an der Tuer eine Klinke":** der Viewer-Standard zeigt die Kleinteile weiterhin nicht (Haken "Kleinteile unter 15 cm zeigen" ist aus, `localStorage`); die Klinke erscheint nur nach dem Einschalten. Das Ziel ist technisch erreicht, im Standardbild nicht.

## Auflagen

| Nr | Auflage | Owner |
|---|---|---|
| A1 | **Vor W65:** in `scripts/bom_artikel.py:237` das Flag `platzhalterkoerper` am Artikel `PRF-st-strebe30x30` entfernen, `bom.py` und `check_bom.py` neu laufen lassen, Paket-Schritt 6 abhaken. Danach Punkt 5 PASS | ICH (Orchestrator/Werkstatt; Datei gehoert nicht zu dieser Pruefung) |
| A2 | Strebe hat keine Querbohrung fuer den Verbindungsbolzen: je Strebe 2 Schrauben und 2 Scheiben durchstossen die Rohrwand (`volume_mm3` 471 je Schraube). Beim Rundstab genauso, also nicht neu; fuer das genaue Modell (W63) eine Bohrung Ø 10 an beiden Enden in `scripts/components/strebe.py` aufnehmen, Lage aus dem Knotenblatt | ICH (Werkstatt, naechste Strebe-Runde) |
| A3 | Screenshot Tuer-Nahansicht und Strebe-Nahansicht nachholen; der Viewer hat keine Kamera-API: eine kleine Messhilfe `window.setzeKamera(pos, ziel)` oder eine Ansicht "Tuer" einbauen. Ausserdem entscheiden, ob "Kleinteile" im Standard an sein soll (Ben-Ziel Klinke sichtbar) | ICH (Viewer-Werkstatt) fuer die Hilfe; DEINE ENTSCHEIDUNG (Ben) fuer den Standard: Empfehlung an lassen fuer die Tuer-Ansicht, sonst aus |
| A4 | Infokarte "Tuer" in `data/descriptions.json:1692` ist veraltet ("Platzhalter, komplette Tuer folgt (M3)", Aufbau "Rahmen und Blatt", Masse 1000 x 2000); eingebaut ist `tuer_komplett` (27 Koerper) | ICH (Werkstatt Beschreibungen) |
| A5 | `check_bom.py` lieferte im ersten Lauf 13 von 14 PASS und im zweiten 14 von 14: pruefen, ob der Check von gleichzeitig laufenden Sitzungen (Schreiben an `data/`) abhaengt; ausserdem Hinweis in die Pruefer-Vorlage, dass `bom.py` generierte Daten neu schreibt | ICH (Orchestrator) |
| A6 | Soll-Wortlaut Punkt 3 im Blatt anpassen: `tuer_komplett.obj` hat 12 Koerper, die 27 ergeben sich aus `.obj` plus `.klein.obj`; Soll "Summe `viewer/defs`" braucht einen gesicherten Vorher-Wert (Datei im Paket) | ICH (Planer) |
| A7 | `nft_tisch_innen` (6 Koerper `Default`) und Nachmessung `check_parts.py` ueber alle Komponenten sowie `model_inventar.py` (zusammen rund 75 Minuten) im Hintergrund nachholen; `check_huelle.py:144` rechnet noch mit `strut_r` 45 (konservativ, 30 mm Luft zu viel) | ICH (Tische-Sitzung, Orchestrator) |

## Abschluss

Geprueft gegen: `solidcraft-cli.exe eval` (strebe_a/b, 7 Komponenten, tuer_komplett), eigenes Rollwinkel-Skript ueber 64 Streben, CAD-Probe (5 Streben, 6 Knoten, `inspect.interference`, plus Gegenprobe alter Rundstab), `bom.py`, `check_bom.py` (2 Laeufe), `check_huelle.py` 68/68, `du -cb viewer/defs`, Viewer auf Port 4521 (`viewerStand`), `git diff`/`git show --stat` der vier Commits, Blatt und Paket.
Offen: A1 bis A7 (siehe oben); Screenshots Tuer und Strebe nicht belegt; Gesamt-`check_parts` nicht belegt.
