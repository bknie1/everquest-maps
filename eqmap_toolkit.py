"""
eqmap_toolkit.py  -- reusable tooling for EQ Legends custom map decoration (_2) files.

Design pattern (think of the map as a spreadsheet):
  * The CONTENT is the actual zone geometry, occupying the center grid.
  * A uniform PADDING frame surrounds the content on all four sides (the "margin").
  * The margin is addressed as CELLS:
        - Row 0 (top heading, full width) .............. TITLE
        - The left/right margin columns hold stacked CELLS (aligned to grid rows)
          for the COMPASS (2nd row, best-fit side) and DOODLES (row of their landmark).
  * The COMPASS and DOODLES are drawn LAST (on top of everything else).

Everything writes EQ-native L/P lines with CRLF endings. Y increases DOWNWARD in game,
so titles are drawn flipped (handled in `title`).

Modular pieces:
    frame(...)     - the padded border ("frame")
    grid(...)      - grid overlay, clipped to content
    title(...)     - full-width heading, styleable
    compass(...)   - ring + rose + center motif, styleable
    doodles: dead_tree / volcano / wizard_gate  (side-view "cartographer" doodles)
    cell layout: Canvas.margin_x / Canvas.row_y  for snapping items to cells
"""
import numpy as np, random, math

CRLF = "\r\n"

# ---------------------------------------------------------------- stick font
LETTERS = {
 'A':[[(0,0),(0.5,1),(1,0)],[(0.25,0.4),(0.75,0.4)]],
 'B':[[(0,0),(0,1),(0.7,1),(0.9,0.8),(0.7,0.55),(0,0.55)],[(0,0.55),(0.75,0.55),(0.95,0.3),(0.7,0),(0,0)]],
 'C':[[(0.95,0.8),(0.7,1),(0.25,1),(0,0.7),(0,0.3),(0.25,0),(0.7,0),(0.95,0.2)]],
 'D':[[(0,0),(0,1),(0.6,1),(0.95,0.7),(0.95,0.3),(0.6,0),(0,0)]],
 'E':[[(1,1),(0,1),(0,0),(1,0)],[(0,0.5),(0.7,0.5)]],
 'F':[[(0,0),(0,1),(1,1)],[(0,0.55),(0.7,0.55)]],
 'G':[[(0.95,0.8),(0.7,1),(0.25,1),(0,0.7),(0,0.3),(0.25,0),(0.7,0),(0.95,0.25),(0.95,0.45),(0.6,0.45)]],
 'H':[[(0,0),(0,1)],[(1,0),(1,1)],[(0,0.5),(1,0.5)]],
 'I':[[(0.5,0),(0.5,1)],[(0.2,1),(0.8,1)],[(0.2,0),(0.8,0)]],
 'J':[[(0.8,1),(0.8,0.2),(0.6,0),(0.3,0),(0.1,0.2)]],
 'K':[[(0,0),(0,1)],[(0,0.45),(0.85,1)],[(0.25,0.55),(0.9,0)]],
 'L':[[(0,1),(0,0),(0.8,0)]],
 'M':[[(0,0),(0,1),(0.5,0.45),(1,1),(1,0)]],
 'N':[[(0,0),(0,1),(1,0),(1,1)]],
 'O':[[(0.25,0),(0.75,0),(1,0.3),(1,0.7),(0.75,1),(0.25,1),(0,0.7),(0,0.3),(0.25,0)]],
 'P':[[(0,0),(0,1),(0.7,1),(0.95,0.8),(0.7,0.55),(0,0.55)]],
 'Q':[[(0.25,0),(0.75,0),(1,0.3),(1,0.7),(0.75,1),(0.25,1),(0,0.7),(0,0.3),(0.25,0)],[(0.6,0.3),(1,-0.05)]],
 'R':[[(0,0),(0,1),(0.7,1),(0.95,0.8),(0.7,0.55),(0,0.55)],[(0.35,0.55),(1,0)]],
 'S':[[(1,0.85),(0.8,1),(0.2,1),(0,0.82),(0,0.6),(0.2,0.5),(0.8,0.5),(1,0.38),(1,0.16),(0.8,0),(0.2,0),(0,0.16)]],
 'T':[[(0,1),(1,1)],[(0.5,1),(0.5,0)]],
 'U':[[(0,1),(0,0.2),(0.2,0),(0.8,0),(1,0.2),(1,1)]],
 'V':[[(0,1),(0.5,0),(1,1)]],
 'W':[[(0,1),(0.25,0),(0.5,0.6),(0.75,0),(1,1)]],
 'X':[[(0,0),(1,1)],[(0,1),(1,0)]],
 'Y':[[(0,1),(0.5,0.5),(1,1)],[(0.5,0.5),(0.5,0)]],
 'Z':[[(0,1),(1,1),(0,0),(1,0)]],
 ' ':[],
}

# ---------------------------------------------------------------- canvas
class Canvas:
    """Holds content bbox + padding, accumulates L/P lines, exposes the cell grid."""
    def __init__(self, content_bbox, pad, gstep=None):
        self.minx, self.maxx, self.miny, self.maxy = content_bbox
        self.pad = pad
        # default grid step ~ largest dimension / 8, min 150, rounded
        raw = max(self.maxx-self.minx, self.maxy-self.miny)/8
        self.gstep = gstep or max(150, round(raw/50)*50)
        self.L, self.P = [], []

    # --- primitives ---
    def add(self, x1, y1, x2, y2, c, z=0.0):
        self.L.append(f"L {x1:.2f}, {y1:.2f}, {z:.4f}, {x2:.2f}, {y2:.2f}, {z:.4f}, {c[0]}, {c[1]}, {c[2]}")
    def label(self, x, y, c, size, text, z=0.0):
        self.P.append(f"P {x:.2f}, {y:.2f}, {z:.4f}, {c[0]}, {c[1]}, {c[2]}, {size}, {text}")

    # --- frame geometry ---
    @property
    def bx0(self): return self.minx - self.pad
    @property
    def by0(self): return self.miny - self.pad
    @property
    def bx1(self): return self.maxx + self.pad
    @property
    def by1(self): return self.maxy + self.pad

    # --- cell layout helpers ---
    def margin_x(self, side):
        """Center x of the left/right margin column."""
        return (self.minx - self.pad*0.5) if side == 'left' else (self.maxx + self.pad*0.5)
    def row_y(self, row):
        """Center y of content row `row` (row 0 = first row below the top edge)."""
        return self.miny + (row + 0.5) * self.gstep
    def snap_row(self, y):
        """Center y of the content row that contains world-y `y` (for landmark alignment)."""
        row = int((y - self.miny) // self.gstep)
        return self.row_y(row)

    def write(self, path):
        open(path, 'w', newline='').write(CRLF.join(self.L + self.P) + CRLF)


# ---------------------------------------------------------------- FRAME
def frame(cv, outer, inner, step=100, depth=60, inset=45, corner=None):
    """Padded two-tone jagged border. `corner(cv,x,y,sx,sy)` optionally decorates each corner."""
    def jag(x0, y0, x1, y1, st, dp, c):
        dx, dy = x1-x0, y1-y0; L = (dx*dx+dy*dy)**.5; ux, uy = dx/L, dy/L; nx, ny = -uy, ux
        n = max(2, int(L/st))
        p = [(x0+dx*i/n + (nx*random.uniform(.35,1)*dp if i % 2 else 0),
              y0+dy*i/n + (ny*random.uniform(.35,1)*dp if i % 2 else 0)) for i in range(n+1)]
        for i in range(len(p)-1): cv.add(*p[i], *p[i+1], c)
    bx0, by0, bx1, by1 = cv.bx0, cv.by0, cv.bx1, cv.by1
    for e in [(bx0,by0,bx1,by0),(bx1,by0,bx1,by1),(bx1,by1,bx0,by1),(bx0,by1,bx0,by0)]:
        jag(*e, step, depth, outer)
    io = inset
    for e in [(bx0+io,by0+io,bx1-io,by0+io),(bx1-io,by0+io,bx1-io,by1-io),
              (bx1-io,by1-io,bx0+io,by1-io),(bx0+io,by1-io,bx0+io,by0+io)]:
        jag(*e, step*1.3, depth*0.55, inner)
    if corner:
        for (cx, cy, sx, sy) in [(bx0+io,by0+io,1,1),(bx1-io,by0+io,-1,1),
                                 (bx0+io,by1-io,1,-1),(bx1-io,by1-io,-1,-1)]:
            corner(cv, cx, cy, sx, sy)


# ---------------------------------------------------------------- GRID
def grid(cv, color, step=None):
    """Grid overlay clipped to the content footprint (drawn under other decoration)."""
    step = step or cv.gstep
    x = np.ceil(cv.minx/step)*step
    while x < cv.maxx: cv.add(x, cv.miny, x, cv.maxy, color); x += step
    y = np.ceil(cv.miny/step)*step
    while y < cv.maxy: cv.add(cv.minx, y, cv.maxx, y, color); y += step


# ---------------------------------------------------------------- TITLE
def _word(text, ox, oy, cw, ch, gap):
    segs = []; x = ox
    for ch_ in text:
        for poly in LETTERS.get(ch_, []):
            for i in range(len(poly)-1):
                ax, ay = poly[i]; bx, by = poly[i+1]
                segs.append((x+ax*cw, oy+ay*ch, x+bx*cw, oy+by*ch))
        x += cw + gap
    return x, segs   # returns end-x and the segments

def title(cv, text, color, shadow=None, height=270, gap=44, framed=True,
          subword=None, subcolor=None):
    """Full-width heading in the top margin (row 0). Auto-scales to fit, drawn flipped.
       Optional `subword` (e.g. 'EAST') is rendered small to the left of `text`."""
    cw = height*0.66
    dcw, dch, dgap, subgap = cw*0.5, height*0.5, gap*0.55, 80
    def group_w():
        w = len(text)*cw + (len(text)-1)*gap
        if subword: w += len(subword)*dcw + (len(subword)-1)*dgap + subgap
        return w
    avail = (cv.bx1 - cv.bx0) - 360
    if group_w() > avail:
        s = avail/group_w(); cw*=s; height*=s; gap*=s; dcw*=s; dch*=s; dgap*=s; subgap*=s
    grp = group_w()
    ox = (cv.minx+cv.maxx)/2 - grp/2
    oy = cv.by0 + max(120, cv.pad*0.2)
    fy = lambda y: 2*oy + height - y     # vertical flip
    x = ox
    if subword:
        _, dsegs = _word(subword, x, oy+(height-dch)/2, dcw, dch, dgap)
        for (a,b,c,d) in dsegs: cv.add(a, fy(b), c, fy(d), subcolor or color)
        x += len(subword)*dcw + (len(subword)-1)*dgap + subgap
    _, segs = _word(text, x, oy, cw, height, gap)
    for (a,b,c,d) in segs:
        cv.add(a, fy(b), c, fy(d), color)
        if shadow: cv.add(a+8, fy(b)+10, c+8, fy(d)+10, shadow)
    if framed:
        cv.add(ox-30, fy(oy-46), ox+grp+30, fy(oy-46), shadow or color)
        cv.add(ox-30, fy(oy+height+42), ox+grp+30, fy(oy+height+42), shadow or color)


# ---------------------------------------------------------------- COMPASS
def spider_motif(cv, cx, cy, s, body, legs):
    cv.add(cx, cy-s*0.5, cx, cy+s*0.7, body)
    for r in (s*0.32, s*0.55):
        p = [(cx+r*0.8*math.cos(t), cy+s*0.18+r*math.sin(t)) for t in np.linspace(0,2*math.pi,9)]
        for i in range(len(p)-1): cv.add(*p[i], *p[i+1], body)
    for si in (-1,1):
        for k in range(4):
            a = math.radians(20+k*35); ly = cy+(k-1.5)*s*0.45
            cv.add(cx+si*s*0.28, cy+(k-1.5)*s*0.33, cx+si*s*0.8*math.cos(a), ly, legs)
            cv.add(cx+si*s*0.8*math.cos(a), ly, cx+si*s*1.35*math.cos(a), ly+s*0.35, legs)

def star_motif(cv, cx, cy, s, body, legs):
    for k in range(8):
        a = math.pi/4*k; rr = s if k % 2 == 0 else s*0.4
        cv.add(cx, cy, cx+rr*math.cos(a), cy+rr*math.sin(a), body if k % 2 == 0 else legs)

def sun_motif(cv, cx, cy, s, body, legs):
    ring = [(cx+s*0.45*math.cos(t), cy+s*0.45*math.sin(t)) for t in np.linspace(0,2*math.pi,13)]
    for i in range(len(ring)-1): cv.add(*ring[i], *ring[i+1], body)
    for k in range(12):
        a = 2*math.pi*k/12; cv.add(cx+s*0.5*math.cos(a), cy+s*0.5*math.sin(a),
                                   cx+s*math.cos(a), cy+s*math.sin(a), body if k % 3 == 0 else legs)

def skull_motif(cv, cx, cy, s, body, legs):
    cr = [(cx+s*0.6*math.cos(t), cy-s*0.3+s*0.55*math.sin(t)) for t in np.linspace(math.pi,2*math.pi,10)]
    for i in range(len(cr)-1): cv.add(*cr[i], *cr[i+1], body)
    cv.add(cx-s*0.6,cy-s*0.3,cx-s*0.28,cy+s*0.5,body); cv.add(cx+s*0.6,cy-s*0.3,cx+s*0.28,cy+s*0.5,body)
    cv.add(cx-s*0.28,cy+s*0.5,cx+s*0.28,cy+s*0.5,body)
    for sx in (-1,1):
        ex = cx+sx*s*0.28
        cv.add(ex-s*0.15,cy-s*0.12,ex+s*0.15,cy-s*0.12,legs)
        cv.add(ex+s*0.15,cy-s*0.12,ex,cy+s*0.06,legs); cv.add(ex,cy+s*0.06,ex-s*0.15,cy-s*0.12,legs)

def compass(cv, cx, cy, R, ring=((95,90,100),(90,70,110)), rose=((95,90,100),(90,70,110)),
            center=None, center_colors=None, label=(90,70,110), n_label=(95,90,100),
            arrow=(95,90,100)):
    """Ring border + 8-point rose + optional center motif + N arrow + N/S/E/W labels.
       Draw compass LAST so it sits on top of all other decoration.
       `center` is a motif fn: spider_motif / star_motif / sun_motif / skull_motif."""
    for rr, c in [(R, ring[0]), (R*1.13, ring[1])]:
        rp = [(cx+rr*math.cos(t), cy+rr*math.sin(t)) for t in np.linspace(0,2*math.pi,37)]
        for i in range(len(rp)-1): cv.add(*rp[i], *rp[i+1], c)
    for k in range(8):
        a = math.pi/4*k - math.pi/2; ln = R if k % 2 == 0 else R*0.6
        cv.add(cx, cy, cx+ln*math.cos(a), cy+ln*math.sin(a), rose[0] if k % 2 == 0 else rose[1])
    if center:
        bc, lc = (center_colors or ((45,38,55),(90,70,110)))
        center(cv, cx, cy, R*0.32, bc, lc)
    cv.add(cx, cy-R*0.5, cx, cy-R*0.9, arrow)
    cv.add(cx-8, cy-R*0.8, cx, cy-R*0.94, arrow); cv.add(cx+8, cy-R*0.8, cx, cy-R*0.94, arrow)
    cv.label(cx, cy-R*1.28, n_label, 3, "N"); cv.label(cx, cy+R*1.28, label, 1, "S")
    cv.label(cx+R*1.28, cy, label, 1, "E"); cv.label(cx-R*1.28, cy, label, 1, "W")


# ---------------------------------------------------------------- DOODLES (side-view)
def _thick(cv, x1, y1, x2, y2, w, c):
    dx, dy = x2-x1, y2-y1; L = (dx*dx+dy*dy)**.5 or 1; nx, ny = -dy/L*w, dx/L*w
    cv.add(x1+nx,y1+ny,x2+nx,y2+ny,c); cv.add(x1-nx,y1-ny,x2-nx,y2-ny,c); cv.add(x1,y1,x2,y2,c)

def dead_tree(cv, cx, cy, h, color, seed_branches=(5,7)):
    _thick(cv, cx, cy, cx, cy-h, 3.2, color)
    for _ in range(random.randint(*seed_branches)):
        yb = cy-h*random.uniform(0.4,0.95); s = random.choice([-1,1]); ln = h*random.uniform(0.2,0.42)
        ex, ey = cx+s*ln*0.7, yb-ln*0.6
        _thick(cv, cx, yb, ex, ey, 2.2, color)
        _thick(cv, ex, ey, ex+s*ln*0.3, ey-ln*0.4, 1.3, color)

def volcano(cv, cx, cy, w, h, black=(38,26,22), red=(185,45,30), orange=(225,120,35)):
    pk = cy-h
    sil = [(cx-w,cy),(cx-w*0.58,cy-h*0.5),(cx-w*0.36,cy-h*0.38),(cx-w*0.22,pk),
           (cx-w*0.06,cy-h*0.8),(cx+w*0.09,cy-h*0.82),(cx+w*0.29,cy-h*0.9),
           (cx+w*0.52,cy-h*0.46),(cx+w,cy)]
    for i in range(len(sil)-1):
        cv.add(*sil[i],*sil[i+1],black); cv.add(sil[i][0],sil[i][1]+2,sil[i+1][0],sil[i+1][1]+2,black)
    cv.add(cx-w*0.22,pk,cx-w*0.06,cy-h*0.8,red); cv.add(cx-w*0.06,cy-h*0.8,cx+w*0.09,cy-h*0.82,orange)
    cv.add(cx+w*0.09,cy-h*0.82,cx+w*0.29,cy-h*0.9,red)
    for k in range(random.randint(4,6)):
        px = cx+random.uniform(-w*0.34,w*0.34); py = cy-h*random.uniform(0.72,0.9)
        col = red if k % 2 == 0 else orange
        for _ in range(random.randint(3,5)):
            nx = px+random.uniform(-w*0.12,w*0.12); ny = py+h*random.uniform(0.12,0.18)
            if ny > cy: break
            cv.add(px,py,nx,ny,col); cv.add(px+2,py,nx+2,ny,col); px, py = nx, ny

def wizard_gate(cv, cx, cy, w, h, stone=(120,116,124), dark=(60,58,64), portal=(150,95,185)):
    """Pseudo-3D truncated pyramid (frustum with cut-off plateau top) + portal swirl."""
    tw = w*0.46; dep = w*0.42; drop = dep*0.55           # top half-width; iso depth/rise
    bl,br = (cx-w,cy),(cx+w,cy); tl,tr = (cx-tw,cy-h),(cx+tw,cy-h)     # front face
    for a,b in [(bl,br),(br,tr),(tr,tl),(tl,bl)]: cv.add(*a,*b,stone)
    br2,tr2 = (br[0]+dep,br[1]-drop),(tr[0]+dep,tr[1]-drop)           # right side face
    for a,b in [(br,br2),(br2,tr2),(tr2,tr)]: cv.add(*a,*b,stone)
    tl2 = (tl[0]+dep,tl[1]-drop)                                      # plateau top
    for a,b in [(tl,tl2),(tl2,tr2)]: cv.add(*a,*b,stone)
    for i in (1,2):                                                   # stone courses (front)
        t = i/3; lx = cx-w+(tw-w)*t*0+(-w+ (w-tw))*0
        yy = cy-h*t; wl = w+(tw-w)*t
        cv.add(cx-wl,yy,cx+wl,yy,stone)
    nsteps = 8; sw = w*0.30; sh = h                                  # steps all the way to the plateau
    topw = tw*0.55
    for i in range(nsteps+1):
        t = i/nsteps; yy = cy - sh*t; ww = sw + (topw-sw)*t
        cv.add(cx-ww, yy, cx+ww, yy, stone)                          # tread
    cv.add(cx-sw, cy, cx-topw, cy-sh, stone)                         # staircase sides
    cv.add(cx+sw, cy, cx+topw, cy-sh, stone)
    ptx, pty = cx+dep*0.5, cy-h-drop*0.5                              # portal swirl on plateau
    for k in range(20):
        a = k*0.6; r = w*0.42*(1-k/22)
        cv.add(ptx+r*math.cos(a),pty-r*0.5*math.sin(a),
               ptx+(r-2)*math.cos(a+0.6),pty-(r-2)*0.5*math.sin(a+0.6),portal)

def web_corner(cv, cx, cy, sx, sy, color=(120,115,125), reach=340):
    for r in (reach*0.35, reach*0.65, reach):
        cv.add(cx, cy+sy*r, cx+sx*r*0.7, cy+sy*r*0.7, color)
        cv.add(cx+sx*r, cy, cx+sx*r*0.7, cy+sy*r*0.7, color)
    for k in range(4):
        cv.add(cx, cy, cx+sx*reach*(k/3), cy+sy*reach*(1-k/3), color)


# ================================================================ DOODLE LIBRARY
# Faithful ports of the doodles built across this atlas. Each takes a Canvas + center
# + size and optional theme colors, so they can be dropped in any zone / any cell.

def oak_tree(cv, cx, cy, r, bark=(110,80,50), leaf=(90,120,70)):
    """Round leafy tree -- trunk + blobby canopy (Qeynos / Surefall)."""
    cv.add(cx, cy, cx, cy-r*0.5, bark)
    n = random.randint(9, 11)
    pts = [(cx + r*random.uniform(0.85,1.12)*math.cos(2*math.pi*k/n),
            cy - r*0.7 + r*random.uniform(0.85,1.12)*math.sin(2*math.pi*k/n)) for k in range(n)]
    for i in range(n): cv.add(*pts[i], *pts[(i+1) % n], leaf)

def acacia_tree(cv, cx, cy, h, trunk=(120,88,52), canopy=(120,120,62), edge=(150,145,80)):
    """Flat-topped savanna acacia (Commonlands)."""
    _thick(cv, cx, cy, cx, cy-h, 3, trunk)
    ct = cy - h
    cv.add(cx-h*0.5, ct, cx+h*0.5, ct, canopy); cv.add(cx-h*0.5, ct-6, cx+h*0.5, ct-6, edge)
    for dx in np.linspace(-0.45, 0.45, 6): cv.add(cx+dx*h*0.9, ct, cx+dx*h*0.7, ct-h*0.18, canopy)
    _thick(cv, cx, cy-h*0.55, cx-h*0.3, ct, 1.5, trunk); _thick(cv, cx, cy-h*0.55, cx+h*0.3, ct, 1.5, trunk)

def pine_tree(cv, cx, cy, h, color=(70,95,70), trunk=(90,70,50)):
    """Layered conifer/pine -- stacked triangular tiers (generic forest)."""
    _thick(cv, cx, cy, cx, cy-h*0.2, 2, trunk)
    tiers = 3
    for i in range(tiers):
        t0 = i/tiers; t1 = (i+1)/tiers
        wy0 = cy - h*0.2 - h*0.8*t0; wy1 = cy - h*0.2 - h*0.8*t1
        w0 = h*0.34*(1-t0*0.7)
        cv.add(cx-w0, wy0, cx, wy1, color); cv.add(cx+w0, wy0, cx, wy1, color); cv.add(cx-w0, wy0, cx+w0, wy0, color)

def grass_tuft(cv, cx, cy, s, color=(150,145,80), up=1):
    """Small grass / brush clump (Commonlands savanna)."""
    for dx in (-1, 0, 1): cv.add(cx+dx*s*0.4, cy, cx+dx*s*0.7, cy-up*s, color)

def spike_pillar(cv, cx, cy, h, w, lit=(120,100,90), shadow=(90,70,60), facet=(140,120,110)):
    """Rocky spike / pillar with lit + shadow faces (Rathe Mountains)."""
    cv.add(cx-w, cy, cx, cy-h, lit); cv.add(cx, cy-h, cx+w, cy, shadow)
    cv.add(cx-w*0.35, cy-h*0.25, cx, cy-h, facet)

def froglok_tent(cv, cx, cy, w, h, tan=(180,150,110), brown=(120,85,45), beam=(90,70,50)):
    """Cone tent with center beam + pennant (Rathe froglok camp)."""
    cv.add(cx-w, cy, cx, cy-h, tan); cv.add(cx, cy-h, cx+w, cy, tan); cv.add(cx-w, cy, cx+w, cy, brown)
    cv.add(cx-w*0.4, cy-h*0.4, cx+w*0.4, cy-h*0.4, tan)
    cv.add(cx, cy-h, cx, cy-h-26, beam)
    cv.add(cx, cy-h-26, cx+13, cy-h-19, brown); cv.add(cx+13, cy-h-19, cx, cy-h-12, brown)

def paw_print(cv, cx, cy, color=(140,120,110)):
    """Animal paw print -- main pad + four toes (Blackburrow gnolls)."""
    def oval(ox, oy, rx, ry):
        p = [(ox+rx*math.cos(t), oy+ry*math.sin(t)) for t in np.linspace(0, 2*math.pi, 10)]
        for i in range(len(p)-1): cv.add(*p[i], *p[i+1], color)
    oval(cx, cy+18, 26, 20)
    for dx in (-34, -12, 12, 34): oval(cx+dx*0.9, cy-24-abs(dx)*0.2, 9, 13)

def vine_edge(cv, x0, y0, x1, y1, nx, ny, leaf=(90,120,70), dleaf=(70,100,55)):
    """Leafy vine run along a border edge (Surefall Glade)."""
    dx, dy = x1-x0, y1-y0; L = (dx*dx+dy*dy)**.5; ux, uy = dx/L, dy/L; n = max(4, int(L/70))
    for i in range(n):
        ax, ay = x0+dx*i/n, y0+dy*i/n; bx, by = x0+dx*(i+1)/n, y0+dy*(i+1)/n
        mx, my = (ax+bx)/2+nx*22, (ay+by)/2+ny*22
        cv.add(ax, ay, mx, my, leaf); cv.add(mx, my, bx, by, leaf)
        if i % 2 == 0: cv.add(mx, my, mx+nx*14-uy*10, my+ny*14+ux*10, dleaf)

# NOTE: the Kerra Isle palms and Toxxulia fish / skunk / hill / s-contour generators
# lived in a prior-session helpers.py that does not persist. Re-upload that file OR the
# toxxulia_2 / kerra_2 decoration files and they can be ported in here exactly.
