# M10-S5-LUFT Luft- und Frischwasserbauteile im Dom setzen (abgetrennter Teil von M10-S5, Montage)

Planer: Sonnet 5.5, 04.11.2026. Nur gelesen, kein Modell, keine Daten, keine Roadmap geaendert. Mini-Plan: `docs/packages/m10-s5-luft.md`. Start-Auftrag: `docs/jobs/start/M10-S5-LUFT-planer.md`.

**Problem:** Die Bauteile aus W37-2 (Aktivkohle-Station T83, Schwimmerventil T84, Drittbecken-Stutzen) und W37-3 (Geblaese T85, Hauptverteiler T86, Pool-Verteiler T87, Scheibe T88, Schrank-Einfuehrung T89) liegen als Dateien vor, sind aber im Dom nicht gesetzt; die Luftkanten K44 bis K51 und die Frischwasserkanten K39 bis K43 und K52 haben im Modell weder Quelle noch Ende (L05, L06, L09).
**Intent:** Das, was in jeder Kreislaufvariante (E20) gleich ist, im Dom setzen, damit S5 nach Bens Entscheidung am 05.11. nur noch die abhaengigen Kanten verlegt.
**Ziel in einem Satz:** Pool-Verteiler mit vier Scheiben und Schwimmerventil am Pool gesetzt, die Enden an Drittbecken und Zweitbecken benannt, alles Abhaengige als "OFFEN (E20)" oder "OFFEN (E13)" gefuehrt; die Technikbereich-Gruppe (Geblaese, Hauptverteiler, Aktivkohle-Station) nur auf Bens Ja zu einem vorlaeufigen Ort.

## Aktualitaetspruefung (04.11.2026, Regel W44)
Ergebnis: **angepasst** (Antwort auf die Frage des Start-Auftrags: **teilweise ja**). Geprueft gegen: `git log --oneline -6` (854276e W37-3, 83d15c0 W37-2), `data/roadmap.json` M10-S5 (gestoppt bis E20), `data/leitungsnetz.json` Version 3 (K39 bis K52), `docs/packages/w37-2-3-frischwasser-luft.md`, `docs/loop-state.md`, `scripts/gen_dome.py` und `scripts/leitungen.py` per Grep, `data/params.json`, `data/layout.json`.
- **E20 blockiert die Luft nicht** (Variantenbefund W37-3: Luft laeuft getrennt vom Wasserumlauf). E20 beruehrt nur den Zulauf K40 am Schwimmerventil (Variante B kann ihn aus dem Ring speisen) und die Kabelzahl der Schrank-Einfuehrung.
- **E13 blockiert die Technikbereich-Gruppe:** Geblaese, Hauptverteiler und Aktivkohle-Station stehen "im Schaltschrankbereich" (Netz Knoten `belueftung`, `docs/parts/aktivkohle_station.md` Zeile 99 und 154). Jede der Kanten K39, K40, K44 bis K48, K50, K52 hat dort ein Ende. `gen_dome.py` Zeile 494 setzt den Schrank "neben den Vorbau" (D62); der Plan-Ort Az -85 / r 5750 ist nur Kabelrechnung. Der Ort ist nicht entschieden.
- **Biofilter und Absetzer** (K45 bis K48): Orte haengen an E20/D75 (Subtank V4 aendert den Hauptkreislauf); K47/K48 sind ausserdem "optional". Alles dazu bleibt offen.
- Gesetzt sind schon: Pool (cx -36, cy 20, Ø 3890, Spiegel Z 515), Zweitbecken (`layout.json` pool2, Spiegel Z 515), Drittbecken `becken_dritt_klein` (`gen_dome.py` Zeile 345, r 4970 / Az -30). Offen sind nur die neuen Teile.

## Aufteilung
| Teil | Inhalt | Status |
|---|---|---|
| **A** | Pool-Verteiler `luftverteiler_4` und 4 Scheiben `luft_scheibenbelueftung` im Pool; Schwimmerventil `schwimmerventil_pool` am Pool-Rand; Port-Liste der Enden an Drittbecken (K41, K42, K43, K49) und Zweitbecken (K51) | **freigegeben, bauen** (variantenunabhaengig, ohne E13) |
| **B** | Technikbereich-Gruppe an einem vorlaeufigen Ort: `geblaese_luft` x2, `luftverteiler_6`, `aktivkohle_station`, `schrank_einfuehrung`; Kanten K39, K41, K44, K49, K50, K51, K52 und K40 bis zum Schwimmerventil | **nur auf Bens Ja** (DEINE ENTSCHEIDUNG unten); sonst **OFFEN (E13)** |
| **C** | K40 Zulauf (Station oder Ring), K45 bis K48 (Biofilter, Absetzer), Kabelzahl und Fuellgrad der Einfuehrung | **OFFEN (E20)**, nicht bauen |

**DEINE ENTSCHEIDUNG (Ben):** Darf Teil B an einem vorlaeufigen Technikbereich-Ort gebaut werden, naemlich am heutigen Schrank-Ort aus `gen_dome.py` (D62), als eine verschiebbare Komponentengruppe (eine Translation setzt sie um, die Leitungen dieser Gruppe werden dann neu verlegt)? Empfehlung: ja, weil es E13 nicht vorwegnimmt und alle Luftkanten sichtbar macht. Ohne Ja bleibt Teil B OFFEN (E13).

## Eingaben (nur diese; Zeilen selbst nachsehen)
- `data/leitungsnetz.json` (nur lesen): Kanten K39 bis K52; Knoten `belueftung`, `aktivkohle`, `frischwasser`, `pool`, `zweitbecken`, `drittbecken`.
- Bauteile `designs/components/`: `luftverteiler_4.sc`, `luft_scheibenbelueftung.sc`, `schwimmerventil_pool.sc`; fuer Teil B zusaetzlich `geblaese_luft.sc`, `luftverteiler_6.sc`, `aktivkohle_station.sc`, `schrank_einfuehrung.sc`. Ports und Ursprung je Teil in `docs/parts/<teil>.md`.
- `scripts/gen_dome.py`: `place_instances` (Zeile 345 als Muster fuer das Drittbecken), `pool_dims` (Zeile 84, Beckenboden und Rand); `data/params.json` pool_rim 650, pool_depth, pool3_r, pool3_az; `data/layout.json` pool, pool2.
- `scripts/leitungen.py` und `scripts/trassen_linie.py` (Trassen-Muster fuer Kanten; Teil B).

## Schritte (je Schritt ein Commit)
1. **Teil A, Pool:** `luftverteiler_4` am Pool-Rand setzen (Muffe A zeigt weg vom Becken zum Technikbereich; Azimut als Annahme [A] markieren, verschiebbar). Vier Scheiben auf einem Kreis r 1000 [A] um die Beckenmitte (Mitte hat den Bodenablauf), Fuss auf dem Beckenboden, Winkel 45/135/225/315 [A]; je Scheibe ein Rohr d25 vom Abgang des Verteilers zum Anschluss (Rohr aus der Bibliothek; Ende am Fuss).
2. **Teil A, Schwimmerventil:** `schwimmerventil_pool` so setzen, dass die Rohrachse auf Z 710 liegt (Spiegel Z 515 plus 195) und die Kugel auf dem Spiegel schwimmt; Port A (Zulauf, nach aussen) als **OFFEN (E20)** markieren, kein Rohr dorthin.
3. **Teil A, Enden:** Drittbecken: Stutzen K41/K42/K43/K49 liegen im Bauteil; Lage im Dom messen und in `docs/packages/m10-s5-luft.md` als Port-Tabelle ablegen. Zweitbecken: Stutzenlage fuer K51 (Luft) und Frischwasser als Annahme eintragen; die Aenderung an `gen_dome.py` (Roadmap: "Zweitbecken-Stutzen in gen_dome") nur nach Rueckfrage beim Orchestrator, weil `gen_dome.py` fremd veraendert ist.
4. **Teil B (nur mit Bens Ja):** Technikbereich-Gruppe an den heutigen Schrank-Ort setzen; Geblaese x2 nebeneinander, Hauptverteiler Port A nach der Reduzierungskette, Aktivkohle-Station wandnah; Kanten K44 (Hauptverteiler zum Pool-Verteiler), K49, K51, K41, K52, K39 und K40 bis zum Schwimmerventil als Trassen. Alle Teile der Gruppe unter einer Gruppen-Komponente mit dem Vermerk "vorlaeufig, E13".
5. Paket nachfuehren, `docs/workshop-state.md`/`docs/loop-state.md` Zeile, Bild je Teil.

## Nicht anfassen
`designs/components/schaltschrank.sc` und `scripts/gen_dome.py` (fremd veraendert; Aenderung nur nach Rueckfrage), `data/params.json`, `data/leitungsnetz.json`, `data/roadmap.json`, `data/katalog.json`, `data/beschaffung/`, `viewer/`, fremde `.sc`; K45 bis K48, K40-Zulauf, Kabelzahl (OFFEN E20); Standort des Schranks (OFFEN E13).

## Ergebnis
Teil A im Dom gesetzt (Verteiler, 4 Scheiben, Schwimmerventil, Rohre Verteiler zu Scheiben), Port-Tabelle der Enden, Paket nachgefuehrt; mit Bens Ja zusaetzlich Teil B. Kurzmeldung: was gesetzt ist, was OFFEN (E20)/(E13) bleibt.

## Pruefpunkte (fuer den Pruefer, fremd messbar)
1. Pool-Verteiler und Scheiben: genau 1 Instanz `luftverteiler_4` und 4 Instanzen `luft_scheibenbelueftung` im Dom (`solidcraft-cli eval designs/dome.sc`, Komponentennamen zaehlen; Soll 1 und 4); jede Scheibenmitte liegt innerhalb des Pools (Abstand zur Beckenmitte unter 1945 minus 135 = 1810 mm) und die Membran-Oberkante unter Z 515.
2. Schwimmerventil: Rohrachse Z 710 (+-1 mm) und Kugelmitte Z 535 (+-1 mm) im Dom gemessen (Bbox der Komponente).
3. Rohre Verteiler zu Scheiben: 4 Rohre d25, Enden fluchten mit den Ports (Abstand Port zu Rohrende unter 1 mm); `scripts/check_leitungen.py` 0 Verstoesse; `inspect.interference` ueber die neuen Komponenten: 0 neue Treffer.
4. Variantenbefund im Blatt und im Paket: jede Kante mit E20- oder E13-Bezug steht als "OFFEN (E20)" oder "OFFEN (E13)" (`grep -c "OFFEN (E20)\|OFFEN (E13)" docs/packages/m10-s5-luft.md`, Soll mindestens 4); keine Leitung zu K40-Zulauf, K45 bis K48 gebaut.
5. Nichts Fremdes veraendert: `git diff HEAD --stat` zeigt nur die im Blatt genannten Pfade; `git hash-object designs/components/schaltschrank.sc scripts/gen_dome.py data/params.json data/leitungsnetz.json` gleich dem Stand vor der Sitzung.

## Start-Hinweis fuer die Montage-Sitzung
1. Teil A bauen ohne Rueckfrage; Teil B nur, wenn der Orchestrator "Ben: Ja vorlaeufiger Ort" ins Start-Prompt schreibt.
2. Alle Bauteil-Ursprungen stehen in `docs/parts/<teil>.md` (Ports): Scheibe Port A unten, Verteiler Port A = Muffe, Schwimmerventil Port A = Muffe mit Rohrachse; Geblaese-KS Mitte Standflaeche.
3. Bekannte Falle: `component.insert_design` kennt nur `translate`; Drehen per `occurrence.move occurrence="<Name>:1" space=world matrix=[12 Zahlen]` (W37-3).
4. Kernel: Schnitte mit gleichem Durchmesser von Lauf und Abgang brauchen 60 s (W37-2); nicht noetig bei dieser Montage, da Bauteile fertig sind.
5. Limit: ein Paket, danach Stand in `docs/loop-state.md` und stoppen; Teil B und C je eigene Sitzung.
