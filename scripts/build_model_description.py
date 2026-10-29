#!/usr/bin/env python3
"""Aktualisiert den Kennzahlen-Block in docs/model-description.md (zwischen den Marken KENNZAHLEN-START/-ENDE).
Aufruf: python scripts/build_model_description.py
Zaehlt nur, was im Repo liegt (Dateien, Entscheidungen, Bilder, Commits); Text und Pruefstand pflegt der Orchestrator von Hand."""
import datetime
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "model-description.md"


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, timeout=60).stdout.strip()


def count(pattern):
    return len(list(ROOT.glob(pattern)))


def main():
    comps = [p for p in (ROOT / "designs" / "components").glob("*.sc")]
    classes = sorted({re.sub(r"(_[a-z]*\d+.*|_(innen|mitte|aussen|klein|gross|t3).*)$", "", p.stem) for p in comps})
    decisions = len(re.findall(r"^\| D\d+", (ROOT / "docs" / "decisions.md").read_text(encoding="utf-8"), re.M))
    first = git("log", "--reverse", "--format=%ad", "--date=format:%d.%m.%Y %H:%M").splitlines()[0]
    last = git("log", "-1", "--format=%ad", "--date=format:%d.%m.%Y %H:%M")
    rows = [
        ("Stand", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
        ("Komponenten-Definitionen (`designs/components/*.sc`)", count("designs/components/*.sc")),
        ("Bauteilklassen (grob nach Dateiname)", len(classes)),
        ("Bauteilblaetter mit Herkunftstabelle (`docs/parts/*.md`)", count("docs/parts/*.md")),
        ("Entscheidungen (`docs/decisions.md`)", decisions),
        ("Recherchen (`docs/research/R*.md`)", count("docs/research/R*.md")),
        ("Pruefskripte (`scripts/check_*.py`, `scripts/workshop/check_*.py`)", count("scripts/check_*.py") + count("scripts/workshop/check_*.py")),
        ("Pruefbilder im Verlauf (`renders/history`)", count("renders/history/*.png")),
        ("Commits", git("rev-list", "--count", "HEAD")),
        ("Erster / letzter Commit", f"{first} / {last}"),
    ]
    block = "| Kennzahl | Wert |\n|---|---|\n" + "\n".join(f"| {k} | {v} |" for k, v in rows)
    text = DOC.read_text(encoding="utf-8")
    new = re.sub(r"(<!-- KENNZAHLEN-START -->).*?(<!-- KENNZAHLEN-ENDE -->)", lambda m: m.group(1) + "\n" + block + "\n" + m.group(2), text, flags=re.S)
    DOC.write_text(new, encoding="utf-8")
    print("Kennzahlen aktualisiert:", len(rows), "Zeilen")


if __name__ == "__main__":
    main()
