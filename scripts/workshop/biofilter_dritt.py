"""Biofilter Drittbecken T98 (N-REWORK B, Mangel M02, Netz-Knoten biofilter_dritt, Kanten K42/K43 d25, 5 l/min):
Weithalsfass PE 60 l als Aufstrom-Biofilter mit 37 l Bioballs (R37 Befund 10). Zulauf K42 ueber eine Muffe d25 im Deckel und ein Tauchrohr d25
bis 60 mm ueber dem Boden; das Wasser steigt durch das Bioball-Bett, das eine Niederhalter-Lochplatte (Bohrungen nicht modelliert) unter Wasser haelt,
und laeuft ueber einen Tankverbinder d25 seitlich 75 mm unter dem Rand per Schwerkraft zurueck ins Drittbecken (K43). Bohrung Oe 8 im Deckel fuer
einen Luftschlauch (Belueftung, R27). KS: Mitte Fassboden aussen, Z hoch; Zulauf -X, Auslauf +X, Luft +X im Deckel.
Schreibt beim ersten Lauf data/components/biofilter_dritt.json (Parameter, Blatt) und danach die Ports.
Aufruf: python -X utf8 scripts/workshop/biofilter_dritt.py [--params] [--out <ordner>]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

PE, PVC, BIO = "PE Tank", "PVC grau", "Biomedium"
GRAF = "Graf-Massskizze Weithalsfass 60 l, Artikel 824410 (graf.info Dimension_drawing/Massskizze_Weithalsfass_60l.pdf): Oe 398 oben, 370 Boden, Oeffnung 338, H 615, mit Deckel 625"
HAENDLER = "Haendlerangaben Weithalsfass 60 l (OBI, Kaufland, toom; Graf 824410 und Nachbauten): Oe 400, H 620 bis 640"
R37 = "docs/research/R37.md Befund 10"

def P(w, e, h): return {"wert": w, "einheit": e, "herkunft": h}

def params_json():
    par = {
        "fass_d": P(398, "mm", f"[E] {GRAF}; {HAENDLER} (zwei Quellen, Konizitaet 398/370 nicht modelliert)"),
        "fass_h": P(615, "mm", f"[E] {GRAF}"),
        "fass_wall": P(3, "mm", "[A] Wandstaerke PE-Fass (Datenblatt nennt keine Wand)"),
        "fass_floor": P(4, "mm", "[A]"),
        "deckel_t": P(10, "mm", f"[E] {GRAF}: 625 mit Deckel minus 615"),
        "bett_l": P(37, "l", f"[E] {R37}: 37 l Bioballs (0,5 l je g Futter, 73 g Futter/Tag); R27 nannte 85 l fuer das groessere Becken 0,94 m3"),
        "bett_spalt": P(3, "mm", "[A] Luft Bett zur Fasswand"),
        "sieb_z": P(460, "mm", "[A] Unterkante Niederhalter-Lochplatte; Bett liegt darunter, Wasserstand (Auslauf 540) darueber"),
        "sieb_t": P(10, "mm", "[A] Lochplatte PE 10 mm, Bohrungen nicht modelliert"),
        "rohr_d": P(25, "mm", "[E] data/leitungsnetz.json K42/K43 dn 25"),
        "zulauf_x": P(-110, "mm", "[A] Lage Zulauf-Muffe im Deckel"),
        "tauch_z": P(60, "mm", "[A] Unterkante Tauchrohr ueber dem Fassboden aussen"),
        "auslauf_z": P(540, "mm", "[A] Achse Auslauf-Tankverbinder, 75 mm unter dem Fassrand (Wasserstand)"),
        "auslauf_l": P(50, "mm", "[A] Ueberstand Tankverbinder aussen"),
        "luft_d": P(8, "mm", "[A] Bohrung fuer Luftschlauch (wie Schlammfass T93)"),
        "luft_x": P(110, "mm", "[A] Lage Luftbohrung"),
        "durchfluss": P(5, "l/min", "[E] data/leitungsnetz.json K42/K43 soll_l_min 5 (TAN-Mindestdurchfluss 2,6 l/min x 2)"),
    }
    d = {"klasse": "biofilter_dritt", "teilenummer": "T98", "revision": "A",
        "beschreibung": "Biofilter Drittbecken (Quarantaene, N-REWORK B): Weithalsfass PE 60 l Oe 398 x 615 als Aufstrom-Biofilter, 37 l Bioballs unter einer Niederhalter-Lochplatte, Zulauf K42 d25 ueber Tauchrohr zum Boden, Auslauf K43 d25 seitlich per Schwerkraft zurueck ins Drittbecken, Luftschlauch-Bohrung Oe 8",
        "quelle_masse": f"{GRAF}; {HAENDLER}; {R37}; data/leitungsnetz.json (Knoten biofilter_dritt, K42/K43)",
        "parameter": par,
        "werkstoff": {"name": "PE (Fass, Deckel, Lochplatte), PVC-U (Stutzen, Tauchrohr), Kunststoff-Bioballs", "dichte_g_cm3": 0.95, "farbe": "#2a4f8f", "herkunft": "[A]"},
        "anzahl": {"soll": "1 (biofilter_dritt, nur am Drittbecken)", "quelle": "data/leitungsnetz.json Knoten biofilter_dritt; Standort neben dem Drittbecken, Auslauf ueber dessen Wasserspiegel, setzt die Montage"},
        "bezugspunkt": "Mitte Fassboden aussen (Z 0), Z hoch; Zulauf und Tauchrohr bei x -110, Auslauf-Tankverbinder +X, Luftbohrung x +110",
        "herkunft_tabelle": [
            ["Weithalsfass PE 60 l, Oe 398 x 615 (625 mit Deckel)", "mm", "belegt (zwei Quellen)", f"{GRAF}; {HAENDLER}", "mittel"],
            ["Bioball-Bett 37 l", "l", "gerechnet", f"{R37} (0,5 l Bioballs je g Futter bei 73 g/Tag)", "mittel"],
            ["Zulauf/Auslauf d25, 5 l/min", "d25", "belegt (Netz)", "data/leitungsnetz.json K42/K43", "hoch"],
            ["Aufstrom mit Niederhalter, Tauchrohr bis 60 mm ueber Boden", "Bauweise", "Annahme", "uebliche Fass-Biofilter-Bauweise, nicht recherchiert", "niedrig"],
            ["Wand 3, Boden 4, Lochplatte 10, Lagen der Stutzen", "mm", "Annahme", "kein Datenblatt fuer Wand und Einbauten", "niedrig"],
        ],
        "blatt": {
            "funktion": "Eigener kleiner Biofilter des Quarantaene-Drittbeckens: Eine Pumpe im Becken drueckt 5 l/min (K42) durch das Tauchrohr an den Fassboden; das Wasser steigt durch 37 l Bioballs, auf denen Nitrifikationsbakterien Ammonium zu Nitrat abbauen, und laeuft seitlich per Schwerkraft zurueck ins Becken (K43). Ein Luftschlauch im Deckel versorgt die Bakterien mit Sauerstoff.",
            "querschnitt": "Weithalsfass Oe 398 x 615 (Wand 3, Boden 4) mit Deckel 10; Tauchrohr d25 von der Deckel-Muffe bis 60 mm ueber dem Boden; Bioball-Bett unter der Lochplatte (Unterkante 460); Tankverbinder d25 mit Muffe bei Z 540 auf +X.",
            "toleranzen": "Bett 3 mm Luft zur Fasswand; Lochplatte liegt mit Spiel im Fass (Oe 386); Wasserstand am Auslauf Z 540, 70 mm ueber der Lochplatte.",
            "verbindungen": ["Zulauf-Muffe d25 im Deckel eingeklebt oder per Tankverbinder [A]; K42 steckt von oben in die Muffe, das Tauchrohr von unten", "Auslauf: Tankverbinder d25 durch die Fasswand mit Dichtung [A]; K43 steckt in die Muffe aussen", "Deckel: Schraubdeckel des Weithalsfasses (Gewinde nicht modelliert)"],
            "abweichung": "Keine OBJ-Vorgabe; Bauteil nach Netz und R37. Fass im Modell zylindrisch (Handelsfass leicht konisch, Boden Oe 370).",
            "montage": ["Fass neben dem Drittbecken waagerecht aufstellen, Auslauf ueber dessen Wasserspiegel", "Bioballs einfuellen, Lochplatte auflegen und gegen Auftrieb sichern (z. B. zwei Klemmleisten) [A]", "Tauchrohr durch Lochplatte bis zum Boden schieben, Deckel mit Muffe aufschrauben, K42 einstecken", "Luftschlauch mit Ausstroemer durch die Bohrung bis zum Boden fuehren; K43 an den Tankverbinder"],
            "werkzeug": "Lochsaege, PVC-Kleber, Bohrer 8 mm",
            "stueckliste": ["T98 Biofilter Drittbecken: 1 Weithalsfass PE 60 l mit Schraubdeckel, 37 l Bioballs, 1 Lochplatte PE Oe 386 x 10, 1 Zulauf-Muffe d25 (Tankverbinder), 1 Tauchrohr d25 L 571, 1 Tankverbinder d25 (Auslauf)"],
            "teileliste": [["Weithalsfass PE 60 l", "Oe 398 x 615", "Graf 824410 oder gleichwertig (Baumarkt DE)", "offen [A]"], ["Bioballs", "37 l", "offen (Aquaristik-/Teichhandel EU)", "offen [A]"], ["Tankverbinder d25", "2 Stueck", "offen (N-BESCHAFFUNG)", "offen [A]"]],
            "lokal": "Lebensmittelechtes Weithalsfass aus dem Baumarkt; Lochplatte aus PE-Plattenrest zuschneiden.",
            "massen_getrennt": [],
            "gewicht_gefuellt": "Wasser bis Auslauf ca. 70 l minus Bettanteil der Bioballs, gefuellt ca. 75 kg [E, Dichte 1]",
            "pruefung": ["scripts/workshop/check_biofilter_dritt.py: Fassmass, Bettvolumen 37 l (+-2 %), Verweilzeit, Wasserstand ueber der Lochplatte, Tauchrohr unter dem Bett, Ports, Interferenz 0"],
            "offen": ["Fassfabrikat: Wand und Konizitaet nicht im Modell [A]", "Niederhalter-Befestigung gegen Auftrieb der Bioballs [A]", "Luftmenge und Ausstroemer offen (R27 nennt Belueftung, keine Menge)", "Pumpe im Drittbecken fuer K42 gehoert nicht zu diesem Teil"],
            "kritiker": "Kein Pruefer-Lauf."}}
    json.dump(d, open(os.path.join(sc.ROOT, "data", "components", "biofilter_dritt.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def derive(p):
    D = {}
    rd = p["rohr_d"]
    D["st_od"] = L.od_f(rd)
    D["lid_top"] = p["fass_h"] + p["deckel_t"]
    D["st_top"] = D["lid_top"] + L.DEPTH[rd] + 10              # Stutzen ueber dem Deckel: Muffe oben, Anschlag, Muffe unten fuer das Tauchrohr
    D["st_anschlag"] = (D["st_top"] - L.DEPTH[rd] - 4, D["st_top"] - L.DEPTH[rd])
    D["st_bot"] = p["fass_h"]                                  # Stutzen sitzt im Deckelloch
    D["tauch_top"] = D["st_anschlag"][0]
    D["di"] = rd - 2 * L.wall_p(rd)
    D["bett_d"] = p["fass_d"] - 2 * p["fass_wall"] - 2 * p["bett_spalt"]
    a = math.pi / 4 * (D["bett_d"] ** 2 - (rd + 2) ** 2)      # Bett ohne Loch fuer das Tauchrohr (d25 + 2 Spiel)
    D["bett_h"] = round(p["bett_l"] * 1e6 / a, 2)
    D["bett_z0"] = p["sieb_z"] - D["bett_h"]
    D["R"] = p["fass_d"] / 2
    D["aus_x0"] = D["R"] - p["fass_wall"] - 10                 # Tankverbinder ragt 10 mm nach innen
    D["aus_x1"] = D["R"] + p["auslauf_l"]
    return D

def build(p, d):
    D = derive(p)
    b = sc.Build()
    b.params_to_design({k: v for k, v in p.items() if d["parameter"][k]["einheit"] in ("mm", "deg")}, d, {k: v["einheit"] for k, v in d["parameter"].items()})
    for nm, dens, col in ((PE, 0.95, "#2a4f8f"), (PVC, 1.4, "#8d9296"), (BIO, 0.15, "#c9b458")):
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    root = "T98_Biofilter_Dritt"
    b.add("component.create", name=root, grounded=True)
    fd, fh, w, rd = p["fass_d"], p["fass_h"], p["fass_wall"], p["rohr_d"]
    zx, za = p["zulauf_x"], p["auslauf_z"]
    # Fass mit Durchbruch fuer den Tankverbinder
    b.add("solid.cylinder", diameter=fd, height=fh, base=[0, 0, 0], operation="new", name="Fass_R", body_name="Fass")
    b.add("solid.cylinder", diameter=fd - 2 * w, height=fh, base=[0, 0, p["fass_floor"]], operation="cut", targets=["Fass"], name="Fass_Hohl")
    b.add("solid.cylinder", diameter=D["st_od"], height=w + 20, base=[D["R"] - w - 10, 0, za], axis=[1, 0, 0], operation="cut", targets=["Fass"], name="Fass_Durchbruch_Auslauf")
    b.add("material.assign", bodies=["Fass"], material=PE)
    # Deckel mit Loechern fuer Zulauf-Stutzen und Luftschlauch
    b.add("solid.cylinder", diameter=fd, height=p["deckel_t"], base=[0, 0, fh], operation="new", name="Deckel_R", body_name="Deckel")
    b.add("solid.cylinder", diameter=D["st_od"], height=p["deckel_t"] + 2, base=[zx, 0, fh - 1], operation="cut", targets=["Deckel"], name="Deckel_Loch_Zulauf")
    b.add("solid.cylinder", diameter=p["luft_d"], height=p["deckel_t"] + 2, base=[p["luft_x"], 0, fh - 1], operation="cut", targets=["Deckel"], name="Deckel_Loch_Luft")
    b.add("material.assign", bodies=["Deckel"], material=PE)
    # Zulauf-Stutzen: Muffe d25 oben (K42), Anschlag, Muffe d25 unten (Tauchrohr)
    b.add("solid.cylinder", diameter=D["st_od"], height=D["st_top"] - D["st_bot"], base=[zx, 0, D["st_bot"]], operation="new", name="Zulauf_R", body_name="Zulaufstutzen")
    b.add("solid.cylinder", diameter=rd, height=L.DEPTH[rd] + 1, base=[zx, 0, D["st_top"] - L.DEPTH[rd]], operation="cut", targets=["Zulaufstutzen"], name="Zulauf_Muffe_oben")
    b.add("solid.cylinder", diameter=D["di"], height=D["st_top"] - D["st_bot"] + 2, base=[zx, 0, D["st_bot"] - 1], operation="cut", targets=["Zulaufstutzen"], name="Zulauf_Durchgang")
    b.add("solid.cylinder", diameter=rd, height=D["st_anschlag"][0] - D["st_bot"] + 1, base=[zx, 0, D["st_bot"] - 1], operation="cut", targets=["Zulaufstutzen"], name="Zulauf_Muffe_unten")
    b.add("material.assign", bodies=["Zulaufstutzen"], material=PVC)
    # Tauchrohr d25 von der unteren Muffe bis tauch_z
    b.add("solid.cylinder", diameter=rd, height=D["tauch_top"] - p["tauch_z"], base=[zx, 0, p["tauch_z"]], operation="new", name="Tauch_R", body_name="Tauchrohr")
    b.add("solid.cylinder", diameter=D["di"], height=D["tauch_top"] - p["tauch_z"] + 2, base=[zx, 0, p["tauch_z"] - 1], operation="cut", targets=["Tauchrohr"], name="Tauch_Bohrung")
    b.add("material.assign", bodies=["Tauchrohr"], material=PVC)
    # Bioball-Bett (Schuettung als ein Koerper) und Niederhalter-Lochplatte, beide mit Loch fuer das Tauchrohr
    b.add("solid.cylinder", diameter=D["bett_d"], height=D["bett_h"], base=[0, 0, D["bett_z0"]], operation="new", name="Bett_R", body_name="Bioballs")
    b.add("solid.cylinder", diameter=rd + 2, height=D["bett_h"] + 2, base=[zx, 0, D["bett_z0"] - 1], operation="cut", targets=["Bioballs"], name="Bett_Loch_Tauchrohr")
    b.add("material.assign", bodies=["Bioballs"], material=BIO)
    b.add("solid.cylinder", diameter=D["bett_d"], height=p["sieb_t"], base=[0, 0, p["sieb_z"]], operation="new", name="Sieb_R", body_name="Lochplatte")
    b.add("solid.cylinder", diameter=rd + 2, height=p["sieb_t"] + 2, base=[zx, 0, p["sieb_z"] - 1], operation="cut", targets=["Lochplatte"], name="Sieb_Loch_Tauchrohr")
    b.add("material.assign", bodies=["Lochplatte"], material=PE)
    # Auslauf-Tankverbinder d25 auf +X: Muffe aussen (K43), Durchgang d_i
    b.add("solid.cylinder", diameter=D["st_od"], height=D["aus_x1"] - D["aus_x0"], base=[D["aus_x0"], 0, za], axis=[1, 0, 0], operation="new", name="Aus_R", body_name="Auslaufstutzen")
    b.add("solid.cylinder", diameter=rd, height=L.DEPTH[rd] + 1, base=[D["aus_x1"] - L.DEPTH[rd], 0, za], axis=[1, 0, 0], operation="cut", targets=["Auslaufstutzen"], name="Aus_Muffe")
    b.add("solid.cylinder", diameter=D["di"], height=D["aus_x1"] - D["aus_x0"] + 2, base=[D["aus_x0"] - 1, 0, za], axis=[1, 0, 0], operation="cut", targets=["Auslaufstutzen"], name="Aus_Durchgang")
    b.add("material.assign", bodies=["Auslaufstutzen"], material=PVC)
    b.add("component.metadata.set", component=root, part_number="T98", description=d["beschreibung"], revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, D

def ports(p, D):
    f = lambda v: f"{round(v):d}"
    return [["Zulauf K42 (Pumpe im Drittbecken)", f"Muffe d{p['rohr_d']:g}, Deckel", f"x {f(p['zulauf_x'])}, y 0, z {f(D['st_top'])}", "+Z"],
            ["Auslauf K43 (Schwerkraft zurueck ins Drittbecken)", f"Muffe d{p['rohr_d']:g}, Tankverbinder seitlich", f"x {f(D['aus_x1'])}, y 0, z {f(p['auslauf_z'])}", "+X"],
            ["Luftschlauch (Belueftung)", f"Bohrung Oe {p['luft_d']:g} im Deckel", f"x {f(p['luft_x'])}, y 0, z {f(D['lid_top'])}", "+Z"]]

if __name__ == "__main__":
    pj = os.path.join(sc.ROOT, "data", "components", "biofilter_dritt.json")
    if not os.path.exists(pj) or "--params" in sys.argv:
        params_json()
    p, d = sc.load_params("biofilter_dritt")
    b, D = build(p, d)
    out_dir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(sc.ROOT, "designs", "components")
    out = os.path.join(out_dir, "biofilter_dritt.sc")
    sc.run(b.write("biofilter_dritt"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v) for v in mn], [round(v) for v in mx], "Masse leer", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 2), "kg", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in D.items()})
    d["blatt"]["ports"] = ports(p, D)
    json.dump(d, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
