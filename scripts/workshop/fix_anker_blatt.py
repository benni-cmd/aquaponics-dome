"""Blatt-Text fuer data/components/fundamentanker.json aus den Parametern und der Messung."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "fundamentanker.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "fundamentanker.sc"))
mass = {b["name"]: b["mass_g"] / 1000 for b in ev["bodies"]}
tot = sum(mass.values())
stahl = tot - mass["Betonpunkt"]
mn, mx = sc.bbox_all(ev)
gap = P["lug_t"] + P["lug_clear"]
z_top = P["lug_hole_z"] - P["clevis_below_hole"]
arme = json.load(open(os.path.join(sc.ROOT, "data", "components", "knoten_arme.json"), encoding="utf-8")) if os.path.exists(os.path.join(sc.ROOT, "data", "components", "knoten_arme.json")) else {}
az = {k: v.get("az_grad") for k, v in arme.items() if v["valenz"] == 4}
bl = {
    "funktion": "Verankert einen der 10 Basisknoten der Kuppel im Erdreich (Ben: Skelett im Boden verankert): Betonpunkt, darauf eine Ankerplatte mit zwei Verbundankern M16 und einer Gabel aus zwei Laschen, in die die Ankerlasche des Basisknotens (60 x 10, Loch D14) mit einem Querbolzen M12 eingehaengt wird.",
    "querschnitt": f"Betonpunkt {P['block_x']:.0f} x {P['block_y']:.0f} x {P['block_z']:.0f} (Oberkante z = {z_top - P['plate_t']:.0f}); Ankerplatte {P['plate_s']:.0f} x {P['plate_s']:.0f} x {P['plate_t']:.0f}; zwei Verbundanker M16 x {P['anchor_len']:.0f} auf der Plattendiagonale (+-{P['anchor_off']:.0f}); Gabel aus zwei Laschen {P['clevis_w']:.0f} x {P['clevis_t']:.0f} x {P['clevis_h']:.0f} mit {gap:.0f} mm Spalt; Loch D14 auf Hoehe z = {P['lug_hole_z']:.0f}.",
    "toleranzen": "Gabelspalt = Knotenlasche 10 + 2 mm Spiel; Lochhoehe und Loch-D gleich der Knotenlasche (Pruefung 15/15, Querpruefung gegen knoten.json); Beton: Bohrloecher D18 fuer die Verbundanker.",
    "ports": [
        ["Anschluss Knotenlasche (Gabel)", "Querbolzen M12x55 ISO 4017, Loch D14 durch beide Laschen", f"x 0, y 0, z {P['lug_hole_z']:.0f} (Lochmitte, Bezug = Knotenmitte); Gabelspalt y +-{gap / 2:.0f}", "Lochachse Y = tangential (waagerecht, senkrecht zur Knotennormalen, umlaufend um die Kuppel); Knotenlasche kommt von oben (+Z)"],
        ["Verbundanker (2 Stueck)", "M16 x 300, Setztiefe ca. 280, Bohrloch D18, chemisch (Verbundmoertel nicht modelliert)", f"x,y = (+{P['anchor_off']:.0f}, +{P['anchor_off']:.0f}) und (-{P['anchor_off']:.0f}, -{P['anchor_off']:.0f}) (Diagonale ++/--), z {z_top:.0f} (Plattenoberkante) bis {z_top - P['anchor_len']:.0f}", "Kopf oben, Schaft nach -Z in den Beton"],
        ["Betonpunkt (Einbau im Erdreich)", f"{P['block_x']:.0f} x {P['block_y']:.0f} x {P['block_z']:.0f}, Oberkante z {z_top - P['plate_t']:.0f}, Unterkante z {z_top - P['plate_t'] - P['block_z']:.0f}", "Mitte x 0, y 0 (unter dem Basisknoten)", "Grube im Erdreich; Verhaeltnis zur Erdflaeche/Fundamentring: Montage"],
        ["Ausrichtung je Basisknoten", "Drehung um Z auf den Azimut des Knotens: X = radial nach aussen", "Azimut je Basisknoten: " + ", ".join(f"n{int(k):02d} {v:.1f} Grad" for k, v in sorted(az.items(), key=lambda kv: int(kv[0]))) if az else "siehe data/components/knoten_arme.json (az_grad)", "Instanz an die Knotenposition (layout.json dome.nodes_list, Wertigkeit 4) setzen"],
    ],
    "verbindungen": ["Ankerplatte auf dem Betonpunkt, Verbundanker = Gewindestange M16 x 300 (8.8) mit Sechskantmutter ISO 4032 und Scheibe ISO 7089 oben, im Modell als Sechskantschraube mit Kopf oben dargestellt (Kopf = Mutter); Platte 15 mm, Loecher D17,5", "Gabellaschen an die Ankerplatte geschweisst (MAG), dann feuerverzinkt [A]", "Querbolzen M12x55 ISO 4017 mit 2 Scheiben ISO 7089 und Mutter ISO 4032 durch Gabel und Knotenlasche", "Betonpunkt: Beton C25/30, Gruendungstiefe frostfrei (Tiefe 600 + Aufbau) nicht nachgewiesen"],
    "abweichung": "Scope-Card: Ankerplatte mit 2 Bolzen, Betonpunkt (Block im Erdreich 400 x 400 x 600 A), Anschlusslaschen zum Basisknoten, Normschrauben: umgesetzt. Hoehenlage: Der Basisknoten sitzt bei z = -14, die Lasche haengt 150 mm unter die Knotenkugel, die Ankerplatte liegt 229 mm unter der Knotenmitte: damit liegt der Betonkopf bei Weltz = -14 - 244 = -258 mm (Gelaende/Fundamentring: Montage pruefen).",
    "montage": ["Grube ausheben (400 x 400 x 600 plus Arbeitsraum), Schalung, Beton C25/30 mit Bohrlochraster einbringen und abbinden lassen", "Bohrloecher D18 setzen, Verbundmoertel einbringen, Verbundanker M16 setzen, Ankerplatte mit Gabel aufsetzen, Muttern/Scheiben anziehen", "Basisknoten mit der Ankerlasche in die Gabel einfuehren, Querbolzen M12 mit Scheiben und Mutter montieren", "Ausrichtung: X radial nach aussen, Lochachse tangential", "Anzugsmomente (Richtwerte [E]): Querbolzen M12 8.8 85 Nm (verspannt die 10-mm-Gabellaschen nicht auf der Knotenlasche: Spalt 12 bleibt frei, Muttern nur handfest plus 1/4 Umdrehung bzw. nach Herstellervorgabe), Verbundanker M16 nach Moertelhersteller (Richtwert 80 Nm)"],
    "werkzeug": "Spaten/Bagger, Schalungsbretter, Betonmischer, Bohrhammer D18, Dosierpistole Verbundmoertel, Schluessel M12/M16, Wasserwaage",
    "stueckliste": ["1 Betonpunkt C25/30 400 x 400 x 600 (0,096 m3, ca. 230 kg)", "1 Ankerplatte S235 250 x 250 x 15 mit 2 Loechern D17,5", "2 Gabellaschen S235 80 x 10 x 140", "2 Gewindestangen M16 x 300 (Verbundanker) mit je 1 Mutter ISO 4032 und 1 Scheibe ISO 7089, Verbundmoertel 2 Kartuschen je 10 Anker [A]", "1 Querbolzen M12x55 ISO 4017 mit 2 Scheiben ISO 7089 und Mutter ISO 4032", "Menge: 10 Anker (je Basisknoten einer): 10 Betonpunkte, 10 Platten, 20 Laschen, 20 Verbundanker, 10 Querbolzen"],
    "lokal": "Betonpunkt vor Ort gegossen; Platte und Laschen vom Metallbauer (Reststuecke S235); Verbundanker aus dem Baustoffhandel oder Gewindestangen M16 mit Ankermoertel.",
    "referenz": "reference/ref-4/ref-5: Anker nicht sichtbar (vergraben bzw. vom Fundamentring verdeckt); Scope-Card fundamentanker; Ben: Skelett im Boden verankert",
    "gewicht_gefuellt": f"Betonpunkt {mass['Betonpunkt']:.0f} kg, Stahlteile {stahl:.1f} kg, gesamt {tot:.0f} kg je Anker (10 Stueck: ca. {10 * tot:.0f} kg)",
    "boxen": [f"fundamentanker: X {mn[0]:.0f} bis {mx[0]:.0f}, Y {mn[1]:.0f} bis {mx[1]:.0f}, Z {mn[2]:.0f} bis {mx[2]:.0f}"],
    "pruefung": ["scripts/workshop/check_fundamentanker.py (Ergebnis renders/components/fundamentanker/check.txt): Block, Platte, Anker, Gabel; QUERPRUEFUNG gegen die Ankerlasche des Knotens (Lochhoehe -159, Loch D14, Gabelspalt 12)", "Kein Bild-Kritiker: der Anker ist in keiner Referenz sichtbar; Spec-Pruefer und Orchestrator-Stichprobe"],
    "offen": ["Statik/Tragfaehigkeit nicht nachgewiesen (Statik ruht): Block, Anker, Laschen sind Annahmen A", "Gruendungstiefe/Frost und Bodenkennwerte offen", "Lage zur Erdflaeche/zum Fundamentring: Der Basisknoten liegt bei z = -14, damit Ankerplatten-Oberkante z = -243 und Betonkopf z = -258 (Welt); das Gelaende (z = 0?) ist nicht definiert -> Montage", "Hebelwirkung: Gabel nimmt nur Querkraefte quer zur Lochachse auf; Zug/Druck in Strebenrichtung ueber die Ankerplatte [A]", "Ausrichtung Lochachse tangential (umlaufend) ist Annahme; im OBJ keine Ankerdetails"],
}
d["blatt"] = bl
d["herkunft_tabelle"] = [
    ["Anzahl 10 (an den 10 Basisknoten)", "10", "OBJ", "layout.json dome.node_valence {4: 10}", "hoch"],
    ["Betonpunkt 400 x 400 x 600", "400x400x600 mm", "A (Scope-Card)", "docs/scope-cards.md fundamentanker nennt das Mass selbst Annahme A, keine Quelle", "niedrig"],
    ["Ankerplatte 250 x 250 x 15", "250x250x15 mm", "A", "Konstruktionspraxis; keine Quelle", "niedrig"],
    ["2 Verbundanker M16 x 300 auf der Diagonale +-75", "M16 x 300", "A (Scope-Card)", "Scope-Card: Ankerplatte mit 2 Bolzen; Groesse Annahme (R01 Statik ruht)", "niedrig"],
    ["Gabel aus 2 Laschen 80 x 10 x 140, Spalt 12", "80x10x140, 12 mm", "A (Scope-Card) + E", "Scope-Card: Anschlusslaschen zum Basisknoten; Spalt = Knotenlasche 10 + 2 (knoten.json)", "mittel"],
    ["Lochhoehe z -159 ab Knotenmitte, Loch D14, Querbolzen M12x55", "z -159, D14, M12", "E + A", "knoten.json: -ball_d/2 + 6 - lug_l + 35 mit lug_l 150 und Lochlage 35 (beide A); Loch D14 durch die M12-Wahl (A); Querpruefung 15/15 prueft die Uebereinstimmung beider Klassen", "mittel"],
    ["Ankerplatte 70 mm unter der Lochmitte (clevis_below_hole)", "70 mm", "A", "Gabelhoehe 140 mit Loch auf halber Hoehe", "niedrig"],
    ["Beton C25/30, 2,4 g/cm3; Stahl S235 7,85 g/cm3", "2,4 / 7,85 g/cm3", "A", "Normwerte; Festigkeitsklasse Annahme", "mittel"],
    ["Azimut je Basisknoten (X radial)", "az je Knoten", "E", "knoten_arme.json (az_grad = atan2(n_y, n_x) der Knotennormalen aus nodes_list)", "hoch"],
    ["Lochachse tangential (umlaufend), Knotenlasche kommt von oben", "tangential", "A", "Annahme der Werkstatt, im OBJ keine Ankerdetails", "niedrig"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("fundamentanker.json gepflegt")
