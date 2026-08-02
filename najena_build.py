"""najena_build.py -- Dark Elf undead dungeon decoration via eqmap_toolkit (cobwebby motif)."""
import numpy as np, random, math
import eqmap_toolkit as T
random.seed(7)
BASE="/mnt/user-data/outputs/najena.txt"; OUT="/mnt/user-data/outputs/najena_2.txt"
DK=(55,40,65); WEB=(150,140,160); GRID=(95,80,110); TITLE=(155,80,120); TSH=(60,40,60)
BONE=(205,200,190); SPIDER=(52,44,60); PUR=(110,70,120)

A=np.array([[float(x) for x in l[2:].split(',')[:6]] for l in open(BASE).read().replace('\r\n','\n').split('\n') if l.strip().startswith('L')])
bbox=(A[:,[0,3]].min(),A[:,[0,3]].max(),A[:,[1,4]].min(),A[:,[1,4]].max())
minx,maxx,miny,maxy=bbox
cv=T.Canvas(bbox, pad=460, gstep=170)

# grid + dark web-cornered frame
T.grid(cv, GRID)
T.frame(cv, DK, PUR, step=95, depth=70, inset=45,
        corner=lambda c,x,y,sx,sy: T.web_corner(c,x,y,sx,sy,WEB,reach=360))

# extra cobwebs draped along the top margin
for fx in np.linspace(minx+200, maxx-200, 5):
    yy=cv.by0+random.uniform(70,150)
    for r in (60,120,180):
        cv.add(fx, yy, fx-r*0.7, yy+r*0.6, WEB); cv.add(fx, yy, fx+r*0.7, yy+r*0.6, WEB)
    for a in np.linspace(-0.6,0.6,4): cv.add(fx,yy,fx+math.sin(a)*180,yy+math.cos(a)*180,WEB)

# undead doodles scattered through the LEFT / RIGHT / BOTTOM margins
def in_margin(x,y): return not (minx<x<maxx and miny<y<maxy)
lx=cv.margin_x('left'); rx=cv.margin_x('right')
skull_rows=[cv.row_y(1),cv.row_y(3)]; bone_rows=[cv.row_y(0),cv.row_y(2),cv.row_y(4)]
for y in skull_rows: T.skull(cv, lx+random.uniform(-40,40), y, 40, BONE)
for y in bone_rows:  T.bone_pile(cv, lx+random.uniform(-40,40), y+90, 46, BONE)
T.spider(cv, lx, cv.row_y(2)-40, 60, SPIDER)
# right column: compass goes top; put a spider + bones lower
T.spider(cv, rx, cv.row_y(3), 60, SPIDER)
T.bone_pile(cv, rx+random.uniform(-30,30), cv.row_y(4), 46, BONE)
T.skull(cv, rx, cv.row_y(2), 40, BONE)
# bottom margin skulls + bones
for bx in np.linspace(minx+250, maxx-250, 4):
    yy=cv.by1-random.uniform(120,230)
    (T.skull if random.random()<0.5 else T.bone_pile)(cv, bx, yy, 42, BONE)

# title + skull compass (2nd row, right, on top)
T.title(cv, "NAJENA", TITLE, shadow=TSH)
T.compass(cv, rx, cv.row_y(0), 130, ring=(WEB,PUR), rose=(WEB,PUR),
          center=T.skull_motif, center_colors=(BONE,PUR), label=PUR, n_label=WEB, arrow=WEB)

cv.write(OUT)
print(f"{OUT}: {len(cv.L)} L + {len(cv.P)} P")
