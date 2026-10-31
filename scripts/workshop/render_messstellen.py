"""Massstabsbild W35: alle Halter und Sonden-Platzhalter in einer Reihe neben der Menschenfigur 1,80 m (mensch_referenz.sc), Vorderansicht; dazu zwei Nahaufnahmen (Halter, Sonden).
Aufruf: python scripts/workshop/render_messstellen.py -> renders/components/messstellen/messstellen-0{1,2,3}-*.png"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import messstellen as M

D = os.path.join(sc.ROOT, "designs", "components")
OUT = os.path.join(sc.ROOT, "renders", "components", "messstellen")
os.makedirs(OUT, exist_ok=True)

items = [("mensch_referenz.sc", "Figur", -450, 0, 0),
         ("halter_mast.sc", "H_MAST", 0, 0, 0), ("halter_tauch.sc", "H_TAUCH", 170, 0, 0), ("halter_beruhig.sc", "H_BERUHIG", 520, 0, 20), ("halter_box.sc", "H_BOX", 800, 0, 12),
         ("halter_inline_d32.sc", "H_INLINE32", 1000, 0, 70), ("halter_inline_d50.sc", "H_INLINE50", 1550, 0, 80), ("halter_zelle.sc", "H_ZELLE", 2100, 0, 24),
         ("halter_hahn.sc", "H_HAHN", 2500, 0, 0), ("halter_druck.sc", "H_DRUCK", 2650, 0, 0)]
x = 2900
for k in M.COMPS:
    if k.startswith("sonde_"):
        items.append((k + ".sc", k, x, 0, 0)); x += 80

def base():
    b = sc.Build()
    for (f, nm, *_r) in items:
        b.add("component.insert_design", path=os.path.join(D, f).replace("\\", "/"), name=nm)
    return b

res = sc.run_results(base().write("ms-probe"))
occ = [r["occurrence"] for r in res if "occurrence" in r]
b = base()
for (f, nm, xx, yy, zz), o in zip(items, occ):
    if xx or yy or zz:
        b.add("occurrence.move", occurrence=o, translate=[xx, yy, zz], space="world", move_grounded=True)
scene = os.path.join(sc.TMP, "messstellen-massstab.sc")
sc.run(b.write("ms-massstab"), scene)
sc.snapshot(scene, os.path.join(OUT, "messstellen-01-massstab.png"), [1750, 0, 800], 0.0, 0.0, 6800, w=1800, h=800)
sc.snapshot(scene, os.path.join(OUT, "messstellen-02-halter.png"), [1200, 0, 600], 0.0, 0.0, 3600, w=1800, h=800)
sc.snapshot(scene, os.path.join(OUT, "messstellen-03-sonden.png"), [3350, 0, 100], 0.0, 0.0, 1300, w=1800, h=800)
print(OUT)
