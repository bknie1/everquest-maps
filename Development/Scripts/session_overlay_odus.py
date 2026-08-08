from PIL import Image, ImageDraw, ImageFont
base=Image.open('/mnt/user-data/uploads/1786168470247_image.png').convert('RGBA')
W,H=base.size; LEG=300
dim=Image.new('RGBA',(W,H),(255,255,255,60)); base=Image.alpha_composite(base,dim)
cv=Image.new('RGBA',(W+LEG,H),(24,22,20,255)); cv.paste(base,(0,0)); d=ImageDraw.Draw(cv)
def fnt(s,b=True):
    try:return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf",s)
    except:return ImageFont.load_default()
Z={
 'Toxxulia Forest':((30,150,120),[("Sylhithis' Dwell",85,68),('Arcadin',310,150),('East Plateau',300,62)]),
 'Stonebrunt Mtns':((150,110,40),[('North Barren Coast',400,215),('The Vasty Deep',405,345),('Cape Dreg',410,505)]),
}
GREY=(120,120,120)
ctx=[('Kerra Isle (your POI kept)',65,300),('Paineel (city - skipped)',195,438),('The Warrens (dungeon - skipped)',315,442)]
for zn,(col,pts) in Z.items():
    for lab,x,y in pts:
        d.ellipse([x-6,y-6,x+6,y+6],fill=col+(255,),outline=(255,255,255,255),width=2)
        f=fnt(11); tb=d.textbbox((0,0),lab,font=f); tw=tb[2]-tb[0]
        tx=x+9 if x<W-110 else x-9-tw
        d.text((tx,y-6),lab,font=f,fill=(20,18,16,255),stroke_width=3,stroke_fill=(255,255,255,235))
for lab,x,y in ctx:
    d.ellipse([x-5,y-5,x+5,y+5],outline=GREY+(255,),width=2)
    d.text((x+8,y-6),lab,font=fnt(10,False),fill=(60,58,55,255),stroke_width=3,stroke_fill=(235,235,235,220))
lx=W+12; d.text((lx,16),'EQOA -> EQ1  (Odus)',font=fnt(17),fill=(240,232,210,255))
d.text((lx,40),'Odus WAS in EQOA - now covered',font=fnt(11,False),fill=(190,182,165,255))
y=72
for zn,(col,pts) in Z.items():
    d.rectangle([lx,y+2,lx+14,y+14],fill=col+(255,),outline=(255,255,255,255),width=1)
    d.text((lx+22,y),zn,font=fnt(13),fill=(238,232,214,255)); y+=18
    for l,_,_ in pts: d.text((lx+22,y),'- '+l,font=fnt(10,False),fill=(180,174,158,255)); y+=13
    y+=6
d.text((lx,y+4),'grey = skipped',font=fnt(10,False),fill=(150,144,130,255)); y+=16
d.text((lx,y+4),'(city / dungeon / already',font=fnt(10,False),fill=(150,144,130,255)); y+=13
d.text((lx,y+4),' has your own POI)',font=fnt(10,False),fill=(150,144,130,255))
d.text((lx,H-30),'Faydwer: not in EQOA ->',font=fnt(10,False),fill=(150,144,130,255))
d.text((lx,H-17),'correctly gets nothing',font=fnt(10,False),fill=(150,144,130,255))
cv.convert('RGB').save('/mnt/user-data/outputs/_eqoa_eq1_alignment_odus.png')
print('saved odus overlay',cv.size)
