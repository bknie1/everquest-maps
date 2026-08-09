"""Diamond justification test.

Brandon's rule: an on-map diamond must have SOMETHING THERE TO LOOK AT.
Two ways a diamond earns its place:

  REGION  - a geographic area that simply persists (plains, valley, hills, forest,
            desert, lake, coast). The terrain IS the thing, so an area label is fine.
  SITE    - a structure/settlement. Only valid if a REAL EQ1 feature sits there,
            proven by a POI in the zone's own `_1` layer. The diamond is then SNAPPED
            onto that feature so walking to it shows something.

Everything else is demoted to a margin signpost.
"""
import os, math, re

O='/mnt/user-data/outputs'

# geographic areas that persist regardless of civilisation
REGION = {
 # broad terrain that persists whatever happens to civilisation
 'Snowblind Plains','Frosteye Valley','Serpent Hills','Dead Hills','West Feerrott',
 'Box Canyons','Eternal Desert','Northwestern Ro','Great Waste','Desert Hate',
 'South Toxxulia','East Toxxulia','West Toxxulia','North Barren Coast','South Barren Coast',
 'The Green Rift','Bandit Hills',"Widow's Peak","Geomancer's Pass",'Mayfly Glade',
 'Unkempt Glade','Guardian Forest','Jaggedpine','The Hunt','Abysmal Sea','The Vastly Deep',
 'Open Sea','Sea of Lions','Lake Noregard','Lake Rathe','Gulf of Uzun','Cape Dreg',
 'North Kithicor','Oasis','Centaur Valley','Snowfist',
}
# caves, mines, ruins, settlements and structures must PROVE something is there

def load_poi(short):
    """Real EQ1 features from the zone's own marker layer."""
    pts=[]
    p=f'{O}/{short}_1.txt'
    if not os.path.exists(p): return pts
    for l in open(p,'rb').read().decode('utf-8','replace').split('\r\n'):
        if l.startswith('P'):
            f=l[1:].split(',')
            try:
                lab=','.join(f[7:]).strip()
                if lab.startswith('to_'): continue          # zone lines aren't features
                pts.append((float(f[0]),float(f[1]),lab))
            except: pass
    return pts

def bbox(short):
    xs=[];ys=[]
    for l in open(f'{O}/{short}.txt',encoding='utf-8',errors='replace'):
        if l.startswith('L'):
            f=l[2:].split(',')
            try: xs+=[float(f[0]),float(f[3])];ys+=[float(f[1]),float(f[4])]
            except: pass
    return min(xs),max(xs),min(ys),max(ys)

def judge(short, dia_names):
    """Returns (keep, demote) where keep = [(name, tier, snap_xy, evidence)]."""
    if not os.path.exists(f'{O}/{short}.txt'): return [],list(dia_names)
    b=bbox(short); span=max(b[1]-b[0], b[3]-b[2])
    poi=load_poi(short)
    keep=[]; demote=[]
    used=set()
    for nm,tier in dia_names:
        if nm in REGION:
            keep.append((nm,tier,None,'geographic region'))
            continue
        # SITE: needs a real EQ1 feature to stand on
        best=None
        for i,(x,y,lab) in enumerate(poi):
            if i in used: continue
            score=_affinity(nm,lab)
            if score>0 and (best is None or score>best[0]): best=(score,i,x,y,lab)
        if best and best[0]>=10:
            used.add(best[1])
            keep.append((nm,tier,(best[2],best[3]),f'1:1 -> {best[4]}'))
        elif best:
            used.add(best[1])
            keep.append((nm,tier,(best[2],best[3]),f'STAND-IN? -> {best[4]}'))
        else:
            demote.append(nm)
    return keep,demote

STOP={'the','of','a','and','ruins','village','camp','hills','tower','towers'}
def _affinity(eqoa_name, eq1_label):
    """Does this EQ1 feature plausibly BE the EQOA place?"""
    a=set(re.findall(r'[a-z]+', eqoa_name.lower()))-STOP
    b=set(re.findall(r'[a-z]+', eq1_label.lower()))-STOP
    if not a or not b: return 0
    shared=a&b
    if shared: return 10+len(shared)          # direct name match, strongest
    # thematic stand-ins: a real structure of the same kind counts
    KIND={'cemetery':{'graveyard','tomb','crypt','undead','ruins','grave'},
          'castle':{'castle','keep','fort','tower','citadel'},
          'citadel':{'citadel','keep','castle','fort'},
          'monastery':{'temple','monastery','shrine'},
          'temple':{'temple','shrine','altar'},
          'mine':{'mine','cave','tunnel'},
          'gate':{'gate','entrance','pass'},
          'fort':{'fort','tower','guard','outpost','keep'},
          'village':{'village','camp','farm','hut','cottage','inn','settlement'},
          'outpost':{'outpost','camp','tower','guard'}}
    for k,v in KIND.items():
        if k in eqoa_name.lower() and (b & v): return 5
    return 0

if __name__=='__main__':
    import importlib.util
    spec=importlib.util.spec_from_file_location("ab","/home/claude/work/align_build.py")
    ab=importlib.util.module_from_spec(spec); spec.loader.exec_module(ab)
    SHORT={'Everfrost Peaks':'everfrost','Blackburrow':'blackburrow','Surefall Glade':'qrg',
     'Qeynos Hills':'qeytoqrg','West Karana':'qey2hh1','North Karana':'northkarana',
     'East Karana':'eastkarana','Beholders Maze':'beholder','South Karana':'southkarana',
     'Misty Thicket':'misty','Rivervale':'rivervale','Highpass Hold':'highpass',
     'Kithicor Wood':'kithicor','West Commonlands':'commons','East Commonlands':'ecommons',
     'Nektulos Forest':'nektulos','Lavastorm Mountains':'lavastorm',
     'Northern Desert of Ro':'nro','Southern Desert of Ro':'sro','Oasis of Marr':'oasis',
     'Innothule Swamp':'innothule','Feerrott':'feerrott','Rathe Mountains':'rathemtn',
     'Lake Rathetear':'lakerathe','Cazic Thule':'cazicthule','Toxxulia Forest':'tox',
     'Stonebrunt Mtns':'stonebrunt'}
    tk=td=0
    for zn,z in list(ab.ANT.items())+list(ab.ODUS.items()):
        sh=SHORT.get(zn)
        if not sh or not z['dia']: continue
        keep,dem=judge(sh,z['dia'])
        tk+=len(keep); td+=len(dem)
        print(f"\n{zn}")
        for nm,t,snap,ev in keep:
            print(f"   KEEP   {nm:24} ({ev})")
        for nm in dem:
            print(f"   ARROW  {nm:24} (nothing there in EQ1)")
    print(f"\n=== {tk} diamonds justified, {td} demoted to signposts ===")
