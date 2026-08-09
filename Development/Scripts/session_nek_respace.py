"""Re-place the trees with BOX collision (canopies rise above the trunk, so
centre-distance was letting them stack vertically), and darken the webs so they
read against the grey map background."""
import math, random, collections
random.seed(1234)
O='/mnt/user-data/outputs'
FIR=(46,72,48); WILLOW=(54,80,46); DEAD=(84,82,76); ROUND=(50,76,50); TRUNK=(56,48,40)
OLD_INKS={(88,104,86),(96,110,82),(104,104,98),(92,108,88),(84,80,74)}
WEB_OLD=(150,154,148); WEB=(112,116,112)          # darker - was washing out in game
TREE_INKS={FIR,WILLOW,DEAD,ROUND,TRUNK,WEB_OLD,WEB}|OLD_INKS
RIVER=(70,150,205)
BX0,BX1,BY0,BY1=5,83,785,1142
def parse(l):
    f=l[2:].split(',')
    return float(f[0]),float(f[1]),float(f[3]),float(f[4]),(int(f[6]),int(f[7]),int(f[8]))

blines=[l.rstrip('\r\n') for l in open(f'{O}/nektulos.txt',encoding='utf-8',errors='replace') if l.startswith('L')]
# the halfling camp stump - nothing may sit on it
cam=[]
for l in open(f'{O}/nektulos_1.txt',encoding='utf-8',errors='replace'):
    if l.startswith('P') and 'Leatherfoot' in l and 'Medic' not in l:
        f=l[1:].split(','); cam.append((float(f[0]),float(f[1])))
STUMP=(sum(p[0] for p in cam)/len(cam), sum(p[1] for p in cam)/len(cam))
print(f"halfling camp stump at ({STUMP[0]:.0f},{STUMP[1]:.0f}) - kept clear")
raw=[l.rstrip('\r\n') for l in open(f'{O}/nektulos_2.txt',encoding='utf-8',errors='replace') if l.strip()]
head=[l for l in raw if not l.startswith('L')]
lines=[l for l in raw if l.startswith('L')]
bridge=[l for l in lines if parse(l)[4]==(96,90,104)]
keep=[l for l in lines if parse(l)[4] not in TREE_INKS and parse(l)[4]!=(96,90,104)]
print(f"wiped {len(lines)-len(keep)-len(bridge)} tree/web lines")

# river band (envelope)
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
ks=sorted(lo); RX0,RX1=ks[0]*BIN,(ks[-1]+1)*BIN
def bandf(x):
    k=int(x//BIN)
    if k in lo: return lo[k],hi[k]
    n=min(ks,key=lambda kk:abs(kk-k)); return lo[n],hi[n]
def in_river(x,y,pad=0.0):
    if not (RX0-40<=x<=RX1+40): return False
    a,b=bandf(x); return a-pad<=y<=b+pad

CELL=100.0; grid=collections.defaultdict(list)
for l in blines:
    x1,y1,x2,y2,c=parse(l)
    n=max(1,int(math.hypot(x2-x1,y2-y1)//45))
    for i in range(n+1):
        t=i/n; px,py=x1+(x2-x1)*t,y1+(y2-y1)*t
        grid[(int(px//CELL),int(py//CELL))].append((px,py))
def clear_of(x,y,r=2):
    gx,gy=int(x//CELL),int(y//CELL); best=1e9
    for dx in range(-r,r+1):
        for dy in range(-r,r+1):
            for px,py in grid.get((gx+dx,gy+dy),()):
                d=(px-x)**2+(py-y)**2
                if d<best: best=d
    return best**0.5
xs=[a for l in blines for a in (parse(l)[0],parse(l)[2])]
ys=[a for l in blines for a in (parse(l)[1],parse(l)[3])]
sx=sorted(xs); sy=sorted(ys)
GX0,GX1=sx[int(len(sx)*0.01)],sx[int(len(sx)*0.99)]
GY0,GY1=sy[int(len(sy)*0.01)],sy[int(len(sy)*0.99)]

out=[]
def L(x1,y1,x2,y2,c): out.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"%(x1,y1,x2,y2,*c))
def fir(cx,cy,h):
    L(cx,cy,cx,cy-h*0.16,TRUNK)
    for i in range(4):
        by=cy-h*0.13-(h*0.80)*i/4; ap=by-h*0.95/4; wv=h*0.30*(1-i/4*0.62)
        L(cx-wv,by,cx,ap,FIR); L(cx,ap,cx+wv,by,FIR); L(cx-wv,by,cx+wv,by,FIR)
def willow(cx,cy,h):
    L(cx,cy,cx,cy-h*0.48,TRUNK)
    cr=cy-h*0.48; rw=h*0.34; prev=None
    for k in range(11):
        t=k/10.0; a=math.pi*t
        x=cx-rw*math.cos(a); y=cr-h*0.20*math.sin(a)
        if prev: L(prev[0],prev[1],x,y,WILLOW)
        prev=(x,y)
    for k in range(6):
        t=(k+0.5)/6.0; a=math.pi*t
        x0=cx-rw*math.cos(a)*0.92; y0=cr-h*0.20*math.sin(a)*0.92
        L(x0,y0,x0+random.uniform(-6,6),y0+h*(0.28+0.14*math.sin(a)),WILLOW)
def dead(cx,cy,h):
    L(cx,cy,cx,cy-h,DEAD)
    for fy,a,ln in [(0.55,-0.6,0.40),(0.40,0.72,0.46),(0.70,0.5,0.28)]:
        by=cy-h*fy
        L(cx,by,cx+math.sin(a)*h*ln,by-math.cos(a)*h*ln,DEAD)
def broadleaf(cx,cy,h):
    r=h*0.34; top=cy-h*0.52; prev=None
    for k in range(25):
        t=2*math.pi*k/24; wob=1.0+0.10*math.sin(7*t)
        x=cx+math.cos(t)*r*wob; y=top+math.sin(t)*r*0.88*wob
        if prev: L(prev[0],prev[1],x,y,ROUND)
        prev=(x,y)
    L(cx,top+r*0.82,cx,cy,TRUNK)

# footprint of each kind: (half-width, height above base, drop below base)
FOOT={'fir':(0.32,1.02,0.04),'round':(0.40,0.92,0.04),'willow':(0.38,0.72,0.46),'dead':(0.24,1.02,0.04)}
PAD=26.0
boxes=[]; placed=0; tries=0
while placed<150 and tries<80000:
    tries+=1
    x=random.uniform(GX0+90,GX1-90); y=random.uniform(GY0+90,GY1-90)
    if in_river(x,y,58): continue
    if BX0-90<=x<=BX1+90 and BY0-90<=y<=BY1+90: continue
    if clear_of(x,y)<46: continue
    if math.hypot(x-STUMP[0],y-STUMP[1])<170: continue      # off the stump
    r=random.random()
    kind='fir' if r<0.44 else ('round' if r<0.68 else ('willow' if r<0.86 else 'dead'))
    h=random.uniform(100,148)
    hw,up,dn=FOOT[kind]
    box=(x-hw*h-PAD, y-up*h-PAD, x+hw*h+PAD, y+dn*h+PAD)
    if any(not (box[2]<b[0] or box[0]>b[2] or box[3]<b[1] or box[1]>b[3]) for b in boxes): continue
    {'fir':fir,'round':broadleaf,'willow':willow,'dead':dead}[kind](x,y,h)
    boxes.append(box); placed+=1
print(f"trees: {placed} placed with BOX collision (no canopy can sit on another)")

def web(cx,cy,R):
    n=9; P=[]
    for k in range(n):
        a=2*math.pi*k/n-math.pi/2; rr=R*random.uniform(0.92,1.08)
        P.append((cx+math.cos(a)*rr, cy+math.sin(a)*rr*0.88))
    for px,py in P: L(cx,cy,px,py,WEB)
    for f_ in (0.30,0.52,0.74,1.0):
        ring=[(cx+(px-cx)*f_, cy+(py-cy)*f_) for px,py in P]
        for i in range(len(ring)): L(*ring[i],*ring[(i+1)%len(ring)],WEB)
nw=0; tries=0; webs=[]
while nw<10 and tries<20000:
    tries+=1
    x=random.uniform(GX0+220,GX1-220); y=random.uniform(GY0+220,GY1-220)
    if in_river(x,y,90) or clear_of(x,y)<80: continue
    if any((x-px)**2+(y-py)**2<340**2 for px,py in webs): continue
    if math.hypot(x-STUMP[0],y-STUMP[1])<240: continue      # never web the stump
    if any(not (x+90<b[0] or x-90>b[2] or y+90<b[1] or y-90>b[3]) for b in boxes): continue
    web(x,y,random.uniform(60,86)); webs.append((x,y)); nw+=1
print(f"webs: {nw} (darker ink {WEB})")

open(f'{O}/nektulos_2.txt','w',newline='').write('\r\n'.join(head+keep+out+bridge)+'\r\n')
b=open(f'{O}/nektulos_2.txt','rb').read()
print("CRLF OK" if sum(1 for i,c in enumerate(b) if c==10 and (i==0 or b[i-1]!=13))==0 else "BAD")
