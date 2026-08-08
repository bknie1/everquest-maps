"""Sivax-style zone-connection graph: EQ1 Antonica + hypothetical EQOA/Tunaria zones."""
from PIL import Image, ImageDraw, ImageFont

W,H=1980,1330
BG=(18,26,40); PANEL=(24,34,52)
GOLD=(206,168,96); GOLDT=(238,216,166)
TEAL=(86,196,188); TEALT=(176,238,232)
RED=(214,92,84)
EDGE=(150,150,155); HEDGE=(86,196,188)

def fnt(s,b=False):
    try: return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf",s)
    except: return ImageFont.load_default()

# name -> (x, y, kind)   kind: 'eq' existing EQ1 zone, 'hy' hypothetical EQOA zone, 'bnd' boundary
N={
 # far north
 "Zantar's Keep":(105,70,'hy'), "Unkempt North":(268,70,'hy'), "Halas":(505,70,'eq'),
 "Snowfist":(672,70,'hy'), "Fayspire Gate":(838,70,'hy'),
 # north band
 "Mariel Village":(105,158,'hy'), "Twisted Tower":(268,158,'hy'), "Everfrost Peaks":(505,158,'eq'),
 "Permafrost":(660,158,'eq'), "Freezeblood Village":(838,158,'hy'), "Fayspire":(1012,158,'hy'),
 "Tethelin":(1170,158,'hy'), "Klik'Anon":(1332,158,'hy'), "Rogue Clockworks":(1508,158,'hy'),
 # upper mid
 "Unkempt Glade":(186,246,'hy'), "Guardian Forest":(420,246,'hy'), "Blackburrow":(578,246,'eq'),
 "Moradhin":(838,246,'hy'), "Kara Village":(1090,246,'hy'), "Solusek's Eye":(1250,246,'eq'),
 "Lavastorm Mtns":(1420,246,'bnd'), "Najena":(1590,246,'eq'),
 # mid-upper
 "Wyndhaven":(105,334,'hy'), "Jethro's Cast":(268,334,'hy'), "Surefall Glade":(430,334,'eq'),
 "Wymondham":(592,334,'hy'), "Merry-by-Water":(754,334,'hy'), "Runnyeye":(916,334,'eq'),
 "Misty Thicket":(1070,334,'eq'), "Castle Feister":(1250,334,'hy'), "Nektulos Forest":(1420,334,'eq'),
 "Neriak":(1590,334,'eq'),
 # mid
 "Whale Hill":(105,422,'hy'), "Crethley Manor":(268,422,'hy'), "Qeynos Hills":(430,422,'eq'),
 "Fog Marsh":(592,422,'hy'), "Gorge of King Xorbb":(916,422,'eq'), "Rivervale":(1070,422,'eq'),
 "Collinridge Cemetery":(1250,422,'hy'),
 # main east-west spine
 "Qeynos":(268,510,'eq'), "West Karana":(430,510,'eq'), "North Karana":(592,510,'eq'),
 "East Karana":(754,510,'eq'), "Highpass Hold":(916,510,'eq'), "Kithicor Forest":(1070,510,'eq'),
 "West Commonlands":(1240,510,'eq'), "East Commonlands":(1410,510,'eq'), "Freeport":(1580,510,'eq'),
 "Hodstock and Temby":(1770,510,'hy'),
 # south-central
 "Highbourne":(105,598,'hy'), "Stoneclaw":(268,598,'hy'), "South Karana":(592,598,'eq'),
 "Befallen":(1240,598,'eq'), "Northern Desert of Ro":(1440,598,'eq'), "Bobble-by-Water":(1770,598,'hy'),
 # lower
 "Geomancer's Citadel":(105,686,'hy'), "Lake Rathetear":(430,686,'eq'), "Arena":(578,686,'eq'),
 "Urglunt's Gate":(730,686,'hy'), "Oasis of Marr":(1440,686,'eq'), "Muniel's Tea Garden":(1770,686,'hy'),
 # lower 2
 "Rathe Mountains":(268,774,'eq'), "Feerrott":(490,774,'eq'), "Oggok":(646,774,'eq'),
 "Southern Desert of Ro":(1440,774,'eq'), "Takish'Hiz":(1770,774,'hy'),
 # bottom
 "Cazic Thule":(268,862,'eq'), "Brog Fens":(490,862,'hy'), "Innothule Swamp":(940,862,'eq'),
 "Upper Guk":(1110,862,'eq'), "Lower Guk":(1264,862,'eq'), "Great Waste":(1770,862,'hy'),
 # bottom 2
 "Stone Watchers":(268,950,'hy'), "Karplunk Outpost":(646,950,'hy'), "Grobb":(940,950,'eq'),
 "Sslathis":(1264,950,'hy'), "Hazinak":(1440,950,'hy'), "Basher's Enclave":(1620,950,'hy'),
}
N={k:(v[0],v[1]+96,v[2]) for k,v in N.items()}

# existing EQ1 connections
E=[("Halas","Everfrost Peaks"),("Everfrost Peaks","Permafrost"),("Everfrost Peaks","Blackburrow"),
 ("Blackburrow","Qeynos Hills"),("Qeynos Hills","Surefall Glade"),("Qeynos Hills","Qeynos"),
 ("Qeynos Hills","West Karana"),("West Karana","North Karana"),("North Karana","East Karana"),
 ("North Karana","South Karana"),("East Karana","Highpass Hold"),("East Karana","Gorge of King Xorbb"),
 ("Gorge of King Xorbb","Runnyeye"),("Runnyeye","Misty Thicket"),("Misty Thicket","Rivervale"),
 ("Rivervale","Kithicor Forest"),("Highpass Hold","Kithicor Forest"),("Kithicor Forest","West Commonlands"),
 ("West Commonlands","East Commonlands"),("West Commonlands","Befallen"),("East Commonlands","Freeport"),
 ("East Commonlands","Nektulos Forest"),("East Commonlands","Northern Desert of Ro"),
 ("Nektulos Forest","Neriak"),("Nektulos Forest","Lavastorm Mtns"),("Lavastorm Mtns","Solusek's Eye"),
 ("Lavastorm Mtns","Najena"),("Northern Desert of Ro","Oasis of Marr"),("Oasis of Marr","Southern Desert of Ro"),
 ("Southern Desert of Ro","Innothule Swamp"),("Innothule Swamp","Upper Guk"),("Upper Guk","Lower Guk"),
 ("Innothule Swamp","Grobb"),("Innothule Swamp","Feerrott"),("Feerrott","Oggok"),("Feerrott","Cazic Thule"),
 ("Feerrott","Rathe Mountains"),("Rathe Mountains","Lake Rathetear"),("Lake Rathetear","Arena"),
 ("Lake Rathetear","South Karana")]
# hypothetical EQOA links
HE=[("Everfrost Peaks","Snowfist"),("Snowfist","Fayspire Gate"),("Fayspire Gate","Fayspire"),
 ("Everfrost Peaks","Freezeblood Village"),("Everfrost Peaks","Guardian Forest"),
 ("Guardian Forest","Moradhin"),("Everfrost Peaks","Unkempt North"),("Unkempt North","Zantar's Keep"),
 ("Unkempt North","Twisted Tower"),("Twisted Tower","Mariel Village"),("Unkempt North","Unkempt Glade"),
 ("Unkempt Glade","Jethro's Cast"),("Wyndhaven","Whale Hill"),("Wyndhaven","Crethley Manor"),
 ("Crethley Manor","Qeynos Hills"),("Jethro's Cast","Surefall Glade"),("Surefall Glade","Wymondham"),
 ("Wymondham","West Karana"),("Fog Marsh","West Karana"),("Fog Marsh","Crethley Manor"),
 ("Merry-by-Water","North Karana"),("Merry-by-Water","Rivervale"),("Moradhin","Misty Thicket"),
 ("Fayspire","Tethelin"),("Tethelin","Klik'Anon"),("Klik'Anon","Rogue Clockworks"),
 ("Klik'Anon","Kara Village"),("Kara Village","Castle Feister"),("Castle Feister","Nektulos Forest"),
 ("Collinridge Cemetery","Nektulos Forest"),("Highbourne","Stoneclaw"),("Stoneclaw","South Karana"),
 ("Highbourne","South Karana"),("Geomancer's Citadel","Rathe Mountains"),("Urglunt's Gate","South Karana"),
 ("Urglunt's Gate","Rathe Mountains"),("Brog Fens","Feerrott"),("Brog Fens","Innothule Swamp"),
 ("Karplunk Outpost","Innothule Swamp"),("Stone Watchers","Cazic Thule"),("Sslathis","Lower Guk"),
 ("Hazinak","Sslathis"),("Basher's Enclave","Hazinak"),("Great Waste","Southern Desert of Ro"),
 ("Takish'Hiz","Southern Desert of Ro"),("Takish'Hiz","Great Waste"),
 ("Muniel's Tea Garden","Northern Desert of Ro"),("Bobble-by-Water","Freeport"),
 ("Hodstock and Temby","Bobble-by-Water"),("Hodstock and Temby","East Karana"),
 ("Kara Village","Lavastorm Mtns")]

BW,BH=140,46
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img,'RGBA')
# subtle vignette panel
d.rounded_rectangle([26,26,W-26,H-26],18,outline=(70,92,124),width=2)

def rect(n):
    x,y,_=N[n]; return (x-BW//2,y-BH//2,x+BW//2,y+BH//2)
def dash(p1,p2,col,w=2,dl=9,gp=7):
    import math
    x1,y1=p1;x2,y2=p2; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy)
    if L==0: return
    ux,uy=dx/L,dy/L; t=0
    while t<L:
        e=min(t+dl,L)
        d.line([x1+ux*t,y1+uy*t,x1+ux*e,y1+uy*e],fill=col,width=w); t=e+gp
def anchor(a,b):
    ax,ay,_=N[a]; bx,by,_=N[b]
    return (ax,ay),(bx,by)

for a,b in E:
    p1,p2=anchor(a,b); d.line([p1,p2],fill=EDGE+(190,),width=2)
for a,b in HE:
    p1,p2=anchor(a,b); dash(p1,p2,HEDGE+(200,),2)

for n,(x,y,k) in N.items():
    r=rect(n)
    if k=='eq':
        d.rounded_rectangle(r,7,fill=(30,42,62),outline=GOLD,width=2); tc=GOLDT
    elif k=='bnd':
        d.rounded_rectangle(r,7,fill=(48,28,30),outline=RED,width=3); tc=(246,196,190)
    else:
        d.rounded_rectangle(r,7,fill=(22,44,56),outline=TEAL,width=2)
        # dashed inner to read as "proposed"
        d.rounded_rectangle((r[0]+4,r[1]+4,r[2]-4,r[3]-4),5,outline=(46,120,118),width=1); tc=TEALT
    words=n.split(' ')
    lines=[]; cur=''
    for wd in words:
        t=(cur+' '+wd).strip()
        if len(t)>17 and cur: lines.append(cur); cur=wd
        else: cur=t
    lines.append(cur)
    fs=13 if max(len(l) for l in lines)<=15 else 12
    f=fnt(fs,True)
    th=len(lines)*(fs+3)
    yy=y-th//2+1
    for l in lines:
        tb=d.textbbox((0,0),l,font=f); tw=tb[2]-tb[0]
        d.text((x-tw//2,yy),l,font=f,fill=tc); yy+=fs+3

# ---- title + legend ----
d.text((60,52),"Tunaria Overlay — hypothetical EQOA zones on the classic Antonica graph",font=fnt(26,True),fill=(238,224,190))
d.text((60,88),"Existing EQ1 zones with the EQOA-only areas filled in as proposed zones + links",font=fnt(15),fill=(150,178,200))

lx,ly=60,1096
d.rounded_rectangle([lx,ly,lx+560,ly+180],12,fill=PANEL,outline=(70,92,124),width=2)
d.text((lx+20,ly+16),"LEGEND",font=fnt(16,True),fill=(226,208,164))
d.rounded_rectangle([lx+20,ly+48,lx+120,ly+80],6,fill=(30,42,62),outline=GOLD,width=2)
d.text((lx+134,ly+56),"existing EQ1 zone",font=fnt(14),fill=GOLDT)
d.rounded_rectangle([lx+20,ly+92,lx+120,ly+124],6,fill=(22,44,56),outline=TEAL,width=2)
d.text((lx+134,ly+100),"hypothetical EQOA/Tunaria zone",font=fnt(14),fill=TEALT)
d.rounded_rectangle([lx+20,ly+136,lx+120,ly+164],6,fill=(48,28,30),outline=RED,width=3)
d.text((lx+134,ly+142),"outside the EQOA world (boundary)",font=fnt(14),fill=(246,196,190))
d.line([lx+330,ly+62,lx+420,ly+62],fill=EDGE,width=2)
d.text((lx+430,ly+54),"EQ1 link",font=fnt(13),fill=(200,200,205))
dash((lx+330,ly+106),(lx+420,ly+106),HEDGE,2)
d.text((lx+430,ly+98),"proposed link",font=fnt(13),fill=TEALT)

nh=sum(1 for v in N.values() if v[2]=='hy')
ne=sum(1 for v in N.values() if v[2]=='eq')
d.text((700,1110),f"{ne} existing zones  ·  {nh} proposed Tunaria zones  ·  {len(E)} existing links  ·  {len(HE)} proposed links",
       font=fnt(15,True),fill=(170,205,222))
d.text((700,1138),"Lavastorm is drawn red: EQOA's map puts it in the NE mountain boundary, so it was never a",font=fnt(13),fill=(150,178,200))
d.text((700,1160),"playable EQOA zone — it is the edge of the old world, which is why it only gets signposts.",font=fnt(13),fill=(150,178,200))
d.text((700,1190),"Proposed links are geographic reads off the EQOA world map, not canon adjacency.",font=fnt(13),fill=(130,155,178))
d.text((700,1212),"Use it to carve out space for future zone development.",font=fnt(13),fill=(130,155,178))

img.save('/mnt/user-data/outputs/_tunaria_hypothetical_zone_map.png')
print(f"hypothetical map: {ne} existing, {nh} proposed, {len(E)}+{len(HE)} links")
