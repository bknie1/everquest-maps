"""Final corrections.

  1. Nektulos: the 'Ditto' trees - an old smooth canopy left underneath my new
     lobed one. Strip everything inside each and redraw a single clean canopy.
  2. Najena archway: mirror left-to-right (the hanging door is on the wrong side).
  3. Lavastorm: drop the Kithicor signpost, move Klik'Anon to the SE pointing
     south, Rogue Clockworks to the south-east, rename Snafitzer's House.
"""
import math, collections
O='/mnt/user-data/outputs'
BASE_INK=(58,60,78)

def parse(l):
    f=l[2:].split(',')
    return float(f[0]),float(f[1]),float(f[3]),float(f[4]),(int(f[6]),int(f[7]),int(f[8]))

# ---------------- 1. Ditto trees ----------------
raw=[l.rstrip('\r\n') for l in open(f'{O}/nektulos.txt',encoding='utf-8',errors='replace') if l.strip()]
head=[l for l in raw if not l.startswith('L')]
lines=[l for l in raw if l.startswith('L')]

short=[(i,(parse(l)[0]+parse(l)[2])/2,(parse(l)[1]+parse(l)[3])/2)
       for i,l in enumerate(lines)
       if math.hypot(parse(l)[2]-parse(l)[0], parse(l)[3]-parse(l)[1])<70]
G=46.0; cells=collections.defaultdict(list)
for i,x,y in short: cells[(int(x//G),int(y//G))].append((i,x,y))
seen=set(); clusters=[]
for c in list(cells):
    if c in seen: continue
    st=[c]; comp=[]
    while st:
        d=st.pop()
        if d in seen or d not in cells: continue
        seen.add(d); comp+=cells[d]
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                n=(d[0]+dx,d[1]+dy)
                if n in cells and n not in seen: st.append(n)
    xs=[p[1] for p in comp]; ys=[p[2] for p in comp]
    w=max(xs)-min(xs); h=max(ys)-min(ys)
    if len(comp)>=6 and w<260 and h<280:
        clusters.append((sum(xs)/len(xs),sum(ys)/len(ys),max(w,h)/2))
print(f"canopy clusters: {len(clusters)}")

drop=set()
for cx,cy,R in clusters:
    rad=max(R*1.25, 52)
    for i,l in enumerate(lines):
        if i in drop: continue
        x1,y1,x2,y2,c=parse(l)
        if math.hypot(x2-x1,y2-y1)>70: continue          # never touch roads
        if math.hypot(x1-cx,y1-cy)<=rad and math.hypot(x2-cx,y2-cy)<=rad:
            drop.add(i)
print(f"stripped {len(drop)} lines (old + new canopies together)")

out=[]
def L(x1,y1,x2,y2): out.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"%(x1,y1,x2,y2,*BASE_INK))
for cx,cy,R in clusters:
    r=max(34.0,min(R*0.92,58.0))
    top=cy-r*0.18; prev=None
    for k in range(29):
        t=2*math.pi*k/28
        wob=1.0+0.10*math.sin(7*t)
        x=cx+math.cos(t)*r*wob; y=top+math.sin(t)*r*0.86*wob
        if prev: L(prev[0],prev[1],x,y)
        prev=(x,y)
    L(cx,top+r*0.80,cx,cy+r*0.86)
keep=[l for i,l in enumerate(lines) if i not in drop]
open(f'{O}/nektulos.txt','w',newline='').write('\r\n'.join(head+keep+out)+'\r\n')
print(f"redrawn: {len(clusters)} single clean canopies ({len(out)} lines)")

# ---------------- 2. archway: mirror left-to-right ----------------
p=f'{O}/lavastorm_2.txt'
raw=[l.rstrip('\r\n') for l in open(p,encoding='utf-8',errors='replace') if l.strip()]
idx=[i for i,l in enumerate(raw) if l.startswith('L') and parse(l)[4]==(80,58,50)]
xs=[]
for i in idx:
    x1,y1,x2,y2,c=parse(raw[i]); xs+=[x1,x2]
mid=min(xs)+max(xs)
for i in idx:
    f=raw[i][2:].split(',')
    f[0]=" %.4f"%(mid-float(f[0])); f[3]=" %.4f"%(mid-float(f[3]))
    raw[i]='L '+','.join(f)
open(p,'w',newline='').write('\r\n'.join(raw)+'\r\n')
print(f"archway mirrored left-to-right ({len(idx)} lines)")

# ---------------- 3. Lavastorm signposts ----------------
p3=f'{O}/lavastorm_3.txt'
raw3=[l.rstrip('\r\n') for l in open(p3,encoding='utf-8',errors='replace') if l.strip()]
V='150, 90, 150'
# group violet lines with the label that follows them
groups=[]; cur=[]
for l in raw3:
    if V not in l:
        continue
    cur.append(l)
    if l.startswith('P'):
        groups.append(cur); cur=[]
other=[l for l in raw3 if V not in l]
def label_of(g):
    for l in g:
        if l.startswith('P'): return l.split(', ')[-1].strip()
    return ''
def bbox(g):
    xs=[];ys=[]
    for l in g:
        if l.startswith('L'):
            x1,y1,x2,y2,c=parse(l); xs+=[x1,x2]; ys+=[y1,y2]
    return (min(xs),max(xs),min(ys),max(ys)) if xs else None

# base extent for placing
bxs=[];bys=[]
for l in open(f'{O}/lavastorm.txt',encoding='utf-8',errors='replace'):
    if l.startswith('L'):
        f=l[2:].split(','); bxs+=[float(f[0]),float(f[3])]; bys+=[float(f[1]),float(f[4])]
BX0,BX1,BY0,BY1=min(bxs),max(bxs),min(bys),max(bys)
fxs=[];fys=[]
for l in open(f'{O}/lavastorm_2.txt',encoding='utf-8',errors='replace'):
    if l.startswith('L'):
        f=l[2:].split(','); fxs+=[float(f[0]),float(f[3])]; fys+=[float(f[1]),float(f[4])]
FX0,FX1,FY0,FY1=min(fxs),max(fxs),min(fys),max(fys)
span=max(BX1-BX0,BY1-BY0)

def rebuild(g, ax, ay, direction, newlabel=None):
    """redraw one signpost at (ax,ay) pointing `direction`"""
    DIR={'S':(0,1),'SE':(0.7,0.7),'SW':(-0.7,0.7),'E':(1,0),'W':(-1,0),
         'N':(0,-1),'NE':(0.7,-0.7),'NW':(-0.7,-0.7)}
    dx,dy=DIR[direction]; ln=math.hypot(dx,dy) or 1; dx,dy=dx/ln,dy/ln
    lab=newlabel or label_of(g)
    size=int(g[-1].split(', ')[-2])
    sh=span*0.085; hd=span*0.017
    tipx,tipy=ax+dx*sh*0.5, ay+dy*sh*0.5
    tailx,taily=ax-dx*sh*0.5, ay-dy*sh*0.5
    V3=(150,90,150)
    o=["L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"%(tailx,taily,tipx,tipy,*V3)]
    px,py=-dy,dx
    o.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"%(tipx,tipy,tipx-dx*hd+px*hd*0.6,tipy-dy*hd+py*hd*0.6,*V3))
    o.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"%(tipx,tipy,tipx-dx*hd-px*hd*0.6,tipy-dy*hd-py*hd*0.6,*V3))
    o.append("P %.4f, %.4f, 0.0000, %d, %d, %d, %d, %s"%(tailx, taily+(BY1-BY0)*0.028, *V3, size, lab))
    return o

newgroups=[]
for g in groups:
    lab=label_of(g)
    if 'Kithicor' in lab:
        print("  removed: North Kithicor (too far - Neriak is the near forest)")
        continue
    if "Klik" in lab:
        ax=BX0+(BX1-BX0)*0.72; ay=(FY1+BY1)/2          # south margin, toward the east
        newgroups.append(rebuild(g,ax,ay,'S')); print("  Klik'Anon -> south-east, pointing S")
        continue
    if 'Rogue' in lab:
        ax=BX0+(BX1-BX0)*0.93; ay=(FY1+BY1)/2+ (BY1-BY0)*0.03
        newgroups.append(rebuild(g,ax,ay,'SE')); print("  Old Rogue Clockworks -> south-east")
        continue
    if 'Snafitzer' in lab:
        g=[l.replace("Snafitzer's_House","Snafitzer_Wood") for l in g]
        print("  renamed: Snafitzer's House -> Snafitzer Wood")
    newgroups.append(g)
flat=[l for g in newgroups for l in g]
open(p3,'w',newline='').write('\r\n'.join(other+flat)+'\r\n')
print(f"lavastorm_3: {len(newgroups)} signposts")

# the same rename in Misty Thicket
pm=f'{O}/misty_3.txt'
t=open(pm,'rb').read().decode('utf-8','replace').replace("Snafitzer's_House","Snafitzer_Wood")
open(pm,'w',newline='').write(t)
print("misty_3: Snafitzer Wood renamed too")

for f_ in (f'{O}/nektulos.txt',f'{O}/lavastorm_2.txt',f'{O}/lavastorm_3.txt',f'{O}/misty_3.txt'):
    b=open(f_,'rb').read()
    ok=sum(1 for i,c in enumerate(b) if c==10 and (i==0 or b[i-1]!=13))==0
    print(f_.split('/')[-1], "CRLF OK" if ok else "BAD")
