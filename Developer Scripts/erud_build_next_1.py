"""Erudin City (erudnext) markers — FRESH build (not append). Full merchant-by-category
coverage (EQL locs), guild masters w/levels, temples/library/inn landmarks, teleporters.
native = (-loc2,-loc1)."""
def wn(p,q): return (-q,-p)
EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); QUEST=(165,60,20); TELE=(20,120,150)
Z=-1.0
lines=[]
def P(x,y,c,s,lb): lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
def L(p,q,c,s,lb): x,y=wn(p,q); P(x,y,c,s,lb)
# zone-line portals (native coords, from uploaded geometry)
for x,y,lb in [(183.8881,1549.1428,'to_Toxxulia_Forest'),(277.5882,644.6471,'to_Erudin_Docks_(in_zone)'),
 (7.0634,328.6423,'to_Erudin_City_(in_zone)'),(183.3911,644.8334,'to_Erudin_Palace'),
 (335.6836,-50.1157,"to_Eruds_Crossing_(ferry)"),(353.9587,-106.5309,"to_Eruds_Crossing_(translocator)")]:
    P(x,y,(150,0,200),3,lb)
P(109,-309,EXIT[0] and EXIT,3,'Succor_(Pier)') if False else L(-309,109,EXIT,3,'Succor_(Pier)')
# --- landmarks (teal) ---
L(-640,-94, LAND,4,'Temple_of_Divine_Light_(Cleric+Paladin,_Quellious)')
L(-1045,-384,LAND,4,'Temple_of_Deepwater_Knights_(Cleric+Paladin,_Prexus)')
L(-1050,-212,LAND,4,'Erudin_City_Library')
L(-1166,-13, LAND,3,'Vasty_Deep_Inn_(Enchanter_Trainer)')
L(-1002,-153,LAND,3,'Erudin_Surplus_(Food,_Bags,_Brew/Oven/Kiln)')
L(166,-331,  LAND,3,'City_Armory_(Chain_+_Plate_Armor,_Forge)')
L(-730,-234, TELE,3,'Teleporter_to_Erudin_Palace')
# --- guild masters (levels kept) ---
for p,q,lb in [(-682,-70,'Cipse_Tospyr_(GM_Cleric_61)'),(-643,-41,'Depnar_Bulrious_(GM_Paladin_70)'),
 (-724,-89,'Reklon_Gnallen_(GM_Paladin_61)'),(-602,-135,'Jras_Solsier_(GM_Paladin_61)'),
 (-709,-89,'Rarnan_Lapice_(GM_Cleric_61)'),(-652,-94,'Lumi_Stergnon_(GM_Cleric_61)'),
 (-640,-94,'Leraena_Shelyrak_(GM_Cleric_61)'),(-1045,-384,'Gans_Paust_(GM_Cleric_61)'),
 (-1070,-415,'Dleria_Mausrel_(GM_Cleric_61)'),(-1062,-387,'Breya_Nostulia_(GM_Paladin_61)'),
 (-1109,-399,'Laoni_Reista_(GM_Paladin_61)'),(-1115,-368,'Mikeana_Tolstaub_(GM_Cleric_61)')]:
    L(p,q,QUEST,2,lb)
# --- MERCHANTS by what they sell ---
for p,q,lb in [
 (-1095,-89,'Merchant_(Adventuring_Supplies)_Otumar'),
 (-1023,-94,'Merchant_(Weapons)_Palus_Weaponsmith'),
 (-725,-286,'Merchant_(Smithing_+_Metals)_Steelfinger'),
 (-994,-78, 'Merchant_(Leather_Armor)_Finleather'),
 (-689,-101,'Merchant_(Leather_+_Tanning)_Tanner'),
 (-755,-112,'Merchant_(Cloth_Armor)_Weaver'),
 (-899,-159,'Merchant_(Cloth_+_Tailoring)_Weaver'),
 (136,109,  'Merchant_(Baked_Goods)_Breadmaker'),
 (-1175,-331,'Merchant_(Alcohol)_Bluehawk'),
 (-1186,-333,'Merchant_(Food_+_Alcohol)_Bluehawk'),
 (232,96,   'Merchant_(Fishing_+_Sailing)_Sailwind'),
 (207,-5,   'Merchant_(Fishing_Supplies)_Saltamer'),
 (-1050,-212,'Merchant_(Enchanter_Illusion_Spells)_Beteria'),
 (-1105,-213,'Merchant_(Cleric_Spells)_Belstince'),
 (-1048,-244,'Merchant_(Wizard_+_Mage_Spells)_Ellent'),
 (-1093,-223,'Merchant_(Bard_Songs_+_Spells)_Rellasp'),
 (-1156,-61,'Merchant_(Bags_+_Boxes)_Renthalis'),
 (-1094,-470,'Merchant_(Weapons)_Deepwater_Aserdon'),
 (-1070,-398,'Merchant_(Sharp_Weapons)_Deepwater_Nyjuss'),
 (-1031,-374,'Merchant_(Blunt_Weapons)_Deepwater_Belstince'),
 (-1066,-417,'Merchant_(Armor)_Deepwater_Varselli'),
 (-622,-83, 'Merchant_(Weapons)_Divine_Light_Niphiria'),
 (-651,-44, 'Merchant_(Cloth_+_Leather)_Divine_Light_Respelti'),
]:
    L(p,q,MERCH,2,lb)
open('erudnext_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('erudnext markers P=%d'%len(lines))
