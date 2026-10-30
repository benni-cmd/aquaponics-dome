"""Aussentische 99 mm nach innen (Ben 30.10. "Tische nach innen", W23-Befund 2): ap_c aussen 4973 -> 4874, damit die aeusserste Rinnenreihe und die Beine innerhalb der Kuppelhaut liegen.
Randbedingungen: Laufweg B (Aussenportal innen 4874 - 515 = 4359 gegen Mittelportal aussen 3858,5) = 500,5 mm (harte Untergrenze D29: 500), Abstand der Rinnenenden zur Feldebene >= 15 mm; die Aussenbeete folgen ap_c (D37: Beete auf der Sektorachse, Apothem = ap_c, Montage). Idempotent.
Aufruf: python scripts/workshop/fix_w25_aussen_innen.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "nft_tisch.json")
d = json.load(open(p, encoding="utf-8"))
T = d["typen"]["aussen"]
T["ap_c"] = 4874
T["ap_c_herkunft"] = "Ben 30.10. (Tische nach innen) + W23-Befund 2: Tischmitte = Aussenbeet-Mitte 4874 (vorher 4973, D30/W17): die aeusserste Rinnenreihe lag bis 87 mm ausserhalb der Kuppelhaut (check_nft_fit, Feldebenen durch die Strebenachsen); Aussenportal 4359..5389, Laufweg B 500,5 mm (harte Untergrenze D29: 500), Wandluft 317 mm; Beete folgen (D37)"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ap_c aussen", T["ap_c"])
