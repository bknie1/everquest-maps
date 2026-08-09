"""Maximum-coverage EQOA signposts.

Every canonical EQOA zone gets an approximate position on the EQOA world map
(1000x1259 px).  Each EQ1 zone also has a position.  Signposts are then derived
by BEARING and distance, so a zone points at its real neighbours and the whole
set connects up.  Distance sets the size tier: close = large, far = small.
"""
import math

# ---- canonical EQOA zones -> approx position on the EQOA world map ----
EQOA_POS = {
 # far north
 'Permafrost':(62,46),'Snowblind Plains':(150,46),'Anu Village':(241,46),
 'Frosteye Valley':(315,53),'Halas':(405,52),'Snowfist':(500,46),
 "Greyvax's Caves":(600,46),'Fayspire Gate':(688,30),
 'Lava Storm':(772,60),'Rogue Clockworks':(945,110),
 # northern band
 "Zentar's Keep":(60,140),'Unkempt North':(140,140),'North Wilderlands':(232,148),
 'Guardian Forest':(330,157),'Goldfeather Eyrie':(440,140),"Snafitzer's House":(520,130),
 'Freezeblood Village':(400,205),'Diren Village':(345,262),'Fayspire / Tethelin':(640,140),
 'Kara Village':(790,132),"Klik'Anon":(872,150),'Collinridge Cemetery':(860,175),
 'Thedruk':(690,180),'Neriak':(960,240),
 # north-central
 'Bogman Village':(55,225),'Salisearaneen':(215,225),'Gramash Ruins':(320,215),
 'Unkempt Glade':(150,258),'Murnf':(250,306),'Mariel Village':(66,300),
 'Twisted Tower':(150,300),"Spirit Talker's Wood":(312,307),'Mt. Hatespike':(430,300),
 'Shon-To Monastery':(520,240),'Moradhim':(490,258),'Misty Thicket':(560,318),
 'Baga Village':(497,328),'Castle Felstar':(690,470),'Surefall Glade':(234,373),
 "Jethro's Cast":(150,404),'Wymondham':(325,401),'Blackburrow':(406,432),
 'Merry-by-Water':(509,398),'Rivervale':(672,351),'North Kithicor':(758,292),
 'The Green Rift':(888,312),'Bobble-by-Water':(973,306),'Hodstock / Temby':(973,400),
 'Moss Mouth Cavern':(702,404),'Saerk Towers':(805,412),"Mu Lin's Reach":(861,382),
 # west coast
 'Wyndhaven':(50,417),'Crethly Manor':(134,461),'Whale Hill':(53,504),'Fog Marsh':(234,504),
 'Al-Karad Ruins':(322,520),'Hagley':(119,579),'Qeynos':(35,610),'Qeynos Prison':(60,660),
 # karana belt
 "Jared's Blight":(406,504),'Blakedown':(316,569),"Alseop's Wall":(406,583),
 "Strag's Rest":(497,558),'Bear Cave':(238,623),"Druid's Watch":(141,683),
 'Spider Mine':(250,686),'Mayfly Glade':(319,651),'Forkwatch':(409,688),
 'Bandit Hills':(513,469),'Highpass Hold':(603,469),'Runnyeye':(588,431),
 "Ferran's Hope":(678,586),"Trail's End":(569,595),'Bastable Village':(664,518),
 'Salt Mine':(519,670),"Dshinn's Redoubt":(600,679),'Desert Hate':(665,679),
 'Tomb of Kings':(752,531),'Temple of Light':(861,484),'Freeport':(915,490),
 'Northwestern Ro':(873,576),'Deathfist Forge':(760,600),'Deathfist Citadel':(788,684),
 "Muniel's Tea Garden":(867,669),'Northern Ro':(940,570),
 # south-west
 'Highbourne':(50,745),'Stoneclaw':(150,745),'Aviak Village':(235,768),
 "Urglunt's Wall":(338,737),'South Crossroads':(421,793),'Centaur Valley':(505,761),
 "Wktaan's 4th Talon":(560,760),'Deathfist Horde':(690,720),'Box Canyons':(788,749),
 'Open Sea':(950,700),
 "Cyclops's Fortress":(235,848),"Urglunt's Gate":(326,889),"Widow's Peak":(435,861),
 'Serpent Hills':(600,865),'Chiktar Hive':(690,860),'Eternal Desert':(760,860),
 'Al Farak Ruins':(864,790),"Sycamore Joy's Rest":(861,869),'Elemental Towers':(960,910),
 "Geomancer's Citadel":(150,875),'Lake Rathe':(255,948),'Sphinx Pyramid':(318,928),
 'Kelinar':(426,948),'Fort Alliance':(175,948),"Geomancer's Pass":(150,985),
 'Dead Hills':(165,1040),'Ogre Ruins':(218,1012),'Elephant Graveyard':(505,1035),
 "Gerntar's Mines":(420,1075),'Oggok':(270,1150),'Oggok Gate':(400,1160),
 'Great Waste':(862,950),'Oasis':(777,975),'Takish\'Hiz':(690,1040),
 "Tak'Xiv West":(600,950),"Tak'Xiz South":(520,1045),'Sea of Lions':(769,1035),
 'Slithar Hive':(900,1090),'Hazinak':(985,1075),'Sslathis':(880,1130),'Guk':(940,1128),
 'Tomb City of Envar':(150,1102),'West Feerrott':(253,1102),'Moggok Gate':(320,1140),
 'Kerplunk Outpost':(508,1114),'Lake Noregard':(596,1137),'Burial Mounds':(677,1137),
 'Ant Colonies':(777,1131),'Brog Fens':(500,880),'Dinbak':(596,1198),
 'Cazic Thule':(450,1220),'Stone Watchers':(560,1240),'Broken Skull Rock':(700,1195),
 "Basher's Cave":(830,1195),'Grobb':(978,1180),"Mila's Reef":(430,1245),
}

# ---- EQ1-side / invented region names from Brandon's cell grid ----
# geographic areas that persist and are worth pointing at even though they're
# outside the EQOA zone index
EQ1_EXTRA = {
 'The Northlands':(150,18),'The Frigid Plain':(420,14),'The Hatchland':(58,182),
 'The Nest':(330,108),'Jaggedpine':(200,430),'Winters Deep':(480,180),
 'Lake Neriuss':(700,300),'The Feerrott (North)':(200,1020),
 'Buried Sea':(200,1245),'Gulf of Gunthak':(620,1252),
}
EQOA_POS.update(EQ1_EXTRA)


# Broad geography: fine to point at, but it must never crowd out the specific,
# characterful places (villages, ruins, castles, named landmarks).
BROAD = set(EQ1_EXTRA) | {
 'Open Sea','Sea of Lions','Abysmal Sea','The Vastly Deep','Great Waste','Eternal Desert',
 'Desert Hate','Snowblind Plains','Frosteye Valley','Serpent Hills','Dead Hills',
 'Northwestern Ro','Northern Ro','North Barren Coast','South Barren Coast','Gulf of Uzun',
 'The Hunt','West Toxxulia','East Toxxulia','South Toxxulia','Box Canyons','Guardian Forest',
 'Unkempt Glade','The Green Rift','Bandit Hills','Lake Rathe','Lake Noregard',
}

# EQOA names that ARE reachable EQ1 zones - a signpost to somewhere you can just
# walk to offers nothing, so they never become arrows.
WALKABLE = {'Lava Storm','Halas','Permafrost','Blackburrow','Surefall Glade','Qeynos',
 'Rivervale','Runnyeye','Misty Thicket','Highpass Hold','Freeport','Neriak','Oasis',
 'Northern Ro','Guk','Grobb','Oggok','Cazic Thule','Lake Rathe','Kerra Isle','Paineel',
 'The Warrens','Stonebrunt Mountains',"Edud's Crossing"}

ZONE_USE={}          # how many maps each broad name has already claimed
def reset_usage(): ZONE_USE.clear()

# ---- EQ1 zones -> position on the same map, and file shortname ----
EQ1_POS = {
 'Everfrost Peaks':(220,110),'Blackburrow':(406,432),'Surefall Glade':(234,373),
 'Qeynos Hills':(235,620),'West Karana':(400,560),'North Karana':(470,430),
 'East Karana':(790,420),'Beholders Maze':(555,450),'South Karana':(400,790),
 'Misty Thicket':(560,320),'Rivervale':(672,351),'Highpass Hold':(620,500),
 'Kithicor Wood':(800,300),'West Commonlands':(700,545),'East Commonlands':(860,480),
 'Nektulos Forest':(870,220),'Lavastorm Mountains':(772,60),
 'Northern Desert of Ro':(880,620),'Southern Desert of Ro':(840,810),
 'Oasis of Marr':(777,975),'Innothule Swamp':(640,1130),'Feerrott':(230,1090),
 'Rathe Mountains':(250,900),'Lake Rathetear':(255,948),'Cazic Thule':(450,1220),
}
# modern-context renames (ruins / former places)
RUINS = {"Klik'Anon":"Ruins of Klik'Anon",'Moradhim':'Ruins of Moradhim',
         'Rogue Clockworks':'Old Rogue Clockworks','Fayspire / Tethelin':'Ruins of Fayspire',
         'Lava Storm':'Lava Storm'}


def _build_guarantee():
    """Each cited region name is guaranteed a slot on its NEAREST EQ1 map -
    so it appears, but never spreads across the continent."""
    g={}
    for nm,(x,y) in EQ1_EXTRA.items():
        best=None
        for z,(zx,zy) in EQ1_POS.items():
            d=math.hypot(x-zx,y-zy)
            if best is None or d<best[0]: best=(d,z)
        if best: g.setdefault(best[1],[]).append(nm)
    return g
GUARANTEE=None

def bearing(dx,dy):
    """dy is +south on the map image. Returns compass string."""
    ang=math.degrees(math.atan2(-dy,dx))%360     # 0=E, 90=N
    for lo,hi,name in [(337.5,360,'E'),(0,22.5,'E'),(22.5,67.5,'NE'),(67.5,112.5,'N'),
                       (112.5,157.5,'NW'),(157.5,202.5,'W'),(202.5,247.5,'SW'),
                       (247.5,292.5,'S'),(292.5,337.5,'SE')]:
        if lo<=ang<hi: return name
    return 'E'

# EQOA names that ARE the EQ1 zone (never signpost a zone to itself)
SELF={'Everfrost Peaks':{'Permafrost','Halas'},'Blackburrow':{'Blackburrow'},
 'Surefall Glade':{'Surefall Glade'},'Misty Thicket':{'Misty Thicket'},
 'Rivervale':{'Rivervale'},'Highpass Hold':{'Highpass Hold'},
 'Beholders Maze':{'Runnyeye'},'Cazic Thule':{'Cazic Thule'},
 'Oasis of Marr':{'Oasis'},'Lake Rathetear':{'Lake Rathe'},
 'Lavastorm Mountains':{'Lava Storm'},'Nektulos Forest':{'Neriak'},
 'East Commonlands':{'Freeport'},'Northern Desert of Ro':{'Northern Ro'},
 'Innothule Swamp':{'Guk','Grobb'},'Feerrott':{'Oggok'},'Qeynos Hills':{'Qeynos'}}

def arrows_for(zone, exclude, max_n=12, radius=360):
    global GUARANTEE
    if GUARANTEE is None: GUARANTEE=_build_guarantee()
    """Nearest EQOA zones by bearing, tiered by distance. exclude = names already on-map."""
    if zone not in EQ1_POS: return []
    zx,zy=EQ1_POS[zone]
    exclude=set(exclude)|SELF.get(zone,set())|{zone}
    cand=[]
    for nm,(x,y) in EQOA_POS.items():
        if nm in exclude or nm in WALKABLE: continue
        d=math.hypot(x-zx,y-zy)
        if d<45 or d>radius: continue          # skip self-ish and too far
        cand.append((d,nm,bearing(x-zx,y-zy)))
    # specific places rank ahead of broad geography at the same distance
    cand.sort(key=lambda c: c[0]*(1.9 if c[1] in BROAD else 1.0))
    out=[]; per_dir={}; broad_here=0
    # guaranteed region names for this map go in first
    for nm in GUARANTEE.get(zone,[]):
        if nm in exclude: continue
        x,y=EQOA_POS[nm]; d=math.hypot(x-zx,y-zy)
        tier = 4 if d<110 else (3 if d<215 else 2)
        out.append((RUINS.get(nm,nm), bearing(x-zx,y-zy), tier))
        per_dir[bearing(x-zx,y-zy)]=per_dir.get(bearing(x-zx,y-zy),0)+1
        ZONE_USE[nm]=ZONE_USE.get(nm,0)+1
    done={o[0] for o in out}
    for d,nm,br in cand:
        if RUINS.get(nm,nm) in done: continue
        if nm in BROAD:
            if broad_here>=3: continue                 # at most 3 broad names per map
            if ZONE_USE.get(nm,0)>=4: continue         # and no name plastered everywhere
        if per_dir.get(br,0)>=3: continue      # at most 3 per compass direction
        per_dir[br]=per_dir.get(br,0)+1
        tier = 4 if d<110 else (3 if d<215 else 2)   # close=large, far=small
        out.append((RUINS.get(nm,nm), br, tier))
        if nm in BROAD:
            broad_here+=1; ZONE_USE[nm]=ZONE_USE.get(nm,0)+1
        if len(out)>=max_n: break
    return out

if __name__=='__main__':
    tot=0
    for z in EQ1_POS:
        a=arrows_for(z,set())
        tot+=len(a)
        print(f"{z}: {len(a)}")
        print("   "+", ".join(f"{n} ({b},t{t})" for n,b,t in a[:6])+(" ..." if len(a)>6 else ""))
    print(f"\nTOTAL signposts available: {tot}")
