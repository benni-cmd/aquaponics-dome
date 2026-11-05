# Bauteilblatt Wasserautobahn (N-AUTOBAHN-V2): Tragwerk (WA-T) und Schlauch (WA-S)

Auftrag: `docs/jobs/N-AUTOBAHN-V2.md` Abschnitt 3. Je Werkstatt-Sitzung ein Abschnitt zwischen eigenen Marken; jede Sitzung aendert nur ihren Abschnitt.

<!-- WA-T Anfang -->
## WA-T Tragwerk

Auftrag: `docs/jobs/N-AUTOBAHN-V2.md` Abschnitt 3, Teile WA1 bis WA4 und WA7. Generator `scripts/workshop/autobahn_t.py`, Pruefung `scripts/workshop/check_autobahn_t.py`, Teiledaten `data/components/autobahn_teile.json` (Schluessel `tragwerk`, mit Lage je Ringecke unter `lagen`), Bilder `renders/components/autobahn/<teil>.png`. [Q] Quelle · [E] eigene Rechnung/Messung · [A] Annahme. Z relativ zum Innenboden (absolut = +400).

**Mini-Plan.** Problem: Der Ring hat keine Stuetzpunkte, Ausleger, Traeger und Ecken; fuer das Podest fehlt die Pruefung gegen das Gefaelle von K10. Intent: Montage R1/R2 setzt das Tragwerk nur noch ein und erfindet keine Teile. Goal: Je Teil eine `.sc` mit Ports, Interferenz 0 gegen echte Nachbarn, Statik und K10-Gefaelle im Check gemessen.

### Befunde, die das Planer-Blatt aendern

1. **Ring liegt bei Apothem 3377, nicht bei 3277.** Seit D63 stehen die Mitteltische 100 mm weiter aussen (`ring_shift_mid`, `scripts/dome-script.json`). Daraus folgen: Eckradius 3551, Seite 2194,5 mm, Umfang 21,95 m (Blatt: 3446 / 2130 / 21,30 m). Die Ausleger-Ziele steigen auf 1591 mm innen und 1784 mm aussen ab dem Ring.
2. **Ring haengt unter der Schiene, er liegt nicht auf ihr.** Laege der Ring auf einer Schiene 41, laege deren Unterkante bei etwa Z 2060, also unter Z 2100 im Gang. Die Hoehenkette ist deshalb fuer alle Stuetzpunkte gleich: Ringachse 2145, tiefster Schellenpunkt 2101,5, Schiene 2212 bis 2253 (Schlitz unten), Ausgleichsplatte bzw. Verbinder 2253 bis 2257, Querriegel, Kragarm und Ausleger 2257 bis 2297. Korridor KR bis 2300 wird eingehalten.
3. **Ringecke = PE-100 kalt gebogen, R 1875 (25 x d).** Ein PVC-U-Klebebogen d75 mit 36, 30, 22,5 oder 18 Grad wurde nicht gefunden: Profec fuehrt 30 und 22,5 Grad erst ab d90, Praher und FIP nur 45 und 90 Grad (Abschnitt Quellen). Der Bogen braucht je Ecke 609 mm Gerade beidseits (Tangente), sein Scheitel liegt 96,5 mm innerhalb der Polygonecke. **Folgen:** (a) An einer Ecke kann kein Abzweig sitzen; die Abzweige liegen auf der Geraden, mindestens 609 mm von der Ecke entfernt. Zwischen zwei Boegen bleiben 976 mm. (b) PE laesst sich nicht kleben. T97 `ring_abzweig_*` und T96 `entluefter_d75` aus PVC-U brauchen deshalb PP-Klemmverbinder: T-Stueck d75 mit Innengewinde 2 1/2 Zoll, Trinkwasser-Zulassung W270/KTW (+GF+ iJOINT, Code 158 400 197) oder Plassim (T 75 x 2 1/2 x 75). Die Wahl trifft die Montage R1b, kein WA-T-Teil.
4. **Podest auf Z 820, nicht auf 950.** Bei 950 passt K10 nicht in den Fassdeckel: Achse 1570 minus Bogen 90 d50 (91) minus Rohrstueck (72) minus Zulauf-Port (575) ergibt 832; mit 1 % Gefaelle auf 1,2 m bleiben 820. Pegel EIN liegt dann bei Z 1160 statt 1290, die Booster heben 130 mm mehr. [E, auf das Planer-Modell Abschn. 5 umgerechnet: 4 Booster 206 statt 187 W bei eta 25 %, gesamt etwa 636 statt 617 W]
5. **Podest-Lage am heutigen A+-Verteiler geht nicht.** Am Ende von K10 laege das Fass mit seinen Stutzen 500 mm in Gang A, am Ende von K26 482 mm in Gang B (Check, BEFUND-Zeile). Die Montage R1c muss K10 und K26 seitlich am Biofilter vorbeifuehren (bis 1,2 m bei 1 %) und dort einen Platz ausserhalb der Gaenge finden. Das Podest selbst ist dafuer bemessen.

### Stuetzpunkte im Ring (aus `lagen`, Montage uebernimmt)

| Ecke (Azimut) | Stuetzpunkt | Teil | Ausleger innen / aussen |
|---|---|---|---|
| 18,3 | Joch an `Tisch_mitte:4` Bock 1 (-X), 591 mm hinter der Ecke | `portal_joch_mitte_a` | 1020 / 1210 |
| 54,3 · 90,3 · 126,3 · 162,3 · -161,7 · -125,7 | Joch an Bock 2 (+X) von `Tisch_mitte:4/5/6/1/2/3`, 501 mm vor der Ecke | `portal_joch_mitte_b` | 1020 / 1210 |
| -89,7 · -53,7 | Stelze, Pfosten innen (r 3108) auf der Winkelhalbierenden, Kragarm nach aussen | `ringstuetze_d75_b` | 1020 am Gegenarm / – |
| -17,7 | Stelze, Pfosten aussen (r 3801), Kragarm zur Mitte | `ringstuetze_d75_b` | 1370 am Kragarm / 1370 am Gegenarm |

Joch-KS = Tisch-KS: Die Montage setzt das Joch mit der Instanzmatrix des Tisches (`matrix_tisch`). Summe: 7 Joche, 3 Stelzen, 18 Ausleger (10 innen, 8 aussen), 10 Schienen, 10 Verbinder, 30 Schellen (20 auf der Schiene an den Tangentenpunkten, 7 an den Verbinder-Laschen, 3 an den Stelzen-Kragarmen), 10 Ring-Ecken.

### WA1 Portal-Joch `portal_joch_mitte_a` / `_b`

Zwei Verlaengerungen 40 x 40 x 3 stehen aussen neben den Bestandsbeinen eines Bocks, 2 mm vor den Diagonalen-Schrauben M6 (Bock 1 bis x -484, Bock 2 bis x 574), mit Distanzblech 8 mm. Je Bein halten zwei Klemmen (Platten 6 mm, 2 x M8, Z 250 bis 310 und 780 bis 840). Oben liegt ein Querriegel 40 x 40 x 3 auf Z 2257 bis 2297 mit Stirnplatten 100 x 40 x 8 fuer die Ausleger. Am Tisch wird nicht geschweisst. Masse 22,3 kg.

| Port (Tisch-KS) | A: Lage | B: Lage | Richtung |
|---|---|---|---|
| Schiene (Auflage Oberkante Schiene) | -506, 0, 2253 | 596, 0, 2253 | -Z |
| Ausleger innen (Stirnplatte) | -506, 575, 2277 | 596, 575, 2277 | +Y |
| Ausleger aussen (Stirnplatte) | -506, -575, 2277 | 596, -575, 2277 | -Y |

### WA2 Ausleger `ausleger_schlauch_1020` / `_1210` / `_1370`

Kragarm 40 x 40 x 3 mit Flansch 100 x 40 x 8 (2 x M10). Halterpaare beidseits im Raster unter 400 mm: Clips fuer Schlauch bis AD 35, Schlauchachse y +-42,5 auf Armmitte. Am Ende sitzt ein Endbuegel mit Viertel-Sattel R 192,5 unter dem Schlauch, das ergibt einen Biegeradius von 210 = 6 x AD (Leitungsordnung R14). **Kein Kopfband:** Unter dem Arm wuerde es in den Gang unter Z 2100 ragen; der Arm traegt ohne Kopfband (Check). Masse 5,6 / 6,3 / 6,9 kg.
Ports (KS: Flanschanlage x 0, Arm +X, Armmitte z 0 = Z 2277): Flansch (0, 0, 0) -X; Halter k l/r (x_k, +-42,5, 0) +X; Fall l/r (L + 210, +-42,5, -210) -Z.

### WA2b Ringstuetze Rev. B `ringstuetze_d75_b` (T95-B)

Fuss, Pfosten 50 x 50 x 3 und Hoehen wie T95. Es gibt keinen Haenger: Der Schienenverbinder liegt unter dem Kragarm bei x 250, die Scheitel-Schelle haengt mit M8 durch den Kragarm bei x 346,5. Der Gegenarm (-X) und beide Armenden tragen Stirnplatten fuer Ausleger. T95 Rev. A bleibt unveraendert. Masse 15,5 kg.
Ports: Schienenecke (250, 0, 2257) -Z; Scheitel-Schelle (346,5, 0, 2297) +Z; Ausleger +X (414,5, 0, 2277); Ausleger -X (-68, 0, 2277); Fuss (0, 0, 0) -Z.

### WA3 Montageschiene, Schellen, Verbinder

1. `montageschiene_41_2179`: C-Profil 41 x 41 x 2,5, Schlitz 22 unten, Laenge 2179 (Seite minus Gehrungsluft), 2,59 kg/m im Modell. Statik mit Datenblattwerten Iy 5,81 cm4 / Wy 2,84 cm3 [Q MUEPRO MPR 41/41/2,5; fischer FUS 41/2,5: 6,0 / 2,85]. Das Modell ergibt 7,17 cm4, weil Lochung und Radien fehlen.
2. `lt_klemme_d75` (Schiene, Mutter im Schlitz), `lt_klemme_d75_ecke` (Mutter auf der Verbinder-Lasche) und `lt_klemme_d75_stelze` (Mutter auf dem Kragarm): Schelle d75 mit EPDM 3 mm. Tiefster Punkt 2101,5. Ports: Rohrachse (0, 0, 0) entlang X; Mutterauflage z 69,5 / 112 / 152 ueber der Achse.
3. `schienenverbinder_36`: Flachstahl 4 mm auf dem Ruecken beider Schienen, je Schenkel 2 Loecher M8. Eine Lasche auf der Winkelhalbierenden (108 Grad) traegt das Loch ueber dem Bogenscheitel (96,5 mm). Masse 0,52 kg.

### WA4 Ring-Ecke `ring_ecke_d75`

PE-100 d75 SDR 17 (Wand 4,41), kalt gebogen um 36 Grad mit R 1875, Schenkel je 150, Achslaenge 1478. Ports: A (0, 0, 0) -Z; B (446,3, 0, 1373,5), Richtung (0,588, 0, 0,809). Lebensmittelecht nach D85: PE-100-Trinkwasserrohr; die Zulassung des gewaehlten Fabrikats pruefen N-STUECKLISTE und Beschaffung.

### WA7 Pegelschacht-Podest `pegelschacht_podest`

Stahlgestell 480 x 480 aus 40 x 40 x 3 mit Rahmen oben und auf Z 400, Deckplatte 6 mm bis Z 820 (Fassboden), Haltering 60 hoch gegen Verrutschen, 4 Fussplatten 100 x 100 x 6 mit je einem Anker M8. Masse 37,0 kg. Ports: Fass (0, 0, 820) +Z, dort steht der Ursprung des T94; Fuss (0, 0, 0).

### Pruefung (`python -X utf8 scripts/workshop/check_autobahn_t.py`, Stand dieses Blatts)

**104/104 PASS**, Exit 0. Gemessen werden je Teil: Koerperliste, Ports als Stirnflaechen, Interferenz 0 (Joch gegen die echte Geometrie von nft_tisch_mitte samt Innenbeet, Ring, Schiene und Ausleger; Podest mit T94 darauf; Klemmen mit Testrohr). Dazu Hoehen (Schellen >= 2100, Oberkante <= 2300, kein Joch-Teil ausserhalb des Portalrands unter 2100) und die Statik. Kennwerte: Joch-Kopfverschiebung radial 0,73 mm und tangential 1,11 mm (Grenze 4,7). Ausleger mit Durchbiegung und Flanschschrauben; Saettel liegen in allen 5 Aufstellungen ausserhalb von Gang A und B. Stelze in 4 Lastfaellen unter L/300. Schiene: groesste Spannweite 2786 mm mit 6,06 mm Durchbiegung (Grenze 13,9), Schellenabstand hoechstens 976 mm. Ring-Ecke R 1875 = 25 x d. K10-Gefaelle 1,0 % auf 1,2 m. Podest kippt ohne Anker nicht. Die Lage am Verteilerplatz ist als BEFUND ausgegeben und wird nicht gezaehlt.

### Quellen (Recherche-Agent 05.11.2026, Texte aus den PDFs gelesen)

| Frage | Ergebnis | Quellen |
|---|---|---|
| Kalt-Biegeradius PE d75 | 25 x d fuer SDR 17 (strengster Wert); 20 x d bei 20 Grad C | PE100+ Association (pe100plus.com, Technical guidance, Trenching); Firat (firat.com, Bending diameter); Ostendorf Sicherheitsblatt PE 80 (media.hornbach.ch). Kein deutscher Herstellerwert fuer PE 100 gefunden |
| PVC-U-Bogen d75 unter 45 Grad | nicht gefunden | Profec ueber Bevo und Bosta (30 und 22,5 Grad erst ab d90), Praher und FIP (nur 45 und 90 Grad, nur Auszuege) |
| PP-Klemmverbinder d75 | vorhanden, T-Stueck mit Innengewinde und Kupplung | +GF+ iJOINT (W270, KTW, DVGW); Plassim (Rohstoff-Zulassung); Unidelta (DVGW, KIWA) |
| Schiene 41 x 41 x 2,5 | Iy 5,81 / 6,0 cm4, 2,45 bis 2,53 kg/m | MUEPRO Datenblatt 33665; fischer FUS 41/2,5 (Meesenburg) |

### Offen (WA-T)

1. **Montage R1c:** Platz fuer Podest und Pegelschacht ausserhalb von Gang A und B finden; K10/K26 duerfen dafuer bis 1,2 m lang werden.
2. **Montage R1b:** Abzweige und Entluefter auf die Ring-Geraden legen, mindestens 609 mm von jeder Ecke; als Uebergang PE zu PVC-U das PP-Klemm-T 75 x 2 1/2 Zoll (+GF+ iJOINT) oder einen Uebergangsadapter waehlen.
3. **Montage R1a:** Die Stelzen -89,7 und -53,7 (Pfosten r 3108) und -17,7 (r 3801) gegen Tanks und Pumpen pruefen; der Standort darf 300 mm entlang der Winkelhalbierenden wandern.
4. **N-STATIK:** Joch-Klemmen per Reibschluss pruefen (Vorspannung M8 mit 5 kN angesetzt [A]) und die Anker der Stelzen.
5. **Planer/Orchestrator:** Ringmasse im Auftragsblatt (Abschn. 1.2 und 2.2) und die Pumpenleistung (636 statt 617 W) nachziehen.
<!-- WA-T Ende -->

<!-- WA-S Anfang -->
## WA-S Schlauch: Fallleitungen, Schnellkupplung, Rueckschlagventil d50, Ruecklauf

Generator `scripts/workshop/autobahn_s.py`, Pruefung `scripts/workshop/check_autobahn_s.py`, Teiledaten `data/components/autobahn_teile.json` Schluessel `wa_s` (aus `autobahn_s.py --json`), Bilder `renders/components/autobahn/<datei>.png`. [Q] Quelle (Liste unten), [E] eigene Rechnung oder Messung, [A] Annahme.

**Problem:** Fallleitungen, Kupplungen, Rueckschlagventil d50 und Schlauch-Ruecklauf gab es nicht als Bauteile. **Intent:** Die Montage R2 setzt nur fertige Teile und erzeugt Schlauchwege mit derselben Funktion. **Goal:** Die Pruefpunkte WA5, WA6, WA8 und WA9 aus dem Blatt sind im Check gemessen.

### Befunde fuer Planer, Montage und Beschaffung
1. **Tische mit ID19 statt ID16.** Einen lichtdichten Schlauch mit Trinkwasser-Nachweis gibt es in ID16 nicht; der Markt fuehrt 12,8 / 19 / 25 mm [Q1, Q2]. Die Fallleitungen der Tische nutzen deshalb REHAU RAUAQUA T-Flex ID19 (AD 26,6). Die Schlauchmenge ID16 aus der Rechnung (60,8 m) gilt fuer ID19.
2. **Ausleger auf Z 2277.** WA-T legt die Ausleger auf Armmitte Z 2277 rel, denn der Ring haengt unter der Montageschiene. Der Schlauch steigt deshalb nach dem waagerechten Abzweig (Z 2145) unter 45 Grad um 132 mm an. Je Ausleger-Abnehmer kommen 187 mm Weg hinzu; der Check vergleicht gegen Rechnung plus diesen Mehrweg.
3. **Rechnung zaehlte Formstuecke als Schlauch.** Vom Weg Ring-Achse bis Abnehmer sind 350 bis 362 mm Abzweig-Kette und etwa 250 mm Regelhahn, Kupplung und Endstueck. Die Schlauch-Zuschnitte im Check sind deshalb je Abnehmer 0,39 bis 0,60 m kuerzer als die Rechnung. Summe gemessen: ID19 50,3 m statt 60,8 m, ID25 31,6 m statt 38,6 m (Zuschnitte aus dem Check x Stueckzahl 6/10/8 bzw. 6/8).
4. **Bodenrinne liegt unter dem Pool-Spiegel.** Ein Schlauch, der einen Gang in der Bodenrinne quert, liegt am Rinnenende bei Z -98 rel (Check, Schlauchsohle), also unter dem Pool-Spiegel Z 515. Er kann nicht mehr frei fallend auf den Halbring K16/K32 an der Poolkrone (Z 650 bis 730) laufen, wie Blatt 2.5 Punkt 1 annimmt. Moeglich ist nur eine Einmuendung unter Wasser durch die Poolwand (Leitungsordnung R13, Feld `grund` = `pool_einmuendung`). Das ist eine Planer-Frage, keine Teil-Frage.
5. **Handels-Bodenrinne zu flach.** ACO Self Hexaline 2.0 NW100 ist 82 mm hoch [Q21, Q23], Euroline 2.0 97 bis 100 mm [Q21, Q22]. Ein Schlauch d50 (AD 64) mit 1 % Gefaelle ueber 1,2 m und Rost braucht mindestens 98 mm lichte Tiefe (Rost 20 + Luft 2 + AD 64 + Gefaelle 12) [E]. Das Modell nutzt 150 mm [A]; ein passendes Handelsteil ist offen.

### WA5 Schlauch-Fallleitung `schlauch_fall_<typ>` (5 Typen)
Kette je Abnehmer: Tuelle oben (Klebezapfen d32/d40 in Muffe B des Abzweig-Hahns T97) -> Schlauch -> Regelhahn auf Greifhoehe -> Zwischenschlauch -> Schnellkupplung -> Schlauch -> Endstueck am Abnehmer (Tisch: Muffe d25 auf das Zulaufverteilerrohr T22; Beet: Klemmverbinder PE d20 auf das Tropfrohr T30).

**KS:** Ursprung = Abgang des Ring-Abzweigs (Stirnflaeche Muffe B), +X radial zum Abnehmer, Z hoch, Endstueck waagerecht entlang +Y (die Montage dreht um Z auf die Port-Richtung des Abnehmers).

| Typ | Abnehmer | Abzweig | Weg waagerecht ab Ringachse | Ziel Z rel | Regelhahn Z rel | Biegeradius | Weg Soll (Rechnung + Anstieg) |
|---|---|---|---|---|---|---|---|
| `id19_mitte` | Mitteltisch (6) | d32 nach unten | 0 | 1090 | 1500 | 160 | 1355 |
| `id19_innen` | Innentisch (10) | d32 waagerecht | 1486 | 1090 | 1500 | 160 | 2841 + 187 = 3027 |
| `id19_aussen` | Aussentisch (8) | d32 waagerecht | 1679 | 1090 | 1500 | 160 | 3034 + 187 = 3221 |
| `id25_mitte` | Innenbeet unter Mitteltisch (6) | d40 nach unten | 0 | 650 | 1150 | 210 | 1795 |
| `id25_aussen` | Aussenbeet (8) | d40 waagerecht | 1679 | 650 | 1150 | 210 | 3474 + 187 = 3661 |

1. **Schlauchfuehrung:** Mittelzone faellt senkrecht unter der Ringecke (dort kein Gang). Innen und aussen: Abzweig um die Ringachse 90 Grad gedreht, Abgang waagerecht radial; Anstieg 45 Grad auf Z 2277, waagerecht in den Clips des Auslegers `ausleger_schlauch_*` (WA-T, Raster <= 400, `schlauch_ad_max` 35), Bogen am Endbuegel, freier Fall zum Regelhahn.
2. **Schlaufe:** Das Endstueck unten ist waagerecht und so lang, dass 300 mm Reserve ueber dem kuerzesten Weg bleiben (Rechnung Abschnitt 3); die Bogenverkuerzung gegen die Polylinie ist darin ausgeglichen.
3. **Halter:** Auf dem Ausleger haelt WA-T (Clips). Der freie Fall ohne Halter bleibt unter 1,5 m (Blatt 2.6 Punkt 3); unten haelt das Endstueck am Abnehmer.
4. **Schnittstelle Ausleger (fuer die Montage):** Die Fallstrecke liegt radial `horiz` ab Ringachse; der Bogen beginnt bei `horiz` - R. WA-T setzt den Fall bei Flansch + `lg` + `biege_r`. Die Montage legt den Ausleger so, dass die Sattelmitte bei `horiz` - R liegt, oder verschiebt die Fallleitung um diesen Betrag; ein Teil muss sich dafuer nicht aendern.
5. **Schlauchschellen:** AD 26,6 passt in `lt_schlauchschelle_id25` (Spannbereich 20 bis 32), nicht in `_id16` (12 bis 22). Fuer ID25 (AD 34,6) fehlt eine Schelle mit Spannbereich bis etwa 40 (offen). Je Fallleitung 8 Schellen (4 Schlauchenden, je zwei).

**Schlauch-Baustein `hose_path(b, prefix, pts, R, ad, idd)`:** Polylinie mit Ausrundung R an jeder Ecke, Koerper je Gerade und Bogen, Bohrung idd; meldet einen Fehler, wenn eine Gerade fuer die Tangente nicht reicht (R14). `hose_R(idd)` gibt den Biegeradius nach R14 (>= 6 x AD und >= Herstellerwert). Die Montage nutzt ihn fuer Fall- und Ruecklauf-Schlaeuche (Leitungsordnung v2, Abschnitt Folgen: Schlauch-Baustein).

### WA6 Schnellkupplung `lt_schnellkupplung_id19` / `_id25`
Kamlok Typ C (Kupplung mit Schlauchtuelle) und Typ E (Stecker mit Schlauchtuelle) aus Edelstahl 1.4401, PN16 [Q10 bis Q13]. Masse ID25: Kupplung 94, Stecker 97,5 [Q12]; gekuppelt 155 [A, Ueberdeckung 36,5]. ID19 mit Faktor 0,85 aus ID25 [A]. Serienmaessig NBR-Dichtung; fuer D85 wird EPDM lebensmittelecht bestellt [A, Konformitaetserklaerung nicht gefunden].
**Ports:** A Tuelle Kupplung (0, 0, 0), -Z; B Tuelle Stecker (0, 0, 136 bzw. 155), +Z. Stueck: 24 (ID19) und 14 (ID25).

### WA8 Rueckschlagventil `lt_rueckschlagventil_d50`
GF Typ 562 PVC-U d50 mit Feder, Klebemuffen: Gehaeuse D 97, Baulaenge L 157, z 95 [Q15, Q16]. Typ 562 statt 561, weil er in jeder Lage dicht schliesst; Oeffnungsdruck etwa 0,05 bar [Q15], hinter dem Booster unerheblich. Zulassungen ACS, KIWA, FDA, DIBt [Q15]. Je Booster eines, 4 Stueck. Dateiname folgt der Bibliothek (`lt_rueckschlagventil_d<d>`), nicht `lt_rsv_d50` aus dem Blatt.
**Ports:** A Zulauf (0, 0, 0), -Z; B Abgang (0, 0, 157), +Z; Muffe DN40.

### WA9 Ruecklauf
1. **`lt_schlauch_d50`:** Semperit LM1S-EPDM NW50: ID 50, Wand 7, AD 64, Biegeradius 250, 2,10 kg/m [Q6, Q7]. Biegeradius nach R14: 6 x 64 = 384 -> 385. Meterware 53,2 m (Rechnung Abschnitt 4). Lichtdicht abgeleitet aus dem Gummiaufbau [A].
2. **`ruecklauf_rinne`:** Gitterrinne OBO GRM 55 100 VA4301 (Edelstahl), 100 x 55, Element 3000 [Q25, Q27]; Modell-Element 2000 mit zwei Konsolen 1450 auseinander. Zulaessig 0,2 kN/m bei 1,5 m Stuetzabstand [Q26]; der volle Schlauch wiegt etwa 0,04 kN/m [E]. Konsole: Klemmplatte am Tischbein 40 x 40 mit Langloch 60 (Gefaelle einstellbar bis 4,1 %) und Arm unter der Rinne. Der Schlauch liegt auf (Leitungsordnung R6 `aufliegend`).
3. **`bodenrinne_rost_ganga` / `_gangb`:** Rinne NW100, lichte Tiefe 150 [A, Befund 5], Gitterrost 20 buendig mit dem Innenboden; Laenge Gang + 2 x 300: Gang A 1200 (4 Stueck), Gang B 1100 (2 Stueck), zusammen 7,0 m wie Rechnung Abschnitt 4. Handelselement 1000 lang, je Querung zwei Elemente gekuerzt [A].

### Werkstoffe und Lebensmitteleignung (D85)
| Teil | Produkt | Werkstoff und Nachweis | Quellen |
|---|---|---|---|
| Schlauch ID19 (D85) | REHAU RAUAQUA T-Flex ID19, AD 26,6, 15 bar | lichtundurchlaessig, UV-bestaendig; KTW-BWGL, DVGW W270, EU 10/2011, 1935/2004 | https://industrial.rehau.com/downloads/2168520/prospekt-rauaqua-rauaqua-varioflex-plus-rauaqua-t-flex.pdf https://www.keller-kalmbach.de/p/E6466349/pdf |
| Schlauch ID25 (D85) | REHAU RAUAQUA T-Flex ID25, Wand 4,8, 10 bar | wie ID19 | https://industrial.rehau.com/downloads/2168520/prospekt-rauaqua-rauaqua-varioflex-plus-rauaqua-t-flex.pdf https://www.schlauch-profi.de/Trinkwasserschlauch-Rauaqua-T-Flex-KTW-A-DVGW-W270/1106019 |
| Schlauch d50 (D85) | Semperit LM1S-EPDM NW50 | EPDM-Lebensmittelschlauch; BfR, FDA, 1935/2004 | https://hoses.semperitgroup.com/de/produkte/industrieschlaeuche/lebensmittel/lm1s-epdm?type=9101 https://shop.reiff-tp.de/en/gi-bierschl-lm1s-epdm-m.-sp.-nw-50/10049412 |
| Schnellkupplung (D85) | Riegler Kamlok Typ C/E, 1.4401 | Edelstahl, kein Messing; Dichtung EPDM statt Serien-NBR [A] | https://www.riegler.de/de/en/kamlok-quick-connect-socket-c-type-1-4401-hose-i-d-25-108100.html https://ehorst.de/nl/Kupplungsmuffe-Typ-C-DN-25-Stutzen-27-mm-Kamlok-Edelstahl-1117590.html |
| Rueckschlagventil d50 (D85) | GF Typ 562 PVC-U d50 | PVC-U, EPDM; ACS, KIWA, FDA, DIBt (zwei Herstellerblaetter) | https://www.gfps.com/content/dam/gfps/com/datasheets/de/gfps-datasheet-561-562-check-valve-de.pdf https://siags-energy.de/out/media/datasheet_306567.pdf |
| Regelhahn (D85) | GF Kugelhahn Typ 546 Pro PVC-U d25 (L 110, D 58) mit Schlauchtuellen | WRAS, ACS, NSF, FDA laut Hersteller; nur eine Quelle, Haendlerlisten nennen keine Zulassung | https://www.gfps.com/content/dam/gfps/com/datasheets/de/gfps-datasheet-546-pro-ball-valve-de.pdf |
| Tuellen | Baenninger Druckschlauchtuelle PVC-U, KTW-BWGL, L 54 bis 80 | Tuellen-Durchmesser etwa gleich Rohr-d: d32 passt nicht auf ID19, d40 nicht auf ID25 -> Reduzier-Tuelle [A] | https://www.schwarte-shop.de/pvc-u-klebefitting-druckschlauchtuelle-32-mm?pdf=true |

Gitterrinne, Bodenrinne und Rost beruehren kein Wasser (der Schlauch liegt darin); D85 gilt dort nicht.

### Quellen
Q1 bis Q28 aus der Recherche WA-S (05.11.2026); die oben genutzten:
- Q1 REHAU Prospekt RAUAQUA / T-Flex 06.2025; Q2 schlauch-profi.de T-Flex; Q3 Keller & Kalmbach T-Flex ID19.
- Q6 Semperit LM1S-EPDM; Q7 Reiff TP LM1S-EPDM NW50.
- Q10 ehorst Kamlok Typ C DN25; Q11 Riegler Kamlok Typ C 1.4401 ID25; Q12 Riegler Katalogblatt P 5-87; Q13 ehorst Kamlok Typ E DN25.
- Q15 GF Datenblatt 561/562 (07/2026); Q16 GF Datenblatt 561 PVC-U; Q19 GF Datenblatt 546 Pro (04/2026); Q20 Schwarte-Shop Baenninger-Tuellen.
- Q21 ACO Produktinformation Self; Q22 baustoffshop ACO Euroline; Q23 bauschnell ACO Hexaline; Q25 OBO Datenblatt 6001072; Q26 OBO Broschuere Gitterrinnen 2018; Q27 OBO Datenblatt 6001442.

### Pruefung (05.11.2026)
`python -X utf8 scripts/workshop/check_autobahn_s.py`: 101/102 PASS, Ausgabe `renders/components/autobahn/check_autobahn_s.txt`. Einziger FAIL: Regelhahn hat nur eine Quelle fuer die Lebensmitteleignung (Offen 1).

### Offen (WA-S)
1. Regelhahn: zweite Quelle fuer die Trinkwasser-Zulassung des GF 546 Pro fehlt; ein Kugelhahn mit angeformten Tuellen und Nachweis wurde nicht gefunden.
2. Biegeradius T-Flex nennt REHAU nicht (Analogwert FITT Pure 90/110 [A]); im Modell gilt ohnehin 6 x AD.
3. Kamlok: gekuppelte Laenge und EPDM-Konformitaet beim Hersteller anfragen.
4. Schlauchschelle fuer AD 34,6 (ID25) fehlt in der Bibliothek.
5. Bodenrinne: Handelsteil mit >= 110 mm lichter Tiefe; Weiterfuehrung unter dem Pool-Spiegel (Befund 4) entscheidet der Planer.
<!-- WA-S Ende -->
