"""Blatt ibc_beet nach W17 (D29): Variante aussen_800 (800 x 2640 x 637) ergaenzt; Werte aus der Messung der .sc. Idempotent; vor partsheet.py ibc_beet.
Aufruf: python scripts/workshop/fix_beet_blatt3.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "ibc_beet.json")
d = json.load(open(p, encoding="utf-8"))
bl = d["blatt"]
ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "ibc_beet_aussen_800.sc"))
B = {b["name"]: b for b in ev["bodies"]}
med_l, med_kg = B["Medium"]["volume_mm3"] / 1e6, B["Medium"]["volume_mm3"] / 1e6 * 0.9
empty = sum(b["mass_g"] for b in ev["bodies"] if not b["name"].startswith("Medium") or b["name"].startswith("Medienschutz")) / 1000
xs = (B["Standrohr"]["bbox"]["min"][0] + B["Standrohr"]["bbox"]["max"][0]) / 2
xz = B["Tropfrohr"]["bbox"]["min"][0]
yz = (B["Tropfrohr"]["bbox"]["min"][1] + B["Tropfrohr"]["bbox"]["max"][1]) / 2
zz = (B["Tropfrohr"]["bbox"]["min"][2] + B["Tropfrohr"]["bbox"]["max"][2]) / 2
if "ibc_beet_aussen_800" not in bl["varianten"]:
    bl["varianten"].insert(2, "ibc_beet_aussen_800")
d["anzahl"]["soll"] = "aussen 8 (OBJ: 5 x 933, 3 x 993; Zielmass nach D29: 8 x aussen_800), innen 6"
d["anzahl"]["quelle"] = "data/layout.json ibc_beds; aussen_800: docs/decisions.md D29 (Montage M7 stellt den Dom um)"
if not any(x.startswith("T30 aussen_800") for x in bl["stueckliste"]):
    bl["stueckliste"].append(f"T30 aussen_800 (W17/D29): 8 Beete 800 x 2640 x 637 statt 5 x 933 + 3 x 993 x 2953; Medium {med_l:.0f} l ({med_kg:.0f} kg bei 0,9 kg/l [A]); leer ohne Medium {empty:.0f} kg; Wannen-Sondermass (HDPE), Siphon wie die anderen Aussenbeete")
if not any(x.startswith("aussen_800:") for x in bl["gewicht_gefuellt"].split(" | ")):
    bl["gewicht_gefuellt"] += f" | aussen_800: leer ohne Medium {empty:.0f} kg; Medium {med_l:.0f} l = {med_kg:.0f} kg (Schuettdichte 0,9 [A]); Wasser nicht gerechnet (wie aussen_933 skaliert ca. 0,8 x)"
if not any(x[0].startswith("aussen_800:") for x in bl["ports"]):
    bl["ports"].append(["aussen_800: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden)", "Rohr d25 (PVC-U d25, etwa DN20), Bulkhead D36 mit Flansch D50", f"x {xs:.0f}, y 0, z -30", "Wasser verlaesst das Beet nach unten; Lage aus der Messung (Siphon 200 mm vor dem Ablaufende)"])
    bl["ports"].append(["aussen_800: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand)", "Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03)", f"x {xz:.0f}, y {yz:.0f}, z {zz:.0f}", "Wasser tritt von aussen ein (Oeffnung zeigt -X); Lage aus der Messung (Rohr 50 mm von der Innenwand)"])
bl["offen"] = [x for x in bl["offen"] if not x.startswith("W17:")] + [
    "W17: aussen_800 (800 x 2640) ist das Zielmass nach D29; layout.json/gen_dome tragen noch 933/993 x 2953 (Montage M7 setzt Layout und Dom um); Aussenbeete sind einseitig erreichbar (Domwand), daher <= 800 breit",
    "W17: Pflanzraster im Aussenbeet: 288 je Beet (24 x 12) passt nicht auf 800 x 2640 (Topfabstand 110 x 67 mm, Kragen 64): Raster/Topfzahl vom Layout/Integrator neu (Substrat-Mindestzahl 152 gesamt ist mit weniger Toepfen erfuellt: R15/D27); NFT-Mindestzahl 459 haengt nicht am Beet"]
rows = d["herkunft_tabelle"]
if not any(r[0].startswith("Aussenbeet 800") for r in rows):
    rows.append(["Aussenbeet 800 x 2640 x 637 (aussen_800)", "800 / 2640 / 637 mm", "Ben + E", "D29: einseitig erreichbar <= 800; Laenge 2640 = Obergrenze aus der Montage-Rechnung (D25/D28 outer_bed_len), Hoehe wie OBJ; Zehneck-Grenze 2 x 4573 x tan 18 - 2 x 100 = 2771", "mittel"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"ibc_beet.json gepflegt: Medium {med_l:.0f} l, leer {empty:.0f} kg, Standrohr x {xs:.0f}, Zulauf x {xz:.0f}")
