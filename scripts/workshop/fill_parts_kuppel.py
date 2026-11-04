"""W60 5a, Gruppe Kuppel (Knoten, Streben): fuellt die Handfelder in data/parts/knoten_*.json (29 Dateien) und strebe_a/strebe_b.json.
Auto-Felder (id, koerper, menge, typ, artikel_id ...) bleiben; Koerpernamen der Normteile werden auf die neuen Namen (ScheibeO_k, Schraube_k, ScheibeU_k, Mutter_k) gesetzt.
Strebe: die .sc tragen fremde, nicht committete Aenderungen und das Material 'Default' (nicht im Katalog zugeordnet): Teile bleiben `geruest: true`, Handfelder stehen trotzdem.
Aufruf: python -X utf8 scripts/workshop/fill_parts_kuppel.py   (idempotent)"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

PD = os.path.join(sc.ROOT, "data", "parts")
ARME = json.load(open(os.path.join(sc.ROOT, "data", "components", "knoten_arme.json"), encoding="utf-8"))
WERK = "stahl_verzinkt"
QK = "docs/parts/knoten.md, docs/parts/knoten-ports.md, data/components/knoten.json"

def kg(g): return f"{g / 1000:.2f}".replace(".", ",") + " kg"

def masse_g(t):
    m = re.search(r"Masse ([\d.]+) g", t.get("masse_mm", ""))
    if m:
        t["masse_g"] = float(m.group(1))
    return t["masse_g"]

def knoten(comp):
    d = json.load(open(os.path.join(PD, comp + ".json"), encoding="utf-8"))
    val = int(comp.split("_")[1])
    m = re.match(r"knoten_\d_n(\d+)$", comp)
    nr = int(m.group(1)) if m else {6: 1, 5: 2, 4: 17}[val]
    rho0 = ARME[str(nr)]["rho0"]
    arm_l = 200 - rho0
    by = {t["id"]: t for t in d["teile"]}
    n = by["arm"]["menge"]
    # Koerpernamen der Normteile
    nm = {"scheibe_m10": [f"Scheibe{x}_{k}" for k in range(1, n + 1) for x in "OU"], "schraube_m10x60": [f"Schraube_{k}" for k in range(1, n + 1)], "mutter_m10": [f"Mutter_{k}" for k in range(1, n + 1)]}
    for tid, names in nm.items():
        by[tid]["koerper"] = names
        assert by[tid]["menge"] == len(names)
    common = {"werkstoff": WERK, "lebensmittelkontakt": "nein", "lebensmittelkontakt_konfidenz": "angenommen", "konfidenz": "angenommen"}
    T = {}
    T["knotenkugel"] = dict(common, name="Knotenkugel", typ="sonderteil",
        masse_mm=f"Vollkugel Ø 100 mm, Masse {kg(masse_g(by['knotenkugel']))}",
        funktion="Die Kugel ist die Mitte des Knotens: An ihr hängen die Steckarme, auf die die Streben der Kuppel geschoben werden.",
        eigenschaften=["Vollkugel aus Stahl, Ø 100 mm.",
                       "Eine Kugel statt zweier Knotenplatten, weil die Streben um 16 bis 18 Grad gegen die Berührungsebene geneigt sind; flache Platten würden die Arme durchdringen.",
                       "Die Arme stecken 4 mm tief in der Kugel und werden dort angeschweißt; danach wird der ganze Knoten feuerverzinkt.",
                       "Maße sind angenommen; zu Kugel und Naben nennt die Recherche keine Vorbilder."],
        norm="Baustahl S235, Feuerverzinkung nach EN ISO 1461 [A]", norm_konfidenz="angenommen", quelle=QK + " (Kugel D100: Annahme; R02 nennt kein Nabenmaß)")
    T["arm"] = dict(common, name="Steckarm", typ="sonderteil",
        masse_mm=f"{n} Steckarme, Rechteckrohr 23 × 23 × 3 mm, Länge {arm_l:.0f} mm (reicht bis 200 mm von der Knotenmitte), zusammen {kg(masse_g(by['arm']))}",
        funktion="Jeder Steckarm trägt eine Strebe: Die Strebe wird 80 mm auf den Arm geschoben und mit einem Querbolzen gesichert.",
        eigenschaften=["Jeder Arm zeigt zum Nachbarknoten (Abweichung unter 0,5 Grad) und ist 16 bis 18 Grad gegen die Berührungsebene der Kugel gekippt.",
                       "Querloch Ø 11 mm für den Bolzen, 50 mm hinter dem Strebenende.",
                       "Der Arm ist 0,5 mm je Seite schmaler als das Innenmaß der Strebe (24 mm): Platz für Zink und Schweißverzug.",
                       f"Der Knoten hat {n} Arme (Wertigkeit {val})."],
        norm="Rechteckhohlprofil, kaltgeformt, nach EN 10219-2; Feuerverzinkung nach EN ISO 1461 [A]", norm_konfidenz="angenommen",
        quelle=QK + ", data/components/knoten_arme.json (Richtungen und Längen je Knoten)",
        explosion={"richtung": "radial", "abstand_mm": 200})
    if "ankerlasche" in by:
        T["ankerlasche"] = dict(common, name="Ankerlasche", typ="sonderteil",
            masse_mm=f"Stahlblech 60 × 10 × 150 mm, Loch Ø 14 mm für M12, Masse {kg(masse_g(by['ankerlasche']))}",
            funktion="Die Lasche verbindet den Basisknoten mit dem Fundamentanker im Boden und leitet die Kräfte der Kuppel ins Fundament.",
            eigenschaften=["Sitzt nur an den 10 Basisknoten (vierwertig), ragt von der Kugel nach unten.",
                           "Das Loch Ø 14 mm nimmt die Schraube M12 des Fundamentankers auf.",
                           "An die Kugel angeschweißt, danach feuerverzinkt."],
            norm="Baustahl S235, Feuerverzinkung nach EN ISO 1461 [A]", norm_konfidenz="angenommen",
            quelle=QK + " (Lasche 60 × 10 × 150: Annahme nach Scope-Card fundamentanker)",
            explosion={"richtung": [0, 0, -1], "abstand_mm": 150})
    ns = by["schraube_m10x60"]["menge"]
    T["schraube_m10x60"] = dict(common, name="Sechskantschraube M10", typ="normteil",
        masse_mm=f"{ns} Schrauben M10, im Modell 55 mm lang, zusammen {kg(masse_g(by['schraube_m10x60']))}",
        funktion="Die Schraube geht quer durch Strebe und Steckarm und hält die Strebe auf dem Arm fest.",
        eigenschaften=["Im Modell M10 × 55; der Katalogartikel ist der Schraubensatz M10 × 60 (Schraube, Mutter, zwei Scheiben): Der Längenunterschied von 5 mm ist noch abzugleichen (N-STATIK).",
                       "Je Strebe ein Bolzen, 50 mm hinter dem Strebenende; Richtwert Anzugsmoment 49 Nm bei Festigkeit 8.8.",
                       "Die Normteile kommen aus der SolidCraft-Bibliothek, nicht aus einem Herstellerkatalog."],
        norm="Sechskantschraube ISO 4017 (DIN 933), Festigkeitsklasse 8.8 nach ISO 898-1, verzinkt [A]", norm_konfidenz="angenommen",
        bezug="Schraubensatz M10 × 60 im Katalog (SRB-satz-m10x60); Händler und Bezug in Europa offen (N-BESCHAFFUNG), Normteil im Standardkatalog [A]",
        quelle=QK + " (Querbolzen M10x55 ISO 4017: Annahme)", explosion={"richtung": "radial", "abstand_mm": 120, "folgt": "arm"})
    T["scheibe_m10"] = dict(common, name="Scheibe M10", typ="normteil",
        masse_mm=f"{by['scheibe_m10']['menge']} Scheiben M10, rund 2 mm dick, zusammen {kg(masse_g(by['scheibe_m10']))}",
        funktion="Die Scheibe verteilt den Druck von Schraubenkopf und Mutter auf die dünne Wand der Strebe.",
        eigenschaften=["Zwei Scheiben je Schraube: eine unter dem Kopf, eine unter der Mutter.",
                       "Gehört zum Schraubensatz; kein eigener Artikel in der Stückliste."],
        norm="Scheibe ISO 7089, verzinkt [A]", norm_konfidenz="angenommen",
        bezug="Im Schraubensatz M10 × 60 enthalten (Katalog SRB-satz-m10x60); Bezug in Europa offen [A]",
        quelle=QK + " (Scheibe ISO 7089, Bibliotheksteil)", explosion={"richtung": "radial", "abstand_mm": 60, "folgt": "schraube_m10x60"})
    T["mutter_m10"] = dict(common, name="Mutter M10", typ="normteil",
        masse_mm=f"{by['mutter_m10']['menge']} Muttern M10, zusammen {kg(masse_g(by['mutter_m10']))}",
        funktion="Die Mutter zieht die Schraube fest und klemmt die Strebe auf den Steckarm.",
        eigenschaften=["Sechskantmutter M10, sitzt auf der Gegenseite des Schraubenkopfes.", "Gehört zum Schraubensatz; kein eigener Artikel in der Stückliste."],
        norm="Sechskantmutter ISO 4032, Festigkeitsklasse 8, verzinkt [A]", norm_konfidenz="angenommen",
        bezug="Im Schraubensatz M10 × 60 enthalten (Katalog SRB-satz-m10x60); Bezug in Europa offen [A]",
        quelle=QK + " (Mutter ISO 4032, Bibliotheksteil)", explosion={"richtung": "radial", "abstand_mm": 100, "folgt": "schraube_m10x60"})
    for t in d["teile"]:
        t.update(T[t["id"]])
        t.pop("geruest", None)
    tn = {4: "vierwertig", 5: "fünfwertig", 6: "sechswertig"}[val]
    rep = "" if m else " (Repräsentant, Kopie von Knoten n%02d)" % nr
    d["teilenummer"] = "T60"
    d["stand"] = "5a"
    d["titel"] = f"Kuppelknoten {tn}, Knoten n{nr:02d}{rep}"
    d["kurz"] = (f"Eine Stahlkugel mit {n} Steckarmen verbindet {n} Streben der Kuppel: Jede Strebe wird 80 mm auf einen Arm geschoben und mit einer Schraube gesichert."
                 + (" Als Basisknoten trägt er unten eine Ankerlasche zum Fundament." if val == 4 else ""))
    d["hinweis"] = ("Texte und Zahlen aus docs/parts/knoten.md, knoten-ports.md und data/components/knoten_arme.json. Alle Maße sind Annahmen (Konfidenz niedrig); Stahlgüte, Armmaße und Schraubenlänge warten auf die Statik (N-STATIK). "
                    "Die Explosion zieht Arme und Schrauben vom Knoten weg; in Wirklichkeit wird die Schraube quer durch Strebe und Arm gezogen, die Darstellung zeigt nur die Zusammengehörigkeit. Der europäische Bezug der Kaufteile ist offen (Regel D76).")
    gr = [{"id": "knotenkoerper", "name": "Knotenkörper", "kurz": "Die geschweißte Stahlbaugruppe: Kugel und Steckarme, auf die die Streben kommen.", "teile": ["knotenkugel", "arm"]}]
    if "ankerlasche" in by:
        gr.append({"id": "verankerung", "name": "Verankerung", "kurz": "Die Lasche am Basisknoten zum Fundamentanker.", "teile": ["ankerlasche"]})
    gr.append({"id": "verschraubung", "name": "Verschraubung", "kurz": "Schraube, Scheiben und Mutter sichern je eine Strebe auf ihrem Steckarm.", "teile": ["schraube_m10x60", "scheibe_m10", "mutter_m10"]})
    d["gruppen"] = gr
    write(comp, d)

def strebe(comp):
    d = json.load(open(os.path.join(PD, comp + ".json"), encoding="utf-8"))
    typ = comp[-1].upper()
    L, stk, ks = (3039, 30, 3279) if typ == "A" else (3468, 34, 3708)
    t = d["teile"][0]
    t["name"] = f"Kuppelstrebe {typ}"
    t["werkstoff_soll"] = WERK
    t["masse_mm"] = f"Platzhalter-Rundstab Ø 90 mm, Länge {L} mm, Masse {kg(masse_g(t))} (Standarddichte 1,29, nicht Stahl)"
    t["funktion"] = "Die Strebe ist ein Stab der Kuppel: Sie verbindet zwei Knoten und trägt zusammen mit den anderen Streben das Dach."
    t["eigenschaften"] = [f"Knoten-zu-Knoten-Maß {ks} mm, abzüglich 2 × 120 mm Endversatz ergibt die Teillänge {L} mm.",
                          f"Das Modell enthält {stk} Streben dieses Typs.",
                          "Im Modell ist die Strebe ein sichtbarer Platzhalter-Rundstab Ø 90 mm; das echte Profil ist 30 × 30 mm (Referenzbild), Wand und Güte sind offen (N-STATIK).",
                          "An jedem Ende sitzt eine runde Steckaufnahme Ø 34 × 80 mm für den Steckarm des Knotens, gesichert mit einem Querbolzen M10."]
    t["norm"] = "Rechteckhohlprofil 30 × 30 nach EN 10219-2, Feuerverzinkung nach EN ISO 1461 [A]; Profil und Wand offen"
    t["norm_konfidenz"] = "angenommen"
    t["lebensmittelkontakt"] = "nein"; t["lebensmittelkontakt_konfidenz"] = "angenommen"; t["konfidenz"] = "angenommen"
    t["quelle"] = "scripts/components/strebe.py, data/params.json (strut_r 45: Platzhalter, strut_end_offset 120, strut_pocket 34), data/layout.json dome.strut_len_mm, docs/parts/knoten.md (Steckmaß 80)"
    d["teilenummer"] = "T1"   # Komponentenname T1_Strebe_A/B in scripts/components/strebe.py
    d["titel"] = f"Kuppelstrebe {typ} (Knoten-zu-Knoten {ks} mm)"
    d["kurz"] = f"Ein Stahlrohr 30 × 30 mm, das zwei Knoten der Kuppel verbindet; Typ {typ} kommt {stk}-mal vor."
    d["hinweis"] = ("Handfelder gefüllt (W60 5a). Die Komponentendatei trägt fremde, nicht committete Änderungen und das Material 'Default', das keinem Katalog-Werkstoff zugeordnet ist: "
                    "darum bleibt das Teil als Gerüst markiert und der Werkstoff steht als 'Default' (Soll: stahl_verzinkt). Profil, Wand und Norm sind angenommen.")
    d["gruppen"] = [{"id": "strebe", "name": "Strebe", "kurz": "Das Stahlrohr zwischen zwei Knoten.", "teile": [t["id"]]}]
    write(comp, d)

def write(comp, d):
    with open(os.path.join(PD, comp + ".json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")

if __name__ == "__main__":
    comps = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(PD, "knoten_*.json")))
    for c in comps:
        knoten(c)
    for c in ("strebe_a", "strebe_b"):
        strebe(c)
    print(len(comps), "Knoten-Dateien und 2 Strebe-Dateien geschrieben")
