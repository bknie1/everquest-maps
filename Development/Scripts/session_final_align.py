"""Age of Adventure — EQOA POI alignment reference, built from the SHIPPED _3 layers."""
from PIL import Image, ImageDraw, ImageFont
import glob, os, re
O='/mnt/user-data/outputs'
base=Image.open('/mnt/user-data/uploads/1786163660342_image.png').convert('RGBA')
W,H=base.size; SC=1.45
base=base.resize((int(W*SC),int(H*SC)),Image.LANCZOS); W,H=base.size
base=Image.alpha_composite(base,Image.new('RGBA',(W,H),(252,250,245,150)))
LEG=470
cv=Image.new('RGBA',(W+LEG,H),(20,18,16,255)); cv.paste(base,(0,0)); d=ImageDraw.Draw(cv,'RGBA')
def fnt(s,b=True):
    try: return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf",s)
    except: return ImageFont.load_default()
import importlib.util
spec=importlib.util.spec_from_file_location("ep","/home/claude/work/eqoa_pos.py")
ep=importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)

# read what actually shipped
dia=set(); arr=set()
for f in sorted(glob.glob(f'{O}/*_3.txt')):
    if os.path.getsize(f)==0: continue
    for l in open(f,'rb').read().decode('utf-8','replace').split('\r\n'):
        if l.startswith('P') and '150, 90, 150' in l:
            nm=l.split(', ')[-1].strip().replace('_',' ')
            if nm.startswith('To '): arr.add(nm[3:])
            elif 'Boundary' not in nm: dia.add(nm)
def key(n):
    n=re.sub(r'^(Ruins of|Old) ','',n)
    return n
GRN=(26,124,56); VIO=(150,80,160); RED=(200,35,35)
plotted=0
for nm in sorted(arr|dia):
    k=key(nm)
    pos=ep.EQOA_POS.get(k) or ep.EQOA_POS.get(nm)
    if not pos: continue
    x,y=pos[0]*SC,pos[1]*SC
    isd = nm in dia
    col = GRN if isd else VIO
    if isd:
        d.polygon([(x,y-11),(x+6,y),(x,y+11),(x-6,y)],outline=col+(255,),width=3)
    else:
        d.line([(x+9,y),(x-9,y)],fill=col+(255,),width=3)
        d.line([(x-9,y),(x-2,y-5)],fill=col+(255,),width=3)
        d.line([(x-9,y),(x-2,y+5)],fill=col+(255,),width=3)
    d.text((x+13,y-6),nm,font=fnt(11),fill=(18,16,14,255),stroke_width=3,stroke_fill=(255,255,255,238))
    plotted+=1
# boundary
bx,by=ep.EQOA_POS['NE Mountain Boundary']
bx*=SC; by*=SC
for r in (10,14): d.ellipse([bx-r,by-r,bx+r,by+r],outline=RED+(255,),width=2)
d.text((bx+18,by-6),'Age of Adventure boundary',font=fnt(11),fill=RED+(255,),
       stroke_width=3,stroke_fill=(255,255,255,238))

lx=W+16
d.text((lx,20),'Age of Adventure',font=fnt(28),fill=(242,232,208,255))
d.text((lx,56),'EQOA POI alignment — as shipped',font=fnt(17),fill=(196,186,166,255))
y=100
d.polygon([(lx+8,y),(lx+15,y+11),(lx+8,y+22),(lx+1,y+11)],outline=GRN+(255,),width=3)
d.text((lx+28,y+3),f'on-map diamond  ({len(dia)})',font=fnt(15),fill=GRN+(255,)); y+=22
d.text((lx+28,y+2),'something is actually there:',font=fnt(11,False),fill=(190,205,190,255)); y+=15
d.text((lx+28,y+2),'terrain, or a real EQ1 feature',font=fnt(11,False),fill=(190,205,190,255)); y+=30
d.line([(lx+16,y+10),(lx,y+10)],fill=VIO+(255,),width=3)
d.line([(lx,y+10),(lx+7,y+4)],fill=VIO+(255,),width=3); d.line([(lx,y+10),(lx+7,y+16)],fill=VIO+(255,),width=3)
d.text((lx+28,y+3),f'margin signpost  ({len(arr)})',font=fnt(15),fill=VIO+(255,)); y+=22
d.text((lx+28,y+2),'off-map: point, don\'t place',font=fnt(11,False),fill=(210,195,215,255)); y+=30
for r in (8,12): d.ellipse([lx+2-r+10,y+2-r+10,lx+2+r-10+10,y+2+r-10+10],outline=RED+(255,),width=2)
d.ellipse([lx,y,lx+20,y+20],outline=RED+(255,),width=2)
d.text((lx+28,y+3),'edge of the EQOA world',font=fnt(15),fill=RED+(255,)); y+=34
for t in ['Rules that decide the fate of a name:','',
          '1. Terrain that persists (plains, valleys,','   hills, canyons, coasts) -> diamond.',
          '2. A real EQ1 feature at the spot -> diamond,','   snapped onto that feature.',
          '3. Everything else -> margin signpost,','   sized by distance (near = large).',
          '4. Not in the game at all -> dropped.','',
          'Names verified against the canonical zone','index at wiki.eqoa.live.','',
          'Lavastorm sits in the NE mountain boundary:','it was never an EQOA zone, so it carries','signposts only.']:
    d.text((lx,y),t,font=fnt(12,False),fill=(202,194,178,255)); y+=17
cv.convert('RGB').save(f'{O}/_age_of_adventure_alignment.png')
print(f"alignment reference: {plotted} names plotted ({len(dia)} diamonds, {len(arr)} signposts)")
