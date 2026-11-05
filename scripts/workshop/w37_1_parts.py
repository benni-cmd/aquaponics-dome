"""W37-1: Teiledaten data/parts/<komp>.json fuer beet_sumpf und schlammfass (Format wie data/parts/schwimmerventil_pool.json, Pruefung check_parts.py).
Masse je Teil aus `solidcraft-cli eval` (bbox, Masse); Texte von Hand. Kein artikel_id: Kaufteile sind nicht im Katalog (data/katalog.json gehoert N-STUECKLISTE),
daher `ausnahme` mit Grund und `bezug` offen (D76).
Aufruf: python -X utf8 scripts/workshop/w37_1_parts.py [beet_sumpf] [schlammfass]"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

AUSN = "Kaufteil/Handelsteil nicht im Katalog (data/katalog.json, N-STUECKLISTE); Artikel offen (D76, N-BESCHAFFUNG)"
HINWEIS = "Texte und Masse aus dem Bauteilblatt und den Parametern des Bauteils. Pumpe, Schwimmer und Deckel sind Platzhalter; Fabrikate und europaeischer Bezug der Kaufteile sind offen (Regel D76)."

def T(id_, name, koerper, typ, werk, funktion, eig, norm, lm, konf, quelle, bezug="offen (D76)", lm_konf="angenommen", norm_konf="angenommen", expl=None):
    t = dict(id=id_, name=name, koerper=koerper, menge=len(koerper), typ=typ, werkstoff=werk, funktion=funktion, eigenschaften=eig, norm=norm,
             norm_konfidenz=norm_konf, lebensmittelkontakt=lm, lebensmittelkontakt_konfidenz=lm_konf, konfidenz=konf, quelle=quelle, ausnahme=AUSN)
    if typ in ("kaufteil", "normteil"):
        t["bezug"] = bezug
    if expl:
        t["explosion"] = {"richtung": expl[0], "abstand_mm": expl[1]}
    return t

Q_S = "docs/parts/beet_sumpf.md, data/components/beet_sumpf.json, docs/research/R45-hydraulik-auslegung.md Abschnitt 3"
Q_F = "docs/parts/schlammfass.md, data/components/schlammfass.json, docs/research/R45-hydraulik-auslegung.md Abschnitt 0"
PVCN = "DIN 8062 / EN 1452 (PVC-U-Rohre) [A]"

def spec_sumpf(names):
    steig = sorted(n for n in names if n.startswith("Steigrohr_") or n == "Sammelrohr")
    pumpen = sorted(n for n in names if n.startswith("Pumpe_"))
    rsv = sorted(n for n in names if n.startswith("Rueckschlagventil_"))
    teile = [
        T("tank", "PE-Rundtank 500 l", ["Tank"], "kaufteil", "pe", "Der Tank nimmt das Ablaufwasser der Beete einer Linie auf (Puffer fuer zwei gleichzeitig leerende Beete).", ["Aussen 800 x 1000 mm, Wand 6 mm [A].", "Domoeffnung oben 580 mm.", "Bis ALARM 620 mm etwa 300 l, bis Oberkante 482 l (Modell)."], "EN 12566-1 / Zisternen-Handelsware [A]", "ja", "angenommen", Q_S + "; Handelsmass nicht gegengeprueft", expl=([0, 0, -1], 300)),
        T("schachtaufsatz", "Schachtaufsatz", ["Schachtaufsatz"], "kaufteil", "pe", "Der Aufsatz hebt den Deckel bis zum Flur, weil der Tank tiefer sitzt als der Beetablauf.", ["Aussen 600 mm, Hoehe 200 mm (Parameter aufsatz_h).", "Hoehe folgt der Einbautiefe (Aktualitaetspruefung 05.11.)."], "Herstellerangabe Domschacht [A]", "nein", "angenommen", Q_S, expl=([0, 0, 1], 150)),
        T("deckel", "Begehbarer Deckel", ["Deckel"], "kaufteil", "pe", "Der Deckel schliesst den Sumpf dicht und lichtdicht ab und traegt die Durchfuehrungen.", ["Oe 700 x 40 mm, vier Durchbrueche.", "Lichtdicht gegen Algen (R45)."], "Deckelklasse offen (R45 Frage 3 Nr. 4) [A]", "nein", "angenommen", Q_S, expl=([0, 0, 1], 300)),
        T("zulauf", "Tankverbinder d50 (Zulauf)", ["Zulauf_Tankverbinder"], "kaufteil", "pvc_u", "Der Tankverbinder fuehrt die Sammelleitung der Beetablaeufe (K14/K30) durch die Tankwand.", ["Muffe d50, Sohle 800 mm ueber Tankboden.", "Dichtung nicht modelliert."], PVCN, "ja", "angenommen", Q_S, expl=([-1, 0, 0], 150)),
        T("pumpe", "Teichpumpe 5300 l/h (Platzhalter)", pumpen, "kaufteil", "pumpengehaeuse", "Die Pumpen foerdern das Wasser ueber die Foerderleitung d40 zum Ruecklauf; die zweite ist Reserve (E19).", ["Platzhalter-Quader 300 x 200 x 180 mm.", "60 W, Hmax 2,8 m (Haendlerangabe R45), Kennlinie offen."], "Fabrikat offen [A]", "ja", "angenommen", Q_S + "; Pumpenfabrikat offen (R45 Frage 3 Nr. 1)", expl=([0, 0, 1], 900)),
        T("rueckschlagventil", "Rueckschlagventil d40", rsv, "kaufteil", "pvc_u", "Das Ventil haelt die Foerderleitung gefuellt und verhindert Rueckfluss in die stehende Pumpe.", ["Masse wie lt_rueckschlagventil_d40 (W39): Laenge 102, Gehaeuse 60."], PVCN, "ja", "angenommen", Q_S + ", docs/parts/leitungsteile.md (W39)", expl=([0, 0, 1], 700)),
        T("foerderleitung", "Steig- und Sammelrohr d40", steig, "rohr", "pvc_u", "Die Rohre fuehren das Wasser von den Pumpen zur Deckeldurchfuehrung.", ["PVC-U d40, Wand 1,9 mm.", "Zwei Steigrohre werden unter dem Deckel zusammengefuehrt."], PVCN, "ja", "angenommen", Q_S, expl=([0, 0, 1], 600)),
        T("durchfuehrung_foerder", "Deckeldurchfuehrung d40", ["Durchfuehrung_Foerder"], "kaufteil", "pvc_u", "Die Durchfuehrung fuehrt die Foerderleitung K58/K59 durch den Deckel (Port).", ["Muffe d40 oben."], PVCN, "ja", "angenommen", Q_S, expl=([0, 0, 1], 400)),
        T("schwimmerstange", "Schwimmerstange", ["Schwimmerstange"], "sonderteil", "pvc_u", "Die Stange traegt die drei Schwimmerschalter auf den Schaltpegeln.", ["Oe 20 mm, vom Boden bis unter den Deckel."], "keine [A]", "ja", "angenommen", Q_S, expl=([-1, 0, 0], 500)),
        T("schwimmer", "Schwimmerschalter AUS, EIN, ALARM", ["Schwimmer_AUS", "Schwimmer_EIN", "Schwimmer_ALARM"], "kaufteil", "pa", "Die Schwimmer schalten die Pumpe (EIN 320, AUS 120 mm) und sperren bei ALARM 620 mm die Beet-Zufuhr.", ["Platzhalter Oe 70 x 60 mm.", "Kabel nicht modelliert."], "Fabrikat offen [A]", "ja", "angenommen", Q_S, expl=([-1, 0, 0], 600)),
        T("entlueftung", "Entlueftung d32", ["Entlueftung"], "kaufteil", "pvc_u", "Die Entlueftung laesst die Verdraengungsluft aus dem Sumpf entweichen.", ["Rohr d32 durch den Deckel, 100 mm hoch."], PVCN, "nein", "angenommen", Q_S, expl=([0, 0, 1], 350)),
        T("insektengitter", "Insektengitter-Kappe", ["Insektengitter_Kappe"], "kaufteil", "pa", "Die Kappe mit Gitter haelt Insekten aus der Entlueftung fern.", ["Oe 60 x 20 mm, Gitter als Vollkoerper vereinfacht."], "keine [A]", "nein", "angenommen", Q_S, expl=([0, 0, 1], 450)),
        T("kabelverschraubung", "Kabelverschraubung M25", ["Kabelverschraubung_1", "Kabelverschraubung_2"], "kaufteil", "pa", "Die Verschraubungen fuehren die Kabel von Pumpen, Schwimmern und Ablaufwaechter (A+) dicht durch den Deckel.", ["M25, Aussen 33 mm, Klemmbereich 16 mm [A]."], "EN 62444 (Kabelverschraubungen) [A]", "nein", "angenommen", Q_S, expl=([0, 0, 1], 350)),
    ]
    gruppen = [
        {"id": "behaelter", "name": "Behaelter", "kurz": "Tank, Schachtaufsatz und Deckel.", "teile": ["tank", "schachtaufsatz", "deckel"]},
        {"id": "zulauf", "name": "Zulauf", "kurz": "Tankverbinder der Beetablaeufe.", "teile": ["zulauf"]},
        {"id": "pumpen", "name": "Pumpen und Foerderleitung", "kurz": "Zwei Pumpen mit Rueckschlagventil auf eine Foerderleitung d40.", "teile": ["pumpe", "rueckschlagventil", "foerderleitung", "durchfuehrung_foerder"]},
        {"id": "steuerung", "name": "Schwimmer, Lueftung, Kabel", "kurz": "Schaltpegel, Entlueftung und Kabeldurchfuehrungen.", "teile": ["schwimmerstange", "schwimmer", "entlueftung", "insektengitter", "kabelverschraubung"]},
    ]
    kopf = dict(bauteilgruppe="Becken und Tanks", titel="Beet-Sumpf (Ablauf der Beete, je Linie)", kurz="Der eingegrabene Tank sammelt das Ablaufwasser der Beete; Pumpen mit Rueckschlagventil foerdern es zurueck, drei Schwimmer schalten und sperren bei Hochwasser die Beet-Zufuhr.")
    return kopf, gruppen, teile

def spec_fass(names):
    teile = [
        T("fass", "Spannringfass PE 220 l", ["Fass"], "kaufteil", "pe", "Das Fass nimmt den abgelassenen Schlamm der Absetzer-Spuelung auf; der Schlamm setzt sich ab.", ["Aussen 580 x 865 mm ohne Deckel, Wand 4, Boden 5 [A].", "Innenraum 221 l (Modell)."], "Handelsware Spannringfass [A]", "ja", "angenommen", Q_F + "; Handelsmass nicht gegengeprueft", expl=([0, 0, -1], 300)),
        T("deckel", "Fassdeckel mit Durchbruechen", ["Deckel"], "kaufteil", "pe", "Der Deckel deckt das Fass ab und traegt Einlaufstutzen, Luftbohrung und Entlueftung.", ["Oe 580 x 15 mm.", "Durchbrueche 48 (Stutzen), 8 (Luftschlauch), 26 (Entlueftung)."], "Handelsware [A]", "nein", "angenommen", Q_F, expl=([0, 0, 1], 200)),
        T("spannring", "Spannring", ["Spannring"], "kaufteil", "stahl_verzinkt", "Der Spannring haelt den Deckel dicht auf dem Fass.", ["Stahl verzinkt, 10 x 35 mm [A]."], "Handelsware [A]", "nein", "angenommen", Q_F, expl=([0, 0, 1], 120)),
        T("einlaufstutzen", "Einlaufstutzen d40", ["Einlaufstutzen"], "kaufteil", "pvc_u", "Der Stutzen nimmt das Fallrohr der Schlammleitung K07/K23 auf (Port).", ["Muffe d40 in der Deckelmitte."], PVCN, "ja", "angenommen", Q_F, expl=([0, 0, 1], 300)),
        T("entlueftung", "Entlueftungsstutzen Oe 20", ["Entlueftungsstutzen"], "kaufteil", "pvc_u", "Der Stutzen laesst Luft aus dem Fass, wenn Schlammwasser einlaeuft.", ["Bohrung Oe 20, 20 mm hoch."], PVCN, "nein", "angenommen", Q_F, expl=([0, 0, 1], 250)),
    ]
    gruppen = [{"id": "fass", "name": "Fass", "kurz": "Fass, Deckel und Spannring.", "teile": ["fass", "deckel", "spannring"]},
               {"id": "anschluesse", "name": "Anschluesse", "kurz": "Einlaufstutzen d40 und Entlueftung.", "teile": ["einlaufstutzen", "entlueftung"]}]
    kopf = dict(bauteilgruppe="Becken und Tanks", titel="Schlammfass (je Linie)", kurz="Das eingegrabene Fass nimmt den Schlamm aus dem Absetzer auf; einmal pro Woche wird Klarwasser abgehoben und der Dickschlamm zum Wurmkompost gebracht.")
    return kopf, gruppen, teile

SPECS = {"beet_sumpf": spec_sumpf, "schlammfass": spec_fass}

def write(komp):
    path = os.path.join(sc.ROOT, "designs", "components", komp + ".sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    kopf, gruppen, teile = SPECS[komp](list(B))
    for t in teile:
        m = sum(B[k]["mass_g"] for k in t["koerper"])
        b = B[t["koerper"][0]]["bbox"]
        e = [b["max"][i] - b["min"][i] for i in range(3)]
        t["masse_mm"] = f"Masse {m:.1f} g, Einzelkoerper {e[0]:.1f} x {e[1]:.1f} x {e[2]:.1f} mm (Modell-Bounding-Box)"
    order = ("id", "name", "koerper", "menge", "typ", "werkstoff", "masse_mm", "funktion", "eigenschaften", "norm", "norm_konfidenz", "lebensmittelkontakt",
             "lebensmittelkontakt_konfidenz", "konfidenz", "quelle", "bezug", "explosion", "ausnahme")
    teile = [{k: t[k] for k in order if k in t} for t in teile]
    d = dict(komponente=komp, datei=f"designs/components/{komp}.sc", bauteilgruppe=kopf["bauteilgruppe"], teilenummer="", stand="teiledaten", titel=kopf["titel"],
             kurz=kopf["kurz"], hinweis=HINWEIS, koerperzahl=len(B), gruppen=gruppen, teile=teile)
    out = os.path.join(sc.ROOT, "data", "parts", komp + ".json")
    json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(out, len(teile), "Teile,", len(B), "Koerper")

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(SPECS)):
        write(k)
