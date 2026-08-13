"""nse_decor.py -- New Sebilis decoration primitives.

The original module was lost before it reached the repo; the iksar glyph below was
recovered by sampling the surviving line data in newsebexp_2.txt and normalising it
to a unit shape. Bookshelves and root drips are rebuilt from nse_build_2.py's usage.
"""
import math, random

# Inks read back off the shipped map, not guessed.
IRON   = (108, 96, 86)
IRON_L = (140, 128, 116)
ROOT   = (108, 80, 48)      # root highlight  (n=158 in newsebexp_2)
ROOT_D = (80, 58, 34)       # root shadow     (n=159) -- drawn as a PAIR with ROOT,
                            # which is what gives the roots their 3D thickness
GLYPH  = (168, 58, 44)      # iksar red
GLYPH_K= (58, 50, 46)       # the black star at the glyph's centre
BOOK_R = (150, 70, 55)      # coloured book spines
BOOK_Y = (140, 120, 70)
BOOK_G = (120, 95, 60)
BOOK_B = (90, 90, 130)
BOOK_C = (176, 168, 140)
BOOKS  = (BOOK_R, BOOK_Y, BOOK_G, BOOK_B, BOOK_C)

_GLYPH_PTS = [(-1.0, -0.149, -0.733, -0.149), (0.383, 0.417, 0.378, 0.343), (0.41, 0.171, 0.296, 0.247), (0.296, 0.247, 0.233, 0.241), (0.233, 0.241, 0.26, 0.174), (0.26, 0.174, 0.373, 0.096), (0.361, 0.043, 0.23, 0.042), (0.23, 0.042, 0.178, 0.0), (0.178, 0.0, 0.23, -0.042), (0.23, -0.042, 0.361, -0.043), (0.386, 0.064, 0.379, 0.0), (0.379, 0.0, 0.386, -0.064), (0.817, -0.043, 0.948, -0.042), (0.948, -0.042, 1.0, 0.0), (1.0, 0.0, 0.948, 0.042), (0.948, 0.042, 0.817, 0.043), (0.805, 0.096, 0.918, 0.174), (0.918, 0.174, 0.945, 0.241), (0.945, 0.241, 0.882, 0.247), (0.882, 0.247, 0.768, 0.171), (0.735, 0.21, 0.8, 0.343), (0.8, 0.343, 0.794, 0.417), (0.794, 0.417, 0.737, 0.385), (0.737, 0.385, 0.671, 0.253), (0.626, 0.267, 0.625, 0.421), (0.625, 0.421, 0.589, 0.482), (0.589, 0.482, 0.553, 0.421), (0.553, 0.421, 0.552, 0.267), (0.507, 0.253, 0.441, 0.385), (0.441, 0.385, 0.383, 0.417), (0.378, 0.343, 0.443, 0.21), (0.799, 0.0, 0.792, 0.064), (0.792, 0.064, 0.771, 0.123), (0.771, 0.123, 0.737, 0.174), (0.737, 0.174, 0.694, 0.213), (0.694, 0.213, 0.643, 0.237), (0.643, 0.237, 0.589, 0.246), (0.589, 0.246, 0.535, 0.237), (0.535, 0.237, 0.484, 0.213), (0.484, 0.213, 0.441, 0.174), (0.441, 0.174, 0.407, 0.123), (0.407, 0.123, 0.386, 0.064), (0.792, -0.064, 0.799, 0.0), (0.799, 0.0, 0.799, 0.0), (0.443, -0.21, 0.378, -0.343), (0.383, -0.417, 0.441, -0.385), (0.441, -0.385, 0.507, -0.253), (0.552, -0.267, 0.553, -0.421), (0.553, -0.421, 0.589, -0.482), (0.589, -0.482, 0.625, -0.421), (0.625, -0.421, 0.626, -0.267), (0.671, -0.253, 0.737, -0.385), (0.737, -0.385, 0.794, -0.417), (0.794, -0.417, 0.8, -0.343), (0.8, -0.343, 0.735, -0.21), (0.768, -0.171, 0.882, -0.247), (0.882, -0.247, 0.945, -0.241), (0.945, -0.241, 0.918, -0.174), (0.918, -0.174, 0.805, -0.096), (0.386, -0.064, 0.407, -0.123), (0.407, -0.123, 0.441, -0.174), (0.441, -0.174, 0.484, -0.213), (0.484, -0.213, 0.535, -0.237), (0.535, -0.237, 0.589, -0.246), (0.589, -0.246, 0.643, -0.237), (0.643, -0.237, 0.694, -0.213), (0.694, -0.213, 0.737, -0.174), (0.737, -0.174, 0.771, -0.123), (0.771, -0.123, 0.792, -0.064), (0.373, -0.096, 0.26, -0.174), (0.26, -0.174, 0.233, -0.241), (0.233, -0.241, 0.296, -0.247), (0.296, -0.247, 0.41, -0.171), (0.378, -0.343, 0.383, -0.417), (-0.733, -0.149, -0.733, 0.253), (-0.733, 0.253, -0.809, 0.32), (-0.809, 0.32, -1.0, 0.253)]

def iksar_glyph(cx, cy, size, ink=GLYPH, core=GLYPH_K):
    """The iksar sunburst: petals around a ring, with a thin spiked star inside it.

    Also sits at the centre of the New Sebilis compass rose.
    """
    out = []
    R  = size*0.46          # inner ring
    PL = size*1.00          # petal tip
    n  = 12
    for k in range(n):
        a  = 2*math.pi*k/n
        aw = math.pi/n*0.62
        bx, by = cx+math.cos(a-aw)*R, cy+math.sin(a-aw)*R
        tx, ty = cx+math.cos(a)*PL,   cy+math.sin(a)*PL
        ex, ey = cx+math.cos(a+aw)*R, cy+math.sin(a+aw)*R
        out.append((bx, by, tx, ty, ink))
        out.append((tx, ty, ex, ey, ink))
        out += _hatch([(bx,by),(tx,ty),(ex,ey)], ink, step=size*0.055)
    prev = None                                  # the ring itself
    for k in range(41):
        a = 2*math.pi*k/40
        pt = (cx+math.cos(a)*R, cy+math.sin(a)*R)
        if prev: out.append((prev[0], prev[1], pt[0], pt[1], ink))
        prev = pt
    for k in range(8):                           # thin spiked star, inside the ring
        a = 2*math.pi*k/8
        out.append((cx, cy, cx+math.cos(a)*R*0.80, cy+math.sin(a)*R*0.80, core))
    for k in range(8):                           # short cross-ticks near the hub
        a = 2*math.pi*(k+0.5)/8
        out.append((cx+math.cos(a)*R*0.10, cy+math.sin(a)*R*0.10,
                    cx+math.cos(a)*R*0.34, cy+math.sin(a)*R*0.34, core))
    return out


def bookshelf(cx, cy, w, h, ink=IRON, spine=None, seed=0):
    """A case of iksar tomes: three shelves of outlined books in mixed colours."""
    rnd = random.Random(seed)
    out = [(cx-w/2, cy-h/2, cx+w/2, cy-h/2, ink),
           (cx-w/2, cy+h/2, cx+w/2, cy+h/2, ink),
           (cx-w/2, cy-h/2, cx-w/2, cy+h/2, ink),
           (cx+w/2, cy-h/2, cx+w/2, cy+h/2, ink)]
    rows = 3
    for r in range(1, rows):
        y = cy - h/2 + h*r/rows
        out.append((cx-w/2, y, cx+w/2, y, ink))
    for r in range(rows):
        y1 = cy - h/2 + h*(r+1)/rows
        x = cx - w/2 + w*0.03
        while x < cx + w/2 - w*0.07:
            bw = w*rnd.uniform(0.045, 0.085)
            bh = (h/rows)*rnd.uniform(0.62, 0.92)
            col = spine or rnd.choice(BOOKS)
            out.append((x, y1, x, y1-bh, col))              # left board
            out.append((x+bw, y1, x+bw, y1-bh, col))        # right board
            out.append((x, y1-bh, x+bw, y1-bh, col))        # top edge
            out += _hatch([(x,y1),(x+bw,y1),(x+bw,y1-bh),(x,y1-bh)], col,
                          step=max(2.0, bh*0.22))
            x += bw*rnd.uniform(1.02, 1.20)
    return out


def root_drip(cx, cy, length, ink=ROOT, dark=ROOT_D, seed=0):
    """A root hanging from the ceiling.

    Drawn as a PAIR of offset strands -- highlight and shadow -- which is how the
    originals got their thickness. A single stroke reads as wire.
    """
    rnd = random.Random(seed)
    out = []
    w0 = length*0.055
    spine = [(cx, cy)]
    n = max(4, int(length/26))
    px, py = cx, cy
    for i in range(n):
        px += rnd.uniform(-length*0.05, length*0.05)
        py += length/n
        spine.append((px, py))
    for i in range(len(spine)-1):
        (ax, ay), (bx, by) = spine[i], spine[i+1]
        t0 = 1.0 - i/len(spine); t1 = 1.0 - (i+1)/len(spine)
        out.append((ax-w0*t0, ay, bx-w0*t1, by, dark))
        out.append((ax+w0*t0, ay, bx+w0*t1, by, ink))
        if i % 2 == 0:
            out.append((ax-w0*t0, ay, ax+w0*t0, ay, dark))
    for k in (len(spine)//2, len(spine)-3):
        if k < 1 or rnd.random() > 0.65: continue
        ax, ay = spine[k]
        fx = ax + rnd.uniform(-length*0.20, length*0.20)
        fy = ay + length*0.24
        out.append((ax-w0*0.4, ay, fx-w0*0.25, fy, dark))
        out.append((ax+w0*0.4, ay, fx+w0*0.25, fy, ink))
    return out


def root_burst(cx, cy, sx, sy, reach=250, ink=ROOT, dark=ROOT_D, seed=0):
    """Roots bursting from a corner, fanning inward."""
    rnd = random.Random(seed)
    out = []
    for k in range(rnd.randint(5, 8)):
        a = math.atan2(sy, sx) + rnd.uniform(-0.9, 0.9)
        px, py = cx, cy
        for i in range(rnd.randint(3, 5)):
            ln = reach*rnd.uniform(0.16, 0.30)
            nx = px + math.cos(a)*ln
            ny = py + math.sin(a)*ln
            out.append((px, py, nx, ny, ink if i % 2 else dark))
            a += rnd.uniform(-0.35, 0.35)
            px, py = nx, ny
    return out


def standard(cx, cy, h, pole=IRON, cloth=GLYPH, seed=0):
    """The iksar standard: a tall pole with a hanging banner, notched at the foot.

    Two swallow-tail points at the bottom of the cloth, a crossbar at the top, and
    a small finial. Reads at margin scale where a full sigil would not.
    """
    rnd = random.Random(seed)
    out = []
    out.append((cx, cy, cx, cy-h, pole))                        # pole
    out.append((cx-h*0.09, cy-h*0.98, cx+h*0.09, cy-h*0.98, pole))   # crossbar
    out.append((cx, cy-h, cx-h*0.035, cy-h*1.06, pole))         # finial
    out.append((cx, cy-h, cx+h*0.035, cy-h*1.06, pole))
    w  = h*0.30
    top = cy-h*0.92
    bot = cy-h*0.34
    out.append((cx, top, cx+w, top, cloth))                     # cloth top
    out.append((cx, top, cx, bot+h*0.10, cloth))                # inner edge
    out.append((cx+w, top, cx+w, bot+h*0.10, cloth))            # outer edge
    out.append((cx, bot+h*0.10, cx+w*0.30, bot, cloth))         # swallow tail
    out.append((cx+w*0.30, bot, cx+w*0.50, bot+h*0.09, cloth))
    out.append((cx+w*0.50, bot+h*0.09, cx+w*0.70, bot, cloth))
    out.append((cx+w*0.70, bot, cx+w, bot+h*0.10, cloth))
    out += _hatch([(cx,top),(cx+w,top),(cx+w,bot+h*0.10),
                   (cx+w*0.70,bot),(cx+w*0.50,bot+h*0.09),
                   (cx+w*0.30,bot),(cx,bot+h*0.10)], cloth, step=h*0.030)
    return out


def wall_candle(cx, cy, h, ink=IRON, flame=GLYPH, seed=0):
    """A bracket candle: sconce arm, candle body, and a small flame."""
    out = []
    out.append((cx-h*0.22, cy, cx+h*0.22, cy, ink))             # bracket
    out.append((cx-h*0.22, cy, cx-h*0.14, cy+h*0.14, ink))
    out.append((cx+h*0.22, cy, cx+h*0.14, cy+h*0.14, ink))
    out.append((cx-h*0.13, cy, cx-h*0.13, cy-h*0.62, ink))      # candle
    out.append((cx+h*0.13, cy, cx+h*0.13, cy-h*0.62, ink))
    out.append((cx-h*0.13, cy-h*0.62, cx+h*0.13, cy-h*0.62, ink))
    out.append((cx-h*0.13, cy-h*0.62, cx-h*0.06, cy-h*0.74, ink))   # drip
    out.append((cx, cy-h*0.62, cx, cy-h*0.72, ink))             # wick
    out.append((cx, cy-h*0.72, cx-h*0.07, cy-h*0.88, flame))    # flame
    out.append((cx, cy-h*0.72, cx+h*0.07, cy-h*0.88, flame))
    out.append((cx-h*0.07, cy-h*0.88, cx, cy-h*1.02, flame))
    out.append((cx+h*0.07, cy-h*0.88, cx, cy-h*1.02, flame))
    return out


def _hatch(pts, ink, step=3.0):
    """Fill a convex-ish polygon with horizontal hatching."""
    ys=[q[1] for q in pts]; out=[]
    y=min(ys)+step*0.5
    while y<max(ys):
        xs=[]
        for i in range(len(pts)):
            (x1,y1),(x2,y2)=pts[i],pts[(i+1)%len(pts)]
            if (y1>y)!=(y2>y): xs.append(x1+(y-y1)*(x2-x1)/(y2-y1))
        xs.sort()
        for i in range(0,len(xs)-1,2):
            if xs[i+1]-xs[i]>1.0: out.append((xs[i],y,xs[i+1],y,ink))
        y+=step
    return out


def root_bunch(cx, cy, length, ink=ROOT, dark=ROOT_D, seed=0):
    """A thick bunch of roots: several tapering strands sharing a crown, shaded."""
    rnd = random.Random(seed)
    out = []
    for k in range(rnd.randint(3, 5)):
        x0 = cx + rnd.uniform(-length*0.16, length*0.16)
        w0 = length*rnd.uniform(0.07, 0.11)
        spine=[(x0, cy)]
        px, py = x0, cy
        n = rnd.randint(5, 7)
        for i in range(n):
            px += rnd.uniform(-length*0.07, length*0.07)
            py += length/n
            spine.append((px, py))
        left=[]; right=[]
        for i,(sx,sy) in enumerate(spine):
            t = 1.0 - i/len(spine)
            left.append((sx-w0*t, sy)); right.append((sx+w0*t, sy))
        poly = left + right[::-1]
        out += _hatch(poly, ink, step=max(2.0, length*0.020))
        for i in range(len(left)-1):
            out.append((left[i][0], left[i][1], left[i+1][0], left[i+1][1], dark))
            out.append((right[i][0], right[i][1], right[i+1][0], right[i+1][1], dark))
        if rnd.random() < 0.7:                       # a fork
            j = len(spine)//2
            fx = spine[j][0] + rnd.uniform(-length*0.24, length*0.24)
            fy = spine[j][1] + length*0.30
            fw = w0*0.55
            fpoly = [(spine[j][0]-w0*0.5, spine[j][1]), (fx-fw, fy),
                     (fx+fw, fy), (spine[j][0]+w0*0.5, spine[j][1])]
            out += _hatch(fpoly, ink, step=max(2.0, length*0.022))
            out.append((spine[j][0]-w0*0.5, spine[j][1], fx-fw, fy, dark))
            out.append((spine[j][0]+w0*0.5, spine[j][1], fx+fw, fy, dark))
    return out
