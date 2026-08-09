"""North of the river takes the Teir'Dal purple - Neriak's side, sinister.
South stays green (halfling country). Also drops the parallel-pair gloom mark,
which read as railroad tracks and represented nothing."""
import math, random, collections
random.seed(555)
O='/mnt/user-data/outputs'
FIR=(46,72,48); WILLOW=(54,80,46); ROUND=(50,76,50); TRUNK=(56,48,40); DEAD=(84,82,76)
# dark elf palette for the northern woods
FIR_N=(62,52,84); WILLOW_N=(70,58,92); ROUND_N=(66,54,88); TRUNK_N=(52,42,58)
GLOOM=(122,124,138); DEEP=(108,110,126); RIVER=(70,150,205)
def parse(l):
    f=l[2:].split(',')
    return float(f[0]),float(f[1]),float(f[3]),float(f[4]),(int(f[6]),int(f[7]),int(f[8]))

blines=[l.rstrip('\r\n') for l in open(f'{O}/nektulos.txt',encoding='utf-8',errors='replace') if l.startswith('L')]
# river centreline by x
pts=[]
for l in blines:
    x1,y1,x2,y2,c=parse(l)
    if c!=RIVER: continue
    n=max(1,int(math.hypot(x2-x1,y2-y1)//12))
    for i in range(n+1):
        t=i/n; pts.append((x1+(x2-x1)*t,y1+(y2-y1)*t))
BIN=45.0
lo=collections.defaultdict(lambda:1e9); hi=collections.defaultdict(lambda:-1e9)
for x,y in pts:
    k=int(x//BIN); lo[k]=min(lo[k],y); hi[k]=max(hi[k],y)
ks=sorted(lo)
def mid_y(x):
    k=int(x//BIN)
    if k not in lo: k=min(ks,key=lambda kk:abs(kk-k))
    return (lo[k]+hi[k])/2
RX0,RX1=ks[0]*BIN,(ks[-1]+1)*BIN
def is_north(x,y):
    xx=min(max(x,RX0),RX1)
    return y < mid_y(xx)

raw=[l.rstrip('\r\n') for l in open(f'{O}/nektulos_2.txt',encoding='utf-8',errors='replace') if l.strip()]
head=[l for l in raw if not l.startswith('L')]
lines=[l for l in raw if l.startswith('L')]

# ---- cluster trees so a whole tree recolours together ----
TREE={FIR,WILLOW,ROUND,TRUNK,DEAD}
idx=[i for i,l in enumerate(lines) if parse(l)[4] in TREE]
G=44.0; cells=collections.defaultdict(list)
for i in idx:
    x1,y1,x2,y2,c=parse(lines[i])
    cells[(int(((x1+x2)/2)//G),int(((y1+y2)/2)//G))].append(i)
seen=set(); trees=[]
for k in list(cells):
    if k in seen: continue
    st=[k]; comp=[]
    while st:
        d=st.pop()
        if d in seen or d not in cells: continue
        seen.add(d); comp+=cells[d]
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                nn=(d[0]+dx,d[1]+dy)
                if nn in cells and nn not in seen: st.append(nn)
    xs=[];ys=[]
    for i in comp:
        x1,y1,x2,y2,c=parse(lines[i]); xs+=[x1,x2]; ys+=[y1,y2]
    trees.append((comp,sum(xs)/len(xs),sum(ys)/len(ys)))
SWAP={FIR:FIR_N, WILLOW:WILLOW_N, ROUND:ROUND_N, TRUNK:TRUNK_N}
n_north=0
for comp,cx,cy in trees:
    if not is_north(cx,cy): continue
    n_north+=1
    for i in comp:
        x1,y1,x2,y2,c=parse(lines[i])
        nc=SWAP.get(c,c)
        lines[i]="L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"%(x1,y1,x2,y2,*nc)
print(f"{len(trees)} trees total; {n_north} north of the river recoloured Teir'Dal purple")

# ---- gloom: drop the parallel-pair marks, keep the subtler ones ----
gl=[i for i,l in enumerate(lines) if parse(l)[4] in {GLOOM,DEEP}]
G2=40.0; c2=collections.defaultdict(list)
for i in gl:
    x1,y1,x2,y2,c=parse(lines[i])
    c2[(int(((x1+x2)/2)//G2),int(((y1+y2)/2)//G2))].append(i)
seen=set(); drop=set(); kept=0
for k in list(c2):
    if k in seen: continue
    st=[k]; comp=[]
    while st:
        d=st.pop()
        if d in seen or d not in c2: continue
        seen.add(d); comp+=c2[d]
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                nn=(d[0]+dx,d[1]+dy)
                if nn in c2 and nn not in seen: st.append(nn)
    # a "railroad track" is two near-horizontal, near-parallel strokes
    if len(comp)==2:
        a=parse(lines[comp[0]]); b=parse(lines[comp[1]])
        aa=math.atan2(a[3]-a[1],a[2]-a[0]); bb=math.atan2(b[3]-b[1],b[2]-b[0])
        if abs(math.sin(aa))<0.45 and abs(math.sin(bb))<0.45 and abs(math.sin(aa-bb))<0.35:
            drop.update(comp); continue
    kept+=1
print(f"gloom: removed {len(drop)} railroad-track lines, kept {kept} marks")
out=[l for i,l in enumerate(lines) if i not in drop]
open(f'{O}/nektulos_2.txt','w',newline='').write('\r\n'.join(head+out)+'\r\n')
b=open(f'{O}/nektulos_2.txt','rb').read()
print("CRLF OK" if sum(1 for i,c in enumerate(b) if c==10 and (i==0 or b[i-1]!=13))==0 else "BAD")
