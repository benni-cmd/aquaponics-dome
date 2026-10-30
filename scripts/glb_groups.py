import struct, json, sys, re, math
f = open(sys.argv[1], 'rb'); f.read(12)
clen, _ = struct.unpack('<I4s', f.read(8)); j = json.loads(f.read(clen)); nodes = j['nodes']
def mmul(a, b): return [[sum(a[i][k]*b[k][j2] for k in range(4)) for j2 in range(4)] for i in range(4)]
def local(n):
    if 'matrix' in n:
        m = n['matrix']; return [[m[c*4+r] for c in range(4)] for r in range(4)]
    t = n.get('translation', [0,0,0]); q = n.get('rotation', [0,0,0,1]); s = n.get('scale', [1,1,1])
    x,y,z,w = q
    R = [[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]]
    return [[R[0][0]*s[0], R[0][1]*s[1], R[0][2]*s[2], t[0]], [R[1][0]*s[0], R[1][1]*s[1], R[1][2]*s[2], t[1]], [R[2][0]*s[0], R[2][1]*s[1], R[2][2]*s[2], t[2]], [0,0,0,1]]
I = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
groups = {}
def mesh_box(mi):
    lo=[1e18]*3; hi=[-1e18]*3
    for p in j['meshes'][mi]['primitives']:
        a = j['accessors'][p['attributes']['POSITION']]
        for i in range(3): lo[i]=min(lo[i],a['min'][i]); hi[i]=max(hi[i],a['max'][i])
    return lo, hi
def walk(i, pm, top):
    n = nodes[i]; m = mmul(pm, local(n))
    if 'mesh' in n:
        lo, hi = mesh_box(n['mesh'])
        pts = [[m[r][0]*(hi[0] if a else lo[0])+m[r][1]*(hi[1] if b else lo[1])+m[r][2]*(hi[2] if c else lo[2])+m[r][3] for r in range(3)] for a in (0,1) for b in (0,1) for c in (0,1)]
        key = (top, re.sub(r'[._]\d+$', '', n.get('name','?')))
        g = groups.setdefault(key, {'n':0,'lo':[1e18]*3,'hi':[-1e18]*3})
        g['n'] += 1
        for p in pts:
            for k in range(3): g['lo'][k]=min(g['lo'][k],p[k]); g['hi'][k]=max(g['hi'][k],p[k])
    for c in n.get('children', []): walk(c, m, top)
for r in j['scenes'][int(sys.argv[2])]['nodes']:
    walk(r, I, re.sub(r'[._]\d+$', '', nodes[r].get('name','?')))
for (top, nm), g in sorted(groups.items()):
    sz = [g['hi'][k]-g['lo'][k] for k in range(3)]
    ctr = [(g['hi'][k]+g['lo'][k])/2 for k in range(3)]
    print('%-28s %-28s n=%-4d size=(%.2f,%.2f,%.2f) ctr=(%.2f,%.2f,%.2f)' % (top[:28], nm[:28], g['n'], *sz, *ctr))
