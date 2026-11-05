"""Pruefung tiefer Ventilschacht d63 (schacht_tief.py): Koerper, Masse, Volumen, Deckel auf Flur, Ports, Bedienbarkeit, Interferenz 0 gegen Hahn/Rohre
in beiden Hebelstellungen, Abstand zu allen Trassen aus data/leitungstrassen.json am Einbauort (KH1/KH2; Stamm-Hahn je Linie auf der besten Geraden).
Aufruf: python -X utf8 scripts/workshop/check_schacht_tief.py [senkrecht|waagerecht] [--render]   (exit 1 bei FAIL)"""
import sys, os, math, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import schacht_tief as S
import check_lt_w36 as C

D = os.path.join(sc.ROOT, "designs", "components")
BEFUND = []
TR = json.load(open(os.path.join(sc.ROOT, "data", "leitungstrassen.json"), encoding="utf-8"))
H = dict(ob=L.od_f(63) + 12, hebel_x=(L.od_f(63) + 12) / 2 + 34, hebel_l=110.0, hebel_b=63 / 5, hebel_h=14.0, spindel_h=(L.od_f(63) + 12) / 2 + 30)
OF63, OF75 = L.od_f(63), L.od_f(75)
LUFT_MIN = 10.0              # [A] Mindestabstand Schacht-Aussenhaut zu fremder Leitung
REICH_MAX = 600.0            # [A] Greiftiefe Flur bis Hebeloberkante, kniend mit gestrecktem Arm (Armlaenge Schulter-Fingerspitze ca. 650, nicht abgerufen)

def cyl(nm, d, ln, base, axis):
    return {"command": "solid.cylinder", "params": {"diameter": d, "height": ln, "base": base, "axis": axis, "operation": "new", "name": nm, "body_name": nm}}
def box(nm, lx, wy, hz, c):
    return {"command": "solid.box", "params": {"length": lx, "width": wy, "height": hz, "center": c, "operation": "new", "name": nm, "body_name": nm}}

def unit(v): n = math.sqrt(sum(x * x for x in v)); return [x / n for x in v]

def kh_frames():
    """KH1/KH2: Ursprung Hahnmitte, X = Richtung K01-m/K17-m (vom Steigrohr weg), Y = Z x X."""
    out = {}
    rs = {r["id"]: r for r in TR["r_stuecke"]}
    tr = {t["id"]: t for t in TR["trassen"]}
    for kh, tm in (("KH1", "K01-m"), ("KH2", "K17-m")):
        p = rs[kh]["pos_a"]; o = [p[0], p[1], p[2] - S.HAHN_L / 2]
        a, b = tr[tm]["pfad"][0], tr[tm]["pfad"][1]
        X = unit([b[0] - a[0], b[1] - a[1], 0.0]); Y = [-X[1], X[0], 0.0]
        out[kh] = (o, X, Y)
    return out

def to_local(fr, p):
    o, X, Y = fr; d = [p[i] - o[i] for i in range(3)]
    return (sum(d[i] * X[i] for i in range(3)), sum(d[i] * Y[i] for i in range(3)), d[2])

def shaft_box(g):
    """Aussenhuelle (Wanne + Deckel) als Achsen-Box im Schacht-KS."""
    du = (g["deckel_x"] - (g["x_out"][1] - g["x_out"][0])) / 2
    return ((g["x_out"][0] - du, g["y_out"][0] - du, g["z_out_bottom"]), (g["x_out"][1] + du, g["y_out"][1] + du, g["z_top"]))

def box_dist(p, bx):
    lo, hi = bx
    dd = [max(lo[i] - p[i], 0, p[i] - hi[i]) for i in range(3)]
    return math.sqrt(sum(x * x for x in dd))

def capsules():
    """Alle Trassen-Segmente (Radius d/2) und T-Stueck-Arme (Radius Formstueck/2, Laenge Muffentiefe + Formstueck/2)."""
    caps = []
    for t in TR["trassen"]:
        p = t["pfad"]; d = t.get("dn") or 0
        for i, (a, b) in enumerate(zip(p, p[1:])):
            caps.append((t["id"], i, a, b, d / 2))
    tr = {t["id"]: t for t in TR["trassen"]}
    for ts in TR["t_stuecke"]:
        d = ts["d"]; a = L.DEPTH.get(d, 40) + L.od_f(d) / 2
        for pt in ts["ports"]:
            t = tr.get(pt["trasse"])
            if not t:
                continue
            q = t["pfad"][1] if pt["ende"] == "start" else t["pfad"][-2]
            u = unit([q[i] - ts["pos"][i] for i in range(3)])
            caps.append((ts["id"] + ":" + pt["trasse"], 0, ts["pos"], [ts["pos"][i] + a * u[i] for i in range(3)], L.od_f(d) / 2))
    return caps

def on_axis(q, axes):
    for kind, c in axes:
        if kind == "z" and math.hypot(q[0], q[1]) < 1.0 and q[2] <= c + 1.0:
            return True
        if kind == "x" and abs(q[1]) < 1.0 and abs(q[2] - c) < 1.0:
            return True
    return False

def clearance(fr, g, axes):
    """Kleinster Abstand fremder Leitungen zur Schachthuelle; Punkte auf den Durchfuehrungs-Achsen zaehlen als gewollt (Rohr durch Dichtung)."""
    bx = shaft_box(g)
    worst = (1e9, None)
    for tid, i, a, b, r in capsules():
        la, lb = to_local(fr, a), to_local(fr, b)
        n = max(2, int(math.dist(la, lb) / 4))
        for k in range(n + 1):
            q = [la[j] + (lb[j] - la[j]) * k / n for j in range(3)]
            if on_axis(q, axes):
                continue
            dd = box_dist(q, bx) - r
            if dd < worst[0]:
                worst = (dd, f"{tid}[{i}]", [round(x, 1) for x in q])
    return worst

def test_bodies_senk(g, closed, abgang):
    h = H; qz = g["quer_z"]; arm = L.DEPTH[75] + OF75 / 2
    c = [cyl("Test_Gehaeuse", h["ob"], 50, [0, 0, -25], [0, 0, 1]),
         cyl("Test_Stutzen_B", OF63, L.DEPTH[63], [0, 0, -S.HAHN_L / 2], [0, 0, 1]), cyl("Test_Stutzen_A", OF63, L.DEPTH[63], [0, 0, 25], [0, 0, 1]),
         cyl("Test_Spindel", 14, h["spindel_h"], [0, 0, 0], [0, 1, 0]),
         (box("Test_Hebel", h["hebel_l"], h["hebel_h"], h["hebel_b"], [0, h["hebel_x"], 0]) if closed else box("Test_Hebel", h["hebel_b"], h["hebel_h"], h["hebel_l"], [0, h["hebel_x"], 0])),
         cyl("Test_Reduzierung_T_Abgang", OF75, qz - S.HAHN_L / 2, [0, 0, S.HAHN_L / 2], [0, 0, 1]),
         cyl("Test_T_Lauf", OF75, 2 * arm, [-arm, 0, qz], [1, 0, 0]),
         cyl("Test_Rohr75_A", 75, 500, [-arm - 500, 0, qz], [1, 0, 0]), cyl("Test_Rohr75_B", 75, 600, [arm, 0, qz], [1, 0, 0]),
         cyl("Test_Bogenschenkel75_A", OF75, 40, [-arm - 40, 0, qz], [1, 0, 0]),
         cyl("Test_Rohr63_unten", OF63, 110, [0, 0, -S.HAHN_L / 2 - 110], [0, 0, 1])]
    zb = -S.HAHN_L / 2 - 110
    c.append(cyl("Test_Tiefleitung", 63, 300, [0, 0, zb], [abgang[0], abgang[1], 0]))
    return c

def run_check(ck, v, render):
    g = S.geom(v); fname = S.FNAME[v]; path = os.path.join(D, fname + ".sc")
    ev = sc.evaluate(path); bb = {b["name"]: b for b in ev["bodies"]}
    seals = ["Dichtung_Boden", "Dichtung_A", "Dichtung_B"] if v == "senkrecht" else ["Dichtung_A", "Dichtung_B"]
    ck.eq(f"{v}: Koerperzahl (Wanne, Deckel, {len(seals)} Dichtungen)", ev["body_count"], 2 + len(seals))
    w = bb["Schachtwanne"]; ax, ay = g["x_out"][1] - g["x_out"][0], g["y_out"][1] - g["y_out"][0]
    ck.eq(f"{v}: Aussenmass laengs X", w["bbox"]["max"][0] - w["bbox"]["min"][0], ax, 0.1)
    ck.eq(f"{v}: Aussenmass quer Y", w["bbox"]["max"][1] - w["bbox"]["min"][1], ay, 0.1)
    ck.eq(f"{v}: Wannenhoehe", w["bbox"]["max"][2] - w["bbox"]["min"][2], g["hoehe_wanne"], 0.1)
    hz = g["z_wall_top"] - g["z_boden_innen"]
    exp = ax * ay * g["hoehe_wanne"] - g["innen_x"] * g["innen_y"] * hz
    if v == "senkrecht":
        exp -= math.pi / 4 * g["boden_loch"] ** 2 * g["boden"] + 2 * math.pi / 4 * g["quer_loch"] ** 2 * g["wand"]
    else:
        exp -= 2 * math.pi / 4 * g["rohr_loch"] ** 2 * g["wand"]
    ck.eq(f"{v}: Wannenvolumen = Aussen - Innenraum - Durchfuehrungen", w["volume_mm3"], exp, exp * 0.002)
    dk = bb["Deckel"]
    exp = g["deckel_x"] * g["deckel_y"] * g["deckel_dicke"] - 2 * 100 * 30 * 15
    ck.eq(f"{v}: Deckelvolumen (minus 2 Griffmulden)", dk["volume_mm3"], exp, exp * 0.002)
    ck.eq(f"{v}: Deckeloberkante = Flur (z = {g['z_top']:.1f} im Schacht-KS = Z {S.FLUR_Z:g} absolut)", dk["bbox"]["max"][2], g["z_top"], 0.1)
    ck.eq(f"{v}: Deckel liegt auf der Wand", dk["bbox"]["min"][2], g["z_wall_top"], 0.1)
    fsd = sc.faces(path, "Deckel")
    ck.eq(f"{v}: Port Deckel (Normale +Z, Mitte auf Schachtachse)", 1 if any(f.get("plane_normal") and f["plane_normal"][2] > 0.999 and math.dist(f["centroid"], (g["versatz_x"], g["versatz_y"], g["z_top"])) < 0.6 for f in fsd) else 0, 1)
    fw = sc.faces(path, "Schachtwanne")
    if v == "senkrecht":
        ck.eq(f"{v}: Bodendurchfuehrung d{g['boden_loch']:g} senkrecht auf der Hahnachse", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - g["boden_loch"] / 2) < 0.01 and abs(abs(f["cylinder"]["axis"][2]) - 1) < 1e-6 and math.hypot(f["cylinder"]["origin"][0], f["cylinder"]["origin"][1]) < 0.01 for f in fw) else 0, 1)
        ck.eq(f"{v}: Querdurchfuehrung d{g['quer_loch']:g} auf Achse y 0 / z {g['quer_z']:.1f}", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - g["quer_loch"] / 2) < 0.01 and abs(abs(f["cylinder"]["axis"][0]) - 1) < 1e-6 and abs(f["cylinder"]["origin"][2] - g["quer_z"]) < 0.01 for f in fw) else 0, 1)
        ck.eq(f"{v}: Bodendichtung Bohrung {g['boden_dichtung_innen']:g} >= Formstueck d63 {OF63:.2f}", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - g["boden_dichtung_innen"] / 2) < 0.01 for f in sc.faces(path, "Dichtung_Boden")) and g["boden_dichtung_innen"] >= OF63 else 0, 1)
        for nmx in ("A", "B"):
            ck.eq(f"{v}: Querdichtung {nmx} Bohrung {g['quer_dichtung_innen']:g} >= Formstueck d75 {OF75:.2f}", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - g["quer_dichtung_innen"] / 2) < 0.01 for f in sc.faces(path, f"Dichtung_{nmx}")) and g["quer_dichtung_innen"] >= OF75 else 0, 1)
        ck.eq(f"{v}: Hahnmitte {g['z_top']:.1f} unter Flur, Hahn-Port A {g['z_top'] - S.HAHN_L / 2:.1f} (Soll 424 +- 1, M10-S2N)", g["z_top"] - S.HAHN_L / 2, S.FLUR_Z - S.KH_PORT_A_Z, 1.0)
        ck.eq(f"{v}: Querleitung d75 {g['z_top'] - g['quer_z']:.1f} unter Flur (Soll 250 = Z 150 absolut, T5/T13)", g["z_top"] - g["quer_z"], S.FLUR_Z - S.QUER_Z, 0.1)
        lever_top = H["hebel_l"] / 2
        ck.eq(f"{v}: Boden innen {g['z_boden_innen']:g} unter Stutzen-Unterkante {-S.HAHN_L / 2:g} und unter Hebel offen {-lever_top:g}", 1 if g["z_boden_innen"] < -lever_top and g["z_boden_innen"] < -S.HAHN_L / 2 else 0, 1)
        zb = -S.HAHN_L / 2 - 110
        ck.eq(f"{v}: Tiefleitung K56-b/K57-b (Achse {zb:g}, Oberkante {zb + 31.5:g}) liegt unter dem Schachtboden {g['z_out_bottom']:g}", 1 if zb + 31.5 < g["z_out_bottom"] else 0, 1)
    else:
        ck.eq(f"{v}: Wanddurchfuehrung d{g['rohr_loch']:g} auf der Rohrachse", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - g["rohr_loch"] / 2) < 0.01 and abs(abs(f["cylinder"]["axis"][0]) - 1) < 1e-6 for f in fw) else 0, 1)
        for nmx in ("A", "B"):
            ck.eq(f"{v}: Dichtung {nmx} Bohrung = Rohr d63", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - 31.5) < 0.01 for f in sc.faces(path, f"Dichtung_{nmx}")) else 0, 1)
        ck.eq(f"{v}: Rohrachse {g['z_top']:g} unter Flur (Soll 186 = Z 214 absolut, K06-T/K22-T)", g["z_top"], S.FLUR_Z - S.STAMM_Z, 0.1)
        lever_top = H["hebel_x"] + H["hebel_h"] / 2
        ck.eq(f"{v}: Luft Hebel-Oberkante {lever_top:.1f} bis Deckelunterkante {g['z_wall_top']:g} >= 30", 1 if g["z_wall_top"] - lever_top >= 30 else 0, 1)
        ck.eq(f"{v}: Platz unter dem Hahn >= 90 (Ist {-H['ob'] / 2 - g['z_boden_innen']:.1f})", 1 if -H["ob"] / 2 - g["z_boden_innen"] >= 90 else 0, 1)
        ck.eq(f"{v}: Hebel offen (laengs, {H['hebel_l']:g}) passt in innen {g['innen_x']:g} mit je >= 60 Griffraum", 1 if g["innen_x"] - H["hebel_l"] >= 120 else 0, 1)
    gross, klein = max(g["innen_x"], g["innen_y"]), min(g["innen_x"], g["innen_y"])
    ck.eq(f"{v}: Oeffnung {gross:g} >= Hebel + 2 x 100 Hand", 1 if gross >= H["hebel_l"] + 200 else 0, 1)
    tief = g["z_top"] - lever_top
    ck.eq(f"{v}: Greiftiefe Flur bis Hebeloberkante {tief:.0f} <= {REICH_MAX:g}", 1 if tief <= REICH_MAX else 0, 1)
    own = {"Schachtwanne", "Deckel", *seals}
    for closed in (False, True):
        if v == "senkrecht":
            for kh, abg in abgaenge().items():
                bad, res = C.interference(path, test_bodies_senk(g, closed, abg))
                bad = [i for i in bad if i.get("a") in own or i.get("b") in own]
                ck.eq(f"{v}: Interferenz 0 mit Hahn d63, T d75, Rohr d75/d63, Tiefleitung Richtung {kh}, Hebel {'zu' if closed else 'offen'} ({res.get('checked', '?')} Koerper)", len(bad), 0)
                for i in bad:
                    print("   Ueberlappung:", i.get("a"), i.get("b"), i.get("volume_mm3"))
        else:
            bad, res = C.interference(path, C.hahn63_test_bodies(closed))
            bad = [i for i in bad if i.get("a") in own or i.get("b") in own]
            ck.eq(f"{v}: Interferenz 0 mit Rohr d63 und Kugelhahn d63, Hebel {'zu' if closed else 'offen'} ({res.get('checked', '?')} Koerper)", len(bad), 0)
            for i in bad:
                print("   Ueberlappung:", i.get("a"), i.get("b"), i.get("volume_mm3"))
    # Einbauort gegen alle Trassen
    if v == "senkrecht":
        for kh, fr in kh_frames().items():
            dd, wo, q = clearance(fr, g, [("z", g["quer_z"]), ("x", g["quer_z"])])
            ck.eq(f"{v} an {kh}: kleinster Abstand fremder Leitung/T-Stueck zur Schachthuelle {dd:.1f} >= {LUFT_MIN:g} (naechste: {wo} bei {q})", 1 if dd >= LUFT_MIN else 0, 1)
    else:
        # Einbauort der Stamm-Haehne legt die Montage (S2N) fest; hier nur Befund je Linie (zaehlt nicht zum Bauteil-Ergebnis)
        for lin, info in stamm_plaetze(g).items():
            if info["frame"] is None:
                BEFUND.append(f"{v} Linie {lin}: keine gerade Strecke bei Z 214 lang genug (Bedarf {info['bedarf']:.0f}, beste {info['best']})")
                continue
            dd, wo, q = clearance(info["frame"], g, [("x", 0.0)])
            txt = f"{v} Linie {lin}: bester Platz Hahnmitte {info['mitte']} auf {info['best']}, Luft zur naechsten fremden Leitung {dd:.1f} (naechste: {wo})"
            print(("EINBAU OK  " if dd >= LUFT_MIN else "BEFUND     ") + txt)
            if dd < LUFT_MIN:
                BEFUND.append(txt)
    print(f"INFO {v}: Masse {ev['total']['mass_g'] / 1000:.2f} kg (Wanne {w['mass_g'] / 1000:.2f}, Deckel {dk['mass_g'] / 1000:.2f}), aussen {ax:g} x {ay:g} x {g['tiefe_gesamt']:.1f}")
    if render:
        tmp = os.path.join(sc.TMP, f"ws-{fname}-bild.json"); out_sc = os.path.join(sc.TMP, f"{fname}-bild.sc")
        cmds = (test_bodies_senk(g, False, abgaenge()["KH1"]) if v == "senkrecht" else C.hahn63_test_bodies(False))
        json.dump({"commands": cmds}, open(tmp, "w"))
        r = subprocess.run([sc.CLI, "run", tmp, "--in", path, "--save", out_sc, "--quiet"], capture_output=True, text=True)
        if r.returncode == 0:
            print("Bild", S.render(v, fname, out_sc))
        else:
            print("Bild FEHLER", r.stderr[-300:])

def abgaenge():
    """Richtung der Tiefleitung K56-b/K57-b (2. Segment) im Schacht-KS von KH1/KH2."""
    tr = {t["id"]: t for t in TR["trassen"]}; out = {}
    for kh, tb in (("KH1", "K56-b"), ("KH2", "K57-b")):
        fr = kh_frames()[kh]; p = tr[tb]["pfad"]
        a, b = to_local(fr, p[1]), to_local(fr, p[2])
        out[kh] = unit([b[0] - a[0], b[1] - a[1], 0.0])
    return out

def stamm_plaetze(g):
    """Je Linie: gerade Segmente bei Z 214 auf K06-T/K06-T-b bzw. K22-T/K22-T-b; frei = Laenge minus Formstueck-Anteil an beiden Enden
    (T: Muffentiefe + Formstueck/2; Bogen: Muffentiefe + R tan(Winkel/2), R = max(Formstueck, 1,2 d)); Bedarf = Aussen laengs + 2 x 3 Dichtung.
    Bestes Segment -> Schacht mittig auf die freie Strecke."""
    R = max(OF63, 1.2 * 63); tarm = L.DEPTH[63] + OF63 / 2
    bedarf = (g["x_out"][1] - g["x_out"][0]) + 6
    tr = {t["id"]: t for t in TR["trassen"]}; tpos = [tuple(t["pos"]) for t in TR["t_stuecke"]]
    out = {}
    for lin, ids in ((1, ("K06-T", "K06-T-b")), (2, ("K22-T", "K22-T-b"))):
        rows = []
        for tid in ids:
            p = tr[tid]["pfad"]
            for i, (a, b) in enumerate(zip(p, p[1:])):
                ln = math.dist(a, b); u = unit([b[j] - a[j] for j in range(3)])
                def ende(k, pt, nb):
                    if any(math.dist(pt, tp) < 1 for tp in tpos):
                        return tarm
                    if nb is None:
                        return L.DEPTH[63] + 20          # Stutzen/Anschluss: Muffe + 20 [A]
                    w = unit([(pt[j] - nb[j]) if k == 0 else (nb[j] - pt[j]) for j in range(3)])     # Nachbar-Segment in Fliessrichtung
                    ang = math.acos(max(-1.0, min(1.0, sum(w[j] * u[j] for j in range(3)))))         # Umlenkwinkel am Knick
                    return L.DEPTH[63] + R * math.tan(ang / 2)
                ea = ende(0, a, p[i - 1] if i > 0 else None)
                eb = ende(1, b, p[i + 2] if i + 2 < len(p) else None)
                rows.append((ln - ea - eb, f"{tid}[{i}]", a, b, ea, eb, ln))
        rows.sort(key=lambda r: -r[0])
        info = {"bedarf": bedarf, "best": f"{rows[0][1]} frei {rows[0][0]:.0f} von {rows[0][6]:.0f}", "liste": [(r[1], round(r[0]), round(r[6])) for r in rows], "frame": None}
        print(f"INFO Stamm Linie {lin}: Bedarf gerade {bedarf:.0f} mm; Segmente (frei/Laenge): " + ", ".join(f"{r[1]} {r[0]:.0f}/{r[6]:.0f}" for r in rows))
        best = None
        for frei, name, a, b, ea, eb, ln in rows:
            if frei < bedarf:
                continue
            u = unit([b[j] - a[j] for j in range(3)])
            s = ea + bedarf / 2
            while s <= ln - eb - bedarf / 2 + 1e-6:
                o = [a[j] + u[j] * s for j in range(3)]
                fr = (o, u, [-u[1], u[0], 0.0])
                dd = clearance(fr, g, [("x", 0.0)])[0]
                if best is None or dd > best[0]:
                    best = (dd, name, fr, s, ln)
                s += 10.0
        if best:
            dd, name, fr, s, ln = best
            info["frame"] = fr; info["mitte"] = [round(x, 1) for x in fr[0]]; info["best"] = f"{name} bei {s:.0f} von {ln:.0f} mm"
            print(f"INFO Stamm Linie {lin}: bester Platz Hahnmitte {info['mitte']} auf {name} ({s:.0f} mm ab Segmentanfang), Rohrrichtung {[round(x, 4) for x in fr[1]]}, Luft {dd:.1f}")
        out[lin] = info
    return out

def main():
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or list(S.VAR)
    ck = sc.Check("schacht_tief")
    for v in want:
        run_check(ck, v, "--render" in sys.argv)
    for b in BEFUND:
        print("BEFUND an die Montage:", b)
    print(f"== Befunde Einbauort: {len(BEFUND)}")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
