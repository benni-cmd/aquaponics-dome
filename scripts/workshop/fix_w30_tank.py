"""W30 (D50, 31.10.): Tank-Staende verkleinern. Plattform = Konusdurchmesser auf Plattform-Unterkante + 2 x plat_margin (60) + Kegelsitz-Spiel; Rippenradius am Innenrand der Querstreben.
Schreibt data/components/tank.json (typen plat_l/plat_w, plat_l_obj, Parameter plat_margin, rib_r_out, tafel_gap) aus der Tank-Geometrie (tank.geometry). Idempotent.
Aufruf: python scripts/workshop/fix_w30_tank.py   (danach fix_tank_blatt.py, tank.py, check_tank.py)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tank as tk

p = os.path.join(sc.ROOT, "data", "components", "tank.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
obj = {"klein": (706, 707), "gross": (977, 976), "gross_t3": (977, 976)}
d["parameter"]["plat_margin"] = {"wert": 60, "einheit": "mm", "herkunft": "Ben 31.10./D50: Rand der Plattform um den Konus 60 mm je Seite; Plattform aus dem Konusdurchmesser auf Plattform-Unterkante berechnet (fix_w30_tank.py), nicht hart"}
d["parameter"]["tafel_gap"] = {"wert": 30, "einheit": "mm", "herkunft": "[A] W30: Pumpentafel steht seitlich am Stand, Abstand von der Aussenkante der Diagonalen/Querstreben 30 mm; Platzierung Montage"}
out = {}
for typ, T in d["typen"].items():
    G = tk.geometry(T, P)
    r_at = lambda z: T["rt"] + (z - T["z0"]) / G["tan_a"]
    r_plat = r_at(T["plat_z0"])
    size = round(2 * (r_plat + P["cone_clear"] + 60))
    T["plat_l_obj"], T["plat_w_obj"] = obj[typ]
    T["plat_l"], T["plat_w"] = size, size
    T["plat_herkunft"] = f"W30/D50: 2 x (Konusradius {r_plat:.1f} auf Z {T['plat_z0']} + Kegelsitz-Spiel {P['cone_clear']:.0f} + Rand 60) = {size} (OBJ {obj[typ][0]} x {obj[typ][1]}); Plattformdicke und Z unveraendert, Tank unveraendert"
    out[typ] = (size, r_plat)
ax = lambda T: T["plat_l"] / 2 - T["leg_w"] / 2
r_out = int(ax(d["typen"]["gross"]) - d["typen"]["gross"]["leg_w"] / 2 - 3)       # Innenkante der Querstreben minus 3 mm Spiel
d["parameter"]["rib_r_out"] = {"wert": r_out, "einheit": "mm", "herkunft": f"W30: Innenkante der Querstreben (Plattformhalbbreite - leg_w = {d['typen']['gross']['plat_l'] / 2 - d['typen']['gross']['leg_w']:.1f}) minus 3 mm Spiel, damit die Rippe die Querstreben nicht durchdringt (OBJ: Rippen bis r 468, vor W30 440) [A]"}
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (v[0], round(v[1], 1)) for k, v in out.items()}, "rib_r_out", r_out)
