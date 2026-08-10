"""fauna.py — creatures and folk, for populating a zone's margins and quarters.

Side-on silhouettes at 40-80 units: map marginalia, not markers. Every function
takes (cx, cy, s, ink=None, seed=0) and returns [(x1,y1,x2,y2,ink)], so they are
interchangeable and can be handed straight to a scatter.

Reading the races at a glance:
  ears        dark elf longest, then high and wood elf, halflings smallest but
              still pointed; gnomes round; kerrans on top of the head
  build       ogre > troll > barbarian > human > dwarf > gnome > halfling
  silhouette  does the work — at this size detail vanishes, so each race gets one
              unmistakable cue: the Erudite's hooded egg, the dwarf's beard, the
              Freeport turban, the Qeynos kite shield
"""
import math, random

PALETTE = {
    'bone':      (108, 104, 96),
    'chitin':    (64, 58, 66),
    'cloth':     (86, 70, 52),
    'teirdal':   (72, 58, 96),
    'highelf':   (86, 96, 124),
    'woodelf':   (68, 92, 62),
    'gnome':     (96, 88, 60),
    'dwarf':     (104, 76, 52),
    'barbarian': (110, 92, 70),
    'qeynos':    (78, 84, 110),
    'freeport':  (116, 88, 56),
    'kerran':    (118, 94, 62),
    'erudite':   (92, 84, 116),
    'troll':     (74, 92, 62),
    'ogre':      (98, 88, 60),
    'froglok':   (74, 100, 62),
    'iksar':     (92, 96, 86),
    'ratman':    (108, 100, 94),
    'kobold':    (104, 88, 70),
    'gnoll':     (120, 102, 74),
    'sprite':    (128, 150, 176),
    'myconid':   (126, 108, 128),
    'snake':     (92, 104, 70),
    'rat':       (110, 100, 92),
    'skunk':     (72, 68, 72),
    'drake':     (128, 82, 58),
    'fur':       (92, 80, 68),
}


def _P(out, pts, ink, close=False):
    for i in range(len(pts)-1):
        out.append((pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], ink))
    if close and len(pts) > 2:
        out.append((pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], ink))

def _ring(out, cx, cy, rx, ry, ink, n=10):
    prev = None
    for k in range(n+1):
        a = 2*math.pi*k/n
        p = (cx+math.cos(a)*rx, cy+math.sin(a)*ry)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p

def _ears(out, cx, cy, s, ink, length=0.30, tilt=0.55):
    """Two pointed ears, swept back. `length` is the race's tell."""
    for side in (-1, 1):
        bx = cx + side*s*0.12
        _P(out, [(bx, cy - s*0.02),
                 (bx + side*s*length, cy - s*length*tilt),
                 (bx + side*s*0.09, cy + s*0.05)], ink)

def _humanoid(out, cx, cy, s, ink, build=1.0, height=1.0, legs=True):
    top = cy - s*0.46*height
    hip = cy + s*0.10*height
    w = s*0.17*build
    _P(out, [(cx-w, hip), (cx-w*1.05, top), (cx+w*1.05, top), (cx+w, hip)], ink, close=True)
    if legs:
        out.append((cx-w*0.5, hip, cx-w*0.6, cy+s*0.42*height, ink))
        out.append((cx+w*0.5, hip, cx+w*0.65, cy+s*0.42*height, ink))
    return top, hip, w


# ------------------------------------------------------------------ elves --
def dark_elf(cx, cy, s, ink=None, seed=0):
    """Teir'Dal: tall, slim, the longest ears of any race, blade at the hip."""
    ink = ink or PALETTE['teirdal']
    out = []
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=0.92, height=1.08)
    hy = top - s*0.20
    _ring(out, cx, hy, s*0.14, s*0.16, ink)
    _ears(out, cx, hy, s, ink, length=0.34, tilt=0.62)
    out.append((cx+w*1.0, top+s*0.08, cx+s*0.34, cy+s*0.06, ink))
    _P(out, [(cx+s*0.28, cy+s*0.02), (cx+s*0.46, cy+s*0.34)], ink)
    return out

def high_elf(cx, cy, s, ink=None, seed=0):
    """Koada'Dal: upright, long robe, staff."""
    ink = ink or PALETTE['highelf']
    out = []
    top = cy - s*0.48
    _P(out, [(cx-s*0.20, cy+s*0.44), (cx-s*0.15, top), (cx+s*0.15, top),
             (cx+s*0.20, cy+s*0.44)], ink, close=True)
    hy = top - s*0.20
    _ring(out, cx, hy, s*0.13, s*0.15, ink)
    _ears(out, cx, hy, s, ink, length=0.30, tilt=0.60)
    out.append((cx+s*0.24, cy-s*0.52, cx+s*0.24, cy+s*0.40, ink))
    _ring(out, cx+s*0.24, cy-s*0.56, s*0.06, s*0.06, ink, n=8)
    return out

def wood_elf(cx, cy, s, ink=None, seed=0):
    """Feir'Dal: light build, bow across the back."""
    ink = ink or PALETTE['woodelf']
    out = []
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=0.88, height=0.96)
    hy = top - s*0.19
    _ring(out, cx, hy, s*0.13, s*0.15, ink)
    _ears(out, cx, hy, s, ink, length=0.24, tilt=0.58)
    prev = None
    for k in range(9):
        t = k/8.0; a = -1.1 + t*2.2
        p = (cx-s*0.30+math.sin(a)*s*0.10, cy-s*0.34+t*s*0.62)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    out.append((cx-s*0.30+math.sin(-1.1)*s*0.10, cy-s*0.34,
                cx-s*0.30+math.sin(1.1)*s*0.10, cy+s*0.28, ink))
    return out

def halfling(cx, cy, s, ink=None, seed=0):
    """Small and narrowly boxy, small pointed ears. Pack and walking stick."""
    ink = ink or PALETTE['cloth']
    out = []
    s = s*0.72
    top = cy - s*0.34; hip = cy + s*0.16; w = s*0.15
    _P(out, [(cx-w, hip), (cx-w, top), (cx+w, top), (cx+w, hip)], ink, close=True)
    out.append((cx-w*0.5, hip, cx-w*0.5, cy+s*0.44, ink))
    out.append((cx+w*0.5, hip, cx+w*0.5, cy+s*0.44, ink))
    hy = top - s*0.17
    _ring(out, cx, hy, s*0.13, s*0.14, ink)
    _ears(out, cx, hy, s, ink, length=0.16, tilt=0.50)
    _P(out, [(cx+w, top+s*0.06), (cx+s*0.30, top+s*0.16), (cx+s*0.28, hip-s*0.02)], ink)
    out.append((cx-s*0.28, top-s*0.14, cx-s*0.24, cy+s*0.46, ink))
    return out


# -------------------------------------------------------------- smallfolk --
def gnome(cx, cy, s, ink=None, seed=0):
    """Round head — no points — pointed cap, tool in hand."""
    ink = ink or PALETTE['gnome']
    out = []
    s = s*0.70
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=1.05, height=0.92)
    hy = top - s*0.19
    _ring(out, cx, hy, s*0.15, s*0.15, ink)
    _P(out, [(cx-s*0.15, hy-s*0.08), (cx+s*0.02, hy-s*0.40), (cx+s*0.15, hy-s*0.06)], ink)
    out.append((cx+w*1.1, cy-s*0.10, cx+s*0.34, cy+s*0.12, ink))
    out.append((cx+s*0.30, cy+s*0.06, cx+s*0.40, cy+s*0.02, ink))
    return out

def dwarf(cx, cy, s, ink=None, seed=0):
    """Short and broad; the beard does the identifying."""
    ink = ink or PALETTE['dwarf']
    out = []
    s = s*0.80
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=1.45, height=0.84)
    hy = top - s*0.17
    _ring(out, cx, hy, s*0.15, s*0.14, ink)
    _P(out, [(cx-s*0.15, hy+s*0.06), (cx-s*0.12, hy+s*0.34), (cx, hy+s*0.44),
             (cx+s*0.12, hy+s*0.34), (cx+s*0.15, hy+s*0.06)], ink)
    out.append((cx+w*1.05, cy-s*0.16, cx+s*0.40, cy-s*0.34, ink))
    _P(out, [(cx+s*0.32, cy-s*0.40), (cx+s*0.50, cy-s*0.30), (cx+s*0.34, cy-s*0.18)], ink)
    return out


# ---------------------------------------------------------------- big folk -
def barbarian(cx, cy, s, ink=None, seed=0):
    ink = ink or PALETTE['barbarian']
    out = []
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=1.35, height=1.10)
    hy = top - s*0.20
    _ring(out, cx, hy, s*0.15, s*0.16, ink)
    _P(out, [(cx-w*1.3, top+s*0.04), (cx, top-s*0.06), (cx+w*1.3, top+s*0.04)], ink)
    out.append((cx+s*0.34, cy-s*0.54, cx+s*0.34, cy+s*0.30, ink))
    _P(out, [(cx+s*0.34, cy-s*0.50), (cx+s*0.54, cy-s*0.38), (cx+s*0.34, cy-s*0.26)], ink)
    return out

def troll(cx, cy, s, ink=None, seed=0):
    """Hunched, arms below the knee, tusks."""
    ink = ink or PALETTE['troll']
    out = []
    top = cy - s*0.44; hip = cy + s*0.14; w = s*0.24
    _P(out, [(cx-w, hip), (cx-w*1.15, top+s*0.10), (cx-s*0.06, top-s*0.02),
             (cx+w*1.15, top+s*0.12), (cx+w, hip)], ink, close=True)
    hy = top - s*0.10
    _ring(out, cx-s*0.04, hy, s*0.15, s*0.13, ink)
    out.append((cx-s*0.12, hy+s*0.10, cx-s*0.16, hy+s*0.24, ink))
    out.append((cx+s*0.04, hy+s*0.10, cx+s*0.08, hy+s*0.24, ink))
    out.append((cx-w*1.1, top+s*0.16, cx-s*0.34, cy+s*0.40, ink))
    out.append((cx+w*1.1, top+s*0.18, cx+s*0.36, cy+s*0.42, ink))
    out.append((cx-w*0.5, hip, cx-w*0.55, cy+s*0.46, ink))
    out.append((cx+w*0.5, hip, cx+w*0.6, cy+s*0.46, ink))
    return out

def ogre(cx, cy, s, ink=None, seed=0):
    """The biggest silhouette on the map."""
    ink = ink or PALETTE['ogre']
    out = []
    s = s*1.15
    top = cy - s*0.42; hip = cy + s*0.16; w = s*0.30
    _P(out, [(cx-w, hip), (cx-w*1.2, top), (cx+w*1.2, top), (cx+w, hip)], ink, close=True)
    hy = top - s*0.12
    _ring(out, cx, hy, s*0.17, s*0.14, ink)
    out.append((cx-s*0.10, hy+s*0.10, cx-s*0.14, hy+s*0.26, ink))
    out.append((cx+s*0.10, hy+s*0.10, cx+s*0.14, hy+s*0.26, ink))
    out.append((cx+w*1.15, top+s*0.06, cx+s*0.44, cy+s*0.10, ink))
    _P(out, [(cx+s*0.40, cy+s*0.04), (cx+s*0.56, cy-s*0.24), (cx+s*0.46, cy-s*0.30),
             (cx+s*0.34, cy-s*0.02)], ink, close=True)
    out.append((cx-w*0.55, hip, cx-w*0.6, cy+s*0.44, ink))
    out.append((cx+w*0.55, hip, cx+w*0.6, cy+s*0.44, ink))
    return out


# ------------------------------------------------------------------ humans -
def qeynos_human(cx, cy, s, ink=None, seed=0):
    """Camelot cast: tabard, kite shield, straight sword."""
    ink = ink or PALETTE['qeynos']
    out = []
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=1.08, height=1.0)
    hy = top - s*0.19
    _ring(out, cx, hy, s*0.14, s*0.15, ink)
    out.append((cx-s*0.02, top, cx-s*0.02, hip, ink))
    _P(out, [(cx-s*0.36, top+s*0.04), (cx-s*0.18, top+s*0.04),
             (cx-s*0.18, cy+s*0.14), (cx-s*0.27, cy+s*0.30),
             (cx-s*0.36, cy+s*0.14)], ink, close=True)
    out.append((cx+s*0.30, cy-s*0.40, cx+s*0.30, cy+s*0.16, ink))
    out.append((cx+s*0.22, cy-s*0.28, cx+s*0.38, cy-s*0.28, ink))
    return out

def freeport_human(cx, cy, s, ink=None, seed=0):
    """Turbaned corsair: sash, curved blade."""
    ink = ink or PALETTE['freeport']
    out = []
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=1.0, height=1.0)
    hy = top - s*0.19
    _ring(out, cx, hy, s*0.13, s*0.14, ink)
    _P(out, [(cx-s*0.17, hy-s*0.08), (cx-s*0.10, hy-s*0.26), (cx+s*0.10, hy-s*0.26),
             (cx+s*0.17, hy-s*0.08)], ink, close=True)
    out.append((cx+s*0.17, hy-s*0.20, cx+s*0.30, hy-s*0.04, ink))
    out.append((cx-w, cy-s*0.06, cx+w, cy-s*0.02, ink))
    prev = None
    for k in range(7):
        t = k/6.0; a = -0.5 + t*1.5
        p = (cx+s*0.28+math.sin(a)*s*0.18, cy-s*0.22+t*s*0.44)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    return out


# ------------------------------------------------------------------ others -
def kerran(cx, cy, s, ink=None, seed=0):
    """Cat folk: ears on top of the head, tail up."""
    ink = ink or PALETTE['kerran']
    out = []
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=0.95, height=1.0)
    hy = top - s*0.19
    _ring(out, cx, hy, s*0.14, s*0.14, ink)
    for side in (-1, 1):
        _P(out, [(cx+side*s*0.05, hy-s*0.12), (cx+side*s*0.13, hy-s*0.30),
                 (cx+side*s*0.17, hy-s*0.08)], ink)
    out.append((cx-s*0.02, hy+s*0.03, cx+s*0.02, hy+s*0.03, ink))
    prev = None
    for k in range(8):
        t = k/7.0
        p = (cx-w-s*0.06-math.sin(t*2.2)*s*0.16, cy+s*0.24-t*s*0.52)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    return out

def erudite(cx, cy, s, ink=None, seed=0):
    """Hooded egg-shaped skull, high brow, book. Reads as almost alien."""
    ink = ink or PALETTE['erudite']
    out = []
    top = cy - s*0.44
    _P(out, [(cx-s*0.19, cy+s*0.44), (cx-s*0.15, top), (cx+s*0.15, top),
             (cx+s*0.19, cy+s*0.44)], ink, close=True)
    hy = top - s*0.26
    prev = None
    for k in range(13):
        a = 2*math.pi*k/12
        p = (cx+math.cos(a)*s*0.14, hy+math.sin(a)*s*0.26)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    _P(out, [(cx-s*0.17, hy+s*0.10), (cx-s*0.13, hy-s*0.30), (cx, hy-s*0.40),
             (cx+s*0.13, hy-s*0.30), (cx+s*0.17, hy+s*0.10)], ink)
    _P(out, [(cx+s*0.14, cy-s*0.02), (cx+s*0.34, cy-s*0.06),
             (cx+s*0.34, cy+s*0.12), (cx+s*0.14, cy+s*0.16)], ink, close=True)
    return out


# --------------------------------------------------------------- creatures -
def spider(cx, cy, s, ink=None, seed=0):
    ink = ink or PALETTE['chitin']
    out = []
    _ring(out, cx, cy, s*0.30, s*0.24, ink, n=12)
    _ring(out, cx-s*0.34, cy, s*0.13, s*0.12, ink, n=8)
    for i in range(4):
        for side in (-1, 1):
            base = (cx-s*0.22+i*s*0.14, cy+side*s*0.10)
            knee = (base[0]-s*0.10+i*s*0.05, base[1]+side*s*(0.34+0.05*i))
            tip  = (knee[0]+s*(0.22+0.06*i), knee[1]+side*s*(0.16+0.04*i))
            _P(out, [base, knee, tip], ink)
    return out

def skeleton(cx, cy, s, ink=None, seed=0):
    ink = ink or PALETTE['bone']
    out = []
    _ring(out, cx, cy-s*0.78, s*0.13, s*0.15, ink, n=8)
    out.append((cx, cy-s*0.63, cx, cy-s*0.22, ink))
    for k in range(3):
        yy = cy-s*0.56+k*s*0.11
        out.append((cx-s*0.13, yy, cx+s*0.13, yy, ink))
    _P(out, [(cx-s*0.15, cy-s*0.58), (cx-s*0.30, cy-s*0.34), (cx-s*0.24, cy-s*0.10)], ink)
    _P(out, [(cx+s*0.15, cy-s*0.58), (cx+s*0.32, cy-s*0.40), (cx+s*0.40, cy-s*0.50)], ink)
    out.append((cx-s*0.12, cy-s*0.22, cx+s*0.12, cy-s*0.22, ink))
    _P(out, [(cx-s*0.08, cy-s*0.22), (cx-s*0.20, cy+s*0.06), (cx-s*0.14, cy+s*0.34)], ink)
    _P(out, [(cx+s*0.08, cy-s*0.22), (cx+s*0.18, cy+s*0.04), (cx+s*0.30, cy+s*0.30)], ink)
    return out

def wolf(cx, cy, s, ink=None, seed=0):
    ink = ink or PALETTE['fur']
    out = []
    _P(out, [(cx-s*0.42, cy-s*0.10), (cx-s*0.30, cy-s*0.24), (cx+s*0.16, cy-s*0.26),
             (cx+s*0.40, cy-s*0.14), (cx+s*0.46, cy-s*0.24), (cx+s*0.50, cy-s*0.06),
             (cx+s*0.34, cy+s*0.02), (cx-s*0.18, cy+s*0.04), (cx-s*0.42, cy-s*0.10)], ink)
    for dx, sw in ((-0.26, 1), (-0.10, -1), (0.16, 1), (0.30, -1)):
        out.append((cx+s*dx, cy+s*0.02, cx+s*(dx+0.06*sw), cy+s*0.30, ink))
    _P(out, [(cx-s*0.42, cy-s*0.10), (cx-s*0.56, cy-s*0.30)], ink)
    return out

def bat(cx, cy, s, ink=None, seed=0):
    ink = ink or PALETTE['chitin']
    out = []
    _P(out, [(cx-s*0.50, cy-s*0.10), (cx-s*0.28, cy-s*0.24), (cx-s*0.10, cy-s*0.06),
             (cx, cy-s*0.14), (cx+s*0.10, cy-s*0.06), (cx+s*0.28, cy-s*0.24),
             (cx+s*0.50, cy-s*0.10)], ink)
    _P(out, [(cx-s*0.50, cy-s*0.10), (cx-s*0.30, cy+s*0.06), (cx-s*0.08, cy+s*0.02)], ink)
    _P(out, [(cx+s*0.50, cy-s*0.10), (cx+s*0.30, cy+s*0.06), (cx+s*0.08, cy+s*0.02)], ink)
    out.append((cx, cy-s*0.14, cx, cy+s*0.06, ink))
    return out


# ------------------------------------------------------- froglok & iksar ---
def froglok(cx, cy, s, ink=None, seed=0):
    """Froglok: broad flat skull with the eyes ON TOP, wide mouth, squat torso,
    long folded legs and big splayed feet. Crouched even when standing."""
    ink = ink or PALETTE['froglok']
    out = []
    top = cy - s*0.34; hip = cy + s*0.14; w = s*0.21
    _P(out, [(cx-w, hip), (cx-w*1.12, top+s*0.04), (cx+w*1.12, top+s*0.04),
             (cx+w, hip)], ink, close=True)                      # squat torso
    hy = top - s*0.16
    _P(out, [(cx-s*0.24, hy+s*0.08), (cx-s*0.22, hy-s*0.06), (cx, hy-s*0.12),
             (cx+s*0.22, hy-s*0.06), (cx+s*0.24, hy+s*0.08)], ink)   # broad skull
    out.append((cx-s*0.24, hy+s*0.08, cx+s*0.24, hy+s*0.08, ink))    # wide mouth
    for side in (-1, 1):                                             # eyes on top
        _ring(out, cx+side*s*0.13, hy-s*0.13, s*0.06, s*0.06, ink, n=8)
    for side in (-1, 1):                                             # folded legs
        _P(out, [(cx+side*w*0.6, hip), (cx+side*s*0.34, cy+s*0.16),
                 (cx+side*s*0.20, cy+s*0.46)], ink)
        _P(out, [(cx+side*s*0.20, cy+s*0.46), (cx+side*s*0.06, cy+s*0.52),
                 (cx+side*s*0.34, cy+s*0.52)], ink)                  # splayed foot
    out.append((cx-w*1.05, top+s*0.12, cx-s*0.30, cy+s*0.02, ink))   # short arms
    out.append((cx+w*1.05, top+s*0.12, cx+s*0.30, cy+s*0.02, ink))
    return out


def iksar(cx, cy, s, ink=None, seed=0):
    """Iksar: tall and lean, crested skull, snout, digitigrade legs, heavy tail
    counterbalancing forward. The tail is the tell."""
    ink = ink or PALETTE['iksar']
    out = []
    top = cy - s*0.48; hip = cy + s*0.08; w = s*0.16
    _P(out, [(cx-w, hip), (cx-w*1.05, top), (cx+w*1.05, top), (cx+w, hip)], ink, close=True)
    hy = top - s*0.20
    _P(out, [(cx-s*0.10, hy+s*0.10), (cx-s*0.14, hy-s*0.06), (cx+s*0.06, hy-s*0.12),
             (cx+s*0.26, hy-s*0.02), (cx+s*0.28, hy+s*0.06),
             (cx+s*0.06, hy+s*0.12)], ink, close=True)               # snouted skull
    _P(out, [(cx-s*0.12, hy-s*0.04), (cx-s*0.24, hy-s*0.22), (cx-s*0.04, hy-s*0.14)], ink)  # crest
    _P(out, [(cx-s*0.06, hy-s*0.10), (cx-s*0.20, hy-s*0.30)], ink)
    prev = None                                                       # tail
    for k in range(9):
        t = k/8.0
        p = (cx-w-s*0.10-t*s*0.46, hip - s*0.04 + math.sin(t*2.4)*s*0.12 + t*s*0.30)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    for side in (-1, 1):                                              # digitigrade
        _P(out, [(cx+side*w*0.55, hip), (cx+side*s*0.24, cy+s*0.22),
                 (cx+side*s*0.12, cy+s*0.42), (cx+side*s*0.30, cy+s*0.46)], ink)
    out.append((cx+w*1.05, top+s*0.10, cx+s*0.32, cy+s*0.02, ink))
    return out


def ratman(cx, cy, s, ink=None, seed=0):
    """Chetari and their kin: upright rat, long snout and whiskers, round ear,
    hunched shoulders, bare rope-like tail, digitigrade feet."""
    ink = ink or PALETTE['ratman']
    out = []
    top = cy - s*0.42; hip = cy + s*0.10; w = s*0.18
    _P(out, [(cx-w, hip), (cx-w*1.14, top+s*0.06), (cx-s*0.02, top-s*0.02),
             (cx+w*1.05, top+s*0.10), (cx+w, hip)], ink, close=True)  # hunched torso
    hy = top - s*0.16
    _P(out, [(cx+s*0.10, hy+s*0.10), (cx-s*0.06, hy+s*0.12), (cx-s*0.14, hy+s*0.02),
             (cx-s*0.06, hy-s*0.10), (cx+s*0.12, hy-s*0.10),
             (cx+s*0.34, hy+s*0.00), (cx+s*0.36, hy+s*0.06),
             (cx+s*0.12, hy+s*0.12)], ink, close=True)                # long snout
    _ring(out, cx-s*0.06, hy-s*0.16, s*0.09, s*0.09, ink, n=8)        # round ear
    for k in (-1, 0, 1):                                              # whiskers
        out.append((cx+s*0.34, hy+s*0.03, cx+s*0.50, hy+s*0.03+k*s*0.08, ink))
    prev = None                                                        # rope tail
    for k in range(10):
        t = k/9.0
        p = (cx-w-s*0.06-t*s*0.52, hip + math.sin(t*2.8)*s*0.14 + t*s*0.24)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    for side in (-1, 1):
        _P(out, [(cx+side*w*0.55, hip), (cx+side*s*0.22, cy+s*0.24),
                 (cx+side*s*0.10, cy+s*0.44), (cx+side*s*0.28, cy+s*0.48)], ink)
    out.append((cx+w*1.0, top+s*0.14, cx+s*0.30, cy+s*0.04, ink))     # arm
    _P(out, [(cx+s*0.26, cy-s*0.02), (cx+s*0.44, cy-s*0.20), (cx+s*0.34, cy-s*0.28)], ink)
    return out


# ------------------------------------------------- beast-folk & vermin -----
def kobold(cx, cy, s, ink=None, seed=0):
    """Kobold: short, hunched, long snouted head with a backswept crest."""
    ink = ink or PALETTE['kobold']
    out = []
    s = s*0.82
    top, hip, w = _humanoid(out, cx, cy, s, ink, build=1.0, height=0.88)
    hy = top - s*0.16
    _P(out, [(cx+s*0.06, hy+s*0.10), (cx-s*0.12, hy+s*0.08), (cx-s*0.14, hy-s*0.04),
             (cx+s*0.06, hy-s*0.12), (cx+s*0.30, hy-s*0.02), (cx+s*0.32, hy+s*0.06)],
       ink, close=True)
    _P(out, [(cx-s*0.06, hy-s*0.10), (cx-s*0.18, hy-s*0.28), (cx+s*0.02, hy-s*0.16)], ink)
    out.append((cx-w*1.0, top+s*0.12, cx-s*0.30, cy+s*0.20, ink))
    out.append((cx+w*1.0, top+s*0.12, cx+s*0.34, cy+s*0.06, ink))
    _P(out, [(cx+s*0.30, cy+s*0.02), (cx+s*0.44, cy-s*0.24)], ink)      # short spear
    return out


def gnoll(cx, cy, s, ink=None, seed=0):
    """Gnoll: tall hyena-folk, sloped back, upright ears, spotted shoulders."""
    ink = ink or PALETTE['gnoll']
    out = []
    top = cy - s*0.46; hip = cy + s*0.10; w = s*0.19
    _P(out, [(cx-w, hip), (cx-w*1.2, top+s*0.14), (cx+s*0.02, top-s*0.02),
             (cx+w*1.05, top+s*0.14), (cx+w, hip)], ink, close=True)     # sloped back
    hy = top - s*0.14
    _ring(out, cx+s*0.02, hy, s*0.13, s*0.12, ink)
    for side in (-1, 1):                                                 # upright ears
        _P(out, [(cx+s*0.02+side*s*0.06, hy-s*0.10),
                 (cx+s*0.02+side*s*0.10, hy-s*0.30),
                 (cx+s*0.02+side*s*0.16, hy-s*0.08)], ink)
    _P(out, [(cx+s*0.14, hy+s*0.04), (cx+s*0.30, hy+s*0.08), (cx+s*0.14, hy+s*0.12)], ink)
    for dx, dy in ((-0.10,-0.22),(0.02,-0.16),(-0.04,-0.06)):            # spots
        _ring(out, cx+s*dx, cy+s*dy, s*0.03, s*0.03, ink, n=6)
    out.append((cx-w*1.1, top+s*0.20, cx-s*0.34, cy+s*0.24, ink))
    out.append((cx+w*1.0, top+s*0.20, cx+s*0.34, cy+s*0.10, ink))
    out.append((cx-w*0.5, hip, cx-w*0.6, cy+s*0.44, ink))
    out.append((cx+w*0.5, hip, cx+w*0.65, cy+s*0.44, ink))
    prev = None
    for k in range(7):                                                    # low tail
        t = k/6.0
        p = (cx-w-s*0.04-t*s*0.30, hip+s*0.02+math.sin(t*2.2)*s*0.10+t*s*0.18)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    return out


def sprite(cx, cy, s, ink=None, seed=0):
    """Sprite: a small body between two upswept wings, with a trailing glimmer."""
    ink = ink or PALETTE['sprite']
    rnd = random.Random(seed)
    out = []
    s = s*0.60
    _ring(out, cx, cy, s*0.10, s*0.16, ink, n=8)
    for side in (-1, 1):
        _P(out, [(cx+side*s*0.08, cy-s*0.06),
                 (cx+side*s*0.34, cy-s*0.44),
                 (cx+side*s*0.44, cy-s*0.10),
                 (cx+side*s*0.22, cy+s*0.06)], ink)
    _ring(out, cx, cy-s*0.24, s*0.07, s*0.07, ink, n=7)
    for k in range(3):
        d = s*(0.30+0.18*k)
        out.append((cx-d, cy+s*0.24+k*s*0.06, cx-d-s*0.10, cy+s*0.26+k*s*0.06, ink))
    return out


def myconid(cx, cy, s, ink=None, seed=0):
    """Mushroom folk: broad cap over a stout stalk, with stubby arms."""
    ink = ink or PALETTE['myconid']
    rnd = random.Random(seed)
    out = []
    s = s*0.78
    capy = cy - s*0.34
    prev = None
    for k in range(15):
        a = math.pi + math.pi*k/14
        p = (cx+math.cos(a)*s*0.36, capy+math.sin(a)*s*0.26)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    out.append((cx-s*0.36, capy, cx+s*0.36, capy, ink))
    for k in range(4):                                                    # gills
        x = cx-s*0.24+k*s*0.16
        out.append((x, capy, x+rnd.uniform(-2,2), capy+s*0.09, ink))
    _P(out, [(cx-s*0.14, capy+s*0.04), (cx-s*0.16, cy+s*0.40),
             (cx+s*0.16, cy+s*0.40), (cx+s*0.14, capy+s*0.04)], ink)      # stalk
    out.append((cx-s*0.15, cy-s*0.02, cx-s*0.30, cy+s*0.10, ink))
    out.append((cx+s*0.15, cy-s*0.02, cx+s*0.30, cy+s*0.10, ink))
    out.append((cx-s*0.22, cy+s*0.40, cx+s*0.22, cy+s*0.40, ink))
    return out


def snake(cx, cy, s, ink=None, seed=0):
    """A serpent in an S-curve, head raised."""
    ink = ink or PALETTE['snake']
    out = []
    prev = None
    for k in range(19):
        t = k/18.0
        x = cx - s*0.48 + t*s*0.92
        y = cy + math.sin(t*3.4)*s*0.20
        if prev: out.append((prev[0], prev[1], x, y, ink))
        prev = (x, y)
    hx, hy = prev
    _P(out, [(hx, hy), (hx+s*0.14, hy-s*0.14), (hx+s*0.26, hy-s*0.10),
             (hx+s*0.16, hy-s*0.02)], ink, close=True)
    out.append((hx+s*0.26, hy-s*0.11, hx+s*0.36, hy-s*0.14, ink))         # tongue
    return out


def rat(cx, cy, s, ink=None, seed=0):
    """Common rat: low body, pointed snout, long bare tail."""
    ink = ink or PALETTE['rat']
    out = []
    s = s*0.62
    _P(out, [(cx-s*0.34, cy), (cx-s*0.20, cy-s*0.18), (cx+s*0.14, cy-s*0.20),
             (cx+s*0.34, cy-s*0.06), (cx+s*0.46, cy+s*0.02),
             (cx+s*0.28, cy+s*0.08), (cx-s*0.18, cy+s*0.10)], ink, close=True)
    _ring(out, cx+s*0.12, cy-s*0.22, s*0.07, s*0.07, ink, n=7)            # ear
    for dx in (-0.16, 0.02, 0.20):
        out.append((cx+s*dx, cy+s*0.08, cx+s*(dx-0.03), cy+s*0.26, ink))
    prev = None
    for k in range(8):
        t = k/7.0
        p = (cx-s*0.34-t*s*0.44, cy+math.sin(t*2.6)*s*0.12)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    return out


def skunk(cx, cy, s, ink=None, seed=0):
    """Skunk: low body, plume tail up, pale stripe along the back."""
    ink = ink or PALETTE['skunk']
    out = []
    s = s*0.66
    _P(out, [(cx-s*0.30, cy), (cx-s*0.16, cy-s*0.16), (cx+s*0.16, cy-s*0.18),
             (cx+s*0.36, cy-s*0.04), (cx+s*0.26, cy+s*0.08),
             (cx-s*0.16, cy+s*0.10)], ink, close=True)
    out.append((cx-s*0.14, cy-s*0.13, cx+s*0.20, cy-s*0.15, ink))         # stripe
    for dx in (-0.12, 0.04, 0.20):
        out.append((cx+s*dx, cy+s*0.08, cx+s*(dx-0.02), cy+s*0.24, ink))
    prev = None                                                            # plume
    for k in range(9):
        t = k/8.0
        a = -0.2 - t*2.0
        p = (cx-s*0.32+math.cos(a)*s*0.30, cy-s*0.02+math.sin(a)*s*0.36)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    return out


def drake(cx, cy, s, ink=None, seed=0):
    """Small drake: long neck, membranous wings, whip tail."""
    ink = ink or PALETTE['drake']
    out = []
    _P(out, [(cx-s*0.22, cy), (cx-s*0.04, cy-s*0.12), (cx+s*0.20, cy-s*0.06),
             (cx+s*0.26, cy+s*0.06), (cx-s*0.10, cy+s*0.10)], ink, close=True)
    _P(out, [(cx-s*0.22, cy-s*0.02), (cx-s*0.38, cy-s*0.24),
             (cx-s*0.52, cy-s*0.30)], ink)                                 # neck
    _P(out, [(cx-s*0.52, cy-s*0.30), (cx-s*0.66, cy-s*0.36),
             (cx-s*0.58, cy-s*0.22), (cx-s*0.48, cy-s*0.24)], ink, close=True)
    for side, sw in ((-1, 0.9), (1, 1.15)):                                # wings
        _P(out, [(cx-s*0.02, cy-s*0.10),
                 (cx+side*s*0.26, cy-s*0.52*sw),
                 (cx+side*s*0.50, cy-s*0.34*sw),
                 (cx+side*s*0.20, cy-s*0.12)], ink)
        out.append((cx+side*s*0.26, cy-s*0.52*sw, cx+side*s*0.24, cy-s*0.18, ink))
    prev = None
    for k in range(8):
        t = k/7.0
        p = (cx+s*0.26+t*s*0.46, cy+s*0.06+math.sin(t*2.4)*s*0.14)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    return out


RACES = {
    'dark_elf': dark_elf, 'high_elf': high_elf, 'wood_elf': wood_elf,
    'halfling': halfling, 'gnome': gnome, 'dwarf': dwarf,
    'barbarian': barbarian, 'troll': troll, 'ogre': ogre,
    'qeynos_human': qeynos_human, 'freeport_human': freeport_human,
    'kerran': kerran, 'erudite': erudite,
    'froglok': froglok, 'iksar': iksar,
}
CREATURES = {'spider': spider, 'skeleton': skeleton, 'wolf': wolf, 'bat': bat,
             'ratman': ratman, 'kobold': kobold, 'gnoll': gnoll, 'sprite': sprite,
             'myconid': myconid, 'snake': snake, 'rat': rat, 'skunk': skunk,
             'drake': drake}

# which folk belong to which home city, for populating a zone plausibly
HOMELANDS = {
    'neriak': ['dark_elf'], 'felwithe': ['high_elf'], 'kelethin': ['wood_elf'],
    'rivervale': ['halfling'], 'akanon': ['gnome'], 'kaladim': ['dwarf'],
    'halas': ['barbarian'], 'qeynos': ['qeynos_human'], 'freeport': ['freeport_human'],
    'erudin': ['erudite'], 'paineel': ['erudite'], 'grobb': ['troll'],
    'oggok': ['ogre'], 'kerraisle': ['kerran'],
    'gukta': ['froglok'], 'cabilis': ['iksar'],
}
