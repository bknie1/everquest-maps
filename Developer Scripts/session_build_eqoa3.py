# EQOA fun-label _3 layer: muted violet, size-3, small sketch doodle per label. Placed by map position (guesstimate).
V=(150,90,150)
def P(x,y,label,z=0.0,s=3): return "P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,z,V[0],V[1],V[2],s,label)
def L(x1,y1,x2,y2,z=0.0): return "L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z,x2,y2,z,V[0],V[1],V[2])
def doodle(x,y,r):
    # a small sketched cairn/marker: diamond + base dot (EQOA easter-egg glyph)
    out=[L(x,y-r, x+r,y), L(x+r,y, x,y+r), L(x,y+r, x-r,y), L(x-r,y, x,y-r)]  # diamond
    out+=[L(x-r*0.5,y+r*1.4, x+r*0.5,y+r*1.4)]  # little base line
    return out
# zone -> list of (label, native_x, native_y, doodle_radius)
ZONES={
 'qeytoqrg':[('Bear_Cave',-600,-2000,120),('Mayfly_Glade',1500,-3000,120),('Forkwatch',600,-4500,120)],
 'qey2hh1':[('Jareds_Blight',3000,1000,260),('Alseops_Wall',7000,-200,260),('Strags_Rest',9500,1500,260)],
 'highpass':[('Ferrans_Hope',150,400,55),('Trails_End',-300,-300,55)],
}
import os
O='/mnt/user-data/outputs'
for z,items in ZONES.items():
    out=[]
    for lab,x,y,r in items:
        out+=doodle(x,y,r)
        out.append(P(x+r*1.6,y,lab))  # label offset to the right of the doodle
    open(f'{O}/{z}_3.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
    print(f'{z}_3.txt: {len(items)} EQOA labels, {len(out)} lines')
