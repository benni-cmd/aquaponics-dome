"""Gemeinsame Hilfen der Runde U2 (N-UNIFY-AUTOBAHN): Bauteil starten, Koerper setzen, bauen/messen, Pruefung aufsetzen.
Jede Komponente hat Parameter in data/components/<name>.json, einen Generator scripts/workshop/<name>.py und einen Check check_<name>.py.
Aufruf der Generatoren: python -X utf8 scripts/workshop/<name>.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
from check_lt_w39 import interference


def start(name, ueberschreiben=None):
    """(p, d, b, root): Parameter (optional ueberschrieben), Metadaten, Build mit Parametern im Design."""
    p, d = sc.load_params(name)
    p = dict(p, **(ueberschreiben or {}))
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    return p, d, b


def material(b, tabelle):
    """tabelle: {name: (dichte g/cm3, farbe)} -- Namen so waehlen, dass data/katalog.json sie einem Werkstoff zuordnet."""
    for nm, (dens, col) in tabelle.items():
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)


def wurzel(b, root, d, teilenummer, werkstoff):
    b.add("component.create", name=root, grounded=True)
    b._root = (root, d, teilenummer, werkstoff)


def box(b, name, size, center, mat, schneiden=None):
    """Quader size=(x, y, z) um center; mit schneiden=[Koerper...] wird er stattdessen aus diesen Koerpern geschnitten."""
    if schneiden:
        b.add("solid.box", length=size[0], width=size[1], height=size[2], center=list(center), operation="cut", targets=list(schneiden), name="C_" + name)
        return
    b.add("solid.box", length=size[0], width=size[1], height=size[2], center=list(center), operation="new", name="R_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material=mat)


def cyl(b, name, d, h, base, axis, mat, schneiden=None, join=None):
    """Zylinder; schneiden=[...] schneidet ihn aus, join=Koerper fuegt ihn an."""
    ax = list(axis)
    if schneiden:
        b.add("solid.cylinder", diameter=d, height=h, base=list(base), axis=ax, operation="cut", targets=list(schneiden), name="C_" + name)
        return
    if join:
        b.add("solid.cylinder", diameter=d, height=h, base=list(base), axis=ax, operation="join", targets=[join], name="J_" + name)
        return
    b.add("solid.cylinder", diameter=d, height=h, base=list(base), axis=ax, operation="new", name="R_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material=mat)


def kugel(b, name, d, center, mat):
    b.add("solid.sphere", diameter=d, center=list(center), operation="new", name="R_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material=mat)


def fertig(b, root, teilenummer, d, werkstoff):
    b.add("component.metadata.set", component=root, part_number=teilenummer, description=d["beschreibung"], revision="A", properties={"Werkstoff": werkstoff})
    return b


def main(name, build, renders=()):
    """Bauen, speichern, messen; renders = [(suffix, target, yaw, pitch, dist, section|None)] mit --render."""
    out = os.path.join(sc.ROOT, "designs", "components", name + ".sc")
    sc.run(build().write(name), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v, 1) for v in mn], [round(v, 1) for v in mx])
    for x in ev["bodies"]:
        print("  ", x["name"], round(x["volume_mm3"] / 1000, 1), "cm3", round(x["mass_g"]), "g", x.get("material"))
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", name)
        os.makedirs(rd, exist_ok=True)
        for suf, tgt, yaw, pit, dist, sec in renders:
            sc.snapshot(out, os.path.join(rd, f"{name}-{suf}.png"), tgt, yaw, pit, dist, w=1000, h=700, section=sec)


class Pruefung:
    """Kopf aller Checks: Parameter, .sc, Koerper nach Name, Hilfsmessungen."""
    def __init__(self, name):
        self.name = name
        self.p, self.d = sc.load_params(name)
        self.path = os.path.join(sc.ROOT, "designs", "components", name + ".sc")
        self.ev = sc.evaluate(self.path)
        self.B = {b["name"]: b for b in self.ev["bodies"]}
        self.ck = sc.Check(name)

    def ausdehnung(self, k, achse):
        bb = self.B[k]["bbox"]
        return bb["max"][achse] - bb["min"][achse]

    def mitte(self, k, achse):
        bb = self.B[k]["bbox"]
        return (bb["max"][achse] + bb["min"][achse]) / 2

    def unten(self, k): return self.B[k]["bbox"]["min"][2]
    def oben(self, k): return self.B[k]["bbox"]["max"][2]

    def eq(self, label, ist, soll, tol=0.0):
        self.ck.eq(label, ist, soll, tol)

    def wahr(self, label, bedingung):
        self.ck.eq(label, 1 if bedingung else 0, 1)

    def koerper(self, namen):
        self.ck.eq(f"Koerperzahl {len(namen)}", len(self.B), len(namen))
        self.ck.eq("Koerpernamen wie erwartet (Differenz)", len(set(self.B) ^ set(namen)), 0)

    def interferenz(self):
        bad, _ = interference(self.path)
        self.ck.eq("Interferenzen (Volumen > 0,5 mm3, ungeprueft zaehlt)", len(bad), 0)
        for i in bad[:5]:
            print("   ", i)

    def port(self, label, koerper, pos, richtung):
        """ebene Stirnflaeche am Koerper mit Normale = richtung und Mittelpunkt pos (0,6 mm)."""
        import math
        fs = sc.faces(self.path, koerper)
        hit = any(f.get("plane_normal") and sum(f["plane_normal"][i] * richtung[i] for i in range(3)) > 0.999 and math.dist(f["centroid"], pos) < 0.6 for f in fs)
        self.ck.eq(f"Port {label}: Stirnflaeche an {tuple(round(v, 1) for v in pos)}", 1 if hit else 0, 1)

    def zylinder(self, label, koerper, radius):
        fs = sc.faces(self.path, koerper)
        self.ck.eq(f"{label}: Zylinderflaeche r {radius:g}", 1 if any(f.get("cylinder") and abs(f["cylinder"]["radius"] - radius) < 0.01 for f in fs) else 0, 1)

    def fertig(self):
        print(f"INFO Masse gesamt {self.ev['total']['mass_g']:.0f} g")
        return self.ck.done()
