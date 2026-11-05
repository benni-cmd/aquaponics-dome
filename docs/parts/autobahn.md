# Bauteilblatt Wasserautobahn (N-AUTOBAHN-V2): Tragwerk (WA-T) und Schlauch (WA-S)

Auftrag: `docs/jobs/N-AUTOBAHN-V2.md` Abschnitt 3. Je Werkstatt-Sitzung ein Abschnitt zwischen eigenen Marken; jede Sitzung aendert nur ihren Abschnitt.

<!-- WA-T Anfang -->
## WA-T Tragwerk
(Abschnitt der Sitzung WA-T.)
<!-- WA-T Ende -->

<!-- WA-S Anfang -->
## WA-S Schlauch: Fallleitungen, Schnellkupplung, Rueckschlagventil d50, Ruecklauf

Generator `scripts/workshop/autobahn_s.py`, Pruefung `scripts/workshop/check_autobahn_s.py`, Teiledaten `data/components/autobahn_teile.json` Schluessel `wa_s` (aus `autobahn_s.py --json`), Bilder `renders/components/autobahn/<datei>.png`. [Q] Quelle (Liste unten), [E] eigene Rechnung oder Messung, [A] Annahme.

**Problem:** Fallleitungen, Kupplungen, Rueckschlagventil d50 und Schlauch-Ruecklauf gab es nicht als Bauteile. **Intent:** Die Montage R2 setzt nur fertige Teile und erzeugt Schlauchwege mit derselben Funktion. **Goal:** Die Pruefpunkte WA5, WA6, WA8 und WA9 aus dem Blatt sind im Check gemessen.

### Befunde fuer Planer, Montage und Beschaffung
1. **Tische mit ID19 statt ID16.** Einen lichtdichten Schlauch mit Trinkwasser-Nachweis gibt es in ID16 nicht; der Markt fuehrt 12,8 / 19 / 25 mm [Q1, Q2]. Die Fallleitungen der Tische nutzen deshalb REHAU RAUAQUA T-Flex ID19 (AD 26,6). Die Schlauchmenge ID16 aus der Rechnung (60,8 m) gilt fuer ID19.
2. **Ausleger auf Z 2277.** WA-T legt die Ausleger auf Armmitte Z 2277 rel, denn der Ring haengt unter der Montageschiene. Der Schlauch steigt deshalb nach dem waagerechten Abzweig (Z 2145) unter 45 Grad um 132 mm an. Je Ausleger-Abnehmer kommen 187 mm Weg hinzu; der Check vergleicht gegen Rechnung plus diesen Mehrweg.
3. **Rechnung zaehlte Formstuecke als Schlauch.** Vom Weg Ring-Achse bis Abnehmer sind 350 bis 362 mm Abzweig-Kette und etwa 250 mm Regelhahn, Kupplung und Endstueck. Die Schlauch-Zuschnitte im Check sind deshalb je Abnehmer etwa 0,6 m kuerzer als die Rechnung; der Check gibt sie als INFO aus.
4. **Bodenrinne liegt unter dem Pool-Spiegel.** Ein Schlauch, der einen Gang in der Bodenrinne quert, liegt danach bei etwa Z -110 rel, also unter dem Pool-Spiegel Z 515. Er kann nicht mehr frei fallend auf den Halbring K16/K32 an der Poolkrone (Z 650 bis 730) laufen, wie Blatt 2.5 Punkt 1 annimmt. Moeglich ist nur eine Einmuendung unter Wasser durch die Poolwand (Leitungsordnung R13, Feld `grund` = `pool_einmuendung`). Das ist eine Planer-Frage, keine Teil-Frage.
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

### Offen (WA-S)
1. Regelhahn: zweite Quelle fuer die Trinkwasser-Zulassung des GF 546 Pro fehlt; ein Kugelhahn mit angeformten Tuellen und Nachweis wurde nicht gefunden.
2. Biegeradius T-Flex nennt REHAU nicht (Analogwert FITT Pure 90/110 [A]); im Modell gilt ohnehin 6 x AD.
3. Kamlok: gekuppelte Laenge und EPDM-Konformitaet beim Hersteller anfragen.
4. Schlauchschelle fuer AD 34,6 (ID25) fehlt in der Bibliothek.
5. Bodenrinne: Handelsteil mit >= 110 mm lichter Tiefe; Weiterfuehrung unter dem Pool-Spiegel (Befund 4) entscheidet der Planer.
<!-- WA-S Ende -->
