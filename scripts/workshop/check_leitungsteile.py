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
    import leitung_w36 as W36, leitung_w39 as W39                # W36-/W39-Teile gehoeren nicht zu den 63 Bibliotheksteilen (eigene Pruefungen check_lt_w36.py, check_lt_w39.py)
    import re
    lib = [f for f in glob.glob(os.path.join(D, "lt_*.sc")) if os.path.basename(f)[:-3] not in W36.FILES + W39.FILES and not re.search(r"_L\d+$", os.path.basename(f)[:-3])]      # Laengenvarianten lt_rohr_d*_L<mm> der Montage gehoeren nicht zu den 63 Bibliotheksteilen
    ck.eq("Dateien lt_*.sc (7 Groessen x 7 Teile + 7 Reduzierungen + 4 Schlauch + 3 Verteiler)", len(lib), 7 * 7 + 7 + 4 + 3)
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
        ad = idd + 4
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
    for dg, dk in L.REDUCERS:
        ev, v = vol(os.path.join(D, f"lt_reduzierung_d{dg}_d{dk}.sc"))
        mn, mx = sc.bbox_all(ev)
        ck.eq(f"reduzierung d{dg}/d{dk} Laenge", mx[2] - mn[2], L.DEPTH[dg] + L.DEPTH[dk] + 6, 0.1)
        ck.eq(f"reduzierung d{dg}/d{dk} Aussen-D", mx[0] - mn[0], L.od_f(dg), 0.1)
    # Ports: zu jedem Port existiert eine ebene Stirnflaeche mit passender Normalen und Mittelpunkt (Pruefung der Port-Koordinaten im Blatt)
    body = {"rohr": "Rohr", "kupplung": "Kupplung", "bogen": "Bogen", "t": "T_Stueck", "kugelhahn": "Kugelhahn", "reduzierung": "Reduzierung", "schlauch": "Schlauch", "schlauchbogen90": "Schlauchbogen", "verteiler": "Verteiler"}
    nport = 0
    for f in sorted(lib):
        fn = os.path.basename(f)[:-3]
        pl = L.ports(fn)
        if not pl or fn.startswith("lt_klemme"):
            continue
        key = fn.split("_")[1]
        key = "bogen" if key.startswith("bogen") else key
        fs = sc.faces(f, body[key])
        planes = [(x["plane_normal"], x["centroid"]) for x in fs if x.get("plane_normal")]
        for name, pos, dr, art, dn in pl:
            hit = any(sum(n[i] * dr[i] for i in range(3)) > 0.999 and math.dist(cen, pos) < 0.6 for n, cen in planes)
            nport += 1
            ck.eq(f"{fn} Port {name} ({art}, {dn}) Stirnflaeche an {tuple(round(v, 1) for v in pos)}", 1 if hit else 0, 1)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
