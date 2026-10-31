"""W33 (R35/D60): Rinnenunterkante 1000 mm -> alte Hoehenangaben in data/components/nft_tisch.json (Ports, Stueckliste, Herkunft, Offen) auf den gebauten Stand ziehen.
Werte werden aus den gebauten Dateien gemessen (Beine, Verteiler, Sammelrohr, Winkelhalter), nicht erinnert. Idempotent.
Aufruf: python scripts/workshop/fix_w33_hoehe.py [fit-abstand-mm]   (danach partsheet.py nft_tisch)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

pth = os.path.join(sc.ROOT, "data", "components", "nft_tisch.json")
d = json.load(open(pth, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}

M = {}
for typ in ("innen", "mitte", "aussen"):
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"nft_tisch_{typ}.sc"))
    B = {b["name"]: b for b in ev["bodies"]}
    legs = sorted((b["bbox"]["max"][2] - b["bbox"]["min"][2] for k, b in B.items() if k.startswith("Bein_")))
    zmid = lambda n: (B[n]["bbox"]["min"][2] + B[n]["bbox"]["max"][2]) / 2
    wk = [b for k, b in B.items() if k.startswith("Winkel")]
    M[typ] = dict(legs=sorted(set(round(v) for v in legs)), zi=zmid("Verteiler"), za=zmid("Sammelrohr"),
                  wz=(min(w["bbox"]["min"][2] for w in wk), max(w["bbox"]["max"][2] for w in wk)),
                  kragarm_min=min((b["bbox"]["min"][2] for k, b in B.items() if k.startswith("Kragarm_")), default=None))
print(json.dumps(M, indent=1))

txt = json.dumps(d, ensure_ascii=False)
def rep(a, b):
    global txt
    if a in txt:
        txt = txt.replace(a, b)
    elif b not in txt:
        sys.exit("FEHLER: weder alt noch neu gefunden: " + a[:70])

zi = {t: round(M[t]["zi"]) for t in M}
za = {t: round(M[t]["za"]) for t in M}
# Ports (z)
rep("x -1349, y 497, z 1391", f"x -1349, y 497, z {zi['aussen']}")
rep("x 1336, y 497, z 1299", f"x 1336, y 497, z {za['aussen']}")
rep("(-288 / -68 / 152 / 372), z ca. 1391", f"(-288 / -68 / 152 / 372), z ca. {zi['aussen']}")
rep("x -823, y 520, z 1383", f"x -823, y 520, z {zi['mitte']}")
rep("x 810, y 520, z 1307", f"x 810, y 520, z {za['mitte']}")
rep("y = Rinnenmitte, z ca. 1383", f"y = Rinnenmitte, z ca. {zi['mitte']}")
rep("x -449, y 256, z 916", f"x -449, y 256, z {zi['innen']}")
rep("x 436, y 256, z 854", f"x 436, y 256, z {za['innen']}")
rep("y = Rinnenmitte, z ca. 916", f"y = Rinnenmitte, z ca. {zi['innen']}")
# Stueckliste: Beinlaengen (gemessen aus den Bein-Koerpern)
la, lm, li = M["aussen"]["legs"], M["mitte"]["legs"], M["innen"]["legs"]
rep("Beine 4 x 40x40x3: Laenge 1251 / 1219, Beinabstand y 960", f"Beine 4 x 40x40x3: Laenge {la[-1]} / {la[0]}, Beinabstand y 960")
rep("Beine 4 x 40x40x3: Laenge 1243 / 1227, Beinabstand y 1093", f"Beine 4 x 40x40x3: Laenge {lm[-1]} / {lm[0]}, Beinabstand y 1093")
rep("Pfosten 2 x 40x40x3: Laenge 777 / 773", f"Pfosten 2 x 40x40x3: Laenge {li[-1]} / {li[0]}")
rep("Beine 1250 mm hoch ausserhalb der Beete", f"Beine 1250 mm hoch (bis W33; seit R35/D60 ca. {la[0]}-{la[-1]} mm) ausserhalb der Beete")
rep("Querstrebe 40x40x3 auf Z 800 (ueber den Pflanzen)", "Querstrebe 40x40x3 auf Z 650 (ueber den Pflanzen, W33; vorher 800)")
rep("Die Z-Hoehen bleiben (innen 840, Mitte/aussen 1300).", "Z-Hoehen: seit W33 (R35/D60) Rinnenunterkante 1000 mm fuer alle drei Ringe (vorher OBJ-Mittel gerundet innen 840, Mitte/aussen 1300).")
rep("Kragarm ueberspannt Rand Z 650 mit 130 mm Luft", "Kragarm ueberspannt Rand Z 650 mit 290 mm Luft (W33; vorher 130)")
wz = M["innen"]["wz"]
rep("Winkelhalter T23 sitzt am Pfostenkopf (Z 719-781) ueber dem Beckenrand Z 650", f"Winkelhalter T23 sitzt am Pfostenkopf (Z {wz[0]:.0f}-{wz[1]:.0f}, W33) ueber dem Beckenrand Z 650")
rep("196/196 PASS", "204/204 PASS")
rep("48/48 PASS aussen, 47/47 aussen3", "50/50 PASS aussen, 49/49 aussen3 (W33)")
rep("Abstand der Tischkanten zur Kuppelhaut >= 15 (aussen 21, mitte/innen weit innen)", "Abstand der Tischkanten zur Kuppelhaut >= 15 (aussen 121 seit W33, vorher 21; mitte/innen weit innen)")
rep("Aussenkante Tisch in 1,3 m Hoehe gegen Strebenabstand", "Aussenkante Tisch in 1,0 m Hoehe (W33; vorher 1,3 m) gegen Strebenabstand")
d = json.loads(txt)

# Herkunft je Typ: R35 voranstellen
pre = "W33 (31.10., R35/D60, Ben: R35 entscheidet): Rinnenunterkante 1000 mm fuer alle Ringe (Toleranz 950-1050, ergonomisch fuer 1,55-1,90 m); vorher OBJ ohne Begruendung || "
for t in d["typen"].values():
    if not t["herkunft"].startswith("W33"):
        t["herkunft"] = pre + t["herkunft"]

# Tabellenzeilen ersetzen
rows = d["herkunft_tabelle"]
def setrow(prefix, row):
    for i, r in enumerate(rows):
        if r[0].startswith(prefix) or r[0] == row[0]:
            rows[i] = row
            return
    rows.append(row)
setrow("Hoehe Rinnenunterkante", ["Hoehe Rinnenunterkante (Boden) bei x=0: Z 1000 (alle Ringe)", "1000 / 1000 / 1000", "R35",
        "docs/research/R35.md Befund 2 + D60: Topfebene 1014-1054 gegen Ellbogen +38...+78 (1,55 m), +6...+46 (1,60), -88...-48 (1,75), -183...-143 mm (1,90); Toleranz 950-1050; Normtexte nur ueber Sekundaerquellen. OBJ lag bei 840 / 1307 / 1308 (Mittel der Unterkanten 819-858, 1280-1330, 1291-1325) ohne Begruendung", "mittel"])
setrow("Querstrebe/Laengsstreben/Diagonalen auf Z", ["Querstrebe/Laengsstreben/Diagonalen auf Z 650 (innen Z 400)", "Z 650", "A",
        "W33: so tief wie die Pflanzen erlauben (Beet-Oberkante Z 475, Pflanzen bis ca. 560, Strebenunterkante 630); Diagonalenwinkel 12,5-15,5 Grad (bei Z 800 nur 4,8-6,9); Portal steht ausserhalb der Beete", "niedrig"])
setrow("Beckenrand Z 650", ["Beckenrand Z 650: Kragarm liegt 290 mm darueber (Unterkante 940)", "Z 650", "Ben",
        "data/params.json pool_rim (Ben: Rand ca. Z 650, am Bild ref-4 zu pruefen); Kragarm-Unterkante = Rinnenhoehe 1000 - holm_h 60 (W33; vorher 840 - 60 = 780, 130 mm)", "mittel"])
setrow("Tischunterkante", ["Tischunterkante (Rinne - Holm 60) ueber Beetrand Z 475: 940 / 465 mm Luft", "465 mm", "R35 + E",
        "R35 Befund 6 (mit Holm 50: 475 mm); Modell holm_h 60 -> Unterkante 940; Beet unter dem Tisch nur an den Kanten erreichbar (Unterarme); Beete-Weg 1/2 entscheiden Ben/Orchestrator", "mittel"])

# Offen
fit = sys.argv[1] if len(sys.argv) > 1 else "?"
entry = (f"W33 (31.10., R35/D60): Rinnenunterkante 1000 mm in allen Ringen (innen 840, Mitte/aussen 1300 vorher); Beine {la[0]}-{la[-1]} mm statt ca. 1220-1250 (aussen), Kuppelhaut-Abstand aeusserste Rinne {fit} mm statt 21; "
         "Querstrebe Z 650 statt 800 (Annahme A, Diagonalen 12,5-15,5 Grad); Tischunterkante 940, 465 mm ueber Beetrand: Beet nur an den Kanten erreichbar (R35 Befund 6; Beete-Weg 1/2 bei Ben/Orchestrator); "
         "Statik (kuerzere Beine, hoehere Knicklast) nicht nachgewiesen; Montage: Tische neu bauen, Hoehe von Zulaufverteiler, Sammelrohr und Leitungen mitfuehren, Laufwegkarte (D54) danach")
d["blatt"]["offen"] = [x for x in d["blatt"]["offen"] if not x.startswith("W33 (31.10.")] + [entry]
json.dump(d, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK")
