"""Splitpaw Lair markers — gnoll den camps by difficulty band + named gnolls (placed by depth)."""
ZONE=(150,0,200); EXIT=(160,105,0); LAND=(30,80,95); DANGER=(110,0,60); NAMED=(150,90,40)
Z=-1.0; lines=[]
def P(x,y,c,s,lb): lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
# keep uploaded zone line
for l in open('paw_1.txt'):
    if l.startswith('P'): lines.append(l.strip())
# camps by difficulty band (entrance=bottom high-y -> deep=top low-y)
P(0,120,    LAND,3,'Entrance_(Three_Talons,_lvl_25-28)')
P(-50,-150, LAND,3,'Double_Doors_Camp_(lvl_30-33)')
P(0,-360,   LAND,2,'Front_Bridge_(drop-down_to_lower_level)')
P(-40,-600, LAND,3,'The_Pond_(underwater_passage_to_Ishva)')
P(0,-760,   LAND,3,'Ishva_Area_(deepest,_lvl_40-50)')
P(0,-1300,  LAND,2,'Deep_Dens_(lvl_40-42)')
# named gnolls (Mas<Mal<Val ranks)
P(0,-780,   DANGER,3,'The_Ishva_Mal_(boss,_drops_Robe,_36hr)')
P(100,-900, DANGER,2,'Tesch_Val_DevalNmak_(named)')
P(-100,-1000,DANGER,2,'Nisch_Val_Torash_Mashk_(Devlas_Ilkvel)')
P(0,-1100,  DANGER,2,'Verishe_Mal_Judges_+_Executioner')
P(50,-1150, NAMED,2,'Kurrpok_Splitpaw_(named)')
P(-60,-250, NAMED,2,'Tesch_Mal_Gnoll_(entrance_named)')
open('paw_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('splitpaw markers P=%d'%len(lines))
