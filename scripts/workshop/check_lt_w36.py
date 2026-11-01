"""Pruefung der W36-Leitungsteile (Verteiler d50, ...): Masse, Ports (stirnflaechen), Interferenz 0, Kollisionsfreiheit der Abgaenge, Volumen unabhaengig per Raster.
Aufruf: python scripts/workshop/check_lt_w36.py [verteiler ...]   (ohne Teil: alle; exit 1 bei FAIL)"""
import sys, os, math, json, subprocess
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

def interference(path, extra=()):
    """inspect.interference ueber alle Koerper (plus optionale Zusatzbefehle, z. B. Gegenstuecke); Rueckgabe: Liste der ueberlappenden Paare mit Volumen > 0,5 mm3."""
    script = os.path.join(sc.TMP, "ws-w36-interf.json"); out = os.path.join(sc.TMP, "ws-w36-interf-out.json")
    json.dump({"commands": list(extra) + [{"command": "inspect.interference", "params": {"budget_s": 240}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--results", "--json-out", out], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER interference: " + r.stderr.strip() + r.stdout.strip())
    d = json.load(open(out, encoding="utf-8"))
    def find(o):
        if isinstance(o, dict):
            if "interferences" in o:
                return o
            for v in o.values():
                x = find(v)
                if x is not None:
                    return x
        elif isinstance(o, list):
            for v in o:
                x = find(v)
                if x is not None:
                    return x
    res = find(d) or {}
    return [i for i in res.get("interferences", []) if i.get("volume_mm3", 0) > 0.5], res

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

def check_schelle(ck):
    for d in W.SCH_SIZES:
        g = W.sch_geom(d)
        fname = f"lt_schelle_vk_d{d}"
        path = os.path.join(D, fname + ".sc")
        ev = sc.evaluate(path)
        names = [b["name"] for b in ev["bodies"]]
        ck.eq(f"schelle d{d} Koerperzahl (3 Blechteile + 8 Normteile M6)", ev["body_count"], 11)
        bb = {b["name"]: b["bbox"] for b in ev["bodies"]}
        hv, hh, sb = bb["Halbschale_vorn"], bb["Halbschale_hinten"], bb["Spannband"]
        ck.eq(f"schelle d{d} Halbschale vorn: Aussenradius (Ring {W.SCH_T:g} mm)", hv["max"][1], g["ro"], 0.05)
        ck.eq(f"schelle d{d} Halbschale vorn: Ohr reicht bis z = ro + 14", hv["max"][2], g["ro"] + 14, 0.05)
        ck.eq(f"schelle d{d} Ringbreite", hv["max"][0] - hv["min"][0], W.SCH_W, 0.05)
        ck.eq(f"schelle d{d} Rueckenplatte Breite", hh["max"][0] - hh["min"][0], 2 * W.SCH_PLATE_HALF, 0.05)
        ck.eq(f"schelle d{d} Platte-Rueckseite y_min = Steg + Platte (Anlageflaeche)", hh["min"][1], g["yf"], 0.05)
        ck.eq(f"schelle d{d} Anlageflaeche am Bein bei y = {g['yf']:g}", hh["min"][1], g["yf"], 0.05)
        ck.eq(f"schelle d{d} Spannband Ruecken liegt {W.SCH_SPIEL:g} mm hinter dem Bein (y = {g['yb'] - W.SCH_SPIEL - W.SCH_BAND_T:g})", sb["min"][1], g["yb"] - W.SCH_SPIEL - W.SCH_BAND_T, 0.05)
        ck.eq(f"schelle d{d} Spannband Breite ueber die Laschen", sb["max"][0] - sb["min"][0], 2 * (W.LEG / 2 + W.SCH_SPIEL + W.SCH_BAND_T - 1 + W.SCH_TAB), 0.05)
        for half in ("vorn", "hinten"):
            fs = sc.faces(path, f"Halbschale_{half}")
            rr = {round(f["cylinder"]["radius"], 2) for f in fs if f.get("cylinder") and abs(f["cylinder"]["axis"][0]) > 0.99}
            ck.eq(f"schelle d{d} Halbschale {half}: Rohrbohrung = d{d}", 1 if round(d / 2, 2) in rr else 0, 1)
        # Port Bein: Anlageflaeche der Rueckenplatte mit Normale -Y und Mittelpunkt auf der Beinachse
        fs = sc.faces(path, "Halbschale_hinten")
        hit = any(f.get("plane_normal") and f["plane_normal"][1] < -0.999 and math.dist(f["centroid"], (0, g["yf"], 0)) < 0.6 for f in fs)
        ck.eq(f"{fname} Port Bein (Vierkant 40x40): Anlageflaeche bei y = {g['yf']:g}, Beinachse y = {g['leg_y']:g}", 1 if hit else 0, 1)
        cax = [f["cylinder"] for f in sc.faces(path, "Halbschale_vorn") if f.get("cylinder") and abs(f["cylinder"]["radius"] - d / 2) < 0.01]
        ck.eq(f"{fname} Port Rohrachse (Aufnahme DN{d}): Bohrungsachse X durch den Ursprung (y = z = 0)", 1 if cax and all(abs(c["origin"][1]) < 0.01 and abs(c["origin"][2]) < 0.01 and abs(abs(c["axis"][0]) - 1) < 1e-6 for c in cax) else 0, 1)
        ck.eq(f"schelle d{d} Abstand Plattenvorderseite zur Rohroberflaeche >= 12 (Mutter + Schraubenende)", 1 if (-d / 2 - g["ypf"]) >= 12 else 0, 1)
        # Interferenz 0 mit Gegenstuecken: Bein 40x40 (Achse Z bei y = leg_y) und Rohr d (Achse X bei y = 0)
        extra = [{"command": "solid.box", "params": {"length": W.LEG, "width": W.LEG, "height": 400, "center": [0, g["leg_y"], 0], "operation": "new", "name": "T_Bein", "body_name": "Test_Bein"}},
                 {"command": "solid.cylinder", "params": {"diameter": d, "height": 400, "base": [-200, 0, 0], "axis": [1, 0, 0], "operation": "new", "name": "T_Rohr", "body_name": "Test_Rohr"}}]
        bad, res = interference(path, extra)
        ck.eq(f"schelle d{d} Interferenz 0 (alle Koerperpaare inkl. Bein und Rohr; geprueft {res.get('checked', '?')} Koerper, Paare mit Ueberlappung)", len(bad), 0)
        for i in bad:
            print("   Ueberlappung:", i.get("a"), i.get("b"), i.get("volume_mm3"))
        # Gewicht (Stahl 7,85) aus der Messung
        print(f"INFO schelle d{d}: Masse {ev['total']['mass_g']:.0f} g (Stahl verzinkt 7,85), Volumen {ev['total']['volume_mm3']:.0f} mm3")

def check_leerrohr(ck):
    for dn, q in W.LR.items():
        d, w, tm, om, R = q["d"], q["wall"], q["t"], q["od_m"], q["R"]
        di = d - 2 * w
        At, Am = math.pi / 4 * (d * d - di * di), math.pi / 4 * (om * om - d * d)
        fname = f"lt_leerrohr_dn{dn}"
        path = os.path.join(D, fname + ".sc")
        ev = sc.evaluate(path)
        v = ev["bodies"][0]["volume_mm3"]
        bb = ev["bodies"][0]["bbox"]
        ck.eq(f"leerrohr DN{dn} Koerperzahl (Interferenz 0: ein Koerper)", ev["body_count"], 1)
        ck.eq(f"leerrohr DN{dn} Laenge {W.LR_L:g} (Standardstange, Muffe eingerechnet)", bb["max"][2] - bb["min"][2], W.LR_L, 0.1)
        ck.eq(f"leerrohr DN{dn} Aussen-D Muffe {om:g}", bb["max"][0] - bb["min"][0], om, 0.1)
        exp = At * (W.LR_L - tm) + Am * tm
        ck.eq(f"leerrohr DN{dn} Volumen = Rohr AD{d:g} x {w} + Muffe", v, exp, exp * 0.002)
        ck.eq(f"leerrohr DN{dn} Innen-D frei {di:g} (Kabeldurchgang)", 1 if any(abs(f["cylinder"]["radius"] - di / 2) < 0.01 for f in sc.faces(path, "Leerrohr") if f.get("cylinder")) else 0, 1)
        port_checks(ck, fname, "Leerrohr")
        ck.eq(f"leerrohr DN{dn} Masse {v * 1.4e-6:.2f} kg (PVC-U 1,4)", 1 if v > 0 else 0, 1)
        for ang in (90, 45):
            fname = f"lt_leerrohr_bogen{ang}_dn{dn}"
            path = os.path.join(D, fname + ".sc")
            ev = sc.evaluate(path)
            v = ev["bodies"][0]["volume_mm3"]
            leg = tm + 20.0
            exp = At * (2 * leg + R * math.radians(ang) - tm) + Am * tm
            ck.eq(f"leerrohr-bogen{ang} DN{dn} Koerperzahl", ev["body_count"], 1)
            ck.eq(f"leerrohr-bogen{ang} DN{dn} Volumen (Pappus: 2 Schenkel + Bogen R {R:g}, Muffe)", v, exp, exp * 0.005)
            ck.eq(f"leerrohr-bogen{ang} DN{dn} Radius {R:g} >= Kabel-Mindestradius 15 x 20 mm (DN50) bzw. 15 x 33 mm (DN100)", 1 if R >= (300 if dn == 50 else 495) else 0, 1)
            port_checks(ck, fname, "Leerrohrbogen")

def hahn63_test_bodies(closed):
    """Gegenstuecke im Schacht: Rohr d63 (zwei Stuecke), Kugelhahn d63 (Gehaeuse, Muffen, Spindel, Hebel offen = parallel zur Rohrachse bzw. zu = quer); Hahn-KS gedreht: Hahnachse Z -> Welt X, Spindel (+X) -> Welt +Z."""
    h = W.HAHN63; of = L.od_f(63); Lh = h["L"]
    def cyl(nm, d, ln, base, axis):
        return {"command": "solid.cylinder", "params": {"diameter": d, "height": ln, "base": base, "axis": axis, "operation": "new", "name": nm, "body_name": nm}}
    def box(nm, lx, wy, hz, c):
        return {"command": "solid.box", "params": {"length": lx, "width": wy, "height": hz, "center": c, "operation": "new", "name": nm, "body_name": nm}}
    cm = [cyl("Test_Rohr_A", 63, 600, [-Lh / 2 - 600, 0, 0], [1, 0, 0]), cyl("Test_Rohr_B", 63, 600, [Lh / 2, 0, 0], [1, 0, 0]),
          cyl("Test_Hahn_Gehaeuse", h["ob"], 50, [-25, 0, 0], [1, 0, 0]), cyl("Test_Hahn_Muffe_A", of, L.DEPTH[63], [-Lh / 2, 0, 0], [1, 0, 0]), cyl("Test_Hahn_Muffe_B", of, L.DEPTH[63], [Lh / 2 - L.DEPTH[63], 0, 0], [1, 0, 0]),
          cyl("Test_Hahn_Spindel", 14, h["spindel_h"], [0, 0, 0], [0, 0, 1])]
    cm.append(box("Test_Hahn_Hebel", h["hebel_b"], h["hebel_l"], h["hebel_h"], [0, 0, h["hebel_x"]]) if closed else box("Test_Hahn_Hebel", h["hebel_l"], h["hebel_b"], h["hebel_h"], [0, 0, h["hebel_x"]]))
    return cm

def check_schacht(ck):
    s, g = W.SCHACHT, W.schacht_geom()
    fname = "lt_schacht_kugelhahn_d63"
    path = os.path.join(D, fname + ".sc")
    ev = sc.evaluate(path)
    bb = {b["name"]: b for b in ev["bodies"]}
    ck.eq("schacht Koerperzahl (Wanne, Deckel, 2 Dichtungen)", ev["body_count"], 4)
    w = bb["Schachtwanne"]
    ck.eq("schacht Aussenmass quer", w["bbox"]["max"][0] - w["bbox"]["min"][0], g["aussen"], 0.1)
    ck.eq("schacht Aussenhoehe (Boden bis Deckelauflage)", w["bbox"]["max"][2] - w["bbox"]["min"][2], g["z_wall_top"] - g["z_out_bottom"], 0.1)
    exp = g["aussen"] ** 2 * (g["z_wall_top"] - g["z_out_bottom"]) - s["innen"] ** 2 * (g["z_wall_top"] - g["z_floor"]) - 2 * math.pi / 4 * s["loch_d"] ** 2 * s["wand"]
    ck.eq("schacht Wannenvolumen = Aussen - Innenraum - 2 Wanddurchfuehrungen", w["volume_mm3"], exp, exp * 0.002)
    d = bb["Deckel"]
    exp = g["deckel"] ** 2 * s["deckel_dicke"] - 2 * 100 * 30 * 15
    ck.eq("schacht Deckelvolumen (420 x 420 x 30 minus 2 Griffmulden 100 x 30 x 15)", d["volume_mm3"], exp, exp * 0.002)
    ck.eq("schacht Deckel Oberkante = Erdoberflaeche (z = Achstiefe)", d["bbox"]["max"][2], g["z_top"], 0.1)
    ck.eq("schacht Deckel liegt auf der Wand (Unterkante = Wandoberkante)", d["bbox"]["min"][2], g["z_wall_top"], 0.1)
    fs = sc.faces(path, "Schachtwanne")
    ck.eq("schacht Wanddurchfuehrung d70 (Loch in Wand A und B)", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - 35) < 0.01 and abs(abs(f["cylinder"]["axis"][0]) - 1) < 1e-6 for f in fs) else 0, 1)
    for nmx in ("A", "B"):
        fsd = sc.faces(path, f"Dichtung_{nmx}")
        ck.eq(f"schacht Dichtung {nmx} Bohrung = Rohr d63", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - 31.5) < 0.01 for f in fsd) else 0, 1)
    fsd = sc.faces(path, "Deckel")
    ck.eq("schacht Port Deckel: Oberflaeche mit Normale +Z bei z = Achstiefe, Mittelpunkt auf der Schachtachse", 1 if any(f.get("plane_normal") and f["plane_normal"][2] > 0.999 and math.dist(f["centroid"], (0, 0, g["z_top"])) < 0.6 for f in fsd) else 0, 1)
    ck.eq("schacht Port Durchfuehrung A/B: Dichtung-Stirnflaeche an der Aussenwand x = +-208 bis +-211 (Dichtung ragt 3 mm)", 1 if abs(bb["Dichtung_B"]["bbox"]["max"][0] - (g["wall_x"] + 3)) < 0.1 and abs(bb["Dichtung_A"]["bbox"]["min"][0] + (g["wall_x"] + 3)) < 0.1 else 0, 1)
    h = W.HAHN63
    ck.eq(f"schacht Hebel oben frei: Hebel-Oberkante {h['hebel_x'] + h['hebel_h'] / 2:.1f} unter Deckelunterkante {g['z_wall_top']:g}, Luft >= 30", 1 if g["z_wall_top"] - (h["hebel_x"] + h["hebel_h"] / 2) >= 30 else 0, 1)
    ck.eq(f"schacht Hahn von oben bedienbar: Oeffnung {s['innen']:g} >= Hebel {h['hebel_l']:g} + Handbreite 2 x 100", 1 if s["innen"] >= h["hebel_l"] + 200 else 0, 1)
    ck.eq(f"schacht Platz unter dem Hahn: Gehaeuseunterkante {-h['ob'] / 2:.1f} bis Boden {g['z_floor']:g} >= 90", 1 if (-h["ob"] / 2 - g["z_floor"]) >= 90 else 0, 1)
    own = {"Schachtwanne", "Deckel", "Dichtung_A", "Dichtung_B"}
    for closed in (False, True):
        bad, res = interference(path, hahn63_test_bodies(closed))
        bad = [i for i in bad if i.get("a") in own or i.get("b") in own]
        ck.eq(f"schacht Interferenz 0 mit Rohr d63 und Kugelhahn d63, Hebel {'zu (quer)' if closed else 'offen (laengs)'} (geprueft {res.get('checked', '?')} Koerper)", len(bad), 0)
        for i in bad:
            print("   Ueberlappung:", i.get("a"), i.get("b"), i.get("volume_mm3"))
    print(f"INFO schacht: Masse {ev['total']['mass_g'] / 1000:.2f} kg (Wanne {bb['Schachtwanne']['mass_g'] / 1000:.2f}, Deckel {d['mass_g'] / 1000:.2f}), Aussen {g['aussen']:g} x {g['aussen']:g} x {g['z_wall_top'] - g['z_out_bottom']:g} + Deckel {s['deckel_dicke']:g}")

def check_d75(ck):
    d = 75; dp = L.DEPTH[d]; of = L.od_f(d); w = L.wall_p(d); R = max(of, 1.2 * d)
    A = math.pi / 4 * (d * d - (d - 2 * w) ** 2)
    D75 = lambda n: os.path.join(D, n + ".sc")
    ev = sc.evaluate(D75("lt_rohr_d75")); mn, mx = sc.bbox_all(ev)
    ck.eq("d75 Rohr Aussen-D", mx[0] - mn[0], d, 0.1); ck.eq("d75 Rohr Laenge", mx[2] - mn[2], 1000, 0.1)
    ck.eq(f"d75 Rohr Volumen = Ringflaeche x Laenge (Wand {w})", ev["bodies"][0]["volume_mm3"], A * 1000, A * 1000 * 0.002)
    ck.eq("d75 Rohr Innen-D 67,8", d - 2 * w, 67.8, 0.001)
    ev = sc.evaluate(D75("lt_kupplung_d75")); mn, mx = sc.bbox_all(ev)
    ck.eq("d75 Kupplung Laenge 2 t + 6", mx[2] - mn[2], 2 * dp + 6, 0.1); ck.eq("d75 Kupplung Aussen-D (Formstueck)", mx[0] - mn[0], of, 0.1)
    for ang in (90, 45):
        ev = sc.evaluate(D75(f"lt_bogen{ang}_d75")); Af = math.pi / 4 * (of ** 2 - d ** 2); exp = Af * (2 * dp + R * math.radians(ang))
        ck.eq(f"d75 Bogen{ang} Volumen (2 Schenkel + Bogen R {R:g})", sum(b["volume_mm3"] for b in ev["bodies"]), exp, exp * 0.005)
    ev = sc.evaluate(D75("lt_t_d75")); mn, mx = sc.bbox_all(ev); a = dp + of / 2
    ck.eq("d75 T Laenge Lauf", mx[0] - mn[0], 2 * a, 0.2); ck.eq("d75 T Abgang Hoehe", mx[2], a, 0.2)
    for dk in (63, 50):
        ev = sc.evaluate(D75(f"lt_reduzierung_d75_d{dk}")); mn, mx = sc.bbox_all(ev)
        ck.eq(f"d75/d{dk} Reduzierung Laenge", mx[2] - mn[2], dp + L.DEPTH[dk] + 6, 0.1); ck.eq(f"d75/d{dk} Reduzierung Aussen-D", mx[0] - mn[0], of, 0.1)
    for fn, body in (("lt_rohr_d75", "Rohr"), ("lt_kupplung_d75", "Kupplung"), ("lt_bogen90_d75", "Bogen"), ("lt_bogen45_d75", "Bogen"), ("lt_t_d75", "T_Stueck"), ("lt_reduzierung_d75_d63", "Reduzierung"), ("lt_reduzierung_d75_d50", "Reduzierung")):
        ck.eq(f"{fn} Koerperzahl (Interferenz 0: ein Koerper)", sc.evaluate(D75(fn))["body_count"], 1)
        port_checks(ck, fn, body)
    print(f"INFO d75: Formstueck-Aussen {of:.2f}, Muffentiefe {dp}, Bogenradius {R:g}, Rohr {A * 1000 * 1.4e-6:.2f} kg/m")

def main():
    want = set(a for a in sys.argv[1:] if not a.startswith("--"))
    ck = sc.Check("lt_w36")
    if not want or "verteiler" in want:
        check_verteiler(ck)
    if not want or "schelle" in want:
        check_schelle(ck)
    if not want or "leerrohr" in want:
        check_leerrohr(ck)
    if not want or "schacht" in want:
        check_schacht(ck)
    if not want or "d75" in want:
        check_d75(ck)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
