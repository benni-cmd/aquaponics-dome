"""N-STUECKLISTE 1a: Typ-Index und Artikelliste aus den Koerpern aller Komponenten-.sc (Preise leer).

Aufruf:
  python -X utf8 scripts/bom_artikel.py --ergaenzen # misst nur neue und seit dem Cache geaenderte .sc nach
  python -X utf8 scripts/bom_artikel.py            # liest data/bom_koerper.json (Cache), schreibt data/katalog.json
  python -X utf8 scripts/bom_artikel.py --messen   # misst zuerst alle designs/components/*.sc neu (rund 15 min)

Eingaben : designs/components/*.sc (ueber solidcraft-cli eval), viewer/instances.json (Instanzzahl je Definition)
Ausgaben : data/bom_koerper.json (Messcache mit Modellstempel), data/katalog.json (additiv: typen, artikel,
           artikel_ausnahmen, artikel_stempel; Pilot-Schluessel bleiben unveraendert)
Regel    : Kaufmengen kommen aus den Koerpern je Bauteil x Instanzen, nie aus der Instanzzahl allein (netztopf/salatkopf).
Preise, Links, Lieferung gehoeren NICHT hierher (data/beschaffung/<klasse>.json, Paket 2).
"""
import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from collections import OrderedDict, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bom_benennung  # noqa: E402
import variante as V  # noqa: E402

ROOT = os.environ.get("BOM_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # BOM_ROOT: Testkopie (check_bom.py)
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
COMP_DIR = os.path.join(ROOT, "designs", "components")
CACHE = os.path.join(ROOT, "data", "bom_koerper.json")
KATALOG = os.path.join(ROOT, "data", "katalog.json")
INST = V.pfad("instances", root=ROOT)

TYPEN = OrderedDict([
    ("PRF", "Stahlprofil (Rechteck-, Vierkantrohr, Rund- und Vollmaterial)"),
    ("WNK", "Winkel und Flachstahl, Halter"),
    ("BLE", "Blech, Platte, Lochblech, Zuschnitt"),
    ("ROH", "PVC-U-Rohr (Meterware)"),
    ("FIT", "Fitting (Bogen, T, Reduzierung, Kupplung, Stutzen, Kappe)"),
    ("ARM", "Armatur (Kugelhahn, Ventil, Bulkhead, Durchfuehrung)"),
    ("SCH", "Schlauch, Schelle, Tuelle"),
    ("SRB", "Schraube, Mutter, Scheibe, Bolzen"),
    ("BEH", "Behaelter und Becken"),
    ("PMP", "Pumpe und Geblaese"),
    ("MES", "Messtechnik (Sonden, Sensoren)"),
    ("ELE", "Elektrik (Schaltschrank, Kabel, Hutschiene)"),
    ("FOL", "Folie, Plane, Dichtband, Dichtung"),
    ("GEW", "Gewebe und Netz"),
    ("TOP", "Topf und Substrat"),
    ("SON", "Sonderteil (Eigenbau mit Rohmaterial als Kaufteil, Tuer, Haut, Knoten)"),
    ("MAT", "Material nach Menge (Gitterrost, Teichfolie; Zuschnitt oder Flaeche)"),
    ("BET", "Beton und Erdarbeit (nicht in der Einkaufsliste, Entscheidung Orchestrator 04.11.2026)"),
])
PVC_D = [16, 20, 25, 32, 40, 50, 63, 75, 90, 110, 125, 160]
LAGER = {"PRF": [3000, 3500, 4000, 6000, 6500, 7000], "WNK": [3000, 6000], "ROH": [5000]}  # [A] Handel, strut_cutting.STOCK_MM


# ------------------------------------------------------------------ Messung
def modellstempel():
    h = hashlib.sha256()
    for f in sorted(glob.glob(os.path.join(COMP_DIR, "*.sc"))):
        h.update(os.path.basename(f).encode())
        h.update(open(f, "rb").read())
    beet = hashlib.sha256()
    for f in sorted(glob.glob(os.path.join(COMP_DIR, "ibc_beet*.sc"))):
        beet.update(open(f, "rb").read())
    built = json.load(open(INST, encoding="utf-8")).get("built")
    return {"instances_built": built, "sc_sha256": h.hexdigest()[:16], "ibc_beet_sha256": beet.hexdigest()[:16],
            "anzahl_sc": len(glob.glob(os.path.join(COMP_DIR, "*.sc")))}


def messen(nur=None):
    """nur: Menge von Komponentennamen (Teilmessung, ergaenzt den Cache); None = alle"""
    import tempfile
    tmp = tempfile.mkdtemp()
    res = json.load(open(CACHE, encoding="utf-8"))["komponenten"] if nur is not None else {}
    for f in sorted(glob.glob(os.path.join(COMP_DIR, "*.sc"))):
        comp = os.path.basename(f)[:-3]
        if nur is not None and comp not in nur:
            continue
        out = os.path.join(tmp, comp + ".json")
        subprocess.run([CLI, "eval", f, "--json-out", out], capture_output=True, text=True)
        if not os.path.exists(out):
            res[comp] = {"n": 0, "fehler": "eval ohne Ausgabe", "bodies": []}
            continue
        bs = json.load(open(out, encoding="utf-8")).get("bodies", [])
        res[comp] = {"n": len(bs), "bodies": [{
            "name": b.get("name"), "material": b.get("material"), "mass_g": round(b.get("mass_g") or 0, 3),
            "bbox_min": [round(x, 2) for x in b["bbox"]["min"]], "bbox_max": [round(x, 2) for x in b["bbox"]["max"]]}
            for b in bs]}
        os.remove(out)
    json.dump({"stempel": modellstempel(), "komponenten": res}, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    return res


# ------------------------------------------------------------------ Hilfen
def dims(b):
    return sorted(round(b["bbox_max"][i] - b["bbox_min"][i]) for i in range(3))


def snap_d(x):
    return min(PVC_D, key=lambda d: abs(d - x))


def lnum(x):
    return str(int(round(x)))


class Art:
    """Ergebnis der Zuordnung eines Koerpers."""
    def __init__(self, aid, typ, bez, einheit="Stk", art="a", werkstoff=None, mass=None, menge=1.0, teil_von=False, flag=None):
        self.id, self.typ, self.bez, self.einheit, self.art = aid, typ, bez, einheit, art
        self.werkstoff, self.mass, self.menge, self.teil_von, self.flag = werkstoff, mass or {}, menge, teil_von, flag


def profil_artikel(b, werkstoff="Stahl verzinkt", tag="st"):
    """Profil aus dem Querschnitt der beiden kleinen Bbox-Masse; Wand aus der Masse (Vollmaterial/Rund/Hohlprofil)."""
    d = dims(b)
    a, c, L = d[0], d[1], d[2]
    dens = 7.85e-3  # g/mm3
    A_meas = b["mass_g"] / (dens * L) if L else 0
    if a <= 0 or c <= 0:
        return None
    if a == c and abs(A_meas - math.pi / 4 * a * a) / (math.pi / 4 * a * a) < 0.04:
        aid, bez, norm = f"PRF-{tag}-rund{a}", f"Rundstahl {a} mm, {werkstoff}", "Rund Vollmaterial [E]"
    elif abs(A_meas - a * c) / (a * c) < 0.04:
        aid, bez, norm = f"PRF-{tag}-voll{a}x{c}", f"Vierkant-/Flachstahl voll {a}x{c} mm, {werkstoff}", "Vollmaterial [E]"
    else:
        # Hohlprofil: A = 2(a+c)t - 4t^2
        t = None
        for tt in [x / 2 for x in range(2, 21)]:
            if abs(2 * (a + c) * tt - 4 * tt * tt - A_meas) / max(A_meas, 1) < 0.12:
                t = tt
                break
        if t is None:
            t = round((a + c - math.sqrt(max((a + c) ** 2 - A_meas, 0))) / 2 * 2) / 2 or 3
        ts = str(t).rstrip("0").rstrip(".") if "." in str(t) else str(t)
        aid, bez, norm = f"PRF-{tag}-rr{a}x{c}x{ts}", f"{'Vierkantrohr' if a == c else 'Rechteckrohr'} {a}x{c}x{ts} mm, {werkstoff}", "Wand aus Modellmasse gerechnet [E]"
    return Art(aid, "PRF", bez, "m", "a", werkstoff, {"querschnitt_mm": [a, c], "norm_hinweis": norm}, menge=L / 1000.0)


def pvc_stueck(typ, prefix, bez, b, einheit="Stk", d=None, **kw):
    dd = d or snap_d(dims(b)[0])
    return Art(f"{typ}-{prefix}-d{dd}", typ, f"{bez} d{dd}", einheit, "a", "PVC-U", {"durchmesser_mm": dd}, **kw)


# Kugelhahn-Nennweite nach Bauteil (Modellmasse nicht eindeutig) [A], Quelle: docs/research/R52, Bauteilblaetter
HAHN_D = {("feinfilter", "kugelhahn_ablass"): 40, ("feinfilter", "kugelhahn_spuelen"): 25, ("puffer_ibc", "kugelhahn"): 63,
          ("puffer_station", "kugelhahn"): 63, ("tank_gross", "kugelhahn"): 50, ("tank_gross_t3", "kugelhahn"): 50,
          ("tank_klein", "kugelhahn"): 40, ("halter_hahn", "kugelhahn"): 20, ("halter_zelle", "absperrhahn"): 20}


# ------------------------------------------------------------------ Leitungsteile (lt_*): ein Artikel je Komponente
def classify_lt(comp, bodies):
    m = re.match(r"lt_([a-z0-9]+(?:_[a-z]+)?)_?(.*)$", comp)
    parts = comp.split("_")
    kind = parts[1]
    rest = "_".join(parts[2:])
    lon = max(bodies, key=lambda x: x["mass_g"])
    if kind == "rohr":
        dd = int(re.match(r"d(\d+)", rest).group(1))
        return Art(f"ROH-pvcu-d{dd}", "ROH", f"PVC-U-Druckrohr d{dd} (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": dd},
                   menge=dims(lon)[2] / 1000.0)
    names = {"bogen90": ("FIT", "bogen90", "PVC-U-Bogen 90 Grad"), "bogen45": ("FIT", "bogen45", "PVC-U-Bogen 45 Grad"),
             "t": ("FIT", "t", "PVC-U-T-Stueck"), "kupplung": ("FIT", "kupplung", "PVC-U-Kupplung (Muffe)"),
             "kappe": ("FIT", "kappe", "PVC-U-Kappe"), "reduzierung": ("FIT", "red", "PVC-U-Reduzierung"),
             "kugelhahn": ("ARM", "kugelhahn", "PVC-U-Kugelhahn"), "rueckschlagventil": ("ARM", "rsv", "PVC-U-Rueckschlagventil"),
             "klemme": ("SCH", "rohrschelle", "Rohrschelle (Klemme, Stahl)"), "schelle": ("SCH", "rohrschelle-vk", "Rohrschelle VK"),
             "verteiler": ("FIT", "verteiler", "PVC-U-Verteiler"), "uebergang": ("FIT", "uebergang-pe-pvc", "Uebergang PE auf PVC-U"),
             "kabeleinfuehrung": ("ARM", "kabeleinfuehrung", "Kabeleinfuehrung"), "schacht": ("SON", "schacht-kugelhahn", "Schacht fuer Kugelhahn (PE-HD)"),
             "schlauch": ("SCH", "schlauch", "Schlauch"), "schlauchbogen90": ("SCH", "schlauchbogen90", "Schlauchbogen 90 Grad"),
             "schlauchschelle": ("SCH", "schlauchschelle", "Schlauchschelle"), "schnellkupplung": ("ARM", "schnellkupplung", "Schnellkupplung"), "sammler": ("FIT", "sammler", "Sammelleitung (Sammler)"), "leerrohr": ("ROH", "leerrohr", "Leerrohr (Kabelschutz)")}
    if kind not in names:
        return None
    typ, pre, bez = names[kind]
    suffix = rest
    if kind == "schacht":
        suffix = "d63"
    if kind == "leerrohr":
        # leerrohr_dn50 | leerrohr_bogen90_dn50 | leerrohr_t_dn50 | leerrohr_red_dn100_dn50
        sub = rest
        if sub.startswith("bogen"):
            typ, pre, bez = "FIT", "leerrohr-" + sub.split("_")[0], "Leerrohr-Bogen " + sub.split("_")[0][5:] + " Grad"
        elif sub.startswith("t_"):
            typ, pre, bez = "FIT", "leerrohr-t", "Leerrohr-T-Stueck"
        elif sub.startswith("red"):
            typ, pre, bez = "FIT", "leerrohr-red", "Leerrohr-Reduzierung"
        suffix = sub.split("_", 1)[1] if "_" in sub and not sub.startswith("dn") else sub
        if typ == "ROH":
            return Art(f"ROH-leerrohr-{suffix}", "ROH", f"Leerrohr {suffix.upper()} (Kabelschutz, Meterware)", "m", "a", "PVC/PP",
                       {"nennweite": suffix}, menge=dims(lon)[2] / 1000.0)
    if kind == "schlauch":
        return Art(f"SCH-schlauch-{rest.split('_L')[0]}", "SCH", f"Schlauch {rest.split('_L')[0].upper()} (Meterware)", "m", "a", "PVC/PE",
                   {"nennweite": rest.split('_L')[0]}, menge=dims(lon)[2] / 1000.0)
    wst = {"ARM": "PVC-U", "FIT": "PVC-U", "SCH": "Stahl" if kind in ("klemme", "schelle") else "Kunststoff"}.get(typ)
    return Art(f"{typ}-{pre}-{suffix}" if suffix else f"{typ}-{pre}", typ, f"{bez} {suffix}".strip(), "Stk", "a", wst, {"groesse": suffix})


# ------------------------------------------------------------------ Koerper -> Artikel (alle anderen Komponenten)
def ausnahme(comp, b):
    n, m = (b["name"] or ""), (b["material"] or "")
    if m == "Salat" or comp == "salatkopf":
        return "Pflanze (Salat), nicht kaufbar"
    if comp.startswith("mensch_referenz"):
        return "Massfigur, kein Bauteil"
    if comp == "erdflaeche":
        return "Aushub und Erde (Entscheidung 04.11.2026)"
    if comp == "fundamentring" or m.startswith("Beton C"):
        return "Beton nach Menge (Entscheidung 04.11.2026)"
    if m == "Wasser" or re.search(r"(^|_)wasser( \(\d+\))?$", n.lower()):
        return "Wasserkoerper, kein Bauteil"
    return None


def classify(comp, b):
    n = (b["name"] or "")
    nl = re.sub(r" \(\d+\)", "", n.lower())
    m = b["material"] or ""
    d = dims(b)
    stahl = m.startswith("Stahl")
    # unbenannte Koerper und Schrauben: Benennung nach Gestalt in zuordnen() (bom_benennung, data/bom_regeln.json)
    # ---- Knoten
    if comp.startswith("knoten"):
        if nl == "knotenkugel":
            return Art("SON-knotenkugel-d100", "SON", "Knotenkugel d100, Stahl (Verbindungsstueck, N-STATIK W43 offen)", art="c", werkstoff="Stahl Knoten")
        if nl.startswith("arm_"):
            return Art("SON-knotenarm-23x23x3", "SON", "Steckarm 23x23x3 am Knoten (Verbindungsstueck, N-STATIK W43 offen)", art="c", werkstoff="Stahl Knoten")
        if nl == "ankerlasche":
            return Art("SON-ankerlasche", "SON", "Ankerlasche am Knoten (Stahl, Zuschnitt)", art="c", werkstoff="Stahl Knoten")
    if comp == "fundamentanker":
        if nl == "ankerplatte":
            return Art("BLE-platte-250x250x15", "BLE", "Ankerplatte 250x250x15 mm, Stahl", art="a", werkstoff="Stahl Anker")
        if nl.startswith("gabel"):
            return Art("SON-ankergabel-80x140", "SON", "Gabelkopf 80x140 (Fundamentanker, Stahl, Zuschnitt)", art="c", werkstoff="Stahl Anker")
    # ---- Streben (Vierkantrohr 30x30x3, N-MODELL-KOMPLETT Schritt 2)
    if comp in ("strebe_a", "strebe_b"):
        return Art("PRF-st-strebe30x30", "PRF", "Strebenprofil 30x30 (Kuppelstrebe, Profil und Wand offen: N-STATIK V1/V2c)", "m", "a", "Stahl verzinkt",
                   {"querschnitt_mm": [30, 30]}, menge=d[2] / 1000.0)
    # ---- Tuer, Haut, Huelle
    if comp.startswith("huelle_folie"):
        return Art("FOL-pe-plane", "FOL", "PE-Planenbahn (Huelle, Zuschnitt je Feld, Flaeche aus Modell)", "m2", "b", "PE Folie", menge=(d[2] * d[1]) / 1e6)
    if comp.startswith("haut_paneel"):
        return Art("SON-polycarbonat-paneel", "SON", "Polycarbonat-Paneel 8 mm (Zuschnitt je Feld)", "Stk", "c", "Polycarbonat", {"dicke_mm": 8})
    if comp == "haut_profil":
        return Art("PRF-alu-haut-profil", "PRF", "Alu-Kappenprofil der Haut", "m", "a", "Aluminium", menge=d[2] / 1000.0)
    if comp == "keilschiene":
        return {"schaumband": Art("FOL-epdm-schaumband", "FOL", "EPDM-Schaumband 25x3", "m", "a", "EPDM", menge=d[2] / 1000.0),
                "kanal": Art("PRF-alu-keilschiene", "PRF", "Alu-Keilschiene (Kanal 25x15)", "m", "a", "Aluminium", menge=d[2] / 1000.0),
                "federdraht": Art("SON-federdraht-d2", "SON", "Federstahldraht d2 (Keilschiene)", "m", "a", "Federstahl", menge=d[2] / 1000.0)}.get(nl)
    if comp.startswith("tuer_zarge"):
        return {"aufsatzrahmen": Art("SON-zarge-aufsatzrahmen", "SON", "Alu-Aufsatzrahmen Tuerzarge (Planenausschnitt)", "Stk", "c", "Aluminium Zarge"),
                "dichtband": Art("FOL-epdm-dichtband-zarge", "FOL", "EPDM-Dichtband Zarge", "m", "a", "EPDM", menge=d[2] / 1000.0),
                "klemmleiste": Art("PRF-alu-klemmleiste", "PRF", "Alu-Klemmleiste Zarge", "m", "a", "Aluminium Zarge", menge=d[2] / 1000.0)}.get(nl)
    if comp == "tuer_komplett" or comp == "tuer":
        if "dichtung" in nl:
            return Art("FOL-epdm-tuerdichtung", "FOL", "EPDM-Tuerdichtung", "m", "a", "EPDM", menge=max(d) / 1000.0)
        if "tuerblatt" in nl or nl.endswith("blatt"):
            return Art("SON-tuerblatt-1000x2000", "SON", "Tuerblatt Sandwich 1000x2000x40", "Stk", "a", "Tuerblatt Sandwich")
        if "scharnier" in nl:
            return Art("SON-tuerscharnier", "SON", "Tuerscharnier (Zargenlasche, Blattlasche, Bolzen)", "Stk", "a", "Stahl verzinkt",
                       teil_von=not nl.endswith("zargenlasche") and "scharnier" in nl and "tuer_komplett" == comp, menge=1)
        if re.search(r"rosette|druecker|griff", nl):
            return Art("SON-tuerdruecker", "SON", "Tuerdruecker mit Rosette", "Stk", "a", "Stahl verzinkt",
                       teil_von=not (nl in ("druecker_hebel_aussen", "druecker_hebel_innen", "griff")), menge=1)
        if comp == "tuer_komplett" and nl.startswith("anschlag"):
            return Art("WNK-flach-14x3", "WNK", "Flachstahl 14x3 (Tuer-Anschlag)", "m", "a", "Stahl verzinkt", menge=max(d) / 1000.0)
        if comp == "tuer_komplett" and nl in ("schwelle", "sturz", "pfosten_links", "pfosten_rechts"):
            return profil_artikel(b)
        if comp == "tuer":
            return Art("SON-tuer-modellvariante", "SON", "Tuer (Alt-Modell, nicht verbaut) " + n, flag="altmodell")
    # ---- IBC-Puffer: Gebinde als EIN Artikel, Gitterkaefig/Palette als Teil
    if comp in ("puffer_ibc", "puffer_station") and (re.match(r"(rahmen_|pfosten_|stab_)", nl) or m in ("HDPE Palette",) or nl in ("blase", "deckel")):
        base = nl == "blase"
        return Art("BEH-ibc-1000l", "BEH", "IBC-Container 1000 l mit Gitterkaefig und Palette (Puffer)", "Stk", "a", "PE/Stahl/HDPE",
                   {"volumen_l": 1000}, teil_von=not base)
    # ---- Behaelter
    if m == "PE Tank" and (nl == "tank" or (comp == "schlammfass" and nl == "fass")):  # W37-1 Schlammfass 220 l
        return Art(f"BEH-tank-pe-{lnum(d[0])}x{lnum(d[2])}", "BEH", f"PE-Tank {lnum(d[0])} mm Durchm., {lnum(d[2])} mm hoch (Kegelboden/Absetzer)", "Stk", "a", "PE", {"bbox_mm": d})
    if m == "PE Tank" and nl == "deckel":
        return Art(f"BEH-tank-pe-{lnum(d[2])}-deckel", "BEH", f"PE-Tankdeckel {lnum(d[2])} mm", "Stk", "a", "PE", {})
    if comp == "beet_sumpf" and m == "PE Tank" and nl == "schachtaufsatz":  # W37-1 T92, Aufsatz Oe 600 x 200 [A]
        return Art("BEH-pe-schachtaufsatz-600x200", "BEH", "PE-Schachtaufsatz (Dom) Oe 600 x 200 mm fuer Tank [A]", "Stk", "a", "PE", {"bbox_mm": d})
    if comp == "beet_sumpf":  # W37-1 T92: Pumpen, RSV, Schwimmer, Entlueftung, Verschraubung (Bauteilblatt beet_sumpf, Annahmen [A])
        if nl.startswith("pumpe_"):
            return Art("PMP-teichpumpe-5300", "PMP", "Teichpumpe 5300 l/h, 60 W, Hmax 2,8 m (Beet-Sumpf, Fabrikat offen) [A]", "Stk", "a", None, {})
        if nl.startswith("rueckschlagventil_"):
            return Art("ARM-rsv-d40", "ARM", "PVC-U-Rueckschlagventil d40", "Stk", "a", "PVC-U", {"groesse": "d40"})
        if nl == "durchfuehrung_foerder":
            return Art("ARM-bulkhead-d50", "ARM", "PVC-U-Bulkhead d50 (Tankverbinder, Tankdurchfuehrung)", "Stk", "a", "PVC-U", {"durchmesser_mm": 50})
        if nl == "schwimmerstange":
            dd = snap_d(d[0])
            return Art(f"ROH-pvcu-d{dd}", "ROH", f"PVC-U-Druckrohr d{dd} (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": dd}, menge=d[2] / 1000.0)
        if nl.startswith("schwimmer_"):
            return Art("MES-schwimmerschalter", "MES", "Schwimmerschalter (Niveau AUS/EIN/ALARM, Fabrikat offen) [A]", "Stk", "a", None, {})
        if nl == "entlueftung":
            return Art("FIT-entlueftung-d32", "FIT", "Entlueftung d32 (PVC-U, mit Insektengitter-Kappe) [A]", "Stk", "a", "PVC-U", {"durchmesser_mm": 32})
        if nl.startswith("kabelverschraubung_"):
            return Art("ELE-kabelverschraubung-m25", "ELE", "Kabelverschraubung M25 (PA)", "Stk", "a", "PA", {})
    if comp == "beet_sumpf" and nl == "zulauf_tankverbinder":  # Tankverbinder d50 durch die Tankwand (Bauteilblatt beet_sumpf)
        return Art("ARM-bulkhead-d50", "ARM", "PVC-U-Bulkhead d50 (Tankverbinder, Tankdurchfuehrung)", "Stk", "a", "PVC-U", {"durchmesser_mm": 50})
    if m == "HDPE weiss" and nl == "wanne":
        return Art("BEH-ibc-beetwanne", "BEH", "IBC-Beetwanne HDPE (aus IBC geschnitten, Laenge je Beet)", "Stk", "b", "HDPE weiss", {"bbox_mm": d})
    if m == "PP grau" and nl == "siebboden":
        return Art("BLE-pp-siebboden-beet", "BLE", "PP-Siebboden 8 mm (Zuschnitt je Beet)", "Stk", "c", "PP grau", {"dicke_mm": 8})
    if m == "PP grau" and nl == "stuetze":
        return Art("SON-pp-stuetze-60x60", "SON", "PP-Stuetze 60x60 (Beetboden, Hoehe je Beet)", "Stk", "c", "PP grau")
    if m == "Medium Blaehton":
        return Art("TOP-blaehton", "TOP", "Blaehton-Substrat 8-16 mm (Beetfuellung)", "m3", "a", "Blaehton", menge=(d[0] * d[1] * d[2]) / 1e9)
    if m == "Biomedium":
        return Art("TOP-biomedium", "TOP", "Biomedium (Biofilter-Fuellkoerper)", "m3", "a", "Kunststoff", menge=(d[0] * d[1] * d[2]) / 1e9)
    if m == "V2A Lochblech":
        return Art("BLE-v2a-lochblech-medienschutz", "BLE", "Edelstahl-Lochblech 1,5 mm RV5-8, Medienschutz-Zylinder 110x320", "Stk", "b", "Edelstahl 1.4301")
    if comp == "becken_dritt_klein" and nl.endswith("wanne"):
        return Art("BEH-drittbecken-klein", "BEH", "Drittbecken klein (Wanne 920x920x1055)", "Stk", "b", "Beton", {"bbox_mm": d}, flag="werkstoff beton fraglich")
    if comp in ("becken_dritt", "zweitbecken", "pool_zentral") and re.search(r"t\d*_(drittbecken|zweitbecken|zentraltank)$", nl):
        nm = {"becken_dritt": "Drittbecken", "zweitbecken": "Zweitbecken", "pool_zentral": "Zentralpool"}[comp]
        return Art(f"BEH-{comp.replace('_','-')}", "BEH", f"{nm} (Eigenbau/Sonderanfertigung, Masse aus Modell)", "Stk", "c", None, {"bbox_mm": d})
    if comp == "pool_zentral" and "stutzen" in nl:
        return Art("ARM-bulkhead-pool", "ARM", "Pool-Durchfuehrung d63 (Stutzen Pool-Wand)", "Stk", "a", "PVC-U", {"durchmesser_mm": 63})
    if comp == "schaltschrank":
        return Art("ELE-schaltschrank-500x800x1200", "ELE", "Schaltschrank 500x800x1200 mm (leer, Ausruestung offen)", "Stk", "a")
    if comp == "pflanztisch":
        return Art("SON-pflanztisch-platte", "SON", "Pflanztischplatte (Alt-Modell, nicht verbaut)", flag="altmodell")
    if comp == "zulaufrohr":
        return Art("ROH-pvcu-d160", "ROH", "PVC-U-Druckrohr d160 (Zulaufrohr, Meterware, Laenge aus Bbox [E])", "m", "a", "PVC-U", {"durchmesser_mm": 160}, menge=d[2] / 1000.0, flag="bbox_laenge")
    if comp == "netztopf":
        return Art("TOP-netztopf-64", "TOP", "Netztopf PP 64 mm (Pflanzkorb, Stueckzahl aus Instanzen)", "Stk", "a", "PP", {"durchmesser_mm": 64})
    if nl == "belueftungsgitter":
        return Art("SON-belueftungsgitter-460", "SON", "Belueftungsgitter 460x460 (PVC, Tankdeckel)", "Stk", "c", "PVC grau Tank")
    if comp == "puffer_station" and nl in ("mess_tellerarm", "mess_haltearm"):
        return profil_artikel(b)
    # ---- Pumpen
    if comp.startswith("pumpe_"):
        gr = comp.split("_")[1]
        if nl == "motor":
            return Art(f"PMP-pumpe-{gr}", "PMP", f"Kreiselpumpe {gr} (Motor, Kopf, Sockel; Foerderstrom/Foerderhoehe offen)", "Stk", "a", None, {"motor_mm": d})
        if nl in ("pumpenkopf", "saugstutzen", "druckstutzen", "pumpensockel", "kabel", "stecker"):
            return Art(f"PMP-pumpe-{gr}", "PMP", f"Kreiselpumpe {gr}", "Stk", "a", None, {}, teil_von=True)
        if nl == "montagetafel":
            return Art(f"BLE-pp-tafel-{lnum(d[2])}x{lnum(d[1])}x{lnum(d[0])}", "BLE", f"PP-Montagetafel {lnum(d[2])}x{lnum(d[1])}x{lnum(d[0])} (Zuschnitt)", "Stk", "c", "PP Tafel")
        if nl in ("konsole",) or "standwinkel" in nl:
            return Art("WNK-pumpenkonsole", "WNK", "Pumpenkonsole/Standwinkel (Stahl, Zuschnitt)", "Stk", "c", "Stahl Pumpe")
    # ---- Sonden
    if comp.startswith("sonde_"):
        return Art(f"MES-{comp[6:].replace('_', '-')}", "MES", f"Sonde {comp[6:]} (Typ und Fabrikat offen: docs/research/R39)", "Stk", "a", None, {"bbox_mm": d})
    # ---- Dosierung, Kanister, Messzelle (puffer_klein/station)
    if m == "Kanister HDPE" and nl.startswith("kanister") and "deckel" not in nl:
        return Art("BEH-kanister-hdpe", "BEH", "HDPE-Kanister (Dosiervorrat)", "Stk", "a", "HDPE")
    if "kanister" in nl and "deckel" in nl:
        return Art("BEH-kanister-hdpe", "BEH", "HDPE-Kanister (Dosiervorrat)", "Stk", "a", "HDPE", teil_von=True)
    if m == "Pumpe Schlauch":
        return Art("PMP-dosierpumpe", "PMP", "Dosierpumpe (Schlauchpumpe)", "Stk", "a", None, {}, teil_von=(comp == "puffer_klein" and nl == "pumpe_eisen"))
    if m == "HDPE blau" and nl == "fass":
        return Art("BEH-fass-hdpe", "BEH", "HDPE-Fass 500 mm (Mischfass)", "Stk", "a", "HDPE blau")
    if m == "HDPE blau":
        return Art("BEH-fass-hdpe", "BEH", "HDPE-Fass 500 mm (Mischfass)", "Stk", "a", "HDPE blau", teil_von=True)
    if m == "Acryl klar" and comp in ("puffer_klein",):
        return Art("BEH-messzelle-acryl", "BEH", "Messzelle Acryl 315x315x260", "Stk", "c", "Acryl klar", teil_von=("deckel" in nl))
    if m == "Acryl klar" and comp == "halter_box":
        return Art("BEH-halter-box-gehaeuse", "BEH", "Anschlussbox PS 200x150x100 mit Acryldeckel", "Stk", "a", "PS/Acryl", teil_von=("deckel" in nl))
    if m == "PS grau":
        return Art("BEH-halter-box-gehaeuse", "BEH", "Anschlussbox PS 200x150x100 mit Acryldeckel", "Stk", "a", "PS/Acryl")
    if m == "PP schwarz" and nl == "blende":
        return Art("BLE-pp-blende-290x260", "BLE", "PP-Blende 290x260x3 (Messzelle)", "Stk", "c", "PP schwarz")
    if m == "Becher PP":
        return Art("BEH-messbecher-pp", "BEH", "Messbecher PP 160x310", "Stk", "a", "PP")
    if m == "Platine gruen":
        return Art("MES-co2-scd41", "MES", "CO2-Sensor SCD41 (Platine)", "Stk", "a")
    if m == "Kanal PVC" and nl.startswith("sondenhalter"):
        return Art("SON-sondenhalter-36", "SON", "Sondenhalter 36x36x40 (PVC, Eigenbau/Stuetze)", "Stk", "c", "Kanal PVC")
    if m == "Kanal PVC" and nl == "kabelkanal":
        return Art("ELE-kabelkanal-30x60", "ELE", "Kabelkanal PVC 30x60", "m", "a", "PVC", menge=d[2] / 1000.0)
    if m == "Sonde":
        return Art(f"MES-{re.sub(r'[^a-z0-9]+','-',nl.replace('sonde_',''))}", "MES", f"Sonde {n.replace('Sonde_','')} (Stationsmessplatz)", "Stk", "a", None, {"bbox_mm": d}, teil_von=False)
    # ---- Halter (Messstellen): PVC-Teile einzeln
    # ---- Kunststoff-Rohr-/Fitting-Teile
    if m.startswith("PVC") or m in ("PP grau", "PP weiss", "PA schwarz", "Ventil blau", "Default", "Kanal PVC", "PVC-U weiss", "LT pvc"):
        if "hebel" in nl and "hahn" in nl or nl == "hahn_hebel" or nl.endswith("hebel"):
            pass
    return None


def classify_late(comp, b):
    """zweiter Durchlauf: Stahl, PVC, Rinnen, Kleinteile."""
    n = (b["name"] or "")
    nl = re.sub(r" \(\d+\)", "", n.lower())
    m = b["material"] or ""
    d = dims(b)
    key = (comp, nl)
    # Kugelhaehne
    if nl in ("kugelhahn", "kugelhahn_ablass", "kugelhahn_spuelen", "absperrhahn") or (comp, nl) in HAHN_D:
        dd = HAHN_D.get((comp, nl), HAHN_D.get((comp, "kugelhahn"), 25))
        return Art(f"ARM-kugelhahn-d{dd}", "ARM", f"PVC-U-Kugelhahn d{dd}", "Stk", "a", "PVC-U", {"durchmesser_mm": dd})
    if nl in ("hahn_hebel", "kugelhahn_hebel", "kugelhahn_spuelen_hebel"):
        dd = HAHN_D.get((comp, "kugelhahn"), HAHN_D.get((comp, "kugelhahn_ablass" if "spuelen" not in nl else "kugelhahn_spuelen"), 25))
        return Art(f"ARM-kugelhahn-d{dd}", "ARM", f"PVC-U-Kugelhahn d{dd}", "Stk", "a", "PVC-U", {"durchmesser_mm": dd}, teil_von=True)
    # Rinnen
    if nl.startswith("rinnenprofil"):
        return Art("PRF-pvcu-rinne-130x100", "PRF", "NFT-Rinnenprofil PVC-U 130x100 (Meterware, Lagerlaenge offen)", "m", "a", "PVC-U weiss", {"querschnitt_mm": [100, 130]}, menge=d[2] / 1000.0)
    if nl.startswith("kappezulauf"):
        return Art("FIT-rinne-kappe-zulauf", "FIT", "Rinnen-Endkappe Zulauf 130x100", "Stk", "a", "PVC-U weiss")
    if nl.startswith("kappeablauf"):
        return Art("FIT-rinne-kappe-ablauf", "FIT", "Rinnen-Endkappe Ablauf 130x100", "Stk", "a", "PVC-U weiss")
    if nl.startswith("schlauch_rinne"):
        return Art("SCH-schlauch-rinne-id16", "SCH", "Schlauch ID16, 110 mm Stueck (Rinne Zulauf)", "Stk", "a", "PVC/PE")
    if nl.startswith("verteiler") and comp.startswith("nft_tisch"):
        return Art("FIT-verteiler-d25-nft", "FIT", "NFT-Verteiler d25 (Zulauf je Rinne, Laenge je Tisch)", "Stk", "c", "PVC blau")
    if nl.startswith("endstopfen_verteiler"):
        return Art("FIT-kappe-d25", "FIT", "PVC-U-Endkappe d25", "Stk", "a", "PVC-U", {"durchmesser_mm": 25})
    if nl.startswith("sammelrohr"):
        return Art("ROH-pvcu-d50", "ROH", "PVC-U-Druckrohr d50 (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": 50}, menge=d[1] / 1000.0 if comp.startswith("nft_tisch") else d[2] / 1000.0)
    if nl.startswith("endstopfen_sammelrohr"):
        return Art("FIT-kappe-d50", "FIT", "PVC-U-Endkappe d50", "Stk", "a", "PVC-U", {"durchmesser_mm": 50})
    if re.match(r"halter_\d+_rinne", nl):
        return Art("WNK-rinnenhalter-25", "WNK", "Rinnenhalter 25x25 (Stahl, Zuschnitt/Kleinteil)", "Stk", "c", "Stahl verzinkt")
    if nl.startswith("winkelhalter") or (nl.startswith("winkel") and not nl.startswith("winkelhalter") and comp != "pumpe_gross"):
        if nl.startswith("winkelhalter"):
            return Art("SRB-halter-klein-12x10x20", "SRB", "Kleinteil am Winkelhalter 12x10x20 (Schraube/Mutter) [A]", "Stk", "a", "Stahl verzinkt", flag="unbenannt")
        return Art("WNK-winkel-36x60x60", "WNK", "Winkel 36x60x60 (Rinnen-Winkelhalter, Stahl)", "Stk", "c", "Stahl verzinkt")
    if nl.startswith("diagonale") or nl.startswith("ldiag"):
        return Art("WNK-flach-3mm-diagonale", "WNK", "Flachstahl 3 mm (Diagonalen, Breite aus Modell nicht ableitbar, Zuschnitt)", "Stk", "c", "Stahl verzinkt", {"dicke_mm": 3}, flag="breite_offen")
    if re.match(r"(fussplatte|mess_fussplatte|kon_fussplatte|plat_fuss)", nl):
        return Art(f"BLE-fussplatte-{lnum(d[2] if False else max(d[0], d[1]))}x{lnum(d[1])}x{lnum(d[0])}", "BLE", f"Fussplatte Stahl verzinkt {lnum(d[1])}x{lnum(d[1])}x{lnum(d[0])} mm", "Stk", "c", "Stahl verzinkt")
    if nl in ("regalboden",) or nl.startswith("auffangrand") or m == "Blech" or nl in ("plat_boden",) or nl.startswith("kon_boden"):
        t = d[0]
        return Art(f"BLE-blech-st-{lnum(d[0])}", "BLE", f"Stahlblech {lnum(d[0])} mm verzinkt, Zuschnitt {lnum(d[2])}x{lnum(d[1])}", "Stk", "c", "Stahl verzinkt", {"dicke_mm": d[0], "zuschnitt_mm": [d[2], d[1]]}, flag="zuschnitt_je_stueck")
    if nl == "plattform":
        return Art(f"SON-plattform-{lnum(d[2])}x{lnum(d[1])}", "SON", f"Tankplattform {lnum(d[2])}x{lnum(d[1])}x{lnum(d[0])} (Stahl, Eigenbau)", "Stk", "c", "Stahl verzinkt")
    if nl in ("zulaufsieb", "auslaufsieb"):
        return Art("SON-tanksieb-stahl", "SON", "Sieb am Tank (Stahl verzinkt, Zulauf/Auslauf)", "Stk", "c", "Stahl verzinkt")
    if nl.startswith("stuetzrippe"):
        return Art("SON-holz-stuetzrippe", "SON", "Stuetzrippe Fichte (Tank-Auflage)", "Stk", "c", "Holz Fichte")
    if nl == "klemme" and comp == "halter_tauch":
        return Art("SON-tauchklemme", "SON", "Klemme Tauchrohr (Stahl, Eigenbau)", "Stk", "c", "Stahl verzinkt")
    if nl.startswith("schelle_"):
        return Art("SCH-rohrschelle-d63", "SCH", "Rohrschelle d63 (Stahl verzinkt, Doppelschelle)", "Stk", "a", "Stahl verzinkt")
    if nl == "hutschiene":
        return Art("ELE-hutschiene-35", "ELE", "Hutschiene 35 mm", "Stk", "a", "Stahl verzinkt")
    if nl.startswith("wandlasche"):
        return Art("WNK-wandlasche-30x30x3", "WNK", "Wandlasche 30x30x3", "Stk", "c", "Stahl verzinkt")
    if nl.startswith("verschraubung_") and comp == "halter_box" or nl == "kabelverschraubung":
        return Art("ELE-kabelverschraubung-pg", "ELE", "Kabelverschraubung PA (PG/M20)", "Stk", "a", "PA schwarz")
    if m.startswith("Edelstahl Feinfilter") or (comp == "feinfilter" and m == "Edelstahl Feinfilter"):
        if nl == "korbflansch":
            return Art("BLE-v2a-3mm-korbflansch", "BLE", "Edelstahlblech 3 mm 1.4301, Zuschnitt 604x414 (Korbflansch)", "Stk", "c", "Edelstahl 1.4301")
        if nl.startswith("spannbock") or nl.startswith("spannhebel"):
            return Art("SON-spannverschluss-edelstahl", "SON", "Spannverschluss Edelstahl (Bock + Hebel)", "Stk", "a", "Edelstahl 1.4301", teil_von=nl.startswith("spannhebel"))
        if nl.startswith("korbgriff"):
            return Art("SON-korbgriff-v2a", "SON", "Korbgriff Edelstahl (Eigenbau)", "Stk", "c", "Edelstahl 1.4301")
        a = profil_artikel(b, "Edelstahl 1.4301", "v2a")
        return a
    if m == "Netz Edelstahl Feinfilter":
        return Art("GEW-v2a-100um", "GEW", "Edelstahl-Siebgewebe 100 um, 1.4301 (Siebkorb, Flaeche aus Modell)", "m2", "a", "Edelstahl 1.4301", {"maschenweite_um": 100}, menge=(2 * (d[1] * d[2] + d[0] * d[2]) + d[0] * d[1]) / 1e6, flag="flaeche_geschaetzt")
    if m == "PP Feinfilter" and nl == "behaelter":
        return Art("BEH-feinfilter-pp-630x440x610", "BEH", "Feinfilter-Behaelter PP 630x440x610 (Eigenbau/Kaufteil offen)", "Stk", "b", "PP")
    if m == "PP Feinfilter":
        return Art("BEH-feinfilter-pp-630x440x610", "BEH", "Feinfilter-Behaelter PP 630x440x610 (Eigenbau/Kaufteil offen)", "Stk", "b", "PP", teil_von=True)
    if m == "EPDM Feinfilter":
        return Art("FOL-epdm-dichtung-630x440", "FOL", "EPDM-Flachdichtung 630x440x3", "Stk", "c", "EPDM")
    if m == "PVC Feinfilter":
        if nl in ("auslauf_flansch_innen",):
            return Art("ARM-bulkhead-d63", "ARM", "PVC-U-Bulkhead d63 (Tank-/Behaelterdurchfuehrung)", "Stk", "a", "PVC-U", {"durchmesser_mm": 63})
        if nl == "auslauf_mutter_aussen":
            return Art("ARM-bulkhead-d63", "ARM", "PVC-U-Bulkhead d63", "Stk", "a", "PVC-U", teil_von=True)
        if "tuelle" in nl:
            return Art("SCH-schlauchtuelle-d25", "SCH", "Schlauchtuelle d25 (PVC)", "Stk", "a", "PVC")
        if nl in ("einlaufrohr", "auslaufrohr", "spritzrohr", "ablassstutzen", "spuelstutzen"):
            dd = snap_d(d[0])
            return Art(f"ROH-pvcu-d{dd}", "ROH", f"PVC-U-Druckrohr d{dd} (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": dd}, menge=d[2] / 1000.0)
    # PVC/PP-Rohrteile aus Tank, Beet, Puffer, Halter
    if m.startswith("PVC") or m in ("PP grau", "PP weiss", "PA schwarz", "Default", "Kanal PVC", "HDPE weiss"):
        if "bulkhead" in nl:
            dd = snap_d(d[0])
            return Art(f"ARM-bulkhead-d{dd}", "ARM", f"PVC-U-Bulkhead d{dd}", "Stk", "a", "PVC-U", {"durchmesser_mm": dd})
        if re.search(r"kappe|stopfen|schutzkappe|schachtkappe|deckelkappe|bodenkappe", nl):
            dd = snap_d(d[0])
            return Art(f"FIT-kappe-d{dd}", "FIT", f"PVC-U-Kappe d{dd}", "Stk", "a", "PVC-U", {"durchmesser_mm": dd})
        if re.search(r"huelse|reduktion", nl):
            dd = snap_d(d[0])
            return Art(f"FIT-reduktion-d{dd}", "FIT", f"PVC-U-Reduktion/Huelse d{dd}", "Stk", "a", "PVC-U", {"durchmesser_mm": dd})
        if re.search(r"stutzen|zapfen|nippel|anschluss_", nl) or nl in ("zulauf", "ueberlauf", "belueftung"):
            dd = snap_d(d[0])
            return Art(f"FIT-stutzen-d{dd}", "FIT", f"PVC-U-Stutzen d{dd} (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": dd})
        if re.search(r"rohr|glocke|schacht|leitrohr|strecke|standrohr", nl) or nl.startswith("zulaufrohr"):
            dd = snap_d(d[0])
            return Art(f"ROH-pvcu-d{dd}", "ROH", f"PVC-U-Druckrohr d{dd} (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": dd}, menge=d[2] / 1000.0)
        if "tuelle" in nl:
            return Art("SCH-schlauchtuelle-d12", "SCH", "Schlauchtuelle (PVC)", "Stk", "a", "PVC")
        if nl == "anbohrschelle":
            return Art("ARM-anbohrschelle", "ARM", "Anbohrschelle PVC-U (Messstelle)", "Stk", "a", "PVC-U")
        if nl.startswith("verschraubung"):
            return Art(f"FIT-verschraubung-d{snap_d(d[1] if d[1] > 40 else d[0])}", "FIT", "PVC-U-Verschraubung (Rohrverbinder)", "Stk", "a", "PVC-U")
        if nl in ("vorfilter", "sensorblock", "beruhigungsstrecke", "zellkoerper"):
            return Art(f"SON-{comp.replace('_','-')}-{nl}", "SON", f"{n} ({comp}, Eigenbau aus PVC-U)", "Stk", "c", "PVC-U")
        if nl == "mastrohr" or nl == "tauchrohr":
            dd = snap_d(d[0])
            return Art(f"ROH-pvcu-d{dd}", "ROH", f"PVC-U-Rohr d{dd} (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": dd}, menge=d[2] / 1000.0)
    if m == "Edelstahl" and comp.startswith("halter_inline"):
        return Art(f"SON-{comp.replace('_','-')}-sieb", "SON", f"Sieb {comp} (Edelstahl)", "Stk", "c", "Edelstahl")
    if m == "Edelstahl" and comp == "halter_druck":
        return Art("FIT-gewindenippel-edelstahl", "FIT", "Gewindenippel Edelstahl (Druckmessstelle)", "Stk", "a", "Edelstahl")
    if m == "PP weiss" and nl == "strahlungsschutz":
        return Art("SON-strahlungsschutz-par", "SON", "Strahlungsschutz PP weiss (Messmast)", "Stk", "c", "PP weiss")
    if m == "PA schwarz" and nl == "kappe":
        return Art("FIT-kappe-pa-d44", "FIT", "Kappe PA schwarz d44 (Tauchrohr)", "Stk", "a", "PA schwarz")
    if m == "Aluminium":
        return None
    # Stahl-Profile (letzter Schritt): Rahmen, Beine, Holme, Ringe, Pfosten, Staender, Traeger, Leiter, Gel_...
    if m.startswith("Stahl verzinkt") and d[0] > 0 and d[2] / max(d[0], 1) >= 3:
        return profil_artikel(b)
    return None


W37_KOMP = ("aktivkohle_station", "geblaese_luft", "luft_scheibenbelueftung", "luftverteiler_4", "luftverteiler_6", "schrank_einfuehrung", "schwimmerventil_pool")


def classify_w37(comp, b):
    """Komponenten aus W37-2/W37-3 (Aktivkohle, Geblaese, Scheibenbelueftung, Luftverteiler, Schrank-Einfuehrung, Schwimmerventil, Drittbecken-Stutzen).
    Zuordnungen nach Bauteilblatt und Gestalt; Annahmen mit [A] im Text, Flag `w37_annahme`."""
    n = (b["name"] or "")
    nl = re.sub(r" \(\d+\)", "", n.lower())
    d = dims(b)
    F = "w37_annahme"
    if comp == "becken_dritt_klein" and nl.startswith("stutzen_"):
        return Art("ARM-bulkhead-pool", "ARM", "Pool-Durchfuehrung d63 (Stutzen Pool-Wand)", "Stk", "a", "PVC-U", {"durchmesser_mm": 63})
    if comp == "aktivkohle_station":
        if nl.startswith("konsole"):
            return Art("SON-ak-konsole", "SON", "Konsole Sedimentfilter (Stahl, Eigenbau) [A]", "Stk", "c", "Stahl", flag=F)
        if nl in ("sedimentgehaeuse", "sedimentpatrone", "kopf_sediment"):
            return Art("BEH-ak-sedimentfilter", "BEH", "Sedimentfilter-Set (Gehaeuse, Kopf, Patrone) [A]", "Satz", "a", "PP", teil_von=(nl != "sedimentgehaeuse"), flag=F)
        if nl.startswith("behaelter_"):
            return Art("BEH-ak-kompositbehaelter-254x790", "BEH", "Aktivkohle-Druckbehaelter Komposit 254x790 mm mit Steuerkopf [A]", "Stk", "a", "Komposit", {"bbox_mm": d}, flag=F)
        if re.match(r"kopf_\d", nl):
            return Art("BEH-ak-kompositbehaelter-254x790", "BEH", "Aktivkohle-Druckbehaelter Komposit 254x790 mm mit Steuerkopf [A]", "Stk", "a", "Komposit", teil_von=True, flag=F)
        if nl.startswith("kohlebett"):
            return Art("TOP-aktivkohle", "TOP", "Aktivkohle-Granulat (Behaelterfuellung)", "m3", "a", "Aktivkohle", menge=(3.14159 / 4 * d[0] * d[1] * d[2]) / 1e9, flag=F)
        if nl.startswith("rohr_"):
            dd = snap_d(d[1])
            return Art(f"ROH-pvcu-d{dd}", "ROH", f"PVC-U-Druckrohr d{dd} (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": dd}, menge=d[2] / 1000.0, flag=F)
        if nl.startswith("t_"):
            return Art("FIT-t-d25", "FIT", "PVC-U-T-Stueck d25", "Stk", "a", "PVC-U", {"groesse": "d25"}, flag=F)
        if nl.startswith("hahn_") and not nl.endswith(("spindel", "hebel")):
            dd = 25 if d[0] >= 42 else 20
            return Art(f"ARM-kugelhahn-d{dd}", "ARM", f"PVC-U-Kugelhahn d{dd}", "Stk", "a", "PVC-U", {"durchmesser_mm": dd}, flag=F)
        if nl.startswith("hahn_") or nl.startswith("probehahn_griff"):
            return None
        if nl == "probehahn":
            return Art("ARM-probehahn-messing", "ARM", "Probierhahn Messing 1/2 Zoll [A]", "Stk", "a", "Messing", flag=F)
        if nl == "begrenzer":
            return Art("ARM-durchflussbegrenzer-messing", "ARM", "Durchflussbegrenzer Messing [A]", "Stk", "a", "Messing", flag=F)
        if nl.startswith("reduzierung"):
            return Art("FIT-red-d32-d25", "FIT", "PVC-U-Reduzierung d32 auf d25", "Stk", "a", "PVC-U", {"groesse": "d32_d25"}, flag=F)
    if comp == "geblaese_luft":
        if nl == "pumpe":
            return Art("PMP-geblaese-luft", "PMP", "Membrangeblaese Luft (Leistung offen, Bauteilblatt geblaese_luft)", "Stk", "a", None, {"bbox_mm": d}, flag=F)
        if nl.startswith("gummifuss"):
            return Art("SON-gummifuss-40", "SON", "Gummifuss 40x40x15", "Stk", "a", "Gummi", flag=F)
        if nl == "netzkabel":
            return Art("PMP-geblaese-luft", "PMP", "Membrangeblaese Luft", "Stk", "a", None, teil_von=True, flag=F)
        if nl == "stutzen_luft":
            return Art("FIT-stutzen-d20", "FIT", "PVC-U-Stutzen d20 (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": 20}, flag=F)
        if nl == "rohrschleife":
            return Art("ROH-pvcu-d20", "ROH", "PVC-U-Druckrohr d20 (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": 20}, menge=b["mass_g"] / 0.122 / 1000.0, flag="laenge_aus_masse")
        if nl == "rueckschlagventil":
            return Art("ARM-rsv-d20", "ARM", "PVC-U-Rueckschlagventil d20", "Stk", "a", "PVC-U", {"groesse": "d20"}, flag=F)
        if nl == "rohr_austritt":
            return Art("ROH-pvcu-d20", "ROH", "PVC-U-Druckrohr d20 (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": 20}, menge=d[2] / 1000.0, flag=F)
    if comp == "luft_scheibenbelueftung":
        if nl == "stutzen":
            return Art("FIT-stutzen-d25", "FIT", "PVC-U-Stutzen d25 (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": 25}, flag=F)
        return Art("SON-scheibenbelueftung-270", "SON", "Scheibenbelueftung d270 (Tragteller, Stuetzfuss, EPDM-Membran) [A]", "Stk", "a", "PP/EPDM",
                   teil_von=(nl != "membran"), flag=F)
    if comp in ("luftverteiler_4", "luftverteiler_6") and nl == "verteiler":
        k = comp[-1]
        return Art(f"SON-luftverteiler-{k}", "SON", f"Luftverteiler {k}-fach (PVC, Eigenbau) [A]", "Stk", "c", "PVC", {"bbox_mm": d}, flag=F)
    if comp == "schrank_einfuehrung":
        if nl == "schrankboden":
            return Art("BLE-schrankboden-3x500x800", "BLE", "Stahlblech 3 mm, Zuschnitt 800x500 (Schrankboden) [A]", "Stk", "c", "Stahl", flag=F)
        if nl == "schrankwand":
            return Art("SON-schrankwand-500x800", "SON", "Schrankwand 500x800 (Eigenbau, Werkstoff offen) [A]", "Stk", "c", "Stahl", flag=F)
        big = d[2] >= 150
        sz = "dn100" if big else "dn50"
        if nl in ("koerper", "dichtung", "gegenmutter"):
            return Art(f"ARM-kabeleinfuehrung-{sz}", "ARM", f"Kabeleinfuehrung {sz.upper()} (Koerper, Dichtung, Gegenmutter)", "Stk", "a", "PP", teil_von=(nl != "koerper"), flag=F)
        if nl == "leerrohrbogen":
            bz = "dn100" if d[2] > 500 else "dn50"
            return Art(f"FIT-leerrohr-bogen90-{bz}", "FIT", f"Leerrohr-Bogen 90 Grad {bz}", "Stk", "a", "PVC/PP", flag=F)
    if comp == "schwimmerventil_pool":
        return Art("ARM-schwimmerventil-pool", "ARM", "Schwimmerventil Pool (Gehaeuse, Wangen, Hebelarm mit Kugel) [A]", "Stk", "a", "PP", teil_von=(nl != "ventilgehaeuse"), flag=F)             if nl != "uebergang" else Art("FIT-stutzen-d32", "FIT", "PVC-U-Stutzen d32 (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": 32}, flag=F)
    return None


# ------------------------------------------------------------------ N-UNIFY-AUTOBAHN U8: Komponenten des einen Kreislaufs (U2 bis U6)
UNIFY_KOMP = re.compile(
    r"^(ring_schlauchwege|ring_ruecklauf|ring_abzweig_d(32|40)|ring_ecke_d75|ringstuetze_d75(_b)?|sumpftank|tauchpumpe_modul|venturi_belueffter|"
    r"notluftpumpe|schwimmerschalter_hochstand|regentank_5m3|schlamm_sammelbehaelter|nachspeise_ventil|entluefter_d75|becken_dritt_klein|"
    r"permakultur_modul|ibc_beet_(aussen|innen)_\d+|ausleger_schlauch_\d+|portal_joch_mitte_[ab]|montageschiene_41_\d+|schienenverbinder_36|"
    r"knoten_schere.*|biofilter_dritt|pegelschacht(_podest)?|ruecklauf_rinne|bodenrinne_rost_gang[ab]|schlauch_fall_id\d+_.*)$")
# Meterlast der Schlaeuche im Modell (Vollzylinder, Median der geraden Segmente, Messung 11.11.2026) [E]
SCHLAUCH_G_PRO_M = {32: 1058.1, 25: 625.4}
_BODIES = {}


def _pfad_od(comp, name):
    """Aussendurchmesser des Schlauchs eines Weges (kleinstes Bbox-Mass seiner Schlauchsegmente), Weg = F<nn> bzw. R<nn>_e<nn>"""
    if "c" not in _BODIES:
        _BODIES["c"] = json.load(open(CACHE, encoding="utf-8"))["komponenten"]
    toks = name.split("_")
    key = "_".join(toks[:2]) if comp == "ring_ruecklauf" else (toks[0] if comp.startswith("ring_") else "")
    k = (comp, key)
    if k not in _BODIES:
        ods = [min(dims(x)[0], 99) for x in _BODIES["c"][comp]["bodies"]
               if (x["material"] or "").startswith("SCH") and (key == "" or "_".join((x["name"] or "").split("_")[:2] if comp == "ring_ruecklauf" else (x["name"] or "").split("_")[:1]) == key)]
        _BODIES[k] = min(ods) if ods else 32
    return _BODIES[k]


def _stahl_teil(b, tag="unify"):
    """Stahlteil nach Gestalt: Profil (lang), Blech-Zuschnitt (flach) oder Sonderteil (kurz, dick)"""
    d = dims(b)
    if d[0] > 0 and d[2] / d[0] >= 3 and d[1] <= 3 * d[0] + 1:
        return profil_artikel(b)
    if d[0] <= 15 and d[1] >= 3 * d[0]:
        return Art(f"BLE-blech-st-{lnum(d[0])}", "BLE", f"Stahlblech {lnum(d[0])} mm verzinkt, Zuschnitt {lnum(d[2])}x{lnum(d[1])}", "Stk", "c", "Stahl verzinkt",
                   {"dicke_mm": d[0], "zuschnitt_mm": [d[2], d[1]]}, flag="zuschnitt_je_stueck")
    return Art(f"SON-stahlteil-{lnum(d[0])}x{lnum(d[1])}x{lnum(d[2])}", "SON", f"Stahlteil {lnum(d[0])}x{lnum(d[1])}x{lnum(d[2])} mm (Eigenbau/Zuschnitt, Stahl verzinkt)", "Stk", "c", "Stahl verzinkt")


def classify_unify(comp, b):
    """Koerper der Komponenten aus U2 bis U6 (und der Knoten-/Portalteile). Rueckgabe: Art, ('ausnahme', Text) oder None."""
    if not UNIFY_KOMP.match(comp):
        return None
    n = (b["name"] or "")
    nl = re.sub(r" \(\d+\)", "", n.lower())
    m = b["material"] or ""
    d = dims(b)
    F = "unify_annahme"
    AUSN_SRB = ("ausnahme", "Mutter/Scheibe im Schraubensatz enthalten")

    # ---- Schlaeuche und Ausstattung der Wege (Quelle: Wege e..., Nennweite D106/D138)
    if comp in ("ring_schlauchwege", "ring_ruecklauf") or comp.startswith("schlauch_fall_id"):
        fall = comp.startswith("schlauch_fall_id")
        if m.startswith("SCH"):
            od = _pfad_od(comp, n)
            idn = int(re.search(r"id(\d+)", comp).group(1)) if fall else (25 if od >= 29 else 19)
            gpm = SCHLAUCH_G_PRO_M.get(int(od)) if not fall else None
            gpm = gpm or 1.316 * math.pi / 4 * od * od  # Dichte aus den Segmenten OD 32: 1,316 g/cm3 [E]
            return Art(f"SCH-schlauch-id{idn}", "SCH", f"Schlauch ID{idn} (Meterware, Laenge aus Modellmasse)", "m", "a", "PVC/PE", {"nennweite": f"id{idn}"},
                       menge=b["mass_g"] / gpm if b["mass_g"] else 0.0, flag="laenge_aus_masse")
        if "tuelle" in nl:
            return Art("SCH-schlauchtuelle-d25", "SCH", "Schlauchtuelle d25 (PVC)", "Stk", "a", "PVC")
        if nl.endswith("regelhahn"):
            return Art("ARM-kugelhahn-d25", "ARM", "PVC-U-Kugelhahn d25", "Stk", "a", "PVC-U", {"durchmesser_mm": 25})
        if nl.endswith("hebel"):
            return Art("ARM-kugelhahn-d25", "ARM", "PVC-U-Kugelhahn d25", "Stk", "a", "PVC-U", {"durchmesser_mm": 25}, teil_von=True)
        if "kupplung_" in nl:
            idn = int(re.search(r"id(\d+)", comp).group(1)) if fall else (25 if _pfad_od(comp, n) >= 29 else 19)
            return Art(f"ARM-schnellkupplung-id{idn}", "ARM", f"Schnellkupplung ID{idn} (Dose und Stecker, Edelstahl) [A]", "Stk", "a", "Edelstahl",
                       teil_von=nl.endswith("stecker"), flag=F)
        if nl.endswith("anschluss"):
            return Art("FIT-schlauchanschluss-abzweig", "FIT", "Schlauchanschluss am Abzweig (Gewinde/Klebe auf Schlauchtuelle) [A]", "Stk", "a", "PVC/PP", flag=F)
        if "halter_" in nl:
            return Art("SON-schlauchhalter-pp", "SON", "Schlauchhalter PP (Clip) [A]", "Stk", "a", "PP", flag=F)
        if nl.endswith("winkel"):
            return Art("FIT-schlauchwinkel-90", "FIT", "Schlauch-Winkelstueck 90 Grad (PVC, Tuelle-Tuelle) [A]", "Stk", "a", "PVC", flag=F)
    # ---- Ring-Abzweige, Ringecke, Stuetzen, Schienen, Ausleger, Portal
    if comp.startswith("ring_abzweig"):
        mm = re.match(r"reduzierung_(\d+)_(\d+)", nl)
        if mm:
            return Art(f"FIT-red-d{mm.group(1)}-d{mm.group(2)}", "FIT", f"PVC-U-Reduzierung d{mm.group(1)} auf d{mm.group(2)}", "Stk", "a", "PVC-U", {"groesse": f"d{mm.group(1)}_d{mm.group(2)}"})
        if nl == "t_d75":
            return Art("FIT-t-d75", "FIT", "PVC-U-T-Stueck d75", "Stk", "a", "PVC-U", {"groesse": "d75"})
        mm = re.match(r"rohrstueck_d(\d+)", nl)
        if mm:
            return Art(f"ROH-pvcu-d{mm.group(1)}", "ROH", f"PVC-U-Druckrohr d{mm.group(1)} (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": int(mm.group(1))}, menge=d[2] / 1000.0)
        mm = re.match(r"kugelhahn_d(\d+)(_spindel|_hebel)?$", nl)
        if mm:
            return Art(f"ARM-kugelhahn-d{mm.group(1)}", "ARM", f"PVC-U-Kugelhahn d{mm.group(1)}", "Stk", "a", "PVC-U", {"durchmesser_mm": int(mm.group(1))}, teil_von=bool(mm.group(2)))
    if comp == "ring_ecke_d75":
        return Art("FIT-ring-ecke-d75", "FIT", "Ring-Ecke d75 (PE100, Segmentbogen/Formteil fuer den Ring) [A]", "Stk", "a", "PE100", {"durchmesser_mm": 75}, flag=F)
    if comp.startswith("montageschiene"):
        return profil_artikel(b)
    if comp.startswith(("ringstuetze", "ausleger_schlauch", "portal_joch", "schienenverbinder", "pegelschacht_podest")):
        if "epdm" in m.lower():
            return Art("FOL-epdm-schelleneinlage-d75", "FOL", "EPDM-Schelleneinlage d75", "Stk", "a", "EPDM")
        if nl.startswith("rohrschelle"):
            return Art("SCH-rohrschelle-d75", "SCH", "Rohrschelle d75 (Stahl verzinkt)", "Stk", "a", "Stahl verzinkt")
        if nl.startswith("schraube_"):
            g = int(round(d[0]))
            return Art(f"SRB-satz-m{g}x{int(round((d[2] - 5.3) / 5.0)) * 5}", "SRB", f"Schraubensatz M{g}x{int(round((d[2] - 5.3) / 5.0)) * 5} (Sechskantschraube + Mutter + 2 Scheiben) [A]", "Satz", "a", "Stahl verzinkt",
                       {"gewinde": f"M{g}"}, flag=F)
        if nl.startswith(("anker_", "gewindestange")):
            return Art(f"SRB-gewindestange-m{int(round(d[0]))}x{int(round(d[2] / 10.0)) * 10}", "SRB", f"Gewindestange M{int(round(d[0]))}x{int(round(d[2] / 10.0)) * 10}, verzinkt", "Stk", "a", "Stahl verzinkt")
        return _stahl_teil(b)
    # ---- Knoten Schere (N-KNOTEN-SCHERE): Laserteile und Schrauben
    if comp.startswith("knoten_schere"):
        if m == "Stahl Laserteil" and nl.startswith("lochplatte"):
            return Art(f"BLE-laser-lochplatte-{lnum(d[1])}x{lnum(d[2])}x{lnum(d[0])}", "BLE", f"Laserteil Lochplatte {lnum(d[1])}x{lnum(d[2])}x{lnum(d[0])} mm, Stahl (Knoten Schere)", "Stk", "c", "Stahl Laserteil")
        if m == "Stahl Laserteil":
            return Art(f"SON-laser-lasche-{lnum(d[0])}x{lnum(d[1])}x{lnum(d[2])}", "SON", f"Laserteil Lasche {lnum(d[0])}x{lnum(d[1])}x{lnum(d[2])} mm, Stahl (Knoten Schere)", "Stk", "c", "Stahl Laserteil")
        if m == "Stahl Schraube":
            if nl.endswith(("mutter", "scheibeo", "scheibeu")):
                return AUSN_SRB
            if nl == "platte_schraube":
                return Art("SRB-satz-m10x60", "SRB", "Schraubensatz M10x60 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben)", "Satz", "a", "Stahl verzinkt", {"gewinde": "M10", "laenge_mm": 60})
            if nl == "dreh_schraube":
                return Art("SRB-satz-m8x30", "SRB", "Schraubensatz M8x30 (Sechskantschraube DIN 933 + Mutter + 2 Scheiben) [A]", "Satz", "a", "Stahl verzinkt", {"gewinde": "M8", "laenge_mm": 30}, flag=F)
    if comp.startswith("bodenrinne_rost_gang"):
        if nl == "rinnenkoerper":
            return Art(f"SON-bodenrinne-pp-{lnum(d[2])}", "SON", f"Bodenrinne PP {lnum(d[0])}x{lnum(d[1])}x{lnum(d[2])} (Laufgang-Entwaesserung, Eigenbau/Zuschnitt) [A]", "Stk", "c", "PP", flag=F)
        if nl == "gitterrost":
            return Art(f"MAT-gitterrost-{lnum(d[1])}x{lnum(d[2])}", "MAT", f"Gitterrost verzinkt {lnum(d[2])}x{lnum(d[1])}x{lnum(d[0])} mm (Rinnenabdeckung) [A]", "Stk", "a", "Stahl verzinkt", flag=F)
    if comp == "ruecklauf_rinne":
        if nl == "rinne":
            return Art(f"SON-ruecklaufrinne-v2a-{lnum(d[2])}", "SON", f"Ruecklaufrinne Edelstahl {lnum(d[0])}x{lnum(d[1])}x{lnum(d[2])} (Altbestand) [A]", "Stk", "c", "Edelstahl", flag=F)
        return _stahl_teil(b)
    if comp == "pegelschacht":
        if nl in ("fass", "deckel"):
            return Art("BEH-pegelschacht-fass", "BEH", "Pegelschacht PE-HD-Fass mit Deckel (Altbestand, entfaellt im Modell) [A]", "Stk", "a", "PE-HD", teil_von=(nl == "deckel"), flag=F)
        if nl.endswith(("stutzen", "stutzen_a", "stutzen_b")) or nl == "notueberlauf":
            dd = snap_d(d[0])
            return Art(f"FIT-stutzen-d{dd}", "FIT", f"PVC-U-Stutzen d{dd} (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": dd})
        if nl == "schwimmerstange":
            dd = snap_d(d[0])
            return Art(f"ROH-pvcu-d{dd}", "ROH", f"PVC-U-Druckrohr d{dd} (Meterware)", "m", "a", "PVC-U", {"durchmesser_mm": dd}, menge=d[2] / 1000.0)
        if nl.startswith("schwimmer_"):
            return Art("ARM-schwimmerschalter-hochstand", "ARM", "Schwimmerschalter Hochstand (Fabrikat offen) [A]", "Stk", "a", None)
    if comp == "biofilter_dritt":
        return Art("BEH-biofilter-dritt-fass", "BEH", "Biofilter-Fass PE mit Lochplatte (Altbestand-Drittbiofilter) [A]", "Stk", "a", "PE", teil_von=(nl != "fass"), flag=F)
    # ---- Sumpftank
    if comp == "sumpftank":
        if m == "Beton":
            return ("ausnahme", "Beton nach Menge (Entscheidung 04.11.2026)")
        if nl == "sumpf_folie":
            return Art("MAT-epdm-teichfolie", "MAT", "EPDM-Teichfolie 1,5 mm (Grubenauskleidung, Flaeche aus Modell: Boden und vier Waende)", "m2", "b", "EPDM",
                       menge=(d[1] * d[2] + 2 * d[0] * (d[1] + d[2])) / 1e6, flag="flaeche_aus_bbox")
        if nl.startswith("trennwand"):
            return Art(f"BLE-pp-platte{lnum(d[0])}-{lnum(d[1])}x{lnum(d[2])}", "BLE", f"PP-Platte {lnum(d[0])} mm, Zuschnitt {lnum(d[2])}x{lnum(d[1])} (Trennwand, Pufferzone)", "Stk", "c", "PP weiss")
        if nl == "pumpensockel":
            return Art(f"BLE-pp-platte{lnum(d[0])}-{lnum(d[1])}x{lnum(d[2])}", "BLE", f"PP-Platte {lnum(d[0])} mm, Zuschnitt {lnum(d[2])}x{lnum(d[1])} (Pumpensockel)", "Stk", "c", "PP grau")
        if nl.startswith("zulauf_"):
            return Art("FIT-stutzen-d32", "FIT", "PVC-U-Stutzen d32 (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": 32})
        if nl == "schwimmerhalter":
            return Art("SON-pp-schwimmerhalter", "SON", "Schwimmerhalter PP 40x60x80 (Eigenbau)", "Stk", "c", "PP grau")
        if nl.startswith("deckel_"):
            return Art("MAT-gitterrost-deckel", "MAT", "Begehbarer Gitterrost 30/10 feuerverzinkt 1229 x 1026 x 40 mm (Grubendeckel)", "Stk", "a", "Stahl verzinkt", {"bbox_mm": d})
        if nl.startswith("zonenschild"):
            return Art("SON-pp-zonenschild", "SON", "Zonenschild PP 2x40x100 (Beschriftung Pufferzone)", "Stk", "c", "PP weiss")
    # ---- Pumpen, Venturi, Schalter, Behaelter, Ventile
    if comp == "tauchpumpe_modul":
        if nl == "gehaeuse":
            return Art("PMP-tauchpumpe-oase-8000", "PMP", "Tauchpumpe (Klasse Oase AquaMax Eco Premium 8000, Typ offen, siehe Beschaffung)", "Stk", "a", None, {"bbox_mm": d})
        if nl == "kabel":
            return Art("PMP-tauchpumpe-oase-8000", "PMP", "Tauchpumpe", "Stk", "a", None, teil_von=True)
        if nl == "druckstutzen":
            return Art("FIT-stutzen-d50", "FIT", "PVC-U-Stutzen d50 (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": 50})
        if nl == "rueckschlagventil":
            return Art("ARM-rueckschlagventil-d50", "ARM", "PVC-U-Rueckschlagventil d50 (Klebemuffe)", "Stk", "a", "PVC-U", {"groesse": "d50"})
    if comp == "venturi_belueffter":
        if nl == "injektor":
            return Art("ARM-venturi-mazzei-1583", "ARM", "Venturi-Injektor (Klasse Mazzei 1583, 1,5 Zoll; Typ offen, D113)", "Stk", "a", "PP")
        if nl.startswith("muffe_") or nl == "saugstutzen":
            return Art("ARM-venturi-mazzei-1583", "ARM", "Venturi-Injektor", "Stk", "a", "PP", teil_von=True)
        if nl == "rueckschlagventil":
            return Art("ARM-rueckschlagventil-luft", "ARM", "Rueckschlagventil Luft (Schlauch)", "Stk", "a", "PP")
        if nl == "luftfilter":
            return Art("SON-luftfilter-ansaug", "SON", "Ansaug-Luftfilter fuer den Venturi (PP) [A]", "Stk", "a", "PP weiss", flag=F)
    if comp == "notluftpumpe":
        if nl == "pumpe":
            return Art("PMP-luftpumpe-notluft", "PMP", "Notluftpumpe (Membranpumpe, Akku/Netz) [A]", "Stk", "a", None, {"bbox_mm": d})
        if nl == "tuelle":
            return Art("SCH-schlauchtuelle-d12", "SCH", "Schlauchtuelle (PVC)", "Stk", "a", "PVC")
        if nl == "rueckschlagventil":
            return Art("ARM-rueckschlagventil-luft", "ARM", "Rueckschlagventil Luft (Schlauch)", "Stk", "a", "PP")
        if nl.startswith("luftschlauch"):
            return Art(f"SCH-schlauch-luft-d{lnum(d[0])}", "SCH", f"Luftschlauch d{lnum(d[0])} (Meterware)", "m", "a", "PVC", {"durchmesser_mm": d[0]}, menge=d[2] / 1000.0)
        if nl == "luftstein":
            return Art("ARM-luftstein-notluft", "ARM", "Luftausstroemer (Luftstein)", "Stk", "a", "PE")
    if comp == "schwimmerschalter_hochstand":
        return Art("ARM-schwimmerschalter-hochstand", "ARM", "Schwimmerschalter Hochstand (Fabrikat offen) [A]", "Stk", "a", None, teil_von=(nl != "schwimmer"))
    if comp == "regentank_5m3":
        if nl == "tank":
            return Art("BEH-regentank-5000", "BEH", "Regenwassertank 5000 l, stehend, oberirdisch (PE)", "Stk", "a", "PE", {"volumen_l": 5000})
        if nl in ("dom", "domdeckel"):
            return Art("BEH-regentank-5000", "BEH", "Regenwassertank 5000 l", "Stk", "a", "PE", teil_von=True)
        if nl.endswith("stutzen"):
            dd = snap_d(d[0])
            return Art(f"FIT-stutzen-d{dd}", "FIT", f"PVC-U-Stutzen d{dd} (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": dd})
    if comp == "schlamm_sammelbehaelter":
        if nl == "behaelter":
            return Art("BEH-schlammbehaelter-350", "BEH", "Schlamm-Sammelbehaelter PE rund 350 l mit Deckel (Durchm. 900 x 600)", "Stk", "a", "PE", {"volumen_l": 350})
        if nl == "deckel":
            return Art("BEH-schlammbehaelter-350", "BEH", "Schlamm-Sammelbehaelter", "Stk", "a", "PE", teil_von=True)
        if nl == "entlueftung":
            return Art("FIT-entlueftung-d32", "FIT", "Entlueftung d32 (PVC-U, mit Insektengitter-Kappe) [A]", "Stk", "a", "PVC-U", {"durchmesser_mm": 32})
        if nl in ("einlaufstutzen", "auslaufrohr"):
            dd = snap_d(d[0])
            return Art(f"FIT-stutzen-d{dd}", "FIT", f"PVC-U-Stutzen d{dd} (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": dd})
        if nl == "kugelhahn":
            return Art("ARM-kugelhahn-d40", "ARM", "PVC-U-Kugelhahn d40", "Stk", "a", "PVC-U", {"durchmesser_mm": 40})
        if nl == "hahnhebel":
            return Art("ARM-kugelhahn-d40", "ARM", "PVC-U-Kugelhahn d40", "Stk", "a", "PVC-U", teil_von=True)
    if comp == "nachspeise_ventil":
        if nl.startswith("ventilgehaeuse"):
            return Art("ARM-schwimmerventil-nachspeise", "ARM", "Schwimmerventil 3/4 Zoll (Nachspeisung, Gehaeuse, Wangen, Hebelarm mit Kugel)", "Stk", "a", "PP")
        if nl.startswith(("wange_", "hebelarm")):
            return Art("ARM-schwimmerventil-nachspeise", "ARM", "Schwimmerventil 3/4 Zoll", "Stk", "a", "PP", teil_von=True)
        if nl.startswith("uebergang"):
            return Art("FIT-stutzen-d32", "FIT", "PVC-U-Stutzen d32 (Klebe/Gewinde)", "Stk", "a", "PVC-U", {"durchmesser_mm": 32})
    if comp == "entluefter_d75":
        if nl == "entlueftungs_t":
            return Art("FIT-t-d75", "FIT", "PVC-U-T-Stueck d75", "Stk", "a", "PVC-U", {"groesse": "d75"})
        if nl == "uebergangsnippel":
            return Art("FIT-uebergangsnippel-d75-d40", "FIT", "PVC-U-Uebergangsnippel d75 auf d40", "Stk", "a", "PVC-U")
        if nl == "entlueftungsventil":
            return Art("ARM-entlueftungsventil-messing", "ARM", "Be-/Entlueftungsventil Messing (Rohrleitung, 1 1/2 Zoll) [A]", "Stk", "a", "Messing", flag=F)
    if comp == "becken_dritt_klein" and nl.endswith("ueberlauf"):
        return Art("ARM-bulkhead-pool", "ARM", "Pool-Durchfuehrung d63 (Stutzen Pool-Wand)", "Stk", "a", "PVC-U", {"durchmesser_mm": 63})
    if comp == "permakultur_modul":
        if nl in ("kompostbox", "kompostdeckel"):
            return Art("SON-permakultur-kompostbox", "SON", "Kompostbox Fichte 525x600x1500 mit Deckel (Permakultur-Modul, Eigenbau) [A]", "Stk", "c", "Holz Fichte", teil_von=(nl == "kompostdeckel"), flag=F)
        if nl == "futterzuchtkiste":
            return Art("BEH-futterzuchtkiste-pe", "BEH", "Futterzuchtkiste PE 350x525x800 (Permakultur-Modul) [A]", "Stk", "a", "PE", {"bbox_mm": d}, flag=F)
    # ---- Beete (A21)
    if comp.startswith("ibc_beet"):
        if nl == "abtropfgitter":
            return Art("BLE-pp-abtropfgitter-beet", "BLE", "PP-Abtropfgitter 25 mm (Stegrost, Zuschnitt je Beet) [A]", "Stk", "c", "PP grau", {"dicke_mm": 25}, flag=F)
        if nl == "vlies":
            return Art("GEW-vlies-pp", "GEW", "PP-Vlies (Beetboden, Flaeche aus Modell)", "m2", "a", "PP Vlies", menge=d[1] * d[2] / 1e6, flag="flaeche_aus_bbox")
        if nl == "sieb":
            return Art("GEW-sieb-v2a-2mm", "GEW", "Edelstahl-Siebgewebe 2 mm (Beetsieb, Flaeche aus Modell)", "m2", "a", "Edelstahl 1.4301", {"maschenweite_mm": 2}, menge=d[1] * d[2] / 1e6, flag="flaeche_aus_bbox")
        if nl == "auslasswinkel":
            return Art("FIT-bogen90-d25", "FIT", "PVC-U-Bogen 90 Grad d25 (Beet-Auslass)", "Stk", "a", "PVC-U", {"groesse": "d25"})
        if nl == "luftschlauch":
            return Art("SCH-schlauch-luft-d8", "SCH", "Luftschlauch d8 (Meterware)", "m", "a", "PVC", {"durchmesser_mm": 8}, menge=d[2] / 1000.0)
        if nl == "ausstroemer":
            return Art("SON-ausstroemer-stab-600", "SON", "Ausstroemer-Stab PP 16x600 (Beet-Belueftung) [A]", "Stk", "a", "PP weiss", flag=F)
    return None


def zuordnen(comp, b):
    ex = ausnahme(comp, b)
    if ex:
        return None, ex
    u = classify_unify(comp, b)  # N-UNIFY-AUTOBAHN U8: Komponenten aus U2 bis U6 vor den Altregeln
    if u is not None:
        return (None, u[1]) if isinstance(u, tuple) else (u, None)
    if comp.startswith("lt_") and not bom_benennung.ist_unbenannt(b["name"]):
        return None, None  # eigene Behandlung
    nl = re.sub(r" \(\d+\)", "", (b["name"] or "").lower())
    if bom_benennung.ist_unbenannt(b["name"]) or nl.startswith("schraube_") or re.match(r"(scheibe|mutter|anker_\d|querbolzen)", nl):  # W60 5a/N-STUECKLISTE 5a: Normteile benannt, Gestalt-Erkennung gilt weiter
        bn = bom_benennung.benenne(comp, b)
        if bn is None:
            return None, None  # ungeklaert -> check_bom meldet
        if bn["kind"] != "schraube":
            return None, "Mutter/Scheibe im Schraubensatz enthalten"
        g, l = bn["gewinde"], bn["laenge"]
        return Art(bn["art_id"], "SRB", f"Schraubensatz {g}x{l} (Sechskantschraube DIN 933 + Mutter + 2 Scheiben)", "Satz", "a",
                   "Stahl verzinkt", {"gewinde": g, "laenge_mm": l}, flag="name_vergeben" if bom_benennung.ist_unbenannt(b["name"]) else None), None
    a = classify(comp, b)
    if a is None:
        a = classify_w37(comp, b)
    if a is None and comp not in W37_KOMP:
        a = classify_late(comp, b)
    if a is None and comp == "aktivkohle_station" and re.match(r"(hahn_.*(spindel|hebel)|probehahn_griff)", re.sub(r" \(\d+\)", "", (b["name"] or "").lower())):
        return None, "Teil eines Hahns (Griff/Spindel/Hebel) im Hahn-Artikel enthalten"
    return a, None


# ------------------------------------------------------------------ Hauptlauf
def main():
    if "--messen" in sys.argv or not os.path.exists(CACHE):
        messen()
    elif "--ergaenzen" in sys.argv:
        alt = json.load(open(CACHE, encoding="utf-8"))
        t0 = os.path.getmtime(CACHE)
        neu = {os.path.basename(f)[:-3] for f in glob.glob(os.path.join(COMP_DIR, "*.sc"))
               if os.path.basename(f)[:-3] not in alt["komponenten"] or os.path.getmtime(f) > t0}
        print("Nachmessung:", sorted(neu))
        messen(neu)
    cache = json.load(open(CACHE, encoding="utf-8"))
    comps = cache["komponenten"]
    inst = defaultdict(int)
    for i in json.load(open(INST, encoding="utf-8"))["instances"]:
        inst[i["d"]] += 1

    artikel = OrderedDict()
    ausn = defaultdict(lambda: defaultdict(int))
    ungeklaert = []

    def add(a, comp, stueck, menge, flag):
        r = artikel.setdefault(a.id, {
            "id": a.id, "typ": a.typ, "bezeichnung": a.bez, "werkstoff": a.werkstoff, "masse": a.mass,
            "lagerlaengen_mm": LAGER.get(a.typ) if a.einheit == "m" and a.typ in LAGER else None,
            "einheit": a.einheit, "beschaffung_art": a.art, "bezug": {"land": None, "ok": "offen"},
            "status": "OFFEN (Quelle)", "hinweise": [], "verwendung": []})
        r["verwendung"].append({"komponente": comp, "koerper": stueck, "instanzen": inst.get(comp, 0), "menge_je_instanz": round(menge, 4)})
        if flag and flag not in r["hinweise"]:
            r["hinweise"].append(flag)

    for comp, v in comps.items():
        agg = defaultdict(lambda: [0, 0.0, None])  # id -> [stueck, menge, Art]
        if comp.startswith("lt_"):
            a = classify_lt(comp, [b for b in v["bodies"] if not bom_benennung.ist_unbenannt(b["name"])] or v["bodies"])
            if a is None:
                ungeklaert.append((comp, "lt-Art unbekannt"))
                continue
            agg[a.id][0] += 1
            agg[a.id][1] += a.menge
            agg[a.id][2] = a
            for b in v["bodies"]:
                if bom_benennung.ist_unbenannt(b["name"]):
                    a2, ex2 = zuordnen(comp, b)
                    if ex2:
                        ausn[ex2][comp] += 1
                    elif a2 is None:
                        ungeklaert.append((comp, f"{b['name']} / {b['material']} / {dims(b)}"))
                    else:
                        agg[a2.id][0] += 1
                        agg[a2.id][1] += a2.menge
                        agg[a2.id][2] = agg[a2.id][2] or a2
        else:
            for b in v["bodies"]:
                a, ex = zuordnen(comp, b)
                if ex:
                    ausn[ex][comp] += 1
                    continue
                if a is None:
                    ungeklaert.append((comp, f"{b['name']} / {b['material']} / {dims(b)}"))
                    continue
                ent = agg[a.id]
                if not a.teil_von:
                    ent[0] += 1
                    ent[1] += a.menge
                ent[2] = ent[2] or a
                if a.teil_von and ent[2] is None:
                    ent[2] = a
        for aid, (st, mg, a) in agg.items():
            add(a, comp, st, mg, a.flag)

    # Summen
    for r in artikel.values():
        r["bedarf"] = {"einheit": r["einheit"], "menge": round(sum(u["instanzen"] * u["menge_je_instanz"] for u in r["verwendung"]), 3),
                       "komponenten_ohne_instanz": sorted(u["komponente"] for u in r["verwendung"] if u["instanzen"] == 0)}
        r["ohne_instanz_im_modell"] = all(u["instanzen"] == 0 for u in r["verwendung"])
        if r["typ"] in ("ROH", "FIT", "ARM", "SCH") and any(u["komponente"].startswith("lt_") for u in r["verwendung"]):
            r["hinweise"].append("e20_pruefen (Leitungsteil, Wasserkreislauf-Variante E20 offen)")

    kat = json.load(open(KATALOG, encoding="utf-8"))
    kat["typen"] = TYPEN
    kat["artikel"] = list(artikel.values())
    kat["artikel_ausnahmen"] = {g: dict(c) for g, c in ausn.items()}
    kat["artikel_ungeklaert"] = [{"komponente": c, "koerper": k} for c, k in ungeklaert]
    kat["artikel_stempel"] = dict(cache["stempel"], erzeugt_von="scripts/bom_artikel.py", preise="leer (Paket 2, data/beschaffung)",
                                  entscheidungen="Preise brutto; Pflanzgut, Fisch, Beton, Aushub nicht in der Liste; UK als Europa offen (Orchestrator 04.11.2026, Ben bestaetigt am 05.11.)")
    json.dump(kat, open(KATALOG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # Kontrollausgabe
    from collections import Counter
    c = Counter(a["typ"] for a in artikel.values())
    print("Artikel:", len(artikel), dict(c))
    print("Ungeklaert:", len(ungeklaert))
    for u in ungeklaert[:60]:
        print("  ", u)
    print("Ausnahmen:", {g: sum(x.values()) for g, x in ausn.items()})


if __name__ == "__main__":
    main()
