"""Vorpruefung Planen-Huelle (W27, D39, R24): keilschiene T43, huelle_folie T42, tuer_zarge_planenausschnitt T44.
Erwartung unabhaengig vom Generator: Profilflaeche aus der Skizze (Formel), Strebenlaengen und Dreiecksflaechen aus data/layout.json, 208 m2 aus R24, Interferenz per inspect.interference.
Aufruf: python scripts/workshop/check_huelle.py [keilschiene|folie|zarge ...]   (exit 1 bei FAIL)"""
import itertools, json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def comp(name):
    return os.path.join(sc.ROOT, "designs", "components", name + ".sc")

def interference(path):
    script = os.path.join(sc.TMP, "ws-huelle-interf.json"); out = os.path.join(sc.TMP, "ws-huelle-interf-out.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 240}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--results", "--json-out", out], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER interference: " + r.stderr.strip())
    d = json.load(open(out, encoding="utf-8"))
    def find(o):
        if isinstance(o, dict):
            if "interferences" in o:
                return o["interferences"]
            for v in o.values():
                x = find(v)
                if x is not None:
                    return x
        elif isinstance(o, list):
            for v in o:
                x = find(v)
                if x is not None:
                    return x
    return [(i["a"], i["b"], i.get("volume_mm3", 0)) for i in find(d) or []]

def strut_lengths():
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    return lay, sorted(set(lay["strut_len_mm"]))

def check_keilschiene(ck):
    p, d = sc.load_params("keilschiene")
    lay, lens = strut_lengths()
    A, B = lens[0], lens[-1]
    ck.eq("Strebenzahl laut layout.json = 65 = Anzahl Keilschienen", lay["struts"], sum(t["anzahl"] for t in d["typen"].values()))
    ck.eq("Typ A: len = Knotenabstand A - 2 x Knotenfreiraum", d["typen"]["A"]["len"], A - 2 * p["node_clear"], 1.0)
    ck.eq("Typ B: len = Knotenabstand B - 2 x Knotenfreiraum", d["typen"]["B"]["len"], B - 2 * p["node_clear"], 1.0)
    ck.eq("Gesamtlaenge Schienen in m (R24: ca. 228 m Knotenabstand, hier minus Freiraeume)", sum(t["anzahl"] * t["len"] for t in d["typen"].values()) / 1000, 30 * (A - 260) / 1000 + 35 * (B - 260) / 1000, 0.5)
    ck.eq("Gesamtlaenge gegen R24 (228 m) in Prozent Abweichung <= 8 %", 1 if abs(sum(t["anzahl"] * t["len"] for t in d["typen"].values()) / 1000 - 228) / 228 <= 0.08 else 0, 1)
    path = comp("keilschiene")
    ev = sc.evaluate(path)
    Bd = {b["name"]: b for b in ev["bodies"]}
    ext = lambda n, i: Bd[n]["bbox"]["max"][i] - Bd[n]["bbox"]["min"][i]
    w, h, t, lip, ft = p["ch_w"], p["ch_h"], p["ch_wall"], p["ch_lip"], p["foam_t"]
    ck.eq("Kanal Laenge (Konfiguration A)", ext("Kanal", 0), d["typen"]["A"]["len"], 0.05)
    ck.eq("Kanal Breite 25", ext("Kanal", 1), w, 0.05)
    ck.eq("Kanal Hoehe 15", ext("Kanal", 2), h, 0.05)
    area = w * t + 2 * t * (h - t) + 2 * (lip - t) * t
    ck.eq("Kanal Volumen = Profilflaeche (w*t + 2*t*(h-t) + 2*(lip-t)*t) x Laenge", Bd["Kanal"]["volume_mm3"], area * d["typen"]["A"]["len"], 20)
    ck.eq("Kanal Unterkante liegt auf dem Schaumband (z = 3)", Bd["Kanal"]["bbox"]["min"][2], ft, 0.01)
    ck.eq("Schaumband 25 x 3 x len", Bd["Schaumband"]["volume_mm3"], p["foam_w"] * ft * d["typen"]["A"]["len"], 20)
    ck.eq("Schaumband Unterkante z = 0 (Bezug)", Bd["Schaumband"]["bbox"]["min"][2], 0.0, 0.01)
    ck.eq("Federdraht Durchmesser 2", ext("Federdraht", 1), p["wire_d"], 0.02)
    ck.eq("Federdraht Laenge = len - 2 x 20", ext("Federdraht", 0), d["typen"]["A"]["len"] - 2 * p["wire_clear"], 0.05)
    ck.eq("Federdraht ist eigener Koerper", 1 if "Federdraht" in Bd else 0, 1)
    wb, kb = Bd["Federdraht"]["bbox"], Bd["Kanal"]["bbox"]
    ck.eq("Federdraht liegt im Kanal (Luft zum Grund 0,5 mm)", wb["min"][2] - (ft + t), p["wire_gap"], 0.01)
    ck.eq("Federdraht unter den Lippen (Oberkante < Lippen-Unterkante, Maul 17 mm > Draht)", 1 if wb["max"][2] < ft + h - t and w - 2 * lip > p["wire_d"] else 0, 1)
    ck.eq("Masse Kanal Typ A in kg (Dichte 2,7)", Bd["Kanal"]["mass_g"] / 1000, area * d["typen"]["A"]["len"] * 2.7 / 1e6, 0.002)
    # Konfiguration B: Zeile aktivieren, speichern, messen
    tmp = os.path.join(sc.TMP, "ws-keilschiene-B.sc"); script = os.path.join(sc.TMP, "ws-keil-B.json")
    json.dump({"commands": [{"command": "config.activate", "params": {"row": "B"}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--save", tmp, "--quiet"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER config B: " + r.stderr.strip())
    evb = sc.evaluate(tmp)
    Bb = {b["name"]: b for b in evb["bodies"]}
    ck.eq("Konfiguration B: Kanal Laenge", Bb["Kanal"]["bbox"]["max"][0] - Bb["Kanal"]["bbox"]["min"][0], d["typen"]["B"]["len"], 0.05)
    ck.eq("Konfiguration B: Federdraht Laenge", Bb["Federdraht"]["bbox"]["max"][0] - Bb["Federdraht"]["bbox"]["min"][0], d["typen"]["B"]["len"] - 2 * p["wire_clear"], 0.05)
    itf = interference(path)
    for x in itf[:6]:
        print("   Interferenz", x)
    ck.eq("Interferenzen Keilschiene (Schaumband, Kanal, Federdraht)", len(itf), 0)

def heron(a, b, c):
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))

def layout_triangles():
    """Dreiecke aus layout.json unabhaengig vom Generator: Knotenpaare mit Abstand = Strebenlaenge (+-15), Tripel paarweise verbunden; Rueckgabe Liste der Flaechen in m2 und der Typen."""
    lay, lens = strut_lengths()
    N = lay["nodes_list"]
    P = [(n["x"], n["y"], n["z"]) for n in N]
    edge = lambda i, j: min(lens, key=lambda L: abs(math.dist(P[i], P[j]) - L)) if min(abs(math.dist(P[i], P[j]) - L) for L in lens) <= 15 else None
    E = {(i, j) for i, j in itertools.combinations(range(len(P)), 2) if edge(i, j)}
    tris = [(i, j, k) for i, j, k in itertools.combinations(range(len(P)), 3) if (i, j) in E and (i, k) in E and (j, k) in E]
    area = lambda t: heron(math.dist(P[t[0]], P[t[1]]), math.dist(P[t[1]], P[t[2]]), math.dist(P[t[0]], P[t[2]])) / 1e6
    return len(E), [area(t) for t in tris]

def check_folie(ck):
    p, d = sc.load_params("huelle_folie")
    hp = json.load(open(os.path.join(sc.ROOT, "data", "components", "haut_paneel.json"), encoding="utf-8"))["typen"]
    G = json.load(open(os.path.join(sc.ROOT, "data", "components", "tuer_komplett.json"), encoding="utf-8"))["geometrie"]
    ne, areas = layout_triangles()
    ck.eq("Streben aus layout.json (Knotenabstaende) = 65", ne, 65)
    ck.eq("Dreiecke aus layout.json = 40", len(areas), 40)
    ck.eq("Anzahl Folien-Bauteile je Typ summiert = 40 Felder", sum(t["anzahl"] for t in d["typen"].values()), 40)
    brutto = sum(areas)
    ck.eq("Huellflaeche brutto aus layout.json in m2 (R24: 209,9)", brutto, 209.9, 0.5)
    zarge = G["zarge_aussen_w"] * G["zarge_hoehe"] / 1e6
    netto = brutto - zarge
    ck.eq("Huellflaeche netto = brutto - Tuerfeld in m2 (R24: 208 +- 3 %)", netto, 208.0, 208.0 * 0.03)
    k_of = {}
    tot_net, tot_gross, tot_mass = 0.0, 0.0, 0.0
    for typ, T in d["typen"].items():
        path = comp(f"huelle_folie_{typ}")
        ev = sc.evaluate(path)
        Bd = {b["name"]: b for b in ev["bodies"]}
        c, a, b_ = T["kanten_nominal"]
        A0 = heron(a, b_, c)
        r = A0 / ((a + b_ + c) / 2)
        k = (r + p["overlap"] / 2) / r
        for lage in ("Folie_innen", "Folie_aussen"):
            ck.eq(f"{typ} {lage}: Dicke 0,15 (Z-Ausdehnung)", Bd[lage]["bbox"]["max"][2] - Bd[lage]["bbox"]["min"][2], p["foil_t"], 0.005)
        ck.eq(f"{typ}: innere Lage bei Z {p['foil_z0']:g} (liegt auf der Keilschiene)", Bd["Folie_innen"]["bbox"]["min"][2], p["foil_z0"], 0.005)
        ck.eq(f"{typ}: Lagenabstand 100 mm (Luftpolster, Unterkante zu Unterkante)", Bd["Folie_aussen"]["bbox"]["min"][2] - Bd["Folie_innen"]["bbox"]["min"][2], p["layer_gap"], 0.005)
        cut = 0.0
        if T["tuerausschnitt"]:
            hw = G["zarge_aussen_w"] - 2 * p["door_overlap"]
            cut = hw * (G["zarge_hoehe"] - p["door_overlap"] + p["overlap"] / 2 + 0.0)
            # Der Ausschnitt reicht von der Basiskante - Ueberstand bis zur Sturz-Oberkante - door_overlap; Hoehe ab der Basiskante: zarge_hoehe - door_overlap, plus Ueberstand nach unten
        A_ist = Bd["Folie_innen"]["volume_mm3"] / p["foil_t"]
        ck.eq(f"{typ}: Folienflaeche je Lage (Volumen / Dicke) gegen Heron mit Ueberstand-Aufmass + Ausschnitt in m2", (A_ist + cut) / 1e6, A0 * k * k / 1e6, A0 * k * k / 1e6 * 0.002)
        if typ == "BBB":
            ck.eq("BBB: Seitenlaenge mit Ueberstand = 3708 + 2 x wurzel(3) x 100 (X-Ausdehnung)", Bd["Folie_innen"]["bbox"]["max"][0] - Bd["Folie_innen"]["bbox"]["min"][0], 3708 + 2 * math.sqrt(3) * p["overlap"] / 2, 0.5)
        if typ == "BBB_tuer":
            ck.eq("BBB_tuer: Ausschnitt entfernt Flaeche (1026 x 2143 = 2,20 m2) aus beiden Lagen", Bd["Folie_aussen"]["volume_mm3"] / p["foil_t"], A0 * k * k - cut, A0 * k * k * 0.002)
        n_vol = 1 if typ == "BBB" else T["anzahl"]
        tot_net += (A0 / 1e6) * (T["anzahl"] if typ != "BBB_tuer" else 0) + (0 if typ != "BBB_tuer" else (A0 / 1e6 - zarge))
        tot_gross += (A_ist / 1e6) * T["anzahl"]
        tot_mass += (Bd["Folie_innen"]["mass_g"] + Bd["Folie_aussen"]["mass_g"]) / 1000 * T["anzahl"]
        ck.eq(f"{typ}: Masse je Feld (2 Lagen) = Flaeche x 0,15 mm x 0,92", (Bd["Folie_innen"]["mass_g"] + Bd["Folie_aussen"]["mass_g"]) / 1000, 2 * A_ist * p["foil_t"] * 0.92 / 1e6, 0.002)
        itf = interference(path)
        ck.eq(f"{typ}: Interferenzen innere/aeussere Lage", len(itf), 0)
    ck.eq("Summe netto aus den Bauteilen (30 AAB + 9 BBB + Tuerfeld) in m2 gegen R24 208 +- 3 %", tot_net, 208.0, 208.0 * 0.03)
    print(f"   Folienflaeche je Lage mit Ueberstand: {tot_gross:.1f} m2 (netto {tot_net:.1f} m2); Gesamtmasse beide Lagen: {tot_mass:.1f} kg")
    kp, dk = sc.load_params("keilschiene")
    strut_r = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8"))["strut_d"]["value"] / 2   # D91: Rundrohr-Radius (Folie auf der Strebe)
    ck.eq(f"Innere Lage liegt ueber Strebe + Schaumband + Kanal ({strut_r:g} + 3 + 15 < {p['foil_z0']:g})", 1 if strut_r + kp["foam_t"] + kp["ch_h"] < p["foil_z0"] else 0, 1)
    ck.eq("Luft zwischen Kanal-Oberkante und innerer Lage in mm (1)", p["foil_z0"] - (strut_r + kp["foam_t"] + kp["ch_h"]), 1.0, 0.01)

def check_zarge(ck):
    p, d = sc.load_params("tuer_zarge_planenausschnitt")
    tp, td = sc.load_params("tuer_komplett")
    fp, fd = sc.load_params("huelle_folie")
    G = td["geometrie"]
    r, sh, lw, lh = tp["rohr"], tp["schwelle_h"], G["lichte_w"], G["lichte_h"]
    xc, yc, ytop = lw / 2 + r / 2, sh + lh + r / 2, sh + lh + r
    wt, cw, ct, sw, st, kw, kt = p["web_t"], p["collar_w"], p["collar_t"], p["seal_w"], p["seal_t"], p["clamp_w"], p["clamp_t"]
    Ly = (ytop + (cw - r) / 2) - sh
    path = comp("tuer_zarge_planenausschnitt")
    ev = sc.evaluate(path)
    Bd = {b["name"]: b for b in ev["bodies"]}
    bb = lambda n: Bd[n]["bbox"]
    # Erwartung aus der Querschnittsformel (Vereinigungsvolumen, unabhaengig vom Generator)
    hs = (fp["foil_z0"] - st) - r / 2
    Lt, Lc = 2 * xc + wt, 2 * xc + cw
    web_fp = 2 * wt * Ly + (Lt - 2 * wt) * wt
    v_web = web_fp * hs
    v_col = 2 * cw * Ly * ct + (Lc - 2 * cw) * cw * ct
    evt = sc.evaluate(comp("tuer_komplett"))
    lugs = [x for x in evt["bodies"] if x["name"].endswith("Zargenlasche")]
    v_notch = sum(wt * ((x["bbox"]["max"][1] - x["bbox"]["min"][1]) + 2 * p["notch_clear"]) * (x["bbox"]["max"][2] + p["notch_clear"] - r / 2) for x in lugs)
    ck.eq("Scharnier-Zargenlaschen der Tuer = 3, je eine Ausklinkung im Steg", len(lugs), 3)
    ck.eq("Aufsatzrahmen Volumen = Stege + Kraegen - Ueberdeckung (Steg im Kragen) - 3 Ausklinkungen", Bd["Aufsatzrahmen"]["volume_mm3"], v_web + v_col - web_fp * ct - v_notch, 60)
    ck.eq("Dichtband Volumen (2 Pfosten + Sturz, ohne Doppelzaehlung der Ecken)", Bd["Dichtband"]["volume_mm3"], (2 * sw * Ly + (2 * xc + sw - 2 * sw) * sw) * st, 20)
    ck.eq("Klemmleiste Volumen", Bd["Klemmleiste"]["volume_mm3"], (2 * kw * Ly + (2 * xc + kw - 2 * kw) * kw) * kt, 20)
    ck.eq("Aufsatzrahmen steht auf der Zarge (Unterkante Z' = 15 = Zargenrohr-Oberflaeche)", bb("Aufsatzrahmen")["min"][2], r / 2, 0.01)
    ck.eq("Aufsatzrahmen Breite X = 2 x 523 + 20 (Kragen 40 breit)", bb("Aufsatzrahmen")["max"][0] - bb("Aufsatzrahmen")["min"][0], 2 * xc + cw, 0.05)
    ck.eq("Kragen-Oberkante Z' = Dichtband-Unterkante", bb("Aufsatzrahmen")["max"][2], bb("Dichtband")["min"][2], 0.01)
    ck.eq(f"Dichtband-Oberkante Z' {fp['foil_z0']:g} = innere Folienlage (liegt auf)", bb("Dichtband")["max"][2], fp["foil_z0"], 0.01)
    ck.eq(f"Klemmleiste-Unterkante = Folien-Oberflaeche ({fp['foil_z0']:g} + 0,15)", bb("Klemmleiste")["min"][2], fp["foil_z0"] + fp["foil_t"], 0.01)
    # Planenausschnitt der Folie liegt auf dem Dichtband
    ck.eq("Folien-Ausschnitt halbe Breite 513 = Dichtband-Innenkante (xc - seal_w/2)", G["zarge_aussen_w"] / 2 - fp["door_overlap"], xc - sw / 2, 0.01)
    ck.eq("Folien-Ausschnitt oben Y' 2043 = Dichtband-Innenkante oben (yc - seal_w/2)", G["zarge_hoehe"] - fp["door_overlap"], yc - sw / 2, 0.01)
    ck.eq("Folie liegt 30 mm auf dem Kragen (Ausschnitt-Kante zu Kragen-Aussenkante)", (xc + cw / 2) - (G["zarge_aussen_w"] / 2 - fp["door_overlap"]), 30.0, 0.01)
    ck.eq("Lichte Weite der Tuer bleibt frei: Aufsatzrahmen-Innenkante x = 521,5 > Blatt halbe Breite 500", 1 if (xc - wt / 2) > tp["blatt_w"] / 2 else 0, 1)
    ck.eq("Schwelle bleibt frei: Rahmen beginnt bei Y' = Schwellenhoehe 30", bb("Aufsatzrahmen")["min"][1], sh, 0.01)
    # Gemeinsames Design: Zarge + Aufsatzrahmen + Folie des Tuerfelds (Folien-KS: Inkreismittelpunkt, Ursprung 1070,4 ueber der Basiskante)
    rr = 3708 / (2 * math.sqrt(3))
    b = sc.Build()
    for nm, f in (("Tuer_Komplett", "tuer_komplett"), ("Zarge_Uebergang", "tuer_zarge_planenausschnitt"), ("Folie_Tuerfeld", "huelle_folie_BBB_tuer")):
        b.add("component.insert_design", path=comp(f).replace("\\", "/"), name=nm)
    b.add("occurrence.move", occurrence="Folie_Tuerfeld:1", matrix=[1, 0, 0, 0, 0, 1, 0, round(rr, 4), 0, 0, 1, 0], tolerance=1e-6, move_grounded=True)
    comb = os.path.join(sc.TMP, "ws-huelle-tuerfeld.sc")
    sc.run(b.write("huelle-tuerfeld"), comb)
    evc = sc.evaluate(comb)
    names = [x["name"] for x in evc["bodies"]]
    ck.eq("Gemeinsames Tuerfeld enthaelt Zarge, Tuerblatt, Aufsatzrahmen, Dichtband, Klemmleiste, 2 Folienlagen", 1 if all(any(n.endswith(x) or x in n for n in names) for x in ("Tuerblatt", "Aufsatzrahmen", "Dichtband", "Klemmleiste", "Folie_innen", "Folie_aussen")) else 0, 1)
    itf = interference(comb)
    for x in itf[:8]:
        print("   Interferenz", x)
    ck.eq("Interferenzen im Tuerfeld (Zarge, Tuerblatt, Aufsatzrahmen, Dichtband, Klemmleiste, Folie)", len(itf), 0)

def main(which):
    ck = sc.Check("huelle")
    if "zarge" in which:
        check_zarge(ck)
    if "keilschiene" in which:
        check_keilschiene(ck)
    if "folie" in which:
        check_folie(ck)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["keilschiene", "folie", "zarge"]))
