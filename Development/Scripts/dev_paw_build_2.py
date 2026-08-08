"""Blackburrow decoration (_2): gnoll-cavern theme.
Shaded brown border, stalactite ceiling, BLACKBURROW title, gnoll-head compass,
and margin sketches (casks, totem, gnoll face, snakes, bone piles, paw trails,
hollow tree). Every sketch is placed through track(), which records the exact
line-extent of each element and validates that no two DISTINCT elements overlap."""
import random, math
from eqmap_toolkit import Canvas, frame, grid, title, compass, paw_print, skull, bone_pile
import bb_decor as G
random.seed(1990)

MINX,MAXX,MINY,MAXY = -489.0, 397.0, -349.0, 254.0
PAD, INSET = 235, 44
cv = Canvas((MINX,MAXX,MINY,MAXY), PAD)
STONE=G.STONE; STONE_L=G.STONE_L; MOSS=G.MOSS; BANNER=G.BANNER; BONE=G.BONE
BORDER_DK=(74,50,30); BORDER_MD=(122,84,48); BORDER_SH=(150,112,74)

LX=(cv.bx0+INSET+cv.minx)/2
RX=(cv.bx1-INSET+cv.maxx)/2

# ---- element tracker: one track() call == one decorative element ----
ELEMENTS=[]
def track(name, fn):
    i0=len(cv.L); fn(); seg=cv.L[i0:]
    if not seg: return
    xs=[];ys=[]
    for l in seg:
        f=l[2:].split(','); xs+= [float(f[0]),float(f[3])]; ys+=[float(f[1]),float(f[4])]
    ELEMENTS.append([name,min(xs),min(ys),max(xs),max(ys)])

# ======================================================= structural (not tracked)
grid(cv, (176,166,146), step=150)
G.shade_border(cv, INSET, BORDER_SH, step=12)
frame(cv, outer=BORDER_DK, inner=BORDER_MD, step=64, depth=30, inset=INSET,
      corner=lambda c,x,y,sx,sy: G.rock_corner(c,x,y,sx,sy,color=BORDER_DK,reach=46))
title(cv, "BLACKBURROW", STONE, shadow=(150,120,80), height=118)

# ======================================================= ceiling / floor spikes
ceil_y = cv.by0+INSET+6
for k,x in enumerate(range(-430, 400, 96)):
    track(f"stalactite{k}", lambda x=x: G.stalactite(cv, x, ceil_y, h=random.randint(34,60), w=12, color=STONE))
GROUND = cv.by1-INSET-46
for k,x in enumerate((-420,-213,68,315)):
    track(f"stalagmite{k}", lambda x=x: G.stalagmite(cv, x, GROUND, h=random.randint(18,26), w=8, color=STONE))

# ======================================================= LEFT margin
track("cask_stack",  lambda: G.cask_stack(cv, LX, -250))
def _paw_trail_L():
    for i,py in enumerate(range(-150,60,46)):
        paw_print(cv, LX+(12 if i%2 else -12), py, color=(120,104,86))
track("paw_trail_L", _paw_trail_L)
track("gnoll_face",  lambda: G.gnoll_face(cv, LX, 140, s=82, color=STONE))
track("bone_pile_L", lambda: G.bone_skull_pile(cv, LX, 236, s=46))

# ======================================================= RIGHT margin
track("totem_R",  lambda: G.totem(cv, RX, -150, h=96))
track("snake_R",  lambda: G.snake(cv, RX-46, 60, length=104, amp=15, color=MOSS))
def _paw_R():
    paw_print(cv, RX-14, 150, color=(120,104,86)); paw_print(cv, RX+16, 186, color=(120,104,86))
track("paw_R", _paw_R)

# ======================================================= BOTTOM row (shifted LEFT to clear the compass)
track("cask_b1",   lambda: G.cask(cv, -320, GROUND-20, 30, 40))
track("cask_b2",   lambda: G.cask(cv, -252, GROUND-18, 26, 36, G.WOOD_D))
track("hollow_tree", lambda: G.hollow_tree(cv, -150, GROUND-6, h=90))
track("bone_pile_b", lambda: G.bone_skull_pile(cv, 10, GROUND, s=38))
track("snake_b",   lambda: G.snake(cv, 90, GROUND-14, length=100, amp=12, color=MOSS))
track("totem_b",   lambda: G.totem(cv, 240, GROUND, h=84))

# ======================================================= compass (open bottom-right margin)
band0=INSET; band1=PAD; bc=(band0+band1)/2; CRpad=max(70,(band1-band0)/2/1.28*0.66)
track("compass", lambda: compass(cv, cv.bx0+bc, cv.by1-bc, CRpad,
        ring=(BORDER_DK, BORDER_MD), rose=(BORDER_DK, (120,96,72)),
        center=G.gnoll_head_motif, center_colors=(BORDER_DK,(150,60,44)),
        label=BORDER_DK, n_label=BORDER_DK, arrow=BORDER_DK))

# ======================================================= validate: no element overlaps
def overlaps(a,b,pad=2):
    return not (a[3]<b[1]-pad or b[3]<a[1]-pad or a[4]<b[2]-pad or b[4]<a[2]-pad)
hits=[]
for i in range(len(ELEMENTS)):
    for j in range(i+1,len(ELEMENTS)):
        if overlaps(ELEMENTS[i],ELEMENTS[j]):
            hits.append((ELEMENTS[i][0],ELEMENTS[j][0]))
cv.write('blackburrow_2.txt')
print('wrote blackburrow_2.txt  L=%d P=%d  elements=%d'%(len(cv.L),len(cv.P),len(ELEMENTS)))
if hits:
    print('OVERLAPS:', hits)
else:
    print('VALIDATION OK: no overlapping decoration elements')
