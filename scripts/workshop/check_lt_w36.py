"""Pruefung der W36-Leitungsteile (Verteiler d50, ...): Masse, Ports (stirnflaechen), Interferenz 0, Kollisionsfreiheit der Abgaenge, Volumen unabhaengig per Raster.
Aufruf: python scripts/workshop/check_lt_w36.py [verteiler ...]   (ohne Teil: alle; exit 1 bei FAIL)"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w36 as W

D = os.path.join(sc.ROOT, "designs", "components")

def port_checks(ck, fname, body, tag=None):
    """Zu jedem Port der Tabelle existiert eine ebene Stirnflaeche mit passender Normalen und Mittelpunkt."""
    fs = sc.faces(os.path.join(D, fname + ".sc"), body)
    planes = [(x["plane_normal"], x["centroid"]) for x in fs if x.get("plane_normal")]
    for name, pos, dr, art, dn in L.ports(fname):
        hit = any(sum(n[i] * dr[i] for i in range(3)) > 0.999 and math.dist(cen, pos) < 0.6 for n, cen in planes)
        ck.eq(f"{fname} Port {name} ({art}, {dn}) Stirnflaeche an {tuple(round(v, 2) for v in pos)}", 1 if hit else 0, 1)

def raster_volume(inside, lo, hi, h=1.0):
    n = 0
    x = lo[0] + h / 2
    while x < hi[0]:
        y = lo[1] + h / 2
        while y < hi[1]:
            z = lo[2] + h / 2
            while z < hi[2]:
                if inside(x, y, z):
                    n += 1
                z += h
            y += h
        x += h
    return n * h ** 3

def check_verteiler(ck):
    g = W.v50_geom()
    fname = "lt_verteiler_d50"
    path = os.path.join(D, fname + ".sc")
    ev = sc.evaluate(path)
    ck.eq("verteiler d50 Koerperzahl (Interferenz 0: ein einziger Koerper, kein Teil durchdringt ein anderes)", ev["body_count"], 1)
    bb = ev["bodies"][0]["bbox"]
    ck.eq("verteiler d50 Laenge", bb["max"][0] - bb["min"][0], g["L"], 0.1)
    ck.eq("verteiler d50 Aussen-D Koerper (Formstueck d50)", bb["max"][1] - bb["min"][1], g["of"], 0.1)
    ck.eq("verteiler d50 Hoehe Zapfen ueber Achse", bb["max"][2], g["top"], 0.1)
    fs = sc.faces(path, "Verteiler")
    cyl = [f["cylinder"] for f in fs if f.get("cylinder")]
    for k, ((fn, ds, kante, q), x) in enumerate(zip(W.V50_ABGAENGE, g["xs"]), 1):
        hit = [c for c in cyl if abs(abs(c["axis"][2]) - 1) < 0.01 and abs(c["origin"][0] - x) < 0.1 and abs(c["radius"] - ds / 2) < 0.05]
        ck.eq(f"verteiler d50 Abgang {k} {fn}: Zapfen d{ds} bei x = {x}", 1 if hit else 0, 1)
        inn = [c for c in cyl if abs(abs(c["axis"][2]) - 1) < 0.01 and abs(c["origin"][0] - x) < 0.1 and abs(c["radius"] - (ds - 2 * L.wall_p(ds)) / 2) < 0.05]
        ck.eq(f"verteiler d50 Abgang {k} {fn}: Bohrung d{ds - 2 * L.wall_p(ds):.1f} (Wand {L.wall_p(ds)})", 1 if inn else 0, 1)
    port_checks(ck, fname, "Verteiler")
    # Geschwindigkeit im Sammler (Druckseite <= 1,5 m/s) fuer beide Linien (Linie 1 mit Messkreis, Linie 2 ohne, dann 17,5 l/min Bypass)
    A = math.pi / 4 * (g["bore"] / 1000) ** 2
    for lin, q in (("Linie 1", sum(a[3] for a in W.V50_ABGAENGE)), ("Linie 2", 54.5 + 38.0 + 17.5)):
        v = q / 60000 / A
        ck.eq(f"verteiler d50 {lin} Zulauf {q:g} l/min im Sammler d{g['bore']:.1f}: v {v:.2f} m/s <= 1,5", 1 if v <= 1.5 else 0, 1)
    # Abgaenge ohne Kollision: Muffen (OD_f) und Kugelhahn-Gehaeuse (OD_f + 12) plus Hebel (+X, bis ob/2 + 41) gegen den Nachbarn, Mindestluft 10 mm
    ds_l = [a[1] for a in W.V50_ABGAENGE]
    for k in range(len(ds_l) - 1):
        dx = g["xs"][k + 1] - g["xs"][k]
        r1, r2 = L.od_f(ds_l[k]) / 2, L.od_f(ds_l[k + 1]) / 2
        h1, h2 = L.od_f(ds_l[k]) / 2 + 6, L.od_f(ds_l[k + 1]) / 2 + 6
        ck.eq(f"verteiler d50 Abgang {k + 1}->{k + 2} Luft Muffe d{ds_l[k]}/d{ds_l[k + 1]} >= 10 (Ist {dx - r1 - r2:.1f})", 1 if dx - r1 - r2 >= 10 else 0, 1)
        ck.eq(f"verteiler d50 Abgang {k + 1}->{k + 2} Luft Kugelhahn-Gehaeuse >= 10 (Ist {dx - h1 - h2:.1f})", 1 if dx - h1 - h2 >= 10 else 0, 1)
        lever = h1 + 41
        ck.eq(f"verteiler d50 Abgang {k + 1}->{k + 2} Luft Hebel (+X) zum Nachbargehaeuse >= 10 (Ist {dx - h2 - lever:.1f})", 1 if dx - h2 - lever >= 10 else 0, 1)
    # Volumen unabhaengig: CSG-Raster 1 mm (Koerper minus Bohrungen), Toleranz 1 %
    R, rb, t = g["of"] / 2, g["bore"] / 2, g["t"]
    ab = [(x, ds / 2, (ds - 2 * L.wall_p(ds)) / 2) for (fn, ds, kante, q), x in zip(W.V50_ABGAENGE, g["xs"])]
    def inside(x, y, z):
        r2 = y * y + z * z
        solid = (x <= g["L"] and r2 <= R * R) or any((x - ax) ** 2 + y * y <= ar * ar and 0 <= z <= g["top"] for ax, ar, ai in ab)
        if not solid:
            return False
        if x < t and r2 < (W.V50_D / 2) ** 2:
            return False
        if t <= x <= g["L"] - W.V50_END and r2 < rb * rb:
            return False
        if any((x - ax) ** 2 + y * y < ai * ai and 0 <= z <= g["top"] + 2 for ax, ar, ai in ab):
            return False
        return True
    v = raster_volume(inside, (0, -R - 1, -R - 1), (g["L"] + 1, R + 1, g["top"] + 1))
    vs = ev["bodies"][0]["volume_mm3"]
    ck.eq("verteiler d50 Volumen = CSG-Raster (1 mm)", vs, v, v * 0.01)
    print(f"INFO verteiler d50: Volumen {vs:.0f} mm3, Masse {vs * 1.4e-6:.3f} kg (PVC-U 1,4), Wasser {math.pi * rb * rb * (g['L'] - W.V50_END - t) / 1e6:.3f} l (nur Sammler)")

def main():
    want = set(a for a in sys.argv[1:] if not a.startswith("--"))
    ck = sc.Check("lt_w36")
    if not want or "verteiler" in want:
        check_verteiler(ck)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
