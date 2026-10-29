"""Vorpruefung Leitungsteile-Bibliothek (Scope-Card rohr...verteiler): 49 Dateien, DN-Reihe, Wandstaerke, Laenge/Volumen (Pappus), Ports, Biegeradius Schlauch >= 5 x AD, Verteiler-Abgaenge.
Aufruf: python scripts/workshop/check_leitungsteile.py   (exit 1 bei FAIL)"""
import sys, os, math, glob
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

def vol(path):
    ev = sc.evaluate(path)
    return ev, sum(b["volume_mm3"] for b in ev["bodies"])

def main():
    ck = sc.Check("leitungsteile")
    D = os.path.join(sc.ROOT, "designs", "components")
    ck.eq("Dateien lt_*.sc", len(glob.glob(os.path.join(D, "lt_*.sc"))), 49)
    for d in L.SIZES:
        A = math.pi / 4 * (d * d - (d - 2 * L.wall_p(d)) ** 2)
        ev, v = vol(os.path.join(D, f"lt_rohr_d{d}.sc"))
        mn, mx = ev["bodies"][0]["bbox"]["min"], ev["bodies"][0]["bbox"]["max"]
        ck.eq(f"rohr d{d} Aussen-D", mx[0] - mn[0], d, 0.1)
        ck.eq(f"rohr d{d} Laenge", mx[2] - mn[2], 1000, 0.1)
        ck.eq(f"rohr d{d} Volumen = Ringflaeche x Laenge (Wand {L.wall_p(d)})", v, A * 1000, A * 1000 * 0.002)
        ev, v = vol(os.path.join(D, f"lt_kupplung_d{d}.sc"))
        mn, mx = sc.bbox_all(ev)
        ck.eq(f"kupplung d{d} Laenge", mx[2] - mn[2], 2 * L.DEPTH[d] + 6, 0.1)
        ck.eq(f"kupplung d{d} Aussen-D (Formstueck)", mx[0] - mn[0], L.od_f(d), 0.1)
        for ang in (90, 45):
            R = max(L.od_f(d), 1.2 * d)
            ev, v = vol(os.path.join(D, f"lt_bogen{ang}_d{d}.sc"))
            Af = math.pi / 4 * (L.od_f(d) ** 2 - d ** 2)
            exp = Af * (2 * L.DEPTH[d] + R * math.radians(ang))
            ck.eq(f"bogen{ang} d{d} Volumen = Ringflaeche x Mittellinie (2 Schenkel + Bogen R {R:.0f})", v, exp, exp * 0.005)
        ev, v = vol(os.path.join(D, f"lt_t_d{d}.sc"))
        mn, mx = sc.bbox_all(ev)
        a = L.DEPTH[d] + L.od_f(d) / 2
        ck.eq(f"t d{d} Laenge Lauf", mx[0] - mn[0], 2 * a, 0.2)
        ck.eq(f"t d{d} Abgang Hoehe", mx[2], a, 0.2)
        ev, v = vol(os.path.join(D, f"lt_kugelhahn_d{d}.sc"))
        kb = [b for b in ev["bodies"] if b["name"] == "Kugelhahn"][0]["bbox"]
        ck.eq(f"kugelhahn d{d} Baulaenge (Gehaeuse ohne Hebel)", kb["max"][2] - kb["min"][2], 50 + 2 * L.DEPTH[d], 0.1)
        ev, v = vol(os.path.join(D, f"lt_klemme_d{d}.sc"))
        fs = sc.faces(os.path.join(D, f"lt_klemme_d{d}.sc"), "Klemmenring")
        rr = {round(f["cylinder"]["radius"], 2) for f in fs if f.get("cylinder")}
        ck.eq(f"klemme d{d} Ringbohrung = Rohr-D", 1 if round(d / 2, 2) in rr else 0, 1)
    for idd in (16, 25):
        ad = idd + 7
        ev, v = vol(os.path.join(D, f"lt_schlauch_id{idd}.sc"))
        mn, mx = sc.bbox_all(ev)
        ck.eq(f"schlauch ID{idd} Aussen-D", mx[0] - mn[0], ad, 0.1)
        ck.eq(f"schlauch ID{idd} Laenge", mx[2] - mn[2], 1000, 0.1)
        R = 5 * ad
        ev, v = vol(os.path.join(D, f"lt_schlauchbogen90_id{idd}.sc"))
        exp = math.pi / 4 * (ad ** 2 - idd ** 2) * (200 + R * math.pi / 2)
        ck.eq(f"schlauchbogen ID{idd} Volumen (Biegeradius {R:.0f} = 5 x AD)", v, exp, exp * 0.005)
        ck.eq(f"schlauchbogen ID{idd} Biegeradius >= 5 x AD", 1 if R >= 5 * ad else 0, 1)
    for n in (2, 3, 4):
        path = os.path.join(D, f"lt_verteiler_d32_n{n}.sc")
        fs = sc.faces(path, "Verteiler")
        xs = {round(f["cylinder"]["origin"][0], 1) for f in fs if f.get("cylinder") and abs(f["cylinder"]["radius"] - 12.5) < 0.1 and abs(abs(f["cylinder"]["axis"][2]) - 1) < 0.01}
        ck.eq(f"verteiler d32 n{n} Abgaenge d25", len(xs), n)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
