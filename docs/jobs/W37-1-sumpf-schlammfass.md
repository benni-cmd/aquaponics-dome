# W37-1 Beet-Sumpf und Schlammfass (Werkstatt B, Sitzung 1 von 3)

Problem: Der Beetablauf liegt etwa 600 mm unter dem Pool-Spiegel (Z -100 gegen Z 515); ohne Sumpf mit Pumpe kommt das Beetwasser nicht zurueck (L04, Kanten K14/K30 enden in `beet_sumpf_1/2`, K58/K59 haengen an der Pumpe). Die Absetzer-Schlammleitungen K07/K23 enden im Nichts (L01, Knoten `schlammfass_1/2`). Beide Teile fehlen im Modell. Intent: S4 (Beet-Rueckfluss) und S5 sollen den Sumpf und das Fass als Bauteile mit Ports setzen koennen; Eigenkonstruktionen bestehen aus Handelsteilen (L21). Ziel in einem Satz: Zwei Bauteile `beet_sumpf` und `schlammfass` mit Ports am Netz (K14, K58, K30, K59, K07, K23), Bauteilblatt, Check und Bild, plus Kugelhahn-Variante mit Federrueckzug, damit L01 und L04 schliessbar sind.

## Aktualitaetspruefung (01.11.2026, Planer)
Ergebnis: **angepasst** (Plan gilt als freigegeben).
- Roadmap W37, L01, L04 gueltig; Netzliste Version 3 (b98c4c1) hat die Knoten `beet_sumpf_1/2`, `schlammfass_1/2` und die Kanten K07, K14, K23, K30, K58, K59 mit den R45-Massen (gelesen, Wortlaut unten).
- E12 (Schlammsammler) steht als **Standardannahme** (Fass 200 bis 220 l in Grube); Ben hat nicht widersprochen, daher baubar; falls Ben anders entscheidet, ist nur das Bauteil `schlammfass` betroffen.
- Beet-Redundanzpumpe (zweite Pumpe) bleibt **OFFEN (Ben)** (R45 Abschnitt 3 Punkt 3): die Skizze plant **eine** Pumpe; der Sumpf muss einen zweiten Pumpenplatz nur vorsehen (Parameter `pumpen = 1`, Wert 2 baut ein zweites Pumpenmodell, ohne Netz-Aenderung).
- Rueckschlagventil d40 kommt aus W39 (Teil 6); wenn W39 noch nicht gelaufen ist, Platzhalter-Klebemuffe d40 setzen und im Blatt vermerken.

## Aktualitaetspruefung (05.11.2026, Werkstatt, Regel W44)
Ergebnis: **angepasst** (Plan gilt als freigegeben, D81). Gelesen: `data/roadmap.json` (W37, E19, E20, L01, L04, M-BEET-TAUSCH), `docs/decisions.md` D81, `docs/jobs/pruefung/M-BEET-TAUSCH.md`, `data/leitungsnetz.json` Version 3, `data/components/ibc_beet.json` Ports, Beet-Matrizen in `scripts/dome-script.json`.
1. **E20 = A+ (D81, Annahme):** W37-1 war bis E20 gestoppt; jetzt frei. A+ fuegt am Sumpf nur den Ablaufwaechter hinzu (R47 Abschnitt 4.1 Befund 3 und 6.6 Folge 2): Schwimmer im Beet, 12 V, auf den Sumpf-Alarm. Am Bauteil: eine zweite Kabeldurchfuehrung im Deckel (Port), kein weiterer Koerper.
2. **E19 = zweite Pumpe ja (D81, Annahme):** Parameter `pumpen` steht auf **2** (nicht 1); beide Pumpen mit eigenem Steigrohr und Rueckschlagventil d40, zusammengefuehrt unter dem Deckel, **ein** Port K58/K59 (keine Netz-Aenderung). Leistung: 60 W Betrieb, die zweite Pumpe 0 W im Normalbetrieb (Reserve, schaltet bei Ausfall) [A].
3. **E12 Schlammfass je Linie (D81):** unveraendert baubar. M10-S2V (Subtank) beruehrt das Schlammfass, bleibt aber GEPARKT; kein Einfluss auf dieses Bauteil.
4. **W39 gelaufen:** `lt_rueckschlagventil_d40` existiert (`designs/components/`), also kein Platzhalter; Masse aus `leitung_w39.rsv_geom(40)`.
5. **Netz Version 3, K14/K30 DN 50 (nicht d63):** Die Kanten tragen `dn: 50` (Sammelleitung d50, Einzelabgang d40). Zulauf-Port daher **Muffe d50**, Parameter `zulauf_d` (auf 63 umstellbar). Pruefpunkt 3 gilt mit d50.
6. **Beete getauscht (M-BEET-TAUSCH, D79): Einlaufhoehe neu geplant.** Der Ablaufport wanderte nur in x/y (aussen_800 x 1096 -> 1040, innen_933 y 0 -> 65), z lokal bleibt -30. Gemessen aus den Beet-Matrizen (`dome-script.json`, Flur = Modell-Z 400): Wannenunterseite flur-relativ aussen -162, innen -209 bis -170; Ablaufport -192 bzw. -239 bis -200; Achse Einzelabgang nach Reduktion und Bogen etwa -260 / -290 (K14 `hoehe`). **Folge:** Mit Deckel buendig (Tankoberkante Flur 0) laege die Einlauf-Rohrsohle bei 800 mm ueber Boden auf **-200, also UEBER dem Beetablauf (-290)**: so fliesst nichts. Neu: Einlaufsohle flur-relativ hoechstens -290 - 25 (halbes d50) - 60 (1 % auf 6 m Sammler [A]) = **-375; gewaehlt -400**. Bei 800 mm Sohle ueber Tankboden: **Tankboden -1200, Tankoberkante -200, Schachtaufsatz 200 mm bis Flur, Grube Tiefe 1,25 m** (1,20 + 0,05 Sandbett). Die Pegel bleiben (AUS 120, EIN 320, ALARM 620 ueber Boden). Parameter `aufsatz_h` = 200 im Bauteil.
7. **Besonderheit Foerderhoehe:** Mit Tankboden -1200 steigt die statische Foerderhoehe vom Sumpfpegel (AUS -1080, EIN -880) bis zum Ruecklauf ueber Z 515 auf **1,40 bis 1,60 m** (R45 rechnete 1,0 bis 1,5 m). Arbeitspunkt der Pumpe (Hmax 2,8 m) sinkt; Nachrechnung mit `r45_sumpf.py` ist Sache des Planers/Orchestrators (Skript hier nicht anfassen).

## Eingaben (nur diese)
- `docs/research/R45-hydraulik-auslegung.md`: Abschnitt 0 (Zeilen 9 bis 70) und Abschnitt 3 (Zeilen 169 bis 224).
- `data/leitungsnetz.json` Version 3 per Python: Knoten `beet_sumpf_1`, `schlammfass_1`; Kanten K07, K14, K58 (und die Gegenstuecke K23, K30, K59); `scripts/r45_sumpf.py` nur ansehen (Pegelrechnung), nicht aendern.
- Bibliothek: `docs/parts/leitungsteile.md` Konvention (Zeilen 7 bis 30), `scripts/workshop/leitung.py` (`kugelhahn`, `bogen`, `rohr`, `save`), Muster fuer Bauteil, Check und Blatt: `scripts/workshop/puffer_klein.py` mit `check_puffer_klein.py` und `docs/parts/puffer_klein.md`, Blatt-Erzeuger `scripts/workshop/partsheet.py`, `docs/provenance.md` (beim Schreiben des Blatts).

## Teile
Gemeinsame Bauweise: eingegrabener PE-Rundtank mit Deckel, Stutzen, Einbauten; beide Bauteile in je eigener Datei, eigenem Generator (`scripts/workshop/beet_sumpf.py`, `schlammfass.py`) und eigenem Check, aber ein Commit-Rhythmus. Bauteil-KS: Ursprung Mitte Tankboden, Z hoch (wie `becken_dritt_klein`); Ports im Bibliotheksformat (Lage = Mitte der Oeffnungsebene, Richtung nach aussen).

### Teil 1 `beet_sumpf` (zwei Instanzen, je Linie)
Mini-Plan zuerst im Blatt. Masse aus R45 Abschnitt 3 (Quelle und Belegstand je Zeile im Blatt vermerken):
| Merkmal | Wert | Beleg |
|---|---|---|
| Tank | PE rund Aussen Ø 0,8 m, H 1,0 m, ca. 500 l; Grube Ø 1,0 m, Tiefe 1,0 m, Deckel buendig oder +50 | gerechnet (`r45_sumpf.py`), Handelsmass Tank [A] |
| Pegel ueber Tankboden | AUS 120, EIN 320, ALARM 620 mm; Einlauf-Rohrsohle 800 mm, hoechster Wasserstand darunter | gerechnet (R45) |
| Zulauf K14/K30 | Port Muffe d63 (Sektorsammler M10 S4) bei Z 800 ueber Boden, Gefaelle >= 1 % | Annahme [A] |
| Foerderleitung K58/K59 | Port Muffe d40 oben aus dem Deckel; innen Steigrohr d40 mit **Rueckschlagventil d40** (W39) und Anschluss an die Pumpe | gerechnet (v 0,94 m/s) |
| Pumpe | Teichpumpe 5300 l/h, 60 W, Hmax 2,8 m als **Handelsteil-Koerper** (Abmessungen aus dem Bibliotheks-/Pumpenblatt `docs/parts/pumpe.md` nur als Platzhalter-Quader, Fabrikat und Kennlinie offen, OASE AquaMax Eco 5500 nur als Beispiel genannt) | Annahme [A] fuer Mass, [Q] fuer Daten |
| Schwimmer | 3 Schwimmerschalter an einer Stange (AUS, EIN, ALARM), Kabeldurchfuehrung | R45 |
| Deckel | dicht, lichtdicht, begehbar (Last-Platzhalter), Entlueftung d32 mit Insektengitter, Kabel- und Leitungsdurchfuehrung | R45, Handelsmass [A] |
Stueckliste aus Handelsteilen (L21): Rundtank PE mit Deckel, Pumpe, Rueckschlagventil d40, 3 Schwimmerschalter, Stange, Entlueftung d32, Durchfuehrungen. Leistung 60 W je Pumpe geht als Zeile ins Blatt; `scripts/system_specs.py` pflegt der Orchestrator, nicht die Werkstatt.

### Teil 2 `schlammfass` (zwei Instanzen, je Linie)
Masse aus R45 Abschnitt 0: Spannringfass PE 200 bis 220 l, Ø 0,58 bis 0,60 m, H 0,88 bis 0,92 m [A, Handelsmass]; Grube Ø 0,8 m, Tiefe 0,95 m, Fassoberkante etwa Z 0 bis +20, Hahn der Absetzer-Kegelspitze Z etwa +150. Deckel mit Stutzen d40 in der Mitte (Port Muffe d40, Richtung +Z), Bohrung Ø8 fuer Luftschlauch, Entlueftung Ø20, kein Auslass. Fassung 105 l/Woche plus Reserve. Grube selbst baut die Montage (Ausschnitt), das Bauteil liefert die Gruben-Parameter `grube_d`, `grube_t` als Zahlen im Blatt.
Dazu `lt_kugelhahn_feder_d40`: Kugelhahn d40 aus der Bibliothek mit **Federrueckzug oder Totmann-Hebel** (Variante von `leitung.kugelhahn(40)`; offen = nur bei Handkraft, Feder schliesst); Fabrikat und Verfuegbarkeit im Standardmass **nicht geprueft** [A] (R45 Offene Punkte Frage 0 Nr. 3). Schutz gegen leeren Pool (Pumpe 12,5 l/min, ein offener d40-Hahn leert den Absetzer in 2 min). Gehoert in die Bibliotheksdatei-Gruppe `leitung_w37.py` mit eigenem Ports-Eintrag; 'lt_' Name, damit die Montage ihn wie die uebrigen Haehne findet.

### Gemeinsame Ergebnisse je Teil
Bauteil `designs/components/<name>.sc`, Check (Masse, Volumen gegen Rechnung, Ports, Interferenz 0, Pegelhoehen), Bauteilblatt per `partsheet.py` aus `data/components/<name>.json`, `data/descriptions.json` (neue Gruppen vor `^puffer` einsortieren; Namen duerfen nicht von bestehenden Mustern wie `^tank` oder `^lt_` eingefangen werden), Bild per `scripts/archive_render.py --role werkstatt`, Zeile in `docs/workshop-state.md`. Je Teil ein Commit, dazwischen push.

## Nicht anfassen
`designs/dome.sc`, `scripts/gen_dome.py` (die Gruben und die Sumpf-Lage setzt die Montage in S4/S5), `scripts/leitungen.py`, `data/leitungsnetz.json`, `data/roadmap.json`, `scripts/system_specs.py` (Orchestrator), `scripts/r45_*.py`, die fremden Dateien aus `docs/workshop-state.md`. Nichts zu Aktivkohle, Luft, Stutzen oder Schaltschrank (W37-2, W37-3).

## Ergebnis
`designs/components/beet_sumpf.sc`, `schlammfass.sc`, `lt_kugelhahn_feder_d40.sc` samt Generatoren, Checks, Blaettern, JSON, descriptions, Bildern. Kurzmeldung: je Teil eine Zeile (Masse, Ports, offene Fragen), Hinweis "System-Specs: 2 x 60 W, 108 bis 120 W" an den Orchestrator, "Besonderheit: ..." falls etwas auffaellt.

## Pruefpunkte (fuer den Pruefer)
1. Check beider Bauteile PASS (Aufruf steht im Blatt-Abschnitt "Pruefung"; Soll: keine FAIL-Zeile).
2. Sumpf-Volumen aus dem Modell: Innenraum Ø 0,8 x Pegel 620 mm ergibt 310 l +/- 5 % (R45: ALARM bei 620 mm = 310 l, Rechnung nimmt Ø 0,8 ohne Wandabzug); Tankinhalt bis 1,0 m etwa 500 l +/- 7 %.
3. Port-Tabelle enthaelt Zulauf d63 bei Z 800, Foerderleitung d40, Kabeldurchfuehrung; DN und Richtung wie Blatt, Netz-Kanten K14/K58 (und K30/K59) im Blatt genannt.
4. Schlammfass: Volumen 200 bis 220 l +/- 5 % aus Ø und H; Stutzen d40 Mitte Deckel; Gruben-Parameter Ø 0,8 / Tiefe 0,95 im Blatt.
5. Herkunftstabelle in beiden Blaettern trennt belegt, gerechnet und Annahme je Mass; keine Fabrikat-Erfindung (`grep -ci oase docs/parts/beet_sumpf.md` darf nur das Beispiel mit dem Vermerk "Beispiel" treffen).

## Start-Hinweis fuer die Bau-Sitzung
1. Reihenfolge: W39 laeuft vor dieser Sitzung (Rueckschlagventil d40); fehlt es, Platzhalter und Vermerk.
2. Pumpe und Schwimmer sind Platzhalter-Koerper mit Ports/Kabel, kein Fabrikat; Datenblatt der echten Pumpe ist OFFEN (R45 Frage 3 Nr. 1).
3. Bauzeit der PE-Tanks klein (2 bis 10 s je Komponente); Boolean-Vereinigung duenner Mantel scheitert: Deckel, Stutzen, Einbauten als eigene Koerper mit 1 mm Ueberlappung.
4. Schlammfass und Sumpf nicht in `gen_dome.py` registrieren; Standort bleibt Sache der Montage (S4/S5).
5. Limit: zwei Teile-Pakete, mehr nicht; bei Kontext ueber 60 Prozent nach dem letzten Commit Stand in `docs/workshop-state.md` und stoppen.
