"""Blackburrow markers (_1): full wiki roster, (-b,-a) transform, per-floor Z, floor tags."""
import numpy as np
P=np.load('geo.npy'); mz=(P[:,2]+P[:,5])/2
b1,b2=[float(x) for x in open('floorcuts.txt').read().split()]
real=P[mz<120]; zr=(real[:,2]+real[:,5])/2
BAND={'F1':(b2,1e9),'F2':(b1,b2),'F3':(-1e9,b1)}

def wn(p,q): return (-q,-p)                 # validated wiki(p,q)->native
def sampleZ(x,y,floor):
    lo,hi=BAND[floor]; m=(zr>=lo)&(zr<hi); S=real[m]
    mxy=np.c_[(S[:,0]+S[:,3])/2,(S[:,1]+S[:,4])/2]
    d=(mxy[:,0]-x)**2+(mxy[:,1]-y)**2
    k=np.argsort(d)[:12]
    return float(np.median(np.concatenate([S[k,2],S[k,5]])))

COL={'exit':(160,105,0),'boss':(110,0,60),'named':(165,60,20),'feat':(30,70,90)}

# (wiki_p, wiki_q, floor, category, label)   -- label uses underscores
ROSTER=[
 (-159, 39,'F1','exit','To_Qeynos_Hills_(Succor)'),
 # Everfrost zone-in from player /loc 95,-340 -> native (340,-95)
 ( 95,-340,'F1','exit','To_Everfrost_Peaks'),
 # ---- Floor 1 (top ravine) ----
 (126,-201,'F1','feat','Plague_Rat_Storeroom_[F1-1]'),
 (  6,-119,'F1','feat','The_Pit_+_a_Razorgill_[F1-2]'),
 ( 66, -21,'F1','named','Splitpaw_Sentry_(Ranger_10)_[F1-2]'),
 (160,-140,'F1','named','Tranixx_Darkpaw_(10,_patrols)_[F1-4]'),
 # ---- Floor 2 (mid dens) ----
 (189, 140,'F2','named','Sabertooth_Clan_Necromancer_(15)_[F2-2]'),
 (265,-124,'F2','named','Mannan_of_the_Sabertooth_(15)_[F2-3]'),
 ( 89,-147,'F2','named','Refugee_Splitpaw_(Shaman_14)_[F2-4]'),
 ( 55,-320,'F2','named','The_Gnoll_High_Shaman_(15,_Quest)_[F2-5]'),
 ( 23,-341,'F2','named','A_Gnoll_Commander_(13-15)_[F2]'),
 (292,-115,'F2','named','A_Gnoll_Commander_(13-15)_[F2]'),
 (-97, -38,'F2','named','Splitpaw_Commander_(14)_[F2-7]'),
 (-85,-286,'F2','named','Socho_Darkpaw_(Rogue_13)_[F2-8]'),
 (-86, 117,'F2','named','A_Gnoll_Tactician_(13-15)'),
 # ---- Floor 3 (deep lake) ----
 (160,-385,'F3','boss','Lord_Elgnub_(SK_22,_BOSS)_[F3-9]'),
 (-150, 384,'F3','boss','Sabertooth_Overseer_(Berserker_20)_[F3-2]'),
 ( 49, 357,'F3','boss','Splitpaw_Sharpshooter_(Ranger_20)_[F3-5]'),
 (-162, 452,'F3','named','Refugee_Splitpaw_(Monk_18)_[F3-3]'),
 ( 53, 386,'F3','named','Master_Brewer_(18,_Casks)_[F3-4]'),
 ( 53, 356,'F3','named','A_Gnoll_Brewer_(17)_[F3-4]'),
 (164, 157,'F3','named','Splitpaw_Explorer_(Rogue_18)_[F3-7]'),
 (251, 363,'F3','named','Splitpaw_Commander_(14)_[F3-6]'),
]

L=[];Pl=[]
def add(x1,y1,x2,y2,c,z): L.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z,x2,y2,z,c[0],c[1],c[2]))
def lab(x,y,c,s,t,z): Pl.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,z,c[0],c[1],c[2],s,t))
def diamond(x,y,c,z,r=7):
    add(x,y-r,x+r,y,c,z);add(x+r,y,x,y+r,c,z);add(x,y+r,x-r,y,c,z);add(x-r,y,x,y-r,c,z)
def star(x,y,c,z,r=9):  # boss
    for a in range(0,360,45):
        import math; add(x,y,x+r*math.cos(math.radians(a)),y+r*math.sin(math.radians(a)),c,z)
    diamond(x,y,c,z,r*0.6)
def square(x,y,c,z,r=6):
    add(x-r,y-r,x+r,y-r,c,z);add(x+r,y-r,x+r,y+r,c,z);add(x+r,y+r,x-r,y+r,c,z);add(x-r,y+r,x-r,y-r,c,z)
def chevron(x,y,c,z,r=8):
    add(x-r,y+r*0.6,x,y-r*0.5,c,z);add(x,y-r*0.5,x+r,y+r*0.6,c,z)

report=[]
for p,q,fl,cat,txt in ROSTER:
    x,y=wn(p,q); z=sampleZ(x,y,fl); c=COL[cat]
    report.append((txt,x,y,z))
    if cat=='boss': star(x,y,c,z)
    elif cat=='exit': square(x,y,c,z,7)
    elif cat=='feat': diamond(x,y,c,z,8)
    else: diamond(x,y,c,z,6)
    sz=3 if cat in('boss','exit') else 2
    lab(x+10,y-3,c,sz,txt,z)

open('blackburrow_1.txt','w',newline='').write('\r\n'.join(L+Pl)+'\r\n')
print('wrote blackburrow_1.txt  L=%d P=%d'%(len(L),len(Pl)))
for t,x,y,z in report[:4]+report[-3:]: print('  %-42s (%.0f,%.0f,z=%.1f)'%(t,x,y,z))
# Everfrost sanity: nearest F1 geometry distance
ex,ey=wn(95,-340)
m=(zr>=b2); S=real[m]; mxy=np.c_[(S[:,0]+S[:,3])/2,(S[:,1]+S[:,4])/2]
d=np.sqrt(((mxy[:,0]-ex)**2+(mxy[:,1]-ey)**2)).min()
print('Everfrost native (%.0f,%.0f) nearest F1 geo dist=%.1f'%(ex,ey,d))
