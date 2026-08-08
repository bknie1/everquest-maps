import cairosvg
V=(150,90,150)
def bb(p):
    xs=[];ys=[]
    for l in open(p,encoding='utf-8',errors='replace'):
        if l.startswith('L'):
            f=l[2:].split(',')
            try: xs+=[float(f[0]),float(f[3])];ys+=[float(f[1]),float(f[4])]
            except:pass
    return min(xs),max(xs),min(ys),max(ys)
def Ll(x1,y1,x2,y2): return "L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"%(x1,y1,x2,y2,*V)
def Pl(x,y,t,s): return "P %.4f, %.4f, 0.0000, %d, %d, %d, %d, %s"%(x,y,*V,s,t)
def ndiamond(cx,cy,span,tier):    # tier 1/2/3 -> small/med/large
    ry=span*(0.010+0.004*tier); rx=ry*0.55
    return [Ll(cx,cy-ry,cx+rx,cy),Ll(cx+rx,cy,cx,cy+ry),Ll(cx,cy+ry,cx-rx,cy),Ll(cx-rx,cy,cx,cy-ry)]
O='/mnt/user-data/outputs'
b=bb(f'{O}/southkarana.txt'); span=max(b[1]-b[0],b[3]-b[2])
# (label, native_x, native_y, tier)  tier 3=large(size4) 2=med(size3) 1=small(size2)
POI=[
 ('Aviak_Village',-1190,6700,3),      # LARGE - real EQ1 loc (south)
 ('South_Crossroads',500,3000,3),     # LARGE - fort/crossroads (center)
 ('Centaur_Valley',2400,-200,2),      # MED - real EQ1 loc (north-east)
 ("Urglunts_Wall",-1600,400,2),       # MED (NW)
 ("Urglunts_Gate",-2500,4200,2),      # MED (W)
 ('Widows_Peak',3100,3400,2),         # MED (E)
 ("Wktaans_4th_Talon",2900,5600,1),   # SMALL ruins (SE)
 ('Serpent_Hills',900,7900,1),        # SMALL (south)
]
sz={3:4,2:3,1:2}
out=[]
for lab,x,y,t in POI:
    out+=ndiamond(x,y,span,t); out.append(Pl(x+span*(0.008+0.003*t),y,lab,sz[t]))
open(f'{O}/southkarana_3.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print(f"southkarana_3: {len(POI)} EQOA labels (large={sum(1 for p in POI if p[3]==3)}, med={sum(1 for p in POI if p[3]==2)}, small={sum(1 for p in POI if p[3]==1)})")

# render north-up with size-scaled text
def load(p):
    L=[];P=[]
    import os
    if not os.path.exists(p): return L,P
    for l in open(p,encoding='utf-8',errors='replace'):
        if l.startswith('L'):
            f=l[2:].split(',')
            try:L.append((float(f[0]),float(f[1]),float(f[3]),float(f[4]),int(f[6]),int(f[7]),int(f[8])))
            except:pass
        elif l.startswith('P'):
            f=l[1:].split(',')
            try:P.append((float(f[0]),float(f[1]),int(f[3]),int(f[4]),int(f[5]),int(f[6]),','.join(f[7:]).strip()))
            except:pass
    return L,P
def esc(s):return s.replace('&','&amp;')
L=[];P=[]
for suf in ['','_2','_3']:
    l,p=load(f'{O}/southkarana{suf}.txt'); L+=l;P+=p
xs=[a for s in L for a in (s[0],s[2])];ys=[a for s in L for a in (s[1],s[3])]
mnx,mxx,mny,mxy=min(xs),max(xs),min(ys),max(ys)
Wt=760; sc=Wt/(mxx-mnx); Hh=int((mxy-mny)*sc)
pr=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt}" height="{Hh}" viewBox="0 0 {Wt} {Hh}"><rect width="{Wt}" height="{Hh}" fill="#f4efe0"/>']
for x1,y1,x2,y2,r,g,bb2 in L:
    w=1.7 if (r,g,bb2)==V else 1
    pr.append(f'<line x1="{(x1-mnx)*sc:.1f}" y1="{(y1-mny)*sc:.1f}" x2="{(x2-mnx)*sc:.1f}" y2="{(y2-mny)*sc:.1f}" stroke="rgb({r},{g},{bb2})" stroke-width="{w}"/>')
for x,y,r,g,bb2,size,lab in P:
    if (r,g,bb2)==V:
        fs={2:12,3:16,4:21}.get(size,14)
        pr.append(f'<text x="{(x-mnx)*sc:.1f}" y="{(y-mny)*sc+4:.1f}" font-size="{fs}" font-family="serif" font-weight="bold" fill="rgb{V}" stroke="white" stroke-width="2.5" paint-order="stroke">{esc(lab)}</text>')
pr.append('</svg>')
cairosvg.svg2png(bytestring=''.join(pr).encode(),write_to='/mnt/user-data/outputs/_review_southkarana_dense.png',output_width=Wt,output_height=Hh)
print("rendered dense south karana")
