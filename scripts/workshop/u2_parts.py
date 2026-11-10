"""Schreibt data/parts/<name>.json (Teiledaten) und ergaenzt data/descriptions.json fuer die elf U2-Komponenten (N-UNIFY-AUTOBAHN U2).
Koerperzahl, Masse und Box je Teilzeile werden aus dem gebauten .sc gemessen (solidcraft-cli eval); Werkstoff je Zeile folgt dem .sc-Material ueber data/katalog.json.
Der Bezug (D76) kommt aus data/beschaffung/u2_wasserkreislauf.json, sofern vorhanden, sonst 'offen'.
Aufruf: python -X utf8 scripts/workshop/u2_parts.py [name ...]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

ROOT = sc.ROOT
KAT = json.load(open(os.path.join(ROOT, "data", "katalog.json"), encoding="utf-8"))
MAT2W = {m: w["id"] for w in KAT["werkstoffe"] for m in w.get("sc_material", [])}
AUSN = "Katalog- und Stueckliste-Eintrag folgt in U8 (Paket n-unify-autobahn); Teil noch nicht im Gesamtmodell"
BESCH = os.path.join(ROOT, "data", "beschaffung", "u2_wasserkreislauf.json")


def bezug(artikel):
    """Europa-Bezug aus der Recherche-Datei (erster Angebotslink) oder ehrlich 'offen'."""
    if artikel and os.path.exists(BESCH):
        a = json.load(open(BESCH, encoding="utf-8")).get("artikel", {}).get(artikel)
        if a and a.get("angebote"):
            o = a["angebote"][0]
            return f"{o.get('haendler')} ({o.get('land')}) {o.get('url')} [{o.get('konfidenz')}]; {a.get('bemerkung_artikel', '')[:160]}"
        if a:
            return "offen: " + a.get("bemerkung_artikel", "")[:200]
    return "offen: Recherche data/beschaffung/u2_wasserkreislauf.json (D76), Bezug noch nicht belegt"


def T(i, name, koerper, typ, funktion, eig, norm, lm, art=None, katalog=None, konf="angenommen", sonder=None):
    t = dict(id=i, name=name, koerper=koerper, typ=typ, funktion=funktion, eigenschaften=eig, norm=norm, lm=lm, art=art, katalog=katalog, konf=konf)
    if sonder:
        t["ausnahme"] = sonder
    return t


# ----- Spezifikation je Komponente --------------------------------------------------------------------------------------------------------------------------
S = {}

S["sumpftank"] = dict(
    gruppe="Becken und Tanks", titel="Sumpftank (Grube mit Pufferzonen)", kurz="Die Grube im Boden sammelt die Ruecklaeufe einer Linie, hat vier Pufferzonen, einen begehbaren Deckel und Platz fuer Pumpe und Schwimmerschalter.",
    gruppen=[("grube", "Grube", "Betonwanne mit EPDM-Folie und Wasserfuellung.", ["t_wanne", "t_folie", "t_wasser"]),
             ("zonen", "Pufferzonen", "Vier Zonen zu 212 mm mit Trennwaenden und Beschriftung.", ["t_trenn", "t_schild"]),
             ("einbauten", "Einbauten", "Pumpensockel, Zulaeufe und Aufnahme fuer den Schwimmerschalter.", ["t_sockel", "t_zulauf", "t_halter"]),
             ("deckel", "Deckel", "Drei begehbare Gitterrost-Platten.", ["t_deckel"])],
    teile=[T("t_wanne", "Betonwanne", ["Sumpf_Wanne"], "sonderteil", "Tragende Wanne der Grube (Selbstbau oder Fertigteil).", ["Aussen 1329 x 3179, Wand und Boden 100", "Oberkante 40 unter dem Fussboden"], "EN 206 (Beton) [A]", "offen"),
            T("t_folie", "EPDM-Folie (Belag)", ["Sumpf_Folie"], "kaufteil", "Dichtet die Wanne und trennt Beton und Wasser.", ["Schale 2 mm, lichte Grube 1125 x 2975 x 500"], "EN 13361 (Dichtungsbahnen, EPDM) [A]", "offen", art="MAT-epdm-teichfolie"),
            T("t_wasser", "Wasserfuellung (nur Darstellung)", ["Wasser"], "sonderteil", "Der Koerper zeigt 823 l bis zum Soll-Pegel -250; er ist kein Bauteil.", ["Reines Darstellungsvolumen"], "keine (kein Bauteil)", "ja", sonder="Wasserkoerper, kein Bauteil"),
            T("t_trenn", "Trennwand Pufferzone", ["Trennwand_1", "Trennwand_2", "Trennwand_3", "Trennwand_4"], "platte", "Trennt die vier Pufferzonen; Wand 1 und 3 bodenoffen, Wand 2 und 4 als Ueberlaufwehr.", ["PP 10 mm, 1125 breit", "Wand 1 und 3: Oeffnung am Boden 80", "Wand 2 und 4: Wehr bis -290"], "DIN EN ISO 1873 (PP) [A]", "offen"),
            T("t_schild", "Zonenschild", ["Zonenschild_1", "Zonenschild_2", "Zonenschild_3", "Zonenschild_4"], "sonderteil", "Beschriftet die Zonen: 1 Kalk, 2 Aktivkohle, 3 frei, 4 frei.", ["PP 100 x 40 x 2 auf dem Deckel"], "keine", "nein"),
            T("t_sockel", "Pumpensockel", ["Pumpensockel"], "platte", "Standflaeche der Tauchpumpe in der Hauptkammer.", ["PP 400 x 400 x 30"], "DIN EN ISO 1873 (PP) [A]", "ja"),
            T("t_zulauf", "Zulauftuelle ID25", ["Zulauf_1", "Zulauf_2", "Zulauf_3"], "kaufteil", "Nimmt die Ruecklauf-Schlaeuche ID25 oben durch die Wand auf (freier Auslauf).", ["Aussen 32, Bohrung 25, Laenge 142"], "keine (Handelsteil) [A]", "ja", art="ARM-schlauchtuelle-id25"),
            T("t_halter", "Schwimmerhalter", ["Schwimmerhalter"], "sonderteil", "Aufnahme des Schwimmerschalters auf dem Hochstand -110.", ["PP 60 x 40 x 80 an der +X-Wand, Z -120 bis -40"], "keine", "ja"),
            T("t_deckel", "Deckelplatte Gitterrost", ["Deckel_1", "Deckel_2", "Deckel_3"], "kaufteil", "Begehbarer Deckel der Grube, Oberkante = Fussboden; drei einzeln abhebbare Platten.", ["1229 x 1026 x 40 je Platte (Modell als Vollplatte)", "Gitterrost 30/10 verzinkt, rund 35 kg je Platte [A]"], "DIN 24537 (Gitterroste) [A]", "nein", art="MAT-gitterrost-deckel")],
    desc=dict(ablauf=["Die Ruecklaeufe der Anbauringe laufen durch die Zulauftuellen in die Hauptkammer.", "Die Pumpe auf dem Sockel hebt das Wasser 1,00 m in den Fischtank; der Soll-Pegel ist -250 mm.", "Der Schwimmerschalter meldet den Hochstand bei -110 mm; die Zonen am Ende nehmen Kalk oder Aktivkohle auf."],
              masse={"Grube innen": "1125 x 2975 x 500 mm", "Soll-Pegel": "-250 mm (823 l im Modell, Soll 850 l)", "Pufferzonen": "4 x 212 mm", "Hochstand": "-110 mm"},
              grenzen="Der Durchstroem der Pufferzonen (auf/ab) ist als passiver Austausch angenommen (D112); Statik und Auftrieb der Betonwanne sind offen.", quelle="docs/parts/sumpftank.md, data/oasis-soll.json (sump_1)"))

for nm, h, tank, plat in (("podest_vortex", 577, "tank_klein", 619), ("podest_biofilter", 230, "tank_gross", 821)):
    S[nm] = dict(
        gruppe="Becken und Tanks", titel="Podest " + ("Vortex" if "vortex" in nm else "Biofilter"), kurz=f"Stahlrahmen, der {tank} um {h} mm anhebt, damit der Ueberlauf auf dem Soll-Wasserspiegel liegt.",
        gruppen=[("rahmen", "Rahmen", "Stuetzen, Fuss- und Kopfrahmen aus Vierkantrohr.", ["t_stuetze", "t_fussrahmen", "t_kopfrahmen"]), ("platten", "Platten und Bleche", "Fussplatten und Knotenbleche.", ["t_fussplatte", "t_knoten"])],
        teile=[T("t_stuetze", "Stuetze", [f"Stuetze_{i}" for i in range(1, 5)], "profil", "Tragen den Tank.", ["Vierkantrohr 40 x 40 x 3"], "DIN EN 10219 (Hohlprofile) [A]", "nein", katalog="vierkantrohr_40x40x3"),
               T("t_fussrahmen", "Fussrahmen", [f"Fussrahmen_{i}" for i in range(1, 5)], "profil", "Verbindet die Stuetzen unten.", ["Vierkantrohr 40 x 40 x 3, Laenge Spannweite - 80"], "DIN EN 10219 [A]", "nein", katalog="vierkantrohr_40x40x3"),
               T("t_kopfrahmen", "Kopfrahmen", [f"Kopfrahmen_{i}" for i in range(1, 5)], "profil", "Auflage fuer die Tankplattform.", ["Vierkantrohr 40 x 40 x 3, Oberkante = Podesthoehe"], "DIN EN 10219 [A]", "nein", katalog="vierkantrohr_40x40x3"),
               T("t_fussplatte", "Fussplatte", [f"Fussplatte_{i}" for i in range(1, 5)], "platte", "Verteilt die Last auf den Fussboden.", ["Blech 100 x 100 x 6"], "DIN EN 10025 (S235) [A]", "nein"),
               T("t_knoten", "Knotenblech", [f"Knotenblech_{i}" for i in range(1, 9)], "platte", "Versteift die Rahmenecken oben und unten.", ["Blech 6 x 100 x 100, aussen an den X-Seiten"], "DIN EN 10025 (S235) [A]", "nein")],
        desc=dict(ablauf=[f"Der Rahmen steht auf dem Fussboden und traegt {tank}.", "Die Hoehe ist ein Parameter und folgt dem Soll-Wasserspiegel.", "Das Wasser laeuft danach per Schwerkraft weiter."],
                  masse={"Hoehe": f"{h} mm", "Standflaeche": "Rahmen + 60 mm", "Profil": "Vierkantrohr 40 x 40 x 3", "Teile": "24 Koerper"},
                  grenzen="Statik (Kippen, Horizontalkraefte, Fussbodenanker) ist offen (N-STATIK); der Check rechnet nur Druck und Knicken.", quelle=f"docs/parts/{nm}.md, data/oasis-soll.json"))

S["venturi_belueffter"] = dict(
    gruppe="Armaturen", titel="Venturi-Belueffter", kurz="Passiver Injektor im Druckrohr d50, der Luft ins Ruecklaufwasser saugt, bevor es in den Fischtank laeuft.",
    gruppen=[("injektor", "Injektor", "Injektorkoerper und Muffen d50.", ["t_injektor", "t_muffe"]), ("luft", "Luftweg", "Stutzen, Rueckschlagventil und Filter.", ["t_stutzen", "t_rv", "t_filter"])],
    teile=[T("t_injektor", "Injektor (Klasse Mazzei 1583)", ["Injektor"], "kaufteil", "Erzeugt Unterdruck und saugt Luft an.", ["Ø 64 x 150 (Annahme)", "Durchgang Ø 36 vereinfacht"], "keine (Handelsteil) [A]", "offen", art="ARM-venturi-mazzei-1583"),
           T("t_muffe", "Klebemuffe d50", ["Muffe_Ein", "Muffe_Aus"], "normteil", "Verbindet den Injektor mit dem Druckrohr d50.", ["PVC-U, Aussen 58,5, Tiefe 31"], "DIN 8063 / EN 1452 (PVC-U Formstuecke) [A]", "ja"),
           T("t_stutzen", "Ansaugstutzen", ["Saugstutzen"], "kaufteil", "Luftanschluss am Injektor.", ["Ø 24 x 30, Bohrung 8"], "keine [A]", "nein"),
           T("t_rv", "Rueckschlagventil Luft", ["Rueckschlagventil"], "kaufteil", "Verhindert Wasseraustritt bei Stillstand.", ["Ø 30 x 55, Bohrung 8"], "keine [A]", "nein", art="ARM-rueckschlagventil-luft"),
           T("t_filter", "Luftfilter", ["Luftfilter"], "kaufteil", "Haelt Staub von der Ansaugluft ab.", ["Ø 45 x 65"], "keine [A]", "nein")],
    desc=dict(ablauf=["Die Pumpe am Sumpf drueckt das Wasser durch den Injektor.", "Die Verengung erzeugt Unterdruck und saugt Luft ueber Filter und Ventil an.", "Das belueftete Wasser laeuft in den Fischtank."],
              masse={"Laenge": "270 mm (Port A bis B)", "Rohr": "d50", "Durchsatz Soll": "110 l/min je Linie", "Injektor": "Klasse Mazzei 1583 (Ø 64 x 150, Annahme)"},
              grenzen="Antriebsdruck und Durchsatz sind nicht belegt: Tabelle verlangt rund 0,7 bar, die Tauchpumpe liefert hoechstens 0,3 bis 0,4 bar (R60, R59).", quelle="docs/parts/venturi_belueffter.md, data/oasis-soll.json (venturi_1)"))

S["schwimmerschalter_hochstand"] = dict(
    gruppe="Armaturen", titel="Schwimmerschalter Hochstand", kurz="Kabel-Schwimmerschalter, der im Sumpf den Hochstand bei -110 mm meldet und ueber die Steuerung die Pumpe Fischtank zu Filter abschaltet.",
    gruppen=[("schalter", "Schalter und Leitung", "Schwimmer, Klemme und Meldeleitung.", ["t_schwimmer", "t_klemme", "t_kabel"])],
    teile=[T("t_schwimmer", "Schwimmerschalter", ["Schwimmer"], "kaufteil", "Schaltet beim Hochstand.", ["Kugel Ø 70, Mitte = Schaltpunkt"], "keine (Handelsteil) [A]", "offen", art="ARM-schwimmerschalter-hochstand"),
           T("t_klemme", "Kabelklemme", ["Kabelklemme"], "kaufteil", "Haelt das Kabel in der Aufnahme.", ["PA 30 x 30 x 30, Bohrung 7"], "keine [A]", "nein"),
           T("t_kabel", "Meldeleitung (Ausschnitt)", ["Kabel"], "kaufteil", "Fuehrt das Signal zur Steuerung.", ["Ø 7, Ausschnitt 400"], "keine [A]", "offen")],
    desc=dict(ablauf=["Der Schwimmer haengt in der Aufnahme im Sumpf; seine Mitte liegt auf dem Hochstand -110 mm.", "Steigt das Wasser, schaltet er und meldet an die Steuerung.", "Die Steuerung schaltet die Pumpe Fischtank zu Filter dieser Linie ab."],
              masse={"Schaltpunkt": "-110 mm", "Wiedereinschalten": "-180 mm (Annahme)", "Schwimmer": "Ø 70"}, grenzen="Fabrikat und Schaltdifferenz offen; Steuerung gehoert zu U6.", quelle="docs/parts/schwimmerschalter_hochstand.md, data/oasis-soll.json (schwimmer_1)"))

S["notluftpumpe"] = dict(
    gruppe="Luft", titel="Notluftpumpe", kurz="Luftpumpe mit Luftstein im Fischtank, startet bei Ausfall der Wasserpumpen oder des Netzes.",
    gruppen=[("pumpe", "Pumpe", "Gehaeuse, Tuelle und Rueckschlagventil.", ["t_pumpe", "t_tuelle", "t_rv"]), ("leitung", "Leitung und Stein", "Schlauch ueber den Rand und Luftstein.", ["t_schlauch", "t_stein"])],
    teile=[T("t_pumpe", "Luftpumpe (Platzhalter)", ["Pumpe"], "kaufteil", "Erzeugt die Notluft.", ["330 x 230 x 320 (Kandidat Kerry KEA3600, Q)", "60 l/min, 35 W, 230 V"], "keine (Handelsteil) [A]", "nein", art="PMP-luftpumpe-notluft"),
           T("t_tuelle", "Ausgangstuelle", ["Tuelle"], "kaufteil", "Anschluss fuer den Schlauch.", ["Ø 12 x 30"], "keine [A]", "nein"),
           T("t_rv", "Rueckschlagventil Luft", ["Rueckschlagventil"], "kaufteil", "Verhindert Rueckfluss in die Pumpe.", ["Ø 18 x 45"], "keine [A]", "nein", art="ARM-rueckschlagventil-luft"),
           T("t_schlauch", "Luftschlauch (Ausschnitt)", ["Luftschlauch_1", "Luftschlauch_2", "Luftschlauch_3", "Luftschlauch_4"], "kaufteil", "Fuehrt die Luft ueber den Rand (Schleife Z 1300) zum Stein.", ["Aussen 12, vier Stuecke"], "keine [A]", "nein"),
           T("t_stein", "Luftstein", ["Luftstein"], "kaufteil", "Verteilt die Luft im Fischtank.", ["Ø 40 x 100, 20 mm ueber dem Boden"], "keine [A]", "offen", art="ARM-luftstein-notluft")],
    desc=dict(ablauf=["Bei Ausfall der Wasserpumpen oder des Netzes startet die Steuerung die Luftpumpe am Notstrom.", "Die Luft steigt ueber den Rand des Fischtanks (Schleife) und faellt zum Luftstein.", "Der Stein haelt die Fische mit Sauerstoff am Leben."],
              masse={"Luftmenge": "55 l/min Richtwert (offen)", "Schleife": "Z 1300 (Rand 1200 + 100)", "Luftstein": "Z -980 bis -880"}, grenzen="Leistung und Luftmenge wie in der Quelle offen (A24).", quelle="docs/parts/notluftpumpe.md, data/oasis-soll.json (luftpumpe)"))

S["nachspeise_ventil"] = dict(
    gruppe="Armaturen", titel="Nachspeise-Ventil (Regenwasser zuerst)", kurz="Zwei Schwimmerventile am Fischtank: erst Regenwasser, bei dessen Ausbleiben 30 mm tiefer Frischwasser.",
    gruppen=[("regen", "Ventil Regenwasser", "Eingang A, hoehere Kugel.", ["t_uebergang", "t_gehaeuse", "t_wange", "t_hebel"])],
    teile=[T("t_uebergang", "Uebergang Klebemuffe d25", ["Uebergang_regen", "Uebergang_frisch"], "kaufteil", "Verbindet Rohr d25 mit dem Ventil.", ["Aussen 32,25, Tiefe 19"], "DIN 8063 [A]", "ja", art="ARM-schwimmerventil-nachspeise"),
           T("t_gehaeuse", "Ventilgehaeuse 3/4 Zoll", ["Ventilgehaeuse_regen", "Ventilgehaeuse_frisch"], "kaufteil", "Oeffnet und schliesst den Zulauf.", ["Ø 38 x 80"], "keine (Handelsteil) [A]", "offen", art="ARM-schwimmerventil-nachspeise"),
           T("t_wange", "Wangenhalter", ["Wange_L_regen", "Wange_R_regen", "Wange_L_frisch", "Wange_R_frisch"], "kaufteil", "Haelt den Hebelarm.", ["4 mm"], "keine [A]", "offen"),
           T("t_hebel", "Hebelarm mit Schwimmerkugel", ["Hebelarm_mit_Kugel_regen", "Hebelarm_mit_Kugel_frisch"], "kaufteil", "Schliesst das Ventil bei Soll-Spiegel; Frischwasser-Kugel haengt 30 mm tiefer.", ["Arm Ø 8, Kugel Ø 110"], "keine [A]", "offen")],
    desc=dict(ablauf=["Sinkt der Spiegel im Fischtank, oeffnet das Regenwasser-Ventil.", "Kommt kein Regenwasser nach, sinkt der Spiegel um 30 mm und das Frischwasser-Ventil oeffnet.", "Steigt der Spiegel, schliessen beide."],
              masse={"Rohrachse": "510 mm ueber dem Spiegel", "Staffelung": "30 mm", "Eingaenge": "A Regenwasser, B Frischwasser (y 120)"}, grenzen="Zwei Ventile mit Staffelung sind Annahme D114; Maße Platzhalter wie T84.", quelle="docs/parts/nachspeise_ventil.md, data/oasis-soll.json (nachspeise)"))

S["schlamm_sammelbehaelter"] = dict(
    gruppe="Becken und Tanks", titel="Schlamm-Sammelbehaelter", kurz="Oberirdischer Behaelter fuer 350 l Schlamm mit Ablasshahn von Hand, ausserhalb des Wasserkreislaufs.",
    gruppen=[("behaelter", "Behaelter", "Behaelter und Deckel.", ["t_behaelter", "t_deckel"]), ("anschluesse", "Anschluesse", "Einlauf, Entlueftung, Ablass.", ["t_einlauf", "t_entl", "t_auslauf", "t_hahn", "t_hebel"])],
    teile=[T("t_behaelter", "Behaelter 350 l", ["Behaelter"], "kaufteil", "Nimmt den Schlamm auf.", ["Ø 900 x 585, Wand 10"], "keine (Handelsteil) [A]", "offen", art="BEH-schlammbehaelter-350"),
           T("t_deckel", "Deckel", ["Deckel"], "kaufteil", "Schliesst den Behaelter.", ["Ø 900 x 15"], "keine [A]", "offen"),
           T("t_einlauf", "Einlaufstutzen d40", ["Einlaufstutzen"], "normteil", "Zulauf vom Vortex.", ["Muffe d40, 60 hoch"], "DIN 8063 [A]", "nein"),
           T("t_entl", "Entlueftung", ["Entlueftung"], "kaufteil", "Gleicht den Druck aus.", ["Ø 26 x 30"], "keine [A]", "nein"),
           T("t_auslauf", "Ablaufrohr d40", ["Auslaufrohr"], "rohr", "Fuehrt den Schlamm zum Hahn.", ["Ø 40, 50 lang"], "DIN 8062 [A]", "nein", katalog="pvc_u_d40"),
           T("t_hahn", "Kugelhahn d40", ["Kugelhahn"], "kaufteil", "Ablass von Hand.", ["Ø 52 x 70"], "keine (Handelsteil) [A]", "nein"),
           T("t_hebel", "Hahnhebel", ["Hahnhebel"], "kaufteil", "Betaetigt den Hahn.", ["12 x 90 x 10"], "keine [A]", "nein")],
    desc=dict(ablauf=["Der Schlamm laeuft vom Vortex per Schwerkraft in den Behaelter.", "Der Ablasshahn bleibt zu, bis der Behaelter von Hand geleert wird.", "Der Schlamm geht von Hand zum Permakultur-Modul."],
              masse={"Inhalt": "350 l", "Aussen": "Ø 900 x 600", "Ablass": "Kugelhahn d40 bei Z 40"}, grenzen="Maße nach der Zeichnung (Radius 450); Fabrikat offen.", quelle="docs/parts/schlamm_sammelbehaelter.md, data/oasis-soll.json (sludge_1)"))

S["regentank_5m3"] = dict(
    gruppe="Becken und Tanks", titel="Regentank 5 m3 (Platzhalter)", kurz="Stehender PE-Tank fuer 5000 l Regenwasser, erste Wahl der Nachspeisung.",
    gruppen=[("tank", "Tank", "Tank, Dom und Deckel.", ["t_tank", "t_dom", "t_domdeckel"]), ("stutzen", "Stutzen", "Auslauf d25 und Ueberlauf d63.", ["t_auslauf", "t_ueberlauf"])],
    teile=[T("t_tank", "Regentank 5000 l", ["Tank"], "kaufteil", "Speichert das Regenwasser.", ["Ø 1700 x 2300 (Annahme)", "Innen 4,97 m3"], "keine (Handelsteil) [A]", "offen", art="BEH-regentank-5000"),
           T("t_dom", "Domschacht", ["Dom"], "kaufteil", "Zugang zum Tank.", ["Ø 500 x 150"], "keine [A]", "offen"),
           T("t_domdeckel", "Domdeckel", ["Domdeckel"], "kaufteil", "Verschliesst den Dom.", ["Ø 520 x 30"], "keine [A]", "offen"),
           T("t_auslauf", "Auslaufstutzen d25", ["Auslaufstutzen"], "normteil", "Wasser zum Nachspeise-Ventil.", ["Muffe d25 bei Z 150"], "DIN 8063 [A]", "ja"),
           T("t_ueberlauf", "Ueberlaufstutzen d63", ["Ueberlaufstutzen"], "normteil", "Ueberlauf bei vollem Tank.", ["Muffe d63 bei Z 2150"], "DIN 8063 [A]", "nein")],
    desc=dict(ablauf=["Regenwasser fuellt den Tank.", "Das Nachspeise-Ventil holt bei Bedarf Wasser ueber den Auslauf d25.", "Bei vollem Tank laeuft das Wasser ueber den Ueberlauf d63 ab."],
              masse={"Inhalt": "5000 l (innen 4,97 m3)", "Aussen": "Ø 1700 x 2300"}, grenzen="Maße, Lage und Typ sind Annahme (D107); Fundament offen.", quelle="docs/parts/regentank_5m3.md, data/oasis-soll.json (rain)"))

S["permakultur_modul"] = dict(
    gruppe="Becken und Tanks", titel="Permakultur-Modul (Platzhalter)", kurz="Kompostbox und Futterzuchtkiste, die den Schlamm von Hand aufnehmen.",
    gruppen=[("box", "Kompostbox", "Box mit Deckel.", ["t_box", "t_deckel"]), ("zucht", "Futterzucht", "Kiste fuer Wuermer.", ["t_kiste"])],
    teile=[T("t_box", "Kompostbox", ["Kompostbox"], "sonderteil", "Nimmt den Schlamm auf.", ["Fichte 25 mm, 1500 x 525 x 600"], "keine [A]", "nein"),
           T("t_deckel", "Deckel", ["Kompostdeckel"], "sonderteil", "Deckt die Box ab.", ["Fichte 25 mm"], "keine [A]", "nein"),
           T("t_kiste", "Futterzuchtkiste", ["Futterzuchtkiste"], "kaufteil", "Wuermerzucht.", ["PE 800 x 525 x 350"], "keine (Handelsteil) [A]", "nein", art="BEH-futterzuchtkiste")],
    desc=dict(ablauf=["Der Schlamm wird von Hand aus dem Sammelbehaelter eingefuellt.", "Kompost und Wuermer bauen ihn ab.", "Es gibt keinen Rueckweg ins Wasser."],
              masse={"Kompostbox": "1500 x 525 x 600", "Kiste": "800 x 525 x 350"}, grenzen="Platzhalter; Permakultur um den Dom nicht modelliert.", quelle="docs/parts/permakultur_modul.md, data/oasis-soll.json (permakultur)"))

S["tauchpumpe_modul"] = dict(
    gruppe="Pumpen", titel="Tauchpumpen-Modul (Eco Premium 8000, Kandidat)", kurz="Vereinfachter Pumpenkoerper (340 x 280 x 165), Rueckschlagventil d50 und Kabel; Pumpstellen 1 und 2.",
    gruppen=[("pumpe", "Pumpe", "Gehaeuse und Kabel.", ["t_gehaeuse", "t_kabel"]), ("druck", "Druckleitung", "Stutzen und Rueckschlagventil.", ["t_stutzen", "t_rv"])],
    teile=[T("t_gehaeuse", "Pumpengehaeuse", ["Gehaeuse"], "kaufteil", "Pumpt das Wasser.", ["340 x 280 x 165 (Hersteller-Shop, Q)", "8000 l/h, Hmax 4,1 m, Tiefe 4 m (R59)"], "keine (Handelsteil) [A]", "offen", art="PMP-tauchpumpe-oase-8000"),
           T("t_kabel", "Netzkabel", ["Kabel"], "kaufteil", "Versorgt die Pumpe.", ["Ø 9, Ausschnitt 400"], "keine [A]", "nein"),
           T("t_stutzen", "Druckstutzen d50", ["Druckstutzen"], "kaufteil", "Abgang der Pumpe.", ["Ø 50 x 70"], "keine [A]", "offen"),
           T("t_rv", "Rueckschlagventil d50", ["Rueckschlagventil"], "kaufteil", "Haelt die Druckleitung gefuellt (A14).", ["Ø 63 x 110, Muffen d50"], "keine (Handelsteil) [A]", "ja", art="ARM-rueckschlagventil-d50")],
    desc=dict(ablauf=["Die Pumpe saugt unten am Becken an.", "Das Rueckschlagventil haelt die Leitung bei Stillstand gefuellt.", "Pumpstelle 1 hebt 1,15 m in den Vortex, Pumpstelle 2 hebt 1,00 m in den Fischtank."],
              masse={"Gehaeuse": "340 x 280 x 165 mm", "Gesamthoehe": "314 mm bis Port", "Hub": "1,15 m und 1,00 m"}, grenzen="Kennlinie nur aus Qmax/Hmax gerechnet; mit Venturi nicht belegt; Typ Kandidat (R59).", quelle="docs/parts/tauchpumpe_modul.md, data/oasis-soll.json (filterpumpe_1)"))


def werkstoff_zeile(ev_bodies, namen):
    ws = {MAT2W.get(ev_bodies[n]["material"], "?" + str(ev_bodies[n]["material"])) for n in namen}
    assert len(ws) == 1, (namen, ws)
    return ws.pop()


def schreiben(name):
    sp = S[name]
    comp = json.load(open(os.path.join(ROOT, "data", "components", name + ".json"), encoding="utf-8"))
    datei = f"designs/components/{name}.sc"
    ev = sc.evaluate(os.path.join(ROOT, datei))
    B = {b["name"]: b for b in ev["bodies"]}
    teile = []
    for t in sp["teile"]:
        k = t["koerper"]
        masse = sum(B[n]["mass_g"] for n in k)
        bb = B[k[0]]["bbox"]
        box = " x ".join(f"{bb['max'][i] - bb['min'][i]:.1f}" for i in range(3))
        z = dict(id=t["id"], name=t["name"], koerper=k, menge=len(k), typ=t["typ"], werkstoff=werkstoff_zeile(B, k),
                 masse_mm=f"Masse {masse:.1f} g, Einzelkoerper {box} mm (Modell-Bounding-Box)", funktion=t["funktion"], eigenschaften=t["eigenschaften"],
                 norm=t["norm"], norm_konfidenz="angenommen", lebensmittelkontakt=t["lm"], lebensmittelkontakt_konfidenz="angenommen", konfidenz=t["konf"],
                 quelle=f"docs/parts/{name}.md, data/components/{name}.json, data/oasis-soll.json")
        if t["typ"] in ("normteil", "kaufteil"):
            z["bezug"] = bezug(t["art"])
        if t["katalog"]:
            z["katalog"] = t["katalog"]
        if t["art"]:
            z["artikel_hinweis"] = t["art"]
        z["ausnahme"] = t.get("ausnahme", AUSN)
        z["artikel_einheit"] = None
        z["artikel_menge_je_instanz"] = 0
        teile.append(z)
    d = dict(komponente=name, datei=datei, bauteilgruppe=sp["gruppe"], teilenummer=comp["teilenummer"], stand="teiledaten", titel=sp["titel"], kurz=sp["kurz"],
             hinweis="Texte und Maße aus dem Bauteilblatt und den Parametern des Bauteils (U2, N-UNIFY-AUTOBAHN). Maße von Handelsteilen sind Annahme; Europa-Bezug und Lebensmittelnachweis stehen je Teil im Feld bezug (D76, D85), offene Nachweise sind als offen gefuehrt. Katalog und Stueckliste folgen in U8.",
             koerperzahl=len(B), gruppen=[dict(id=g[0], name=g[1], kurz=g[2], teile=g[3]) for g in sp["gruppen"]], teile=teile)
    json.dump(d, open(os.path.join(ROOT, "data", "parts", name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return d


def beschreibung(name):
    """Eintrag fuer data/descriptions.json bauteile (Felder wie die bestehenden Eintraege)."""
    sp, d = S[name], json.load(open(os.path.join(ROOT, "data", "parts", name + ".json"), encoding="utf-8"))
    comp = json.load(open(os.path.join(ROOT, "data", "components", name + ".json"), encoding="utf-8"))
    aufbau = [{"t": g["name"], "p": [t["name"] + (f" ({t['menge']}x)" if t["menge"] > 1 else "") for t in d["teile"] if t["id"] in g["teile"]]} for g in d["gruppen"]]
    return {"match": "^" + name, "titel": sp["titel"], "was": sp["kurz"], "status": "Komponente gebaut und geprueft (U2), noch nicht im Gesamtmodell", "ablauf": sp["desc"]["ablauf"], "aufbau": aufbau,
            "masse": sp["desc"]["masse"], "grenzen": sp["desc"]["grenzen"], "quelle": sp["desc"]["quelle"]}


if __name__ == "__main__":
    namen = sys.argv[1:] or list(S)
    pfad = os.path.join(ROOT, "data", "descriptions.json")
    desc = json.load(open(pfad, encoding="utf-8"))
    for n in namen:
        d = schreiben(n)
        e = beschreibung(n)
        desc["bauteile"] = [x for x in desc["bauteile"] if x.get("match") != e["match"]] + [e]
        print(n, "Koerper", d["koerperzahl"], "Teile", len(d["teile"]))
    open(pfad, "w", encoding="utf-8").write(json.dumps(desc, ensure_ascii=False, indent=2) + chr(10))
