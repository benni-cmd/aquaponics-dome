"""Inventur des Gesamtmodells (N-MODELL-KOMPLETT Schritt 1): welche Komponenten stehen im Modell, mit welchem Werkstoff?
Quelle: viewer/instances.json (Definitionen + Instanzen), designs/components/*.sc (je `solidcraft-cli eval`).
Schreibt docs/model-inventar.md. Aufruf: python -X utf8 scripts/model_inventar.py
Kennzahlen am Ende der Ausgabe: 'eingesetzt mit Default ausser Ausnahmeliste: N' (Soll 0)."""
import json, os, re, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "workshop"))
import sc, subprocess, tempfile
CACHE = os.path.join(os.environ.get("WORKSHOP_TMP", tempfile.gettempdir()), "model_inventar_cache.json")
try:
    _cache = json.load(open(CACHE, encoding="utf-8"))
except Exception:
    _cache = {}

def ev_cached(path, limit=90):
    """eval mit Zeitgrenze und Zwischenspeicher (Schluessel Pfad + Aenderungszeit); None bei Zeitueberschreitung."""
    key = path + "|" + str(os.path.getmtime(path))
    if key in _cache:
        return _cache[key]
    try:
        r = subprocess.run([sc.CLI, "eval", path], capture_output=True, text=True, timeout=limit)
    except subprocess.TimeoutExpired:
        print("ZEIT", os.path.basename(path), file=sys.stderr, flush=True)
        return None
    if r.returncode != 0:
        return None
    ev = json.loads(r.stdout)
    _cache[key] = {"bodies": [{"name": b["name"], "material": b.get("material", "?"), "mass_g": b.get("mass_g", 0)} for b in ev["bodies"]]}
    json.dump(_cache, open(CACHE, "w", encoding="utf-8"))
    print("ok", os.path.basename(path), file=sys.stderr, flush=True)
    return _cache[key]

ROOT = sc.ROOT
# Ausnahmeliste (Owner-Auftrag): kein Katalog-Werkstoff gewollt
AUSNAHMEN = {
    "mensch_referenz": "Menschfigur (Massstab, kein Bauteil)",
    "erdflaeche": "Erde mit Grund (Bodenflaeche, kein Kaufteil)",
}

def main():
    inst = json.load(open(os.path.join(ROOT, "viewer", "instances.json"), encoding="utf-8"))
    count = collections.Counter(x["d"] for x in inst["instances"])
    defs = sorted(inst["defs"])
    comp_dir = os.path.join(ROOT, "designs", "components")
    alle_sc = sorted(f[:-3] for f in os.listdir(comp_dir) if f.endswith(".sc"))
    zeilen, ohne_sc, zeit = [], [], []
    for d in defs:
        p = os.path.join(comp_dir, d + ".sc")
        if not os.path.exists(p):
            ohne_sc.append(d)
            continue
        ev = ev_cached(p)
        if ev is None:
            zeit.append(d)
            continue
        mats = collections.Counter(b.get("material", "?") for b in ev["bodies"])
        n_body = len([b for b in ev["bodies"] if re.fullmatch(r"Body\d+", b["name"])])
        zeilen.append({"d": d, "n": count[d], "koerper": len(ev["bodies"]), "mats": dict(mats),
                       "default": mats.get("Default", 0), "body": n_body, "mass_kg": sum(b.get("mass_g", 0) for b in ev["bodies"]) / 1000})
    ohne_inst = [c for c in alle_sc if c not in set(defs)]
    ohne_inst_info = {}
    for c in ohne_inst:
        ev = ev_cached(os.path.join(comp_dir, c + ".sc"))
        if ev is None:
            ohne_inst_info[c] = (0, {"nicht ausgewertet (Zeit)": 0})
            continue
        mats = collections.Counter(b.get("material", "?") for b in ev["bodies"])
        ohne_inst_info[c] = (len(ev["bodies"]), dict(mats))
    default_ok = [z for z in zeilen if z["default"] and z["d"] not in AUSNAHMEN]
    default_ausn = [z for z in zeilen if z["default"] and z["d"] in AUSNAHMEN]
    L = ["# Modell-Inventar (erzeugt, nicht von Hand)", "",
         "Erzeugt von `scripts/model_inventar.py` (`python -X utf8 scripts/model_inventar.py`). Quelle: `viewer/instances.json` (Stand "
         + str(inst.get("built")) + "), `designs/components/*.sc` je `solidcraft-cli eval`.", "",
         f"- Definitionen im Modell: **{len(defs)}** (davon ohne gleichnamige `.sc`: {len(ohne_sc)})",
         f"- Instanzen gesamt: {sum(count.values())}",
         f"- `.sc`-Dateien insgesamt: {len(alle_sc)}; davon ohne Instanz im Modell: **{len(ohne_inst)}**",
         f"- Eingesetzte Komponenten mit Werkstoff `Default` ausser Ausnahmeliste: **{len(default_ok)}**",
         f"- Eingesetzte Komponenten mit Werkstoff `Default` in der Ausnahmeliste: {len(default_ausn)} ({', '.join(z['d'] for z in default_ausn) or '-'})",
         f"- Eingesetzte Komponenten mit unbenannten Koerpern `Body<n>`: {len([z for z in zeilen if z['body']])}", ""]
    L += ["## Ausnahmeliste Werkstoff `Default`", ""] + [f"- `{k}`: {v}" for k, v in AUSNAHMEN.items()] + [""]
    L += ["## Komponenten ohne Instanz im Modell", "", "| Datei | Koerper | Werkstoffe |", "|---|---|---|"]
    for c, (n, m) in ohne_inst_info.items():
        L.append(f"| `{c}.sc` | {n} | {', '.join(f'{k} ({v})' for k, v in m.items())} |")
    L += ["", "## Eingesetzte Komponenten", "", "| Komponente | Instanzen | Koerper | Masse kg | Werkstoffe | Default | Body<n> |", "|---|---:|---:|---:|---|---:|---:|"]
    for z in zeilen:
        flag = z["default"] and z["d"] not in AUSNAHMEN
        L.append(f"| `{z['d']}` | {z['n']} | {z['koerper']} | {z['mass_kg']:.1f} | "
                 + ", ".join(f"{k} ({v})" for k, v in z["mats"].items()) + f" | {'**' + str(z['default']) + '**' if flag else z['default']} | {z['body']} |")
    if zeit:
        L += ["", "## Nicht ausgewertet (eval ueber 90 s)", ""] + [f"- `{d}` ({count[d]} Instanzen)" for d in zeit]
    if ohne_sc:
        L += ["", "## Definitionen ohne `.sc`", ""] + [f"- `{d}`" for d in ohne_sc]
    open(os.path.join(ROOT, "docs", "model-inventar.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"Definitionen {len(defs)}, ohne .sc {len(ohne_sc)}, .sc ohne Instanz {len(ohne_inst)}")
    print(f"nicht ausgewertet (Zeit): {len(zeit)} {zeit}")
    print(f"eingesetzt mit Default ausser Ausnahmeliste: {len(default_ok)}")
    for z in default_ok:
        print("  Default:", z["d"], z["mats"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
