"""Blatt-Inhalt tuer_komplett (T50) und Nachtrag haut_paneel (Tuerfeld, Variante BBB_tuer) fuer W20 Schritt 5; Zahlen aus tuer_komplett.json und der Messung. Idempotent; danach partsheet.py tuer_komplett und haut_paneel.
Aufruf: python scripts/workshop/fix_tuer_blatt.py"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))

p, d = load("tuer_komplett")
P = {k: v["wert"] for k, v in d["parameter"].items()}
G = d["geometrie"]
ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "tuer_komplett.sc"))
mass = sum(b["mass_g"] for b in ev["bodies"]) / 1000
m_blatt = [b for b in ev["bodies"] if b["name"] == "Tuerblatt"][0]["mass_g"] / 1000
m_zarge = sum(b["mass_g"] for b in ev["bodies"] if b["name"] in ("Schwelle", "Pfosten_links", "Pfosten_rechts", "Sturz")) / 1000
fw, lh, lw = G["zarge_aussen_w"], G["lichte_h"], G["lichte_w"]
S = G["hang_laenge_spitze"]
s_mid = P["schwelle_h"] + lh + P["rohr"] / 2
w_mid = G["basis_w"] * (1 - s_mid / S)
d["werkstoff"] = {"name": "Stahl verzinkt (Zarge, Beschlaege), Tuerblatt Sandwich, EPDM (Dichtung)", "dichte_g_cm3": 7.85, "farbe": "#aeb4b8", "herkunft": "[A] Zarge Rechteckrohr 30 x 30 x 2 verzinkt; Tuerblatt Sandwich 0,31 g/cm3 (ca. 25 kg fuer 1 x 2 x 0,04 m, Normtuer-Richtwert, nicht recherchiert); EPDM 1,1 g/cm3"}
bl = d.setdefault("blatt", {})
bl["funktion"] = "Eingang der Kuppel: rechteckige Zarge aus Rohr 30 x 30 x 2 (Schwelle, 2 Pfosten, Sturz) in der Ebene des Basisfeldes BBB 149,2 (D36) mit Normtuerblatt 1000 x 2000 x 40, nach aussen oeffnend, 3 Aufschraubbaendern, Druecker, Anschlag und Dichtung."
bl["querschnitt"] = f"Zarge Aussenbreite {fw:.0f} x Hoehe {G['zarge_hoehe']:.0f} (in der Feldebene gemessen, Neigung der Feldebene {G['neigung_feldebene_grad']:.1f} Grad zur Senkrechten, senkrechte Hoehe {G['senkrechte_hoehe_sturz']:.0f}), Lichte {lw:.0f} x {lh:.0f}; Blatt 1000 x 2000 x 40 mit Spiel 8 seitlich / 6 oben / 2 unten; Anschlag Flachstahl 14 x 3 innen, Dichtung EPDM 6 x 1; Beschlaege: 3 Aufschraubbaender links (Lasche 48 x 90 x 4, Bolzen D10), Druecker rechts auf 1 m (Rosette D50, Hebel 130)."
bl["toleranzen"] = f"Spiel Blatt zu Zarge 8 mm je Seite, oben 6, unten 2 (gemessen); Zarge passt ins Feld: Feldbreite in Sturzhoehe {G['feldbreite_sturz_oben']:.0f} mm gegen Zarge {fw:.0f}, Reserve {G['reserve_je_seite_sturz']:.0f} mm je Seite (>= 100)."
bl["ports"] = [
    ["Anschluss Sturz links / rechts an die schraege Strebe (Knoten 24-6 / 22-6)", "Flachstahl-Lasche 30 x 4, Schrauben M6 [A, nicht modelliert]", f"Sturzende x +-{fw / 2:.0f}, y' {s_mid:.0f}, z' 0; Strebenachse bei x +-{w_mid / 2:.0f} (Luecke {(w_mid - fw) / 2:.0f} mm je Seite)", "Sturz liegt in der Feldebene, Strebe verlaeuft schraeg nach oben; die Lasche ueberbrueckt die Luecke"],
    ["Anschluss Pfosten / Schwelle an den Boden", "Ankerplatten 70 x 70 x 5 mit M8 [A, nicht modelliert]", f"Schwellenenden x +-{fw / 2:.0f}, y' 0..{P['schwelle_h']:g}", "Zarge steht auf dem Fundament/Boden; Tuer ist hoch beanspruchte Zone (R13: zusaetzliche Bodenverankerung)"],
    ["Basisstrebe: Mittelstueck zwischen den Pfosten entfaellt", "Strebe 3708 (Knoten 24-22) wird gekuerzt", f"Basiskante y' 0, x +-{G['basis_w'] / 2:.0f}; es entfaellt das Mittelstueck x +-{fw / 2:.0f}, es bleiben Reststrecken von {(G['basis_w'] - fw) / 2:.0f} mm je Seite (je eine Kappe T41 mit len {(G['basis_w'] - fw) / 2:.0f})", "die Schwelle ersetzt das Mittelstueck der Basisstrebe (R13); im Dom wird die Strebe gekuerzt (Montage)"],
    ["Tuerausschnitt im Paneel BBB", "haut_paneel_BBB_tuer.sc", f"Rechteck {fw:.0f} x {G['zarge_hoehe']:.0f} ab der Basiskante, mittig", "Paneel liegt aussen an der Zarge; Ausschnitt = Zarge-Aussenmass"]]
bl["verbindungen"] = ["Zarge geschweisst (MAG) und verzinkt [A]; Anschluss an die Streben ueber Laschen mit M6 (nicht modelliert)", "Aufschraubbaender: Zargenlasche auf dem linken Pfosten, Blattlasche auf dem Blatt, Bolzen D10 dazwischen; Schrauben der Baender nicht modelliert", "Anschlag Flachstahl 14 x 3 innen auf Pfosten und Sturz geklebt/genietet [A], Dichtung EPDM darauf"]
bl["abweichung"] = "keine OBJ-Vorgabe fuer die Tuer ausser Normmass 1000 x 2000 und Azimut 167 (OBJ); D36 legt die Tuer mittig in das Basisfeld BBB 149,2 (Azimut 149,2) statt auf den Basisknoten 22."
bl["montage"] = ["Zarge in die Feldebene stellen (Schwelle am Boden, Pfosten parallel zu den Hangkanten ausrichten), Sturz-Laschen an die schraegen Streben schrauben, Basisstrebe zwischen den Pfosten entfernen", "Anschlag und Dichtung innen setzen, Blatt mit den 3 Baendern einhaengen (oeffnet nach aussen), Druecker montieren", "Paneel BBB_tuer auflegen (Ausschnitt an der Zarge), Seitenfelder neben der Tuer sind Teil des Paneels"]
bl["werkzeug"] = "Schweissgeraet, Akkuschrauber, Wasserwaage, Bohrmaschine"
bl["stueckliste"] = [f"T50 Tuer komplett: Zarge Rohr 30 x 30 x 2 (Schwelle {fw:.0f}, 2 Pfosten {lh:.0f}, Sturz {fw:.0f}) {m_zarge:.1f} kg; Tuerblatt 1000 x 2000 x 40 {m_blatt:.1f} kg; 3 Aufschraubbaender; Druecker (Rosette D50 + Hebel) innen/aussen; Anschlag 3 Leisten; Dichtung EPDM 3 Streifen; gesamt {mass:.1f} kg (1 Stueck)"]
bl["lokal"] = "Normtuer 1000 x 2000 (Stahl-/Holzsandwich) ist Baumarktware; Zarge selbst geschweisst oder aus Systemprofil; Beschlaege Standard [A, nicht recherchiert]."
bl["pruefung"] = ["scripts/workshop/check_tuer.py (30/30 PASS, Ergebnis renders/components/tuer_komplett/check.txt): Lichte, Spiel, Zarge im Feld (Reserve), Neigung und Feldtyp aus den Knoten, Beschlaege, Interferenz 0, Paneelausschnitt gegen numerische Rechnung", "Bilder renders/components/tuer_komplett/ und renders/components/haut_paneel/haut_paneel_BBB_tuer-01-draufsicht.png; kein Spec-Pruefer, kein Bild-Kritiker (Auftrag W20)"]
bl["kritiker"] = "offen (kein Pruefer-Lauf, Auftrag W20)"
bl["offen"] = ["Zarge in der Feldebene (Neigung 10,8 Grad) ist Annahme A (R13 nennt auch rechteckigen senkrechten Rahmen mit verlaengerten Streben); ein senkrechter Rahmen braeuchte Tiefe 388 mm am Sturz (603 mm an der Spitze), Entscheidung Orchestrator/Ben", "Anschlag-Laschen an die Streben, Bodenanker, Schrauben der Baender, Schloss/Schliessblech nicht modelliert; Statik (Schnee/Wind auf Sturz, R13 Befund 8) nicht gerechnet", "Oeffnungsrichtung nach aussen (Shelter Dome, R13) und Windfang offen (Ben: wohin soll die Tuer)", "Platzhalter designs/components/tuer.sc (Integrator, alter Stand) ist durch tuer_komplett.sc zu ersetzen (Montage)", "Zweites Becken muss auf die Tuerachse 149,2 gedreht werden (D36, Montage)", "Spitze Z: D36/W20 3140 absolut = 3154 relativ zu base_z -14 (R13 rundet 3150); Schwelle liegt auf Basisknotenhoehe -14, nicht auf Erdniveau 0 (Sockel/Fundament offen im Tuerfeld)", "Zarge liefert nur das Mass; der Tuerausschnitt gehoert dem Paneel T40 (haut_paneel.py liest tuer_komplett.json, check_tuer prueft die Paneelflaeche): Zustaendigkeit bei Gelegenheit trennen", "Reserve 122 mm je Seite gilt zur Strebenachse; zur Strebenkante (Rohr 30, 17,3 mm) sind es 105 mm"]
d["herkunft_tabelle"] = [
    ["Tuer mittig im Basisfeld BBB 149,2", "Azimut 149,2", "OBJ + E", "D36: Spitze Z 3140, 1353 mm breit in 2 m (R13); Feld aus layout.json dome.nodes_list (Knoten 24, 22, 6)", "mittel"],
    ["Normtuer 1000 x 2000 x 40", "1000 x 2000 x 40", "OBJ + A", "docs/components.md Tuer 1000 x 2000 (OBJ-Normtuer), Dicke 40 Annahme", "mittel"],
    ["Zarge Rohr 30 x 30 x 2, Schwelle 30", "30 x 30 x 2", "A", "Auftrag W20 (Rohr wie die Streben); R13 Befund 8: kein belastbares Mass fuer Sturz/Schwelle", "niedrig"],
    ["Spiel 8 seitlich, 6 oben, 2 unten", "8 / 6 / 2 mm", "A", "Normtuer-Praxis 5-10 mm", "niedrig"],
    ["Zarge in der Feldebene, Neigung 10,8 Grad", f"{G['neigung_feldebene_grad']:.1f} Grad", "A", "Neigung gerechnet (E) aus den Knoten 24, 22, 6 (layout.json); die WAHL der Feldebene statt des senkrechten Rahmens ist Annahme (R13 Befund 2 nennt rechteckigen Rahmen mit verlaengerten Streben)", "niedrig"],
    ["Blatt oeffnet nach aussen, Anschlag innen", "nach aussen", "A", "R13 Befund 7 (Shelter Dome: oeffnet nach aussen)", "niedrig"],
    ["3 Aufschraubbaender, Druecker auf 1 m, Dichtung EPDM", "3 + 1 + 1", "A", "Standard-Tuerbeschlag; Beschlagmasse Annahme", "niedrig"],
    ["Tuerblatt 0,31 g/cm3 (25 kg)", "0,31 g/cm3", "A", "Sandwich-Tuerblatt 1 x 2 x 0,04 m ca. 25 kg (Richtwert, nicht recherchiert)", "niedrig"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------- haut_paneel: Tuerfeld nur BBB 149,2 (D36), Variante BBB_tuer
p, d = load("haut_paneel")
bl = d["blatt"]
bl["varianten"] = ["haut_paneel_AAB", "haut_paneel_BBB", "haut_paneel_BBB_tuer"]
bl["verbindungen"] = [x if not x.startswith("Tuerfelder:") else "Tuerfeld (D36): das Basisfeld BBB 149,2 bekommt das Paneel haut_paneel_BBB_tuer mit Ausschnitt = Zarge (1076 x 2068, in der Feldebene) ab der Basiskante; Zarge siehe docs/parts/tuer_komplett.md" for x in bl["verbindungen"]]
bl["montage"] = [x if not x.startswith("Tuerfelder") else "Tuerfeld BBB 149,2: Paneel BBB_tuer auflegen (Ausschnitt an der Zarge)" for x in bl["montage"]]
bl["stueckliste"] = [x.replace("0 mit Tuerausschnitt", "0 mit Tuerausschnitt") for x in bl["stueckliste"]]
bl["offen"] = [x if not x.startswith("Tuer: die zwei Basisfelder") else "Tuer (D36): nur das Basisfeld BBB 149,2 (Basisknoten-Azimut 149,2) traegt den Tuerausschnitt (haut_paneel_BBB_tuer.sc, 9 Flaechen); Zargenlage in der Feldebene Annahme A (siehe tuer_komplett)" for x in bl["offen"]]
d["herkunft_tabelle"] = [r if not r[0].startswith("Tuer bei Azimut 167") else ["Tuerfeld BBB 149,2 (D36)", "1 Feld", "E", "D36 (30.10.): Tuer mittig im Basisfeld BBB 149,2 statt auf Knoten 22 (OBJ Azimut 167 beruehrte zwei Felder); Ausschnitt = Zarge Aussenmass (tuer_komplett.json)", "mittel"] for r in d["herkunft_tabelle"]]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("tuer_komplett/haut_paneel Blatt-Inhalt gepflegt, Masse", round(mass, 1), "kg")
