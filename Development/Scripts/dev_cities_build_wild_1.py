"""Everfrost / Runnyeye / Stonebrunt landmark markers (hunting/dungeon zones).
Camps & areas placed by map position (native coords), labeled; zone lines kept."""
ZONE=(150,0,200); EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60)
Z=-1.0
def write(fn, rows):
    lines=["P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb) for (x,y,c,s,lb) in rows]
    open(fn,'w',newline='').write('\r\n'.join(lines)+'\r\n'); print(fn,'P=%d'%len(lines))

# EVERFROST (native coords; keep existing zone lines)
write('everfrost_1.txt',[
 (7038.99,-2018.17,ZONE,3,'to_Permafrost'),
 (-371.82,-3723.72,ZONE,3,'to_Halas'),
 (507.34,3009.41,  ZONE,3,'to_Blackburrow'),
 (300,-2400, LAND,3,'Newbie_Canyons_(lvl_1-7)'),
 (4200,-600, LAND,3,'Mammoth_Tundra_(plains)'),
 (5200,900,  LAND,2,'Ice_Goblin_Camps_(igloos)'),
 (3400,-1600,DANGER,2,'Snow_Orc_Camp'),
 (6200,-1600,DANGER,2,'Permafrost_Approach_(Ice_Giants)'),
 (-200,-3300,LAND,2,'Halas_Ferry_Approach'),
])

# RUNNYEYE Citadel (bbox x[-220,295] y[-380,284]) — 4-level goblin stronghold
write('runnyeye_1.txt',[
 (250,-330, ZONE,3,'to_Gorge_of_King_Xorbb'),
 (150,180,  LAND,3,'Upper_Goblin_Camps_(lvl_1)'),
 (-40,60,   LAND,2,'Central_Warrens_(lvl_2)'),
 (60,-120,  LAND,2,'Lower_Camps_(lvl_3)'),
 (-120,-260,DANGER,3,'King_Grumblug_(Goblin_King,_lvl_4)'),
 (120,-40,  DANGER,2,'Evil_Eye_(Beholder)_Wardens'),
])

# STONEBRUNT Mountains (bbox x[-3751,3852] y[-4557,4952]) — kobold wilderness
write('stonebrunt_1.txt',[
 (200,-700, LAND,3,'Kejek_Village_(merchants+tradeskill+rest)'),
 (200,-700, MERCH,2,'Kejekan_Merchants_(Kejek)'),
 (-2600,-1200,ZONE,3,'to_The_Warrens'),
 (900,2600,  LAND,3,'Mount_Klaw_(Kerran_Village,_north)'),
 (-1400,1800,LAND,2,'Southern_Kobold_Camps'),
 (1600,900,  LAND,2,'Kobold_Camps_(east)'),
 (0,0,       DANGER,3,'The_Ancients_(roaming_Titans)'),
 (-2000,-3200,LAND,2,'Granite_Golem_Grounds'),
])
