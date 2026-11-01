"""Leitungsteile W39 (Kleinteile zur Bibliothek T70): Reduzierung d40/d20, Uebergang PE-PVC d20, Schlauch ID16 kurz, Kappen, Schlauchschelle,
Rueckschlagventile, Leerrohr-Reduzierung/-T, Kabeleinfuehrung. Bauweise wie leitung.py/leitung_w36.py (gleiche Helfer, gleiche Konvention).
leitung.py und leitung_w36.py bleiben unveraendert (Auftrag W39: nur lesen); ports() hier liefert die W39-Ports und fragt sonst leitung.ports().
Aufruf: python scripts/workshop/leitung_w39.py [teil ...]   (ohne Teil: alle; Teile: red pe hose kappe schelle rsv lr_red lr_t kabel)
        python scripts/workshop/leitung_w39.py --json [teil ...]   (schreibt w39_teile in leitungsteile.json und descriptions.json)"""
import sys, os, math, re, json
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

FILES = []          # Dateinamen (ohne .sc) der W39-Teile; check_leitungsteile.py zaehlt sie nicht zu den 63 Bibliotheksteilen
JOBS = []           # (teil, dateiname, Baufunktion)
PORTS = {}          # dateiname -> Funktion () -> [(name, (x,y,z), (dx,dy,dz), art, dn)]
JSON = {}           # teil -> Funktion () -> {dateiname: eintrag}
DESC = {}           # teil -> Liste von descriptions-Eintraegen
RENDER = {}         # dateiname -> Kamera-/Schnitt-Optionen fuer render()

def reg(teil, fname, fn):
    FILES.append(fname); JOBS.append((teil, fname, fn))

def mats(b):
    b.add("material.create", name="LT pp", density_g_cm3=0.91, color="#3d6b9c")
    b.add("material.create", name="LT pom", density_g_cm3=1.41, color="#e9e6df")
    b.add("material.create", name="LT epdm", density_g_cm3=1.1, color="#1a1a1a")

def pr(p):
    return tuple(round(float(v), 3) for v in p)

def ports(fname):
    """Ports eines W39-Teils (Format wie leitung.ports()); unbekannte Namen gehen an leitung.ports()."""
    if fname in PORTS:
        return PORTS[fname]()
    return L.ports(fname)

def jent(fname, pn, komp, werkstoff, **kw):
    return dict(teilenummer=pn, komponente=komp, werkstoff=werkstoff, **kw,
                ports=[{"name": n, "lage": list(pr(p)), "richtung": list(pr(dr)), "art": a, "dn": dn} for n, p, dr, a, dn in ports(fname)])

# ---------------------------------------------------------------- Teil 1: Reduzierung d40/d20
KETTE = [(40, 32), (32, 25), (25, 20)]                         # bisherige Kette je Beet (W36 Teil 5): drei Reduziermuffen, drei Klebestellen
def red_len(dg, dk): return L.DEPTH[dg] + L.DEPTH[dk] + 6
def red_kette(): return sum(red_len(a, b) for a, b in KETTE)

reg("red", "lt_reduzierung_d40_d20", lambda: L.reduzierung(40, 20))
JSON["red"] = lambda: {"lt_reduzierung_d40_d20": jent("lt_reduzierung_d40_d20", "T70-RED-40-20", "T70_Reduzierung_d40_d20", "PVC-U (Klebemuffen)",
    d_gross=40, d_klein=20, laenge=red_len(40, 20), aussen_d=L.od_f(40), muffentiefe_gross=L.DEPTH[40], muffentiefe_klein=L.DEPTH[20], innen_d=20 - 2 * L.wall_p(20),
    ersetzt={"kette": "40/32 + 32/25 + 25/20", "laenge_kette": red_kette(), "klebestellen_kette": 6, "klebestellen_neu": 2},
    herkunft={"Bauweise": "belegt (leitung.reduzierung, Bibliothek)", "laenge": "gerechnet t40 + t20 + 6", "muffentiefen": "Annahme EN 1452-3 gerundet", "handelsteil": "Katalog offen, Nachweis N-BESCHAFFUNG"})}
DESC["red"] = [{"match": "^lt_reduzierung_d40_d20$", "titel": "Reduzierung d40 auf d20 (Beet-Anschluss)", "was": "Eine Reduziermuffe vom Beete-Strang d40 direkt auf das Tropfrohr-Anschlussrohr d20; ersetzt die Kette aus drei Reduziermuffen.",
    "status": "gebaut, Prüfungen mit Volumen und Ports",
    "ablauf": ["Das Rohr d40 steckt in die große Muffe, das Rohr d20 in die kleine.", "Eine Klebestelle weniger je Seite: zwei statt sechs je Beet."],
    "aufbau": [{"t": "Maße", "p": ["Länge 48 mm (statt 142 mm der Kette)", "Außen 48, Muffentiefe 26 und 16"]}],
    "masse": {"Länge": "48 mm", "Kette bisher": "142 mm, drei Teile"}, "grenzen": "Muffentiefen und Außenmaß sind Bibliotheksnäherung; Handelsteil im Katalog offen.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- Teil 2: Uebergang PE-Rohr d20 auf Klebemuffe d20 (Klemmverbinder)
PE = dict(d=20.0, tiefe=30.0, mutter_d=32.0, mutter_l=18.0, mutter_boden=3.0, gegenbohrung=25.0, loch=20.4, ring_d=24.8, ring_z0=7.0, ring_z1=12.0,
          hals_d=24.6, hals_z0=12.0, kragen_d=30.0, kragen_z0=18.0, kragen_z1=30.0, muffe_z0=34.0, laenge=50.0)

def uebergang_pe():
    q = PE; dp = L.DEPTH[20]; of = L.od_f(20); wi = 20 - 2 * L.wall_p(20)
    b = sc.Build(); nm = "T70_Uebergang_PE_PVC_d20"
    L.setup(b, nm, 20, {"laenge": q["laenge"], "einstecktiefe_PE": q["tiefe"], "mutter_aussen": q["mutter_d"]})
    mats(b)
    z0, z1 = q["kragen_z0"], q["kragen_z1"]
    b.add("solid.cylinder", diameter=q["kragen_d"], height=z1 - z0, base=[0, 0, z0], operation="new", name="Kragen_R", body_name="Koerper")
    b.add("solid.cylinder", diameter=q["hals_d"], height=(z0 - q["hals_z0"]) + 1, base=[0, 0, q["hals_z0"]], operation="join", targets=["Koerper"], name="Gewindehals_R")
    b.add("solid.cylinder", diameter=of, height=q["laenge"] - z1 + 1, base=[0, 0, z1 - 1], operation="join", targets=["Koerper"], name="Klebemuffe_R")
    b.add("solid.cylinder", diameter=20, height=q["tiefe"] - q["hals_z0"] + 1, base=[0, 0, q["hals_z0"] - 1], operation="cut", targets=["Koerper"], name="PE_Aufnahme")
    b.add("solid.cylinder", diameter=wi, height=q["laenge"] - q["hals_z0"] + 3, base=[0, 0, q["hals_z0"] - 1], operation="cut", targets=["Koerper"], name="Durchgang")
    b.add("solid.cylinder", diameter=20, height=dp + 1, base=[0, 0, q["muffe_z0"]], operation="cut", targets=["Koerper"], name="Muffe_B")
    b.add("solid.cylinder", diameter=q["mutter_d"], height=q["mutter_l"], base=[0, 0, 0], operation="new", name="Mutter_R", body_name="Mutter")
    b.add("solid.cylinder", diameter=q["gegenbohrung"], height=q["mutter_l"] - q["mutter_boden"] + 1, base=[0, 0, q["mutter_boden"]], operation="cut", targets=["Mutter"], name="Mutter_Innen")
    b.add("solid.cylinder", diameter=q["loch"], height=q["mutter_boden"] + 2, base=[0, 0, -1], operation="cut", targets=["Mutter"], name="Mutter_Loch")
    b.add("solid.cylinder", diameter=q["ring_d"], height=q["ring_z1"] - q["ring_z0"], base=[0, 0, q["ring_z0"]], operation="new", name="Ring_R", body_name="Klemmring")
    b.add("solid.cylinder", diameter=20, height=q["ring_z1"] - q["ring_z0"] + 2, base=[0, 0, q["ring_z0"] - 1], operation="cut", targets=["Klemmring"], name="Ring_Bohrung")
    b.add("material.assign", bodies=["Koerper", "Mutter"], material="LT pp")
    b.add("material.assign", bodies=["Klemmring"], material="LT pom")
    L.meta(b, nm, "T70-UEB-PE20", "Klemmverbinder PE-Rohr d20 auf Klebemuffe PVC-U d20: A Klemme (Mutter, Klemmring), B Klebemuffe, Einstecktiefe PE 30")
    return b, nm, dict(q)

def ports_pe():
    return [("A", (0, 0, 0), (0, 0, -1), "Klemme", "PE d20"), ("B", (0, 0, PE["laenge"]), (0, 0, 1), "Muffe", L.DN[20])]
RENDER["lt_uebergang_pe_pvc_d20"] = dict(yaw=3.14159, pitch=0.0, section="XZ", zoom=2.2)
reg("pe", "lt_uebergang_pe_pvc_d20", uebergang_pe); PORTS["lt_uebergang_pe_pvc_d20"] = ports_pe
JSON["pe"] = lambda: {"lt_uebergang_pe_pvc_d20": jent("lt_uebergang_pe_pvc_d20", "T70-UEB-PE20", "T70_Uebergang_PE_PVC_d20", "PP (Koerper, Mutter), POM (Klemmring); Klebemuffe PVC-U-kompatibel",
    laenge=PE["laenge"], einstecktiefe_pe=PE["tiefe"], mutter={"aussen_d": PE["mutter_d"], "laenge": PE["mutter_l"], "gewinde_im_eingriff": PE["kragen_z0"] - PE["hals_z0"]},
    klemmring={"aussen_d": PE["ring_d"], "innen_d": 20, "breite": PE["ring_z1"] - PE["ring_z0"]}, kragen={"aussen_d": PE["kragen_d"], "laenge": PE["kragen_z1"] - PE["kragen_z0"]},
    klebemuffe={"d": 20, "tiefe": L.DEPTH[20], "aussen_d": L.od_f(20)}, durchgang_d=20 - 2 * L.wall_p(20),
    herkunft={"Bauform": "Annahme (kein Katalog gelesen), Handelsteil 'Klemmverbinder PE-PVC'", "einstecktiefe 30, mutter 32 x 18, kragen 30": "Annahme", "klebemuffe": "gerechnet aus Bibliothek (d20, Tiefe 16)", "handelsteil": "Katalog offen, Nachweis N-BESCHAFFUNG"})}
DESC["pe"] = [{"match": "^lt_uebergang_pe_pvc_d20$", "titel": "Übergang PE-Rohr d20 auf Klebemuffe", "was": "Klemmverbinder zwischen dem PE-Tropfrohr d20 des Beets und dem geklebten PVC-Rohrnetz; das PE-Rohr ist nicht klebbar.",
    "status": "gebaut, Prüfungen mit Interferenz 0 gegen das eingesteckte PE-Rohr",
    "ablauf": ["Das PE-Rohr wird 30 mm tief durch Mutter und Klemmring gesteckt und mit der Mutter geklemmt.", "Auf der anderen Seite wird das PVC-Rohr d20 in die Klebemuffe geklebt."],
    "aufbau": [{"t": "Teile", "p": ["Körper mit Kragen, Gewindehals und Klebemuffe", "Überwurfmutter 32 × 18", "Klemmring (POM)"]}],
    "masse": {"Länge": "50 mm", "Einstecktiefe PE": "30 mm"}, "grenzen": "Maße angenommen, kein Katalog gelesen; Nachweis später in N-BESCHAFFUNG.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- Teil 3: Schlauch ID16, Laenge 100 (Stueck zwischen Stutzen und Tuelle)
HOSE_L = 100
reg("hose", "lt_schlauch_id16_L100", lambda: L.schlauch(16, HOSE_L))
PORTS["lt_schlauch_id16_L100"] = lambda: [("A", (0, 0, 0), (0, 0, -1), "Schlauchende", "ID16"), ("B", (0, 0, HOSE_L), (0, 0, 1), "Schlauchende", "ID16")]
JSON["hose"] = lambda: {"lt_schlauch_id16_L100": jent("lt_schlauch_id16_L100", "T70-SCH-16", "T70_Schlauch_ID16", "PVC-Schlauch hellblau (Frischwasser)", innen_d=16, aussen_d=20, wand=2.0, laenge=HOSE_L,
    stueck=76, variante_von="lt_schlauch_id16 (Laenge 1000)", herkunft={"laenge": "belegt (Tisch-Blatt hose_gap 70 mm plus Aufsteckenden)", "wand 2": "Annahme der Bibliothek", "stueckzahl 76": "gerechnet 38 Rinnen x 2 Linien"})}
DESC["hose"] = [{"match": "^lt_schlauch_id16_L100$", "titel": "Schlauch ID16, kurz (100 mm)", "was": "Kurzes Schlauchstück für den Zulauf je NFT-Rinne zwischen Verteilerstutzen und Tülle; Variante des Schlauchs ID16 der Bibliothek.",
    "status": "gebaut, Prüfungen mit Volumen und Ports",
    "ablauf": ["Beide Enden werden auf Tüllen D16 gesteckt und mit je einer Schlauchschelle gesichert.", "76 Stück: 38 Rinnen je Linie, zwei Linien."],
    "aufbau": [{"t": "Maße", "p": ["Innen 16, Außen 20, Länge 100", "Farbe hellblau (Frischwasser)"]}],
    "masse": {"Länge": "100 mm"}, "grenzen": "Die Länge 100 deckt den freien Abschnitt 70 mm plus Aufsteckenden; genaue Länge entscheidet die Montage.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- Teil 4: Kappe d20 und d50 (Stopfen als Aufsteck-Kappe, Boden geschlossen)
KAPPE_SIZES = (20, 50)
KAPPE_BODEN = 3.0                                             # geschlossener Boden [A]

def kappe(d):
    dp = L.DEPTH[d]; h = dp + KAPPE_BODEN
    b = sc.Build(); nm = f"T70_Kappe_d{d}"
    L.setup(b, nm, d, {"hoehe": h, "boden": KAPPE_BODEN})
    b.add("solid.cylinder", diameter=L.od_f(d), height=h, base=[0, 0, 0], operation="new", name="Kappe_R", body_name="Kappe")
    b.add("solid.cylinder", diameter=d, height=dp + 1, base=[0, 0, -1], operation="cut", targets=["Kappe"], name="Muffe_A")
    b.add("material.assign", bodies=["Kappe"], material="LT pvc")
    L.meta(b, nm, f"T70-KAP-{d}", f"Kappe PVC-U d{d} ({L.DN[d]}), Klebemuffe, Boden {KAPPE_BODEN:g} geschlossen, steckt auf einen Zapfen/ein Rohrende")
    return b, nm, dict(h=h)

for _d in KAPPE_SIZES:
    reg("kappe", f"lt_kappe_d{_d}", (lambda d=_d: kappe(d)))
    PORTS[f"lt_kappe_d{_d}"] = (lambda d=_d: [("A", (0, 0, 0), (0, 0, -1), "Muffe", L.DN[d])])
JSON["kappe"] = lambda: {f"lt_kappe_d{d}": jent(f"lt_kappe_d{d}", f"T70-KAP-{d}", f"T70_Kappe_d{d}", "PVC-U (Klebemuffe)", d=d, hoehe=L.DEPTH[d] + KAPPE_BODEN, boden=KAPPE_BODEN, aussen_d=L.od_f(d), muffentiefe=L.DEPTH[d],
    verwendung={"d20": "Messkreis-Abgang am Verteiler d50, Linie 2 unbenutzt (Abgang 3, 1 Stueck); Reserveabgang", "d50": "Reserveabgang d50 am Verteiler d50 (Abgang 4 Bypass bei abgesperrter Linie)"}[f"d{d}"],
    herkunft={"Bauweise": "A (SDR-21-Naeherung der Bibliothek)", "boden 3": "Annahme", "aussen": "gerechnet od_f(d)", "handelsteil": "Katalog offen, Nachweis N-BESCHAFFUNG"}) for d in KAPPE_SIZES}
DESC["kappe"] = [{"match": "^lt_kappe_d", "titel": "Kappe d20 und d50 (Abgang verschließen)", "was": "Aufsteck-Kappe mit geschlossenem Boden, die einen unbenutzten Abgang oder ein Rohrende verschließt, z. B. den Messkreis-Abgang d20 am Verteiler d50 der Linie 2.",
    "status": "gebaut, Prüfungen mit Interferenz 0 gegen den Zapfen und den Verteiler d50",
    "ablauf": ["Die Kappe wird auf den Zapfen geklebt (Einstecktiefe wie die Muffe: d20 16 mm, d50 31 mm).", "Der Boden ist 3 mm dick und verschließt den Abgang."],
    "aufbau": [{"t": "Maße", "p": ["d20: Außen 27, Höhe 19", "d50: Außen 58,5, Höhe 34"]}],
    "masse": {"Kappe d20": "8,2 g", "Kappe d50": "42,7 g"}, "grenzen": "Maße aus der Bibliotheksnäherung, Handelsteil im Katalog offen.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- Teil 6: Rueckschlagventil d40, d25, d20 (Kugel-/Klappen-Rueckschlagventil, Klebemuffen), Durchfluss A nach B (+Z)
RSV_SIZES = (40, 25, 20)
RSV_LB = 50.0                                                 # Gehaeuselaenge wie der Kugelhahn (L = 50 + 2 t)
def rsv_geom(d):
    of = L.od_f(d); dp = L.DEPTH[d]; wi = d - 2 * L.wall_p(d)
    return dict(of=of, ob=of + 12, dp=dp, wi=wi, L=RSV_LB + 2 * dp)
def rsv_vol(d):
    g = rsv_geom(d)
    return math.pi / 4 * (g["of"] ** 2 * 2 * g["dp"] + g["ob"] ** 2 * RSV_LB - d ** 2 * 2 * g["dp"] - g["wi"] ** 2 * RSV_LB)

def rueckschlagventil(d):
    g = rsv_geom(d); of, ob, dp = g["of"], g["ob"], g["dp"]
    b = sc.Build(); nm = f"T70_Rueckschlagventil_d{d}_A-B"          # A-B = Pfeil: Durchfluss nur von A nach B (+Z)
    L.setup(b, nm, d, {"laenge": round(g["L"], 1)})
    b.add("solid.cylinder", diameter=ob, height=RSV_LB, base=[0, 0, dp], operation="new", name="Gehaeuse_R", body_name="Rueckschlagventil")
    for z0, nmn in ((0, "A"), (dp + RSV_LB, "B")):
        b.add("solid.cylinder", diameter=of, height=dp, base=[0, 0, z0], operation="join", targets=["Rueckschlagventil"], name="Stutzen_" + nmn)
    b.add("solid.cylinder", diameter=d, height=dp + 1, base=[0, 0, -1], operation="cut", targets=["Rueckschlagventil"], name="Muffe_A")
    b.add("solid.cylinder", diameter=d, height=dp + 1, base=[0, 0, g["L"] - dp], operation="cut", targets=["Rueckschlagventil"], name="Muffe_B")
    b.add("solid.cylinder", diameter=g["wi"], height=g["L"] + 2, base=[0, 0, -1], operation="cut", targets=["Rueckschlagventil"], name="Durchgang")
    b.add("material.assign", bodies=["Rueckschlagventil"], material="LT hahn")
    L.meta(b, nm, f"T70-RSV-{d}", f"Rueckschlagventil PVC-U d{d} ({L.DN[d]}), Klebemuffen, Durchfluss nur von A nach B (+Z) -> ; Einbau waagerecht oder senkrecht aufwaerts")
    return b, nm, g

for _d in RSV_SIZES:
    RENDER[f"lt_rueckschlagventil_d{_d}"] = dict(yaw=3.14159, pitch=0.0, section="XZ", zoom=2.0)
    reg("rsv", f"lt_rueckschlagventil_d{_d}", (lambda d=_d: rueckschlagventil(d)))
    PORTS[f"lt_rueckschlagventil_d{_d}"] = (lambda d=_d: [("A (Zulauf)", (0, 0, 0), (0, 0, -1), "Muffe", L.DN[d]), ("B (Abgang)", (0, 0, rsv_geom(d)["L"]), (0, 0, 1), "Muffe", L.DN[d])])
JSON["rsv"] = lambda: {f"lt_rueckschlagventil_d{d}": jent(f"lt_rueckschlagventil_d{d}", f"T70-RSV-{d}", f"T70_Rueckschlagventil_d{d}_A-B", "PVC-U (Klebemuffen), Innenteile nicht modelliert", d=d, laenge=rsv_geom(d)["L"], gehaeuse_aussen_d=rsv_geom(d)["ob"],
    gehaeuse_laenge=RSV_LB, muffentiefe=L.DEPTH[d], durchgang_d=rsv_geom(d)["wi"], durchfluss="nur von A nach B (+Z)", einbaulage="waagerecht oder senkrecht aufwaerts (Fluss nach oben); nie senkrecht abwaerts",
    verwendung={40: "Foerderleitung K58/K59 (Sumpf)", 25: "Luft-Hauptverteiler, 6 Abgaenge, und Pool-Verteiler (W37)", 20: "Luft-Hauptverteiler, 6 Abgaenge, und Pool-Verteiler (W37)"}[d],
    herkunft={"Bauweise": "A, Vorbild leitung.kugelhahn ohne Hebel", "gehaeuse 50 lang, aussen od_f + 12": "Annahme wie Kugelhahn", "handelsteil": "Kugel-/Klappen-Rueckschlagventil, Katalog offen, Nachweis N-BESCHAFFUNG"}) for d in RSV_SIZES}
DESC["rsv"] = [{"match": "^lt_rueckschlagventil_d", "titel": "Rückschlagventil d40, d25 und d20", "was": "Sperrt die Gegenrichtung der Leitung: Wasser oder Luft fließt nur von A nach B. Gebraucht an den Förderleitungen des Sumpfs (d40) und an den Luftverteilern (d25, d20).",
    "status": "gebaut, Prüfungen mit Volumen und Ports",
    "ablauf": ["Einbau in Flussrichtung A nach B; waagerecht oder senkrecht aufwärts, nie senkrecht abwärts.", "Klebemuffen wie der Kugelhahn, Länge 50 plus zwei Muffentiefen.", "Innenteile (Kugel oder Klappe, Feder) sind nicht modelliert."],
    "aufbau": [{"t": "Maße", "p": [f"d40: Länge {rsv_geom(40)['L']:g}, Gehäuse {rsv_geom(40)['ob']:g}", f"d25: Länge {rsv_geom(25)['L']:g}, Gehäuse {rsv_geom(25)['ob']:g}", f"d20: Länge {rsv_geom(20)['L']:g}, Gehäuse {rsv_geom(20)['ob']:g}"]}],
    "masse": {f"d{d}": f"{rsv_vol(d) * 1.4e-3:.0f} g" for d in RSV_SIZES}, "grenzen": "Bauform und Maße angenommen (Kugelhahn ohne Hebel); Handelsteil im Katalog offen.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- Teil 9: Kabeleinfuehrung DN50 und DN100 (Leerrohr-Muffe unten, Flansch-Aufnahme im Schaltschrank-Boden oben)
import leitung_w36 as W36                                     # nur lesen: Leerrohr-Masse LR (Muffentiefe, Muffen-Aussen, AD, Wand)
KAB_SIZES = (50, 100)
KAB = dict(kragen_dicke=6.0, dichtung=3.0, boden=3.0, mutter=8.0, ueberstand=4.0, hals_plus=7.0, kragen_plus=30.0, dichtung_minus=10.0, mutter_plus=18.0)   # alle [A]

def kab_geom(dn):
    q = W36.LR[dn]; t, om = q["t"], q["od_m"]; k = KAB
    hals = om + k["hals_plus"]; kragen = hals + k["kragen_plus"]
    z_k1 = t + k["kragen_dicke"]; z_d1 = z_k1 + k["dichtung"]; z_b1 = z_d1 + k["boden"]; z_m1 = z_b1 + k["mutter"]; z_top = z_m1 + k["ueberstand"]
    return dict(t=t, od_m=om, d=q["d"], wi=q["d"] - 2 * q["wall"], hals=hals, kragen=kragen, dichtung_aussen=kragen - k["dichtung_minus"], mutter_aussen=hals + k["mutter_plus"],
                z_k1=z_k1, z_d1=z_d1, z_b1=z_b1, z_m1=z_m1, z_top=z_top)

def kabeleinfuehrung(dn):
    g = kab_geom(dn); k = KAB; t = g["t"]
    b = sc.Build(); nm = f"T70_Kabeleinfuehrung_DN{dn}"
    L.setup(b, nm, 20, {"muffentiefe": t, "hals_aussen": g["hals"], "kragen_aussen": g["kragen"], "boden_dicke": k["boden"]})
    mats(b)
    b.add("solid.cylinder", diameter=g["od_m"], height=t + 1, base=[0, 0, 0], operation="new", name="Muffe_R", body_name="Koerper")
    b.add("solid.cylinder", diameter=g["kragen"], height=k["kragen_dicke"], base=[0, 0, t], operation="join", targets=["Koerper"], name="Kragen_R")
    b.add("solid.cylinder", diameter=g["hals"], height=g["z_top"] - (g["z_k1"] - 1), base=[0, 0, g["z_k1"] - 1], operation="join", targets=["Koerper"], name="Gewindehals_R")
    b.add("solid.cylinder", diameter=g["d"], height=t + 1, base=[0, 0, -1], operation="cut", targets=["Koerper"], name="Muffe_A")
    b.add("solid.cylinder", diameter=g["wi"], height=g["z_top"] + 2, base=[0, 0, t - 1], operation="cut", targets=["Koerper"], name="Kabeldurchgang")
    b.add("solid.cylinder", diameter=g["dichtung_aussen"], height=k["dichtung"], base=[0, 0, g["z_k1"]], operation="new", name="Dichtung_R", body_name="Dichtung")
    b.add("solid.cylinder", diameter=g["hals"], height=k["dichtung"] + 2, base=[0, 0, g["z_k1"] - 1], operation="cut", targets=["Dichtung"], name="Dichtung_Bohrung")
    b.add("solid.cylinder", diameter=g["mutter_aussen"], height=k["mutter"], base=[0, 0, g["z_b1"]], operation="new", name="Mutter_R", body_name="Gegenmutter")
    b.add("solid.cylinder", diameter=g["hals"], height=k["mutter"] + 2, base=[0, 0, g["z_b1"] - 1], operation="cut", targets=["Gegenmutter"], name="Mutter_Bohrung")
    b.add("material.assign", bodies=["Koerper", "Gegenmutter"], material="LT pp")
    b.add("material.assign", bodies=["Dichtung"], material="LT epdm")
    L.meta(b, nm, f"T70-KE-{dn}", f"Kabeleinfuehrung DN{dn} fuer Leerrohr AD{g['d']:g}: A Steckmuffe (Leerrohr), B Flansch-Aufnahme im Schaltschrank-Boden ({k['boden']:g} mm), Dichtung EPDM, Gegenmutter")
    return b, nm, g

for _dn in KAB_SIZES:
    reg("kabel", f"lt_kabeleinfuehrung_dn{_dn}", (lambda dn=_dn: kabeleinfuehrung(dn)))
    PORTS[f"lt_kabeleinfuehrung_dn{_dn}"] = (lambda dn=_dn: [("A", (0, 0, 0), (0, 0, -1), "Muffe", f"DN{dn}"), ("B", (0, 0, kab_geom(dn)["z_d1"]), (0, 0, 1), "Flansch-Aufnahme", f"Boden {KAB['boden']:g} mm, Loch {kab_geom(dn)['hals']:g}")])
    RENDER[f"lt_kabeleinfuehrung_dn{_dn}"] = dict(yaw=3.14159, pitch=0.0, section="XZ", zoom=2.0)
JSON["kabel"] = lambda: {f"lt_kabeleinfuehrung_dn{dn}": jent(f"lt_kabeleinfuehrung_dn{dn}", f"T70-KE-{dn}", f"T70_Kabeleinfuehrung_DN{dn}", "PP (Koerper, Gegenmutter), EPDM (Dichtung)", dn=dn, leerrohr_aussen_d=kab_geom(dn)["d"], muffentiefe=kab_geom(dn)["t"], muffe_aussen=kab_geom(dn)["od_m"],
    kabeldurchgang_d=kab_geom(dn)["wi"], kragen={"aussen_d": kab_geom(dn)["kragen"], "dicke": KAB["kragen_dicke"]}, hals={"aussen_d": kab_geom(dn)["hals"], "gewindelaenge": kab_geom(dn)["z_top"] - kab_geom(dn)["z_k1"]},
    dichtung={"aussen_d": kab_geom(dn)["dichtung_aussen"], "innen_d": kab_geom(dn)["hals"], "dicke": KAB["dichtung"]}, gegenmutter={"aussen_d": kab_geom(dn)["mutter_aussen"], "dicke": KAB["mutter"]},
    boden={"dicke": KAB["boden"], "lochdurchmesser": kab_geom(dn)["hals"], "z_unterkante": kab_geom(dn)["z_d1"], "z_oberkante": kab_geom(dn)["z_b1"]}, hoehe=kab_geom(dn)["z_top"],
    verwendung="Schaltschrank (Teil von W37-3): Leerrohr kommt von unten, Kabel gehen durch den Boden in den Schrank; Standort des Schranks offen (E13)",
    herkunft={"Bauform Wanddurchfuehrung mit Dichtung und Gegenmutter": "A, Handelsteil, kein Katalog gelesen", "Kragen, Hals, Dichtung, Mutter, Boden 3": "Annahme", "Muffe": "gerechnet aus lt_leerrohr_dn* (W36)", "handelsteil": "Katalog offen, Nachweis N-BESCHAFFUNG"}) for dn in KAB_SIZES}
DESC["kabel"] = [{"match": "^lt_kabeleinfuehrung_dn", "titel": "Kabeleinführung DN50 und DN100 (Schaltschrank)", "was": "Verbindet das unterirdische Leerrohr mit dem Boden des Schaltschranks: unten die Muffe für das Leerrohr, oben ein Flansch mit Gewindehals, Dichtung und Gegenmutter, der durch den Boden des Schranks geführt wird.",
    "status": "gebaut, Prüfungen mit Interferenz 0 gegen ein Boden-Blech",
    "ablauf": ["Das Leerrohr steckt von unten in die Muffe.", "Der Hals geht durch das Loch im Schrankboden; die Dichtung liegt unter dem Boden, die Gegenmutter oben.", "Die Kabel laufen durch das Leerrohr in den Schrank; Abzweige nur mit Zugdose."],
    "aufbau": [{"t": "Maße", "p": [f"DN50: Muffe 56 × 40, Hals {kab_geom(50)['hals']:g}, Flansch {kab_geom(50)['kragen']:g}", f"DN100: Muffe 123 × 64, Hals {kab_geom(100)['hals']:g}, Flansch {kab_geom(100)['kragen']:g}", "Boden des Schranks 3 mm"]}],
    "masse": {"Höhe DN50": f"{kab_geom(50)['z_top']:g} mm", "Höhe DN100": f"{kab_geom(100)['z_top']:g} mm"}, "grenzen": "Bauform und Maße angenommen, kein Katalog gelesen; der Standort des Schaltschranks ist offen (Entscheidung E13).", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- Teil 5: Schlauchschelle ID16 und ID25 (Schneckengewinde-Schelle)
SS = {16: dict(ad=20.0, lo=12.0, hi=22.0), 25: dict(ad=29.0, lo=20.0, hi=32.0)}      # Schlauch-Innen-D -> Aussen-D und Spannbereich (Handelsangabe [A])
SS_BAND_W, SS_BAND_T = 9.0, 0.7                                # Band 9 breit, 0,7 dick [A]
SS_GEH = dict(laenge=16.0, hoehe=8.0, spalt=0.2, kanal=5.4, schraube=5.0, kopf=8.0, kopf_l=3.0, schaft_l=18.0)   # Gehaeuse 9 x 16 x 8 [A]

def ss_geom(idd):
    q = SS[idd]; g = SS_GEH
    ro = q["ad"] / 2 + SS_BAND_T
    zb = q["ad"] / 2 + g["spalt"]                              # Gehaeuseunterkante
    zs = zb + g["hoehe"] / 2                                   # Schraubenachse (Y) in Gehaeusemitte
    return dict(ad=q["ad"], ro=ro, zb=zb, zs=zs, zt=zb + g["hoehe"], lo=q["lo"], hi=q["hi"])

def schlauchschelle(idd):
    s = ss_geom(idd); g = SS_GEH; w = SS_BAND_W
    b = sc.Build(); nm = f"T70_Schlauchschelle_ID{idd}"
    L.setup(b, nm, 20, {"bandbreite": w, "bandstaerke": SS_BAND_T, "spannbereich_von": s["lo"], "spannbereich_bis": s["hi"]})
    b.add("solid.cylinder", diameter=2 * s["ro"], height=w, base=[-w / 2, 0, 0], axis=[1, 0, 0], operation="new", name="Band_R", body_name="Schelle")
    b.add("solid.box", length=w, width=g["laenge"], height=g["hoehe"], center=[0, 0, s["zb"] + g["hoehe"] / 2], operation="join", targets=["Schelle"], name="Gehaeuse_R")
    b.add("solid.cylinder", diameter=s["ad"], height=w + 2, base=[-w / 2 - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Schelle"], name="Band_Bohrung")
    b.add("solid.cylinder", diameter=g["kanal"], height=g["laenge"] + 2, base=[0, -g["laenge"] / 2 - 1, s["zs"]], axis=[0, 1, 0], operation="cut", targets=["Schelle"], name="Schneckenkanal")
    b.add("solid.cylinder", diameter=g["schraube"], height=g["schaft_l"], base=[0, -g["laenge"] / 2 - 1, s["zs"]], axis=[0, 1, 0], operation="new", name="Schaft_R", body_name="Schneckenschraube")
    b.add("solid.cylinder", diameter=g["kopf"], height=g["kopf_l"] + 1, base=[0, g["laenge"] / 2 - 1 + 1, s["zs"]], axis=[0, 1, 0], operation="join", targets=["Schneckenschraube"], name="Kopf_R")
    b.add("material.assign", bodies=["Schelle", "Schneckenschraube"], material="LT stahl")
    L.meta(b, nm, f"T70-SS-{idd}", f"Schlauchschelle (Schneckengewinde) fuer Schlauch ID{idd}/AD{s['ad']:g}, Spannbereich {s['lo']:g} bis {s['hi']:g}, Band {w:g} breit, Achse X")
    return b, nm, s

for _i in SS:
    reg("schelle", f"lt_schlauchschelle_id{_i}", (lambda i=_i: schlauchschelle(i)))
    PORTS[f"lt_schlauchschelle_id{_i}"] = (lambda i=_i: [("Schlauchachse", (0, 0, 0), (1, 0, 0), "Aufnahme", f"AD{SS[i]['ad']:g}")])
    RENDER[f"lt_schlauchschelle_id{_i}"] = dict(yaw=0.9, pitch=0.5, zoom=2.4)
JSON["schelle"] = lambda: {f"lt_schlauchschelle_id{i}": jent(f"lt_schlauchschelle_id{i}", f"T70-SS-{i}", f"T70_Schlauchschelle_ID{i}", "Stahl verzinkt (Band, Gehaeuse, Schnecke)", schlauch_id=i, schlauch_aussen_d=SS[i]["ad"], spannbereich=[SS[i]["lo"], SS[i]["hi"]],
    band={"breite": SS_BAND_W, "dicke": SS_BAND_T, "aussen_d": 2 * ss_geom(i)["ro"]}, gehaeuse={"laenge": SS_GEH["laenge"], "breite": SS_BAND_W, "hoehe": SS_GEH["hoehe"], "unterkante_z": ss_geom(i)["zb"]}, hoehe=ss_geom(i)["zt"],
    stueckzahl={16: "152 (2 je Schlauch ID16 laut Stueckliste der Bibliothek, 76 kurze Schlaeuche)", 25: "nach Bedarf der Montage"}[i],
    herkunft={"Bauform Schneckengewinde-Schelle": "A, Handelsteil; kein Katalog gelesen", "Band 9 x 0,7, Gehaeuse 16 x 8, Schraube d5": "Annahme", "Spannbereich": "Handelsangabe [A]", "ID25-Variante": "dieselbe Funktion schlauchschelle(idd), kein Mehraufwand"}) for i in SS}
DESC["schelle"] = [{"match": "^lt_schlauchschelle_id", "titel": "Schlauchschelle ID16 und ID25", "was": "Schneckengewinde-Schelle, die einen Schlauch auf einer Tülle sichert: ID16 (Außen 20, Spannbereich 12 bis 22) für die Rinnen-Zuläufe, ID25 (Außen 29, Spannbereich 20 bis 32) für die größeren Schläuche.",
    "status": "gebaut, Prüfungen mit Interferenz 0 gegen den Schlauch",
    "ablauf": ["Die Schelle wird über den Schlauch auf der Tülle geschoben.", "Mit der Schneckenschraube anziehen; zwei Schellen je Schlauch."],
    "aufbau": [{"t": "Teile", "p": ["Band 9 × 0,7 mit Gehäuse 16 × 8", "Schneckenschraube Ø5 mit Kopf"]}],
    "masse": {"Stückzahl ID16": "152 (Stückliste der Bibliothek)"}, "grenzen": "Bauform und Maße angenommen, kein Katalog gelesen; Nachweis später in N-BESCHAFFUNG.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- Teil 7: Leerrohr-Reduzierung DN100 auf DN50 (Muffe A DN100, Zapfen B DN50)
LRR = dict(wand_boden=6.0, neck_d=70.0, neck_l=10.0, zapfen_l=50.0)
def lrr_geom():
    q1, q0 = W36.LR[100], W36.LR[50]
    z1 = q1["t"] + LRR["wand_boden"]; z2 = z1 + LRR["neck_l"]; Ltot = z2 + LRR["zapfen_l"]
    return dict(q1=q1, q0=q0, z1=z1, z2=z2, L=Ltot, wi=q0["d"] - 2 * q0["wall"])

def leerrohr_red():
    g = lrr_geom(); q1, q0 = g["q1"], g["q0"]
    b = sc.Build(); nm = "T70_LeerrohrRed_DN100_DN50"
    W36.lr_setup(b, nm, 100, {"laenge": g["L"], "d_klein": q0["d"]})
    b.add("solid.cylinder", diameter=q1["od_m"], height=g["z1"], base=[0, 0, 0], operation="new", name="Muffe_R", body_name="Reduzierung")
    b.add("solid.cylinder", diameter=LRR["neck_d"], height=LRR["neck_l"] + 1, base=[0, 0, g["z1"] - 1], operation="join", targets=["Reduzierung"], name="Uebergang_R")
    b.add("solid.cylinder", diameter=q0["d"], height=LRR["zapfen_l"] + 1, base=[0, 0, g["z2"] - 1], operation="join", targets=["Reduzierung"], name="Zapfen_R")
    b.add("solid.cylinder", diameter=q1["d"], height=q1["t"] + 1, base=[0, 0, -1], operation="cut", targets=["Reduzierung"], name="Muffe_A")
    b.add("solid.cylinder", diameter=g["wi"], height=g["L"] + 2, base=[0, 0, -1], operation="cut", targets=["Reduzierung"], name="Durchgang")
    b.add("material.assign", bodies=["Reduzierung"], material="LT leerrohr")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number="T70-LRR-100-50", description="Leerrohr-Reduzierung PVC-U DN100 (AD110) auf DN50 (AD50): Muffe A DN100, glattes Ende B DN50 (Zapfen)", revision="A", properties={"Werkstoff": "PVC-U"})
    return b, nm, g

reg("lr_red", "lt_leerrohr_red_dn100_dn50", leerrohr_red)
PORTS["lt_leerrohr_red_dn100_dn50"] = lambda: [("A", (0, 0, 0), (0, 0, -1), "Muffe", "DN100"), ("B", (0, 0, lrr_geom()["L"]), (0, 0, 1), "Zapfen", "DN50")]
RENDER["lt_leerrohr_red_dn100_dn50"] = dict(yaw=3.14159, pitch=0.0, section="XZ", zoom=2.0)
JSON["lr_red"] = lambda: {"lt_leerrohr_red_dn100_dn50": jent("lt_leerrohr_red_dn100_dn50", "T70-LRR-100-50", "T70_LeerrohrRed_DN100_DN50", "PVC-U (Kabelschutzrohr)", farbe="orange", laenge=lrr_geom()["L"], muffe_a={"dn": 100, "d": 110.0, "aussen_d": 123.0, "tiefe": 64.0},
    zapfen_b={"dn": 50, "aussen_d": 50.0, "laenge": LRR["zapfen_l"], "innen_d": lrr_geom()["wi"]}, uebergang={"aussen_d": LRR["neck_d"], "laenge": LRR["neck_l"], "form": "gestuft, nicht konisch"}, routing="buried",
    herkunft={"Muffe A und Zapfen B": "E aus lt_leerrohr_dn100/dn50 (W36 Teil 3, Katalognaeherung)", "Bodenwand 6, Uebergang 70 x 10, Zapfen 50 lang": "Annahme", "Reihenfolge Muffe A / Zapfen B": "wie die Leerrohr-Bogen (Muffe A, Zapfen B)", "handelsteil": "Katalog offen, Nachweis N-BESCHAFFUNG"})}
DESC["lr_red"] = [{"match": "^lt_leerrohr_red_", "titel": "Leerrohr-Reduzierung DN100 auf DN50", "was": "Wechselt unterirdisch vom Leerrohr DN100 (230-V-Kabel) auf DN50 (Signalkabel); Muffe für das große Rohr, glattes Ende für die Muffe des kleinen.",
    "status": "gebaut, Prüfungen mit Volumen und Ports",
    "ablauf": ["Das glatte Ende des Leerrohrs DN100 steckt in die Muffe A.", "Das Zapfenende B (Außen 50) steckt in die Muffe des Leerrohrs DN50 oder eines Bogens."],
    "aufbau": [{"t": "Maße", "p": ["Länge 130, Muffe 123 × 64, Zapfen AD50 × 50 lang", "Übergang gestuft, nicht konisch"]}],
    "masse": {"Länge": "130 mm"}, "grenzen": "Der Übergang ist gestuft statt konisch; Maße aus den Katalognäherungen von W36.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- Teil 8: Leerrohr-T DN50 und DN100 (Abzweig 90 Grad, gleich gross, drei Muffen)
def lrt_geom(dn):
    q = W36.LR[dn]
    return dict(q=q, a=q["t"] + q["od_m"] / 2, wi=q["d"] - 2 * q["wall"])

def leerrohr_t(dn):
    g = lrt_geom(dn); q = g["q"]; a = g["a"]; t = q["t"]; om = q["od_m"]
    b = sc.Build(); nm = f"T70_LeerrohrT_DN{dn}"
    W36.lr_setup(b, nm, dn, {"arm": round(a, 1)})
    b.add("solid.cylinder", diameter=om, height=2 * a, base=[-a, 0, 0], axis=[1, 0, 0], operation="new", name="Lauf_R", body_name="Leerrohr_T")
    b.add("solid.cylinder", diameter=om, height=a, base=[0, 0, 0], axis=[0, 0, 1], operation="join", targets=["Leerrohr_T"], name="Abgang_R")
    b.add("solid.cylinder", diameter=q["d"], height=t + 1, base=[-a - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Leerrohr_T"], name="Muffe_L")
    b.add("solid.cylinder", diameter=q["d"], height=t + 1, base=[a - t, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Leerrohr_T"], name="Muffe_R")
    b.add("solid.cylinder", diameter=q["d"], height=t + 1, base=[0, 0, a - t], axis=[0, 0, 1], operation="cut", targets=["Leerrohr_T"], name="Muffe_Z")
    b.add("solid.cylinder", diameter=g["wi"], height=2 * a + 2, base=[-a - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Leerrohr_T"], name="Durchgang_X")
    b.add("solid.cylinder", diameter=g["wi"], height=a + 1, base=[0, 0, 0], axis=[0, 0, 1], operation="cut", targets=["Leerrohr_T"], name="Durchgang_Z")
    b.add("material.assign", bodies=["Leerrohr_T"], material="LT leerrohr")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number=f"T70-LRT-{dn}", description=f"Leerrohr-T PVC-U DN{dn} AD{q['d']:g}, drei Steckmuffen, Abzweig 90 Grad (scharfer Abzweig: Kabel nur mit Zugdose)", revision="A", properties={"Werkstoff": "PVC-U"})
    return b, nm, g

for _dn in (50, 100):
    reg("lr_t", f"lt_leerrohr_t_dn{_dn}", (lambda dn=_dn: leerrohr_t(dn)))
    PORTS[f"lt_leerrohr_t_dn{_dn}"] = (lambda dn=_dn: [("A", (-lrt_geom(dn)["a"], 0, 0), (-1, 0, 0), "Muffe", f"DN{dn}"), ("B", (lrt_geom(dn)["a"], 0, 0), (1, 0, 0), "Muffe", f"DN{dn}"), ("C", (0, 0, lrt_geom(dn)["a"]), (0, 0, 1), "Muffe", f"DN{dn}")])
    RENDER[f"lt_leerrohr_t_dn{_dn}"] = dict(yaw=0.7, pitch=0.5, zoom=1.8)
JSON["lr_t"] = lambda: {f"lt_leerrohr_t_dn{dn}": jent(f"lt_leerrohr_t_dn{dn}", f"T70-LRT-{dn}", f"T70_LeerrohrT_DN{dn}", "PVC-U (Kabelschutzrohr)", farbe="orange", dn=dn, aussen_d=lrt_geom(dn)["q"]["d"], muffentiefe=lrt_geom(dn)["q"]["t"], muffe_aussen=lrt_geom(dn)["q"]["od_m"], arm=lrt_geom(dn)["a"],
    kabel_hinweis="Abzweig 90 Grad ohne Radius: Kabel (Mindestradius 15 x Kabel-d) laufen nur mit Zugdose im T durch, nicht als Kabelbogen", routing="buried",
    herkunft={"Teilung a = t + Muffen-Aussen/2": "E wie lt_t_d* der Bibliothek", "Muffe, AD, Wand": "E aus lt_leerrohr_dn* (W36 Teil 3, Katalognaeherung)", "handelsteil": "Katalog offen, Nachweis N-BESCHAFFUNG"}) for dn in (50, 100)}
DESC["lr_t"] = [{"match": "^lt_leerrohr_t_dn", "titel": "Leerrohr-T DN50 und DN100", "was": "Abzweig 90° für Leerrohre mit drei Steckmuffen; der Abzweig hat keinen Kabelradius, Kabel laufen nur mit einer Zugdose hindurch.",
    "status": "gebaut, Prüfungen mit Volumen gegen unabhängiges Raster und Ports",
    "ablauf": ["Alle drei Rohr-Zapfen stecken in die Muffen.", "Kabel nie durch den scharfen Abzweig ziehen: Zugdose setzen oder Bögen verwenden."],
    "aufbau": [{"t": "Maße", "p": [f"DN50: Arm {lrt_geom(50)['a']:g}, Muffe 56 × 40", f"DN100: Arm {lrt_geom(100)['a']:g}, Muffe 123 × 64"]}],
    "masse": {"Arm DN50": f"{lrt_geom(50)['a']:g} mm", "Arm DN100": f"{lrt_geom(100)['a']:g} mm"}, "grenzen": "Maße aus den Katalognäherungen von W36; Abzweigradius hart (siehe Blatt).", "quelle": "docs/parts/leitungsteile.md (Ergänzung W39)"}]

# ---------------------------------------------------------------- MARKE-EINFUEGEN (weitere Teile werden oberhalb dieser Zeile ergaenzt)

# ---------------------------------------------------------------- Ausgabe nach JSON und descriptions
def write_json(teile):
    p = os.path.join(sc.ROOT, "data", "components", "leitungsteile.json")
    d = json.load(open(p, encoding="utf-8"))
    for t in teile:
        d.setdefault("w39_teile", {}).update(JSON[t]())
    txt = json.dumps(d, indent=1, ensure_ascii=False).replace("\n", "\r\n")
    open(p, "w", encoding="utf-8", newline="").write(txt)

def write_descriptions(teile):
    """Fuegt die W39-Eintraege vor dem ersten lt_-Eintrag (^lt_verteiler_d50$) in data/descriptions.json ein (Viewer nimmt den ersten Treffer; ^lt_leerrohr_ stuende sonst davor); idempotent."""
    p = os.path.join(sc.ROOT, "data", "descriptions.json")
    txt = open(p, "rb").read().decode("utf-8")
    anchor = '    {\r\n      "match": "^lt_verteiler_d50$",'
    assert txt.count(anchor) == 1
    for t in teile:
        for e in DESC[t]:
            if json.dumps(e["match"], ensure_ascii=False) in txt:
                continue
            body = json.dumps(e, indent=2, ensure_ascii=False).replace("\n", "\n    ").replace("\n", "\r\n")
            txt = txt.replace(anchor, "    " + body + ",\r\n" + anchor)
    json.loads(txt)
    open(p, "wb").write(txt.encode("utf-8"))

def render(fname, yaw=0.7, pitch=0.4, section=None, zoom=1.7):
    """Pruefbild renders/components/leitungsteile/<datei>.png: Mitte der Huellbox, Abstand zoom x Diagonale."""
    path = os.path.join(sc.ROOT, "designs", "components", fname + ".sc")
    mn, mx = sc.bbox_all(sc.evaluate(path))
    tgt = [(a + b) / 2 for a, b in zip(mn, mx)]
    diag = math.dist(mn, mx)
    out = os.path.join(sc.ROOT, "renders", "components", "leitungsteile", fname + ".png")
    sc.snapshot(path, out, tgt, yaw, pitch, diag * zoom, w=900, h=700, section=section)
    return out

if __name__ == "__main__":
    want = set(a for a in sys.argv[1:] if not a.startswith("--"))
    if "--render" in sys.argv:
        for key, fname, fn in JOBS:
            if not want or key in want:
                print(render(fname, **RENDER.get(fname, {})))
        sys.exit(0)
    if "--json" in sys.argv:
        ts = [t for t in JSON if not want or t in want]
        write_json(ts); write_descriptions(ts); print("json:", ts); sys.exit(0)
    for key, fname, fn in JOBS:
        if want and key not in want:
            continue
        res = fn()
        L.save(res[0], res[1], fname)
        print(fname, res[2] if len(res) > 2 else "")
