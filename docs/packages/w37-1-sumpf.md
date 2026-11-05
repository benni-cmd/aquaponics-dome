# Paket W37-1: Beet-Sumpf und Schlammfass (Werkstatt)

**Problem:** Das Beetwasser kommt nicht zurueck in den Pool (Beetablauf liegt unter dem Pool-Spiegel, Luecke L04), und die Schlammleitungen K07/K23 der Absetzer enden im Nichts (Luecke L01). Die Bauteile `beet_sumpf` und `schlammfass` fehlen.
**Intent:** Die Montage (M10 S4/S5) soll Sumpf und Fass mit Ports ans Netz setzen koennen; Eigenkonstruktion aus Handelsteilen (L21), Kaufteile mindestens in Europa (D76).
**Goal:** Drei Bauteile `beet_sumpf`, `schlammfass`, `lt_kugelhahn_feder_d40` mit Generator, Check PASS, Bauteilblatt, Teiledaten, Beschreibung, Bild; die fuenf Pruefpunkte des Blatts `docs/jobs/W37-1-sumpf-schlammfass.md` gemessen und hier eingetragen.

Blatt: `docs/jobs/W37-1-sumpf-schlammfass.md` (Aktualitaetspruefung 05.11.2026: angepasst).

## Plan
1. [x] Aktualitaetspruefung W44 gegen Roadmap (E19, E20, L01, L04), D81 und M-BEET-TAUSCH; Einlaufhoehe gegen den neuen Ablaufport (Ergebnis im Blatt).
2. [ ] `beet_sumpf`: Generator `scripts/workshop/beet_sumpf.py`, Parameter `data/components/beet_sumpf.json`, Check `check_beet_sumpf.py`, Blatt, Teiledaten, Beschreibung, Bild. Commit + Push.
3. [ ] `schlammfass` und `lt_kugelhahn_feder_d40` (`scripts/workshop/leitung_w37.py`): wie 2. Commit + Push.
4. [ ] Pruefpunkte 1 bis 5 messen, hier eintragen; `docs/workshop-state.md` Zeile. Commit + Push, Kurzmeldung, STOPP.

## Mini-Plan beet_sumpf
- Bauteil-KS: Ursprung Mitte Tankboden, Z hoch. Tank Ø 800 aussen, H 1000, Wand 8 [A]; Schachtaufsatz Ø 600 x 200 (`aufsatz_h`, Einlaufhoehe gegen Beetablauf, Blatt Punkt 6); Deckel begehbar Ø 700 x 40 auf dem Aufsatz.
- Zulauf Muffe d50 (`zulauf_d`) radial bei Z 800 (Sohle), Richtung -X.
- 2 Pumpen (`pumpen` = 2, E19) als Platzhalter-Quader auf dem Boden, je Steigrohr d40 mit Rueckschlagventil d40 (Masse W39), Sammelrohr unter dem Deckel, Port d40 oben (+Z).
- Schwimmerstange mit drei Schwimmern (Mitte bei 120, 320, 620), zwei Kabeldurchfuehrungen M25 (Pumpen/Schwimmer, Ablaufwaechter A+), Entlueftung d32 mit Gitterkappe.
- Einzelkoerper mit 1 mm Ueberlappung statt Boolean an duennen Mantelflaechen.

## Stand
05.11.2026: Schritt 1 erledigt (Blatt-Abschnitt "Aktualitaetspruefung (05.11.2026, Werkstatt)").

## DoD
Pruefpunkte 1 bis 5 des Blatts mit Befehl und Messwert in der Tabelle unten.

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
