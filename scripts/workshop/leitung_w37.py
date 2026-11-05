"""Leitungsteile W37 (Bibliothek T70, Gruppe W37): Kugelhahn d40 mit Federrueckzug (Schlammablass der Absetzer K07/K23, R45 Abschnitt 0 Gefahr).
Bauweise wie leitung.kugelhahn (gleiche Helfer, Muffen, Gehaeuse); Zusatz: Federgehaeuse auf der Spindel, Hebel in Ruhelage GESCHLOSSEN (quer zur Rohrachse):
offen nur, solange die Hand den Hebel haelt, die Feder schliesst. Fabrikat und Verfuegbarkeit im Standardmass NICHT geprueft [A] (R45 Offene Punkte Frage 0 Nr. 3).
leitung.py und leitung_w39.py bleiben unveraendert; ports() hier liefert die W37-Ports und fragt sonst leitung_w39.ports().
Aufruf: python -X utf8 scripts/workshop/leitung_w37.py [--json] [--render]"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w39 as W39

FILES = ["lt_kugelhahn_feder_d40"]   # check_leitungsteile.py zaehlt sie nicht zu den 63 Bibliotheksteilen
FED = dict(d=36.0, l=22.0, spindel_l=5.0, hebel_dicke=14.0, hebel_l=110.0)   # Federgehaeuse Oe 36 x 22, Hebel 110 lang [A]

def geom(d=40):
    of = L.od_f(d); ob = of + 12; Lb = 50.0
    return dict(of=of, ob=ob, Lb=Lb, L=Lb + 2 * L.DEPTH[d], zc=L.DEPTH[d] + Lb / 2, dp=L.DEPTH[d])

def kugelhahn_feder(d=40):
    g = geom(d); of, ob, Lb, dp, zc = g["of"], g["ob"], g["Lb"], g["dp"], g["zc"]
    b = sc.Build(); nm = f"T70_Kugelhahn_Feder_d{d}"
    L.setup(b, nm, d, {"laenge": round(g["L"], 1)})
    b.add("solid.cylinder", diameter=ob, height=Lb, base=[0, 0, dp], operation="new", name="Gehaeuse_R", body_name="Kugelhahn")
    for z0, nmn in ((0, "A"), (dp + Lb, "B")):
        b.add("solid.cylinder", diameter=of, height=dp, base=[0, 0, z0], operation="join", targets=["Kugelhahn"], name="Stutzen_" + nmn)
    b.add("solid.cylinder", diameter=d, height=dp + 1, base=[0, 0, -1], operation="cut", targets=["Kugelhahn"], name="Muffe_A")
    b.add("solid.cylinder", diameter=d, height=dp + 1, base=[0, 0, g["L"] - dp], operation="cut", targets=["Kugelhahn"], name="Muffe_B")
    b.add("solid.cylinder", diameter=d - 2 * L.wall_p(d), height=g["L"] + 2, base=[0, 0, -1], operation="cut", targets=["Kugelhahn"], name="Durchgang")
    b.add("material.assign", bodies=["Kugelhahn"], material="LT hahn")
    b.add("component.activate", component=nm)
    b.add("component.create", name="T70a_Federrueckzug")
    x0 = ob / 2                                                    # Gehaeuse-Mantel (Tangentialebene), Federgehaeuse setzt dort an
    b.add("solid.cylinder", diameter=FED["d"], height=FED["l"], base=[x0, 0, zc], axis=[1, 0, 0], operation="new", name="Feder_R", body_name="Federgehaeuse")
    x1 = x0 + FED["l"]
    b.add("solid.cylinder", diameter=14, height=FED["spindel_l"], base=[x1, 0, zc], axis=[1, 0, 0], operation="new", name="Spindel_R", body_name="Spindel")
    x2 = x1 + FED["spindel_l"]
    # Hebel in Ruhelage GESCHLOSSEN: quer zur Rohrachse (+Y), Totmann-Griff
    b.add("solid.box", length=FED["hebel_dicke"], width=FED["hebel_l"], height=max(8, d / 5), center=[x2 + FED["hebel_dicke"] / 2, FED["hebel_l"] / 2 - 10, zc], operation="new", name="Hebel_R", body_name="Hebel")
    b.add("material.assign", bodies=["Federgehaeuse", "Spindel", "Hebel"], material="LT hahn")
    L.meta(b, nm, f"T70-KHF-{d}", f"Kugelhahn PVC-U d{d} mit Federrueckzug (Totmann): Hebel quer = geschlossen (Ruhelage), offen nur bei Handkraft; Klebemuffen A/B")
    return b, nm, g

def ports(fname):
    if fname == "lt_kugelhahn_feder_d40":
        return [("A", (0, 0, 0), (0, 0, -1), "Muffe", L.DN[40]), ("B", (0, 0, geom(40)["L"]), (0, 0, 1), "Muffe", L.DN[40])]
    return W39.ports(fname)

def json_entry():
    g = geom(40)
    return {"lt_kugelhahn_feder_d40": dict(teilenummer="T70-KHF-40", komponente="T70_Kugelhahn_Feder_d40", werkstoff="PVC-U (Klebemuffen), Feder Edelstahl (nicht modelliert)", d=40, laenge=g["L"],
        gehaeuse_aussen_d=g["ob"], gehaeuse_laenge=g["Lb"], muffentiefe=g["dp"], federgehaeuse={"d": FED["d"], "laenge": FED["l"]}, hebel={"laenge": FED["hebel_l"], "ruhelage": "geschlossen, quer zur Rohrachse (+Y)"},
        funktion="Schlammablass Absetzer K07/K23: offen nur bei Handkraft, Feder schliesst (Schutz gegen leeren Pool, R45 Abschnitt 0: 12,5 l/min Zulauf, offener d40-Hahn leert den Absetzer in 2 min)",
        verwendung="Absetzer-Kegelspitze Linie 1 und 2 (K07, K23), je 1", herkunft={"Bauweise": "E wie lt_kugelhahn_d40 (leitung.kugelhahn)", "Federgehaeuse 36 x 22, Hebel 110": "Annahme",
        "handelsteil": "Kugelhahn mit Federrueckzug d40: Fabrikat und Verfuegbarkeit im Standardmass nicht geprueft [A] (R45 Frage 0 Nr. 3)"},
        ports=[{"name": n, "lage": list(W39.pr(p)), "richtung": list(W39.pr(dr)), "art": a, "dn": dn} for n, p, dr, a, dn in ports("lt_kugelhahn_feder_d40")])}

DESC = {"match": "^lt_kugelhahn_feder_d", "titel": "Kugelhahn d40 mit Federrückzug",
    "was": "Absperrhahn am Schlammablass der Absetzer: Er ist nur offen, solange die Hand den Hebel hält; lässt man los, schließt die Feder. Schützt den Pool vor dem Leerlaufen.",
    "status": "gebaut (Werkstatt W37-1); Bauform wie der Kugelhahn d40, Fabrikat nicht geprüft",
    "ablauf": ["Hebel gegen die Feder in Rohrrichtung drehen: der Hahn öffnet, 20 bis 40 l Schlammwasser laufen ins Schlammfass.", "Hebel loslassen: die Feder dreht ihn quer zur Rohrachse, der Hahn ist zu."],
    "aufbau": [{"t": "Maße", "p": [f"Länge {geom(40)['L']:g}, Gehäuse Ø {geom(40)['ob']:g}", "Federgehäuse Ø 36 × 22, Hebel 110 (Ruhelage quer = zu)"]}],
    "masse": {"Länge": f"{geom(40)['L']:g} mm"}, "grenzen": "Fabrikat und Verfügbarkeit im Standardmaß nicht geprüft; Feder und Kugel nicht modelliert.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W37), docs/research/R45-hydraulik-auslegung.md Abschnitt 0"}

def write_json():
    p = os.path.join(sc.ROOT, "data", "components", "leitungsteile.json")
    d = json.load(open(p, encoding="utf-8"))
    d.setdefault("w37_teile", {}).update(json_entry())
    open(p, "w", encoding="utf-8", newline="").write(json.dumps(d, indent=1, ensure_ascii=False).replace("\n", "\r\n"))

def write_descriptions():
    """Vor ^lt_kugelhahn... gibt es keinen eigenen Eintrag; der Sammeleintrag ^lt_ (Index 27) wuerde den Hahn fangen: einfuegen vor ^lt_reduzierung_d40_d20$ (erster lt_-Eintrag)."""
    p = os.path.join(sc.ROOT, "data", "descriptions.json")
    txt = open(p, "rb").read().decode("utf-8")
    anchor = '    {\r\n      "match": "^lt_reduzierung_d40_d20$",'
    assert txt.count(anchor) == 1
    if '"match": ' + json.dumps(DESC["match"], ensure_ascii=False) + "," not in txt:
        body = json.dumps(DESC, indent=2, ensure_ascii=False).replace("\n", "\n    ").replace("\n", "\r\n")
        txt = txt.replace(anchor, "    " + body + ",\r\n" + anchor)
    json.loads(txt)
    open(p, "wb").write(txt.encode("utf-8"))

if __name__ == "__main__":
    if "--json" in sys.argv:
        write_json(); write_descriptions(); print("json + descriptions: lt_kugelhahn_feder_d40"); sys.exit(0)
    if "--render" in sys.argv:
        print(W39.render("lt_kugelhahn_feder_d40", yaw=0.9, pitch=0.45, zoom=1.8)); sys.exit(0)
    res = kugelhahn_feder(40)
    L.save(res[0], res[1], "lt_kugelhahn_feder_d40")
    print("lt_kugelhahn_feder_d40", res[2])
