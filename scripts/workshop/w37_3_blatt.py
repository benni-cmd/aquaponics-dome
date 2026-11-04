"""Blatt-Texte, Herkunftstabellen und Viewer-Beschreibungen der fuenf W37-3-Teile (von w37_3_json.py eingelesen).
Zahlen (Geschwindigkeiten, Summen) werden hier gerechnet, Masse und Volumen misst partsheet.py aus den .sc-Dateien."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import leitung as L
from w37_3_json import AB6, AB4

def v_area(dmm): return math.pi / 4 * dmm ** 2
def v_ms(q_lmin, dmm): return q_lmin * 1e6 / 60 / v_area(dmm) / 1000

BORE40 = 40 - 2 * L.wall_p(40)                      # 36,2
DNN = {20: 15, 25: 20, 40: 32}

def ABB(ds):
    return ds - 2 * L.wall_p(ds) - (0.2 if ds >= 40 else 0.0)

LUFT_NICHT = "Luft nicht freigegeben (Seite nennt Wasser, PN16), Oeffnungsdruck bei 130 l/min ungeprueft"
TL_RSV = ["Rueckschlagventil d40, d25, d20 (Klebemuffe)", "d40 / d25 / d20, PVC-U",
          "Baenninger Art. 75328, 75326, 75325 (schwarte-shop, DE), 15,67 bis 35,93 EUR [Q-Treffer, R53 Abschnitt 5, aus dem Blatt W37-3 uebernommen]; zweite Quelle (Bevo) Zuordnung ungeprueft",
          "nur eine Quelle; " + LUFT_NICHT + "; Ersatz fuer kleine Leitungen Luftschlauch-Rueckschlagventile (Tetra CV4 u. a. [Q-Treffer R53]), fuer d40 keine belegt"]
TL_T = ["T-Stueck 40x25x40 und 40x20x40, Reduzierung 40x25 und 40x20", "PVC-U Klebemuffen",
        "Bevo Profec (NL); schwarte-shop (DE); Weinmann-Schanz (DE) Art. 93 049 64 Reduktion 40 x 25 [Q-Treffer R52, Seite beim Abruf 404]; Vanmarcke GF 40 x 25 (BE) [Q R52]",
        "beschaffbar (zwei Quellen fuer 40 x 25 nach R52); 40 x 20 nur ueber Reduzierungen aus der Bibliothek, Artikel offen"]
TL_KH = ["Kugelhahn d40 / d25 / d20", "PVC-U Klebemuffe, Hebel",
         "d40: Bevo VDL Typ EIL d40 DN32 (NL) und Profec Typ 2000 [Q-Treffer R52]; d25, d20: Georg Fischer Typ 546 (RS-Seiten, AT/DE/NL) [Q-Treffer], Zuordnung d25/d20 ungeprueft",
         "d40 beschaffbar (R52); d25 und d20 offen bis Datenblatt"]
TL_KAPPE = ["Endkappe d40", "PVC-U Klebekappe", "Katalog offen, N-BESCHAFFUNG (W47); W39 baute nur Kappen d20 und d50", "offen"]

def d_text(n):
    if n == 6:
        return ("Teilt die Druckluft beider Geblaese-Pumpen (N+1) auf: Pool (d40, K44), Biofilter 1 und 2 (d25, K45/K46), Drittbecken (d20, K49), Zweitbecken (d20, K51) und die optionalen Absetzer (d20, K47/K48). "
                "Sammler d40 mit Klebemuffe am Einlauf, sechs Zapfen nach oben (je Abgang spaeter Rueckschlagventil und Kugelhahn), Ende geschlossen. Formstueck-Verteiler nach dem Muster lt_verteiler_d50 (W36). "
                "Gilt in jeder Kreislaufvariante (E20), die Luft laeuft getrennt vom Wasserumlauf")
    return ("Pool-Verteiler am Becken: nimmt die Pool-Luft (K44, Planwert 130 l/min, Spitze 205) in einer Muffe d40 auf und gibt sie ueber vier Zapfen d25 (je 33 l/min) an vier Scheibenbelueftungsteile weiter. "
            "Formstueck-Verteiler nach dem Muster lt_verteiler_d50 (W36). Gilt in jeder Kreislaufvariante (E20)")

def blatt_verteiler(name):
    n = 6 if name.endswith("6") else 4
    ab = AB6 if n == 6 else AB4
    of = L.od_f(40); top = of / 2 + 50
    xs = [75 + 120 * k for k in range(n)]
    Lg = xs[-1] + 25 + 10
    ports = [["A Einlauf (Muffe)", "PVC-U d40 (DN32), Klebemuffe, Einstecktiefe 26", "x 0, y 0, z 0 (Mitte der Oeffnung)",
              "Oeffnung zeigt -X; " + ("Rohr d40 vom Geblaese (zwei Pumpen ueber Rueckschlagventil, T-Stueck d25 und Reduzierungen d25/d32, d32/d40 aus der Bibliothek)" if n == 6 else "Rohr d40 vom Hauptverteiler (K44, Pool-Leitung)")]]
    for k, (a, x) in enumerate(zip(ab, xs), 1):
        ports.append([f"Abgang {k} {a[0]} ({a[2]})", f"PVC-U d{a[1]} (DN{DNN[a[1]]}), Zapfen, Aussen-Ø {a[1] - (0.25 if a[1] >= 40 else 0):g}, Bohrung {ABB(a[1]):.1f}", f"x {x}, y 0, z {top:g}", "zeigt +Z; Rohr oder Ventil wird aufgeklebt (Zapfen steckt in die Muffe)"])
    q = []
    if n == 4:
        for k in range(1, 5):
            q.append(f"Strom Abgang {k}: 33 l/min im Innen-Ø {ABB(25):.1f} = {v_ms(33, ABB(25)):.2f} m/s [E]")
        q.append(f"Summe der Abgangsstroeme 4 x 33 = 132 l/min gegen Planwert 130 l/min (Abweichung {abs(132 - 130) / 130 * 100:.1f} Prozent, unter 2 Prozent) [E]")
        q.append(f"Sammler Innen-Ø {BORE40:.1f}: 130 l/min = {v_ms(130, BORE40):.2f} m/s; Spitze 205 l/min = {v_ms(205, BORE40):.2f} m/s (R45: d40 bei 200 l/min 3,2 m/s)")
    else:
        q.append("Einlauf: Pool 130 + Drittbecken 2 + Zweitbecken 5 = 137 l/min [E, Planwerte] plus Reserve fuer Biofilter 1/2 (K45/K46) und Absetzer (K47/K48); deren Menge ist OFFEN (Traegerhersteller, K1). Die Pumpe traegt bei 26 kPa grob 176 l/min [E R53, Vorbehalt]: Reserve 39 l/min")
        q.append(f"Sammler Innen-Ø {BORE40:.1f}: 137 l/min = {v_ms(137, BORE40):.2f} m/s; Pool-Abgang d40 (Bohrung {ABB(40):.1f}) 130 l/min = {v_ms(130, ABB(40)):.2f} m/s; Spitze 205 l/min = {v_ms(205, BORE40):.2f} m/s")
        q.append(f"Drittbecken d20 (Bohrung {ABB(20):.1f}) 2 l/min = {v_ms(2, ABB(20)):.2f} m/s; Zweitbecken d20 5 l/min = {v_ms(5, ABB(20)):.2f} m/s [E]")
    if n == 6:
        teil = [TL_T, TL_RSV, TL_KH, TL_KAPPE]
        sl = ["Sammler d40 aus Handelsteilen (L21): 1 T-Stueck 40x40x40 (Pool), 2 T-Stuecke 40x25x40 (Biofilter), 3 T-Stuecke 40x20x40 (Drittbecken, Zweitbecken, Absetzer), 5 Rohrstuecke d40 zwischen den T-Stuecken, 1 Endkappe d40",
              "je Abgang 1 Kugelhahn und 1 Rueckschlagventil (Pool d40; Biofilter d25; Drittbecken, Zweitbecken, Absetzer d20) aus der Bibliothek (lt_kugelhahn_d*, lt_rueckschlagventil_d* aus W39)",
              "Das Modell ist der Formstueck-Verteiler des W36-Musters (ein Koerper); der Nachbau aus T-Stuecken ist die Beschaffungsvariante (Teilung 120 groesser als die T-Stueck-Laenge 100)"]
        montage = ["Hauptverteiler am Geblaese im Schaltschrankbereich aufstellen (Standort E13 OFFEN); Rohr d40 aus der Geblaese-Baugruppe (T-Stueck d25 beider Pumpen, Reduzierungen d25/d32 und d32/d40) in Muffe A kleben",
                   "Je Abgang Rueckschlagventil (Fluss von A nach B, nach oben) und Kugelhahn aufkleben, dann Rohr zum Verbraucher: Pool d40 (K44 zum Pool-Verteiler), Biofilter 1/2 d25 (K45/K46), Drittbecken d20 (K49), Zweitbecken d20 (K51), Absetzer d20 (K47/K48, optional)",
                   "Jeden Abgang einzeln mit dem Hahn abgleichen und den Pool-Zulauf messen"]
        offen = ["Biofilter-Luft K45/K46 und Absetzer K47/K48: Menge OFFEN (Traegerhersteller, R45 Abschnitt 4); Einlaufstrom im Blatt nur 137 l/min plus Reserve",
                 "Rueckschlagventile: " + LUFT_NICHT,
                 "Kennlinie der Pumpe bei 26 kPa OFFEN (R53): Spitze 205 l/min nur mit beiden Pumpen",
                 "Standort des Hauptverteilers im Schaltschrankbereich OFFEN (E13)",
                 "Kreislaufvariante E20 beruehrt die Luft nicht (Variantenbefund, Luft laeuft getrennt vom Wasserumlauf)"]
    else:
        teil = [["T-Stueck 40x25x40 (4 Stueck), Reduzierung 40x25", "PVC-U Klebemuffen (Teilung 120, T-Stueck 40 ist 100 lang)", TL_T[2], TL_T[3]], TL_KAPPE]
        sl = ["Sammler d40 aus Handelsteilen (L21): 4 T-Stuecke 40x25x40, Rohrstuecke d40 zwischen den T-Stuecken, 1 Endkappe d40",
              "Je Abgang ein Rohr d25 zu einem Scheibenbelueftungsteil (luft_scheibenbelueftung, 4 Stueck); Einzelabsperrung je Scheibe nicht im Auftrag (Montage/Planer)"]
        montage = ["Pool-Verteiler am Beckenrand befestigen (Befestigung Montage); Rohr d40 (K44) in Muffe A kleben",
                   "Jeden Abgang d25 mit einem Rohr zu je einem Scheibenbelueftungsteil verbinden; die Scheiben (Ø 270) brauchen mehr Abstand als die Teilung 120: die Rohre fuehren auseinander",
                   "Luft einschalten und das Blasenbild kontrollieren"]
        offen = ["Menge je Scheibe 33 l/min ist Annahme (130 geteilt durch 4); Kennlinie der Scheibe (Druckverlust, Blasenbild) OFFEN",
                 "Befestigung am Beckenrand und Wegfuehrung der vier Rohre: Montage",
                 "Einzelabsperrung je Scheibe: nicht im Auftrag",
                 "Rueckschlagventil im Zulauf: bei Pumpenstillstand sperrt das Ventil der Geblaese-Baugruppe (Schleife ueber dem Spiegel); " + LUFT_NICHT]
    return {
        "blatt": {
            "funktion": d_text(n),
            "querschnitt": f"Sammler Aussen {of:g} (Formstueck d40: 40 + 2 x 4), Innen-Ø {BORE40:.1f} (Wand 1,9), Muffe A d40 Tiefe 26; Zapfen Aussen-Ø = d (Pool-Abgang 39,75), Zapfenende {top:g} ueber der Achse; Teilung 120, Laenge {Lg:g}, Ende B mit 10 mm Endkappe geschlossen.",
            "toleranzen": "Der Pool-Abgang d40 des Hauptverteilers ist 0,25 mm duenner, seine Bohrung 0,2 mm kleiner als der Sammler (sonst braucht der Kernel 60 s je Schnitt, W37-2); fuer die Montage bedeutungslos (Handelsteile)." if n == 6 else "Kein Abgang hat den Durchmesser des Sammlers; keine Kernel-Korrektur noetig.",
            "ports": ports,
            "verbindungen": q,
            "abweichung": "Kein OBJ-Bestand (Luftverteiler fehlte, L06).",
            "montage": montage,
            "werkzeug": "Rohrschneider, Klebstoff PVC, Entgrater",
            "stueckliste": sl,
            "lokal": "Handelsteile (T-Stuecke, Reduzierungen, Kappe) aus dem Katalog; Eigenbau aus Rohr d40 mit Anbohrung und aufgeschweissten Abgaengen nur als Notloesung.",
            "massen_getrennt": [],
            "gewicht_gefuellt": "Luft fuehrend, keine Fuellmasse; Masse leer siehe Messung",
            "pruefung": ["scripts/workshop/check_luft_verteiler.py " + name + " (Ergebnis renders/components/" + name + "/check.txt): Koerper, Aussen-Ø, Laenge, Muffe A, Abgaenge (Zahl, Ø, Bohrung, Port-Stirnflaechen) " + ("und DN je Abgang gegen das Netz K44 bis K51" if n == 6 else "und Strom je Abgang, Summe 132 gegen 130") + ", Geschwindigkeit im Sammler, Interferenz 0"],
            "offen": offen,
            "kritiker": "Kein Pruefer-Lauf (Auftrag W37-3: Selbstcheck; gebuendelter Pruefer W37-2/W37-3 folgt).",
            "teileliste": teil,
        },
        "herkunft_tabelle": [
            ["Hauptleitung d40 / Sammler", "d40, Innen-Ø 36,2", "E", "Netz K44 (R45 Abschnitt 4): d40 bei 200 l/min 3,2 m/s", "hoch"],
            ["Abgaenge", f"{n} Zapfen: " + ", ".join(f"d{a[1]} ({a[2]})" for a in ab), "E" if n == 6 else "A", "Netz K44 bis K51 (Hauptverteiler); Pool-Verteiler 4 Abgaenge d25 aus dem Auftrag W37-3 [A]", "hoch" if n == 6 else "mittel"],
            ["Teilung 120, Zapfenueberstand 50, Endkappe 10", "wie lt_verteiler_d50", "A", "docs/parts/leitungsteile.md Verteiler d50 (W36)", "mittel"],
            ["Strom je Abgang", "Pool 130 (Spitze 205), Dritt 2, Zweit 5, Biofilter und Absetzer offen" if n == 6 else "4 x 33 = 132 l/min", "E/A", "R45 Abschnitt 4; Netz K49 2 l/min; Zweitbecken 5 [A]", "mittel"],
            ["Handelsteile (T, Reduzierung, Hahn, Rueckschlagventil)", "Europa-Teileliste im Blatt", "Q-Treffer", "R52, R53, Auftrag W37-3 Europa-Teileliste", "niedrig"],
        ],
    }

# ------------------------------------------------------------------ Scheibe
def blatt_scheibe():
    ks = [["Scheibenbelueftung 270 EPDM, Anschluss 3/4 Zoll bzw. d25 (Klebe/Gewinde)", "Membran Ø 270",
           "Jaeger JetFlex HD 270 (DE) [Q-Treffer R53]; Disque diffuseur 270 EPDM, Ref. DD-0270-EPDM-HCS (FR) [Q R53]; Datenblatt Jaeger nicht lesbar",
           "beschaffbar (schwach): zwei Herkuenfte, je eine Quelle; Datenblatt und Anschluss ungeprueft"]]
    return {
        "blatt": {
            "funktion": "Gibt die Luft des Pool-Verteilers als feine Blasen ins Pool-Wasser ab: EPDM-Membran auf einem Tragteller, darunter ein Stuetzfuss mit Anschlussstutzen d25 nach unten. Vier Stueck im Pool, je einer an einem Abgang des Pool-Verteilers (K44). Parameter d (Standard 270) und pipe_d bilden die Luftstein-Variante fuer das Drittbecken (K49, d20) ohne eigenes Bauteil ab. Gilt in jeder Kreislaufvariante (E20)",
            "querschnitt": "Anschlussstutzen d25 x 40 mit Luftkanal Ø 16, Stuetzfuss Ø 70 x 50 mit Luftkanal Ø 16 (Kanal im Tragteller nicht modelliert), Tragteller Ø 250 x 20, EPDM-Membran Ø 270 x 6 (nicht geschlitzt modelliert); Gesamthoehe 116.",
            "toleranzen": "Handelsmass-Platzhalter; Membran-Schlitze, Kanaele im Tragteller und Gewinde nicht modelliert; Stuetzfuss steht auf der Rohrleitung (Zuleitung kommt von unten, Bogen unter dem Fuss: Montage).",
            "ports": [["A Luft-Anschluss (Zapfen)", "PVC-U d25 (DN20), Zapfen, Aussen-Ø 25, Luftkanal Ø 16", "x 0, y 0, z 0 (Mitte der Stirnflaeche)", "Oeffnung zeigt -Z (nach unten); Rohr d25 vom Pool-Verteiler wird aufgesteckt oder als Muffe ueber den Zapfen geklebt"]],
            "verbindungen": ["Port A: Rohr d25 vom Abgang des Pool-Verteilers (luftverteiler_4)", "Fuss auf dem Beckenboden: Befestigung (Gewicht, Auftrieb) nicht modelliert (Montage)"],
            "abweichung": "Kein OBJ-Bestand.",
            "montage": ["Scheibe auf dem Beckenboden am vorgesehenen Platz absetzen (Abstand der vier Scheiben mindestens 270 mm; Verteilung im Pool Montage)", "Rohr d25 vom Abgang des Pool-Verteilers an Port A anschliessen", "Luft einschalten, Blasenbild pruefen; Fuss gegen Auftrieb beschweren"],
            "werkzeug": "Rohrschneider, Klebstoff PVC",
            "stueckliste": ["4 Scheibenbelueftungsteile EPDM 270 mit Anschluss d25 (Pool); 1 Luftstein klein (Variante d 100, pipe_d 20) im Drittbecken (K49)", "4 Beschwerungen oder Halter (Montage)"],
            "lokal": "Handelsteil (Teichbelueftung, EPDM-Scheibe 215 bis 270 mm).",
            "massen_getrennt": [],
            "gewicht_gefuellt": "Luft fuehrend; EPDM-Membran schwimmt nicht, der Fuss muss beschwert werden (Montage)",
            "pruefung": ["scripts/workshop/check_luft_verteiler.py luft_scheibenbelueftung (Ergebnis renders/components/luft_scheibenbelueftung/check.txt): vier Koerper, Stutzen-, Fuss-, Teller- und Membran-Maße, Stapelhoehe 116, Port A, Volumen Membran und Stutzen gegen Rechnung, Interferenz 0"],
            "offen": ["Hersteller-Maß und Kennlinie (Druckverlust, Luftmenge je Scheibe) OFFEN, Katalog N-BESCHAFFUNG (W47)", "Biofilter-Rohr- und Plattenbelueftungsteile: nur Platzhalter-Hinweis (Menge nach Traegerhersteller, K1), nicht modelliert", "Anschluss d25 vs. 3/4 Zoll Gewinde der Handelsscheibe: Uebergang offen"],
            "kritiker": "Kein Pruefer-Lauf (Auftrag W37-3: Selbstcheck; gebuendelter Pruefer W37-2/W37-3 folgt).",
            "teileliste": ks,
        },
        "herkunft_tabelle": [
            ["Membran-Ø 270", "270 (Parameter d, 215 bis 270)", "A", "Auftrag W37-3 Teil 3; R53 (JetFlex HD 270, Disque diffuseur 270) [Q-Treffer]", "niedrig"],
            ["Anschluss d25 nach unten", "Zapfen Ø 25, Kanal Ø 16", "A", "Auftrag W37-3 Teil 3 (d25 senkrecht nach unten)", "mittel"],
            ["Stuetzfuss, Tragteller, Membran-Dicke", "Ø 70 x 50, Ø 250 x 20, 6 mm", "A", "Annahme, Handelsmass nicht gelesen", "niedrig"],
            ["Luftstein-Variante Drittbecken", "d 100, pipe_d 20", "A", "Netz K49 (d20, 2 l/min)", "niedrig"],
        ],
    }

# ------------------------------------------------------------------ Geblaese
def blatt_geblaese():
    tl = [["Linear-Membranpumpe 200 l/min", "Klasse 200 l/min bei mindestens 26 kPa, 100 bis 250 W, 42 bis 48 dB",
           "Hiblow HP-200: Hiblow France S.A.S. und Spain S.L., Katalog 2015 gelesen [Q R53], Haendler eBay.de [Q-Treffer]; Secoh JDK-S-200: BIBUS (HU/NL) [Q R53] und tanks.ie (IE, SKU 0022090, 372,70 EUR netto) [Q R53]",
           "beschaffbar als Geraet (Secoh: zwei europaeische Haendler; Hiblow: Hersteller-Niederlassungen); Kennlinie bei 26 kPa OFFEN, Fortschreibung 176 l/min [E, Vorbehalt]; Typ NICHT gewaehlt"],
          TL_RSV[:1] + ["d20, PVC-U Klebemuffe"] + TL_RSV[2:],
          ["Rohr d20 PVC-U (Schleife, Austritt)", "d20 x 1,8", "Katalog offen, N-BESCHAFFUNG (W47)", "offen"],
          ["Reduzierung d25/d20 am Austritt", "PVC-U Klebemuffen", "Bevo Profec (NL), schwarte-shop (DE), Artikel d25/d20 nicht geoeffnet [A]", "offen bis Artikel; Bibliotheksteil lt_reduzierung_d25_d20 vorhanden"]]
    return {
        "blatt": {
            "funktion": "Eine Luftpumpe samt Luftleitung: die Linear-Membranpumpe (Platzhalterquader) blaest durch einen Stutzen d20, die Leitung steigt senkrecht auf Z 710 ueber den hoechsten Wasserspiegel (Pool-Rand Z 650 plus 60, Spiegel Z 515), biegt waagerecht ab und fuehrt durch ein Rueckschlagventil d20 zum Luftaustritt. Zwei Stueck (N+1: eine laeuft, die zweite ist Reserve; die Spitze 205 l/min braucht beide). Die Schleife ueber dem Spiegel ist der Hauptschutz gegen Rueckfluss von Wasser in die Pumpe, das Ventil die zweite Sperre. Gilt in jeder Kreislaufvariante (E20): Luft laeuft getrennt vom Wasserumlauf, Luftausfall ist der harte Termin (0,8 bis 1,2 h bis 3 mg/l, R45)",
            "querschnitt": "Pumpe 240 x 180 x 230 auf vier Gummifuessen Ø 40 x 15; Stutzen d20 x 1,8 (40 lang) oben; Rohrschleife d20 mit Biegeradius 80, senkrechter Schenkel bis Z 710 (Mitte), waagerecht 150; Rueckschlagventil d20 (Gehaeuse Ø 39, Laenge 82); Austrittsrohr 100. Netzkabel Ø 8 an der Rueckseite (-Y).",
            "toleranzen": "Rohre stossen stumpf an das Rueckschlagventil (Muffentiefe 16 nicht modelliert); Pumpe als Vollquader, Dichte so gesetzt, dass die Pumpe 10,0 kg wiegt ([A], Beispiel Secoh JDK-S-200 laut BIBUS).",
            "ports": [["Luftaustritt (Zapfen)", "PVC-U d20 (DN15), Zapfen, Austrittsrohr", "x 412, y 0, z 710 (Mitte der Stirnflaeche)", "Oeffnung zeigt +X; weiter ueber Reduzierung d20 auf d25 und T-Stueck d25 beider Pumpen in Port A des Hauptverteilers (luftverteiler_6)"],
                      ["Stromanschluss (Kabelende)", "230 V, 1 Ader-Stueck laut Netz (204 W Fischwasser-Belueftung)", "x -80, y -190, z 130", "Stirnflaeche zeigt -Y; Kabel zur Kabeleinfuehrung DN100 des Schaltschranks (schrank_einfuehrung); Kabelrechnung Orchestrator, hier nicht berechnet"]],
            "verbindungen": ["Port Luftaustritt: Rohr d20 zur Reduzierung d20/d25, dann T-Stueck d25 zu Luftverteiler 6 (Hauptverteiler Port A)", "Befestigung: Pumpe auf Gummifuessen im Schaltschrankbereich (Standort E13 OFFEN); Netzkabel 230 V zur Einfuehrung", "Schleife: Scheitel (Rohrachse) Z 710, Reserve 195 mm ueber dem Spiegel Z 515 und 60 mm ueber dem Pool-Rand Z 650"],
            "abweichung": "Kein OBJ-Bestand (Gebläse fehlte, L06).".replace("ä", "ae"),
            "montage": ["Pumpe im Schaltschrankbereich auf ebener Flaeche aufstellen (Standort E13 OFFEN); Aufstellflaeche gilt als Z 0 im Bauteil, bei anderer Hoehe die Schleife anpassen: Scheitel absolut auf Z 710 halten", "Stutzen d20 mit der Rohrschleife verkleben, Rueckschlagventil in Flussrichtung (nach +X) einkleben, Austrittsrohr anschliessen", "Zwei Baugruppen nebeneinander; beide Austritte ueber T-Stueck d25 und Reduzierung auf d40 in den Hauptverteiler (Port A) fuehren", "Netzkabel mit Reserve zur Kabeleinfuehrung DN100 fuehren (230-V-Stamm)"],
            "werkzeug": "Rohrschneider, Heissluft zum Biegen (oder Formbogen aus der Bibliothek), Klebstoff PVC",
            "stueckliste": ["2 Linear-Membranpumpen der Klasse 200 l/min bei mindestens 26 kPa (Typ nicht gewaehlt)", "2 Rueckschlagventile d20", "2 Rohrschleifen d20 (Rohr d20, Biegung R80) mit Austrittsrohr", "2 Reduzierungen d25/d20 und 1 T-Stueck d25 zum Hauptverteiler"],
            "lokal": "Handelsteil (Pumpe); Schleife aus Rohr d20 oder Formbogen.",
            "massen_getrennt": [],
            "gewicht_gefuellt": "Luft fuehrend; Pumpe 10 kg [A, Beispiel]",
            "pruefung": ["scripts/workshop/check_geblaese_luft.py (Ergebnis renders/components/geblaese_luft/check.txt): 10 Koerper, Pumpe 240 x 180 x 230 und 10 kg, Fuesse auf Z 0, Schleife Rohrachse Z 710 (Reserve 195 ueber Spiegel, +60 ueber Pool-Rand), Volumen der Schleife nach Pappus, Rueckschlagventil, Stoss-Kontakte, Ports (Luftaustritt +X, Strom -Y), Interferenz 0"],
            "offen": ["Pumpentyp NICHT gewaehlt: Kennlinie bei 26 kPa OFFEN (R53: Hiblow HP-200 200 l/min nur bei 20 kPa, Fortschreibung 176 l/min bei 26 kPa [E, Vorbehalt]); DEINE HANDLUNG (Ben): Kennlinie bei BIBUS, Hiblow France oder Nitto Kohki Europe anfragen", "Spitze 205 l/min traegt nur eine Pumpe nicht: N+1 faellt bei Parallellauf weg (Auslegungsfrage Ben/Planung)", "Rueckschlagventil: " + LUFT_NICHT + "; Regel Schleife ueber dem Spiegel zweite Quelle nur teilweise (R53 Abschnitt 5), Hoehe Z 710 bleibt [A]", "Notstromkonzept fuer die Pumpen OFFEN (Ben/Orchestrator; R45 Abschnitt 4)", "Standort Schaltschrankbereich OFFEN (E13)"],
            "kritiker": "Kein Pruefer-Lauf (Auftrag W37-3: Selbstcheck; gebuendelter Pruefer W37-2/W37-3 folgt).",
            "teileliste": tl,
        },
        "herkunft_tabelle": [
            ["Pumpenklasse", "200 l/min bei mindestens 26 kPa, N+1", "E", "R45 Abschnitt 4 Empfehlung 3 und 4; Planwert 130, Spitze 205 l/min", "mittel"],
            ["Pumpenmasse", "240 x 180 x 230, 10 kg", "A", "Beispielreihe Secoh JDK-S-200 (BIBUS: 240 x 180 x 230,5, 10,0 kg [Q R53]); Typ nicht gewaehlt", "niedrig"],
            ["Kennlinie bei 26 kPa", "176 l/min (Fortschreibung)", "E", "R53 Abschnitt 4: 200 - 20 x (260-200)/50, nur Fortschreibung der Secoh-Tabelle; Hiblow HP-200 200 l/min bei 20 kPa, Bereich bis 35,3 kPa [Q]", "niedrig"],
            ["Schleife ueber dem Spiegel", "Rohrachse Z 710", "E", "R45 Empfehlung 7, params.json pool_rim 650 + 60 (wie Schwimmerventil); layout pool2.water_z 515 (nur gelesen)", "mittel"],
            ["Rueckschlagventil d20", "Laenge 82, Gehaeuse Ø 39", "A", "Muster lt_rueckschlagventil_d20 (W39); Katalog offen", "niedrig"],
            ["Leistung", "204 W (Netz-Kabeleintrag)", "Q", "data/leitungsnetz.json kabel schaltschrank -> geblaese_fisch (nur gelesen, nicht berechnet)", "mittel"],
        ],
    }

# ------------------------------------------------------------------ Schrank
def blatt_schrank():
    tl = [["Kabelschutzrohr 110 mm (DN100)", "AD 110, Innen 94 (Fraenkische)", "Fraenkische Kabuflex S NW 110, Art. 0000185796, 25,46 EUR (DE) [Q-Treffer, Blatt W37-3]", "nur eine Quelle; Aussen-Ø 110, Innen 94: Bauteilmass AD 110 passt; Innen-Ø der Bibliothek 103,6"],
          ["Kabelschutzrohr 50 mm (DN50)", "AD 50", "Fraenkische Kabuflex R plus 50, Art. 19210050 (DE) [Q-Treffer], mehrere im Preisvergleich", "beschaffbar (mehrere Haendler im Preisvergleich); Ring zu 50 m"],
          ["Einfuehrungsplatte / Schrankboden", "800 x 500 x 3", "Rittal SZ 8800.100 (DE) [Q-Treffer, PDF nicht lesbar]", "offen; Schrankserie und Breite (800 x 500 x 1200 [A]) vor der Wahl klaeren"],
          ["Kabeleinfuehrung mit Dichtung (Flansch, Gegenmutter)", "DN100 und DN50", "Katalog offen, N-BESCHAFFUNG (W47); Bibliotheksteile lt_kabeleinfuehrung_dn100/dn50 (W39)", "offen"]]
    return {
        "blatt": {
            "funktion": "Fuehrt die Kabel unterirdisch in den Schaltschrank: eine Einfuehrungsplatte im Schrankboden (800 x 500, Blech 3 mm) nimmt zwei Kabeleinfuehrungen auf, DN100 fuer den 230-V-Stamm (Pumpen, Gebläse) und DN50 fuer den Signal-Stamm (Sensoren). Darunter laeuft je ein Leerrohr-Bogen 90 Grad nach aussen (DN100 nach -X, DN50 nach +X) in die Erde. Die Achsen sind 300 mm auseinander (freier Abstand der Muffen 210,5 mm gegen 200 mm EMV). Nur das Bauteil: Standort des Schranks OFFEN (E13), Kabelzahl und Fuellgrad OFFEN (E20)".replace("Gebläse", "Geblaese"),
            "querschnitt": "Boden 800 x 500 x 3 (Unterkante Z 0) mit zwei Loechern (DN100: Ø 130 bei X -150; DN50: Ø 63 bei X +150); Kabeleinfuehrungen W39: Dichtung unter dem Boden, Gegenmutter auf dem Boden, Gewindehals 15 ueber der Unterkante; Leerrohr-Bogen DN100 (R 500) und DN50 (R 300) mit Ende B in der Muffe der Einfuehrung (Stoss, Z -9). Wandstummel 2 x 100 umlaufend (nur fuer die Interferenzpruefung).",
            "toleranzen": "Leerrohr-Ende B stoesst an den Muffen-Anschlag (Einstecktiefe voll); Loch gleich Halsdurchmesser (kein Spiel modelliert); Dichtung Auflage ohne Pressung.",
            "ports": [["Leerrohr DN100 (Muffe A, 230 V)", "PVC-U DN100 (AD 110), Muffe", "x -734, y 0, z -593 (Mitte der Oeffnung)", "Oeffnung zeigt -X (unterflur, Z bis -654); das Leerrohr (lt_leerrohr_dn100, glattes Ende) wird eingesteckt"],
                      ["Leerrohr DN50 (Muffe A, Signal)", "PVC-U DN50 (AD 50), Muffe", "x 510, y 0, z -369 (Mitte der Oeffnung)", "Oeffnung zeigt +X (unterflur, Z bis -397)"],
                      ["Kabel DN100 in den Schrank", "Kabeldurchgang Innen-Ø 103,6", "x -150, y 0, z 15", "Oeffnung zeigt +Z (nach oben in den Schrank)"],
                      ["Kabel DN50 in den Schrank", "Kabeldurchgang Innen-Ø 46,4", "x 150, y 0, z 15", "Oeffnung zeigt +Z (nach oben in den Schrank)"]],
            "verbindungen": ["Schrankboden: Bodenblech gegen die Schrankwand (Wandstummel) nur Pruefhilfe; echter Schrank siehe schaltschrank.sc (von gen_dome.py erzeugt, hier nicht angefasst)", "Kabeleinfuehrung: Hals durch den Bodenausschnitt, Dichtung unter dem Boden, Gegenmutter oben", "Leerrohr: Bogen B in der Muffe der Einfuehrung, Bogen A nimmt das Leerrohr auf (Abzweige nur mit Zugdose, W39)"],
            "abweichung": "Kein OBJ-Bestand. Der Schaltschrank selbst ist weiter schaltschrank.sc (gen_dome.py, 'neben den Vorbau' D62); die Einfuehrung ist ein eigenes Bauteil mit lokalen Koordinaten.",
            "montage": ["Standort des Schranks klaeren (E13) und erst dann die Einfuehrung mit ihrem Nullpunkt dort setzen; die Platte ersetzt im Montagemodell den Schrankboden des Standorts", "Leerrohr-Boegen unterflur einbauen: DN50 bis Z -397, DN100 bis Z -654 relativ zum Schrankboden (R 500 des Bogens; Plan Z -100 bis -400 nur mit kleinerem Bogen oder zwei 45-Grad-Boegen)", "Kabeleinfuehrungen im Boden verschrauben, Leerrohre einstecken, 230 V und Signal in getrennte Stamm legen (200 mm Abstand)"],
            "werkzeug": "Stufenbohrer oder Lochsaege fuer die Ausschnitte, Leerrohr-Schneider, Klebstoff PVC",
            "stueckliste": ["1 Einfuehrungsplatte 800 x 500 x 3 mit zwei Ausschnitten (Boden des Schaltschranks)", "1 Kabeleinfuehrung DN100 und 1 Kabeleinfuehrung DN50 (W39: lt_kabeleinfuehrung_dn100, _dn50)", "1 Leerrohr-Bogen 90 Grad DN100 und 1 DN50 (W36: lt_leerrohr_bogen90_dn100, _dn50)", "Gebläse-Strom 204 W je Pumpe und 8 Pumpenkabel: Hinweis fuer die Kabelrechnung des Orchestrators, hier nicht berechnet".replace("Gebläse", "Geblaese")],
            "lokal": "Handelsteile; Einfuehrungsplatte als Blech nach Mass.",
            "massen_getrennt": [],
            "gewicht_gefuellt": "keine Fuellung; Masse leer siehe Messung (Stahlblech Platzhalter)",
            "pruefung": ["scripts/workshop/check_schrank_einfuehrung.py (Ergebnis renders/components/schrank_einfuehrung/check.txt): Boden gegen params.json (cab_x, cab_y), beide Einfuehrungen mit Loch, Dichtung und Mutter, Achsabstand 300 und EMV-Abstand 210,5 mm, Leerrohr-Enden, Ports, Interferenz 0 inklusive Schrankwand; schaltschrank.sc und gen_dome.py unveraendert"],
            "offen": ["OFFEN (E13): Standort des Schaltschranks (Ben); gen_dome.py setzt ihn heute neben den Vorbau (D62), Az -85 / r 5750 ist nur Kabelrechnung", "OFFEN (E20): Kabelzahl und Fuellgrad je Stamm (A+: Durchfluss-/Pegelwaechter, 2 Sensoren; B und C: Booster bzw. Ring-Pumpen, 548 W bzw. 503 W gegen 430 W in A; Entscheidung Ben 05.11.)", "OFFEN (D75, geparkt): Tauchpumpen im Subtank beruehren nur die Kabelzahl", "DN100-Bogen R 500 liegt tiefer (Z -654) als die Plantiefe -400 (Plan nannte Z -100 bis -400): Entscheidung Montage/Planer, kleinerer Bogen oder zwei 45-Grad-Boegen", "Einfuehrungsplatte Handelsartikel (Rittal SZ 8800.100) und Schrankserie offen (N-BESCHAFFUNG W47)"],
            "kritiker": "Kein Pruefer-Lauf (Auftrag W37-3: Selbstcheck; gebuendelter Pruefer W37-2/W37-3 folgt).",
            "teileliste": tl,
        },
        "herkunft_tabelle": [
            ["Boden 800 x 500", "800 x 500 x 3", "E/A", "data/params.json cab_x 800, cab_y 500 (ref-5 geschaetzt, nur gelesen); Blech 3 mm [A]", "niedrig"],
            ["Einfuehrungen DN100 und DN50", "aus W39", "E", "docs/parts/leitungsteile.md Ergaenzung W39 (lt_kabeleinfuehrung); Loch = Halsdurchmesser", "mittel"],
            ["Leerrohr-Boegen", "R 500 und R 300", "E", "docs/parts/leitungsteile.md W36 (lt_leerrohr_bogen90_dn*)", "mittel"],
            ["Abstand 230 V gegen Signal", "Achsen 300, Muffen 210,5", "A", "Plan Abschnitt 4 Regel 9 und Auftrag W37-3 (mindestens 200 mm)", "mittel"],
            ["Standort Schrank", "nicht enthalten", "offen", "OFFEN (E13)", "-"],
            ["Kabelzahl und Fuellgrad", "nicht enthalten", "offen", "OFFEN (E20)", "-"],
        ],
    }

# ------------------------------------------------------------------ Viewer-Beschreibungen (data/descriptions.json, Umlaute erlaubt)
DESC = [
    {"match": "^luftverteiler_6", "titel": "Luft-Hauptverteiler (6-fach)",
     "was": "Teilt die Druckluft der Gebläse auf Pool, beide Biofilter, Drittbecken, Zweitbecken und Absetzer auf.",
     "status": "gebaut (Werkstatt W37-3), Prüfung 34/34; Handelsteile (Hahn, Rückschlagventil) Katalog offen; gilt in jeder Kreislaufvariante",
     "ablauf": ["Das Rohr d40 aus der Gebläse-Baugruppe steckt in die Muffe am Einlauf.",
                "Sechs Abgänge nach oben: Pool (d40, 130 l/min, Spitze 205), Biofilter 1 und 2 (d25), Drittbecken, Zweitbecken und Absetzer (je d20).",
                "Jeder Abgang bekommt später ein Rückschlagventil und einen Kugelhahn; das Ende ist geschlossen."],
     "aufbau": [{"t": "Sammler", "p": ["Formstück d40, 48 mm außen, Länge 710", "Einlauf als Klebemuffe d40"]},
                {"t": "Abgänge", "p": ["6 Zapfen, 50 mm Überstand, Teilung 120", "Platz für Hähne und Rückschlagventile ohne Kollision"]}],
     "masse": {"Leergewicht": "0,82 kg (PVC-U)", "Einlauf": "137 l/min (Pool 130, Drittbecken 2, Zweitbecken 5) plus Biofilter und Absetzer offen", "Geschwindigkeit": "2,2 m/s im Sammler bei 137 l/min (Spitze 205 l/min: 3,3 m/s)"},
     "grenzen": "Menge für Biofilter und Absetzer, Öffnungsdruck der Rückschlagventile für Luft und die Pumpen-Kennlinie bei 26 kPa sind offen.",
     "quelle": "docs/parts/luftverteiler_6.md, docs/research/R45-hydraulik-auslegung.md Abschnitt 4"},
    {"match": "^luftverteiler_4", "titel": "Pool-Luftverteiler (4-fach)",
     "was": "Verteilt die Pool-Luft auf vier Scheibenbelüftungsteile.",
     "status": "gebaut (Werkstatt W37-3), Prüfung 28/28; gilt in jeder Kreislaufvariante",
     "ablauf": ["Die Pool-Leitung d40 (K44, Planwert 130 l/min) steckt in die Muffe am Einlauf.", "Vier Abgänge d25 mit je 33 l/min gehen an die vier Scheiben; das Ende ist geschlossen."],
     "aufbau": [{"t": "Sammler", "p": ["Formstück d40, 48 mm außen, Länge 470", "Einlauf als Klebemuffe d40"]}, {"t": "Abgänge", "p": ["4 Zapfen d25, Teilung 120"]}],
     "masse": {"Leergewicht": "0,55 kg (PVC-U)", "Summe der Abgänge": "132 l/min gegen Planwert 130 (1,5 %)", "Geschwindigkeit": "1,5 m/s je Abgang, 2,1 m/s im Sammler"},
     "grenzen": "33 l/min je Abgang ist eine Annahme (130 geteilt durch 4); Befestigung am Beckenrand ist Montage.",
     "quelle": "docs/parts/luftverteiler_4.md, docs/research/R45-hydraulik-auslegung.md Abschnitt 4"},
    {"match": "^luft_scheibenbelueftung", "titel": "Scheibenbelüftungsteil (Pool)",
     "was": "Gibt die Luft als feine Blasen ins Pool-Wasser ab; vier Stück am Pool-Verteiler.",
     "status": "gebaut (Werkstatt W37-3), Prüfung 15/15; Handelsmaße als Platzhalter, Fabrikat offen",
     "ablauf": ["Die Luft kommt über das Rohr d25 von unten in den Stützfuß.", "Durch den Tragteller drückt sie sich durch die EPDM-Membran (Ø 270) und steigt als feine Blasen auf."],
     "aufbau": [{"t": "Teile", "p": ["Anschlussstutzen d25", "Stützfuß Ø 70 × 50", "Tragteller Ø 250", "EPDM-Membran Ø 270 × 6"]}],
     "masse": {"Höhe": "116 mm", "Membran": "Ø 270 (Parameter d, auch kleiner als Luftstein-Variante für das Drittbecken)", "Masse": "ca. 1,5 kg"},
     "grenzen": "Membran-Schlitze, Hersteller-Kennlinie und der Anschluss d25 gegen 3/4 Zoll der Handelsscheibe sind offen.",
     "quelle": "docs/parts/luft_scheibenbelueftung.md, docs/research/R53-europa-frischwasser-luft.md"},
    {"match": "^geblaese", "titel": "Gebläse-Baugruppe Luft (N+1)",
     "was": "Eine Luftpumpe mit Luftleitung über den höchsten Wasserspiegel; zwei Stück, eine läuft, die zweite ist Reserve.",
     "status": "gebaut (Werkstatt W37-3), Prüfung 26/26; Pumpentyp nicht gewählt, Kennlinie bei 26 kPa offen; gilt in jeder Kreislaufvariante",
     "ablauf": ["Die Linear-Membranpumpe (Platzhalterquader 240 × 180 × 230) bläst durch einen Stutzen d20 nach oben.",
                "Das Rohr steigt bis Z 710 über den höchsten Wasserspiegel (Pool-Rand Z 650 plus 60) und biegt waagerecht ab; so läuft kein Wasser in die Pumpe zurück.",
                "Ein Rückschlagventil d20 ist die zweite Sperre; danach folgt der Luftaustritt zum Hauptverteiler."],
     "aufbau": [{"t": "Pumpe", "p": ["Gehäuse 240 × 180 × 230, 10 kg (Beispiel)", "4 Gummifüße, Stutzen d20, Netzkabel"]}, {"t": "Luftleitung", "p": ["Rohr d20 mit Bogen R80, Scheitel Z 710", "Rückschlagventil d20, Austrittsrohr"]}],
     "masse": {"Masse": "ca. 10,3 kg", "Scheitel der Schleife": "195 mm über dem Spiegel Z 515", "Luftmenge": "Klasse 200 l/min bei mindestens 26 kPa; bei 26 kPa grob 176 l/min (Fortschreibung)"},
     "grenzen": "Pumpentyp und Kennlinie bei 26 kPa offen (R53); die Spitze 205 l/min trägt nur der Parallellauf beider Pumpen; Notstrom und Standort (E13) offen.",
     "quelle": "docs/parts/geblaese_luft.md, docs/research/R45-hydraulik-auslegung.md Abschnitt 4, docs/research/R53-europa-frischwasser-luft.md"},
    {"match": "^schrank_einfuehrung", "titel": "Schaltschrank-Einführung (Leerrohre)",
     "was": "Boden-Einführungsplatte des Schaltschranks mit zwei Kabeleinführungen (230 V DN100, Signal DN50) und je einem Leerrohr-Bogen nach unten.",
     "status": "gebaut (Werkstatt W37-3), Prüfung 30/30; nur das Bauteil, Standort OFFEN (E13), Kabelzahl OFFEN (E20)",
     "ablauf": ["Die Kabel laufen unterirdisch durch Leerrohre (DN100 für 230 V, DN50 für Signal) zum Schrank.", "Der Bogen führt das Rohr von der Seite nach oben in die Einführung; deren Hals geht durch den Schrankboden, Dichtung unten, Gegenmutter oben.", "Die beiden Stämme liegen 300 mm auseinander (Abstand der Muffen 210 mm, Mindestmaß 200 mm gegen Störungen)."],
     "aufbau": [{"t": "Platte", "p": ["Boden 800 × 500 × 3 mit zwei Ausschnitten"]}, {"t": "Einführungen", "p": ["DN100 (Ø 130 Hals) und DN50 (Ø 63 Hals) aus W39", "Leerrohr-Bogen R500 und R300 aus W36"]}],
     "masse": {"Boden": "800 × 500 × 3", "Tiefe unterflur": "DN50 bis 397 mm, DN100 bis 654 mm unter dem Schrankboden", "Masse": "ca. 15,3 kg (mit Wandstummel)"},
     "grenzen": "Standort des Schranks (E13), Kabelzahl und Füllgrad (E20) sind offen; der DN100-Bogen liegt tiefer als die Plantiefe von 400 mm.",
     "quelle": "docs/parts/schrank_einfuehrung.md, docs/jobs/W37-3-luft-schaltschrank.md"},
]

BLATT = {"luftverteiler_6": lambda: blatt_verteiler("luftverteiler_6"), "luftverteiler_4": lambda: blatt_verteiler("luftverteiler_4"),
         "luft_scheibenbelueftung": blatt_scheibe, "geblaese_luft": blatt_geblaese, "schrank_einfuehrung": blatt_schrank}
