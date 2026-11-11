"""U3b (N-UNIFY-AUTOBAHN): Teiledaten data/parts/ibc_beet_<typ>.json an den A21-Aufbau anpassen (Sperrboden, Medienschutz, Plattenhuelse, Reduktion entfallen;
Abtropfgitter, Vlies, Sieb, Auslasswinkel, Auslassrohr, Reduzierhuelse Auslass, Schlauchtuelle, Luftschlauch, Ausstroemer neu) und zwei Werkstoffe in data/katalog.json ergaenzen.
Koerper, Masse und Box je Zeile werden aus dem gebauten .sc gemessen (solidcraft-cli eval). Aufruf: python -I -X utf8 scripts/workshop/u3b_parts.py [typ ...]"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

ROOT = sc.ROOT
AUSN = "Katalog- und Stueckliste-Eintrag folgt in U8 (Paket n-unify-autobahn); Teil neu in U3b (D132 bis D135)"
OFFEN = "offen: Recherche folgt in U8 (D76), Bezug noch nicht belegt"
QUELLE = "docs/parts/ibc_beet.md, data/components/ibc_beet.json (a21_*), docs/decisions.md D132 bis D135, Quelle A21 (docs/quellen/oasis-showcase-2026-11-10-nachtrag/flow-diagram.html)"
WERKSTOFFE = [
    {"id": "pp_vlies", "name": "Polypropylen-Vlies (Drainagevlies, Geotextil)", "norm": "Herstellerangabe offen [A]", "dichte_g_cm3": 0.075,
     "dichte_hinweis": "Ersatzdichte der 2-mm-Lage im Modell (150 g/m2 bei 2 mm), nicht die Werkstoffdichte", "lebensmittelkontakt": "ja", "konfidenz": "angenommen",
     "sc_material": ["PP Vlies"], "pilot": False, "quelle": "data/components/ibc_beet.json (a21_vlies_t), docs/decisions.md D132", "marke": "[A]"},
    {"id": "edelstahl_gewebe_2mm", "name": "Edelstahl-Drahtgewebe, Maschenweite 2 mm", "norm": "DIN ISO 9044 (Industriedrahtgewebe) [A]", "dichte_g_cm3": 1.24,
     "dichte_hinweis": "Ersatzdichte der 1-mm-Lage im Modell (Draht 0,5 mm, Teilung 2,5: rund 1,24 kg/m2), nicht die Werkstoffdichte", "lebensmittelkontakt": "ja", "konfidenz": "angenommen",
     "sc_material": ["Sieb Edelstahlgewebe 2 mm"], "pilot": False, "quelle": "data/components/ibc_beet.json (a21_sieb_mm, a21_sieb_t), docs/decisions.md D132", "marke": "[A]"},
]


def rw(path):
    raw = open(path, "rb").read()
    return json.loads(raw.decode("utf-8")), b"\r\n" in raw


def wr(path, d, crlf):
    s = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    if crlf:
        s = s.replace("\n", "\r\n")
    open(path, "wb").write(s.encode("utf-8"))


def katalog():
    p = os.path.join(ROOT, "data", "katalog.json")
    d, crlf = rw(p)
    have = {w["id"] for w in d["werkstoffe"]}
    for w in WERKSTOFFE:
        if w["id"] not in have:
            i = [x["id"] for x in d["werkstoffe"]].index("edelstahl_gewebe_100um") + 1
            d["werkstoffe"].insert(i, w)
    wr(p, d, crlf)


def messen(B, names):
    g = round(sum(B[n]["mass_g"] for n in names), 1)
    bb = B[names[0]]["bbox"]
    e = sorted(bb["max"][i] - bb["min"][i] for i in range(3))
    return g, e


def mtext(prefix, B, names):
    g, e = messen(B, names)
    return f"{prefix}; Masse {g} g, Einzelkoerper {e[0]:.1f} x {e[1]:.1f} x {e[2]:.1f} mm (Modell-Bounding-Box)"


def row(old, i, name, names, B, typ, werk, prefix, funktion, eig, norm, artikel=None, einheit="Stk", menge_je=None, lm="ja", expl=None, bezug=None, ausn=False):
    t = dict(id=i, name=name, koerper=names, menge=len(names), typ=typ, werkstoff=werk, masse_mm=mtext(prefix, B, names))
    if artikel:
        t.update(artikel_id=artikel, artikel_einheit=einheit, artikel_menge_je_instanz=menge_je if menge_je is not None else float(len(names)))
    t["masse_g"] = messen(B, names)[0]
    t.update(funktion=funktion, eigenschaften=eig, norm=norm, norm_konfidenz="angenommen", lebensmittelkontakt=lm, lebensmittelkontakt_konfidenz="angenommen", konfidenz="angenommen", quelle=QUELLE)
    t["bezug"] = bezug or (old.get("bezug") if old else OFFEN)
    if ausn:
        t["ausnahme"] = AUSN
    if expl:
        t["explosion"] = expl
    return t


def bearbeite(typ):
    path = os.path.join(ROOT, "designs", "components", f"ibc_beet_{typ}.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    p, dd = sc.load_params("ibc_beet")
    T = dd["typen"][typ]
    pp = os.path.join(ROOT, "data", "parts", f"ibc_beet_{typ}.json")
    d, crlf = rw(pp)
    old = {t["id"]: t for t in d["teile"]}
    z = [1, 0, 0]
    stz = sorted([k for k in B if k == "Stuetze" or re.fullmatch(r"Stuetze \(\d+\)", k)], key=lambda s: int(re.findall(r"\d+", s)[0]) if "(" in s else 1)
    rim_gap = T["hoehe"] - (p["a21_boden"] + p["media_depth"])
    ls = max(messen(B, ["Standrohr"])[1]) / 1000
    gh = max(messen(B, ["Glocke"])[1]) / 1000
    ar = max(messen(B, ["Auslassrohr"])[1]) / 1000
    vol_m = B["Medium"]["volume_mm3"] / 1e6
    gi_vol = B["Abtropfgitter"]["volume_mm3"]
    teile = []
    # Wanne
    t = dict(old["wanne"]); t["masse_mm"] = mtext(t["masse_mm"].split("; Masse ")[0], B, ["Wanne"]); t["masse_g"] = messen(B, ["Wanne"])[0]
    t["eigenschaften"] = ["Gebrauchter IBC (1000 l) aus HDPE, passend gesägt, Wand 4 mm, Innenradius der Ecken 40 mm.",
                          f"Länge und Breite je Beettyp; Randsims 20 × 14 mm; die Medienoberfläche liegt {rim_gap:.0f} mm unter dem Rand.",
                          "Der Wannenboden ist ohne Bohrung (U3b): drei Bohrungen in den Stirnwänden, Auslass Ø 36 (+X, Achse 28 über dem Boden), Luftschlauch Ø 10 (−X) und Zulauf Ø 22 (−X, 25 mm unter dem Rand)."]
    teile.append(t)
    # Stuetzen
    t = dict(old["stuetze"]); t["koerper"] = stz; t["menge"] = len(stz); t["masse_g"] = messen(B, stz)[0]
    h_post = B[stz[0]]["bbox"]["max"][2] - B[stz[0]]["bbox"]["min"][2]
    t["masse_mm"] = mtext("Klotz 60 × 60 mm", B, stz)
    t["artikel_menge_je_instanz"] = float(len(stz))
    t["funktion"] = "Die Stützklötze tragen das Abtropfgitter und darüber Vlies, Sieb und Medium auf dem Wannenboden."
    t["eigenschaften"] = [f"Klotz 60 × 60 × {h_post:.0f} mm aus PP, drei Reihen unter dem Gitter, Abstand höchstens 420 mm; die Klötze im Weg von Siphon und Auslass fehlen ({len(stz)} statt {3 * (int(p['post_nx']) if T['laenge'] > 2500 else 5)}).",
                          "Hält rund 500 bis 700 kg Medium.", f"Darunter bleibt ein {h_post:.0f} mm hoher Luftraum, durch den das Wasser zur Glocke abläuft."]
    teile.append(t)
    teile.append(row(None, "abtropfgitter", "Abtropfgitter", ["Abtropfgitter"], B, "platte", "pp", "PP-Rost 25 mm hoch, Stegrost: Schlitze 16 × 296, Steg 4, Rand 8 mm zur Wand",
                     "Das Abtropfgitter liegt am Boden des Beets, trägt Vlies, Sieb und Medium und lässt das Wasser durch die Schlitze zur Glocke ablaufen (Quelle A21).",
                     ["Stegrost aus PP, 25 mm hoch, auf den Stützklötzen, 8 mm Abstand zur Wannenwand.",
                      f"Modellvereinfachung: Schlitze 16 × 296 (Teilung 20 und 300), freie Fläche {100 - 100 * gi_vol / ((B['Abtropfgitter']['bbox']['max'][0] - B['Abtropfgitter']['bbox']['min'][0]) * (B['Abtropfgitter']['bbox']['max'][1] - B['Abtropfgitter']['bbox']['min'][1]) * 25):.0f} Prozent; real Maschen 20 × 20 mit 64 Prozent.",
                      "Die Glocke geht durch ein Loch Ø 79 im Gitter bis zum Wannenboden."],
                     "PP-Gitterrost 25 mm, Maschen 20 × 20, Herstellerangabe offen [A]", ausn=True, expl={"richtung": [0, 0, 1], "abstand_mm": 300}))
    teile.append(row(None, "vlies", "Drainagevlies", ["Vlies"], B, "kaufteil", "pp_vlies", "Vlies PP 2 mm (Annahme 150 g/m²), bis 2 mm vor die Wand",
                     "Das Vlies liegt über dem Gitter und hält Schlamm und feine Teilchen aus dem Wasserraum unter dem Medium fern (Quelle A21).",
                     ["Drainagevlies aus PP, 2 mm dick, ganzflächig unter dem Sieb.", "Loch Ø 79 für die Glocke.", "Maße und Flächengewicht sind angenommen; Datenblatt nicht gelesen."],
                     "Drainagevlies aus PP, Herstellerangabe offen [A]", ausn=True, expl={"richtung": [0, 0, 1], "abstand_mm": 420}))
    teile.append(row(None, "sieb", "Sieb (Edelstahlgewebe)", ["Sieb"], B, "kaufteil", "edelstahl_gewebe_2mm", "Edelstahlgewebe, Maschenweite 2 mm, Ersatzdicke 1 mm",
                     "Das Sieb liegt über dem Vlies, hält Blähton und Schlamm vom Siphon fern und trägt das Medium (Quelle A21).",
                     ["Drahtgewebe aus Edelstahl, Maschenweite 2 mm (Draht 0,5 mm), im Modell eine Platte von 1 mm Ersatzdicke.", "Loch Ø 79 für die Glocke.", "Maschenweite und Draht sind angenommen."],
                     "Edelstahl-Drahtgewebe, DIN ISO 9044 [A]", ausn=True, expl={"richtung": [0, 0, 1], "abstand_mm": 520}))
    t = dict(old["medium"]); t["masse_mm"] = mtext(t["masse_mm"].split("; Masse ")[0], B, ["Medium"]); t["masse_g"] = messen(B, ["Medium"])[0]
    t["artikel_menge_je_instanz"] = round(vol_m / 1000, 4)
    t["eigenschaften"] = ["Blähton 8 bis 16 mm, gewaschen, 300 mm hoch, liegt auf dem Sieb.", f"Menge in diesem Beettyp: {vol_m:.0f} Liter (Schüttdichte 0,9 [A]).",
                          "Das Wasser steht nur in den Poren (rund 40 Prozent); beim Flutstand 250 über dem Flur reicht es 180 mm über das Sieb.", f"Die Netztöpfe der Pflanzen stehen auf der Oberfläche, {rim_gap:.0f} mm unter dem Rand."]
    teile.append(t)
    t = dict(old["standrohr"]); t["masse_mm"] = mtext("Rohr d25 × 1,5 mm", B, ["Standrohr"]); t["masse_g"] = messen(B, ["Standrohr"])[0]; t["artikel_menge_je_instanz"] = round(ls, 3)
    t["eigenschaften"] = [f"PVC-U-Druckrohr d25 × 1,5 mm, rund {ls * 1000:.0f} mm lang, steckt im Auslasswinkel.", "Das Wasser steht bis zur Rohrkante, 120 mm unter der Medienoberfläche (Flutstand 250 über dem Flur).", "Die Glocke steht konzentrisch darüber."]
    teile.append(t)
    t = dict(old["glocke"]); t["masse_mm"] = mtext("Rohr d75 × 275 mm, 3 Kerben 14 × 12, Luftloch Ø 10, Auslassloch Ø 27", B, ["Glocke"]); t["masse_g"] = messen(B, ["Glocke"])[0]; t["artikel_menge_je_instanz"] = round(gh, 3)
    t["eigenschaften"] = ["Rohr d75 mit Deckel, 275 mm lang, steht auf dem Wannenboden und geht durch Gitter, Vlies und Sieb (Quelle A21: Siphon bis ganz nach unten).",
                          "Drei Kerben 14 × 12 mm am Fuß (zusammen 504 mm², das Standrohr 380 mm²) und ein Luftloch Ø 10 liegen unter dem Gitter.",
                          "Das Loch Ø 27 in der +X-Wand lässt das Auslassrohr durch (im Bau abzudichten).", "Das Anspringen bei 3,3 l/min ist nur am Muster prüfbar."]
    teile.append(t)
    teile.append(row(None, "auslasswinkel", "Auslasswinkel 90° d25", ["Auslasswinkel"], B, "kaufteil", "pvc_u", "PVC-U-Winkel 90° für Rohr d25, Muffen 14 mm tief (Modell)",
                     "Der Winkel verbindet das Standrohr mit dem waagerechten Auslassrohr und liegt unter der Glocke.",
                     ["Klebemuffen d25, Außen-Ø 34, Mittelpunkt bis Muffenende 29 mm.", "Er liegt 28 mm über dem Wannenboden und endet innerhalb der Glocke.", "Maße sind angenommen; Datenblatt nicht gelesen."],
                     "PVC-U-Winkel 90°, d25, Klebemuffe [A]", ausn=True, expl={"richtung": [1, 0, 0], "abstand_mm": 150}))
    teile.append(row(old["standrohr"], "auslassrohr", "Auslassrohr d25", ["Auslassrohr"], B, "rohr", "pvc_u", "Rohr d25 × 1,5 mm, waagerecht", "Das Auslassrohr führt das abgesaugte Wasser durch Glocke, Tankverbinder und Stirnwand nach außen.",
                     [f"PVC-U-Druckrohr d25 × 1,5 mm, rund {ar * 1000:.0f} mm lang, Achse 28 mm über dem Wannenboden.", "Es bleibt unter dem Gitter und endet bündig mit dem Tankverbinder; daran sitzt die Schlauchtülle."], "PVC-U-Druckrohr PN10, ISO 4422 [A]",
                     artikel="ROH-pvcu-d25", einheit="m", menge_je=round(ar, 3), expl={"richtung": [1, 0, 0], "abstand_mm": 300}))
    t = dict(old["bulkhead"]); t["name"] = "Tankverbinder (Stirnwand)"; t["masse_mm"] = mtext("Tankverbinder 32 mm × 1 Zoll, Flansch Ø 44", B, ["Bulkhead"]); t["masse_g"] = messen(B, ["Bulkhead"])[0]
    t["funktion"] = "Der Tankverbinder führt das Wasser dicht durch die +X-Stirnwand aus dem Beet heraus."
    t["eigenschaften"] = ["Kunststoff-Wanddurchführung 32 mm × 1 Zoll mit Flansch (Modell: Ø 36, Flansch Ø 44 innen an der Wand), mit Dichtung und Kontermutter.", "In der Bohrung Ø 36 der Stirnwand, Achse 28 mm über dem Wannenboden; darin die Reduzierhülse 32/25.", "Flanschmaß ist angenommen; Datenblatt nicht gelesen."]
    t["explosion"] = {"richtung": [1, 0, 0], "abstand_mm": 200}
    teile.append(t)
    t = row(old["reduzierhuelse_boden"], "reduzierhuelse_auslass", "Reduzierhülse 32/25 (Stirnwand)", ["Reduzierhuelse_Auslass"], B, "kaufteil", "pvc_u", "Reduzierhülse 32/25", "Die Reduzierhülse passt das Auslassrohr d25 in den Tankverbinder ein.",
            ["Außen-Ø 32, innen 25, steckt im Tankverbinder.", "Maße sind angenommen."], "PVC-U-Reduzierhülse 32/25, Klebemuffe [A]", artikel="FIT-reduktion-d32", expl={"richtung": [1, 0, 0], "abstand_mm": 120})
    teile.append(t)
    teile.append(row(None, "schlauchtuelle", "Schlauchtülle ID25 (Rücklauf-Anschluss)", ["Schlauchtuelle"], B, "kaufteil", "pvc_u", "Schlauchtülle für Schlauch ID25, zwei Widerhaken Ø 28, 40 mm lang",
                     "Die Schlauchtülle ist der Anschluss des Beets an den Rücklaufschlauch ID25 zum Sumpftank (D106); sie ragt 32 mm über den Randwulst.",
                     ["Rohr 25 / 20 mit zwei Widerhaken, sitzt am Ende des Tankverbinders auf der Auslassachse.", "Die Nennweite ID25 ist angenommen (Quelle nennt keine; D106: Sumpf-Zuläufe Schlauch ID25).", "Auf dieser Achse schließt U6 den Rücklaufschlauch an."],
                     "Schlauchtülle d25 aus PVC [A]", artikel="SCH-schlauchtuelle-d25", expl={"richtung": [1, 0, 0], "abstand_mm": 450}))
    teile.append(row(None, "luftschlauch", "Luftschlauch d8 (Belüftung)", ["Luftschlauch"], B, "rohr", "pvc_p_schlauch", "Luftschlauch Ø 8 × 1,5 mm",
                     "Der Luftschlauch bringt die Luft für die Belüftung unten im Beet durch die −X-Stirnwand zum Ausströmerstab (Quelle A21).",
                     ["Schlauch Ø 8 (innen 5), kommt 40 mm aus der Wand und endet am Ausströmerstab.", "Die Luftquelle legt die Quelle nicht fest; U6 verbindet den Anschluss mit der Belüftungsanlage (D130)."], "PVC-P-Luftschlauch, Herstellerangabe offen [A]", ausn=True, expl={"richtung": [-1, 0, 0], "abstand_mm": 300}))
    teile.append(row(None, "ausstroemer", "Ausströmerstab Ø 16 × 600", ["Ausstroemer"], B, "kaufteil", "pp", "Ausströmerstab Ø 16 × 600 mm (poröser Kunststoff, im Modell massiv)",
                     "Der Ausströmerstab liegt unten im Beet und gibt Luft ab, damit der Wasserraum unter dem Gitter nicht fault (Quelle A21).",
                     ["Poröser Stab Ø 16, 600 mm lang, auf dem Wannenboden zwischen den Stützreihen.", "Im Modell ein Vollkörper; die Poren sind nicht gezeichnet."], "Ausströmerstab, Herstellerangabe offen [A]", ausn=True, expl={"richtung": [0, 0, 1], "abstand_mm": 220}))
    for k in ("tropfrohr", "endstopfen_zulauf", "reinigungsschacht", "schachtkappe"):
        t = dict(old[k]); nm = t["koerper"]
        t["masse_mm"] = mtext(t["masse_mm"].split("; Masse ")[0], B, nm); t["masse_g"] = messen(B, nm)[0]
        teile.append(t)
    for t in teile:                                   # Wortreste des alten Aufbaus
        for f in ("funktion", "masse_mm"):
            if isinstance(t.get(f), str):
                t[f] = t[f].replace("Sperrboden", "Sieb")
        t["eigenschaften"] = [e.replace("Sperrboden", "Sieb") for e in t["eigenschaften"]]
    d["teile"] = teile
    d["koerperzahl"] = len(ev["bodies"])
    d["gruppen"] = [
        {"id": "wanne_und_boden", "name": "Wanne und Stützen", "kurz": "Die Wanne mit den Stützklötzen trägt Gitter und Medium.", "teile": ["wanne", "stuetze"]},
        {"id": "drainage", "name": "Drainage nach A21", "kurz": "Abtropfgitter, Vlies und Sieb halten das Wasser unter dem Medium offen und Schlamm vom Siphon fern.", "teile": ["abtropfgitter", "vlies", "sieb"]},
        {"id": "medium", "name": "Medium", "kurz": "Der Blähton, in dem die Pflanzen wurzeln.", "teile": ["medium"]},
        {"id": "ablauf", "name": "Ablauf mit Siphon", "kurz": "Standrohr, Glocke, Winkel, Auslassrohr und Tankverbinder entleeren das Beet im Takt seitlich in den Rücklauf.", "teile": ["standrohr", "glocke", "auslasswinkel", "auslassrohr", "bulkhead", "reduzierhuelse_auslass", "schlauchtuelle"]},
        {"id": "belueftung", "name": "Belüftung unten", "kurz": "Luftschlauch und Ausströmerstab belüften den Wasserraum unter dem Gitter.", "teile": ["luftschlauch", "ausstroemer"]},
        {"id": "zulauf", "name": "Zulauf", "kurz": "Das Tropfrohr bringt das Wasser ins Beet.", "teile": ["tropfrohr", "endstopfen_zulauf"]},
        {"id": "reinigung", "name": "Reinigung", "kurz": "Der Schacht zum Absaugen des Schlamms.", "teile": ["reinigungsschacht", "schachtkappe"]}]
    d["kurz"] = "Ein halber IBC-Container als Flut-und-Ebbe-Beet nach Quelle A21: Blähton auf Sieb, Vlies und Abtropfgitter, Wasser über das Tropfrohr, Entleeren per Glockensiphon bis zum Wannenboden, seitlicher Auslass mit Schlauchtülle, Belüftung unten."
    d["hinweis"] = ("Texte aus docs/parts/ibc_beet.md und data/components/ibc_beet.json (Stand U3b, D132 bis D135). Maße von Gitter, Vlies, Sieb, Winkel, Tankverbinder-Flansch, Schlauchtülle und Ausströmer sind angenommen; "
                    "Datenblätter der Kaufteile nicht gelesen. Neue Teile ohne Katalog- und Stücklistenzeile (Ausnahme bis U8). Netztöpfe und Pflanzen sind Instanzen des Domes, nicht Teil des Beets.")
    wr(pp, d, crlf)
    print(typ, "Zeilen", len(teile), "Koerper", d["koerperzahl"])


if __name__ == "__main__":
    katalog()
    for typ in [a for a in sys.argv[1:]] or ["aussen_800", "innen_933", "aussen_933", "aussen_993"]:
        bearbeite(typ)
