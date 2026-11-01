"""M10-S2c: Heber-Verlust der Pool-Filter-Leitung (K01 Linie 1, K17 Linie 2) gegen die Druckhoehe Spiegel - Einlaufachse.
Aufruf: python -X utf8 scripts/heber_rechnung.py        (liest data/leitungstrassen.json, nur Lesen)
Methode [A, Ueberschlag, Eichung an S2a: K01 98 bis 131 mm]: Darcy-Weisbach (glatt, Blasius) im d63-Rohr (Innendurchmesser 57 mm), dazu Einzelverluste in Geschwindigkeitshoehen v^2/2g:
Eintritt aus dem Pool 0,5 | Bogen 90 je 0,5 (gut) bis 0,9 (scharf) | T im Durchgang je 0,2 bis 0,4 (Notbypass-T mit geschlossenem Abzweig, Absetzer-T mit Zufluss) | Austritt in den Filter 1,0.
Strom: 97,5 l/min vor dem Absetzer-T, 110 l/min dahinter (Absetzer-Auslauf 12,5 l/min). Reserve = Druckhoehe - Verlust; unter 30 mm gilt als Befund."""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR = json.load(open(os.path.join(ROOT, "data", "leitungstrassen.json"), encoding="utf-8"))
PAR = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}
D, NU, G = 0.057, 1.0e-6, 9.81
SPIEGEL, EINLAUF = 915.0, 720.0                       # absolut, aus check_leitungen.py (Flur 400 + water_z 515) und Filter-Einlaufachse

def fr(q_lmin):
    """Reibung je m in mm/m und Geschwindigkeitshoehe in mm bei q l/min."""
    v = q_lmin / 60000.0 / (math.pi / 4 * D * D); re = v * D / NU; f = 0.316 / re ** 0.25
    return f / D * v * v / (2 * G) * 1000.0, v * v / (2 * G) * 1000.0

def laenge(t):
    p = t["pfad"]; return sum(math.dist(p[i], p[i + 1]) for i in range(len(p) - 1))

def rechne(pf, abs_t, byp_t, q1=97.5, q2=110.0, tk=(0.2, 0.4)):
    """pf = Trassen der Pool-Filter-Leitung in Flussrichtung, davor das Absetzer-T (abs_t) und das Bypass-T (byp_t) als Trassen-IDs der Teilstuecke."""
    teile = [t for t in TR["trassen"] if t["id"] in pf]; teile.sort(key=lambda t: pf.index(t["id"]))
    hinter_abs = 0.0; vor_abs = 0.0; seen = False
    for t in teile:
        if seen: hinter_abs += laenge(t)
        else: vor_abs += laenge(t)
        if t["id"] == abs_t: seen = True
    r1, h1 = fr(q1); r2, h2 = fr(q2)
    # Bogen vor/hinter dem Absetzer-T: Bogen 1 und 2 liegen auf dem ersten Stueck (Pool-Ende bis Grabenstart), Bogen 3 und 4 am Ende des Grabens
    out = {}
    for lab, kb, kt in (("gut", 0.5, tk[0]), ("scharf", 0.9, tk[1])):
        v = 0.5 * h1 + vor_abs / 1000.0 * r1 + hinter_abs / 1000.0 * r2 + 2 * kb * h1 + 2 * kb * h2 + 1.0 * h2 + kt * h1 + kt * h2
        out[lab] = v
    return vor_abs, hinter_abs, out

if __name__ == "__main__":
    kopf = "Druckhoehe %.0f mm (Spiegel %.0f - Einlaufachse %.0f)" % (SPIEGEL - EINLAUF, SPIEGEL, EINLAUF)
    print(kopf)
    print("Reibung 97,5 l/min: %.2f mm/m, 110 l/min: %.2f mm/m; Geschwindigkeitshoehe %.1f / %.1f mm" % (fr(97.5)[0], fr(110.0)[0], fr(97.5)[1], fr(110.0)[1]))
    for tk, txt in (((0.2, 0.4), "T 0,2 bis 0,4 (konservativ)"), ((0.1, 0.3), "T 0,1 bis 0,3 (Annahme S2b)")):
        for name, pf, a in (("K01 (Linie 1)", ["K01", "K01-m", "K01-b"], "K01-m"), ("K17 (Linie 2)", ["K17", "K17-m", "K17-b"], "K17-m")):
            vor, hint, out = rechne(pf, a, None, tk=tk)
            gut, scharf = out["gut"], out["scharf"]
            res = (SPIEGEL - EINLAUF) - scharf
            print("%-14s %-30s Laenge %4.0f + %4.0f mm; Verlust %3.0f bis %3.0f mm; Reserve %3.0f bis %3.0f mm%s" % (name, txt, vor, hint, gut, scharf, SPIEGEL - EINLAUF - scharf, SPIEGEL - EINLAUF - gut, "  <-- unter 30 mm: BEFUND" if res < 30 else ""))
