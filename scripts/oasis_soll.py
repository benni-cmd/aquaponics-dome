"""N-UNIFY-AUTOBAHN P1a: Leons Oasis-Showcase (Wasserkreislauf-Soll) als Daten: `data/oasis-soll.json`.

Aufruf (Projektordner):  python -I -X utf8 scripts/oasis_soll.py            schreibt die Datei und druckt die Pruefungen
                         python -I -X utf8 scripts/oasis_soll.py --pruefen  schreibt nichts, Exit 1 bei einer gescheiterten Pruefung
Reproduzierbar: keine Zeitstempel, nur Eingabe = die zwei gesicherten Quelldateien (SHA256 im README der Ordner).
`node` wird nur gebraucht, um `nodeDatabase.getMetrics()` auszuwerten (Kennzahlen); fehlt es, bleiben `kennzahlen_index` leer
und eine Pruefung meldet es.

Eingaben (Fremdmaterial, nicht aendern):
  docs/quellen/oasis-showcase-2026-11-10/index.html            Draufsicht + Seitenprofil (Inline-SVG), nodeDatabase, sollStufen, sollWasserspiegel
  docs/quellen/oasis-showcase-2026-11-10-nachtrag/flow-diagram.html   JSON-Bloecke `flow-data` (43 Bauteile, 90 Wege, Teile) und
                                                                       `schema-data` (Stufen, Wasserspiegel, Antrieb), Hoehenschnitt

Umrechnung Zeichnung -> Modell (ANNAHME, siehe docs/research/R61 Abschnitt 5 und docs/decisions.md):
  * Zeichnungsrahmen 1000 x 1000 Einheiten; die Kuppel ist der Kreis (cx 500, cy 480, r 480). Die 12-m-Kuppel (Aussendurchmesser
    12000 mm) hat damit 12000 / 960 = 12,5 mm je Einheit (MM_JE_EINHEIT). Gemessen: Sumpftank 90 x 238 Einheiten = 1125 x 2975 mm,
    das ist 3,35 m2, passt zu 1680 l bei 0,50 m Tiefe (A22 der Quelle).
  * Kuppelmitte (500, 480) = Modell (0, 0). Zeichnung-oben = Modell +Y (Norden), Zeichnung-rechts = Modell +X; die Technik der
    Zeichnung liegt unten = Modell -Y, wie die Technik-Sektoren des Modells (Az -90 bis -18). Keine Spiegelung.
  * Fussboden der Quelle (Oberkante Bodenplatte, A25) = Modell-Z 400 mm (FUSSBODEN_Z_MM; `viewer/instances.json` walk_z = 400,
    Tische/Tanks/Pumpen stehen bei Z 400). Auftrag nannte Z 0: das ist die Unterkante des Sockels, nicht der begehbare Boden.
    Alle `z_modell_mm` = 400 + Hoehe ueber Fussboden. Eine Zahl aendern genuegt, falls Ben anders entscheidet.
  * Drehung +18 Grad (DREHUNG_GRAD, ANNAHME): Die Quelle hat das Zehneck so gedreht, dass die zwei Kupplungsstrecken auf der Achse
    liegen, und die Winkel aus Bens Konzept nicht uebernommen (A16). Das Ring-B2-Modell hat die Ecken bei Az 18 + 36 k (Tisch-Zulaeufe
    an den Sektorgrenzen) und die Kupplungsstrecken bei Az 108 und -72; das ist genau die Zeichnung, um +18 Grad gedreht (Pruefung unten).
    Die Zeichnung zeigt ihre Koordinaten weiter unveraendert in `zeichnung`/`d`.
  * Die Zeichnung ist an Becken, Filtern und Rohrfuehrung schematisch (A16): Mittelpunkte und Reihenfolge gelten, Rohrverlaeufe
    sind Verbindungen, keine Trassen. Wo die Quelle Masse nennt (A26 Fischtank 4 m x 2,2 m, Anzucht 2 m x 1 m, Futterbecken 1 m x 1 m),
    stehen sie als `masse_text_mm` und gehen der Zeichnungsgroesse vor.
"""
import hashlib
import html
import json
import math
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
Q1 = os.path.join(ROOT, "docs", "quellen", "oasis-showcase-2026-11-10")
Q2 = os.path.join(ROOT, "docs", "quellen", "oasis-showcase-2026-11-10-nachtrag")
INDEX = os.path.join(Q1, "index.html")
FLOW = os.path.join(Q2, "flow-diagram.html")
OUT = os.path.join(ROOT, "data", "oasis-soll.json")

SHA = {"index.html": "37c1a78f1dcd685891512bf297648705633e6359591b6228d0a76d1bcf552dcc",
       "flow-diagram.html": "68e35886735e0c544c2439aa845c7db0a691815921197f6b795ed7259dca1799"}
MM_JE_EINHEIT = 12.5
MITTE = (500.0, 480.0)
KUPPEL_R_MM = 6000
FUSSBODEN_Z_MM = 400
DREHUNG_GRAD = 18.0   # ANNAHME D95: Zeichnung -> Modell um +18 Grad (CCW) gedreht; Begruendung im Kopf und in R61 Abschnitt 5

# Kurzrolle je Bauteil (eigene Worte, ein Satz); die Quelltexte stehen unveraendert in `beschreibung`.
ROLLE = {
    "rain": "Regenwassertank (Zisterne): erste Wahl der Nachspeisung",
    "tap": "Frischwasseranschluss: zweite Wahl der Nachspeisung",
    "nachspeise": "mechanisches Schwimmerventil am Fischtank: Regenwasser vor Frischwasser, schuetzt vor Ueberfuellen",
    "pv": "Solaranlage (Strom, ausserhalb des Wasserkreislaufs)",
    "battery": "Batteriespeicher (Strom, ausserhalb des Wasserkreislaufs)",
    "control": "Steuerung: schaltet Pumpen, Belueftung, nimmt Schwimmer-Meldungen an (Strom, Referenz)",
    "fish": "Haupt-Fischtank: Start und tiefster Punkt des Kreislaufs, teilversenkt, 22 m3",
    "nursery": "Anzuchtbecken (mittlerer Beckenring): Ueberlauf vom Lebendfutterbecken in den Fischtank",
    "feed": "Lebendfutterbecken (aeusserer Beckenring): bekommt Biofilterwasser, Ueberlauf in das Anzuchtbecken",
    "filterpumpe_1": "Pumpstelle 1, Linie 1: hebt vom Fischtank in Vortex 1 (+1,15 m), mit Rueckschlagventil",
    "filterpumpe_2": "Pumpstelle 1, Linie 2: hebt vom Fischtank in Vortex 2 (+1,15 m), mit Rueckschlagventil",
    "vortex_1": "Wirbelabscheider Linie 1: Feststoffe in den Schlammreaktor, Ueberlauf per Schwerkraft in Biofilter 1",
    "vortex_2": "Wirbelabscheider Linie 2: Feststoffe in den Schlammreaktor, Ueberlauf per Schwerkraft in Biofilter 2",
    "bio_1": "Biofilter Linie 1: speist Halbring 1, Lebendfutterbecken und per Notueberlauf den Sumpf 1",
    "bio_2": "Biofilter Linie 2: speist Halbring 2 und per Notueberlauf den Sumpf 2",
    "sludge_1": "Sammelbehaelter fuer Schlamm Linie 1 mit Ablasshahn von Hand, ausserhalb des Wasserkreislaufs",
    "sludge_2": "Sammelbehaelter fuer Schlamm Linie 2 mit Ablasshahn von Hand, ausserhalb des Wasserkreislaufs",
    "permakultur": "Schlamm-Senke: Permakultur und Futterzucht, kein Rueckweg ins Wasser",
    "ring_1": "Halbring 1 der Wasserautobahn (haengende Verteilleitung d75, reine Zufuhr)",
    "ring_2": "Halbring 2 der Wasserautobahn (haengende Verteilleitung d75, reine Zufuhr)",
    "kupplungshahn": "zwei Kugelhaehne d63 in den Kupplungsstrecken, im Betrieb offen: beide Halbringe = ein Ring",
    "ringende_1": "Ablassstelle von Halbring 1 in den Sumpf 1 (Ueberschuss 17,5 l/min)",
    "ringende_2": "Ablassstelle von Halbring 2 in den Sumpf 2 (Ueberschuss 17,5 l/min)",
    "abf_nft_1": "12 NFT-Abfahrten d32 vom Halbring 1 (Aussen 4, Mitte 3, Innen 5), 38 l/min",
    "abf_fd_1": "7 Flood-and-Drain-Abfahrten d40 vom Halbring 1 (Aussen 4, Mitte 3), 54,5 l/min",
    "abf_nft_2": "12 NFT-Abfahrten d32 vom Halbring 2 (Aussen 4, Mitte 3, Innen 5), 38 l/min",
    "abf_fd_2": "7 Flood-and-Drain-Abfahrten d40 vom Halbring 2 (Aussen 4, Mitte 3), 54,5 l/min",
    "nft_aussen": "NFT-Tische Anbauring Aussen (8), Rinnenwasser 1,05 m, Ablauf in die Sumpftanks",
    "fd_aussen": "Flood-and-Drain-Substratbeete Anbauring Aussen (8, je ein Siphon), Flutstand 0,25 m, Ablauf in die Sumpftanks",
    "nft_mitte": "NFT-Tische Anbauring Mitte (6), Rinnenwasser 0,90 m, Ablauf in die Sumpftanks",
    "fd_mitte": "Flood-and-Drain-Substratbeete Anbauring Mitte (6, je ein Siphon), Flutstand 0,25 m, Ablauf in die Sumpftanks",
    "nft_innen": "NFT-Tische Anbauring Innen (10) auf dem Poolrand, Rinnenwasser 1,25 m, Ablauf direkt in den Fischtank",
    "sump_1": "Sumpftank 1 im Boden (begehbarer Deckel): Sammelpunkt der Ruecklaeufe Linie 1, 4 Pufferzonen",
    "sump_2": "Sumpftank 2 im Boden (begehbarer Deckel): Sammelpunkt der Ruecklaeufe Linie 2, 4 Pufferzonen",
    "hauptpumpe_1": "Pumpstelle 2, Linie 1: hebt vom Sumpf 1 durch den Venturi in den Fischtank (+1,00 m), mit Rueckschlagventil",
    "hauptpumpe_2": "Pumpstelle 2, Linie 2: hebt vom Sumpf 2 durch den Venturi in den Fischtank (+1,00 m), mit Rueckschlagventil",
    "venturi_1": "passiver Venturi-Belueffter im Druckrohr vor dem Einlauf in den Fischtank, Linie 1",
    "venturi_2": "passiver Venturi-Belueffter im Druckrohr vor dem Einlauf in den Fischtank, Linie 2",
    "schwimmer_1": "Hochstand-Schwimmerschalter im Sumpf 1: schaltet ueber die Steuerung die Pumpe Fischtank->Filter 1 ab",
    "schwimmer_2": "Hochstand-Schwimmerschalter im Sumpf 2: schaltet ueber die Steuerung die Pumpe Fischtank->Filter 2 ab",
    "luftpumpe": "Notluftpumpe mit Luftstein im Fischtank, startet bei Ausfall der Wasserpumpen oder des Netzes",
    "luftpumpe_1": "Belueftungsanlage Linie 1 (Alternative zu Venturi, gestrichelt): 4 Luftarme zu Biofilter 1, Sumpf 1, Anzucht, Fischtank",
    "luftpumpe_2": "Belueftungsanlage Linie 2 (Alternative zu Venturi, gestrichelt): 4 Luftarme zu Biofilter 2, Sumpf 2, Futterbecken, Fischtank",
}
# Masse, die die Quelle im Text nennt (A22, A26); Durchmesser/Tiefe in mm.
MASSE_TEXT = {
    "fish": {"durchmesser": 4000, "tiefe_gesamt": 2200, "im_boden": 1000, "quelle": "A26 (Wasserspiegel 0,75 m = 22 m3, 1,75 m Wassertiefe)"},
    "nursery": {"durchmesser": 2000, "tiefe_gesamt": 1000, "im_boden": 0, "quelle": "A26 (steht auf dem Boden)"},
    "feed": {"durchmesser": 1000, "tiefe_gesamt": 1000, "im_boden": 0, "quelle": "A26 (steht auf dem Boden)"},
    "sump_1": {"inhalt_l": 1680, "soll_inhalt_l": 850, "quelle": "A22 (Boden -0,50 m, Rand 0,00 m, Soll-Pegel -0,25 m)"},
    "sump_2": {"inhalt_l": 1680, "soll_inhalt_l": 850, "quelle": "A22 (Boden -0,50 m, Rand 0,00 m, Soll-Pegel -0,25 m)"},
}
# Rohrnennweiten, die die Quelle nennt: Wegnummer -> (Text, Fundstelle im Quelltext). `quelle_text` muss im Quelltext vorkommen (Pruefung).
NENNWEITE = {
    "e25": ("d63", "Einspeise-Anschluss d63 vom Biofilter"), "e26": ("d63", "Einspeise-Anschluss d63 vom Biofilter"),
    "e27": ("d63 (Kugelhahn), Ring d75", "2 Kugelhähne d63 in den 2 Kupplungsstrecken"),
    "e28": ("d63 (Kugelhahn), Ring d75", "2 Kugelhähne d63 in den 2 Kupplungsstrecken"),
    "e29": ("d63 (Kugelhahn), Ring d75", "2 Kugelhähne d63 in den 2 Kupplungsstrecken"),
    "e30": ("d63 (Kugelhahn), Ring d75", "2 Kugelhähne d63 in den 2 Kupplungsstrecken"),
    "e31": ("d63", "Kugelhahn d63"), "e32": ("d63", "Kugelhahn d63"),
    "e35": ("d32", "Abzweig-Kugelhahn d32"), "e37": ("d32", "Abzweig-Kugelhahn d32"),
    "e36": ("d40", "Abzweig-Kugelhahn d40"), "e38": ("d40", "Abzweig-Kugelhahn d40"),
    "e39": ("Schlauch ID19", "Schlauch-Fallleitung ID19"), "e40": ("Schlauch ID19", "Schlauch-Fallleitung ID19"),
    "e41": ("Schlauch ID19", "Schlauch-Fallleitung ID19"), "e44": ("Schlauch ID19", "Schlauch-Fallleitung ID19"),
    "e45": ("Schlauch ID19", "Schlauch-Fallleitung ID19"), "e46": ("Schlauch ID19", "Schlauch-Fallleitung ID19"),
    "e42": ("Schlauch ID25", "Schlauch-Fallleitung ID25"), "e43": ("Schlauch ID25", "Schlauch-Fallleitung ID25"),
    "e47": ("Schlauch ID25", "Schlauch-Fallleitung ID25"), "e48": ("Schlauch ID25", "Schlauch-Fallleitung ID25"),
}
# Durchfluss in l/min, den die Quelle nennt (Kantentext oder Bauteilfeld `durchfluss`); abgeleitete Werte stehen getrennt.
DURCHFLUSS = {"e25": 110, "e26": 110, "e31": 17.5, "e32": 17.5, "e35": 38, "e37": 38, "e36": 54.5, "e38": 54.5}

PRUEF = []


def pruefe(name, ok, detail=""):
    PRUEF.append({"pruefung": name, "ok": bool(ok), "detail": detail})
    return ok


def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def sha_passt(p, erwartet):
    """SHA256 der Datei; ein Windows-Checkout mit autocrlf aendert nur die Zeilenenden, nicht den Inhalt: roh, LF und CRLF werden geprueft."""
    roh = open(p, "rb").read()
    lf = roh.replace(bytes([13, 10]), bytes([10]))
    kandidaten = {hashlib.sha256(x).hexdigest() for x in (roh, lf, lf.replace(bytes([10]), bytes([13, 10])))}
    return erwartet in kandidaten


def mm(x, y):
    """Zeichnungseinheiten -> Modell-Millimeter (X rechts, Y oben = Norden), um DREHUNG_GRAD gedreht."""
    dx, dy = (x - MITTE[0]) * MM_JE_EINHEIT, -(y - MITTE[1]) * MM_JE_EINHEIT
    c, s_ = math.cos(math.radians(DREHUNG_GRAD)), math.sin(math.radians(DREHUNG_GRAD))
    return round(dx * c - dy * s_, 1) + 0.0, round(dx * s_ + dy * c, 1) + 0.0


def polar(xm, ym):
    return {"r_mm": round(math.hypot(xm, ym), 1) + 0.0, "az_grad": round(math.degrees(math.atan2(ym, xm)), 2) + 0.0}


def pt(x, y):
    xm, ym = mm(x, y)
    return {"zeichnung": [round(x, 2), round(y, 2)], "x_mm": xm, "y_mm": ym, **polar(xm, ym)}


def zahlen(s):
    return [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", s)]


def pfad_punkte(d):
    """Ecken eines SVG-Pfads (absolut M/L/H/V/Q/A/C, relativ a/q/l/m/h/v): Q-Kontrollpunkt = Ecke, A/C/L/M = Endpunkt."""
    out, cur, start = [], (0.0, 0.0), None
    for cmd, args in re.findall(r"([MLHVQACZmlhvqacz])([^MLHVQACZmlhvqacz]*)", d):
        a = zahlen(args)
        rel = cmd.islower()
        c = cmd.upper()
        if c == "Z":
            continue
        if c in "ML":
            for i in range(0, len(a) - 1, 2):
                cur = (cur[0] + a[i], cur[1] + a[i + 1]) if rel else (a[i], a[i + 1])
                out.append(cur)
        elif c == "H":
            cur = (cur[0] + a[0] if rel else a[0], cur[1]); out.append(cur)
        elif c == "V":
            cur = (cur[0], cur[1] + a[0] if rel else a[0]); out.append(cur)
        elif c == "Q":
            for i in range(0, len(a) - 3, 4):
                k = (cur[0] + a[i], cur[1] + a[i + 1]) if rel else (a[i], a[i + 1])
                e = (cur[0] + a[i + 2], cur[1] + a[i + 3]) if rel else (a[i + 2], a[i + 3])
                out.append(k); cur = e
        elif c == "A":
            for i in range(0, len(a) - 6, 7):
                cur = (cur[0] + a[i + 5], cur[1] + a[i + 6]) if rel else (a[i + 5], a[i + 6]); out.append(cur)
        elif c == "C":
            for i in range(0, len(a) - 5, 6):
                cur = (cur[0] + a[i + 4], cur[1] + a[i + 5]) if rel else (a[i + 4], a[i + 5]); out.append(cur)
    return out


def klasse(e):
    return (e.get("class") or "").split()


def transl(g):
    m = re.search(r"translate\(([-\d.]+)[ ,]([-\d.]+)\)(?: rotate\(([-\d.]+)\))?", g.get("transform", ""))
    return (float(m.group(1)), float(m.group(2)), float(m.group(3) or 0)) if m else None


def teil_geometrie(p):
    """Primitive eines Plan-Teils (g.part) in Modell-mm."""
    prim, symbole = [], []
    for e in p.iter():
        t = e.tag.split("}")[-1]
        k = klasse(e)
        if "hit" in k or "ground-hatch" in k:
            continue
        if t == "circle" and ("sbody" in k or "base" in k):
            kind = "kreis" if "sbody" in k else "abzweig"
            cx, cy, r = float(e.get("cx")), float(e.get("cy")), float(e.get("r"))
            d = pt(cx, cy)
            if kind == "kreis":
                d.update({"typ": "kreis", "radius_zeichnung": r, "radius_mm": round(r * MM_JE_EINHEIT, 1)})
            else:
                d.update({"typ": "abzweig_punkt"})
            prim.append(d)
        elif t == "rect" and "sbody" in k:
            x, y, w, h = (float(e.get(v)) for v in ("x", "y", "width", "height"))
            d = pt(x + w / 2, y + h / 2)
            d.update({"typ": "rechteck", "breite_mm": round(w * MM_JE_EINHEIT, 1), "hoehe_mm": round(h * MM_JE_EINHEIT, 1),
                      "zeichnung_rect": [x, y, w, h]})
            prim.append(d)
        elif t == "path" and ("lane" in k or "road" in k):
            dd = e.get("d")
            pts = pfad_punkte(dd)
            d = {"typ": "bogen" if "lane" in k else "linienzug", "d": dd, "punkte": [pt(x, y) for x, y in pts]}
            m = re.search(r"A\s*([\d.]+)", dd)
            if "lane" in k and m:
                d["radius_zeichnung"] = float(m.group(1)); d["radius_mm"] = round(float(m.group(1)) * MM_JE_EINHEIT, 1)
                d["mittelpunkt_zeichnung"] = list(MITTE)
                a0, a1 = d["punkte"][0]["az_grad"], d["punkte"][-1]["az_grad"]
                d["von_az_grad"], d["bis_az_grad"] = a0, a1
                d["offener_winkel_grad"] = round(360 - abs(a1 - a0), 1) if abs(a1 - a0) > 180 else round(abs(a1 - a0), 1)
                d["bogen_hinweis"] = "Zeichnung: Bogen mit Oeffnung nach unten (Sueden), schematisch (A16); Tisch-/Beetlage gilt nach Modell (A25)"
            prim.append(d)
        elif t == "path" and ("valve" in k or "venturi" in k) and "sbody" in k:
            xs = zahlen(e.get("d"))[0::2]; ys = zahlen(e.get("d"))[1::2]
            d = pt(sum(xs) / len(xs) if "valve" not in k else (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
            d["typ"] = "venturi" if "venturi" in k else "ventil"; symbole.append(d)
        elif t == "ellipse" and "floatsw" in k:
            d = pt(float(e.get("cx")), float(e.get("cy"))); d["typ"] = "schwimmerschalter"; symbole.append(d)
        elif t == "g" and "rvg" in k:
            tr = transl(e)
            if tr:
                d = pt(tr[0], tr[1]); d["typ"] = "rueckschlagventil"; d["drehung_grad"] = tr[2]; symbole.append(d)
        elif t == "g" and "sipg" in k:
            tr = transl(e)
            if tr:
                d = pt(tr[0], tr[1]); d["typ"] = "siphon"; symbole.append(d)
        elif t == "g" and e.get("data-pufferzone"):
            r = e.find("rect"); ti = e.find("title")
            x, y, w, h = (float(r.get(v)) for v in ("x", "y", "width", "height"))
            d = pt(x + w / 2, y + h / 2); d.update({"typ": "pufferzone", "nummer": int(e.get("data-pufferzone")), "text": ti.text if ti is not None else ""})
            symbole.append(d)
        elif t == "path" and "pump-tri" in k:
            pass
    return prim, symbole


def zentrum_von(prim, symb):
    """Mittelpunkt eines Teils in Modell-mm: Kreis/Rechteck = Mitte, Bogen = Kuppelmitte (mit Radius), Linienzug/Punkte/Symbole = Schwerpunkt."""
    if not prim and not symb:
        return None
    p0 = prim[0] if prim else symb[0]
    if p0["typ"] in ("kreis", "rechteck"):
        return {"x_mm": p0["x_mm"], "y_mm": p0["y_mm"], **polar(p0["x_mm"], p0["y_mm"])}
    if p0["typ"] == "bogen":
        return {"x_mm": 0.0, "y_mm": 0.0, "r_mm": 0.0, "az_grad": None}
    if not prim and len(symb) > 1:
        return None
    punkte = [q for q in prim if "x_mm" in q] + [q for q in symb if "x_mm" in q]
    if p0["typ"] == "linienzug":
        punkte = p0["punkte"]
    if not punkte:
        return None
    x = round(sum(q["x_mm"] for q in punkte) / len(punkte), 1); y = round(sum(q["y_mm"] for q in punkte) / len(punkte), 1)
    return {"x_mm": x, "y_mm": y, **polar(x, y)}


def lade_plan():
    L = lies(INDEX).split("\n")
    a = next(i for i, l in enumerate(L) if ">>> SOLL-DRAUFSICHT" in l)
    b = next(i for i, l in enumerate(L) if "<<< SOLL-DRAUFSICHT" in l)
    frag = re.sub(r"<!--.*?-->", "", "\n".join(L[a:b + 1]), flags=re.S)
    root = ET.fromstring("<root>" + frag + "</root>")
    plan = next(g for g in root if g.get("id") == "soll-plan")
    profil = next(g for g in root if g.get("id") == "soll-profile")
    teile, kanten = {}, {}
    for g in plan:
        if "node-group" in klasse(g):
            for p in g:
                if "part" in klasse(p):
                    teile[p.get("data-part")] = (g.get("data-node"), p)
    for e in plan.iter():
        if "flow-path" in klasse(e) and e.get("data-edge"):
            kanten[e.get("data-edge")] = e
    return teile, kanten, profil


def lade_json(blk):
    m = re.search(r'<script type="application/json" id="%s">(.*?)</script>' % blk, lies(FLOW), re.S)
    return json.loads(m.group(1))


def lade_index_js():
    """sollStufen und sollWasserspiegel (JSON-Literale) und nodeDatabase (per node ausgewertet)."""
    t = lies(INDEX)
    stufen = json.loads(re.search(r"const sollStufen = (\{.*?\});", t).group(1))
    wsp = json.loads(re.search(r"const sollWasserspiegel = (\{.*?\});", t).group(1))
    a = t.index("let simVariables"); b = t.index("// <<< SOLL-BAUTEILE")
    js = ("const fs=require('fs');const src=fs.readFileSync(process.argv[1],'utf8');"
          "const a=src.indexOf('let simVariables'),b=src.indexOf('// <<< SOLL-BAUTEILE');"
          "const r=new Function(src.slice(a,b)+';return {nodeDatabase,simVariables};')();const o={};"
          "for(const [k,v] of Object.entries(r.nodeDatabase)){let m={};try{m=v.getMetrics(r.simVariables)}catch(e){m={fehler:e.message}}"
          "o[k]={name:v.name,desc:v.desc,kennzahlen:m};}console.log(JSON.stringify(o));")
    try:
        res = subprocess.run(["node", "-e", js, INDEX], capture_output=True, text=True, encoding="utf-8", timeout=60)
        nd = json.loads(res.stdout) if res.returncode == 0 else {}
    except (OSError, ValueError, subprocess.SubprocessError):
        nd = {}
    return stufen, wsp, nd


def meter(s):
    """'0,75 m über dem Fußboden' / '−0,25 m ...' / '0,90 bis 1,25 m ...' -> (min_mm, max_mm)"""
    s = s.replace("−", "-").replace(",", ".")
    v = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", s)[:2]]
    return round(min(v) * 1000), round(max(v) * 1000)


def klasse_armatur(text):
    """Art der Zeile aus `teile` der Quelle; die Reihenfolge der Schluessel ist wichtig (spezifisch vor allgemein)."""
    t = text.lower()
    for key, typ in (("rückschlag", "rueckschlagventil"), ("regelhahn", "regelhahn"), ("ablasshahn", "ablasshahn"),
                     ("entleerungshahn", "entleerungshahn"), ("kugelhahn", "kugelhahn"), ("kugelhähne", "kugelhahn"),
                     ("entlüfter", "entlueffter"), ("abtropfgitter", "abtropfgitter"), ("vlies", "vlies_sieb"),
                     ("etwas belüftung", "belueftung_beet"), ("siphon", "siphon"), ("schwimmerschalter (hochstand)", "schwimmerschalter"),
                     ("schwimmerschalter für", "schwimmerschalter"), ("schwimmerventil", "schwimmerventil"), ("trockenlaufschutz", "schwimmerventil"),
                     ("luftpumpe", "luftpumpe"), ("luftverteiler", "luftverteiler"), ("luftstein", "luftstein"), ("luftleitung", "luftleitung"),
                     ("lufteinlass", "lufteinlass"), ("venturi-injektor", "venturi_injektor"), ("schnellkupplung", "schnellkupplung"),
                     ("reduzierung", "reduzierung"), ("t-stück", "t_stueck"), ("tülle", "schlauchtuelle"), ("schlauch-fall", "schlauch"),
                     ("muffe", "endstueck"), ("klemmverbinder", "endstueck"), ("pufferzone", "pufferzone"), ("meldeleitung", "meldeleitung"),
                     ("ring d75", "rohr"), ("anschluss", "anschluss"), ("pumpe(n)", "pumpe"), ("saugseite", "beschreibung"),
                     ("sammelbehälter", "behaelter"), ("offen", "offene_angabe"), ("hahn", "kugelhahn")):
        if key in t:
            return typ
    return "sonstiges"


# Zeilen, die keine eigene Stueckzahl tragen: Beschreibung des Bauteils selbst, offene Angabe, Behaelter, Pumpe (= das Bauteil)
NICHT_ZAEHLEN = {"pumpe", "luftpumpe", "beschreibung", "offene_angabe", "behaelter", "sonstiges"}
# der Schwimmerschalter steht im Sumpf-Text UND als eigenes Bauteil: nur das eigene Bauteil zaehlt
DOPPELT = {("sump_1", "schwimmerschalter"): "schwimmer_1", ("sump_2", "schwimmerschalter"): "schwimmer_2"}


def baue():
    teile, kanten_plan, profil = lade_plan()
    fd, sd = lade_json("flow-data"), lade_json("schema-data")
    stufen_i, wsp_i, nd = lade_index_js()
    nodes = {n["id"]: n for n in fd["nodes"]}
    kanten = {e["id"]: e for e in fd["edges"]}
    flow_text = lies(FLOW)

    # --- Pruefung 1: Quelldateien unveraendert
    for name, p in (("index.html", INDEX), ("flow-diagram.html", FLOW)):
        pruefe("SHA256 " + name + " (Zeilenenden egal)", sha_passt(p, SHA[name]), SHA[name])

    # --- Pruefung 2: Bauteile <-> Plan-Teile, Kanten <-> Plan-Kanten
    pruefe("43 Bauteile in flow-data", len(nodes) == 43, str(len(nodes)))
    fehlt = sorted(set(nodes) - set(teile)); extra = sorted(set(teile) - set(nodes))
    pruefe("jedes Bauteil hat ein Teil in der Draufsicht", not fehlt and not extra, "fehlt %s, extra %s" % (fehlt, extra))
    pruefe("90 Wege in flow-data", len(kanten) == 90, str(len(kanten)))
    pruefe("Wege der Draufsicht = Wege in flow-data", set(kanten_plan) == set(kanten),
           "nur Plan %s, nur Daten %s" % (sorted(set(kanten_plan) - set(kanten)), sorted(set(kanten) - set(kanten_plan))))
    diff = [k for k, e in kanten_plan.items() if k in kanten and (e.get("data-from") != kanten[k]["from"] or e.get("data-to") != kanten[k]["to"]
                                                               or e.get("data-medium") != kanten[k]["medium"])]
    pruefe("Wege: von/nach/Medium stimmen in Zeichnung und Daten", not diff, str(diff))

    # --- Pruefung 3: Stufen und Wasserspiegel in beiden Dateien gleich
    sn = sd["showcaseNode"]
    ab = [i for i, s in sd["stufen"].items() if i in sn and sn[i] in stufen_i and "Stufe %d " % s["stufe"] != stufen_i[sn[i]][:8]]
    pruefe("Stufen: index.html (sollStufen) = flow-diagram.html (schema-data)", not ab, str(ab))
    ab2 = []
    for i, s in sd["stufen"].items():
        if s.get("wsp") is None or i not in sn or sn[i] not in wsp_i:
            continue
        lo, hi = meter(wsp_i[sn[i]])
        if not (lo <= round(s["wsp"] * 1000) <= hi):
            ab2.append(i)
    pruefe("Wasserspiegel: index.html (sollWasserspiegel) = flow-diagram.html (schema-data)", not ab2, str(ab2))

    # --- Bauteile
    bauteile, armaturen = [], []
    for nid, n in nodes.items():
        st = sd["stufen"].get(nid)
        prim, symb = teil_geometrie(teile[nid][1]) if nid in teile else ([], [])
        zentrum = zentrum_von(prim, symb)
        z = {}
        wsp_mm = None
        if st:
            wsp_mm = round(st["wsp"] * 1000) if st.get("wsp") is not None else None
            for feld in ("wsp", "boden", "rand", "hochstand"):
                if st.get(feld) is not None:
                    z[feld + "_ueber_fussboden_mm"] = round(st[feld] * 1000)
                    z[feld + "_z_modell_mm"] = FUSSBODEN_Z_MM + round(st[feld] * 1000)
        lage = {"zeichnung_primitive": prim, "symbole": symb, "ausserhalb_kuppel": bool(zentrum and zentrum["r_mm"] > KUPPEL_R_MM)}
        if zentrum:
            lage["mittelpunkt_x_mm"] = zentrum["x_mm"]; lage["mittelpunkt_y_mm"] = zentrum["y_mm"]
            lage["mittelpunkt_r_mm"] = zentrum["r_mm"]; lage["mittelpunkt_az_grad"] = zentrum["az_grad"]
        if prim and prim[0]["typ"] == "abzweig_punkt":
            lage["abzweige"] = [p for p in prim if p["typ"] == "abzweig_punkt"]
        if prim and prim[0]["typ"] == "bogen":
            lage["bogen_radius_mm"] = prim[0]["radius_mm"]; lage["offener_winkel_grad"] = prim[0]["offener_winkel_grad"]
        ndx = nd.get(sn.get(nid, nid), {})
        im_umfang = n["kind"] not in ("energie",) and nid not in ("control",)
        b = {
            "id": nid, "name": n["label"], "gruppe": n["group"], "art": n["kind"], "herkunft_in_quelle": n["origin"],
            "im_umfang": im_umfang,
            "umfang_hinweis": "" if im_umfang else "Strom/Steuerung: nur Referenz fuer Pumpen, Belueftung, Schwimmer (Auftrag: Strom nur soweit er Wasser-Bauteile betrifft)",
            "rolle": ROLLE.get(nid, ""), "beschreibung": n.get("beschreibung", ""),
            "wasserkreislauf": n["kind"] in ("source", "armatur", "becken", "pumpe", "filter", "ring", "abfahrt", "verbraucher", "sumpf") and nid not in ("luftpumpe", "luftpumpe_1", "luftpumpe_2", "pv", "battery", "control"),
            "medium_bereich": "luft" if nid.startswith("luftpumpe") else ("schlamm" if n["kind"] in ("speicher", "sink") else ("strom" if n["kind"] in ("energie", "steuerung") else "wasser")),
            "anzahl": n.get("count", 1), "linie": n.get("linie"), "halbring": n.get("halbring"), "modul": n.get("modul"),
            "zonen": n.get("zonen"),
            "stufe": st["stufe"] if st else None, "stufe_festgelegt": (not st.get("offen")) if st else None,
            "stufe_status": ("ohne Hoehenangabe (Quelle: Hoehe nicht festgelegt)" if not st else ("nicht festgelegt" if st.get("offen") else "festgelegt")),
            "stufe_grund": st["grund"] if st else "",
            "wasserspiegel_ueber_fussboden_mm": wsp_mm,
            "wasserspiegel_status": ("festgelegt (Vorschlag A25, einstellbar)" if wsp_mm is not None else "nicht festgelegt"),
            "wasserspiegel_grund": (st.get("wspGrund") or "") if st else "",
            "hoehen": z, "masse_text_mm": MASSE_TEXT.get(nid),
            "durchfluss_l_min": n.get("durchfluss"), "nennweite": n.get("nennweite"), "regler": n.get("regler"),
            "teile": n.get("teile") or [],
            "kennzahlen_index": ndx.get("kennzahlen", {}), "beschreibung_index": ndx.get("desc", ""),
            "lage": lage,
            "wege_ein": sorted(e for e, v in kanten.items() if v["to"] == nid),
            "wege_aus": sorted(e for e, v in kanten.items() if v["from"] == nid),
        }
        bauteile.append(b)
        # Armaturen und Zubehoer: je Zeile `teile` der Quelle eine Zeile (Text unveraendert)
        mult = n.get("count", 1) if n["kind"] in ("abfahrt", "verbraucher") else 1
        for i, tx in enumerate(n.get("teile") or []):
            m = re.match(r"(\d+)\s*[x×]?\s", tx)
            je = int(m.group(1)) if m else 1
            typ = klasse_armatur(tx)
            sym = [s for s in symb if s["typ"] == {"rueckschlagventil": "rueckschlagventil", "siphon": "siphon", "schwimmerschalter": "schwimmerschalter",
                                                     "kugelhahn": "ventil", "venturi_injektor": "venturi", "pufferzone": "pufferzone"}.get(typ, "-")]
            zaehlt = typ not in NICHT_ZAEHLEN and (nid, typ) not in DOPPELT
            armaturen.append({"id": "%s.t%d" % (nid, i + 1), "an_bauteil": nid, "typ": typ, "text_quelle": tx,
                              "anzahl_je_einheit": je, "einheiten": mult, "anzahl_gesamt": je * mult if zaehlt else 0,
                              "zaehlt": zaehlt, "zaehlt_nicht_weil": ("" if zaehlt else ("steht als eigenes Bauteil " + DOPPELT[(nid, typ)] if (nid, typ) in DOPPELT else "Beschreibung/offene Angabe/Bauteil selbst")),
                              "einheit_art": "je Abzweig/Beet" if mult > 1 else "je Bauteil", "lage_symbole": sym})
    # Armaturen, die nur die Zeichnung zeigt (Symbol ohne eigene Zeile in `teile`)
    for b in bauteile:
        if b["id"] in ("nachspeise",):
            armaturen.append({"id": "nachspeise.t0", "an_bauteil": "nachspeise", "typ": "schwimmerventil",
                              "text_quelle": "Mechanisches Schwimmerventil am Fischtank: gibt Regenwasser zuerst frei, Frischwasser nur nachrangig (nodeDatabase.nachspeise.desc)",
                              "anzahl_je_einheit": 1, "einheiten": 1, "anzahl_gesamt": 1, "zaehlt": True, "zaehlt_nicht_weil": "", "einheit_art": "je Bauteil", "lage_symbole": b["lage"]["symbole"]})
        for s in b["lage"]["symbole"]:
            if s["typ"] == "siphon" and b["id"] in ("fd_aussen", "fd_mitte"):
                pass
    # --- Wege
    wege = []
    for eid, e in kanten.items():
        pe = kanten_plan.get(eid)
        pfad = []
        if pe is not None and pe.get("d"):
            pfad = [pt(x, y) for x, y in pfad_punkte(pe.get("d"))]
        elif pe is not None:
            pfad = [pt(float(l.get("x1")), float(l.get("y1"))) for l in pe.iter("line")]
        nw = NENNWEITE.get(eid)
        bauteil_von, bauteil_nach = nodes[e["from"]], nodes[e["to"]]
        wege.append({
            "id": eid, "von": e["from"], "nach": e["to"], "medium": e["medium"], "label": e["label"], "optional": bool(e.get("optional")),
            "im_umfang": e["medium"] in ("water", "air", "sludge") or e["to"] in ("filterpumpe_1", "filterpumpe_2", "hauptpumpe_1", "hauptpumpe_2", "luftpumpe", "luftpumpe_1", "luftpumpe_2") or e["from"] in ("schwimmer_1", "schwimmer_2"),
            "antrieb": sd["antrieb"].get(eid) or ("Strom" if e["medium"] == "power" else None),
            "antrieb_text": sd["antriebNamen"].get(sd["antrieb"].get(eid), ""),
            "nennweite": nw[0] if nw else None, "nennweite_status": "Quelle" if nw else "nicht festgelegt",
            "nennweite_quelle_text": nw[1] if nw else "",
            "durchfluss_l_min": DURCHFLUSS.get(eid), "durchfluss_status": "Quelle" if eid in DURCHFLUSS else "nicht festgelegt",
            "stueckzahl": (bauteil_von.get("count") if bauteil_von["kind"] == "abfahrt" and bauteil_nach["kind"] == "verbraucher" else None),
            "pfad_zeichnung_d": pe.get("d") if pe is not None else None,
            "pfad_punkte": pfad,
            "pfad_schematisch": True,
        })
    # Fallleitungen: Anzahl je Weg steht im Label ("4 × Fallleitung ID19")
    for w in wege:
        m = re.match(r"(\d+) ×", w["label"])
        if m:
            w["stueckzahl"] = int(m.group(1))
        if w["id"] in ("e39", "e40", "e41", "e42", "e43", "e44", "e45", "e46", "e47", "e48"):
            w["durchfluss_l_min_abgeleitet"] = round((38 if w["nennweite"] == "Schlauch ID19" else 54.5) * w["stueckzahl"] / (12 if w["nennweite"] == "Schlauch ID19" else 7), 2)
            w["durchfluss_status"] = "abgeleitet: Halbring-Menge anteilig nach Abnehmerzahl (A12, A6; keine Quellzahl)"
    # Quelltext-Belege der Nennweiten
    pruefe("Nennweiten: jeder Beleg steht im Quelltext", all(html.unescape(t[1]) in flow_text or t[1] in flow_text for t in NENNWEITE.values()),
           str([k for k, t in NENNWEITE.items() if t[1] not in flow_text]))

    # --- Inhaltliche Pruefungen (Rechnung, keine Zahlen aus der Erinnerung)
    ring = nodes["ring_1"]["durchfluss"]; an = nodes["abf_nft_1"]["durchfluss"]; af = nodes["abf_fd_1"]["durchfluss"]; re_ = nodes["ringende_1"]["durchfluss"]
    pruefe("Mengenbilanz je Halbring: 110 = 38 + 54,5 + 17,5", abs(ring - (an + af + re_)) < 1e-9, "%s = %s + %s + %s" % (ring, an, af, re_))
    nft = sum(nodes[i]["count"] for i in ("nft_aussen", "nft_mitte", "nft_innen")); fdb = sum(nodes[i]["count"] for i in ("fd_aussen", "fd_mitte"))
    pruefe("Abnehmer: 2 x 12 NFT-Abfahrten = 24 = 8 + 6 + 10 Tische", 2 * nodes["abf_nft_1"]["count"] == nft == 24, "%d / %d" % (2 * nodes["abf_nft_1"]["count"], nft))
    pruefe("Abnehmer: 2 x 7 FD-Abfahrten = 14 = 8 + 6 Beete", 2 * nodes["abf_fd_1"]["count"] == fdb == 14, "%d / %d" % (2 * nodes["abf_fd_1"]["count"], fdb))
    w_abf = {k: sum(z["n"] for z in nodes[k]["zonen"]) for k in ("abf_nft_1", "abf_fd_1")}
    pruefe("Zonen je Halbring: NFT 4+3+5 = 12, FD 4+3 = 7", w_abf == {"abf_nft_1": 12, "abf_fd_1": 7}, str(w_abf))
    abfp = {b["id"]: len(b["lage"].get("abzweige", [])) for b in bauteile if b["id"].startswith("abf_")}
    pruefe("Zeichnung zeigt je Halbring 12 NFT- und 7 FD-Abzweigpunkte", abfp == {"abf_nft_1": 12, "abf_fd_1": 7, "abf_nft_2": 12, "abf_fd_2": 7}, str(abfp))
    pruefe("Abnehmer insgesamt 38 (Ist: 38 Schlauch-Fallleitungen im Ring-B2-Modell)", nft + fdb == 38, str(nft + fdb))

    W = {k: (round(v["wsp"] * 1000) if v.get("wsp") is not None else None) for k, v in sd["stufen"].items()}
    b_ = {k: v for k, v in sd["stufen"].items()}
    def d(a, b_nach):
        return W[a] - W[b_nach]
    regeln = [
        ("Schwerkraft: Vortex -> Biofilter faellt (Ueberlauf 10 cm)", d("vortex_1", "bio_1"), lambda x: 20 <= x <= 100),
        ("Schwerkraft: Biofilter -> Ring faellt", d("bio_1", "ring_1"), lambda x: x >= 20),
        ("Schwerkraft: Ring -> NFT Innen faellt (Regelkopf 0,30 m)", d("ring_1", "nft_innen"), lambda x: x >= 20),
        ("Schwerkraft: Ring -> NFT Aussen faellt", d("ring_1", "nft_aussen"), lambda x: x >= 20),
        ("Schwerkraft: Ring -> NFT Mitte faellt", d("ring_1", "nft_mitte"), lambda x: x >= 20),
        ("Schwerkraft: Ring -> Beet Aussen faellt", d("ring_1", "fd_aussen"), lambda x: x >= 20),
        ("Schwerkraft: Ring -> Beet Mitte faellt", d("ring_1", "fd_mitte"), lambda x: x >= 20),
        ("Schwerkraft: NFT Mitte -> Sumpf faellt", d("nft_mitte", "sump_1"), lambda x: x >= 20),
        ("Schwerkraft: NFT Aussen -> Sumpf faellt", d("nft_aussen", "sump_1"), lambda x: x >= 20),
        ("Schwerkraft: Beet -> Sumpf faellt", d("fd_aussen", "sump_1"), lambda x: x >= 20),
        ("Schwerkraft: NFT Innen -> Fischtank faellt", d("nft_innen", "fish"), lambda x: x >= 20),
        ("Schwerkraft: Biofilter -> Lebendfutterbecken faellt", d("bio_1", "feed"), lambda x: x >= 20),
        ("Schwerkraft: Notueberlauf Biofilter -> Sumpf faellt 2,05 m", d("bio_1", "sump_1"), lambda x: x == 2050),
        ("Ueberlauf: Lebendfutterbecken -> Anzuchtbecken <= 10 cm", d("feed", "nursery"), lambda x: 0 < x <= 100),
        ("Ueberlauf: Anzuchtbecken -> Fischtank <= 10 cm", d("nursery", "fish"), lambda x: 0 < x <= 100),
        ("Pumpe nach oben: Fischtank -> Vortex = 1,15 m", d("vortex_1", "fish"), lambda x: x == 1150),
        ("Pumpe nach oben: Sumpf -> Fischtank = 1,00 m", d("fish", "sump_1"), lambda x: x == 1000),
        ("Freibord Fischtank >= 5 cm (Rand 1,20 m)", round(b_["fish"]["rand"] * 1000) - W["fish"], lambda x: x >= 50),
        ("Freibord Sumpf >= 5 cm (Rand 0,00 m)", round(b_["sump_1"]["rand"] * 1000) - W["sump_1"], lambda x: x >= 50),
        ("Hochstand des Sumpfs liegt ueber dem Soll-Pegel und unter dem Rand", round(b_["sump_1"]["hochstand"] * 1000) - W["sump_1"], lambda x: 0 < x < 250),
        ("Fischtank hat den tiefsten Boden (-1,00 m < Sumpf -0,50 m)", round(b_["sump_1"]["boden"] * 1000) - round(b_["fish"]["boden"] * 1000), lambda x: x > 0),
        ("Innentische liegen ueber dem Poolrand (Rinne 1,25 m > Rand 1,20 m)", W["nft_innen"] - round(b_["fish"]["rand"] * 1000), lambda x: x > 0),
        ("in jedem Anbauring liegt das Beet unter dem NFT (Mitte)", W["nft_mitte"] - W["fd_mitte"], lambda x: x > 0),
        ("in jedem Anbauring liegt das Beet unter dem NFT (Aussen)", W["nft_aussen"] - W["fd_aussen"], lambda x: x > 0),
    ]
    for name, wert, ok in regeln:
        pruefe(name, ok(wert), "%+d mm" % wert)
    stufen_ok = all(a >= b2 for a, b2 in ((sd["stufen"]["vortex_1"]["stufe"], sd["stufen"]["bio_1"]["stufe"]), (sd["stufen"]["bio_1"]["stufe"], sd["stufen"]["ring_1"]["stufe"]),
                                         (sd["stufen"]["ring_1"]["stufe"], sd["stufen"]["nft_innen"]["stufe"]), (sd["stufen"]["nft_innen"]["stufe"], sd["stufen"]["fd_aussen"]["stufe"])))
    pruefe("Stufenreihenfolge 5 > 4 > 3 > 2 > 1 > 0 (Vortex > Biofilter > Ring > NFT > Beet > Fischtank)",
           stufen_ok and sd["stufen"]["fish"]["stufe"] == 0 and sd["maxStufe"] == 5, "maxStufe %s" % sd["maxStufe"])
    corners = [p for b in bauteile if b["id"] == "ring_1" for q in b["lage"]["zeichnung_primitive"] for p in q.get("punkte", [])]
    rr = sorted({round(p["r_mm"]) for p in corners if abs(p["r_mm"] - 3550) < 60})
    pruefe("Ring-Ecken liegen auf Eckradius 3550 mm (Zehneck, Halbring 1: 5 Ecken)", len(rr) == 1 and rr[0] == 3550 and len([p for p in corners if abs(p["r_mm"] - 3550) < 5]) == 5,
           "Radien %s, Ecken %d" % (rr, len([p for p in corners if abs(p["r_mm"] - 3550) < 5])))
    azs = sorted({round(p["az_grad"]) for p in corners if abs(p["r_mm"] - 3550) < 5})
    pruefe("Ring-Ecken Halbring 1 liegen bei Az -54, -18, 18, 54, 90 (= Ring B2 im Modell: Ecken bei 18 + 36 k)", azs == [-54, -18, 18, 54, 90], str(azs))
    pruefe("Quelle: 9 Bauteile ohne Hoehenangabe (ohneStufe)", len(sd["ohneStufe"]) == 9, str(sd["ohneStufe"]))
    if not nd:
        pruefe("nodeDatabase per node ausgewertet", False, "node fehlt oder Fehler: kennzahlen_index leer")
    else:
        pruefe("nodeDatabase per node ausgewertet (27 Showcase-Bauteile)", len(nd) == 27, str(len(nd)))

    meta = {
        "titel": "Soll-Wasserkreislauf nach Leons Oasis-Showcase (Wasserautobahn), D93/W89",
        "quellen": {"index.html": {"pfad": "docs/quellen/oasis-showcase-2026-11-10/index.html", "sha256": SHA["index.html"]},
                    "flow-diagram.html": {"pfad": "docs/quellen/oasis-showcase-2026-11-10-nachtrag/flow-diagram.html", "sha256": SHA["flow-diagram.html"]}},
        "erzeugt_von": "scripts/oasis_soll.py (python -I -X utf8 scripts/oasis_soll.py)",
        "umrechnung": {
            "mm_je_zeichnungseinheit": MM_JE_EINHEIT, "kuppelmitte_zeichnung": list(MITTE), "kuppel_radius_zeichnung": 480,
            "drehung_grad": DREHUNG_GRAD,
            "x_modell_mm": "dx = (x - 500) * 12,5, dy = -(y - 480) * 12,5 (Zeichnung unten = Modell -Y), dann um drehung_grad gegen den Uhrzeigersinn gedreht",
            "fussboden_z_modell_mm": FUSSBODEN_Z_MM, "z_modell_mm": "400 + Hoehe ueber Fussboden",
            "hinweis": "Zeichnung ist schematisch (A16): Mittelpunkte und Reihenfolge gelten; Rohrverlaeufe (pfad_punkte) sind Verbindungen, keine Trassen."},
        "stufen_bedeutung": "Stufe 0 bis 5 = nur Reihenfolge (A15); das Mass steht in wasserspiegel_ueber_fussboden_mm (A25, Vorschlaege, einstellbar)",
        "zaehlung": {"bauteile": len(bauteile), "wege": len(wege), "armaturen_zeilen": len(armaturen),
                     "bauteile_im_umfang": sum(1 for b in bauteile if b["im_umfang"]), "wege_im_umfang": sum(1 for w in wege if w["im_umfang"]),
                     "wege_wasser": sum(1 for w in wege if w["medium"] == "water"), "wege_luft": sum(1 for w in wege if w["medium"] == "air"),
                     "wege_schlamm": sum(1 for w in wege if w["medium"] == "sludge"), "wege_strom": sum(1 for w in wege if w["medium"] == "power")},
    }
    return {"meta": meta, "bauteile": bauteile, "wege": wege, "armaturen": armaturen, "pruefungen": PRUEF}


def main():
    nur_pruefen = "--pruefen" in sys.argv
    daten = baue()
    s = json.dumps(daten, ensure_ascii=False, indent=1) + "\n"
    if not nur_pruefen:
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            f.write(s)
    bad = [p for p in PRUEF if not p["ok"]]
    for p in PRUEF:
        print("%-5s %s  [%s]" % ("OK" if p["ok"] else "FAIL", p["pruefung"], p["detail"][:90]))
    z = daten["meta"]["zaehlung"]
    print("Bauteile %(bauteile)d (im Umfang %(bauteile_im_umfang)d), Wege %(wege)d (im Umfang %(wege_im_umfang)d; Wasser %(wege_wasser)d, Luft %(wege_luft)d, Schlamm %(wege_schlamm)d, Strom %(wege_strom)d), Armaturen-Zeilen %(armaturen_zeilen)d" % z)
    print("Pruefungen: %d OK, %d FAIL%s" % (len(PRUEF) - len(bad), len(bad), "" if nur_pruefen else "  -> " + os.path.relpath(OUT, ROOT)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
