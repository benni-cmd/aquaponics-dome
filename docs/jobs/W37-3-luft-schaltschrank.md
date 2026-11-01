# W37-3 Gebläse mit Luftverteilern und Schaltschrank-Einfuehrung (Werkstatt B, Sitzung 3 von 3)

Problem: Die Luftkanten K44 bis K51 haben keine Quelle und keine Enden (L06): es gibt weder Geblaese noch Luftverteiler, Rueckschlagventile oder Scheibenbelueftungsteile im Modell. Der Schaltschrank ist als Komponente vorhanden (von `gen_dome.py` erzeugt, 800 x 500 x 1200), hat aber keine Leerrohr-Einfuehrung, sein Standort ist OFFEN (Ben, E13) (L08). Intent: S5 und S6 sollen Luft verlegen und Leerrohre am Schrank enden lassen koennen. Ziel in einem Satz: Zwei Geblaese-Baugruppen (N+1), ein Hauptverteiler 6-fach, ein Pool-Verteiler 4-fach, Scheibenbelueftungsteile und eine Einfuehrungsplatte mit Leerrohr-Stutzen fuer den Schaltschrank, jeweils mit Ports, Blatt, Check und Bild.

## Aktualitaetspruefung (01.11.2026, Planer)
Ergebnis: **angepasst** (Plan gilt als freigegeben).
- Roadmap L06, L08, W37 gueltig. R45 Abschnitt 4 hat den Widerspruch 130 gegen 25 bis 63 l/min geloest (Planwert 130, Spitze 205 l/min, zwei Linear-Membranpumpen N+1, mindestens 26 kPa); die Netzkanten K44 bis K51 sind in Version 3 uebernommen.
- **Standort Schaltschrank OFFEN (Ben, E13)**: Plan nimmt nur fuer die Kabelrechnung Az -85 / r 5750 an. Dieses Blatt plant **nur das Bauteil** mit Leerrohr-Einfuehrung, nicht den Ort; kein Eingriff in `gen_dome.py` und keine Neuberechnung der Lage.
- Kabeleinfuehrung kommt aus W39 (Teil 9); W39 laeuft vor W37.
- Offen aus R45 Abschnitt 4 (nicht in dieser Sitzung zu klaeren): Kennlinie bei 26 kPa (Datenblatt, Werkstatt/Beschaffung), Notstromkonzept (Ben/Orchestrator), Biofilter-Luft K45/K46 (Mengen nach Traegerhersteller), Zweitbecken K51 wenige l/min [A].
- Die Rueckschlagventil-Regel (zweite Quelle offen) wird als Regel im Blatt gefuehrt, nicht neu geprueft.

## Eingaben (nur diese)
- `docs/research/R45-hydraulik-auslegung.md` Abschnitt 4 (Zeilen 225 bis 279): Tabelle Empfehlung 1 bis 7, Kanten K44 bis K51.
- `data/leitungsnetz.json` per Python: Knoten `belueftung`; Kanten K44 bis K51; `kabel`-Eintrag "schaltschrank -> geblaese_fisch" (nur die Zeile mit 204 W).
- `docs/parts/leitungsteile.md` Konvention (Zeilen 7 bis 30) und W36-Abschnitt Verteiler d50 (ab Zeile 222) als Muster fuer Mehrfach-Verteiler; `scripts/workshop/leitung_w36.py` (`verteiler_d50`) und `leitung.py` (`verteiler`, `rohr`, `kugelhahn`, `save`) als Bauvorlage.
- Schaltschrank: `data/params.json` Schluessel `cab_x`, `cab_y`, `cab_z` (800 x 500 x 1200, [A] "ref-5 geschaetzt"), `data/descriptions.json` Zeile 1168 (`^schaltschrank`), `scripts/gen_dome.py` Zeilen 490 bis 499 **nur lesen**.
- W39-Ergebnisse: `docs/parts/leitungsteile.md` Abschnitt "Ergaenzung W39" (Rueckschlagventil d25/d20/d40, Kabeleinfuehrung DN50/DN100, Kappe).

## Teile
### Teil 1 Luft-Baugruppe `geblaese_luft` (zwei Stueck, N+1)
Mini-Plan zuerst im Blatt. Handelsteil-Platzhalter nach R45: **Linear-Membranpumpe** Klasse 200 l/min bei mindestens 26 kPa, 42 bis 48 dB, 100 bis 250 W (Beispielreihe Hiblow HP-200 mit 200 l/min bei 20 kPa und 250 W, HP-120LL mit 120 l/min bei 17,7 kPa; bei 26 kPa weniger, Kennlinie offen) [Q] Haendlerangaben, Kennlinie [A]. Koerper als Quader mit Stutzen d20 (Abmessungen Platzhalter, aus Katalog nachzumessen), Befestigung Schaltschrankbereich; Luftleitung wird **ueber dem hoechsten Wasserspiegel** (Z > 515 plus Reserve) gefuehrt (Schleife) mit Rueckschlagventil (R45 Empfehlung 7). Ports: Luftaustritt d20/d25, Stromanschluss (Kabeleinfuehrung). Nicht erfinden: keine Hersteller- oder Gewichtsangabe ohne Quelle; Gewicht als [A] kennzeichnen.

### Teil 2 Hauptverteiler `luftverteiler_6` und Pool-Verteiler `luftverteiler_4`
Beide nach dem Muster `lt_verteiler_d50` (Sammler als Formstueck, Abgaenge als Zapfen, Teilung 120). Fest vorgegeben:
- **Hauptverteiler 6-fach** am Geblaese: Abgaenge Pool (d40, K44), Biofilter 1 und 2 (d25, K45/K46), Drittbecken (d20, K49), Zweitbecken (d20, K51), Puffer/Absetzer (d20, K47/K48 optional); je Abgang Kugelhahn und Rueckschlagventil aus der Bibliothek/W39; Sammler d40.
- **Pool-Verteiler 4-fach** am Becken: vier Abgaenge d25 [A, 33 l/min je Abgang] fuer vier Scheibenbelueftungsteile; Sammler d40 mit Zulauf K44 (Planwert 130, Spitze 205 l/min).
Strom und Geschwindigkeit je Abgang im Blatt rechnen (Innen-Ø aus der Bibliothek; Hinweis R45: d40 bei 200 l/min 3,2 m/s, Innen-Ø 36,2). Eigenkonstruktion aus Handelsteilen (L21): Stueckliste mit T-Stuecken, Reduzierungen, Haehnen und Rueckschlagventilen angeben, damit der Nachweis in N-BESCHAFFUNG moeglich ist.

### Teil 3 Scheibenbelueftungsteile `luft_scheibenbelueftung`
EPDM-Membran-Scheibenbelueftungsteil Ø 215 bis 270 mm [A, Handelsmass], Parameter `d` (Standard 270), Anschluss d25 senkrecht nach unten, Stuetzfuss; 4 Stueck im Pool, Biofilter-Rohr-/Plattenbelueftungsteile nur als Platzhalter-Hinweis (Menge nach Traegerhersteller, K1). Nur ein Teil; Variante fuer Drittbecken K49 (Luftstein klein) als Parameter, kein eigenes Bauteil.

### Teil 4 `schrank_einfuehrung` (Schaltschrank, nur das Bauteil mit Leerrohr-Einfuehrung)
Neue Komponente **neben** `schaltschrank.sc` (Name mit `schrank_`, nicht `schaltschrank`, damit das Muster `^schaltschrank` der descriptions nicht greift und `gen_dome.py` unangetastet bleibt): Einfuehrungsplatte am Schrankboden (Boden 800 x 500, Blech [A]) mit Ausschnitten und je einer `lt_kabeleinfuehrung_dn100` (230-V-Trunk) und `lt_kabeleinfuehrung_dn50` (Signal-Trunk) aus W39, Leerrohr-Bogen aus der W36-Bibliothek darunter (Abstand der beiden Rohre >= 200 mm wegen EMV, Plan Abschnitt 4 Regel 9). Ports: Leerrohr DN100 und DN50 nach unten (unterflur Z -100 bis -400), Schrank-Anschlussflaeche. **Standort nicht enthalten**: Koordinaten des Bauteils sind lokal; die Montage setzt es nach E13. Gebläse-Strom 204 W und 8 Pumpenkabel nur als Hinweis auf die Kabelrechnung des Orchestrators, nicht berechnen.

## Gemeinsame Ergebnisse
Bauteile in `designs/components/`, Generatoren in `scripts/workshop/` (`geblaese_luft.py`, `luft_verteiler.py`, `schrank_einfuehrung.py`), Checks, Bauteilblaetter per `partsheet.py`, `data/components/*.json`, `data/descriptions.json` (neue Gruppen vor `^puffer` einsortieren; `^luft`/`^geblaese`/`^schrank_e` vorab gegen `grep -n '"match"'` pruefen), Bilder per `scripts/archive_render.py --role werkstatt`, Zeile in `docs/workshop-state.md`. Je Teil ein Commit, dazwischen push.

## Nicht anfassen
`designs/components/schaltschrank.sc` (von `gen_dome.py` erzeugt), `scripts/gen_dome.py`, `data/params.json`, `scripts/leitungen.py`, `data/leitungsnetz.json`, `data/roadmap.json`, `scripts/system_specs.py` (Orchestrator), die fremden Dateien aus `docs/workshop-state.md`. Nichts zu Sumpf, Schlammfass, Aktivkohle, Stutzen Drittbecken.

## Ergebnis
`geblaese_luft.sc`, `luftverteiler_6.sc`, `luftverteiler_4.sc`, `luft_scheibenbelueftung.sc`, `schrank_einfuehrung.sc` samt Generatoren, Checks, Blaettern, JSON, descriptions, Bildern. Kurzmeldung: je Teil eine Zeile (Masse, Ports, offene Fragen); an den Orchestrator: Schaltschrank-Standort E13 offen, Notstromkonzept offen, Kennlinie bei 26 kPa offen.

## Pruefpunkte (fuer den Pruefer)
1. Check aller Teile PASS (Aufruf im Blatt-Abschnitt "Pruefung"; Soll: keine FAIL-Zeile).
2. Hauptverteiler hat genau 6 Abgaenge und Pool-Verteiler genau 4; Port-Tabelle nennt K44 bis K51 passend (`grep -c "K4[4-9]\|K5[01]" docs/parts/luftverteiler_6.md`, Soll >= 6), DN je Abgang wie Netz (d40/d25/d20).
3. Strom je Abgang im Blatt nachgerechnet: Summe der Abgangsstroeme des Pool-Verteilers 4 x 33 = 132 l/min gegen Planwert 130 (Abweichung unter 2 %); Hauptverteiler Einlauf 130 l/min Pool plus Reserve im Blatt benannt.
4. `schrank_einfuehrung`: beide Einfuehrungen vorhanden (DN100, DN50), Abstand der Achsen >= 200 mm, Interferenz 0 gegen die Schrankwand; `schaltschrank.sc` und `gen_dome.py` unveraendert (`git diff HEAD --stat -- designs/components/schaltschrank.sc scripts/gen_dome.py`, Soll: leer fuer diese Sitzung; bestehende fremde Aenderungen nicht mitzaehlen).
5. Herkunftstabellen trennen belegt, gerechnet, Annahme; Geblaesetyp nur als Beispielreihe mit Vermerk "Beispiel", Kennlinie bei 26 kPa als OFFEN gefuehrt.

## Start-Hinweis fuer die Bau-Sitzung
1. W39 vorher (Rueckschlagventil d40/d25/d20, Kabeleinfuehrung DN50/DN100, Kappe d20); fehlt ein Teil, Platzhalter und Vermerk.
2. Standort Schaltschrank nicht entscheiden und nicht in `gen_dome.py` eintragen; `schaltschrank.sc` ist eine fremde, modifizierte Datei (`git status`), nicht committen.
3. Der Verteiler laeuft nach dem Muster W36 (Sammler als Formstueck, Zapfen); bei Boolean-Fehlern "implausible result volume" Teile als eigene Koerper mit 1 mm Ueberlappung bauen.
4. Alle Geblaese- und Belueftungs-Masse sind Handelsmass-Platzhalter [A]; Datenblatt-Recherche ist Sache von N-BESCHAFFUNG.
5. Limit: vier Teile, aber nur zwei Teile-Pakete (Luft, Schrank); bei Kontext ueber 60 Prozent nach dem letzten Commit Stand in `docs/workshop-state.md` und stoppen, Reihenfolge dann: Teil 2, Teil 1, Teil 4, Teil 3.
