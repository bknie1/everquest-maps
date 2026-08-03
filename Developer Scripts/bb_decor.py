"""Gnoll-themed doodles for Blackburrow decoration."""
import math, numpy as np
STONE=(66,58,50); STONE_L=(120,110,98); WOOD=(120,84,48); WOOD_D=(90,60,34)
BONE=(206,200,186); IRON=(92,86,80); BANNER=(150,62,44); MOSS=(96,112,70); HIDE=(150,120,80)

def _poly(cv,pts,c,z=0.0,close=False):
    P=list(pts)
    if close: P=P+[P[0]]
    for i in range(len(P)-1): cv.add(P[i][0],P[i][1],P[i+1][0],P[i+1][1],c,z)

def cask(cv,cx,cy,w=34,h=44,wood=WOOD,band=IRON):
    """Beer cask / barrel (Blackburrow Stout)."""
    # bulging staves
    for t in (-1,-0.5,0,0.5,1):
        x=cx+t*w; bulge=(1-t*t)*6
        cv.add(x,cy-h/2, x+ (bulge if t<0 else -bulge if t>0 else 0), cy, wood)
        cv.add(x+ (bulge if t<0 else -bulge if t>0 else 0), cy, x, cy+h/2, wood)
    cv.add(cx-w,cy-h/2,cx+w,cy-h/2,wood); cv.add(cx-w,cy+h/2,cx+w,cy+h/2,wood)
    for yy in (-h*0.28,h*0.28):
        cv.add(cx-w-2,cy+yy,cx+w+2,cy+yy,band)
    cv.add(cx-w*0.5,cy-h*0.5,cx+w*0.5,cy-h*0.5,band)

def cask_stack(cv,cx,cy):
    cask(cv,cx-30,cy,26,38); cask(cv,cx+30,cy,26,38); cask(cv,cx,cy-40,26,38,WOOD_D)

def stalactite(cv,cx,cy,h=46,w=13,color=STONE):
    """Hanging cave spike (points DOWN from ceiling at cy)."""
    cv.add(cx-w,cy,cx,cy+h,color); cv.add(cx+w,cy,cx,cy+h,color)
    cv.add(cx-w,cy,cx+w,cy,color); cv.add(cx-w*0.3,cy,cx,cy+h*0.6,color)

def stalagmite(cv,cx,cy,h=40,w=13,color=STONE):
    cv.add(cx-w,cy,cx,cy-h,color); cv.add(cx+w,cy,cx,cy-h,color); cv.add(cx-w,cy,cx+w,cy,color)

def totem(cv,cx,cy,h=90,wood=WOOD,accent=BANNER):
    """Clan totem pole: post + two stacked carved faces + a hide banner."""
    cv.add(cx,cy,cx,cy-h,wood); cv.add(cx-3,cy,cx-3,cy-h,WOOD_D)
    for k,fy in enumerate((cy-h*0.28,cy-h*0.66)):
        cv.add(cx-16,fy+12,cx+16,fy+12,wood); cv.add(cx-16,fy-12,cx+16,fy-12,wood)
        cv.add(cx-16,fy-12,cx-16,fy+12,wood); cv.add(cx+16,fy-12,cx+16,fy+12,wood)
        cv.add(cx-8,fy-3,cx-3,fy+2,STONE); cv.add(cx+8,fy-3,cx+3,fy+2,STONE)  # eyes
        cv.add(cx-6,fy+7,cx+6,fy+7,STONE)                                      # snarl
    # top feathers / ears
    cv.add(cx,cy-h,cx-12,cy-h-18,accent); cv.add(cx,cy-h,cx+12,cy-h-18,accent)
    # hanging hide banner
    cv.add(cx+16,cy-h*0.66,cx+52,cy-h*0.66,IRON)
    _poly(cv,[(cx+22,cy-h*0.6),(cx+48,cy-h*0.6),(cx+48,cy-h*0.28),(cx+35,cy-h*0.2),(cx+22,cy-h*0.28)],accent,close=True)
    cv.add(cx+35,cy-h*0.55,cx+35,cy-h*0.3,IRON)

def gnoll_figure(cv,cx,cy,s=60,color=STONE):
    """Dog-headed biped (gnoll) leaning on a spear."""
    hy=cy-s
    # head: muzzle + ears
    _poly(cv,[(cx-6,hy),(cx-14,hy+6),(cx-6,hy+12),(cx+8,hy+12),(cx+16,hy+6),(cx+8,hy)],color,close=True)
    cv.add(cx-6,hy,cx-11,hy-9,color); cv.add(cx+8,hy,cx+13,hy-9,color)   # ears
    cv.add(cx-14,hy+6,cx-20,hy+7,color)                                   # snout tip
    cv.add(cx-9,hy+5,cx-6,hy+5,color)                                     # eye
    # body
    cv.add(cx,hy+12,cx,cy+s*0.35,color)
    cv.add(cx,cy+s*0.05,cx-15,cy+s*0.3,color); cv.add(cx,cy+s*0.05,cx+14,cy+s*0.28,color) # arms
    cv.add(cx,cy+s*0.35,cx-12,cy+s*0.8,color); cv.add(cx,cy+s*0.35,cx+12,cy+s*0.8,color)  # legs
    cv.add(cx+18,cy-s*0.2,cx+18,cy+s*0.85,IRON)                            # spear shaft
    cv.add(cx+18,cy-s*0.2,cx+13,cy-s*0.05,IRON); cv.add(cx+18,cy-s*0.2,cx+23,cy-s*0.05,IRON) # spearhead
    cv.add(cx+14,cy+s*0.28,cx+18,cy+s*0.2,color)                          # hand to spear

def snake(cv,cx,cy,length=120,amp=15,color=MOSS):
    """Giant snake: double-line body (two parallel rails), rounded head, tongue."""
    n=40; pts=[]
    for i in range(n+1):
        t=i/n; x=cx+t*length; y=cy+amp*math.sin(t*3.0*math.pi)
        pts.append((x,y))
    hw=lambda t: 6.0*(0.25+0.75*math.sin(min(max(t,0),1)*math.pi))   # fat mid, thin ends
    up=[];dn=[]
    for i,(x,y) in enumerate(pts):
        if i<n: dx,dy=pts[i+1][0]-x,pts[i+1][1]-y
        else:   dx,dy=x-pts[i-1][0],y-pts[i-1][1]
        L=math.hypot(dx,dy) or 1; nx,ny=-dy/L,dx/L; w=hw(i/n)
        up.append((x+nx*w,y+ny*w)); dn.append((x-nx*w,y-ny*w))
    _poly(cv,up,color); _poly(cv,dn,color)
    cv.add(*up[0],*dn[0],color)                                       # cap tail
    hx,hy=pts[-1]
    head=[(hx+8*math.cos(a),hy+5.5*math.sin(a)) for a in np.linspace(0,2*math.pi,11)]
    _poly(cv,head,color)                                              # rounded head
    cv.add(hx+7,hy,hx+15,hy-3,color); cv.add(hx+15,hy-3,hx+20,hy-5,color)   # forked tongue
    cv.add(hx+7,hy,hx+15,hy+3,color); cv.add(hx+15,hy+3,hx+20,hy+5,color)
    cv.add(hx+2,hy-3,hx+4,hy-3,STONE)                                 # eye

def gnoll_face(cv,cx,cy,s=74,color=STONE,accent=BANNER):
    """Front-on snarling gnoll head (hyena/dog-like) -- margin emblem."""
    # head outline: brow -> cheeks -> muzzle -> chin
    _poly(cv,[(cx-s*0.42,cy-s*0.30),(cx-s*0.50,cy+s*0.02),(cx-s*0.30,cy+s*0.30),
              (cx-s*0.12,cy+s*0.42),(cx,cy+s*0.50),(cx+s*0.12,cy+s*0.42),
              (cx+s*0.30,cy+s*0.30),(cx+s*0.50,cy+s*0.02),(cx+s*0.42,cy-s*0.30)],color)
    cv.add(cx-s*0.42,cy-s*0.30,cx+s*0.42,cy-s*0.30,color)             # brow ridge
    # pointed ears
    cv.add(cx-s*0.42,cy-s*0.30,cx-s*0.58,cy-s*0.74,color); cv.add(cx-s*0.58,cy-s*0.74,cx-s*0.16,cy-s*0.40,color)
    cv.add(cx+s*0.42,cy-s*0.30,cx+s*0.58,cy-s*0.74,color); cv.add(cx+s*0.58,cy-s*0.74,cx+s*0.16,cy-s*0.40,color)
    # eyes (angled, menacing)
    for sgn in (-1,1):
        ex=cx+sgn*s*0.22
        _poly(cv,[(ex-s*0.11,cy-s*0.15),(ex+s*0.11,cy-s*0.07),(ex-s*0.02,cy-s*0.01)],color,close=True)
        cv.add(ex-s*0.03,cy-s*0.09,ex+s*0.02,cy-s*0.09,accent)        # eye glint
    # snout bridge + nose
    cv.add(cx,cy-s*0.05,cx,cy+s*0.17,color)
    _poly(cv,[(cx-s*0.07,cy+s*0.17),(cx,cy+s*0.25),(cx+s*0.07,cy+s*0.17)],color,close=True)
    # snarling mouth + fangs
    _poly(cv,[(cx-s*0.20,cy+s*0.30),(cx-s*0.10,cy+s*0.40),(cx,cy+s*0.34),
              (cx+s*0.10,cy+s*0.40),(cx+s*0.20,cy+s*0.30)],color)
    cv.add(cx-s*0.11,cy+s*0.31,cx-s*0.09,cy+s*0.41,color); cv.add(cx+s*0.11,cy+s*0.31,cx+s*0.09,cy+s*0.41,color)  # fangs
    # cheek fur tufts
    for sgn in (-1,1):
        cv.add(cx+sgn*s*0.50,cy+s*0.02,cx+sgn*s*0.63,cy+s*0.05,color)
        cv.add(cx+sgn*s*0.48,cy+s*0.12,cx+sgn*s*0.60,cy+s*0.17,color)

def bone(cv,cx,cy,l=30,color=BONE,ang=0):
    ca,sa=math.cos(ang),math.sin(ang)
    ax,ay=cx-l/2*ca,cy-l/2*sa; bx,by=cx+l/2*ca,cy+l/2*sa
    cv.add(ax,ay,bx,by,color)
    for (px,py,d) in [(ax,ay,-1),(bx,by,1)]:
        cv.add(px,py,px+d*4*ca-4*sa,py+d*4*sa+4*ca,color)
        cv.add(px,py,px+d*4*ca+4*sa,py+d*4*sa-4*ca,color)

def gnoll_head_motif(cv,cx,cy,s,body,legs):
    """Compass center: front-on gnoll head (snout down)."""
    # skull outline
    _poly(cv,[(cx-s*0.5,cy-s*0.3),(cx-s*0.55,cy+s*0.15),(cx-s*0.2,cy+s*0.5),
              (cx,cy+s*0.62),(cx+s*0.2,cy+s*0.5),(cx+s*0.55,cy+s*0.15),
              (cx+s*0.5,cy-s*0.3)],body,close=False)
    # ears
    cv.add(cx-s*0.5,cy-s*0.3,cx-s*0.66,cy-s*0.72,body); cv.add(cx-s*0.66,cy-s*0.72,cx-s*0.2,cy-s*0.4,body)
    cv.add(cx+s*0.5,cy-s*0.3,cx+s*0.66,cy-s*0.72,body); cv.add(cx+s*0.66,cy-s*0.72,cx+s*0.2,cy-s*0.4,body)
    # eyes + snout
    cv.add(cx-s*0.28,cy-s*0.02,cx-s*0.12,cy-s*0.02,legs); cv.add(cx+s*0.28,cy-s*0.02,cx+s*0.12,cy-s*0.02,legs)
    cv.add(cx-s*0.1,cy+s*0.5,cx+s*0.1,cy+s*0.5,legs)
    # fang hints
    cv.add(cx-s*0.12,cy+s*0.5,cx-s*0.16,cy+s*0.62,legs); cv.add(cx+s*0.12,cy+s*0.5,cx+s*0.16,cy+s*0.62,legs)

def rock_corner(cv,x,y,sx,sy,color=STONE,reach=120):
    """Jagged rock cluster tucked in a frame corner."""
    import random
    for k in range(5):
        r=reach*(0.4+0.14*k)
        a=math.radians(20+k*13)
        px=x+sx*r*math.cos(a); py=y+sy*r*math.sin(a)
        w=18-k*2
        stalagmite(cv,px,py,h=sy* -30 if sy<0 else 30, w=w, color=color) if False else None
        cv.add(px-w,py,px,py-sy*abs(28-2*k),color); cv.add(px+w,py,px,py-sy*abs(28-2*k),color); cv.add(px-w,py,px+w,py,color)

def hollow_tree(cv,cx,base_y,h=118,trunk=WOOD,dark=WOOD_D,void=STONE,leaf=MOSS):
    """Side-view cutaway: a hollow gnoll tree whose 'floor' is false -- planks
    with a broken gap and a dark drop to the level below."""
    w=h*0.30; top=base_y-h
    # --- outer trunk walls (gnarled, tapering up), front cut away ---
    for s in (-1,1):
        cv.add(cx+s*w, base_y, cx+s*w*0.92, base_y-h*0.45, trunk)
        cv.add(cx+s*w*0.92, base_y-h*0.45, cx+s*w*0.72, top+h*0.14, trunk)
    # broken hollow rim at the top (concave, snapped)
    rim=[(cx-w*0.72,top+h*0.14),(cx-w*0.4,top+h*0.02),(cx-w*0.12,top+h*0.12),
         (cx+w*0.16,top),(cx+w*0.44,top+h*0.11),(cx+w*0.72,top+h*0.14)]
    _poly(cv,rim,trunk)
    # a couple of dead branches
    cv.add(cx-w*0.6,top+h*0.2,cx-w*1.5,top-h*0.02,dark); cv.add(cx-w*1.5,top-h*0.02,cx-w*1.9,top-h*0.14,dark)
    cv.add(cx+w*0.55,top+h*0.16,cx+w*1.4,top+h*0.04,dark); cv.add(cx+w*1.4,top+h*0.04,cx+w*1.7,top-h*0.1,dark)
    # small tuft of leaves on one branch
    for dx,dy in [(-w*1.9,top-h*0.14),(-w*1.7,top-h*0.2),(-w*2.05,top-h*0.05)]:
        cv.add(dx,dy,dx-6,dy-9,leaf); cv.add(dx,dy,dx+6,dy-9,leaf)
    # bark hatch on the two walls
    for s in (-1,1):
        for k in range(1,5):
            yy=base_y-h*0.16*k
            cv.add(cx+s*w*0.9, yy, cx+s*w*0.64, yy-6, dark)
    # inner back wall (offset, darker) => hollow depth
    cv.add(cx-w*0.5, base_y-2, cx-w*0.4, top+h*0.2, dark)
    cv.add(cx+w*0.5, base_y-2, cx+w*0.4, top+h*0.2, dark)
    # --- FALSE FLOOR: plank band ~42% up, with a clear hole in the middle ---
    fy=base_y-h*0.42; gap=w*0.24
    for yy in (fy,fy+5):                               # two plank lines, split by the hole
        cv.add(cx-w*0.68,yy,cx-gap,yy,trunk); cv.add(cx+gap,yy,cx+w*0.68,yy,trunk)
    for px in (-0.56,-0.40,0.40,0.56):                # plank divisions
        cv.add(cx+w*px,fy,cx+w*px,fy+5,dark)
    # broken plank ends tipping down into the hole
    cv.add(cx-gap,fy,cx-gap*0.4,fy+11,trunk); cv.add(cx+gap,fy,cx+gap*0.4,fy+10,trunk)
    # hole rim + walls of the shaft
    cv.add(cx-gap,fy+2,cx-gap,fy+16,void); cv.add(cx+gap,fy+2,cx+gap,fy+16,void)
    # --- DROP below: dark chamber you fall into (level 2) ---
    for k in range(1,5):                              # chamber shadow lines
        yy=fy+18+k*((base_y-10)-(fy+18))/5
        cv.add(cx-w*0.44, yy, cx+w*0.44, yy, void)
    cv.add(cx,fy+16,cx,base_y-16,void)                # fall line
    cv.add(cx-7,base_y-26,cx,base_y-14,void); cv.add(cx+7,base_y-26,cx,base_y-14,void)  # ▼
    # roots at the base
    for s in (-1,1):
        cv.add(cx+s*w,base_y,cx+s*w*1.5,base_y+8,trunk); cv.add(cx+s*w*1.5,base_y+8,cx+s*w*1.9,base_y+6,trunk)
