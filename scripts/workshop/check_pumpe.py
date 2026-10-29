"""Vorpruefung Pumpenmodule gegen layout.json tanks[].modules und Scope-Card pumpe: Tafel-/Gehaeusemasse = OBJ, Anzahl (eindeutige Positionen), Pumpe steht auf der Konsole, Stutzen-Durchmesser, Anschlusslagen.
Aufruf: python scripts/workshop/check_pumpe.py [typ ...]   (exit 1 bei FAIL)"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import sc

def uniq_modules(lay, l, h, w_max=None):
    out = set()
    for t in lay:
        for m in t["modules"]:
            if abs(m["l"] - l) <= 2 and abs(m["h"] - h) <= 2 and (w_max is None or m["w"] <= w_max):
                out.add((t["id"], int(m["cx"] // 50), int(m["cy"] // 50)))      # Duplikate (1-5 mm Versatz) zusammenfassen
    return out

def main(typs):
    p, d = sc.load_params("pumpe")
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["tanks"]
    ck = sc.Check("pumpe")
    for typ in typs:
        T = d["typen"][typ]
        ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"{typ}.sc"))
        B = {b["name"]: b for b in ev["bodies"]}
        if T["art"] == "pumpe":
            ck.eq(f"{typ} Anzahl laut layout.json (eindeutige Positionen)", len(uniq_modules(lay, T["tafel_l"], T["tafel_h"], 10)), T["anzahl"])
            tb = B["Montagetafel"]["bbox"]
            ck.eq(f"{typ} Tafel Laenge", tb["max"][0] - tb["min"][0], T["tafel_l"], 0.5)
            ck.eq(f"{typ} Tafel Dicke", tb["max"][1] - tb["min"][1], T["tafel_t"], 0.5)
            ck.eq(f"{typ} Tafel Hoehe", tb["max"][2] - tb["min"][2], T["tafel_h"], 0.5)
            ck.eq(f"{typ} Pumpensockel steht auf der Konsole", B["Pumpensockel"]["bbox"]["min"][2], p["pump_z"] - T["motor_d"] / 2 - ((T["kopf_d"] - T["motor_d"]) / 2 + 1), 0.01)      # Oberkante der waagerechten Konsole (Sockelhoehe = Kopfueberstand + 1 mm)
            ck.eq(f"{typ} Konsole ist ein Winkel (Oberkante Vertikalschenkel = Oberkante Platte)", B["Konsole"]["bbox"]["max"][2], B["Pumpensockel"]["bbox"]["min"][2], 0.01)
            ck.eq(f"{typ} Pumpenkopf kollidiert nicht mit der Konsole (Luft >= 0,5 mm)", 1 if B["Pumpenkopf"]["bbox"]["min"][2] - B["Pumpensockel"]["bbox"]["min"][2] >= 0.5 else 0, 1)
            ck.eq(f"{typ} Motor ruht auf dem Sockel (tangential)", B["Motor"]["bbox"]["min"][2], B["Pumpensockel"]["bbox"]["max"][2], 0.01)
            ck.eq(f"{typ} Motor-D", B["Motor"]["bbox"]["max"][2] - B["Motor"]["bbox"]["min"][2], T["motor_d"], 0.2)
            ck.eq(f"{typ} Saugstutzen D", B["Saugstutzen"]["bbox"]["max"][2] - B["Saugstutzen"]["bbox"]["min"][2], T["saug_d"], 0.2)
            ck.eq(f"{typ} Druckstutzen D", B["Druckstutzen"]["bbox"]["max"][0] - B["Druckstutzen"]["bbox"]["min"][0], T["druck_d"], 0.2)
            ck.eq(f"{typ} Druckstutzen zeigt nach oben (Oberkante ueber Pumpenkopf)", 1 if B["Druckstutzen"]["bbox"]["max"][2] > B["Pumpenkopf"]["bbox"]["max"][2] else 0, 1)
            ck.eq(f"{typ} Pumpe vor der Tafel (+Y)", 1 if B["Motor"]["bbox"]["min"][1] > tb["max"][1] else 0, 1)
            ck.eq(f"{typ} Pumpe liegt innerhalb der Tafellaenge (Motor+Kopf)", 1 if B["Motor"]["bbox"]["min"][0] > tb["min"][0] and B["Saugstutzen"]["bbox"]["max"][0] < tb["max"][0] else 0, 1)
            ck.eq(f"{typ} Standwinkel", len([k for k in B if k.startswith("Standwinkel")]), 2)
            ck.eq(f"{typ} Kabel mit Stecker", len([k for k in B if k in ("Kabel", "Stecker")]), 2)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["pumpe_klein", "pumpe_gross"]))
