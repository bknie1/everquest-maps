"""Produce the final justified-diamond table, with manual overrides on the
stand-in matches the automated test got wrong."""
import json, importlib.util
import justify as J
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
# automated stand-in matches that are actually wrong -> demote to signpost
OVERRIDE_DEMOTE={
 "Urglunt's Gate",      # matched Splitpaw Lair entrance - gnoll lair, not an ogre gate
 'Moggok Gate',         # matched the hidden Plane of Fear portal - not a gate you can see
 'Ogre Ruins',          # matched an ogre MERCHANT - an NPC is not a ruin
}
out={}; kept=0; demoted=0; flagged=[]
for zn,z in list(ab.ANT.items())+list(ab.ODUS.items()):
    sh=SHORT.get(zn)
    if not sh or not z['dia']: continue
    keep,dem=J.judge(sh,z['dia'])
    rows=[]
    for nm,tier,snap,ev in keep:
        if nm in OVERRIDE_DEMOTE:
            dem.append(nm); continue
        rows.append({'name':nm,'tier':tier,'snap':snap,'why':ev})
        if 'STAND-IN' in ev: flagged.append((sh,nm,ev))
    if rows: out[sh]=rows
    kept+=len(rows); demoted+=len(dem)
json.dump(out,open('/home/claude/work/justified_dia.json','w'),indent=1)
print(f"FINAL: {kept} on-map diamonds, {demoted} demoted to signposts\n")
for sh,rows in sorted(out.items()):
    print(f"  {sh:12} "+", ".join(r['name'] for r in rows))
if flagged:
    print("\n  stand-ins kept (your call):")
    for sh,nm,ev in flagged: print(f"    {sh}: {nm}  [{ev}]")
