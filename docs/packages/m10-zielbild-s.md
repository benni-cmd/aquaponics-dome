# Paket: M10-ZIELBILD-S — Montage-Kette auf Zielbild S mit eingelassenem Pool (D88)

**Problem:** Die Kette M10-S3 bis S7 plant A+ (Heber, Feinfilter-Gruben, Absetzer, Bypass, Beet-Suempfe); D88 hat Zielbild S beschlossen, und im Modell stehen 56,3 m Leitung, die entfallen.
**Intent:** Das Modell zeigt die Anlage, die gebaut werden soll: einmal heben, frei in den Pool zurueck, wenig Graben, wenig Teile.
**Goal:** Nach M10-Z1 bis Z7 sind Pool nach D88, Beete auf dem Flur, Tauchpumpen, Wasserstationen, freie Ruecklaeufe und Schlamm draussen gebaut; die Pruefpunkte aus `docs/jobs/M10-ZIELBILD-S.md` Abschnitt 6 sind gruen.

Auftragsblatt: `docs/jobs/M10-ZIELBILD-S.md`. Rechnung: `python -X utf8 scripts/m10_zielbild_s_rechnung.py`. Grundlage: `docs/research/R57-systemreview.md` (Nachtraege D88, W86).

## Plan
1. [x] Planer: Blatt, Rechnung, Netz-v4-Vorschlag, Prinzipien-Check (05.11.2026).
2. Orchestrator: Roadmap M10-S3..S7 durch M10-Z1..Z7 ersetzen, M10-S2V schliessen, Netz v4.
3. Recherche ZR1 (Tauchpumpe) und ZR2 (Gelaenderhoehe), parallel.
4. Werkstatt ZW-A (Becken: Aufkantung, Gelaender, Einmuendung, Pegelschalter) und ZW-B (Wasserweg: Pumpe, Siebkorb, Hahntafel, Schlamm, Schlauch-Bibliothek, Kanal), parallel.
5. Montage M10-Z1 bis Z7, je Schritt Bau A+-Basis und Ring B2.
6. Pruefer je Meilenstein (nach Z2, nach Z4, nach Z7).

## Stand
- 05.11.2026, Planer: Blatt und Rechenskript geschrieben, nichts gebaut. Gemessen:
  1. Rueckbau 63 Trassen, 56,3 m (45,3 m unter Flur), 20 Zusatzteile, 3 Gruben.
  2. Pool: Spiegel Z 515 -> -150, Rand 650 -> 150 (Aufkantung), Innenboden -2370, 26,4 m3 bleiben.
  3. Beete 162 bis 209 mm hoeher auf den Flur.
  4. Gelaender passt nur auf die Aufkantung und hoechstens 750 mm hoch unter den Kragarmen der Innentische (Ben-Frage).
  5. Wasserstation mit Hahn je Strang statt je Abnehmer: 31/29 m statt 123/127 m Leitung je Linie (Abweichung von R57 2a, Ben-Frage).

## DoD
1. Pruefpunkte 1 bis 5 des Blatts von einem fremden Pruefer als PASS belegt.
2. Viewer-Screenshot im echten Browser: eingelassener Pool mit Gelaender, Beete auf dem Flur, Tauchpumpen, Wasserstation.
3. Bilanz unter Flur <= 25 m gemessen und in `docs/model-description.md`.
4. Jeder Schritt mit Pfad-Commit und Push.
