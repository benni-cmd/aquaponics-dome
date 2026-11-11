"""Teiledaten data/parts/<komp>.json fuer die Werkstatt-Teile tiefer Ventilschacht (schacht_tief.py) und Ring B2 (ringleitung.py).
Masse und Abmessungen aus `solidcraft-cli eval`; Texte, Normen und Bezug als angenommen [A] (keine Datenblaetter gelesen).
artikel_id nur, wenn der Artikel in data/katalog.json UND data/stueckliste.json steht; sonst `ausnahme` (Stueckliste/Katalog baut N-STUECKLISTE).
Aufruf: python -X utf8 scripts/workshop/parts_ringleitung.py"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import sc

KAT = json.load(open(os.path.join(sc.ROOT, "data", "katalog.json"), encoding="utf-8"))
ART = {a["id"] for a in KAT.get("artikel", [])} & {z["artikel_id"] for z in json.load(open(os.path.join(sc.ROOT, "data", "stueckliste.json"), encoding="utf-8"))["zeilen"]}
WERK = {m: w["id"] for w in KAT["werkstoffe"] for m in w.get("sc_material", [])}
HINWEIS = "Werkstatt 05.11.2026 (M10-S2N Vorbedingung, N-VARIANTEN V2): Masse aus dem Modell; Texte, Normverweise und Bezug aus Fachwissen, alle angenommen [A]."
AUSNAHME = "Artikel noch nicht in data/katalog.json und data/stueckliste.json; Aufnahme durch N-STUECKLISTE (Werkstatt darf diese Dateien nicht schreiben)"
BEZUG_EU = "offen (D76: Handelsteil, in der EU bestellbar angenommen [A]; Haendler nicht abgerufen)"

def T(id, name, koerper, typ, funktion, eig, norm, lm="nein", art=None, expl=None, bezug=None):
    return dict(id=id, name=name, koerper=koerper, typ=typ, funktion=funktion, eigenschaften=eig, norm=norm, lm=lm, art=art, expl=expl, bezug=bezug)

SCHACHT_TEILE = lambda seals: [T("schachtwanne", "Schachtwanne", ["Schachtwanne"], "sonderteil", "Die Wanne umschliesst den Kugelhahn d63 im Erdreich; von oben wird der Hahn bedient.", ["PE-HD, Wand 8, Boden 15 [A].", "Durchfuehrungen fuer die Rohre mit Dichtung."], "EN ISO 17855-1 (PE-Formmassen) [A]")] + \
    [T("dichtung_" + s.split("_")[1].lower(), "Dichtung " + s.split("_")[1], [s], "kaufteil", "Die Ringraumdichtung dichtet die Rohrdurchfuehrung gegen Erdreich und Sickerwasser.", ["EPDM-Manschette [A]."], "Herstellerangabe [A]", expl={"richtung": [0, 0, -1] if s.endswith("Boden") else ([-1, 0, 0] if s.endswith("A") else [1, 0, 0]), "abstand_mm": 80}, bezug=BEZUG_EU) for s in seals] + \
    [T("deckel", "Schachtdeckel", ["Deckel"], "sonderteil", "Der Deckel schliesst den Schacht buendig mit dem Innenboden und wird zum Bedienen abgehoben.", ["PE-HD 30 mm, zwei Griffmulden, nicht befahrbar [A]."], "EN ISO 17855-1 (PE-Formmassen) [A]", expl={"richtung": [0, 0, 1], "abstand_mm": 250})]

KOMP = {
    "lt_schacht_kugelhahn_d63_tief_senkrecht": dict(titel="Tiefer Ventilschacht (senkrechter Hahn)", gruppe="Leitungen", tn="T70-SCH-KH63-TS",
        kurz="Schacht um den senkrechten Bypass-Kugelhahn KH1/KH2, Hahnmitte 486 mm unter dem Innenboden; Heberleitung d75 laeuft oben quer durch, das Rohr d63 unten durch den Boden.",
        teile=SCHACHT_TEILE(["Dichtung_Boden", "Dichtung_A", "Dichtung_B"])),
    "lt_schacht_kugelhahn_d63_tief_waagerecht": dict(titel="Ventilschacht Stamm-Hahn (waagerecht)", gruppe="Leitungen", tn="T70-SCH-KH63-TW",
        kurz="Schacht um einen waagerechten Kugelhahn d63 im Filter-Stamm, Rohrachse 186 mm unter dem Innenboden.",
        teile=SCHACHT_TEILE(["Dichtung_A", "Dichtung_B"])),
    "pegelschacht": dict(titel="Pegelschacht Ring B2", gruppe="Leitungen", tn="T94",
        kurz="Kleines Fass zwischen Biofilter-Ueberlauf und den zwei Boostern des Rings; entkoppelt Zulauf und Pumpen, Schwimmer schalten die Booster, Notueberlauf fuehrt Ueberschuss in den Ruecklauf.",
        teile=[T("fass", "Fass 60 l", ["Fass"], "kaufteil", "Das Fass sammelt das Wasser aus dem Biofilter-Ueberlauf, aus dem die Booster saugen.", ["Weithalsfass PE-HD, 60 l Nenninhalt, aussen 400 x 520 [A].", "Lebensmitteltaugliches PE angenommen."], "EN ISO 17855-1 (PE-Formmassen) [A]", lm="ja", bezug=BEZUG_EU),
               T("deckel", "Fassdeckel", ["Deckel"], "kaufteil", "Der Deckel haelt Licht und Schmutz fern und traegt Zulauf, Schwimmerstange, Kabel und Entlueftung.", ["PE-HD 15 mm, Bohrungen vor Ort [A]."], "EN ISO 17855-1 [A]", lm="ja", expl={"richtung": [0, 0, 1], "abstand_mm": 200}, bezug=BEZUG_EU),
               T("zulaufstutzen", "Zulaufstutzen d50", ["Zulaufstutzen"], "sonderteil", "Der Stutzen fuehrt K10/K26 vom Biofilter frei fallend ins Fass (kein Rueckstau).", ["PVC-U d50 mit Klebemuffe und Kragen [A]."], "EN 1452 (PVC-U Druckrohre) [A]", lm="ja", expl={"richtung": [0, 0, 1], "abstand_mm": 300}),
               T("saugstutzen", "Tankdurchfuehrung Saug d50", ["Saugstutzen_A", "Saugstutzen_B"], "kaufteil", "Je ein Saugstutzen versorgt einen Booster (pumpe_gross) geflutet von unten.", ["Tankdurchfuehrung PVC d50 mit Flansch und Mutter [A]."], "Herstellerangabe [A]", lm="ja", expl={"richtung": "radial", "abstand_mm": 120}, bezug=BEZUG_EU),
               T("notueberlauf", "Tankdurchfuehrung Notueberlauf d63", ["Notueberlauf"], "kaufteil", "Der Notueberlauf fuehrt den ganzen Zulauf in den Ruecklauf, wenn die Booster stehen.", ["Tankdurchfuehrung PVC d63; d63 statt d50, weil d50 bei 2 % Gefaelle nur rund 75 l/min traegt [E]."], "Herstellerangabe [A]", lm="ja", expl={"richtung": [-1, 0, 0], "abstand_mm": 120}, bezug=BEZUG_EU),
               T("schwimmerstange", "Schwimmerstange", ["Schwimmerstange"], "kaufteil", "Die Stange fuehrt die zwei Schwimmerschalter senkrecht.", ["PVC Rundstab d16 [A]."], "Herstellerangabe [A]", lm="ja", bezug=BEZUG_EU),
               T("schwimmer", "Schwimmerschalter AUS/EIN", ["Schwimmer_AUS", "Schwimmer_EIN"], "kaufteil", "AUS schuetzt die Booster vor Trockenlauf, EIN gibt sie wieder frei.", ["Ring-Schwimmerschalter PP, Reedkontakt 24 V [A].", "AUS bei 250 mm, EIN bei 340 mm ueber Fassboden."], "EN 60730-1 (Regel- und Steuergeraete) [A]", lm="ja", bezug=BEZUG_EU),
               T("kabelverschraubung", "Kabelverschraubung M20", ["Kabelverschraubung"], "normteil", "Fuehrt das Schwimmerkabel dicht durch den Deckel.", ["PA, M20, IP68 [A]."], "EN 62444 (Kabelverschraubungen) [A]", bezug=BEZUG_EU)]),
    "ringstuetze_d75": dict(titel="Ringstuetze d75", gruppe="Leitungen", tn="T95",
        kurz="Bodenstuetze fuer den Druck-Halbring d75 unter dem Dach: Pfosten mit Kragarm, das Rohr haengt in einer Schelle; unter dem Rohr bleibt der Gang frei.",
        teile=[T("fussplatte", "Fussplatte", ["Fussplatte"], "sonderteil", "Die Platte verteilt die Last auf den Innenboden und nimmt vier Anker auf.", ["Stahl verzinkt 200 x 200 x 10, 4 Bohrungen 12 [A]."], "EN 10025-2 (S235) [A]"),
               T("anker", "Anker M10", ["Anker_1", "Anker_2", "Anker_3", "Anker_4"], "normteil", "Die Anker halten die Stuetze im Boden gegen Kippen.", ["Gewindeanker M10 x 110 mit Mutter, verzinkt [A]."], "ISO 4032 (Mutter), Anker Herstellerangabe [A]", expl={"richtung": [0, 0, -1], "abstand_mm": 150}, bezug=BEZUG_EU),
               T("pfosten", "Pfosten", ["Pfosten"], "profil", "Der Pfosten traegt Kragarm und Rohr bis auf Ringhoehe.", ["Quadratrohr 50 x 50 x 3, verzinkt [A].", "Biegespannung unter 5 MPa (Check)."], "EN 10219 (Hohlprofile) [A]"),
               T("kragarm", "Kragarm", ["Kragarm"], "profil", "Der Arm kragt ueber den Gang aus und haelt den Haenger ueber dem Rohr.", ["Quadratrohr 40 x 40 x 3, an den Pfosten geschweisst [A]."], "EN 10219 [A]"),
               T("gewindestange", "Haenger M10", ["Gewindestange"], "normteil", "Die Gewindestange haengt die Schelle an den Arm; die Hoehe ist ueber die Muttern einstellbar.", ["Gewindestange M10 mit 2 Muttern, verzinkt [A]."], "DIN 976-1 [A]", bezug=BEZUG_EU),
               T("rohrschelle", "Rohrschelle d75", ["Rohrschelle"], "kaufteil", "Die Schelle umfasst das Rohr d75 von oben.", ["Stahl verzinkt mit Anschweissmutter M10 [A]."], "Herstellerangabe [A]", expl={"richtung": [0, 1, 0], "abstand_mm": 120}, bezug=BEZUG_EU),
               T("einlage", "Schelleneinlage EPDM", ["Schelleneinlage"], "kaufteil", "Die Einlage daempft und schuetzt das PVC-Rohr gegen die Stahlschelle.", ["EPDM 3 mm [A]."], "Herstellerangabe [A]", expl={"richtung": [0, -1, 0], "abstand_mm": 120}, bezug=BEZUG_EU)]),
    "entluefter_d75": dict(titel="Entluefter d75", gruppe="Leitungen", tn="T96",
        kurz="Automatische Entlueftung am Hochpunkt jedes Halbrings: T d75 mit Abgang d25, Uebergangsnippel und Schwimmer-Schnellentlueftungsventil 1 Zoll.",
        teile=[T("t_stueck", "T d75 mit Abgang d25", ["Entlueftungs_T"], "kaufteil", "Das T sitzt im Ring am Hochpunkt; Luft sammelt sich im Abgang.", ["PVC-U, Klebemuffen d75, reduzierter Abgang d25 [A]."], "EN 1452-3 (Formstuecke) [A]", lm="ja", bezug=BEZUG_EU),
               T("nippel", "Uebergangsnippel d25 auf 1 Zoll", ["Uebergangsnippel"], "kaufteil", "Verbindet die Klebemuffe d25 mit dem Gewinde des Ventils.", ["PVC-U, Zapfen d25, Aussengewinde 1 Zoll [A]."], "EN 1452-3 [A]", lm="ja", expl={"richtung": [0, 0, 1], "abstand_mm": 60}, bezug=BEZUG_EU),
               T("ventil", "Schnellentlueftungsventil 1 Zoll", ["Entlueftungsventil"], "kaufteil", "Der Schwimmer im Ventil laesst gesammelte Luft ab und schliesst bei Wasser.", ["Messing, Innengewinde 1 Zoll, PN10 [A]."], "EN 1074-4 (Be- und Entlueftungsventile) [A]", lm="ja", expl={"richtung": [0, 0, 1], "abstand_mm": 120}, bezug=BEZUG_EU)]),
}

def abzweig_teile(dk):
    return [T("t_stueck", "T d75", ["T_d75"], "kaufteil", "Das T sitzt im Halbring; sein Abgang zeigt nach unten zum Abnehmer.", ["Bibliotheksteil lt_t_d75, PVC-U [A]."], "EN 1452-3 [A]", lm="ja", bezug=BEZUG_EU),
            T("rohrstuecke", "Rohrstuecke", ["Rohrstueck_d75", "Rohrstueck_d50", f"Rohrstueck_d{dk}"], "rohr", "Kurze Rohrstuecke verbinden Muffe mit Muffe (je zwei Muffentiefen plus 10 mm).", ["PVC-U SDR 21 [A]."], "EN 1452-2 [A]", lm="ja", expl={"richtung": [1, 0, 0], "abstand_mm": 120}),
            T("reduzierung_75_50", "Reduziermuffe d75/d50", ["Reduzierung_75_50"], "kaufteil", "Reduziert vom Ring d75 auf d50.", ["Bibliotheksteil lt_reduzierung_d75_d50 [A]."], "EN 1452-3 [A]", lm="ja", art="ARM-reduzierung-d75-d50", bezug=BEZUG_EU),
            T(f"reduzierung_50_{dk}", f"Reduziermuffe d50/d{dk}", [f"Reduzierung_50_{dk}"], "kaufteil", f"Reduziert auf den Abnehmer-Durchmesser d{dk}.", [f"Bibliotheksteil lt_reduzierung_d50_d{dk} [A]."], "EN 1452-3 [A]", lm="ja", art=f"ARM-reduzierung-d50-d{dk}", bezug=BEZUG_EU),
            T("kugelhahn", f"Kugelhahn d{dk} (Regler)", [f"Kugelhahn_d{dk}", f"Kugelhahn_d{dk}_Spindel", f"Kugelhahn_d{dk}_Hebel"], "kaufteil", "Der Hahn stellt den Strom je Abnehmer ein und sperrt ihn bei Wartung.", [f"Bibliotheksteil lt_kugelhahn_d{dk}, PVC-U [A]."], "EN ISO 16135 [A]", lm="ja", art=f"ARM-kugelhahn-d{dk}", expl={"richtung": [0, 0, -1], "abstand_mm": 150}, bezug=BEZUG_EU)]

for _dk in (40, 32):
    KOMP[f"ring_abzweig_d{_dk}"] = dict(titel=f"Ring-Abzweig d75 auf d{_dk}", gruppe="Leitungen", tn=f"T97-{_dk}",
        kurz=f"Abzweig vom Halbring d75 zu einem {'Beet' if _dk == 40 else 'Tisch'}: T, zwei Reduziermuffen, Rohrstuecke und Kugelhahn d{_dk} als Regler; nur Bibliotheksteile.", teile=abzweig_teile(_dk))

def masse(b):
    bb = b["bbox"]; dims = sorted((bb["max"][i] - bb["min"][i] for i in range(3)), reverse=True)
    return f"Masse {b['mass_g']:.1f} g, Einzelkoerper {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm (Modell-Bounding-Box)"

def build(komp, spec):
    path = os.path.join("designs", "components", komp + ".sc")
    ev = sc.evaluate(os.path.join(sc.ROOT, path)); bb = {b["name"]: b for b in ev["bodies"]}
    teile, gruppen = [], {}
    for t in spec["teile"]:
        b0 = bb[t["koerper"][0]]
        werk = WERK.get(b0["material"], "unbestimmt_modell")
        row = {"id": t["id"], "name": t["name"], "koerper": t["koerper"], "menge": len(t["koerper"]), "typ": t["typ"], "werkstoff": werk, "masse_mm": masse(b0)}
        if t["art"] and t["art"] in ART:
            row.update(artikel_id=t["art"], artikel_einheit="Stk", artikel_menge_je_instanz=float(len(t["koerper"]) if t["id"] != "kugelhahn" else 1))
        else:
            row["ausnahme"] = AUSNAHME
        row.update(funktion=t["funktion"], eigenschaften=t["eigenschaften"], norm=t["norm"], norm_konfidenz="angenommen", lebensmittelkontakt=t["lm"], lebensmittelkontakt_konfidenz="angenommen",
                   konfidenz="angenommen", quelle=f"Modell {path} (Masse aus solidcraft-cli eval); Texte und Norm aus Fachwissen [A]")
        if t["bezug"]:
            row["bezug"] = t["bezug"]
        if t["expl"]:
            row["explosion"] = t["expl"]
        teile.append(row)
        g = {"sonderteil": "sonderteile", "profil": "profile", "rohr": "rohre", "normteil": "normteile"}.get(t["typ"], "kaufteile")
        gruppen.setdefault(g, []).append(t["id"])
    GN = {"sonderteile": ("Sonderteile (Eigenbau)", "Teile, die selbst gebaut oder angepasst werden."), "kaufteile": ("Kaufteile", "Teile, die man fertig bestellt."),
          "profile": ("Profile", "Stahlprofile, auf Laenge geschnitten."), "rohre": ("Rohre", "Rohr, auf Laenge geschnitten."), "normteile": ("Normteile", "Schrauben, Muttern, Verschraubungen.")}
    d = {"komponente": komp, "datei": path.replace("\\", "/"), "bauteilgruppe": spec["gruppe"], "teilenummer": spec["tn"], "stand": "5a", "titel": spec["titel"],
         "kurz": f"Baugruppe aus {len(ev['bodies'])} Koerpern. " + spec["kurz"], "hinweis": HINWEIS, "koerperzahl": len(ev["bodies"]),
         "gruppen": [{"id": k, "name": GN[k][0], "kurz": GN[k][1], "teile": v} for k, v in gruppen.items()], "teile": teile}
    out = os.path.join(sc.ROOT, "data", "parts", komp + ".json")
    open(out, "w", encoding="utf-8").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    print("geschrieben", out, len(ev["bodies"]), "Koerper")

if __name__ == "__main__":
    for k in (sys.argv[1:] or KOMP):
        build(k, KOMP[k])
