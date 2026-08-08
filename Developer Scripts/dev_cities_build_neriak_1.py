"""Neriak Foreign Quarter / Commons / Third Gate markers. native=(-loc2,-loc1)."""
def wn(p,q): return (-q,-p)
ZONE=(150,0,200); EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60); GM=(90,35,110)
def build(fn, rows, zlines):
    Z=-1.0; lines=[]
    def P(x,y,c,s,lb): lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
    for x,y,lb in zlines: P(x,y,ZONE,3,lb)
    for p,q,c,s,lb in rows:
        x,y=wn(p,q); P(x,y,c,s,lb)
    open(fn,'w',newline='').write('\r\n'.join(lines)+'\r\n'); print(fn,'P=%d'%len(lines))

# ---- FOREIGN QUARTER (neriaka) ----
build('neriaka_1.txt',[
 (-3,157, EXIT,3,'Succor_(to_Nektulos)'),
 (159,-104, MERCH,2,'Merchant_(Alcohol+Food)_Smugglers_Inn'),
 (106,-238, MERCH,2,'Merchant_(Food+Baking)_Dranas_Butcher'),
 (210,-244, MERCH,2,'Merchant_(Alcohol+Food)_Slugs_Tavern'),
 (199,-57,  MERCH,2,'Merchant_(Shoes+Bags)_Farlain'),
 (-268,-172,MERCH,2,'Merchant_(Jewelry+Gems)_Shinie_Tings'),
 (-323,-125,MERCH,2,'Merchant_(Food)_The_Gobbler'),
 (-291,-455,MERCH,2,'Merchant_(Weapons)_Thrack'),
 (-242,-388,MERCH,2,'Merchant_(Ogre/Troll_goods)_Bronk'),
 (15,1,     LAND,3,'City_Entrance_(Guard_SKor)'),
 (-336,-194,LAND,2,'Arena_(PvP)'),
 (0,-30,    NAMED,2,'XTa_Tempi/Timpi/Tompi_(40_Necro,_Robe)'),
 (-261,-237,DANGER,2,'Jacker_(44_SK)'),
 (-311,-222,DANGER,2,'Mrak_(48_Warrior)'),
 (-372,-317,DANGER,2,'Uglan_(50_Warrior)'),
 (-367,-438,DANGER,2,'Oosa_Shadowthumper_(42_SK)'),
 (-340,-209,DANGER,2,'Svunsa_(50_Warrior)'),
],[(-153.54,-29.04,'to_Nektulos_Forest'),(342.46,-83.98,'to_Neriak_Commons'),(454.50,252.43,'to_Neriak_Commons')])

# ---- COMMONS (neriakb) ----
build('neriakb_1.txt',[
 (46,-918,  LAND,3,'Bank_(Neriak_Down_Under)'),
 (46,-796,  MERCH,2,'Merchant_(Smithing)_Blind_Fish'),
 (59,-866,  MERCH,2,'Merchant_(Weapons)_Opal_HRugla'),
 (82,-901,  MERCH,2,'Merchant_(Jewelcraft)_Forge_House'),
 (40,-1218, MERCH,2,'Merchant_(Alcohol)_Lysanda'),
 (-135,-1062,MERCH,2,'Merchant_(Fletching+Arrows)_Bleek_Fletcher'),
 (132,-899, LAND,3,'Caster_Guild_(Tower_of_the_Spurned)'),
 (139,-900, MERCH,2,'Merchant_(Wiz/Mag/Ench_Spells)_Library'),
 (-28,-1150,LAND,3,'Warrior_Guild_Hall'),
 (132,-899, GM,2,'Aslyn_CLuzz_(GM_Wizard_61)'),
 (142,-963, GM,2,'Gath_NMare_(GM_Wizard_61)'),
 (128,-926, GM,2,'Belux_JVer_(GM_Magician_61)'),
 (149,-969, GM,2,'Jayna_DBious_(GM_Magician_61)'),
 (156,-963, GM,2,'Camia_VRetta_(GM_Enchanter_61)'),
 (133,-938, GM,2,'Drizm_JAxx_(GM_Enchanter_61)'),
 (-28,-1150,GM,2,'Jarrex_NRyt_(GM_Warrior_61)'),
 (24,-1127, GM,2,'Seloxia_Punox_(GM_Warrior_61)'),
 (-36,-1144,GM,2,'Narex_TVem_(GM_Warrior_61)'),
 (-51,-1217,GM,2,'Yegek_BLarin_(GM_Warrior_61)'),
 (-180,-560,NAMED,2,'A_Leatherfoot_Spy_(20_Rogue)'),
],[(854.17,-194.67,'to_Neriak_Third_Gate'),(389.31,-85.38,'to_Foreign_Quarter'),(465.03,229.92,'to_Foreign_Quarter')])

# ---- THIRD GATE (neriakc) ----
build('neriakc_1.txt',[
 (892,-969, EXIT,3,'Succor'),
 (408,-789, LAND,3,'Temple_of_Innoruuk_(Cleric_Guild)'),
 (400,-854, MERCH,2,'Merchant_(Cleric_Spells)_Myris'),
 (1303,-1255,LAND,3,'Necromancer+SK_Guild_(Hall_of_the_Dead)'),
 (913,-1278,LAND,3,'Library_(Wiz/Ench/Mag_Spells)'),
 (913,-1278,MERCH,2,'Merchant_(Wizard_Portal_Spells)_Jusar'),
 (628,-1318,LAND,3,'Rogue_Guild_(Hall_of_the_Ebon_Mask)'),
 (769,-1310,MERCH,2,'Merchant_(Small_Leather)_Furrier_Royale'),
 (864,-1424,LAND,2,'The_Maidens_Fancy_(Bar)'),
 (816,-1425,MERCH,2,'Merchant_(Gems/Jewelcraft)_The_Bauble'),
 (703,-1472,MERCH,2,'Merchant_(Alcohol)_Cuisine_Excelsior'),
 (763,-1512,MERCH,2,'Merchant_(Wine)_The_Rack'),
 (694,-1780,MERCH,2,'Merchant_(Smithing/DE_Chain)_Draan'),
 (408,-789, GM,2,'Perrir_Zexus_(GM_Cleric_61)'),
 (447,-848, GM,2,'Ithvol_KJasn_(GM_Cleric_61)'),
 (414,-810, GM,2,'Ulazia_WSelo_(GM_Cleric_61)'),
 (1303,-1255,GM,2,'Noxhil_VSek_(GM_Necromancer_61)'),
 (1280,-1250,GM,2,'Xon_Quexill_(GM_Necromancer_61)'),
 (1255,-1270,GM,2,'Loveal_SNez_(GM_Shadow_Knight_61)'),
 (1280,-1235,GM,2,'Nezzka_Tolax_(GM_Shadow_Knight_61)'),
 (628,-1318,GM,2,'Eolorn_JAxx_(GM_Rogue_61)'),
 (677,-1362,GM,2,'Pazin_Punox_(GM_Rogue_61)'),
 (411,-812, NAMED,2,'Verina_Tomb_(60_Cleric,_Innoruuks_Word)'),
 (1352,-1323,DANGER,2,'Degarran_Kixl_(38_SK)'),
],[(851.59,-215.86,'to_Neriak_Commons')])
