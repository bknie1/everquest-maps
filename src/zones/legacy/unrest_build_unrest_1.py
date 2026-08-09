"""Estate of Unrest markers — haunted house floors, yard camps, named undead (dungeon; placed by position)."""
ZONE=(150,0,200); EXIT=(160,105,0); LAND=(30,80,95); DANGER=(110,0,60); NAMED=(150,90,40)
Z=-1.0; lines=[]
def P(x,y,c,s,lb): lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
P(-40,10,   ZONE,3,'to_Dagnors_Cauldron')
# grounds / gardens
P(0,-450,   LAND,3,'The_Grounds_(Yard_Trash:_beetles,_skeletons)')
P(-40,-340, LAND,2,'Garden_Hedge_Maze')
P(250,-420, LAND,2,'The_Gazebo_(yard_camp)')
# the manor house
P(0,-650,   LAND,3,'Manor_House_(1st_Floor,_Main_Room)')
P(-60,-680, LAND,2,'Fireplace_Camp_(FP)')
P(-120,-650,LAND,2,'Barroom_(Undead_Barkeep,_Zombie_Noble)')
P(-100,-720,LAND,2,'Back_Room_(Lesser_Blade_Fiend)')
P(60,-700,  LAND,2,'2nd_Floor_(Reclusive_Ghoul_Magus)')
P(0,-760,   LAND,2,'3rd_Floor_Towers_(Festering_Hags)')
P(0,-600,   LAND,2,'Basement_(highest_level)')
# named / danger
P(0,-700,   DANGER,3,'Garanel_Rucksif_(Ghost_Lord_of_Unrest)')
P(-30,-660, NAMED,2,'Torklar_Battlemaster_(named)')
P(20,-770,  DANGER,2,'Undead_Knight_of_Unrest')
P(90,-710,  DANGER,2,'Khrix_Fritchoff_(Gnome,_avoid)')
P(30,-775,  DANGER,2,'a_priest_of_Najena_(avoid)')
open('unrest_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('unrest markers P=%d'%len(lines))
