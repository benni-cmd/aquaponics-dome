# Paket: N-AUTOBAHN-V2 — Wasserautobahn mit Stelzen, Schlauch-Abzweigen und Schlauch-Ruecklauf bauen (W78)

**Problem:** Die Wasserautobahn (Ring B2) gibt es nur als Bauteile und Rechnung; im Modell fehlt sie, und der alte Plan R1/R2 kannte weder passende Stelzen noch Schlaeuche noch einen fairen Zahlenvergleich.
**Intent:** Ben und Leon sehen beide Kreislaeufe im Viewer so, wie sie gebaut wuerden, und entscheiden E20 auf gemessenen Zahlen.
**Goal:** `designs/dome-ring_b2.sc` enthaelt Ring, 10 Stuetzpunkte, 18 Ausleger, 38 Schlauch-Fallleitungen, Einspeisung je Linie und Schlauch-Ruecklauf; die Pruefpunkte aus `docs/jobs/N-AUTOBAHN-V2.md` Abschnitt 6 sind fuer beide Varianten gruen; die Vergleichstabelle traegt Messwerte.

Auftragsblatt: `docs/jobs/N-AUTOBAHN-V2.md`. Rechnung: `python -X utf8 scripts/n_autobahn_rechnung.py`. Vorgaenger: `docs/packages/n-varianten.md` (V1a, V1b, VV, V2 gebaut).

## Plan
1. [x] Planer: Blatt, Rechnung, Vergleich und Empfehlung (05.11.2026).
2. Werkstatt WA-T Tragwerk: Portal-Joch, Ausleger, Montageschiene mit `lt_klemme_d75`, Ring-Ecke 36 Grad, Pegelschacht-Podest (sofort, parallel).
3. Werkstatt WA-S Schlauch: Fallleitung ID16/ID25, Schnellkupplung, Rueckschlagventil d50, Ruecklauf-Rinne, Bodenrinne, Schlauch d50 (sofort, parallel).
4. Orchestrator O1: Netz-Delta K60 bis K76 (Blatt 2.7), Roadmap-Eintrag.
5. Montage R1: Tragwerk, Ring, Einspeisung beider Linien (nach WA-T und Leitungsordnung v2).
6. Montage R2: Ausleger, 38 Fallleitungen, Ruecklauf, Viewer-Export, Screenshots (nach R1 und WA-S).
7. Pruefer: Pruefpunkte 1 bis 5 beider Varianten; Vergleichstabelle mit Messwerten nachtragen.

## Stand
- 05.11.2026, Planer: Blatt und Rechenskript geschrieben, nichts gebaut. Ergebnisse der Rechnung:
  1. Ring als Zehneck ueber der Mittelzone: 21,3 m, 10 Ecken, 7 Portal-Joche und 3 eigene Stelzen, kein Stuetzpunkt im Gang.
  2. 38 Fallleitungen: 12 direkt unter dem Ring, 26 ueber 18 Ausleger; Schlauch ID25 38,6 m, ID16 60,8 m.
  3. Pumpen: 617 W gegen 430 W (A+), wenn der Pegelschacht auf einem Podest steht; am Boden 754 W.
  4. Teile Zulauf 540 gegen 267; Mehrkosten mindestens 2.769 EUR (6 Posten ohne Preis); Graben Zulauf 0 gegen 4,6 bis 29,6 m.
  5. Empfehlung: A+ bleibt Bau-Empfehlung; Autobahn wird als vollwertige Anschauungs-Variante gebaut. Umkehr-Ausloeser stehen im Blatt Abschnitt 5.

## DoD
1. Pruefpunkte 1 bis 5 aus dem Blatt von einem fremden Pruefer als PASS belegt (`docs/jobs/pruefung/N-AUTOBAHN-V2.md`).
2. Viewer-Screenshot beider Varianten im echten Browser, Ring mit Schlaeuchen nur in Ring B2.
3. Vergleichstabelle im Blatt mit Messwerten aus den Trassen statt Rechnung.
4. Jeder Schritt mit Pfad-Commit und Push.
