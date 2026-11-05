"""Pruefung Biofilter Drittbecken T98 (N-REWORK B): Fassmass (zwei Quellen), Bettvolumen 37 l (+-2 %) aus dem Modell, Verweilzeit im Bett bei 5 l/min,
Wasserstand ueber der Lochplatte, Tauchrohr endet unter dem Bett, Durchgaenge d25, Ports (Lage gegen Modell), Netz-Kanten K42/K43, Interferenz 0.
Aufruf: python -X utf8 scripts/workshop/check_biofilter_dritt.py [--sc <datei>]   (exit 1 bei FAIL)"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import biofilter_dritt as BF
from check_puffer_klein import interference

def xyz(s):
    return {k: float(v) for k, v in re.findall(r"([xyz]) (-?\d+)", s)}

def main():
    path = sys.argv[sys.argv.index("--sc") + 1] if "--sc" in sys.argv else os.path.join(sc.ROOT, "designs", "components", "biofilter_dritt.sc")
    p, d = sc.load_params("biofilter_dritt"); D = BF.derive(p)
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ext = lambda n, i: (B[n]["bbox"]["min"][i], B[n]["bbox"]["max"][i])
    ck = sc.Check("biofilter_dritt")
    ck.eq("Koerper (Fass, Deckel, Zulaufstutzen, Tauchrohr, Bioballs, Lochplatte, Auslaufstutzen)", len(B), 7)
    ck.eq("alle Koerper geschlossen", sum(1 for b in B.values() if b["closed"]), 7)
    ck.eq("Koerper mit Material Default", sum(1 for b in B.values() if b["material"] == "Default"), 0)
    fx = ext("Fass", 0)
    ck.eq("Fass Oe 398 (Graf 824410; Haendler 400)", fx[1] - fx[0], 398, 0.2)
    ck.eq("Fass H mit Deckel 625 (Graf 824410)", ext("Deckel", 2)[1] - ext("Fass", 2)[0], 625, 0.2)
    v_innen = math.pi / 4 * (p["fass_d"] - 2 * p["fass_wall"]) ** 2 * (p["fass_h"] - p["fass_floor"]) / 1e6
    ck.eq(f"Innenvolumen Zylinder {v_innen:.1f} l >= Nennvolumen 60 l", 1 if v_innen >= 60 else 0, 1)
    vb = B["Bioballs"]["volume_mm3"] / 1e6
    ck.eq(f"Bettvolumen aus Modell {vb:.2f} l = 37 l (R37) +-2 %", vb, 37, 0.74)
    ebct = vb / p["durchfluss"]
    ck.eq(f"Verweilzeit im Bett {ebct:.1f} min bei {p['durchfluss']:g} l/min (Leerbett) >= 5", 1 if ebct >= 5 else 0, 1)
    sz = ext("Lochplatte", 2)
    ck.eq("Bett liegt unter der Lochplatte (Oberkante Bett = Unterkante Platte)", ext("Bioballs", 2)[1], sz[0], 0.05)
    ck.eq(f"Wasserstand (Auslauf-Unterkante Durchgang {p['auslauf_z'] - D['di'] / 2:.1f}) ueber der Lochplatte {sz[1]:g} um >= 50", 1 if p["auslauf_z"] - D["di"] / 2 - sz[1] >= 50 else 0, 1)
    tz = ext("Tauchrohr", 2)
    ck.eq(f"Tauchrohr endet unter dem Bett (Unterkante {tz[0]:g} < Bett {ext('Bioballs', 2)[0]:.1f})", 1 if tz[0] < ext("Bioballs", 2)[0] else 0, 1)
    ck.eq("Tauchrohr ueber dem Fassboden (Abstand > 0)", 1 if tz[0] > p["fass_floor"] else 0, 1)
    ck.eq("Tauchrohr steckt 16 mm in der unteren Muffe des Zulaufstutzens", tz[1] - ext("Zulaufstutzen", 2)[0], 16, 0.05)
    # Durchgaenge: Volumen der Stutzen und des Tauchrohrs = Rechnung (Ringquerschnitte)
    ri, rm, ro = D["di"] / 2, p["rohr_d"] / 2, D["st_od"] / 2
    t = L.DEPTH[p["rohr_d"]]
    h_st = D["st_top"] - D["st_bot"]
    v_st = math.pi * (ro ** 2 * h_st - rm ** 2 * (t + (D["st_anschlag"][0] - D["st_bot"])) - ri ** 2 * 4)
    ck.eq("Zulaufstutzen: Muffe oben 19, Anschlag 4, Muffe unten 16 (Volumen)", B["Zulaufstutzen"]["volume_mm3"], v_st, 1e-3 * v_st)
    v_t = math.pi * (rm ** 2 - ri ** 2) * (tz[1] - tz[0])
    ck.eq("Tauchrohr d25 x 1,8 offen (Volumen)", B["Tauchrohr"]["volume_mm3"], v_t, 1e-3 * v_t)
    h_a = D["aus_x1"] - D["aus_x0"]
    v_a = math.pi * (ro ** 2 * h_a - rm ** 2 * t - ri ** 2 * (h_a - t))
    ck.eq("Auslaufstutzen: Muffe aussen 19, Durchgang d21,4 (Volumen)", B["Auslaufstutzen"]["volume_mm3"], v_a, 1e-3 * v_a)
    # Ports gegen Modell
    P = {r[0].split(" ")[0]: r for r in d["blatt"]["ports"]}
    c = xyz(P["Zulauf"][2])
    ck.eq("Port Zulauf z = Oberkante Zulaufstutzen", c["z"], ext("Zulaufstutzen", 2)[1], 0.6)
    ck.eq("Port Zulauf x = Achse Zulaufstutzen", c["x"], sum(ext("Zulaufstutzen", 0)) / 2, 0.6)
    c = xyz(P["Auslauf"][2])
    ck.eq("Port Auslauf x = Aussenende Tankverbinder", c["x"], ext("Auslaufstutzen", 0)[1], 0.6)
    ck.eq("Port Auslauf z = Achse Tankverbinder", c["z"], sum(ext("Auslaufstutzen", 2)) / 2, 0.6)
    ck.eq("Port Auslauf Richtung +X", 1 if P["Auslauf"][3] == "+X" else 0, 1)
    # Netz: Knoten und Kanten
    net = json.load(open(os.path.join(sc.ROOT, "data", "leitungsnetz.json"), encoding="utf-8"))
    K = {k["id"]: k for k in net["kanten"]}
    ck.eq("Netz K42 drittbecken -> biofilter_dritt dn 25", 1 if K["K42"]["nach"] == "biofilter_dritt" and K["K42"]["dn"] == p["rohr_d"] else 0, 1)
    ck.eq("Netz K43 biofilter_dritt -> drittbecken dn 25", 1 if K["K43"]["von"] == "biofilter_dritt" and K["K43"]["dn"] == p["rohr_d"] else 0, 1)
    ck.eq("Durchfluss = Netz K42", p["durchfluss"], K["K42"]["soll_l_min"])
    v = 5 / 60000 / (math.pi / 4 * (D["di"] / 1000) ** 2)
    ck.eq(f"Geschwindigkeit im Auslauf d{D['di']:.1f}: {v:.2f} m/s <= 0,5 (Schwerkraft)", 1 if v <= 0.5 else 0, 1)
    it = interference(path)
    for x in it[:5]:
        print("   Interferenz:", x.get("a"), x.get("b"), round(x.get("volume_mm3", 0), 1))
    ck.eq("Interferenz (Paare)", len(it), 0)
    print(f"INFO biofilter_dritt: Masse leer {sum(b['mass_g'] for b in B.values()) / 1000:.2f} kg (davon Bioballs {B['Bioballs']['mass_g'] / 1000:.2f} kg Ersatzdichte 0,15), Bett {vb:.2f} l, Verweilzeit {ebct:.1f} min")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
