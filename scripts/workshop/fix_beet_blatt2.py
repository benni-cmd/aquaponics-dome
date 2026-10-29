"""Blatt ibc_beet nach Spec-Pruefer (29.10.): Gewichte getrennt (leer ohne Medium, Medium, Wasser), Portkoordinaten mit aktuellen Parametern, Herkunftszeilen, Stueckliste mit Mengen."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "ibc_beet.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
bl = d["blatt"]
ports, gew, mat = [], [], []
for typ, T in d["typen"].items():
    L, W, H = T["laenge"], T["breite"], T["hoehe"]
    rw, wl = P["rim_w"], P["wall"]
    Lw, Ww = L - 2 * rw, W - 2 * rw
    Li, Wi = Lw - 2 * wl, Ww - 2 * wl
    xsp = Li / 2 - 200
    yin = -(Wi / 2 - 50)
    zin = H - P["inflow_below_rim"]
    zms = H - P["rim_gap"]
    zm0 = zms - P["media_depth"]
    zg0 = zm0 - P["grid_t"]
    top_sp = zm0 + P["standpipe_over"]
    ports.append([f"{typ}: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden)", "Rohr d25 (PVC-U d25, etwa DN20), Bulkhead D36 mit Flansch D50", f"x {xsp:.0f}, y 0, z -30", "Wasser verlaesst das Beet nach unten (Oeffnung zeigt -Z; Beet ist eingelassen, Ablauf unter dem Wannenboden)"])
    ports.append([f"{typ}: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand)", "Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03)", f"x {-Lw / 2 - 60:.0f}, y {yin:.0f}, z {zin:.0f}", "Wasser tritt von aussen ein (Oeffnung zeigt -X); Rohr liegt laengs, nicht quer (Auslegung E: 2,9 m Beetlaenge)"])
    n_post = 24 if L > 2500 else 15
    # Massen: Wanne/Siebboden/Stuetzen/Siphon (ohne Medium) aus der Messung, Medium getrennt
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"ibc_beet_{typ}.sc"))
    leer = sum(b["mass_g"] for b in ev["bodies"] if not b["name"].startswith("Medium") or b["name"].startswith("Medienschutz")) / 1000
    vmed = [b for b in ev["bodies"] if b["name"] == "Medium"][0]["volume_mm3"] / 1e6
    sump = (zg0 - P["floor_t"]) * Wi * Li / 1e6 + (zm0 - zg0) * Wi * Li / 1e6 * 0              # Wasserraum unter dem Siebboden (l)
    pore = 0.4 * P["standpipe_over"] * (Wi - 4) * (Li - 4) / 1e6                              # Porenwasser im gefluteten Teil des Mediums (l), Porositaet 40 % [A]
    wat = sump + pore
    gew.append(f"{typ}: leer ohne Medium {leer:.0f} kg; Medium {vmed:.0f} l = {vmed * 0.9:.0f} kg (Schuettdichte 0,9 [A]); Wasser bis Standrohrkante {wat:.0f} l = {wat:.0f} kg (Wasserraum unter dem Siebboden {sump:.0f} l + Porenwasser {pore:.0f} l bei 40 % Porositaet [A]); gefuellt gesamt {leer + vmed * 0.9 + wat:.0f} kg")
    mat.append((typ, vmed, n_post))
bl["ports"] = ports
bl["gewicht_gefuellt"] = " | ".join(gew)
bl["massen_getrennt"] = ["Medium"]
bl["toleranzen"] = bl["toleranzen"].split(" Wasserstand")[0] + " Wasserstand in der Flutphase = Standrohrkante, 220 mm ueber der Medienunterkante = 80 mm unter der Medienoberflaeche (R03 Befund 5: Standrohr 22 cm bei 30 cm Medium); R03 Befund 4 nennt eine trockene Oberzone von 2-5 cm, SRAC 5007 einen Wasserstand 1 Zoll unter der Oberflaeche -> Abweichung 3-6 cm, siehe offen."
bl["abweichung"] += " Innenbeete: OBJ z0 -209, -173, -172, -170, -194, -194 (Rand Z 440-479): die Medienoberflaeche liegt absolut bei Z 365-404, nicht einheitlich 400 (Vorpruefung Toleranz 40 mm fuer innen; R03-Z-400 gilt fuer aussen)."
bl["stueckliste"] = [
    "T30a Wanne HDPE (Sonderwanne 2953/1865 mm): 1 je Beet; 14 gesamt (aussen 8: 5 x 933 + 3 x 993, innen 6)",
    "T30b Stuetzkloetze PP 60x60: 24 (aussen) / 15 (innen) je Beet",
    "T30c Siebboden PP 8 mm (Rasterlochplatte): 1 je Beet",
    "T30d Medium Blaehton/Kies 8-20 mm: " + "; ".join(f"{t} {v:.0f} l ({v * 0.9:.0f} kg)" for t, v, n in mat) + " je Beet; 14 Beete gesamt ca. 8,4 m3",
    "T30e Siphon: 1 Bulkhead D36 mit Flansch D50 + Dichtung + Kontermutter, 1 Standrohr PVC-U d25 (Laenge 30 + 482 mm), 1 Glocke PVC-U d75 x 250 mit Deckel, 1 Medienschutz PVC-U d110 x 320",
    "T30f Zulauf: 1 Tropfrohr PE d20 (Laenge siehe Messung), 1 Endstopfen d20, 1 Gummitulle D22 fuer die Wanddurchfuehrung, 1 Anschluss-Kupplung d20",
    "Normbezeichnungen: PVC-U Rohr nach DIN 8062 / EN 1452; PE-Rohr nach DIN 8074; Medium gewaschen, Korn 8-20 mm (R03)"]
bl["montage"][5] = "Zulauf anschliessen und Zyklus pruefen; Netztoepfe und Pflanzen setzt der Integrator als Instanzen nach layout.json (nicht Teil des Beets)"
bl["varianten"] = ["ibc_beet_aussen_933", "ibc_beet_aussen_993", "ibc_beet_innen_933"]
bl["funktion"] = bl["funktion"].replace("Pflanzen in Netztoepfen im Medium", "Pflanzen (Instanzen; 288 je Aussenbeet, Beet bei Azimut 113 hat 144) in Netztoepfen im Medium")
bl["offen"] = [x for x in bl["offen"] if not x.startswith("Pflanzen (Netztoepfe")]
bl["offen"] += ["Pflanzen: 288 je Aussenbeet (Beet bei Azimut 113: 144; 7 x 288 + 144 = 2160) sind Instanzen des Integrators", "Wasserstand 80 mm unter der Oberflaeche (FarmHub-Standrohr 22 cm) gegen trockene Oberzone 2-5 cm (R03 Befund 4) und SRAC 1 Zoll: Standrohrhoehe als E, Konfidenz niedrig; Siphon steht auf dem Siebboden, darunter ein Wasserraum von 262-274 mm (Annahme A)"]
hk = d["herkunft_tabelle"]
d["medium"]["herkunft"] = "[A] Schuettdichte Blaehton 0,5-0,8, Kies 1,5 g/cm3: Mittel 0,9 trocken; nass ca. 1,3; nur fuer die Gewichtsabschaetzung"
d["werkstoff"]["herkunft"] = "ref-5/ref-6 weisse Wannen (HDPE IBC-Innenbehaelter 0,95 g/cm3); Siebboden/Stuetzen PP 0,91, Rohre PVC-U 1,4 g/cm3"
for r in hk:
    if r[0].startswith("Werkstoff"):
        r[0] = "Werkstoffe: Wanne HDPE 0,95; Siebboden/Stuetzen PP 0,91; Rohre PVC-U 1,4; Medium 0,9 (trocken)"
        r[1] = "0,95 / 0,91 / 1,4 / 0,9 g/cm3"
        r[3] = "ref-5/6 weisse Wannen; Normwerte Kunststoffe; Medium Mittelwert"
    if r[0].startswith("Wandstaerke 4"):
        r[3] = "R03 nennt 3-4 mm nur als Folgerung fuer das Modell (Scope-Card), keine eigene Quelle; Boden Annahme"
        r[1] = "4 / 5 mm"
hk += [
    ["Wandstaerken Rohre: Standrohr 2, Glocke 3, Medienschutz 3, Tropfrohr 2", "2 / 3 / 3 / 2 mm", "A", "PVC-U/PE Rohre d25/d75/d110/d20 Normwanddicken ungefaehr; nicht recherchiert", "niedrig"],
    ["Medium-Spiel zur Wannenwand", "2 mm", "A", "Konstruktionspraxis", "niedrig"],
    ["Medienschutz-Durchbrueche 12 x 12 mm, 3 Ringe x 4 (z 40/120/200)", "12 Stueck", "R03 + A", "R03: kleine Seitenloecher; Anzahl und Form (quadratisch statt rund wegen Rechenzeit) Annahme", "niedrig"],
    ["Tropfloecher 4 x 4 mm, Teilung 200 mm, ab 150 mm von der Stirn", "4 / 200 mm", "A", "R03: gelochtes Rohr oder Tropfschlauch; Raster Annahme", "niedrig"],
    ["Zulauf-Wanddurchfuehrung D22 in der Stirnwand (Rohr d20)", "D22", "A", "Konstruktionspraxis (Gummitulle); y = -(Wi/2 - 50)", "niedrig"],
    ["Zulaufrohr liegt laengs (nicht quer), 25 mm unter dem Rand", "z 612 lokal / 450 abs.", "R03 + E", "R03: 'quer ueber das Beet auf Z 450'; bei 2,9 m Laenge laengs ausgelegt (E)", "niedrig"],
    ["Gewichtsrechnung: leer ohne Medium, Medium 0,9, Wasser bis Standrohrkante (Sumpf + 40 % Poren)", "siehe Gewicht", "E", "Messung aus .sc (eval) und Dichten oben; Porositaet 40 % Annahme", "niedrig"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ibc_beet.json (2) gepflegt")
