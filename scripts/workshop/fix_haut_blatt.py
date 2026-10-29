"""Blatt-Inhalt haut_paneel (T40) und haut_profil (T41) in den JSON-Dateien (W19 Schritt 4); Zahlen aus haut_paneel.tri_points und der Messung. Idempotent; danach partsheet.py haut_paneel / haut_profil.
Aufruf: python scripts/workshop/fix_haut_blatt.py"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import haut_paneel as HP

def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))

# ---------------- haut_paneel
p, d = load("haut_paneel")
P = {k: v["wert"] for k, v in d["parameter"].items()}
bl = d.setdefault("blatt", {})
ports, flaechen, massen = [], {}, {}
for typ, T in d["typen"].items():
    strebe, pan, r = HP.tri_points(T["kanten_nominal"], P["edge_inset"])
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"haut_paneel_{typ}.sc"))
    b = ev["bodies"][0]
    flaechen[typ] = b["volume_mm3"] / P["panel_t"] / 1e6
    massen[typ] = b["mass_g"] / 1000
    for k, (i, j) in enumerate(((0, 1), (1, 2), (2, 0))):
        mx, my = (pan[i][0] + pan[j][0]) / 2, (pan[i][1] + pan[j][1]) / 2
        L = math.dist(pan[i], pan[j])
        ports.append([f"{typ} Kante e{k} (P{i}P{j}): Auflage auf Randprofil", f"Randkante {L:.0f} mm, Strebe {T['kanten_nominal'][k]} mm", f"Kantenmitte x {mx:.0f}, y {my:.0f}, z 0..{P['panel_t']:g} (Bezug = Inkreismittelpunkt)", f"Kante liegt {P['edge_inset']:g} mm vor der Strebenachse auf der Kappe T41 (Kappe 30 breit: 15 mm Auflage je Seite); Normale in der Plattenebene nach aussen"])
bl["varianten"] = [f"haut_paneel_{t}" for t in d["typen"]]
bl["funktion"] = "Transparente Haut der Kuppel: dreieckiges Paneel (Polycarbonat-Doppelstegplatte 8 mm) je Kuppelfeld; haelt Wind und Regen ab und laesst Licht durch; Befestigung ueber das Randprofil T41 auf den Streben."
bl["querschnitt"] = "Ebenes Dreieck, 8 mm dick (Doppelstegplatte), Randabstand 15 mm vor der Strebenachse (Strebendreieck um den Inkreismittelpunkt mit Faktor (r - 15)/r verkleinert); Typ AAB = Strebenlaengen 3279 / 3279 / 3708 (30 Felder), Typ BBB = 3708 x 3 (10 Felder); Hohlkammern der Doppelstegplatte nicht modelliert (Vollkoerper)."
bl["toleranzen"] = "Fuge zum Randprofil und Dehnung (Polycarbonat ca. 0,07 mm/m/K) nicht modelliert; Aussenflaeche eben (die Kuppelfelder sind plan, die Streben bilden die Kanten)."
bl["ports"] = ports
bl["verbindungen"] = ["Paneelkante liegt auf dem Randprofil T41 (Aluminium-Kappe 30 x 8) ueber der Strebe, 15 mm Auflage je Seite; Befestigung der Kappe auf der Strebe (Schrauben/Klemmung) und Dichtband nicht modelliert [A]", "Tuerfelder: die zwei Basisfelder am Tuerknoten brauchen einen Tuerausschnitt 1000 x 2000 (Zuschnitt = spaeterer Schritt, nicht modelliert)"]
bl["abweichung"] = "keine OBJ-Vorgabe (das OBJ-Dom hat keine Haut); Dreiecksseiten aus den Strebenlaengen layout.json dome.strut_len_mm (3279 A / 3708 B, gemessene Knotenabstaende 3278,8-3279,8 bzw. 3707,6-3708,9)."
bl["montage"] = ["Randprofile T41 auf alle 65 Streben setzen und befestigen", "Paneele je Feld auflegen (Typ AAB/BBB nach Feld, Lage aus den Knoten), Kanten auf die Kappen, Klemmleisten/Dichtband setzen", "Tuerfelder mit Ausschnitt zuschneiden"]
bl["werkzeug"] = "Akkuschrauber, Dichtband, Hebezeug/Helfer (ein Paneel bis ca. 9 kg)"
bl["stueckliste"] = [f"T40 Haut-Paneel Typ AAB: {d['typen']['AAB']['anzahl_voll']} voll + {d['typen']['AAB']['anzahl_mit_tuerausschnitt']} mit Tuerausschnitt = {d['typen']['AAB']['anzahl_felder']}; Flaeche {flaechen['AAB']:.2f} m2, {massen['AAB']:.1f} kg",
                     f"T40 Haut-Paneel Typ BBB: {d['typen']['BBB']['anzahl_voll']} voll + {d['typen']['BBB']['anzahl_mit_tuerausschnitt']} mit Tuerausschnitt = {d['typen']['BBB']['anzahl_felder']}; Flaeche {flaechen['BBB']:.2f} m2, {massen['BBB']:.1f} kg",
                     f"Gesamtflaeche Haut ca. {sum(flaechen[t] * d['typen'][t]['anzahl_felder'] for t in flaechen):.0f} m2 (40 Felder)"]
bl["lokal"] = "Doppelstegplatten 8 mm sind Baumarktware (Gewaechshausbau); Zuschnitt auf Dreiecke selbst oder per Zuschnittservice [A, nicht recherchiert]; Folie als billige Variante (R11)."
bl["pruefung"] = ["scripts/workshop/check_haut.py (27/27 PASS, Ergebnis renders/components/haut_paneel/check.txt): Felderzahl (Euler), Typen, Dicke 8, Flaeche gegen Heron-Rechnung, Randkanten, Randabstand 15 mm (Inkreisradius), Masse", "Bild renders/components/haut_paneel/haut_paneel_AAB-01-draufsicht.png (und BBB); kein Bild-Kritiker, kein Spec-Pruefer (Wochenlimit, W19 Auftrag)"]
bl["kritiker"] = "offen (kein Pruefer-Lauf, Wochenlimit)"
bl["offen"] = ["Tuer: die zwei Basisfelder am Tuerknoten 22 (Azimut 167,2) tragen den Tuerausschnitt; Zuschnittform nicht modelliert; Lage der Tuer im Dom (Knoten statt Feldmitte) mit Montage/Orchestrator pruefen", "Hohlkammern, Dichtband, Klemmleisten, Lueftungsklappen nicht modelliert; Material/Preis/UV nicht recherchiert (R11 offen)", "Paneele sind eben; die Streben liegen auf der Kugel, die Felder sind plan (Pfeilhoehe zur Kugel bei 3,7 m Kante ca. 0,2 m): Aussenflaeche haengt an den Streben, Einbau durch die Montage", "Plattenlage: Inkreismittelpunkt des Strebendreiecks (Strebenachsen), nicht Schwerpunkt; Z 0 = Innenseite"]
d["herkunft_tabelle"] = [
    ["Dreieckstypen AAB (30) und BBB (10), 40 Felder", "40 Felder", "OBJ", "layout.json dome.nodes_list + strut_len_mm: 65 Streben aus Knotenabstaenden, Dreiecke = Knotentripel (V - E + F = 1)", "hoch"],
    ["Strebenlaengen 3279 (A) / 3708 (B)", "3279 / 3708 mm", "OBJ", "layout.json dome.strut_len_mm; gemessene Knotenabstaende 3278,8-3279,8 / 3707,6-3708,9", "hoch"],
    ["Doppelstegplatte 8 mm, transparent", "8 mm", "A", "docs/decisions.md D35, R11 (Domerama, Northern Homestead: Polycarbonat/Folie auf Kanalprofilen); 6 mm ca. 80 % Licht, 16 mm 65 %", "niedrig"],
    ["Rand 15 mm vor der Strebenachse", "15 mm", "A", "R11: halbe Kappenbreite 30/2", "niedrig"],
    ["Dichte 0,19 g/cm3", "0,19 g/cm3", "A", "Flaechengewicht ca. 1,5 kg/m2 (Herstellerrichtwert, nicht recherchiert) / 8 mm", "niedrig"],
    ["Opazitaet 0,35 im Viewer", "0,35", "A", "R11/D35", "niedrig"],
    ["Tuer bei Azimut 167 (Basisknoten 22) beruehrt 2 Felder", "2 Felder", "OBJ + E", "docs/components.md (Tuer Azimut 167 im OBJ, 1000 x 2000); Basisknoten 22 hat Azimut 167,2: beide Basisfelder am Knoten (149,2 BBB und 185,2 AAB) beruehrt", "mittel"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------- haut_profil
p, d = load("haut_profil")
bl = d.setdefault("blatt", {})
ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "haut_profil.sc"))
b = ev["bodies"][0]
mA, mB = b["mass_g"] / 1000, b["mass_g"] / 1000 * 3708 / 3279
bl["funktion"] = "Randprofil der Kuppelhaut: Aluminium-Kappe auf jeder Strebe, auf der die Paneelkanten beider Nachbarfelder aufliegen (je 15 mm Auflage) und gehalten werden."
bl["querschnitt"] = f"U-Profil 30 breit x 8 hoch, Wand 2 mm, offen nach unten (sitzt auf der Strebe), Querschnitt 84 mm2; Laenge A 3279 / B 3708 als Konfiguration; Masse A {mA:.2f} kg, B {mB:.2f} kg."
bl["toleranzen"] = "Laenge = Knoten-zu-Knoten-Mass (Knotenversatz nicht abgezogen, A); Wand 2 mm Strangpressprofil."
bl["ports"] = [["Auflage Strebe", "U-Profil Innenbreite 26 mm", "Z 0 (Unterkante), y +-13 (Innenwaende)", "Kappe sitzt auf dem Strebenrohr, offene Seite nach unten"], ["Auflage Paneel", "Oberseite 30 mm breit", "Z 8 (Oberkante), y +-15", "Paneelkanten beider Nachbarfelder liegen je 15 mm auf der Kappe"]]
bl["verbindungen"] = ["Befestigung auf der Strebe (Schrauben/Klemmung) und Dichtband zwischen Kappe und Paneel nicht modelliert [A]"]
bl["abweichung"] = "keine OBJ-Vorgabe (das OBJ-Dom hat keine Haut)."
bl["montage"] = ["Kappe auf die Strebe legen, ausrichten, befestigen", "Paneele auflegen, Dichtband einlegen"]
bl["werkzeug"] = "Saege (Zuschnitt), Akkuschrauber"
bl["stueckliste"] = [f"T41 Haut-Randprofil Alu-Kappe 30 x 8 x 2: 30 x Laenge 3279 (A) + 35 x Laenge 3708 (B) = 65 Stueck, gesamt ca. {30 * mA + 35 * mB:.0f} kg"]
bl["lokal"] = "Aluminium-Kappenprofile gibt es als Strangpressprofil (Gewaechshausbau, Foliensysteme); Standardlaenge 6 m, Zuschnitt auf 3279/3708 [A, nicht recherchiert]."
bl["pruefung"] = ["scripts/workshop/check_haut.py (27/27 PASS): Laenge A/B, Breite, Hoehe, Querschnitt 84 mm2, Masse", "Bilder renders/components/haut_profil/ (Iso, Querschnitt); kein Bild-Kritiker, kein Spec-Pruefer (Wochenlimit)"]
bl["kritiker"] = "offen (kein Pruefer-Lauf, Wochenlimit)"
bl["offen"] = ["Befestigung der Kappe auf der Strebe, Dichtband und Eckverbindung an den Knoten nicht modelliert", "Profilform (U 30 x 8, Wand 2) ist Annahme A; R11 nennt nur Breite/Hoehe", "Laenge ohne Knotenversatz (Knoten-zu-Knoten-Mass)"]
d["herkunft_tabelle"] = [
    ["Kappe 30 x 8 mm", "30 x 8 mm", "A", "R11: Aluminium-Kappe 30 mm breit, 8 mm hoch", "niedrig"],
    ["Wand 2 mm, U-Profil offen nach unten", "2 mm", "A", "Strangpressprofil-Annahme", "niedrig"],
    ["Laengen A 3279 / B 3708, 65 Stueck", "30 x A + 35 x B", "OBJ", "layout.json dome.strut_len_mm", "hoch"],
    ["Aluminium EN AW-6063, 2,7 g/cm3", "2,7 g/cm3", "A", "Standardwerkstoff Strangpressprofil", "niedrig"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("haut_paneel/haut_profil Blatt-Inhalt gepflegt")
