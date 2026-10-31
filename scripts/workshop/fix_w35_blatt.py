"""W35: erzeugt aus messstellen.COMPS, data/messstellen.json (R39) und den gebauten .sc-Dateien (Masse, Box)
(1) data/components/messstellen.json (Parameter, Teile, Ports aller 23 Komponenten, maschinenlesbar fuer die Montage),
(2) das Sammelblatt docs/parts/messstellen.md (Herkunft Q/E/A, Preis aus R39, Kalibrierintervall, Lebensmittelkontakt),
(3) die descriptions-Gruppen ^halter_ und ^sonde_ in data/descriptions.json (Funktion, Alarmgrenze). Idempotent.
Aufruf: python scripts/workshop/fix_w35_blatt.py   (nach messstellen.py und check_messstellen.py)"""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import messstellen as M

D = json.load(open(os.path.join(sc.ROOT, "data", "messstellen.json"), encoding="utf-8"))
MS = D["messstellen"]
AL = {a["id"]: a for a in D["alarmgrenzen"]}
fmt = lambda v: f"{v:g}" if isinstance(v, float) else str(v)

# ---- Messung der gebauten Dateien
MEAS = {}
for key in M.COMPS:
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", key + ".sc"))
    mn, mx = sc.bbox_all(ev)
    MEAS[key] = dict(bodies={b["name"]: b["mass_g"] for b in ev["bodies"]}, mass=sum(b["mass_g"] for b in ev["bodies"]) / 1000, box=(mn, mx))

# ---- Stueckzahlen aus den Messstellen
hz = collections.Counter(); sz = collections.Counter(); sp = collections.Counter(); sstufe = collections.defaultdict(lambda: [0, 0])
alarm_of = collections.defaultdict(set)
for m in MS:
    for h, n in m["halter"]:
        hz[h] += n
    for s, n in m["sonden"].items():
        sz[s] += n
        sstufe[s][0 if m["stufe"] == "pflicht" else 1] += n
        alarm_of[s].update(m.get("alarm") or [])
hz["H_BOX"] = len(D["messknoten"])
d50 = sum(m["sonden"].get("flow_gross", 0) for m in MS)
STUECK = {"halter_inline_d50": d50, "halter_inline_d32": hz["H_INLINE"] - d50}
def stueck(key):
    c = M.COMPS[key]
    return STUECK.get(key, hz[c["id"]]) if c["kind"] == "halter" else sz[c["id"]]

# ---- Lebensmittelkontakt je Sondentyp und Halter (Annahmen, keine Zulassung belegt)
LM = {"do_ind": "Wasserkontakt ja (Fischwasser); Gehaeusewerkstoff des Herstellers nicht belegt [A], Konformitaet fuer Lebensmittelkontakt ungeprueft",
      "do_mini": "wie do_ind", "ph": "wie do_ind (Glas/Epoxid-Gehaeuse laut Hersteller-Erscheinung [A])", "ec": "wie do_ind",
      "temp_ds": "Wasserkontakt ja; Edelstahlhuelse (Handelsware)", "level_float": "Wasserkontakt ja; Kunststoff, Konformitaet offen [A]",
      "level_druck": "Wasserkontakt ja; Edelstahl/Keramik (Herstellerblog), Konformitaet offen", "flow_12": "Wasserkontakt ja (Paddelrad im Strom); Werkstoff nicht belegt [A]",
      "flow_gross": "Clamp-on: kein Wasserkontakt; Inline-Typ: ja, offen", "druck_schalter": "Wasser- bzw. Luftkontakt; Edelstahl-Anschluss statt Messing (Kupfer ist fuer Fische giftig) [A]",
      "strom_ct": "kein Wasserkontakt (Schaltschrank)", "co2_scd41": "kein Wasserkontakt (Kuppelluft), Strahlungsschutz", "par": "kein Wasserkontakt (Kuppelluft)", "leck": "kein Lebensmittelkontakt (Boden, Kontaktflaeche trocken bis zur Leckage)"}
LMH = {"H_TAUCH": "PVC-U-Rohr im Wasser (EN 1452, handelsueblich fuer Trinkwasser; Zulassung des Fabrikats pruefen [A]); Klemme (Stahl) ausserhalb des Wassers",
       "H_BERUHIG": "PVC-U im Wasser (wie H_TAUCH); Schelle ausserhalb", "H_ZELLE": "PVC-U/PVC-Armatur im Wasser; Zulassung des Fabrikats pruefen [A]",
       "H_INLINE": "PVC-U-Bloecke, Union-Verschraubung PVC; Sieb Edelstahl; Zulassung des Fabrikats pruefen [A]", "H_HAHN": "PVC-Hahn und -Tuelle im Wasser; Zulassung pruefen [A]",
       "H_DRUCK": "PVC-Anbohrschelle; Nippel Edelstahl (nicht Messing)", "H_MAST": "Luft, kein Wasserkontakt", "H_BOX": "Luft, kein Wasserkontakt (IP65)"}

def alarm_text(s):
    ids = sorted(alarm_of[s])
    out = []
    for i in ids[:3]:
        a = AL[i]
        t = f"{i} {a['groesse']} {a['ort']}: Warnung {a['warn'] or '-'}, Alarm {a['alarm'] or '-'}" + (f", Notfall {a['notfall']}" if a.get("notfall") else "")
        out.append(t)
    return "; ".join(out) if out else "kein eigener Alarm (Signal fuer Verknuepfungen)"

def preis(t):
    p = t["preis"]
    if p["min"] is None:
        return f"offen ({p['beleg']})"
    return (f"{fmt(p['min'])}" if p["min"] == p["max"] else f"{fmt(p['min'])}-{fmt(p['max'])}") + f" {p['waehrung']} ({p['beleg']})"

# ---- (1) maschinenlesbar
out = {"klasse": "messstellen", "stand": "31.10.2026 (W35)", "quelle": "docs/research/R39.md, data/messstellen.json; Masse der Sonden Annahme [A]", "komponenten": {}}
for key, c in M.COMPS.items():
    p = {k: v[0] for k, v in c["params"].items()}
    out["komponenten"][key] = {"id": c["id"], "art": c["kind"], "teilenummer": c["nr"], "titel": c["titel"], "ks": c["ks"], "funktion": c["funktion"], "stueck_laut_R39": stueck(key),
                               "parameter": {k: {"wert": v[0], "einheit": v[1], "herkunft": v[2]} for k, v in c["params"].items()},
                               "teile": [{"koerper": t[0], "beschreibung": t[1], "werkstoff": t[2], "herkunft": t[3], "masse_g": round(MEAS[key]["bodies"][t[0]], 1)} for t in c["teile"]],
                               "ports": [{"name": q[0], "mass": q[1], "lage": [round(v, 2) for v in q[2]], "richtung": list(q[3]), "koerper": q[4], "spitze": q[5]} for q in c["ports"](p)],
                               "masse_kg": round(MEAS[key]["mass"], 3), "box": [[round(v, 1) for v in MEAS[key]["box"][0]], [round(v, 1) for v in MEAS[key]["box"][1]]]}
json.dump(out, open(os.path.join(sc.ROOT, "data", "components", "messstellen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- (2) Sammelblatt
L = []
L.append("# Sammelblatt Messstellen-Bauteile T90/T91 (erzeugt von `scripts/workshop/fix_w35_blatt.py` aus `scripts/workshop/messstellen.py`, `data/messstellen.json` und den gebauten Dateien, nicht von Hand aendern)\n")
L.append("**Funktion:** Halter und Sonden-Platzhalter fuer die 67 Messstellen der Fachrecherche R39 (22 Pflicht, 45 Zusatz). Die Montage setzt sie an den Messstellen (`data/messstellen.json`: `halter`, `sonden`); jede Komponente hat Ports (Lage der Spitze im Bauteil-KS, Richtung), die Teile-Zeilen entsprechen 1:1 den Koerpern der Datei (Roadmap B1).\n")
L.append("**Scope:** DRIN: 8 Halter (H_INLINE in zwei Groessen) = 9 Dateien `halter_*.sc`, 14 Sonden-Platzhalter `sonde_*.sc` (je ein Koerper). DRAUSSEN: Alarmwaehler, Spannungswaechter, Batteriemonitor (Schaltschrank, kein Bauteil), `hahn_probe` (= H_HAHN), Messrechner/Platinen, Kabelwege (M10).\n")
L.append("**Herkunft-Kuerzel:** Q = aus gelesener Quelle (R39, `messstellen.json`), E = Handelsmass/Norm/eigene Rechnung, R = Rechenwert aus anderen Parametern, A = Annahme. **Alle Sondenmasse sind A:** `data/messstellen.json` enthaelt keine Abmessungen und die Hersteller-Datenblaetter sind nicht gelesen; Farbe nach vermuteter Hersteller-Erscheinung.\n")
L.append("## Uebersicht\n")
L.append("| Datei | Bauteil | Teilenummer | Koerper | Masse leer | Gesamt-Box (mm) | Stueck laut R39 |\n|---|---|---|---|---|---|---|")
for key, c in M.COMPS.items():
    mn, mx = MEAS[key]["box"]
    L.append(f"| `{key}.sc` | {c['id']}{' ' + c['variant'] if c.get('variant') else ''} {c['titel'] if c['kind'] == 'halter' else ''} | {c['nr']} | {len(c['teile'])} | {MEAS[key]['mass'] * 1000:.0f} g | {mx[0] - mn[0]:.0f} x {mx[1] - mn[1]:.0f} x {mx[2] - mn[2]:.0f} | {stueck(key)} |")
tot = sum(MEAS[k]["mass"] * stueck(k) for k in M.COMPS)
L.append(f"\nGesamt: {sum(stueck(k) for k in M.COMPS if M.COMPS[k]['kind'] == 'halter')} Halter und {sum(stueck(k) for k in M.COMPS if M.COMPS[k]['kind'] == 'sonde')} Sonden (Summe Stueck x Masse leer: {tot:.1f} kg); H_BOX = 7 Messknoten.\n")
L.append("## Halter\n")
for key, c in M.COMPS.items():
    if c["kind"] != "halter":
        continue
    p = {k: v[0] for k, v in c["params"].items()}
    mn, mx = MEAS[key]["box"]
    L.append(f"### {c['id']}{(' ' + c['variant']) if c.get('variant') else ''} {c['titel']} (`{key}.sc`, {c['nr']})\n")
    L.append(f"**Funktion:** {c['funktion']}\n")
    L.append(f"**Bauteil-KS:** {c['ks']}. **Gesamt-Box:** X {mn[0]:.1f} bis {mx[0]:.1f}, Y {mn[1]:.1f} bis {mx[1]:.1f}, Z {mn[2]:.1f} bis {mx[2]:.1f} mm. **Masse leer:** {MEAS[key]['mass'] * 1000:.0f} g. **Stueck:** {stueck(key)} (R39).\n")
    L.append("**Parameter:**\n\n| Parameter | Wert | Einheit | Herkunft |\n|---|---|---|---|")
    for k, v in c["params"].items():
        L.append(f"| `{k}` | {v[0]} | {v[1]} | {v[2]} |")
    L.append("\n**Teile (Zeile = Koerper der Datei):**\n\n| Nr | Koerper | Beschreibung | Werkstoff | Q/E/A | Masse |\n|---|---|---|---|---|---|")
    for i, t in enumerate(c["teile"], 1):
        L.append(f"| {i} | `{t[0]}` | {t[1]} | {t[2]} | {t[3]} | {MEAS[key]['bodies'][t[0]]:.0f} g |")
    L.append("\n**Ports:**\n\n| Name | Mass | Lage (Bauteil-KS) | Richtung | Koerper |\n|---|---|---|---|---|")
    for q in c["ports"](p):
        L.append(f"| {q[0]} | {q[1]} | x {q[2][0]:g}, y {q[2][1]:g}, z {q[2][2]:g} | {q[3]} | `{q[4]}` |")
    L.append(f"\n**Lebensmittel-/Wasserkontakt:** {LMH[c['id']]}.\n")
L.append("## Sonden-Platzhalter (ein Koerper je Typ, Masse Annahme)\n")
L.append("| Datei | Typ / Produkt (R39) | Platzhalter (Teile-Zeile = 1 Koerper) | Masse | Stueck (Pflicht/Zusatz) | Preis (R39) | Kalibrierung | Wartung / Standzeit | Kabel | Konfidenz R39 |\n|---|---|---|---|---|---|---|---|---|---|")
for key, c in M.COMPS.items():
    if c["kind"] != "sonde":
        continue
    t = D["sondentypen"][c["id"]]
    pf, zu = sstufe[c["id"]]
    L.append(f"| `{key}.sc` | `{c['id']}`: {t['name']} | {c['teile'][0][1]} ({c['teile'][0][2]}, A) | {MEAS[key]['mass'] * 1000:.0f} g | {sz[c['id']]} ({pf}/{zu}) | {preis(t)} | {t['kalibrierung']} | {t['wartung']}; {t['standzeit']} | {t['kabel_art']}, {t['adern']} Adern, {t['versorgung']} | {t['konfidenz']} |")
L.append("\n**Ports aller Sonden:** Messspitze/Anlage unten (x 0, y 0, z 0, -Z) und Kabel am oberen Ende (x 0, y 0, z = Hoehe, +Z) mit Adernzahl und Versorgung aus `messstellen.json`.\n")
L.append("**Lebensmittel-/Wasserkontakt und Alarm je Sonde:**\n\n| Typ | Wasser-/Lebensmittelkontakt | Alarmgrenzen (R39, aus den Messstellen) |\n|---|---|---|")
for key, c in M.COMPS.items():
    if c["kind"] == "sonde":
        L.append(f"| `{c['id']}` | {LM[c['id']]} | {alarm_text(c['id'])} |")
L.append("\n## Passung Sonde und Halter (Check)\n")
L.append("do_ind (d25) im Tauchrohr d40 (ID 36,2); ph, ec, temp_ds, do_mini in den Sondenstutzen d25/Bohrung 16 (H_ZELLE und Messzelle puffer_klein); level_float (d30) im Beruhigungsrohr d63 (ID 57); flow_12 deckt den Sensorsitz d30 ab; druck_schalter auf dem R1/4-Nippel; par (d30) und SCD41-Platine unter den Strahlungsschutz d90; Details in `scripts/workshop/check_messstellen.py` (`fit_checks`).\n")
L.append("## Montage (L4)\n")
L.append("1. Halter an der Messstelle setzen (Beckenrand, Rohr, Wand, Boden), Anbohrschellen auf das Rohr; 2. Sonden einsetzen, Kabel ins Messknoten-Gehaeuse (H_BOX) fuehren; 3. Messknoten per Trunk (RS-485 + 24 V) an die Zentrale; 4. Sonden kalibrieren (Intervalle oben), Alarmgrenzen einstellen (R39).\n")
L.append("**Werkzeug:** Akkuschrauber, Rohrschneider, PVC-Kleber, Bohrer, Klemmen; Kalibrierloesungen pH 4/7/10, EC-Standard, Luft fuer DO-Ein-Punkt.\n")
L.append("## Stueckliste-Zeile\n")
L.append("- Messstellen-Bauteile: " + ", ".join(f"{stueck(k)} x {M.COMPS[k]['id']}{(' ' + M.COMPS[k]['variant']) if M.COMPS[k].get('variant') else ''}" for k in M.COMPS if M.COMPS[k]["kind"] == "halter") + "; Sonden: " + ", ".join(f"{sz[M.COMPS[k]['id']]} x {M.COMPS[k]['id']}" for k in M.COMPS if M.COMPS[k]["kind"] == "sonde") + ".\n")
L.append("## Alternative lokale Fertigung\n")
L.append("Halter aus PVC-U-Rohr und Bloecken (Kunststoffhandel) selbst gebohrt und geklebt; Klemmen und Laschen aus Flachstahl 25 x 3 gebogen; Messknoten-Gehaeuse als Standard-IP65-Verteilerkasten; Sonden nach R39-Produktliste (Atlas Scientific) oder gleichwertig.\n")
L.append("## Pruefung\n")
L.append("- `scripts/workshop/check_messstellen.py` (alle 23 Komponenten, Ergebnis `renders/components/messstellen/check.txt`): Koerper = Teile-Zeilen, Namen, Masse > 0, Ports an den Koerpern mit Spitzen am Rand, Mass-/Volumenpruefungen je Halter, Sondenmasse = Volumen x Dichte, Passung Sonde/Halter, Abdeckung der Sondentypen, Interferenz 0.\n- Kein Pruefer-Lauf (Auftrag W35: Selbstcheck).\n")
L.append("## Offene Fragen\n")
for x in ("Hersteller-Abmessungen und -Werkstoffe der Sonden (Atlas-Datenblaetter, SCT-013, SCD41-Modul, PAR-Sensor) nicht gelesen: alle Sondenmasse und Farben Annahme; vor der Bestellung gegen Datenblatt pruefen",
          "Konformitaet fuer Lebensmittelkontakt: Rohre, Armaturen und Sondengehaeuse nur als Handelsware angenommen, keine Zulassung belegt",
          "H_INLINE: Rohrdurchmesser je Kante stehen nur in `leitungsnetz.json` (R40, nicht anfassen): d32 fuer flow_12 angenommen, d50 fuer flow_gross; Kanten d40/d25 brauchen Reduzierung (Bibliothek T70)",
          "Anbohrschelle (H_HAHN, H_DRUCK) als flache Platte: Rohrsattel und Dichtung nicht modelliert; Sattelform je Rohr-d offen",
          "Siebfeinheit >= 80 um (H_INLINE) und Schlitzbreite (H_BERUHIG) sind Masse, keine gepruefte Filterleistung",
          "Kabelwege und Kabellaengen der Sonden (Atlas-Kabel 1-3 m) liegen bei der Montage (M10); Verlaengerung nicht gelesen (R39)",
          "Statik des Sensor-Masts (1,7 m PVC d32 auf 100 x 100 Platte) nicht gerechnet; Wind und Berührung nicht betrachtet",
          "Messzelle puffer_klein: Sondenstutzen d25 passen zu ph, ec, do_mini, temp_ds (Bohrung 16); die endgueltige Belegung der 4 Stutzen liegt bei der Montage"):
    L.append(f"- {x}")
open(os.path.join(sc.ROOT, "docs", "parts", "messstellen.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

# ---- (3) descriptions
dpath = os.path.join(sc.ROOT, "data", "descriptions.json")
desc = json.load(open(dpath, encoding="utf-8"))
H = [k for k in M.COMPS if M.COMPS[k]["kind"] == "halter"]
S = [k for k in M.COMPS if M.COMPS[k]["kind"] == "sonde"]
halter_g = {"match": "^halter_", "titel": "Messstellen-Halter (8 Bauteile)", "was": "Standardhalter, an denen die Sonden der 67 Messstellen sitzen: Tauchrohr am Beckenrand, Beruhigungsrohr, Durchflusszelle, Einbaustück mit Vorfilter, Probenahmehahn, Druckstutzen, Sensor-Mast und Messknoten-Gehäuse.",
            "status": "Werkstatt W35 (R39, D65), check_messstellen alle Komponenten PASS",
            "ablauf": ["Der Halter nimmt die Sonde auf und bringt sie in den Wasserstrom, den Beckenrand-Bereich oder die Kuppelluft.", "Das Sondenkabel läuft zum Messknoten-Gehäuse (H_BOX) neben dem Halter; von dort geht ein Bus (RS-485 plus 24 V) zur Zentrale.", "Alarm- und Warngrenzen je Messgröße stehen bei den Sonden (R39)."],
            "aufbau": [{"t": "Halter", "p": [f"{M.COMPS[k]['id']}{(' ' + M.COMPS[k]['variant']) if M.COMPS[k].get('variant') else ''}: {M.COMPS[k]['titel']} ({stueck(k)} Stück)" for k in H]}],
            "masse": {f"{M.COMPS[k]['id']}{(' ' + M.COMPS[k]['variant']) if M.COMPS[k].get('variant') else ''}": f"{len(M.COMPS[k]['teile'])} Teile, {MEAS[k]['mass'] * 1000:.0f} g, Box {MEAS[k]['box'][1][0] - MEAS[k]['box'][0][0]:.0f} × {MEAS[k]['box'][1][1] - MEAS[k]['box'][0][1]:.0f} × {MEAS[k]['box'][1][2] - MEAS[k]['box'][0][2]:.0f} mm; Funktion: {M.COMPS[k]['funktion'].split(' (R39')[0]}" for k in H},
            "grenzen": "Handelsware (PVC-U, Stahl, Edelstahl) angenommen, keine Zulassung für Lebensmittelkontakt belegt; Anbohrschelle als flache Platte; Rohrdurchmesser je Messstelle bestimmt R40; Statik des Masts nicht gerechnet.",
            "quelle": "docs/parts/messstellen.md, docs/research/R39.md, data/messstellen.json", "rolle": "Messnetz der Anlage (R39): trägt 22 Pflicht- und 45 Zusatzmessstellen; Pflicht = Fischtod oder Anlagenschaden binnen Stunden (O₂, Temperatur, Wasserstand, Pumpenausfall, Strom, Luft)."}
sonde_g = {"match": "^sonde_", "titel": "Sonden-Platzhalter (14 Typen)", "was": "Je ein schlichter Körper pro Sondentyp in Maß und Farbe einer Hersteller-Sonde (Maße Annahme), damit die Montage jede Messstelle mit einem Bauteil besetzen kann.",
           "status": "Werkstatt W35 (R39, D65), Maße Annahme, check_messstellen PASS",
           "ablauf": ["Die Sonde misst eine Größe (O₂, pH, EC, Temperatur, Pegel, Durchfluss, Druck, Strom, CO₂, Licht, Leckage) und gibt ein Signal über Kabel an den Messknoten.", "Der Messknoten wertet aus; bei Überschreiten der Warn- oder Alarmgrenze meldet die Steuerung (lokal, Wähler, Software).", "Kalibrierung und Standzeit stehen im Blatt je Typ."],
           "aufbau": [{"t": "Typen", "p": [f"{M.COMPS[k]['id']}: {D['sondentypen'][M.COMPS[k]['id']]['name']} ({sz[M.COMPS[k]['id']]} Stück)" for k in S]}],
           "masse": {M.COMPS[k]["id"]: f"Funktion: {D['sondentypen'][M.COMPS[k]['id']]['technik']}; Alarmgrenze: {alarm_text(M.COMPS[k]['id'])}; Preis {preis(D['sondentypen'][M.COMPS[k]['id']])}; Kalibrierung: {D['sondentypen'][M.COMPS[k]['id']]['kalibrierung']}; Platzhalter {M.COMPS[k]['teile'][0][1]}" for k in S},
           "grenzen": "Alle Sondenmaße und Farben sind Annahmen (keine Abmessungen in R39, Datenblätter nicht gelesen); Konformität der Gehäuse für Lebensmittelkontakt nicht belegt; Kalibrierintervalle Herstellerangaben bzw. Annahme [A].",
           "quelle": "docs/parts/messstellen.md, docs/research/R39.md, data/messstellen.json (sondentypen, alarmgrenzen)", "rolle": "Messnetz der Anlage (R39): 72 Sonden und Fühler an 67 Messstellen; Alarm in drei Stufen (lokal, GSM-Wähler, Software)."}
desc["bauteile"] = [b for b in desc["bauteile"] if b["match"] not in ("^halter_", "^sonde_")]
i = next(i for i, b in enumerate(desc["bauteile"]) if b["match"] == "^puffer_klein")
desc["bauteile"][i + 1:i + 1] = [halter_g, sonde_g]
json.dump(desc, open(dpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
first = lambda stem: next(b["match"] for b in desc["bauteile"] if re.search(b["match"], stem))
bad = [k for k in M.COMPS if first(k) != ("^halter_" if k.startswith("halter_") else "^sonde_")]
print("descriptions: falsche Treffer", bad)
print("Blatt", os.path.join("docs", "parts", "messstellen.md"), "Zeilen", len(L))
