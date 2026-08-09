"""EQOA -> EQ1 alignment: single source of truth for maps + report."""
from PIL import Image, ImageDraw, ImageFont

# tier: 3=large(size4) 2=med(size3) 1=small(size2)
# kind: 'D' diamond (on map), 'A' arrow/signpost (dir), 'B' boundary
# ASSIGN[eq1_zone] = dict(pos=(x,y) in Trutz orig 474x631, off=(dx,dy) label-block offset,
#                          dia=[(name,tier)], arr=[(name,dir)], note=str)
ANT = {
 'Everfrost Peaks': dict(pos=(170,107), off=(-150,-60), dia=[
      ('Snowblind Plains',2),('Anu Village',2),('Frosteye Valley',2),('Snowfist',1),
      ("Greyvax's Caves",1),('Freezeblood Village',1),('Diren Village',1),('Goldfeather Eyrie',1)],
    arr=[('Unkempt North','W'),("Zentar's Keep",'W'),('Fayspire Gate','NE')],
    note='Huge zone; EQOA names the whole northern icefield.'),
 'Blackburrow': dict(pos=(140,197), off=(-118,10), dia=[], arr=[],
    note='EQOA name = the EQ1 zone name. Nothing to add.'),
 'Surefall Glade': dict(pos=(80,223), off=(-70,-34), dia=[], arr=[("Jethro's Cast",'W'),('Wymondham','E')],
    note='EQOA "Surefall Glade" = same place. Tiny zone -> signposts only.'),
 'Qeynos Hills': dict(pos=(68,261), off=(-62,26), dia=[
      ('Bear Cave',2),('Mayfly Glade',2),('Forkwatch',2),("Druid's Watch",1),
      ('Spider Mine',1),('Blakedown',1),('Hagley',1),('Qeynos Prison',1)],
    arr=[('Wyndhaven','W'),('Crethly Manor','NW')],
    note='Dense EQOA cluster NE of Qeynos maps almost 1:1 onto this zone.'),
 'West Karana': dict(pos=(114,261), off=(-40,64), dia=[
      ("Jared's Blight",2),("Alseop's Wall",2),("Strag's Rest",2),('Al-Karad Ruins',1),('Salt Mine',1)],
    arr=[('Fog Marsh','W'),('Wymondham','NW')],
    note="Jared's Blight = Dorvar Manor on the EQOA map."),
 'North Karana': dict(pos=(156,261), off=(6,-70), dia=[
      ], arr=[("Spirit Talker's Wood",'NW')],
    note='Merry-by-Water is the halfling town feuding with Bobble-by-Water (Great Pie Crisis).'),
 'East Karana': dict(pos=(199,261), off=(52,-78), dia=[
      ('Saerk Towers',2),("Mu Lin's Reach",2),('Moss Mouth Cavern',1),('The Green Rift',1)],
    arr=[('Hodstock / Temby','E'),('Bobble-by-Water','E')], note=''),
 'Beholders Maze': dict(pos=(210,205), off=(58,-30), dia=[('Bandit Hills',1)], arr=[],
    note='Gorge of King Xorbb. EQOA has no beholder analog; Bandit Hills is the nearest fit.'),
 'South Karana': dict(pos=(158,330), off=(-118,52), dia=[
      ('Aviak Village',3),('South Crossroads',3),('Centaur Valley',2),("Urglunt's Wall",2),
      ("Urglunt's Gate",2),("Widow's Peak",2),("Wktaan's 4th Talon",1),('Serpent Hills',1)],
    arr=[('Highbourne','W'),('Stoneclaw','NW')],
    note='South Crossroads = "Fort Solitude" on some maps; EQOA name preferred. Aviak Village + Centaur Valley have real EQ1 locs.'),
 'Misty Thicket': dict(pos=(258,211), off=(52,-16), dia=[('Baga Village',2)],
    arr=[('Mt. Hatespike','NW'),('Moradhim','N')],
    note='Mt. Hatespike (The Lost Isle) sits NW, outside the zone.'),
 'Rivervale': dict(pos=(262,243), off=(56,12), dia=[], arr=[('Merry-by-Water','NW'),('Bobble-by-Water','E')],
    note='EQOA "Rivervale" = same. The two -by-Water halfling towns are a lore pair.'),
 'Highpass Hold': dict(pos=(249,270), off=(-96,40), dia=[
      ("Ferran's Hope",2),("Trail's End",2),('Bastable Village',2),("Dshinn's Redoubt",1)],
    arr=[], note='EQOA labels "Highpass Hold" in the same spot - strongest 1:1 anchor on the continent.'),
 'Kithicor Wood': dict(pos=(291,279), off=(-30,58), dia=[('North Kithicor',2),('The Green Rift',1)],
    arr=[], note=''),
 'West Commonlands': dict(pos=(337,281), off=(-16,74), dia=[('Tomb of Kings',2),('Desert Hate',1)],
    arr=[], note=''),
 'East Commonlands': dict(pos=(375,281), off=(30,90), dia=[('Temple of Light',2),('Deathfist Forge',1)],
    arr=[('Bobble-by-Water','NE')], note=''),
 'Nektulos Forest': dict(pos=(393,226), off=(48,-46), dia=[
      ],
    arr=[('Klik\'Anon','NE')],
    note='Castle Felstar = Fort Barick. Foggy witch-woods styling (see tree study).'),
 'Lavastorm Mountains': dict(pos=(373,129), off=(-104,-58), dia=[],
    arr=[('Kara Village','SW'),("Klik'Anon",'S'),('Fayspire','SW')],
    note='*** NOT an EQOA zone -- sits in the grey "NE Mountain Boundary" band. Boundary marker + signposts only, no on-map diamonds.'),
 'Northern Desert of Ro': dict(pos=(402,335), off=(46,-8), dia=[
      ('Deathfist Citadel',2),("Muniel's Tea Garden",2),('Northwestern Ro',1)], arr=[], note=''),
 'Southern Desert of Ro': dict(pos=(327,478), off=(-128,-30), dia=[
      ('Box Canyons',2),('Al Farak Ruins',2),("Sycamore Joy's Rest",1),('Eternal Desert',1)],
    arr=[('Great Waste','E'),("Takish'Hiz","SE")],
    note='Box Canyons (not "Fox") per wiki.eqoa.live.'),
 'Oasis of Marr': dict(pos=(367,423), off=(44,-16), dia=[('Oasis',1)],
    arr=[('Sea of Lions','E'),('Great Waste','NE')], note='EQOA "Oasis" sits in the same spot.'),
 'Innothule Swamp': dict(pos=(353,527), off=(40,10), dia=[
      ('Lake Noregard',1),('Burial Mounds',1),('Ant Colonies',1)],
    arr=[('Kerplunk Outpost','W'),('Broken Skull Rock','S')],
    note='EQ1 shows only ONE SLICE of the EQOA swamp - Kerplunk Outpost sits outside it, so it becomes a signpost (W from here, E from Feerrott).'),
 'Feerrott': dict(pos=(120,460), off=(-112,26), dia=[
      ('West Feerrott',2),('Tomb City of Envar',1),('Ogre Ruins',1),('Dead Hills',1),("Moggok Gate",1)],
    arr=[('Kerplunk Outpost','E'),("Gerntar's Mines",'E'),('Oggok','NE (path curves back W)')],
    note='Paired signpost: Kerplunk lies E of Feerrott and W of Innothule - the two arrows bracket it.'),
 'Rathe Mountains': dict(pos=(112,429), off=(-116,-40), dia=[
      ("Cyclops's Fortress",2),('Sphinx Pyramid',2),("Geomancer's Citadel",2),("Geomancer's Pass",1)],
    arr=[], note=''),
 'Lake Rathetear': dict(pos=(146,398), off=(36,-6), dia=[('Kelinar',1),('Fort Alliance',1)],
    arr=[], note='EQOA "Lake Rathe" = same lake.'),
 'Cazic Thule': dict(pos=(56,459), off=(-52,44), dia=[],
    arr=[('Stone Watchers','S'),('Dinbak','SE')], note='EQOA "Cazic Thule" = same name.'),
}

ODUS = {
 'Toxxulia Forest': dict(pos=(96,118), off=(-88,26), dia=[('South Toxxulia',2),('East Toxxulia',2)],
    arr=[('West Toxxulia','NW'),('Old Arcadin','NE'),('Grand Plateau','N')],
    note='EQ1 covers South Toxxulia + a strip of North. Arcadin = pre-rebuild Erudin -> lore signpost. East Plateau dropped (not in game).'),
 'Stonebrunt Mtns': dict(pos=(150,150), off=(40,26), dia=[],
    arr=[('North Barren Coast','NE'),('South Barren Coast','SE'),('Cape Dreg','SE'),('The Vastly Deep','E')],
    note='*** Stonebrunt runs down the MIDDLE of Odus - the Barren Coast and Vasty Deep all lie EAST of its in-game footprint, so they are all signposts, not on-map labels.'),
 'Erudin': dict(pos=(112,40), off=(26,-30), dia=[],
    arr=[('Old Arcadin','SE'),('Grand Plateau','NW')],
    note='Erudin IS Arcadin rebuilt - the SE signpost mirrors the NE one on Toxxulia.'),
 'Kerra Isle': dict(pos=(40,118), off=(-38,34), dia=[], arr=[('Abysmal Sea','W')],
    note='Your own POI layer kept untouched; only an "on the way" sea signpost added.'),
 'Paineel': dict(pos=(78,168), off=(-70,30), dia=[], arr=[('Abysmal Sea','W')],
    note='Sea signpost gives a sense of what lies beyond the western cliffs.'),
 'The Warrens': dict(pos=(96,196), off=(24,30), dia=[], arr=[('Gulf of Uzun','S')],
    note='Southward signpost toward the gulf.'),
 "Erud's Crossing": dict(pos=(196,60), off=(26,30), dia=[], arr=[('The Vastly Deep','SE')],
    note='EQOA name matches; one open-water signpost.'),
}

VIO=(150,80,160); GRN=(28,120,58); RED=(200,35,35); INK=(24,22,20)

def fnt(s,b=True):
    try: return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf",s)
    except: return ImageFont.load_default()

def render(src, assign, out, scale, legend_title, extra_notes):
    base=Image.open(src).convert('RGBA')
    W,H=base.size
    base=base.resize((int(W*scale),int(H*scale)), Image.LANCZOS); W,H=base.size
    base=Image.alpha_composite(base, Image.new('RGBA',(W,H),(252,250,245,140)))
    LEG=470
    cv=Image.new('RGBA',(W+LEG,H),(22,20,18,255)); cv.paste(base,(0,0))
    d=ImageDraw.Draw(cv,'RGBA')
    def S(x,y): return x*scale, y*scale
    # ---- pre-compute label block rects and resolve collisions ----
    def blk_size(z):
        w=0
        for nm,tier in z['dia']: w=max(w, 16+len(nm)*(6.6 if tier>=2 else 6.0))
        for nm,dr in z['arr']: w=max(w, 16+len(f'{nm} ({dr})')*5.9)
        w=max(w, len('')*1)
        h=19+15*(len(z['dia'])+len(z['arr']))
        return w,h
    placed=[]
    blocks={}
    for zn,z in assign.items():
        if not (z['dia'] or z['arr']):
            blocks[zn]=None; continue
        w,h=blk_size(z); w=max(w, len(zn)*8.2+8)
        bx,by=S(z['pos'][0]+z['off'][0], z['pos'][1]+z['off'][1])
        bx=min(max(bx,4), W-w-6); by=max(by,4)
        for _ in range(200):
            r=(bx,by,bx+w,by+h); hit=False
            for pr in placed:
                if not (r[2]<pr[0]-6 or r[0]>pr[2]+6 or r[3]<pr[1]-4 or r[1]>pr[3]+4):
                    by=pr[3]+8; hit=True; break
            if not hit: break
        if by+h>H-6: by=max(4,H-h-6)
        placed.append((bx,by,bx+w,by+h)); blocks[zn]=(bx,by)
    # zone boxes + label blocks
    for zn,z in assign.items():
        zx,zy=S(*z['pos'])
        has=z['dia'] or z['arr']
        col=RED if z['note'].startswith('***') else (GRN if z['dia'] else VIO)
        if not has: col=(130,125,120)
        # ring the zone box
        d.ellipse([zx-16,zy-11,zx+16,zy+11], outline=col+(255,), width=3)
        if blocks.get(zn) is None:
            continue
        bx,by=blocks[zn]
        # leader line
        d.line([zx,zy,bx+6,by+8], fill=col+(170,), width=2)
        # header
        d.text((bx,by),zn,font=fnt(15),fill=col+(255,),stroke_width=3,stroke_fill=(255,255,255,235))
        yy=by+19
        for nm,tier in z['dia']:
            ry=4+tier*2; rx=ry*0.55
            cx0=bx+7
            d.polygon([(cx0,yy+7-ry),(cx0+rx,yy+7),(cx0,yy+7+ry),(cx0-rx,yy+7)],outline=GRN+(255,),width=2)
            d.text((bx+16,yy),nm,font=fnt(12 if tier>=2 else 11,tier>=3),fill=INK+(255,),
                   stroke_width=3,stroke_fill=(255,255,255,235)); yy+=15
        for nm,dr in z['arr']:
            ax=bx+7
            d.line([(ax+6,yy+7),(ax-6,yy+7)],fill=VIO+(255,),width=2)
            d.line([(ax-6,yy+7),(ax-1,yy+3)],fill=VIO+(255,),width=2)
            d.line([(ax-6,yy+7),(ax-1,yy+11)],fill=VIO+(255,),width=2)
            d.text((bx+16,yy),f'{nm} ({dr})',font=fnt(11,False),fill=VIO+(255,),
                   stroke_width=3,stroke_fill=(255,255,255,235)); yy+=15
        if z['note'].startswith('***'):
            d.ellipse([zx-24,zy-18,zx+24,zy+18], outline=RED+(255,), width=2)
    # legend
    lx=W+16; d.text((lx,18),legend_title,font=fnt(17),fill=(242,235,216,255))
    y=52
    d.polygon([(lx+8,y),(lx+15,y+10),(lx+8,y+20),(lx+1,y+10)],outline=GRN+(255,),width=3)
    d.text((lx+26,y+2),'diamond = ON the zone map',font=fnt(14),fill=GRN+(255,)); y+=20
    d.text((lx+26,y+1),'size = large / medium / small tier',font=fnt(11,False),fill=(190,205,190,255)); y+=26
    d.line([(lx+16,y+9),(lx,y+9)],fill=VIO+(255,),width=3)
    d.line([(lx,y+9),(lx+7,y+3)],fill=VIO+(255,),width=3); d.line([(lx,y+9),(lx+7,y+15)],fill=VIO+(255,),width=3)
    d.text((lx+26,y+2),'arrow = margin signpost',font=fnt(14),fill=VIO+(255,)); y+=20
    d.text((lx+26,y+1),'(EQOA area with no EQ1 zone)',font=fnt(11,False),fill=(210,195,215,255)); y+=26
    d.ellipse([lx,y,lx+18,y+18],outline=RED+(255,),width=3)
    d.text((lx+26,y+2),'boundary = edge of EQOA world',font=fnt(14),fill=RED+(255,)); y+=32
    for t in extra_notes:
        d.text((lx,y),t,font=fnt(12,False),fill=(206,199,183,255)); y+=17
    cv.convert('RGB').save(out)
    nd=sum(len(z['dia']) for z in assign.values()); na=sum(len(z['arr']) for z in assign.values())
    print(f"{out}: {nd} diamonds, {na} arrows across {len(assign)} zones")
    return nd,na

if __name__=='__main__':
    a=render('/mnt/user-data/uploads/1786213618051_image.png', ANT,
        '/mnt/user-data/outputs/_alignment_antonica_eq1.png', 2.9,
        'Antonica — EQOA labels keyed to EQ1 zones',
        ['Proposed placement for the _3 easter-egg layer.','',
         'KEY FINDING: Lavastorm was NOT an EQOA zone —','it sits in the NE mountain boundary band.','-> boundary marker + signposts only.','',
         "Klik'Anon is the EQOA gnome city (EQ1's Ak'Anon","is its Faydwer cousin — different place).",'',
         'Diamonds are drawn 25% smaller than the last','pass so they can stay toggled on full-time.'])
    o=render('/mnt/user-data/uploads/1786213689572_image.png', ODUS,
        '/mnt/user-data/outputs/_alignment_odus_eq1.png', 5.2,
        'Odus — EQOA labels keyed to EQ1 zones',
        ['Odus WAS in EQOA (only Faydwer was not).','',
         'Arcadin = pre-rebuild Erudin -> lore signpost.','East Plateau dropped: not in the game.','',
         'Kerra Isle keeps your own POI layer untouched.'])
    print("TOTALS:", a[0]+o[0], "diamonds,", a[1]+o[1], "arrows")
