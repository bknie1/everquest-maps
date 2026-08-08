# Continent-wide EQOA fun-label _3 pass across ALL outdoor Antonica zones.
# muted violet, size-3, diamond doodle. Placed by-position (guesstimate). APPENDS to existing _3.
import os
V=(150,90,150); O='/mnt/user-data/outputs'
def Pl(x,y,label,z=0.0,s=3): return "P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,z,V[0],V[1],V[2],s,label)
def Ll(x1,y1,x2,y2,z=0.0): return "L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z,x2,y2,z,*V)
def doodle(x,y,r):
    return [Ll(x,y-r,x+r,y),Ll(x+r,y,x,y+r),Ll(x,y+r,x-r,y),Ll(x-r,y,x,y-r),Ll(x-r*0.5,y+r*1.4,x+r*0.5,y+r*1.4)]

def bbox(zone):
    xs=[];ys=[]
    for l in open(f'{O}/{zone}.txt',encoding='utf-8',errors='replace'):
        if l.startswith('L'):
            f=l[2:].split(',')
            try: xs+=[float(f[0]),float(f[3])]; ys+=[float(f[1]),float(f[4])]
            except: pass
    return min(xs),max(xs),min(ys),max(ys)
def existing_pts(zone):
    pts=[]
    for suf in ['_1','_3']:
        p=f'{O}/{zone}{suf}.txt'
        if os.path.exists(p):
            for l in open(p,encoding='utf-8',errors='replace'):
                if l.startswith('P'):
                    f=l[1:].split(',')
                    try: pts.append((float(f[0]),float(f[1])))
                    except: pass
    return pts

# spread patterns (normalized fx,fy) by label count
PAT={1:[(0.5,0.4)],2:[(0.34,0.34),(0.66,0.62)],3:[(0.3,0.3),(0.62,0.5),(0.4,0.74)],
     4:[(0.28,0.3),(0.7,0.32),(0.35,0.72),(0.68,0.7)]}

# zone -> curated EQOA fun-labels (outdoor Antonica). Skips: cities/dungeons/non-Tunaria.
ZL={
 'everfrost':['Snowblind_Plains','Anu_Village','Frosteye_Valley'],
 'qrg':['Jethros_Cast','Wyndhaven'],
 'northkarana':['Bandit_Hills','Spirit_Talkers_Wood'],
 'southkarana':['Aviak_Village','Centaur_Valley','Fort_Solitude'],
 'eastkarana':['Saerk_Towers','Mu_Lins_Reach','Moss_Mouth_Cavern'],
 'misty':['Baga_Village','Mount_Haledrake'],
 'rivervale':['Merry-by-Water'],
 'kithicor':['North_Kithicor','The_Green_Rift'],
 'commons':['Bastable_Village','Tomb_of_Kings'],
 'ecommons':['Temple_of_Light','Babble-by-Water'],
 'nektulos':['Collinridge_Cemetery','Thedruk'],
 'lavastorm':['Kara_Village','NE_Mountain_Boundary'],
 'nro':['Deathfist_Citadel','Muriels_Tea_Garden','Northwestern_Ro'],
 'sro':['Fox_Canyons','Al-Farak_Ruins','Sycamore_Joys_Rest'],
 'oasis':['Sea_of_Lions'],
 'innothule':['Kerplunk_Outpost','Lake_Noregard','Burial_Mounds'],
 'feerrott':['West_Feerrott','Envar','Ogre_Ruins'],
 'rathemtn':['Cyclops_Fortress','Sphinx_Pyramid','Geomancers_Citadel'],
 'lakerathe':['Kelinar'],
}
report=[]
for zone,labels in ZL.items():
    if not os.path.exists(f'{O}/{zone}.txt'): report.append((zone,'MISSING BASE',0)); continue
    minx,maxx,miny,maxy=bbox(zone); w=maxx-minx; h=maxy-miny; span=max(w,h)
    r=max(40,int(span*0.018))
    ex=existing_pts(zone); mind=span*0.05
    pat=PAT.get(len(labels),PAT[3])
    new=[]
    for i,lab in enumerate(labels):
        fx,fy=pat[i%len(pat)]
        x=minx+fx*w; y=miny+fy*h
        # nudge away from existing points
        for _ in range(6):
            if all((x-px)**2+(y-py)**2 > mind*mind for px,py in ex): break
            x+=span*0.06; y-=span*0.04
        ex.append((x,y))
        new+=doodle(x,y,r); new.append(Pl(x+r*1.6,y,lab))
    # APPEND to existing _3 (preserve bytes), else create
    p3=f'{O}/{zone}_3.txt'
    old=b''
    if os.path.exists(p3): old=open(p3,'rb').read()
    if old and not old.endswith(b'\r\n'): old+=b'\r\n'
    open(p3,'wb').write(old + ('\r\n'.join(new)+'\r\n').encode())
    report.append((zone, 'APPEND' if old else 'NEW', len(labels)))
for z,mode,n in report: print(f"  {z:14} {mode:7} +{n} labels")
print(f"\n{sum(n for _,_,n in report)} EQOA labels across {len(report)} zones")
