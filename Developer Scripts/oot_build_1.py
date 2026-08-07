"""Ocean of Tears markers — islands, named NPCs, merchants, succor.
Coords are game /loc; native = (-loc2, -loc1). Levels kept."""
def wn(p,q): return (-q,-p)
EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60); QUEST=(165,60,20)
Z=-1.0
M=[
 # --- islands (landmarks) ---
 (209,9413,   LAND,4,'Siren_Rocks_(Aqua_Goblins_+_Sirens)'),
 (-1052,1914, LAND,3,'Siren_Spires_(no_boat)'),
 (-2095,7612, LAND,4,'Zachariah_Reigh_Isle_(Freeport_dock,_Inn)'),
 (1785,4071,  LAND,4,'Aviak_Island'),
 (-3007,-698, LAND,4,'Aqua_Goblin_Isle_(Temple)'),
 (779,-5387,  LAND,4,'Seafury_Isle_(Cyclops_+_Pirate_Camp)'),
 (156,-4773,  LAND,4,'Undead_Isle_(Spectres_+_Gargoyles,_Tower)'),
 (1309,-7875, LAND,4,'Mudtoe_Isle_(Temple_+_Pet_Merchant)'),
 (-529,-8843, LAND,4,'Goblin_Isle_(Oracle_of_KArnon)'),
 (503,-9253,  LAND,4,'Sister_Isle_(Butcherblock_dock,_Inn,_Kiola_Nuts)'),
 # --- boats / succor ---
 (390,-9200,  EXIT,3,'Succor_(Sister_pier)'),
 (503,-9253,  EXIT,3,'Boat_to_Butcherblock_(Sister_Isle)'),
 (-2095,7612, EXIT,3,'Boat_to_East_Freeport_(Zachariah_Isle)'),
 # --- named / bosses (levels kept) ---
 (-3007,-698, DANGER,4,'Allizewsaur_(50)'),
 (1021,-7900, DANGER,3,'Ancient_Cyclops'),
 (1183,-5978, DANGER,3,'Quag_Maelstrom_(45,_mana_drain)'),
 (-2906,8576, DANGER,3,'Seplawishinl_Bladeblight_(60)'),
 (-492,-8854, NAMED,3,'Guardian_of_KArnon_(42)'),
 (-529,-8843, NAMED,3,'Oracle_of_KArnon_(36)'),
 (1785,4071,  NAMED,3,'Gull_Skytalon_(35)'),
 (1942,3332,  NAMED,3,'Soarin_Brightfeather_(37)'),
 (-1200,-8594,NAMED,2,'A_Goblin_Headmaster_(26)'),
 (779,-5387,  NAMED,2,'Capt_Surestout_(21)'),
 (613,-5602,  NAMED,2,'Gornit_(36)'),
 (900,-6573,  NAMED,2,'Goob_Mudtoe_(22)'),
 (1008,-8022, NAMED,2,'Boog_Mudtoe_(18)'),
 (831,-5445,  NAMED,2,'Wiltin_Windwalker_(32)'),
 (730,8800,   NAMED,2,'Nerbilik_(20)'),
 (209,9413,   NAMED,2,'Brawn_(22)'),
 (156,-4773,  QUEST,2,'Sentry_Xyrin_(19,_quest)'),
 # --- merchants ---
 (1309,-7875, MERCH,3,'Elesseryl_Terussar_(Mage_Pet_Spells)'),
 (503,-9253,  MERCH,2,'Cleonae_Kalen_(Sister_Isle_goods)'),
 (1287,-9244, MERCH,2,'Doran_Vargnus_(Dwarven_smith)'),
 (-2211,7721, MERCH,2,'Endan_Halson_(Zach_Isle_goods)'),
 (-2102,7798, MERCH,2,'Sanian_Shearsin_(Zach_fishing)'),
]
lines=[]
for p,q,c,s,lb in M:
    x,y=wn(p,q); lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
open('oot_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('oot markers P=%d'%len(lines))
