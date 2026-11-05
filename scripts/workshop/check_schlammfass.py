"""Pruefung Schlammfass T93 (W37-1 Teil 2): Fassmass, Volumen 200-220 l (+-5 %) aus Oe und H (Blatt Pruefpunkt 4) und Innenvolumen aus dem Modell,
Stutzen d40 Mitte Deckel, Bohrungen Oe 8 und Oe 20, kein Auslass (Mantel und Boden ohne Durchbruch), Ports, Gruben-Parameter, Interferenz 0.
Aufruf: python -X utf8 scripts/workshop/check_schlammfass.py   (exit 1 bei FAIL)"""
import math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
from check_puffer_klein import interference

def xyz(s):
    return {k: float(v) for k, v in re.findall(r"([xyz]) (-?\d+)", s)}

def main():
    p, d = sc.load_params("schlammfass")
    path = os.path.join(sc.ROOT, "designs", "components", "schlammfass.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ext = lambda n, i: (B[n]["bbox"]["min"][i], B[n]["bbox"]["max"][i])
    ck = sc.Check("schlammfass")
    ck.eq("Koerper (Fass, Deckel, Spannring, Einlaufstutzen, Entlueftungsstutzen)", len(B), 5)
    fx = ext("Fass", 0)
    D = fx[1] - fx[0]
    H = ext("Deckel", 2)[1] - ext("Fass", 2)[0]
    ck.eq("Fass Oe = 580 (R45: 580-600)", D, 580, 0.2)
    ck.eq("Fass H mit Deckel = 880 (R45: 880-920)", H, 880, 0.2)
    v_aussen = math.pi / 4 * D ** 2 * H / 1e6
    di = D - 2 * p["fass_wall"]; hi = ext("Fass", 2)[1] - p["fass_floor"]
    v_innen = math.pi / 4 * di ** 2 * hi / 1e6
    v_mod = (math.pi / 4 * D ** 2 * (ext("Fass", 2)[1] - ext("Fass", 2)[0]) - B["Fass"]["volume_mm3"]) / 1e6
    print(f"INFO schlammfass: Volumen aus Aussen-Oe und H (Huellzylinder inkl. Wand und Deckel) {v_aussen:.1f} l; Nennvolumen = Innenraum (naechste Zeilen)")
    ck.eq(f"Innenvolumen Rechnung {v_innen:.1f} l im Band 190-231", 1 if 190 <= v_innen <= 231 else 0, 1)
    ck.eq(f"Innenvolumen aus Modell {v_mod:.1f} l = Rechnung", v_mod, v_innen, 0.5)
    ck.eq(f"Fassung >= 105 l/Woche plus Reserve (Innen {v_innen:.0f} l)", 1 if v_innen >= 2 * 105 else 0, 1)
    sx, sy = ext("Einlaufstutzen", 0), ext("Einlaufstutzen", 1)
    ck.eq("Stutzen Mitte Deckel x", (sx[0] + sx[1]) / 2, 0, 0.1)
    ck.eq("Stutzen Mitte Deckel y", (sy[0] + sy[1]) / 2, 0, 0.1)
    ck.eq("Stutzen Aussen-Oe = od_f(40) 48", sx[1] - sx[0], 48, 0.2)
    dv = B["Deckel"]["volume_mm3"]
    voll = math.pi / 4 * D ** 2 * p["deckel_t"]
    loecher = math.pi / 4 * (48 ** 2 + p["luft_d"] ** 2 + (p["entl_d"] + 6) ** 2) * p["deckel_t"]
    ck.eq("Deckel: drei Durchbrueche (Stutzen 48, Luft 8, Entlueftung 26) aus Volumen", dv, voll - loecher, 1e-3 * dv)
    fv = B["Fass"]["volume_mm3"]
    mantel_boden = math.pi / 4 * (D ** 2 - di ** 2) * (ext("Fass", 2)[1] - p["fass_floor"]) + math.pi / 4 * D ** 2 * p["fass_floor"]
    ck.eq("Kein Auslass: Fasskoerper ohne Durchbruch (Volumen = Mantel + Boden)", fv, mantel_boden, 1e-3 * fv)
    P = {r[0].split(" ")[0]: r for r in d["blatt"]["ports"]}
    e = P["Einlauf"]; c = xyz(e[2])
    ck.eq("Port Einlauf d40", 1 if "d40" in e[1] else 0, 1)
    ck.eq("Port Einlauf z = Oberkante Stutzen", c["z"], ext("Einlaufstutzen", 2)[1], 0.6)
    ck.eq("Port Einlauf Richtung +Z", 1 if e[3] == "+Z" else 0, 1)
    ck.eq("Port Einlauf nennt K07 und K23", 1 if "K07" in e[0] and "K23" in e[0] else 0, 1)
    c = xyz(P["Entlueftung"][2])
    ck.eq("Port Entlueftung z = Oberkante Stutzen", c["z"], ext("Entlueftungsstutzen", 2)[1], 0.6)
    ck.eq("Gruben-Parameter grube_d = 800", p["grube_d"], 800)
    ck.eq("Gruben-Parameter grube_t = 950", p["grube_t"], 950)
    ck.eq(f"Fassoberkante flur-relativ {round(H - p['grube_t'] + 70):d} im Band 0 bis +20 (Sandbett 70)", 1 if -0.01 <= H - p["grube_t"] + 70 <= 20 else 0, 1)
    it = interference(path)
    ck.eq("Interferenz (Paare)", len(it), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
