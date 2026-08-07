"""Southern Felwithe markers — FRESH. GMs, named, guards, and the full merchant roster
grouped by guild (= what they sell). native = (-loc2,-loc1)."""
def wn(p,q): return (-q,-p)
EXIT=(150,0,200); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(165,60,20); DANGER=(110,0,60); GM=(90,35,110); GUARD=(90,90,90)
Z=-1.0; lines=[]
def P(x,y,c,s,lb): lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
def L(p,q,c,s,lb): x,y=wn(p,q); P(x,y,c,s,lb)
# zone lines / teleporters (native coords from uploaded file)
for x,y,lb in [(833.8158,-233.1077,'to_Northern_Felwithe'),(619.1793,-435.7907,'to_Enchanter_Guild'),
 (601.4756,-457.9738,'to_Magician_Guild'),(584.8321,-435.2731,'to_Wizard_Guild'),
 (338.8209,-504.2612,'Teleporter_(back_to_entrance)'),(920.4243,-553.3588,'Teleporter_(back_to_entrance)'),
 (532.3592,-745.5568,'Teleporter_(back_to_entrance)')]:
    P(x,y,EXIT,3,lb)
# GMs (levels)
L(507,-409,GM,3,'Tarker_Blazetoss_(GM_Wizard_61)')
L(795,-599,GM,3,'Niola_Impholder_(GM_Magician_61)')
L(556,-839,GM,3,'Kinool_Goldsinger_(GM_Enchanter_61)')
# named / danger
L(736,-658,NAMED,3,'Joren_Nobleheart_(60,_Ghoulbane)')
L(375,-846,DANGER,2,'Farios_Elianos_(50,_Wizard)')
# guards
for p,q,lb in [(503,-366,'Guard_Golyn_(41)'),(692,-522,'Guard_Spioko_(41)'),(295,-584,'Guard_Plage_(41)'),
 (415,-585,'Guard_Psape_(39)'),(510,-855,'Guard_Tistan_(40)'),(415,-614,'Guard_Tynthal_(40)'),(408,-601,'Guard_Mystan_(40)')]:
    L(p,q,GUARD,2,lb)
# MERCHANTS grouped by guild = what they sell
WIZ=[(464,-348,'Earlyn'),(450,-340,'Celent_Newmist'),(465,-439,'Quiss_Stormseeker'),(437,-451,'Serri_Moonwatcher'),(462,-459,'Stormy')]
MAG=[(664,-514,'Elle_Leafdancer'),(720,-514,'Griff_Candleflame'),(664,-528,'Osisa_Goldenspear'),(692,-489,'Reff_Truewood'),(719,-528,'Vellera_Wintergreen')]
ENC=[(580,-872,'Lyssia'),(435,-872,'Moonthread'),(607,-935,'Alicia_Starshimmer'),(531,-869,'Berill_Gladeleaper'),
 (593,-911,'Est_Treewalker'),(496,-929,'Nestess_Branchtop'),(577,-801,'Porra'),(511,-910,'Seren_the_Swift'),
 (448,-811,'Srell_Tumblebrook'),(527,-800,'Xista_Finder'),(448,-805,'Yisasan')]
for p,q,nm in WIZ: L(p,q,MERCH,2,'Merchant_(Wizard_Spells)_'+nm)
for p,q,nm in MAG: L(p,q,MERCH,2,'Merchant_(Magician_Spells)_'+nm)
for p,q,nm in ENC: L(p,q,MERCH,2,'Merchant_(Enchanter_Spells)_'+nm)
L(567,-609,MERCH,2,'Merchant_Jewyln_(by_pond)')
L(445,-777,MERCH,2,'Merchant_(Jewelcraft)_Tyslin')
L(450,-340,MERCH,2,'Merchant_(Cloth+Gems+Potions)_common')
open('felwitheb_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('felwitheb markers P=%d'%len(lines))
