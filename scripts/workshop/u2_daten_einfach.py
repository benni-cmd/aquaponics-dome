"""Schreibt data/components/{schlamm_sammelbehaelter,regentank_5m3,permakultur_modul,tauchpumpe_modul}.json (U2): Parameter mit Herkunft und Text-Block 'blatt' fuer das Bauteilblatt.
Aufruf: python -X utf8 scripts/workshop/u2_daten_einfach.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

Q, A, E = "[Q] ", "[A] ", "[E] "
BL = dict(teileliste=[], kritiker="offen (Pruefer P-Pruef)", abweichung="Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).")


def P(w, einheit, h):
    return {"wert": w, "einheit": einheit, "herkunft": h}


KOMP = {}

KOMP["schlamm_sammelbehaelter"] = dict(
    teilenummer="T106",
    beschreibung="Schlamm-Sammelbehaelter 350 l (U2, D104, Quelle A11): oberirdischer runder PE-Behaelter Ø 900 x 600 mit Deckel, Einlaufstutzen d40 (Zulauf vom Vortex per Schwerkraft), Entlueftung und Ablasshahn d40 von Hand; ausserhalb des Wasserkreislaufs, Schlamm geht von Hand zum Permakultur-Modul",
    quelle_masse="data/oasis-soll.json (sludge_1: Sammelbehaelter 350 l, Ablasshahn von Hand, Stufe 1 nicht festgelegt, Zeichnung Radius 450 mm); docs/research/R61-oasis-wasserkreislauf.md Abschnitt 4 (O5); docs/decisions.md D104",
    parameter={
        "aussen_d": P(900, "mm", Q + "Zeichnung sludge_1: Radius 450 mm (Fussabdruck der Lage-Probe U1); Behaelter Ø 900 aussen"),
        "wand": P(10, "mm", A + "Wand und Boden PE 10 mm"),
        "innen_h": P(575, "mm", E + "350 l = pi x 440^2 x 575 mm (Innen-Ø 880): 349,7 l; Hoehe so gewaehlt, dass der Zulauf unter dem Schlammstutzen des Vortex liegt"),
        "deckel_t": P(15, "mm", A + "Deckel PE 15 mm, aufgesetzt"),
        "einlauf_l": P(60, "mm", A + "Einlaufstutzen d40 (Klebemuffe, Aussen 46,25 laut leitung.py) 60 hoch auf dem Deckel"),
        "ent_d": P(26, "mm", A + "Entlueftungsstutzen Ø 26 x 30 auf dem Deckel (Bohrung 10)"),
        "auslauf_z": P(40, "mm", A + "Achse des Ablaufs 40 mm ueber der Behaelter-Unterkante (Restmenge unter dem Ablauf rund 18 l)"),
        "hahn_d": P(52, "mm", A + "Kugelhahn d40 PVC-U, Gehaeuse Ø 52 x 70 (Platzhalter, Handelsmaß offen)"),
        "vortex_schlammstutzen_z": P(697, "mm", E + "Vortex-Schlammstutzen: Podest 577 + Kugelhahn des tank_klein bei z 120 (data/parts/tank_klein.json 'kugelhahn z 120 bis 160'); der Behaelter muss tiefer stehen, damit der Schlamm abwaerts laeuft"),
    },
    werkstoff={"name": "PE-HD (Behaelter, Deckel), PVC-U (Stutzen, Hahn)", "dichte_g_cm3": 0.95, "farbe": "#d9d4c0", "herkunft": "[A] PE-Fass oder Rundbehaelter; Wasserkontakt Schlamm, nicht Fisch (D85: Nachweis offen)"},
    anzahl={"soll": "2 (je Linie einer)", "quelle": "data/oasis-soll.json sludge_1, sludge_2"},
    bezugspunkt="Mitte der Standflaeche in X und Y, Z 0 = Fussboden (Behaelter-Unterkante); Ablasshahn bei +X, Einlauf in der Deckelmitte",
    herkunft=[["Inhalt 350 l", "Innen Ø 880 x 575", "E", "Quelle: 350 l (sludge_1); Rechnung pi x 0,44^2 x 0,575 m", "hoch"],
              ["Ø 900 aussen", "Zeichnung Radius 450", "Q", "data/oasis-soll.json sludge_1 radius_mm 450", "mittel"],
              ["oberirdisch, Ablasshahn von Hand", "Hahn d40 bei Z 40", "Q/A", "Quelle A11, D104; Hahnmaße Platzhalter", "mittel"]],
    blatt=dict(
        funktion="Nimmt den Feststoffschlamm des Vortex (und eventuell des Biofilters) auf: Zulauf per Schwerkraft ueber den Einlaufstutzen, Ablass nur von Hand ueber den Kugelhahn d40; steht oberirdisch ausserhalb des Wasserkreislaufs, der Schlamm geht von Hand an das Permakultur-Modul, kein Rueckweg (Quelle A11, D104, Designprinzip 8). Steht tiefer als der Schlammstutzen des Vortex.",
        querschnitt="PE-Behaelter aussen Ø 900, Wand und Boden 10, innen Ø 880 x 575 (350 l); Deckel 15; Einlaufstutzen d40 (60 hoch, Muffe d40) mittig; Entlueftung Ø 26 x 30; Ablaufrohr d40 durch die Wand bei Z 40 mit Kugelhahn Ø 52 x 70 und Hebel.",
        toleranzen="Rohr und Hahn stossen an; Rohr ragt 10 mm in den Behaelter. Restmenge unter dem Ablauf rund 18 l.",
        ports=[["Einlauf (Muffe d40)", "PVC-U d40, Tiefe 26", "x 0, y 0, Z 600 bis 660", "Oeffnung oben; Rohr d40 vom Schlammstutzen des Vortex"], ["Ablass (Kugelhahn d40)", "PVC-U d40", "x 454 bis 524, z 40", "Hahn von Hand, Ablass in Eimer oder Karre"]],
        verbindungen=["Einlaufstutzen mit dem Deckel verklebt oder verschweisst", "Ablaufrohr durch die Wand mit Dichtung, Hahn auf das Rohr geklebt", "Deckel lose aufgesetzt"],
        montage=["Behaelter auf ebenen Fussboden stellen, Standort tiefer als der Schlammstutzen des Vortex", "Rohr d40 vom Vortex zum Einlaufstutzen mit Gefaelle fuehren", "Hahn schliessen, Deckel aufsetzen, Entlueftung offen lassen"],
        werkzeug="Lochsaege 40 mm, PVC-Kleber, Wasserwaage",
        pruefung=["python -X utf8 scripts/workshop/check_schlamm_sammelbehaelter.py"],
        offen=["Fabrikat und Wanddicke des PE-Behaelters offen (Ø 900 x 600 ist Platzhalter nach der Zeichnung); Bezug Europa siehe data/beschaffung/", "Zulauf-Gefaelle ab Vortex-Schlammstutzen: Rohrlaenge und Gefaelle gehoeren zu U6", "Geruch und Schlammverfestigung (Entlueftung, Reinigung) nicht gerechnet"], **BL))

KOMP["regentank_5m3"] = dict(
    teilenummer="T107",
    beschreibung="Regenwassertank 5 m3 (Platzhalter, U2, D107, Quelle A8): stehender runder PE-Tank Ø 1700 x 2300 mit Domschacht und Domdeckel, Auslaufstutzen d25 (zum Nachspeise-Ventil) und Ueberlaufstutzen d63; erste Wahl der Nachspeisung, ausserhalb der Kuppel an der Technikseite; Maße Annahme",
    quelle_masse="data/oasis-soll.json (rain: Regenwassertank 5 m3, Salzgehalt < 12 mg/l, freies Chlor 0; Hoehe nicht festgelegt; Zeichnung Rechteck 1625 x 500 schematisch); docs/decisions.md D107",
    parameter={
        "aussen_d": P(1700, "mm", A + "Platzhalter: stehender PE-Tank Ø 1700 (die Zeichnung zeigt nur ein Rechteck 1625 x 500, schematisch A16)"),
        "wand": P(15, "mm", A + "Wand, Boden und Deckel PE 15 mm"),
        "h": P(2300, "mm", E + "5 m3 = pi x 0,835^2 x 2,27 m = 4,97 m3 (Innen-Ø 1670, Innenhoehe 2270)"),
        "dom_d": P(500, "mm", A + "Domschacht Ø 500 aussen, Bohrung Ø 440"),
        "dom_h": P(150, "mm", A + "Domschacht 150 hoch"),
        "domdeckel_d": P(520, "mm", A + "Domdeckel Ø 520 x 30"),
        "auslauf_z": P(150, "mm", A + "Auslauf d25 (Klebemuffe, Aussen 32,25) 150 mm ueber dem Boden (Bodensatz bleibt im Tank)"),
        "ueberlauf_z": P(2150, "mm", A + "Ueberlauf d63 (Aussen 72,15) 150 mm unter dem Rand"),
        "stutzen_l": P(100, "mm", A + "Stutzen ragen 100 mm aus der Wand"),
        "volumen_l": P(5000, "", Q + "Quelle: Tank-Kapazitaet 5,0 m3 (5000 Liter)"),
    },
    werkstoff={"name": "PE-HD (Tank, Dom, Deckel), PVC-U (Stutzen)", "dichte_g_cm3": 0.95, "farbe": "#d9d4c0", "herkunft": "[A] Platzhalter; Regenwasser mit Fischkontakt (Nachspeisung): Tankwerkstoff lebensmittelecht, Nachweis offen (D85)"},
    anzahl={"soll": "1 (Regenwassertank)", "quelle": "data/oasis-soll.json rain (anzahl 1)"},
    bezugspunkt="Mitte der Standflaeche in X und Y, Z 0 = Fussboden; Stutzen bei +X, Dom oben mittig",
    herkunft=[["5 m3", "Innen Ø 1670 x 2270 = 4,97 m3", "E/Q", "Quelle rain 5,0 m3; Rechnung pi x 0,835^2 x 2,27", "hoch"],
              ["Maße Ø 1700 x 2300", "Platzhalter", "A", "Quelle legt Hoehe und Lage nicht fest (rain: stufe_status ohne Hoehenangabe)", "niedrig"]],
    blatt=dict(
        funktion="Sammelt Regenwasser (salz- und chlorfrei, erste Wahl der Nachspeisung) und gibt es ueber den Auslaufstutzen d25 an das Nachspeise-Ventil am Fischtank ab; der Ueberlaufstutzen d63 leitet bei Fuellung zum Versickern oder in die Permakultur. Einfacher Platzhalter ausserhalb der Kuppel (Quelle A16, D107, Designprinzip 4 Ausnahme).",
        querschnitt="PE-Tank aussen Ø 1700 x 2300, Wand 15; Innen 1670 x 2270; Domschacht Ø 500 x 150 mit Bohrung Ø 440; Domdeckel Ø 520 x 30; Auslaufstutzen d25 bei Z 150, Ueberlaufstutzen d63 bei Z 2150.",
        toleranzen="Platzhalter: Maße aus Annahme; Stutzen durch die Wand in Passbohrung.",
        ports=[["Auslauf (Muffe d25)", "PVC-U d25, Tiefe 19", "x 850 bis 950, z 150", "waagerecht zum Nachspeise-Ventil (Rohr d25, Eingang A)"], ["Ueberlauf (Muffe d63)", "PVC-U d63, Tiefe 37,5", "x 850 bis 950, z 2150", "waagerecht, Wasser zum Versickern"]],
        verbindungen=["Stutzen mit Dichtung durch die Wand", "Domdeckel lose, gegen Kinder gesichert"],
        montage=["Tank auf tragfaehigen, ebenen Grund stellen (5 t Last)", "Zulauf vom Kuppeldach (Regenrinne) an den Dom, Auslauf d25 zum Nachspeise-Ventil", "Ueberlauf ableiten"],
        werkzeug="Wasserwaage, Lochsaege",
        pruefung=["python -X utf8 scripts/workshop/check_regentank_5m3.py"],
        offen=["Maße, Lage und Typ (stehend/liegend) vom Orchestrator angenommen, weil die Quelle sie nicht festlegt (D107); Fabrikat und Bezug Europa siehe data/beschaffung/", "Fundament und Statik fuer 5 t Wasser: N-STATIK", "Regenwasserfuehrung von der Kuppelhaut (Rinne, Filter) ist nicht modelliert"], **BL))

KOMP["permakultur_modul"] = dict(
    teilenummer="T111",
    beschreibung="Permakultur-Modul (Platzhalter, U2, D104, D107, Quelle permakultur): Kompostbox aus Holz 1500 x 525 x 600 mit Deckel und Futterzuchtkiste aus PE 800 x 525 x 350 fuer Wuermer; nimmt den Schlamm von Hand auf, kein Rueckweg ins Wasser; ausserhalb der Kuppel; Maße Annahme",
    quelle_masse="data/oasis-soll.json (permakultur: Schlamm-Senke, Zeichnung Rechteck 1500 x 525 mm, Hoehe nicht festgelegt; Beschreibung 'Permakultur um den Dom und Futterzucht (Wuermer, Kompostbox, Soldatenfliegen)'); docs/decisions.md D104, D107",
    parameter={
        "kompost_l": P(1500, "mm", Q + "Zeichnung permakultur: Rechteck 1500 mm breit"),
        "kompost_b": P(525, "mm", Q + "Zeichnung permakultur: Rechteck 525 mm tief"),
        "kompost_h": P(600, "mm", A + "Hoehe Kompostbox (Quelle: Hoehe nicht festgelegt)"),
        "holz_t": P(25, "mm", A + "Fichte 25 mm (Wand, Boden, Deckel)"),
        "kiste_l": P(800, "mm", A + "Futterzuchtkiste PE 800 x 525 x 350 (Wuermer)"),
        "kiste_h": P(350, "mm", A + "Hoehe der Futterzuchtkiste"),
        "kiste_wand": P(6, "mm", A + "PE-Kiste Wand und Boden 6 mm"),
        "abstand": P(50, "mm", A + "Abstand der Kiste neben der Kompostbox"),
    },
    werkstoff={"name": "Fichtenholz (Kompostbox), PE (Futterzuchtkiste)", "dichte_g_cm3": 0.45, "farbe": "#c8a878", "herkunft": "[A] einfacher Platzhalter; kein Kontakt zu Wasser, Fisch oder Pflanzen des Kreislaufs (D85 greift nicht)"},
    anzahl={"soll": "1 (Permakultur-Modul)", "quelle": "data/oasis-soll.json permakultur (anzahl 1)"},
    bezugspunkt="Mitte der Kompostbox in X und Y, Z 0 = Fussboden; Futterzuchtkiste bei +X neben der Kompostbox",
    herkunft=[["Rechteck 1500 x 525", "Kompostbox", "Q", "data/oasis-soll.json permakultur zeichnung_rect", "mittel"], ["Hoehen und Futterzuchtkiste", "Annahme", "A", "Quelle legt Hoehe nicht fest; D104/D107: einfacher Platzhalter", "niedrig"]],
    blatt=dict(
        funktion="Nimmt den Schlamm aus den Sammelbehaeltern von Hand auf (Kompost, Wuermer, Futterzucht); keine Rueckleitung ins Wasser, getrennt vom Lebendfutterbecken (Quelle). Einfacher Platzhalter fuer die Schlamm-Senke ausserhalb der Kuppel; die Permakultur um den Dom ist nicht modelliert.",
        querschnitt="Kompostbox Fichte 25 mm, aussen 1500 x 525 x 600, offen, mit Deckel 25 mm; Futterzuchtkiste PE 800 x 525 x 350, Wand 6 mm.",
        toleranzen="Platzhalter; Kiste steht 50 mm neben der Box.",
        ports=[["Schlammannahme", "offen von oben", "Oberkante Kompostbox Z 600", "Schlamm von Hand einfuellen"]],
        verbindungen=["Holz verschraubt (Normteile nicht modelliert)"],
        montage=["Box auf ebenem Grund stellen", "Schlamm aus dem Sammelbehaelter von Hand einfuellen, mit Laub abdecken"],
        werkzeug="Schaufel, Karre",
        pruefung=["python -X utf8 scripts/workshop/check_permakultur_modul.py"],
        offen=["Maße und Aufbau sind Annahme (Quelle nennt nur Rechteck und Stichworte); Permakultur um den Dom, Soldatenfliegen und Wuermer-Besatz nicht modelliert", "Eigener Baustein ausserhalb der zehn Namen des Auftrags: das Soll-Bauteil `permakultur` hat sonst keine Komponente (D112 Zusatz)"], **BL))

KOMP["tauchpumpe_modul"] = dict(
    teilenummer="T110",
    beschreibung="Tauchpumpen-Modul (U2, D92, D102, A14): vereinfachter Koerper der Oase AquaMax Eco Premium 8000 (Kandidat nach R59, Typ nicht bestaetigt) mit Ansaugkorb, Druckstutzen, Rueckschlagventil d50 in der Druckleitung und Netzkabel; steht auf dem Boden von Fischtank (Pumpstelle 1, Hub 1,15 m) oder Sumpf (Pumpstelle 2, Hub 1,00 m); Pumpenzahl und Leistung offen (A3)",
    quelle_masse="data/oasis-soll.json (filterpumpe_1: Rueckschlagventil in der Druckleitung A14; hauptpumpe_1; Zeichnung Pumpe Radius 137,5 mm); docs/research/R59-tauchpumpe.md (Eco Premium 8000: 8000 l/h, Hmax 4,1 m [A], 65 W, Eintauchtiefe 4 m); docs/decisions.md D92, D102, D106",
    parameter={
        "korb_d": P(275, "mm", Q + "Zeichnung Pumpe: Radius 137,5 mm = Ø 275 (Lage-Probe U1 nutzt Ø 275 als Fussabdruck)"),
        "korb_h": P(50, "mm", A + "Ansaugkorb mit Sieb, Standflaeche Z 0"),
        "geh_d": P(230, "mm", A + "Pumpengehaeuse Ø 230 (Maß nicht aus dem Datenblatt gelesen)"),
        "geh_h": P(190, "mm", A + "Pumpengehaeuse 190 hoch ueber dem Korb (Gesamthoehe bis Gehaeuse-Oberkante 240)"),
        "stutzen_l": P(70, "mm", A + "Druckstutzen Ø 50 (Schlauchtuelle auf Klebeadapter) 70 hoch, 31 mm davon im Rueckschlagventil"),
        "rv_d": P(63, "mm", A + "Rueckschlagventil PVC-U d50 (Klappe oder Kugel), Gehaeuse Ø 63 x 110"),
        "rv_l": P(110, "mm", A + "Baulaenge Rueckschlagventil mit Muffe d50 oben und unten"),
        "kabel_d": P(9, "mm", A + "Netzkabel Ø 9"),
        "kabel_l": P(400, "mm", A + "Kabelstueck im Modell (Ausschnitt)"),
        "qmax_l_min": P(133.3, "", E + "8000 l/h aus R59 (Herstellerangabe Eco Premium 8000)"),
        "hmax_m": P(4.1, "", A + "R59: 4,1 m, Zuordnung der Hmax-Spalte im Handbuch unsicher"),
        "tiefe_max_mm": P(4000, "mm", Q + "R59: wasserdicht bis 4 m (Handbuch der Baureihe)"),
    },
    werkstoff={"name": "Kunststoffgehaeuse (Pumpe), PP (Korb, Stutzen), PVC-U (Rueckschlagventil)", "dichte_g_cm3": 1.5, "farbe": "#3a5f9a", "herkunft": "[A] Platzhalterkoerper; Gehaeusewerkstoff und Lebensmittelnachweis der Teichpumpe nicht belegt (R59, D85)"},
    anzahl={"soll": "4 (2 Pumpstelle 1 im Fischtank, 2 Pumpstelle 2 im Sumpf)", "quelle": "docs/decisions.md D102; data/oasis-soll.json filterpumpe_1/_2, hauptpumpe_1/_2"},
    bezugspunkt="Mitte der Standflaeche (Unterkante Ansaugkorb) in X und Y, Z 0 = Boden des Beckens; Druckleitung d50 senkrecht nach oben (Port bei Z 389), Kabel +X",
    herkunft=[["Eco Premium 8000 als Kandidat", "Körper Ø 230 x 190, Korb Ø 275", "A", "R59 Empfehlung (bedingt); Kennlinie nur aus Qmax/Hmax gerechnet, Nachweis offen", "niedrig"],
              ["Rueckschlagventil in der Druckleitung", "d50 PVC-U", "Q", "A14, filterpumpe_1.t3 und hauptpumpe_1.t2", "mittel"]],
    blatt=dict(
        funktion="Hebt Wasser von unten nach oben: Pumpstelle 1 saugt im Fischtank und hebt 1,15 m (Wsp 750 zu Vortex 1900), Pumpstelle 2 saugt im Sumpf und hebt 1,00 m (Wsp -250 zu 750) durch den Venturi-Belueffter in den Fischtank. Das Rueckschlagventil in der Druckleitung haelt die Leitung bei Stillstand gefuellt (A14). Typ bleibt Kandidat (R59/D92). Die Rechnung der Foerderleistung im Check zeigt: Pumpstelle 1 trifft 110 l/min nur nach den optimistischen Kennlinienformen, Pumpstelle 2 mit Venturi nicht; Nachweis offen.",
        querschnitt="Ansaugkorb PP Ø 275 x 50 (Z 0 bis 50); Gehaeuse Ø 230 x 190 (Z 50 bis 240); Druckstutzen Ø 50 x 70 (Z 240 bis 310); Rueckschlagventil Ø 63 x 110 mit Muffe d50 unten (nimmt den Stutzen) und oben (Z 279 bis 389); Kabel Ø 9 x 400 seitlich bei Z 120.",
        toleranzen="Platzhalterkoerper; Pumpeninneres nicht modelliert; Stutzen steckt 31 mm im Ventil (Beruehrung).",
        ports=[["Druckleitung (Muffe d50)", "PVC-U d50, Tiefe 31", "x 0, y 0, z 389", "Oeffnung zeigt +Z; Rohr d50 nach oben (D106)"], ["Strom", "Netzkabel Ø 9", "x 115 bis 515, z 120", "an die Steuerung (nicht modelliert)"]],
        verbindungen=["Druckleitung d50 in die Muffe oben kleben", "Pumpe steht auf Sockel oder Boden, Kabel zum Schaltschrank"],
        montage=["Pumpe auf den Boden (Fischtank) oder den Pumpensockel (Sumpf) stellen", "Rueckschlagventil in die Druckleitung d50, Rohr nach oben fuehren", "Kabel ueber den Rand zum Schaltschrank; Probelauf mit Pegelkontrolle"],
        werkzeug="Rohrschneider, PVC-Kleber",
        pruefung=["python -X utf8 scripts/workshop/check_tauchpumpe_modul.py"],
        offen=["Foerderleistung: Kennlinie nur aus Qmax/Hmax gerechnet (R59), Herstellerkennlinie und zweite Quelle fehlen; Pumpstelle 2 mit Venturi nach der Rechnung nicht belegt", "Lebensmittel- und Fischvertraeglichkeit der Teichpumpe (D85) nicht belegt; Rueckfall Aquaforte EC-10000 (R59)", "Im Sumpf liegt das Gehaeuse bei Soll-Pegel -250 mit Sockel 30 teilweise trocken (Oberkante -230): flachere Pumpe oder Sockel anpassen, offen", "Anzahl und Leistung wie in der Quelle offen (A3)"], **BL))


def schreiben(name, k):
    d = {"klasse": name, "teilenummer": k["teilenummer"], "revision": "A", "beschreibung": k["beschreibung"], "quelle_masse": k["quelle_masse"], "parameter": k["parameter"],
         "werkstoff": k["werkstoff"], "anzahl": k["anzahl"], "bezugspunkt": k["bezugspunkt"], "herkunft_tabelle": k["herkunft"], "blatt": k["blatt"]}
    pfad = os.path.join(sc.ROOT, "data", "components", name + ".json")
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben", pfad)


if __name__ == "__main__":
    for n, k in KOMP.items():
        schreiben(n, k)
