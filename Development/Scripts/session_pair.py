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
def Pl(x,y,t,s=3): return "P %.4f, %.4f, 0.0000, %d, %d, %d, %d, %s"%(x,y,*V,s,t)
def narrow_diamond(cx,cy,span):
    ry=span*0.014; rx=ry*0.55
    return [Ll(cx,cy-ry,cx+rx,cy),Ll(cx+rx,cy,cx,cy+ry),Ll(cx,cy+ry,cx-rx,cy),Ll(cx-rx,cy,cx,cy-ry)]
def signpost(tipx,tipy,label,span,dir='W'):
    sh=span*0.10; hd=span*0.02
    dx={'W':-1,'E':1}[dir]
    out=[Ll(tipx,tipy,tipx-dx*sh,tipy),
         Ll(tipx,tipy,tipx-dx*hd,tipy+hd*0.6),Ll(tipx,tipy,tipx-dx*hd,tipy-hd*0.6)]
    out.append(Pl(tipx-dx*sh*0.5,tipy+span*0.03,label))
    return out
O='/mnt/user-data/outputs'

# ---------- SOUTH KARANA: 3 narrow diamonds (2 from real EQ1 locs) ----------
b=bb(f'{O}/southkarana.txt'); span=max(b[1]-b[0],b[3]-b[2])
sk=[]
for cx,cy,lab in [(-1190,6700,'Aviak_Village'),(2400,-200,'Centaur_Valley'),(0,2900,'South_Crossroads')]:
    sk+=narrow_diamond(cx,cy,span); sk.append(Pl(cx+span*0.011,cy,lab))
open(f'{O}/southkarana_3.txt','w',newline='').write('\r\n'.join(sk)+'\r\n')

# ---------- MISTY THICKET: 1 diamond (Baga Village) + 1 signpost (Mount Hatespike, W margin) ----------
b2=bb(f'{O}/misty.txt'); f2=bb(f'{O}/misty_2.txt'); span2=max(b2[1]-b2[0],b2[3]-b2[2])
mi=[]
mi+=narrow_diamond(300,250,span2); mi.append(Pl(300+span2*0.011,250,'Baga_Village'))
# signpost in the west margin (x between frame-left f2[0] and base-left b2[0]); Mount Hatespike lies NW
margin_x=(f2[0]+b2[0])/2
mi+=signpost(margin_x+span2*0.05, b2[3]*0.55, 'To_Mount_Hatespike', span2, 'W')
open(f'{O}/misty_3.txt','w',newline='').write('\r\n'.join(mi)+'\r\n')
print("built southkarana_3 (3 diamonds) + misty_3 (1 diamond + 1 signpost)")

# ---------- render both NORTH-UP (in-game orientation: screen_y=(y-miny)) ----------
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
            try:P.append((float(f[0]),float(f[1]),int(f[3]),int(f[4]),int(f[5]),','.join(f[7:]).strip()))
            except:pass
    return L,P
def esc(s): return s.replace('&','&amp;')
def render(z,out,Wt=780):
    L=[];P=[]
    for suf in ['','_2','_3']:
        l,p=load(f'{O}/{z}{suf}.txt'); L+=l; P+=p
    xs=[a for s in L for a in (s[0],s[2])]; ys=[a for s in L for a in (s[1],s[3])]
    mnx,mxx,mny,mxy=min(xs),max(xs),min(ys),max(ys)
    sc=Wt/(mxx-mnx); Hh=int((mxy-mny)*sc)
    def SX(x):return (x-mnx)*sc
    def SY(y):return (y-mny)*sc      # NORTH-UP (matches in-game)
    pr=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt}" height="{Hh}" viewBox="0 0 {Wt} {Hh}"><rect width="{Wt}" height="{Hh}" fill="#f4efe0"/>']
    for x1,y1,x2,y2,r,g,b in L:
        w=1.6 if (r,g,b)==V else 1
        pr.append(f'<line x1="{SX(x1):.1f}" y1="{SY(y1):.1f}" x2="{SX(x2):.1f}" y2="{SY(y2):.1f}" stroke="rgb({r},{g},{b})" stroke-width="{w}"/>')
    for x,y,r,g,b,lab in P:
        if (r,g,b)==V:
            pr.append(f'<text x="{SX(x):.1f}" y="{SY(y)+4:.1f}" font-size="14" font-family="serif" font-weight="bold" fill="rgb{V}" stroke="white" stroke-width="3" paint-order="stroke">{esc(lab)}</text>')
    pr.append('</svg>')
    cairosvg.svg2png(bytestring=''.join(pr).encode(),write_to=out,output_width=Wt,output_height=Hh)
render('southkarana','/mnt/user-data/outputs/_review_southkarana.png')
render('misty','/mnt/user-data/outputs/_review_misty.png')
print("rendered pair north-up")
