"""Erud's Crossing markers — Kerrans, crater, haunted ship, sharks, merchant, named.
/loc -> native (-loc2,-loc1). Zone line preserved from upload."""
def wn(p,q): return (-q,-p)
EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60); QUEST=(165,60,20)
Z=-1.0
lines=[l.strip() for l in open('erudsxing_1.txt',encoding='utf-8',errors='replace').read().replace('\r\n','\n').split('\n') if l.startswith('P')]
ADD=[
 (-1767,795,  EXIT,3,'Succor_(Pier)'),
 (-1771,797,  LAND,4,'Dock_+_Kerran_Camp_(Boat_to_Erudin)'),
 (-1175,1239, LAND,4,'Volcanic_Crater'),
 (-1157,2108, LAND,3,'Sunken_Haunted_Ship_(Zombie_Sailors)'),
 (-1479,857,  MERCH,3,'Renna_(Fishing_Supplies_+_Weapons)'),
 (-919,1638,  DANGER,3,'Ooglyn_(45,_Shaman_Epic)'),
 (-1108,3982, DANGER,3,'Killer_Sharks_(40,_west_waters)'),
 (-2400,1650, DANGER,3,'Plague_Shark_(33,_patrols)'),
 (-1175,1239, NAMED,2,'Yelesom_Paust_(20,_crater_wall)'),
 (-1690,1055, NAMED,2,'Erudite_Madman_(15)'),
 (-425,800,   NAMED,2,'Hastashi_(rare_Mermaid)'),
 (-1334,746,  NAMED,2,'Jarra_+_Kala_(Kerrans_14-17)'),
 (-1779,678,  NAMED,2,'Monala_+_Nifta_(Kerrans_17)'),
 (-1200,1315, NAMED,2,'Willowisps_+_Beetles_(lightstones)'),
]
for p,q,c,s,lb in ADD:
    x,y=wn(p,q); lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
open('erudsxing_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('erudsxing markers P=%d'%len(lines))
