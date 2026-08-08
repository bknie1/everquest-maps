"""Ak'Anon markers — full merchant-by-category coverage (P1999) + guilds + landmarks.
loc -> native (-loc2,-loc1). Merchants labeled by what they sell (small green markers)."""
def wn(p,q): return (-q,-p)
EXIT=(160,105,0); LAND=(30,80,95); MERCH=(35,95,55); NAMED=(150,90,40); DANGER=(110,0,60); QUEST=(165,60,20)
Z=-1.0
M=[
 # --- exits ---
 (61,-78,      EXIT,3,'to_Steamfont_Mountains'),      # already native-ish; keep as-is below
 # --- guilds / landmarks (teal, size 3) ---
 (-429,848,    LAND,3,'Warrior_Guild_Gemchopper_Hall_(Trainers)'),
 (-1238,548,   LAND,3,'Abbey_of_Deep_Musing_(Cleric_Trainers)'),
 (-1181,558,   LAND,2,'Rogue_Guild_(hidden_under_Abbey)'),
 (-1090,1030,  LAND,3,'Library_Mechanamagica_(Ench/Mag/Wiz_Trainers)'),
 (-813,200,    LAND,3,'AkAnon_Palace_(King_AkAnon,_Oven/Kiln/Wheel)'),
 (-862,1348,   LAND,3,'Bank_of_AkAnon'),
 (-1252,946,   LAND,2,'The_Bar_(Brew_Barrel)'),
 (-1253,715,   LAND,2,'The_Smithy_(Weapons_+_Forge)'),
 (-880,470,    LAND,2,'AkAnon_Zoo'),
 # --- danger ---
 (-2100,407,   DANGER,3,'Necro_Guild_+_Mines_of_Malfunction_(Undead)'),
 # --- named / quest ---
 (-429,848,    NAMED,2,'Baxok_Curhunter_(GM_Warrior_61)'),
 (-813,813,    QUEST,2,'Priest_of_Discord_(PvP)'),
 (-192,1482,   NAMED,2,'A_Mechanic_(27)'),
 # --- MERCHANTS by what they sell (native = -loc2,-loc1) ---
]
# merchant list as raw P1999 loc (p,q) -> converted below
MERCH_LIST=[
 (1253,-715,'Merchant_(Weapons)_Smithy'),
 (1329,-762,'Merchant_(Weapons)_Warrior_Guild'),
 (1208,-714,'Merchant_(Smithing_+_Armor_Supplies)'),
 (1250,-879,'Merchant_(Fletching_Supplies)'),
 (1174,-759,'Merchant_(Shoes)'),
 (1347,-952,'Merchant_(Jewelry_Gems)'),
 (1332,-917,'Merchant_(Jewelry_Metals)'),
 (904,-284, 'Merchant_(Food_and_Drink)'),
 (891,-301, 'Merchant_(Baked_Goods_+_Alchemy)'),
 (1313,-915,'Merchant_(Tailoring_Supplies)'),
 (954,-37,  'Merchant_(Small_Cloth_+_Leather_Armor)'),
 (750,-173, 'Merchant_(Pottery_Supplies)'),
 (762,-140, 'Merchant_(Tinkering_Supplies)'),
 (760,-155, 'Merchant_(Ore_+_Metals)'),
 (1252,-946,'Merchant_(Alcohol)'),
 (1198,-551,'Merchant_(Cleric_Spells)'),
 (1090,-1030,'Merchant_(Magician_Spells)'),
 (1055,-980,'Merchant_(Wizard_Spells)'),
 (1105,-988,'Merchant_(Enchanter_Spells)'),
 (2098,-410,'Merchant_(Necromancer_Spells)'),
 (2112,-426,'Merchant_(Cleric_Spells_Dark)'),
 (1348,-862,'Merchant_(Banker)'),
]
lines=[]
# zone line + succor first (already native from prior file)
lines.append("P 78.4863, -61.4073, -0.8014, 150, 0, 200, 3, to_The_Steamfont_Mountains")
lines.append("P 35.0000, -47.0000, -1.0000, 160, 105, 0, 2, Succor_(to_Steamfont)")
for entry in M[1:]:
    x,y,c,s,lb=entry
    lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
for p,q,lb in MERCH_LIST:
    x,y=wn(p,q); lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,MERCH[0],MERCH[1],MERCH[2],2,lb))
open('akanon_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('akanon markers P=%d'%len(lines))
