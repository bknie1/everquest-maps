"""Neriak place labels: the Foreign Quarter's two racial districts, and the
Commons row of shops and halls.

Placement is by /loc, not by which map the list arrived under — native = (-loc2, -loc1)
and the zone is whichever one actually contains the point.

Guild halls are colour-classified rather than spelled out.
"""
import os, collections

O = '/mnt/user-data/outputs'

VENUE   = (40, 26, 58)     # near-black plum: shops, taverns, dens
GUILD   = (62, 24, 92)     # deep purple: guild halls (classified, not labelled)
LANDMARK= (28, 48, 112)    # dark blue: civic buildings
CRAFT   = (104, 56, 26)    # dark brown-red: tradeskill
AREA    = (70, 22, 96)     # dark purple: district names

# name, loc1, loc2, z, ink, forced zone (None = decide by extent)
POI = [
    ("Toadstool",                  -156.95, -1013.17, -38.15, VENUE,    None),
    ("The_Indigo_Brotherhood",      -27.84, -1132.86, -24.19, GUILD,    None),
    ("House_of_D`Abth",             -28.10, -1030.23, -38.15, LANDMARK, None),
    ("Forge_House",                  59.71,  -930.43, -38.15, CRAFT,    None),
    ("Neriak_Down_Under_2",          32.61,  -951.59, -38.15, VENUE,    None),
    ("The_Burnished_Coin",           25.97,  -925.40, -52.15, VENUE,    None),
    ("The_Refined_Palate",           63.61,  -879.35, -52.15, VENUE,    None),
    ("Bounty_of_the_Earth",          36.44,  -879.25, -52.15, VENUE,    None),
    ("The_Blind_Fish",               29.96,  -851.32, -52.15, VENUE,    None),
    ("Neriak_Down_Under_1",          76.50,  -813.20, -38.15, VENUE,    None),
    ("The_Bleek_Fletcher",         -147.41, -1090.26, -37.15, VENUE,    None),
    ("Task_Master`s_Quarters",        -5.00,   -89.77,   3.81, LANDMARK, 'neriaka'),
    # --- Northern Quarter: the neutral races ---
    ("Silk_Underground",             132.01,  -163.91,   3.81, VENUE,    'neriaka'),
    ("Slugs_Tavern",                 189.56,  -196.62,  17.81, VENUE,    'neriaka'),
    ("The_Smugglers_Inn",            151.62,   -98.78,   2.81, VENUE,    'neriaka'),
    ("Drana`s_Bread_n`_Butcher",     121.16,  -244.43,   3.81, VENUE,    'neriaka'),
    # --- Southern Quarter: trolls and ogres ---
    ("Bulls_Pit",                   -344.42,  -268.91,  -0.19, VENUE,    'neriaka'),
    ("Shinie_Tings",                -303.59,  -188.80,   3.81, VENUE,    'neriaka'),
    ("Bronk`s",                     -251.15,  -375.49,   6.81, VENUE,    'neriaka'),
    ("Bites_n`_Pieces",             -349.09,  -134.10,   3.81, VENUE,    'neriaka'),
    ("Pig_Sticker",                 -296.27,  -437.46,  18.81, VENUE,    'neriaka'),
    ("Southern_Guard_House",        -466.42,  -419.80,   4.81, LANDMARK, 'neriaka'),
]
NORTH = {"Silk_Underground","Slugs_Tavern","The_Smugglers_Inn","Drana`s_Bread_n`_Butcher"}
SOUTH = {"Bulls_Pit","Shinie_Tings","Bronk`s","Bites_n`_Pieces","Pig_Sticker","Southern_Guard_House"}

def extent(z):
    xs=[];ys=[]
    for l in open(f'{O}/{z}.txt',encoding='utf-8',errors='replace'):
        if l.startswith('L'):
            f=l[2:].split(','); xs+=[float(f[0]),float(f[3])]; ys+=[float(f[1]),float(f[4])]
    return min(xs),max(xs),min(ys),max(ys)
E={z:extent(z) for z in ['neriaka','neriakb','neriakc']}

by_zone = collections.defaultdict(list)
north_pts=[]; south_pts=[]
for name, l1, l2, lz, ink, forced in POI:
    nx, ny = -l2, -l1
    if forced: z = forced
    else:
        fits=[k for k,e in E.items() if e[0]<=nx<=e[1] and e[2]<=ny<=e[3]]
        z = fits[0] if fits else 'neriaka'
    size = 3 if ink in (LANDMARK, GUILD) else 2
    by_zone[z].append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(nx,ny,lz,*ink,size,name))
    if name in NORTH: north_pts.append((nx,ny))
    if name in SOUTH: south_pts.append((nx,ny))

# district names, set above each cluster
for pts, label in ((north_pts,'Northern_Quarter'), (south_pts,'Southern_Quarter')):
    cx = sum(p[0] for p in pts)/len(pts)
    cy = min(p[1] for p in pts) - 60
    by_zone['neriaka'].append("P %.4f, %.4f, 0.0000, %d, %d, %d, 3, %s"%(cx,cy,*AREA,label))
    print(f"  {label} centred at ({cx:.1f}, {cy:.1f}) over {len(pts)} places")

for z, lines in by_zone.items():
    p=f'{O}/{z}_3.txt'
    prev = open(p,'rb').read().decode('utf-8','replace').rstrip('\r\n') if os.path.exists(p) else ''
    body = ('\r\n'.join([prev]+lines) if prev else '\r\n'.join(lines))
    open(p,'w',newline='').write(body+'\r\n')
    print(f"{z}_3: +{len(lines)} labels")

# ---- guild halls: name the place, let the colour say what it is ----
p=f'{O}/neriakb_1.txt'
raw=[l.rstrip('\r\n') for l in open(p,encoding='utf-8',errors='replace') if l.strip()]
out=[]
for l in raw:
    if 'Tower_of_the_Spurned' in l:
        f=l[1:].split(',')
        f[3]=' %d'%GUILD[0]; f[4]=' %d'%GUILD[1]; f[5]=' %d'%GUILD[2]
        f[7]=' Tower_of_the_Spurned'
        out.append('P'+','.join(f)); print("  renamed -> Tower_of_the_Spurned (guild ink)")
    elif 'Warrior_Guild_Hall' in l:
        print("  dropped the generic Warrior Guild Hall marker (superseded by The Indigo Brotherhood)")
    else: out.append(l)
open(p,'w',newline='').write('\r\n'.join(out)+'\r\n')

for z in ['neriaka','neriakb']:
    for suf in ['_1','_3']:
        b=open(f'{O}/{z}{suf}.txt','rb').read()
        assert sum(1 for i,ch in enumerate(b) if ch==10 and (i==0 or b[i-1]!=13))==0, f'{z}{suf}'
print("\nCRLF OK")
