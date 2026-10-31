"""Massstabsbild W34: kleiner Puffer (T82), Menschenfigur 1,80 m (mensch_referenz.sc) und Drittbecken klein (T14k) nebeneinander, Vorderansicht; dazu die drei Standardansichten des Puffers.
Becken: Unterkante Z -405 (Wasserspiegel Z 515 im Modellrahmen = 920 im Bauteil), Rand Z 650.
Aufruf: python scripts/workshop/render_puffer_klein.py -> renders/components/puffer_klein/puffer_klein-0{1..4}-*.png"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

D = os.path.join(sc.ROOT, "designs", "components")
OUT = os.path.join(sc.ROOT, "renders", "components", "puffer_klein")
os.makedirs(OUT, exist_ok=True)
puf = os.path.join(D, "puffer_klein.sc")
for nme, yaw, pitch, kw in (("01-schraeg", 0.7, 0.35, {}), ("02-vorn", 0.0, 0.0, {}), ("03-schnitt", 1.5708, 0.0, {"section": "x=0"})):
    sc.snapshot(puf, os.path.join(OUT, f"puffer_klein-{nme}.png"), [0, 0, 600], yaw, pitch, 2600, w=1100, h=800, **kw)

items = [("puffer_klein.sc", "Puffer", 0, 0, 0), ("mensch_referenz.sc", "Figur", 900, -150, 0), ("becken_dritt_klein.sc", "Drittbecken", 1900, 0, -405)]
def base():
    b = sc.Build()
    for (f, nm, *_r) in items:
        b.add("component.insert_design", path=os.path.join(D, f).replace("\\", "/"), name=nm)
    return b
res = sc.run_results(base().write("pk-probe"))
occ = [r["occurrence"] for r in res if "occurrence" in r]
b = base()
for (f, nm, x, y, z), o in zip(items, occ):
    if x or y or z:
        b.add("occurrence.move", occurrence=o, translate=[x, y, z], space="world", move_grounded=True)
scene = os.path.join(sc.TMP, "puffer-massstab.sc")
sc.run(b.write("pk-massstab"), scene)
png = os.path.join(OUT, "puffer_klein-04-massstab.png")
sc.snapshot(scene, png, [950, 0, 700], 0.0, 0.0, 5200, w=1400, h=800)
print(png)
