#!/usr/bin/env python3
"""Foto-Look-Illustration des Kuppelmodells ueber die lokale ComfyUI-API (SDXL + ControlNet Canny).

Aufruf:
  python scripts/photoreal.py                      alle Kameras aus data/photoreal.json
  python scripts/photoreal.py uebersicht           nur diese Kamera(s)
  python scripts/photoreal.py --stil skizze uebersicht      nur Tuschestrich-Skizze
  python scripts/photoreal.py --seed 7 --staerke 0.7 uebersicht

Ablauf je Kamera: designs/dome.sc (Kopie) -> solidcraft-cli snapshot ohne Haut und Erde (Eingabebild)
-> ComfyUI (Workflow scripts/comfy/workflow_canny.json, Seed aus der Kamera-Tabelle)
-> renders/photoreal/<datum>_<kamera>_<stil>_s<seed>.jpg + .json (Prompt, Seed, Modelle, Eingabe-SHA, Commit).
Das PNG liegt in renders/photoreal/_png/, das Eingabebild in renders/photoreal/_input/ (beide nicht im Repo).
ComfyUI wird gestartet, falls es nicht laeuft, und danach wieder beendet (nur wenn dieses Skript es gestartet hat).
Das Ergebnis ist eine ILLUSTRATION, kein Modellbeleg: Pflanzen, Rasen und Himmel erfindet die KI. Das Modell wird nie veraendert.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "data" / "photoreal.json"
WORKFLOW = ROOT / "scripts" / "comfy" / "workflow_canny.json"
OUT = ROOT / "renders" / "photoreal"
CLI = os.environ.get("SOLIDCRAFT_CLI", r"C:\Program Files\SolidCraft\solidcraft-cli.exe")
COMFY = Path(os.environ.get("COMFYUI_DIR", r"C:\Users\benkn\Tools\ComfyUI\ComfyUI_windows_portable"))
HOST = os.environ.get("COMFYUI_HOST", "http://127.0.0.1:8188")
HINWEIS = "Illustration, kein Modellbeleg (Pflanzen, Rasen, Himmel erfindet die KI)"


def api(path, data=None, timeout=60):
    req = urllib.request.Request(
        HOST + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def server_up():
    try:
        api("/system_stats", timeout=5)
        return True
    except (OSError, urllib.error.URLError):
        return False


def start_server():
    log = open(COMFY / "comfyui-server.log", "w")
    # HIP_VISIBLE_DEVICES=1 (fuer Modly/Hunyuan gesetzt) laesst ComfyUI keine GPU finden: nur fuer dieses Kind-Programm entfernen
    env = {k: v for k, v in os.environ.items() if k != "HIP_VISIBLE_DEVICES"}
    proc = subprocess.Popen(
        [str(COMFY / "python_embeded" / "python.exe"), "-s", "ComfyUI/main.py",
         "--windows-standalone-build", "--port", HOST.rsplit(":", 1)[1]],
        cwd=COMFY, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    for _ in range(90):
        if server_up():
            return proc
        if proc.poll() is not None:
            break
        time.sleep(2)
    proc.terminate()
    sys.exit("ComfyUI startet nicht (siehe comfyui-server.log).")


def upload(path, name):
    """Eingabebild per API hochladen (kein Kopieren in den ComfyUI-Ordner)."""
    boundary = uuid.uuid4().hex
    head = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
            f"Content-Type: image/png\r\n\r\n").encode()
    tail = (f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue"
            f"\r\n--{boundary}--\r\n").encode()
    req = urllib.request.Request(
        HOST + "/upload/image", data=head + Path(path).read_bytes() + tail,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["name"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def git_commit():
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return ""


def snapshot(design, out, camera, cfg):
    """Eingabebild: CAD-Ansicht ohne Haut und Erde. Arbeitet auf einer Kopie des Designs (design) und aendert sie nur im Speicher.
    Erde: browser.visibility (Skript), Haut: Deckkraft 0. Fehlt ein Koerper (Namen aendern sich), wird er ausgelassen."""
    glas = list(cfg["ausblenden_glas"])
    ganz = list(cfg["ausblenden_ganz"])
    for _ in range(len(glas) + len(ganz) + 2):
        script = Path(design).with_name("ausblenden.json")
        script.write_text(json.dumps({"commands": [{"command": "browser.visibility",
                          "params": {"visible": False, "items": ganz}}] if ganz else []}), encoding="utf-8")
        cmd = [CLI, "snapshot", str(script), "--in", str(design), "--out", str(out), "--width", str(cfg["bild"]["breite"]),
               "--height", str(cfg["bild"]["hoehe"]), "--camera", json.dumps(camera), "--no-grid", "--no-axes"]
        for b in glas:
            cmd += ["--body", f"{b}:opacity=0"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if r.returncode == 0 and out.exists():
            return
        msg = r.stderr + r.stdout
        m = re.search(r"no body `([^`]+)`", msg)
        if m and m.group(1) in glas:
            glas.remove(m.group(1))
            continue
        for g in list(ganz):
            if re.search(re.escape(g), msg):
                ganz.remove(g)
                break
        else:
            sys.exit("snapshot fehlgeschlagen: " + msg[-400:])
    sys.exit("snapshot fehlgeschlagen (Koerperliste).")


def build_graph(cfg, stil, prompt_over, seed, image_name):
    g = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    by = {n["_meta"]["title"]: n for n in g.values()}
    p = cfg["stile"][stil]
    by["Prompt positiv"]["inputs"]["text"] = prompt_over.get("positiv", p["positiv"])
    by["Prompt negativ"]["inputs"]["text"] = p["negativ"]
    by["Bildgroesse"]["inputs"].update(width=cfg["bild"]["breite"], height=cfg["bild"]["hoehe"])
    by["Eingabe Modellbild"]["inputs"]["image"] = image_name
    by["Kanten"]["inputs"].update(low_threshold=p["canny_low"], high_threshold=p["canny_high"])
    by["ControlNet anwenden"]["inputs"]["strength"] = prompt_over.get("staerke", p["staerke"])
    by["Sampler"]["inputs"].update(seed=seed, steps=p["schritte"], cfg=p["cfg"])
    return g, by


def run_graph(graph, by):
    pid = api("/prompt", {"prompt": graph})["prompt_id"]
    for _ in range(600):
        hist = api(f"/history/{pid}")
        if pid in hist:
            break
        time.sleep(2)
    else:
        sys.exit("ComfyUI-Zeitlimit (20 min).")
    entry = hist[pid]
    if entry["status"]["status_str"] != "success":
        sys.exit(json.dumps(entry["status"], indent=1)[:800])
    ids = {t: next(k for k, v in graph.items() if v is by[t]) for t in ("Ausgabe", "Ausgabe Kanten")}
    got = {}
    for t, nid in ids.items():
        img = entry["outputs"][nid]["images"][0]
        q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img["subfolder"], "type": img["type"]})
        with urllib.request.urlopen(f"{HOST}/view?{q}", timeout=60) as r:
            got[t] = r.read()
    return got


def model_info(graph, by):
    info = {}
    for key, sub, field in (("checkpoint", "checkpoints", by["Modell"]["inputs"]["ckpt_name"]),
                            ("controlnet", "controlnet", by["ControlNet"]["inputs"]["control_net_name"])):
        f = COMFY / "ComfyUI" / "models" / sub / field
        info[key] = {"datei": field, "bytes": f.stat().st_size if f.exists() else None}
    return info


def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kameras", nargs="*", help="Kameranamen aus data/photoreal.json (leer = alle)")
    ap.add_argument("--stil", help="Stile aus data/photoreal.json, mit Komma getrennt (foto,skizze); Standard: stile_standard")
    ap.add_argument("--seed", type=int, help="statt des Seeds aus der Tabelle")
    ap.add_argument("--staerke", type=float, help="ControlNet-Staerke statt Tabellenwert")
    ap.add_argument("--prompt", help="positiver Prompt statt Tabellenwert")
    ap.add_argument("--design", default=str(ROOT / "designs" / "dome.sc"))
    ap.add_argument("--neu", action="store_true", help="Eingabebild neu rendern, auch wenn aktuell")
    ap.add_argument("--keep", action="store_true", help="ComfyUI nicht beenden")
    a = ap.parse_args()

    stile = a.stil.split(",") if a.stil else cfg["stile_standard"]
    for st in stile:
        if st not in cfg["stile"]:
            sys.exit(f"Unbekannter Stil {st}; vorhanden: {', '.join(cfg['stile'])}")
    names = a.kameras or list(cfg["kameras"])
    for n in names:
        if n not in cfg["kameras"]:
            sys.exit(f"Unbekannte Kamera {n}; vorhanden: {', '.join(cfg['kameras'])}")

    inp, png = OUT / "_input", OUT / "_png"
    for d in (OUT, inp, png):
        d.mkdir(parents=True, exist_ok=True)
    design = Path(a.design)
    over = {k: v for k, v in (("positiv", a.prompt), ("staerke", a.staerke)) if v is not None}

    # 1) Eingabebilder (Kopie des Designs, damit ein gleichzeitiges Speichern nicht stoert)
    ready = {}
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "dome.sc"
        for n in names:
            img = inp / f"{n}.png"
            if a.neu or not img.exists() or img.stat().st_mtime < design.stat().st_mtime:
                if not copy.exists():
                    shutil.copy(design, copy)
                print(f"[{n}] Eingabebild rendern ...", flush=True)
                snapshot(copy, img, cfg["kameras"][n]["camera"], cfg)
            ready[n] = img

    # 2) ComfyUI
    proc = None
    if not server_up():
        print("ComfyUI starten ...", flush=True)
        proc = start_server()
    stats = api("/system_stats")
    try:
        stamp = datetime.date.today().strftime("%Y%m%d")
        for n in names:
            seed = a.seed if a.seed is not None else cfg["kameras"][n]["seed"]
            name = upload(ready[n], f"dome_{n}.png")
            for st in stile:
                graph, by = build_graph(cfg, st, over, seed, name)
                print(f"[{n}/{st}] ComfyUI rechnet (Seed {seed}) ...", flush=True)
                t0 = time.time()
                got = run_graph(graph, by)
                base = f"{stamp}_{n}_{st}_s{seed}"
                (png / f"{base}.png").write_bytes(got["Ausgabe"])
                (png / f"{base}_kanten.png").write_bytes(got["Ausgabe Kanten"])
                try:
                    from PIL import Image
                    Image.open(png / f"{base}.png").convert("RGB").save(OUT / f"{base}.jpg", quality=90)
                except ImportError:
                    shutil.copy(png / f"{base}.png", OUT / f"{base}.png")
                (OUT / f"{base}.json").write_text(json.dumps({
                    "hinweis": HINWEIS, "kamera": n, "stil": st, "kamera_parameter": cfg["kameras"][n]["camera"], "seed": seed,
                    "prompt_positiv": by["Prompt positiv"]["inputs"]["text"], "prompt_negativ": by["Prompt negativ"]["inputs"]["text"],
                    "controlnet_staerke": by["ControlNet anwenden"]["inputs"]["strength"], "schritte": by["Sampler"]["inputs"]["steps"],
                    "cfg": by["Sampler"]["inputs"]["cfg"], "canny": [by["Kanten"]["inputs"]["low_threshold"], by["Kanten"]["inputs"]["high_threshold"]],
                    "modelle": model_info(graph, by), "comfyui_version": stats.get("system", {}).get("comfyui_version"),
                    "eingabe_sha256_16": sha(ready[n]), "design_mtime": datetime.datetime.fromtimestamp(design.stat().st_mtime).isoformat(timespec="seconds"),
                    "commit": git_commit(), "dauer_s": round(time.time() - t0, 1),
                }, indent=1, ensure_ascii=False), encoding="utf-8")
                print(f"[{n}/{st}] fertig: renders/photoreal/{base}.jpg  ({HINWEIS})", flush=True)
    finally:
        if proc is not None and not a.keep:
            proc.terminate()


if __name__ == "__main__":
    main()
