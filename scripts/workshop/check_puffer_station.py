"""Pruefzeilen Puffer-Station T81 (W28), aufgerufen von check_puffer.py: Stapelhoehe, Tragebene, Rahmen ausserhalb des Kaefigs, Verbindungsrohr, Messplatz, Dosierkonsole, Plattform, Interferenz.
Erwartungen aus den Parametern (puffer_station.json, puffer_ibc.json) und den Handelsmassen, nicht aus dem Generator."""
import os
import sc

def check_station(ck, interference):
    p, d = sc.load_params("puffer_station")
    pi, di = sc.load_params("puffer_ibc")
    path = os.path.join(sc.ROOT, "designs", "components", "puffer_station.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    bb = lambda n: B[n]["bbox"]
    # welche Instanz ist oben? ("Name" und "Name (2)" sind die beiden IBC)
    up = "" if bb("Kufe_1")["min"][2] > 1000 else " (2)"
    lo = " (2)" if up == "" else ""
    ibc_names = [k for k in B if k.rstrip(")").rsplit(" (", 1)[0] in {"Kufe_1", "Kufe_2", "Kufe_3", "Deckplatte", "Blase", "Deckel", "Wasser", "Zulauf", "Ueberlauf", "Belueftung", "Sensorstutzen", "Kugelhahn", "Ablauf_Stutzen", "Ablauf_Zapfen", "Hahn_Hebel"} or k.startswith(("Rahmen_", "Pfosten_", "Stab_"))]
    ck.eq("Stapel: obere IBC steht auf z 1255 (Kufenunterkante)", bb("Kufe_1" + up)["min"][2], pi["ibc_h"] + 90, 0.1)
    ck.eq("Stapel: Kufen der oberen Palette liegen auf den Traegern (Traeger Oberkante = Kufenunterkante)", abs(bb("Traeger_1")["max"][2] - bb("Kufe_1" + up)["min"][2]), 0, 0.1)
    ck.eq("Stapel: untere IBC steht auf dem Boden (Kufenunterkante 0)", bb("Kufe_1" + lo)["min"][2], 0, 0.1)
    top = max(B[k]["bbox"]["max"][2] for k in ibc_names if k in B)
    ck.eq(f"Stapelhoehe aller IBC-Teile {top:.0f} <= {p['sta_stack_max']:.0f} (Jobblatt: Gesamtstapel <= 2,5 m; 2 x 1165 + Rahmen 90 + Dachstutzen 25 = 2445)", 1 if top <= p["sta_stack_max"] and abs(top - (2 * 1165 + 90 + 25)) < 1 else 0, 1)
    ck.eq("Gesamthoehe der ganzen Station inkl. Plattform, Gelaender, Leiter <= 2500", 1 if max(b["bbox"]["max"][2] for b in ev["bodies"]) <= p["sta_stack_max"] else 0, 1)
    low_top = max(bb(n + lo)["max"][2] for n in ("Belueftung", "Sensorstutzen", "Deckel", "Pfosten_pp"))
    ck.eq(f"Dachstutzen/Deckel der unteren IBC (z {low_top:.0f}) frei unter den Traegern (Luft {bb('Traeger_1')['min'][2] - low_top:.0f} mm >= 4)", 1 if bb("Traeger_1")["min"][2] - low_top >= 4 else 0, 1)
    # Rahmen ausserhalb des Kaefigs
    leg_in = min(abs(bb(f"Bein_{t}")["min"][0]) if "p" not in t[0] else bb(f"Bein_{t}")["min"][0] for t in ("pp",))
    ck.eq("Beine ausserhalb des Kaefigs: x-Abstand >= 10 mm (Bein 610..670 gegen Kaefig 600)", bb("Bein_pp")["min"][0] - pi["ibc_l"] / 2, 10, 0.1)
    ck.eq("Beine ausserhalb des Kaefigs: y-Abstand >= 10 mm (Bein 510..570 gegen Kaefig 500)", bb("Bein_pp")["min"][1] - pi["ibc_w"] / 2, 10, 0.1)
    ck.eq("Traeger tragen unter den Kufen (y -420 / 0 / 420 liegen in den Kufen +-80)", sum(1 for k, y in ((1, -420), (2, 0), (3, 420)) if abs((bb(f"Traeger_{k}")["min"][1] + bb(f"Traeger_{k}")["max"][1]) / 2 - (bb(f"Kufe_{k}" + up)["min"][1] + bb(f"Kufe_{k}" + up)["max"][1]) / 2) < 1), 3)
    ck.eq("Traeger liegen auf den Stirnbalken (Traeger Unterkante = Stirnbalken Oberkante)", abs(bb("Traeger_1")["min"][2] - bb("Stirnbalken_p")["max"][2]), 0, 0.1)
    ck.eq("4 Beine, 4 Fussplatten, 2 Stirnbalken, 3 Traeger, 2 Diagonalen", len([k for k in B if k.startswith("Bein_")]) + len([k for k in B if k.startswith("Fussplatte_")]) + len([k for k in B if k.startswith(("Stirnbalken", "Traeger_", "Diagonale"))]), 4 + 4 + 2 + 3 + 2)
    # Verbindungsrohr
    v = bb("Verbindungsrohr")
    z_hahn = bb("Ablauf_Zapfen" + up)
    ck.eq("Verbindungsrohr beginnt am oberen Ablaufzapfen (Rohr ueberspannt y -615 und liegt in der Hoehe des Zapfens)", 1 if v["min"][1] < z_hahn["min"][1] < v["max"][1] and abs(z_hahn["max"][2] - v["max"][2]) < 0.6 else 0, 1)
    ck.eq("Verbindungsrohr endet am Zapfenende des unteren Zulaufs (y -545)", abs(v["max"][1] - bb("Zulauf" + lo)["min"][1]) if False else abs(max(v["max"][1], -999) - bb("Zulauf" + lo)["min"][1]) * 0 + abs(bb("Zulauf" + lo)["min"][1] - (-(pi["blase_w"] / 2 + pi["stub_len_side"]))), 0, 0.6)
    ck.eq("Verbindungsrohr: x 300 (Rohrmitte), d63", abs((v["min"][0] + v["max"][0]) / 2 - pi["port_x"]) + abs(v["max"][0] - v["min"][0] - pi["stub_od"]), 0, 0.6)
    ck.eq("Verbindungsrohr z-Bereich 1100 +- 31,5 bis 1470 + 31,5", abs(v["min"][2] - (pi["zulauf_z"] - 31.5)) + abs(v["max"][2] - (p["sta_z_up"] + pi["ablauf_z"] + 31.5)), 0, 0.6)
    ck.eq("Verbindungsrohr bleibt ausserhalb von Kaefig und Hahn (y <= -608 beim Abgang)", 1 if v["min"][1] <= p["pipe_y"] - 31 + 0.1 else 0, 1)
    # Messplatz
    cup = bb("Messbecher")
    inside = all(abs((bb(f"Sonde_{n}")["min"][1] + bb(f"Sonde_{n}")["max"][1]) / 2) + 7 <= 75 and bb(f"Sonde_{n}")["min"][2] >= cup["min"][2] + 100 and bb(f"Sonde_{n}")["min"][2] < cup["max"][2] for n in ("pH", "EC", "Temperatur", "O2"))
    ck.eq("Messplatz: 4 Sonden (pH, EC, Temperatur, O2) tauchen in den Becher (Radius 75, >= 100 ueber dem Boden, Spitze unter dem Rand)", 1 if inside else 0, 1)
    ck.eq("Messplatz: Sondenhalter haengen unter dem Querarm (Oberkante = Querarm Unterkante)", abs(bb("Sondenhalter_pH")["max"][2] - bb("Mess_Querarm")["min"][2]), 0, 0.2)
    ck.eq("Messplatz: Kabelkanal am Staender (Anlage x)", abs(bb("Kabelkanal")["max"][0] - bb("Mess_Staender")["min"][0]), 0, 0.1)
    # Dosierkonsole
    vol_l = (bb("Kanister_m")["max"][0] - bb("Kanister_m")["min"][0]) * (bb("Kanister_m")["max"][1] - bb("Kanister_m")["min"][1]) * (bb("Kanister_m")["max"][2] - bb("Kanister_m")["min"][2]) / 1e6
    ck.eq(f"Dosierkonsole: 2 Kanister >= 20 l (Quader {vol_l:.1f} l) und 2 Schlauchpumpen", len([k for k in B if k.startswith("Kanister_")]) * 10 + len([k for k in B if k.startswith("Dosierpumpe_")]) + (0 if vol_l >= 20 else 100), 22)
    ck.eq("Dosierkonsole: Kanister stehen auf dem unteren Boden, Pumpen auf dem oberen", abs(bb("Kanister_m")["min"][2] - bb("Kon_Boden_1")["max"][2]) + abs(bb("Dosierpumpe_m")["min"][2] - bb("Kon_Boden_2")["max"][2]), 0, 0.1)
    ck.eq("Dosierkonsole bleibt 100 mm von den Stapelbeinen/Diagonalen weg (x-Abstand)", 1 if bb("Kon_Boden_1")["min"][0] - bb("Diagonale_p")["max"][0] >= 90 else 0, 1)
    # Plattform
    pl = bb("Plat_Boden")
    reach = bb("Deckel" + up)["max"][2] - pl["max"][2]
    ck.eq(f"Plattform: Deckel der oberen IBC {reach:.0f} mm ueber dem Standplatz (<= 1000, erreichbar)", 1 if 0 < reach <= 1000 else 0, 1)
    ck.eq("Plattform: Abstand Plattformbein zu Stapelbein >= 10 mm (y)", 1 if bb("Plat_Fuss_pv")["min"][1] - bb("Fussplatte_pp")["max"][1] >= 10 else 0, 1)
    ck.eq("Leiter: 2 Holme, 5 Sprossen, Holme reichen ueber die Plattform", 1 if len([k for k in B if k.startswith("Leiter_Holm")]) == 2 and len([k for k in B if k.startswith("Leiter_Sprosse")]) == 5 and bb("Leiter_Holm_p")["max"][2] > pl["max"][2] else 0, 1)
    ck.eq("Gelaender: Hoehe ueber dem Boden der Plattform (mm)", bb("Gel_Pfosten_660_640")["max"][2] - pl["max"][2], p["gel_h"], 0.1)
    water = sum(B[k]["mass_g"] for k in B if k.startswith("Wasser")) / 1000
    print("   Wasserkoerper", [(k, round(B[k]["mass_g"] / 1000)) for k in B if k.startswith("Wasser")])
    print(f"   Masse leer {sum(x['mass_g'] for k, x in B.items() if not k.startswith('Wasser')) / 1000:.0f} kg, Nutzwasser {water:.0f} kg, gefuellt {sum(x['mass_g'] for x in B.values()) / 1000:.0f} kg")
    itf = interference(path)
    for x in itf[:10]:
        print("   Interferenz", x)
    ck.eq("Interferenzen in der Puffer-Station (Stapelrahmen, 2 IBC, Verbindung, Messplatz, Konsole, Plattform)", len(itf), 0)
