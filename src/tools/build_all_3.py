"""Generate the complete EQOA `_3` easter-egg layer across every listed zone.

  - on-map NARROW DIAMONDS, 25% smaller than the old pass, sized by tier
      tier 3 -> size 4 (cities/forts/iconic)   2 -> size 3 (villages/landmarks)   1 -> size 2 (ruins/camps)
  - MARGIN SIGNPOSTS: violet arrow + "To X" in the margin band on the matching side
  - appends to existing `_3` content (e.g. Lavastorm's vents); strips only prior violet work
"""
import math, importlib.util, os
spec=importlib.util.spec_from_file_location("ab","/home/claude/work/align_build.py")
ab=importlib.util.module_from_spec(spec); spec.loader.exec_module(ab)
ANT, ODUS = ab.ANT, ab.ODUS
import eqoa_pos as EP, json
JUSTIFIED=json.load(open('/home/claude/work/justified_dia.json'))
O='/mnt/user-data/outputs'
V=(150,90,150)

# Odus signposts (separate landmass - curated, canonical names)
ODUS_ARROWS={
 'Toxxulia Forest':[('West Toxxulia','NW',4),('East Toxxulia','NE',4),
    ("Syhilthis' Dwell",'N',3),('Old Arcadin','NE',3),('West Plateau','NW',2),('The Hunt','S',2)],
 'Stonebrunt Mtns':[('North Barren Coast','NE',4),('South Barren Coast','SE',4),
    ('Cape Dreg','SE',3),('The Vastly Deep','E',4),('East Plateau','N',2),('Gulf of Uzun','SW',2)],
 'Erudin':[('Old Arcadin','SE',4),('West Plateau','NW',4),('East Plateau','NE',3),
    ("Syhilthis' Dwell",'W',2)],
 'Kerra Isle':[('Abysmal Sea','W',4),('West Toxxulia','NE',3),('The Hunt','SE',2)],
 'Paineel':[('Abysmal Sea','W',4),('The Hunt','SW',3),('Stone of Morthalis','S',3),
    ('South Toxxulia','N',3)],
 'The Warrens':[('Gulf of Uzun','S',4),('South Barren Coast','E',3),('Stone of Morthalis','SW',2)],
 "Erud's Crossing":[('The Vastly Deep','SE',4),('East Plateau','W',3),('North Barren Coast','S',3)],
}
SIZE={3:4,2:3,1:2}

# ---- flavour signposts: the deliberately-invented modern-context names ----
# (EQOA cities read as RUINS five centuries on)
FLAVOUR={
 'Everfrost Peaks':[('Tethelin Forest','E'),('Ruins of Fayspire','NE'),
                    ('The Northlands','NW'),('The Nest','SE')],
 'Lavastorm Mountains':[('Ruins of Fayspire','W'),('Tethelin Forest','SW')],
 'Blackburrow':[('Jaggedpine','W')],
}
# modern-context renames
RENAME={"Klik'Anon":"Ruins of Klik'Anon", 'Fayspire':'Ruins of Fayspire',
        'Moradhim':'Ruins of Moradhim', 'Arcadin':'Old Arcadin',
        'Tethelin':'Tethelin Forest'}

def bbox(p):
    xs=[];ys=[]
    for l in open(p,encoding='utf-8',errors='replace'):
        if l.startswith('L'):
            f=l[2:].split(',')
            try: xs+=[float(f[0]),float(f[3])];ys+=[float(f[1]),float(f[4])]
            except: pass
    return (min(xs),max(xs),min(ys),max(ys)) if xs else None
def poi_pts(z):
    pts=[]
    p=f'{O}/{z}_1.txt'
    if os.path.exists(p):
        for l in open(p,encoding='utf-8',errors='replace'):
            if l.startswith('P'):
                f=l[1:].split(',')
                try: pts.append((float(f[0]),float(f[1])))
                except: pass
    return pts

# zone display-name -> file shortname
SHORT={'Everfrost Peaks':'everfrost','Blackburrow':'blackburrow','Surefall Glade':'qrg',
 'Qeynos Hills':'qeytoqrg','West Karana':'qey2hh1','North Karana':'northkarana',
 'East Karana':'eastkarana','Beholders Maze':'beholder','South Karana':'southkarana',
 'Misty Thicket':'misty','Rivervale':'rivervale','Highpass Hold':'highpass',
 'Kithicor Wood':'kithicor','West Commonlands':'commons','East Commonlands':'ecommons',
 'Nektulos Forest':'nektulos','Lavastorm Mountains':'lavastorm',
 'Northern Desert of Ro':'nro','Southern Desert of Ro':'sro','Oasis of Marr':'oasis',
 'Innothule Swamp':'innothule','Feerrott':'feerrott','Rathe Mountains':'rathemtn',
 'Lake Rathetear':'lakerathe','Cazic Thule':'cazicthule',
 'Toxxulia Forest':'tox','Stonebrunt Mtns':'stonebrunt','Erudin':'erudnext',
 'Kerra Isle':'kerraridge','Paineel':'paineel','The Warrens':'warrens',
 "Erud's Crossing":'erudsxing'}

# spread pattern: centre first, then cardinals, then diagonals (one per direction)
PAT=[(0.50,0.48),(0.50,0.20),(0.79,0.47),(0.50,0.79),(0.21,0.47),
     (0.74,0.24),(0.75,0.73),(0.25,0.74),(0.26,0.25)]

def build(zone_name, z):
    short=SHORT.get(zone_name)
    if not short or not os.path.exists(f'{O}/{short}.txt'): return None
    b=bbox(f'{O}/{short}.txt')
    f2=f'{O}/{short}_2.txt'
    fr=bbox(f2) if os.path.exists(f2) else b
    bx0,bx1,by0,by1=b; fx0,fx1,fy0,fy1=fr
    w=bx1-bx0; h=by1-by0; span=max(w,h)
    out=[]
    def Ll(x1,y1,x2,y2): out.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"%(x1,y1,x2,y2,*V))
    def Pl(x,y,t,s): out.append("P %.4f, %.4f, 0.0000, %d, %d, %d, %d, %s"%(x,y,*V,s,t))
    def diamond(cx,cy,tier):
        ry=span*(0.0075+0.0030*tier)          # 25% smaller than the previous pass
        rx=ry*0.55
        Ll(cx,cy-ry,cx+rx,cy); Ll(cx+rx,cy,cx,cy+ry)
        Ll(cx,cy+ry,cx-rx,cy); Ll(cx-rx,cy,cx,cy-ry)
        return ry
    # ---------- diamonds ----------
    ex=poi_pts(short)
    rows=JUSTIFIED.get(short,[])
    dias=sorted([(r['name'],r['tier']) for r in rows], key=lambda t:-t[1])
    SNAP={r['name']:(tuple(r['snap']) if r['snap'] else None) for r in rows}
    mind=span*0.055
    for i,(nm,tier) in enumerate(dias):
        snap=SNAP.get(nm)
        if snap:                                   # sits on a real EQ1 feature
            cx,cy=snap
            ry=diamond(cx,cy,tier)
            Pl(cx+ry*1.7, cy, nm.replace(' ','_'), SIZE[tier])
            ex.append((cx,cy))
            continue
        fx,fy=PAT[i%len(PAT)]
        cx=bx0+fx*w; cy=by0+fy*h
        for _ in range(10):
            if all((cx-px)**2+(cy-py)**2>mind*mind for px,py in ex): break
            cx+=span*0.045; cy-=span*0.030
            cx=min(max(cx,bx0+span*0.04),bx1-span*0.04)
            cy=min(max(cy,by0+span*0.04),by1-span*0.04)
        ex.append((cx,cy))
        ry=diamond(cx,cy,tier)
        Pl(cx+ry*1.7, cy, nm.replace(' ','_'), SIZE[tier])
    # ---------- signposts ----------
    dnames={r['name'] for r in JUSTIFIED.get(short,[])}
    if zone_name in ODUS_ARROWS:
        arrows=[(n,d,t) for n,d,t in ODUS_ARROWS[zone_name]]
    else:
        arrows=EP.arrows_for(zone_name, dnames, max_n=10)
    arrows += [(RENAME.get(nm,nm), d, 3) for nm,d in FLAVOUR.get(zone_name,[])]
    seen=set(); ded=[]
    for nm,d,t in arrows:
        if nm in seen or nm in dnames: continue
        seen.add(nm); ded.append((nm,d,t))
    arrows=ded

    # lay each signpost into one of four margin bands; diagonals bias to an end
    BAND={'N':('N',0.5),'S':('S',0.5),'E':('E',0.5),'W':('W',0.5),
          'NE':('E',0.12),'SE':('E',0.88),'NW':('W',0.12),'SW':('W',0.88)}
    DIR={'N':(0,-1),'S':(0,1),'E':(1,0),'W':(-1,0),
         'NE':(0.7,-0.7),'SE':(0.7,0.7),'NW':(-0.7,-0.7),'SW':(-0.7,0.7)}
    bands={}
    for nm,d,t in arrows:
        side=d.split()[0].upper()
        b_,pref=BAND.get(side,('E',0.5))
        bands.setdefault(b_,[]).append((pref,nm,side,t))
    SH={4:0.100,3:0.078,2:0.058}; HD={4:0.020,3:0.016,2:0.012}
    for b_,items in bands.items():
        items.sort(key=lambda i:i[0])
        n=len(items)
        for i,(pref,nm,side,tier) in enumerate(items):
            frac=(i+0.5)/n
            if b_=='W':   ax=(fx0+bx0)/2;            ay=fy0+(fy1-fy0)*frac
            elif b_=='E': ax=(fx1+bx1)/2;            ay=fy0+(fy1-fy0)*frac
            elif b_=='N': ay=(fy0+by0)/2;            ax=fx0+(fx1-fx0)*frac
            else:         ay=(fy1+by1)/2;            ax=fx0+(fx1-fx0)*frac
            dx,dy=DIR.get(side,(1,0))
            L=math.hypot(dx,dy) or 1; dx,dy=dx/L,dy/L
            sh=span*SH[tier]; hd=span*HD[tier]
            tipx,tipy=ax+dx*sh*0.5, ay+dy*sh*0.5
            tailx,taily=ax-dx*sh*0.5, ay-dy*sh*0.5
            # keep the whole arrow inside the frame
            for (px,py) in ((tipx,tipy),(tailx,taily)):
                pass
            offx=min(0,fx1-max(tipx,tailx))+max(0,fx0-min(tipx,tailx))
            offy=min(0,fy1-max(tipy,taily))+max(0,fy0-min(tipy,taily))
            tipx+=offx; tailx+=offx; tipy+=offy; taily+=offy
            Ll(tailx,taily,tipx,tipy)
            px_,py_=-dy,dx
            Ll(tipx,tipy, tipx-dx*hd+px_*hd*0.6, tipy-dy*hd+py_*hd*0.6)
            Ll(tipx,tipy, tipx-dx*hd-px_*hd*0.6, tipy-dy*hd-py_*hd*0.6)
            lab='To_'+nm.replace(' ','_')
            # anchor the label to its OWN arrow: just under the arrow's left end.
            # (no width-based right-alignment - that was throwing long names mid-map)
            # anchor to the arrow's TAIL (its inner end) so the label always
            # reads as belonging to that arrow, whatever the shaft angle
            lx=tailx
            ly=taily + min(w,h)*0.028
            lx=max(lx, fx0+span*0.006)
            Pl(lx, ly, lab, tier)

    # ---------- write (append, stripping only prior violet work) ----------
    p3=f'{O}/{short}_3.txt'
    keep=[]
    if os.path.exists(p3):
        for l in open(p3,encoding='utf-8',errors='replace'):
            l=l.rstrip('\r\n')
            if not l: continue
            if '150, 90, 150' in l: continue
            keep.append(l)
    open(p3,'w',newline='').write('\r\n'.join(keep+out)+'\r\n')
    return len(z['dia']), len(arrows), len(keep)

EP.reset_usage()
tot_d=tot_a=0; rows=[]
for name,z in list(ANT.items())+list(ODUS.items()):
    r=build(name,z)
    if r is None:
        rows.append((name,'-','-','no base file')); continue
    d,a,k=r; tot_d+=d; tot_a+=a
    rows.append((name,d,a,f'{k} kept'))
for n,d,a,k in rows: print(f"  {n:24} diamonds={d!s:>3}  signposts={a!s:>3}  ({k})")
print(f"\nTOTAL: {tot_d} diamonds, {tot_a} signposts")
