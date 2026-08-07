"""Recolor the base geometry BY AREA -> newsebexp_colored base.
Same geometry as newsebexp.txt, but each region tinted a distinct atlas hue so
the sub-areas read at a glance. Water stays blue; the portal marker stays purple.
This REPLACES the base layer (swap in for newsebexp.txt) -- it is not an overlay,
to avoid drawing every wall twice."""
import render_svg as R

segs, _ = R.parse_file('newsebexp.txt')   # (x1,y1,x2,y2,color)

# ---- area palette (muted, parchment-friendly; markers still pop over these) ----
GUILD   = (150,110, 52)   # warm gold  - martial guild halls (top)
BAZAAR  = ( 74,118, 82)   # civic green - vendor & bank halls
GROTTO  = ( 74,104,150)   # slate blue  - west water grotto
PASSAGE = (120,100, 70)   # stone brown - central passages
VAULT   = (116, 84,124)   # dusk violet - pillared temple vaults
CAVERN  = ( 58,112,122)   # deep teal   - sunken caverns (bottom)
WATER   = ( 40, 95,200)   # rivers / pools (kept blue in every area)
PORTAL  = (150,  0,200)   # zone-line marker in the base (kept as-is)

def is_water(c):
    r,g,b=c; return b>150 and b>r+40 and b>g+40
def is_portal(c):
    r,g,b=c; return (r,g,b)==(150,0,200) or (b>150 and r>110 and g<60)

def area(x,y):
    # y is EQ-native (increases downward; top of map is most-negative y)
    if y <= -400:                         # top band
        return GUILD if x >= 0 else GROTTO
    if y <= -20:                          # upper-mid band
        return BAZAAR if x >= 0 else GROTTO
    if y <= 330:                          # central passages (full width)
        return PASSAGE
    if y <= 640:                          # temple vaults / pillared chambers
        return VAULT
    return CAVERN                         # sunken caverns (bottom)

out=[]
for x1,y1,x2,y2,c in segs:
    if is_water(c):      col=WATER
    elif is_portal(c):   col=PORTAL
    else:                col=area((x1+x2)/2,(y1+y2)/2)
    out.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000,  %d, %d, %d"%(x1,y1,x2,y2,col[0],col[1],col[2]))

open('newsebexp_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
# tally
from collections import Counter
tally=Counter()
for x1,y1,x2,y2,c in segs:
    if is_water(c): tally['water']+=1
    elif is_portal(c): tally['portal']+=1
    else:
        col=area((x1+x2)/2,(y1+y2)/2)
        name={GUILD:'guild',BAZAAR:'bazaar',GROTTO:'grotto',PASSAGE:'passage',VAULT:'vault',CAVERN:'cavern'}[col]
        tally[name]+=1
print('wrote newsebexp_colored.txt  L=%d'%len(out))
for k,v in tally.most_common(): print('  %-8s %d'%(k,v))
