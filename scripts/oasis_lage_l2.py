"""N-UNIFY-AUTOBAHN L2: Bauplaetze in data/oasis-lage.json direkt aus der Quell-Draufsicht (data/oasis-draufsicht.json, D117).

Ersetzt die Lage-Probe U1 (D108 bis D110: Verschiebung, Vorbau aussen) fuer alle Teile mit Soll-Mitte in der Zeichnung.
Hoehen (z_modell_mm) bleiben wie in U1/U4/U5; Ausnahme Filterpumpen: die Quelle zeichnet sie neben dem Fischtank (r 2662,
Tankrand r 2250), sie stehen darum auf dem Fussboden (ANNAHME D152, Bedenken B23).
Drehung: Rechtecke der Quelle 18 Grad (Breite der Zeichnung = Modell-Richtung 18 Grad); Sumpftanks: Langachse 108 Grad.
Aufruf (Projektordner): python -I -X utf8 scripts/oasis_lage_l2.py [--pruefen]   (--pruefen schreibt nicht, Exit 1 bei Abweichung)
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAGE = os.path.join(ROOT, "data", "oasis-lage.json")
SOLL = os.path.join(ROOT, "data", "oasis-draufsicht.json")
FUSSBODEN_Z = 400.0
# Teile, deren Bauplatz L2 setzt (alle Soll-Teile mit Mitte; Ringe und Leitungen nicht)
IDS = ["rain", "tap", "nachspeise", "fish", "nursery", "feed", "filterpumpe_1", "filterpumpe_2", "vortex_1", "vortex_2", "bio_1", "bio_2",
       "sludge_1", "sludge_2", "permakultur", "sump_1", "sump_2", "hauptpumpe_1", "hauptpumpe_2", "venturi_1", "venturi_2",
       "schwimmer_1", "schwimmer_2", "luftpumpe", "luftpumpe_1", "luftpumpe_2"]
RECHTECK_DREHUNG = {"sump_1": 108.0, "sump_2": 108.0}   # Langachse (2975) quer zur Zeichnungs-Breite (1125 entlang 18 Grad)
Z_NEU = {"filterpumpe_1": FUSSBODEN_Z, "filterpumpe_2": FUSSBODEN_Z}


def soll_platz(sid, alt, so):
    if so["art"] == "rechteck":
        dreh = RECHTECK_DREHUNG.get(sid, so["drehung_grad"])
    else:
        dreh = alt.get("drehung_grad", 0.0) if alt else 0.0
    x, y = round(so["x_mm"], 1), round(so["y_mm"], 1)
    z = Z_NEU.get(sid, alt["z_modell_mm"] if alt else FUSSBODEN_Z)
    return {"x_mm": x, "y_mm": y, "drehung_grad": dreh, "z_modell_mm": z, "r_mm": round(math.hypot(x, y), 1),
            "az_grad": round(math.degrees(math.atan2(y, x)), 1), "quelle": "L2: Soll-Mitte aus data/oasis-draufsicht.json (D117, D152)"}


def main():
    lage = json.load(open(LAGE, encoding="utf-8"))
    soll = json.load(open(SOLL, encoding="utf-8"))["teile"]
    pruef = "--pruefen" in sys.argv
    abw = 0
    for b in lage["bauteile"]:
        if b["id"] not in IDS:
            continue
        neu = soll_platz(b["id"], b.get("bauplatz"), soll[b["id"]])
        alt = b.get("bauplatz") or {}
        d = math.hypot(neu["x_mm"] - alt.get("x_mm", 1e9), neu["y_mm"] - alt.get("y_mm", 1e9))
        if pruef:
            if d > 0.5:
                abw += 1
                print("ABW %-14s %.0f mm" % (b["id"], d))
            continue
        if alt and "u1_bauplatz" not in b:
            b["u1_bauplatz"] = {k: alt[k] for k in ("x_mm", "y_mm", "drehung_grad", "z_modell_mm") if k in alt}
        b["bauplatz"] = neu
        print("%-14s %6.0f / %6.0f  Drehung %6.1f  Z %6.0f  (verschoben %.0f mm)" % (b["id"], neu["x_mm"], neu["y_mm"], neu["drehung_grad"], neu["z_modell_mm"], d))
    if pruef:
        print("Abweichungen:", abw)
        return 1 if abw else 0
    lage["meta"]["l2"] = ("11.11.2026 N-UNIFY-AUTOBAHN L2: Bauplaetze = Soll-Mitten der Quell-Draufsicht (scripts/oasis_lage_l2.py); "
                          "die U1-Werte stehen je Teil unter u1_bauplatz; D108 bis D110 ueberholt (D152)")
    with open(LAGE, "w", encoding="utf-8") as f:
        json.dump(lage, f, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
