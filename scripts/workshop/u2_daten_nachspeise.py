"""Schreibt data/components/nachspeise_ventil.json (U2, D107): abgeleitet aus data/components/schwimmerventil_pool.json (T84), mit zweitem Eingang (Regenwasser zuerst, Frischwasser nachrangig)
und der Hoehe des Fischtanks (Rohrachse 510 ueber dem Spiegel). Aufruf: python -X utf8 scripts/workshop/u2_daten_nachspeise.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

pool = json.load(open(os.path.join(sc.ROOT, "data", "components", "schwimmerventil_pool.json"), encoding="utf-8"))
par = {k: v for k, v in pool["parameter"].items() if k not in ("water_z", "ventil_h")}
par["ventil_h"] = {"wert": 510, "einheit": "mm", "herkunft": "[E] Rohrachse ueber dem Spiegel des Fischtanks: Rand 1200 minus Wsp 750 = 450 (data/oasis-soll.json fish) plus 60 mm ueber dem Rand (freier Auslauf wie T84); Lage Modell-Z 1150 + 510"}
par["spiegel"] = {"wert": 750, "einheit": "mm", "herkunft": "[Q] data/oasis-soll.json fish wsp_ueber_fussboden_mm 750 (Fussboden-Bezug; Modell-Z 1150)"}
par["staffel"] = {"wert": 30, "einheit": "mm", "herkunft": "[A] Staffelung: das Frischwasser-Ventil schliesst 30 mm tiefer als das Regenwasser-Ventil; so oeffnet Frischwasser erst, wenn Regenwasser nicht mehr nachlaeuft (D114)"}
par["abstand_y"] = {"wert": 120, "einheit": "mm", "herkunft": "[A] Abstand der beiden Ventilachsen (Regenwasser y 0, Frischwasser y 120): groesser als die Kugel Ø 110"}
d = {
    "klasse": "nachspeise_ventil", "teilenummer": "T108", "revision": "A",
    "beschreibung": "Nachspeise-Ventil am Fischtank (U2, D107, Quelle A8): zwei mechanische Schwimmerventile 3/4 Zoll (aus schwimmerventil_pool T84) nebeneinander; Eingang A Regenwasser (Z 0 Spiegel), Eingang B Frischwasser aus der Aktivkohle-Station, die Kugel des Frischwasser-Ventils haengt 30 mm tiefer: Regenwasser zuerst, Frischwasser nachrangig; Rohrachse 510 ueber dem Spiegel, freier Auslauf",
    "quelle_masse": "data/oasis-soll.json (nachspeise: mechanisches Schwimmerventil am Fischtank, Regenwasser zuerst, Frischwasser nachrangig; fish: Rand 1200, Wsp 750); docs/decisions.md D107; data/components/schwimmerventil_pool.json (T84, Maße und Herkunft des Ventils); docs/research/R53-europa-frischwasser-luft.md",
    "parameter": par,
    "werkstoff": pool["werkstoff"],
    "anzahl": {"soll": "1 (Nachspeise-Ventil am Fischtank)", "quelle": "data/oasis-soll.json nachspeise (anzahl 1)"},
    "bezugspunkt": "Port A Regenwasser (Mitte Muffenoeffnung) im Ursprung, Port B Frischwasser bei y 120; Rohrachse +X (Zulauf aus -X), Z hoch, Hebelarme nach unten; Einbau: Rohrachse Modell-Z 1660 (Spiegel 1150 + 510)",
    "herkunft_tabelle": [
        ["Ventil 3/4 Zoll, Handelsteil", "zwei Gehaeuse Ø 38 x 80", "A", "T84 (R53: R+M Suttner 701403); Maße aus dem Blatt T84, nicht aus einem Datenblatt", "niedrig"],
        ["Regenwasser zuerst", "Frischwasser-Kugel 30 mm tiefer", "A", "D114: mechanische Staffelung statt zweitem Mechanismus; Quelle A8 nennt nur die Reihenfolge", "mittel"],
        ["Rohrachse 510 ueber dem Spiegel", "Rand 450 + 60", "E", "data/oasis-soll.json fish: Rand 1200, Wsp 750; freier Auslauf 60 mm ueber dem Rand (EN 1717 sinngemaess)", "mittel"],
    ],
    "blatt": {
        "funktion": "Haelt den Wasserspiegel im Fischtank bei 750 mm: sinkt er (Verdunstung, Wasserwechsel), oeffnet zuerst das Regenwasser-Ventil (Eingang A, Regenwassertank 5 m3, erste Wahl, salz- und chlorfrei); laeuft kein Regenwasser nach, sinkt der Spiegel um weitere 30 mm und das Frischwasser-Ventil (Eingang B, ueber die Aktivkohle-Station entchlort) oeffnet. Steigt der Spiegel, schliessen beide: Schutz vor Ueberfuellen. Mechanisch, ohne Strom (Designprinzip 1). Auslauf frei ueber dem Rand: kein Rueckfluss in die Leitungen.",
        "querschnitt": "Je Ventil: Klebemuffe d25 (Aussen 32,25, Tiefe 19) mit Gewindeteil 40 lang, Ventilgehaeuse Ø 38 x 80, zwei Wangen, Hebelarm Ø 8 mit Schwimmerkugel Ø 110 (PP); Achsabstand 120; Frischwasser-Kugel 30 mm tiefer als die Regenwasser-Kugel.",
        "toleranzen": "Hebelarm und Kugel je ein Koerper; Maße Platzhalter wie T84; Schliessdruck mit Drossel offen.",
        "ports": [
            ["A Regenwasser (Muffe)", "PVC-U d25, Klebemuffe, Tiefe 19", "x 0, y 0, z 0", "Oeffnung zeigt -X; Rohr d25 vom Regenwassertank"],
            ["B Frischwasser (Muffe)", "PVC-U d25, Klebemuffe, Tiefe 19", "x 0, y 120, z 0", "Oeffnung zeigt -X; Rohr d25 von der Aktivkohle-Station"],
        ],
        "verbindungen": ["Beide Rohre d25 in die Klebemuffen", "Befestigung am Rand des Fischtanks: Halter nicht modelliert (Montage)"],
        "montage": ["Ventile so ans Rohrende kleben, dass die Rohrachse 510 ueber dem Spiegel liegt (Modell-Z 1660)", "Hebelarme einstellen: Regenwasser schliesst bei Spiegel 750, Frischwasser bei Spiegel 720", "Regenwassertank an A, Aktivkohle-Station an B; Begrenzer 4 l/min vor dem Frischwasser-Ventil pruefen"],
        "werkzeug": "Saege, PVC-Kleber nach DIN EN 14814, Wasserwaage",
        "teileliste": [], "kritiker": "offen (Pruefer P-Pruef)",
        "pruefung": ["python -X utf8 scripts/workshop/check_nachspeise_ventil.py"],
        "offen": [
            "Zwei Ventile mit gestaffelter Kugelhoehe sind eine Annahme (D114); die Quelle nennt ein Ventil mit Regenwasser zuerst. Rueckfall: ein Mehrwege-Schwimmerventil oder die Frischwasser-Nachspeisung im Regentank",
            "Handelsteil, Fabrikat und Schliessdruck mit Drossel offen (wie T84); Bezug Europa und Lebensmittelnachweis (D85) siehe data/beschaffung/",
            "Der Bestand T84 (schwimmerventil_pool) wird in U3/U5 durch dieses Teil ersetzt; T84 bleibt bis dahin unberuehrt",
        ],
        "abweichung": "Kein OBJ-Bestand (Bauteil ersetzt T84 am Fischtank).",
    },
}
if __name__ == "__main__":
    pfad = os.path.join(sc.ROOT, "data", "components", "nachspeise_ventil.json")
    json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben", pfad)
