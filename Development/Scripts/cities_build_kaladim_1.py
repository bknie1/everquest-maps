"""Kaladim South (kaladima) + North (kaladimb) markers. native=(-loc2,-loc1)."""
def wn(p,q): return (-q,-p)
ZONE=(150,0,200); EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60); GM=(90,35,110)
def build(fn, rows, zlines):
    Z=-1.0; lines=[]
    def P(x,y,c,s,lb): lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
    for x,y,lb in zlines: P(x,y,ZONE,3,lb)
    for p,q,c,s,lb in rows:
        x,y=wn(p,q); P(x,y,c,s,lb)
    open(fn,'w',newline='').write('\r\n'.join(lines)+'\r\n'); print(fn,'P=%d'%len(lines))

# ---- SOUTH KALADIM (kaladima) — precise locs ----
build('kaladima_1.txt',[
 (-18,-2, EXIT,3,'Succor_(to_Butcherblock)'),
 (-118,-360, NAMED,3,'King_Kazon_Stormhammer_(50,_Castle)'),
 (73,300, LAND,3,'Warrior_Guild_(Storm_Guard)'),
 (100,360, LAND,2,'The_Arena_(not_PvP)'),
 (195,329, MERCH,2,'Merchant_(Adventuring_Supplies)_Haneka'),
 (178,313, MERCH,2,'Merchant_(Alcohol)_Tumpy_Irontoe'),
 (196,299, MERCH,2,'Merchant_(Baking/Muffins)_Gretta'),
 (136,221, MERCH,2,'Merchant_(Swords)_Staff_and_Spear'),
 (137,232, MERCH,2,'Merchant_(Fletching)_Alanury'),
 (95,233,  MERCH,2,'Merchant_(Brewing)_Pub_Kal'),
 (125,399, MERCH,2,'Merchant_(Shields+Weapons)_Redfists_Metal'),
 (173,389, MERCH,2,'Merchant_(Small_Leather)_Tanned_Assets'),
 (33,408,  MERCH,2,'Merchant_(Weapons)_Warrior_Guild'),
 (254,-186,MERCH,2,'Merchant_(Potions+Crystals)_Baldoleky'),
 (183,-138,MERCH,2,'Merchant_(Bags/Containers)_Aarina'),
 (224,-254,MERCH,2,'Merchant_(Cloth+Pottery)_Gurthas_Ware'),
 (73,300,  GM,2,'Furtog_Ogrebane_(GM_Warrior_61)'),
 (83,404,  GM,2,'Beno_Targnarle_(GM_Warrior_61)'),
 (-16,536, GM,2,'Canloe_Nusback_(GM_Warrior_61)'),
 (142,306, GM,2,'Hogunk_Ventille_(GM_Warrior_61)'),
 (-88,416, GM,2,'Bronlor_Lightblade_(Paladin_61)'),
],[(-39.79,57.27,'to_Butcherblock'),(-330.20,-411.64,'to_North_Kaladim'),(257.29,-379.61,'to_North_Kaladim')])

# ---- NORTH KALADIM (kaladimb) — guilds/bank/forge from map key (approx placement) ----
build('kaladimb_1.txt',[
 (494,300, EXIT,3,'Succor'),
 (700,250, LAND,3,'Bank_(Ratsbone_Treasure)'),
 (700,250, MERCH,2,'Merchant_(Throwing_Wpns)_Kafia_Ratsbone'),
 (710,255, MERCH,2,'Merchant_(Mining+Boxes)_Kadek'),
 (690,235, LAND,3,'Rogue_Guild_(Miners_Guild_628)'),
 (900,-40, LAND,3,'Cleric_Guild_(Clerics_of_Underfoot)'),
 (900,-40, MERCH,2,'Merchant_(Blunt_Weapons+Food)_Cleric_Guild'),
 (1080,90, LAND,3,'Paladin_Guild_(Miners_Guild_249)'),
 (600,200, MERCH,2,'Merchant_(Gems)'),
 (750,180, MERCH,2,'Merchant_(Ore+Smithy_Hammers)'),
 (1000,150,LAND,2,'Everhot_Forge_(Weapons+Armor+Molds)'),
 (1000,150,MERCH,2,'Merchant_(Jewelry_Metal+Gems)_Everhot'),
 (1150,60, MERCH,2,'Merchant_(Grapes,_Greybloom_Farms)'),
 (1080,90, GM,2,'Datur_Nightseer_(GM_Paladin)'),
 (1075,95, NAMED,2,'Gunlok_Jure_(Paladin,_Bone_Chips_turn-in)'),
 (690,235, GM,2,'Mater_(GM_Rogue)'),
 (900,-40, GM,2,'Priestess_Ghalea_(GM_Cleric)'),
],[(229.90,-360.07,'to_South_Kaladim'),(-341.46,-404.64,'to_South_Kaladim')])
