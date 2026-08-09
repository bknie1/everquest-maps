"""The Feerrott markers — ogre merchants, lizardman camps, Cazic-Thule + Plane of Fear,
bouncers, Cyndreela. native=(-loc2,-loc1)."""
def wn(p,q): return (-q,-p)
ZONE=(150,0,200); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60); QUEST=(165,60,20); EXIT=(160,105,0)
Z=-1.0; lines=[]
def P(x,y,c,s,lb): lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
def L(p,q,c,s,lb): x,y=wn(p,q); P(x,y,c,s,lb)
# zone lines (native, from uploaded _1)
for x,y,lb in [(-1444.79,1091.63,'to_Oggok'),(2988.00,-1266.00,'to_Rathe_Mountains'),
 (-2690.00,1475.00,'portal_to_Plane_of_Fear'),(-902.00,-1091.00,'to_Temple_of_Cazic-Thule'),
 (2988.00,900.00,'to_Innothule_Swamp')]:
    P(x,y,ZONE,3,lb)
L(1091,905, EXIT,3,'Succor_(near_Oggok)')
# landmarks
L(410,-1850, LAND,3,'Druid_Ring_(spiders)')
L(-1475,2690,LAND,3,'Plane_of_Fear_Entrance_(hidden,_Spectres)')
L(-902,-1091,LAND,4,'Temple_of_Cazic-Thule_(entrance)')
L(1144,1444, LAND,3,'Oggok_Outpost_(Inn_+_Merchants)')
# ogre merchants (by wares)
L(1144,1444, MERCH,2,'Merchant_(Food)_Innkeep_Gub')
L(1144,-145, MERCH,2,'Merchant_(Baking/Bread)_Innkeep_Morpa')
L(1129,-138, MERCH,2,'Merchant_(Tailoring)_Murga')
L(1182,117,  MERCH,2,'Merchant_(Baking)_Bup')
L(975,1267,  MERCH,2,'Merchant_(Ogre_goods)_Fugla')
# bosses / danger (levels)
L(-2370,2604,DANGER,3,'Cyndreela_(40_Necro,_Fear_Portal)')
L(-2419,2797,DANGER,3,'Annaelia_Wylassi_(61_Necro)')
L(-175,55,   DANGER,3,'Bouncer_Hurd_(37_Ogre,_KOS_good)')
L(-1041,813, DANGER,2,'Bouncer_Flerb_(37)')
L(1467,876,  DANGER,2,'Bouncer_Fug_+_Prud_(50,_Oggok_guards)')
L(804,1153,  DANGER,2,'Oknoggin_Stonesmacker_(55_Bard)')
L(-1376,-78, DANGER,2,'A_Gorilla_(19)')
# named
L(-2597,2604,NAMED,2,'Roror_(49_Lizard_High_Priest)') if False else L(-1400,2000,NAMED,2,'Roror_(49_Lizard_High_Priest,_wanders_W)')
L(-1128,-2923,NAMED,2,'Drizda_Tunesinger_(25_Bard)')
L(-1460,1046,NAMED,2,'Aqaar/Eleann/Spanner_camp_(25)')
L(-599,2512, NAMED,2,'Lizardman_Mystic_Camp_(3-11)')
L(984,2323,  NAMED,2,'Lizardman_Scout_Camps_(3-5)')
# NW danger note
L(-2419,2400,DANGER,2,'Dark_Assassin_(KOS_all,_wanders_NW)')
open('feerrott_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('feerrott markers P=%d'%len(lines))
