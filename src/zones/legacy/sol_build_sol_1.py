"""Solusek fire-dungeon markers — bosses, camps, zone connections placed by depth/position."""
ZONE=(150,0,200); EXIT=(160,105,0); LAND=(30,80,95); DANGER=(110,0,60); NAMED=(150,90,40)
Z=-1.0
def build(fn, rows):
    lines=["P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb) for (x,y,c,s,lb) in rows]
    open(fn,'w',newline='').write('\r\n'.join(lines)+'\r\n'); print(fn,'P=%d'%len(lines))

# SOLUSEK'S EYE (soldunga) x[-28,1214] y[-89,1090] — fire goblins + gnome miners
build('soldunga_1.txt',[
 (120,120,   ZONE,3,'to_Lavastorm_(entrance)'),
 (1050,520,  ZONE,3,'to_Nagafens_Lair_(Sol_B)'),
 (250,180,   LAND,3,'Fire_Goblin_Entrance_Camps'),
 (430,340,   LAND,3,'Solusek_Mining_Company_(Gnomes)'),
 (760,760,   LAND,3,'Throne_Room'),
 (860,720,   DANGER,3,'Solusek_Goblin_King_(Ring_of_Goblin_Lords)'),
 (700,840,   DANGER,2,'Inferno_Goblin_Torturer_(Jail)'),
 (900,300,   DANGER,2,'Solusek_Kobolds_+_Fire_Elementals'),
])
# NAGAFEN'S LAIR (soldungb) x[-358,980] y[-28,1589] — Lord Nagafen, fire giants
build('soldungb_1.txt',[
 (350,120,   ZONE,3,'to_Lavastorm_(entrance)'),
 (-200,700,  ZONE,3,'to_Soluseks_Eye_(Sol_A)'),
 (400,220,   LAND,3,'Kobold_Entrance_Caverns'),
 (200,560,   LAND,3,'Kobold_King_Room_(Targin_the_Rock)'),
 (520,880,   NAMED,2,'Efreeti_Lord_Djarn_(Golden_Efreeti_Boots)'),
 (300,1120,  LAND,3,'Fire_Giant_Halls'),
 (300,1240,  DANGER,2,'Magi_Rokyl_(Channelling_Crystal)'),
 (360,1440,  DANGER,3,'Lord_Nagafen_(RED_DRAGON_RAID_BOSS)'),
 (600,760,   DANGER,2,'Stone_Spider_(45)'),
 (150,900,   LAND,2,'Voidling_(hail_for_Raid_instance)'),
])
# CAVERNS OF EXILE (soldungc) x[-936,875] y[-950,536]
build('soldungc_1.txt',[
 (0,450,     ZONE,3,'to_the_Sol_complex'),
 (-600,-600, LAND,3,'Fire_Cavern_Camps_(west)'),
 (500,-500,  LAND,3,'Lava_Caverns_(east)'),
 (0,-200,    LAND,2,'Central_Chasm'),
 (-700,300,  DANGER,2,'Solusek_Guardians'),
 (600,200,   NAMED,2,'Exiled_Named_Spawn'),
])
# TEMPLE OF SOLUSEK RO (soltemple) x[-102,88] y[-611,-196]
build('soltemple_1.txt',[
 (0,-230,    ZONE,3,'to_Lavastorm_(entrance)'),
 (0,-410,    LAND,3,'Central_Altar_(Lava_Hall)'),
 (-60,-330,  LAND,2,'Side_Chambers'),
 (60,-330,   LAND,2,'Side_Chambers'),
 (0,-560,    DANGER,3,'Solusek_Ro_(Fire_God)_Sanctum'),
 (0,-480,    DANGER,2,'Fire_Guardians'),
])
