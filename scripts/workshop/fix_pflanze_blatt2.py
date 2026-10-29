"""Nachbesserung Blaetter netztopf/salatkopf nach Spec-Pruefer (29.10.): Anzahl 2160 + 556, Scope-Card-Luecke, Widersprueche im Salatkopf-JSON, Herkunftszeilen. Nach fix_pflanze_blatt.py ausfuehren."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))
# ---------------- Netztopf
p, d = load("netztopf")
bl = d["blatt"]
d["anzahl"] = {"soll": "Beete 2160 (OBJ) + Rinnen 556 (E) = 2716", "quelle": "data/layout.json pots.total (7 x 288 + 144) und docs/parts/nft_rinne.md (20 Rinnen x 5 + 24 x 7 + 24 x 12 Loecher)"}
bl["stueckliste"] = ["T10 Netztopf 50/64 x 63, PP schwarz: Beete 2160 (OBJ: 7 Aussenbeete x 288 + 144 im Beet bei Azimut 113) + Rinnen 556 (20 Rinnen K x 5 Loecher + 24 Rinnen M x 7 + 24 Rinnen L x 12; Auslegung E) = 2716 gesamt; Ob Rinnen UND Beete bepflanzt werden (Tische stehen ueber den Beeten, decisions D04), entscheidet der Orchestrator/Integrator"]
bl["pruefung"] = ["scripts/workshop/check_pflanze.py (14/14 PASS): Masse 50 x 64 x 63 (OBJ), Kragen D64, Bezugspunkt Z=0, 8 Schlitze, Material PP", "Schnitt `renders/components/netztopf/netztopf-02-schnitt.png` zeigt Wand, Kragen, Schlitze und Bodenloch; Sitz im Topfloch: `renders/components/nft_rinne/nft_rinne-06-schnitt-zulauf.png`", "Kein Bild-Kritiker: der Netztopf ist in keiner Referenz sichtbar (vom Salat bzw. der Erde verdeckt); Spec-Pruefer (Runde 1: FAIL -> behoben)"]
bl["offen"] = bl.get("offen", []) + ["Scope-Card netztopf/salatkopf ist nur eine Zeile (ohne Format nach review-protocol 1): Orchestrator ergaenzen (Anzahl je Eltern, Referenz, Pruefzahlen)", "Anzahl gesamt 2716 gegen Board 'Salatkopf ca. 240+': Orchestrator klaeren", "Beet-Raster 288 je Beet (24 x 12) gegen layout.json distinct_along 64 / distinct_across 39: Integrator"]
rows = d["herkunft_tabelle"]
rows += [["Schlitze 3 x 38 mm, 8 Stueck, ab 8 mm ueber dem Boden", "3 x 38 mm, 8 St.", "A", "Netztoepfe haben Schlitze fuer den Wurzeldurchtritt; Mass geschaetzt", "niedrig"],
         ["Bodenloch D10", "D10", "A", "Standard-Netztopf; OBJ hat nur eine Box", "niedrig"],
         ["Konischer Korpus 34 -> 50 mm, Innenwand parallel", "D34 / D50", "A", "Standard-Netztopf konisch; Aussen-D oben 50 = OBJ", "niedrig"],
         ["Gesamtzahl 2716 = 2160 (Beete) + 556 (Rinnen)", "2716", "OBJ + E", "layout.json pots.total + Rinnen-Blatt (Loecher 5/7/12 je Rinne)", "mittel"]]
for r in rows:
    if r[1] in ("-", "mm", "63", "50", "64", "1,5", "2160"):
        pass
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------- Salatkopf
p, d = load("salatkopf")
d["beschreibung"] = "Salatkopf als buschige Blattrosette aus 36 einzelnen, geneigten Blattscheiben (7 Gruppen, deterministischer Zufallsversatz) um einen Kuppelkoerper, Groessen S/M/L ueber head_d"
d["quelle_masse"] = "ref-6: Kopf ca. 1,5-2 x Topfkragen (64 mm) breit, flacher Huegel (Hoehe ca. 0,5 x Breite) [A]"
d["werkstoff"]["herkunft"] = "[A] Bulk-Dichte Naeherung nur fuer die Gewichtsangabe; Frischmasse eines Kopfes real 150-250 g (Blatt: Modellmasse ist die Frischmasse-Naeherung)"
bl = d["blatt"]
bl["offen"] = [x for x in bl.get("offen", []) if "Konfigurationszeile" not in x] + ["Konfigurationen S/L wirken auf verknuepfte Instanzen im Dom: Integrator pruefen", "Instanzvariation (zufaellige Drehung um Z, S/M/L gemischt) ist Sache des Layouts/Tisches (Kritiker R3/R4 Hinweis)", "Bild-Kritiker: vier Runden, Referenz gewaehlt (Stilunterschied CAD gegen Raytracing; gekraeuselte Blaetter mit < 8 Flaechen je Koerper nicht erreichbar); Restluecken: Blattraender kreisrund, glatte Scheiben"]
rows = d["herkunft_tabelle"]
rows += [["Kuppelkoerper Radius 0,27 x head_d, Hoehe 0,20 x head_d", "0,27 / 0,20 x head_d", "A", "Kritiker R3: Kern klein halten, Blattmasse bestimmt das Bild", "niedrig"],
         ["Blattdicke 0,045 x head_d (4,5 mm bei M)", "0,045 x head_d", "A", "Scheibenblatt; Mindestdicke fuer stabile Geometrie", "niedrig"],
         ["7 Blattgruppen (Saum haengt -14 Grad, Herz 56-64 Grad)", "36 Blaetter", "A + Bild", "ref-6: Randblaetter haengen nach unten (Kritiker R3), Herzblaetter aufrecht", "niedrig"],
         ["Zufallsversatz je Blatt (Azimut +-8 Grad, Radius +-14 %, Neigung +-4,5 Grad, Hoehe, Abstand)", "Seed sin(i*12,9898)", "A", "Kritiker R3/R4: unregelmaessige Silhouette; deterministisch fuer reproduzierbare .sc", "niedrig"]]
for r in rows:
    if r[1] in ("-", "mm"):
        pass
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("netztopf/salatkopf (2) gepflegt")
