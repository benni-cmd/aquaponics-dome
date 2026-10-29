"""Bauteil Pflanztisch (T8, ref-6): weisse Rinnenplatte mit Rippen, 3 gestaffelte Reihen Loecher, 4 Beine + Winkelstuetzen.
Ursprung: Mitte, Boden z=0, Laengsachse X. Aufruf: python scripts/components/pflanztisch.py <out.json>"""
import json, sys
P = dict(len=2300, w=900, h=950, plate=60, leg_r=30, rib_h=25, rib_w=30, hole_d=70, cols=6, pitch=330, row_pitch=270)
cmds = []
def add(c, **p): cmds.append({"command": c, "params": p})
def build(P=P):
    L, W, H, T = P["len"], P["w"], P["h"], P["plate"]
    add("solid.box", length=L, width=W, height=T, center=[0, 0, H - T/2], operation="new", name="Platte", body_name="T8_Platte")
    for i, y in enumerate((-405, -135, 135, 405)):   # Rinnenrippen
        add("solid.box", length=L - 120, width=P["rib_w"], height=P["rib_h"], center=[0, y, H + P["rib_h"]/2], operation="join", targets=["T8_Platte"], name=f"Rippe{i+1}")
    for r in range(3):
        for c in range(P["cols"]):
            x = (c - (P["cols"] - 1)/2)*P["pitch"] + (r % 2)*P["pitch"]/2 - P["pitch"]/4
            add("solid.cylinder", diameter=P["hole_d"], height=T + P["rib_h"] + 10, base=[round(x, 1), (r - 1)*P["row_pitch"], H - T - 5], operation="cut", targets=["T8_Platte"], name=f"Loch{r*P['cols']+c+1}")
    k = 0
    for sx in (-1, 1):
        for sy in (-1, 1):
            k += 1
            add("solid.cylinder", radius=P["leg_r"], height=H - T, base=[sx*(L/2 - 80), sy*(W/2 - 45), 0], operation="join", targets=["T8_Platte"], name=f"Bein{k}")
    for sx in (-1, 1):   # Winkelstuetzen: vom Bein schraeg nach innen oben in die Platte
        add("solid.cylinder", radius=15, height=650, base=[sx*(L/2 - 80), -(W/2 - 45), 450], axis=[-sx*0.707, 0, 0.707], operation="join", targets=["T8_Platte"], name=f"Stuetze{sx+2}")
    add("appearance.assign", bodies=["T8_Platte"], color="#f3f3f1")
if __name__ == "__main__":
    build(); json.dump({"commands": cmds}, open(sys.argv[1], "w"))
