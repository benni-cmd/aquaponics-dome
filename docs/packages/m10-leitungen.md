# Paket M10 Leitungen: Rohre, Schlaeuche, Kabel (PLAN, nichts gebaut)

Stand 01.11.2026, Rolle Montage. Auftragsblatt `docs/jobs/M10-leitungen.md` (Abschnitt "Aktualitaetspruefung 01.11.2026" geht vor). Eingaben: `data/leitungsnetz.json` Version 2 (55 Kanten, 7 Trunks), `docs/leitungsnetz-aenderungen.md`, `docs/parts/leitungsteile.md`, `docs/hydraulics.md`, `docs/loop-state.md`, `docs/parts/feinfilter.md`, `scripts/dome-script.json`, `data/messstellen.json`. Kein Edit an `gen_dome.py`, `designs/`, Komponenten, `params.json`.

## 1. Zieldefinition
- **Problem:** Im Modell Runde 60 fehlen alle Rohre, Schlaeuche und Kabel; die zwei Feinfilter (T55) stehen nicht im Modell, das Platz-Szenario (Reserve 132 mm) und D71 rechneten ohne sie.
- **Intent:** Ben will die Anlage komplett, logisch und kollisionsfrei verlegt sehen (D50), mit Gaengen >= 500 mm, damit Montage und Bedienung am Modell pruefbar werden.
- **Goal:** Alle Kanten K01 bis K57 und 7 Trunks im Modell, Rohrverlauf aus dem Graphen, Anschluss an die Ports, 0 Kollisionen, kein Gang schlechter als vorher, Gefaelle und Hoehenlagen nach Abschnitt 4.

## 2. BEFUND ZUERST: Standort der zwei Feinfilter (T55)
**Antwort: Ein Standort mit allseits >= 500 mm gibt es NICHT (weder Ost noch West). D71 geht damit zurueck an Ben.** Ich loese das nicht selbst. Gerechnet mit `scripts/place_feinfilter.py` (streng) und `scripts/place_feinfilter_zone.py` (gelockert), reine Geometrie, Knie-Scheibe 0,3 m ueber Flur, Raster 50 mm (Fehler etwa 25 bis 50 mm), Hindernisse wie `check_walkways_voll.py` plus Puffer-Bedienzone.

| Annahme / Rechnung | Ergebnis | Befehl |
|---|---|---|
| Filter-Grundriss 770 x 680 (Behaelter 630 x 440 plus Stutzen), Hoehe 903 | in der Grube Oberkante Z +407 ueber Flur, im Knie-Schnitt Hindernis | `docs/parts/feinfilter.md` Zeilen 1 bis 12, 100 bis 107 |
| Streng: Bedienseite und beide Stirnseiten >= 500, Rueckseite >= 150 | Ost 0, West 0 Kandidaten (8942 bzw. 15648 Lagen geprueft) | `python -X utf8 scripts/place_feinfilter.py` |
| Groesste Luecke West (770 x 680) | 325 mm bei x 775 y -2825 (Puffer-Zwickel), 175 mm zu wenig | dito |
| Groesste Luecke Ost bei den Pumpen | nur 181 mm; Ost sonst 295 mm, aber auf der Tuerachse (Tuergang) | dito |
| Nur Behaelter 630 x 440 (Stutzen in der Grube versenkt) | West 436 mm bei x -1775 y -3525, 425 mm bei x 775 y -2825; Ost 336 mm bei x 3825 y 725; nirgends 500 | `FFL=630 FFW=440 python -X utf8 scripts/place_feinfilter.py` |
| Gesamte Kuppel, 770 x 680, ab Luecke 300 mm | 1 Ort; ab 250 mm 4 Orte | dito (Zeilen "Gesamte Kuppel"); Luecke ab 250 mm: x 775 y -2825, x 1525 y -5075 (Tuer), x -1775 y -3525, x 525 y -5025 |

**Gelockerte Regel "Bedienzone"** (mein Vorschlag, nicht entschieden): vor der Front freier Streifen 630 x 500, Stirn- und Rueckseite je >= 150 (Rohranschluss, Spuelschlauch), nie in der Puffer-Bedienzone (700 x 650), danach bleiben alle 40 Bauteile ueber 500-mm-Gang erreichbar, ebenso Filter-Bediengasse und Puffer-Zone (`python -X utf8 scripts/place_feinfilter_zone.py`, 66 Ost- und 487 West-Lagen, 3 bis 5 getrennte Orte):

| Ort | Mitte x / y, Drehung | Az / r | Rohr Pool~ / Pumpe~ | Engste Nachbarn (Rand) | Gangzellen verloren >700 mm weg |
|---|---|---|---|---|---|
| **Ost A** (Linie 1) | 3925 / 825, 285 Grad | 12 / 4011 | 1913 / 714 | Pumpe_gross:2 115 (am Auslauf, ok), Beet 203 bis 249 | 0 |
| **West A** (Linie 2) | 875 / -2725, 255 Grad | -72 / 2862 | 452 / 1107 | Puffer 174, Tisch-Fuss 158, Pool 261 | 0 |
| **West B** (Linie 2) | -1575 / -3175, 285 Grad | -116 / 3544 | 1170 / 904 | Beet_innen:3 212, Tank_gross_t3 208 | 3 Zellen (0,01 m2) |

Wo West A und der zweite Ost-Treffer (975 / -2675) liegen, ist derselbe Zwickel: dort passt nur EIN Filter. Die Rohr-Masse sind Luftlinie Filter-Stirn bis Pool-Aussenrand (r 2095) bzw. bis Pumpe_gross (Auslauf-Seite), keine Trasse. Alle drei Orte haben Gaenge < 500 mm an Stirn- oder Rueckseite (siehe Spalte "Engste Nachbarn"); sie sind Nischen am Gangrand, kein neuer Gang entsteht.

**Optionen fuer Ben (Orchestrator ordnet, ich empfehle a):**
- a) Bedienzone-Regel akzeptieren: Ost A + West B (West A frisst die Puffer-Reserve 132 mm: 174 mm Abstand zum Puffer, Tisch-Fuss 158). Kosten: Rohr Ost A etwa 1,9 m Unterflur vom Pool.
- b) Grube mit begehbarem Deckel bis Oberkante Flur (Grube 903 statt 496 tief): Filter verschwindet aus dem Knie-Schnitt, Gaenge frei; verlangt Pumpen/Tafeln tiefer oder Pumpe vor dem Filter (Saugstutzen Z 120 muss unter dem Filterspiegel bleiben), Grubenabdichtung und Sumpf. Gewichtiger Eingriff in F1.
- c) Gaenge verbessern (Tank-Abstand, Puffer schieben): kein Rechenbeleg, braucht eine neue Platzsuche.
- d) D71 neu oeffnen (R44 Kandidat B: Sieb nur am NFT-Zweig, ein Sieb statt zwei).
- e) R44 Kandidat A: Absetzer weg (2 x Tank_klein samt 4 x Pumpe_klein samt Tafeln), siehe 2e.

### 2e Rechnung ohne Tank_klein x2 samt Pumpentafeln (R44 Kandidat A, Stand 01.11.)
Befehle: `FEXCL=Tank_klein,Pumpe_klein python -X utf8 scripts/place_feinfilter.py` (streng), `... scripts/place_feinfilter_zone.py` (Bedienzone), `... scripts/place_feinfilter_paar.py` (Paare); `FEXCL` leer = heutiges Modell. 44 statt 50 Hindernisse; Rest wie Abschnitt 2.
- **Streng (>= 500 allseits, Rueckseite >= 150): Einzellagen gibt es jetzt** (985 Lagen, 4 Orte ab 400 mm, beste Luecke 671 mm bei x 925 y -4625, 560 bei x 975 y -3675, 497 bei x 2875 y -1975). Ost-Linie: nur 3 Lagen, alle bei x 1125 bis 1175 y -3425 (Az -71, 59 mm neben der Tuerachse); West-Linie: 982 Lagen.
- **Aber kein gueltiges Paar:** Es gibt 4 Orts-Paare mit >= 500 mm untereinander (z. B. x 925 y -3425 mit x 925 y -4725, Summe Rohr etwa 9,5 m). Sie sitzen im Tuergang: Zellen mit Gang >= 900 mm (D29) sinken von 1226 auf 10 bis 12, Gang-500-Zellen von 6700 auf 5200; das Paar x 1175 y -3425 + x 825 y -4625 versiegelt die Tuer (kein Bauteil mehr erreichbar). **Streng also auch bei Kandidat A: NEIN fuer ein Paar ausserhalb des Tuergangs.**
- **Bedienzone-Regel mit Kandidat A: ja, deutlich besser.** Ost B x 2575 y -1375, Drehung 30 (Az -28, r 2919; Rohr Pool~640, Pumpe~624, an der Stelle von Tank_klein:2) und West B x -1575 y -3175, Drehung 285 (wie in Abschnitt 2, Pool~1170, Pumpe~904). Zusatzort Ost C x 3175 y -1425, Drehung 0 (Pool~1038, Pumpe~686), West A x 725 y -2875, Drehung 240 (Pool~607). Paar Ost B + West B: alle Bauteile erreichbar, Tuergang 900 unveraendert (1226 Zellen), Gang-500-Zellen 6700 -> 5772 (nur die lokale Filterzone). Ost B + West A kostet Tuergang-Zellen (1226 -> 832): nicht nehmen.
- **Einordnung:** Kandidat A heisst: Vortex-Absetzer (267 l) und Absetzer-Teilstrom K03 bis K05 entfallen, in D71 nur Kandidat, Quellenlage reicht nicht fuer zwei unabhaengige Quellen. Rohrnetz aendert sich: K03/K04/K05/K07 (und Gegenstuecke Linie 2) entfallen, Pool-Bodenablauf ginge dann ueber ein Sieb/Schlammfang oder direkt in den Feinfilter; das waere eine neue Netzliste, keine Annahme von mir.

Pumpe vor dem Filter (Druckseite) scheidet mit T55 aus: offenes Gehaeuse mit Deckel auf EPDM-Flachdichtung, kein Druckgehaeuse; ein neues Bauteil waere noetig.

**Hoehenlage F1 (Rechnung, gilt fuer jede Variante):** Netzlisten-Z sind auf den Flur bezogen (Beleg Abschnitt 3). Seitenablauf Z 340, Filter-Einlauf muss <= Z 320 liegen: Standflaeche Z -496, also Grube ca. 500 mm unter Flur (Oberkante Behaelter Z +407). Auslauf dann Z -186, Pumpen-Saugstutzen Z 120 liegt im Normalbetrieb (Filterspiegel etwa am Einlauf Z 320) rund 200 mm unter dem Filterspiegel, damit geflutet. Grube etwa 900 x 800 x 500 [A].

## 3. Grundlagen aus den Eingaben
- **Hoehenbezug:** `params.json` sock_h = 400 "Bodenniveau (Z=400 absolut)". Die Netzlisten-Z (Pool 515, Beetboden -162, Tisch 1000) sind Flur-relativ: Beet-Instanz Z 238 absolut = 400 - 162. Bau rechnet absolut = relativ + 400 [A, Probe in S0: Pumpe_gross Saugstutzen Z 120 relativ muss 520 absolut messen]. Poolrand 650, Spiegel 515, Bodenablauf -1685.
- **Linien (Rechnung aus den Instanz-Azimuten):** Die Tuerachse (Az -54 / 126) teilt die Kuppel in zwei Haelften mit je 12 Tischen und 7 Beeten (D67 erfuellt, Tisch-Zaehlung je Sektor 1,2,3,3,3 | 3,3,3,2,1). **Linie 1 = Ost** (Sektoren Az -35,7 / 0,3 / 36,3 / 72,3 / 108,3; Tank_gross:1, Pumpe_gross:1 und 2, Tank_klein:2, Pumpe_klein:3 und 4, Messknoten mk_l1 liegt dort). **Linie 2 = West** (Sektoren Az 144,3 / -179,7 / -143,7 / -107,7 / -71,7; Tank_gross_t3:1, Pumpe_gross:3 und 4, Tank_klein:1, Pumpe_klein:1 und 2). Befund: Die Netzliste fuehrt Absetzer 1 und Pumpe_klein 1 und 2 zu Linie 1, im Modell stehen sie aber in der West-Gruppe; die Netz-Etiketten absetzer_1/2 und pumpe_klein_1..4 muessen auf die Modell-Instanzen umgehaengt werden (nur Namen, [A], Orchestrator bestaetigt).
- **Port-Hoehen (relativ zum Flur):** Pumpe_gross Saug Z 120, Druck Z 255; Tank_klein Zulauf tangential Z 997, Auslauf 1147, Schlammablass Z 80; Tank_gross Zulauf Z 1420, Ueberlauf 1570, Belueftung Deckel 1676; Tisch Zulauf Z 1076 bis 1091, Ablauf 999 bis 1014; Beet Ablauf d25 Rohrende unter dem Boden, Tropfrohr-Zulauf Z 612 bis 624; Puffer klein Messkreis-Zulauf Z 933, Ablauf Z 1138.
- **Gaenge:** Laufwege A 700 / B 600 / Wandluft 110; 58 rote und 72 gelbe Engstellen vorhanden (`docs/loop-state.md`). Regel des Blatts: Leitungen verschlechtern keine Engstelle.
- **Schaltschrank:** nur als Komponentendatei, nicht im Modell, "Flaeche 0" seit D62/D63; Standort offen (E4).

## 4. Trassenregeln
1. **Hoehenbaender:** U = unterflur (Z -100 bis -400 relativ, Graben im Erdboden mit Leerrohr); W = am Tank, Pumpentafel, Beckenrand (Z 0 bis 1000, nur in den Technikgruppen); T = Tischebene (Z 900 bis 1100, nur unter den Rinnen); Ü = ueber Kopf (Z >= 2100). Nichts liegt frei zwischen Z 0 und 2100 quer im Gang.
2. **Ringsammler Ruecklauf:** je Linie ein Halbring d110 auf der Pool-Wandkrone (Z 660 bis 720, ueber Spiegel 515 und Rand 650, nicht im Gang A), Gefaelle >= 1 % zu zwei offenen Enden ueber dem Wasser (K16, K32). Die Halbringe treffen sich an der Tuerachse nicht; jede Linie behaelt ihre Haelfte.
3. **Sektorsammler:** pro Sektor ein Sammelrohr d63 laengs der Sektorfuge (zwischen zwei Tisch-/Portalreihen) auf Z 900 bis 950 unter den Tischablaeufen, Gefaelle 1,5 % nach innen (K15, K31), Tisch-Ablauf d50 per T auf d63. Anschluss an den Halbring am Poolrand. Mittel- und Aussenring entwaessern in den Sammler des gleichen Sektors.
4. **Abgaenge je Sektor und Linie:** Biofilter-Ueberlauf d50 (Z 1570) per Schwerkraft zum Verteiler der Linie in der Tech-Gruppe; vom Verteiler: Beete d40 (K11) mit Tropfrohr d20 je Beet, NFT d32 (K12) als Strang durch die Sektoren der Linie am Tischbein, Z ca. 1090, je Tisch Zulaufverteiler und Schlauch ID16/AD20 je Rinne (38 Rinnen je Linie), Bypass d50 (K13/K29) unterflur direkt in den Ruecklauf, Messkreis d20 (K35) zur Puffer-Messzelle.
5. **Unterflur-Leitungen:** Pool-Seitenablauf Z 340 -> Graben -> Filter-Einlauf Z 320 (Pipe-voll, Heber, nie oberhalb Spiegel; Verlust bei 97,5 l/min in d63 < 20 mm gegen 195 mm Druckhoehe [E]); Pool-Bodenablauf d50 -> d40 (K03/K19); Beet-Ablaeufe d25 -> Sammelleitung d50 -> Sumpf (F3); Frischwasser d25 und Luft d40/d25/d20; Kabel-Leerrohre.
6. **Gangkreuzungen:** nur Unterflur (Leerrohr) oder Ü >= 2100. Bis zu 2 Kreuzungen je Sektorsammler (Aussen/Mitte und Mitte/Innen) und je eine am Poolring sind zu erwarten; jede wird im Schritt gegen die Gangkarte geprueft. Gefaelle-Rohre, die nicht unterflur gehen koennen (Ruecklauf oberhalb 515), liegen in den Fugen an den Tischbeinen.
7. **Befestigung ohne Streben:** Tischbein-Fussplatten und Beine, Portale, Tank- und Pumpentafeln, Pool-Wandkrone, Fundamentring; niemals Streben, Knoten, Haut oder Plane (Statik offen, N-STATIK). Klemmen alle 0,5 bis 1 m (`hydraulics.md` 5, Rohrklemme ist Fuss-Klemme: fuer Vierkant-Beine fehlt die Schelle, siehe Abschnitt 7).
8. **Biegeradius und Teile:** Schlauch >= 5 x AD, nur Standardteile (Bogen, T, Ventil, Kupplung), jedes als Bauteil; Rohrverlauf aus dem Graphen. Geschwindigkeit Druckseite <= 1,5, Saugseite <= 1,0 m/s (`scripts/check_netz.py`). Farben: Frischwasser hellblau, Filterlinie dunkelblau, Ruecklauf grau, Luft schwarz oder gruen.
9. **Kabel:** Leerrohre unterflur vom Schaltschrank zu Ost- und West-Gruppe; 230 V (8 Pumpen mit Stecker) und Signal-Trunks in getrennten Rohren oder >= 200 mm Abstand [A, EMV].

## 5. Entscheidungen F1 bis F7
| F | Vorschlag / Annahme | Begruendung |
|---|---|---|
| F1 Feinfilter-Hoehe | Grube Standflaeche Z -496, Einlauf 320, Auslauf -186 (siehe Abschnitt 2); Pumpe vor dem Filter verworfen | T55 ist offenes Gehaeuse; Pumpen-Saug Z 120 geflutet; Grubenboden-Wasser und Pumpensumpf ungeklaert [A] |
| F2 Seitenablauf Z 340 | **annehmen** [A]; je Linie ein eigener Ablauf d63 am Pool, am Azimut des zugehoerigen Filters | 175 mm Ueberdeckung >= 171 mm Mindestwert (Faustformel nach Gordon, nicht aus Quelle gelesen); Z 450 haette 65 mm |
| F3 Beet-Sumpf | je Linie 1 Sumpf 300 l eingegraben (>= 234 l, ein Beet-Flutzyklus), Tauchpumpe ca. 55 l/min bei etwa 1,0 bis 1,3 m, 36 W laut F3 [E], Schwimmerschalter, Deckel begehbar; Beet-Ablaeufe d25 per Sammelleitung d50 unterflur zum Sumpf; Druckleitung d32 unterflur zum Poolrand, am Beckenaussenrand hoch zum Halbring | Beetablauf Z -100 liegt 600 mm unter Spiegel 515; Beet-Port ist d25 (36 l/min waeren 1,6 m/s), Netz fuehrt d40: Widerspruch, siehe Risiken |
| F4 Luftbedarf Pool | Gebläse am hoeheren Wert dimensionieren (130 l/min Pool, K44 120), Gesamtleitung d40, Abzweige d25/d20 | Wert spaeter nach Messung zurueckstufbar; kein Mehrpreis im Rohr, nur im Geblaese |
| F5 Signalkabel | 7 Trunks unterflur, Abschnitt 8; Spannungsabfall < 0,6 % bei 0,5 mm2 | Rechnung Abschnitt 8; Notstrom: Zentrale an der 24-V-Batterie, 28 W Messnetz [A] |
| F6 Aktivkohle | Platzhalter-Gehaeuse Handelsteil (Fabrikat offen) im Frischwasser hinter dem Zulaufrohr, Schwimmerventil am Pool | Kontaktzeit/Wechsel nicht Teil von M10; Bauteil fehlt (Abschnitt 7) |
| F7 Biofilter-Bett | Netzliste 67 %, Werkstatt gleicht an | beeinflusst keine Rohrstroeme (Pumpen 4 x 55 l/min) |
Zusatz E1 bis E5 (Entscheidungen fuer Ben): E1 Feinfilter-Option a bis e; E2 Netz-Etiketten Linie 1/2 umhaengen; E3 Beet-Sumpf und neue Verbraucher (2 x 36 W) akzeptieren; E4 Schaltschrank-Standort ([A] aussen am Fundamentring neben der Tuer, Az etwa -85, Kabelrechnung +-2 m); E5 Kuppel-Trunk (mk_kuppel) erst nach N-STATIK, Mast statt Strebe.

## 6. Bauschritte (je einzeln committbar, Build nur nach Orchestrator-Gegenlesen)
| Schritt | Inhalt | Pruefung vor Commit |
|---|---|---|
| S0 | Entscheidungen E1 bis E5; Hoehenprobe (relativ + 400); neues Skript `scripts/check_leitungen.py`: Rohrachsen aus dem Graphen als Zylinder gegen Hindernisse und Gangkarte, Hoehenband-Test, Gangkreuzung | Skript laeuft auf leerem Modell, `py_compile` |
| S1 | 2 x T55 in Grube setzen, Grube, Ports am Pool (Seitenablauf Z 340, Bodenablauf) | `check_walkways.py`, `WCELL=100 WSLICES=knie python scripts/check_walkways_voll.py` (Probelauf), Filter erreichbar |
| S2 | Hauptkreislauf Linie 1 (K01 bis K10, Absetzerkreis K03 bis K05, Notbypass K56): Pool -> Filter -> Pumpen -> Biofilter; dann Linie 2 (K17 bis K26, K57) | Kollision `check_leitungen.py`, `check_netz.py` PASS, Gangkarte Probelauf |
| S3 | Verteiler, Beete und NFT je Linie (K11/K12/K13, K27 bis K29) | wie S2, Gangkreuzungen einzeln gelistet |
| S4 | Ruecklauf: Tisch-/Sektorsammler, Beet-Sumpf, Halbringe, Zweitbecken-Teilstrom (K14 bis K16, K30 bis K34) | wie S2, Gefaelle >= 1 % aus den Koordinaten |
| S5 | Drittbecken, Zweitbecken, Belueftung, Frischwasser/Aktivkohle, Puffer-Messkreis, Dosierleitungen (K35 bis K55) | wie S2 |
| S6 | Kabel: Leerrohre, 230 V, Trunks, Messstellen-Halter (Abschnitt 8) | `check_leitungen.py`, Trunk-Laengen gegen Abschnitt 8 |
| S7 | Abschluss: `check_walkways.py` und volle `check_walkways_voll.py` (7,5 min bei 50 mm), Kollision, Draufsicht und Seitenansicht per `scripts/archive_render.py` in den Bildverlauf; `docs/model-description.md`, `docs/integration-board.md`; PAUSE Zwischencheck mit Ben | alle drei Pruefungen gruen oder offen benannt |
Commit je Schritt `M10-Sn: ...`, WIP-Commit nach jedem Schritt, nie `git add -A`. Der grosse `check_latte` und die Viewer-Messstellenebene (V-MESS) sind nicht Teil von M10.

## 7. Fehlende Leitungsteile (Werkstatt-Notiz, nicht selbst bauen)
Bibliothek `docs/parts/leitungsteile.md`: 63 Definitionen, 3 Verteiler nur als d32 n=2 bis 4. Fehlt oder fehlt vermutlich:
1. **Verteiler d50** mit Abgaengen d40 (Beete), d32 (NFT), d50 (Bypass), d20 (Messkreis) fuer die zwei Linien.
2. **Pool-Ports** am Bauteil Zentralpool: Seitenablauf d63 Z 340 (je Linie), Bodenablauf d50, Einlauf Ringsammler; Zweitbecken und Drittbecken haben keine Ports (`becken_dritt_klein.md`: Stutzen nicht modelliert).
3. **Beet-Sumpf** (Behaelter 300 l, eingegraben, Deckel, Schwimmerschalter) plus **Tauchpumpe** ca. 36 W.
4. **Aktivkohle-Gehaeuse** (Handelsteil Platzhalter) und **Schwimmerventil**.
5. **Schaltschrank**: Komponente einsetzen mit Leerrohr-Einfuehrung (Standort E4).
6. **Geblaese** (Seitenkanal/Membran), Luftverteiler 4- und 6-fach d40 auf d25/d20, Rueckschlagventil, Membranausstroemer.
7. **Rohrschelle fuer Vierkantprofil** (Tischbeine) d32/d63 statt Fuss-Klemme; **Leerrohr-Stuecke** DN50/DN100 mit Bogen; **Kabel-Trasse** als Sweep-Bauteil.
8. **T-Stueck d63/d50/d50** (Feinfilter-Auslauf, K06/K22): ggf. T d63 plus Reduziermuffe, Pruefung durch Werkstatt.
9. **Grubenbauteil** fuer den Feinfilter (Wannen/Auskleidung, Abdeckung) je nach E1.

## 8. Rest-Messstellen und Signalkabel
**Zuordnung nach `docs/loop-state.md` (M-SETZEN):**
| Messstellen | Was | Schritt |
|---|---|---|
| MS14, MS15 | Feinfilter-Halter (Einlauf/Auslauf) | S1 |
| MS28 bis MS31 | Tank-Auslass / Druckkopf (Lage am Tank offen) | S2/S3 |
| MS06, 11 bis 13, 20 bis 23, 32 bis 45, 47, 50, 56, 58 | H_INLINE / H_HAHN / H_DRUCK am Rohr; Kante je MS aus `data/messstellen.json` (in diesem Plan nicht gelesen), gebuendelt nach Kette K01 bis K10 (S2), K11 bis K13 (S3), K14 bis K16 (S4), K35 bis K43 (S5) | S2 bis S5 |
| MS48, 49, 51, 52 | Fass/Dosierkonsole-Sonden am Puffer | S5 |
| MS16 bis 19, 24 bis 27, 57, 64 bis 67 | Schaltschrank-Sonden | S6, nach E4 |
| MS59 bis MS63 | Kuppel/Heizung | nach N-STATIK (E5) |

**7 Trunks** (je 4 Adern Bus RS-485 + 2 Adern 24 V, Schaltschrank-Ende [A] bei Az -85, r 5750), Kabellaenge = 1,35 x Luftlinie + 3 m unterflur/senkrecht, Spannungsabfall bei 0,5 mm2 Kupfer, Strom aus der Leistung je Knoten:
| Trunk | Ziel | Luftlinie | Kabel | Leistung / Abfall |
|---|---|---|---|---|
| mk_pool | Beckenrand Zentralpool | 3,7 m | 8,0 m | 3 W / 0,3 % |
| mk_zd | zwischen Zweit- und Drittbecken | 4,0 m | 8,4 m | 2 W / 0,2 % |
| mk_l1 | Tank_gross:1 (Ost) | 6,1 m | 11,3 m | 3 W / 0,4 % |
| mk_l2 | Tank_gross_t3 (West) | 2,6 m | 6,5 m | 3 W / 0,2 % |
| mk_puffer | Puffer klein | 3,8 m | 8,1 m | 5 W / 0,5 % |
| mk_schrank | im Schaltschrank | 0 | 3 m | 10 W / 0,4 % |
| mk_kuppel | Kuppelinneres (Mast, Scheitel) | offen | etwa 15 bis 20 m [A] | 2 W / vernachlaessigbar |
Rechnung: Python im Scratchpad ueber `dome-script.json`-Positionen, 24 V, rho 0,0178 Ohm mm2/m; 230-V-Wege zu den Pumpen 5 bis 12 m. F5 ist damit entschieden, Trasse siehe Regel 9. Sonden-Stichleitungen sind Herstellerkabel (pH/EC 1 m, DO 3 m): Knoten neben dem Halter.

## 9. Risiken
1. **Feinfilter-Platz** (Abschnitt 2): ohne Entscheidung kein S1; West A zerstoert die Puffer-Reserve.
2. **Ruecklauf quer ueber Gaenge:** Gefaelle verbietet Unterflur oberhalb Spiegel 515; bleibt nur Ü >= 2100 oder Fuge am Tischbein. Zaehlt erst im Bau (check_leitungen).
3. **Hoehenbezug:** Flur-relative Netz-Z gegen absolute Modell-Z; falsche Probe wuerde alles um 400 mm verschieben.
4. **Beet-Ablauf-Widerspruch:** Beet-Port d25 (`ibc_beet.md`) gegen Netz K14/K30 d40; bei d25 liegen die 36 l/min Spitze bei 1,6 m/s > 1,5.
5. **Netz-Etiketten Linie 1/2** gegen Modellinstanzen; sonst falsche Pumpen/Tanks verbunden.
6. **Modellgroesse:** Viewer meldet 212 MB defs (Ziel < 40 MB); Leitungen nur als Instanzen der Bibliothek, Zeitaufwand Neubau/`export_model.py` pruefen.
7. **Statik offen:** keine Strebenbefestigung, Kuppel-Trunk wartet; Grube/Sumpf im Erdboden ohne Grundwasserangabe [A].
8. Schlauchradius 5 x AD in engen Fugen (Tisch d20: 100 mm) kann nicht immer eingehalten werden.

## 10. Was der Orchestrator gegenlesen muss
1. Befund Feinfilter: strenger Standort NEIN, kleinste Luecke 325 mm West / 181 mm Ost; Option a bis e an Ben (e = Kandidat A, Abschnitt 2e), D71 geht zurueck.
2. Hoehenbezug Flur Z 400 (Netz-Z relativ) und die Grube Z -496 fuer F1.
3. Linie 1 = Ost, Linie 2 = West (Teilung an der Tuerachse, 12 + 7 je Seite) und das Umhaengen der Netz-Etiketten.
4. Ruecklaufkonzept (Halbring auf der Wandkrone, Sektorsammler, Kreuzung nur Unterflur oder ueber 2100) und Beet-Sumpf mit zusaetzlicher Pumpe 2 x 36 W.
5. Fehlteile-Liste (Abschnitt 7) und Schaltschrank-Standort E4, bevor S2 beginnt.

Geprueft gegen: `docs/jobs/M10-leitungen.md`, `data/leitungsnetz.json` v2, `docs/leitungsnetz-aenderungen.md` 85 bis 117, `docs/parts/leitungsteile.md`, `docs/hydraulics.md` 51 bis 56, `docs/loop-state.md` M-SETZEN und Laufwegkarte, `docs/parts/feinfilter.md`, `tank.md`, `pumpe.md`, `ibc_beet.md`, `nft_tisch.md`, `puffer_klein.md` (Ports), `scripts/dome-script.json`, `data/messstellen.json` (messknoten, signalweg), `data/params.json` sock_h · Offen: Feinfilter-Standort (Entscheidung Ben), Messstellen-Kanten je MS-ID (nicht gelesen), Kuppel-Trunk, Schaltschrank-Standort, Beet-Ablauf-DN, Grundwasser an der Grube, nichts gebaut oder gebaut-geprueft.
