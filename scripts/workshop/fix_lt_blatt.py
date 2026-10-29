"""Sammelblatt docs/parts/leitungsteile.md und data/components/leitungsteile.json (Parameter, Herkunft) aus leitung.py und der Messung der 49 Dateien."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

D = os.path.join(sc.ROOT, "designs", "components")
def mass(fn):
    ev = sc.evaluate(os.path.join(D, fn + ".sc"))
    return sum(b["mass_g"] for b in ev["bodies"]) / 1000

rows = []
masses = {}
for d in L.SIZES:
    m = {t: mass(f"lt_{t}_d{d}") for t in ("rohr", "kupplung", "bogen90", "bogen45", "t", "kugelhahn", "klemme")}
    masses[d] = m
    rows.append(f"| d{d} | {L.DN[d]} | {L.wall_p(d)} | {L.DEPTH[d]} | {L.od_f(d):.1f} | {max(L.od_f(d), 1.2 * d):.0f} | {m['rohr']:.2f} | {m['kupplung']:.3f} | {m['bogen90']:.3f} | {m['bogen45']:.3f} | {m['t']:.3f} | {m['kugelhahn']:.3f} | {m['klemme']:.3f} |")
hose = {i: (mass(f"lt_schlauch_id{i}"), mass(f"lt_schlauchbogen90_id{i}")) for i in (16, 25)}
vt = {n: mass(f"lt_verteiler_d32_n{n}") for n in (2, 3, 4)}
P = {"sizes": {str(d): dict(dn=L.DN[d], wand=L.wall_p(d), muffentiefe=L.DEPTH[d], formstueck_aussen=round(L.od_f(d), 2), bogenradius=round(max(L.od_f(d), 1.2 * d), 1)) for d in L.SIZES},
     "schlauch": {"16": dict(aussen=23.0, farbe="hellblau", biegeradius=115.0), "25": dict(aussen=32.0, farbe="dunkelblau", biegeradius=160.0)}}
md = []
md.append("# Sammelblatt Leitungsteile-Bibliothek T70 (erzeugt von `scripts/workshop/fix_lt_blatt.py`, Dateien aus `scripts/workshop/leitung.py`, Pruefung `check_leitungsteile.py` 78/78)\n")
md.append("**Funktion:** Normteile des Rohrnetzes als Komponenten mit Ports: Rohr, Kupplung (Doppelmuffe), Bogen 90/45 Grad, T-Stueck, Kugelhahn, Rohrklemme, Schlauch gerade und Bogen, Verteiler. Die Montage-Sitzung verlegt sie nach `data/system.json` (Wegfuehrung gehoert NICHT in diese Klasse). Dateien `designs/components/lt_<teil>_d<groesse>.sc` (49 Stueck).\n")
md.append("**Scope-Card:** DRIN Geometrie und Ports je Teil, DN parametrisch, Biegeradius Schlauch >= 5 x AD, Farben nach `docs/hydraulics.md` 5; DRAUSSEN Verlegung, Anschlussreihenfolge, `routing surface/buried`.\n")
md.append("## Konvention (Bauteil-Koordinatensystem)\n")
md.append("Port A liegt im Ursprung (Rohr-/Schlauchachse +Z, bei Bogen/T in der XZ-Ebene). Alle Maße in mm. Ports (Name, DN, Lage, Richtung der Oeffnung):\n")
md.append("| Teil | Port | Lage x, y, z | Richtung (Oeffnung) |\n|---|---|---|---|")
md.append("| Rohr (Laenge L, Standard 1000) | A | 0, 0, 0 | -Z |")
md.append("| Rohr | B | 0, 0, L | +Z |")
md.append("| Kupplung (L = 2 x Muffentiefe + 6) | A / B | 0, 0, 0 / 0, 0, L | -Z / +Z |")
md.append("| Bogen 90 (Radius R, Schenkel = Muffentiefe t) | A | 0, 0, 0 | -Z |")
md.append("| Bogen 90 | B | R + t, 0, t + R | +X |")
md.append("| Bogen 45 | B | R(1 - cos 45) + t sin 45, 0, t + R sin 45 + t cos 45 | (sin 45, 0, cos 45) |")
md.append("| T-Stueck (Arm a = t + OD_f/2) | A / B / C | -a, 0, 0 / +a, 0, 0 / 0, 0, +a | -X / +X / +Z |")
md.append("| Kugelhahn (L = 50 + 2 t) | A / B | 0, 0, 0 / 0, 0, L | -Z / +Z; Hebel +X (offen = parallel zur Rohrachse) |")
md.append("| Schlauch (ID16 / ID25, Standard 1000) | A / B | 0, 0, 0 / 0, 0, L | -Z / +Z |")
md.append("| Schlauchbogen 90 (R = 5 x AD, Schenkel 100) | A / B | 0, 0, 0 / R + 100, 0, 100 + R | -Z / +X |")
md.append("| Rohrklemme (Aufnahme Rohr d) | Rohrachse | 0, 0, z = 4 + (d + 6)/2, Achse X | Rohr liegt entlang X; Fuss unten (Z = 0), 2 Schrauben M6x20 |")
md.append("| Verteiler d32 (n = 2, 3, 4 Abgaenge d25, Teilung 120) | Sammler A / B | 0, 0, 0 / L, 0, 0 (L = 120 n + 120) | -X / +X |")
md.append("| Verteiler | Abgang k | x_k = 60 + 60 + 120 (k - 1), 0, 66 | +Z |\n")
md.append("DN-Naeherung: d25 = DN20, d32 = DN25, d40 = DN32, d50 = DN40, d63 = DN50, d110 = DN100 (PVC-U-Rohr d entspricht dem Nenndurchmesser um etwa eine Stufe kleiner).\n")
md.append("## Masse und Gewichte je Groesse (PVC-U, Messung aus den .sc)\n")
md.append("| d | DN | Wand | Muffentiefe t | Formstueck-Aussen | Bogenradius R | Rohr 1 m (kg) | Kupplung | Bogen 90 | Bogen 45 | T | Kugelhahn | Klemme |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
md += rows
md.append(f"\nSchlauch (Standard 1000 mm): ID16 / AD23, hellblau, {hose[16][0]:.2f} kg, Bogen 90 R = 115 (5 x AD) {hose[16][1]:.3f} kg; ID25 / AD32, dunkelblau, {hose[25][0]:.2f} kg, Bogen 90 R = 160 {hose[25][1]:.3f} kg. Verteiler d32: n2 {vt[2]:.3f} kg, n3 {vt[3]:.3f} kg, n4 {vt[4]:.3f} kg.\n")
md.append("## Farben nach Funktion (docs/hydraulics.md 5)\n\nFrischwasser hellblau (#7fc4ea, Schlauch ID16), Filterlinie dunkelblau (#2a5da8, Schlauch ID25, Kugelhahn), Ruecklauf grau (#8d9296, PVC-Rohre/Formstuecke, Standard), Luft schwarz oder gruen. Die Montage setzt die Farbe je Leitung per `appearance.assign` auf die Instanz; die Bibliothek liefert grau (Rohre/Formstuecke) und die Standardfarbe der Schlaeuche.\n")
md.append("## Verbindungen und Befestigungen\n\n- Rohr und Formstueck: Klebemuffe nach DIN EN 1452 (Muffentiefe t aus der Tabelle, Spiel 0), PVC-U-Kleber; Kugelhahn mit Klebemuffen (Verschraubung als Variante).\n- Schlauch: Aufstecken auf Tuelle/Stutzen mit Schlauchschelle (nicht modelliert).\n- Rohrklemme: 2 Schrauben M6x20 ISO 4017 in Duebel/Holz; Abstand der Klemmen 0,5-1 m (hydraulics.md 5).\n")
md.append("## Herkunft (docs/provenance.md)\n\n| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |\n|---|---|---|---|---|")
H = [["Rohrgroessen d25/32/40/50/63/110", "d25-d110", "OBJ + Bauteilblaetter", "layout.json tanks fittings 30-56; Rinne d32, Tuelle ID16, Tankzulauf d50/d63, Beet Standrohr d25/Tropfrohr d20 (PE), Pumpe d32-d50; Scope-Card nennt DN 25/32/50/110", "mittel"],
     ["Wandstaerke PVC-U PN10 (SDR 21): max(1,8; d/21)", "1,8 - 5,2 mm", "A", "DIN 8062/EN 1452 Naeherung ohne Tabelle; keine Quelle abgerufen", "niedrig"],
     ["Muffentiefe 19/22/26/31/37,5/61", "mm", "A", "EN 1452-3 Klebemuffen (aus dem Gedaechtnis gerundet, nicht abgerufen)", "niedrig"],
     ["Formstueckwand 3 + d/40, Aussen-D = d + 2 x Wand", "mm", "A", "Praxis PVC-U-Formstuecke", "niedrig"],
     ["Bogenradius R = max(OD_f, 1,2 d)", "mm", "A", "kompakte Klebebogen; keine Quelle", "niedrig"],
     ["Kugelhahn Gehaeuse 50 mm lang, Hebel 110 x d/5", "mm", "A", "Bauform; keine Quelle", "niedrig"],
     ["Schlauch ID16/ID25, Wand 3,5; Biegeradius 5 x AD", "ID16 / ID25", "Bauteilblaetter + hydraulics.md 5", "Tuelle ID16 (Rinne), Tankzulauf/Pumpe; Biegeradius >= 5 x Schlauchdurchmesser", "mittel"],
     ["Schlauchfarben hellblau/dunkelblau", "#7fc4ea / #2a5da8", "Bild + hydraulics.md 5", "ref-6: hellblaue Schlaeuche; Farbe nach Funktion", "mittel"],
     ["Rohrklemme: Ring 3 mm, Breite 20, Fuss 4 mm, 2 x M6x20", "M6", "A", "Konstruktionspraxis (Klemmen alle 0,5-1 m laut hydraulics.md 5)", "niedrig"],
     ["Verteiler d32 mit n Abgaengen d25, Teilung 120", "n = 2-4", "A + Bauteilblatt Tisch", "analog Zulaufverteiler des NFT-Tischs; Teilung Annahme", "niedrig"],
     ["Werkstoff PVC-U 1,4 g/cm3, Schlauch 1,0", "g/cm3", "Fachwert", "Handbuchwerte", "mittel"]]
md += ["| " + " | ".join(r) + " |" for r in H]
md.append("\n## Montage (L4)\n\n1. Teile nach der Leitungsliste der Montage zuschneiden (Rohr: Saege, entgraten) und trocken ausrichten.\n2. Klebemuffen mit PVC-U-Reiniger anrauen, Kleber auftragen, bis Anschlag einschieben, 1/4 Drehung, Abbinden lassen.\n3. Schlaeuche mit Schelle auf Tuellen/Stutzen; Rohrklemmen alle 0,5-1 m.\n4. Dichtheitsprobe (Wasser), Kugelhaehne Hebelstellung pruefen.\n\n**Werkzeug:** Rohrschneider/Saege, Entgrater, Kleber, Schluessel M6, Bohrer.\n")
md.append("## Stueckliste (Mengen)\n\nBibliothek: 49 Definitionen = 6 Rohre, 6 Kupplungen, 12 Boegen (90/45), 6 T-Stuecke, 6 Kugelhaehne, 6 Klemmen je Groesse d25-d110, 4 Schlauchteile (ID16/25 gerade und Bogen), 3 Verteiler. Mengen je Anlage ergeben sich aus `data/system.json` (Montage, Graph); jede Instanz ist ein Verknuepfen der Definition (keine Einzelkoerper).\n")
md.append("## Alternative lokale Fertigung\n\nPVC-/PE-Rohre und Fittings aus dem Sanitaer-/Bewaesserungshandel; Schlaeuche als PVC-Gewebeschlauch (Gartenbedarf).\n")
md.append("## Offene Fragen\n\n- DN-Zuordnung, Wandstaerken und Muffentiefen sind Naeherungen ohne Normtabelle (keine Quelle abgerufen).\n- Weitere Teile (Reduzierung, Winkel-T, Flansch, Rueckschlagventil, Schlauchschelle) fehlen; bei Bedarf der Montage nachbauen.\n- Rohrlaengen: Standard 1000 mm; Montage setzt Laengen ueber den Parameter `laenge` (Generator `leitung.rohr(d, L)`).\n- Verlegung/Weg und `routing surface|buried`: Montage (nicht Klasse).\n")
md.append("## Renders\n\n" + "\n".join(f"- `renders/components/leitungsteile/{f}`" for f in sorted(os.listdir(os.path.join(sc.ROOT, "renders", "components", "leitungsteile"))) if f.endswith(".png")) + "\n")
md.append("## Pruefung\n\n- `scripts/workshop/check_leitungsteile.py` (Ergebnis `renders/components/leitungsteile/check.txt`): 49 Dateien, Aussen-D, Laenge, Volumen = Ringflaeche x Mittellinie (Pappus, Rohr/Bogen/Schlauchbogen), Baulaengen, Biegeradius, Verteiler-Abgaenge.\n- Kein Bild-Kritiker: Normteile ohne Referenzbild; Spec-Pruefer und Orchestrator-Stichprobe.\n")
open(os.path.join(sc.ROOT, "docs", "parts", "leitungsteile.md"), "w", encoding="utf-8").write("\n".join(md))
json.dump(P, open(os.path.join(sc.ROOT, "data", "components", "leitungsteile.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("leitungsteile.md geschrieben")
