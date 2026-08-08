"""Steamfont markers: existing embedded labels + wiki POI (landmarks + notables)."""
raw=open('steamfont.txt',encoding='utf-8',errors='replace').read().replace('\r\n','\n')
Ls=[l for l in raw.split('\n') if l.startswith('L')]
Ps=[l for l in raw.split('\n') if l.startswith('P')]
# base becomes geometry-only
open('steamfont_base.txt','w',newline='').write('\r\n'.join(Ls)+'\r\n')

def wn(p,q): return (-q,-p)
EXIT=(160,105,0); LAND=(30,80,95); NAMED=(150,90,40); DANGER=(110,0,60)
Z=-30.0
ADD=[
 (159,-273, EXIT,  2,'Succor_(Windmills)'),
 (1690,-2100,LAND, 3,'Minotaur_Caves'),
 (1675,-1600,LAND, 2,'Giant_Clockwork_Cogs'),
 (1870,-240, LAND, 2,'The_Observers'),
 (1690,-2209,DANGER,3,'Meldrath_the_Malignant_(35)'),
 (1555,-2410,DANGER,3,'Minotaur_Lord_(30)'),
 (1227,-1639,DANGER,3,'Minotaur_Hero_(35)'),
 (1675,-1600,DANGER,2,'Nilits_Contraption_(20)'),
 (1891,-1716,NAMED, 2,'Kobold_Missionary_+_Camp'),
 (-306,1742, NAMED, 2,'Kobold_Shaman_Camp'),
 (245,-1135, NAMED, 2,'Feddi_Dooger_(Butcher_Knife)'),
 (128,-848,  NAMED, 2,'Charlotte_(Spider_35)'),
 (1350,-850, NAMED, 2,'Crusader_Swiftmoon_(28)'),
 (-1469,1719,DANGER,2,'Yendar_Starpyre_(65)'),
 (-153,-1913,NAMED, 2,'Winex_Kloktik_(12)'),
]
lines=list(Ps)
for p,q,c,s,lb in ADD:
    x,y=wn(p,q)
    lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,Z,c[0],c[1],c[2],s,lb))
open('steamfont_1.txt','w',newline='').write('\r\n'.join(lines)+'\r\n')
print('base geometry-only L=%d ; markers P=%d (%d embedded + %d added)'%(len(Ls),len(lines),len(Ps),len(ADD)))
