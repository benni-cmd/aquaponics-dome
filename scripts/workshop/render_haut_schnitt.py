"""Bild W22: Paneel (edge_inset 0) und Randprofil-Kappe im Schnitt an der Kante P0P1 des Typs BBB: Paneel liegt mit 15 mm Auflage je Seite auf der Kappe (zwei Paneelkanten, eine Kappe). Nur Darstellung (Schnittpunkt-Szenario), kein Bauteil.
Aufruf: python scripts/workshop/render_haut_schnitt.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
D = os.path.join(sc.ROOT, "designs", "components")
OUT = os.path.join(sc.ROOT, "renders", "components", "haut_profil")
os.makedirs(OUT, exist_ok=True)
def base():
    b = sc.Build()
    b.add("component.insert_design", path=os.path.join(D, "haut_paneel_BBB.sc").replace("\\", "/"), name="Paneel_A")
    b.add("component.insert_design", path=os.path.join(D, "haut_paneel_BBB.sc").replace("\\", "/"), name="Paneel_B")
    b.add("component.insert_design", path=os.path.join(D, "haut_profil.sc").replace("\\", "/"), name="Kappe")
    return b
res = sc.run_results(base().write("haut-schnitt-probe"))
occ = [r["occurrence"] for r in res if "occurrence" in r]
b = base()
p, d = sc.load_params("haut_paneel")
# Basiskante des Paneels liegt bei y = -r (r = 1070,4); zweites Paneel an dieser Kante gespiegelt (Drehung um X 180 Grad), Kappe liegt mittig auf der Kante, Z 8 darueber
r = 3708.0 * 3 ** 0.5 / 6
b.add("occurrence.move", occurrence=occ[0], translate=[0, r, 0], move_grounded=True)                         # Kante y = 0
b.add("occurrence.move", occurrence=occ[1], axis=[0, 0, 1], angle="180 deg", origin=[0, 0, 0], space="world", move_grounded=True)
b.add("occurrence.move", occurrence=occ[1], translate=[0, -r, 0], move_grounded=True)                         # Spiegelbild jenseits der Kante
b.add("occurrence.move", occurrence=occ[2], axis=[0, 0, 1], angle="90 deg", origin=[0, 0, 0], space="world", move_grounded=True)
b.add("occurrence.move", occurrence=occ[2], translate=[0, 0, 8], move_grounded=True)                           # Kappe liegt auf den Paneelen (Z 8..16)
out = os.path.join(sc.TMP, "haut-schnitt.sc")
sc.run(b.write("haut-schnitt"), out)
img = os.path.join(OUT, "haut_profil-03-schnitt-paneel-kappe.png")
sc.snapshot(out, img, [0, 0, 8], 0.0, 0.0, 120, w=1000, h=500, section="XZ")
print(img)
