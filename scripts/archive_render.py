#!/usr/bin/env python3
"""Sammelt alle Pruefbilder (Renders, Kritiker-Bilder, Schnitte) im Verlauf-Ordner renders/history/.

Aufruf:
  python scripts/archive_render.py <bild.png> [<bild2.png> ...] --role werkstatt --subject pumpe [--note "Kritiker Runde 2"]
  python scripts/archive_render.py --backfill      (einmalig: alle bisherigen Bilder unter renders/ einsortieren)
  python scripts/archive_render.py --rebuild       (nur Galerie und Index neu schreiben)

Ergebnis: renders/history/YYYYMMDD-HHMMSS_<role>_<subject>_<name>.png, renders/history/index.json und
renders/history/index.html (Galerie, neueste zuerst, filterbar). Das Original bleibt liegen (Dokumente verweisen darauf).
Gleiche Bilder (gleicher Hash) werden nicht doppelt abgelegt.
"""
import argparse
import datetime
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HIST = ROOT / "renders" / "history"
INDEX = HIST / "index.json"
EXT = {".png", ".jpg", ".jpeg", ".webp"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def git(*args):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return ""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"


def load():
    if INDEX.exists():
        return json.loads(INDEX.read_text(encoding="utf-8"))
    return []


def add(src, role, subject, note, entries, when=None, commit=None):
    src = Path(src).resolve()
    h = sha(src)
    if any(e["sha"] == h for e in entries):
        return None
    when = when or datetime.datetime.fromtimestamp(src.stat().st_mtime)
    stamp = when.strftime("%Y%m%d-%H%M%S")
    name = f"{stamp}_{slug(role)}_{slug(subject)}_{slug(src.stem)}{src.suffix.lower()}"
    HIST.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, HIST / name)
    e = {
        "file": name, "sha": h, "time": when.strftime("%Y-%m-%d %H:%M:%S"), "role": role,
        "subject": subject, "note": note, "commit": commit if commit is not None else git("rev-parse", "--short", "HEAD"),
        "source": str(src.relative_to(ROOT)).replace("\\", "/") if ROOT in src.parents else str(src),
    }
    entries.append(e)
    return e


def classify(p):
    rel = p.relative_to(ROOT / "renders").parts
    if rel[0] == "components" and len(rel) >= 3:
        note = "Kritiker" if "critic" in rel else ""
        return "werkstatt", rel[1], note
    if rel[0] == "history":
        return None
    stem = p.stem
    if stem.startswith("section"):
        return "montage", "gesamt-schnitt", ""
    if stem.startswith("comp-"):
        return "werkstatt", stem.split("-")[1], ""
    return "montage", "gesamt", ""


def backfill(entries):
    n = 0
    for p in sorted((ROOT / "renders").rglob("*")):
        if p.suffix.lower() not in EXT or HIST in p.parents:
            continue
        c = classify(p)
        if not c:
            continue
        commit = git("log", "-1", "--format=%h", "--", str(p.relative_to(ROOT))) or ""
        if add(p, c[0], c[1], c[2], entries, commit=commit):
            n += 1
    return n


def gallery(entries):
    entries = sorted(entries, key=lambda e: e["time"], reverse=True)
    subjects = sorted({e["subject"] for e in entries})
    roles = sorted({e["role"] for e in entries})
    cards = []
    for e in entries:
        cards.append(
            f'<figure data-subject="{html.escape(e["subject"])}" data-role="{html.escape(e["role"])}">'
            f'<a href="{html.escape(e["file"])}"><img loading="lazy" src="{html.escape(e["file"])}" alt=""></a>'
            f'<figcaption><b>{html.escape(e["subject"])}</b> · {html.escape(e["role"])}<br>{e["time"]}'
            f' · {html.escape(e["commit"])}<br>{html.escape(e["note"])}</figcaption></figure>'
        )
    opts = "".join(f"<option>{html.escape(s)}</option>" for s in subjects)
    ropts = "".join(f"<option>{html.escape(s)}</option>" for s in roles)
    page = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kuppel Bildverlauf</title><style>
:root{{--bg:#fff;--fg:#1b1f24;--mut:#59636e;--card:#f3f4f6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#14171c;--fg:#e6e8eb;--mut:#9aa4af;--card:#1e232a}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:14px system-ui,sans-serif}}
h1{{font-size:18px;margin:0 0 4px}}p{{color:var(--mut);margin:0 0 12px}}
select{{margin-right:8px;font:inherit}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:12px}}
figure{{margin:0;background:var(--card);border-radius:8px;overflow:hidden}}
img{{width:100%;display:block;aspect-ratio:4/3;object-fit:contain;background:#0001}}
figcaption{{padding:8px;font-size:12px;color:var(--mut)}}figcaption b{{color:var(--fg)}}
</style></head><body><h1>Kuppel Bildverlauf</h1>
<p>{len(entries)} Bilder, neueste zuerst. Quelle: renders/history/index.json (scripts/archive_render.py).</p>
<label>Bauteil <select id="s"><option value="">alle</option>{opts}</select></label>
<label>Rolle <select id="r"><option value="">alle</option>{ropts}</select></label>
<main id="m">{''.join(cards)}</main>
<script>
const s=document.getElementById('s'),r=document.getElementById('r');
function f(){{for(const c of document.querySelectorAll('figure'))c.style.display=((!s.value||c.dataset.subject===s.value)&&(!r.value||c.dataset.role===r.value))?'':'none'}}
s.onchange=r.onchange=f;
</script></body></html>"""
    (HIST / "index.html").write_text(page, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="*")
    ap.add_argument("--role", default="montage")
    ap.add_argument("--subject", default="gesamt")
    ap.add_argument("--note", default="")
    ap.add_argument("--backfill", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    a = ap.parse_args()
    HIST.mkdir(parents=True, exist_ok=True)
    entries = load()
    added = 0
    if a.backfill:
        added += backfill(entries)
    for img in a.images:
        if add(img, a.role, a.subject, a.note, entries):
            added += 1
    INDEX.write_text(json.dumps(sorted(entries, key=lambda e: e["time"]), ensure_ascii=False, indent=1), encoding="utf-8")
    gallery(entries)
    print(f"{added} neu, {len(entries)} gesamt -> {HIST / 'index.html'}")


if __name__ == "__main__":
    sys.exit(main())
