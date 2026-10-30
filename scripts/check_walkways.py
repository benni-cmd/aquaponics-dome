"""Laufwege, Radialbudget und Bodenauslastung (M7, D28/D29): reine Geometrie aus scripts/dome-script.json (Instanzmatrizen) und data/layout.json, kein CAD-Lauf.
Aufruf: python scripts/check_walkways.py   (Exit 0 = alles PASS)
Portal = Beet-Rechteck + je 115 mm Breite (Beine/Fussplatten ausserhalb des Beets, D18); Mass in mm im Modellrahmen.
Laufweg A = Beckenrand (Aussenradius 2095) zu Innenportal, B = Innenportal zu Aussenportal, Wandluft = Aussenportal zur Fundamentring-Innenflaeche (Zehneck, Apothem 5706).
Tuer-Gang: kleinster Abstand der Beet-/Becken-Hindernisse beiderseits des Tuerkorridors (Tuer -> Mitte), Breite = 2 x kleinster Abstand zur Korridorachse im Bereich Tuer bis Zentralpool."""
import json, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
P = {c["params"]["name"]: float(c["params"]["expression"]) for c in cmds if c["command"] == "parameters.add"}
LAY = json.load(open(os.path.join(ROOT, "data", "layout.json")))
mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
PORTAL = 115.0
vdim = {"Beet_aussen_800": (2640, 800, True)}   # Aussenbeet W17/D29
for b in LAY["ibc_beds"]:
    if "plants" not in b: vdim.setdefault("Beet_innen_933", (b["length"], b["width"], False))

def rect(m, l, w):
    c, s = m[0], m[4]; return [(m[3] + u * c - v * s, m[7] + u * s + v * c) for u, v in ((-l / 2, -w / 2), (l / 2, -w / 2), (l / 2, w / 2), (-l / 2, w / 2))]
def seg_pt(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
def inside(p, R):
    s = [(R[(i + 1) % 4][0] - R[i][0]) * (p[1] - R[i][1]) - (R[(i + 1) % 4][1] - R[i][1]) * (p[0] - R[i][0]) for i in range(4)]
    return all(x >= 0 for x in s) or all(x <= 0 for x in s)
def dist(A, B):
    """Abstand zweier Rechtecke (0 bei Ueberlappung)."""
    if any(inside(p, B) for p in A) or any(inside(p, A) for p in B): return 0.0
    return min(seg_pt(p, Q[i], Q[(i + 1) % 4]) for P_, Q in ((A, B), (B, A)) for p in P_ for i in range(4))
def circ(R, cx, cy, r):
    return (0.0 if inside((cx, cy), R) else min(seg_pt((cx, cy), R[i], R[(i + 1) % 4]) for i in range(4))) - r

inner, outer, beds = [], [], []
for k, m in mv.items():
    cls = k.split(":")[0]
    if cls in vdim:
        l, w, out = vdim[cls]; (outer if out else inner).append(rect(m, l, w + 2 * PORTAL)); beds.append(rect(m, l, w))
# Zentralpool/Zweitbecken aus layout.json (Position wie gen_dome: um ROT gedreht; Zweitbecken pool2_r_factor nach aussen)
ROT = math.radians(P["door_az"] - 167)
rot = lambda x, y: (x * math.cos(ROT) - y * math.sin(ROT), x * math.sin(ROT) + y * math.cos(ROT))
pc = (0.0, 0.0); pr = LAY["pool"]["d"] / 2 + P["wall"]   # D35: Zentralpool auf der Achse
p2 = rot(math.hypot(LAY["pool2"]["cx"], LAY["pool2"]["cy"]) * P["pool2_r_factor"] * math.cos(math.radians(149.2)), math.hypot(LAY["pool2"]["cx"], LAY["pool2"]["cy"]) * P["pool2_r_factor"] * math.sin(math.radians(149.2))); p2r = LAY["pool2"]["d"] / 2 + 60
res = []
def chk(name, ist, soll, ok): res.append(ok); print(("PASS" if ok else "FAIL"), name, "| Ist:", ist, "| Soll:", soll)
wmin = P["walkway_min"]
A = min(circ(R, pc[0], pc[1], pr) for R in inner)
B = min(dist(i, o) for i in inner for o in outer)
nrm = [(math.cos(math.radians(P["door_edge_az"] + 36 * k)), math.sin(math.radians(P["door_edge_az"] + 36 * k))) for k in range(10)]
wall = P["dome_base_d"] / 2 * math.cos(math.radians(18)) - max(p[0] * n[0] + p[1] * n[1] for R in outer for p in R for n in nrm)   # Eckpunkt gegen die Zehneck-Seite, die er am weitesten ueberschreitet
chk("Laufweg A Beckenrand - Innenportal [mm]", round(A), f">= {wmin:.0f} (nie < 500)", A >= 500)
chk("Laufweg B Innenportal - Aussenportal [mm]", round(B), f">= {wmin:.0f} (nie < 500)", B >= 500)
chk("Wandluft Aussenportal - Fundamentring-Innenflaeche [mm]", round(wall), ">= 0 (Ziel 218)", wall >= 0)
neighbors = min(dist(a, b) for i, a in enumerate(outer) for b in outer[i + 1:])
chk("Aussenbeete: Abstand Nachbarportale an den Ecken [mm] (W17: Beet ~2640 lang)", round(neighbors), ">= 0", neighbors >= 0)
# Tuer-Gang: Korridor Tuer -> Mitte entlang der Tuerachse, Hindernisse = Portale, Zweitbecken, Beete; Breite = 2 x kleinster Abstand zur Achse
a = math.radians(P["door_edge_az"]); d0 = (math.cos(a), math.sin(a)); ap = P["dome_base_d"] / 2 * math.cos(math.radians(18))
axis = ((ap * d0[0], ap * d0[1]), (pr * d0[0], pr * d0[1]))
dmin = 1e9
for R in inner + outer:   # Abstand Rechteckrand zur Achsstrecke (Eckpunkte reichen, sonst Rechteck schneidet die Achse)
    sides = [((R[i][0] - axis[0][0]) * (axis[1][1] - axis[0][1]) - (R[i][1] - axis[0][1]) * (axis[1][0] - axis[0][0])) for i in range(4)]
    if (min(sides) < 0 < max(sides)) and min(seg_pt(p, axis[0], axis[1]) for p in R) < 800: dmin = 0
    else: dmin = min(dmin, min(seg_pt(p, axis[0], axis[1]) for p in R))
gang = 2 * dmin
chk("Tuer-Gang Breite bis zum Zentralpool (Beete/Portale beiderseits der Tuerachse) [mm]", round(gang), ">= 900", gang >= 900)
# Bodenauslastung: Grundflaechen (Portale, Pool, Zweitbecken, Tanks) / Zehneckflaeche
dec = 10 * ap * ap * math.tan(math.radians(18))   # regelmaessiges Zehneck mit Apothem ap
area = sum(abs(sum(R[i][0] * R[(i + 1) % 4][1] - R[(i + 1) % 4][0] * R[i][1] for i in range(4))) / 2 for R in inner + outer) + math.pi * pr ** 2 + math.pi * p2r ** 2 \
       + sum(math.pi * (t["d"] / 2) ** 2 for t in LAY["tanks"])
print(f"BODENAUSLASTUNG {100 * area / dec:.0f} % der Zehneckflaeche ({dec / 1e6:.1f} m2): Portale {len(inner)} innen + {len(outer)} aussen, Pool, Zweitbecken, 4 Tanks")
print("RADIALBUDGET (Apothem): Rand", round(pr), "| A", round(A), "| B", round(B), "| Wandluft", round(wall))
sys.exit(0 if all(res) else 1)
