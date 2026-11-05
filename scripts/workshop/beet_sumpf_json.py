"""W37-1 Teil 1: schreibt die Parameter- und Blattdatei data/components/beet_sumpf.json (einmalig; der Generator beet_sumpf.py ergaenzt blatt.ports).
Aufruf: python -X utf8 scripts/workshop/beet_sumpf_json.py"""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def P(w, e, h): return {"wert": w, "einheit": e, "herkunft": h}

R45 = "docs/research/R45-hydraulik-auslegung.md Abschnitt 3"
par = {
    "tank_d": P(800, "mm", f"[E] {R45}: Rundtank PE Oe 0,8 m x 1,0 m, ca. 500 l (r45_sumpf.py); Handelsmass [A] nicht gegengeprueft"),
    "tank_h": P(1000, "mm", f"[E] {R45}"),
    "tank_wall": P(6, "mm", "[A] Wandstaerke PE-Rundtank (kein Datenblatt gelesen)"),
    "tank_floor": P(6, "mm", "[A] Bodenstaerke wie Wand"),
    "oeffnung_d": P(580, "mm", "[A] Domoeffnung oben (Schulterring 110 mm breit), traegt den Schachtaufsatz"),
    "aufsatz_d": P(600, "mm", "[A] Schachtaufsatz PE (Teleskop-/Domschacht wie bei Zisternen), Aussen-Oe"),
    "aufsatz_wall": P(6, "mm", "[A]"),
    "aufsatz_h": P(200, "mm", "[E] Aktualitaetspruefung 05.11. Punkt 6: Einlaufsohle flur-relativ <= -375 (Beetablauf-Achse -290, halbes d50, 1 % auf 6 m [A]); gewaehlt -400 -> Tankboden -1200, Tankoberkante -200, Aufsatz 200 bis Flur"),
    "deckel_d": P(700, "mm", "[A] begehbarer Deckel (Last-Platzhalter), liegt auf dem Aufsatz"),
    "deckel_t": P(40, "mm", "[A]"),
    "zulauf_d": P(50, "mm", "[E] data/leitungsnetz.json Version 3, K14/K30 dn 50 (Blatt nannte d63 aus R45; Netz gilt)"),
    "zulauf_sohle": P(800, "mm", f"[E] {R45}: Einlauf-Rohrsohle 800 mm ueber Tankboden, hoechster Wasserstand darunter"),
    "pumpen": P(2, "", "[A] D81 Annahme E19: zweite Pumpe als Reserve ja; 1 baut eine Pumpe"),
    "pumpe_l": P(300, "mm", "[A] Platzhalter-Quader Teichpumpe 5300 l/h, Fabrikat offen (R45 Frage 3 Nr. 1)"),
    "pumpe_w": P(200, "mm", "[A] Platzhalter"),
    "pumpe_h": P(180, "mm", "[A] Platzhalter"),
    "pumpe_x": P(100, "mm", "[A] Lage Pumpenmitte"),
    "pumpe_dy": P(170, "mm", "[A] Abstand Pumpenmitte von y 0 (bei 2 Pumpen)"),
    "foerder_d": P(40, "mm", f"[E] {R45}: Foerderleitung PVC-U d40 (v 0,94 m/s), K58/K59"),
    "rsv_z": P(300, "mm", "[A] Unterkante Rueckschlagventil d40 (W39, lt_rueckschlagventil_d40) im Steigrohr"),
    "sammel_z": P(1120, "mm", "[A] Achse Sammelrohr d40 der beiden Steigrohre, im Schachtaufsatz"),
    "pegel_aus": P(120, "mm", f"[E] {R45} Pegelhoehen 1"),
    "pegel_ein": P(320, "mm", f"[E] {R45} Pegelhoehen 2"),
    "pegel_alarm": P(620, "mm", f"[E] {R45} Pegelhoehen 3 (Flutsperre K11/K27)"),
    "stange_x": P(-200, "mm", "[A] Schwimmerstange Lage"),
    "stange_d": P(20, "mm", "[A]"),
    "schwimmer_d": P(70, "mm", "[A] Schwimmerschalter Platzhalter"),
    "schwimmer_h": P(60, "mm", "[A]"),
    "entl_d": P(32, "mm", f"[E] {R45}: Entlueftung d32 mit Insektengitter"),
    "kabel_d": P(33, "mm", "[A] Kabelverschraubung M25, Aussen 33"),
}
d = {
    "klasse": "beet_sumpf", "teilenummer": "T92", "revision": "A",
    "beschreibung": "Beet-Sumpf je Linie (L04, R45 Abschnitt 3): eingegrabener PE-Rundtank Oe 800 x 1000 (ca. 500 l) mit Schachtaufsatz 200 mm und begehbarem Deckel; Zulauf d50 der Beetablaeufe bei 800 mm ueber Boden, zwei Teichpumpen (Betrieb + Reserve, E19) mit Rueckschlagventil d40 auf eine Foerderleitung d40, drei Schwimmerschalter (AUS 120, EIN 320, ALARM 620 mm), Entlueftung d32, zwei Kabeldurchfuehrungen (Pumpen/Schwimmer, Ablaufwaechter A+)",
    "quelle_masse": "docs/research/R45-hydraulik-auslegung.md Abschnitt 3 (Bauteil-Skizze, Pegel), data/leitungsnetz.json Version 3 (K14/K30, K58/K59), docs/research/R47-wasserkreislauf-neu.md 4.1/6.6 (Ablaufwaechter), docs/jobs/W37-1-sumpf-schlammfass.md (Aktualitaetspruefung 05.11.)",
    "parameter": par,
    "werkstoff": {"name": "PE (Tank, Aufsatz, Deckel), PVC-U (Leitungen), Pumpen als Platzhalter", "dichte_g_cm3": 0.95, "farbe": "#3b3f44", "herkunft": "[A]; PE schwarz/dunkel lichtdicht (Algen, R45 Abdeckung)"},
    "anzahl": {"soll": "2 (je Linie: beet_sumpf_1, beet_sumpf_2)", "quelle": "data/leitungsnetz.json Knoten beet_sumpf_1/2; Standort setzt die Montage (M10 S4)"},
    "bezugspunkt": "Mitte Tankboden aussen (Z 0), Z hoch; Zulauf -X; Pumpen +X; Schwimmerstange -X. Einbau: Tankboden flur-relativ Z -1200 (Modell Z -800), Deckeloberkante dann flur-relativ +40",
    "herkunft_tabelle": [
        ["Tank Oe 800 x 1000, ca. 500 l", "Oe 800 x 1000", "gerechnet + Annahme", "R45 Abschnitt 3 (r45_sumpf.py: Spitze 2 Beete 168 l + Totvolumen + Hysterese); Handelsmass nicht gegengeprueft", "mittel"],
        ["Pegel AUS / EIN / ALARM", "120 / 320 / 620 mm", "gerechnet", "R45 Abschnitt 3 Pegelhoehen (Oe 0,8 m, 1 cm = 5 l)", "mittel"],
        ["Einlauf-Rohrsohle", "800 mm ueber Tankboden", "gerechnet", "R45 Abschnitt 3 Punkt 4", "mittel"],
        ["Zulauf DN", "d50", "belegt (Netz)", "data/leitungsnetz.json V3 K14/K30 dn 50", "hoch"],
        ["Einbautiefe Tankboden", "flur-relativ -1200", "gerechnet", "Aktualitaetspruefung 05.11. Punkt 6 aus Beet-Matrizen (dome-script.json) und K14 hoehe; Sammlerlaenge 6 m angenommen", "mittel"],
        ["Schachtaufsatz", "Oe 600 x 200", "Annahme", "Folge der Einbautiefe; Handelsteil nicht gegengeprueft", "niedrig"],
        ["Deckel begehbar", "Oe 700 x 40", "Annahme", "R45 Abdeckung; Deckelklasse offen (R45 Frage 3 Nr. 4)", "niedrig"],
        ["Pumpe Teichpumpe 5300 l/h, 60 W, Hmax 2,8 m", "Quader 300 x 200 x 180, Dichte 0,4 (ca. 4 kg)", "Annahme (Mass), belegt nur Haendlerdaten (Leistung)", "R45 Abschnitt 3 Tabelle (Haendlerseiten; ein Beispiel-Fabrikat dort genannt); Kennlinie und Abmessung offen", "niedrig"],
        ["Zweite Pumpe (Reserve)", "2", "Annahme", "D81 Annahme E19", "mittel"],
        ["Rueckschlagventil d40", "L 102, Oe 60", "Annahme (Bibliothek)", "W39 lt_rueckschlagventil_d40 (rsv_geom)", "mittel"],
        ["Foerderleitung", "d40", "gerechnet", "R45 Abschnitt 3 (v 0,94 m/s)", "mittel"],
        ["Schwimmer, Stange", "Oe 70 x 60, Stange Oe 20", "Annahme", "Platzhalter, kein Fabrikat", "niedrig"],
        ["Entlueftung", "d32 mit Gitterkappe", "gerechnet (DN) / Annahme (Kappe)", "R45 Abdeckung", "mittel"],
        ["Kabeldurchfuehrungen", "2 x M25", "Annahme", "R45 (Kabel), R47 4.1 Befund 3 (Ablaufwaechter, A+)", "niedrig"],
    ],
    "blatt": {
        "funktion": "Sammelt das Ablaufwasser der Beete einer Linie (Glockensiphons, K14/K30), weil der Beetablauf unter dem Pool-Spiegel liegt, und pumpt es ueber die Foerderleitung d40 (K58/K59) zurueck zum Ruecklauf. Die Schwimmer schalten die Pumpe (EIN 320, AUS 120 mm) und sperren bei ALARM (620 mm) die Beet-Zufuhr K11/K27. Kein Schwerkraft-Notueberlauf; die zweite Pumpe ist Reserve (E19).",
        "querschnitt": "Tank Oe 800 x 1000, Wand und Boden 6, Domoeffnung oben Oe 580; Schachtaufsatz Oe 600 x 200, Wand 6, auf dem Schulterring; Deckel Oe 700 x 40 auf dem Aufsatz mit vier Durchbruechen (Foerderleitung d40, Entlueftung d32, 2 Kabelverschraubungen M25). Innen: 2 Pumpen-Quader 300 x 200 x 180 auf dem Boden, je Steigrohr d40 mit Rueckschlagventil, Sammelrohr d40 bei Z 1120, Steigrohr zur Deckeldurchfuehrung; Schwimmerstange Oe 20 mit drei Schwimmern.",
        "toleranzen": "Pumpen-Ecken 26 mm vor der Tankwand (Radius 368 gegen 394 innen); Steigrohre und Sammelrohr liegen innerhalb der Domoeffnung und des Aufsatzes (Radius <= 215 gegen 290/294); Einlauf-Sohle 180 mm ueber ALARM.",
        "verbindungen": [
            "Tank und Aufsatz: Aufsatz steht auf dem Schulterring, Dichtung/Verschweissung nicht modelliert [A]",
            "Deckel aufgelegt, verschraubt oder verriegelt (nicht modelliert), Dichtung lichtdicht [A]",
            "Zulauf: Tankverbinder d50 durch die Wand (Dichtung nicht modelliert); Leitungen PVC-U geklebt",
            "Pumpen stehen frei auf dem Boden; Steigrohre ueber Verschraubung an den Pumpenstutzen (nicht modelliert)",
        ],
        "abweichung": "Keine OBJ-Vorgabe; Bauteil nach R45 Abschnitt 3 (Bauteil-Skizze), Einbautiefe nach Aktualitaetspruefung 05.11. (Beet-Tausch).",
        "montage": [
            "Grube Oe 1,0 m, Tiefe 1,25 m (Tankboden flur-relativ -1200 plus 50 Sandbett); Tank waagerecht setzen, lagenweise verfuellen",
            "Schachtaufsatz aufsetzen, Zulauf d50 mit >= 1 % Gefaelle zum Sumpf anschliessen (Sohle 800 ueber Tankboden = flur-relativ -400)",
            "Pumpen einsetzen, Steigrohre mit Rueckschlagventil, Sammelrohr und Deckeldurchfuehrung kleben; Schwimmerstange einhaengen, Hoehen 120/320/620 einstellen",
            "Kabel durch die Verschraubungen, Deckel auflegen und sichern",
        ],
        "werkzeug": "Spaten/Bagger, Wasserwaage, Lochsaege fuer Tankverbinder, PVC-Kleber, Schluesselsatz",
        "stueckliste": [
            "T92 Beet-Sumpf je Linie: 1 PE-Rundtank Oe 800 x 1000 (ca. 500 l), 1 Schachtaufsatz Oe 600 x 200, 1 begehbarer Deckel Oe 700, 1 Tankverbinder d50, 2 Teichpumpen 5300 l/h (60 W, Hmax 2,8 m; Fabrikat offen), 2 Rueckschlagventile d40, Rohr d40 ca. 2,2 m mit Formstuecken, 3 Schwimmerschalter, 1 Stange, 1 Entlueftung d32 mit Insektengitter, 2 Kabelverschraubungen M25",
            "Leistung: 60 W je Pumpe im Betrieb (Laufanteil 90 %, Mittel 54 W je Linie, R45); Reservepumpe 0 W im Normalbetrieb [A]; beide Linien 108 bis 120 W",
        ],
        "teileliste": [
            ["PE-Rundtank 500 l mit Domoeffnung", "Oe 800 x 1000", "offen (Zisternen-/Pumpenschacht-Handel, z. B. Hersteller in DE)", "offen [A]"],
            ["Schachtaufsatz Oe 600", "200 mm", "offen", "offen [A]"],
            ["Teichpumpe 5300 l/h, 60 W", "Hmax 2,8 m", "Haendlerangabe in R45 (OBI/topratgeber24, nur Beispiel)", "offen, Datenblatt nicht gelesen"],
            ["Rueckschlagventil PVC-U d40", "Klebemuffe", "offen (N-BESCHAFFUNG)", "offen [A]"],
            ["Schwimmerschalter (3)", "Kabel", "offen", "offen [A]"],
        ],
        "lokal": "Tank und Aufsatz aus dem Zisternen-/Kleinklaeranlagen-Handel; Deckel alternativ aus PE-Platte 20 mm mit Rippen (Kunststoffhandel).",
        "massen_getrennt": [],
        "gewicht_gefuellt": "Bis ALARM 620 mm ca. 300 l Wasser, bis Tankoberkante ca. 485 l [E, Dichte 1]; eingegraben, Auftrieb bei leerem Tank und hohem Grundwasser nicht gerechnet [A]",
        "pruefung": ["scripts/workshop/check_beet_sumpf.py (Ergebnis renders/components/beet_sumpf/check.txt): Tank Mass, Volumen bis ALARM und bis Oberkante gegen R45, Pegelhoehen, Ports (Lage und Richtung), Pumpenzahl, Interferenz 0"],
        "offen": [
            "Statische Foerderhoehe steigt mit der Einbautiefe auf 1,40 bis 1,60 m (R45: 1,0 bis 1,5 m); Arbeitspunkt der Pumpe nachrechnen (r45_sumpf.py, Planer/Orchestrator)",
            "Sammlerlaenge 6 m und 1 % Gefaelle angenommen; die echte Trasse legt M10 S4 fest; bei laengerem Sammler Aufsatz hoeher (Parameter aufsatz_h)",
            "Pumpenfabrikat, Kennlinie und Abmessung offen (R45 Frage 3 Nr. 1); Quader ist Platzhalter",
            "Auftriebssicherung des leeren Tanks bei hohem Grundwasser nicht geprueft",
            "Deckelklasse (begehbar) und Schachtfabrikat offen (R45 Frage 3 Nr. 4)",
        ],
        "kritiker": "Kein Pruefer-Lauf (Pruefpunkte fuer den Pruefer im Blatt W37-1).",
    },
}
out = os.path.join(ROOT, "data", "components", "beet_sumpf.json")
json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out)
