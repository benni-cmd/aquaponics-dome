"""Bauteilblatt docs/parts/<klasse>.md aus data/components/<klasse>.json (Parameter, Text-Block 'blatt') und der gemessenen .sc (Masse, Volumen, Boxen).
Aufruf: python scripts/workshop/partsheet.py <klasse> [kritiker-urteil-text]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import json

def main(name):
    d = json.load(open(os.path.join(sc.ROOT, "data", "components", name + ".json"), encoding="utf-8"))
    bl = d.get("blatt", {})
    main_sc = os.path.join(sc.ROOT, "designs", "components", name + ".sc")
    if not os.path.exists(main_sc):                       # Klassen mit Typ-Dateien: erste Variante als Hauptmessung
        main_sc = os.path.join(sc.ROOT, "designs", "components", bl["varianten"][0] + ".sc")
    ev = sc.evaluate(main_sc)
    mn, mx = sc.bbox_all(ev)
    sep = bl.get("massen_getrennt", [])                  # Koerper, die nicht zur Leermasse zaehlen (z. B. Medium)
    isep = lambda b: any(b["name"].startswith(x) and not b["name"].startswith("Medienschutz") for x in sep)
    mass = sum(b["mass_g"] for b in ev["bodies"] if not isep(b))
    vol = sum(b["volume_mm3"] for b in ev["bodies"] if not isep(b))
    L = []
    L.append(f"# Bauteilblatt {d['teilenummer']} {name} (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/{name}.json` und `designs/components/{name}.sc`, nicht von Hand aendern)\n")
    L.append(f"**Funktion:** {bl.get('funktion', d['beschreibung'])}\n")
    L.append(f"**Datei:** `designs/components/{name}.sc` · **Teilenummer:** {d['teilenummer']} · **Revision:** A · **Bezugspunkt:** {d['bezugspunkt']}\n")
    L.append(f"**Anzahl (Instanzen):** {d['anzahl']['soll']} (Quelle: {d['anzahl']['quelle']})\n")
    L.append("## Masse und Parameter\n")
    L.append("| Parameter | Wert | Einheit | Herkunft |\n|---|---|---|---|")
    for k, v in d["parameter"].items():
        L.append(f"| `{k}` | {v['wert']} | {v['einheit']} | {v['herkunft']} |")
    if d.get("typen"):
        cols = []
        for v in d["typen"].values():
            cols += [c for c in v if c not in cols]
        L.append("\n| Typ | " + " | ".join(cols) + " |\n|---|" + "---|" * len(cols))
        for k, v in d["typen"].items():
            L.append(f"| {k} | " + " | ".join(str(v.get(c, "")) for c in cols) + " |")
    L.append(f"\nGesamt-Box (Messung): X {mn[0]:.1f} bis {mx[0]:.1f}, Y {mn[1]:.1f} bis {mx[1]:.1f}, Z {mn[2]:.1f} bis {mx[2]:.1f} mm; Koerper: {len(ev['bodies'])}.\n")
    if bl.get("toleranzen"):
        L.append(f"**Toleranzen / Spiel:** {bl['toleranzen']}\n")
    L.append("## Werkstoff und Gewicht\n")
    w = d["werkstoff"]
    L.append(f"- Werkstoff: {w['name']}, Dichte {w['dichte_g_cm3']} g/cm3, Farbe {w['farbe']} ({w['herkunft']})")
    L.append(f"- Volumen (Messung, `solidcraft-cli eval`): {vol/1000:.1f} cm3 · Masse leer{' (ohne ' + ', '.join(sep) + ')' if sep else ''}: {mass:.0f} g ({mass/1000:.2f} kg)")
    for v in bl.get("varianten", []):
        evv = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", v + ".sc"))
        L.append(f"- Variante `{v}`: {sum(b['mass_g'] for b in evv['bodies'])/1000:.2f} kg leer")
    if bl.get("gewicht_gefuellt"):
        L.append(f"- Gefuellt/in Betrieb: {bl['gewicht_gefuellt']}")
    if bl.get("querschnitt"):
        L.append(f"\n## Querschnitt / Profil\n\n{bl['querschnitt']}")
    if bl.get("ports"):
        L.append("\n## Ports (Anschluesse)\n\n| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |\n|---|---|---|---|")
        for p in bl["ports"]:
            L.append("| " + " | ".join(p) + " |")
    if bl.get("verbindungen"):
        L.append("\n## Verbindungen und Befestigungen\n")
        L += [f"- {x}" for x in bl["verbindungen"]]
    L.append("\n## Herkunft (docs/provenance.md)\n\n| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |\n|---|---|---|---|---|")
    for r in d.get("herkunft_tabelle", []):
        L.append("| " + " | ".join(r) + " |")
    L.append("\n## Referenz und Abweichung zum OBJ\n")
    L.append(f"- Referenzbild: {bl.get('referenz', 'reference/ref-6-grow-tables-detail.jpg')}")
    L.append(f"- Quelle der Masse: {d['quelle_masse']}")
    if bl.get("abweichung"):
        L.append(f"- Abweichung zum OBJ: {bl['abweichung']}")
    L.append("\n## Montage (L4)\n")
    L += [f"{i+1}. {s}" for i, s in enumerate(bl.get("montage", ["offen"]))]
    if bl.get("werkzeug"):
        L.append(f"\n**Werkzeug:** {bl['werkzeug']}")
    if bl.get("stueckliste"):
        L.append("\n## Stueckliste-Zeile\n")
        L += [f"- {x}" for x in bl["stueckliste"]]
    if bl.get("lokal"):
        L.append(f"\n## Alternative lokale Fertigung\n\n{bl['lokal']}")
    L.append("\n## Renders\n")
    base = os.path.join(sc.ROOT, "renders", "components")
    for dn in sorted(x for x in os.listdir(base) if x == name or x.startswith(name + "_")):
        L += [f"- `renders/components/{dn}/{f}`" for f in sorted(os.listdir(os.path.join(base, dn))) if f.endswith(".png")]
    L.append("\n## Pruefung\n")
    L.append(f"- Gauntlet-Urteil: {sys.argv[2] if len(sys.argv) > 2 else bl.get('kritiker', 'offen')}")
    L += [f"- {x}" for x in bl.get("pruefung", [])]
    L.append("\n## Offene Fragen\n")
    L += [f"- {x}" for x in bl.get("offen", ["keine"])]
    os.makedirs(os.path.join(sc.ROOT, "docs", "parts"), exist_ok=True)
    open(os.path.join(sc.ROOT, "docs", "parts", name + ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("docs/parts/%s.md: %.0f g, %.1f cm3" % (name, mass, vol/1000))

if __name__ == "__main__":
    main(sys.argv[1])
