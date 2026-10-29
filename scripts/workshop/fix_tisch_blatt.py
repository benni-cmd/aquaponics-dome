"""Einmalige Pflege des Blatt-Textes in data/components/nft_tisch.json (Spec-Pruefer-Befunde 29.10.): Stueckliste mit Laengen, Port-Richtungen, Herkunft."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "nft_tisch.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
sl = P["slope_pct"] / 100
d["parameter"]["col_od"]["herkunft"] = "[A] Sammelrohr d50 (Aussen 50, Wand 3; entspricht etwa DN40, Muffen d40/d32)"
d["parameter"]["hdr_od"]["herkunft"] = "[A] Zulaufverteiler d25 (entspricht etwa DN20), Wand 3"
d["typen"]["aussen"]["herkunft"] = "layout.json hydro_tables r 4888/5176, Rinnen-Unterkante Z 1291-1325 (Mittel 1308, gerundet auf 1300 = -8 mm); 3 Rinnen: Ben (OBJ/Bild zeigen nur 2, oasis-obj-analysis) + A (3 nach Beetbreite)"
d["typen"]["mitte"]["herkunft"] = "layout.json hydro_tables r 2987-3775, Rinnen-Unterkante Z 1280-1330 (Mittel 1307, gerundet 1300 = -7 mm), Abstand 263"
d["typen"]["innen"]["herkunft"] = "layout.json hydro_tables r 1733/1995, Rinnen-Unterkante Z 819-858 (Mittel 838,5, gerundet 840 = +1,5 mm), Abstand 262"
bl = d["blatt"]
lines, legs = [], []
for typ, T in d["typen"].items():
    n, rp, L, zc = T["n"], T["rinnen_abstand"], T["laenge"], T["z_rinne_mitte"]
    Wt = (n - 1) * rp + 130
    yl = Wt / 2 - P["holm_overhang"] - P["leg_inset"]
    hl = Wt + 120
    xb = [-(L / 2 - P["bock_inset"]), L / 2 - P["bock_inset"]]
    leg = [zc - x * sl - P["holm_h"] - P["foot_t"] for x in xb]
    zh = [zc - x * sl for x in xb]
    dg = [math.hypot(2 * yl, (zh[i] - P["holm_h"] - 40) - P["strut_z"]) for i in range(2)]
    lines.append(f"{typ}: Beine 4 x 30x30x2: Laenge {leg[0]:.0f} (Zulauf-Bock) / {leg[1]:.0f} (Ablauf-Bock), Beinabstand y {2*yl:.0f}; Holm 40x30x2 x 2: Laenge {Wt+60:.0f}; Querstrebe 30x30x2 x 2: Laenge {2*yl-30:.0f}; Laengsstreben 30x30x2 x 2: Laenge {xb[1]-xb[0]-30:.0f}; Diagonalen 25x3 x 4: Laenge {dg[0]:.0f}/{dg[1]:.0f}; Fussplatten 80x80x5 x 4; Rinnen {n} x nft_rinne_{T['rinne']} (Laenge {L}); Verteiler d25: Laenge {hl:.0f}, {n} Stutzen d16; Sammelrohr d50: Laenge {hl:.0f}; Schlaeuche {n} x ID16/AD20 x 110")
    legs.append(f"{typ}: Beinabstand y {2*yl:.0f}, Bockabstand x {xb[1]-xb[0]:.0f}")
bl["stueckliste"] = ["Pro Tisch je Typ (Laengen in mm):"] + ["  " + x for x in lines] + [
    "Je Bock: 2 Beine, 1 Holm, 1 Querstrebe, 2 Diagonalen, 2 Fussplatten, 4 Schrauben M8x30 (Fussplatten, 2 je Platte), 4 Schrauben M6x40 + 4 Muttern M6 (Diagonalen, 1 je Ende), 2 Rinnenhalter je Rinne (je Rinnenseite 1) mit Schraube M5x12; Bock-Anzahl je Tisch 2, Tische gesamt 10 / 6 / 8 (Boecke gesamt 48)",
    "Dabei: 4 Duebel/Anker M8 je Bock (Boden), je 1 Endstopfen d25 und d50 je Tisch (-Y-Rohrende)"]
bl["toleranzen"] += " Gewichte: Summe je Koerper nach Werkstoff (Stahl 7,85, PVC 1,4 g/cm3; die Messung am .sc enthaelt auch die verknuepften Rinnen)."
bl["gewicht_gefuellt"] = "Wasserfuellung der Rinnen (Film 10 mm, 1 l = 1 kg): aussen 3 x 4,0 = 12 kg, Mitte 4 x 2,5 = 10 kg, innen 2 x 1,6 = 3,2 kg [E]; Verteiler d25 und Sammelrohr d50 gefuellt je ca. 0,3-1,6 kg [E]"
for i, pt in enumerate(bl["ports"]):
    if "Zulauf Tisch" in pt[0]:
        bl["ports"][i][3] = "Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y); Rohr d25 (etwa DN20)"
    if "Ablauf Tisch" in pt[0]:
        bl["ports"][i][3] = "Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal)"
    if "Fussplatten-Anker" in pt[0]:
        bl["ports"][i] = [pt[0], "M8, 2 Schrauben je Platte, Loch D9, Diagonalversatz +-25", "Fusspunkte z 5; " + "; ".join(legs) + " (je Bock zwei Fuesse bei y = +-Beinabstand/2)", "Befestigung auf Boden/Betonpunkt, Richtung -Z"]
bl["offen"] += [
    "STANDORT DER BEINE (components.md Z.44): Fusspunkte liegen auf Z=0 des Bauteils; die Innentische (Apothem 1733-1995) liegen ueber dem Pool (Wasserradius 1945): ihre Beine stuenden im Wasser -> Stuetzung des Innenrings (Ausleger/Konsole am Beckenrand oder Beine ausserhalb) ist OFFEN, Entscheidung beim Orchestrator/Integrator; Aussen/Mitte: Beine neben den Beeten auf dem Boden (Beinabstand siehe Ports), Kollision mit den Beeten vom Integrator zu pruefen",
    "Gefaelle: detail-standard.md und Scope-Card nennen noch 1 cm/m, gebaut 1,5 % nach R06 (Orchestrator-Vorgabe)",
    "Wasserfilm 10 mm ist ein Rinnenmerkmal (Blatt nft_rinne)"]
hk = d["herkunft_tabelle"]
for r in hk:
    if r[0].startswith("Hoehe Rinnenmitte"):
        r[0] = "Hoehe Rinnenunterkante (Boden) bei x=0: Z 840 / 1300 / 1300"
        r[1] = "840 / 1300 / 1300"
        r[3] = "layout.json hydro_tables Z (Unterkanten 819-858, 1280-1330, 1291-1325), Mittel 838,5 / 1307 / 1308 gerundet (Abweichung <= 8 mm)"
    if r[0].startswith("Rinnenzahl"):
        r[2] = "OBJ + Ben + A"
        r[3] = "layout.json hydro_tables (2 innen, 4 Mitte, 2 aussen im OBJ/Bild); aussen 3: Ben (Bild/OBJ zeigen nur 2, oasis-obj-analysis) + A Anzahl nach Beetbreite 933-993"
fix = {"Zickzack": "125 mm", "Gekreuzte": "2 je Bock", "Fussplatten": "80x80x5", "Rinnenhalter": "25x25x25 x 3 mm, M5x12", "Zulaufverteiler": "d25; Schlauch ID16/AD20", "Sammelrohr": "d50, Muffen d40/d32",
       "Rechteckrohr": "30x30x2; 40x30x2", "Laengsstreben": "30x30x2, z 250", "Zwei Boecke": "2 Boecke (4 Beine)", "Rinnenabstand": "262 / 263 / 288 mm", "Rinnenlaenge": "1304 / 1983 / 3232 mm",
       "Durchfluss": "0,5 l/min je Rinne", "Gefaelle": "1,5 % (0,86 Grad)", "Anzahl Tische": "10 / 6 / 8"}
for r in hk:
    for k, v in fix.items():
        if r[0].startswith(k) and r[1] in ("-", "mm", "2", "125", "250", "24", "262/263/288", "1,5 %", "1,5", "0,5"):
            r[1] = v
hk += [
    ["Zulaufverteiler: Achse auf Hoehe der Tuellenachse (+70 mm), freier Schlauchabschnitt 70 mm (hose_gap)", "70 / 70", "E + A", "Rinne: Tuelle z 70 (nft_rinne.json); hose_gap Annahme", "niedrig"],
    ["Sammelrohr: Achse auf Hoehe der Ablaufachse der Rinne (+20 mm ueber dem tiefen Rinnenende)", "20", "E", "Rinne: Ablaufstutzen z 20 (nft_rinne.json)", "mittel"],
    ["Holmueberstand 30 mm, Beineinzug 25 mm", "30 / 25", "A", "Konstruktionspraxis (Holm ragt je Seite 30 mm ueber die Beine)", "niedrig"],
    ["Diagonalenschrauben M6x40 mit Mutter", "M6x40", "A + Normteil", "SolidCraft parts.insert hex_bolt/hex_nut M6", "mittel"]]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("nft_tisch.json gepflegt")
