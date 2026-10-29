"""Blatt netztopf nach Spec-Pruefer W07 (29.10., FAIL -> behoben): Herkunft OBJ-Box/Achszuordnung, Pruefzeile 18/18, erledigte offene Fragen raus, Kind-Prosa raus, Werkstoffmarke. Idempotent; vor partsheet.py ausfuehren."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "netztopf.json")
d = json.load(open(p, encoding="utf-8"))
d["werkstoff"]["herkunft"] = "[A] Standardwerkstoff Netztopf (PP, Spritzguss); Farbe schwarz wie ref-6 (dunkle Toepfe unter dem Kopf nicht sichtbar) [A]"
bl = d["blatt"]
bl["abweichung"] = "OBJ-Box 50 x 64 x 63 (layout.json pots.size_mm, in extract_layout.py festgeschrieben; reference/oasis-obj-analysis.md nennt 0,05 x 0,06 x 0,06 m, Achszuordnung Hoehe/Kragen daher offen): Modell Korpus 50, Kragen 64, Hoehe 63; Innenprofil und Schlitze sind Annahmen."
bl["stueckliste"] = [x.split("; Ob Rinnen UND")[0] + " (Besatz Rinnen und Beete laut decisions D17)" for x in bl["stueckliste"]]
bl["pruefung"] = ["scripts/workshop/check_pflanze.py (18/18 PASS, davon 9 Netztopf): Masse 50 x 64 x 63 (liest die Konstante aus layout.json, kein unabhaengiger OBJ-Beleg), Kragen D64, Bezugspunkt Z=0, 8 Schlitze, Material PP, Masse 14-20 g, Spiel im Rinnen-Topfloch D52 = 2 mm",
                  "Schnitt `renders/components/netztopf/netztopf-02-schnitt.png` zeigt Wand, Kragen, Schlitze und Bodenloch; Sitz im Topfloch: `renders/components/nft_rinne/nft_rinne-06-schnitt-zulauf.png`",
                  "Kein Bild-Kritiker: der Netztopf ist in keiner Referenz sichtbar (vom Salat bzw. der Erde verdeckt); Spec-Pruefer: Runde 1 FAIL -> behoben, Runde 2 (29.10. W07) FAIL (Herkunft/Altlasten) -> behoben, siehe workshop-log"]
bl["kritiker"] = "Kein Bild-Kritiker (Netztopf in keiner Referenz sichtbar); Spec-Pruefer Runde 1 und 2, siehe workshop-log"
bl["offen"] = ["Farbe schwarz oder weiss (nicht sichtbar in ref-6)",
               "Topfhoehe 63 laut OBJ-Box; Standardware ist oft 50 mm; Achszuordnung der OBJ-Box (Hoehe 60-64 laut oasis-obj-analysis) offen",
               "Beet-Raster 288 je Beet (24 x 12) gegen layout.json distinct_along 64 / distinct_across 39: Integrator",
               "Topfboden und Naehrloesungsfilm in der Rinne (Topf ragt ca. 59,5 mm unter die Deckelflaeche, Schlitze 8-46 mm ueber dem Boden): Rinne/Tisch pruefen"]
for r in d["herkunft_tabelle"]:
    if r[0] in ("Hoehe 63 mm", "Korpus-D oben 50 mm"):
        r[2], r[4] = "OBJ-Box + E", "mittel"
        r[3] = "layout.json pots.size_mm (50, 64, 63; Konstante in extract_layout.py); Zuordnung zu Hoehe/Korpus/Kragen ist Auslegung E, oasis-obj-analysis nennt 0,05 x 0,06 x 0,06 m"
    if r[0] == "Anzahl 2160":
        r[2], r[3] = "OBJ", "layout.json pots.total (7 Beete x 288 + 144); Topfzahl der Rinnen kommt aus dem Tisch; Besatz D17"
    if r[0] == "Kragen D64 x 3,5 mm":
        r[3] = "OBJ-Box 64 = Kragen (groesste Breite, Auslegung E); Kragendicke Annahme A"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("netztopf.json gepflegt")
