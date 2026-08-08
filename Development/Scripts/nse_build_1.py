"""Assemble newsebexp_1.txt -- the POI / marker layer for New Sebilis Expedition."""
import math
import nse_data as D

segs, V = D.load_geo()
pois = D.native_pois(V)

L=[]; P=[]
def add(x1,y1,x2,y2,c,z): L.append("L %.4f, %.4f, %.4f,  %.4f, %.4f, %.4f,  %d, %d, %d"%(x1,y1,z,x2,y2,z,c[0],c[1],c[2]))
def lab(x,y,c,size,text,z): P.append("P %.4f, %.4f, %.4f,  %d, %d, %d,  %d,  %s"%(x,y,z,c[0],c[1],c[2],size,text))

# ---- marker glyphs (small L shapes) ----
def diamond(x,y,c,z,r=6):
    add(x,y-r,x+r,y,c,z); add(x+r,y,x,y+r,c,z); add(x,y+r,x-r,y,c,z); add(x-r,y,x,y-r,c,z)
def square(x,y,c,z,r=5):
    add(x-r,y-r,x+r,y-r,c,z); add(x+r,y-r,x+r,y+r,c,z); add(x+r,y+r,x-r,y+r,c,z); add(x-r,y+r,x-r,y-r,c,z)
def coin(x,y,c,z,r=6):
    pts=[(x+r*math.cos(t),y+r*math.sin(t)) for t in [i*math.pi/5 for i in range(11)]]
    for i in range(len(pts)-1): add(*pts[i],*pts[i+1],c,z)
    add(x-r*0.4,y,x+r*0.4,y,c,z)
def chevron(x,y,c,z,r=7):        # shield/chevron for guilds & guards
    add(x-r,y-r*0.6,x,y+r*0.5,c,z); add(x,y+r*0.5,x+r,y-r*0.6,c,z); add(x-r,y-r*0.6,x+r,y-r*0.6,c,z)

GLYPH={'spell':diamond,'craft':square,'econ':coin,'gm':chevron,'guard':chevron}

# ---- POI markers: glyph + function label (+ name for gm/econ/guard) ----
NAME_CATS={'gm','econ','guard'}
for p in pois:
    c=D.COL[p['cat']]; x,y,z=p['x'],p['y'],p['z']
    GLYPH[p['cat']](x,y,c,z)
    lab(x+9, y-3, c, 2, p['fn'], z)
    if p['cat'] in NAME_CATS:
        lab(x+9, y+12, tuple(int(v*0.75+40) for v in c), 1, p['name'], z)

# ---- zone exit: keep the clickable purple line, add an orange EXIT accent ----
EXIT=D.COL['exit']
ex,ey,ez = 143.9682,-646.3381,-23.9360           # matches the seed clickable
# little orange arrow-chevron pointing up toward the exit + label
add(ex-10,ey+16,ex,ey+2,EXIT,ez); add(ex,ey+2,ex+10,ey+16,EXIT,ez)
add(ex,ey+2,ex,ey+22,EXIT,ez)
lab(ex+12, ey+20, EXIT, 3, "EXIT", ez)

# ---- color legend (upper-left open area) ----
lx,ly,dz = -486.0, -600.0, -23.0
lab(lx, ly-18, (60,54,48), 2, "-_LEGEND_-", dz)
legend=[('gm','Guild_/_Guard'),('spell','Spell_Vendor'),('craft','Craft_Supply'),
        ('econ','Banker_/_Mote'),('exit','Zone_Exit')]
for i,(cat,txt) in enumerate(legend):
    yy=ly+i*26; c=D.COL[cat]
    square(lx+7, yy, c, dz, r=6)
    lab(lx+20, yy+4, (55,50,45), 1, txt, dz)

# ---- write with the original seed exit line preserved at the top ----
seed=open('newsebexp_1_seed.txt').read().strip()
out=[seed]+L+P
open('newsebexp_1.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('wrote newsebexp_1.txt  lines=%d (L=%d P=%d + seed)'%(len(out),len(L),len(P)))
