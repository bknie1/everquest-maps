"""Ak'Anon markers — guild halls/trainers + services + merchants.
Coords from Project 1999 (same /loc convention as EQL); native = (-loc2, -loc1)."""
def wn(p,q): return (-q,-p)
EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60)
Z=-1.0
lines=["P 78.4863, -61.4073, -0.8014, 150, 0, 200, 3, to_The_Steamfont_Mountains"]
ADD=[
 (47,-35,     EXIT,  2,'Succor_(to_Steamfont)'),
 # --- guild halls / trainers ---
 (848,-429,   LAND,  3,'Warrior_Guild_(Baxok_GM_+_Narron_Jenork)'),
 (1238,-548,  LAND,  3,'Abbey_of_Deep_Musing_(Cleric_Trainers)'),
 (1181,-558,  LAND,  2,'Rogue_Guild_(under_Abbey)'),
 (1090,-1030, LAND,  3,'Library_Mechanamagica_(Ench/Mag/Wiz)'),
 (2100,-407,  DANGER,3,'Necro_Guild_+_Mines_of_Malfunction_(Undead)'),
 (813,-200,   LAND,  2,'AkAnon_Palace_Info_(to_King)'),
 # --- landmarks / services ---
 (1348,-862,  LAND,  3,'Bank_of_AkAnon'),
 (1252,-946,  LAND,  2,'The_Bar_(Brew_Barrel)'),
 (1253,-715,  LAND,  2,'The_Smithy_(Weapons_+_Forge)'),
 # --- clockwork merchants (distinct services) ---
 (1347,-952,  MERCH, 2,'Clockwork_Jeweler'),
 (1250,-879,  MERCH, 2,'Clockwork_Bowyer_(Fletching)'),
 (1174,-759,  MERCH, 2,'Clockwork_Cobbler_(Shoes)'),
 (1208,-714,  MERCH, 2,'Clockwork_Armorer'),
 (1265,-924,  MERCH, 2,'Clockwork_Brewmaster'),
 (891,-301,   MERCH, 2,'Clockwork_Alchemist_+_Baker'),
 (904,-284,   MERCH, 2,'Clockwork_Grocer_(Food)'),
 (987,-52,    MERCH, 2,'Clockwork_Tailor'),
 (954,-37,    MERCH, 2,'Clockwork_Tanner_(Leather)'),
 (760,-155,   MERCH, 2,'Clockwork_Miner'),
 (750,-173,   MERCH, 2,'Clockwork_Potter'),
 (762,-140,   MERCH, 2,'Clockwork_Sketcher'),
 (1482,-192,  NAMED, 2,'A_Mechanic_(27)'),
]
for p,q,c,s,lb in ADD:
    x,y=wn(p,q); lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
open('akanon_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('akanon markers P=%d (1 zone line + %d)'%(len(lines),len(ADD)))
