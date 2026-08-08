"""Ak'Anon decoration (_2): Romulan palette (grey-green + green gems), gear-'O' title,
gear/clockwork margin doodles, gear compass. draw_fit + content validation."""
import math
import eqmap_toolkit as TK
from eqmap_toolkit import Canvas, frame, compass, draw_fit, build_occupancy, seg_hits_content, parse_L_segments
import steam_decor as G

MINX,MAXX,MINY,MAXY=-210.0,1050.0,-2255.0,84.0
PAD,INSET,CLEAR=360,80,90
cv=Canvas((MINX,MAXX,MINY,MAXY),PAD)
# Romulan palette
BR=(46,58,52); INNER=(74,88,80); STEELg=(72,86,78); GEM=(46,180,96); TEAL=(46,128,120); DARK=(36,46,42)
TIN=INSET+CLEAR
SX0=cv.bx0+TIN; SX1=cv.bx1-TIN; SY0=cv.by0+TIN; SY1=cv.by1-TIN
BOX=150; LX=SX0+BOX/2; RX=SX1-BOX/2

ELEMENTS=[]
def track(name, fn):
    i0=len(cv.L); fn(); seg=cv.L[i0:]
    if not seg: return
    S=[];xs=[];ys=[]
    for l in seg:
        f=l[2:].split(','); a,b,c,d=float(f[0]),float(f[1]),float(f[3]),float(f[4]); S.append((a,b,c,d)); xs+=[a,c]; ys+=[b,d]
    ELEMENTS.append([name,min(xs),min(ys),max(xs),max(ys),S])

GC=(120,132,124); STEP=430
gx=math.ceil(MINX/STEP)*STEP
while gx<MAXX: cv.add(gx,MINY,gx,MAXY,GC); gx+=STEP
gy=math.ceil(MINY/STEP)*STEP
while gy<MAXY: cv.add(MINX,gy,MAXX,gy,GC); gy+=STEP
for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),(MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]: cv.add(a,b,c,d,GC)

frame(cv, outer=BR, inner=INNER, step=200, depth=54, inset=INSET,
      corner=lambda c,x,y,sx,sy: (G.gear(c, x+sx*56, y+sy*56, 40, teeth=9, c=STEELg), G.gear(c, x+sx*56, y+sy*56, 15, teeth=6, c=GEM)))

# --- gear-'O' title ---
def gear_title(cv, text, color, gem, shadow=None, height=250, gap=48):
    cw=height*0.66
    gwid=lambda: sum(TK._adv(c,cw) for c in text)+(len(text)-1)*gap
    avail=(cv.bx1-cv.bx0)-360
    if gwid()>avail:
        s=avail/gwid(); cw*=s; height*=s; gap*=s
    grp=gwid(); ox=(cv.minx+cv.maxx)/2-grp/2
    oy=cv.by0+max(120,cv.pad*0.2); fy=lambda y:2*oy+height-y
    x=ox
    for ch in text:
        adv=TK._adv(ch,cw)
        if ch=='O':
            gcx=x+adv/2; gcy=fy(oy+height/2); r=height*0.32
            G.gear(cv,gcx,gcy,r,teeth=12,c=color); G.gear(cv,gcx,gcy,r*0.42,teeth=8,c=gem)
        else:
            for poly in TK.LETTERS.get(ch,[]):
                for i in range(len(poly)-1):
                    ax,ay=poly[i]; bx,by=poly[i+1]
                    cv.add(x+ax*adv, fy(oy+ay*height), x+bx*adv, fy(oy+by*height), color)
                    if shadow: cv.add(x+ax*adv+7, fy(oy+ay*height)+9, x+bx*adv+7, fy(oy+by*height)+9, shadow)
        x+=adv+gap
    cv.add(ox-30, fy(oy-46), ox+grp+30, fy(oy-46), color)
    cv.add(ox-30, fy(oy+height+42), ox+grp+30, fy(oy+height+42), color)
gear_title(cv, "AK'ANON", BR, GEM, shadow=DARK, height=250)

def _cogs(c): G.gear(c,-40,40,80,teeth=12,c=STEELg); G.gear(c,60,-60,50,teeth=9,c=TEAL); G.gear(c,-40,40,20,teeth=6,c=GEM)
def _spider(c): G.clockwork_spider(c,0,0,s=160,c=STEELg,c2=DARK,brass=GEM)
for k,by in enumerate((-1950,-1400,-850,-300)):
    track(f"L{k}", (lambda by=by,k=k: draw_fit(cv, (_cogs if k%2 else _spider), LX, by, BOX, BOX)))
    track(f"R{k}", (lambda by=by,k=k: draw_fit(cv, (_spider if k%2 else _cogs), RX, by, BOX, BOX)))

CR=150; LR=CR*1.30
band0=INSET; band1=PAD; bc=(band0+band1)/2; CRpad=max(70,(band1-band0)/2/1.28*0.66)
track("compass", lambda: compass(cv, cv.bx1-bc, cv.by1-bc, CRpad,
        ring=(BR,STEELg), rose=(BR,GEM), center=G.cog_motif,
        center_colors=(STEELg,GEM), label=BR, n_label=BR, arrow=BR))

def ov(a,b,p=4): return not (a[3]<b[1]-p or b[3]<a[1]-p or a[4]<b[2]-p or b[4]<a[2]-p)
hits=[(ELEMENTS[i][0],ELEMENTS[j][0]) for i in range(len(ELEMENTS)) for j in range(i+1,len(ELEMENTS)) if ov(ELEMENTS[i],ELEMENTS[j])]
occ=build_occupancy(parse_L_segments('akanon_colored.txt'), (MINX,MAXX,MINY,MAXY), cell=36, dilate=1)
content_hits=[e[0] for e in ELEMENTS if seg_hits_content(e[5], occ)]
cv.write('akanon_2.txt')
print('wrote akanon_2.txt L=%d elements=%d'%(len(cv.L),len(ELEMENTS)))
print('SKETCH OVERLAPS:', hits if hits else 'none')
print('CONTENT OVERLAPS:', content_hits if content_hits else 'none — VALIDATION OK')
