from PIL import Image, ImageDraw, ImageFont
base=Image.open('/mnt/user-data/uploads/1786163660342_image.png').convert('RGBA')
W,H=base.size; LEG=400
# dim base so markers pop
dim=Image.new('RGBA',(W,H),(255,255,255,70)); base=Image.alpha_composite(base,dim)
cv=Image.new('RGBA',(W+LEG,H),(24,22,20,255)); cv.paste(base,(0,0)); d=ImageDraw.Draw(cv)
def fnt(s,b=True):
    try:return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf",s)
    except:return ImageFont.load_default()
# zone -> (color, [(label,px,py)])  ; px,py in EQOA map pixels (1000x1259)
Z={
 'Qeynos Hills':((0,150,160),[('Bear Cave',238,623),('Mayfly Glade',319,651),('Forkwatch',409,688)]),
 'West Karana':((210,150,20),[('Jared\'s Blight',406,504),('Alseop\'s Wall',406,583),('Strag\'s Rest',497,558)]),
 'Highpass Hold':((215,60,25),[('Ferran\'s Hope',678,586),('Trail\'s End',569,595)]),
 'Everfrost':((70,130,200),[('Snowblind Plains',150,46),('Anu Village',241,46),('Frosteye Valley',315,53)]),
 'Surefall Glade':((40,140,70),[('Jethro\'s Cast',150,404),('Wyndhaven',50,417)]),
 'North Karana':((190,170,40),[('Bandit Hills',513,469),('Spirit Talker\'s Wood',285,130)]),
 'South Karana':((150,160,50),[('Aviak Village',235,768),('Centaur Valley',505,761),('Fort Solitude',421,793)]),
 'East Karana':((120,160,60),[('Saerk Towers',805,412),('Mu Lin\'s Reach',861,382),('Moss Mouth Cavern',702,404)]),
 'Misty Thicket':((60,150,90),[('Baga Village',497,328),('Mount Haledrake',438,306)]),
 'Rivervale':((90,180,120),[('Merry-by-Water',509,398)]),
 'Kithicor':((40,110,60),[('North Kithicor',758,292),('The Green Rift',888,312)]),
 'West Commonlands':((150,120,70),[('Bastable Village',664,518),('Tomb of Kings',752,531)]),
 'East Commonlands':((175,140,80),[('Temple of Light',861,484),('Babble-by-Water',973,306)]),
 'Nektulos':((110,80,140),[('Collinridge Cemetery',860,175),('Thedruk',690,180)]),
 'Lavastorm':((200,60,40),[('Kara Village',790,130),('NE Mountain Boundary',720,40)]),
 'Northern Ro':((200,170,90),[('Deathfist Citadel',788,684),('Muriel\'s Tea Garden',867,669),('Northwestern Ro',873,576)]),
 'Southern Ro':((210,180,70),[('Fox Canyons',788,749),('Al-Farak Ruins',864,790),('Sycamore Joy\'s Rest',861,869)]),
 'Oasis of Marr':((180,160,100),[('Sea of Lions',769,1035)]),
 'Innothule':((130,90,150),[('Kerplunk Outpost',508,1114),('Lake Noregard',596,1137),('Burial Mounds',677,1137)]),
 'Feerrott':((80,120,60),[('West Feerrott',253,1102),('Envar',150,1102),('Ogre Ruins',218,1012)]),
 'Rathe Mountains':((110,100,90),[('Cyclops\' Fortress',235,848),('Sphinx Pyramid',318,928),('Geomancer\'s Citadel',150,875)]),
 'Lake Rathetear':((80,130,170),[('Kelinar',426,948)]),
}
# plot markers + tiny labels
for zn,(col,pts) in Z.items():
    for lab,x,y in pts:
        d.ellipse([x-6,y-6,x+6,y+6],fill=col+(255,),outline=(255,255,255,255),width=2)
        f=fnt(11); tb=d.textbbox((0,0),lab,font=f); tw=tb[2]-tb[0]
        tx=x+9 if x<W-120 else x-9-tw
        d.text((tx,y-6),lab,font=f,fill=(20,18,16,255),
               stroke_width=3,stroke_fill=(255,255,255,235))
# legend
lx=W+14; d.text((lx,16),'EQOA -> EQ1  fun-label pass',font=fnt(20),fill=(240,232,210,255))
d.text((lx,42),'continent-wide easter-egg alignment',font=fnt(12,False),fill=(190,182,165,255))
y=74
for zn,(col,pts) in Z.items():
    d.rectangle([lx,y+2,lx+14,y+14],fill=col+(255,),outline=(255,255,255,255),width=1)
    d.text((lx+22,y),f'{zn}',font=fnt(13),fill=(238,232,214,255)); y+=17
    labs=', '.join(l for l,_,_ in pts)
    for line in [labs[i:i+52] for i in range(0,len(labs),52)]:
        d.text((lx+22,y),line,font=fnt(10,False),fill=(180,174,158,255)); y+=13
    y+=4
d.text((lx,H-20),'placements are guesstimates - eyeball & correct',font=fnt(11,False),fill=(150,144,130,255))
cv.convert('RGB').save('/mnt/user-data/outputs/_eqoa_eq1_alignment.png')
print('saved continent overlay',cv.size,'-',sum(len(p) for _,p in Z.values()),'labels')
