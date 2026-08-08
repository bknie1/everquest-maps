# Build _1 POI layers for the 6 new zones.
# Palette (generating convention, per spec §4):
ZL=(150,0,200); EXIT=(160,105,0); CAMP=(30,80,95); MERCH=(35,95,55)
NAMED=(150,90,40); BOSS=(110,0,60); GM=(90,35,110)
def wn(loc1,loc2): return (-loc2,-loc1)   # native=(-loc2,-loc1)

# base bounding boxes (from recon) to bounds-check placed POI
BBOX={
 'qeytoqrg':(-1201,2452,-5213,344),'qcat':(-350,658,-1064,182),
 'qey2hh1':(-82,16062,-1492,4448),'beholder':(-672,1898,-1328,1677),
 'highpass':(-565,280,-896,1036),'highkeep':(-152,606,-188,170),
}
def clamp(z,x,y):
    x0,x1,y0,y1=BBOX[z]; pad=30
    return (min(max(x,x0+pad),x1-pad), min(max(y,y0+pad),y1-pad))
def inb(z,x,y):
    x0,x1,y0,y1=BBOX[z]; m=200
    return x0-m<=x<=x1+m and y0-m<=y<=y1+m

def P(x,y,c,size,label,z=0.0):
    return "P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,z,c[0],c[1],c[2],size,label)

def load_src(z):  # source _1 zone-lines, verbatim
    lines=[]
    try:
        for l in open(f'src_new/{z}_1.txt',encoding='utf-8',errors='replace'):
            if l.strip().startswith('P'): lines.append(l.rstrip('\r\n'))
    except FileNotFoundError: pass
    return lines

# ---- per-zone POI definitions: (loc1,loc2, color, size, label)  [loc = game /loc, transformed] ----
DEFS={
 'qeytoqrg':[  # no source _1 -> build zone-lines too
   (3400,-100, ZL,3,'to_Blackburrow'),(-350,100, ZL,3,'to_North_Qeynos'),
   (5050,-200, ZL,3,'to_Surefall_Glade'),(1240,-2450, ZL,3,'to_West_Karana'),
   (3416,-998, CAMP,2,'Blackburrow_Entrance_(gnolls)'),(1344,281, CAMP,2,'Cottage'),
   (526,102, CAMP,2,'Crossroads'),(3951,960, CAMP,2,'Fishing_Pond'),
   (1037,-824, CAMP,2,'Guard_Tower'),(4978,122, CAMP,2,'Miller_Camp'),
   (4718,-977, CAMP,2,'Haunted_Ruins_(undead)'),
   (3400,-500, NAMED,3,'Holly_Windstalker_(Undead_Ranger_20)'),  # roams; near ruins/BB
 ],
 'qey2hh1':[  # + source zone-lines
   (401,-6510, CAMP,2,'Bandit_Camp'),(432,-5359, CAMP,2,'Bandits_Farmhouse'),
   (-3969,-2221, CAMP,2,'Barbarian_Fishing_Village'),(-1968,-8969, CAMP,2,'Brenzi_McMannus_Hut'),
   (-3521,-10978, CAMP,2,'Druid_Bandit_Camp'),(-3008,-13397, MERCH,2,'Farrns_Poison_Merchant'),
   (-1486,-12910, MERCH,2,'Food_and_Blacksmith_Inn'),(493,-2420, CAMP,2,'Guard_Tower'),
   (-762,-4238, CAMP,2,'Guard_Tower'),(-2916,-2041, CAMP,2,'Guard_Tower'),
   (-3712,-7680, NAMED,3,'Linya_Sowlin_(Ex-Druid)'),(500,-9000, CAMP,2,'Ogre_Spawn'),
   (-3899,-5584, CAMP,2,'Millers_Shack_(scarecrows)'),(-3674,-15196, CAMP,2,'Undead_Ruins_(ghoul_camp)'),
   (-3567,-14814, CAMP,2,'Wizard_Spires_(teleport)'),
   (-2239,-1849, NAMED,3,'Oobnopterbevny_(Undead_40)'),
 ],
 'beholder':[  # + source zone-lines
   (-500,600, CAMP,2,'Xorbbs_Altar_/_Kings_Throne'),
   (-500,600, BOSS,3,'King_Xorbb_(Evil_Eye_BOSS_~35)'),
   (-480,650, NAMED,3,'Sviir_and_Syrkl_(Xorbbs_Lords)'),
 ],
 'highpass':[  # + source zone-lines
   (-630,220, CAMP,2,'East_Gate'),(350,-100, CAMP,2,'Golden_Roosters_Inn'),
   (-15,-45, CAMP,2,'Highpass_Hold_(the_Keep)'),(-270,330, CAMP,2,'Waterfall'),
   (550,150, CAMP,2,'West_Gate'),
   (0,-50, BOSS,3,'Bandit_Camp_(aggressive)'),
 ],
 'highkeep':[],  # placed-by-position below (no reliable locs)
 'qcat':[],      # placed-by-position below
}
# by-position POI (native coords directly; approximate) for dungeons w/o loc tables
POS={
 'beholder':[(300,1000,CAMP,2,'Goblin_Lookouts_(approx)'),(750,150,CAMP,2,'Minotaur_and_Muddite_Camp_(approx)')],
 'highkeep':[(40,20,CAMP,2,'Guard_Barracks_(approx)'),(300,40,CAMP,2,'Kings_Chamber_(approx)'),
             (480,-80,BOSS,3,'Pickclaw_Goblins_(mines_below_approx)'),(120,-120,BOSS,3,'Giant_Dungeon_(below_approx)')],
 'qcat':[(-90,-500,CAMP,2,'Necromancer_Guild_(approx)'),(200,-300,BOSS,3,'Bloodsaber_Cult_(approx)'),
         (-130,-860,CAMP,2,'Rogue_Guild_(approx)')],
}
import os
for z in DEFS:
    out=load_src(z)  # source zone-lines verbatim
    skipped=[]
    for loc1,loc2,c,s,lab in DEFS[z]:
        x,y=wn(loc1,loc2)
        if not inb(z,x,y): skipped.append((lab,round(x),round(y))); continue
        x,y=clamp(z,x,y)
        out.append(P(x,y,c,s,lab))
    for x,y,c,s,lab in POS.get(z,[]):
        x,y=clamp(z,x,y); out.append(P(x,y,c,s,lab))
    open(f'/mnt/user-data/outputs/{z}_1.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
    nzl=sum(1 for l in out if '150, 0, 200' in l or '150,0,200' in l)
    print(f'{z}_1.txt: {len(out)} POI ({nzl} zone-lines)'+ (f'  SKIPPED oob: {skipped}' if skipped else ''))
