"""Druid Ring: reusable stonehenge-style margin sketch module.
Placed in the margin of any zone that has a Druid Ring POI.
Local coords are y-DOWN; the placer flips to native (where -y = north)."""
import math, random

def druid_ring_segs(seed=3):
    """Returns [(x1,y1,x2,y2)] in a ~560x420 local box, y-down."""
    random.seed(seed)
    S=[]
    def seg(a,b,c,d): S.append((a,b,c,d))
    def poly(p,close=True):
        for i in range(len(p)-1): seg(*p[i],*p[i+1])
        if close: seg(*p[-1],*p[0])
    CX,CY=280,250          # ellipse centre
    RX,RY=210,86           # perspective ellipse
    # --- ground ellipse (the ring's footprint), dashed feel via short arcs
    prev=None
    for k in range(49):
        t=2*math.pi*k/48
        x=CX+RX*math.cos(t); y=CY+RY*math.sin(t)
        if prev and k%2==0: seg(prev[0],prev[1],x,y)
        prev=(x,y)
    # --- standing stones around the ring ---
    n=9
    stones=[]
    for i in range(n):
        t=math.pi*0.12+2*math.pi*i/n
        bx=CX+RX*math.cos(t); by=CY+RY*math.sin(t)
        depth=(math.sin(t)+1)/2                 # 0 = back, 1 = front
        h=54+46*depth                            # nearer stones taller
        w=17+13*depth
        lean=random.uniform(-3.5,3.5)
        top=by-h
        # stone body (slightly irregular slab)
        poly([(bx-w/2,by),(bx-w/2+lean,top),(bx+w/2+lean,top-random.uniform(0,5)),(bx+w/2,by)])
        # a shading stroke down the right face
        seg(bx+w/2-3,by-4,bx+w/2+lean-3,top+5)
        stones.append((bx,by,top,w,lean,depth))
    # --- lintels across the two back pairs (trilithons) ---
    back=sorted(stones,key=lambda s:s[5])[:4]
    back=sorted(back,key=lambda s:s[0])
    for a,b in [(back[0],back[1]),(back[2],back[3])]:
        y1=a[2]; y2=b[2]
        seg(a[0]-a[3]/2+a[4], y1-3, b[0]+b[3]/2+b[4], y2-3)
        seg(a[0]-a[3]/2+a[4], y1-11, b[0]+b[3]/2+b[4], y2-11)
        seg(a[0]-a[3]/2+a[4], y1-3, a[0]-a[3]/2+a[4], y1-11)
        seg(b[0]+b[3]/2+b[4], y2-3, b[0]+b[3]/2+b[4], y2-11)
    # --- a fallen stone in the foreground ---
    fx,fy=CX-58,CY+RY+30
    poly([(fx,fy),(fx+86,fy-13),(fx+92,fy+8),(fx+6,fy+21)])
    seg(fx+22,fy+3,fx+72,fy-6)
    # --- centre altar stone ---
    poly([(CX-24,CY+6),(CX-16,CY-12),(CX+18,CY-12),(CX+26,CY+6)])
    seg(CX-16,CY-12,CX+18,CY-12)
    # --- tufts of grass at the base of a few stones ---
    for bx,by,top,w,lean,depth in stones[::3]:
        for g in (-1,0,1):
            gx=bx+g*7
            seg(gx,by+3,gx-3,by-7); seg(gx,by+3,gx+3,by-8)
    return S


if __name__=='__main__':
    O='/mnt/user-data/outputs'
    def bbox(p):
        xs=[];ys=[]
        for l in open(p,encoding='utf-8',errors='replace'):
            if l.startswith('L'):
                f=l[2:].split(',')
                try: xs+=[float(f[0]),float(f[3])];ys+=[float(f[1]),float(f[4])]
                except: pass
        return min(xs),max(xs),min(ys),max(ys)
    def knockout(lines, box):
        kept=[];removed=0
        x0,x1,y0,y1=box
        for L in lines:
            f=L[2:].split(',')
            mx=(float(f[0])+float(f[3]))/2; my=(float(f[1])+float(f[4]))/2
            if x0<=mx<=x1 and y0<=my<=y1: removed+=1; continue
            kept.append(L)
        return kept,removed

    # zone -> (ink colour, corner) ; corner: 'NW','NE','SW','SE' in NORTH-UP terms (-y = north)
    JOBS={'lavastorm':((92,70,60),'NW'),
          'feerrott':((70,86,58),'NE'),
          'misty':((78,92,60),'SW')}
    segs=druid_ring_segs()
    lminx=min(min(s[0],s[2]) for s in segs); lmaxx=max(max(s[0],s[2]) for s in segs)
    lminy=min(min(s[1],s[3]) for s in segs); lmaxy=max(max(s[1],s[3]) for s in segs)
    for zone,(INK,corner) in JOBS.items():
        p2=f'{O}/{zone}_2.txt'
        lines=[l.rstrip('\r\n') for l in open(p2,encoding='utf-8',errors='replace') if l.startswith('L')]
        head=[l.rstrip('\r\n') for l in open(p2,encoding='utf-8',errors='replace') if not l.startswith('L')]
        bx0,bx1,by0,by1=bbox(f'{O}/{zone}.txt')
        fx0,fx1,fy0,fy1=bbox(p2)
        th=(by1-by0)*0.17                       # doodle height ~17% of zone height
        s=th/(lmaxy-lminy)
        wpx=(lmaxx-lminx)*s
        mx_left=(fx0+bx0)/2; mx_right=(fx1+bx1)/2
        my_north=(fy0+by0)/2; my_south=(fy1+by1)/2
        cx_n = mx_left if corner in ('NW','SW') else mx_right
        cy_n = my_north if corner in ('NW','NE') else my_south
        NX0=cx_n-(lminx+lmaxx)/2*s
        def tx(x): return NX0+x*s
        def ty(y): return cy_n+((lminy+lmaxy)/2-y)*s      # flip: local down -> native north-up
        new=[f"L {tx(a):.2f}, {ty(b):.2f}, 0.0000, {tx(c):.2f}, {ty(d):.2f}, 0.0000, {INK[0]}, {INK[1]}, {INK[2]}"
             for a,b,c,d in segs]
        nxs=[tx(x) for sg in segs for x in (sg[0],sg[2])]; nys=[ty(y) for sg in segs for y in (sg[1],sg[3])]
        pad=(max(nxs)-min(nxs))*0.10
        kept,rm=knockout(lines,(min(nxs)-pad,max(nxs)+pad,min(nys)-pad,max(nys)+pad))
        open(p2,'w',newline='').write('\r\n'.join(head+kept+new)+'\r\n')
        print(f"{zone}_2: druid ring in {corner} margin  x[{min(nxs):.0f},{max(nxs):.0f}] y[{min(nys):.0f},{max(nys):.0f}]  (knocked out {rm})")
