"""Schreibt data/components/<klasse>.json (Parameter, Herkunft, Blatt) der fuenf W37-3-Teile: luftverteiler_6, luftverteiler_4, luft_scheibenbelueftung, geblaese_luft, schrank_einfuehrung.
Einmal zuerst (nur Parameter, damit die Generatoren laufen), am Ende nochmals mit Messwerten (Blatt-Texte). Aufruf: python -X utf8 scripts/workshop/w37_3_json.py [klasse ...]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

def P(wert, einheit, herkunft):
    return {"wert": wert, "einheit": einheit, "herkunft": herkunft}

# ------------------------------------------------------------------ Verteiler
WERK_PVC = {"name": "PVC-U (Formstueck, Sammler und Zapfen aus einem Koerper)", "dichte_g_cm3": 1.4, "farbe": "#3d6f9e", "herkunft": "[A] wie lt_verteiler_d50 (W36)"}
AB6 = [
    ["Pool", 40, "K44", "130 (Spitze 205)", "E R45 Abschnitt 4: Planwert 130 l/min, Spitze 205; d40"],
    ["Biofilter 1", 25, "K45", "offen", "A: Menge nach Traegerhersteller (R45 Abschnitt 4, K1), Anschluss d25 (Netz)"],
    ["Biofilter 2", 25, "K46", "offen", "A: wie Biofilter 1"],
    ["Drittbecken", 20, "K49", "2", "E Netz K49: 0,3 bis 0,5 l/min gerechnet, ausgelegt 2 l/min [A, Reserve]"],
    ["Zweitbecken", 20, "K51", "5", "A: wenige l/min (Netz K51 Aufzucht, soll_l_min leer); 5 l/min als Planwert"],
    ["Absetzer (optional)", 20, "K47/K48", "offen", "A: optional, ein Abgang fuer beide Absetzer (Netz K47/K48 'optional')"],
]
AB4 = [[f"Scheibe {k}", 25, "K44 (Teil)", "33", "A: 130 l/min Planwert / 4 = 32,5, gerundet 33 l/min je Abgang"] for k in range(1, 5)]

def spec_verteiler(name):
    n = 6 if name.endswith("6") else 4
    ab = AB6 if n == 6 else AB4
    zweck = ("Hauptverteiler am Geblaese: nimmt die Druckluft beider Pumpen (N+1) in Port A auf und teilt sie auf Pool, Biofilter 1 und 2, Drittbecken, Zweitbecken und Absetzer"
             if n == 6 else "Pool-Verteiler am Becken: nimmt die Pool-Luft (K44, Planwert 130 l/min) in Port A auf und gibt sie an vier Scheibenbelueftungsteile weiter")
    return {
        "klasse": name, "teilenummer": "T86" if n == 6 else "T87", "revision": "A",
        "beschreibung": f"Luftverteiler {n}-fach d40 (W37-3, R45 Abschnitt 4, Netz K44 bis K51): {zweck}. Sammler d40 mit Muffe A, {n} Zapfen nach oben, Teilung 120, Ende B geschlossen; Masse nach W36-Muster, Handelsteile (Hahn, Rueckschlagventil, T-Stuecke) Katalog offen",
        "quelle_masse": "docs/research/R45-hydraulik-auslegung.md Abschnitt 4 (Zeilen 225 bis 279); data/leitungsnetz.json Version 3 K44 bis K51 (nur gelesen); docs/parts/leitungsteile.md Verteiler d50 (W36); scripts/workshop/leitung.py (od_f, wall_p, DEPTH)",
        "parameter": {
            "pipe_d": P(40, "mm", "[E] Netz K44: Hauptleitung d40 (R45 Abschnitt 4: d40 bei 200 l/min 3,2 m/s, Innen-Ø 36,2)"),
            "pitch": P(120, "mm", "[A] Teilung wie lt_verteiler_d50 (Kugelhahn-Gehaeuse d25 = 43,25 plus Hebel; Ventil d40 = 60 mm)"),
            "x0": P(75, "mm", "[A] erster Abgang: Muffe A d40 (Tiefe 26) plus Abgangsbohrung d40 (Radius 18,1) plus Steg"),
            "end_cap": P(10, "mm", "[A] integrierte Endkappe (Wand) am Ende B wie lt_verteiler_d50"),
        },
        "abgaenge": ab,
        "werkstoff": WERK_PVC,
        "anzahl": {"soll": "1 " + ("Hauptverteiler am Geblaese" if n == 6 else "Pool-Verteiler am Becken"), "quelle": "R45 Abschnitt 4 Empfehlung 4 und 5; Netz Version 3"},
        "bezugspunkt": "Port A (Mitte der Muffenoeffnung d40, Einlauf) im Ursprung; Sammlerachse +X (Muffe oeffnet nach -X), Abgaenge zeigen nach +Z (Zapfen-Ende 74 ueber der Achse), Ende B bei X = Laenge geschlossen",
    }

# ------------------------------------------------------------------ Scheibenbelueftung
def spec_scheibe():
    return {
        "klasse": "luft_scheibenbelueftung", "teilenummer": "T88", "revision": "A",
        "beschreibung": "EPDM-Scheibenbelueftungsteil Ø 270 (W37-3, R45 Abschnitt 4): Anschlussstutzen d25 senkrecht nach unten, Stuetzfuss, Tragteller und EPDM-Membran; 4 Stueck im Pool, am Pool-Verteiler. Parameter d (Standard 270) und pipe_d (25, Variante Drittbecken K49 d20 mit d 100) bilden die Luftstein-Variante ohne eigenes Bauteil ab. Handelsmass-Platzhalter, Fabrikat offen (N-BESCHAFFUNG)",
        "quelle_masse": "docs/research/R45-hydraulik-auslegung.md Abschnitt 4; docs/research/R53-europa-frischwasser-luft.md (Jaeger JetFlex HD 270 [Q-Treffer], Disque diffuseur 270 EPDM Ref. DD-0270-EPDM-HCS [Q]); data/leitungsnetz.json K44, K49",
        "parameter": {
            "d": P(270, "mm", "[A] Membran-Ø Handelsmass 215 bis 270 (Auftrag W37-3); Standard 270 (R53: JetFlex HD 270, Disque diffuseur 270)"),
            "pipe_d": P(25, "mm", "[A] Anschlussstutzen d25 (Pool-Verteiler d25, Auftrag W37-3); Variante Drittbecken K49: 20"),
            "stutzen_l": P(40, "mm", "[A] Anschlussstutzen Laenge: Rohr steckt in die Muffe der Zuleitung (Tiefe 19)"),
            "fuss_h": P(50, "mm", "[A] Stuetzfuss: Hoehe von der Stutzenoberkante bis zum Tragteller"),
            "teller_h": P(20, "mm", "[A] Tragteller PP"),
            "teller_rand": P(20, "mm", "[A] Tragteller Ø = d minus 20 (Membranrand liegt ueber)"),
            "membran_h": P(6, "mm", "[A] EPDM-Membran, nicht geschlitzt modelliert (Schlitze nicht modelliert)"),
            "luft_bohrung": P(16, "mm", "[A] Luftkanal Ø 16 durch Stutzen und Stuetzfuss (Kanal im Tragteller nicht modelliert)"),
        },
        "werkstoff": {"name": "PP (Stutzen, Stuetzfuss, Tragteller), EPDM (Membran)", "dichte_g_cm3": 0.91, "farbe": "#e8e5d8", "herkunft": "[A] Handelsteil, Werkstoff nach Katalog offen"},
        "anzahl": {"soll": "4 Stueck im Pool (Pool-Verteiler 4-fach); 1 Luftstein-Variante im Drittbecken (K49) als Parameter", "quelle": "Auftrag W37-3 Teil 3; Netz K44, K49"},
        "bezugspunkt": "Port A (Ende des Anschlussstutzens, Mitte) im Ursprung; Oeffnung zeigt -Z (nach unten), Stutzen, Stuetzfuss, Tragteller und Membran stehen auf der Achse +Z",
    }


# ------------------------------------------------------------------ Geblaese
def spec_geblaese():
    return {
        "klasse": "geblaese_luft", "teilenummer": "T85", "revision": "A",
        "beschreibung": "Geblaese-Baugruppe Luft (W37-3 Teil 1, R45 Abschnitt 4, R53 Abschnitt 4 und 5): Linear-Membranpumpe der Klasse 200 l/min bei mindestens 26 kPa als Platzhalterquader mit Gummifuessen, Stutzen d20, Netzkabel, dazu die Luftleitung ueber den hoechsten Wasserspiegel (Schleife) mit Rueckschlagventil d20. Zwei Stueck (N+1). Pumpentyp NICHT gewaehlt (Beispielreihe Hiblow HP-200, Secoh JDK-S-200), Kennlinie bei 26 kPa OFFEN; Standort Schaltschrankbereich OFFEN (E13)",
        "quelle_masse": "docs/research/R45-hydraulik-auslegung.md Abschnitt 4 (Empfehlung 3, 4, 7); docs/research/R53-europa-frischwasser-luft.md Abschnitt 4 (Secoh JDK-S-200: 240 x 180 x 230,5 mm, 10,0 kg, BIBUS [Q]) und 5; data/leitungsnetz.json Kabel schaltschrank -> geblaese_fisch 204 W (nur gelesen); data/layout.json pool2.water_z 515 und data/params.json pool_rim 650 (nur gelesen)",
        "parameter": {
            "box_x": P(240, "mm", "[A] Platzhalter nach Beispielreihe Secoh JDK-S-200 (BIBUS, R53: 240 x 180 x 230,5); Typ nicht gewaehlt, aus Katalog nachzumessen"),
            "box_y": P(180, "mm", "[A] wie box_x"),
            "box_z": P(230, "mm", "[A] wie box_x"),
            "pump_mass_g": P(10000, "", "[A] 10,0 kg (Secoh JDK-S-200, BIBUS [Q] R53; Hiblow HP-200 8,5 bis 9 kg); Gehaeuse als Vollquader, Dichte so gesetzt, dass die Pumpe 10 kg wiegt"),
            "foot_d": P(40, "mm", "[A] Gummifuss Ø 40"),
            "foot_h": P(15, "mm", "[A] Gummifuss Hoehe 15"),
            "foot_x": P(90, "mm", "[A] Fussmitte x (innerhalb der 240er Grundflaeche)"),
            "foot_y": P(60, "mm", "[A] Fussmitte y (innerhalb der 180er Grundflaeche)"),
            "out_d": P(20, "mm", "[A] Luftaustritt d20 (Auftrag W37-3 Teil 1; R45: d20/d25); weiter ueber Reduzierung auf d25 zum Verteiler"),
            "out_l": P(40, "mm", "[A] Stutzen Laenge ueber dem Gehaeuse"),
            "bend_r": P(80, "mm", "[A] Biegeradius der Rohrschleife (4 x d, warm gebogen)"),
            "apex_z": P(710, "mm", "[E] Rohrachse der Schleife ueber der Aufstellflaeche: Pool-Rand Z 650 (params pool_rim) + 60 wie Schwimmerventil = Z 710; Wasserspiegel Z 515 (layout pool2.water_z) -> Reserve 195 mm. R45 Empfehlung 7: 'ueber dem hoechsten Wasserspiegel'; Aufstellflaeche Z 0 angenommen (E13 offen)"),
            "arm_l": P(150, "mm", "[A] waagerechter Schenkel nach dem Bogen bis zum Rueckschlagventil"),
            "out_tube_l": P(100, "mm", "[A] Austrittsrohr hinter dem Rueckschlagventil bis Port Luftaustritt"),
            "cable_d": P(8, "mm", "[A] Netzkabel Ø 8 (Stummel Platzhalter)"),
            "cable_l": P(100, "mm", "[A] Netzkabel-Stummel Laenge"),
            "cable_x": P(-80, "mm", "[A] Netzkabel x-Lage an der Rueckseite"),
        },
        "werkstoff": {"name": "Gehaeuse Aluminium/Kunststoff (Platzhalter), Fuesse Gummi, Luftleitung PVC-U", "dichte_g_cm3": 1.0, "farbe": "#2f3a44", "herkunft": "[A] Platzhalter; Dichte des Quaders so, dass 10,0 kg erreicht werden ([Q] Secoh JDK-S-200)"},
        "anzahl": {"soll": "2 Stueck (N+1: eine Pumpe laeuft, die zweite ist Reserve; Spitze 205 l/min nur mit beiden)", "quelle": "R45 Abschnitt 4 Empfehlung 3 und 4; D45 e (Reserve-Geblaese)"},
        "bezugspunkt": "Mitte der Standflaeche der Pumpe am Boden (Z 0 = Aufstellflaeche); X zeigt zum Luftaustritt, Y quer (Netzkabel -Y), Z hoch; Rohrachse der Schleife bei Z 710, Port Luftaustritt am Ende des Austrittsrohrs (+X)",
    }


# ------------------------------------------------------------------ Schrank-Einfuehrung
def spec_schrank():
    return {
        "klasse": "schrank_einfuehrung", "teilenummer": "T89", "revision": "A",
        "beschreibung": "Schrank-Einfuehrung (W37-3 Teil 4, L08): Einfuehrungsplatte am Boden des Schaltschranks (800 x 500, Blech 3 mm) mit Kabeleinfuehrung DN100 (230-V-Stamm) und DN50 (Signal-Stamm) aus W39 und je einem Leerrohr-Bogen 90 Grad aus W36 darunter. Nur das Bauteil, lokale Koordinaten: Standort des Schranks OFFEN (E13); Kabelzahl und Fuellgrad OFFEN (E20); Tauchpumpen im Subtank OFFEN (D75, geparkt)",
        "quelle_masse": "data/params.json cab_x 800, cab_y 500, cab_z 1200 ([A] ref-5 geschaetzt, nur gelesen); docs/parts/leitungsteile.md (Ergaenzung W39: Kabeleinfuehrung DN50/DN100; W36: Leerrohr-Bogen); scripts/workshop/leitung_w39.py (kab_geom) und leitung_w36.py (LR); docs/jobs/W37-3-luft-schaltschrank.md Teil 4 (EMV-Abstand 200 mm, Plan Abschnitt 4 Regel 9)",
        "parameter": {
            "cab_x": P(800, "mm", "[E] data/params.json cab_x (Schrankbreite, gelesen); [A] ref-5 geschaetzt"),
            "cab_y": P(500, "mm", "[E] data/params.json cab_y (Schranktiefe, gelesen)"),
            "boden_t": P(3, "mm", "[A] Blech 3 mm wie lt_kabeleinfuehrung (Boden der Einfuehrung, W39 KAB boden)"),
            "wand_t": P(2, "mm", "[A] Schrankwand-Stummel 2 mm (nur fuer die Interferenzpruefung)"),
            "wand_h": P(100, "mm", "[A] Hoehe des Wandstummels ueber dem Boden (Schrank 1200 hoch, hier nur der Fussbereich)"),
            "x_dn100": P(-150, "mm", "[A] Achse der Einfuehrung DN100 (230 V); Abstand der beiden Achsen 300: freier Abstand der Muffen 300 - 61,5 - 28 = 210,5 mm gegen 200 mm EMV"),
            "x_dn50": P(150, "mm", "[A] Achse der Einfuehrung DN50 (Signal)"),
            "y_achse": P(0, "mm", "[A] beide Achsen auf der Mittellinie der Schranktiefe"),
            "emv_min": P(200, "mm", "[E] Plan Abschnitt 4 Regel 9: Abstand 230 V gegen Signal mindestens 200 mm (Auftrag W37-3)"),
        },
        "werkstoff": {"name": "Stahlblech (Boden, Wandstummel), PP und EPDM (Kabeleinfuehrung), PVC-U (Leerrohr-Bogen)", "dichte_g_cm3": 7.85, "farbe": "#9aa0a4", "herkunft": "[A] Platzhalter; Blech Stahl, Rest aus den Bibliotheksteilen"},
        "anzahl": {"soll": "1 am Schaltschrank", "quelle": "Auftrag W37-3 Teil 4; Netz-Kabeleintraege (Schaltschrank)"},
        "bezugspunkt": "Mitte der Boden-Unterkante des Schaltschranks (Z 0 = Unterkante Schrankboden, Boden Z 0 bis 3); X Schrankbreite, Y Schranktiefe, Z nach oben in den Schrank; Leerrohre darunter bei negativem Z. Standort im Modell: NICHT enthalten (OFFEN E13)",
    }

SPECS = {"schrank_einfuehrung": spec_schrank, "geblaese_luft": spec_geblaese, "luftverteiler_6": lambda: spec_verteiler("luftverteiler_6"), "luftverteiler_4": lambda: spec_verteiler("luftverteiler_4"), "luft_scheibenbelueftung": spec_scheibe}

def write(name, extra=None):
    d = SPECS[name]()
    import w37_3_blatt
    d.update(w37_3_blatt.BLATT[name]())
    if extra:
        d.update(extra)
    path = os.path.join(sc.ROOT, "data", "components", name + ".json")
    old = {}
    if os.path.exists(path):
        old = json.load(open(path, encoding="utf-8"))
    for k in ("blatt", "herkunft_tabelle"):               # bereits geschriebene Blatt-Teile nicht verlieren
        if k in old and k not in d:
            d[k] = old[k]
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben", path)


def write_descriptions():
    """Fuegt die W37-3-Eintraege vor dem Eintrag '^puffer' in data/descriptions.json ein (Viewer nimmt den ersten Treffer; keine Mustergleichheit mit ^schaltschrank); idempotent."""
    import w37_3_blatt
    p = os.path.join(sc.ROOT, "data", "descriptions.json")
    txt = open(p, "rb").read().decode("utf-8")
    anchor = '    {\r\n      "match": "^puffer",'
    assert txt.count(anchor) == 1
    for e in w37_3_blatt.DESC:
        if json.dumps(e["match"], ensure_ascii=False) in txt:
            continue
        body = json.dumps(e, indent=2, ensure_ascii=False).replace("\n", "\n    ").replace("\n", "\r\n")
        txt = txt.replace(anchor, "    " + body + ",\r\n" + anchor)
    json.loads(txt)
    open(p, "wb").write(txt.encode("utf-8"))
    print("descriptions.json: W37-3-Eintraege vorhanden")

if __name__ == "__main__":
    for n in ([a for a in sys.argv[1:] if not a.startswith("--")] or list(SPECS)):
        write(n)
    if "--descriptions" in sys.argv:
        write_descriptions()
