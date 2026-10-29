"""NICHT ERNEUT AUSFUEHREN ohne danach fix_tisch_blatt4.py (haengt Herkunftszeilen an). Blatt nft_tisch Rev. B (W16, D18, 29.10. ~17:40): Rinnenlaenge je Reihe, Portal-/Auslegerbock, schraege Rohre; Ports, Stueckliste, Herkunft, Abweichung, offene Fragen aus tisch_geom.py berechnet.
Aufruf: python scripts/workshop/fix_tisch_blatt3.py <check_tisch-PASS> <check_fit-PASS>; danach partsheet.py nft_tisch."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

n_t, n_f = sys.argv[1], sys.argv[2]
p = os.path.join(sc.ROOT, "data", "components", "nft_tisch.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
bl = d["blatt"]
Gs = {t: TG.geometry(t, P, d["typen"][t]) for t in ("aussen", "mitte", "innen")}
zrow = lambda G, x: G["zc"] - (x - G["rows"][0]["xc"]) * G["slope"]
T18 = TG.T18
kk = math.sqrt(1 + T18 ** 2)

def fmt(v):
    return f"{v:.0f}"

# --- Typen: Rinnenlaengen je Reihe statt eine Laenge
for t, G in Gs.items():
    T = d["typen"][t]
    T["laenge"] = " / ".join(str(r["L"]) for r in G["rows"]) + " (je Reihe)"
    T["herkunft"] = T["herkunft"].split(" || ")[0] + f" || Rinnenlaenge je Reihe = 2 x (ap x tan 18 Grad - corner_gap) - Ueberstaende {TG.E_IN + TG.E_OUT:.0f} (D18); Tischmitte ap_c {T['ap_c']} mm ({T['ap_c_herkunft'][:3]})"
d["quelle_masse"] = "data/layout.json hydro_tables, ibc_beds, pool; Rinnenlaenge je Reihe aus der Zehneck-Seite (D18, docs/jobs/W16-nft-tisch-passung.md); Beetbreite aus data/components/ibc_beet.json"

# --- Textbloecke
bl["funktion"] = bl["funktion"].replace("Tragt n NFT-Rinnen", "Traegt n NFT-Rinnen") + " Rev. B (W16/D18): jede Reihe hat ihre eigene Rinnenlaenge (Zehneck-Seite minus 2 x corner_gap minus Ueberstaende), Verteiler und Sammelrohr laufen schraeg entlang der Sektorgrenze, die Beine stehen ausserhalb der Beete (Portalbock) bzw. ausserhalb des Pools (Auslegerbock innen)."
bl["querschnitt"] = ("Mitte/aussen: Portalbock aus Rechteckrohr verzinkt: Beine 40x40x3, Querholm 40 x 60 x 3 (Hoehe 60) ueber die Beet-Aussenbreite, Querstrebe 40x40x3 auf Z 800 (ueber den Pflanzen), Diagonalen Flachstahl 25x3 gekreuzt, Fussplatten 100x100x5 mit 2 x M8. "
                     "Innen: Auslegerbock: je Bock ein Pfosten 40x40x3 ausserhalb des Beckenrands, Kragarm 40 x 60 x 3 ueber das Wasser, Laengsstrebe auf Z 400 unter dem Kragarm. Rinnen: Instanzen nft_rinne_<typ>_r<k> (eigene Laenge je Reihe), Phase 0 / pitch/2 abwechselnd.")
bl["toleranzen"] = ("Rinnenunterkante = Holm-/Kragarm-Oberkante an jedem Bock (Pruefung +-1 mm); Gefaelle 1,5 % +-0,05 %; Rinnenhoehe Z +-1,5 mm; Lochlage je Rinne +-1,5 mm zur Rechnung; Abstand zwischen benachbarten Tischen an der Ecke >= corner_gap (100 mm; gemessen 171-190 mm); Beine/Fussplatten >= 30 mm von jedem Beet-Rechteck (leg_clearance 60 mm sollwert). "
                    "Gewichte: Summe je Koerper nach Werkstoff (Stahl 7,85, PVC 1,4 g/cm3; die Messung am .sc enthaelt auch die verknuepften Rinnen).")

ports = []
for t, G in Gs.items():
    zi = sum(zrow(G, r["xc"] - r["L"] / 2) + 70 for r in G["rows"]) / len(G["rows"])
    za = sum(zrow(G, r["xc"] + r["L"] / 2) + 20 for r in G["rows"]) / len(G["rows"])
    y1 = G["Wt"] / 2 + 60                                     # offenes Rohrende: radial innen (+Y)
    xh = -((G["apc"] - y1) * T18 - G["gap"]) + 12.5 * kk
    xs = ((G["apc"] - y1) * T18 - G["gap"]) - 25 * kk
    ports.append([f"{t}: Zulauf Tisch (Verteilerrohr D25 offen, +Y-Ende, schraeg)", "Rohr d25, Wand 3 (Anschluss Rohr/Schlauch)", f"x {fmt(xh)}, y {fmt(y1)}, z {fmt(zi)} (Achse laeuft schraeg: dx/dy = +tan 18 Grad, entlang der Sektorgrenze)", "Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y, 18 Grad zur Y-Achse geneigt); Rohr d25 (etwa DN20)"])
    ports.append([f"{t}: Ablauf Tisch (Sammelrohr d50 offen, +Y-Ende, schraeg)", "Rohr d50, Wand 3 (etwa DN40)", f"x {fmt(xs)}, y {fmt(y1)}, z {fmt(za)} (Achse dx/dy = -tan 18 Grad)", "Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal)"])
    xs_list = ", ".join(fmt(r["xc"] - r["L"] / 2 - 29 - P["hose_gap"]) for r in G["rows"])
    ports.append([f"{t}: Verteiler-Stutzen je Rinne (n={G['n']})", "Schlauch ID 16, Durchfluss je Rinne 0,5 l/min (R06)", f"x {xs_list} (Stutzenspitze je Reihe), y = Rinnenmitte, z ca. {fmt(zi)}", "aus Verteiler, Richtung +X"])
    legs = "; ".join(f"x {fmt(x)} / y {fmt(y)}" for (x, y) in G["legs"])
    ports.append([f"{t}: Fussplatten-Anker", "M8, 2 Schrauben je Platte (100 x 100 x 5), Loch D9, Diagonalversatz +-35", f"Fusspunkte z 5 an: {legs}", "Befestigung auf dem Boden/Betonpunkt, Richtung -Z"])
bl["ports"] = ports
bl["verbindungen"] = [
    "Beine an Fussplatte und Querholm/Kragarm: geschweisst (MAG), danach verzinkt [A]",
    "Fussplatten: 2 Schrauben M8x30 (hex_bolt) je Platte in den Boden/Betonpunkt, Loch D9; Kragarm-Pfosten innen mit Verbundankern (Kippmoment ca. 165 Nm, Statik nicht nachgewiesen)",
    "Diagonalen (nur Portal): je Ende Schraube M6x40 mit Mutter durch das Bein",
    "Rinnenhalter: L-Blech 3 mm, 25 x 25 x 25, je Rinnenseite und Bock, Schraube M5x12",
    "Verteiler: schraeges Rohr d25 mit Stutzen D16 (Verklebung/Schweissen), Schlaeuche ID 16 auf Tuelle und Stutzen; Sammelrohr d50 schraeg mit Muffen d40/d32 auf den Ablaufstutzen",
]
holes = {t: sum(r["n_holes"] for r in G["rows"]) for t, G in Gs.items()}
tot_h = holes["innen"] * 10 + holes["mitte"] * 6 + holes["aussen"] * 8
bl["abweichung"] = ("layout.json hydro_tables liefert je Ring nur ein Beispiel (Reihen ap 1733/1995 innen, 2987-3775 Mitte, 4888/5176 aussen) mit gleicher Rinnenlaenge 1304/1983/3232; diese Laengen sind groesser als die Zehneck-Seite 2 x ap x tan 18 Grad der Reihe (innen 1126/1296, Mitte 1916-2429, aussen 3198-3572) und kollidierten an den Ecken (Ben-Fund 29.10.). "
                    "Rev. B folgt D18: Rinnenlaenge je Reihe = Zehneck-Seite - 2 x corner_gap (100) - Ueberstaende (Zulaufseite 169, Ablaufseite 79); Ergebnis innen 678/848, Mitte 1468/1639/1810/1981, aussen 2750/2937/3124 mm. "
                    "Folge: Topfloecher je Tisch innen " + str(holes["innen"]) + " statt 10, Mitte " + str(holes["mitte"]) + " statt 28, aussen " + str(holes["aussen"]) + " statt 36; gesamt " + str(tot_h) + " statt 556 (check_nft_fit.py). Tischmitte liegt auf der Beetmitte (Mittel der Beetradien: aussen 5209, innen-Beet 3343) und weicht von den OBJ-Reihen um 33-38 mm ab (Annahme A, Layout/Integrator). "
                    "Die Tisch-Beine des OBJ stehen nicht im Layout (Platten ohne Beine). Die Z-Hoehen bleiben (innen 840, Mitte/aussen 1300). Ausrichtung: X tangential gegen den Uhrzeigersinn (+X Sammelrohr/tiefes Ende), Y radial nach INNEN; die Instanz wird mit yaw = Azimut + 90 Grad (= yaw der OBJ-Tische in layout.json hydro_tables) auf die Sektorachse bei ap_c gesetzt, aussen liegt dann -Y. Mit yaw = Azimut - 90 Grad waere die Konvention gespiegelt (Fehler des ersten Kritiker-Bildes, W16).")
bl["montage"] = [
    "Bock am Boden ausrichten: Portal ausserhalb der Beete bzw. Pfosten ausserhalb des Pools, Fussplatten mit M8 / Verbundankern verschrauben",
    "Querstrebe und Laengsstreben einsetzen, Diagonalen verschrauben (Portal)",
    "Rinnen auf die Querholme/Kragarme legen (Zulaufende hoeher), Halteclips M5 setzen",
    "Zulaufverteiler schraeg entlang der Sektorgrenze haengen, Schlaeuche ID 16 auf Stutzen und Tuellen",
    "Sammelrohr mit Muffen auf die Ablaufstutzen stecken, Gefaelle kontrollieren (1,5 %)",
]
# Stueckliste
lines = []
for t, G in Gs.items():
    x1, x2 = G["xb"]
    n = G["n"]
    zb = [zrow(G, x) - P["holm_h"] - P["foot_t"] for x in G["xb"]]
    if G["art"] == "portal":
        lines.append(f"{t}: Beine 4 x 40x40x3: Laenge {fmt(zb[0])} / {fmt(zb[1])}, Beinabstand y {fmt(2 * G['yl'])}; Querholm 40x60x3 x 2: Laenge {fmt(2 * G['yl'] + P['leg_w'])}; Querstrebe 40x40x3 x 2: Laenge {fmt(2 * G['yl'] - P['leg_w'])}; Laengsstreben 40x40x3 x 2: Laenge {fmt(x2 - x1 - P['leg_w'])}; Diagonalen 25x3 x 4; Laengsdiagonalen 25x3 x 2; Fussplatten 100x100x5 x 4")
    else:
        y_in = G["Wt"] / 2 + P["holm_overhang"]
        lines.append(f"{t}: Pfosten 2 x 40x40x3: Laenge {fmt(zb[0])} / {fmt(zb[1])}; Kragarm 40x60x3 x 2: Laenge {fmt(y_in - G['yl'] + P['leg_w'] / 2)}; Laengsstrebe 40x40x3 x 1: Laenge {fmt(x2 - x1 - P['leg_w'])} (Z 400); Laengsdiagonale 25x3 x 1; Fussplatten 100x100x5 x 2")
    lines.append(f"   Rinnen ({n}): " + ", ".join(f"{r['L']} mm / {r['n_holes']} Loecher" for r in G["rows"]) + f"; Verteiler d25 schraeg: Laenge {fmt((G['Wt'] + 120) * kk)}; Sammelrohr d50 schraeg: Laenge {fmt((G['Wt'] + 120) * kk)}")
bl["stueckliste"] = ["Pro Tisch je Typ (Laengen in mm):"] + ["  " + x for x in lines] + [
    "Je Bock (Portal): 2 Beine, 1 Holm, 1 Querstrebe, 2 Diagonalen, 2 Fussplatten, 4 Schrauben M8x30, 4 Schrauben M6x40 + 4 Muttern M6, 2 Rinnenhalter je Rinne mit Schraube M5x12; Bock-Anzahl 2 je Tisch. Je Bock (Ausleger): 1 Pfosten, 1 Kragarm, 1 Fussplatte, 2 Schrauben M8x30, 2 Rinnenhalter je Rinne.",
    "Dabei: 4 Duebel/Anker M8 je Bock (Boden; innen Verbundanker), je 1 Endstopfen d25 und d50 je Tisch (-Y-Rohrende)"]
bl["pruefung"] = [
    f"scripts/workshop/check_nft_tisch.py ({n_t}/{n_t} PASS, Ergebnis renders/components/nft_tisch_innen/check.txt): Rinnenzahl, Abstand, Laenge je Reihe, Lochlage, Zickzack pitch/2, Gefaelle, Hoehe, Auflage, Boecke, Beinlage, Verteiler/Sammelrohr an der Sektorgrenze",
    f"scripts/workshop/check_nft_fit.py ({n_f}/{n_f} PASS, Ergebnis renders/components/nft_tisch_innen/check_fit.txt): reine Geometrie fuer alle 24 Tische: Rinne + Ueberstaende + 2 x corner_gap <= Zehneck-Seite, Footprint-Abstand benachbarter Tische >= 100 (gemessen 171-190), Beine >= 30 mm ausserhalb jedes Beet-Rechtecks, Pfosten ausserhalb des Pools",
    "Bild-Kritiker (Ecke Draufsicht/Iso, Querschnitt Bock + Beet, Innen/Aussen) und Spec-Pruefer: Runden siehe docs/workshop-log.md (W16)",
]
bl["offen"] = [
    "Statik der Portal-/Auslegerboecke nicht nachgewiesen (Querholm 40x60x3 ueber ca. 1,2 m: Biegung 50 kg mittig ca. 150 Nm, ca. 15 N/mm2 [E]; Kragarm innen ca. 165 Nm am Pfosten, Fussplatte/Verbundanker nachzurechnen)",
    "Tischmitte = Beetmitte ist Annahme (OBJ-Reihen weichen um 33-38 mm ab); die Instanz-Platzierung gehoert dem Integrator (yaw = Azimut + 90 Grad wie OBJ, Y radial INNEN)",
    f"Rinnenlaenge je Reihe ist die Folge von D18; weniger Topfloecher ({tot_h} statt 556) beim Orchestrator/Ben bestaetigen",
    "Aufhaengung des Verteilers an den Boecken (Rohrschellen) nicht modelliert; Verteiler/Sammelrohr laufen frei schraeg",
    "aussen 3 Rinnen (OBJ 2) bleibt Annahme; die aeusserste (3.) Reihe liegt auf ap 5497 (Beetmitte 5209 + 288), die inneren auf 5209 und 4921",
    "Beine ausserhalb der Beete stehen im Gehweg: Durchgangsbreite zwischen den Beeten und Tischen vom Integrator zu pruefen (Beinabstand y aussen " + fmt(2 * Gs["aussen"]["yl"]) + ", Mitte " + fmt(2 * Gs["mitte"]["yl"]) + ")",
    "Rinnenabstand 262-288 (OBJ) bei Rinnenbreite 130 laesst 132-158 mm Luecken; ref-6 zeigt fast buendige Rinnen: Widerspruch OBJ/Bild, OBJ gilt (provenance)",
    "Schlaeuche gerade statt gebogen; Kopfplatten/Winkelhalter an den Beinkoepfen (W11) nicht modelliert",
    "Innen: Pfosten stehen ausserhalb des Beckenrands (Wasserradius 1945 + Wand 150 + 60 + 50); der Kragarm ueberspannt Rand Z 650 mit 130 mm Luft; ein Stuetzwinkel am Pfosten ist wegen der Beckenwand nicht moeglich (Annahme A)",
    "Gefaelle: detail-standard.md und Scope-Card nennen noch 1 cm/m, gebaut 1,5 % nach R06 (Orchestrator-Vorgabe)",
]
# --- Parameter-Herkunft
d["parameter"]["bock_inset"]["herkunft"] = "[A] Abstand Bock zur Stirn der KUERZESTEN Reihe (250 mm)"
d["parameter"]["strut_z"]["herkunft"] += "; innen Laengsstrebe auf Z 400 (Ausleger ausserhalb des Beckenrands)"
# --- Herkunftstabelle: veraltete Zeilen ersetzen
new_rows = [
    ["Rinnenlaenge je Reihe 678/848 (innen), 1468-1981 (Mitte), 2750-3124 (aussen)", "je Reihe", "E", "Zehneck-Seite 2 x ap x tan 18 Grad (ap aus ap_c +- Reihenabstand) - 2 x corner_gap 100 - Ueberstaende 169 + 79 (Orchestrator D18, docs/jobs/W16-nft-tisch-passung.md); OBJ-Reihen nur als Beispiel", "hoch"],
    ["Rinnenlaenge 1304 / 1983 / 3232 (OBJ-Beispiel je Ring)", "nur Beleg des Problems", "OBJ", "layout.json hydro_tables: groesser als die Zehneck-Seite der Reihen (innen -178/-8, Mitte -42, aussen -56), daher ersetzt (D18)", "hoch"],
    ["Beine ausserhalb der Beet-Aussenbreite (Portal): y = +-(bed_outer_w/2 + 60 + 50)", f"y +-{Gs['aussen']['yl']:.0f} (aussen), +-{Gs['mitte']['yl']:.0f} (Mitte)", "E + A", "bed_outer_w aus ibc_beet.json (993 / 933), leg_clearance 60 (D18), Fussplatte 100: Plattenkante 60 mm vom Beet", "mittel"],
    ["Auslegerbock innen: Pfosten bei ap = Pool-Aussenradius 2095 + 60 + 50", "ap 2205", "E + A", "layout.json pool.d/2 1945 + params.json wall 150 (A) + leg_clearance + Fussplatte/2; Kragarm 40x60x3 ueber das Wasser, Statik nicht nachgewiesen", "niedrig"],
    ["Querholm/Kragarm Rechteckrohr 40 x 60 x 3, Beine 40x40x3", "40x60x3; 40x40x3", "A + E", "Biegung 50 kg mittig auf 1,2 m = 150 Nm, W ca. 10 cm3 -> ca. 15 N/mm2 gegen S235 235 N/mm2", "niedrig"],
    ["Querstrebe/Laengsstreben/Diagonalen auf Z 800 (innen Z 400)", "Z 800", "A", "ueber den Pflanzen (Beet-Oberkante Z 475, Pflanzen bis ca. 560); Portal steht ausserhalb der Beete", "niedrig"],
    ["Verteiler und Sammelrohr schraeg entlang der Sektorgrenze (18 Grad)", "dx/dy = +-tan 18", "E", "jede Reihe hat anderen Abstand zur Ecke; schraeges Rohr haelt Ueberstand und corner_gap fuer alle Reihen gleich", "mittel"],
    ["Rinnenmitte um +45 mm nach +X versetzt", "+45 mm", "E", "(Ueberstand Zulaufseite 169 - Ablaufseite 79)/2", "hoch"],
    ["Lochraster je Reihe mit Phase 0 / pitch/2, n = floor(L/250)", "Phase 0 / 125", "Bild + E", "ref-6 Zickzack; Versatz je Reihe aus hole_plan() (tisch_geom.py), Loecher >= 46 mm vom Rinnenende", "mittel"],
    ["Tischmitte auf der Beetmitte: ap_c aussen 5209, Mitte 3343, innen 1864", "mm", "E + A", "Mittel der Beetradien (ibc_beds r) bzw. Mittel der OBJ-Reihen innen; Abweichung zum OBJ 33-38 mm", "mittel"],
    ["Tischzahl je Sektor: innen 10, Mitte 6 (Sektoren 0-2, 7-9), aussen 8 (0-3, 6-9)", "24", "OBJ", "Beet-Azimute in layout.json ibc_beds (5,3 + 36 Grad x i)", "mittel"],
]
keep = [r for r in d["herkunft_tabelle"] if not any(r[0].startswith(s) for s in ("Rinnenlaenge 1304", "Zwei Boecke", "Rechteckrohr 30x30x2", "Fussplatten 80x80x5", "Laengsstreben 30x30x2", "Holmueberstand", "Zulaufverteiler: Achse", "Sammelrohr: Achse"))]
keep += [r for r in d["herkunft_tabelle"] if r[0].startswith(("Zulaufverteiler: Achse", "Sammelrohr: Achse", "Holmueberstand"))]
keep.append(["Laengsdiagonalen 25x3 je Beinseite zwischen den Boecken", "1 / 2 je Tisch", "A", "Bild-Kritiker W16: Gestell in Laengsrichtung weich, nur unterer Laengsriegel", "niedrig"])
keep.append(["Zwei Boecke je Tisch (4 Beine Portal, 2 Pfosten innen), Abstand zur Stirn der kuerzesten Reihe 250", "2 Boecke", "Scope-Card + A", "docs/scope-cards.md nft_tisch (4 Beine mit Querstreben, Diagonalen); innen 2 Pfosten wegen Pool (D18)", "mittel"])
keep.append(["Fussplatten 100x100x5, M8", "100x100x5", "A", "Kippmoment der Ausleger und Plattenkante-Abstand 60 mm zum Beet", "niedrig"])
d["herkunft_tabelle"] = new_rows + keep
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("nft_tisch.json aktualisiert", n_t, n_f)
