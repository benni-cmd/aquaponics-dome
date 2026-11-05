"""Pruefung N-VERBINDER Montage (D91): Scherenknoten und Rundrohr-Streben im Gesamtmodell.

Prueft (unabhaengig vom Bau nachrechenbar):
  1. Befehlsskript der Variante: 26 Plattenpaare, Arme A/B und Streben A/B in der erwarteten Zahl, kein Kugelknoten knoten_<n>_nNN.sc mehr.
  2. Nase im Gegenloch: je Strebenende Lage der Nasen (Arm-Instanz) gegen die Gegenloecher (Streben-Instanz); die Nase 10 x link_t
     passt, wenn ihre Ecke im Loch liegt: sqrt((5 + |axial|)^2 + (t/2 + |quer|)^2) <= wall_hole/2.
  3. Folie auf der Strebe: groesster Abstand von Knoten-Hardware (Bounding-Box-Ecken Plattenpaar und Arm) und Rohr-Oberkante ueber der
     Feldebene (drei Knotenpunkte) muss unter foil_z0 liegen (Folie liegt auf Schaumband + Keilschiene).
  4. Durchdringung: Probe-Szenen (Plattenpaar + Arme + volle Streben) an einem 4-, 5- und 6-wertigen Knoten, inspect.interference;
     erlaubt sind nur Gewinde Schraube/Mutter und Flaechenkontakt Lasche 1/2 im eigenen Arm (< 0,2 mm Facetten).
Aufruf: python -X utf8 scripts/check_verbinder_montage.py [--variante a_plus|ring_b2] [--ohne-probe]   (Exit 1 bei FAIL)"""
import json, math, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "workshop"))
import variante, knoten_montage as KM, knoten_schere as KS, sc

V = variante.aktiv()
P = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}
ROT = P["door_az"] - 167
FP = {k: v["wert"] for k, v in json.load(open(os.path.join(ROOT, "data", "components", "huelle_folie.json"), encoding="utf-8"))["parameter"].items()}
TMP = os.environ.get("WORKSHOP_TMP", tempfile.gettempdir())
res = []


def chk(name, ist, soll, ok):
    res.append(ok)
    print(("PASS " if ok else "FAIL ") + f"{name}: Ist {ist}, Soll {soll}")


def apply(m, p):
    return [m[0] * p[0] + m[1] * p[1] + m[2] * p[2] + m[3], m[4] * p[0] + m[5] * p[1] + m[6] * p[2] + m[7], m[8] * p[0] + m[9] * p[1] + m[10] * p[2] + m[11]]


def col(m, j):
    return [m[j], m[4 + j], m[8 + j]]


segs = json.load(open(os.path.join(HERE, ".segs.json")))
platten, arme, streben, K = KM.montage(segs, ROT)
LEN = KM.rohrlaengen(segs, ROT)
base_z = min(min(A[2], B[2]) for A, B in segs)
center = [0.0, 0.0, base_z]

# 1. Befehlsskript
cmds = json.load(open(variante.pfad("dome_script", V, root=ROOT), encoding="utf-8"))["commands"]
moves = {}
for c in cmds:
    if c["command"] == "occurrence.move" and "matrix" in c["params"]:
        cls = c["params"]["occurrence"].split(":")[0]
        moves.setdefault(cls, []).append(c["params"]["matrix"])
paths = [c["params"]["path"] for c in cmds if c["command"] == "component.insert_design"]
soll = {"Knoten_Platte": 26, "Schere_A": len(arme["A"]), "Schere_B": len(arme["B"]), "Strebe_A": 30, "Strebe_B": 34}
for cls, n in soll.items():
    chk(f"{V}: Instanzen {cls}", len(moves.get(cls, [])), n, len(moves.get(cls, [])) == n)
chk(f"{V}: Arme gesamt = 2 x Streben", len(arme["A"]) + len(arme["B"]), 2 * len(segs), len(arme["A"]) + len(arme["B"]) == 2 * len(segs))
alt = [p for p in paths if re.search(r"knoten_\d_n\d\d\.sc$", p)]
chk(f"{V}: Kugelknoten knoten_<n>_nNN.sc im Skript", len(alt), 0, not alt)

# 2. Nase im Gegenloch (aus den Matrizen des Skripts, nicht aus dem Generator)
t, hole, s_hole = KS.P["link_t"], KS.P["wall_hole"], KS.P["b_pivot_to_nose"] - KS.P["pivot_out"]
holes_w = []   # (mitte, achse) aller Gegenloecher der Streben-Instanzen
for typ in "AB":
    L = LEN[typ][0]
    for m in moves.get(f"Strebe_{typ}", []):
        for z, x, sy in ((s_hole, -t / 2, 1), (s_hole, t / 2, -1), (L - s_hole, -t / 2, -1), (L - s_hole, t / 2, 1)):
            r = KS.P["tube_d"] / 2 - KS.P["tube_t"] / 2
            holes_w.append((apply(m, [x, sy * r, z]), [sy * q for q in col(m, 1)], col(m, 2)))
worst, worst_at, n_nose = -1e9, None, 0
for typ in "AB":
    g = KS.Geo(typ)
    for m in moves.get(f"Schere_{typ}", []):
        for k, side in ((1, -1), (2, 1)):
            nose = apply(m, g.pt(g.s_nose, -t / 2 if k == 1 else t / 2, side * (KS.P["tube_d"] / 2 - KS.P["tube_t"] / 2)))
            c, ax, u = min(holes_w, key=lambda h: math.dist(h[0], nose))
            d = [nose[i] - c[i] for i in range(3)]
            a = abs(sum(d[i] * u[i] for i in range(3)))                  # axial
            dq = [d[i] - sum(d[j] * u[j] for j in range(3)) * u[i] for i in range(3)]
            b = math.sqrt(max(0.0, sum(q * q for q in dq) - sum(dq[i] * ax[i] for i in range(3)) ** 2))   # quer (ohne Lochachse)
            corner = math.hypot(KS.P["nose_w"] / 2 + a, t / 2 + b)
            n_nose += 1
            if corner - hole / 2 > worst:
                worst, worst_at = corner - hole / 2, (typ, round(a, 2), round(b, 2))
chk(f"{V}: Nasen geprueft (2 je Arm)", n_nose, 2 * (len(arme["A"]) + len(arme["B"])), n_nose == 2 * (len(arme["A"]) + len(arme["B"])))
chk(f"{V}: Nasenecke im Gegenloch D{hole:g}, groesster Ueberstand ueber den Lochrand mm (Typ, axial, quer)", f"{worst:+.2f} {worst_at}", "<= 0", worst <= 0)

# 3. Folie auf der Strebe: Hardware und Rohr unter der inneren Folienlage
bb = {}
for nm, f in (("platte", "knoten_schere_platte"), ("A", "knoten_schere_arm_a_montage"), ("B", "knoten_schere_arm_b_montage")):
    ev = sc.evaluate(os.path.join(ROOT, "designs", "components", f + ".sc"))
    bb[nm] = []   # Ecken der Bounding-Box JE KOERPER (die Box ueber alle Teile eines Arms ist wegen des Knicks 25 mm zu hoch)
    for body in ev["bodies"]:
        lo, hi = body["bbox"]["min"], body["bbox"]["max"]
        bb[nm] += [[(lo, hi)[a][0], (lo, hi)[b][1], (lo, hi)[c][2]] for a in (0, 1) for b in (0, 1) for c in (0, 1)]
node_pts = {k: o for k, (o, _, _) in K.items()}
edges = {frozenset(s["knoten"]) for s in streben}
tris = set()
for e in edges:
    a, b = tuple(e)
    for c in node_pts:
        if c not in e and frozenset((a, c)) in edges and frozenset((b, c)) in edges:
            tris.add(frozenset((a, b, c)))
hw = {k: [] for k in node_pts}
for k, m in platten:
    hw[k] += [apply(m, p) for p in bb["platte"]]
for typ in "AB":
    for k, nb, m in arme[typ]:
        hw[k] += [apply(m, p) for p in bb[typ]]
top = -1e9; top_at = None
for tri in tris:
    A, B, C = (node_pts[k] for k in tri)
    n = KM.cross(KM.sub(B, A), KM.sub(C, A)); n = KM.unit(n)
    cen = [(A[i] + B[i] + C[i]) / 3 - center[i] for i in range(3)]
    if KM.dot(n, cen) < 0:
        n = [-q for q in n]
    for k in tri:
        for p in hw[k]:
            h = KM.dot(KM.sub(p, A), n)
            if h > top: top, top_at = h, f"Knoten-Hardware {k} (Koerper-Box-Ecke)"
    for s in streben:
        if set(s["knoten"]) <= set(tri):
            for p in (s["start"], [s["start"][i] + s["u"][i] * s["laenge"] for i in range(3)]):
                h = KM.dot(KM.sub(p, A), n) + KS.P["tube_d"] / 2
                if h > top: top, top_at = h, f"Rohr-Oberkante {s['knoten']}"
chk(f"{V}: Dreiecksfelder aus den Streben", len(tris), 40 if len(segs) == 65 else "39-40", len(tris) in (39, 40))
chk(f"{V}: hoechster Punkt (Hardware, Rohr) ueber der Feldebene mm, innere Folie bei foil_z0 {FP['foil_z0']:g} ({top_at})", round(top, 1), f"< {FP['foil_z0']:g}", top < FP["foil_z0"])

# 4. Probe-Szenen mit Durchdringung
NORM = {"Platte_Schraube", "Platte_Mutter", "Platte_ScheibeO", "Platte_ScheibeU", "Dreh_Schraube", "Dreh_Mutter", "Dreh_ScheibeO", "Dreh_ScheibeU"}


def probe(knoten):
    b = [{"command": "component.create", "params": {"name": f"Probe_{knoten}"}}]
    def ins(cls, f, mats):
        b.append({"command": "component.insert_design", "params": {"path": os.path.join(ROOT, "designs", "components", f).replace("\\", "/"), "name": cls}})
        for _ in range(len(mats) - 1):
            b.append({"command": "occurrence.copy", "params": {"component": cls}})
        for i, mt in enumerate(mats, 1):
            b.append({"command": "occurrence.move", "params": {"occurrence": f"{cls}:{i}", "matrix": mt, "tolerance": 1e-6, "move_grounded": True}})
    ins("Platte", "knoten_schere_platte.sc", [m for k, m in platten if k == knoten])
    for typ in "AB":
        ms = [m for k, nb, m in arme[typ] if k == knoten]
        if ms:
            ins(f"Arm_{typ}", f"knoten_schere_arm_{typ.lower()}_montage.sc", ms)
        sm = [KM.strebe_matrix(s, center, LEN[typ][0])[0] for s in streben if s["typ"] == typ and knoten in s["knoten"]]
        if sm:
            ins(f"Strebe_{typ}", f"strebe_{typ.lower()}.sc", sm)
    script = os.path.join(TMP, f"vm-probe-{knoten}.json"); out = os.path.join(TMP, f"vm-probe-{knoten}.sc")
    json.dump({"commands": b}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--save", out, "--quiet"], capture_output=True, text=True)
    if r.returncode:
        sys.exit("FEHLER Probe: " + (r.stderr + r.stdout)[-400:])
    s2 = os.path.join(TMP, "vm-int.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 240}}]}, open(s2, "w"))
    r = subprocess.run([sc.CLI, "run", s2, "--in", out, "--results"], capture_output=True, text=True)
    d = json.loads(r.stdout)[0]
    inst = lambda nm: (re.search(r"\((\d+)\)$", nm) or [None, "1"])[1]
    base = lambda nm: nm.split(" (")[0]
    bad, ok = [], 0
    for p in d.get("interferences", []):
        a, c, vol = p["a"], p["b"], p.get("volume_mm3", 0) or 0
        same = inst(a) == inst(c) and base(a)[:5] != "T1_St" and base(c)[:5] != "T1_St"
        if vol <= 0.1 or (same and (base(a) in NORM or base(c) in NORM)):
            ok += 1; continue
        bad.append((a, c, round(vol, 3)))
    unch = [u for u in d.get("unchecked", []) if not ({base(u["a"]), base(u["b"])} == {"Lasche_1", "Lasche_2"} and inst(u["a"]) == inst(u["b"])
            and float((re.search(r"by more than ([0-9.eE+-]+) mm", u.get("reason", "")) or [0, "9"])[1]) < 0.2)]
    for x in bad[:8]:
        print("   Durchdringung:", x)
    for u in unch[:4]:
        print("   ungeprueft:", u["a"], u["b"], u.get("reason", "")[:90])
    chk(f"{V}: Probe {knoten} ({K[knoten][2]['wertigkeit']}-wertig, Platte + Arme + Streben): Durchdringungen > 0,1 mm3 / ungeprueft", f"{len(bad)} / {len(unch)}", "0 / 0", not bad and not unch)


if "--ohne-probe" not in sys.argv:
    four = min((k for k in K if K[k][2]["wertigkeit"] == 4), key=lambda k: K[k][0][2])
    for kn in ("n02", "n01", four):
        probe(kn)
print(f"== check_verbinder_montage {V}: {sum(res)}/{len(res)} PASS")
sys.exit(0 if all(res) else 1)
