"""Pruefung Luftverteiler 6-fach (T86), Pool-Verteiler 4-fach (T87) und Scheibenbelueftung (T88), W37-3: Masse, Muffe A, Abgaenge (Zahl, Ø, Port-Stirnflaechen), DN je Abgang gegen das Netz (data/leitungsnetz.json),
Stroemung je Abgang und im Sammler (Innen-Ø aus dem Modell), Scheibe: vier Koerper, Stapelhoehe, Interferenz 0.
Aufruf: python -X utf8 scripts/workshop/check_luft_verteiler.py [luftverteiler_6 luftverteiler_4 luft_scheibenbelueftung]   (exit 1 bei FAIL)"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import luft_verteiler as V
from check_lt_w39 import interference

def netz_dn():
    n = json.load(open(os.path.join(sc.ROOT, "data", "leitungsnetz.json"), encoding="utf-8"))
    return {k["id"]: (k["dn"], k.get("soll_l_min")) for k in n["kanten"]}

def area(dmm): return math.pi / 4 * dmm ** 2

def check_verteiler(name):
    p, d = sc.load_params(name)
    ab = d["abgaenge"]; n = len(ab)
    g = V.v_geom(p, ab)
    path = os.path.join(sc.ROOT, "designs", "components", name + ".sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check(name)
    bb = B["Verteiler"]["bbox"]
    ck.eq("Koerperzahl (ein Koerper Verteiler)", len(B), 1)
    ck.eq(f"Sammler Aussen-Ø = Formstueck d40 ({g['of']:g})", bb["max"][1] - bb["min"][1], g["of"], 0.1)
    ck.eq(f"Laenge {g['L']:g} (letzter Abgang + 25 + Endkappe)", bb["max"][0] - bb["min"][0], g["L"], 0.1)
    ck.eq(f"Zapfenende {g['top']:g} ueber der Achse", bb["max"][2], g["top"], 0.1)
    fs = sc.faces(path, "Verteiler")
    cyl = [f["cylinder"]["radius"] for f in fs if f.get("cylinder")]
    has = lambda r: 1 if any(abs(c - r) < 0.011 for c in cyl) else 0
    ck.eq("Muffe A d40: Zylinderflaeche r 20", has(20.0), 1)
    bore_r = g["bore"] / 2
    ck.eq(f"Sammlerbohrung: Zylinderflaeche r {bore_r:g} (Innen-Ø {g['bore']:g})", has(bore_r), 1)
    hit = any(f.get("plane_normal") and f["plane_normal"][0] < -0.999 and math.dist(f["centroid"], (0, 0, 0)) < 0.6 for f in fs)
    ck.eq("Port A Muffe d40: Stirnflaeche im Ursprung, Oeffnung -X", 1 if hit else 0, 1)
    ends = [f for f in fs if f.get("plane_normal") and f["plane_normal"][2] > 0.999 and abs(f["centroid"][2] - g["top"]) < 0.2]
    ck.eq(f"Abgaenge: {n} Zapfen-Stirnflaechen bei Z {g['top']:g}", len(ends), n)
    nd = netz_dn()
    for k, (a, x) in enumerate(zip(ab, g["xs"]), 1):
        ds = a[1]
        ok = any(abs(e["centroid"][0] - x) < 0.6 and abs(e["centroid"][1]) < 0.6 for e in ends)
        ck.eq(f"Abgang {k} {a[0]} ({a[2]}): Stirnflaeche bei X {x:g}", 1 if ok else 0, 1)
        ck.eq(f"Abgang {k} Zapfen Ø {V.abgang_d(ds):g}: Zylinderflaeche", has(V.abgang_d(ds) / 2), 1)
        ck.eq(f"Abgang {k} Bohrung Ø {V.abgang_bohrung(ds):g}: Zylinderflaeche", has(V.abgang_bohrung(ds) / 2), 1)
        if name == "luftverteiler_6":
            kid = a[2].split("/")[0]
            ck.eq(f"Abgang {k} {a[2]}: DN d{ds} = Netz ({nd[kid][0]})", ds, nd[kid][0])
    if name == "luftverteiler_4":
        ck.eq("Pool-Verteiler: Zulauf d40 = Netz K44", 40, nd["K44"][0])
        qs = [float(a[3]) for a in ab]
        ck.eq(f"Summe Abgangsstroeme {sum(qs):g} l/min gegen Planwert 130 (Abweichung unter 2 Prozent)", abs(sum(qs) - 130) / 130 * 100, 0, 2.0)
        for k, (a, q) in enumerate(zip(ab, qs), 1):
            v = q * 1e6 / 60 / area(V.abgang_bohrung(a[1])) / 1000
            ck.eq(f"Abgang {k}: {q:g} l/min im Innen-Ø {V.abgang_bohrung(a[1]):g} = {v:.2f} m/s (unter 2 m/s)", 1 if v < 2.0 else 0, 1)
    v130 = 130e6 / 60 / area(g["bore"]) / 1000
    ck.eq(f"Sammler Innen-Ø {g['bore']:g}: 130 l/min = {v130:.2f} m/s", v130, 2.1, 0.05)
    v205 = 205e6 / 60 / area(g["bore"]) / 1000
    print(f"INFO Spitze 205 l/min im Sammler: {v205:.2f} m/s (R45: d40 bei 200 l/min 3,2 m/s)")
    if name == "luftverteiler_6":
        ein = 130 + 2 + 5
        print(f"INFO Einlauf Hauptverteiler: Pool 130 + Drittbecken 2 + Zweitbecken 5 = {ein} l/min plus Biofilter 1/2 und Absetzer (offen); {ein * 1e6 / 60 / area(g['bore']) / 1000:.2f} m/s im Sammler")
    bad, res = interference(path)
    ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(bad), 0)
    print(f"INFO Masse {ev['total']['mass_g']:.0f} g")
    return ck.done()

def check_scheibe():
    name = "luft_scheibenbelueftung"
    p, d = sc.load_params(name)
    g = V.s_geom(p)
    path = os.path.join(sc.ROOT, "designs", "components", name + ".sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    ck = sc.Check(name)
    ck.eq("Koerperzahl (Stutzen, Stuetzfuss, Tragteller, Membran)", len(B), 4)
    w = lambda n: B[n]["bbox"]["max"][0] - B[n]["bbox"]["min"][0]
    h = lambda n: B[n]["bbox"]["max"][2] - B[n]["bbox"]["min"][2]
    ck.eq("Stutzen Ø = Anschluss d25", w("Stutzen"), p["pipe_d"], 0.1)
    ck.eq(f"Stutzen Laenge {p['stutzen_l']}", h("Stutzen"), p["stutzen_l"], 0.1)
    ck.eq(f"Stuetzfuss Ø {g['fuss_d']:g}", w("Stuetzfuss"), g["fuss_d"], 0.1)
    ck.eq(f"Stuetzfuss Hoehe {p['fuss_h']}", h("Stuetzfuss"), p["fuss_h"], 0.1)
    ck.eq(f"Tragteller Ø {g['teller_d']:g}", w("Tragteller"), g["teller_d"], 0.1)
    ck.eq(f"Membran Ø {p['d']} (Parameter d)", w("Membran"), p["d"], 0.1)
    ck.eq("Membran Dicke 6", h("Membran"), p["membran_h"], 0.1)
    ck.eq(f"Gesamthoehe {g['z3']:g} (Stutzen + Fuss + Teller + Membran)", B["Membran"]["bbox"]["max"][2], g["z3"], 0.1)
    fs = sc.faces(path, "Stutzen")
    hit = any(f.get("plane_normal") and f["plane_normal"][2] < -0.999 and math.dist(f["centroid"], (0, 0, 0)) < 0.6 for f in fs)
    ck.eq("Port A d25: Stirnflaeche im Ursprung, Oeffnung -Z (nach unten)", 1 if hit else 0, 1)
    ck.eq("Luftkanal Ø 16: Zylinderflaeche r 8 im Stutzen", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - g["bohr"] / 2) < 0.01 for f in fs) else 0, 1)
    vm = math.pi / 4 * p["d"] ** 2 * p["membran_h"]
    ck.eq("Membran-Volumen = Kreisscheibe (mm3)", B["Membran"]["volume_mm3"], vm, vm * 0.002)
    vs = math.pi / 4 * (p["pipe_d"] ** 2 - g["bohr"] ** 2) * p["stutzen_l"]
    ck.eq("Stutzen-Volumen = Ringflaeche x Laenge (mm3)", B["Stutzen"]["volume_mm3"], vs, vs * 0.002)
    mn, mx = sc.bbox_all(ev)
    ck.eq(f"Membran-Ø {2 * mx[0]:.0f} (Bauteil rund um die Achse)", 1 if abs(mx[0] + mn[0]) < 0.1 and abs(mx[1] + mn[1]) < 0.1 else 0, 1)
    bad, res = interference(path)
    ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(bad), 0)
    for i in bad[:5]:
        print("   ", i)
    print(f"INFO Masse {ev['total']['mass_g']:.0f} g")
    return ck.done()

def main():
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or ["luftverteiler_6", "luftverteiler_4", "luft_scheibenbelueftung"]
    rc = 0
    for n in want:
        rc |= check_scheibe() if n == "luft_scheibenbelueftung" else check_verteiler(n)
    return rc

if __name__ == "__main__":
    sys.exit(main())
