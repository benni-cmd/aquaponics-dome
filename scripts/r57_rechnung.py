"""R57 Systemreview (N-MINIMAL, W75/W76/W79): Rechnung heute (A+ wie gebaut und geplant) gegen Zielbild S (schlank).
Nur lesen. Aufruf: python -X utf8 scripts/r57_rechnung.py [abschnitt]   abschnitt = vergraben | aushub | pegel | pumpen | kosten | alle (Standard)
Eingaben: data/leitungstrassen.json (ueber scripts/leitungen.laden_variante(), Variante A+), data/leitungsnetz.json, data/system-specs.json,
data/beschaffung/*.json (kleinster belegter Preis je Artikel, Stand 04./05.11.2026), docs/research/R45, R47, R49 (zitierte Zahlen, unten je Wert benannt).
Herkunft je Zahl: [Q] Datei/Quelle gelesen, [E] hier gerechnet, [A] Annahme dieses Skripts. Keine fachliche Freigabe.
Zielbild S: Pool ist der tiefste Punkt (Ruhepegel Z -150 statt +515), Tauchpumpen im Pool heben ueber Schlauch in Siebkorb auf dem Biofilter,
alles andere fliesst frei zurueck in den Pool; Beete stehen auf dem Flur statt 162 bis 209 mm eingegraben; Absetzerkreis, Heber, Filtergrube,
Filter-Stamm, Notbypass, Beet-Sumpf entfallen; Schlamm per Schlauch nach draussen in ein Fass ueber dem Boden."""
import glob, json, math, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import leitungen as LG

FZ = 400.0                                     # Flur absolut [Q leitungsordnung.md Begriffe]
NETZ = {k["id"]: k for k in json.load(open(os.path.join(ROOT, "data", "leitungsnetz.json"), encoding="utf-8"))["kanten"]}
SPEC = json.load(open(os.path.join(ROOT, "data", "system-specs.json"), encoding="utf-8"))
ARG = sys.argv[1] if len(sys.argv) > 1 else "alle"

def kopf(t): print("\n== " + t)

# ------------------------------------------------------------------ 1 vergraben
GRUPPE = {
    "Saugseite Hauptkreislauf (Heber, Stamm, Zweig, Notbypass)": ("K01", "K17", "K02", "K06", "K18", "K22", "K56", "K57"),
    "Absetzerkreis (Bodenablauf, Absetzer-Auslauf, Schlamm, Revision)": ("K03", "K19", "K05", "K21", "K07", "K23", "REV"),
    "Luft (Geblaese zu Pool, Biofiltern, Becken)": ("K44", "K45", "K46", "K47", "K48", "K49", "K51"),
    "Frischwasser und Aktivkohle": ("K39", "K40", "K41", "K52"),
}
def gruppe_von(tid):
    for g, ks in GRUPPE.items():
        if any(tid == k or tid.startswith(k + "-") or tid.startswith(k) and k == "REV" for k in ks): return g
    return "sonstige"

def vergraben():
    kopf("1 Vergrabene Meter (Segmentmitte unter Z 400 absolut, Variante A+ aus data/leitungstrassen.json)")
    doc = LG.laden_variante()
    agg = defaultdict(lambda: [0.0, 0.0]); ges = unt = 0.0
    for t in doc["trassen"]:
        p = t["pfad"]; g = gruppe_von(t["id"])
        for a, b in zip(p, p[1:]):
            L = math.dist(a, b) / 1000.0; ges += L; agg[g][0] += L
            if (a[2] + b[2]) / 2 < FZ: unt += L; agg[g][1] += L
    print("  Trassen %d, gesamt %.1f m, davon unter Flur %.1f m [E]" % (len(doc["trassen"]), ges, unt))
    for g, (a, u) in sorted(agg.items(), key=lambda x: -x[1][1]): print("  %-66s gesamt %5.1f  unter Flur %5.1f m" % (g, a, u))
    kuenftig = {"K14/K30 Beet-Sammler (R49 Abschn. 4, +-25 %)": 58.9, "K58/K59 Beet-Sumpf-Foerderleitung (R49)": 8.0, "K11 Beet-Zufuhr Gangquerungen (R49 [A])": 12.0}
    print("  geplante, noch nicht gebaute Graeben A+ [Q R49 Abschn. 4]: " + ", ".join("%s %.1f m" % kv for kv in kuenftig.items()) + " = %.1f m" % sum(kuenftig.values()))
    # Zielbild S
    s = {"Beet-Ruecklauf: Einmuendung am Pool, flacher Kanal je Linie [A 2 x 3 m]": 6.0,
         "Gangquerungen Luft/Frischwasser/Beet-Zufuhr als Leerrohr DN100 [A 10 x 1,2 m]": 12.0}
    av2 = unt - agg["Luft (Geblaese zu Pool, Biofiltern, Becken)"][1] - agg["Frischwasser und Aktivkohle"][1]
    print("  Zwischenvariante A+ mit Ordnung v2 (Luft und Frischwasser als Schlauch ueber Flur, Rest wie A+): gebaut %.1f m + geplant %.1f m = %.1f m [E]" % (av2, sum(kuenftig.values()), av2 + sum(kuenftig.values())))
    print("  Zielbild S unter Flur [A]: " + ", ".join("%s %.1f m" % kv for kv in s.items()) + " = %.1f m" % sum(s.values()))
    return dict(heute_gebaut=unt, heute_geplant=sum(kuenftig.values()), s=sum(s.values()), gruppen={g: round(v[1], 1) for g, v in agg.items()})

# ------------------------------------------------------------------ 2 Aushub ohne Pool
def aushub():
    kopf("2 Aushub ohne Poolgrube (m3)")
    doc = LG.laden_variante(); gr = {g["id"]: g for g in doc.get("gruben", [])}
    sf = sum(math.pi / 4 * (g["d"] / 1000) ** 2 * (FZ - g["sohle"]) / 1000 for k, g in gr.items() if k.startswith("schlammfass"))
    pos = [
        ("Schlammfass-Gruben 2 x (Durchmesser 0,8 m, Sohle aus data/leitungstrassen.json 'gruben') [E]", sf, 0.0),
        ("Beet-Sumpf-Gruben 2 x (Durchmesser 1,0 m, Tiefe 1,0 m, R45 Abschn. 3) [Q/E]", 2 * math.pi / 4 * 1.0 ** 2 * 1.0, 0.0),
        ("Feinfilter-Gruben 2 x (Grundflaeche 1,0 x 0,8 m [A], 0,5 m tief, D72) [A/Q]", 2 * 1.0 * 0.8 * 0.5, 0.0),
        ("Schaechte Kugelhahn 4 x (0,25 x 0,47 x 0,48 m, SCH-KH1 in 'gruben') [Q/E]", 4 * 0.2546 * 0.4666 * 0.48, 0.0),
        ("Beete eingelassen 14 x (0,80 x 2,64 m [Q BEH-ibc-beetwanne], 0,18 m Mittel aus Beetboden Z -162 bis -209 [Q K14]) [E]", 14 * 0.80 * 2.64 * 0.18, 0.0),
        ("Graeben heute gebaut 0,3 m breit [A] x mittlere Tiefe 0,5 m [A] je Meter unter Flur", None, None),
        ("Graeben A+ geplant (K14, K58/59, K11 = 78,9 m) 0,3 x 0,5 m [A]", 78.9 * 0.3 * 0.5, 0.0),
        ("Zielbild S: Pool-Einmuendung Beet-Ruecklauf 2 x 3 m Kanal 0,3 x 0,3 m [A]", 0.0, 6.0 * 0.3 * 0.3),
        ("Zielbild S: Leerrohr-Querungen 12 m, 0,3 x 0,4 m [A]", 0.0, 12.0 * 0.3 * 0.4),
    ]
    v = vergraben.__dict__.get("cache") or {}
    unt = v.get("heute_gebaut")
    if unt is None:
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()): unt = vergraben()["heute_gebaut"]
    h = s = 0.0
    for name, a, b in pos:
        if a is None: a, b = unt * 0.3 * 0.5, 0.0
        h += a; s += b; print("  %-118s heute %5.2f  S %5.2f" % (name, a, b))
    print("  Summe heute %.1f m3, Zielbild S %.1f m3 [E]" % (h, s))
    return dict(heute=h, s=s)

# ------------------------------------------------------------------ 3 Poolpegel
POOL_D = 3.89          # m Innendurchmesser [Q params.json pool_depth.source, system-concept.md]
SPIEGEL_HEUTE = 515    # mm rel. Flur [Q D26, Netz pool]
RAND = 650             # mm rel. [Q params.json pool_rim]
TIEFE = 2200           # mm [Q D26]
BEET_FLUT_L = 234      # l je Beet und Flutung [Q Netz beete_linie_1]
FISCH_KG = 346         # [Q D61]
FISCHWASSER = 28.5     # m3 [Q system-specs wasser.fischwasser_m3]
AREA = math.pi / 4 * POOL_D ** 2

def pegel():
    kopf("3 Poolpegel im Zielbild S (Pool als tiefster Punkt)")
    anhebung_beet = 162                             # Beete auf Flur statt Beetboden Z -162 (aussen) [Q K14]; innen -209..-173 heben 173..209
    ablauf = -100 + anhebung_beet                   # Beetablauf heute Z -100 [Q K14, R47/R49]
    # Regel R49 Abschn. 3.1: Ablauf >= Einlauf + Gefaelle x Laenge + Rohr-d + 50; Einlauf = Pegel + 25
    faelle = [("Aussenbeet ueber Sammelring 9 m, 0,5 %, d90", 9000, 0.005, 90), ("Innenbeet direkt 3,5 m, 1 %, d50", 3500, 0.01, 50),
              ("Aussenbeet Schlauch d50 direkt 6 m, 1 %", 6000, 0.01, 50)]
    lim = []
    for n, L, g, d in faelle:
        p = ablauf - 50 - d - g * L - 25; lim.append(p)
        print("  %-42s Pegel hoechstens Z %5.0f [E]" % (n, p))
    ruhe = -150                                     # gewaehlter Ruhepegel [A], <= alle Grenzen
    assert ruhe <= min(lim) + 1
    dh = SPIEGEL_HEUTE - ruhe; dv = AREA * dh / 1000
    pool_heute = AREA * TIEFE / 1000
    fw = FISCHWASSER - dv
    flut = 2 * 2 * BEET_FLUT_L / 1000 / AREA * 1000     # beide Linien je 2 Beete gleichzeitig (R45 Planfall) [Q R45 Abschn. 3]
    flut1 = 2 * 1 * BEET_FLUT_L / 1000 / AREA * 1000
    alle_beete = 14 * BEET_FLUT_L / 1000 / AREA * 1000  # Stromausfall, alle Beete laufen in den Pool zurueck
    print("  Beetablauf auf Flur Z %d, gewaehlter Ruhepegel Z %d, Absenkung %d mm [E]" % (ablauf, ruhe, dh))
    print("  Poolflaeche %.2f m2, Volumen heute %.1f m3 (Rechnung, system-specs 26,15), weniger %.1f m3 [E]" % (AREA, pool_heute, dv))
    print("  Fischwasser %.1f -> %.1f m3, Besatz %.1f -> %.1f kg/m3 (FAO-Grenze 20, R44) [E]" % (FISCHWASSER, fw, FISCH_KG / FISCHWASSER, FISCH_KG / fw))
    print("  Pegelschwankung durch Flutung: je Linie 1 Beet %.0f mm, je Linie 2 Beete %.0f mm [E]" % (flut1, flut))
    print("  Freibord Rand Z %d - Ruhepegel = %d mm; Stromausfall, alle 14 Beete leer laufen: +%.0f mm, Rest %.0f mm [E]" % (RAND, RAND - ruhe, alle_beete, RAND - ruhe - alle_beete))
    print("  Waermespeicher Wasser 40,4 kWh/K [Q system-specs] -> %.1f kWh/K [E]" % (40.4 * (34.7 - dv) / 34.7))
    return dict(ruhe=ruhe, dh=dh, dv=dv, fw=fw, dichte=FISCH_KG / fw, flut=flut, freibord=RAND - ruhe)

# ------------------------------------------------------------------ 4 Pumpen und Strom
def p_w(q_lmin, h_m, eta=0.25): return 1000 * 9.81 * q_lmin / 60000 * h_m / eta

def pumpen():
    kopf("4 Pumpen und Dauerstrom (Wirkungsgrad 25 % wie Projektstandard, R47/R49)")
    l = SPEC["leistung"]
    heute = {"Hauptpumpen 2 Linien (110 l/min, H 2,0 m)": 2 * l["pumpe_elektrisch_w"], "Absetzer-Kleinpumpen": l["pumpe_klein_w"], "Beet-Sumpf (2 laufend, 90 %)": l["beet_sumpf_w"]}
    flut = 2 * 2 * BEET_FLUT_L / 1000 / AREA * 1000
    h_stat = (1750 - (-150 - flut)) / 1000          # Auslauf Schlauch ueber Siebkorb Z 1750 [A], Biofilter-Spiegel 1600 [Q R49 2.1]; tiefster Pegel
    h_s = h_stat + 0.30                             # Reibung Schlauch d40 6 m je Pumpe, Boegen, Korb [A]
    s = {"Hauptpumpen 2 Linien (110 l/min, H %.2f m)" % h_s: 2 * p_w(110, h_s)}
    for t, d in (("heute", heute), ("Zielbild S", s)):
        print("  %s: " % t + ", ".join("%s %.0f W" % kv for kv in d.items()) + " -> Summe %.0f W = %.1f kWh/Tag [E]" % (sum(d.values()), sum(d.values()) * 24 / 1000))
    print("  Pumpen gesamt heute 4 gross + 4 klein + 4 Teichpumpen (2 Reserve) = 12; S 4 Tauchpumpen (2 je Linie parallel) [Q Netz, D81 E19]")
    print("  Hinweis: Bei H %.2f m braucht jede Pumpe 55 l/min; heutige Eheim 3400 (Hmax 3,6 m) liefert dort rechnerisch %.0f l/min (parabolisch [A]) -> Pumpenwahl offen" % (h_s, 56.7 * math.sqrt(max(0, 1 - h_s / 3.6))))
    print("  Gegenprobe heute H 2,0 m: Eheim 3400 rechnerisch %.0f l/min (Soll 55) -> die Pumpenfrage besteht schon heute" % (56.7 * math.sqrt(1 - 2.0 / 3.6)))
    return dict(heute=sum(heute.values()), s=sum(s.values()), h_s=h_s)

# ------------------------------------------------------------------ 5 Teile und Kosten
def preise():
    out = {}
    for f in glob.glob(os.path.join(ROOT, "data", "beschaffung", "*.json")):
        a = json.load(open(f, encoding="utf-8"))["artikel"]
        items = a.items() if isinstance(a, dict) else [(x.get("id"), x) for x in a]
        for aid, it in items:
            if isinstance(it, dict):
                ps = [o["preis_eur"] for o in it.get("angebote", []) if isinstance(o.get("preis_eur"), (int, float))]
                out[aid] = min(ps) if ps else None
    return out

# Neue Artikel im Zielbild ohne Eintrag in data/beschaffung: Preis aus der R57-Recherche (Quelle im Bericht R57 Abschnitt 7) oder None
NEU = {   # Recherche R57 am 05.11.2026, Preise inkl. MwSt.; Quellen in docs/research/R57-systemreview.md Abschnitt 7
    "NEU-schlauch-spiral-id32-lm": 6.86,      # asdec-life.de FITT Metal-Flex 32 (205,79 EUR / 30 m); esska 11,99 EUR/m
    "NEU-schlauch-spiral-id40-lm": 14.32,     # esska.de 702414040430 (716,17 EUR / 50 m); imkado 15,10 EUR/m
    "NEU-schlauch-spiral-id50-lm": 15.10,     # imkado.de Meterware 50 mm; esska 51 mm 20,31 EUR/m
    "NEU-fass-220l-lm": 99.00,                # fermetech.eu 220 l food grade (Einzelquelle, ohne Hahn)
}
if os.path.exists(os.path.join(ROOT, "data", "r57_preise_neu.json")):
    NEU.update({k: v["preis_eur"] for k, v in json.load(open(os.path.join(ROOT, "data", "r57_preise_neu.json"), encoding="utf-8")).items()})

def laengen():
    """Rohrmeter je Kante (Variante A+), Praefix K.. oder REV."""
    import re
    agg = defaultdict(float)
    for t in LG.laden_variante()["trassen"]:
        m = re.match(r"(K\d+|REV)", t["id"]); k = m.group(1) if m else t["id"]
        agg[k] += sum(math.dist(a, b) for a, b in zip(t["pfad"], t["pfad"][1:])) / 1000.0
    return agg
LEN = laengen()
def lsum(*ks): return round(sum(LEN.get(k, 0.0) for k in ks), 1)

# (Gruppe, Artikel, Menge heute, Menge S, Herkunft der Menge)
POS = [
    ("G3 Absetzerkreis", "PMP-pumpe-klein", 4, 0, "Netz pumpe_klein_1..4"),
    ("G3 Absetzerkreis", "BEH-tank-pe-673x1075", 2, 0, "stueckliste tank_klein"),
    ("G3 Absetzerkreis", "ROH-pvcu-d50", lsum("K03", "K19", "K05", "K21", "REV"), 0, "Trassen K03/K19/K05/K21/REV (A+), d40/d50 als d50"),
    ("G3 Absetzerkreis", "ROH-pvcu-d32", lsum("K04", "K20"), 0, "Trassen K04/K20"),
    ("G4 Schlammfass Grube", "BEH-tank-pe-580x865", 2, 0, "R45 Abschn. 0, behaelter.json"),
    ("G4 Schlammfass Grube", "ARM-kugelhahn-d40", 2, 0, "K07/K23 Federhahn (Preis normaler Hahn [A])"),
    ("G4 Schlammfass Grube", "ROH-pvcu-d40", lsum("K07", "K23"), 0, "Trassen K07/K23"),
    ("G4 Schlamm draussen (neu)", "NEU-fass-220l-lm", 0, 2, "je Linie ein Fass ueber Boden [A]"),
    ("G4 Schlamm draussen (neu)", "NEU-schlauch-spiral-id32-lm", 0, 16, "2 x 8 m Schlammschlauch [A]"),
    ("G5/G6/G7 Saugseite", "ARM-bulkhead-pool", 2, 0, "Seitenablauf-Durchfuehrungen d63 in der Poolwand unter dem Spiegel (K01/K17)"),
    ("G5/G6/G7 Saugseite", "ROH-pvcu-d75", lsum("K01", "K17"), 0, "Trassen Heber K01/K17"),
    ("G5/G6/G7 Saugseite", "ROH-pvcu-d63", lsum("K56", "K57"), 0, "Trassen Notbypass K56/K57"),
    ("G5/G6/G7 Saugseite", "ROH-pvcu-d50", lsum("K02", "K06", "K18", "K22"), 0, "Trassen Stamm und Zweig K02/K06/K18/K22"),
    ("G5/G6/G7 Saugseite", "ARM-kugelhahn-d63", 4, 0, "Bypass-Haehne KH1/KH2, Stamm-Haehne (M10-S2N)"),
    ("G5/G6/G7 Saugseite", "SON-schacht-kugelhahn-d63", 4, 0, "M10-S2N Schaechte"),
    ("G5/G6/G7 Saugseite", "BEH-feinfilter-pp-630x440x610", 2, 0, "Feinfilter-Kasten (Korb bleibt)"),
    ("G8 Hauptpumpen", "PMP-pumpe-gross", 4, 4, "gleiche Zahl; staerkere Kennlinie noetig (Abschn. 4)"),
    ("G8 Hauptpumpen (neu)", "NEU-schlauch-spiral-id40-lm", 0, 24, "4 x 6 m Pool bis Siebkorb [A]"),
    ("G12 Beet-Ruecklauf", "ROH-pvcu-d50", 58.9, 0, "heute K14/K30 (R49)"),
    ("G12 Beet-Ruecklauf", "NEU-schlauch-spiral-id50-lm", 0, 46.5, "S Ring + Stiche als Schlauch (R49 3.1, 44-49 m)"),
    ("G13 Beet-Sumpf", "BEH-tank-pe-800x1000", 2, 0, "R45 Abschn. 3"),
    ("G13 Beet-Sumpf", "PMP-teichpumpe-5300", 4, 0, "2 laufend + 2 Reserve (D81 E19)"),
    ("G13 Beet-Sumpf", "MES-level-float", 6, 0, "3 Schwimmer je Sumpf (R45)"),
    ("G13 Beet-Sumpf", "ARM-rsv-d40", 2, 0, "Rueckschlagventil je Foerderleitung (R45)"),
    ("G13 Beet-Sumpf", "ROH-pvcu-d40", 8, 0, "K58/K59 (R49)"),
    ("G20 Sensorik (neu)", "MES-level-float", 0, 2, "Poolpegel tief/hoch statt Sumpfschwimmer [A]"),
    ("G20 Sensorik (neu)", "MES-flow-12", 0, 2, "Durchflusswaechter je Linie (R47b M5)"),
]

def kosten():
    kopf("5 Teile und Kosten (kleinster belegter Preis je Artikel in data/beschaffung, brutto; None = kein Preis belegt)")
    P = preise(); P.update(NEU)
    sh = ss = 0.0; offen = set(); grp = defaultdict(lambda: [0.0, 0.0])
    for g, a, mh, ms, her in POS:
        p = P.get(a)
        if p is None: offen.add(a)
        eh = (p or 0) * mh; es = (p or 0) * ms; sh += eh; ss += es; grp[g][0] += eh; grp[g][1] += es
        print("  %-26s %-30s heute %6.1f  S %6.1f  je %8s EUR  -> %8.2f / %8.2f   (%s)" % (g, a, mh, ms, "%.2f" % p if p else "None", eh, es, her))
    print("  Summe mit Preis: heute %.0f EUR, S %.0f EUR, Differenz %.0f EUR [E]" % (sh, ss, ss - sh))
    print("  ohne belegten Preis (nicht in der Summe): " + ", ".join(sorted(offen)))
    for g, (h, s) in grp.items(): print("    %-26s heute %7.0f  S %7.0f" % (g, h, s))
    teile_h = sum(1 for g, a, mh, ms, _ in POS if mh and not a.startswith("ROH") and not a.startswith("SCH"))
    print("  Positionen (ohne Rohr/Schlauch-Meterware): heute %d Artikelzeilen mit Menge, S %d [E]" % (teile_h, sum(1 for g, a, mh, ms, _ in POS if ms and not a.startswith(("ROH", "SCH", "NEU-schlauch")))))
    stueck_h = sum(mh for g, a, mh, ms, _ in POS if not a.startswith(("ROH", "SCH", "NEU-schlauch")))
    stueck_s = sum(ms for g, a, mh, ms, _ in POS if not a.startswith(("ROH", "SCH", "NEU-schlauch")))
    print("  Stueckzahl dieser Gruppen (ohne Meterware): heute %d, S %d [E]" % (stueck_h, stueck_s))
    return dict(heute=sh, s=ss, offen=sorted(offen))

if __name__ == "__main__":
    if ARG in ("vergraben", "alle"): vergraben.cache = vergraben()
    if ARG in ("aushub", "alle"): aushub()
    if ARG in ("pegel", "alle"): pegel()
    if ARG in ("pumpen", "alle"): pumpen()
    if ARG in ("kosten", "alle"): kosten()
