"""Orchestrator-Vorgabe 29.10. ~08:00 fuer ibc_beet: standpipe_h = media_depth - 35 mm (265), FarmHub 220 als Variante; Glocke 30 mm ueber dem Standrohr (295); Bezeichnung 'IBC-Wanne (Sondermass nach OBJ)'; Zulauf laengs als A."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "ibc_beet.json")
d = json.load(open(p, encoding="utf-8"))
P = d["parameter"]
P["standpipe_over"]["wert"] = 265
P["standpipe_over"]["herkunft"] = "Orchestrator 29.10.: standpipe_h = media_depth - 35 mm = 265 ueber der Medienunterkante (Wasserstand 35 mm unter der Oberflaeche, dazwischen SRAC 1 Zoll = 25 mm / R03 trockene Zone 2-5 cm); Variante FarmHub 220 (R03 Befund 5, widerspricht Befund 4); Gesamtlaenge ab Bulkhead = Stuetzhoehe + 265 [E]"
P["bell_h"]["wert"] = 295
P["bell_h"]["herkunft"] = "[E] Glocke = Standrohrhoehe + 30 mm (R03: 250 bei Standrohr 220); oben verschlossen"
d["beschreibung"] = d["beschreibung"].replace("Wanne mit Randwulst", "IBC-Wanne (Sondermass nach OBJ) mit Randsims")
txt = json.dumps(d, ensure_ascii=False)
rep = [("220 mm ueber der Medienunterkante = 80 mm unter der Medienoberflaeche (R03 Befund 5: Standrohr 22 cm bei 30 cm Medium)", "265 mm ueber der Medienunterkante = 35 mm unter der Medienoberflaeche (Orchestrator-Vorgabe 29.10.: media_depth - 35; FarmHub-Variante 220 = 80 mm unter der Oberflaeche, R03 Befund 5)"),
       ("Standrohr PVC-U d25 (Laenge 30 + 482 mm)", "Standrohr PVC-U d25 (Laenge 30 + 527 mm)"),
       ("Glocke PVC-U d75 x 250 mit Deckel", "Glocke PVC-U d75 x 295 mit Deckel"),
       ("Glocke d75 x 250", "Glocke d75 x 295"),
       ("Standrohrhoehe 220 ueber Medienunterkante (R03 gibt 220 bei Medientiefe 300 ohne Wasserraum) [E]", "Standrohrhoehe 265 ueber Medienunterkante (Orchestrator: media_depth - 35), Variante FarmHub 220 mit Glocke 250; R03 gibt 220 bei Medientiefe 300 ohne Wasserraum"),
       ("Wasserstand 80 mm unter der Oberflaeche (FarmHub-Standrohr 22 cm) gegen", "Wasserstand 35 mm unter der Oberflaeche (Standrohr 265; FarmHub 220 = 80 mm) gegen"),
       ("Standrohr d25, 220 mm ueber Medienunterkante", "Standrohr d25, 265 mm ueber Medienunterkante (Variante FarmHub 220)"),
       ('"25 / 220"', '"25 / 265"'),
       ("Standrohr 220 mm hoch ueber der Medienunterkante", "Standrohr 265 mm hoch ueber der Medienunterkante")]
for a, b in rep:
    txt = txt.replace(a, b)
d = json.loads(txt)
for r in d["herkunft_tabelle"]:
    if r[0].startswith("Glocke"):
        r[0] = "Glocke d75 x 295, Schlitze 10x40, Luftloch 10"
        r[2] = "R03 + E"
        r[3] = "R03: d75, Schlitze 10x40 (FarmHub); Hoehe 295 = Standrohr 265 + 30 (R03: 250 bei 220)"
    if r[0].startswith("Standrohr d25"):
        r[2] = "Orchestrator + R03"
        r[3] = "Vorgabe media_depth - 35 mm (29.10.), FarmHub 220 als Variante; R03 Befund 5 widerspricht Befund 4/SRAC"
d["blatt"]["abweichung"] = d["blatt"]["abweichung"].replace("die Bezeichnung 'halbe IBC' (OBJ-Gruppe IBC_Open_Top) passt nicht zu 2953 mm (eine halbe IBC misst ca. 1200 x 1000): die 2953-mm-Wanne ist ein Sonderbau (verschweisste/laengere Wanne) - Bild-Kritiker Luecke 1, offen beim Orchestrator;", "die OBJ-Gruppe heisst IBC_Open_Top, das Mass 2953 x 933-993 x 637 ist ein Sondermass: Bezeichnung im Modell 'IBC-Wanne (Sondermass nach OBJ)', Werkstoff A (Orchestrator-Entscheidung 29.10.);")
d["blatt"]["offen"] = [x for x in d["blatt"]["offen"] if not x.startswith("Wanne 2953 mm lang")]
d["blatt"]["offen"].append("Zulaufrohr laengs statt quer: Auslegung A, vom Orchestrator bestaetigt (29.10.)")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ibc_beet.json (3) gepflegt")
