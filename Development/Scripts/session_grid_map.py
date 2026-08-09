"""EQOA-style zone grid: EQ1 zones as cells, gaps filled with EQOA / suggested names."""
from PIL import Image, ImageDraw, ImageFont

# kind: eq=EQ1 zone in atlas | sub=dungeon/sub-zone (little surface space)
#       fill=Brandon's suggested gap name | eqoa=EQOA name | water | bnd=outside EQOA | na=didn't exist yet
A={
 (1,0):("The Northlands","fill"),(3,0):("Halas","eq"),(4,0):("Permafrost","sub"),
 (5,0):("Frigid Plain","fill"),(6,0):("Snowfist","eqoa"),(7,0):("Greyvax's Caves","eqoa"),
 (8,0):("Fayspire Gate","eqoa"),
 (0,1):("Zantar's Keep","eqoa"),(1,1):("Unkempt North","eqoa"),(2,1):("The Hatchland","fill"),
 (3,1):("Everfrost Peaks","eq"),(4,1):("The Nest","fill"),(5,1):("Freezeblood Village","eqoa"),
 (6,1):("Goldfeather Eyrie","eqoa"),(7,1):("Tethelin Forest","fill"),(8,1):("Ruins of Fayspire","fill"),
 (9,1):("Kara Village","eqoa"),(10,1):("Lavastorm","bnd"),(11,1):("Najena","sub"),
 (0,2):("Bogman Village","eqoa"),(1,2):("Unkempt Woods","fill"),(2,2):("Unkempt Glade","eqoa"),
 (3,2):("Guardian Forest","eqoa"),(4,2):("Diren Hold","eqoa"),(5,2):("Winters Deep","fill"),
 (6,2):("Moradhin","eqoa"),(7,2):("Shon-To Monastery","eqoa"),(8,2):("Thedruk","eqoa"),
 (9,2):("Ruins of Klick'Anon","fill"), (0,3):("Mariel Village","eqoa"),(1,3):("Twisted Tower","eqoa"),(2,3):("Jaggedpine","fill"),
 (3,3):("Blackburrow","sub"),(4,3):("Spirit Talker's Wood","eqoa"),(5,3):("Mount Hatespike","eqoa"),
 (6,3):("Baga Village","eqoa"),(7,3):("Lake Nerkuss","fill"),(8,3):("Castle Feister","eqoa"),
 (9,3):("Nektulos","eq"),(10,3):("Neriak","eq"),
 (0,4):("Wyndhaven","eqoa"),(1,4):("Jethro's Cast","eqoa"),(2,4):("Surefall Glade","eq"),
 (3,4):("Wymondham","eqoa"),(4,4):("Merry-by-Water","eqoa"),(5,4):("Runnyeye","sub"),
 (6,4):("Misty","eq"),(7,4):("Rivervale","eq"),(8,4):("Kithicor+","eq"),
 (9,4):("Collinridge Cemetery","eqoa"),
 (0,5):("Whale Hill","eqoa"),(1,5):("Crethley Manor","eqoa"),(2,5):("Q. Hills","eq"),
 (3,5):("Karana (W)","eq"),(4,5):("Karana (N)","eq"),(5,5):("Gorge","eq"),
 (6,5):("High Pass","eq"),(7,5):("Kithicor","eq"),(8,5):("Bobble-by-Water","eqoa"),
 (1,6):("Qeynos","eq"),(2,6):("Qeynos Prison","fill"),(3,6):("Fog Marsh","eqoa"),
 (4,6):("Karana (E)","eq"),(5,6):("Bandit Hills","eqoa"),(6,6):("Bastable Village","eqoa"),
 (7,6):("The Commonlands","eq"),(8,6):("Freeport","eq"),(9,6):("Hodstock and Temby","eqoa"),
 (0,7):("Highbourne","eqoa"),(1,7):("Stoneclaw","eqoa"),(2,7):("Splitpaw","sub"),
 (3,7):("Karana (S)","eq"),(4,7):("Urglunt's Wall","eqoa"),(5,7):("Widow's Peak","eqoa"),
 (6,7):("Befallen","sub"),(7,7):("North Ro","eq"),(8,7):("Muniel's Tea Garden","eqoa"),
 (1,8):("Geomancer's Citadel","eqoa"),(2,8):("Arena","sub"),(3,8):("Aviak Village","eqoa"),
 (4,8):("South Crossroads","eqoa"),(5,8):("Urglunt's Gate","eqoa"),(6,8):("Deathfist Citadel","eqoa"),
 (7,8):("Oasis","eq"),(8,8):("Sea of Lions","eqoa"),
 (0,9):("Geomancer's Pass","eqoa"),(1,9):("Cyclops' Fortress","eqoa"),(2,9):("Rathe Mountains","eq"),
 (3,9):("Lake Rathetear","eq"),(4,9):("Sphinx Pyramid","eqoa"),(5,9):("Kelinar","eqoa"),
 (6,9):("Takish'Hiz","eqoa"),(7,9):("South Ro","eq"),(8,9):("Great Waste","eqoa"),
 (0,10):("Dead Hills","fill"),(1,10):("The Feerrott (North)","fill"),(2,10):("Ogre Ruins","eqoa"),
 (3,10):("Oggok","eq"),(4,10):("Gerotar's Mines","eqoa"),(5,10):("Fort Alliance","eqoa"),
 (6,10):("Brog Fens","eqoa"),(7,10):("Guk","sub"),(8,10):("Sslathis","eqoa"),
 (0,11):("Envar","eqoa"),(1,11):("The Feerrott","eq"),(2,11):("West Feerrott","eqoa"),
 (3,11):("Moggok's Gate","eqoa"),(4,11):("Kerplunk Outpost","eqoa"),(5,11):("Innothule Swamp","eq"),
 (6,11):("Lake Noregard","eqoa"),(7,11):("Ant Colonies","eqoa"),(8,11):("Hazinak","eqoa"),
 (1,12):("Cazic Thule","sub"),(2,12):("Dinbak","eqoa"),(3,12):("Stone Watchers","eqoa"),
 (4,12):("Grobb","eq"),(5,12):("Burial Mounds","eqoa"),(6,12):("Broken Skull Rock","fill"),
 (7,12):("Basher's Enclave","eqoa"),
 (1,13):("Buried Sea","water"),(3,13):("Mila's Reef","eqoa"),(5,13):("Gulf of Gunthak","water"),
}
O={
 (1,0):("Grand Plateau","fill"),(2,0):("Grand Plateau","fill"),(3,0):("Erud's Crossing","eq"),
 (0,1):("Grand Plateau","fill"),(1,1):("Grand Plateau","fill"),(2,1):("Erudin","eq"),
 (3,1):("Ruins of Arcadin","fill"),
 (0,2):("Toxx W","eqoa"),(1,2):("Toxx N","eq"),(2,2):("Vasty Deep","eqoa"),(3,2):("Vasty Deep","eqoa"),
 (0,3):("Kerra Ridge","eq"),(1,3):("Toxx S","eq"),(2,3):("Stonebrunt","eq"),(3,3):("Vasty Deep","eqoa"),
 (4,3):("Barren Coast","eqoa"),
 (0,4):("Paineel","eq"),(1,4):("Warrens","sub"),(2,4):("Barren Coast","eqoa"),(3,4):("Barren Coast","eqoa"),
 (0,5):("The Hole","na"),(1,5):("Gulf of Uzun","water"),(2,5):("Barren Coast","eqoa"),
 (2,6):("Barren Coast","eqoa"),
}

STYLE={
 'eq'  :((44,58,80),(214,176,102),(244,226,186),'EQ1 zone (in the atlas)'),
 'sub' :((38,44,60),(150,140,120),(206,198,182),'dungeon / sub-zone (little surface space)'),
 'fill':((62,48,34),(226,150,72),(250,214,168),"suggested gap name"),
 'eqoa':((22,50,60),(86,196,188),(180,238,232),'EQOA name'),
 'water':((26,42,66),(96,140,196),(176,206,240),'water'),
 'bnd' :((56,30,32),(214,92,84),(248,198,192),'outside the EQOA world'),
 'na'  :((40,40,44),(110,108,112),(150,148,152),"didn't exist yet"),
}
CW,CH,GX,GY=150,58,158,66
def fnt(s,b=False):
    try: return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf",s)
    except: return ImageFont.load_default()

def wrap(d,txt,f,maxw):
    words=txt.split(' '); lines=[];cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textbbox((0,0),t,font=f)[2]>maxw and cur: lines.append(cur); cur=w
        else: cur=t
    lines.append(cur); return lines

def draw_grid(d,grid,ox,oy,title):
    d.text((ox,oy-44),title,font=fnt(26,True),fill=(238,226,196))
    for (c,r),(lab,kind) in grid.items():
        bg,br,tc,_=STYLE[kind]
        x=ox+c*GX; y=oy+r*GY
        h=CH if kind!='sub' else int(CH*0.62)
        yy=y+(CH-h)//2
        d.rounded_rectangle([x,yy,x+CW,yy+h],7,fill=bg,outline=br,width=3 if kind in('bnd','eq') else 2)
        if kind=='sub':
            d.ellipse([x+7,yy+h//2-3,x+13,yy+h//2+3],fill=br)
        if kind=='na':
            d.line([x+6,yy+h-8,x+CW-6,yy+8],fill=br,width=2)
        f=fnt(13 if len(lab)<=16 else 12,True)
        lines=wrap(d,lab,f,CW-18)
        th=len(lines)*16
        ty=yy+(h-th)//2
        for L in lines:
            tw=d.textbbox((0,0),L,font=f)[2]
            d.text((x+CW//2-tw//2,ty),L,font=f,fill=tc); ty+=16

maxAc=max(c for c,r in A); maxAr=max(r for c,r in A)
maxOc=max(c for c,r in O); maxOr=max(r for c,r in O)
OX_A,OY_A=60,150
OX_O=OX_A+(maxAc+1)*GX+110
W=OX_O+(maxOc+1)*GX+70
H=OY_A+(maxAr+1)*GY+300
img=Image.new('RGB',(W,H),(14,20,32)); d=ImageDraw.Draw(img,'RGBA')
d.rounded_rectangle([22,22,W-22,H-22],18,outline=(64,86,118),width=2)
d.text((60,44),"Norrath on an EQOA-style grid",font=fnt(34,True),fill=(240,228,198))
d.text((60,88),"EQ1 zones translated into EQOA-density cells, with the gaps filled in — a naming canvas for future zones",
       font=fnt(16),fill=(150,178,200))
draw_grid(d,A,OX_A,OY_A,"ANTONICA")
draw_grid(d,O,OX_O,OY_A,"ODUS")

# legend
ly=OY_A+(maxAr+1)*GY+40
d.rounded_rectangle([60,ly,60+1020,ly+180],12,fill=(24,34,52),outline=(70,92,124),width=2)
d.text((80,ly+16),"LEGEND",font=fnt(17,True),fill=(226,208,164))
i=0
for k,(bg,br,tc,desc) in STYLE.items():
    cx=80+(i%2)*500; cy=ly+50+(i//2)*32
    d.rounded_rectangle([cx,cy,cx+46,cy+22],5,fill=bg,outline=br,width=2)
    d.text((cx+58,cy+3),desc,font=fnt(13),fill=(206,202,192)); i+=1
n={k:sum(1 for v in list(A.values())+list(O.values()) if v[1]==k) for k in STYLE}
d.text((1120,ly+16),
   f"{n['eq']} EQ1 zones · {n['sub']} dungeons · {n['fill']} suggested names · {n['eqoa']} EQOA names",
   font=fnt(15,True),fill=(172,206,224))
for j,t in enumerate([
  "Dungeons are drawn as short cells: they sit under or beside a zone and shouldn't eat surface real estate.",
  "Lavastorm is red — EQOA's map puts it in the NE mountain boundary, so it was never a playable EQOA zone.",
  "The Hole is struck through: it didn't exist in the EQOA era.",
  "Stonebrunt runs down the middle of Odus; everything east of it is off-map from EQ1's slice -> signposts.",
  "Cell adjacency is geographic, not zone-connection: EQ1 links can curve (Feerrott->Oggok reads N in game).",]):
    d.text((1120,ly+46+j*24),t,font=fnt(13),fill=(140,166,190))
img.save('/mnt/user-data/outputs/_norrath_eqoa_grid.png')
print(f"grid: {len(A)} Antonica cells, {len(O)} Odus cells -> {W}x{H}")
print(" counts:",{k:v for k,v in n.items()})
