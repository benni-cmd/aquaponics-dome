"""N-VARIANTEN V1a: Vergleich A+ gegen Ring B2 -> docs/varianten-vergleich.md (Blatt docs/jobs/N-VARIANTEN.md 1.3, Pruefpunkt P5).

Liest (nur): data/stueckliste.json (A+), data/stueckliste-ring_b2.json, data/system-specs.json, data/system-specs-ring_b2.json.
Schreibt: docs/varianten-vergleich.md. Gleiche Eingabe, gleiche Ausgabe (kein Zeitstempel).
Ist die Stueckliste einer Variante noch nicht erzeugt (Modell der Variante nicht gebaut), steht das im Kopf; die Tabellen bleiben leer.
Aufruf: python -X utf8 scripts/bom_vergleich.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import variante as V  # noqa: E402

ROOT = V.ROOT
A, B = "a_plus", "ring_b2"


def laden(art, v):
    p = V.pfad(art, v, root=ROOT)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def eur(x):
    return "%s EUR" % "{:,.2f}".format(x).replace(",", "X").replace(".", ",").replace("X", ".")


def zeilen_platziert(sl):
    return {z["artikel_id"]: z for z in sl["zeilen"] if not z["nicht_platziert"]}


def preis(z):
    return (z.get("preis") or {}).get("gesamtpreis_eur")


def main():
    sa, sb = laden("stueckliste_json", A), laden("stueckliste_json", B)
    ka, kb = laden("system_specs", A), laden("system_specs", B)
    L = ["# Vergleich Kreislauf A+ und Ring B2 (W70)", "",
         "Erzeugt von `scripts/bom_vergleich.py` aus `data/stueckliste.json` und `data/stueckliste-ring_b2.json` (Mehr und Weniger von Ring B2 gegen A+). Nicht von Hand aendern.", ""]
    if sa is None or sb is None:
        fehlt = [p for p, s in (("data/stueckliste.json", sa), ("data/stueckliste-ring_b2.json", sb)) if s is None]
        L += ["**Stand: Ring B2 noch nicht gebaut.** Es fehlt: %s. Die Stueckliste von Ring B2 entsteht mit `python -X utf8 scripts/bom.py --variante ring_b2`, sobald `viewer/varianten/ring_b2/instances.json` existiert (Montage R1/R2)." % ", ".join(fehlt), ""]
    else:
        pa, pb = zeilen_platziert(sa), zeilen_platziert(sb)
        L += ["## Summe", "", "| | A+ | Ring B2 | Unterschied |", "|---|---|---|---|",
              "| Summe platzierte Zeilen mit Preis | %s | %s | %s |" % (eur(sa["kopf"]["summe_eur_platziert"]), eur(sb["kopf"]["summe_eur_platziert"]), eur(sb["kopf"]["summe_eur_platziert"] - sa["kopf"]["summe_eur_platziert"])),
              "| platzierte Artikel | %d | %d | %+d |" % (len(pa), len(pb), len(pb) - len(pa)),
              "| platzierte Zeilen ohne Preis | %d | %d | %+d |" % (sa["kopf"]["zeilen_ohne_preis_platziert"], sb["kopf"]["zeilen_ohne_preis_platziert"], sb["kopf"]["zeilen_ohne_preis_platziert"] - sa["kopf"]["zeilen_ohne_preis_platziert"]), ""]
        nur_b = sorted(set(pb) - set(pa))
        nur_a = sorted(set(pa) - set(pb))
        gem = sorted(k for k in set(pa) & set(pb) if abs(pb[k]["bedarf"] - pa[k]["bedarf"]) > 1e-9)
        L += ["## Nur in Ring B2 (Mehr)", "", "| Artikel | Bezeichnung | Bedarf | Gesamt |", "|---|---|---|---|"]
        L += ["| `%s` | %s | %s %s | %s |" % (k, pb[k]["bezeichnung"].replace("|", "/"), pb[k]["bedarf"], pb[k]["einheit"], eur(preis(pb[k])) if preis(pb[k]) is not None else "-") for k in nur_b] or ["| - | - | - | - |"]
        L += ["", "## Nur in A+ (Weniger in Ring B2)", "", "| Artikel | Bezeichnung | Bedarf | Gesamt |", "|---|---|---|---|"]
        L += ["| `%s` | %s | %s %s | %s |" % (k, pa[k]["bezeichnung"].replace("|", "/"), pa[k]["bedarf"], pa[k]["einheit"], eur(preis(pa[k])) if preis(pa[k]) is not None else "-") for k in nur_a] or ["| - | - | - | - |"]
        L += ["", "## Anderer Bedarf in beiden", "", "| Artikel | A+ | Ring B2 | Unterschied |", "|---|---|---|---|"]
        L += ["| `%s` | %s %s | %s %s | %+.3f |" % (k, pa[k]["bedarf"], pa[k]["einheit"], pb[k]["bedarf"], pb[k]["einheit"], pb[k]["bedarf"] - pa[k]["bedarf"]) for k in gem] or ["| - | - | - | - |"]
        L.append("")
    L += ["## Kennzahlen (`data/system-specs*.json`, Block `kreislauf`)", ""]
    if ka is None or kb is None or "kreislauf" not in ka or "kreislauf" not in kb:
        L += ["Block `kreislauf` fehlt: `python -X utf8 scripts/system_specs.py` und `... --variante ring_b2` ausfuehren.", ""]
    else:
        a, b = ka["kreislauf"], kb["kreislauf"]
        zeilen = [("Pumpstufen Linienwasser", "pumpstufen_linienwasser"), ("Pumpenleistung elektrisch eta 25 % (W)", "pumpenleistung_el_w_eta25"),
                  ("Pumpenleistung elektrisch eta 18 % (W)", "pumpenleistung_el_w_eta18"), ("Foerderhoehe Hauptpumpe (m)", "foerderhoehe_hauptpumpe_m"),
                  ("Foerderhoehe Booster (m)", "foerderhoehe_booster_m"), ("Graeben Zulauf zu Beeten", "graeben_zulauf_beete"),
                  ("Ring ueber Kopf, Nennlaenge (m)", "ring_nennlaenge_ueber_kopf_m"), ("Rohr ueber Kopf, gemessen (m)", "rohr_ueber_kopf_gemessen_m"),
                  ("Rohrlaenge gesamt, gemessen (m)", "rohrlaenge_m"), ("Wasser in Rohren, gemessen (l)", "wasser_in_rohren_l")]
        fmt = lambda x: "-" if x is None else ("ja" if x is True else "nein" if x is False else str(x))
        L += ["| Kennzahl | A+ | Ring B2 |", "|---|---|---|"] + ["| %s | %s | %s |" % (t, fmt(a.get(k)), fmt(b.get(k))) for t, k in zeilen]
        L += ["", "Herkunft: %s" % a["herkunft"]["pumpenleistung"], "", a["herkunft"]["hinweis"], ""]
    out = V.pfad("vergleich", root=ROOT)
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print("geschrieben:", os.path.relpath(out, ROOT), "| Ring B2 Stueckliste:", "da" if sb else "fehlt")


if __name__ == "__main__":
    main()
