"""Blatt-Text fuer data/components/pumpe.json (Ports, Gewichte, Stueckliste, Herkunft), aus den Parametern berechnet."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "pumpe.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
ports, gew, sl, boxes = [], [], [], []
for typ, T in d["typen"].items():
    if typ == "filtermodul":
        continue
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"{typ}.sc"))
    mass = sum(b["mass_g"] for b in ev["bodies"]) / 1000
    mn, mx = sc.bbox_all(ev)
    boxes.append(f"{typ}: X {mn[0]:.0f} bis {mx[0]:.0f}, Y {mn[1]:.0f} bis {mx[1]:.0f}, Z {mn[2]:.0f} bis {mx[2]:.0f}")
    if T["art"] == "pumpe":
        L, t, H = T["tafel_l"], T["tafel_t"], T["tafel_h"]
        md, ml, kd, kl = T["motor_d"], T["motor_l"], T["kopf_d"], T["kopf_l"]
        x0 = -(ml + kl) / 2
        yc = t / 2 + P["bracket_t"] + md / 2 + 12
        za = P["pump_z"]
        dn = {40: "DN32", 32: "DN25", 50: "DN40"}
        ports.append([f"{typ}: Saugstutzen (Pumpenkopf)", f"PVC-U d{T['saug_d']} ({dn[T['saug_d']]}), Wand 3", f"x {x0 + ml + kl + 66:.0f}, y {yc:.0f}, z {za:.0f}", "Wasser tritt ein, Oeffnung zeigt +X"])
        ports.append([f"{typ}: Druckstutzen (Pumpenkopf oben)", f"PVC-U d{T['druck_d']} ({dn[T['druck_d']]}), Wand 3", f"x {x0 + ml + kl / 2:.0f}, y {yc:.0f}, z {za + kd / 2 + 70:.0f}", "Wasser tritt aus, Oeffnung zeigt +Z"])
        ports.append([f"{typ}: Stromanschluss (Kabel 3 x 1,5 mm2 mit Schutzkontaktstecker)", "230 V, Stecker 55 x 45 x 40", f"x {x0 - 150 - P['plug_l'] / 2:.0f}, y {yc:.0f}, z {za:.0f}", "Strom ein; Kabel laeuft nach -X (Laenge 150 modelliert, real 1,5-3 m)"])
        ports.append([f"{typ}: Standwinkel (Befestigung am Boden)", "2 Winkel 50 x 100 x 5 hinten an der Tafel", f"x +-{L / 2 - 60:.0f}, y {-t / 2 - 40:.0f}, z 0", "Befestigung auf dem Boden (Schrauben nicht modelliert), Richtung -Z"])
        gew.append(f"{typ}: leer {mass:.1f} kg (Tafel PP, Pumpe Kunststoff, Konsole Stahl); Pumpe real je nach Fabrikat 4-9 kg [A]; Betriebsfuellung der Pumpe ca. 0,5 l")
        sl.append(f"{typ} (je Modul, Menge {T['anzahl']} gesamt = 2 je Tank): Montagetafel PP {L}x{t}x{H} 1, Standwinkel 50x100x5 2, Pumpenkonsole 150x100x5 + 40 hoch 1, Pumpensockel 1, Kreiselpumpe (Motor D{md} x {ml}, Kopf D{kd} x {kl}) 1 mit Stutzen d{T['saug_d']} und d{T['druck_d']}, Kabel mit Stecker 1, Schrauben M6x16 ISO 4017 mit Muttern ISO 4032 2")
    else:
        L, t, H = T["box_l"], T["box_t"], T["box_h"]
        w = P["wall"]
        dep = t - P["lid_t"]
        vol = (L - 2 * w) * (dep - w) * (H - 2 * w) / 1e6
        ports.append([f"{typ}: Einlass (Stutzen oben, +X-Ende)", f"PVC-U d{T['port_d']} (DN40), Wand 3", f"x {L / 2 - 60:.0f}, y {-t / 2 + dep / 2:.1f}, z {H + 60:.0f}", "Wasser tritt ein, Oeffnung zeigt +Z"])
        ports.append([f"{typ}: Auslass (Stutzen seitlich unten, -X-Wand)", f"PVC-U d{T['port_d']} (DN40), Wand 3", f"x {-L / 2 - 60:.0f}, y {-t / 2 + dep / 2:.1f}, z 70", "Wasser tritt aus, Oeffnung zeigt -X"])
        ports.append([f"{typ}: Montagelaschen (4 Stueck, je 1 Schraube M6x16)", "M6x16 ISO 4017, Loch D7, Lasche 30 x 5 x 40", f"x +-{L / 2 + 15:.0f}, y {-t / 2:.0f}, z {H * 0.15:.0f} und {H * 0.85:.0f}", "Befestigung an der Montageflaeche (z. B. Tankbein), Richtung -Y"])
        gew.append(f"{typ}: leer {mass:.2f} kg; gefuellt: Wasserraum {vol:.1f} l = ca. {vol:.1f} kg (Siebeinsatz als Matte, Porenanteil nicht abgezogen) [E]")
        sl.append(f"{typ} (je Modul, Menge {T['anzahl']} gesamt = 5 je Tank gross): Gehaeuse PP {L}x{t - P['lid_t']}x{H} (Wand 3) 1, Deckel PP {L}x{P['lid_t']}x{H} 1, Siebeinsatz (Filtermatte) 1, Stutzen d{T['port_d']} 2, Montagelaschen 4, Schrauben M6x16 ISO 4017 4, Deckelschrauben M6x14 ISO 4017 4 (im Modell, 2 Stueck mehr in Reserve)")
bl = {
    "funktion": "Pump-/Filtermodule an den Tanks (Rolle laut docs/components.md Annahme): Pumpenmodul = Montagetafel mit Kreiselpumpe fuer den Umlauf; Filtermodul = flache Filterkassette mit Siebeinsatz (Feinfilter, Matte) im Wasserweg zwischen Absetzer und Biofilter. Ob die OBJ-Platten wirklich Pumpentafeln und die 384-mm-Kassetten Filter sind, ist offen.",
    "querschnitt": "Pumpenmodul: Montagetafel PP (502x5x345 bzw. 693x7x463) stehend auf zwei Standwinkeln; Konsole aus Winkel 5 mm mit Pumpensockel; Pumpe: Motor (D90 x 150 / D110 x 180) + Pumpenkopf (D110 x 70 / D130 x 80), Saugstutzen axial, Druckstutzen nach oben; Kabel mit Stecker. Filtermodul: Gehaeuse 384x39x419 PP, Wand 3 mm, Deckel 5 mm, Siebeinsatz 4 mm Spiel; Einlass oben, Auslass seitlich unten; vier Montagelaschen.",
    "toleranzen": "Tafel-/Gehaeusemasse = OBJ (Pruefung +-0,5 mm); Siebeinsatz 4 mm Spiel zur Gehaeusewand; Pumpensockel liegt auf der Konsole (tangentialer Kontakt Motor/Sockel).",
    "ports": ports,
    "verbindungen": ["Konsole an der Tafel: je 2 Schrauben M6x16 ISO 4017 mit Mutter ISO 4032 (im Modell), Tafel steht auf 2 Standwinkeln (am Boden/Tankbein zu verschrauben, nicht modelliert)", "Pumpe auf dem Sockel: 4 Schrauben M6 (nicht modelliert) [A]", "Filtermodul: 4 Montagelaschen mit Schrauben M6x16; Deckel mit 4 Schrauben M6x14 (im Modell; Gewindeeinsaetze/Flansch nicht modelliert)", "Stutzen PVC-U d40/d50 (DIN 8062): geklebt oder mit Verschraubung am Rohrnetz (Montage)"],
    "abweichung": "layout.json tanks[].modules: Tafel- und Kassettenmasse 502x5x345 / 693x7x463 / 384x44x419 stimmen (0 mm Abweichung); Lage und Drehung je Modul stehen in layout.json (yaw, z0: Tafeln am Boden Z -6..3, Kassetten z0 249-256 an den Tankbeinen) und sind Sache des Integrators. Die Rolle der Module ist Annahme (docs/components.md); im OBJ sind es nur Platten/Kassetten ohne Pumpe, Anschluesse oder Kabel; Pumpe, Konsole, Stutzen, Kabel sind [A].",
    "montage": ["Standwinkel an der Tafelrueckseite anschrauben, Tafel am vorgesehenen Platz ausrichten und befestigen", "Konsole an die Tafel schrauben, Pumpe mit Sockel aufsetzen und fixieren", "Saug- und Druckstutzen mit dem Rohrnetz verbinden (Montage-Sitzung), Kabel zum Schaltschrank fuehren, Stecker anschliessen", "Filtermodul: Laschen anschrauben (z. B. am Tankbein), Ein-/Auslass anschliessen, Siebeinsatz einsetzen, Deckel verschrauben"],
    "werkzeug": "Akkuschrauber, Schluessel M6, Wasserwaage, Rohrschneider, PVC-Kleber",
    "stueckliste": sl + ["Module gesamt: Pumpenmodul klein 4, gross 4, Filtermodul 10 (layout.json tanks[].modules; Duplikate des OBJ zusammengefasst)"],
    "lokal": "Pumpe: handelsuebliche Kreiselpumpe (Teich-/Umwaelzpumpe) auf Montagebrett; Filtermodul: Kunststoff-Kassette aus dem Aquaristik-/Teichbedarf mit Filtermatte (Feinfilter).",
    "referenz": "reference/ref-4/ref-5: Module im Bild nicht erkennbar; data/layout.json tanks[].modules (nur Boxen); docs/components.md (Rolle Annahme); docs/hydraulics.md (Wasserweg)",
    "varianten": ["pumpe_klein", "pumpe_gross", "filtermodul"],
    "gewicht_gefuellt": " | ".join(gew),
    "boxen": boxes,
    "render_dirs": ["filtermodul"],
    "pruefung": ["scripts/workshop/check_pumpe.py (Ergebnis renders/components/pumpe_klein/check.txt)", "Kein Bild-Kritiker: die Module sind in keiner Referenz sichtbar; Spec-Pruefer und Orchestrator-Stichprobe"],
    "offen": ["Rolle der Module (Pumpentafel/Filterkassette) ist Annahme; OBJ liefert nur Boxen", "Pumpenfabrikat, Foerderstrom und Leistung offen (R07 pausiert)", "Schrauben der Pumpe auf dem Sockel, Standwinkel-Befestigung und Deckel-Flansch nicht modelliert", "Kabel gerade und 150 mm kurz modelliert (real 1,5-3 m)", "Lage der 693-mm-Tafeln am Boden und der Kassetten an den Tankbeinen: Integrator"],
}
d["blatt"] = bl
d["herkunft_tabelle"] = [
    ["Tafel klein 502 x 5 x 345 (2 je Tank, 4 gesamt)", "502x5x345 mm", "OBJ", "layout.json tanks 1 und 4 modules (Duplikate zusammengefasst)", "hoch"],
    ["Tafel gross 693 x 7 x 463 (2 je Tank, 4 gesamt)", "693x7x463 mm", "OBJ", "layout.json tanks 2 und 3 modules", "hoch"],
    ["Filterkassette 384 x 44 x 419 (5 je Tank gross, 10 gesamt)", "384x44x419 mm", "OBJ", "layout.json tanks 2 und 3 modules (z0 249-256, yaw je 90 Grad versetzt)", "hoch"],
    ["Rolle: Tafel = Pumpenmodul, Kassette = Filtermodul", "-", "A", "docs/components.md: Bedeutung Annahme; docs/hydraulics.md: Pumpen, Feinfilter (Matten) im Wasserweg", "niedrig"],
    ["Kreiselpumpe: Motor D90 x 150 / D110 x 180, Kopf D110 x 70 / D130 x 80, Achse 120 ueber der Tafelunterkante", "mm", "A", "typische Teich-/Umwaelzpumpen; keine Quelle (R07 pausiert)", "niedrig"],
    ["Saug-/Druckstutzen d40/d32 (klein) und d50/d40 (gross)", "d40/d32; d50/d40", "A", "Rohr d50/d63 am Tank (R09 A); DN der Pumpen Annahme", "niedrig"],
    ["Konsole Winkel 5 mm, 150 breit; Pumpensockel", "150 x 5 mm", "A", "Konstruktionspraxis", "niedrig"],
    ["Standwinkel 50 x 100 x 5 (2 je Tafel)", "50x100x5", "A", "gegen Kippen", "niedrig"],
    ["Kabel 3 x 1,5 mm2 (D8) mit Schutzkontaktstecker", "D8", "A", "230 V Standard; Laenge modelliert 150 mm", "niedrig"],
    ["Filtergehaeuse Wand 3 mm, Deckel 5 mm, Siebeinsatz mit 4 mm Spiel", "3 / 5 / 4 mm", "A", "Kunststoffgehaeuse Praxis", "niedrig"],
    ["Ein-/Auslass d50 (DN40): Einlass oben, Auslass seitlich unten", "d50", "A", "Wasserweg: Zulauf oben, Ablauf unten (Schwerkraft); keine Quelle", "niedrig"],
    ["Montagelaschen 30x5x40 mit M6x16", "M6", "A", "Befestigung an Tankbein/Wand (OBJ: Kassetten stehen an den Tankbeinen)", "niedrig"],
    ["Werkstoffe PP 0,91, Stahl 7,85, PVC 1,4", "g/cm3", "Fachwert", "Handbuchwerte", "mittel"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pumpe.json gepflegt")
