"""N-PREIS-PRUEF Messlauf: prueft jeden Bestell-Link der Einkaufsliste und schreibt eine Plausibilitaetsliste je Zeile.

Aufruf:
  python -X utf8 scripts/check_links.py              # Messlauf, schreibt docs/preis-pruefung-links.md und data/preis_pruefung_links.json
  python -X utf8 scripts/check_links.py --ohne-netz  # nur Plausibilitaetsliste, Links ungeprueft

Nur Standardbibliothek. Ruft jede URL einmal per GET ab (nichts kaufen, keine Anmeldung, keine Formulare).
Quelle: data/stueckliste.json (preis.url und alternativen[].url je Zeile; Bezugsdatei steht in quelle_preis).

Urteil je Link:
  FEHLER     HTTP >= 400 (ausser 401/403/429), Netzfehler, oder Weiterleitung auf Startseite/Suche/Kategorie
  GESPERRT   HTTP 401/403/429 oder Bot-Schutz: Seite fuer Skripte nicht lesbar, von Hand pruefen
  VERDACHT   Seite geladen, nennt aber die Kennmasse des Artikels nicht in Titel oder URL (Zahlen aus Bezeichnung/Massen),
             oder die Bemerkung des Angebots sagt selbst ERSATZ/nicht passend
  OK         Seite geladen, Kennmasse gefunden
"""
import concurrent.futures as cf
import gzip
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zlib
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
SUCHE = re.compile(r"(/search|/suche|[?&](q|query|search|s|keyword|k)=|/s\?|/sch/|/kategorie|/category|/c/)", re.I)
BOT = re.compile(r"(captcha|cf-chl|challenge-platform|access denied|zugriff verweigert|are you a robot|px-captcha)", re.I)
ERSATZ = re.compile(r"(ERSATZ|nicht \d|nicht passend|nicht belegt|nicht lebensmittel|Platzhalter)", re.I)
WASSER_TYPEN = {"ROH", "FIT", "ARM", "BEH", "PMP", "FOL", "GEW", "TOP", "BLE", "PRF", "MES", "SON"}
EUROPA = {"DE", "AT", "NL", "BE", "FR", "IT", "ES", "PL", "CZ", "DK", "SE", "FI", "HU", "CH", "LU", "SI", "SK", "PT", "IE", "EU", "UK", "GB"}


def jl(p):
    return json.load(open(p, encoding="utf-8"))


def kennzahlen(zeile):
    """Zahlen, die eine passende Produktseite nennen sollte (Durchmesser, Querschnitt)."""
    txt = zeile.get("bezeichnung", "") + " " + zeile.get("artikel_id", "")
    zahlen = set(re.findall(r"(?<![\d.,])(\d{2,4})(?![\d])", txt))
    for k, v in (zeile.get("masse") or {}).items():
        if isinstance(v, (int, float)) and v >= 10 and float(v).is_integer():
            zahlen.add(str(int(v)))
    return sorted(zahlen)


def links(zeilen):
    out = []
    for z in zeilen:
        p = z.get("preis") or {}
        angebote = ([dict(p, _rang="1")] if p.get("url") else []) + [
            dict(a, _rang=str(i + 2)) for i, a in enumerate(z.get("alternativen", [])) if a.get("url")]
        for a in angebote:
            out.append({"artikel_id": z["artikel_id"], "bezeichnung": z.get("bezeichnung", ""),
                        "datei": z.get("quelle_preis") or "-", "rang": a["_rang"], "url": a["url"],
                        "haendler": a.get("haendler", ""), "land": a.get("land", ""),
                        "bemerkung": a.get("bemerkung", ""), "kenn": kennzahlen(z)})
    return out


def lesen(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*",
                                               "Accept-Language": "de-DE,de;q=0.9,en;q=0.5",
                                               "Accept-Encoding": "gzip, deflate"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            roh = r.read(3_000_000)
            enc = (r.headers.get("Content-Encoding") or "").lower()
            if enc == "gzip":
                roh = gzip.decompress(roh)
            elif enc == "deflate":
                roh = zlib.decompress(roh)
            return r.status, r.geturl(), roh.decode(r.headers.get_content_charset() or "utf-8", "replace"), ""
    except urllib.error.HTTPError as e:
        try:
            text = e.read(500_000).decode("utf-8", "replace")
        except Exception:
            text = ""
        return e.code, e.geturl() if hasattr(e, "geturl") else url, text, ""
    except Exception as e:  # Netzfehler, Zeitueberschreitung, TLS
        return 0, url, "", type(e).__name__ + ": " + str(e)[:80]


def urteil(l, status, ziel, text, fehler):
    a, b = urllib.parse.urlsplit(l["url"]), urllib.parse.urlsplit(ziel)
    titel = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    titel = html.unescape(re.sub(r"\s+", " ", titel.group(1))).strip()[:90] if titel else ""
    if fehler:
        return "FEHLER", "Netz: " + fehler, titel
    if status in (401, 403, 429) or (status >= 400 and BOT.search(text[:20000])):
        return "GESPERRT", f"HTTP {status}", titel
    if status >= 400:
        return "FEHLER", f"HTTP {status}", titel
    if ziel != l["url"]:
        if b.path in ("", "/") or (len(b.path) < len(a.path) // 2 and not b.query):
            return "FEHLER", "Weiterleitung auf Startseite/Oberseite: " + ziel[:80], titel
        if SUCHE.search(b.path + "?" + b.query) and not SUCHE.search(a.path + "?" + a.query):
            return "FEHLER", "Weiterleitung auf Suche/Kategorie: " + ziel[:80], titel
    if BOT.search(text[:20000]) and len(text) < 40000:
        return "GESPERRT", "Bot-Schutz", titel
    sicht = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", text)))
    sicht = sicht + " " + titel + " " + urllib.parse.unquote(ziel)
    def da(k, t):
        return re.search(r"(?<!\d)" + k + r"(?!\d)", t)
    kopfzeile = titel + " " + urllib.parse.unquote(ziel)
    fehlt = [k for k in l["kenn"] if not da(k, sicht)]
    nur_text = [k for k in l["kenn"] if k not in fehlt and not da(k, kopfzeile)]
    if re.search(r"(nicht (mehr )?verf(ue|ü)gbar|ausverkauft|out of stock|nicht lieferbar|404|seite nicht gefunden|page not found)",
                 titel, re.I):
        return "FEHLER", "Seite meldet nicht verfuegbar/404 im Titel", titel
    gruende = []
    if fehlt:
        gruende.append("Kennmass fehlt auf der Seite: " + ", ".join(fehlt))
    if nur_text:
        gruende.append("Kennmass nicht in Titel/URL (nur im Seitentext): " + ", ".join(nur_text))
    if ERSATZ.search(l["bemerkung"]):
        gruende.append("Bemerkung: " + ERSATZ.search(l["bemerkung"]).group(0))
    if gruende:
        return "VERDACHT", "; ".join(gruende), titel
    return "OK", f"HTTP {status}", titel


def plausi(z):
    """Plausibilitaet je Zeile: Funktion, Mass, Einheit, Werkstoff, Lebensmitteleignung, Europa-Bezug."""
    p = z.get("preis") or {}
    bem = (p.get("bemerkung") or "") + " " + " ".join(a.get("bemerkung", "") for a in z.get("alternativen", []))
    masse = ", ".join(f"{k}={v}" for k, v in (z.get("masse") or {}).items()) or "-"
    wasser = z.get("typ") in WASSER_TYPEN
    verneint = re.search(r"nicht[^.;]{0,40}(lebensmittel|trinkwasser|food)", bem, re.I)
    lm = "-" if not wasser else ("OFFEN (Bemerkung verneint)" if verneint else "belegt" if re.search(r"(lebensmittel|trinkwasser|KTW|W270|food|LFGB|1935/2004|DVGW|ACS)", bem, re.I) else "OFFEN")
    land = (p.get("land") or "").split()[0].strip("(),") if p.get("land") else ""
    eu = "-" if not p else ("ja" if land.upper() in EUROPA else "NEIN/unklar: " + (p.get("land") or "?"))
    ersatz = "ERSATZ" if ERSATZ.search(bem) else ""
    return {"artikel_id": z["artikel_id"], "bezeichnung": z.get("bezeichnung", ""), "typ": z.get("typ"),
            "datei": z.get("quelle_preis") or "-", "masse": masse, "einheit": z.get("einheit", ""),
            "werkstoff": z.get("werkstoff") or "-", "lebensmittel": lm, "europa": eu,
            "konfidenz": p.get("konfidenz", "-"), "ersatz": ersatz, "bedarf": z.get("bedarf", 0),
            "status": z.get("status", "")}


def zelle(s):
    return str(s).replace("|", "/").replace("\n", " ")


def main():
    netz = "--ohne-netz" not in sys.argv
    sl = jl(os.path.join(ROOT, "data", "stueckliste.json"))
    zeilen = sl["zeilen"]
    ll = links(zeilen)
    urls = sorted({l["url"] for l in ll})
    roh = {}
    if netz:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            for u, r in zip(urls, ex.map(lesen, urls)):
                roh[u] = r
    for l in ll:
        if netz:
            st, ziel, text, fe = roh[l["url"]]
            l["status"], l["ziel"] = st, ziel
            l["urteil"], l["grund"], l["titel"] = urteil(l, st, ziel, text, fe)
        else:
            l.update(status="-", ziel="", urteil="UNGEPRUEFT", grund="", titel="")
    pl = [plausi(z) for z in zeilen]
    zaehl = Counter(l["urteil"] for l in ll)
    mit_link = sum(1 for z in zeilen if (z.get("preis") or {}).get("url") or any(a.get("url") for a in z.get("alternativen", [])))
    kopf = sl.get("kopf", {})
    json.dump({"stand_stueckliste": kopf.get("erzeugt") or kopf.get("stand"), "zeilen": len(zeilen),
               "zeilen_mit_link": mit_link, "links": len(ll), "urls_eindeutig": len(urls),
               "urteile": dict(zaehl), "link_liste": [{k: v for k, v in l.items() if k != "kenn"} for l in ll],
               "plausi": pl},
              open(os.path.join(ROOT, "data", "preis_pruefung_links.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    reihen = {"FEHLER": 0, "GESPERRT": 1, "VERDACHT": 2, "OK": 3, "UNGEPRUEFT": 4}
    o = ["# Preis-Pruefung: Link-Messlauf und Plausibilitaet (N-PREIS-PRUEF)", "",
         "Erzeugt von `python -X utf8 scripts/check_links.py` aus `data/stueckliste.json`; Rohdaten `data/preis_pruefung_links.json`.",
         "Nicht von Hand bearbeiten: neu erzeugen. Urteile: FEHLER (404/Netz/Weiterleitung auf Startseite, Suche, Kategorie), "
         "GESPERRT (Seite blockt Skripte, von Hand oeffnen), VERDACHT (Kennmass des Artikels fehlt auf der Seite oder steht nicht in Titel/URL, oder Bemerkung sagt ERSATZ), OK.", "",
         "## Zahlen", "",
         f"- Zeilen der Stueckliste: {len(zeilen)}; Zeilen mit mindestens einem Link: {mit_link}",
         f"- Links (Haupt- und Alternativangebote): {len(ll)}; eindeutige URLs: {len(urls)}"]
    o += [f"- {k}: {zaehl.get(k, 0)}" for k in reihen if zaehl.get(k)]
    o += [f"- Zeilen ohne Link: {len(zeilen) - mit_link}",
          f"- Plausibilitaet: Lebensmittel OFFEN {sum(1 for p in pl if p['lebensmittel'].startswith('OFFEN'))}, "
          f"belegt {sum(1 for p in pl if p['lebensmittel'] == 'belegt')}; Europa NEIN/unklar {sum(1 for p in pl if p['europa'].startswith('NEIN'))}; "
          f"Ersatz laut Bemerkung {sum(1 for p in pl if p['ersatz'])}"]
    gr = Counter((l["datei"], l["urteil"]) for l in ll)
    o += ["", "| Bezugsdatei | FEHLER | GESPERRT | VERDACHT | OK |", "|---|---|---|---|---|"]
    for d in sorted({l["datei"] for l in ll}):
        o.append(f"| {d} | " + " | ".join(str(gr.get((d, k), 0)) for k in ("FEHLER", "GESPERRT", "VERDACHT", "OK")) + " |")
    o += ["", "## Links je Angebot", "", "Rang 1 = Hauptangebot (Preis der Liste), 2+ = Alternativen.", "",
          "| Urteil | Artikel | Rang | Haendler | HTTP | Grund | Seitentitel | URL |", "|---|---|---|---|---|---|---|---|"]
    for l in sorted(ll, key=lambda l: (reihen[l["urteil"]], l["datei"], l["artikel_id"], l["rang"])):
        o.append("| " + " | ".join(zelle(x) for x in (l["urteil"], l["artikel_id"], l["rang"], l["haendler"][:30], l["status"],
                                                         l["grund"], l["titel"][:60], l["url"])) + " |")
    o += ["", "## Plausibilitaet je Zeile", "",
          "Lebensmittel: nur fuer Typen mit Wasser- oder Pflanzenkontakt (ROH, FIT, ARM, BEH, PMP, FOL, GEW, TOP, BLE, PRF, MES, SON); "
          "`belegt` = Bemerkung nennt Trinkwasser/Lebensmittel/KTW/W270/LFGB/1935/2004, sonst OFFEN. Europa nach Land des Hauptangebots (D76).", "",
          "| Artikel | Bezeichnung | Datei | Mass | Einheit | Werkstoff | Lebensmittel | Europa | Konfidenz | Ersatz | Bedarf |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for p in sorted(pl, key=lambda p: (p["datei"], p["artikel_id"])):
        o.append("| " + " | ".join(zelle(x) for x in (p["artikel_id"], p["bezeichnung"][:50], p["datei"], p["masse"][:40], p["einheit"],
                                                         p["werkstoff"], p["lebensmittel"], p["europa"], p["konfidenz"], p["ersatz"],
                                                         round(p["bedarf"], 2))) + " |")
    open(os.path.join(ROOT, "docs", "preis-pruefung-links.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")
    print(f"Zeilen {len(zeilen)}, mit Link {mit_link}, Links {len(ll)}, URLs {len(urls)}, Urteile {dict(zaehl)}")


if __name__ == "__main__":
    main()
