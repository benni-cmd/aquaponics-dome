"""Leitungsteile-Bibliothek T70 (W10): Rohr, Kupplung, Bogen 90/45, T-Stueck, Kugelhahn, Schlauch gerade/Bogen, Rohrklemme, Verteiler als Komponenten mit Ports.
Konvention: Teile liegen mit Port A im Ursprung; Ports siehe docs/parts/leitungsteile.md (Name, DN, Lage, Richtung). Masse PVC-U nach DIN 8062/EN 1452 (Naeherung).
Aufruf: python scripts/workshop/leitung.py [teil ...]   (ohne Teil: alle)"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(__file__))
import sc

SIZES = [20, 25, 32, 40, 50, 63, 110]                   # Rohr-Aussendurchmesser d (mm), DN-Naeherung 15/20/25/32/40/50/100 (d20 = PE-Tropfrohr des Beets)
DEPTH = {20: 16, 25: 19, 32: 22, 40: 26, 50: 31, 63: 37.5, 110: 61}   # Muffentiefe (EN 1452-3, gerundet)
DN = {20: "DN15", 25: "DN20", 32: "DN25", 40: "DN32", 50: "DN40", 63: "DN50", 110: "DN100"}
HOSE = {16: "hellblau", 25: "dunkelblau"}               # Schlauch-Innendurchmesser -> Standardfarbe (hydraulics.md 5: Frischwasser hellblau, Filterlinie dunkelblau)
COL = {"pvc": "#8d9296", "hellblau": "#7fc4ea", "dunkelblau": "#2a5da8", "stahl": "#aeb4b8", "hahn": "#2a5da8"}

def wall_p(d): return max(1.8, round(d / 21.0, 1))        # PVC-U SDR 21 (entspricht PN12,5)
def wall_f(d): return 3 + d / 40.0                         # Muffenwand Formstueck
def od_f(d): return d + 2 * wall_f(d)

def setup(b, name, d, extra=None):
    b.add("parameters.add", name="d", expression=f"{d} mm")
    b.add("parameters.add", name="wall", expression=f"{wall_p(d)} mm")
    b.add("parameters.add", name="depth", expression=f"{DEPTH[d]} mm")
    for k, v in (extra or {}).items():
        b.add("parameters.add", name=k, expression=f"{v} mm")
    for m, c in COL.items():
        b.add("material.create", name=f"LT {m}", density_g_cm3={"pvc": 1.4, "hellblau": 1.0, "dunkelblau": 1.0, "stahl": 7.85, "hahn": 1.4}[m], color=c)
    b.add("component.create", name=name, grounded=True)

def meta(b, name, pn, desc):
    b.add("component.activate", component=name)
    b.add("component.metadata.set", component=name, part_number=pn, description=desc, revision="A", properties={"Werkstoff": "PVC-U / PE nach Funktion"})

def rohr(d, L=1000):
    b = sc.Build(); nm = f"T70_Rohr_d{d}"
    setup(b, nm, d, {"laenge": L})
    b.add("solid.cylinder", diameter=d, height=L, base=[0, 0, 0], operation="new", name="Rohr_R", body_name="Rohr")
    b.add("solid.cylinder", diameter=d - 2 * wall_p(d), height=L + 2, base=[0, 0, -1], operation="cut", targets=["Rohr"], name="Bohrung")
    b.add("material.assign", bodies=["Rohr"], material="LT pvc")
    meta(b, nm, f"T70-ROHR-{d}", f"Rohr PVC-U d{d} x {wall_p(d)} ({DN[d]}), Laenge {L}")
    return b, nm

def kupplung(d):
    L = 2 * DEPTH[d] + 6
    b = sc.Build(); nm = f"T70_Kupplung_d{d}"
    setup(b, nm, d, {"laenge": L})
    b.add("solid.cylinder", diameter=od_f(d), height=L, base=[0, 0, 0], operation="new", name="Muffe_R", body_name="Kupplung")
    b.add("solid.cylinder", diameter=d, height=DEPTH[d] + 1, base=[0, 0, -1], operation="cut", targets=["Kupplung"], name="Muffe_A")
    b.add("solid.cylinder", diameter=d, height=DEPTH[d] + 1, base=[0, 0, L - DEPTH[d]], operation="cut", targets=["Kupplung"], name="Muffe_B")
    b.add("solid.cylinder", diameter=d - 2 * wall_p(d), height=L + 2, base=[0, 0, -1], operation="cut", targets=["Kupplung"], name="Durchgang")
    b.add("material.assign", bodies=["Kupplung"], material="LT pvc")
    meta(b, nm, f"T70-KUP-{d}", f"Kupplung (Doppelmuffe) PVC-U d{d}, Klebemuffen")
    return b, nm

def bend(b, body, od, idd, leg, R, ang, mat, base_z=0.0):
    """Rohrbogen: gerader Schenkel (leg) + Kreisbogen (R) + gerader Schenkel; Aussen od, Innen idd; Port A bei (0,0,0) nach -Z. Rueckgabe: Endpunkt und Richtung von Port B."""
    t = math.radians(ang)
    b.add("solid.cylinder", diameter=od, height=leg, base=[0, 0, 0], operation="new", name=body + "_L1", body_name=body)
    b.add("sketch.create", plane={"origin": [0, 0, leg], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_Bogen")
    b.add("sketch.circle.center", center=[0, 0], radius=od / 2)
    b.add("sketch.finish")
    b.add("solid.revolve", axis={"origin": [R, 0, leg], "dir": [0, 1, 0]}, angle=f"{ang} deg", operation="join", targets=[body], name=body + "_Bogen")
    ex, ez = R - R * math.cos(t), leg + R * math.sin(t)
    dx, dz = math.sin(t), math.cos(t)
    b.add("solid.extrude", face=[round(ex, 4), 0, round(ez, 4)], face_body=body, distance=leg, operation="join", targets=[body], name=body + "_L2")      # zweiter Schenkel: Endflaeche des Bogens verlaengert (kein Boolean an schraegen Flaechen)
    # Bohrung als Werkzeugkoerper (Schenkel + Bogen + Schenkel vereinigt), dann solid.combine cut (Revolve-Cut direkt scheitert an deckungsgleichen Stirnflaechen)
    tool = body + "_Werkzeug"
    b.add("solid.cylinder", diameter=idd, height=leg + 1, base=[0, 0, -1], operation="new", name=tool + "_1", body_name=tool)
    b.add("sketch.create", plane={"origin": [0, 0, leg], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_BogenBohr")
    b.add("sketch.circle.center", center=[0, 0], radius=idd / 2)
    b.add("sketch.finish")
    b.add("solid.revolve", axis={"origin": [R, 0, leg], "dir": [0, 1, 0]}, angle=f"{ang} deg", operation="join", targets=[tool], name=tool + "_Bogen")
    b.add("solid.extrude", face=[round(ex, 4), 0, round(ez, 4)], face_body=tool, distance=leg + 2, operation="join", targets=[tool], name=tool + "_2")
    b.add("solid.combine", target=body, tools=[tool], operation="cut")
    b.add("material.assign", bodies=[body], material=mat)
    return (ex + dx * leg, 0, ez + dz * leg), (dx, 0, dz)

def bogen(d, ang):
    b = sc.Build(); nm = f"T70_Bogen{ang}_d{d}"
    R = max(od_f(d), 1.2 * d)
    setup(b, nm, d, {"radius": round(R, 1)})
    end, dr = bend(b, "Bogen", od_f(d), d, DEPTH[d], R, ang, "LT pvc")
    meta(b, nm, f"T70-B{ang}-{d}", f"Bogen {ang} Grad PVC-U d{d}, Klebemuffen, Radius {R:.0f}")
    return b, nm, dict(end=end, dir=dr, R=R)

def t_stueck(d):
    a = DEPTH[d] + od_f(d) / 2
    b = sc.Build(); nm = f"T70_T_d{d}"
    setup(b, nm, d, {"arm": round(a, 1)})
    of = od_f(d)
    b.add("solid.cylinder", diameter=of, height=2 * a, base=[-a, 0, 0], axis=[1, 0, 0], operation="new", name="Lauf_R", body_name="T_Stueck")
    b.add("solid.cylinder", diameter=of, height=a, base=[0, 0, 0], axis=[0, 0, 1], operation="join", targets=["T_Stueck"], name="Abgang_R")
    b.add("solid.cylinder", diameter=d, height=DEPTH[d] + 1, base=[-a - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["T_Stueck"], name="Muffe_L")
    b.add("solid.cylinder", diameter=d, height=DEPTH[d] + 1, base=[a - DEPTH[d], 0, 0], axis=[1, 0, 0], operation="cut", targets=["T_Stueck"], name="Muffe_R")
    b.add("solid.cylinder", diameter=d, height=DEPTH[d] + 1, base=[0, 0, a - DEPTH[d]], axis=[0, 0, 1], operation="cut", targets=["T_Stueck"], name="Muffe_Z")
    b.add("solid.cylinder", diameter=d - 2 * wall_p(d), height=2 * a + 2, base=[-a - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["T_Stueck"], name="Durchgang_X")
    b.add("solid.cylinder", diameter=d - 2 * wall_p(d), height=a + 1, base=[0, 0, 0], axis=[0, 0, 1], operation="cut", targets=["T_Stueck"], name="Durchgang_Z")
    b.add("material.assign", bodies=["T_Stueck"], material="LT pvc")
    meta(b, nm, f"T70-T-{d}", f"T-Stueck PVC-U d{d}, drei Klebemuffen")
    return b, nm, dict(a=a)

def kugelhahn(d):
    of = od_f(d)
    ob = of + 12
    Lb = 50
    L = Lb + 2 * DEPTH[d]
    b = sc.Build(); nm = f"T70_Kugelhahn_d{d}"
    setup(b, nm, d, {"laenge": round(L, 1)})
    b.add("solid.cylinder", diameter=ob, height=Lb, base=[0, 0, DEPTH[d]], operation="new", name="Gehaeuse_R", body_name="Kugelhahn")
    for z0, nmn in ((0, "A"), (DEPTH[d] + Lb, "B")):
        b.add("solid.cylinder", diameter=of, height=DEPTH[d], base=[0, 0, z0], operation="join", targets=["Kugelhahn"], name="Stutzen_" + nmn)
    b.add("solid.cylinder", diameter=d, height=DEPTH[d] + 1, base=[0, 0, -1], operation="cut", targets=["Kugelhahn"], name="Muffe_A")
    b.add("solid.cylinder", diameter=d, height=DEPTH[d] + 1, base=[0, 0, L - DEPTH[d]], operation="cut", targets=["Kugelhahn"], name="Muffe_B")
    b.add("solid.cylinder", diameter=d - 2 * wall_p(d), height=L + 2, base=[0, 0, -1], operation="cut", targets=["Kugelhahn"], name="Durchgang")
    b.add("material.assign", bodies=["Kugelhahn"], material="LT hahn")
    # Spindel und Hebel (Stellung offen: Hebel parallel zur Rohrachse)
    b.add("component.activate", component=nm)
    b.add("component.create", name="T70a_Hebel")
    zc = DEPTH[d] + Lb / 2
    b.add("solid.cylinder", diameter=14, height=ob / 2 + 30, base=[0, 0, zc], axis=[1, 0, 0], operation="new", name="Spindel_R", body_name="Spindel")      # 3 mm Einschub in den Hebel (Schweissverbindung)
    b.add("solid.box", length=14, width=max(8, d / 5), height=110, center=[ob / 2 + 34, 0, zc], operation="new", name="Hebel_R", body_name="Hebel")
    b.add("material.assign", bodies=["Spindel", "Hebel"], material="LT hahn")
    meta(b, nm, f"T70-KH-{d}", f"Kugelhahn PVC-U d{d}, Klebemuffen, Hebel +X (offen = parallel zur Rohrachse)")
    return b, nm, dict(L=L)

REDUCERS = [(110, 63), (63, 50), (50, 40), (50, 32), (40, 32), (32, 25), (25, 20)]

def reduzierung(dg, dk):
    """Reduziermuffe: grosse Muffe d_g an Port A, kleine Muffe d_k an Port B; Aussen-D = Formstueck der grossen Seite."""
    L = DEPTH[dg] + DEPTH[dk] + 6
    b = sc.Build(); nm = f"T70_Reduzierung_d{dg}_d{dk}"
    setup(b, nm, dg, {"laenge": L, "d_klein": dk})
    b.add("solid.cylinder", diameter=od_f(dg), height=L, base=[0, 0, 0], operation="new", name="Red_R", body_name="Reduzierung")
    b.add("solid.cylinder", diameter=dg, height=DEPTH[dg] + 1, base=[0, 0, -1], operation="cut", targets=["Reduzierung"], name="Muffe_gross")
    b.add("solid.cylinder", diameter=dk, height=DEPTH[dk] + 1, base=[0, 0, L - DEPTH[dk]], operation="cut", targets=["Reduzierung"], name="Muffe_klein")
    b.add("solid.cylinder", diameter=dk - 2 * wall_p(dk), height=L + 2, base=[0, 0, -1], operation="cut", targets=["Reduzierung"], name="Durchgang")
    b.add("material.assign", bodies=["Reduzierung"], material="LT pvc")
    meta(b, nm, f"T70-RED-{dg}-{dk}", f"Reduziermuffe PVC-U d{dg} auf d{dk}, Klebemuffen")
    return b, nm, dict(L=L)

def ports(fname, L_rohr=1000):
    """Ports eines Teils (Lage im Bauteil-KS, Richtung der Oeffnung, Art 'Muffe' = Rohr wird eingesteckt, 'Zapfen' = Rohr-/Schlauchende, Lage auf der Oeffnungsebene): [(name, (x,y,z), (dx,dy,dz), art, dn)]."""
    import re
    m = re.match(r"lt_(rohr|kupplung|bogen90|bogen45|t|kugelhahn|klemme)_d(\d+)$", fname)
    if m:
        t, d = m.group(1), int(m.group(2))
        dp, of = DEPTH[d], od_f(d)
        if t == "rohr":
            return [("A", (0, 0, 0), (0, 0, -1), "Zapfen", DN[d]), ("B", (0, 0, L_rohr), (0, 0, 1), "Zapfen", DN[d])]
        if t == "kupplung":
            Lk = 2 * dp + 6
            return [("A", (0, 0, 0), (0, 0, -1), "Muffe", DN[d]), ("B", (0, 0, Lk), (0, 0, 1), "Muffe", DN[d])]
        if t in ("bogen90", "bogen45"):
            ang = 90 if t == "bogen90" else 45
            R = max(of, 1.2 * d); r = math.radians(ang)
            ex, ez = R - R * math.cos(r), dp + R * math.sin(r)
            dx, dz = math.sin(r), math.cos(r)
            return [("A", (0, 0, 0), (0, 0, -1), "Muffe", DN[d]), ("B", (ex + dx * dp, 0, ez + dz * dp), (dx, 0, dz), "Muffe", DN[d])]
        if t == "t":
            a = dp + of / 2
            return [("A", (-a, 0, 0), (-1, 0, 0), "Muffe", DN[d]), ("B", (a, 0, 0), (1, 0, 0), "Muffe", DN[d]), ("C", (0, 0, a), (0, 0, 1), "Muffe", DN[d])]
        if t == "kugelhahn":
            Lh = 50 + 2 * dp
            return [("A", (0, 0, 0), (0, 0, -1), "Muffe", DN[d]), ("B", (0, 0, Lh), (0, 0, 1), "Muffe", DN[d])]
        return [("Rohrachse", (0, 0, 4 + (d + 6) / 2), (1, 0, 0), "Aufnahme", DN[d])]
    m = re.match(r"lt_reduzierung_d(\d+)_d(\d+)$", fname)
    if m:
        dg, dk = int(m.group(1)), int(m.group(2))
        return [("A (gross)", (0, 0, 0), (0, 0, -1), "Muffe", DN[dg]), ("B (klein)", (0, 0, DEPTH[dg] + DEPTH[dk] + 6), (0, 0, 1), "Muffe", DN[dk])]
    m = re.match(r"lt_schlauch_id(\d+)$", fname)
    if m:
        return [("A", (0, 0, 0), (0, 0, -1), "Schlauchende", "ID" + m.group(1)), ("B", (0, 0, L_rohr), (0, 0, 1), "Schlauchende", "ID" + m.group(1))]
    m = re.match(r"lt_schlauchbogen90_id(\d+)$", fname)
    if m:
        idd = int(m.group(1)); ad = idd + 4; R = 5 * ad
        return [("A", (0, 0, 0), (0, 0, -1), "Schlauchende", f"ID{idd}"), ("B", (R + 100, 0, 100 + R), (1, 0, 0), "Schlauchende", f"ID{idd}")]
    m = re.match(r"lt_verteiler_d32_n(\d+)$", fname)
    if m:
        n = int(m.group(1)); Lv = n * 120 + 120
        out = [("A", (0, 0, 0), (-1, 0, 0), "Zapfen", DN[32]), ("B", (Lv, 0, 0), (1, 0, 0), "Zapfen", DN[32])]
        out += [(f"Abgang {k}", (60 + 60 + 120 * (k - 1), 0, 66.0), (0, 0, 1), "Zapfen", DN[25]) for k in range(1, n + 1)]
        return out
    return []

def schlauch(idd, L=1000):
    wh = 2.0
    ad = idd + 2 * wh
    b = sc.Build(); nm = f"T70_Schlauch_ID{idd}"
    b.add("parameters.add", name="id", expression=f"{idd} mm"); b.add("parameters.add", name="wand", expression=f"{wh} mm"); b.add("parameters.add", name="laenge", expression=f"{L} mm")
    for m, c in COL.items():
        b.add("material.create", name=f"LT {m}", density_g_cm3=1.0, color=c)
    b.add("component.create", name=nm, grounded=True)
    b.add("solid.cylinder", diameter=ad, height=L, base=[0, 0, 0], operation="new", name="S_R", body_name="Schlauch")
    b.add("solid.cylinder", diameter=idd, height=L + 2, base=[0, 0, -1], operation="cut", targets=["Schlauch"], name="Bohrung")
    b.add("material.assign", bodies=["Schlauch"], material="LT " + HOSE[idd])
    meta(b, nm, f"T70-SCH-{idd}", f"Schlauch ID{idd} / AD{ad:.0f}, Laenge {L}, Farbe {HOSE[idd]}")
    return b, nm, dict(ad=ad)

def schlauch_bogen(idd):
    wh = 2.0
    ad = idd + 2 * wh
    R = 5 * ad                                                   # Biegeradius >= 5 x Aussendurchmesser (hydraulics.md 5)
    b = sc.Build(); nm = f"T70_SchlauchBogen90_ID{idd}"
    b.add("parameters.add", name="id", expression=f"{idd} mm"); b.add("parameters.add", name="radius", expression=f"{R:.1f} mm")
    for m, c in COL.items():
        b.add("material.create", name=f"LT {m}", density_g_cm3=1.0, color=c)
    b.add("component.create", name=nm, grounded=True)
    end, dr = bend(b, "Schlauchbogen", ad, idd, 100, R, 90, "LT " + HOSE[idd])
    meta(b, nm, f"T70-SB-{idd}", f"Schlauchbogen 90 Grad ID{idd}, Biegeradius {R:.0f} (5 x AD), Schenkel 100")
    return b, nm, dict(end=end, dir=dr, R=R, ad=ad)

def klemme(d):
    t = 3.0
    ring_od = d + 2 * t
    plate = 4.0
    w = 20.0
    b = sc.Build(); nm = f"T70_Klemme_d{d}"
    setup(b, nm, d)
    zc = plate + ring_od / 2
    fw = ring_od + 36                                          # Fussbreite: Schrauben liegen ausserhalb des Rings
    b.add("solid.box", length=44, width=fw, height=plate, center=[0, 0, plate / 2], operation="new", name="Fuss_R", body_name="Klemmenfuss")
    b.add("solid.cylinder", diameter=ring_od, height=w, base=[-w / 2, 0, zc], axis=[1, 0, 0], operation="new", name="Ring_R", body_name="Klemmenring")
    b.add("solid.cylinder", diameter=d, height=w + 2, base=[-w / 2 - 1, 0, zc], axis=[1, 0, 0], operation="cut", targets=["Klemmenring"], name="Ring_Bohrung")
    b.add("material.assign", bodies=["Klemmenfuss", "Klemmenring"], material="LT stahl")
    for sy in (-1, 1):
        b.add("parts.insert", family="hex_bolt", size="M6", length=20, point=[0, sy * (ring_od / 2 + 12), plate], direction=[0, 0, 1], name=f"Schraube_{sy}")
    meta(b, nm, f"T70-KL-{d}", f"Rohrklemme/Halter fuer Rohr d{d}, Fuss 44 x {ring_od + 36:.0f}, Ring B20, 2 Schrauben M6x20")
    return b, nm, dict(zc=zc)

def verteiler(d, n, ds=25, pitch=120):
    of = od_f(d)
    L = n * pitch + 2 * 60
    b = sc.Build(); nm = f"T70_Verteiler_d{d}_n{n}"
    setup(b, nm, d, {"laenge": L, "anzahl_abgaenge": n})
    b.add("solid.cylinder", diameter=d, height=L, base=[0, 0, 0], axis=[1, 0, 0], operation="new", name="Sammler_R", body_name="Verteiler")
    xs = [60 + pitch / 2 + k * pitch for k in range(n)]
    for k, x in enumerate(xs, 1):
        b.add("solid.cylinder", diameter=ds, height=d / 2 + 50, base=[x, 0, 0], axis=[0, 0, 1], operation="join", targets=["Verteiler"], name=f"Abgang_{k}")
    b.add("solid.cylinder", diameter=d - 2 * wall_p(d), height=L + 2, base=[-1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Verteiler"], name="Sammlerbohrung")
    for k, x in enumerate(xs, 1):
        b.add("solid.cylinder", diameter=ds - 2 * wall_p(ds), height=d / 2 + 52, base=[x, 0, 0], axis=[0, 0, 1], operation="cut", targets=["Verteiler"], name=f"Abgangsbohrung_{k}")
    b.add("material.assign", bodies=["Verteiler"], material="LT pvc")
    meta(b, nm, f"T70-V-{d}-{n}", f"Verteiler d{d} mit {n} Abgaengen d{ds}, Teilung {pitch}")
    return b, nm, dict(L=L, xs=xs, ds=ds, top=d / 2 + 50)

def save(b, name, fname):
    out = os.path.join(sc.ROOT, "designs", "components", fname + ".sc")
    sc.run(b.write(fname), out)
    return out

if __name__ == "__main__":
    want = set(a for a in sys.argv[1:] if not a.startswith("--"))
    info = {}
    def do(key, fname, res):
        if want and key not in want:
            return
        b, nm = res[0], res[1]
        save(b, nm, fname)
        info[fname] = res[2] if len(res) > 2 else {}
        print(fname)
    for d in SIZES:
        do("rohr", f"lt_rohr_d{d}", rohr(d))
        do("kupplung", f"lt_kupplung_d{d}", kupplung(d))
        do("bogen", f"lt_bogen90_d{d}", bogen(d, 90))
        do("bogen", f"lt_bogen45_d{d}", bogen(d, 45))
        do("t", f"lt_t_d{d}", t_stueck(d))
        do("kugelhahn", f"lt_kugelhahn_d{d}", kugelhahn(d))
        do("klemme", f"lt_klemme_d{d}", klemme(d))
    for dg, dk in REDUCERS:
        do("reduzierung", f"lt_reduzierung_d{dg}_d{dk}", reduzierung(dg, dk))
    for idd in (16, 25):
        do("schlauch", f"lt_schlauch_id{idd}", schlauch(idd))
        do("schlauch", f"lt_schlauchbogen90_id{idd}", schlauch_bogen(idd))
    for n in (2, 3, 4):
        do("verteiler", f"lt_verteiler_d32_n{n}", verteiler(32, n))
    json.dump(info, open(os.path.join(sc.TMP, "lt-info.json"), "w"), default=str)
