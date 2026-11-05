"""Pruefung WA-S (docs/jobs/N-AUTOBAHN-V2.md Abschnitt 3, Spalte Pruefung): WA5 Fallleitungen, WA6 Schnellkupplung, WA8 Rueckschlagventil d50,
WA9 Ruecklauf-Rinne, Bodenrinne mit Rost, Schlauch d50. Misst an den gebauten .sc (designs/components), nicht an den Generator-Parametern,
wo das geht: Schlauchlaengen aus Volumen / Ringflaeche (Pappus, gilt fuer Gerade und Bogen), Biegeradius aus dem Bogenvolumen, Lagen aus Huellboxen.
Aufruf: python -X utf8 scripts/workshop/check_autobahn_s.py [kupplung|rsv|fall|rinne|bodenrinne|schlauch50|d85]   (exit 1 bei FAIL)"""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import autobahn_s as A
import ring_b2 as R
from check_ring_b2 import port_faces, interf

D = A.DC
BLATT = os.path.join(sc.ROOT, "docs", "parts", "autobahn.md")

def ev_bodies(path):
    ev = sc.evaluate(path); return ev, {b["name"]: b for b in ev["bodies"]}

def ext(bb, i): return bb["bbox"]["max"][i] - bb["bbox"]["min"][i]

def check_kupplung(ck):
    for i in (19, 25):
        tag = f"kupplung ID{i}"; path = os.path.join(D, f"lt_schnellkupplung_id{i}.sc"); ev, bb = ev_bodies(path)
        ck.eq(f"{tag} Koerper = Dose + Stecker (2)", len(set(bb) ^ {"Kupplung_Dose", "Kupplung_Stecker"}), 0)
        lz = max(b["bbox"]["max"][2] for b in bb.values()) - min(b["bbox"]["min"][2] for b in bb.values())
        ck.eq(f"{tag} Baulaenge gekuppelt", lz, A.sk_len(i), 0.05)
        port_faces(ck, tag, path, ["Kupplung_Dose", "Kupplung_Stecker"], A.kupplung_ports(i))
        interf(ck, tag, path)
        dens = [b["mass_g"] / b["volume_mm3"] * 1000 for b in bb.values()]
        ck.eq(f"{tag} Werkstoff Edelstahl 1.4401 (Dichte 7,95 g/cm3, kein Messing)", max(abs(x - 7.95) for x in dens), 0.0, 0.01)

def check_rsv(ck):
    path = os.path.join(D, "lt_rueckschlagventil_d50.sc"); ev, bb = ev_bodies(path); g = A.rsv_geom()
    ck.eq("rsv Koerper = Rueckschlagventil (1)", len(set(bb) ^ {"Rueckschlagventil"}), 0)
    ck.eq(f"rsv Baulaenge = Herstellerwert {A.RSV['L']:g}", ext(bb["Rueckschlagventil"], 2), A.RSV["L"], 0.05)
    ck.eq(f"rsv Gehaeuse aussen = Herstellerwert {A.RSV['ob']:g}", ext(bb["Rueckschlagventil"], 0), A.RSV["ob"], 0.05)
    port_faces(ck, "rsv", path, ["Rueckschlagventil"], A.rsv_ports())
    dp = g["dp"]
    test = [{"command": "solid.cylinder", "params": {"diameter": 50, "height": 300, "base": [0, 0, dp - 300], "axis": [0, 0, 1], "operation": "new", "name": "T_A", "body_name": "Test_Rohr_A"}},
            {"command": "solid.cylinder", "params": {"diameter": 50, "height": 300, "base": [0, 0, A.RSV["L"] - dp], "axis": [0, 0, 1], "operation": "new", "name": "T_B", "body_name": "Test_Rohr_B"}}]
    interf(ck, "rsv", path, test)
    print(f"INFO rsv: Muffentiefe {dp:g}, Durchgang d{g['wi']:.1f}, Masse {ev['total']['mass_g']:.0f} g; 4 Stueck (je Booster eines, Blatt 2.1)")

def hose_bodies(bb):
    return {n: b for n, b in bb.items() if n.startswith("Schlauch_")}

def gang_band(zone):
    """Gang neben der Abnehmer-Zone entlang der Ecklinie (radial, Abstand von der Ringecke): A innen 2195..2695, B aussen 3858..4359 (Apothem, docs/parts/nft_tisch.md)."""
    c = math.cos(A.NR.HALB)
    if zone == "innen":
        return ("A", A.R_ECKE - 2695 / c, A.R_ECKE - 2195 / c)
    return ("B", 3858 / c - A.R_ECKE, 4359 / c - A.R_ECKE)

def check_fall(ck):
    for t in A.TYPES:
        g = A.fall_geom(t); tag = f"fall {t}"; path = os.path.join(D, f"schlauch_fall_{t}.sc"); ev, bb = ev_bodies(path)
        idd, ad, Rb = g["idd"], g["ad"], g["Rb"]
        soll = {"Tuelle_oben", "Regelhahn", "Kupplung_Dose", "Kupplung_Stecker", "Anschluss"}
        ck.eq(f"{tag} Glieder vorhanden: Tuelle, Regelhahn, Kupplung (2), Anschluss", len(soll - set(bb)), 0)
        hb = hose_bodies(bb); area = math.pi / 4 * (ad ** 2 - idd ** 2)
        l_hose = sum(b["volume_mm3"] for b in hb.values()) / area
        bends = {n: b for n, b in hb.items() if re.search(r"_B\d+$", n)}
        n_b_soll = 1 if g["fall"] else 4
        ck.eq(f"{tag} Schlauchboegen ({'unten 1' if g['fall'] else 'Anstieg 2 x 45 Grad, Auslegerende 1, unten 1'}) = {n_b_soll}", len(bends), n_b_soll)
        th = {}
        for pre, pts in (("Schlauch_1", g["s1"]), ("Schlauch_3", g["s3"])):
            for n, sg in enumerate(A.hose_layout(pts, Rb), 1):
                if sg[0] == "B":
                    th[f"{pre}_B{n}"] = sg[6]
        r_ist = [b["volume_mm3"] / area / th[n] for n, b in bends.items()]
        r_min = max(6 * ad, A.HOSE[idd]["r_hersteller"])
        ck.eq(f"{tag} Biegeradius aus Bogenvolumen min {min(r_ist):.1f} >= max(6 x AD {6 * ad:g}, Hersteller {A.HOSE[idd]['r_hersteller']:g}) (R14)", 1 if min(r_ist) >= r_min - 0.5 else 0, 1)
        # Weg Ring-Achse -> Abnehmer-Port: Abzweig-Kette (T97) + Kragen + Schlaeuche + Koerper der Glieder entlang der Achse
        reg_l = ext(bb["Regelhahn"], 2) - 2 * g["tl"]                       # Hahn ohne die beiden Tuellen (stecken im Schlauch)
        kup_l = (max(bb["Kupplung_Dose"]["bbox"]["max"][2], bb["Kupplung_Stecker"]["bbox"]["max"][2]) - min(bb["Kupplung_Dose"]["bbox"]["min"][2], bb["Kupplung_Stecker"]["bbox"]["min"][2])) - 2 * g["tl"]
        an = bb["Anschluss"]; an_l = (ext(an, 1) if abs(g["end_dir"][1]) > 0.5 else ext(an, 0)) - g["tl"]
        weg = g["al"] + A.FT["kragen"] + l_hose + reg_l + kup_l + an_l
        ck.eq(f"{tag} Weg Ring-Achse bis Abnehmer {weg:.0f} = Rechnung {g['soll']:.0f} + Anstieg zum Ausleger {g['soll_korr'] - g['soll']:.0f} = {g['soll_korr']:.0f} (+-50; Abzweig {g['al']:.0f} + Schlauch {l_hose:.0f} + Glieder {A.FT['kragen'] + reg_l + kup_l + an_l:.0f})", weg, g["soll_korr"], 50)
        # Port-Lage aus dem gebauten Anschluss: Stirnflaeche auf Ziel-Hoehe
        z_port_rel = (an["bbox"]["min"][2] + an["bbox"]["max"][2]) / 2 + g["z0"]
        ck.eq(f"{tag} Anschluss-Achse auf Ziel-Hoehe Z {g['z_ziel']:g} rel ({'Tisch-Zulaufverteiler' if g['art'] == 'tisch' else 'Beet-Tropfrohr'})", z_port_rel, g["z_ziel"], 0.5)
        port_faces(ck, tag, path, ["Tuelle_oben", "Anschluss"], A.fall_ports(t))
        # Regelhahn auf Greifhoehe 1000..1600 rel [A, Ergonomie wie Rinnenunterkante 950..1050 R35 plus Armreichweite]
        zh = (bb["Regelhahn"]["bbox"]["min"][2] + bb["Regelhahn"]["bbox"]["max"][2]) / 2 + g["z0"]
        ck.eq(f"{tag} Regelhahn-Mitte Z {zh:.0f} rel in Greifhoehe 1000..1600", 1 if 1000 <= zh <= 1600 else 0, 1)
        # Gang: Unterkante aller Koerper ueber dem Gang >= Z 2100 rel; freier Fall <= 1500 (Blatt 2.6 Punkt 3)
        if not g["fall"]:
            gang, x0, x1 = gang_band(g["T"]["zone"])
            lx0, lx1 = x0 - g["al"], x1 - g["al"]               # lokal (Ursprung = Abzweig-Abgang, al vor der Ringachse)
            im_gang = [b for b in bb.values() if b["bbox"]["max"][0] > lx0 and b["bbox"]["min"][0] < lx1]
            z_low = min(b["bbox"]["min"][2] for b in im_gang) + g["z0"]
            ck.eq(f"{tag} Gang {gang} (lokal x {lx0:.0f}..{lx1:.0f}): tiefster Punkt Z {z_low:.1f} rel >= {A.Z_UK:g}", 1 if z_low >= A.Z_UK - 1e-6 else 0, 1)
            x_bogen = g["x_v"] - Rb
            ck.eq(f"{tag} Bogen am Auslegerende beginnt hinter dem Gang (x {x_bogen:.0f} >= {lx1:.0f})", 1 if x_bogen >= lx1 else 0, 1)
            halter = [A.FT["kragen"] + k * 400 for k in range(int((x_bogen - 10) // 400) + 1)] + [x_bogen]
            gaps = [halter[k + 1] - halter[k] for k in range(len(halter) - 1)]
            print(f"INFO {tag}: Schlauchhalter am Ausleger (WA-T) bei lokal x {[round(h) for h in halter]} (groesste Luecke {max(gaps):.0f} <= 400); Achse auf Z {A.Z_AUSLEGER:g} rel (Armmitte), seitlich in den Clips des Auslegers")
            fall_l = (A.Z_AUSLEGER - Rb) - (g["z_ziel"] + Rb)
        else:
            corner_r = A.R_ECKE
            ok = all(not (lo <= corner_r <= hi) for lo, hi in ((2195 / math.cos(A.NR.HALB), 2695 / math.cos(A.NR.HALB)), (3858 / math.cos(A.NR.HALB), 4359 / math.cos(A.NR.HALB))))
            ck.eq(f"{tag} faellt an der Ringecke r {corner_r:.0f} (kein Gang darunter)", 1 if ok else 0, 1)
            fall_l = (g["z0"] - A.FT["kragen"]) - (g["z_ziel"] + Rb)
        ck.eq(f"{tag} freier Fall ohne Halter {fall_l:.0f} mm <= 1500 (Blatt 2.6 Punkt 3; unten haelt der Abnehmer-Anschluss)", 1 if fall_l <= 1500 else 0, 1)
        interf(ck, tag, path)
        print(f"INFO {tag}: Schlauch ID{idd}/AD{ad:g} Zuschnitt {l_hose:.0f} mm (Rechnung zaehlte {g['soll']:.0f} als Schlauch), Biegeradius {Rb:g}, Endstueck waagerecht {g['a']:.0f} (Schlaufe 300 + Bogenverkuerzung {g['loss']:.0f}), Masse {ev['total']['mass_g'] / 1000:.2f} kg")

def check_rinne(ck):
    p, g = A.RR, A.rr_geom(); path = os.path.join(D, "ruecklauf_rinne.sc"); ev, bb = ev_bodies(path)
    ck.eq("rinne Koerper = Rinne + 2 Konsolen", len(set(bb) ^ {"Rinne", "Konsole_1", "Konsole_2"}), 0)
    ck.eq(f"rinne Breite innen {p['b_innen']:g} (Schlauch d50 AD {A.HOSE[50]['ad']:g} passt)", 1 if p["b_innen"] >= A.HOSE[50]["ad"] + 10 else 0, 1)
    ad = A.HOSE[50]["ad"]
    test = [{"command": "solid.cylinder", "params": {"diameter": ad, "height": p["L"], "base": [-p["L"] / 2, 0, p["t"] + ad / 2 + 0.1], "axis": [1, 0, 0], "operation": "new", "name": "T_S", "body_name": "Test_Schlauch_d50"}}]
    for i, x in enumerate(g["xs"], 1):
        test.append({"command": "solid.box", "params": {"length": p["bein"], "width": p["bein"], "height": 1200, "center": [x, g["y_bein"], -500], "operation": "new", "name": f"T_B{i}", "body_name": f"Test_Tischbein_{i}"}})
    interf(ck, "rinne", path, test)
    gef = p["langloch"] / p["kons_abstand"] * 100
    ck.eq(f"rinne Gefaelle einstellbar bis {gef:.2f} % (Langloch {p['langloch']:g} / Konsolenabstand {p['kons_abstand']:g}) >= 1 % (R11)", 1 if gef >= 1.0 else 0, 1)
    ck.eq(f"rinne Konsolenabstand {p['kons_abstand']:g} <= Stuetzabstand Hersteller {p['stuetz_max']:g}", 1 if p["kons_abstand"] <= p["stuetz_max"] else 0, 1)
    print(f"INFO rinne: Rechnung Abschn. 4: Gefaellebedarf laengster Weg 128 mm bei 1 %, verfuegbar >= 225 mm; Schlauch liegt auf (R6 'aufliegend'); Masse {ev['total']['mass_g'] / 1000:.2f} kg je {p['L']:g}")

def check_bodenrinne(ck):
    p = A.BR; ad = A.HOSE[50]["ad"]
    for gg in ("A", "B"):
        tag = f"bodenrinne Gang {gg}"; path = os.path.join(D, f"bodenrinne_rost_gang{gg.lower()}.sc"); ev, bb = ev_bodies(path); Lr = A.br_len(gg)
        ck.eq(f"{tag} Koerper = Rinnenkoerper + Gitterrost", len(set(bb) ^ {"Rinnenkoerper", "Gitterrost"}), 0)
        ck.eq(f"{tag} Rost-Oberkante = Boden Z 0 rel (+-2)", bb["Gitterrost"]["bbox"]["max"][2], 0.0, 2.0)
        ck.eq(f"{tag} Rinnenkoerper-Oberkante = Boden Z 0 rel (+-2)", bb["Rinnenkoerper"]["bbox"]["max"][2], 0.0, 2.0)
        ck.eq(f"{tag} Laenge {Lr:g} >= Gang {p['gang'][gg]:g} + 2 x 300", 1 if Lr >= p["gang"][gg] + 600 else 0, 1)
        # Schlauch d50 mit 1 % Gefaelle ueber die ganze Laenge: Testkoerper geneigt, darf weder Rost noch Boden beruehren
        z_top = -(p["rost_t"] + 2 + ad / 2); s = 0.01; u = [1 / math.sqrt(1 + s * s), 0, -s / math.sqrt(1 + s * s)]
        test = [{"command": "solid.cylinder", "params": {"diameter": ad, "height": Lr, "base": [-Lr / 2, 0, z_top], "axis": u, "operation": "new", "name": "T_S", "body_name": "Test_Schlauch_1pct"}}]
        interf(ck, tag, path, test)
        z_end = z_top - Lr * s - ad / 2
        ck.eq(f"{tag} Schlauch mit 1 % passt: tiefster Punkt {z_end:.0f} >= Rinnensohle {-p['h_innen']:g}", 1 if z_end >= -p["h_innen"] else 0, 1)
        print(f"INFO {tag}: Schlauch-Sohle am Ende Z {z_end:.0f} rel liegt unter dem Pool-Spiegel Z 515 rel -> Weiterfuehrung nur als Einmuendung unter Wasser (Wanddurchfuehrung, grund 'pool_einmuendung'), nicht ueber den Halbring K16/K32 auf der Krone; Masse {ev['total']['mass_g'] / 1000:.2f} kg")

def check_schlauch50(ck):
    path = os.path.join(D, "lt_schlauch_d50.sc"); ev, bb = ev_bodies(path); s = bb["Schlauch"]
    ck.eq("schlauch50 Aussen-D", ext(s, 1), A.HOSE[50]["ad"], 0.05)
    ck.eq("schlauch50 Innen-D 50 aus Volumen", math.sqrt(A.HOSE[50]["ad"] ** 2 - s["volume_mm3"] / A.S50_L * 4 / math.pi), 50.0, 0.1)
    ck.eq(f"schlauch50 Biegeradius {A.hose_R(50):g} >= max(6 x AD, Hersteller) (R14)", 1 if A.hose_R(50) >= max(6 * A.HOSE[50]["ad"], A.HOSE[50]["r_hersteller"]) else 0, 1)

def check_d85(ck):
    """Lebensmitteleignung (D85) im Teileblatt belegt: je Zeile der WA-S-Werkstofftabelle zwei Quellen (URL)."""
    txt = open(BLATT, encoding="utf-8").read() if os.path.exists(BLATT) else ""
    sec = txt.split("<!-- WA-S Anfang -->")[-1].split("<!-- WA-S Ende -->")[0] if "<!-- WA-S Anfang -->" in txt else ""
    for key in ("Schlauch ID19", "Schlauch ID25", "Schlauch d50", "Schnellkupplung", "Rueckschlagventil d50", "Regelhahn"):
        rows = [ln for ln in sec.splitlines() if ln.startswith("|") and key in ln and "D85" in ln]
        n = max((len(set(re.findall(r"https?://[^\s|)]+", ln))) for ln in rows), default=0)
        ck.eq(f"d85 Teileblatt: {key} lebensmittelecht mit >= 2 Quellen", 1 if n >= 2 else 0, 1)

def main():
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or ["kupplung", "rsv", "fall", "rinne", "bodenrinne", "schlauch50", "d85"]
    ck = sc.Check("autobahn_s")
    for w in want:
        globals()["check_" + w](ck)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
