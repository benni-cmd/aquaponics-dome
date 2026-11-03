# Work package: W40-BEET Beet leert sich ganz (Bauteil ibc_beet)

**Problem:** Der Wasserraum unter dem Siebboden (485 l aussen_800, 420 l innen) bleibt dauernd gefüllt, weil die Glocke auf dem Sieb steht (R51 Befund 5a); es droht Plörre. Schutzkorb, Reinigungszugang und Reduktion d40 × d25 fehlen.
**Intent:** Ben (03.11.2026): das Beet leert sich ganz, nur Standardteile, alle Kaufteile mindestens in Europa bestellbar (D76), Selbstbau nur wenn super simpel.
**Goal:** `ibc_beet` mit ungelochtem Sperrboden, Kerben-Glocke (Film höchstens 12 mm, Rest höchstens 10 l bei aussen_800), Lochblech-Schutzkorb, stehendem Schacht d110 und Reduktion; Entleerzeit bleibt im Bereich R45; Check, Interferenz, Bauteilblatt grün. Blatt: `docs/jobs/W40-BEET.md`.

## Plan

1. [ ] Werkstatt 1a: `scripts/w40_beet_rechnung.py` schreiben und laufen lassen
2. [ ] Werkstatt 1b: `ibc_beet.py`, Parameter, Check ändern, vier Typen bauen
3. [ ] Werkstatt 1c: Bauteilblatt neu erzeugen, Interferenz und Körpernamen prüfen
4. [ ] Prüfer: `docs/jobs/pruefung/W40-BEET.md` nach den fünf Prüfpunkten
5. [ ] Orchestrator: Netz K14/K30 Höhe und Sumpf-Einlauf, Wasserbilanz ohne Wasserräume, Montage baut 14 Beete neu

## Status

03.11.2026: Planer-Blatt geschrieben, Aktualität angepasst. Gewählt V3 Sperrboden; V1 (Schacht bis Boden) verworfen, weil ein Zyklus 649 l den Beet-Sumpf (500 l) sprengt. Nichts gebaut. Offen (Ben): V3 bestätigen, Schutzkorb beim Metallbauer, Standrohr d25 mit Reduzierhülse oder d32.

## Definition of Done

Geprüft gegen: `python -X utf8 scripts/w40_beet_rechnung.py`, `python scripts/workshop/check_ibc_beet.py` (Exit 0), `solidcraft-cli.exe eval` je Typ (Körpernamen, Siebboden ohne Lochabzug), Teileliste mit Hersteller und Artikel im Bauteilblatt.
Offen: Bau (nichts begonnen), Dichtheit und Anspringen am Muster, Datenblätter der Kaufteile, Dichtband und Kleber ohne Quelle.
