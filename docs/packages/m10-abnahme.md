# M10 Verrohrung: Stand zur Abnahme (Ben, spaeter im Detail)

Stand 01.11.2026 abends, Orchestrator. Alles hier ist gesichert; nichts laeuft. Die Roadmap (`roadmap/index.html`, Desktop-Verknuepfung "Kuppel Roadmap") fuehrt dieselben Punkte: Abschnitt "Deine Entscheidungen" (E11) und "Offene Luecken und Risiken" (L01 bis L19).

## 1. Was steht (belegt)
- Hauptkreislauf beider Linien vom Pool ueber Feinfilter, Pumpen und Biofilter bis zum Verteiler-Eingang, dazu Absetzerkreis und Notbypass: 20 von 55 Kanten, 53,6 m Rohr, 199 Instanzen in der Gruppe `08_Leitungen` (Runde 65).
- Pruefungen (selbst gelaufen): `scripts/check_leitungen.py` 0 Verstoesse (Eingabe, Kollision, Hoehenband, Gang, Gefaelle); `scripts/check_walkways.py` PASS (Laufweg A 700, B 600, Wandluft 110). Nicht gelaufen: voller check_latte, volle Gangkarte nach Runde 61 (50 mm).
- Bilder zum Ansehen: `renders/leitungen-s2c-65-top.png` (Draufsicht), `renders/round-65.png`, `renders/section-65.png`; Feinfilter und Pool-Stutzen: `renders/top-61.png`, `renders/top-62.png`.
- Entschieden und gebaut: D72 (Feinfilter Ost A und West B in Gruben, Bedienzone-Regel), Pool-Stutzen (zwei Seitenablaeufe d63 auf Z 740, ein Bodenablauf d50).

## 2. Was fehlt (Details in den Luecken L01 bis L19)
- Verteiler d50 (L02, Werkstatt-Blatt `docs/jobs/W36-verteiler-d50.md`, bereit, nicht gebaut), dann Verteilung auf Beete und NFT (S3).
- Rest: Ruecklauf (S4), Becken, Luft, Puffer-Messkreis, Frischwasser (S5), Kabel (S6), Abschluss (S7). Werkstatt-Teile dafuer: Beet-Sumpf mit Pumpe, Aktivkohle-Gehaeuse, Geblaese und Luftverteiler, Rohrschelle fuer Vierkantbeine, Leerrohre, Kabel-Bauteil, Schaltschrank, Zweit-/Drittbecken-Stutzen, Schlammsammler.
- Kann direkt passieren, ohne Werkstatt: Ruecklauf-Halbringe und Sektorsammler (S4a), Puffer-Messzelle zum Pool (K37), Dosierschlauch (K38). Muss vorher passieren: siehe Plan `docs/packages/m10-leitungen.md` Abschnitt 11.

## 3. Was du dir im Detail ansehen solltest (Entscheidungen und tiefere Themen)
1. **Schlammablass (L01), Optionen aus bestehender Recherche** (`docs/filter-konzept.md` Art 6, R30; keine neue Recherche): Die zwei Absetzer haben je einen Schlammablass (d40, Kugelhahn), die Netzlisten-Kanten K07 und K23 (0,5 l/min) enden im Nichts. Menge nach der heutigen Last (346 kg, 1,04 kg Feststoff/Tag laut R44, Swirl-Anteil 23 % unsicher): etwa 22 bis 28 l Frischschlamm je Tag zusammen [E aus R44 und Goddek 2018 Tab. 2, nicht neu geprueft]. Optionen: (a) abgedeckter, belueftet-aerober Kompostbehaelter oder Wurmkompost AUSSERHALB des Kreislaufs (Empfehlung der R30, Groesse dort nicht festgelegt; die 0,53 m3 der R30 gelten nur fuer einen Mineralisations-Reaktor); (b) Schlamm in ein Beet oder Kompost leiten (so steht es in der Netzliste); (c) aerober oder anaerober Reaktor zur Mineralisation (R30 rat ab: Quellenlage duenn, in der gelesenen Messung rueckte die belueftete Variante am schlechtesten ab). Offen: Standort (im Dom ist Platz knapp; ausserhalb braucht eine Leitung durch Fundamentring und Plane, Frost), Entleerung von Hand oder Pumpe, ob 22 bis 28 l/Tag reale Zahlen sind (Betriebsmessung).
2. **Heber-Reserve an den Seitenablaeufen (L10):** K01 27 bis 78 mm, K17 34 bis 81 mm gegen 195 mm Druckhoehe, an der 30-mm-Grenze (Ueberschlag `scripts/heber_rechnung.py`). Was tun: groesseres Rohr, kuerzere Wege, weniger Boegen, oder anderes Konzept (Pumpe statt Heber)?
3. **Beet-Ablauf d25 gegen d40 (L03):** Bauteil hat d25, Netz rechnet d40; bei d25 sind 36 l/min Spitze 1,6 m/s. Aenderung am Bauteil oder am Netz?
4. **Schaltschrank-Standort (L08):** nur Annahme Az -85, r 5750 aussen neben der Tuer; haengt Alarm und Kabelwege dran.
5. **Feinfilter-Nische West B (L13):** zwischen Filter und Pumpe_gross:4 etwa 100 mm statt der 150 mm aus D72 (Raster +-25 bis 50 mm); Auslass-Seite.
6. **Neue Verbraucher Beet-Sumpf (L04):** 2 x 36 W Pumpen und die Frage, ob der Beetrueckfluss so bleibt (Sumpf mit Pumpe, weil Beetablauf 600 mm unter Pool-Spiegel liegt).

## 4. Wie es nach deiner Durchsicht weitergeht (vorbereitet, nichts gestartet)
Reihenfolge, jeweils mit Aktualitaetspruefung vor dem Start (Regel W44): W36 Verteiler d50 -> S3 (Verteilung, Beete, NFT) -> Werkstatt-Buendel (Beet-Sumpf, Aktivkohle, Geblaese, Rohrschelle/Leerrohr/Kabel, Schaltschrank, Becken-Stutzen, Schlammsammler nach deiner Entscheidung zu Punkt 1) -> S4, S5, S6, S7 -> Zwischencheck mit dir. Eine Sitzung gleichzeitig.
