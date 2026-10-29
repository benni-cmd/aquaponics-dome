"""Kontextbild fuer den Bild-Kritiker (salatkopf): drei Netztoepfe mit Salatkoepfen (S/M/L-Mischung ueber Drehung) auf einer Rinnenoberseite, 3/4-Sicht wie ref-6.
Aufruf: python scripts/workshop/render_salat_kontext.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

D = os.path.join(sc.ROOT, "designs", "components")
def base():
    b = sc.Build()
    b.add("solid.box", length=560, width=140, height=6, center=[0, 0, 63 - 3.5 - 3], operation="new", name="Rinnendeckel_R", body_name="Rinnenoberseite")
    b.add("material.create", name="Rinne weiss", density_g_cm3=1.0, color="#d9dcde")
    b.add("material.assign", bodies=["Rinnenoberseite"], material="Rinne weiss")
    for i in range(3):
        b.add("component.insert_design", path=os.path.join(D, "netztopf.sc").replace("\\", "/"), name=f"Netztopf_{i}")
        b.add("component.insert_design", path=os.path.join(D, "salatkopf.sc").replace("\\", "/"), name=f"Salatkopf_{i}")
    return b

res = sc.run_results(base().write("salat-kontext-probe"))
occ = [r["occurrence"] for r in res if "occurrence" in r]          # Reihenfolge: NT0, SK0, NT1, SK1, NT2, SK2
b = base()
for i, x in enumerate((-170, 0, 170)):
    b.add("occurrence.move", occurrence=occ[2 * i], translate=[x, 0, 0], move_grounded=True)
    b.add("occurrence.move", occurrence=occ[2 * i + 1], translate=[x, 0, 63], axis=[0, 0, 1], angle=f"{i * 70 + 20} deg", move_grounded=True)
out = os.path.join(sc.TMP, "salat-kontext.sc")
sc.run(b.write("salat-kontext"), out)
img = os.path.join(sc.ROOT, "renders", "components", "salatkopf", "critic", "k4-modell-im-eltern-kontext-rinne.png")
sc.snapshot(out, img, [0, 0, 85], 0.55, 0.5, 560, w=1100, h=520)
print(img)
