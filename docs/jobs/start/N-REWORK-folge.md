# Start-Auftraege nach der Maengel-Inventur (N-REWORK, W71), Grundlage `docs/model-maengel.md` (7d59462)

Fuer alle: PROJEKT aquaponics-dome, Kontext mit 1.000.000 Token rechnen, ueber 35 % melden statt anfangen; Nachtmodus D82 (kein Gesamtmodell-Bau, kein check_latte im Arbeitsbaum); Commits nur per Pfad, Push, WIP alle 20 Minuten; danach STOPP mit Kurzmeldung.

## A Planer (planer-m10-aplus): Leitungsordnung und Umbau des Gebauten
1. Standard `docs/leitungsordnung.md`: Trassen nur achsparallel in festen Korridoren (unter Tischen, an der Wandkrone, Graben), gebuendelt, Boegen nur 90/45 Grad, keine Bogenketten (M05, M06, M10), Halter je Rohrtyp mit Abstand nach Nennweite (M04: heute 0 Halter), Gaenge frei, Kreuzungen nur unterflur oder ueber Kopfhoehe.
2. Die Blaetter `docs/jobs/M10-S2N.md` bis `M10-S7.md` und `M10-S5-LUFT-B.md` auf diesen Standard bringen; neues Blatt `docs/jobs/M10-UMBAU.md` fuer den Umbau der schon gebauten Strecken S0 bis S2 und Luft A (M03 Schlammablass, M07 Luftrohre im Poolvolumen bewerten, M08 Ueberlauf frei, M09). Reihenfolge so, dass M10-UMBAU vor M10-S2N baut. Kanten-Liste M01 als Abdeckungs-Pruefpunkt (am Ende 0 Kanten ohne Rohr in A+).

## B Werkstatt (werkstatt-strebe): fehlende Bauteile aus M02 und Tank-Befund M11
1. Fehlende Netz-Bauteile bauen, soweit nicht vorhanden: Verteiler je Linie (`lt_verteiler`, Nennweite und Abgaenge aus `data/leitungsnetz.json`), Ruecklauf-Sammler; Biofilter Drittbecken pruefen. Teiledaten `data/parts/`, Bauteilblatt, Check.
2. M11: Tankdeckel zeigt im Viewer den Grund: Tankkoerper `tank_klein`, `tank_gross`, `tank_gross_t3` auf offene Flaechen am Kegelboden pruefen und ggf. schliessen.
Nur `designs/components/`, `scripts/components/`, `scripts/workshop/`, `docs/parts/`, `data/components/`, `data/parts/`.

## C Viewer (werkstatt-stueckliste-1b): M12 Anschluesse immer sichtbar
Stutzen, Muffen, Kugelhaehne und Abgaenge (Anschlussteile) bleiben auch bei ausgeschalteten Kleinteilen sichtbar (Ausnahmeliste als Datei, `viewer/export_model.py` + `viewer/index.html`), sonst sieht Ben Durchbrueche ohne Rohr. Export nur am Muster in Kopie; voller Export macht die naechste Montage. Screenshot Absetzer vorher/nachher.

## D Werkstatt Daten (preis-werkstatt-2): Pruefer-FAIL N-MODELL-KOMPLETT Punkt 5
`scripts/bom_artikel.py:237` setzt `platzhalterkoerper` an `PRF-st-strebe30x30` fest: entfernen, `bom.py`, `check_bom.py` Exit 0, Menge 209,082 m pruefen. Befund `docs/jobs/pruefung/N-MODELL-KOMPLETT.md` (291531f) Punkt 5.

## E Pruefer (pruefer-w40-beet): N-PREIS-PRUEF
Nach `docs/jobs/N-PREIS-PRUEF.md` Pruefpunkte 1 bis 5, Befund `docs/jobs/pruefung/N-PREIS-PRUEF.md`; Stand Commit 7d3fd5d. Du hast nichts davon gebaut.
