"""Neriak entrance — corner sketch for the Nektulos map.

Leaning monoliths and a dolmen framing the cut in the rock, with the Teir'Dal
sigil (twin spires over a V) carved on a tilted slab, and the ramp descending
into the dark.  Local coords are y-DOWN; the placer flips to the in-game
convention (the same one the Najena archway now uses).
"""
import math, random
random.seed(77)

def neriak_gate_segs():
    S=[]
    def seg(a,b,c,d): S.append((a,b,c,d))
    def poly(p,close=True):
        for i in range(len(p)-1): seg(*p[i],*p[i+1])
        if close: seg(*p[-1],*p[0])

    # --- rock face behind, jagged ---
    poly([(20,250),(40,150),(110,120),(150,60),(230,40),(300,70),(360,45),
          (430,95),(480,80),(520,140),(540,250)],close=False)
    for i in range(9):                                   # face hatching, clear of the slab
        x=60+i*52
        if 170<x<400: continue
        seg(x,150+(i%3)*18, x+34, 235+(i%3)*14)

    # --- the cut: a dark tunnel mouth, shaded solid ---
    T=[(215,250),(330,250),(360,430),(185,430)]
    poly(T)
    ty_=252.0
    while ty_ < 428.0:                      # dense fill = reads as a dark opening
        xs_=[]
        n=len(T)
        for i in range(n):
            x1,y1=T[i]; x2,y2=T[(i+1)%n]
            if (y1>ty_)!=(y2>ty_):
                xs_.append(x1+(ty_-y1)*(x2-x1)/(y2-y1))
        xs_.sort()
        for i in range(0,len(xs_)-1,2):
            if xs_[i+1]-xs_[i]>1.5: seg(xs_[i],ty_,xs_[i+1],ty_)
        ty_+=2.1
    # a rim around the mouth so the opening still reads as cut stone
    poly([(207,244),(338,244),(368,436),(177,436)])

    # --- dolmen on the left: two uprights + capstone ---
    poly([(58,262),(92,258),(96,392),(60,396)])          # upright
    poly([(120,258),(152,262),(150,392),(118,388)])      # upright
    poly([(44,238),(168,230),(172,262),(40,268)])        # capstone
    seg(70,290,86,286); seg(70,330,86,326); seg(130,296,146,292)

    # --- leaning monoliths right of the cut ---
    poly([(392,206),(430,196),(452,398),(410,404)])
    seg(404,250,442,242); seg(408,310,446,302)
    poly([(470,244),(500,238),(516,392),(484,398)])
    seg(478,286,510,280)
    # a shorter stone in front, tilted
    poly([(346,338),(384,330),(396,428),(354,436)])

    # --- the carved slab, tilted, with the Teir'Dal sigil ---
    sx,sy=196,84
    W_,H_=160,154
    poly([(sx,sy),(sx+W_,sy),(sx+W_,sy+H_),(sx,sy+H_)])           # even rectangular block
    seg(sx+W_,sy,sx+W_+12,sy+10); seg(sx+W_,sy+H_,sx+W_+12,sy+H_+10)   # block thickness
    seg(sx+W_+12,sy+10,sx+W_+12,sy+H_+10)
    seg(sx,sy+H_,sx+12,sy+H_+10); seg(sx+12,sy+H_+10,sx+W_+12,sy+H_+10)
    # sigil: ONE polygon - two ears, centre notch, tapering to a point - shaded in
    SX,SY=sx+34,sy+18
    W_,H_=92,118
    P=[(SX+0.06*W_, SY+0.00*H_),      # left ear tip
       (SX+0.50*W_, SY+0.46*H_),      # centre notch, dips down between the ears
       (SX+0.94*W_, SY+0.00*H_),      # right ear tip
       (SX+0.80*W_, SY+0.52*H_),      # right outer shoulder
       (SX+0.50*W_, SY+1.00*H_),      # bottom point
       (SX+0.20*W_, SY+0.52*H_)]      # left outer shoulder  (symmetric)
    poly(P)                            # outline
    def _inside(px,py):
        c=False; n=len(P)
        for i in range(n):
            x1,y1=P[i]; x2,y2=P[(i+1)%n]
            if (y1>py)!=(y2>py):
                xx=x1+(py-y1)*(x2-x1)/(y2-y1)
                if px<xx: c=not c
        return c
    ys_=[p[1] for p in P]
    yy=min(ys_)+2.0
    while yy<max(ys_)-1.0:            # hatch fill, clipped to the polygon
        xs_=[]
        n=len(P)
        for i in range(n):
            x1,y1=P[i]; x2,y2=P[(i+1)%n]
            if (y1>yy)!=(y2>yy):
                xs_.append(x1+(yy-y1)*(x2-x1)/(y2-y1))
        xs_.sort()
        for i in range(0,len(xs_)-1,2):
            if xs_[i+1]-xs_[i]>1.5: seg(xs_[i],yy,xs_[i+1],yy)
        yy+=1.9
    # --- ground line + rubble ---
    seg(30,432,530,432)
    for rx in (110,250,420,500):
        poly([(rx-16,432),(rx-6,420),(rx+8,422),(rx+16,432)],close=False)
    # a bare tree, Nektulos-style, at the left edge
    seg(96,432,96,352)
    for fy,ang,ln in [(0.5,-0.7,34),(0.34,0.8,40),(0.72,0.55,24)]:
        by=432-80*fy
        ex=96+math.sin(ang)*ln; ey=by-math.cos(ang)*ln
        seg(96,by,ex,ey)
    return S


if __name__=='__main__':
    import cairosvg
    O='/mnt/user-data/outputs'
    INK=(72,66,86)                     # cool dark ink, matches Nektulos
    segs=neriak_gate_segs()
    lminx=min(min(s[0],s[2]) for s in segs); lmaxx=max(max(s[0],s[2]) for s in segs)
    lminy=min(min(s[1],s[3]) for s in segs); lmaxy=max(max(s[1],s[3]) for s in segs)

    def bbox_lines(lines):
        xs=[];ys=[]
        for l in lines:
            f=l[2:].split(','); xs+=[float(f[0]),float(f[3])]; ys+=[float(f[1]),float(f[4])]
        return min(xs),max(xs),min(ys),max(ys)
    raw=[l.rstrip('\r\n') for l in open(f'{O}/nektulos_2.txt',encoding='utf-8',errors='replace') if l.strip()]
    head=[l for l in raw if not l.startswith('L')]
    lines=[l for l in raw if l.startswith('L') and
           tuple(int(v) for v in l[2:].split(',')[6:9])!=INK]
    fx0,fx1,fy0,fy1=bbox_lines(lines)
    bl=[l.rstrip('\r\n') for l in open(f'{O}/nektulos.txt',encoding='utf-8',errors='replace') if l.startswith('L')]
    bx0,bx1,by0,by1=bbox_lines(bl)
    # SW margin band (bottom-left): clear of title, compass and the right-side icon
    mx0,mx1 = fx0, bx0
    my0,my1 = by1, fy1
    padx=(mx1-mx0)*0.10; pady=(my1-my0)*0.12
    s=min(((mx1-mx0)-2*padx)/(lmaxx-lminx), ((my1-my0)-2*pady)/(lmaxy-lminy))
    cx=(mx0+mx1)/2; cy=(my0+my1)/2
    NX0=cx-(lminx+lmaxx)/2*s
    def tx(x): return NX0+x*s
    def ty(y): return cy - (y-(lminy+lmaxy)/2)*s        # in-game convention
    new=[f"L {tx(a):.2f}, {ty(b):.2f}, 0.0000, {tx(c):.2f}, {ty(d):.2f}, 0.0000, {INK[0]}, {INK[1]}, {INK[2]}"
         for a,b,c,d in segs]
    nxs=[tx(x) for g in segs for x in (g[0],g[2])]; nys=[ty(y) for g in segs for y in (g[1],g[3])]
    print(f"Neriak gate placed x[{min(nxs):.0f},{max(nxs):.0f}] y[{min(nys):.0f},{max(nys):.0f}]  ({len(new)} lines)")
    open(f'{O}/nektulos_2.txt','w',newline='').write('\r\n'.join(head+lines+new)+'\r\n')

    # preview in the in-game orientation (my render is mirrored, so flip for the preview)
    W=460; sc=W/(lmaxx-lminx); H=int((lmaxy-lminy)*sc)
    pr=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#f4efe0"/>']
    for a,b,c,d in segs:
        pr.append(f'<line x1="{(a-lminx)*sc:.1f}" y1="{(b-lminy)*sc:.1f}" x2="{(c-lminx)*sc:.1f}" y2="{(d-lminy)*sc:.1f}" stroke="rgb{INK}" stroke-width="1.7"/>')
    pr.append('</svg>')
    cairosvg.svg2png(bytestring=''.join(pr).encode(),write_to=f'{O}/_neriak_gate_sketch.png',output_width=W,output_height=H)
    print("sketch preview written (shown as it will appear in game)")
