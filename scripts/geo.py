"""3V icosahedral geodesic frame: vertices + struts (unit sphere), vertex up."""
import math, itertools
def ico():
    p=(1+5**.5)/2
    v=[(-1,p,0),(1,p,0),(-1,-p,0),(1,-p,0),(0,-1,p),(0,1,p),(0,-1,-p),(0,1,-p),(p,0,-1),(p,0,1),(-p,0,-1),(-p,0,1)]
    f=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
    return v,f
def norm(a):
    l=math.sqrt(sum(x*x for x in a));return tuple(x/l for x in a)
def rot_vertex_up(v):
    a=norm(v[0]);  # rotate so a -> +Z
    z=(0,0,1);ax=(a[1]*z[2]-a[2]*z[1],a[2]*z[0]-a[0]*z[2],a[0]*z[1]-a[1]*z[0])
    s=math.sqrt(sum(x*x for x in ax));c=sum(x*y for x,y in zip(a,z))
    k=norm(ax)
    def R(p):
        p=norm(p);kp=sum(x*y for x,y in zip(k,p))
        cr=(k[1]*p[2]-k[2]*p[1],k[2]*p[0]-k[0]*p[2],k[0]*p[1]-k[1]*p[0])
        return tuple(p[i]*c+cr[i]*s+k[i]*kp*(1-c) for i in range(3))
    return R
def build(freq=3):
    v,f=ico();R=rot_vertex_up(v);v=[R(p) for p in v]
    pts={};edges=set()
    def key(p):return tuple(round(x,6) for x in p)
    def add(p):
        p=norm(p);k=key(p);pts.setdefault(k,p);return k
    for a,b,c in f:
        A,B,C=v[a],v[b],v[c]
        grid={}
        for i in range(freq+1):
            for j in range(freq+1-i):
                k=freq-i-j
                p=tuple((A[t]*i+B[t]*j+C[t]*k)/freq for t in range(3))
                grid[(i,j)]=add(p)
        for (i,j),k0 in grid.items():
            for d in ((1,0),(0,1),(-1,1)):
                n=(i+d[0],j+d[1])
                if n in grid: edges.add(tuple(sorted((k0,grid[n]))))
    return pts,edges
if __name__=="__main__":
    pts,e=build()
    zs=sorted({round(p[2],3) for p in pts.values()});print(len(pts),len(e));print(zs)
