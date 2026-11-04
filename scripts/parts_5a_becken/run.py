"""W60 Schritt 5a, Gruppe "Becken, Tanks, Filter, Pumpen, Puffer": fuellt die Handfelder in data/parts/<komp>.json
(Funktion, Erklaertext, Explosion, Gruppen, Norm, Lebensmittelkontakt, Konfidenz, Quelle, bezug) und ergaenzt data/katalog.json um fehlende Werkstoffe.

Aufruf:  python -X utf8 scripts/parts_5a_becken/run.py            # schreibt
         python -X utf8 scripts/parts_5a_becken/run.py --trocken  # nur Bericht
Regeln: Auto-Felder des Geruests (id, koerper, menge, typ, masse_mm, artikel_id ...) bleiben; Teile bekommen den Marker `geruest` nicht mehr.
Erneuter Lauf ueberschreibt die Handfelder dieser Gruppe mit den Texten aus texte_*.py (Texte sind die Quelle der Wahrheit dieser Gruppe)."""
import json
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import texte_tank as TT  # noqa: E402
import texte_puffer as TP  # noqa: E402
import texte_becken as TB  # noqa: E402

PARTS = os.path.join(ROOT, "data", "parts")
KATALOG = os.path.join(ROOT, "data", "katalog.json")
TROCKEN = "--trocken" in sys.argv

# Werkstoffe, die fuer diese Gruppe im Katalog fehlen (id, name, norm, dichte, lebensmittelkontakt, sc_material, quelle)
NEU = [
    ("hdpe", "Polyethylen hoher Dichte (HDPE)", "EN ISO 17855-1 (PE-Formmassen) [A]", 0.95, "ja", ["HDPE Palette", "HDPE blau", "Kanister HDPE", "PE Blase", "SV Kugel"],
     "Handbuchwert HDPE 0,95 g/cm3; IBC-Blase, Palette, Kanister und Fass sind HDPE"),
    ("messing", "Messing (CW617N, trinkwassergeeignet)", "EN 12165 (Schmiedemessing) [A]", 8.4, "ja", ["AK Messing"], "Handbuchwert 8,4 g/cm3; Probehahn und Durchflussbegrenzer der Aktivkohle-Station"),
    ("gfk_komposit", "Komposit (GFK mit PE-Liner), Druckbehälter", "Herstellerangabe, Fabrikat offen [A]", 1.9, "ja", ["AK Komposit"], "Modelldichte; Handelsbehälter 10 x 35 Zoll, Fabrikat offen"),
    ("aktivkohle", "Katalytische Aktivkohle (Schüttgut)", "Herstellerangabe, Fabrikat offen [A]", 0.5, "ja", ["AK Kohle"], "Schüttdichte der Kohle im Behälter, Handbuchwert 0,5 g/cm3"),
    ("biomedium", "Biomedium (Schwebebett-Träger aus Kunststoff)", "Herstellerangabe, Fabrikat offen [A]", 0.15, "ja", ["Biomedium"], "docs/parts/tank.md (Schüttung 470 l x 0,15 g/cm3)"),
    ("holz_fichte", "Fichtenholz (Kantholz)", "EN 338 (Festigkeitsklassen Bauholz) [A]", 0.45, "nein", ["Holz Fichte"], "Handbuchwert Fichte 0,45 g/cm3"),
    ("beton", "Beton", "EN 206 (Beton) [A]", 2.4, "ja", ["Beton"], "Handbuchwert 2,4 g/cm3; Werkstoff des kleinen Drittbeckens laut Modell fraglich"),
    ("wasser", "Wasser (Füllung, kein Bauteil)", "-", 1.0, "ja", ["Wasser"], "Darstellungsvolumen der Füllung; nicht kaufbar"),
    ("kabel_pvc", "Kabel (Kupfer mit PVC-Mantel)", "VDE 0281 / H05VV-F [A]", 1.2, "nein", ["Kabel schwarz"], "Mittlere Modelldichte 1,2 g/cm3; Pumpenkabel 3 x 1,5 mm2"),
    ("pumpengehaeuse", "Kunststoffgehäuse von Pumpen", "Herstellerangabe, Fabrikat offen [A]", 1.5, "nein", ["Pumpe blau", "Pumpe Schlauch"], "docs/parts/pumpe.md (Pumpe Kunststoffgehäuse 1,5 g/cm3); Hüllform"),
]
# vorhandene Werkstoffe, die zusaetzliche .sc-Materialnamen bekommen
ERWEITERN = {
    "pp": ["AK PP", "Becher PP", "PP Tafel", "PP schwarz", "SV PP", "AK Kopf"],
    "pvc_u": ["AK PVC", "AK Hahn", "PVC grau", "PVC blau", "PVC grau Pumpe", "Stutzen PVC", "SV PVC", "Kanal PVC"],
    "stahl_verzinkt": ["Blech", "Stahl Pumpe", "AK Konsole"],
    "sonde_gehaeuse": ["Sonde"],
}


ENTFERNEN = ("acryl", "messsonde", "modell_default")  # eigene Doppler von pmma, sonde_gehaeuse, unbestimmt_modell (andere Gruppe, gleichzeitig angelegt)


def katalog_ergaenzen():
    k = json.load(open(KATALOG, encoding="utf-8"), object_pairs_hook=OrderedDict)
    k["werkstoffe"] = [w for w in k["werkstoffe"] if w["id"] not in ENTFERNEN]
    vorh = {w["id"]: w for w in k["werkstoffe"]}
    neu_n = erw_n = 0
    for wid, mats in ERWEITERN.items():
        for m in mats:
            if m not in vorh[wid]["sc_material"]:
                vorh[wid]["sc_material"].append(m)
                erw_n += 1
    for wid, name, norm, dichte, lm, mats, quelle in NEU:
        if wid in vorh:
            for m in mats:
                if m not in vorh[wid]["sc_material"]:
                    vorh[wid]["sc_material"].append(m)
            continue
        e = OrderedDict([("id", wid), ("name", name), ("norm", norm), ("dichte_g_cm3", dichte), ("lebensmittelkontakt", lm), ("konfidenz", "angenommen"),
                         ("sc_material", list(mats)), ("pilot", False), ("quelle", quelle), ("marke", "[A]")])
        k["werkstoffe"].append(e)
        vorh[wid] = e
        neu_n += 1
    if not TROCKEN:
        with open(KATALOG, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(k, ensure_ascii=False, indent=2) + "\n")
    print(f"Katalog: {neu_n} neue Werkstoffe, {erw_n} neue sc_material-Namen")
    return {m: w["id"] for w in k["werkstoffe"] for m in w.get("sc_material", [])}, {w["id"]: w for w in k["werkstoffe"]}


def folgt_id(pid, folgt, ids):
    if not folgt:
        return None
    if folgt in ids and folgt != pid:
        return folgt
    m = re.search(r"_([a-z]{1,2})$", pid)
    if m and "_" in folgt:
        cand = folgt.rsplit("_", 1)[0] + "_" + m.group(1)
        if cand in ids and cand != pid:
            return cand
    return None


def anwenden(comp, titel, kurz, hinweis, eintraege, gruppen, quelle, sc_zu_werk, werk, ibc_gruppe=None):
    pfad = os.path.join(PARTS, comp + ".json")
    d = json.load(open(pfad, encoding="utf-8"), object_pairs_hook=OrderedDict)
    ids = [t["id"] for t in d["teile"]]
    id_set = set(ids)
    fehlt = []
    gruppe_von = {}
    for t in d["teile"]:
        tr = None
        for ent in eintraege:
            if re.fullmatch(ent[0], t["id"]):
                tr = ent
                break
        if tr is None:
            fehlt.append(t["id"])
            continue
        pat, name, funk, eig, expl, grp, extra = tr
        mats = {b for b in [t["werkstoff"]] for b in b.split(" / ")}
        m0 = sorted(mats)[0]
        m0 = {"modell_default": "Default", "messsonde": "Sonde", "acryl": "Acryl klar"}.get(m0, m0)  # erneuter Lauf: schon umgesetzte Werkstoff-IDs zulassen
        wid = sc_zu_werk.get(m0) or (m0 if m0 in werk else None)
        if wid is None:
            fehlt.append(t["id"] + " (Werkstoff " + t["werkstoff"] + ")")
            continue
        w = werk[wid]
        # Reihenfolge der Felder wie im Pilot
        neu = OrderedDict()
        for k, v in t.items():
            if k in ("geruest", "werkstoff", "artikel_id", "artikel_einheit", "artikel_menge_je_instanz", "ausnahme", "name"):
                continue
            neu[k] = v
        out = OrderedDict()
        out["id"] = t["id"]
        out["name"] = name
        out["koerper"] = t["koerper"]
        out["menge"] = t["menge"]
        out["typ"] = t["typ"]
        out["werkstoff"] = wid
        out["masse_mm"] = t["masse_mm"]
        out["funktion"] = funk
        out["eigenschaften"] = list(eig)
        out["norm"] = w["norm"] if w["norm"] != "-" else "keine (kein Bauteil)"
        out["norm_konfidenz"] = "angenommen"
        lm = extra.get("lm", w["lebensmittelkontakt"])
        out["lebensmittelkontakt"] = lm
        out["lebensmittelkontakt_konfidenz"] = "angenommen"
        out["konfidenz"] = "angenommen"
        out["quelle"] = quelle
        if extra.get("katalog"):
            out["katalog"] = extra["katalog"]
        if t["typ"] in ("normteil", "kaufteil"):
            out["bezug"] = "offen (R52)"
        if expl:
            r, a, f = expl
            ex = OrderedDict([("richtung", r), ("abstand_mm", a)])
            ff = folgt_id(t["id"], f, id_set)
            if ff:
                ex["folgt"] = ff
            out["explosion"] = ex
        if t.get("artikel_id") is not None:
            out["artikel_id"] = t["artikel_id"]
        if t.get("artikel_ids"):
            out["artikel_ids"] = t["artikel_ids"]
        for k in ("artikel_einheit", "artikel_menge_je_instanz", "ausnahme"):
            if k in t:
                out[k] = t[k]
        t.clear()
        t.update(out)
        gruppe_von[t["id"]] = grp
    if fehlt:
        sys.exit(f"{comp}: ohne Text: {fehlt}")
    gl = []
    for gid, gname, gkurz, _ in gruppen:
        ts = [i for i in ids if gruppe_von.get(i) == gid]
        if ts:
            gl.append(OrderedDict([("id", gid), ("name", gname), ("kurz", gkurz), ("teile", ts)]))
    rest = [i for i in ids if not any(i in g["teile"] for g in gl)]
    if rest:
        sys.exit(f"{comp}: Teile ohne Gruppe: {rest}")
    d["gruppen"] = gl
    d["titel"] = titel
    d["kurz"] = kurz
    d["hinweis"] = hinweis
    d["stand"] = "teiledaten"
    if not TROCKEN:
        with open(pfad, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    print(f"{comp}: {len(ids)} Teile gefuellt, {len(gl)} Gruppen")
    return len(ids)


def main():
    sc_zu_werk, werk = katalog_ergaenzen()
    HW = ("Texte und Maße aus dem Bauteilblatt und den Parametern des Bauteils. Rohr-, Wand- und Fabrikatangaben sind angenommen; "
          "der europäische Bezug der Kaufteile ist offen (Regel D76, Recherche R52).")
    ibc_gr = [(g[0], g[1], g[2], None) for g in TP.IBC_GRUPPEN]
    summe = 0
    # Tanks
    for comp in ("tank_gross", "tank_gross_t3"):
        extra = " Variante mit gedrehtem Rippenmuster (Tank 3)." if comp.endswith("t3") else ""
        summe += anwenden(comp, "Biofilter-Tank mit Schwebebett (großer Tank)" + (", Tank 3" if extra else ""),
                          "Das Wasser tritt tangential in den Kegeltank ein; lose Träger im belüfteten Wasser tragen die Bakterien, die Ammonium abbauen. Das Wasser verlässt den Tank oben über den Überlauf, Schlamm wird unten abgelassen." + extra,
                          HW, TT.TANK, TT.TANK_GRUPPEN, TT.QUELLE_TANK, sc_zu_werk, werk)
    for comp, ti in (("pumpe_gross", "Pumpenmodul groß (Hauptkreislauf)"), ("pumpe_klein", "Pumpenmodul klein (Teilstrom des Absetzers)")):
        summe += anwenden(comp, ti, "Eine Kreiselpumpe auf einer Montagetafel: Wasser tritt axial in den Saugstutzen ein und verlässt die Pumpe nach oben durch den Druckstutzen.",
                          HW, TT.PUMPE, TT.PUMPE_GRUPPEN, TT.QUELLE_PUMPE, sc_zu_werk, werk)
    # Puffer
    summe += anwenden("puffer_ibc", "Puffertank (IBC 1000 Liter)",
                      "Der Container nimmt rund 900 Liter Wasser auf; Zulauf und Überlauf liegen oben, der Ablauf mit Kugelhahn unten.", HW, TP.IBC, TP.IBC_GRUPPEN, TP.QUELLE_IBC, sc_zu_werk, werk)
    st_gr = []
    for gid, gname, gkurz, _ in TP.STATION_GRUPPEN:
        st_gr.append((gid, gname, gkurz, None))
    st_ent = []
    for pat, name, funk, eig, expl, grp, ex in TP.IBC:
        st_ent.append((pat, name, funk, eig, expl, "ibc", ex))
    st_ent = TP.STATION + st_ent
    summe += anwenden("puffer_station", "Puffer-Station (zwei IBC, Messplatz, Dosierung)",
                      "Zwei IBC stehen übereinander: oben Zulauf und Messung, unten der Vorrat. Ein Messplatz misst pH, Leitwert, Temperatur und Sauerstoff; zwei Schlauchpumpen dosieren Nährstoffe und pH-Puffer.",
                      HW, st_ent, st_gr, TP.QUELLE_STATION, sc_zu_werk, werk)
    summe += anwenden("puffer_klein", "Kleiner Puffer (Fass, Messzelle, Dosierung)",
                      "Ein Fass für die Stammlösung, eine Messzelle mit vier Sondenstutzen und zwei Schlauchpumpen auf einem Gestell mit Regalboden.", HW, TP.KLEIN, TP.KLEIN_GRUPPEN, TP.QUELLE_KLEIN, sc_zu_werk, werk)
    summe += anwenden("aktivkohle_station", "Aktivkohle-Station (Entchlorung des Frischwassers)",
                      "Das Frischwasser läuft über einen Absperrhahn, einen Sedimentvorfilter und zwei Kohlebehälter in Reihe. Ein Probehahn zeigt den Durchbruch, ein Durchflussbegrenzer hält 4 Liter je Minute.",
                      HW, TP.AK, TP.AK_GRUPPEN, TP.QUELLE_AK, sc_zu_werk, werk)
    # Becken
    summe += anwenden("schwimmerventil_pool", "Schwimmerventil des Pools", "Hält den Wasserspiegel im Pool: sinkt er, öffnet die Schwimmerkugel das Ventil und Frischwasser läuft nach.",
                      HW, TB.SV, TB.SV_GRUPPEN, TB.QUELLE_SV, sc_zu_werk, werk)
    summe += anwenden("becken_dritt_klein", "Drittbecken klein (Quarantäne- und Notbecken)", "Eine in den Boden eingelassene Wanne mit 0,4 m³ Wasser für kranke Tiere oder Zuchttiere.",
                      HW, TB.DK, TB.DK_GRUPPEN, TB.QUELLE_DK, sc_zu_werk, werk)
    summe += anwenden("becken_dritt", "Drittbecken", "Quarantäne- und Notbecken im Boden. Das Modell ist eine Hüllform aus dem Layout; Werkstoff und Bauart sind offen.",
                      HW, TB.BECKEN_DRITT, TB.BECKEN_GRUPPEN, TB.QUELLE_BECKEN, sc_zu_werk, werk)
    summe += anwenden("pool_zentral", "Zentralpool", "Das Hauptbecken der Anlage mit zwei Seitenabläufen und einem Bodenablauf. Das Modell ist eine Hüllform aus dem Layout; Werkstoff und Bauart sind offen.",
                      HW, TB.POOL, TB.POOL_GRUPPEN, TB.QUELLE_BECKEN, sc_zu_werk, werk)
    summe += anwenden("zweitbecken", "Zweitbecken", "Zweites Fischbecken im Boden. Das Modell ist eine Hüllform aus dem Layout; Werkstoff und Bauart sind offen.",
                      HW, TB.ZWEIT, TB.ZWEIT_GRUPPEN, TB.QUELLE_BECKEN, sc_zu_werk, werk)
    summe += anwenden("zulaufrohr", "Zulaufrohr zum Pool", "Ein langes Rohr d160 führt Wasser zum Zentralpool. Das Modell ist eine Hüllform aus dem Layout.",
                      HW, TB.ZULAUF, TB.ZULAUF_GRUPPEN, TB.QUELLE_BECKEN, sc_zu_werk, werk)
    print("Teile gefuellt gesamt:", summe)


if __name__ == "__main__":
    main()
