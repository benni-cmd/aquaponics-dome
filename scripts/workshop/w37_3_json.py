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

SPECS = {"luftverteiler_6": lambda: spec_verteiler("luftverteiler_6"), "luftverteiler_4": lambda: spec_verteiler("luftverteiler_4"), "luft_scheibenbelueftung": spec_scheibe}

def write(name, extra=None):
    d = SPECS[name]()
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

if __name__ == "__main__":
    for n in (sys.argv[1:] or list(SPECS)):
        write(n)
