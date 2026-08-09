prov=[l.strip() for l in open('butcher_1.txt',encoding='utf-8',errors='replace').read().replace('\r\n','\n').split('\n') if l.startswith('P')]
def wn(p,q): return (-q,-p)
EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60)
Z=0.0
ADD=[
 (2550,-700, EXIT,  2,'Succor_(SE_of_Kaladim)'),
 (3041,-224, LAND,  3,'Kaladim_Gates_+_Statue'),
 (1108,1712, LAND,  3,'Docks_(Boats:_Freeport_+_Kunark)'),
 (847,-2280, DANGER,3,'The_Chessboard_(Undead)'),
 (1335,-1645,LAND,  2,'Ancient_Stone_Ring'),
 (-2086,2016,MERCH, 2,'Spire_+_Ellona_(Merchant)'),
 (-2001,-202,NAMED, 2,'Corflunk_(Ogre)'),
 (1235,3500, NAMED, 2,'Glubbsink_(Ocean_Rare)'),
 (165,2476,  NAMED, 2,'Blyle_Bundin_(Deserter)'),
 (2793,-688, MERCH, 2,'Bilgum_Sisters_+_Merchants'),
 (-1080,471, DANGER,2,'Goblin_Camp'),
 (-302,1080, DANGER,2,'Enraged_Goblins'),
 (2813,179,  DANGER,2,'Aqua_Goblin_Camp_(Shore)'),
 (447,-1459, DANGER,2,'Orc_Camp'),
 (-514,-568, DANGER,2,'Dwarf_Bandit_Camp'),
]
lines=list(prov)
for p,q,c,s,lb in ADD:
    x,y=wn(p,q); lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
open('butcher_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('butcher markers P=%d (%d zone-lines + %d added)'%(len(lines),len(prov),len(ADD)))
