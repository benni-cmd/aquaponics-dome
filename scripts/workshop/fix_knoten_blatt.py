"""Blatt-Text fuer data/components/knoten.json (Ports, Gewichte, Stueckliste, Herkunft) aus den Parametern und der Messung."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import knoten as kn
p = os.path.join(sc.ROOT, "data", "components", "knoten.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
N, _ = kn.nodes()
nb = kn.neighbours(N, P["neighbor_tol"])
arme = json.load(open(os.path.join(sc.ROOT, "data", "components", "knoten_arme.json"), encoding="utf-8"))
reps = {"6": 0, "5": 1, "4": 16}
ports, gew, boxes = [], [], []
tot = 0.0
for val, i in reps.items():
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"knoten_{val}_n{i + 1:02d}.sc"))
    m = sum(b["mass_g"] for b in ev["bodies"]) / 1000
    mn, mx = sc.bbox_all(ev)
    boxes.append(f"knoten_{val} (n{i + 1:02d}): X {mn[0]:.0f} bis {mx[0]:.0f}, Y {mn[1]:.0f} bis {mx[1]:.0f}, Z {mn[2]:.0f} bis {mx[2]:.0f}")
    cnt = sum(1 for n in N if n["valence"] == int(val))
    gew.append(f"Knoten {val}-wertig: {m:.2f} kg je Knoten (Stahl S235), {cnt} Stueck = {m * cnt:.1f} kg")
    tot += m * cnt
    a = arme[str(i + 1)]
    for k, ar in enumerate(a["arme"], 1):
        u = ar["u"]
        L = P["strut_end_offset"] + P["hub_insert"]
        ports.append([f"knoten_{val} n{i + 1:02d}: Steckarm {k} (zu Knoten n{ar['nachbar']:02d}, Strebe {ar['typ']} {ar['laenge']:.0f})", "Rechteckrohr 23,6 x 23,6 x 3, steckt 80 mm in die Strebe 30 x 30", f"Spitze x {u[0] * L:.0f}, y {u[1] * L:.0f}, z {u[2] * L:.0f}; Strebenende bei {P['strut_end_offset']} mm", f"Richtung u = ({u[0]:.4f}, {u[1]:.4f}, {u[2]:.4f}), Kipp {ar['kipp_gegen_tangentialebene']:.1f} Grad gegen die Tangentialebene"])
    if val == "4":
        ports.append([f"knoten_4: Ankerlasche (Basisknoten)", f"Lasche {P['lug_w']:.0f} x {P['lug_t']:.0f} x {P['lug_l']:.0f}, Loch D{P['lug_hole']:.0f} fuer M12", f"x 0, y 0, z {-P['ball_d'] / 2 + 6 - P['lug_l'] + 35:.0f} (Lochmitte; Lasche haengt unter der Knotenkugel)", "Anschluss Fundamentanker, Lochachse tangential, Richtung -Z"])
ports.append(["alle 26 Knoten", "Armrichtungen je Knoten", "data/components/knoten_arme.json (Richtung u, Nachbar, Strebenart, Kipp je Arm)", "Montage: Instanz an layout.json dome.nodes_list-Position, Drehung wie die Streben (layout_rot um Z)"])
bl = {
    "funktion": "Verbindet die Streben der 2V-Kuppel: Knotenkugel D100 mit 4, 5 oder 6 Steckarmen in den Strebenrichtungen (Nachbarknoten aus layout.json); jede Strebe wird 80 mm auf einen Steckarm geschoben und mit einem Querbolzen M10 gesichert; die 10 Basisknoten tragen eine Ankerlasche fuer den Fundamentanker.",
    "querschnitt": f"Kugel D100; Steckarm Rechteckrohr 23,6 x 23,6 x 3 (passt in die Strebe 30 x 30 x 3), Laenge {P['strut_end_offset'] + P['hub_insert'] - (P['ball_d'] / 2 - P['arm_root']):.0f} mm ab Kugel (Strebenende bei {P['strut_end_offset']}, Stecktiefe {P['hub_insert']}); Querbolzen M10x55 mit 2 Scheiben und Mutter {P['bolt_dist']} mm hinter dem Strebenende; Ankerlasche {P['lug_w']:.0f} x {P['lug_t']:.0f} x {P['lug_l']:.0f} (nur 4-wertig).",
    "toleranzen": "Armrichtung = Richtung zum Nachbarknoten (Pruefung <= 0,5 Grad, gemessen 0,00 Grad); Steckarm 0,2 mm Spiel je Seite zur Strebe; Kugel D100 +-0,3.",
    "ports": ports,
    "verbindungen": ["Arme an die Knotenkugel geschweisst (MAG, 4 mm Ueberlappung), danach feuerverzinkt [A]", "Strebe auf Steckarm: Querbolzen M10x55 ISO 4017 mit 2 Scheiben ISO 7089 und Mutter ISO 4032, Loch D11, je Strebe 1 Bolzen", "Ankerlasche an die Kugel geschweisst, Loch D14 fuer M12 zum Fundamentanker (Normteil dort)"],
    "abweichung": "ABWEICHUNG von der Scope-Card (zwei Knotenplatten): Die Strebenrichtungen sind wegen des Sehnenwinkels der 2V-Kuppel um 16 bis 18 Grad gegen die Tangentialebene (Plattenebene) geneigt (Abstand Knoten-zu-Knoten 3279/3708 auf R 6000); flache Platten mit Steckarmen in der Plattenebene wuerden die Arme durchdringen oder verlangen gebogene Arme. Darum Knotenkugel mit Steckhuelsen (R02: Huelsen-/Sternnaben als Bauart genannt). Anzahl, Wertigkeit und Strebenrichtungen exakt aus layout.json (26 Knoten, 65 Streben, 10/6/10).",
    "montage": ["Arme an die Knotenkugel schweissen (Vorrichtung nach den Armwinkeln aus knoten_arme.json), verzinken lassen", "Streben auf die Steckarme schieben (80 mm), Loch durch Strebe und Steckarm bohren bzw. vorgebohrt ausrichten, Querbolzen M10 mit Scheiben und Mutter anziehen", "Basisknoten: Ankerlasche mit dem Fundamentanker verschrauben (M12)", "Reihenfolge: Basisring, dann Reihe fuer Reihe nach oben, Apex zuletzt"],
    "werkzeug": "Schweissgeraet und Vorrichtung (Armwinkel), Bohrmaschine D11, Schluessel M10, Hebezeug/Geruest",
    "stueckliste": [f"Je Knoten: 1 Kugel D100, n Steckarme (n = Wertigkeit, Rechteckrohr 23,6 x 23,6 x 3, Laenge 154 ab Kugel), n Querbolzen M10x55 ISO 4017, 2n Scheiben ISO 7089, n Muttern ISO 4032; Basisknoten zusaetzlich 1 Ankerlasche 60 x 10 x 150", "Gesamt 26 Knoten: 26 Kugeln, 130 Steckarme (= 2 x 65 Streben), 130 Bolzen M10x55, 260 Scheiben, 130 Muttern, 10 Ankerlaschen", "Knoten: 10 vierwertig (Basis), 6 fuenfwertig, 10 sechswertig; Dateien designs/components/knoten_<wertigkeit>_n<nr>.sc (26) und Repraesentanten knoten_4/5/6.sc"],
    "lokal": "Kugeln als Vollkugel oder Rohrstueck mit Kappen aus dem Stahlhandel; Steckarme aus Rechteckrohr 25 x 25 x 3 abgedreht/abgeschliffen; Schweissen und Verzinken beim Metallbauer; Ersatz: Holzstreben mit Bandstahl-Nabe (R02 Bauart D).",
    "referenz": "ref-4/ref-5: Knoten in den Referenzen nicht erkennbar (Streben treffen sich ohne sichtbare Nabe); data/layout.json dome.nodes_list; docs/research/R02.md",
    "varianten": ["knoten_6", "knoten_5", "knoten_4"],
    "render_dirs": ["knoten_4", "knoten_5", "knoten_6"],
    "gewicht_gefuellt": " | ".join(gew) + f" | Summe aller Knoten ca. {tot:.0f} kg",
    "boxen": boxes,
    "pruefung": ["scripts/workshop/check_knoten.py (Ergebnis renders/components/knoten_6/check.txt): Anzahl 10/6/10, Armzahl = Wertigkeit, Armrichtung je Knoten <= 0,5 Grad, Bolzen je Strebe, Ankerlasche nur Basisknoten", "Kein Bild-Kritiker: die Knoten sind in keiner Referenz sichtbar; Spec-Pruefer und Orchestrator-Stichprobe"],
    "offen": ["Tragfaehigkeit nicht nachgewiesen (Statik ruht): Kugel D100, Steckarm 23,6 x 3 und M10 sind Annahmen A", "ABWEICHUNG von der Scope-Card (Platten statt Kugel) begruendet, Entscheidung beim Orchestrator", "Tuerknoten: Sonderanschluss fuer den Sturz (Montage/Tuer-Klasse); Knoten im Tuer-Dreieck nur als Standardknoten gebaut", "strut_end_offset 120 und hub_insert 80 sind Annahmen A (Scope-Card)", "Strebenquerschnitt: 30 x 30 x 3 angenommen; das OBJ gibt 30 x 30 ohne Wand, die Integrator-Strebe ist ein Vollzylinder", "Armrichtungen liegen im OBJ-Frame (layout.json); die Montage dreht wie die Streben"],
}
d["blatt"] = bl
d["herkunft_tabelle"] = [
    ["Knotenzahl 26: 10 vierwertig, 6 fuenfwertig, 10 sechswertig", "26 (10/6/10)", "OBJ", "layout.json dome.nodes (26), node_valence {6:10, 5:6, 4:10}", "hoch"],
    ["Knotenpositionen (Ursprung je Instanz)", "26 Positionen", "OBJ", "layout.json dome.nodes_list (x, y, z)", "hoch"],
    ["Armrichtungen = Richtung zum Nachbarknoten (65 Streben)", "26 x 4-6 Richtungen", "OBJ + E", "Nachbarn aus Knotenabstand 3279/3708 +-40 (alle 65 Streben, Wertigkeit stimmt bei allen 26 Knoten); knoten_arme.json", "hoch"],
    ["Bauart Huelse/Kugel statt Platten", "Kugel D100", "R02 + A", "R02: Huelsen-/Sternnaben, flachgedrueckte Enden fuer 12 m ungeeignet; Kugel wegen Strebenneigung 16-18 Grad (Abweichung von der Scope-Card)", "mittel"],
    ["strut_end_offset 120 mm, hub_insert 80 mm", "120 / 80 mm", "A", "Scope-Card (Annahme A); R02 nennt keine Masse fuer Plattennaben", "niedrig"],
    ["Steckarm Rechteckrohr 23,6 x 23,6 x 3", "23,6 x 3 mm", "E + A", "passt in die Strebe 30 x 30 x 3 (Innenmass 24); Strebenwand Annahme", "niedrig"],
    ["Querbolzen M10x55 ISO 4017, Scheiben ISO 7089, Mutter ISO 4032, Loch D11", "M10x55", "A + Normteil", "R02: Bolzen M10 als Annahme; ISO-Normteile aus der SolidCraft-Bibliothek (parts.insert); Bolzenmass fuer grosse Streben nicht gefunden", "niedrig"],
    ["Kugel D100, Arme 4 mm in der Kugel (Schweissung)", "D100 / 4 mm", "A", "keine Quelle zum Nabenmass (R02 Luecke)", "niedrig"],
    ["Ankerlasche 60 x 10 x 150 mit Loch D14 (nur Basisknoten)", "60x10x150, D14", "Scope-Card + A", "Scope-Card fundamentanker: Anschlusslaschen zum Basisknoten; Mass Annahme", "niedrig"],
    ["Werkstoff Stahl S235 feuerverzinkt, 7,85 g/cm3", "7,85 g/cm3", "A", "ueblicher Baustahl; ref-4/5 helle Metallknoten", "mittel"],
    ["Kippwinkel der Arme gegen die Tangentialebene (16-18 Grad bei Strebe A/B)", "15,9 / 18,0 Grad", "E", "knoten_arme.json: asin(u.n) je Arm, L/2R = 0,27 (Sehnenwinkel)", "hoch"],
    ["Anzahl Teile: 130 Arme, 130 Bolzen, 260 Scheiben, 130 Muttern, 10 Laschen", "siehe Stueckliste", "E", "Summe der Wertigkeiten = 2 x 65 Streben", "hoch"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("knoten.json gepflegt")
