"""Nektulos-style tree band along Lavastorm's southern edge, stopping short of
the first lava pools - the forest creeping up from the Nektulos line."""
import math, random
random.seed(19)
O='/mnt/user-data/outputs'
FIR=(88,104,86); WILLOW=(96,110,82); DEAD=(104,104,98); TRUNK=(84,80,74); FOG=(176,180,174)
BAND_INK={FIR,WILLOW,DEAD,TRUNK,FOG}

# base extent + lava reach
xs=[];ys=[];lava=[]
for l in open(f'{O}/lavastorm.txt',encoding='utf-8',errors='replace'):
    if l.startswith('L'):
        f=l[2:].split(','); c=(int(f[6]),int(f[7]),int(f[8]))
        x1,y1,x2,y2=float(f[0]),float(f[1]),float(f[3]),float(f[4])
        xs+=[x1,x2]; ys+=[y1,y2]
        if c==(255,0,0): lava.append(((x1+x2)/2,(y1+y2)/2))
bx0,bx1,by0,by1=min(xs),max(xs),min(ys),max(ys)
lava_south=max(p[1] for p in lava)
print(f"base y {by0:.0f}..{by1:.0f}; lava reaches south to y={lava_south:.0f}")
Y0=lava_south+120        # start clear of the pools
Y1=by1-40                # up to the southern edge
print(f"tree band: y {Y0:.0f} .. {Y1:.0f}  (south of the lava, toward the Nektulos line)")

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
        t=k/10.0; ang=math.pi*t
        x=cx-rw*math.cos(ang); y=cr-h*0.20*math.sin(ang)
        if prev: L(prev[0],prev[1],x,y,WILLOW)
        prev=(x,y)
    for k in range(6):
        t=(k+0.5)/6.0; ang=math.pi*t
        x0=cx-rw*math.cos(ang)*0.92; y0=cr-h*0.20*math.sin(ang)*0.92
        ln=h*(0.28+0.14*math.sin(ang))
        L(x0,y0,x0+random.uniform(-6,6),y0+ln,WILLOW)
def dead(cx,cy,h):
    L(cx,cy,cx,cy-h,DEAD)
    for fy,ang,ln in [(0.55,-0.6,0.40),(0.40,0.72,0.46),(0.70,0.5,0.28)]:
        by=cy-h*fy
        ex=cx+math.sin(ang)*h*ln; ey=by-math.cos(ang)*h*ln
        L(cx,by,ex,ey,DEAD)

placed=[]
tries=0
while len(placed)<34 and tries<4000:
    tries+=1
    x=random.uniform(bx0+90, bx1-90)
    y=random.uniform(Y0, Y1)
    # denser toward the southern (Nektulos) edge
    if random.random() > 0.35+0.65*((y-Y0)/max(1,(Y1-Y0))): continue
    if any((x-px)**2+(y-py)**2 < 150**2 for px,py in placed): continue
    if any((x-lx)**2+(y-ly)**2 < 200**2 for lx,ly in lava): continue
    placed.append((x,y))
    h=random.uniform(105,155); r=random.random()
    if r<0.58: fir(x,y,h)
    elif r<0.80: willow(x,y,h*0.95)
    else: dead(x,y,h)
print(f"placed {len(placed)} trees")
# a couple of low fog wisps through the band
for k in range(4):
    fy=Y0+(Y1-Y0)*(k+0.5)/4; px=bx0+random.uniform(100,500); span=(bx1-bx0)*random.uniform(0.28,0.45)
    prev=None
    for s_ in range(11):
        xx=px+span*s_/10; yy=fy+math.sin(s_*0.9+k)*26
        if prev: L(prev[0],prev[1],xx,yy,FOG)
        prev=(xx,yy)

p2=f'{O}/lavastorm_2.txt'
raw=[l.rstrip('\r\n') for l in open(p2,encoding='utf-8',errors='replace') if l.strip()]
raw=[l for l in raw if not (l.startswith('L') and tuple(int(v) for v in l[2:].split(',')[6:9]) in BAND_INK)]
open(p2,'w',newline='').write('\r\n'.join(raw+out)+'\r\n')
b=open(p2,'rb').read()
print("lavastorm_2 +",len(out),"lines |","CRLF OK" if sum(1 for i,c in enumerate(b) if c==10 and (i==0 or b[i-1]!=13))==0 else "BAD")
