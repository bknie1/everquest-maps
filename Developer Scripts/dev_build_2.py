"""Blackburrow decoration (_2): gnoll-cavern theme.
Rocky border, stalactite ceiling, BLACKBURROW title, gnoll-head compass, and
margin doodles (brewery casks, clan totem, gnoll figure, giant snake, bones,
paw-print trails) laned cleanly between the inner frame and the map."""
import random, math
from eqmap_toolkit import Canvas, frame, grid, title, compass, paw_print, skull, bone_pile, spike_pillar
import bb_decor as G
random.seed(1990)

MINX,MAXX,MINY,MAXY = -489.0, 397.0, -349.0, 254.0
PAD, INSET = 235, 44
cv = Canvas((MINX,MAXX,MINY,MAXY), PAD)
Z=0.0
STONE=G.STONE; STONE_L=G.STONE_L; MOSS=G.MOSS; BANNER=G.BANNER; BONE=G.BONE

# lanes (clean band between inner frame line and content edge)
LX=(cv.bx0+INSET+cv.minx)/2
RX=(cv.bx1-INSET+cv.maxx)/2

# 1) grid under everything
grid(cv, (176,166,146), step=150)

# 2) rocky border + jagged rock corners
frame(cv, outer=STONE, inner=STONE_L, step=64, depth=30, inset=INSET,
      corner=lambda c,x,y,sx,sy: G.rock_corner(c,x,y,sx,sy,color=STONE,reach=120))

# 3) title
title(cv, "BLACKBURROW", STONE, shadow=(150,120,80), height=118)

# 4) stalactites hanging from the top inner border (cave ceiling)
ceil_y = cv.by0+INSET+6
for x in range(-430, 400, 96):
    G.stalactite(cv, x, ceil_y, h=random.randint(34,60), w=12, color=STONE)
# a few stalagmites rising from the bottom border
floor_y = cv.by1-INSET-6
for x in range(-380, 400, 130):
    G.stalagmite(cv, x, floor_y, h=random.randint(26,44), w=12, color=STONE)

# 5) LEFT margin doodles
G.cask_stack(cv, LX, -250)
cv.label(LX-40, -196, STONE, 1, "Blackburrow_Stout")
for i,py in enumerate(range(-150,60,46)):            # paw-print trail down the lane
    paw_print(cv, LX+(12 if i%2 else -12), py, color=(120,104,86))
G.gnoll_face(cv, LX, 140, s=82, color=STONE)
G.bone(cv, LX-18, 232, 34, ang=0.5); G.bone(cv, LX+14, 240, 30, ang=-0.4)

# 6) RIGHT margin doodles
G.totem(cv, RX, -150, h=96)
G.snake(cv, RX-46, 60, length=104, amp=15, color=MOSS)
skull(cv, RX, 150, 16, color=BONE)
paw_print(cv, RX-14, 210, color=(120,104,86)); paw_print(cv, RX+16, 244, color=(120,104,86))

# 7) BOTTOM margin row
by = cv.by1-INSET-30
G.cask(cv, -300, by, 30, 40); G.cask(cv, -232, by, 26, 36, G.WOOD_D)
G.hollow_tree(cv, -120, cv.by1-INSET-18, h=94)           # gnoll false-floor tree
bone_pile(cv, 34, by, 18, color=BONE)
G.snake(cv, 150, by-6, length=110, amp=12, color=MOSS)
G.totem(cv, 322, by+30, h=84)

# 8) compass -- gnoll head center, tucked in open top-left area of the map
compass(cv, cv.minx+120, cv.miny+150, 92,
        ring=(STONE, STONE_L), rose=(STONE, (110,96,80)),
        center=G.gnoll_head_motif, center_colors=(STONE,(150,60,44)),
        label=STONE, n_label=STONE, arrow=STONE)

cv.write('blackburrow_2.txt')
print('wrote blackburrow_2.txt  L=%d P=%d'%(len(cv.L),len(cv.P)))
