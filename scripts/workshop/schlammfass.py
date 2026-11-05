"""Schlammfass T93 (W37-1 Teil 2, L01, R45 Abschnitt 0, E12): Spannringfass PE 220 l in einer Grube neben dem Absetzer; Deckel mit Einlaufstutzen d40 in der Mitte
(K07 Linie 1 / K23 Linie 2), Bohrung Oe 8 fuer Luftschlauch, Entlueftung Oe 20, kein Auslass (Entleerung von oben).
KS: Ursprung Mitte Fassboden aussen, Z hoch. Einbau: Grube Oe 800, Tiefe 950 (Parameter grube_d, grube_t; die Grube baut die Montage), Fassoberkante etwa Flur 0.
Schreibt beim ersten Lauf data/components/schlammfass.json (Parameter, Blatt) und danach die Ports.
Aufruf: python -X utf8 scripts/workshop/schlammfass.py [--render]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

PE, PVC, STAHL = "PE Tank", "PVC grau", "Stahl verzinkt"
R45 = "docs/research/R45-hydraulik-auslegung.md Abschnitt 0"

def P(w, e, h): return {"wert": w, "einheit": e, "herkunft": h}

def params_json():
    par = {
        "fass_d": P(580, "mm", f"[A] {R45}: Spannringfass PE 200-220 l, Oe 0,58-0,60 m (Handelsmass, nicht gegengeprueft)"),
        "fass_h": P(880, "mm", f"[A] {R45}: H 0,88-0,92 m inklusive Deckel"),
        "fass_wall": P(4, "mm", "[A] Wandstaerke PE-Fass (kein Datenblatt gelesen)"),
        "fass_floor": P(5, "mm", "[A]"),
        "deckel_t": P(15, "mm", "[A] Deckel mit Spannring"),
        "ring_b": P(10, "mm", "[A] Spannring radial"),
        "ring_h": P(35, "mm", "[A] Spannring hoch"),
        "stutzen_d": P(40, "mm", f"[E] {R45}: Deckel mit Stutzen d40 Mitte; K07/K23 d40 (Netz V3)"),
        "luft_d": P(8, "mm", f"[E] {R45}: Bohrung Oe 8 fuer Luftschlauch (Luftstein optional, Frage 4)"),
        "luft_x": P(150, "mm", "[A] Lage Luftbohrung"),
        "entl_d": P(20, "mm", f"[E] {R45}: Entlueftung Oe 20"),
        "entl_x": P(-150, "mm", "[A] Lage Entlueftung"),
        "grube_d": P(800, "mm", f"[E] {R45} Bauteil-Skizze: Grube Oe 0,8 m (baut die Montage)"),
        "grube_t": P(950, "mm", f"[E] {R45}: Tiefe etwa 0,95 m; Fassoberkante etwa Flur 0 bis +20 bei 70 mm Sandbett"),
    }
    d = {"klasse": "schlammfass", "teilenummer": "T93", "revision": "A",
        "beschreibung": "Schlammfass je Linie (L01, R45 Abschnitt 0, E12): Spannringfass PE 220 l Oe 580 x 880 in einer Grube Oe 0,8 m, Tiefe 0,95 m neben dem Absetzer; Deckel mit Einlaufstutzen d40 in der Mitte (K07/K23), Luftschlauch-Bohrung Oe 8, Entlueftung Oe 20, kein Auslass; woechentlich von Hand geleert",
        "quelle_masse": f"{R45} (Bauteil-Skizze, Zahlen), data/leitungsnetz.json Version 3 (K07/K23, Knoten schlammfass_1/2)",
        "parameter": par,
        "werkstoff": {"name": "PE (Fass, Deckel), Stahl verzinkt (Spannring), PVC-U (Stutzen)", "dichte_g_cm3": 0.95, "farbe": "#2a4f8f", "herkunft": "[A]"},
        "anzahl": {"soll": "2 (je Linie: schlammfass_1, schlammfass_2)", "quelle": "data/leitungsnetz.json Knoten schlammfass_1/2; Standort 0,7-0,8 m neben dem Kegelspitzen-Hahn setzt die Montage (M10 S5)"},
        "bezugspunkt": "Mitte Fassboden aussen (Z 0), Z hoch; Luftbohrung +X, Entlueftung -X. Einbau: Fassboden flur-relativ -880 auf 70 mm Sandbett (Grubensohle -950), Fassoberkante Flur 0",
        "herkunft_tabelle": [
            ["Fass 220 l, Oe 580 x 880", "Oe 580 x 880", "Annahme (Handelsmass)", f"{R45} Bauteil-Skizze (Oe 0,58-0,60, H 0,88-0,92); nicht gegengeprueft", "mittel"],
            ["Fassung 105 l/Woche plus Reserve", "220 l nominal", "gerechnet", f"{R45} Zahlen: 70-105 l je Linie und Woche (Spanne 47-140)", "mittel"],
            ["Stutzen d40 Mitte Deckel", "d40", "belegt (Netz) / gerechnet", "data/leitungsnetz.json V3 K07/K23 dn 40; R45 Einlauf", "hoch"],
            ["Luftbohrung Oe 8, Entlueftung Oe 20", "Oe 8 / Oe 20", "gerechnet (R45-Skizze)", f"{R45} Entlueftung/Luft", "mittel"],
            ["Grube Oe 800, Tiefe 950", "800 / 950", "gerechnet (R45-Skizze)", f"{R45} Bauteil-Skizze; Kollision mit eingegrabenen Rohren prueft die Montage (Frage 0 Nr. 5)", "mittel"],
            ["Wand 4, Boden 5, Deckel 15, Spannring 10 x 35", "mm", "Annahme", "kein Datenblatt gelesen", "niedrig"],
        ],
        "blatt": {
            "funktion": "Nimmt den Schlamm auf, den der Absetzer alle 2 bis 3 Tage ueber den Federrueckzug-Kugelhahn und K07/K23 ablaesst (20 bis 40 l je Spuelung). Der Schlamm setzt sich ab; einmal pro Woche wird Klarwasser abgehoben (zurueck in den Pool) und Dickschlamm zum Wurmkompost gebracht. Kein Reaktor, kein Auslass.",
            "querschnitt": "Fass Oe 580 x 865 (Wand 4, Boden 5) mit Deckel Oe 580 x 15 und Spannring 600 x 35; Einlaufstutzen d40 (Muffe) in der Deckelmitte, Bohrung Oe 8 bei x +150, Entlueftungsstutzen Oe 20 bei x -150.",
            "toleranzen": "Grube Oe 800 laesst 100 mm Ringspalt um das Fass (Verfuellung); Fassoberkante Flur 0, Stutzen-Muffe bis Flur +40.",
            "verbindungen": ["Deckel mit Spannring (Schnellverschluss) auf dem Fass; Dichtung nicht modelliert [A]", "Einlaufstutzen d40 in den Deckel eingeklebt oder per Tankverbinder [A]; K07/K23 steckt mit dem Fallrohr in die Muffe"],
            "abweichung": "Keine OBJ-Vorgabe; Bauteil nach R45 Abschnitt 0 (Bauteil-Skizze).",
            "montage": ["Grube Oe 0,8 m, Tiefe 0,95 m neben dem Absetzer (0,7-0,8 m Mitte zu Mitte vom Kegelspitzen-Hahn), Sandbett 70 mm", "Fass einsetzen, Oberkante auf Flur 0 ausrichten, Ringspalt verfuellen", "Deckel mit Stutzen aufsetzen, Spannring schliessen; K07/K23 (d40, 5 % Gefaelle, Bogen 90, Fallrohr 0,1 m) in die Muffe stecken"],
            "werkzeug": "Spaten, Wasserwaage, Lochsaege, PVC-Kleber",
            "stueckliste": ["T93 Schlammfass je Linie: 1 Spannringfass PE 220 l mit Deckel und Spannring, 1 Einlaufstutzen d40 (Tankverbinder oder Klebemuffe), 1 Entlueftungsstutzen Oe 20; Federrueckzug-Kugelhahn d40 am Absetzer siehe lt_kugelhahn_feder_d40"],
            "teileliste": [["Spannringfass PE 220 l", "Oe 580 x 880", "offen (Fasshandel in DE/EU)", "offen [A]"], ["Tankverbinder/Stutzen d40", "Klebemuffe", "offen (N-BESCHAFFUNG)", "offen [A]"]],
            "lokal": "Gebrauchtes Lebensmittel-Spannringfass (gereinigt) aus dem regionalen Fasshandel.",
            "massen_getrennt": [],
            "gewicht_gefuellt": "Bis 105 l Schlammwasser ca. 105 kg, voll ca. 220 kg [E, Dichte 1]; Entleerung von Hand (Heber/Tauchpumpe, Eimer)",
            "pruefung": ["scripts/workshop/check_schlammfass.py (Ergebnis renders/components/schlammfass/check.txt): Fassmass, Volumen 200-220 l (+-5 %) aus Oe und H und aus dem Modell, Stutzen d40 Mitte Deckel, Bohrungen, Ports, Gruben-Parameter, Interferenz 0"],
            "offen": ["Fassfabrikat und Mass im Handel nicht gegengeprueft [A]", "Kollision der Grube mit eingegrabenen Rohren: Montage mit check_leitungen.py (R45 Frage 0 Nr. 5)", "Luftstein/Luftmenge optional, Menge offen (R45 Frage 4)", "Schlammkonzentration im Betrieb messen (R45 Frage 0 Nr. 1)", "M10-S2V (Subtank, GEPARKT) beruehrt die Schlammfuehrung; bei Freigabe pruefen"],
            "kritiker": "Kein Pruefer-Lauf (Pruefpunkte fuer den Pruefer im Blatt W37-1)."}}
    json.dump(d, open(os.path.join(sc.ROOT, "data", "components", "schlammfass.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def derive(p):
    D = {"body_top": p["fass_h"] - p["deckel_t"]}
    D["st_od"] = L.od_f(p["stutzen_d"])
    D["st_top"] = p["fass_h"] + L.DEPTH[p["stutzen_d"]] + 14
    D["en_od"] = p["entl_d"] + 6
    D["en_top"] = p["fass_h"] + 20
    return D

def build():
    p, d = sc.load_params("schlammfass")
    D = derive(p)
    b = sc.Build()
    b.params_to_design(p, d, {k: v["einheit"] for k, v in d["parameter"].items()})
    for nm, dens, col in ((PE, 0.95, "#2a4f8f"), (PVC, 1.4, "#8d9296"), (STAHL, 7.85, "#aeb4b8")):
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    root = "T93_Schlammfass"
    b.add("component.create", name=root, grounded=True)
    fd, fh, w = p["fass_d"], p["fass_h"], p["fass_wall"]
    b.add("solid.cylinder", diameter=fd, height=D["body_top"], base=[0, 0, 0], operation="new", name="Fass_R", body_name="Fass")
    b.add("solid.cylinder", diameter=fd - 2 * w, height=D["body_top"], base=[0, 0, p["fass_floor"]], operation="cut", targets=["Fass"], name="Fass_Hohl")
    b.add("material.assign", bodies=["Fass"], material=PE)
    b.add("solid.cylinder", diameter=fd, height=p["deckel_t"], base=[0, 0, D["body_top"]], operation="new", name="Deckel_R", body_name="Deckel")
    for nm, x, dd in (("Stutzen", 0, D["st_od"]), ("Luft", p["luft_x"], p["luft_d"]), ("Entl", p["entl_x"], D["en_od"])):
        b.add("solid.cylinder", diameter=dd, height=p["deckel_t"] + 2, base=[x, 0, D["body_top"] - 1], operation="cut", targets=["Deckel"], name=f"Deckel_Loch_{nm}")
    b.add("material.assign", bodies=["Deckel"], material=PE)
    rz = fh - p["ring_h"]
    b.add("solid.cylinder", diameter=fd + 2 * p["ring_b"], height=p["ring_h"], base=[0, 0, rz], operation="new", name="Ring_R", body_name="Spannring")
    b.add("solid.cylinder", diameter=fd, height=p["ring_h"] + 2, base=[0, 0, rz - 1], operation="cut", targets=["Spannring"], name="Ring_Innen")
    b.add("material.assign", bodies=["Spannring"], material=STAHL)
    sd = p["stutzen_d"]
    b.add("solid.cylinder", diameter=D["st_od"], height=D["st_top"] - D["body_top"], base=[0, 0, D["body_top"]], operation="new", name="Stutzen_R", body_name="Einlaufstutzen")
    b.add("solid.cylinder", diameter=sd, height=L.DEPTH[sd] + 1, base=[0, 0, D["st_top"] - L.DEPTH[sd]], operation="cut", targets=["Einlaufstutzen"], name="Stutzen_Muffe")
    b.add("solid.cylinder", diameter=sd - 2 * L.wall_p(sd), height=D["st_top"] - D["body_top"] + 2, base=[0, 0, D["body_top"] - 1], operation="cut", targets=["Einlaufstutzen"], name="Stutzen_Durchgang")
    b.add("material.assign", bodies=["Einlaufstutzen"], material=PVC)
    b.add("solid.cylinder", diameter=D["en_od"], height=D["en_top"] - D["body_top"], base=[p["entl_x"], 0, D["body_top"]], operation="new", name="Entl_R", body_name="Entlueftungsstutzen")
    b.add("solid.cylinder", diameter=p["entl_d"], height=D["en_top"] - D["body_top"] + 2, base=[p["entl_x"], 0, D["body_top"] - 1], operation="cut", targets=["Entlueftungsstutzen"], name="Entl_Bohrung")
    b.add("material.assign", bodies=["Entlueftungsstutzen"], material=PVC)
    b.add("component.metadata.set", component=root, part_number="T93", description=d["beschreibung"], revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, p, d, D

def ports(p, D):
    f = lambda v: f"{round(v):d}"
    return [["Einlauf Schlamm (K07 Linie 1 / K23 Linie 2, vom Federrueckzug-Kugelhahn des Absetzers)", f"Muffe d{p['stutzen_d']:g}, Mitte Deckel", f"x 0, y 0, z {f(D['st_top'])}", "+Z"],
            ["Luftschlauch (optional Luftstein)", f"Bohrung Oe {p['luft_d']:g} im Deckel", f"x {f(p['luft_x'])}, y 0, z {f(p['fass_h'])}", "+Z"],
            ["Entlueftung", f"Stutzen Oe {p['entl_d']:g} innen", f"x {f(p['entl_x'])}, y 0, z {f(D['en_top'])}", "+Z"]]

if __name__ == "__main__":
    pj = os.path.join(sc.ROOT, "data", "components", "schlammfass.json")
    if not os.path.exists(pj) or "--params" in sys.argv:
        params_json()
    b, p, d, D = build()
    out = os.path.join(sc.ROOT, "designs", "components", "schlammfass.sc")
    sc.run(b.write("schlammfass"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v) for v in mn], [round(v) for v in mx], "Masse leer", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 1), "kg")
    d["blatt"]["ports"] = ports(p, D)
    json.dump(d, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "schlammfass")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "schlammfass-01-schraeg.png"), [0, 0, 450], 0.7, 0.4, 2200, w=1000, h=800)
        sc.snapshot(out, os.path.join(rd, "schlammfass-02-schnitt.png"), [0, 0, 450], 3.14159, 0.0, 2200, w=1000, h=800, section="y=0")
