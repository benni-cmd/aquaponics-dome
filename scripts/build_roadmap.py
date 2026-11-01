"""Roadmap-Seite bauen: data/roadmap.json -> roadmap/index.html (eine Datei, Daten inline).

Aufruf: python scripts/build_roadmap.py
Nur Standardbibliothek. Der Orchestrator pflegt data/roadmap.json und fuehrt dieses Skript danach aus.
"""
import json
import sys
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "roadmap.json"
OUT = ROOT / "roadmap" / "index.html"

LABEL = {"erledigt": "erledigt", "laeuft": "läuft", "geplant": "geplant", "entscheidung": "Entscheidung", "luecke": "Lücke"}
STATUS = set(LABEL)
PHASEN = {"vor_zwischencheck", "nach_zwischencheck", "dauerhaft"}

CSS = """
:root{--bg:#f6f7f9;--card:#fff;--text:#1c2330;--muted:#5b6475;--line:#d9dde5;
--ok:#1b7a3d;--ok-bg:#dcf2e2;--run:#8a6200;--run-bg:#fff0b8;--plan:#4a5262;--plan-bg:#e6e9ef;
--ask:#1750b0;--ask-bg:#dce8fd;--pause:#a33a00;--pause-bg:#ffe6d4;--bar:#1b7a3d}
@media (prefers-color-scheme:dark){:root{--bg:#12161d;--card:#1b212b;--text:#e8ebf0;--muted:#9aa4b5;--line:#2e3644;
--ok:#7fd69a;--ok-bg:#16361f;--run:#f2cf6b;--run-bg:#3b2f0a;--plan:#c3cad6;--plan-bg:#2a313d;
--ask:#9cc2ff;--ask-bg:#14284d;--pause:#ffb38a;--pause-bg:#40200c;--bar:#7fd69a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:860px;margin:0 auto;padding:16px}
h1{font-size:1.5rem;margin:8px 0 2px}
h2{font-size:1.2rem;margin:28px 0 8px}
.stand{color:var(--muted);font-size:.9rem;margin:0 0 14px}
.zaehler{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}
.zaehler span{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 12px}
.balken{height:14px;background:var(--plan-bg);border-radius:7px;overflow:hidden}
.balken div{height:100%;background:var(--bar)}
.balkentext{color:var(--muted);font-size:.9rem;margin:4px 0 0}
ol,ul{list-style:none;margin:0;padding:0}
li.schritt{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:0 0 8px;
display:grid;grid-template-columns:auto 1fr;gap:2px 10px;align-items:start}
li.schritt .nr{color:var(--muted);font-variant-numeric:tabular-nums;min-width:1.6em;text-align:right}
li.schritt .titel{font-weight:600;overflow-wrap:anywhere}
li.schritt .meta{grid-column:2;color:var(--muted);font-size:.9rem;overflow-wrap:anywhere}
.marke{display:inline-block;font-size:.78rem;font-weight:600;border-radius:5px;padding:1px 7px;margin-left:6px;white-space:nowrap}
.m-erledigt{color:var(--ok);background:var(--ok-bg)}
.m-laeuft{color:var(--run);background:var(--run-bg)}
.m-geplant{color:var(--plan);background:var(--plan-bg)}
.m-entscheidung{color:var(--ask);background:var(--ask-bg)}
.m-luecke{color:var(--pause);background:var(--pause-bg)}
li.pause{background:var(--pause-bg);border-color:var(--pause);border-width:2px}
li.pause .titel{color:var(--pause)}
details{margin-top:28px}
summary{font-size:1.2rem;font-weight:700;cursor:pointer;margin-bottom:8px}
.leer{color:var(--muted)}
.untertitel{color:var(--muted);font-size:.9rem;margin:12px 0 6px}
@media (max-width:480px){main{padding:16px}}
"""


def fail(msg):
    sys.exit("build_roadmap: " + msg)


def laden():
    daten = json.loads(DATA.read_text(encoding="utf-8"))
    schritte = daten.get("schritte")
    if not isinstance(schritte, list) or not schritte:
        fail("data/roadmap.json hat keine Liste 'schritte'")
    ids = set()
    for s in schritte:
        for k in ("id", "titel", "status", "phase", "reihenfolge", "wer", "notiz"):
            if k not in s:
                fail("Schritt %r: Feld '%s' fehlt" % (s.get("id", "?"), k))
        if s["status"] not in STATUS:
            fail("Schritt %s: unbekannter Status %r" % (s["id"], s["status"]))
        if s["phase"] not in PHASEN:
            fail("Schritt %s: unbekannte Phase %r" % (s["id"], s["phase"]))
        if s["id"] in ids:
            fail("doppelte id " + s["id"])
        ids.add(s["id"])
    return daten.get("stand", ""), schritte


def marke(status):
    return '<span class="marke m-%s">%s</span>' % (status, LABEL[status])


def item(s, nr=None):
    klassen = "schritt" + (" pause" if s["id"] == "PAUSE" else "")
    nummer = "%d." % nr if nr else "•"
    ist_pause = s["id"] == "PAUSE"
    kopf = '<span class="marke m-geplant">PAUSE</span> ' if ist_pause else escape(s["id"]) + ": "
    return (
        '<li class="%s"><span class="nr">%s</span>'
        '<span class="titel">%s%s%s</span>'
        '<span class="meta">%s · %s</span></li>'
        % (klassen, nummer, kopf, escape(s["titel"]), "" if ist_pause else marke(s["status"]),
           escape(s["wer"]), escape(s["notiz"]))
    )


def liste(schritte, nummeriert):
    if not schritte:
        return '<p class="leer">Nichts offen.</p>'
    tag = "ol"
    zeilen = [item(s, i if nummeriert else None) for i, s in enumerate(schritte, 1)]
    return "<%s>%s</%s>" % (tag, "".join(zeilen), tag)


def sortiert(schritte):
    return sorted(schritte, key=lambda s: s["reihenfolge"])


def bauen():
    stand, alle = laden()
    ablauf = [s for s in alle if s["status"] not in ("entscheidung", "luecke") and s["phase"] != "dauerhaft"]
    erledigt = sortiert([s for s in alle if s["status"] == "erledigt"])
    laeuft = sortiert([s for s in alle if s["status"] == "laeuft" and s["phase"] != "dauerhaft"])
    laufend = sortiert([s for s in alle if s["phase"] == "dauerhaft" and s["status"] != "erledigt"])
    vor = sortiert([s for s in alle if s["status"] == "geplant" and s["phase"] == "vor_zwischencheck"])
    nach = sortiert([s for s in alle if s["status"] == "geplant" and s["phase"] == "nach_zwischencheck"])
    fragen = sortiert([s for s in alle if s["status"] == "entscheidung"])
    luecken = sortiert([s for s in alle if s["status"] == "luecke"])

    n_ok = sum(1 for s in ablauf if s["status"] == "erledigt")
    n_run = sum(1 for s in ablauf if s["status"] == "laeuft")
    n_plan = sum(1 for s in ablauf if s["status"] == "geplant")
    gesamt = len(ablauf)
    prozent = round(100 * n_ok / gesamt) if gesamt else 0
    gebaut = datetime.now().strftime("%d.%m.%Y %H:%M")

    arbeit = liste(laeuft, False)
    if laufend:
        arbeit += '<p class="untertitel">Dauerhaft laufend</p>' + liste(laufend, False)

    html = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kuppel Roadmap</title>
<style>%(css)s</style>
</head>
<body>
<main>
<h1>Kuppel Roadmap</h1>
<p class="stand">Stand: %(stand)s · Seite gebaut am %(gebaut)s</p>
<div class="zaehler">
<span>%(n_ok)d erledigt</span><span>%(n_run)d läuft</span><span>%(n_plan)d geplant</span><span>%(n_ask)d Entscheidungen</span><span>%(n_luecke)d Lücken</span>
</div>
<div class="balken" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="%(prozent)d"><div style="width:%(prozent)d%%"></div></div>
<p class="balkentext">%(n_ok)d von %(gesamt)d Schritten erledigt (%(prozent)d %%), ohne Entscheidungen und Dauerhaftes</p>

<h2>Gerade in Arbeit</h2>
%(arbeit)s

<h2>Als Nächstes, in Reihenfolge (vor dem Zwischencheck)</h2>
%(vor)s

<h2>Nach dem Zwischencheck</h2>
%(nach)s

<h2>Deine Entscheidungen</h2>
%(fragen)s

<h2>Offene Lücken und Risiken (nicht verlieren)</h2>
<p class="balkentext">Fehlende Teile, ungeklärte Befunde und Risiken aus den Bauschritten. Sie bleiben hier stehen, bis sie geschlossen oder bewusst verworfen sind.</p>
%(luecken)s

<details>
<summary>Erledigt (%(n_ok)d)</summary>
%(erledigt)s
</details>
</main>
<script type="application/json" id="roadmap-daten">%(daten)s</script>
</body>
</html>
""" % {
        "css": CSS, "stand": escape(stand), "gebaut": gebaut,
        "n_ok": n_ok, "n_run": n_run, "n_plan": n_plan, "n_ask": len(fragen), "n_luecke": len(luecken),
        "prozent": prozent, "gesamt": gesamt,
        "arbeit": arbeit, "vor": liste(vor, True), "nach": liste(nach, True),
        "fragen": liste(fragen, False), "luecken": liste(luecken, False), "erledigt": liste(erledigt, False),
        "daten": json.dumps(alle, ensure_ascii=False).replace("</", "<\\/"),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print("roadmap/index.html: %d erledigt, %d laeuft, %d geplant, %d Entscheidungen, %d Luecken" % (n_ok, n_run, n_plan, len(fragen), len(luecken)))


if __name__ == "__main__":
    bauen()
