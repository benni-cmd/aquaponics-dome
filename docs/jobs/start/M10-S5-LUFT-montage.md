# Start-Auftrag: Montage M10-S5-LUFT Teil A

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Montage, einzige Modell-Schreibsitzung zur Zeit. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen.

1. Grundlage: `docs/jobs/M10-S5-LUFT.md` Schritte 1 bis 3 (Teil A: Pool-Verteiler, 4 Scheibenbelueftungen, Rohre d25, Schwimmerventil, Port-Tabelle der Enden). Teil B NICHT bauen (Ben hat kein Ja gegeben, E13).
2. Pruefer-Auflage W37 A3: Bogen der DN100-Leerrohr-Fuehrung R500 bei Z -654 beachten (siehe `docs/jobs/pruefung/` zu W37-2/3), keine neue Kollision damit.
3. `gen_dome.py` darf fuer Teil A geaendert werden (Sperrliste fremder Aenderungen aufgehoben, Ben 04.11.); Zweitbecken-Stutzen nur als Annahme in der Port-Tabelle, nicht bauen.
4. Parallel laufen nur Daten-Sitzungen (`data/parts/`, `data/katalog.json`, Kennzeichnung `tuer`) und keine Aenderung an `scripts/components/strebe.py`. Nicht anfassen: Beet-Bauteile, `data/layout.json`, `data/leitungsnetz.json` ausser den Kanten von Teil A.
5. Messen: `sh scripts/build.sh` Exit 0, `check_latte` ohne neue Kollision gegen Runde 68 (115 KOLL Altbestand Leitungen), `check_walkways.py` PASS, danach `python viewer/export_model.py` Exit 0. Paket `docs/packages/m10-s5-luft.md` und `docs/loop-state.md` Runde 69 nachfuehren. Commits nur per Pfad, je Teilschritt, Push, WIP alle 20 Minuten. Danach STOPP.
