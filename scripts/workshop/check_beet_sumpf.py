"""Pruefung Beet-Sumpf T92 (W37-1 Teil 1): Teile, Tankmass, Innenvolumen bis ALARM und bis Oberkante gegen R45 (Oe 0,8 m ohne Wandabzug), Pegelhoehen der Schwimmer,
Einlaufsohle ueber ALARM, Ports (Lage gegen die gebauten Koerper, Richtung), Einbautiefe gegen den Beetablauf (Beet-Tausch), Interferenz 0.
Erwartungen aus R45 und den Parametern; Port-Lagen aus blatt.ports (nicht aus dem Generator). Volumen aus dem Hohlraum des Modells (Oe innen x Hoehe aus den Tank-bbox-Massen).
Aufruf: python -X utf8 scripts/workshop/check_beet_sumpf.py   (exit 1 bei FAIL)"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
from check_puffer_klein import interference

def xyz(s):
    return {k: float(v) for k, v in re.findall(r"([xyz]) (-?\d+)", s)}

def main():
    p, d = sc.load_params("beet_sumpf")
    path = os.path.join(sc.ROOT, "designs", "components", "beet_sumpf.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    bb = lambda n: B[n]["bbox"]
    ext = lambda n, i: (bb(n)["min"][i], bb(n)["max"][i])
    ck = sc.Check("beet_sumpf")
    cnt = lambda pre: len([k for k in B if k.startswith(pre)])
    n = int(p["pumpen"])
    ck.eq("Pumpen (E19: 2)", cnt("Pumpe_"), 2)
    ck.eq("Rueckschlagventile d40 (je Pumpe eins)", cnt("Rueckschlagventil_"), n)
    ck.eq("Schwimmer", cnt("Schwimmer_"), 3)
    ck.eq("Kabelverschraubungen (Pumpen/Schwimmer, Ablaufwaechter A+)", cnt("Kabelverschraubung_"), 2)
    ck.eq("Koerper gesamt", len(B), 23)
    # --- Tank
    tx, tz = ext("Tank", 0), ext("Tank", 2)
    ck.eq("Tank Aussen-Oe = 800", tx[1] - tx[0], 800, 0.2)
    ck.eq("Tank Hoehe = 1000", tz[1] - tz[0], 1000, 0.2)
    di = p["tank_d"] - 2 * p["tank_wall"]
    # Hohlraum aus der Modellmessung: Vollzylinder-Volumen minus gemessenes Koerpervolumen (Tank ist ein Koerper: Mantel, Boden, Schulter)
    v_full = math.pi / 4 * (tx[1] - tx[0]) ** 2 * (tz[1] - tz[0])
    v_hohl_mod = v_full - B["Tank"]["volume_mm3"]                  # Hohlraum + Oeffnung + Zulaufloch
    v_oeff = math.pi / 4 * p["oeffnung_d"] ** 2 * p["tank_wall"]
    v_inner = v_hohl_mod - v_oeff - math.pi / 4 * (L_od := 58.5) ** 2 * p["tank_wall"]
    v_soll_inner = math.pi / 4 * di ** 2 * (p["tank_h"] - p["tank_floor"] - p["tank_wall"])
    ck.eq(f"Hohlraum aus Messung {v_inner/1e6:.1f} l = Rechnung aus Wand/Boden {v_soll_inner/1e6:.1f} l", v_inner / 1e6, v_soll_inner / 1e6, 2.0)
    floor_in = p["tank_floor"]
    v_alarm = math.pi / 4 * di ** 2 * (p["pegel_alarm"] - floor_in) / 1e6
    r45_alarm = math.pi / 4 * 800 ** 2 * 620 / 1e6
    ck.eq(f"Volumen bis ALARM 620: {v_alarm:.1f} l gegen R45 310 l (+-5 %)", v_alarm, 310, 310 * 0.05)
    ck.eq(f"R45-Rechnung Oe 0,8 x 620 = {r45_alarm:.1f} l (Gegenprobe der Sollzahl)", r45_alarm, 310, 310 * 0.05)
    v_voll = v_soll_inner / 1e6
    ck.eq(f"Tankinhalt bis Oberkante {v_voll:.1f} l gegen 500 l (+-7 %)", v_voll, 500, 35)
    # --- Pegel der Schwimmer (Mitte ueber Tankboden)
    for nm, soll in (("AUS", 120), ("EIN", 320), ("ALARM", 620)):
        z = ext(f"Schwimmer_{nm}", 2)
        ck.eq(f"Schwimmer {nm} Mitte = {soll} mm", (z[0] + z[1]) / 2, soll, 0.5)
    zz = ext("Zulauf_Tankverbinder", 2)
    sohle = (zz[0] + zz[1]) / 2 - p["zulauf_d"] / 2
    ck.eq("Einlauf-Rohrsohle = 800 mm ueber Tankboden", sohle, 800, 0.5)
    ck.eq("Einlaufsohle ueber ALARM (Abstand > 0, R45 Punkt 4)", 1 if sohle - p["pegel_alarm"] > 0 else 0, 1)
    # --- Einbautiefe gegen den Beetablauf (flur-relativ): Tankboden = -(tank_h + aufsatz_h); Sohle flur-relativ <= -375
    boden = -(p["tank_h"] + p["aufsatz_h"])
    sohle_flur = boden + sohle
    ck.eq(f"Einlaufsohle flur-relativ {sohle_flur:.0f} <= -375 (Beetablauf-Achse -290, d50/2, 1 % auf 6 m)", 1 if sohle_flur <= -375 else 0, 1)
    dz = ext("Deckel", 2)
    ck.eq(f"Deckeloberkante flur-relativ {boden + dz[1]:.0f} (buendig bis +50)", 1 if 0 <= boden + dz[1] <= 50 else 0, 1)
    # --- Ports gegen die Koerper
    P = {r[0].split(" (")[0].split(" zum")[0]: r for r in d["blatt"]["ports"]}
    def port(key):
        return next(r for r in d["blatt"]["ports"] if r[0].startswith(key))
    z = port("Zulauf"); c = xyz(z[2])
    ck.eq("Port Zulauf DN d50 (Netz V3 K14/K30)", 1 if "d50" in z[1] else 0, 1)
    ck.eq("Port Zulauf x = Muffenebene", c["x"], ext("Zulauf_Tankverbinder", 0)[0], 0.6)
    ck.eq("Port Zulauf z = Achse", c["z"], (zz[0] + zz[1]) / 2, 0.6)
    ck.eq("Port Zulauf Richtung -X", 1 if z[3] == "-X" else 0, 1)
    ck.eq("Port Zulauf nennt K14 und K30", 1 if "K14" in z[0] and "K30" in z[0] else 0, 1)
    f = port("Foerderleitung"); c = xyz(f[2])
    ck.eq("Port Foerderleitung DN d40", 1 if "d40" in f[1] else 0, 1)
    ck.eq("Port Foerderleitung z = Oberkante Durchfuehrung", c["z"], ext("Durchfuehrung_Foerder", 2)[1], 0.6)
    ck.eq("Port Foerderleitung Richtung +Z", 1 if f[3] == "+Z" else 0, 1)
    ck.eq("Port Foerderleitung nennt K58 und K59", 1 if "K58" in f[0] and "K59" in f[0] else 0, 1)
    for k in (1, 2):
        kp = port(f"Kabeldurchfuehrung {k}"); c = xyz(kp[2])
        ck.eq(f"Port Kabel {k} z = Oberkante Verschraubung", c["z"], ext(f"Kabelverschraubung_{k}", 2)[1], 0.6)
    e = port("Entlueftung"); c = xyz(e[2])
    ck.eq("Port Entlueftung z = Oberkante Gitterkappe", c["z"], ext("Insektengitter_Kappe", 2)[1], 0.6)
    # --- Lage im Tank
    for k in range(1, n + 1):
        x0, x1 = ext(f"Pumpe_{k}", 0); y0, y1 = ext(f"Pumpe_{k}", 1)
        r = max(math.hypot(x, y) for x in (x0, x1) for y in (y0, y1))
        ck.eq(f"Pumpe {k} Ecken innerhalb der Tankwand (r {r:.0f} < {di/2:.0f})", 1 if r < di / 2 else 0, 1)
    # --- Interferenz
    it = interference(path)
    ck.eq("Interferenz (Paare mit Volumen)", len([x for x in it if (x.get("volume_mm3") or x.get("volume") or 0) > 1e-3]), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
