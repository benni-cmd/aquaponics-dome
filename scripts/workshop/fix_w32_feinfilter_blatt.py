"""W32 Feinfilter: Blatt-Text und Herkunftstabelle in data/components/feinfilter.json schreiben (Ports und Massen aus der gebauten .sc gemessen). Danach partsheet.py feinfilter.
Aufruf: python scripts/workshop/fix_w32_feinfilter_blatt.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

p, d = sc.load_params("feinfilter")
ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "feinfilter.sc"))
B = {b["name"]: b for b in ev["bodies"]}
bb = lambda n: B[n]["bbox"]
r0 = lambda v: f"{v:.0f}"
mass = sum(b["mass_g"] for b in ev["bodies"]) / 1000
L, W, H, w, zb = p["tank_l"], p["tank_w"], p["tank_h"], p["wall"], p["foot_h"]
il, iw = L - 2 * w, W - 2 * w
kl, kw, kd = p["basket_l"], p["basket_w"], p["basket_d"]
a_wet = (p["wet_frac"] * 2 * (kl + kw) * kd + kl * kw) / 1e6
q_m3h = p["q_lmin"] * 60 / 1000
zi, zo, zd, zs = zb + p["inlet_z"], zb + p["outlet_z"], zb + p["drain_z"], zb + p["spray_z"]
water_l = il * iw * ((zi - p["inlet_d"] / 2) - (zb + w)) / 1e6
e, a, ab, sp = bb("Einlaufrohr"), bb("Auslaufrohr"), bb("Schlauchtuelle"), bb("Spuel_Tuelle")
gz = max(b["bbox"]["max"][2] for b in ev["bodies"])
d["blatt"] = {
 "funktion": (f"Mechanischer Feinfilter je Linie im HAUPTSTROM (Schritt 3 der Kette in docs/filter-konzept.md, D51, neu bemessen in W32/D55): Das Wasser der Linie ({p['q_lmin']} l/min, vom Pool zu den grossen Pumpen) laeuft ueber ein senkrechtes Einlaufrohr d63 in einen Siebkorb aus Edelstahlgewebe (Maschenweite {p['mesh_um']} Mikrometer) und tritt durch das Gewebe in die Ablaufkammer, aus der der Auslauf d63 zur Saugseite der grossen Pumpen fuehrt. "
              f"Die Siebflaeche folgt aus der Rechnung A = Q / Siebbelastung = {q_m3h:.1f} m3/h / {p['sieve_load']} m/h = {q_m3h / p['sieve_load']:.3f} m2; der Korb {kl} x {kw} x {kd} mm liefert {a_wet:.3f} m2 benetzte Flaeche ({q_m3h / a_wet:.2f} m/h). "
              "Gewebe 100 Mikrometer hielt im Versuch von Mortensen 21 % der Schwebstoffe zurueck (R30). Zum Reinigen alle 1-2 Wochen: Spuelanschluss mit Spritzrohr oeffnen, Deckel per Spannverschluss oeffnen, Korb an den Buegelgriffen herausheben und ausspuelen, Behaelter ueber den Kugelhahn ablassen."),
 "querschnitt": (f"Behaelter PP-Platte {w} mm geschweisst, innen {il} x {iw} x {H - w}; 12 x 12 Auflageleisten an den langen Innenwaenden tragen den Korbflansch (Edelstahl 3 mm, 22 mm breit). Korb {kl} x {kw} x {kd}: Gewebehuelle mit Stuetzrahmen aus Edelstahl {p['rod']} x {p['rod']} (4 Eckstaebe, Bodenrahmen). "
                 f"Ablaufkammer unter dem Korb {p['chamber']} mm hoch. Standrahmen Vierkantrohr {p['leg']} x {p['leg']} x {p['leg_wall']} verzinkt mit Fussplatten {p['plate']} x {p['plate']} x {p['plate_t']}, {int(p['bar_n'])} Auflagestege im Raster {p['bar_pitch']:.0f} mm."),
 "toleranzen": (f"Spalt Korbflansch zur Wand {p['flange_gap']} mm je Seite (Entnahme ohne Klemmen); Einlaufrohr {p['inlet_air']} mm ueber dem Korbflansch; Korbboden {p['chamber']} mm ueber dem Behaelterboden; Dichtflansch des Auslaufs (D{p['outlet_collar_d']}) mindestens 15 mm unter dem Korbboden; Pruefung check_feinfilter.py (Masse +-0,5 mm); "
                f"Rohrgeschwindigkeit d63 (Innen 57 mm): {(p['q_lmin'] / 1000 / 60) / (3.14159265 / 4 * 0.057 ** 2):.2f} m/s (Saugseite <= 1,0)."),
 "ports": [
  ["Einlauf (Stutzen links, Winkel in den Korb)", "PVC-U d63 (DN50), Wand 3,0", f"x {r0(e['min'][0])}, y 0, z {r0(zi)} (Oeffnungsebene aussen, Mitte); senkrechtes Rohr endet bei z {r0(zi - p['inlet_down'])}, x {-p['inlet_in']:.0f}", f"Hauptstrom {p['q_lmin']} l/min tritt ein (vom Pool, Netz K05/K21 neu zu fuehren), Oeffnung zeigt -X"],
  ["Auslauf (Durchfuehrung rechts, unter dem Korb)", "PVC-U d63 (DN50), Wand 3,0; Dichtflansch und Gegenmutter D90", f"x {r0(a['max'][0])}, y 0, z {r0(zo)} (Oeffnungsebene aussen, Mitte)", "Wasser tritt aus zur Saugseite der grossen Pumpen (K06/K22), Oeffnung zeigt +X"],
  ["Ablass mit Kugelhahn (Vorderwand, unten)", "PVC-U d40 (DN32), Kugelhahn D56, Schlauchtuelle", f"x {r0(p['drain_x'])}, y {r0(ab['min'][1])}, z {r0(zd)} (Ende der Tuelle, Mitte)", "Wasser tritt aus zum Spuelen/Entleeren, Oeffnung zeigt -Y; Hebel quer = zu"],
  ["Spuelanschluss mit Kugelhahn (Rueckwand, oben)", "PVC-U d25 (DN20), Kugelhahn D40, Schlauchtuelle; innen Spritzrohr d25 quer ueber den Korb", f"x {r0(p['spray_x'])}, y {r0(sp['max'][1])}, z {r0(zs)} (Ende der Tuelle, Mitte)", "Spuelwasser tritt ein (Schlauch), Oeffnung zeigt +Y; das Spritzrohr (Duesen nicht modelliert) spuelt den Korb"]
 ],
 "verbindungen": [
  "Rohrdurchfuehrungen in der PP-Wand: Auslauf mit Dichtflansch innen (D90 x 5), Gegenmutter aussen (D90 x 5) und Flachdichtung (nicht modelliert); Einlauf, Ablass und Spuelanschluss als PP-Schweissstutzen oder Tankdurchfuehrungen (Hersteller offen) [A]",
  "Rohre PVC-U nach DIN 8062 (d63 Hauptstrom, d40 Ablass, d25 Spuelen), Anschluss an die Leitungen der Montage ueber Muffe oder Verschraubung (leitungsteile)",
  "Spannverschluesse: 4 Stueck Edelstahl-Exzenterspanner mit Haken am Behaelter und Bock-Hebel am Deckel (Handelsteil, Fabrikat offen) [A]; Deckel liegt auf EPDM-Flachdichtung 3 mm",
  f"Standrahmen: Vierkantrohr {p['leg']} x {p['leg']} x {p['leg_wall']} geschweisst oder verschraubt (M8), Fussplatten {p['plate']} x {p['plate']} x {p['plate_t']}; der Behaelterboden liegt auf Ring und {int(p['bar_n'])} Auflagestegen (Spannweite <= 125 mm, Biegespannung PP rechnerisch ca. 2,5 MPa bei 5,5 kPa Wasserdruck) [E]; PP-Wand {w} mm: Biegung bei {zi - p['inlet_d'] / 2 - zb - w:.0f} mm Wasserhoehe ca. 5 MPa ohne Rippen, reale Behaelter mit Rippen/Rahmen [E]"
 ],
 "abweichung": ("Das Bauteil kommt nicht aus dem OBJ; es ist eine Empfehlung der Filteranalyse (R28, R30, D51, D55). W31 hatte 400 x 300 x 500 fuer den Teilstrom 12,5 l/min (Gewebe 150 Mikrometer); W32 bemisst es fuer den Hauptstrom 110 l/min je Linie und Gewebe 100 Mikrometer neu "
                f"(Behaelter {L:.0f} x {W:.0f} x {H:.0f}, Korb {kl} x {kw} x {kd}). Das Blatt W32 nennt 'Ports DN 63': gemeint ist wie in W31 der Aussendurchmesser d63 der Rohrbibliothek (DN50); die Netzliste fuehrt K05/K06 noch mit d50 und 12,5 l/min: Orchestrator/Montage ziehen sie nach. "
                "Die Siebbelastung 8 m/h ist eine Annahme: R30 fand keine belegte Auslegungsgroesse (Hersteller-Datenblaetter ungelesen); der Bestand aus W31 (1,6 m/h) haette bei 110 l/min 4,1 m2 Sieb verlangt."),
 "gewicht_gefuellt": f"leer {mass:.1f} kg; im Betrieb mit Wasser bis zur Unterkante des Einlaufs (z {zi - p['inlet_d'] / 2:.0f}, ca. {water_l:.0f} l) ca. {mass + water_l:.0f} kg [E]; Standrahmen und Untergrund muessen das tragen (Montage). Hoehe gesamt {gz:.0f} mm (Deckelgriff), Hub zum Herausheben des Korbs ca. {kd + 60:.0f} mm ueber dem Deckel noetig.",
 "montage": [
  "Standrahmen aufstellen, ausrichten (Wasserwaage), Fussplatten auf tragfaehigem Untergrund befestigen",
  "Behaelter auf den Rahmen setzen und gegen Verrutschen sichern",
  "Einlauf-, Auslauf-, Ablass- und Spuelstutzen mit den Leitungen verbinden (Einlauf mit Gefaelle vom Pool, Auslauf zur Saugseite der grossen Pumpen, Spuelanschluss mit Schlauch)",
  "Siebkorb einsetzen (Flansch auf den Leisten), Deckel mit Dichtung auflegen und die vier Spannverschluesse schliessen",
  f"Probelauf mit {p['q_lmin']} l/min; Wasserstand im Behaelter pruefen (steigt der Spiegel ueber den Einlauf, ist der Korb verstopft: spuelen)"
 ],
 "werkzeug": "Wasserwaage, Schluessel M8, Rohrschneider, PVC-Kleber, ggf. Kunststoffschweissgeraet",
 "stueckliste": [
  f"Behaelter PP {L:.0f} x {W:.0f} x {H:.0f}, Wand {w}, mit 2 Auflageleisten, 4 Durchfuehrungen: 1",
  f"Siebkorb Edelstahl (Flansch {kl + 44} x {kw + 44} x 3, Gewebehuelle {kl} x {kw} x {kd}, Gewebe {p['mesh_um']} Mikrometer, 4 Eckstaebe, Bodenrahmen, 2 Buegelgriffe): 1",
  f"Deckel PP {L + 8:.0f} x {W + 8:.0f} x 6 mit Griff: 1, EPDM-Flachdichtung 3 mm: 1, Spannverschluesse Edelstahl: 4",
  "Einlaufwinkel PVC-U d63: 1, Auslaufrohr PVC-U d63 mit Dichtflansch D90 und Gegenmutter D90: 1",
  "Ablassstutzen PVC-U d40: 1, Kugelhahn d40: 1, Schlauchtuelle d40: 1",
  "Spuelstutzen PVC-U d25: 1, Kugelhahn d25: 1, Schlauchtuelle d25: 1, Spritzrohr PVC-U d25: 1",
  f"Standrahmen: 4 Beine, 4 Ringstege, {int(p['bar_n'])} Auflagestege, 2 Querstege (Vierkantrohr {p['leg']} x {p['leg']} x {p['leg_wall']}), 4 Fussplatten {p['plate']} x {p['plate']} x {p['plate_t']}",
  "Gesamt: 2 Stueck (Linie 1 und 2)"
 ],
 "lokal": "Handelsueblich: Beutel-/Taschenfilter-Gehaeuse oder Siebkorbfilter fuer Teichtechnik (Edelstahl, 100 Mikrometer Filterbeutel) statt Eigenbau; Standrahmen aus Kantholz.",
 "referenz": "kein Referenzbild (Bauteil fehlt im OBJ); docs/filter-konzept.md Art 2; docs/research/R30.md; data/leitungsnetz.json feinfilter_1/2",
 "varianten": [],
 "render_dirs": [],
 "kritiker": "kein Pruefer-Lauf (Auftrag W32: Selbstcheck)",
 "pruefung": [
  "scripts/workshop/check_feinfilter.py: Ergebnis in renders/components/feinfilter/check.txt (Siebflaeche aus gemessenem Korb gegen Q / Siebbelastung, Masse, Wand, Korb im Behaelter, Ports, Hoehenfolge, Spuelanschluss, Rohrgeschwindigkeit, Standrahmen, Interferenz)",
  "Kein Bild-Kritiker und kein Spec-Pruefer (Auftrag W32)"
 ],
 "offen": [
  "Siebbelastung 8 m/h ist [A]: R30 nennt keine belegte Auslegungsgroesse; Hersteller-Datenblatt des 100-Mikrometer-Gewebes und die Standzeit bis zum Verstopfen offen (bei 4 m/h waere die Siebflaeche doppelt so gross, bei 12 m/h zwei Drittel)",
  "Netzliste data/leitungsnetz.json fuehrt K05/K06 und K21/K22 noch mit d50 und 12,5 l/min; der Feinfilter sitzt jetzt im Hauptstrom d63 mit 110 l/min je Linie (Orchestrator/Montage M10: Strom vor den grossen Pumpen, Seitenablauf des Pools muss durch den Filter)",
  f"Platz: Behaelter {L:.0f} x {W:.0f} (mit Stutzen ca. 770 x 680) und {gz:.0f} mm hoch plus Hub zum Herausheben des Korbs; Hoehe gegen Pool-Spiegel (Z 515) und Pumpen-Saugseite prueft die Montage; foot_h {zb} anpassbar",
  "Kein Notueberlauf/Bypass: verstopft der Korb, steigt der Wasserstand ueber den Einlauf und staut zum Pool; Ueberlauf in den Pool oder Bypass ist Sache der Hydraulik",
  "Gewebe-Maschenweite 100 Mikrometer ist ein Hinweis (nicht modelliert); die Huelle ist 1 mm mit Ersatzdichte 0,55; Gewebe-Fabrikat offen",
  "Spannverschluesse, Durchfuehrungen, Kugelhaehne und das Spritzrohr (Duesen) sind Ersatzformen (Handelsteile, Fabrikat offen)",
  "PP-Wand 10 mm und Auflagestege sind eine Ueberschlagsrechnung (Biegung), kein Festigkeitsnachweis; reale Behaelter mit Rippen",
  "Das Bauteil steht nicht in layout.json: Montage setzt die zwei Instanzen nach leitungsnetz.json"
 ]
}
d["herkunft_tabelle"] = [
 ["Funktion Feinfilter, Zweck, Reinigung alle 1-2 Wochen", "Schritt 3 der Kette", "Q", "docs/filter-konzept.md Art 2 (FAO 589; SRAC 454), Befund 1", "hoch"],
 ["Anzahl 2 (eine je Linie)", "2", "Q", "data/leitungsnetz.json knoten feinfilter_1/2", "hoch"],
 ["Hauptstrom 110 l/min je Linie", "110 l/min", "Q", "Auftrag W32/D55; R30 Befund 1 (Feinfilter sah nur 11 % des Stroms)", "hoch"],
 ["Gewebe <= 100 Mikrometer", "100 Mikrometer", "Q", "Auftrag W32/D55; R30: Mortensen 2000: 100 Mikrometer = 21 % Schwebstoffe", "mittel"],
 ["Siebbelastung 8 m/h", "8 m/h", "A", "R30 nennt keine belegte Auslegungsgroesse; Bestand W31 rechnete 1,6 m/h bei 12,5 l/min", "niedrig"],
 ["Siebflaeche 0,825 m2 (Soll) / gebauter Korb", "0,825 / 0,840 m2", "E", "A = Q / Siebbelastung; wet_frac 0,85; aus den gemessenen Korbmassen (check_feinfilter.py)", "mittel"],
 ["Ports d63 (Ein-/Auslauf), Spuelanschluss d25", "d63 / d25", "Q", "Auftrag W32 (DN 63 = d63 der Rohrbibliothek); leitungsteile.json sizes 63/25", "mittel"],
 ["Behaelter, Korb, Hoehen aus der Siebflaeche abgeleitet", "siehe Parameter", "E", "scripts/workshop/feinfilter.py derive()", "mittel"],
 ["Behaelterwand PP 10, Deckel 6, Dichtung EPDM 3", "10 / 6 / 3 mm", "A", "Konstruktionspraxis PP-Behaelter (Wand aus Biegeueberschlag)", "niedrig"],
 ["Standrahmen 40 x 40 x 3, Auflagesteg-Raster <= 125", "mm", "A", "Konstruktionspraxis; Boden-Biegespannung ca. 2,5 MPa", "niedrig"],
 ["Rohrwand d63 3,0 / d40 1,9 / d25 1,8", "mm", "Q", "data/components/leitungsteile.json", "mittel"],
 ["Dichten PP 0,91 / Edelstahl 7,9 / Stahl 7,85 / PVC 1,4 / EPDM 1,1 / Gewebe 0,55", "g/cm3", "A", "Handbuchwerte; Gewebe-Ersatzdichte aus 0,5 kg/m2 Gewebemasse", "niedrig"],
 ["Port-Koordinaten (Einlauf, Auslauf, Ablass, Spuelen)", "siehe Ports", "E", "gemessen aus den Stutzen-Boxen (fix_w32_feinfilter_blatt.py)", "mittel"]
]
json.dump(d, open(os.path.join(sc.ROOT, "data", "components", "feinfilter.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
