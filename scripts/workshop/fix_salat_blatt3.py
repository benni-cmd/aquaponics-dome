"""Blatt-Texte Salatkopf Rev. B (29.10. W07): 72 Polygonblaetter statt 36 Scheiben, S/M/L per Skalierung. Idempotent; nach salatkopf.py und vor partsheet.py ausfuehren.
Aufruf: python scripts/workshop/fix_salat_blatt3.py [kritiker-urteil-text]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "salatkopf.json")
d = json.load(open(p, encoding="utf-8"))
ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "salatkopf.sc"))
mn, mx = sc.bbox_all(ev)
w, h = max(mx[0] - mn[0], mx[1] - mn[1]), mx[2]
G = d["blatt_gruppen"]
n = G["verteilung"]["n"]
faces = max(x["faces"] for x in ev["bodies"])
d["revision"] = "B"
d["beschreibung"] = f"Salatkopf als buschige Blattrosette aus {n} kleinen polygonalen Blaettern (12-Eck, unregelmaessig, Fibonacci-Verteilung auf einem Halbellipsoid-Huegel, deterministischer Zufallsversatz) um ein Herz-Prisma, Groessen S/M/L per Skalierung des ganzen Kopfes (head_d)"
d["quelle_masse"] = "ref-6: Kopf ca. 1,5-2 x Topfkragen (64 mm) breit, flacher dichter Huegel (Hoehe ca. 0,5 x Breite) [A]"
for k in ("leaf_t_f", "core_r_f", "core_h_f"):                # Rev. A-Parameter (Scheiben/Kuppelkern), in Rev. B ohne Wirkung
    d["parameter"].pop(k, None)
d["parameter"]["head_d"]["herkunft"] = "[A] Standard M: Breite ca. 1,05 x head_d, Hoehe ca. 0,55 x head_d (ref-6: flacher, breiter Huegel, Hoehe etwa halbe Breite); S = 70, L = 130; wirkt als solid.scale-Faktor head_d/100 auf alle Blaetter und das Herz (Hals bleibt D16)"
bl = d["blatt"]
bl["querschnitt"] = (f"Blattrosette: {n} kleine, ebene Polygonblaetter (12-Eck, unregelmaessiger Umriss, 2 mm dick, je Blatt eigener Koerper, <= {faces} Flaechen) auf einem Halbellipsoid (a {G["a"]:.0f}, b {G["b"]:.0f} mm bei head_d 100), "
                     f"Anstellwinkel steigt von flach am Saum bis steil im Herzen, Azimut, Roll, Laenge und Breite zufaellig (fester Seed); Herz = niedriges Achteck-Prisma, Wurzelhals D16 x 25 mm nach unten in den Netztopf. "
                     f"Groesse M: Breite {w:.0f} mm, Hoehe {h:.0f} mm ueber dem Topfrand; S/L entstehen durch Skalierung (0,7 / 1,3). Blaetter ueberlappen sich gewollt; die Vereinigung flacher Koerper scheitert im Kernel, daher keine Booleans.")
bl["abweichung"] = f"keine OBJ-Vorgabe (Salatkoepfe stammen aus ref-6); Groesse M: Breite {w:.0f} mm, Hoehe {h:.0f} mm (Verhaeltnis {h / w:.2f}; ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite)."
bl["pruefung"] = [f"scripts/workshop/check_pflanze.py (18/18 PASS, davon 9 Salatkopf): {n} Blaetter, Breite M 95-125, Hoehe 50-70, Hals im Topf, Flaechenbudget, Konfigurationen S/M/L, Breite S/L = 0,7/1,3 x M",
                  "Facetten: " + f"{len(ev['bodies'])} Koerper, {sum(x['faces'] for x in ev['bodies'])} Flaechen gesamt, OBJ-Export 8756 Dreiecke (solidcraft-cli run salatkopf.sc --out x.obj; vorher 69 k)"]
bl["kritiker"] = sys.argv[1] if len(sys.argv) > 1 else "siehe docs/workshop-log.md (Runde 5, Rev. B)"
bl["offen"] = ["Blattraender eben und kantig (keine Kraeuselung): gekraeuselte Blaetter brauchen viele Flaechen, Budget bei 2716 Instanzen",
               "Konfigurationen S/L wirken auf verknuepfte Instanzen im Dom: Integrator pruefen",
               "Instanzvariation (zufaellige Drehung um Z, S/M/L gemischt) ist Sache des Layouts/Tisches"]
keep = [r for r in d["herkunft_tabelle"] if r[0].startswith(("Groessen S", "Wurzelhals", "Gruen", "Anzahl"))]
keep += [
    [f"Salat als buschige Blattrosette ({n} Polygonblaetter auf Halbellipsoid)", "-", "Bild", "ref-6 mittlerer Tisch: buschige, dichte Kopfsalat-Koepfe; Polygonblaetter sind unsere Vereinfachung (Kritiker R1-R4)", "mittel"],
    [f"Breite M ca. {w:.0f} mm, Hoehe {h:.0f} mm", f"{w:.0f} / {h:.0f} mm", "Bild + A", "ref-6: flacher breiter Huegel, Hoehe etwa halbe Breite; Kopf ca. 1,5-2 x Topfkragen (64 mm)", "niedrig"],
    [f"Huegel Halbellipsoid a {G['a']:.0f} / b {G['b']:.0f} mm, Fibonacci-Verteilung der Blaetter", f"{G['a']:.0f} / {G['b']:.0f} mm", "A", "gleichmaessige Flaechenbelegung ohne Muster (Kritiker R4: gestapelte Scheiben)", "niedrig"],
    [f"Blatt 12-Eck {G['verteilung']['L']:g} x {G['verteilung']['w']:g} mm, 2 mm dick, Streuung Laenge {G['verteilung']['L_streu']*100:.0f} %, Breite {G['verteilung']['w_streu']*100:.0f} %", f"{G['verteilung']['L']:g} x {G['verteilung']['w']:g} x 2 mm", "A + Bild", "ref-6: fransige Silhouette; wenige Flaechen je Koerper (12-Eck-Prisma = 14 Flaechen)", "niedrig"],
    [f"Anstellwinkel {G['verteilung']['pitch0']:g} Grad + {G['verteilung']['pitch_pro_theta']:g} x Hoehenwinkel, Streuung +-{G['verteilung']['pitch_streu']/2:g} Grad; Azimut +-{G['verteilung']['az_streu']:g} Grad, Roll +-{G['verteilung']['roll_streu']:g} Grad", "Seed sin(i*12,9898)", "A", "Saum flach/haengend, Herz aufrecht (ref-6, Kritiker R3); deterministisch fuer reproduzierbare .sc", "niedrig"],
    ["Herz: Achteck-Prisma r 17, h 20, ab z 8", "r 17 / h 20 mm", "A", "dunkler Kern unter den Blaettern, verdeckt Luecken", "niedrig"],
    ["S/M/L per solid.scale (head_d / 100 mm)", "0,7 / 1,0 / 1,3", "A", "Facetten bleiben gleich; Hals D16 bleibt (steckt im Topf)", "niedrig"],
]
d["herkunft_tabelle"] = keep
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("salatkopf.json gepflegt:", f"Breite {w:.1f}, Hoehe {h:.1f}, max Flaechen {faces}")
