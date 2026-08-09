"""Neriak decoration, built on the EXISTING toolkit — not a bespoke one-off.

Uses eqmap_toolkit (Canvas / frame / grid / title / compass / web_corner /
spider_motif) and bb_decor.shade_border, exactly as Najena and Blackburrow do.
The toolkit's 'dark' theme is literally commented "neriak/nektulos".

Title follows the Freeport pattern: a big stylised NERIAK with the quarter as
the small subword, via title(..., subword=...).
"""
import sys, math
sys.path.insert(0, '/home/claude/work/maps_repo/Maps Repo/Developer Scripts')
sys.path.insert(0, '/home/claude/work')
from eqmap_toolkit import (Canvas, frame, grid, title, compass, web_corner,
                            spider_motif, _word, _adv)

def subtitle_bottom(cv, text, color, height, gap=None, shadow=None):
    """Quarter name set in the BOTTOM margin - the long names crowd the heading."""
    gap = gap if gap is not None else height*0.30
    cw = height*0.66
    w = sum(_adv(c, cw) for c in text) + (len(text)-1)*gap
    avail = (cv.bx1 - cv.bx0) - 420
    if w > avail:
        sc_ = avail/w; cw *= sc_; height *= sc_; gap *= sc_; w = avail
    ox = (cv.minx + cv.maxx)/2 - w/2
    oy = cv.by1 - max(110, cv.pad*0.62)
    fy = lambda y: 2*oy + height - y
    _, segs = _word(text, ox, oy, cw, height, gap)
    for (a, b, c, d) in segs:
        cv.add(a, fy(b), c, fy(d), color)
        if shadow: cv.add(a+6, fy(b)+7, c+6, fy(d)+7, shadow)
    cv.add(ox-24, fy(oy-34), ox+w+24, fy(oy-34), shadow or color)
    cv.add(ox-24, fy(oy+height+30), ox+w+24, fy(oy+height+30), shadow or color)
import bb_decor
import darkelf as DE

O = '/mnt/user-data/outputs'

# the toolkit's own 'dark' theme (neriak/nektulos)
T = dict(OUT=(50,40,64), INN=(120,90,150), GC=(120,110,130), TC=(90,60,120), SH=(120,90,150))
SHADE = (108, 96, 128)      # margin hatch — reads as cavern rock outside the city

ZONES = {          # zone: (title, subtitle, LEFT scene, RIGHT scene)
    'neriaka': ('NERIAK', 'FOREIGN QUARTER', 'gate',   'graffiti'),  # gate is west in game
    'neriakb': ('NERIAK', 'COMMONS',         'cavern', 'graffiti'),  # the falls
    'neriakc': ('NERIAK', 'THIRD GATE',      'lodge+temple', 'bastion+library'),
}

def parse(path):
    L=[]
    for l in open(path, encoding='utf-8', errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(',')
            L.append((float(f[0]),float(f[1]),float(f[3]),float(f[4])))
    return L

for z,(main, sub, accent, right) in ZONES.items():
    B = parse(f'{O}/{z}.txt')
    xs=[v for a,b,c,d in B for v in (a,c)]; ys=[v for a,b,c,d in B for v in (b,d)]
    MINX,MAXX,MINY,MAXY = min(xs),max(xs),min(ys),max(ys)
    span = max(MAXX-MINX, MAXY-MINY)
    PAD  = max(200, int(span*0.28))          # deep margin: room for a big arched heading
    INSET= int(span*0.055); CLEAR=int(span*0.06)
    cv = Canvas((MINX,MAXX,MINY,MAXY), PAD)

    # ---- 1. shaded margin: the rock outside the city ----
    bb_decor.shade_border(cv, INSET, SHADE, step=max(9,int(span*0.011)))

    # ---- 2. grid over the content ----
    STEP = max(60, round(span/8/20)*20)
    gx = math.ceil(MINX/STEP)*STEP
    while gx < MAXX: cv.add(gx, MINY, gx, MAXY, T['GC']); gx += STEP
    gy = math.ceil(MINY/STEP)*STEP
    while gy < MAXY: cv.add(MINX, gy, MAXX, gy, T['GC']); gy += STEP
    for a,b,c,d in [(MINX,MINY,MAXX,MINY),(MINX,MAXY,MAXX,MAXY),
                    (MINX,MINY,MINX,MAXY),(MAXX,MINY,MAXX,MAXY)]:
        cv.add(a,b,c,d,T['GC'])

    # ---- 3. frame ----
    frame(cv, outer=T['OUT'], inner=T['INN'],
          step=max(120,int(span*0.06)), depth=max(30,int(span*0.02)), inset=INSET)

    # ---- 4. title: big NERIAK with the quarter as subword (Freeport pattern) ----
    th = int(PAD*0.40)                        # fits inside the top margin band
    title(cv, main, T['TC'], shadow=T['SH'], height=th, arc=th*0.20)
    subtitle_bottom(cv, sub, T['OUT'], height=max(70, int(span*0.042)), shadow=T['INN'])

    # ---- 5. compass, bottom-left ----
    TIN = INSET + CLEAR
    SX0, SY1 = cv.bx0+TIN, cv.by1-TIN
    CR = max(90, int(span*0.05)); LR = CR*1.25
    compass(cv, SX0+LR, SY1-LR, CR, ring=(T['OUT'],T['INN']), rose=(T['INN'],T['GC']),
            label=T['OUT'], n_label=T['TC'], arrow=T['TC'])

    # ---- 6. Teir'Dal touches: webs in the corners, a spider ----
    R = max(120, int(span*0.085))
    web_corner(cv, cv.bx0+INSET, cv.by0+INSET,  1,  1, color=T['GC'], reach=R)
    web_corner(cv, cv.bx1-INSET, cv.by0+INSET, -1,  1, color=T['GC'], reach=R)
    web_corner(cv, cv.bx0+INSET, cv.by1-INSET,  1, -1, color=T['GC'], reach=R)
    spider_motif(cv, cv.bx1-INSET-R*0.45, cv.by1-INSET-R*0.45, max(30,int(span*0.022)),
                 T['OUT'], T['INN'])

    # ---- 7. the gate sketch, TOP-RIGHT margin ----
    # ---- 7. the scenes, LEFT margin (level with where each stands in game) ----
    lb_w = MINX - (cv.bx0 + INSET)
    ax = cv.bx0 + INSET + lb_w*0.5
    segs=[]
    if accent == 'gate':
        gw = lb_w*0.88; gh = gw/1.9
        segs = DE.arched_gate(ax, MINY + R*0.85 + gh*1.2, gw, gh, T['OUT'])
    elif accent == 'cavern':
        gw = lb_w*0.92; gh = gw*0.72
        segs = DE.commons_scene(ax, MINY + R*0.85 + gh*1.15, gw, gh, T['OUT'])
    elif accent == 'lodge+temple':
        # each sketch sits level with the building it depicts: the Lodge keeps
        # hall in the north, Innoruuk's shrine stands away to the south-west
        gw = lb_w*0.92
        lh = gw*0.60
        segs += DE.lodge_of_the_dead(ax, MINY + R*0.85 + lh*1.15, gw, lh, T['OUT'])
        th_ = gw*0.62
        temple_y = (SY1 - LR) - CR*2.15          # clear above the compass
        segs += DE.innoruuk_temple(ax, temple_y, gw, th_, T['OUT'])
    else:
        gw = lb_w*0.92; gh = gw*0.66
        segs = DE.innoruuk_temple(ax, MINY + R*0.85 + gh*1.2, gw, gh, T['OUT'])
    for (x1,y1,x2,y2,ink) in segs:
        cv.add(x1, y1, x2, y2, ink)

    # ---- 8. right margin ----
    rb_w = (cv.bx1 - INSET) - MAXX
    rx = MAXX + rb_w*0.5
    if right == 'bastion+library':
        # spaced down the right margin: bastion upper third (it guards the
        # north-east), library below it with clear air between the two
        H_ = MAXY - MINY
        bw = rb_w*0.92; bh = bw*0.70
        rsegs  = DE.bastion_gate(rx, MINY + H_*0.20 + bh*0.5, bw, bh, T['OUT'])
        lw = rb_w*0.92; lh = lw*0.56
        rsegs += DE.library_facade(rx, MINY + H_*0.58 + lh*0.5, lw, lh, T['OUT'])
    elif right == 'library':
        lw = rb_w*0.92; lh = lw*0.58
        rsegs = DE.library_facade(rx, (MINY+MAXY)*0.5 + lh*0.5, lw, lh, T['OUT'])
    else:
        gw2 = rb_w*0.86; gh2 = gw2*0.62
        rsegs = DE.rune_graffiti(rx, (MINY+MAXY)*0.5, gw2, gh2, seed=abs(hash(z)) % 97)
    for (x1,y1,x2,y2,ink) in rsegs:
        cv.add(x1, y1, x2, y2, ink)

    # ---- 9. water: shade the pools, knock out the bridges ----
    water=[(a,b,c,d) for (a,b,c,d,ink) in
           [(float(f[0]),float(f[1]),float(f[3]),float(f[4]),(int(f[6]),int(f[7]),int(f[8])))
            for f in (l[2:].split(',') for l in open(f'{O}/{z}.txt',encoding='utf-8',errors='replace')
                      if l.startswith('L'))]
           if ink == DE.PALETTE['arcane']]
    if water:
        struct=[]
        for l in open(f'{O}/{z}.txt',encoding='utf-8',errors='replace'):
            if l.startswith('L'):
                f=l[2:].split(',')
                ink2=(int(f[6]),int(f[7]),int(f[8]))
                if ink2 in (DE.PALETTE['obsidian'], DE.PALETTE['stone'],
                            DE.PALETTE['basalt'], DE.PALETTE['lamp']):
                    struct.append((float(f[0]),float(f[1]),float(f[3]),float(f[4])))
        fill = DE.water_flood(water, struct,
                              cell=max(2.5, span*0.0026),
                              row=max(2.5, span*0.0026),   # tight rows = solid water
                              clearance=4, solid=True, corridor=34.0)
        raw_n = len(fill)
        for (x1,y1,x2,y2,ink) in fill: cv.add(x1,y1,x2,y2,ink)
        print(f"   {z}: water {raw_n} strokes by flood fill "
              f"(bounded by {len(struct)} structural lines + {len(water)} shoreline)")

    cv.write(f'{O}/{z}_2.txt')
    print(f"{z}_2: L={len(cv.L)}  '{main}' / '{sub}'  left={accent}  right={right}")
    b=open(f'{O}/{z}_2.txt','rb').read()
    assert sum(1 for i,ch in enumerate(b) if ch==10 and (i==0 or b[i-1]!=13))==0
print("CRLF OK — built on the toolkit, not a one-off")
