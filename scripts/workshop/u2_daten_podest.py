"""Schreibt data/components/podest_vortex.json und podest_biofilter.json (U2): beide Podeste haben denselben Aufbau (podest_lib.py), nur Tank, Hoehe und Standflaeche unterscheiden sich.
Aufruf: python -X utf8 scripts/workshop/u2_daten_podest.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

TANKS = {
    "podest_vortex": dict(tn="T102", tank="tank_klein", hkey="podest_vortex_h", h=577, span=720, plat=619, wsp=1900, tank_ok=1323, last_kg=500,
                          h_herkunft="[E] Soll-Wasserspiegel Vortex 1900 (data/oasis-soll.json vortex_1) minus Tankoberkante 1323 (tank_klein, R61 Abschnitt 6 Nr. 3) = 577; mindestens, D100",
                          titel="Podest Vortex", rolle="Vortex 1 und 2"),
    "podest_biofilter": dict(tn="T103", tank="tank_gross", hkey="podest_biofilter_h", h=230, span=920, plat=821, wsp=1800, tank_ok=1570, last_kg=1100,
                             h_herkunft="[E] Soll-Wasserspiegel Biofilter 1800 (data/oasis-soll.json bio_1) minus gebauter Ueberlauf 1570 (N-AUTOBAHN-V2 2.1, R61 Abschnitt 6 Nr. 3) = 230, D100",
                             titel="Podest Biofilter", rolle="Biofilter 1 und 2"),
}


def daten(name, t):
    return {
        "klasse": name, "teilenummer": t["tn"], "revision": "A",
        "beschreibung": f"{t['titel']} (U2, D100): Stahlrahmen aus Vierkantrohr 40 x 40 x 3 fuer {t['tank']} (Standflaeche {t['plat']} x {t['plat']}), Hoehe {t['h']} mm als Parameter {t['hkey']}; 4 Fussplatten, 4 Stuetzen, Fuss- und Kopfrahmen, 8 Knotenbleche; hebt den Tank, bis der Ueberlauf auf dem Soll-Wasserspiegel {t['wsp']} liegt",
        "quelle_masse": f"data/oasis-soll.json ({t['rolle']}: Wasserspiegel {t['wsp']} ueber Fussboden); docs/research/R61-oasis-wasserkreislauf.md Abschnitt 4 (O2, O10) und 6 Nr. 3; docs/decisions.md D100; data/components/tank.json (plat_l {t['plat']})",
        "parameter": {
            t["hkey"]: {"wert": t["h"], "einheit": "mm", "herkunft": t["h_herkunft"] + "; U4/U5 setzen den Wert aus data/oasis-lage.json"},
            "span": {"wert": t["span"], "einheit": "mm", "herkunft": f"[A] Aussenmass des Rahmens = Plattform {t['plat']} + 2 x 50 mm Ueberstand (Annahme Lage-Probe U1, Paket Abschnitt Grenzen), auf {t['span']} gerundet"},
        },
        "werkstoff": {"name": "Stahl, feuerverzinkt (Vierkantrohr 40 x 40 x 3, Blech 6 mm)", "dichte_g_cm3": 7.85, "farbe": "#b8bcc2", "herkunft": "[A] Normprofil aus dem Katalog (vierkantrohr_40x40x3), Selbstbau durch Schweissen oder Verschrauben (Designprinzip 7: Podeste sind Selbstbau)"},
        "anzahl": {"soll": f"{t['rolle']}: je 1 Podest je Tank", "quelle": "data/oasis-soll.json (vortex_1/_2, bio_1/_2); D100"},
        "bezugspunkt": f"Mitte der Standflaeche in X und Y, Z 0 = Boden (Fussplatten-Unterkante); Auflage fuer {t['tank']} auf Z = {t['hkey']} (Oberkante Kopfrahmen)",
        "herkunft_tabelle": [
            [f"Hoehe {t['h']} mm", f"Parameter {t['hkey']}", "E", t["h_herkunft"], "mittel"],
            [f"Standflaeche {t['span']} x {t['span']}", f"{t['tank']} Plattform {t['plat']} + Ueberstand", "A", "data/components/tank.json plat_l; Ueberstand 50 mm aus der Lage-Probe U1", "niedrig"],
            ["Vierkantrohr 40 x 40 x 3", "Stuetzen und Rahmen", "A", "data/katalog.json vierkantrohr_40x40x3; Tragfaehigkeit gerechnet im Check, Statik N-STATIK offen", "mittel"],
        ],
        "blatt": {
            "funktion": f"Hebt {t['tank']} ({t['rolle']}) um {t['h']} mm, damit der Ueberlauf auf dem Soll-Wasserspiegel {t['wsp']} liegt und das Wasser danach per Schwerkraft weiterlaeuft (Designprinzip 1). Reiner Stahlrahmen aus Normprofil, kein eigener Kreislaufteil.",
            "querschnitt": f"Vierkantrohr 40 x 40 x 3; Fussplatten 100 x 100 x 6; Stuetzen von Z 6 bis {t['h']}; Fussrahmen (Z 6 bis 46) und Kopfrahmen (Z {t['h'] - 40} bis {t['h']}) zwischen den Stuetzen; 8 Knotenbleche 6 x 100 x 100 aussen an den X-Seiten.",
            "toleranzen": "Rahmenstuecke stossen auf Stoss an die Stuetzen (Beruehrung, keine Durchdringung); Hoehe ueber den Parameter einstellbar.",
            "ports": [["Auflage Tank", f"{t['tank']} Plattform {t['plat']} x {t['plat']}", f"Z = {t['h']}", "Tank steht mittig auf dem Kopfrahmen"]],
            "verbindungen": ["Rahmen verschweisst oder verschraubt (Normprofil, Selbstbau)", "Fussplatten mit Fussbodenankern (Loecher im Modell nicht gebohrt)", "Tank mit Tankplattform auf dem Kopfrahmen verschraubt"],
            "montage": ["Fussplatten setzen, Stuetzen und Fussrahmen verschweissen/verschrauben, Kopfrahmen aufsetzen und ausrichten", "Knotenbleche anschweissen, Rahmen auf Fussboden dueblen", f"{t['tank']} aufsetzen und mit dem Kopfrahmen verbinden"],
            "werkzeug": "Winkelschleifer, Schweissgeraet oder Schrauben M8, Wasserwaage",
            "teileliste": [], "kritiker": "offen (Pruefer P-Pruef)",
            "pruefung": [f"python -X utf8 scripts/workshop/check_{name}.py"],
            "offen": ["Statik (Kippsicherheit, Horizontallast, Fussbodenanker) ist Sache von N-STATIK; der Check rechnet nur Stuetzendruck und Knicken", "Verzinkung und Werkstoff-Lebensmittelnachweis nicht noetig (kein Wasserkontakt)"],
            "abweichung": "Kein OBJ-Bestand (Bauteil ist neu nach der Quelle)."
        },
        "u2": {"tank": t["tank"], "last_kg": t["last_kg"], "tank_ok": t["tank_ok"], "wsp": t["wsp"], "plat": t["plat"]},
    }


if __name__ == "__main__":
    for name, t in TANKS.items():
        pfad = os.path.join(sc.ROOT, "data", "components", name + ".json")
        json.dump(daten(name, t), open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("geschrieben", pfad)
