from PIL import Image, ImageDraw, ImageFont
base=Image.open('/mnt/user-data/uploads/1786163660342_image.png').convert('RGBA')
W,H=base.size
LEG=360
canvas=Image.new('RGBA',(W+LEG,H),(20,18,16,255))
canvas.paste(base,(0,0))
ov=Image.new('RGBA',(W+LEG,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
def fnt(sz,bold=True):
    try: return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",sz)
    except: return ImageFont.load_default()

# EQ1 zone footprints on EQOA terrain (orig 1000x1259 coords) + candidate EQOA POI
ZONES=[
 dict(name="Qeynos Hills",short="qeytoqrg",col=(0,165,175),
   poly=[(80,545),(360,540),(375,705),(90,705)],
   poi=[("Bear Cave",238,623,'g'),("Blakedown",316,569,'g'),("Druid's Watch",141,683,'g'),
        ("Spider Mine",250,686,'g'),("Mayfly Glade",319,651,'g'),("Hagley",119,579,'g')]),
 dict(name="West Karana",short="qey2hh1",col=(210,150,20),
   poly=[(360,470),(575,470),(575,705),(378,705)],
   poi=[("Jared's Blight",406,504,'g'),("Alseop's Wall",406,583,'g'),("Strag's Rest",497,558,'g'),
        ("Forkwatch",409,688,'g'),("Al-Karad Ruins",322,520,'b'),("Salt Mine",519,670,'b')]),
 dict(name="Gorge of King Xorbb",short="beholder",col=(175,0,140),
   poly=[(500,398),(625,398),(625,500),(500,500)],
   poi=[("Bandit Hills",513,469,'g'),("Merry-by-Water",509,398,'b')]),
 dict(name="Highpass Hold",short="highpass",col=(215,60,25),
   poly=[(620,430),(770,430),(770,645),(565,645),(560,560)],
   poi=[("Highpass Hold",603,469,'G'),("Ferran's Hope",678,586,'g'),
        ("Trail's End",569,595,'g'),("Dshinn's Redoubt",600,679,'b')]),
]
# translucent footprints
for z in ZONES:
    r,g,b=z['col']
    d.polygon(z['poly'],fill=(r,g,b,55),outline=(r,g,b,235))
    d.line(z['poly']+[z['poly'][0]],fill=(r,g,b,235),width=3)
canvas=Image.alpha_composite(canvas,ov)
d=ImageDraw.Draw(canvas)
# POI rings + labels
for z in ZONES:
    r,g,b=z['col']
    for nm,x,y,conf in z['poi']:
        rad=13 if conf=='G' else 9
        wdt=4 if conf in ('G',) else 3
        d.ellipse([x-rad,y-rad,x+rad,y+rad],outline=(255,255,255,255),width=wdt+2)
        d.ellipse([x-rad,y-rad,x+rad,y+rad],outline=(r,g,b,255),width=wdt)
        if conf=='b':  # borderline -> dashed feel: smaller hollow
            d.ellipse([x-3,y-3,x+3,y+3],fill=(r,g,b,255))
# zone name chips at polygon centroid
for z in ZONES:
    r,g,b=z['col']; xs=[p[0] for p in z['poly']]; ys=[p[1] for p in z['poly']]
    cx=sum(xs)//len(xs); cy=min(ys)-2
    t=z['name']; f=fnt(19); tb=d.textbbox((0,0),t,font=f); tw=tb[2]-tb[0]; th=tb[3]-tb[1]
    d.rectangle([cx-tw//2-7,cy-th-9,cx+tw//2+7,cy+3],fill=(r,g,b,255),outline=(255,255,255,255),width=2)
    d.text((cx-tw//2,cy-th-6),t,font=f,fill=(255,255,255,255))

# ---- Legend panel ----
lx=W+16; d.text((lx,20),"EQOA -> EQ1  fun-label alignment",font=fnt(20),fill=(240,232,210,255))
d.text((lx,48),"easter-egg candidates for the _3 layer",font=fnt(13,False),fill=(190,182,165,255))
y=92
key=[('G',"name matches EQ1 (grounded)"),('g',"in-zone (good fit)"),('b',"borderline / neighbor")]
for c,lab in key:
    if c=='G': d.ellipse([lx,y,lx+16,y+16],outline=(255,255,255,255),width=4)
    elif c=='g': d.ellipse([lx+2,y+2,lx+14,y+14],outline=(255,255,255,255),width=3)
    else: d.ellipse([lx+5,y+5,lx+11,y+11],fill=(220,220,220,255))
    d.text((lx+26,y-1),lab,font=fnt(13,False),fill=(210,204,188,255)); y+=24
y+=12
for z in ZONES:
    r,g,b=z['col']
    d.rectangle([lx,y,lx+16,y+16],fill=(r,g,b,255),outline=(255,255,255,255),width=1)
    d.text((lx+24,y-1),f"{z['name']}  ({z['short']})",font=fnt(15),fill=(238,232,214,255)); y+=24
    for nm,x,px,conf in z['poi']:
        mark={'G':'* ','g':'+ ','b':'~ '}[conf]
        col=(238,230,205,255) if conf!='b' else (170,164,150,255)
        d.text((lx+30,y),mark+nm,font=fnt(13,False),fill=col); y+=19
    y+=10
d.text((lx,H-70),"* grounded  + good fit  ~ borderline",font=fnt(12,False),fill=(160,154,140,255))
d.text((lx,H-50),"Positions = my interpretation;",font=fnt(12,False),fill=(160,154,140,255))
d.text((lx,H-34),"eyeball & correct as usual.",font=fnt(12,False),fill=(160,154,140,255))
canvas.convert('RGB').save('/mnt/user-data/outputs/_eqoa_eq1_alignment.png')
print("saved overlay", canvas.size)
