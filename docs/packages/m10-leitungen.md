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

## 11. Stand und Luecken (Orchestrator, 01.11.2026 abends)
**Verlegt:** 20 von 55 Kanten (K01 bis K06, K08 bis K10, K17 bis K22, K24 bis K26, Notbypass K56/K57), 53,6 m Rohr, 199 Instanzen in `08_Leitungen`, 0 Verstoesse im Pruefskript, Laufwege A 700 / B 600 / Wandluft 110. Beide Linien des Hauptkreislaufs enden offen am Verteiler-Eingang (K10, K26). **Offen:** 35 Wasser-/Luftkanten und 23 Kabelzeilen (7 Trunks).
**Kann direkt passieren (nur Bibliotheksteile):** S4a Ruecklauf-Halbringe d110 und Sektorsammler d63 (Rohr, Bogen, T), Pool-Einlaeufe; K37 Puffer-Messzelle -> Pool; Leitungen K38 (Dosierschlauch). Vorher pruefen (Aktualitaetspruefung): Beetanschluss d25/d40.
**Muss vorher passieren:** W36 Verteiler d50 (dann S3: K11 bis K13, K27 bis K29, K35); Klaerung Beet-Ablauf-DN (L03) und Tropfrohr/Tischzulauf (L16) vor den Beet-Anschluessen; Beet-Sumpf mit Pumpe (L04) vor dem Beet-Rueckfluss; Aktivkohle/Schwimmerventil (L05), Geblaese/Luftverteiler (L06), Zweit-/Drittbecken-Stutzen (L09), Schlammsammler (L01) vor S5; Rohrschelle Vierkant, Leerrohr, Kabel-Sweep, Schaltschrank (L07, L08) vor S6.
**Alle Luecken** stehen mit Nummer L01 bis L19 in `data/roadmap.json` und auf der Roadmap-Seite unter "Offene Luecken und Risiken".

## 12. Luecken-Zuordnung und Sitzungszuschnitt (Orchestrator, 01.11.2026 abends, wartet auf Bens Freigabe E11)
Zuschnitt nach gemeinsamen Dateien, nicht nach Teilen: Teile, die dieselben Bibliotheksdateien schreiben, gehoeren in eine Sitzung (zwei Schreiber wuerden sich ueberschreiben); eine Sitzung je Mini-Teil wuerde jedes Mal Konvention und Werkzeug neu einlesen. Lesen und Rechnen darf parallel laufen, schreiben nur eine Sitzung gleichzeitig.
| Welle | Sitzung | Schliesst | Voraussetzung |
|---|---|---|---|
| 1 | NETZ-ETIKETT (Orchestrator, klein) | L14 | Freigabe |
| 1 | R45 Hydraulik und Auslegung (Fachrecherche, nur lesen und rechnen, parallel erlaubt) | Zahlen fuer L03, L04, L05, L06, L10 | Freigabe |
| 1 | W36 Werkstatt A: Leitungsteile (Verteiler d50, Rohrschelle, Leerrohr, Schacht, Tropfrohr-Pruefung) | L02, L07 (Teile), L16, L17 | Freigabe |
| 2 | W37 Werkstatt B: Anlagenteile (Beet-Sumpf, Aktivkohle, Geblaese, Schaltschrank, Becken-Stutzen, Schlammsammler) | L01, L04, L05, L06, L08, L09 | R45, E12, E13 |
| 3 | M10 S3, S4, S5, S6, S7 (je eine Montage-Sitzung) | L11, L12, L13, L15, L10 (Nachrechnung) | siehe Roadmap je Schritt |
| danach | V-MESS (L18), CHECK (L19) | L18, L19 | M10 fertig |
Nicht vorab schliessbar, weil sie erst am fertigen Rohr pruefbar sind: L10 (Nachrechnung), L11, L12, L13, L15, L19; sie stehen als Pruefauftrag im jeweiligen Schritt. Die Fragen, die nur Ben beantworten kann (E11 bis E16), stehen oben auf der Roadmap-Seite.

## 13. M10-S2R Heber K01/K17 auf d75 (Montage, 01.11.2026 spaet; Blatt `docs/jobs/M10-S2R-heber-d75.md`)
**Problem:** K01/K17 sind mit d63 verlegt (Runde 65); R45 Abschnitt 2: Reserve im ungünstigen Fall -22/-14 mm, Grenze 30 mm. **Intent:** Ben hat E14 = durchgehend d75 entschieden. **Goal:** K01/K17 (je Linie `K01`, `K01-m`, `K01-b`) in d75, Achshoehen Z 740 / 150 / 720 unveraendert, Reserve >= 85 mm im ungünstigen Fall, alle Pruefungen gruen, Runde 66.
**Mini-Plan (je Schritt ein Pfad-Commit):**
1. `scripts/trassen_linie.py`: `pool_filter` mit Rohr d75; je Ende Reduziermuffe d75/d63 auf dem d63-Stutzen (kleine Seite B steckt auf dem Stutzen, grosse Seite A nach aussen), danach Rohrstueck 2 t und Bogen d75 (Kreuzungspunkt k = 134 mm hinter Ebene A); Achsen-Z unveraendert, die Senkrechten rutschen waagerecht nach aussen. T4/T12 (Absetzer-Zulauf) und T5/T13 (Notbypass) als T d75 (`leitungen.t_stueck` rechnet Rohrstueck + Reduziermuffe d75/d50 bzw. d75/d63 selbst); Kugelhahn K56/K57 sitzt unter dem verlaengerten Abgang (86,4 + 87,5 mm statt 73,6 mm), Tiefleitung faellt um denselben Betrag (Luft zum Filterkasten wird groesser). `data/leitungstrassen.json` neu erzeugen (Linie 1, dann Linie 2) und gegen den Altstand vergleichen: nur K01/K17-Teile, T4/T5/T12/T13, K05/K21-Enden, Bypass duerfen sich aendern.
2. Build `scripts/build.sh 5 66`: Platzierung, Graben (`erde_fn`, Formstuecke 84,75 mm; Boolean Linie 1 und 2 gleich behandeln und melden).
3. Pruefung: `check_leitungen.py` 0 Verstoesse, `check_walkways.py` PASS, `python -X utf8 scripts/r45_heber.py` (Reserve >= 85 mm im ungünstigen Fall), Bild per `archive_render.py --role montage` (Draufsicht, Schnitt durch den Graben).
**Stand (01.11.2026 nachts): Schritte 1 bis 3 erledigt, Runde 66.**
- Schritt 1 (Commit 6dc2d75): `trassen_linie.py`: Heber d75, Reduziermuffe d75/d63 an Pool- und Filterstutzen (`heber_red`), T4/T5/T12/T13 als T d75; die T-Lagen bleiben an ihrem Ort (`s_alt`: Parameter `lt_*_s` von der alten d63-Ecke gemessen); `check_leitungen.py` kennt das Feld `dn_abweichung` (dokumentierte Abweichung vom Netz-dn ist kein Verstoss).
- Schritt 2 (Commit 3351758): Build `scripts/build.sh 5 66` Exit 0, 23 neue Rohrlaengen `lt_rohr_d<d>_L<mm>.sc`, Erdflaeche mit allen Graeben ohne Boolean-Fehler (Linie 1 und 2 gleich behandelt, keine Sonderlogik noetig); Schnitt z=165 zeigt beide Graeben mit Rohr, T und Abzweigen.
- Schritt 3: `check_leitungen.py` 0 Verstoesse (6 dokumentierte dn-Abweichungen), Selbsttest bestanden; `check_walkways.py` PASS (A 700, B 600, Wandluft 110); `r45_heber.py` mit den gebauten Laengen: K01 3076 mm (1322 + 1754), K17 2216 mm (1078 + 1137), zusammen 5,29 m Rohr d75; Reserve d75 im ungünstigen Fall (Crane Gehrung/T 0,9, gealtert) K01 85 mm, K17 88 mm (Soll >= 85), Mittel 124 / 127 mm. Bilder: `renders/round-66.png`, `section-66.png`, `leitungen-s2r-66-heber1/2.png` (Draufsicht), `-graben-schnitt.png` und `-graben-schnitt-l2.png` (Schnitt z=165).
- Befunde: (1) Die d75-Ecken sitzen 108 mm weiter aussen (Reduziermuffe 50 mm + Bogen-Schenkel 134 mm gegen 75,6 mm vorher); der Graben dreht dadurch (Linie 2: 225,1 auf 215,7 Grad). K21 (Linie 2) behielt seinen 45-Grad-Knick nur durch Drehen der beiden Laeufe um 9,3 Grad (Nordlauf jetzt 80,7, Westlauf 170,7 Grad, Nordlauf driftet 166 mm nach Osten), K21 `check_leitungen` ohne Verstoss. Mit beiden Ecken auf Mindestabstand laesst sich die alte Richtung nicht erreichen (rechnerisch negative Rohrstuecke). (2) Bypass: Abgang T d75 + Reduziermuffe = 173,9 mm statt 73,6 mm; Kugelhahn und Tiefleitung K56/K57 liegen 99,5 mm tiefer (Z -258,9 statt -158,6), die Luft zum Filterkasten wird groesser; Stamm K06-T/K22-T teilt sich an verschobenem T6/T14. (3) Netzliste fuehrt K01/K17 weiter d63; `dn_abweichung` haelt das fest, bis der Orchestrator `data/leitungsnetz.json` nachzieht. (4) Muffentiefe d75 44 mm bleibt Annahme [A], Reserve 85 mm beruht auf den R45-Beiwerten (zwei Reduzierstuecke 0,3), die T-Reduzierungen laufen nicht im Strom. (5) Nicht gelaufen: voller check_latte, check_walkways_voll.

## 14a. Vorbedingung S2N: tiefer Ventilschacht d63 (Werkstatt, 05.11.2026; Blatt `docs/jobs/M10-S2N.md` Aktualitaetspruefung Punkt 5)
**Problem:** `lt_schacht_kugelhahn_d63` passt nur fuer eine waagerechte Achse 160 mm unter Flur; KH1/KH2 sitzen senkrecht (Port A 424 mm unter Flur), die Stamm-Haehne waagerecht 186 mm unter Flur. **Intent:** S2N kann die Schaechte (R47 M2) setzen statt sie OFFEN zu fuehren. **Goal:** Schacht-Bauformen fuer beide Lagen, Deckel buendig Z 400, Interferenz 0, Abstand zu allen Bestandstrassen am Einbauort gemessen.
**Stand: gebaut und gemessen.**
- Dateien: `designs/components/lt_schacht_kugelhahn_d63_tief_senkrecht.sc` (KH1/KH2) und `..._tief_waagerecht.sc` (Stamm); Generator `scripts/workshop/schacht_tief.py`, Pruefung `scripts/workshop/check_schacht_tief.py`, Daten `data/components/lt_schacht_tief.json`, Blatt `docs/parts/schacht_kugelhahn_tief.md`, Teiledaten `data/parts/lt_schacht_kugelhahn_d63_tief_*.json`.
- Messung: `python -X utf8 scripts/workshop/check_schacht_tief.py` 46/46 PASS; `python -X utf8 scripts/workshop/check_parts.py lt_schacht_kugelhahn_d63_tief_senkrecht lt_schacht_kugelhahn_d63_tief_waagerecht` 2 x 22/22.
- Senkrecht: innen 188 x 400, Hahnmitte 486,4 unter Flur, Heber d75 laeuft 250 unter Flur quer durch (Durchfuehrung d100), Rohr d63 unten durch den Boden; Luft >= 10 mm zu allen Trassen und T-Armen an KH1 und KH2 (schmal laengs, weil K17-Bogen und T12-Abgang K21 beidseits nah liegen).
- Waagerecht: innen 240 x 400, Rohrachse 186 unter Flur.
- **Befund fuer S2N (Stamm-Haehne):** Auf K06-T-b/K22-T-b (Plan M3) ist keine Gerade lang genug (frei hoechstens 148 mm, Bedarf 262 mm). Linie 1 passt auf K06-T[2], Hahnmitte 3626,0 / 458,2 / 214,0, 99,5 mm Luft (Hahn sperrt dann den Filterauslauf; Bypass K56 versorgt die Pumpen). Linie 2 hat keinen Platz: K18 laeuft 68 mm neben K22-T, die Schachtwand laege 25 mm im Rohr. Optionen im Blatt; Entscheidung Montage/Orchestrator.
- Einbau-Lage (Achsen, Hahn-Drehung) und Ports: Blatt `docs/parts/schacht_kugelhahn_tief.md`.

## 14b. M10-UMBAU Bestand nach der Leitungsordnung neu verlegen (Montage, 05.11.2026; Blatt `docs/jobs/M10-UMBAU.md`, Runde 71)
**Problem:** 21 gebaute Kanten liegen schraeg, in Bogenketten und ohne Halter; Schlammablaesse blind, Ueberlauf K10/K26 frei, Luft K44 in Bogenketten. **Intent:** saubere, realistische Leitungen als Grundlage fuer S2N bis S7 (Ben, W71). **Goal:** `check_leitungsordnung.py` R1 bis R9 0 Verstoesse, R10 34, Heber-Reserve >= 85/88 mm, Instanzen Schlammfass 2, Federhahn 2, Verteiler 2.

**Plan (Reihenfolge laut Blatt):** (1) Pruefskript, (2) Router Manhattan im Welt-Rahmen, (3) Linie 1, Bild, (4) Linie 2, (5) Schlammfass K07/K23, (6) Verteiler K10/K26, (7) Luft K44, (8) M09, (9) Halter, (10) Build Runde 71 und Messung.

**Schritt 1 erledigt:** `scripts/check_leitungsordnung.py` (R1 bis R9, R10 als Info; R4 wie die Inventur instanzbasiert; R7 und R9 als Naeherung, siehe Skriptkopf). **Vorher (Bestand Runde 70), Befehl `python -X utf8 scripts/check_leitungsordnung.py`, Exit 1:**
- Rohr-Instanzen 114, davon schraeg > 3 Grad **74**; Boegen **79**; Halter **0**; waagerechte Richtungen (5-Grad-Klassen, ohne Heber/Port-Ausnahme) 4.
- R1 **51** Pfadsegmente neben der Achse; R2 0; R3 0; R4 **4** Bogenketten (K02/K06-T-b, K18/K22-T, K01/K56-b, K17/K21/K57-b; gleich der Inventur); R5 0; R6 **21** Rohre ueber Flur ohne ausreichende Halter; R7 0 (keine Halter); R8 **1** (K06/K08 138 mm licht); R9 **11** Probepunkte frei im Gang (K08, K10, K24, K25, K26, T15).
- R10 **36** Netz-Kanten ohne Trasse (K07, K11 bis K16, K23, K27 bis K35, K37 bis K43, K45 bis K49, K51 bis K55, K58, K59).

**Befund Router (Messung `TL.port()` ueber alle Bauteil-Ports der Linien 1 und 2):** 16 von 28 waagerechten Ports liegen 3,7 bis 18,2 Grad neben den Weltachsen (Feinfilter 15,0; Absetzer Linie 1 16,6, Linie 2 3,7; Biofilter-Tank 10,9 / 18,2; Pumpen Linie 2 18,1; Pumpen Linie 1 0,1 bis 0,3). Weg ohne Sonderbogen: Port -> Rohr in Port-Richtung (<= 300 mm, Ausnahme 2) -> 90-Grad-Bogen lotrecht -> Steiger -> 90-Grad-Bogen in eine Weltachse (der Steiger entkoppelt das Azimut; Etage nach R3).

**Korrektur Vorher-Zahl R4 (05.11.):** Mit Muffentiefe als Verbindungs-Toleranz (statt 25 mm plus groesste Muffentiefe) findet der Vorher-Stand **1** echte Bogenkette (K18, Linie 2); die drei weiteren Ketten der Inventur waren Nachbarschaften verschiedener Leitungen. Befehl: `python -X utf8 scripts/check_leitungsordnung.py --trassen <Kopie Runde 70>`.

**Schritt 2/3 Linie 1 (45af03b):** `trassen_linie.linie1_ordnung` ersetzt fuer Linie 1 das 15-Grad-Raster (alte Funktionen bleiben als Vorlage fuer Linie 2). Lagen-Konstanten `U1` im Skript (Dateiliste erlaubt in `data/params.json` nur `schlammfass_*`).
- Stamm K06-T: Filterauslauf -> Bogen d63 direkt auf dem Stutzen lotrecht -> Etage auf Z 14 -> -X -> T6 (Bypass) -> -X/-Y -> T1 bei x 3000; K06 geradeaus, Steiger vor Pumpe_gross:1; K02 lotrecht aus T1 vor Pumpe_gross:2.
- K08/K09 auf Z 900 ueber der Montagetafel, T2 neben dem Tank, Stamm lotrecht zum Zulauf, 150 mm in Port-Richtung. K10 100 mm in Port-Richtung (Verteiler Schritt 6).
- Heber K01 unveraendert (Laenge 3076 mm, 4 Boegen); T5 (K56) und T4 (K05) mit lotrechtem Abgang nach unten; Bypass-Tiefleitung -Y unter den Stamm, +X, lotrecht in T6.
- K04: Z 780 ueber der Montagetafel, -X, -Y, Steiger, 150 mm in Port-Richtung. K05: Fallrohr, +X / +Y / -X mit 1,5 % auf Z -40 bis -100, lotrecht in T4.
- **Messung Trassen (vor Build), `python -X utf8 scripts/check_leitungsordnung.py`:** Linie 1: R1 0, R2 0, R3 0, R4 0, R5 0, R7 0, R8 0, R9 0; **R6 6 Rohre ohne Halter** (Schritt 9). Gesamt (mit Linie 2 und Luft unveraendert): R1 33 (vorher 51), R4 1 (K18), R6 17, R9 9; Rohre schraeg 54 (vorher 74).
- `python -X utf8 scripts/check_leitungen.py`: 2 Verstoesse (vorher 0): KOLL K08 im Grobkasten Tank_gross:1 (Koerperpruefung mit Kegel/Beinen/Platte: frei; Grobkasten = ganze Grundflaeche bis Plattform), GEFAELLE K05 (siehe Befund B2).
- `python -X utf8 scripts/r45_heber.py`: K01 3076 mm, 4 Boegen, unveraendert; Reserve ungünstig K01 65 / K17 68 mm **vorher und nachher gleich** (Soll Blatt >= 85/88; siehe Befund B3).

**Befunde (an den Orchestrator):**
- **B1 Strebe ueber den Pumpen-Druckstutzen:** Pumpe_gross:2 (unter Tank_gross:1) hat den Druckstutzen 5 mm innerhalb der Querstrebe `Strebe_4` (Tank-Rahmen lokal y -365 gegen -370 bis -410, Z 680 bis 720 abs); jede Leitung nach oben ueberlappt sie um 15 mm (Kastenpruefung). Pumpe_klein:3 unter Tank_klein:2 ebenso 3 mm (`Strebe_2`). Nur durch Bauteil-Lage (Pumpe 20 mm nach innen) oder Strebe loesbar; Lage nicht im Auftrag. Bisheriger Bestand hatte dieselbe Ueberlappung.
- **B2 K05 Gefaelle:** Der Heber liegt schraeg (Az 31,6), sein T4-Abgang kann nur lotrecht in Weltrichtung zeigen. Von oben braeuchte die Etage eine Grabenhoehe Z 304,4 (Band U endet bei Z 300 + 2 mm Toleranz), deshalb kommt K05 von unten und steigt am Ende 239 mm (Tiefpunkt). Entscheidung: (a) Band U um 5 mm erweitern und K05 von oben mit einem schraegen Endstueck <= 300 mm (Ausnahme 2 sinngemaess fuer Heber-T) oder (b) Tiefpunkt hinnehmen (Klarwasser, Leitung ist geflutet). Empfehlung (a).
- **B3 Heber-Reserve:** `r45_heber.py` "GEBAUT, schlechter Fall" meldet schon im Bestand Runde 70 K01 65 / K17 68 mm (unter 85/88); Pruefpunkt 3 des Blatts ist damit unabhaengig vom Umbau rot. Der Umbau aendert Laenge und Formstueckzahl nicht.

**Runde 71 (e881f56), Stand und STOPP (Kontext > 35 %, Blatt Start-Hinweis 5):**
- Build `sh scripts/build.sh 5 71` Exit 0 im vierten Lauf. Lauf 1/2: Erdflaechen-Schnitt ohne Ergebnis (Graeben Linie 1 deckungsgleich; behoben: `leitungen.graben` behandelt Linie 1 wie Linie 2, Bypass-Tiefleitung 200 mm suedlich des Stamms, T6 bei x 3550). Lauf 3: `unknown parameter a_plus` (Text-Parameter `kreislauf_variante` aus d0819fe brach jeden Build; `gen_dome.params()` uebergibt nur Zahlen).
- `check_walkways.py` PASS (A 700, B 600, Wandluft 110, Nachbarportale 307, Tuer-Gang 3177; gleich Runde 70). `check_leitungen.py` 2 Verstoesse (K08 Grobkasten, K05 Gefaelle B2). `default_werkstoffe.py --apply` Exit 0.
- `check_leitungsordnung.py` nach Runde 71: **Linie 1 R1 0, R4 0, R8 0, R9 0, R6 6**; gesamt R1 33 (vorher 51), R4 1 (vorher 1, K18), R6 17, R8 0 (vorher 1), R9 9 (vorher 11), R10 36. Alle Rest-Verstoesse R1/R4/R9 liegen in Linie 2 (K17 bis K26, K57) und Luft K44; R10 36 statt 34, weil K07/K23 (Schritt 5) noch nicht gebaut sind.
- **Nicht gebaut (Rest des Blatts, naechste Montage-Sitzung):** Schritt 4 Linie 2 (Vorlage `linie1_ordnung`, gleiche Etage-Methode; Ports Linie 2 bis 18,2 Grad schraeg), Schritt 5 Schlammfass K07/K23, Schritt 6 Verteiler K10/K26, Schritt 7 Luft K44, Schritt 8 M09, Schritt 9 Halter (R6), Inventur und Bilder je Schritt.
