"""Surefall Glade markers: keep provided _1, add notable NPCs from wiki (native=(-b,-a))."""
provided=open('qrg_1.txt',encoding='utf-8',errors='replace').read().replace('\r\n','\n').strip('\n').split('\n')
provided=[l for l in provided if l.startswith('P')]

def wn(p,q): return (-q,-p)
EXIT=(160,105,0); MERCH=(35,95,55); FLETCH=(30,70,90); GM=(165,60,20); NAMED=(150,90,40); DANGER=(110,0,60)
Z=3.7510
# (wiki_p, wiki_q, color, size, label)
ADD=[
 (0,   0,   EXIT,   2,'Succor_(Evacuate)'),
 (225,-180, DANGER, 3,'Mammoth_(Great_Bear,_20-25)'),
 (144,-415, DANGER, 2,'Talym_Shoontar_(15)'),
 (143,-419, DANGER, 2,'Poacher_+_Gnoll_Poacher'),
 (243,-70,  NAMED,  2,'Merdan_Fleetfoot_(38)'),
 (111,-188, NAMED,  2,'Niera_Farbreeze_(Ranger_40)'),
 (239,-178, NAMED,  1,'Bren_Treeclimber_(7)'),
 (-9.75,-78.74, NAMED, 2,'Krystal_Aspen_(30,_camp)'),
 (67,-192,  GM,     2,'Corun_Finisc_(Druid,_Quest)'),
 (-103,-303,GM,     2,'Frenway_Marthank_(Quest)'),
 (154,-8,   MERCH,  2,'Colnro_Cedar_(Adv._Supplies)'),
 (118,-64,  FLETCH, 2,'Sivina_(Bard)'),
]
lines=list(provided)
for p,q,c,s,lb in ADD:
    x,y=wn(p,q)
    lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
open('qrg_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('wrote qrg_1.txt  P=%d (%d provided + %d added)'%(len(lines),len(provided),len(ADD)))
