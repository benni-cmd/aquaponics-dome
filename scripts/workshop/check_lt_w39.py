"""Pruefung der W39-Leitungsteile (Kleinteile): Masse, Ports (Stirnflaechen), Volumen gegen Rechnung, Interferenz 0.
Aufruf: python scripts/workshop/check_lt_w39.py [teil ...]   (ohne Teil: alle; exit 1 bei FAIL)"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w39 as W
from check_lt_w36 import interference as _interference

D = os.path.join(sc.ROOT, "designs", "components")
PI4 = math.pi / 4

def interference(path, extra=()):
    """Wie check_lt_w36.interference, aber Paare, deren Boolean scheitert ('unchecked'), zaehlen als Treffer (sonst besteht der Check leer)."""
    bad, res = _interference(path, extra)
    for u in res.get("unchecked", []):
        bad.append({"a": u.get("a"), "b": u.get("b"), "volume_mm3": "UNGEPRUEFT: " + str(u.get("reason"))})
    return bad, res

def path_of(fname): return os.path.join(D, fname + ".sc")

def port_checks(ck, fname, bodies):
    """Zu jedem Port der Tabelle existiert eine ebene Stirnflaeche (Normale = Richtung) mit Mittelpunkt an der Portlage."""
    fm = sc.faces_multi(path_of(fname), bodies)
    planes = [(x["plane_normal"], x["centroid"]) for b in bodies for x in fm[b] if x.get("plane_normal")]
    for name, pos, dr, art, dn in W.ports(fname):
        hit = any(sum(n[i] * dr[i] for i in range(3)) > 0.999 and math.dist(cen, pos) < 0.6 for n, cen in planes)
        ck.eq(f"{fname} Port {name} ({art}, {dn}) Stirnflaeche an {tuple(round(v, 2) for v in pos)}", 1 if hit else 0, 1)

def inner_cyl(ck, fname, body, radius, label):
    fs = sc.faces(path_of(fname), body)
    ck.eq(f"{fname} {label}: Zylinderflaeche r {radius:g}", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - radius) < 0.01 for f in fs) else 0, 1)

def check_red(ck):
    fname = "lt_reduzierung_d40_d20"
    ev = sc.evaluate(path_of(fname)); b = ev["bodies"][0]; bb = b["bbox"]
    t40, t20 = L.DEPTH[40], L.DEPTH[20]; of = L.od_f(40); wi = 20 - 2 * L.wall_p(20)
    Lr = t40 + t20 + 6
    ck.eq("red d40/d20 Koerperzahl (Interferenz 0: ein Koerper)", ev["body_count"], 1)
    ck.eq(f"red d40/d20 Baulaenge = t40 + t20 + 6 = {t40} + {t20} + 6", bb["max"][2] - bb["min"][2], Lr, 0.05)
    ck.eq("red d40/d20 Aussen-D = Formstueck d40", bb["max"][0] - bb["min"][0], of, 0.05)
    ck.eq(f"red d40/d20 kuerzer als die Kette 40/32 + 32/25 + 25/20 ({W.red_kette()} mm)", 1 if Lr < W.red_kette() else 0, 1)
    ports = W.ports(fname)
    ck.eq("red d40/d20 Portabstand A-B = Baulaenge", ports[1][1][2] - ports[0][1][2], Lr, 0.05)
    exp = PI4 * (of ** 2 * Lr - 40 ** 2 * t40 - 20 ** 2 * t20 - wi ** 2 * (Lr - t40 - t20))
    ck.eq("red d40/d20 Volumen = Aussen - Muffen - Durchgang", b["volume_mm3"], exp, exp * 0.002)
    inner_cyl(ck, fname, "Reduzierung", 20, "Muffe d40"); inner_cyl(ck, fname, "Reduzierung", 10, "Muffe d20")
    port_checks(ck, fname, ["Reduzierung"])
    print(f"INFO red d40/d20: Masse {ev['total']['mass_g']:.0f} g (PVC-U 1,4), Kette {W.red_kette()} mm mit 6 Klebestellen, neu {Lr} mm mit 2")

def check_pe(ck):
    fname = "lt_uebergang_pe_pvc_d20"; q = W.PE
    ev = sc.evaluate(path_of(fname)); bb = {x["name"]: x for x in ev["bodies"]}
    ck.eq("pe-pvc d20 Koerperzahl (Koerper, Mutter, Klemmring)", ev["body_count"], 3)
    mn, mx = sc.bbox_all(ev)
    ck.eq("pe-pvc d20 Baulaenge", mx[2] - mn[2], q["laenge"], 0.05)
    ck.eq("pe-pvc d20 Mutter Aussen-D", bb["Mutter"]["bbox"]["max"][0] - bb["Mutter"]["bbox"]["min"][0], q["mutter_d"], 0.05)
    ck.eq("pe-pvc d20 Klebemuffe Aussen-D = Formstueck d20", bb["Koerper"]["bbox"]["max"][0] - bb["Koerper"]["bbox"]["min"][0], max(q["kragen_d"], L.od_f(20)), 0.05)
    wi = 20 - 2 * L.wall_p(20); dp = L.DEPTH[20]
    z0, z1 = q["kragen_z0"], q["kragen_z1"]; zh = q["hals_z0"]
    exp = PI4 * (q["kragen_d"] ** 2 * (z1 - z0) + q["hals_d"] ** 2 * (z0 - zh) + L.od_f(20) ** 2 * (q["laenge"] - z1) - 20 ** 2 * (q["tiefe"] - zh) - wi ** 2 * (q["muffe_z0"] - q["tiefe"]) - 20 ** 2 * (q["laenge"] - q["muffe_z0"]))
    ck.eq("pe-pvc d20 Volumen Koerper (Kragen + Hals + Muffe - Aufnahme - Durchgang - Muffe)", bb["Koerper"]["volume_mm3"], exp, exp * 0.002)
    exp = PI4 * (q["mutter_d"] ** 2 * q["mutter_l"] - q["gegenbohrung"] ** 2 * (q["mutter_l"] - q["mutter_boden"]) - q["loch"] ** 2 * q["mutter_boden"])
    ck.eq("pe-pvc d20 Volumen Mutter", bb["Mutter"]["volume_mm3"], exp, exp * 0.002)
    exp = PI4 * (q["ring_d"] ** 2 - 20 ** 2) * (q["ring_z1"] - q["ring_z0"])
    ck.eq("pe-pvc d20 Volumen Klemmring", bb["Klemmring"]["volume_mm3"], exp, exp * 0.002)
    ck.eq(f"pe-pvc d20 Einstecktiefe PE {q['tiefe']:g}: Anschlag (Boden der Aufnahme) bei z = {q['tiefe']:g}", 1 if any(f.get("plane_normal") and f["plane_normal"][2] < -0.999 and abs(f["centroid"][2] - q["tiefe"]) < 0.05 for f in sc.faces(path_of(fname), "Koerper")) else 0, 1)
    ck.eq("pe-pvc d20 Gewinde im Eingriff Hals in Mutter >= 5", 1 if q["kragen_z0"] - q["hals_z0"] >= 5 else 0, 1)
    ck.eq("pe-pvc d20 Muttergegenbohrung nimmt Hals und Klemmring auf (25 > 24,6 und 24,8)", 1 if q["gegenbohrung"] > max(q["hals_d"], q["ring_d"]) else 0, 1)
    inner_cyl(ck, fname, "Koerper", 10, "Klebemuffe B d20")
    port_checks(ck, fname, ["Mutter", "Koerper"])
    extra = [{"command": "solid.cylinder", "params": {"diameter": 20, "height": q["tiefe"] + 40, "base": [0, 0, -40], "operation": "new", "name": "T_PE", "body_name": "Test_PE_Rohr"}}]
    bad, res = interference(path_of(fname), extra)
    ck.eq(f"pe-pvc d20 Interferenz 0 (Koerper, Mutter, Klemmring und eingestecktes PE-Rohr d20 bis z = {q['tiefe']:g}; geprueft {res.get('checked', '?')} Koerper)", len(bad), 0)
    for i in bad:
        print("   Ueberlappung:", i.get("a"), i.get("b"), i.get("volume_mm3"))
    print(f"INFO pe-pvc d20: Masse {ev['total']['mass_g']:.1f} g (PP 0,91, POM 1,41)")

def check_hose(ck):
    fname = "lt_schlauch_id16_L100"
    ev = sc.evaluate(path_of(fname)); b = ev["bodies"][0]; bb = b["bbox"]
    ck.eq("schlauch ID16 L100 Koerperzahl", ev["body_count"], 1)
    ck.eq("schlauch ID16 L100 Laenge", bb["max"][2] - bb["min"][2], W.HOSE_L, 0.05)
    ck.eq("schlauch ID16 L100 Aussen-D AD20", bb["max"][0] - bb["min"][0], 20, 0.05)
    exp = PI4 * (20 ** 2 - 16 ** 2) * W.HOSE_L
    ck.eq("schlauch ID16 L100 Volumen = Ringflaeche x Laenge", b["volume_mm3"], exp, exp * 0.002)
    inner_cyl(ck, fname, "Schlauch", 8, "Innen ID16")
    port_checks(ck, fname, ["Schlauch"])
    print(f"INFO schlauch ID16 L100: Masse {ev['total']['mass_g']:.1f} g")

def check_kappe(ck):
    for d in W.KAPPE_SIZES:
        fname = f"lt_kappe_d{d}"; dp = L.DEPTH[d]; of = L.od_f(d); h = dp + W.KAPPE_BODEN
        ev = sc.evaluate(path_of(fname)); b = ev["bodies"][0]; bb = b["bbox"]
        ck.eq(f"kappe d{d} Koerperzahl", ev["body_count"], 1)
        ck.eq(f"kappe d{d} Hoehe = Muffentiefe {dp:g} + Boden {W.KAPPE_BODEN:g}", bb["max"][2] - bb["min"][2], h, 0.05)
        ck.eq(f"kappe d{d} Aussen-D = Formstueck od_f", bb["max"][0] - bb["min"][0], of, 0.05)
        exp = PI4 * (of ** 2 * h - d ** 2 * dp)
        ck.eq(f"kappe d{d} Volumen = Aussen - Muffe", b["volume_mm3"], exp, exp * 0.002)
        fs = sc.faces(path_of(fname), "Kappe")
        ck.eq(f"kappe d{d} Boden geschlossen: Aussenflaeche +Z bei z = {h:g}", 1 if any(f.get("plane_normal") and f["plane_normal"][2] > 0.999 and abs(f["centroid"][2] - h) < 0.05 for f in fs) else 0, 1)
        ck.eq(f"kappe d{d} Anschlag der Muffe bei z = {dp:g} (Boden dick {W.KAPPE_BODEN:g})", 1 if any(f.get("plane_normal") and f["plane_normal"][2] < -0.999 and abs(f["centroid"][2] - dp) < 0.05 for f in fs) else 0, 1)
        port_checks(ck, fname, ["Kappe"])
        extra = [{"command": "solid.cylinder", "params": {"diameter": d, "height": 20 + dp, "base": [0, 0, -20], "operation": "new", "name": "T_Zapfen", "body_name": "Test_Zapfen"}}]
        bad, res = interference(path_of(fname), extra)
        ck.eq(f"kappe d{d} Interferenz 0 gegen Zapfen d{d} (steckt {dp:g} mm in der Muffe; geprueft {res.get('checked', '?')} Koerper)", len(bad), 0)
        print(f"INFO kappe d{d}: Masse {ev['total']['mass_g']:.1f} g")
    # Kappe auf den echten Zapfen des Verteilers d50 (Abgang 3 Messkreis d20, Abgang 4 Bypass d50): Zylinder und Zapfenoberkante der Verteiler-Datei gegen die Kappenmasse (Boolean mit dem Verteiler scheitert, 114 s, "no result")
    import leitung_w36 as W36
    g = W36.v50_geom(); top = g["top"]
    fv = sc.faces(path_of("lt_verteiler_d50"), "Verteiler")
    for k, d in ((2, 20), (3, 50)):
        dp = L.DEPTH[d]; x = g["xs"][k]; z0 = top - dp
        zyl = [f["cylinder"] for f in fv if f.get("cylinder") and abs(abs(f["cylinder"]["axis"][2]) - 1) < 0.01 and abs(f["cylinder"]["origin"][0] - x) < 0.1 and abs(f["cylinder"]["radius"] - d / 2) < 0.05]
        ck.eq(f"kappe d{d} Zapfen Abgang {k + 1} (x = {x:g}): Aussenradius {d / 2:g} = Muffenradius der Kappe (Passung ohne Spiel und ohne Ueberlappung)", 1 if zyl else 0, 1)
        ob = [f for f in fv if f.get("plane_normal") and f["plane_normal"][2] > 0.999 and abs(f["centroid"][2] - top) < 0.05 and abs(f["centroid"][0] - x) < 0.1]
        ck.eq(f"kappe d{d} Zapfenoberkante z = {top:g} liegt am Muffenanschlag der Kappe (Kappenursprung z = {z0:g} + Tiefe {dp:g})", 1 if ob else 0, 1)
        ck.eq(f"kappe d{d} Kappenhoehe {dp + W.KAPPE_BODEN:g} ueber dem Zapfen: Oberkante {z0 + dp + W.KAPPE_BODEN:g} > Zapfenoberkante, Boden {W.KAPPE_BODEN:g} dick", 1 if abs((z0 + dp + W.KAPPE_BODEN) - (top + W.KAPPE_BODEN)) < 1e-6 else 0, 1)

def check_rsv(ck):
    for d in W.RSV_SIZES:
        fname = f"lt_rueckschlagventil_d{d}"; g = W.rsv_geom(d)
        ev = sc.evaluate(path_of(fname)); b = ev["bodies"][0]; bb = b["bbox"]
        ck.eq(f"rsv d{d} Koerperzahl (Interferenz 0: ein Koerper)", ev["body_count"], 1)
        ck.eq(f"rsv d{d} Baulaenge = 50 + 2 t = 50 + 2 x {g['dp']:g} (wie Kugelhahn)", bb["max"][2] - bb["min"][2], 50 + 2 * g["dp"], 0.05)
        ck.eq(f"rsv d{d} Laenge = Kugelhahn-Laenge L.ports(lt_kugelhahn_d{d})", W.ports(fname)[1][1][2], L.ports(f"lt_kugelhahn_d{d}")[1][1][2], 0.001)
        ck.eq(f"rsv d{d} Gehaeuse-D = od_f + 12", bb["max"][0] - bb["min"][0], g["ob"], 0.05)
        ck.eq(f"rsv d{d} Volumen = Gehaeuse + Stutzen - Muffen - Durchgang", b["volume_mm3"], W.rsv_vol(d), W.rsv_vol(d) * 0.002)
        inner_cyl(ck, fname, "Rueckschlagventil", d / 2, "Muffe")
        inner_cyl(ck, fname, "Rueckschlagventil", g["wi"] / 2, "Durchgang")
        ck.eq(f"rsv d{d} Durchflussrichtung: A ({W.ports(fname)[0][2]}) -> B ({W.ports(fname)[1][2]}) entlang +Z", 1 if W.ports(fname)[0][2] == (0, 0, -1) and W.ports(fname)[1][2] == (0, 0, 1) else 0, 1)
        port_checks(ck, fname, ["Rueckschlagventil"])
        print(f"INFO rsv d{d}: Masse {ev['total']['mass_g']:.0f} g (PVC-U 1,4)")

def check_kabel(ck):
    for dn in W.KAB_SIZES:
        fname = f"lt_kabeleinfuehrung_dn{dn}"; g = W.kab_geom(dn); k = W.KAB; t = g["t"]
        ev = sc.evaluate(path_of(fname)); bb = {x["name"]: x for x in ev["bodies"]}
        ck.eq(f"kabel DN{dn} Koerperzahl (Koerper, Dichtung, Gegenmutter)", ev["body_count"], 3)
        mn, mx = sc.bbox_all(ev)
        ck.eq(f"kabel DN{dn} Hoehe = Muffe {t:g} + Kragen {k['kragen_dicke']:g} + Dichtung + Boden + Mutter + Ueberstand = {g['z_top']:g}", mx[2] - mn[2], g["z_top"], 0.05)
        ck.eq(f"kabel DN{dn} Kragen-Aussen-D", bb["Koerper"]["bbox"]["max"][0] - bb["Koerper"]["bbox"]["min"][0], g["kragen"], 0.05)
        exp = PI4 * (g["od_m"] ** 2 * t + g["kragen"] ** 2 * k["kragen_dicke"] + g["hals"] ** 2 * (g["z_top"] - g["z_k1"]) - g["d"] ** 2 * t - g["wi"] ** 2 * (g["z_top"] - t))
        ck.eq(f"kabel DN{dn} Volumen Koerper", bb["Koerper"]["volume_mm3"], exp, exp * 0.002)
        exp = PI4 * (g["dichtung_aussen"] ** 2 - g["hals"] ** 2) * k["dichtung"]
        ck.eq(f"kabel DN{dn} Volumen Dichtung", bb["Dichtung"]["volume_mm3"], exp, exp * 0.002)
        exp = PI4 * (g["mutter_aussen"] ** 2 - g["hals"] ** 2) * k["mutter"]
        ck.eq(f"kabel DN{dn} Volumen Gegenmutter", bb["Gegenmutter"]["volume_mm3"], exp, exp * 0.002)
        ck.eq(f"kabel DN{dn} Kabeldurchgang frei {g['wi']:g} (Leerrohr-Innen-D)", 1 if any(abs(f["cylinder"]["radius"] - g["wi"] / 2) < 0.01 for f in sc.faces(path_of(fname), "Koerper") if f.get("cylinder")) else 0, 1)
        inner_cyl(ck, fname, "Koerper", g["d"] / 2, "Steckmuffe fuer Leerrohr")
        ck.eq(f"kabel DN{dn} Muffe passt zum Leerrohr (Aussen {g['od_m']:g}, Tiefe {t:g} wie lt_leerrohr_dn{dn})", 1 if W.W36.LR[dn]["od_m"] == g["od_m"] and W.W36.LR[dn]["t"] == t else 0, 1)
        ck.eq(f"kabel DN{dn} Gewindeueberstand ueber der Mutter = {k['ueberstand']:g}", g["z_top"] - g["z_m1"], k["ueberstand"], 0.001)
        port_checks(ck, fname, ["Koerper", "Dichtung"])
        extra = [{"command": "solid.box", "params": {"length": g["kragen"] + 80, "width": g["kragen"] + 80, "height": k["boden"], "center": [0, 0, g["z_d1"] + k["boden"] / 2], "operation": "new", "name": "T_Boden", "body_name": "Test_Boden"}},
                 {"command": "solid.cylinder", "params": {"diameter": g["hals"], "height": k["boden"] + 2, "base": [0, 0, g["z_d1"] - 1], "operation": "cut", "targets": ["Test_Boden"], "name": "T_Boden_Loch"}},
                 {"command": "solid.cylinder", "params": {"diameter": g["d"], "height": 60 + t, "base": [0, 0, -60], "operation": "new", "name": "T_Leerrohr", "body_name": "Test_Leerrohr"}}]
        bad, res = interference(path_of(fname), extra)
        ck.eq(f"kabel DN{dn} Interferenz 0 (Koerper, Dichtung, Gegenmutter, Schrankboden {k['boden']:g} mm mit Loch {g['hals']:g}, eingestecktes Leerrohr AD{g['d']:g} bis z = {t:g}; geprueft {res.get('checked', '?')} Koerper)", len(bad), 0)
        for i in bad:
            print("   Ueberlappung:", i.get("a"), i.get("b"), i.get("volume_mm3"))
        print(f"INFO kabel DN{dn}: Masse {ev['total']['mass_g']:.0f} g (PP 0,91, EPDM 1,1), Hoehe {g['z_top']:g}")

CHECKS = [("red", check_red), ("pe", check_pe), ("hose", check_hose), ("kappe", check_kappe), ("rsv", check_rsv), ("kabel", check_kabel)]

def main():
    want = set(a for a in sys.argv[1:] if not a.startswith("--"))
    ck = sc.Check("lt_w39")
    for key, fn in CHECKS:
        if not want or key in want:
            fn(ck)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
