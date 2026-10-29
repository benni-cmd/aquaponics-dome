"""Blatt nft_tisch nach Spec-Pruefer W16 Runde 2 (29.10. ~18:45): Duplikate der Herkunftstabelle (fix_tisch_blatt3 lief zweimal) entfernen, wirkungslose Parameter streichen,
yaw-Angabe auf volle 360 Grad praezisieren, Herkunftsmarken (nur OBJ/Bild/R/Ben/E/A) und fehlende Herkunftszeilen, Revision B. Idempotent; danach partsheet.py nft_tisch."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "nft_tisch.json")
d = json.load(open(p, encoding="utf-8"))
bl, P = d["blatt"], d["parameter"]
d["revision"] = "B"

def sub(s, old, new):
    return s.replace(old, new) if old in s else s

# 1 Duplikate (erste Fassung je Merkmal behalten) und ueberholte Zeilen
seen, rows = set(), []
for r in d["herkunft_tabelle"]:
    if r[0].startswith("Holmueberstand 30 mm"):
        continue
    if r[0] in seen:
        continue
    seen.add(r[0]); rows.append(r)
# 2 Marken
for r in rows:
    if r[2] == "Scope-Card + A":
        r[2] = "A"; r[3] = "docs/scope-cards.md nft_tisch (4 Beine mit Querstreben, Diagonalen); innen 2 Pfosten wegen Pool (D18)"
    if r[2] == "A + Normteil":
        r[2] = "A"
    if r[2] == "A + Bild" or r[2] == "Bild + A":
        pass
def has(key):
    return any(r[0].startswith(key) for r in rows)
extra = [
    ("corner_gap 100 mm", ["corner_gap 100 mm je Seite der Sektorgrenze", "100 mm (Abstand zwischen zwei Tischen 190 mm)", "A", "Vorgabe des Orchestrators, docs/decisions.md D18 (Auftrag W16); Abstand = 2 x 100 x cos 18 Grad", "mittel"]),
    ("leg_clearance 60 mm", ["leg_clearance 60 mm zwischen Beet-Aussenbreite und Fussplattenkante", "60 mm", "A", "Vorgabe des Orchestrators, docs/decisions.md D18; Beet-Aussenbreite aus ibc_beet.json", "mittel"]),
    ("Beckenrand Z 650", ["Beckenrand Z 650: Kragarm liegt 130 mm darueber (Unterkante 780)", "Z 650", "Ben", "data/params.json pool_rim (Ben: Rand ca. Z 650, am Bild ref-4 zu pruefen); Kragarm-Unterkante = Rinnenhoehe 840 - holm_h", "mittel"]),
    ("Durchgangsloch D9", ["Durchgangsloch D9 in der Fussplatte fuer M8", "D9", "E", "ISO 273 mittel fuer M8 (9 mm)", "hoch"]),
    ("Kragarm-Ueberstand 30 mm", ["Kragarm-Ueberstand 30 mm ueber die innerste Rinne (nur innen)", "30 mm", "A", "Konstruktionspraxis; Portalholm endet buendig an der Beinaussenseite (kein Ueberstand)", "niedrig"]),
    ("Tisch-KS und Platzierung", ["Tisch-KS und Platzierung: X tangential CCW, Y radial nach innen, yaw = Azimut + 90 Grad (volle 360 Grad)", "yaw az + 90", "E", "Y = Z x X bei dieser Drehung; layout.json hydro_tables speichert yaw nur modulo 180 (aussen Sektor 3, 6-9 und Mitte/innen 7-9 haben dort az - 90): wer den OBJ-Wert woertlich nimmt, setzt den Tisch um 180 Grad gedreht", "hoch"]),
]
for key, r in extra:
    if not has(key):
        rows.append(r)
d["herkunft_tabelle"] = rows
# 3 Parameter: wirkungslose streichen, Herkunft praezisieren
P.pop("leg_inset", None)
P["holm_overhang"]["herkunft"] = "[A] Kragarm (nur innen) ragt 30 mm ueber die innerste Rinne hinaus; der Portalholm endet buendig an der Beinaussenseite"
P["corner_gap"]["herkunft"] = "[A] Vorgabe Orchestrator, docs/decisions.md D18: Abstand von der Zehneck-Ecke (Sektorgrenze) zum Rinnen-/Verteilerende je Seite; Abstand zwischen zwei Tischen 2 x corner_gap x cos 18 Grad = 190 mm"
P["leg_clearance"]["herkunft"] = "[A] Vorgabe Orchestrator, docs/decisions.md D18: Luft zwischen Beet-Aussenbreite (ibc_beet.json) und Fussplattenkante"
# 4 Duplikate in Textfeldern
marker = " Rev. B (W16/D18): jede Reihe"
f = bl["funktion"]
if f.count(marker) > 1:
    i = f.index(marker, f.index(marker) + 1)
    bl["funktion"] = f[:i]
P["strut_z"]["herkunft"] = P["strut_z"]["herkunft"].split("; innen Laengsstrebe")[0] + "; innen Laengsstrebe auf Z 400 (Ausleger ausserhalb des Beckenrands)"
# 5 yaw-Angabe
old1 = "(= yaw der OBJ-Tische in layout.json hydro_tables)"
new1 = "(volle 360 Grad; layout.json hydro_tables speichert yaw nur modulo 180: aussen Sektoren 3 und 6-9 sowie Mitte/innen 7-9 haben dort az - 90, den Tisch dann um 180 Grad gedreht setzen)"
bl["abweichung"] = sub(bl["abweichung"], old1, new1)
bl["offen"] = [sub(x, "yaw = Azimut + 90 Grad wie OBJ, Y radial INNEN", "yaw = Azimut + 90 Grad in vollen 360 Grad, OBJ-yaw nur modulo 180; Y radial INNEN") for x in bl["offen"]]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("nft_tisch.json bereinigt:", len(rows), "Herkunftszeilen")
