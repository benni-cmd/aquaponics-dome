"""R47: Netzliste lesen und Kanten/Knoten kompakt ausgeben (nur lesen)."""
import json, sys
d = json.load(open('data/leitungsnetz.json', encoding='utf-8'))
print(list(d.keys()))
for k, v in d.items():
    if isinstance(v, list):
        print(k, len(v), (list(v[0].keys()) if v and isinstance(v[0], dict) else v[:2]))
    elif isinstance(v, dict):
        print(k, 'dict', list(v.keys())[:12])
mode = sys.argv[1] if len(sys.argv) > 1 else ''
if mode == 'kanten':
    for e in d.get('kanten', d.get('edges', [])):
        print(json.dumps(e, ensure_ascii=False)[:260])
if mode == 'knoten':
    for n in d.get('knoten', d.get('nodes', [])):
        print(json.dumps(n, ensure_ascii=False)[:200])
