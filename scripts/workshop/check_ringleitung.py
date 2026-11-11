"""Pruefung Bauteile Ring B2 (ringleitung.py): Koerper, Ports (Stirnflaechen), Interferenz 0, Pegel-Hydraulik, Statik Ringstuetze, Abzweig = Bibliotheksgeometrie.
Aufruf: python -X utf8 scripts/workshop/check_ringleitung.py [pegelschacht|ringstuetze|entluefter|abzweig]   (exit 1 bei FAIL)"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import ringleitung as R
import check_lt_w36 as C

D = R.DC
G = 9.81

def port_faces(ck, tag, path, bodies, ports):
    fs = [f for v in sc.faces_multi(path, bodies).values() for f in v]
    planes = [(f["plane_normal"], f["centroid"]) for f in fs if f.get("plane_normal")]
    for name, pos, dr, art, dn in ports:
        hit = any(sum(n[i] * dr[i] for i in range(3)) > 0.999 and math.dist(c, pos) < 0.6 for n, c in planes)
        ck.eq(f"{tag} Port {name} ({art}, {dn}): Stirnflaeche bei {tuple(round(v, 1) for v in pos)}", 1 if hit else 0, 1)

def interf(ck, tag, path, extra=(), own=None):
    bad, res = C.interference(path, list(extra))
    if own is not None:
        bad = [i for i in bad if i.get("a") in own or i.get("b") in own]
    lib = [i for i in bad if str(i.get("a", "")).startswith("Kugelhahn_d") and str(i.get("b", "")).startswith("Kugelhahn_d")]
    if lib:
        print(f"INFO {tag}: {len(lib)} Ueberlappungen innerhalb des Bibliotheks-Kugelhahns (Spindel steckt bauartbedingt in Gehaeuse und Hebel, leitung.kugelhahn), nicht gezaehlt")
    bad = [i for i in bad if i not in lib]
    ck.eq(f"{tag} Interferenz 0 ({res.get('checked', '?')} Koerper inkl. Gegenstuecke)", len(bad), 0)
    for i in bad:
        print("   Ueberlappung:", i.get("a"), i.get("b"), round(i.get("volume_mm3", 0), 1))

def check_pegelschacht(ck):
    p, g = R.PS, R.ps_geom(); path = os.path.join(D, "pegelschacht.sc"); ev = sc.evaluate(path)
    names = {b["name"] for b in ev["bodies"]}
    soll = {"Fass", "Deckel", "Zulaufstutzen", "Saugstutzen_A", "Saugstutzen_B", "Notueberlauf", "Schwimmerstange", "Schwimmer_AUS", "Schwimmer_EIN", "Kabelverschraubung"}
    ck.eq("pegelschacht Koerper = Sollliste (10)", len(names ^ soll), 0)
    bb = {b["name"]: b for b in ev["bodies"]}
    f = bb["Fass"]
    ck.eq("pegelschacht Fass aussen D", f["bbox"]["max"][0] - f["bbox"]["min"][0], p["fass_d"], 0.5)
    ck.eq("pegelschacht Fass Hoehe", f["bbox"]["max"][2] - f["bbox"]["min"][2], p["fass_h"], 0.1)
    v_brutto = math.pi * g["ri"] ** 2 * (p["fass_h"] - p["boden"]) / 1e6
    ck.eq(f"pegelschacht Nenninhalt Fass {v_brutto:.1f} l (Handelsgroesse 60 l, +-10 %)", v_brutto, 60.0, 6.0)
    port_faces(ck, "pegelschacht", path, ["Zulaufstutzen", "Saugstutzen_A", "Saugstutzen_B", "Notueberlauf", "Kabelverschraubung"], [x for x in R.ps_ports() if x[0] != "Entlueftung"])
    ent = [x for x in R.ps_ports() if x[0] == "Entlueftung"][0]
    ck.eq(f"pegelschacht Port Entlueftung: Bohrung d{p['entl_d']:g} im Deckel bei {ent[1][:2]}", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - p["entl_d"] / 2) < 0.01 and math.hypot(f["cylinder"]["origin"][0] - ent[1][0], f["cylinder"]["origin"][1] - ent[1][1]) < 0.01 for f in sc.faces(path, "Deckel")) else 0, 1)
    interf(ck, "pegelschacht", path)
    # Pegel und Hydraulik
    di = p["saug_d"] - 2 * L.wall_p(p["saug_d"]); q = 55 / 60000; v = q / (math.pi / 4 * (di / 1000) ** 2); fr = v / math.sqrt(G * di / 1000)
    s_min = di * (1 + 2.3 * fr)
    ck.eq(f"pegelschacht Ueberdeckung Saugstutzen bei AUS {p['pegel_aus'] - p['saug_z']:g} >= S = D(1 + 2,3 Fr) = {s_min:.0f} mm (v {v:.2f} m/s, Fr {fr:.2f}, 55 l/min je Booster)", 1 if p["pegel_aus"] - p["saug_z"] >= s_min else 0, 1)
    ck.eq(f"pegelschacht Pegel steigend: Saugachse {p['saug_z']:g} < AUS {p['pegel_aus']:g} < EIN {p['pegel_ein']:g} < Ueberlauf-Sohle {g['sohle_ueberlauf']:.1f} < Fassrand {p['fass_h']:g}",
          1 if p["saug_z"] < p["pegel_aus"] < p["pegel_ein"] < g["sohle_ueberlauf"] < p["fass_h"] else 0, 1)
    ck.eq(f"pegelschacht Schwimmer EIN/AUS liegen auf ihrem Pegel (Mitte)", 1 if abs((bb["Schwimmer_EIN"]["bbox"]["min"][2] + bb["Schwimmer_EIN"]["bbox"]["max"][2]) / 2 - p["pegel_ein"]) < 0.1 and abs((bb["Schwimmer_AUS"]["bbox"]["min"][2] + bb["Schwimmer_AUS"]["bbox"]["max"][2]) / 2 - p["pegel_aus"]) < 0.1 else 0, 1)
    zu_unten = bb["Zulaufstutzen"]["bbox"]["min"][2]
    ck.eq(f"pegelschacht freier Einlauf: Zulauf-Unterkante {zu_unten:.0f} > Ueberlauf-Oberkante {p['ueberlauf_z'] + g['of_u'] / 2:.0f} (kein Rueckstau in K10)", 1 if zu_unten > p["ueberlauf_z"] + g["of_u"] / 2 else 0, 1)
    # Notueberlauf: volle Rohrstroemung bei 2 % Gefaelle (Manning n 0,009 PVC) muss den ganzen Zulauf (110 l/min) tragen, wenn beide Booster stehen
    dii = (p["ueberlauf_d"] - 2 * L.wall_p(p["ueberlauf_d"])) / 1000; Rh = dii / 4; qn = (1 / 0.009) * Rh ** (2 / 3) * 0.02 ** 0.5 * math.pi / 4 * dii ** 2 * 60000
    d50 = (50 - 2 * L.wall_p(50)) / 1000; q50 = (1 / 0.009) * (d50 / 4) ** (2 / 3) * 0.02 ** 0.5 * math.pi / 4 * d50 ** 2 * 60000
    ck.eq(f"pegelschacht Notueberlauf d{p['ueberlauf_d']} traegt {qn:.0f} l/min >= Zulauf 110 l/min (2 % Gefaelle; d50 waere nur {q50:.0f})", 1 if qn >= 110 else 0, 1)
    ck.eq(f"pegelschacht Schaltpuffer AUS-EIN {g['vol_aus_ein_l']:.1f} l >= 10 l (Booster-Takt bei 110 l/min Ueberschuss >= 5 s)", 1 if g["vol_aus_ein_l"] >= 10 else 0, 1)
    ring_l = math.pi / 4 * 0.0678 ** 2 * 10.7 * 1000
    print(f"INFO pegelschacht: Reserve EIN bis Ueberlauf {g['vol_ein_ueberlauf_l']:.1f} l < Rueckfluss eines Halbrings d75 x 10,7 m {ring_l:.1f} l -> bei Booster-Stopp laeuft der Rest ueber den Notueberlauf in den Ruecklauf (kein Wasserverlust); "
          f"Inhalt bis Ueberlauf {g['vol_bis_ueberlauf_l']:.1f} l; Masse leer {ev['total']['mass_g'] / 1000:.2f} kg")

def check_ringstuetze(ck):
    p, g = R.RS, R.rs_geom(); path = os.path.join(D, "ringstuetze_d75.sc"); ev = sc.evaluate(path)
    bb = {b["name"]: b for b in ev["bodies"]}
    soll = {"Fussplatte", "Pfosten", "Kragarm", "Gewindestange", "Rohrschelle", "Schelleneinlage", "Anker_1", "Anker_2", "Anker_3", "Anker_4"}
    ck.eq("ringstuetze Koerper = Sollliste (10)", len(set(bb) ^ soll), 0)
    fs = sc.faces(path, "Schelleneinlage")
    hit = [f["cylinder"] for f in fs if f.get("cylinder") and abs(f["cylinder"]["radius"] - p["rohr_d"] / 2) < 0.01 and abs(abs(f["cylinder"]["axis"][1]) - 1) < 1e-6]
    ck.eq(f"ringstuetze Port Rohrachse: Einlage-Bohrung d{p['rohr_d']:g}, Achse Y durch x {p['ausladung']:g} / z {p['achse_h']:g}", 1 if hit and abs(hit[0]["origin"][0] - p["ausladung"]) < 0.01 and abs(hit[0]["origin"][2] - p["achse_h"]) < 0.01 else 0, 1)
    fp = bb["Fussplatte"]["bbox"]
    ck.eq("ringstuetze Port Fuss: Fussplatte unten auf z 0", fp["min"][2], 0.0, 0.01)
    low = min(b["bbox"]["min"][2] for n, b in bb.items() if n in ("Rohrschelle", "Schelleneinlage"))
    ck.eq(f"ringstuetze tiefster Punkt der Schelle {low:.1f} >= Ring-Unterkante 2100 (Gang darunter frei)", 1 if low >= 2100 - 1e-6 else 0, 1)
    unter = [n for n, b in bb.items() if b["bbox"]["max"][2] < p["achse_h"] and b["bbox"]["max"][0] > p["ausladung"] - p["rohr_d"] / 2 - 50 and b["bbox"]["min"][0] < p["ausladung"] + p["rohr_d"] / 2 + 50 and n not in ("Rohrschelle", "Schelleneinlage")]
    ck.eq(f"ringstuetze nichts unter dem Rohr (Koerper im Streifen Rohr +- 50 unterhalb der Achse: {unter})", len(unter), 0)
    test = [{"command": "solid.cylinder", "params": {"diameter": p["rohr_d"], "height": 1650, "base": [p["ausladung"], -825, p["achse_h"]], "axis": [0, 1, 0], "operation": "new", "name": "T_Ring", "body_name": "Test_Ring_d75"}}]
    interf(ck, "ringstuetze", path, test)
    # Statik [E]: Feldlast d75 voll Wasser je Stuetze bei Abstand 1,65 m; Biegung Kragarm und Pfosten, Kopfverschiebung, Ankerzug
    q = (math.pi / 4 * (0.075 ** 2 - 0.0678 ** 2) * 1400 + math.pi / 4 * 0.0678 ** 2 * 1000) * G * 1.65
    M = q * p["ausladung"] / 1000
    def W(b, w): I = (b ** 4 - (b - 2 * w) ** 4) / 12; return I, I / (b / 2)
    Ip, Wp = W(p["pfosten_b"], p["pfosten_w"]); Ia, Wa = W(p["arm_b"], p["arm_w"])
    sp, sa = M * 1000 / Wp, M * 1000 / Wa
    Lp = g["z_top"]; delta = M * 1000 * Lp ** 2 / (2 * 210000 * Ip)
    zug = M / (p["anker_abstand"] / 1000) / 2
    ck.eq(f"ringstuetze Biegespannung Pfosten {sp:.1f} MPa und Kragarm {sa:.1f} MPa <= 100 MPa (S235 mit Sicherheit), Last {q:.0f} N, Moment {M:.1f} Nm", 1 if max(sp, sa) <= 100 else 0, 1)
    ck.eq(f"ringstuetze Kopfverschiebung Pfosten {delta:.2f} mm <= L/300 = {Lp / 300:.1f} mm", 1 if delta <= Lp / 300 else 0, 1)
    print(f"INFO ringstuetze: Ankerzug {zug:.0f} N je Seite (2 Anker M10), Hoehe {g['z_top']:.0f} + Mutter, Masse {ev['total']['mass_g'] / 1000:.2f} kg; Stuetzen je Halbring 10,7 / 1,65 -> 7")

def check_entluefter(ck):
    p, g = R.EL, R.el_geom(); path = os.path.join(D, "entluefter_d75.sc"); ev = sc.evaluate(path)
    bb = {b["name"]: b for b in ev["bodies"]}
    ck.eq("entluefter Koerper = T, Nippel, Ventil (3)", len(set(bb) ^ {"Entlueftungs_T", "Uebergangsnippel", "Entlueftungsventil"}), 0)
    t = bb["Entlueftungs_T"]["bbox"]
    ck.eq("entluefter Lauflaenge = lt_t_d75 (2 x 86,375)", t["max"][0] - t["min"][0], 2 * g["a"], 0.1)
    port_faces(ck, "entluefter", path, ["Entlueftungs_T", "Entlueftungsventil"], R.el_ports())
    fs = sc.faces(path, "Entlueftungs_T")
    ck.eq(f"entluefter Durchgang d{g['bore']:.1f} wie Rohr d75 (kein Querschnittsverlust im Ring)", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - g["bore"] / 2) < 0.01 and abs(abs(f["cylinder"]["axis"][0]) - 1) < 1e-6 for f in fs) else 0, 1)
    test = [{"command": "solid.cylinder", "params": {"diameter": 75, "height": 400, "base": [-g["a"] + L.DEPTH[75] - 400, 0, 0], "axis": [1, 0, 0], "operation": "new", "name": "T_A", "body_name": "Test_Rohr_A"}},
            {"command": "solid.cylinder", "params": {"diameter": 75, "height": 400, "base": [g["a"] - L.DEPTH[75], 0, 0], "axis": [1, 0, 0], "operation": "new", "name": "T_B", "body_name": "Test_Rohr_B"}}]
    interf(ck, "entluefter", path, test)
    print(f"INFO entluefter: Hoehe ueber Rohrachse {g['z_top']:.0f} mm (Ring-Achse 2145 + {g['z_top']:.0f} = {2145 + g['z_top']:.0f} rel), Masse {ev['total']['mass_g'] / 1000:.2f} kg")

def check_abzweig(ck):
    for dk in (40, 32):
        tag = f"abzweig d{dk}"; fn = f"ring_abzweig_d{dk}"; path = os.path.join(D, fn + ".sc"); ev = sc.evaluate(path)
        bb = {b["name"]: b for b in ev["bodies"]}
        soll = {"T_d75", "Rohrstueck_d75", "Reduzierung_75_50", "Rohrstueck_d50", f"Reduzierung_50_{dk}", f"Rohrstueck_d{dk}", f"Kugelhahn_d{dk}", f"Kugelhahn_d{dk}_Spindel", f"Kugelhahn_d{dk}_Hebel"}
        ck.eq(f"{tag} Koerper = Sollliste (9)", len(set(bb) ^ soll), 0)
        # Geometrie der Bibliotheksteile unveraendert: Volumen je Teil = Volumen der Bibliotheks-.sc
        for lib, body in (("lt_t_d75", "T_d75"), ("lt_reduzierung_d75_d50", "Reduzierung_75_50"), (f"lt_reduzierung_d50_d{dk}", f"Reduzierung_50_{dk}"), (f"lt_kugelhahn_d{dk}", f"Kugelhahn_d{dk}")):
            le = sc.evaluate(os.path.join(D, lib + ".sc")); lv = sum(b["volume_mm3"] for b in le["bodies"] if b["name"] in ("T_Stueck", "Reduzierung", "Kugelhahn"))
            ck.eq(f"{tag} {body} Volumen = Bibliothek {lib}", bb[body]["volume_mm3"], lv, lv * 1e-4)
        # Steckmass: jedes Rohrstueck steckt beidseits genau die Muffentiefe tief (Kette aus ringleitung.ab_kette)
        ch = R.ab_kette(dk)
        for art, f, d, za, zb in ch:
            if art != "rohr":
                continue
            b_ = bb[f"Rohrstueck_d{d}"]["bbox"]
            ck.eq(f"{tag} Rohrstueck d{d} Laenge {za - zb:g} = 2 x Muffentiefe {L.DEPTH[d]:g} + Spalt {R.SPALT:g}", b_["max"][2] - b_["min"][2], 2 * L.DEPTH[d] + R.SPALT, 0.05)
        port_faces(ck, tag, path, ["T_d75", f"Kugelhahn_d{dk}"], R.ab_ports(dk))
        interf(ck, tag, path)
        di = dk - 2 * L.wall_p(dk); q = (54.5 / 7 if dk == 40 else 38.0 / 12) / 60000; v = q / (math.pi / 4 * (di / 1000) ** 2)
        print(f"INFO {tag}: Laenge T-Achse bis Abgang {-ch[-1][4]:.1f} mm, Strom je Abnehmer {q * 60000:.1f} l/min, v {v:.2f} m/s im Abzweig d{dk}; Masse {ev['total']['mass_g'] / 1000:.2f} kg")

def main():
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or ["pegelschacht", "ringstuetze", "entluefter", "abzweig"]
    ck = sc.Check("ringleitung")
    for w in want:
        globals()["check_" + w](ck)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
