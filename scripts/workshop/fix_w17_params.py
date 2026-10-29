"""W17 (D28/D29/D30, 29.10.): Parameter der NFT-Tische und des Aussenbeets auf das Radialbudget bringen. Idempotent.
Budget (Apothem-Koordinate, mm): Beckenrand aussen 2095 | Laufweg A 600 | Innenportal 2695..3858 (Beet 933 + 2 x 115, Mitte 3277) | Laufweg B 600 | Aussenportal 4458..5488 (Beet 800 + 2 x 115, Mitte 4973) | Wandluft 218 -> 5706.
Portalrand = Aussenkante der Fussplatte: Beet-Aussenkante + leg_clearance + foot_plate = 115 -> foot_plate 70, leg_clearance 45.
NFT-Mindestzahl 459 (R15): mit gap 100 nur 442 (Aussentische 236 mm weiter innen, Rinnen kuerzer) -> corner_gap 60 liefert 462 (Annahme A, Entscheidung beim Orchestrator).
Aufruf: python scripts/workshop/fix_w17_params.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))

p, d = load("nft_tisch")
P, T = d["parameter"], d["typen"]
P["foot_plate"]["wert"] = 70
P["foot_plate"]["herkunft"] = "[A] Fussplatte 70 x 70 x 5 (W17: vorher 100; Portalrand = Beet-Aussenkante + 115 nach D29, Radialbudget); Lochbild +-20, M8 mit 15 mm Randabstand"
P["leg_clearance"]["wert"] = 45
P["leg_clearance"]["herkunft"] = "[A] W17/D29: Abstand Fussplattenkante zur Beet-Aussenkante 45 mm (vorher 60; gemessen kleinster Abstand zu den OBJ-Beeten >= 30 mm); Portalrand = 45 + 70 = 115 mm ausserhalb des Beets (Radialbudget D28/D29)"
P["corner_gap"]["wert"] = 60
P["corner_gap"]["herkunft"] = "[A] W17: Abstand Rinnenende/Rohr zur Sektorgrenze 60 mm (vorher 100, D18); noetig, damit die NFT-Mindestzahl 459 (R15, D27) mit den auf das Radialbudget verschobenen Aussentischen erreicht wird (gap 100 -> 442, gap 60 -> 462); Entscheidung beim Orchestrator/Ben"
T["aussen"]["ap_c"] = 4973
T["aussen"]["ap_c_herkunft"] = "W17/D30: Tischmitte = Aussenbeet-Mitte 4973 (Aussenportal 4458..5488, Beet 800 + 2 x 115); vorher 5209 (OBJ-Mittel)"
T["mitte"]["ap_c"] = 3277
T["mitte"]["ap_c_herkunft"] = "W17/D30: Tischmitte = Innenbeet-Mitte 3277 (Innenportal 2695..3858, Beet 933 + 2 x 115); vorher 3343 (OBJ-Mittel)"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

p, d = load("ibc_beet")
d["typen"]["aussen_800"] = {"laenge": 2640, "breite": 800, "hoehe": 637, "anzahl": 8,
                            "herkunft": "W17/D29: Aussenbeet einseitig erreichbar <= 800 breit; Laenge 2640 = Obergrenze aus der Montage-Rechnung (Streben/Sockel, D25; Zehneck-Grenze 2 x 4573 x tan 18 - 2 x 100 = 2771); Hoehe wie OBJ 637; ersetzt aussen_933/aussen_993 im Dom (Montage M7 stellt um)"}
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("W17-Parameter gesetzt")
