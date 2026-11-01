"""Messung des Prompt-Zwischenspeichers der Sitzungen (01.11.2026, Orchestrator): liest die Transkripte der letzten 40 Sitzungen in ~/.claude/projects,
gruppiert die API-Aufrufe nach dem Abstand zum vorigen Aufruf und zeigt den Anteil der aus dem Zwischenspeicher gelesenen Eingabe-Tokens.
Aufruf: python -X utf8 scripts/messung_sitzungs_cache.py  (nur Standardbibliothek, aendert nichts)"""
import glob, json, os, sys, datetime
base = os.path.expanduser('~/.claude/projects')
files = sorted(glob.glob(base + '/*/*.jsonl'), key=os.path.getmtime, reverse=True)[:40]
today = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=14)

def ts(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))

BUCK = [(0, 300, '<5 min'), (300, 1800, '5-30 min'), (1800, 3600, '30-60 min'), (3600, 10**9, '>60 min')]
tot = {b[2]: [0, 0, 0, 0] for b in BUCK}   # n, cache_read, cache_create, input
rows = []
for f in files:
    prev_t = None
    seen = set()
    per = {b[2]: [0, 0, 0, 0] for b in BUCK}
    n_msgs = 0
    first = None
    for line in open(f, encoding='utf-8', errors='ignore'):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get('type') != 'assistant':
            continue
        m = o.get('message', {})
        u = m.get('usage')
        t = o.get('timestamp')
        if not u or not t:
            continue
        mid = m.get('id') or o.get('uuid')
        if mid in seen:
            continue
        seen.add(mid)
        t = ts(t)
        if first is None:
            first = t
        cr = u.get('cache_read_input_tokens', 0) or 0
        cc = u.get('cache_creation_input_tokens', 0) or 0
        inp = u.get('input_tokens', 0) or 0
        n_msgs += 1
        if prev_t is not None:
            dt = (t - prev_t).total_seconds()
            for lo, hi, name in BUCK:
                if lo <= dt < hi:
                    per[name][0] += 1; per[name][1] += cr; per[name][2] += cc; per[name][3] += inp
                    tot[name][0] += 1; tot[name][1] += cr; tot[name][2] += cc; tot[name][3] += inp
                    break
        prev_t = t
    if n_msgs > 5:
        rows.append((os.path.basename(f)[:8], n_msgs, first, per))
print('Dateien mit Nutzungsdaten:', len(rows))
print('\nSumme je Abstand zum vorigen Aufruf (n Aufrufe, Anteil Cache-Lesen an allen Eingabe-Tokens, mittlere neue Cache-Schreib-Tokens je Aufruf):')
for lo, hi, name in BUCK:
    n, cr, cc, inp = tot[name]
    allin = cr + cc + inp
    print('  %-10s n=%5d  Cache-Lesen %5.1f %%  Cache-Schreiben je Aufruf %8.0f  Eingabe gesamt je Aufruf %9.0f' % (name, n, 100.0 * cr / allin if allin else 0, cc / n if n else 0, allin / n if n else 0))
print('\nEinzelne grosse Luecken (>30 min) mit Cache-Lesen-Anteil des Aufrufs danach:')
for f in files:
    prev_t = None; prev_in = None
    for line in open(f, encoding='utf-8', errors='ignore'):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get('type') != 'assistant':
            continue
        m = o.get('message', {}); u = m.get('usage'); t = o.get('timestamp')
        if not u or not t:
            continue
        t = ts(t)
        cr = u.get('cache_read_input_tokens', 0) or 0; cc = u.get('cache_creation_input_tokens', 0) or 0; inp = u.get('input_tokens', 0) or 0
        if prev_t is not None and (t - prev_t).total_seconds() > 1800:
            allin = cr + cc + inp
            print('  %s  Pause %5.0f min  Eingabe %8d  Cache-Lesen %5.1f %%  neu geschrieben %8d' % (os.path.basename(f)[:8], (t - prev_t).total_seconds() / 60, allin, 100.0 * cr / allin if allin else 0, cc))
        prev_t = t
