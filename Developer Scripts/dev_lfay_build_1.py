prov=[l.strip() for l in open('lfaydark_1.txt',encoding='utf-8',errors='replace').read().replace('\r\n','\n').split('\n') if l.startswith('P')]
def wn(p,q): return (-q,-p)
EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60)
Z=1.0
ADD=[
 (-108,-1770,EXIT,2,'Succor'),
 (1775,3100, MERCH,2,'Brownie_Compound_(Ench_Spells)'),
 (1094,3618, LAND, 3,'Faerie_Village_+_Gearheart'),
 (1390,2075, LAND, 2,'Bandit_Camp'),
 (-280,1255, MERCH,2,'Wood_Elf_Ranger_Outpost'),
 (-900,1100, LAND, 2,'Teirdal_Camp_(Wu)'),
 (-522,1683, LAND, 2,'Orc_Camp'),
 (1585,505,  DANGER,3,'Equestrielle_the_Corrupted_(40)'),
 (-522,1683, DANGER,2,'Orc_Chief_(22)'),
 (1307,-1218,DANGER,3,'Pained_Unicorn_(60)'),
 (-902,1185, DANGER,2,'Dragoon_Szorn_(45)'),
 (-899,1101, DANGER,2,'Priestess_Llandra_(45)'),
 (1082,-142, NAMED, 2,'Whimsy_Larktwitter_(Pixie)'),
 (46,2245,   NAMED, 2,'Larik_ZVole_(17)'),
 (400,-640,  NAMED, 2,'Crookstinger_(Wasp)'),
 (-720,1690, MERCH, 2,'Kalayia_Woodwhisper_(Druid)'),
 (1066,2899, NAMED, 2,'Old_Dimshimmer'),
]
lines=list(prov)
for p,q,c,s,lb in ADD:
    x,y=wn(p,q); lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
open('lfaydark_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('lfay markers P=%d (%d provided + %d added)'%(len(lines),len(prov),len(ADD)))
