"""W60 5a, Gruppe "Tische, Rinnen, Beete, Toepfe": fuellt die Handfelder in data/parts/<komp>.json fuer 28 Komponenten
(nft_tisch_innen/mitte/aussen, 4 ibc_beet_*, nft_rinne + 16 Reihenvarianten, netztopf, salatkopf, winkelhalter, pflanztisch)
und ergaenzt data/katalog.json um die fehlenden Werkstoffe (Blaehton, Salat) und .sc-Materialnamen.
Auto-Felder des Geruests (id, koerper, menge, typ, artikel_id ...) bleiben; die Texte dieses Skripts sind die Wahrheit dieser Gruppe.
Aufruf: python -X utf8 scripts/workshop/fill_parts_tische.py          (idempotent; --trocken schreibt nichts)
Quellen: docs/parts/nft_tisch.md, nft_rinne.md, ibc_beet.md, netztopf.md, salatkopf.md, winkelhalter.md, data/components/*.json, data/stueckliste.json (Bezug)."""
import json, os, re, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PD = os.path.join(ROOT, "data", "parts")
KAT = os.path.join(ROOT, "data", "katalog.json")
STL = os.path.join(ROOT, "data", "stueckliste.json")
TROCKEN = "--trocken" in sys.argv

# ---------------------------------------------------------------- Katalog
NEU = [("blaehton", "Blähton (Substrat, Schüttgut 8–16 mm)", "Herstellerangabe, gewaschen, Körnung 8–16 mm [A]", 0.9, "ja", ["Medium Blaehton"],
        "Schüttdichte 0,9 g/cm3 laut docs/parts/ibc_beet.md [A]; im Modell ein Volumenkörper (Medium)"),
       ("salat", "Kopfsalat (Pflanze, kein Bauteil)", "-", 0.4, "ja", ["Salat"], "docs/parts/salatkopf.md: Bulk-Dichte 0,4 g/cm3 nur Näherung für die Gewichtsangabe; nicht kaufbar")]
ERWEITERN = {"pp": ["PP", "PP grau"], "pvc_u": ["PVC-U weiss", "PVC grau Beet"], "hdpe": ["HDPE weiss"], "pvc_p_schlauch": ["Schlauch hellblau"], "edelstahl_1_4301": ["V2A Lochblech"]}


def katalog():
    k = json.load(open(KAT, encoding="utf-8"), object_pairs_hook=OrderedDict)
    vorh = {w["id"]: w for w in k["werkstoffe"]}
    n_neu = n_erw = 0
    for wid, mats in ERWEITERN.items():
        for m in mats:
            if m not in vorh[wid]["sc_material"]:
                vorh[wid]["sc_material"].append(m)
                n_erw += 1
    for wid, name, norm, dichte, lm, mats, quelle in NEU:
        if wid in vorh:
            continue
        k["werkstoffe"].append(OrderedDict([("id", wid), ("name", name), ("norm", norm), ("dichte_g_cm3", dichte), ("lebensmittelkontakt", lm), ("konfidenz", "angenommen"),
                                            ("sc_material", list(mats)), ("pilot", False), ("quelle", quelle), ("marke", "[A]")]))
        n_neu += 1
    if not TROCKEN and (n_neu or n_erw):
        with open(KAT, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(k, ensure_ascii=False, indent=2) + "\n")
    print(f"Katalog: {n_neu} neue Werkstoffe, {n_erw} neue sc_material-Namen")
    return {m: w["id"] for w in k["werkstoffe"] for m in w.get("sc_material", [])}


# ---------------------------------------------------------------- Bezug aus der Stueckliste
def bezug_text(zeile):
    if zeile is None:
        return "offen (N-BESCHAFFUNG)"
    p = zeile.get("preis")
    if not p:
        a = (zeile.get("alternativen") or [None])[0]
        grund = zeile.get("status_grund") or "kein Angebot belegt"
        if a and a.get("preis_eur") is not None:
            return f"Händler offen: {grund}; Richtpreis {str(a['preis_eur']).replace('.', ',')} EUR je {a.get('bezug_einheit', 'Stk')} als Annahme [A] (N-BESCHAFFUNG)"
        return f"offen: {grund} (N-BESCHAFFUNG)"
    eur = f"{p['einzelpreis_eur']:.2f}".replace(".", ",")
    land = p.get("land") or "Land offen"
    return (f"{p.get('haendler', 'Händler offen')} ({land}), {eur} EUR je {p.get('bezug_einheit', 'Stk')}, Stand {p.get('stand', '?')}, "
            f"Konfidenz {p.get('konfidenz', '?')}; Lieferung nach Deutschland: {p.get('lieferung_de', 'unbekannt')} (N-BESCHAFFUNG)")


# ---------------------------------------------------------------- Texte
S_NORM = "Rechteckhohlprofil, kaltgeformt, EN 10219-2 (Stahl S235); Feuerverzinkung EN ISO 1461 [A]"
NORM_SRB = "Sechskantschraube ISO 4017 (DIN 933), Festigkeitsklasse 8.8 nach ISO 898-1, verzinkt [A]"
Q_T = "docs/parts/nft_tisch.md, data/components/nft_tisch.json, scripts/workshop/nft_tisch.py"
Q_B = "docs/parts/ibc_beet.md, data/components/ibc_beet.json (blatt), docs/jobs/W40-BEET.md"
Q_R = "docs/parts/nft_rinne.md, data/components/nft_rinne.json"
NEIN, JA = "nein", "ja"


def E(name, funk, eig, norm, quelle, lm=NEIN, dim=None, expl=None, konf="angenommen", extra=None):
    return dict(name=name, funk=funk, eig=eig, norm=norm, quelle=quelle, lm=lm, dim=dim, expl=expl, konf=konf, extra=extra or {})


TISCH = {
    "bein": E("Bein (Pfosten)",
              "Die Beine tragen den Tisch: Je zwei Beine bilden mit dem Querholm einen Portalbock, der neben dem Beet auf dem Boden steht (beim Innentisch ein Pfosten außerhalb des Beckenrands).",
              ["Rechteckrohr aus verzinktem Stahl, unten an die Fußplatte geschweißt (MAG), danach feuerverzinkt.",
               "Die Beine stehen außerhalb der Beete: Die Fußplattenkante hat 45 mm Abstand zur Beetkante (innen 30 mm zum Beckenrand).",
               "Länge = Höhe der Rinnenunterkante (1000 mm) minus Holmhöhe 60 mm minus Fußplatte 5 mm, also rund 940 mm.",
               "Im Modell Wand 3 mm; der Katalogartikel ist ein Rohr mit 2,5 mm Wand: Abgleich offen."],
              S_NORM, Q_T + ", docs/research/R35.md (Rinnenhöhe)", dim="Rechteckrohr 40 × 40 × 3 mm, rund 940 mm lang"),
    "fussplatte": E("Fußplatte",
                    "Die Fußplatte verteilt die Last des Beins auf den Boden und wird mit zwei Schrauben M8 an Boden oder Betonpunkt befestigt.",
                    ["Blech 70 × 70 × 5 mm mit zwei Löchern Ø 9 mm für M8, diagonal angeordnet, 15 mm Randabstand.",
                     "Am Bein angeschweißt; Bohrungen vor dem Feuerverzinken.",
                     "Beim Innentisch muss der Pfosten wegen des Kippmoments des Kragarms mit Verbundankern gesichert werden; die Statik ist nicht nachgewiesen."],
                    "Stahlblech S235, Feuerverzinkung EN ISO 1461 [A]", Q_T, dim="Blech 70 × 70 × 5 mm, Löcher Ø 9 mm", expl={"richtung": [0, 0, -1], "abstand_mm": 150}),
    "holm": E("Querholm",
              "Der Querholm liegt quer über dem Bock und trägt die Rinnen: Auf seiner Oberkante liegen die Rinnen, an ihm sitzen die Rinnenhalter.",
              ["Rechteckrohr 60 mm hoch und 40 mm breit, so lang wie die Beet-Außenbreite plus Beine.",
               "Die Oberkante ist die Rinnenunterkante (Prüfmaß ±1 mm); die Höhe folgt dem Gefälle der Rinne von 1,5 %.",
               "Nicht an die Beine geschweißt, sondern über je einen Winkelhalter angeschraubt, damit der Tisch lösbar bleibt.",
               "Biegung: 50 kg mittig auf 1,2 m Spannweite ergeben 150 Nm, rund 15 N/mm² gegen 235 N/mm² Streckgrenze [E]."],
              S_NORM, Q_T, dim="Rechteckrohr 60 × 40 × 3 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 250}),
    "kragarm": E("Kragarm",
                 "Der Kragarm trägt die zwei Rinnen des Innentischs über dem Pool: Er geht vom Pfosten außerhalb des Beckenrands über das Wasser bis hinter die innerste Rinne.",
                 ["Rechteckrohr 60 mm hoch, 40 mm breit; ragt 30 mm über die innerste Rinne hinaus.",
                  "Die Unterkante liegt bei 940 mm; der Beckenrand bei etwa 650 mm: 290 mm Luft.",
                  "Der Arm wird wie der Querholm über einen Winkelhalter am Pfosten angeschraubt.",
                  "Das Kippmoment am Fuß beträgt rund 165 Nm; die Statik ist nicht nachgewiesen."],
                 S_NORM, Q_T, dim="Rechteckrohr 60 × 40 × 3 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 250}),
    "querstrebe": E("Querstrebe",
                    "Die Querstrebe verbindet die beiden Beine eines Bocks auf halber Höhe und steift ihn quer aus.",
                    ["Rechteckrohr 40 × 40 mm auf Höhe 650 mm (Unterkante 630 mm): so tief, wie die Pflanzen es erlauben (Pflanzen reichen bis etwa 560 mm).",
                     "An den Enden an die Beine geschweißt.",
                     "Im Modell Wand 3 mm; Katalogartikel 2,5 mm."],
                    S_NORM, Q_T + " (Höhe: Auftrag W33)", dim="Rechteckrohr 40 × 40 × 3 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 150}),
    "laengs": E("Längsstrebe",
                "Die Längsstrebe verbindet die beiden Böcke in Längsrichtung und steift den Tisch längs aus.",
                ["Rechteckrohr 40 × 40 mm, liegt an den Beinen auf Höhe 650 mm (beim Innentisch auf 400 mm unter dem Kragarm).",
                 "Je Beinseite eine Strebe, das Portal hat zwei, der Innentisch eine.",
                 "Im Modell Wand 3 mm; Katalogartikel 2,5 mm."],
                S_NORM, Q_T, dim="Rechteckrohr 40 × 40 × 3 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 150}),
    "diagonale": E("Diagonale (Portalbock)",
                   "Die beiden gekreuzten Diagonalen steifen den Portalbock gegen seitliches Verschieben aus.",
                   ["Flachstahl 3 mm dick (Breite 25 mm), außen an den Beinen, je Bock zwei gekreuzt.",
                    "Der Winkel zur Waagerechten liegt bei 12,5 bis 15,5 Grad; steiler geht nicht, weil die Strebe unter den Pflanzen liegt.",
                    "Jedes Ende ist mit einer Schraube M6 × 40 und Mutter durch das Bein gesichert."],
                   "Flachstahl S235, Feuerverzinkung EN ISO 1461 [A]", Q_T + " (Bild-Kritiker W16, Höhe W33)", dim="Flachstahl 25 × 3 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 100}),
    "ldiag": E("Längsdiagonale",
               "Die Längsdiagonale steift den Tisch in Längsrichtung zwischen den beiden Böcken aus.",
               ["Flachstahl 25 × 3 mm, außen an den Beinen, je Beinseite eine.",
                "Eingeführt nach dem Befund, dass das Gestell längs sonst nur über den unteren Riegel gehalten wird.",
                "Befestigung wie die Diagonalen mit M6-Schrauben durch das Bein."],
               "Flachstahl S235, Feuerverzinkung EN ISO 1461 [A]", Q_T + " (Bild-Kritiker W16)", dim="Flachstahl 25 × 3 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 100}),
    "winkel": E("Winkel des Winkelhalters",
                "Der Winkel verbindet Bein und Holm (beim Innentisch Pfosten und Kragarm) als lösbare Schraubverbindung.",
                ["Stahlwinkel 36 × 60 × 60 × 4 mm; ein Schenkel liegt an der Beininnenseite, der andere unter dem Holm.",
                 "36 mm Breite: 2 mm schmaler als Bein und Holm, damit die Diagonalen frei bleiben.",
                 "Je Bein ein Winkel; er trägt je zwei Löcher Ø 6,6 mm für M6 in beiden Schenkeln."],
                "Winkelstahl S235, Feuerverzinkung EN ISO 1461 [A]", "docs/parts/winkelhalter.md, " + Q_T, dim="Winkel 36 × 60 × 60 × 4 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 120}),
    "winkelhalter": E("Schrauben und Muttern der Winkelhalter",
                      "Diese Kleinteile schrauben die Winkelhalter fest: je Winkel zwei Schrauben M6 × 55 mit Muttern durch das Bein und zwei Schrauben M6 × 16 unter dem Holm.",
                      ["Sechs Normteile je Winkelhalter (vier Schrauben, zwei Muttern); im Modell haben sie keine einzelnen Namen mehr.",
                       "Die Schrauben unter dem Holm greifen in Blindnietmuttern M6, die nicht modelliert sind.",
                       "Der Katalog führt sie als Sammelartikel „Kleinteil am Winkelhalter“; die Maße 12 × 10 × 20 gelten genau für die kurzen Schrauben."],
                      NORM_SRB, "docs/parts/winkelhalter.md", dim="Normteile M6", expl={"richtung": [0, 0, 1], "abstand_mm": 200, "folgt": "winkel"}),
    "schraube_m8x30": E("Schraube M8 × 30 (Fußplatte)",
                        "Die Schraube hält die Fußplatte am Boden bzw. am Betonpunkt.",
                        ["Zwei Schrauben je Fußplatte durch die Löcher Ø 9 mm.",
                         "Im Modell steckt sie im Blech; real kommt unter die Platte ein Dübel oder Verbundanker (Statik offen).",
                         "Zählt im Katalog als Schraubensatz (Schraube, Mutter, zwei Scheiben)."],
                        NORM_SRB, "docs/parts/nft_tisch.md (Verbindungen), data/components/nft_tisch.json", dim="Sechskantschraube M8 × 30", expl={"richtung": [0, 0, -1], "abstand_mm": 250}),
    "schraube_m6x40": E("Schraube M6 × 40 (Diagonale)",
                        "Die Schraube sichert je ein Ende der Diagonale am Bein.",
                        ["Je Diagonalenende eine Schraube M6 × 40 quer durch das Bein, Mutter auf der Innenseite.",
                         "Der Kopf sitzt auf der Außenseite der Diagonale."],
                        NORM_SRB, "docs/parts/nft_tisch.md (Verbindungen)", dim="Sechskantschraube M6 × 40", expl={"richtung": [1, 0, 0], "abstand_mm": 120}),
    "mutter_m6": E("Mutter M6 (Diagonale)",
                   "Die Mutter zieht die Schraube der Diagonale am Bein fest.",
                   ["Sechskantmutter M6, sitzt innen am Bein.", "Gehört zum Schraubensatz; kein eigener Artikel in der Stückliste."],
                   "Sechskantmutter ISO 4032, Festigkeitsklasse 8, verzinkt [A]", "docs/parts/nft_tisch.md (Verbindungen)", dim="Sechskantmutter M6",
                   expl={"richtung": [-1, 0, 0], "abstand_mm": 120}, extra=dict(bezug="Im Schraubensatz M6 × 40 enthalten (Katalog SRB-satz-m6x40) [A]")),
    "schraube_m5x12": E("Schraube M5 × 12 (Rinnenhalter)",
                        "Die Schraube befestigt einen Rinnenhalter am Holm.",
                        ["Je Rinnenhalter eine Schraube M5 × 12 durch das Blech in den Holm.", "Zählt im Katalog als Schraubensatz."],
                        NORM_SRB, "docs/parts/nft_tisch.md (Verbindungen)", dim="Sechskantschraube M5 × 12", expl={"richtung": [0, 0, 1], "abstand_mm": 100, "folgt": "halter_rinne_l"}),
    "halter_rinne_l": E("Rinnenhalter links",
                        "Der Rinnenhalter hält die Rinne seitlich auf dem Holm: Je Rinne und Bock sitzt ein L-Blech links und eines rechts an der Rinnenwand.",
                        ["L-Blech 3 mm dick, 25 mm breit und 25 mm hoch, aus verzinktem Stahl.",
                         "Mit einer Schraube M5 × 12 auf dem Holm befestigt.",
                         "Der linke und der rechte Halter sind spiegelgleich; im Katalog ein Artikel."],
                        "Blech S235, 3 mm, verzinkt [A]", "docs/parts/nft_tisch.md (Rinnenhalter: Bild und Annahme)", dim="L-Blech 25 × 25 × 25 mm, 3 mm dick", expl={"richtung": [0, 0, 1], "abstand_mm": 250}),
    "halter_rinne_r": E("Rinnenhalter rechts",
                        "Der Rinnenhalter hält die Rinne seitlich auf dem Holm: Je Rinne und Bock sitzt ein L-Blech links und eines rechts an der Rinnenwand.",
                        ["L-Blech 3 mm dick, 25 mm breit und 25 mm hoch, aus verzinktem Stahl.",
                         "Mit einer Schraube M5 × 12 auf dem Holm befestigt.",
                         "Der linke und der rechte Halter sind spiegelgleich; im Katalog ein Artikel."],
                        "Blech S235, 3 mm, verzinkt [A]", "docs/parts/nft_tisch.md (Rinnenhalter: Bild und Annahme)", dim="L-Blech 25 × 25 × 25 mm, 3 mm dick", expl={"richtung": [0, 0, 1], "abstand_mm": 250}),
    "verteiler": E("Zulaufverteiler",
                   "Der Zulaufverteiler verteilt das Wasser vom Zulauf auf alle Rinnen des Tischs: An jeder Rinne zweigt ein Stutzen ab, auf den ein Schlauch zur Rinne gesteckt wird.",
                   ["PVC-Rohr d25, Wand 3 mm, schräg entlang der Sektorgrenze (18 Grad zur Querachse), damit jede Reihe denselben Abstand zur Ecke hat.",
                    "Ein Stutzen Ø 16 mm je Rinne, Richtung +X.",
                    "Durchfluss 0,5 l/min je Rinne.",
                    "Der Verteiler im Modell ist ein Einzelkörper; real aus Rohr, Stutzen und Klebefittings geklebt oder geschweißt."],
                   "PVC-U-Rohr DIN 8062 / EN 1452 [A]", Q_T + ", docs/research/R06.md (Durchfluss)", lm=JA, dim="Rohr d25, Wand 3 mm", expl={"richtung": [-1, 0, 0], "abstand_mm": 350}),
    "endstopfen_verteiler": E("Endstopfen Verteiler",
                              "Der Stopfen verschließt das freie Ende des Zulaufverteilers, damit das Wasser nur über die Stutzen zu den Rinnen fließt.",
                              ["Passt in das Verteilerrohr d25.", "Wird eingeklebt."],
                              "PVC-U-Kappe d25 [A]", Q_T, lm=JA, dim="Kappe d25", expl={"richtung": [0, 1, 0], "abstand_mm": 120, "folgt": "verteiler"}),
    "schlauch_rinne": E("Schlauch zur Rinne",
                        "Der Schlauch führt das Wasser vom Stutzen des Verteilers zur Tülle am Zulaufende einer Rinne.",
                        ["Innen Ø 16 mm, außen Ø 20 mm, hellblau; ein Schlauch je Rinne.", "Zwischen Stutzen und Tülle bleiben 70 mm frei, in denen der Schlauch sichtbar ist.", "Auf Stutzen und Tülle gesteckt, ohne Schelle im Modell."],
                        "Schlauch nach Herstellerangabe [A]", Q_T, lm=JA, dim="Schlauch ID 16 / AD 20 mm", expl={"richtung": [-1, 0, 0], "abstand_mm": 200}),
    "sammelrohr": E("Sammelrohr",
                    "Das Sammelrohr fängt das Wasser am Ablaufende aller Rinnen auf und führt es aus dem Tisch heraus.",
                    ["PVC-Rohr d50, Wand 3 mm, schräg entlang der Sektorgrenze.",
                     "Je Rinne eine Muffe d40 mit Bohrung d32 für den Ablaufstutzen.",
                     "Das Gefälle zum Anschluss ist im Modell nicht ausgeführt; das Rohr liegt waagerecht."],
                    "PVC-U-Rohr DIN 8062 / EN 1452 [A]", Q_T, lm=JA, dim="Rohr d50, Wand 3 mm", expl={"richtung": [1, 0, 0], "abstand_mm": 350}),
    "endstopfen_sammelrohr": E("Endstopfen Sammelrohr",
                               "Der Stopfen verschließt das freie Ende des Sammelrohrs.",
                               ["Passt in das Sammelrohr d50.", "Wird eingeklebt."],
                               "PVC-U-Kappe d50 [A]", Q_T, lm=JA, dim="Kappe d50", expl={"richtung": [0, 1, 0], "abstand_mm": 120, "folgt": "sammelrohr"}),
    "rinnenprofil": E("Rinne",
                      "Die Rinne führt einen dünnen Wasserfilm an den Wurzeln der Pflanzen entlang; die Pflanzen stehen in Netztöpfen in den Löchern der Oberseite.",
                      ["Hohlkammerprofil 130 × 100 mm; die Rinne selbst ist gerade, das Gefälle von 1,5 % entsteht durch die Böcke.",
                       "Jede Reihe hat ihre eigene Länge (rund 760 bis 2990 mm), eine Lochreihe in der Mitte, Lochabstand 200 mm; benachbarte Rinnen sind um 100 mm versetzt (Zickzack).",
                       "Zulaufende links, Ablaufende rechts; Wasser rund 10 mm hoch.",
                       "Im Tischmodell hat die Rinne kein Material (Standard), im Rinnenmodell PVC-U weiß: Der Katalog führt sie als PVC-U-Profil."],
                      "PVC-U, UV-stabilisiert (alternativ PP) [A]", Q_R, lm=JA, dim="Profil 130 × 100 mm, Länge je Reihe",
                      expl={"richtung": [0, 0, 1], "abstand_mm": 500}, extra=dict(werkstoff_soll="pvc_u")),
    "kappezulauf": E("Endkappe Zulauf",
                     "Die Zulaufkappe schließt die Rinne am Zulaufende ab und trägt die Tülle, auf die der Schlauch gesteckt wird.",
                     ["Tülle Ø 16 mm, Achse 70 mm über dem Rinnenboden.", "Auf die Rinne gesteckt und mit einer Dichtleiste abgedichtet; real aus 4-mm-PVC-Platte oder Spritzguss."],
                     "PVC-U [A]", Q_R, lm=JA, dim="Kappe für Profil 130 × 100 mm", expl={"richtung": [-1, 0, 0], "abstand_mm": 150, "folgt": "rinnenprofil"},
                     extra=dict(werkstoff_soll="pvc_u")),
    "kappeablauf": E("Endkappe Ablauf",
                     "Die Ablaufkappe schließt die Rinne am Ablaufende ab und trägt den Stutzen, über den das Wasser ins Sammelrohr fließt.",
                     ["Stutzen d32, Achse 20 mm über dem Rinnenboden: Es bleibt ein Restfilm in der Rinne.", "Auf die Rinne gesteckt und abgedichtet."],
                     "PVC-U [A]", Q_R, lm=JA, dim="Kappe für Profil 130 × 100 mm", expl={"richtung": [1, 0, 0], "abstand_mm": 150, "folgt": "rinnenprofil"},
                     extra=dict(werkstoff_soll="pvc_u")),
}

BEET = {
    "wanne": E("Beetwanne",
               "Die Wanne trägt das ganze Beet: Sie hält Medium, Wasser und Pflanzen und ist aus einem halben IBC-Container geschnitten.",
               ["Gebrauchter IBC (1000 l) aus HDPE, passend gesägt, Wand 4 mm, Innenradius der Ecken 40 mm.",
                "Länge und Breite je Beettyp; Randsims 20 × 14 mm; die Medienoberfläche liegt 75 mm unter dem Rand.",
                "Der Wannenboden hat eine Bohrung für den Tankverbinder des Ablaufs.",
                "Eingelassen in die Grube und waagerecht ausgerichtet."],
               "HDPE nach EN ISO 17855-1 [A]; gebrauchter IBC ohne Lebensmittelnachweis des Vornutzers [A]", Q_B, lm=JA, dim="HDPE, Wand 4 mm, aus IBC geschnitten", expl=None),
    "stuetze": E("Stützklotz",
                 "Die Stützklötze tragen den Sperrboden und das Medium auf dem Wannenboden.",
                 ["Klotz 60 × 60 mm aus PP, drei Reihen unter dem Sperrboden, Abstand höchstens 420 mm.",
                  "Hält rund 500 bis 700 kg Medium.",
                  "Die Höhe passt den Sperrboden an den Rand der Wanne an; darunter bleibt eine ungenutzte, trockene Luftkammer."],
                 "Polypropylen, Herstellerangabe offen [A]", Q_B, dim="Klotz 60 × 60 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 120}),
    "siebboden": E("Sperrboden",
                   "Der Sperrboden trennt das Medium vom Wannenboden, sodass unter dem Medium kein Wasser stehen bleibt; das Wasser läuft über ihn zum Siphon.",
                   ["PP-Platte 8 mm, ungelocht; nur eine Durchführung Ø 36 mm für die Plattenhülse des Siphons.",
                    "Der Name „Siebboden“ im Modell ist ein Altname: Die Platte ist seit der Umstellung nicht mehr gelocht.",
                    "Rand mit selbstklebendem EPDM-Zellkautschuk abgedichtet (Spalt 2 mm; Maß des Bandes offen).",
                    "Dichtheit am Muster zu prüfen: Leckwasser unter der Platte wäre wieder stehendes Wasser."],
                   "Polypropylen, Platte [A]", Q_B + " (Entscheidung Sperrboden)", dim="PP-Platte 8 mm, ungelocht", expl={"richtung": [0, 0, 1], "abstand_mm": 300}),
    "medium": E("Medium (Blähton)",
                "Das Medium trägt die Wurzeln der Pflanzen und ist Biofilter für das Wasser.",
                ["Blähton 8 bis 16 mm, gewaschen, 300 mm hoch; reicht bei Medienschutz 5 mm.",
                 "Menge je Beettyp: 467 bis 813 Liter (Schüttdichte 0,9 [A]).",
                 "Das Wasser steht nur in den Poren (rund 40 Prozent), nicht darunter.",
                 "Die Netztöpfe der Pflanzen stehen auf der Oberfläche, 75 mm unter dem Rand."],
                "Blähton, Körnung 8–16 mm, Herstellerangabe offen [A]", Q_B, lm=JA, dim="Schüttung 300 mm hoch", expl={"richtung": [0, 0, 1], "abstand_mm": 700}),
    "bulkhead": E("Tankverbinder (Wannenboden)",
                  "Der Tankverbinder führt das Wasser dicht durch den Wannenboden aus dem Beet heraus.",
                  ["Kunststoff-Wanddurchführung 32 mm × 1 Zoll mit Flansch (Modell: Ø 36, Flansch Ø 50), mit Dichtung und Kontermutter.",
                   "Im Ablaufloch des Wannenbodens, darin die Reduzierhülse 32/25.",
                   "Flanschmaß ist angenommen; Datenblatt nicht gelesen."],
                  "PVC-U-Tankverbinder, Klebemuffe, 10 bar [A]", Q_B, lm=JA, dim="Tankverbinder 32 mm × 1 Zoll, Flansch Ø 50", expl={"richtung": [0, 0, -1], "abstand_mm": 150}),
    "plattenhuelse": E("Plattenhülse (Tankverbinder im Sperrboden)",
                       "Die Plattenhülse dichtet den Durchgang des Siphons im Sperrboden ab, damit kein Wasser unter die Platte läuft.",
                       ["Tankverbinder wie im Wannenboden, hier durch die Bohrung Ø 36 mm im Sperrboden gesteckt und gekontert.",
                        "Darin sitzt eine Reduzierhülse 32/25 für das Standrohr."],
                       "PVC-U-Tankverbinder [A]", Q_B, lm=JA, dim="Hülse Ø 50 × 15 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 250}),
    "reduzierhuelse_boden": E("Reduzierhülse 32/25 (Wannenboden)",
                              "Die Hülse passt das Standrohr d25 in den Tankverbinder 32 mm ein.",
                              ["Klebefitting, Stutzen 32 mm, Muffe 25 mm; Baulänge im Modell 39 mm, nach Katalog 22 mm (Abweichung offen).",
                               "Wird in den Tankverbinder geklebt."],
                              "PVC-U-Reduzierung 32 × 25 [A]", Q_B, lm=JA, dim="Hülse Ø 32 × 39 mm", expl={"richtung": [0, 0, -1], "abstand_mm": 80, "folgt": "bulkhead"}),
    "reduzierhuelse_platte": E("Reduzierhülse 32/25 (Sperrboden)",
                               "Die Hülse passt das Standrohr d25 in die Plattenhülse ein.",
                               ["Klebefitting 32 auf 25 mm; Baulänge im Modell 15 mm.", "Sitzt im Tankverbinder des Sperrbodens, das Standrohr steckt darin."],
                               "PVC-U-Reduzierung 32 × 25 [A]", Q_B, lm=JA, dim="Hülse Ø 32 × 15 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 80, "folgt": "plattenhuelse"}),
    "reduktion": E("Reduktion unter dem Boden",
                   "Die Reduktion setzt den Ablauf unter dem Wannenboden vom Standrohr d25 auf das größere Rohr der Leitung (d40) um.",
                   ["Kurze Reduzierung d40 auf d25, Bauhöhe etwa 50 mm, unter dem Boden aufgeklebt.",
                    "Hier schließt das Leitungsnetz an; der Ablaufport liegt etwa 30 mm unter dem Wannenboden.",
                    "Der Katalogartikel führt sie als Reduktion d50 (Bezeichnung zu klären)."],
                   "PVC-U-Klebefitting [A]", Q_B + " (Port Ablauf)", lm=JA, dim="Reduktion 40 × 25 mm, rund 50 mm hoch", expl={"richtung": [0, 0, -1], "abstand_mm": 250}),
    "standrohr": E("Standrohr",
                   "Das Standrohr bestimmt den Wasserstand im Beet: Steigt das Wasser darüber, springt der Siphon an und entleert das Beet.",
                   ["PVC-U-Druckrohr d25 × 1,5 mm, rund 560 mm lang ab dem Boden.",
                    "Das Wasser steht bis zur Rohrkante, 35 mm unter der Medienoberfläche.",
                    "Die Glocke steht konzentrisch darüber."],
                   "PVC-U-Druckrohr PN10, ISO 4422 [A]", Q_B, lm=JA, dim="Rohr d25 × 1,5 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 400}),
    "glocke": E("Glocke (Siphon)",
                "Die Glocke deckt das Standrohr ab: Sie macht das Beet zum Flut-und-Ebbe-Beet, weil sie das Wasser bei Überschreiten des Standes in einem Zug durch das Standrohr zieht.",
                ["Rohr d75 mit Deckel, 295 mm lang, vier Kerben 10 × 12 mm am Fuß: Der Restfilm bleibt höchstens 12 mm hoch.",
                 "Die Kerben haben zusammen 480 mm², das Standrohr 380 mm²: Es läuft genug nach.",
                 "Das Anspringen bei 3,3 l/min ist nur am Muster prüfbar."],
                "PVC-U-Rohr d75 nach DIN 8062 / EN 1452 [A]", Q_B, lm=JA, dim="Rohr d75 × 295 mm, 4 Kerben 10 × 12", expl={"richtung": [0, 0, 1], "abstand_mm": 650}),
    "medienschutz": E("Medienschutz (Lochblech)",
                      "Der Medienschutz hält den Blähton von der Glocke fern, damit der Siphon nicht verstopft.",
                      ["Lochblech aus Edelstahl 1.4301, 1,5 mm, Rundloch 5 mm, Teilung 8 mm; im Modell als zwei Ringe aus 12 Schlitzen vereinfacht (6000 mm²).",
                       "Zylinder Ø 110 × 320 mm, gerollt und genietet (Zuschnitt etwa 366 × 340 mm).",
                       "Steht auf dem Sperrboden, oben mit loser Kappe.",
                       "Anfrage beim Metallbauer für Zuschnitt und Rollen liegt bei Ben."],
                      "Lochblech DIN 24041, Edelstahl 1.4301 [A]", Q_B + " (Entscheidung Schutzkorb)", lm=JA, dim="Zylinder Ø 110 × 320 mm, Blech 1,5 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 900}),
    "schutzkappe": E("Kappe Medienschutz",
                     "Die Kappe verschließt den Medienschutz oben, damit kein Blähton hineinfällt.",
                     ["Muffenstopfen DN110, lose aufgesetzt.", "Lässt sich zum Reinigen abnehmen."],
                     "Muffenstopfen DN110, PVC-U oder PP [A]", Q_B, lm=JA, dim="Stopfen DN110", expl={"richtung": [0, 0, 1], "abstand_mm": 1100, "folgt": "medienschutz"}),
    "tropfrohr": E("Zulauf-Tropfrohr",
                   "Das Tropfrohr verteilt das Zulaufwasser über die Länge des Beets.",
                   ["Rohr d20 (PE, Modell PVC), liegt längs im Beet, 50 mm von der Innenwand; Länge je Beettyp (Außenbeet 800: 2,36 m).",
                    "Durchfluss 200 bis 500 l/h; Tropflöcher sind im Modell quadratisch vereinfacht, real rund.",
                    "Das offene Ende reicht durch die Stirnwand nach außen; die Wanddurchführung ist nicht modelliert."],
                   "PE-Rohr nach DIN 8074 [A]", Q_B + " (Port Zulauf)", lm=JA, dim="Rohr d20, rund 2,36 m lang", expl={"richtung": [0, 0, 1], "abstand_mm": 500}),
    "endstopfen_zulauf": E("Endstopfen Tropfrohr",
                           "Der Stopfen verschließt das hintere Ende des Tropfrohrs, damit das Wasser aus den Tropflöchern austritt.",
                           ["Passt in das Rohr d20.", "Wird gesteckt oder geklebt."],
                           "Kappe d20 [A]", Q_B, lm=JA, dim="Stopfen d20", expl={"richtung": [1, 0, 0], "abstand_mm": 120, "folgt": "tropfrohr"}),
    "reinigungsschacht": E("Reinigungsschacht",
                           "Der Reinigungsschacht erlaubt, Schlamm vom Sperrboden abzusaugen, ohne das Medium auszuräumen.",
                           ["Rohr DN100 (Außen-Ø 110) steht senkrecht auf dem Sperrboden, rund 320 mm hoch.",
                            "Zwei Kerben 30 × 30 mm am Fuß lassen Wasser und Schlamm in den Schacht fließen.",
                            "Das Medium wird um den Schacht herum eingefüllt; Saugschlauch bis 75 mm Ø passt hinein."],
                           "KG- oder HT-Rohr DN100 [A]", Q_B, lm=JA, dim="Rohr Ø 110 × 320 mm", expl={"richtung": [0, 0, 1], "abstand_mm": 900}),
    "schachtkappe": E("Kappe Reinigungsschacht",
                      "Die Kappe verschließt den Reinigungsschacht oben und wird zum Reinigen abgenommen.",
                      ["Muffenstopfen DN110, lose aufgesetzt."], "Muffenstopfen DN110 [A]", Q_B, lm=JA, dim="Stopfen DN110", expl={"richtung": [0, 0, 1], "abstand_mm": 1100, "folgt": "reinigungsschacht"}),
}

# Rinne einzeln (nft_rinne und 16 Reihenvarianten): gleiche Teile wie im Tisch, eigene Quelle
RINNE = {k: TISCH[k] for k in ("rinnenprofil", "kappezulauf", "kappeablauf")}

NETZTOPF = {"netztopf": E("Netztopf",
                          "Der Netztopf hält die Pflanze im Beet (Blähton) oder in der Rinne und lässt die Wurzeln durch die Schlitze zum Wasser wachsen.",
                          ["Konischer Korb aus PP, 63 mm hoch, Kragen Ø 64 mm, Korpus oben Ø 50 mm, unten Ø 34 mm, Wand 1,5 mm.",
                           "Acht Schlitze 3 × 38 mm am Umfang, Boden mit Loch Ø 10 mm.",
                           "Steckt lose im Loch der Rinne (Loch Ø 52 mm, Kragen liegt auf) oder im Medium des Beets.",
                           "2222 Stück im Dom (Beete und Rinnen zusammen), ein Katalogartikel."],
                          "Polypropylen, Spritzguss [A]", "docs/parts/netztopf.md, data/components/netztopf.json", lm=JA, dim="Korb Ø 64 × 63 mm, Wand 1,5 mm",
                          expl={"richtung": [0, 0, 1], "abstand_mm": 120})}
SALAT = {
    "herz": E("Herz", "Das Herz ist die Mitte der Salatrosette, aus der die inneren Blätter wachsen.", ["Niedriges Achteck-Prisma, rund 20 mm hoch.", "Reine Darstellung: Der Salat ist kein Kaufteil."],
              "-", "docs/parts/salatkopf.md", lm=JA, dim="Achteck-Prisma, 20 mm hoch", expl={"richtung": [0, 0, 1], "abstand_mm": 40}),
    "blatt": E("Blätter", "Die Blätter bilden die sichtbare Rosette des Kopfsalats.",
               ["96 ebene Blätter, je 2 mm dick, auf einem Halbellipsoid angeordnet; Anstellwinkel steigt von flach am Rand bis steil in der Mitte.", "Größe: Standardkopf 100 mm; kleiner (70) und größer (130) sind Größenvarianten.", "Reine Darstellung für das Bild, nicht kaufbar."],
               "-", "docs/parts/salatkopf.md", lm=JA, dim="96 Blätter, je 2 mm dick", expl={"richtung": [0, 0, 1], "abstand_mm": 80}),
    "hals": E("Wurzelhals", "Der Hals steckt im Netztopf und trägt den Kopf.", ["Zylinder Ø 16 mm, 25 mm lang nach unten in den Topf.", "Reine Darstellung; echte Pflanzen haben Wurzeln, hier keine."],
              "-", "docs/parts/salatkopf.md", lm=JA, dim="Zylinder Ø 16 × 25 mm", expl={"richtung": [0, 0, -1], "abstand_mm": 60}),
}
PFLANZ = {"t_platte": E("Pflanztischplatte (Altmodell)",
                        "Die Platte war eine frühe Ansicht des Pflanztischs; sie ist ein Altmodell und im Dom nicht verbaut.",
                        ["Ein einziger Körper 2300 × 975 × 900 mm ohne Beine, Löcher und Rinnen.", "Ersetzt durch den NFT-Tisch mit Rinnen; kein Kaufteil, im Katalog als Altmodell geführt.", "Material im Modell: Standard (ohne Zuordnung)."],
                        "-", "scripts/workshop/pflanztisch.py, docs/components.md", lm=NEIN, dim="Platte 2300 × 975 × 900 mm (Altmodell)", expl=None, extra=dict(werkstoff_soll="holz_fichte"))}


# ---------------------------------------------------------------- Anwenden
def stl_zeilen():
    z = json.load(open(STL, encoding="utf-8"))["zeilen"]
    return {r["artikel_id"]: r for r in z}


def werkstoff_id(sc_name, sc_zu_werk):
    if sc_name in sc_zu_werk:
        return sc_zu_werk[sc_name]
    return sc_name


def anwenden(comp, titel, kurz, hinweis, teilenr, texte, gruppen, sc_zu_werk, zeilen, bez_override=None):
    pf = os.path.join(PD, comp + ".json")
    d = json.load(open(pf, encoding="utf-8"), object_pairs_hook=OrderedDict)
    ids = {t["id"] for t in d["teile"]}
    fehlt = ids - set(texte)
    if fehlt:
        sys.exit(f"FEHLER {comp}: keine Texte fuer {sorted(fehlt)}")
    for t in d["teile"]:
        e = texte[t["id"]]
        m = re.search(r"Masse ([\d.]+) g.*$", t["masse_mm"])
        t["masse_g"] = float(m.group(1)) if m else t.get("masse_g")
        orig = m.group(0) if m else t["masse_mm"]
        t["name"] = e["name"]
        t["masse_mm"] = (e["dim"] + "; " + orig) if e["dim"] else orig
        t["werkstoff"] = werkstoff_id(t["werkstoff"], sc_zu_werk) if t["werkstoff"] in sc_zu_werk else t["werkstoff"]
        t["funktion"] = e["funk"]
        t["eigenschaften"] = list(e["eig"])
        t["norm"] = e["norm"]
        t["norm_konfidenz"] = "angenommen"
        t["lebensmittelkontakt"] = e["lm"]
        t["lebensmittelkontakt_konfidenz"] = "angenommen"
        t["konfidenz"] = e["konf"]
        t["quelle"] = e["quelle"]
        art = t.get("artikel_id")
        if "bezug" in e["extra"]:
            t["bezug"] = e["extra"]["bezug"]
        elif art:
            t["bezug"] = bezug_text(zeilen.get(art))
        elif t["typ"] in ("normteil", "kaufteil"):
            t["bezug"] = "Kein eigener Artikel (im Schraubensatz oder Sammelartikel enthalten) [A]"
        if "werkstoff_soll" in e["extra"]:
            t["werkstoff_soll"] = e["extra"]["werkstoff_soll"]
        if e["expl"]:
            ex = dict(e["expl"])
            if ex.get("folgt") and ex["folgt"] not in ids:
                ex.pop("folgt")
            t["explosion"] = ex
        else:
            t.pop("explosion", None)
        t.pop("geruest", None)
    d["teilenummer"] = teilenr
    d["stand"] = "5a"
    d["titel"] = titel
    d["kurz"] = kurz
    d["hinweis"] = hinweis
    d["gruppen"] = [OrderedDict([("id", gid), ("name", gn), ("kurz", gk), ("teile", [i for i in gt if i in ids])]) for gid, gn, gk, gt in gruppen if any(i in ids for i in gt)]
    in_gr = {i for g in d["gruppen"] for i in g["teile"]}
    assert in_gr == ids, (comp, ids ^ in_gr)
    if not TROCKEN:
        with open(pf, "w", encoding="utf-8", newline="\n") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return d


GR_TISCH = [("gestell", "Gestell", "Beine, Holme und Streben tragen die Rinnen und stehen neben dem Beet.", ["bein", "fussplatte", "holm", "kragarm", "querstrebe", "laengs", "diagonale", "ldiag"]),
            ("verbindungen", "Verbindungen", "Winkelhalter und Schrauben halten die Teile lösbar zusammen.", ["winkel", "winkelhalter", "schraube_m8x30", "schraube_m6x40", "mutter_m6"]),
            ("rinnenhalter", "Rinnenhalter", "Die Halter fixieren jede Rinne auf dem Holm.", ["halter_rinne_l", "halter_rinne_r", "schraube_m5x12"]),
            ("rinnen", "Rinnen", "Die Rinnen mit ihren Endkappen, in denen die Pflanzen stehen.", ["rinnenprofil", "kappezulauf", "kappeablauf"]),
            ("wasserfuehrung", "Wasserführung", "Verteiler, Schläuche und Sammelrohr bringen das Wasser zu den Rinnen und wieder heraus.", ["verteiler", "endstopfen_verteiler", "schlauch_rinne", "sammelrohr", "endstopfen_sammelrohr"])]
GR_BEET = [("wanne_und_boden", "Wanne und Boden", "Die Wanne mit den Stützen und dem Sperrboden trägt das Medium.", ["wanne", "stuetze", "siebboden"]),
           ("medium", "Medium", "Der Blähton, in dem die Pflanzen wurzeln.", ["medium"]),
           ("ablauf", "Ablauf mit Siphon", "Tankverbinder, Standrohr, Glocke und Medienschutz entleeren das Beet im Takt.", ["bulkhead", "plattenhuelse", "reduzierhuelse_boden", "reduzierhuelse_platte", "reduktion", "standrohr", "glocke", "medienschutz", "schutzkappe"]),
           ("zulauf", "Zulauf", "Das Tropfrohr bringt das Wasser ins Beet.", ["tropfrohr", "endstopfen_zulauf"]),
           ("reinigung", "Reinigung", "Der Schacht zum Absaugen des Schlamms.", ["reinigungsschacht", "schachtkappe"])]
GR_RINNE = [("rinne", "Rinne", "Das Profil mit den Endkappen.", ["rinnenprofil", "kappezulauf", "kappeablauf"])]


def main():
    sc_zu_werk = katalog()
    zeilen = stl_zeilen()
    n = 0
    # Tische
    tinfo = {"innen": ("Innentisch (Ausleger über dem Pool, 2 Rinnen)", "Ein Auslegerbock hält zwei Rinnen über dem Pool: Pfosten außerhalb des Beckenrands, Kragarm über dem Wasser, Zulaufverteiler und Sammelrohr.", 10, 2),
             "mitte": ("Mitteltisch (Portal, 4 Rinnen)", "Zwei Portalböcke aus Rechteckrohr tragen vier Rinnen neben dem Innenbeet; Zulaufverteiler und Sammelrohr liegen schräg entlang der Sektorgrenze.", 6, 4),
             "aussen": ("Außentisch (Portal, 4 Rinnen)", "Zwei Portalböcke aus Rechteckrohr tragen vier Rinnen neben dem Außenbeet; Zulaufverteiler und Sammelrohr liegen schräg entlang der Sektorgrenze.", 8, 4)}
    hint_t = ("Texte und Zahlen aus docs/parts/nft_tisch.md, nft_rinne.md und winkelhalter.md. Maße sind überwiegend angenommen (Statik der Böcke nicht nachgewiesen); Katalogartikel führen die Rohre mit 2,5 mm Wand, das Modell mit 3 mm. "
              "Die Rinnen des Tischmodells tragen das Material Standard (ohne Zuordnung), der Katalog führt sie als PVC-U. Der europäische Bezug steht nur, wo die Stückliste ihn belegt.")
    for typ, (titel, kurz, anz, nr) in tinfo.items():
        anwenden(f"nft_tisch_{typ}", f"NFT-Tisch {titel}", kurz + f" Im Modell {anz}-mal.", hint_t, "T22", TISCH, GR_TISCH, sc_zu_werk, zeilen)
        n += 1
    # Beete
    binfo = {"aussen_800": ("Außenbeet 800 × 2640 mm (8 Stück)", 8), "aussen_933": ("Außenbeet 933 × 2953 mm (Variante, nicht verbaut)", 0),
             "aussen_993": ("Außenbeet 993 × 2953 mm (Variante, nicht verbaut)", 0), "innen_933": ("Innenbeet 933 × 1865 mm (6 Stück)", 6)}
    hint_b = ("Texte aus docs/parts/ibc_beet.md und data/components/ibc_beet.json (Beet mit ungelochtem Sperrboden, Medienschutz und Reinigungsschacht). Rohrwandstärken, Flansch D50 und Reduktionshöhe sind angenommen; "
              "Datenblätter der Kaufteile nicht gelesen. Die Artikelzuordnung von Plattenhülse, Reduzierhülse und den drei Kappen kommt aus der Gestaltregel der Stückliste und ist grob (Kappe d16, Reduktion d16/d32/d50): "
              "Korrektur gehört in die Regeln der Stückliste. Netztöpfe und Pflanzen sind Instanzen des Domes, nicht Teil des Beets.")
    for typ, (titel, anz) in binfo.items():
        anwenden(f"ibc_beet_{typ}", f"Substratbeet aus halbem IBC, {titel}", "Ein halber IBC-Container als Flut-und-Ebbe-Beet: Blähton über einem ungelochten Sperrboden, Wasser über das Tropfrohr, Entleeren per Glockensiphon bis auf 12 mm Restfilm.", hint_b, "T30", BEET, GR_BEET, sc_zu_werk, zeilen)
        n += 1
    # Rinnen
    rn = sorted(f[:-5] for f in os.listdir(PD) if f.startswith("nft_rinne") and f.endswith(".json"))
    for comp in rn:
        suffix = comp[len("nft_rinne"):].strip("_")
        titel = "NFT-Rinne" + (f" (Reihe {suffix.replace('_', ' ')})" if suffix else " (Vorlage)")
        anwenden(comp, titel, "Hohlkammerrinne 130 × 100 mm mit einer Lochreihe für Netztöpfe, Zulaufkappe mit Schlauchtülle und Ablaufkappe mit Stutzen.",
                 "Texte aus docs/parts/nft_rinne.md. Das Material der Rinne ist im Modell PVC-U weiß; Länge je Reihe aus dem Tischentwurf. Der europäische Bezug steht nur, wo die Stückliste ihn belegt.", "T20", RINNE, GR_RINNE, sc_zu_werk, zeilen)
        n += 1
    # Netztopf, Salat, Winkelhalter, Pflanztisch
    anwenden("netztopf", "Netztopf (Pflanzkorb)", "Ein konischer Kunststoffkorb mit Schlitzen: Er hält die Pflanze, die Wurzeln wachsen durch die Schlitze ins Wasser.",
             "Maße aus dem Modell (63 × Ø 64 mm). Die Zahl der Instanzen kommt aus dem Dom (2222); Fabrikat und Bezug in Europa sind offen.", "T10", NETZTOPF,
             [("topf", "Topf", "Der Korb selbst.", ["netztopf"])], sc_zu_werk, zeilen)
    anwenden("salatkopf", "Salatkopf (Darstellung)", "Ein Kopfsalat als Rosette aus 96 Blättern auf einem Herz und einem Hals; nur Darstellung, kein Kaufteil.",
             "Pflanzenmodell nur für das Bild; Werkstoff und Gewicht sind Näherungen. Kein Bezug nötig.", "T12", SALAT,
             [("pflanze", "Pflanze", "Herz, Blätter und Hals bilden den Kopf.", ["herz", "blatt", "hals"])], sc_zu_werk, zeilen)
    anwenden("winkelhalter", "Winkelhalter (Bein an Holm)", "Ein Stahlwinkel mit vier Schrauben und zwei Muttern verbindet das Bein eines Tischs lösbar mit dem Holm.",
             "Texte aus docs/parts/winkelhalter.md. Die Schrauben unter dem Holm greifen in Blindnietmuttern, die nicht modelliert sind.", "T23", {
                 "winkel": TISCH["winkel"],
                 "schraube_m6x16": E("Schraube M6 × 16 (unter dem Holm)", "Die Schraube hält den Winkel am Holm bzw. Kragarm.", ["Zwei Schrauben M6 × 16 durch den waagerechten Schenkel in die Blindnietmuttern im Holm.", "Zählt im Katalog als Schraubensatz."],
                                     NORM_SRB, "docs/parts/winkelhalter.md", dim="Sechskantschraube M6 × 16", expl={"richtung": [0, 0, -1], "abstand_mm": 100}),
                 "schraube_m6x55": E("Schraube M6 × 55 (am Bein)", "Die Schraube hält den Winkel am Bein.", ["Zwei Schrauben M6 × 55 durch den senkrechten Schenkel und das Bein, Mutter auf der Außenseite.", "Zählt im Katalog als Schraubensatz."],
                                     NORM_SRB, "docs/parts/winkelhalter.md", dim="Sechskantschraube M6 × 55", expl={"richtung": [0, 1, 0], "abstand_mm": 120}),
                 "mutter_m6": E("Mutter M6 (am Bein)", "Die Mutter zieht die Schraube durch das Bein fest.", ["Sechskantmutter M6 auf der Außenseite des Beins.", "Gehört zum Schraubensatz; kein eigener Artikel in der Stückliste."],
                                "Sechskantmutter ISO 4032, Festigkeitsklasse 8, verzinkt [A]", "docs/parts/winkelhalter.md", dim="Sechskantmutter M6",
                                expl={"richtung": [0, -1, 0], "abstand_mm": 120}, extra=dict(bezug="Im Schraubensatz M6 × 55 enthalten (Katalog SRB-satz-m6x55) [A]")),
             }, [("winkel", "Winkel", "Der Stahlwinkel.", ["winkel"]), ("schrauben", "Schrauben", "Schrauben und Muttern.", ["schraube_m6x16", "schraube_m6x55", "mutter_m6"])], sc_zu_werk, zeilen)
    anwenden("pflanztisch", "Pflanztisch (Altmodell)", "Eine einzelne Platte als frühe Ansicht des Pflanztischs; im Dom nicht verbaut.",
             "Altmodell ohne Instanz im Dom; kein Kaufteil, Stückliste führt es als Altmodell (Menge 0).", "T8", PFLANZ, [("platte", "Platte", "Die einzelne Tischplatte.", ["t_platte"])], sc_zu_werk, zeilen)
    print(n + 4, "Komponenten", "(Trockenlauf)" if TROCKEN else "geschrieben")


if __name__ == "__main__":
    main()
