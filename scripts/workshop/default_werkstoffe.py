"""Werkstoff-Zuweisung fuer die in gen_dome.py inline gebauten Komponenten (N-MODELL-KOMPLETT Schritt 4).
gen_dome.py (component_file) schreibt diese .sc ohne Werkstoff (Default); sie werden bei jedem Modell-Build neu erzeugt.
Dieses Skript weist den Koerpern SolidCraft-Werkstoffe zu, deren Namen in data/katalog.json unter sc_material stehen.
Aufruf:  python -X utf8 scripts/workshop/default_werkstoffe.py            -> zeigt Plan, aendert nichts
         python -X utf8 scripts/workshop/default_werkstoffe.py --apply    -> schreibt designs/components/<komp>.sc
         python -X utf8 scripts/workshop/default_werkstoffe.py --copy DIR -> arbeitet auf Kopien in DIR (zum Pruefen)
Gehoert NACH jedem gen_dome-Build ausgefuehrt (Montage-Sitzung, build.sh)."""
import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(__file__))
import sc

# komponente -> {Koerpername: SolidCraft-Werkstoff}; Marke [A] = angenommen
PLAN = {
    "fundamentring": {"T3_Sockel": "Beton"},                                   # [A] Betonsockel, Katalog beton
    "pool_zentral": {"T5_Zentraltank": "PE Tank",                              # [A] Beckenwerkstoff offen (R32), PE als Platzhalter
                     "T5_Stutzen_SA_Ost_A": "PVC grau", "T5_Stutzen_SA_West_B": "PVC grau",
                     "T5_Stutzen_BA_Mitte": "PVC grau", "T5_Wasser": "Wasser"},
    "zweitbecken": {"T6_Zweitbecken": "PE Tank", "T6_Wasser": "Wasser"},       # [A] wie Pool
    "zulaufrohr": {"T10_Zulaufrohr": "PVC grau"},                              # [A] PVC-U Rohr
    "schaltschrank": {"T11_Schaltschrank": "Stahl verzinkt"},                  # [A] Stahlblech-Gehaeuse (N-ALARM offen)
}

FARBE = {"Beton": "#9a9a96", "PE Tank": "#3f7d4e", "PVC grau": "#8d9296", "Wasser": "#6fb6e8", "Stahl verzinkt": "#aeb4b8"}

def katalog_dichte():
    k = json.load(open(os.path.join(sc.ROOT, "data", "katalog.json"), encoding="utf-8"))
    return {m: w["dichte_g_cm3"] for w in k["werkstoffe"] for m in w.get("sc_material", [])}

def katalog_namen():
    k = json.load(open(os.path.join(sc.ROOT, "data", "katalog.json"), encoding="utf-8"))
    return {m for w in k["werkstoffe"] for m in w.get("sc_material", [])}

def main(argv):
    apply_ = "--apply" in argv
    copy = argv[argv.index("--copy") + 1] if "--copy" in argv else None
    ok_namen = katalog_namen()
    rc = 0
    for komp, m in PLAN.items():
        for mat in set(m.values()):
            if mat not in ok_namen:
                print(f"FEHLER {komp}: Werkstoff '{mat}' steht nicht im Katalog (sc_material)"); rc = 1
    if rc:
        return rc
    for komp, m in PLAN.items():
        src = os.path.join(sc.ROOT, "designs", "components", komp + ".sc")
        if copy:
            os.makedirs(copy, exist_ok=True)
            dst = os.path.join(copy, komp + ".sc"); shutil.copyfile(src, dst); src = dst
        ev = sc.evaluate(src)
        namen = {b["name"] for b in ev["bodies"]}
        fehlt = [k for k in m if k not in namen]
        if fehlt:
            print(f"FEHLER {komp}: Koerper nicht im .sc: {fehlt}"); rc = 1; continue
        offen = [b["name"] for b in ev["bodies"] if b["name"] not in m]
        if offen:
            print(f"WARNUNG {komp}: Koerper ohne Zuordnung: {offen}")
        print(f"{komp}: " + ", ".join(f"{k}->{v}" for k, v in m.items()))
        if apply_ or copy:
            for mat in sorted(set(m.values())):
                bodies = [k for k, v in m.items() if v == mat]
                script = os.path.join(sc.TMP, "ws-defmat.json")
                json.dump({"commands": [
                    {"command": "material.create", "params": {"name": mat, "density_g_cm3": katalog_dichte()[mat], "color": FARBE[mat]}},
                    {"command": "material.assign", "params": {"bodies": bodies, "material": mat}}]}, open(script, "w"))
                import subprocess
                r = subprocess.run([sc.CLI, "run", script, "--in", src, "--save", src, "--quiet"], capture_output=True, text=True)
                if r.returncode:
                    print("FEHLER material.assign", komp, r.stderr.strip()); rc = 1
            ev2 = sc.evaluate(src)
            print("   danach:", {b["name"]: b["material"] for b in ev2["bodies"]})
    return rc

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
