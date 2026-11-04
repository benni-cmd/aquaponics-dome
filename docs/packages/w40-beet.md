# Work package: W40-BEET Beet leert sich ganz (Bauteil ibc_beet)

**Problem:** Der Wasserraum unter dem Siebboden (485 l aussen_800, 420 l innen) bleibt dauernd gefüllt, weil die Glocke auf dem Sieb steht (R51 Befund 5a); es droht Plörre. Schutzkorb, Reinigungszugang und Reduktion d40 × d25 fehlen.
**Intent:** Ben (03.11.2026): das Beet leert sich ganz, nur Standardteile, alle Kaufteile mindestens in Europa bestellbar (D76), Selbstbau nur wenn super simpel.
**Goal:** `ibc_beet` mit ungelochtem Sperrboden, Kerben-Glocke (Film höchstens 12 mm, Rest höchstens 10 l bei aussen_800), Lochblech-Schutzkorb, stehendem Schacht d110 und Reduktion; Entleerzeit bleibt im Bereich R45; Check, Interferenz, Bauteilblatt grün. Blatt: `docs/jobs/W40-BEET.md`.

## Plan

1. [x] Werkstatt 1a: `scripts/w40_beet_rechnung.py` schreiben und laufen lassen (Commit 3c4acc2)
2. [x] Werkstatt 1b: `ibc_beet.py`, Parameter, Check ändern, vier Typen bauen (Commit c9b7f50)
3. [x] Werkstatt 1c: Bauteilblatt neu erzeugen, Interferenz und Körpernamen prüfen (Commit 0f0c84a)
4. [ ] Prüfer: `docs/jobs/pruefung/W40-BEET.md` nach den fünf Prüfpunkten
5. [ ] Orchestrator: Netz K14/K30 Höhe und Sumpf-Einlauf, Wasserbilanz ohne Wasserräume, Montage baut 14 Beete neu

## Status

03.11.2026: Planer-Blatt geschrieben, Aktualität angepasst. Gewählt V3 Sperrboden; V1 (Schacht bis Boden) verworfen, weil ein Zyklus 649 l den Beet-Sumpf (500 l) sprengt. Nichts gebaut. Offen (Ben): V3 bestätigen, Schutzkorb beim Metallbauer, Standrohr d25 mit Reduzierhülse oder d32.

04.11.2026, Ben entscheidet (D77): V3 Sperrboden ja (Wasserraum und rund 6400 l Systemvolumen entfallen); Standrohr bleibt d25 mit Reduzierhuelse 32/25 im Tankverbinder; Schutzkorb Lochblech 5 mm, Zuschnitt und Rollen beim Metallbauer (Anfrage macht Ben). Werkstatt-Sitzung gestartet (Schritte 1a bis 1c).

04.11.2026, Werkstatt (Sonnet 5.5) Schritte 1a bis 1c gebaut und gesichert. Bezugsquellen-Nachtrag (Orchestrator) stand im Blatt und ist in die Teileliste übernommen.

- **1a** `scripts/w40_beet_rechnung.py`: Film aussen_800 9,3 l, innen_933 7,6 l, aussen_933 12,3 l; Entleerzeit d25 siehe Prüfpunkt 2; Systemvolumen stehendes Wasser 6400 l (V0) gegen 120 l Film (V3).
- **1b** `ibc_beet.py`, `check_ibc_beet.py`, `data/components/ibc_beet.json`, vier `.sc`: Sperrboden ungelocht (einzige Öffnung Durchführung d36), Glocke mit 4 Kerben 10 × 12, Medienschutz Lochblech V2A d110 × 1,5 (Modell: 2 Ringe × 12 Schlitze 5 × 50 = 6000 mm² = 15,8 × Standrohr) mit loser Kappe, Reinigungsschacht d110 stehend auf dem Sperrboden (x = −Li/2 + 250) mit Kappe und 2 Kerben, Reduktion d40 × d25 (Oberkante Port z −30, 50 mm), Tankverbinder D36 mit Reduzierhülse 32/25 im Boden und in der Platte. Check um 25 Messungen je Typ erweitert (Siebboden-Volumen, Kerben, Schlitzflächen, Schacht, Reduktion, Reduzierhülsen, Interferenz). Körper `Siebboden`, `Standrohr`, `Medienschutz` behalten ihre Namen.
- **1c** `docs/parts/ibc_beet.md` neu per `partsheet.py` (Generator um Abschnitt „Teileliste mit Bezug in Europa (D76)“ erweitert); Gewichte gefüllt ohne Wasserraum: aussen_800 784 kg, innen_933 634 kg, aussen_933 1027 kg (vorher 1670 kg).

### Messungen der fünf Prüfpunkte (selbst gemessen, 04.11.2026)

1. **Restwasser:** `python -X utf8 scripts/w40_beet_rechnung.py` → aussen_800 **9,3 l** (≤ 10 ✓), innen_933 **7,6 l** (≤ 8 ✓). Modell: `Siebboden` aussen_800 15,4685 l = Fläche × 8 mm minus Durchführung d36 (keine Löcher; `check_ibc_beet.py` PASS, Toleranz ±0,02 l; innen_933 12,5943 l). Kerben-Oberkante z 274 (aussen_800) und z 286 (innen_933) = Plattenoberkante + 12 ✓.
2. **Entleerzeit:** d25, h 0,30 / 0,45 / 0,60 m → 38,1 / 46,9 / 54,4 l/min. aussen_800 **3,6 bis 5,1 min** ✓ (Ablaufvolumen **194 l** nach R45-Definition, 196 l nach V3-Geometrie; das Blatt nennt 195 l, Differenz von 1 l kommt aus der gerundeten Fläche 1,95 m² gegen 1,936 m² gemessener Kontur). **Abweichung zu R45 4,3 bis 6,1 min ausgewiesen:** R45 setzt fest 234 l an (Herkunft nicht nachvollzogen), die Rechnung nimmt die Beetfläche; aussen_933 mit eigener Fläche 256 l → 4,7 bis 6,7 min; innen_933 158 l → 2,9 bis 4,1 min. Sollbereich R45 unverändert Maßstab.
3. **Check:** `python -X utf8 scripts/workshop/check_ibc_beet.py` → Exit 0, 190/190 PASS, 0 FAIL (vier Typen, inklusive Interferenz); danach `--no-interf` erneut: Exit 0, 187 PASS (Stand nach 1c).
4. **Körper und Interferenz:** `inspect.interference` je Typ (in `check_ibc_beet.py`): aussen_933 0, aussen_993 0, aussen_800 0, innen_933 0. Alle Körper benannt, keine `Body<n>` (Check PASS); `Reduktion`, `Reinigungsschacht`, `Medienschutz`, `Schutzkappe`, `Schachtkappe`, `Plattenhuelse`, `Reduzierhuelse_Boden`, `Reduzierhuelse_Platte` vorhanden; Gesamt-Box aussen_933 Z −80 bis 637, 40 Körper.
5. **Europa-Bezug:** `docs/parts/ibc_beet.md` Abschnitt „Teileliste mit Bezug in Europa (D76)“, 10 Zeilen. Durch den Bezugsquellen-Nachtrag (Orchestrator, 04.11.) sind Reduzierhülse 32/25 (Schwarte 75208, Bevo 7002656) und Kleber (Tangit PVC-U Plus, toom 8150236) „beschaffbar“; **nicht beschafft bleibt nur das Dichtband-Maß** („Maß offen“, Werkstoff EPDM-Zellkautschuk selbstklebend bei stuv.de; Zeile hat keinen Artikel). Das weicht vom Wortlaut des Prüfpunkts („Plattenhülse, Dichtband, Kleber als nicht beschafft“) ab, weil der Nachtrag die Blocker gelöst hat. Schutzkorb: Anfrage Metallbauer liegt bei Ben.

Ausgabe `python -X utf8 scripts/w40_beet_rechnung.py` (gekürzt auf die Zahlen):

```
aussen_800: Fläche 1.936 m2, Film 9.3 l (Wasserraum V0 485 l)
innen_933:  Fläche 1.575 m2, Film 7.6 l (Wasserraum V0 420 l)
aussen_933: Fläche 2.556 m2, Film 12.3 l (Wasserraum V0 640 l)
Siphon d25: h 0.30 m 38.1 | 0.45 m 46.9 | 0.60 m 54.4 l/min
aussen_800: 194 l -> 3.6 bis 5.1 min; innen_933: 158 l -> 2.9 bis 4.1 min; aussen_933: 256 l -> 4.7 bis 6.7 min
Kerben 4 x 10 x 12 = 480 mm2 (1.26x Standrohr 380 mm2)
Fluten aussen_800: 196 l, 24 bis 59 min bei 8,3 bis 3,3 l/min; innen_933 159 l, 19 bis 48 min
Systemvolumen: V0 6400 l stehendes Wasser; V3 120 l Film; Differenz 6280 l
Nachlaufbohrung d4 (nur falls nötig): 1,02 l/min (Cd 0,6) bis 0,51 l/min (Cd 0,3); Blatt nannte etwa 0,5
```

**Gebrochene oder angepasste Annahmen des Blatts:** (a) Ablaufvolumen 194/196 statt 195 l (Rundung). (b) Nachlaufbohrung 0,5 bis 1,0 l/min je nach Ausflussbeiwert, nicht fest 0,5. (c) Prüfpunkt 5 durch den Nachtrag verändert (siehe oben). (d) Die Reduzierhülse hat laut Bevo 22 mm Baulänge, im Modell ist sie ein Rohrstück von Hülsenlänge (Boden 39 mm, Platte 15 mm): Modell vereinfacht, offen.

## Definition of Done

Geprüft gegen: `python -X utf8 scripts/w40_beet_rechnung.py`, `python -X utf8 scripts/workshop/check_ibc_beet.py` (Exit 0, 190/190 PASS inkl. Interferenz 0 je Typ), `solidcraft-cli.exe eval` über `sc.evaluate` je Typ (Siebboden-Volumen ohne Lochabzug, Körpernamen), Teileliste mit Hersteller und Artikel im Bauteilblatt, Bezugsquellen-Nachtrag im Blatt.
Offen:
1. Prüfer (frische Sitzung) misst die fünf Prüfpunkte selbst: Orchestrator startet ihn.
2. Dichtheit des Sperrbodens und Anspringen bei 3,3 l/min nur am Muster prüfbar: Ben/Montage.
3. Dichtband-Maß (EPDM-Zellkautschuk, Spalt 2 mm) festlegen; Anfrage Metallbauer für den Schutzkorb: Ben.
4. Datenblätter der Kaufteile (Flansch D50, Reduktion 50 mm, Reduzierhülse 22 mm Baulänge) nicht gelesen: Annahmen [A].
5. Orchestrator/Montage: Netz K14/K30 `hoehe` und Sumpf-Einlauf, Wasserbilanz ohne Wasserräume (6280 l weniger), Montage baut 14 Beete neu, `data/descriptions.json` (Beet-Text nennt Schlitze, Siebboden, Standrohr 220) nachziehen.

04.11.2026 nachts, Pruefer: PASS mit Auflagen (2dd81ff). Orchestrator: Auflage 1 korrigiert (190/190), Auflage 2 entschieden (D78, Sollbereich je Typ), Netz K14/K30 Hoehe und Text nachgefuehrt, Beschreibung Substratbeet nachgefuehrt. Auflagen 3 und 4 (Bauteilblatt-Artikel, Check-Text) und 5 (Huelsenlaenge, Flansch) gehen in den Montage-Schritt Beete (Werkstatt-Vorlauf).
