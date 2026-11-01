"""M10-PLAN: Paarsuche Feinfilter (T55): zwei Lagen, die streng (Luecke >= 500, Rueckseite >= 150) gelten UND untereinander >= 500 mm Abstand haben.
Aufruf: FEXCL=Tank_klein,Pumpe_klein python -X utf8 scripts/place_feinfilter_paar.py   (FEXCL leer = heutiges Modell; nur Lesen)
Ost-Filter bekommt die Ost-Pumpen (Pumpe_gross:1,2), West-Filter die West-Pumpen (3,4); Rohrmass = Luftlinie wie in place_feinfilter.py."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import place_feinfilter as F

def seg_d(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy))); return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
def rr(A, B):
    if any(F.inside_poly(p[0], p[1], B) for p in A) or any(F.inside_poly(p[0], p[1], A) for p in B): return 0.0
    return min(seg_d(p, Q[i], Q[(i + 1) % 4]) for X, Q in ((A, B), (B, A)) for p in X for i in range(4))

res = [r for r in F.search("X", -180, 180, True) if r[0]]   # (ok, min, back, x, y, yaw, az, r, sc)
print("streng erfuellte Lagen:", len(res), "FEXCL =", sorted(F.EXCL) or "leer")
best = {}
for line in ("Ost", "West"):
    best[line] = sorted(res, key=lambda r: sum(F.pipe_proxy(r[3], r[4], math.radians(r[5]), line)))[:400]
out = []
for a in best["Ost"]:
    for b in best["West"]:
        if math.hypot(a[3] - b[3], a[4] - b[4]) < 1180: continue
        if rr(F.rect(a[3], a[4], math.radians(a[5])), F.rect(b[3], b[4], math.radians(b[5]))) < 500: continue
        pa, pb = F.pipe_proxy(a[3], a[4], math.radians(a[5]), "Ost"), F.pipe_proxy(b[3], b[4], math.radians(b[5]), "West")
        out.append((sum(pa) + sum(pb), a, b, pa, pb))
out.sort(key=lambda t: t[0])
print("Paare mit Luecke >= 500 untereinander (aus je 400 besten Lagen je Linie):", len(out))
for tot, a, b, pa, pb in out[:4]:
    print(f"  Ost x{a[3]:.0f} y{a[4]:.0f} Dr {a[5]} (Luecke {a[1]:.0f}, Pool~{pa[0]:.0f} Pumpe~{pa[1]:.0f}) | West x{b[3]:.0f} y{b[4]:.0f} Dr {b[5]} (Luecke {b[1]:.0f}, Pool~{pb[0]:.0f} Pumpe~{pb[1]:.0f})")
