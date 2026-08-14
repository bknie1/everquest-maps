"""gnome_decor.py -- Ak'Anon clockwork elements.

Persisted deliberately: these were first drawn inline in a build script, which is
how the original nse_decor module was lost. Anything used on a map lives in a kit.
"""
import math, random

BRASS = (120, 150, 120)
IRON  = (96, 112, 104)
DARK  = (70, 96, 86)
GLOW  = (70, 200, 120)      # the green checkpoint lanterns


def gear(cx, cy, r, ink=BRASS, hub=DARK, teeth=10):
    out = []; prev = None
    for k in range(25):
        a = 2*math.pi*k/24
        p = (cx+math.cos(a)*r, cy+math.sin(a)*r)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p
    for k in range(teeth):
        a = 2*math.pi*k/teeth
        out.append((cx+math.cos(a)*r, cy+math.sin(a)*r,
                    cx+math.cos(a)*r*1.28, cy+math.sin(a)*r*1.28, ink))
    prev = None
    for k in range(13):
        a = 2*math.pi*k/12
        p = (cx+math.cos(a)*r*0.34, cy+math.sin(a)*r*0.34)
        if prev: out.append((prev[0], prev[1], p[0], p[1], hub))
        prev = p
    return out


def gear_pair(cx, cy, r, ink=BRASS, hub=DARK):
    """Two meshed gears -- reads as machinery rather than an isolated cog."""
    out = gear(cx, cy, r, ink, hub)
    out += gear(cx + r*1.95, cy - r*0.35, r*0.62, ink, hub, teeth=8)
    return out


def pump(cx, cy, r, ink=IRON, accent=BRASS, dark=DARK, seed=0):
    """A steam pump: cylinder, piston rod, flywheel, exhaust stack."""
    out = []
    w, h = r*0.55, r*1.05
    out += [(cx-w, cy, cx-w, cy-h, ink), (cx+w, cy, cx+w, cy-h, ink),
            (cx-w, cy-h, cx+w, cy-h, ink), (cx-w*1.35, cy, cx+w*1.35, cy, dark)]
    out.append((cx, cy-h, cx, cy-h*1.55, dark))
    prev = None
    for k in range(13):
        a = 2*math.pi*k/12
        p = (cx+w*1.5+math.cos(a)*r*0.34, cy-h*0.45+math.sin(a)*r*0.34)
        if prev: out.append((prev[0], prev[1], p[0], p[1], accent))
        prev = p
    out.append((cx, cy-h*1.55, cx+w*1.5, cy-h*0.45, dark))
    for k in range(3):
        xx = cx-w + w*2*(k+1)/4
        out.append((xx, cy-h*0.15, xx, cy-h*0.85, ink))
    return out


def cog_tower(cx, cy, r, ink=IRON, accent=BRASS, dark=DARK, seed=0):
    """A stack of gearing on a frame -- the clanking machinery of Ak'Anon."""
    rnd = random.Random(seed)
    out = []
    w, h = r*0.85, r*1.7
    out += [(cx-w, cy, cx-w, cy-h, ink), (cx+w, cy, cx+w, cy-h, ink),
            (cx-w*1.25, cy, cx+w*1.25, cy, dark)]
    for k in range(3):
        yy = cy - h*(0.22 + 0.30*k)
        rr = r*(0.34 - 0.05*k)
        out += gear(cx + (w*0.35 if k % 2 else -w*0.35), yy, rr, accent, dark, teeth=8)
        out.append((cx-w, yy, cx+w, yy, ink))
    for k in range(2):
        out.append((cx-w, cy-h*(0.5+0.3*k), cx+w, cy-h*(0.35+0.3*k), dark))
    return out


def lantern(cx, cy, r, ink=IRON, glow=GLOW):
    """A green diamond checkpoint lantern on a post."""
    out = []
    s = r*0.34
    out += [(cx, cy-s*2.6, cx-s, cy-s*1.5, glow), (cx-s, cy-s*1.5, cx, cy-s*0.4, glow),
            (cx, cy-s*0.4, cx+s, cy-s*1.5, glow), (cx+s, cy-s*1.5, cx, cy-s*2.6, glow)]
    out.append((cx, cy-s*0.4, cx, cy+r*0.85, ink))
    out.append((cx-r*0.28, cy+r*0.85, cx+r*0.28, cy+r*0.85, ink))
    for k in range(4):
        a = math.pi/2*k + math.pi/4
        out.append((cx+math.cos(a)*s*1.5, cy-s*1.5+math.sin(a)*s*1.5,
                    cx+math.cos(a)*s*2.3, cy-s*1.5+math.sin(a)*s*2.3, glow))
    return out


def pipe_run(cx, cy, r, ink=IRON, dark=DARK, seed=0):
    """A run of pipework with elbows and flanges."""
    rnd = random.Random(seed)
    out = []
    x, y = cx - r, cy
    for k in range(4):
        ln = r*rnd.uniform(0.4, 0.8)
        vert = k % 2
        nx, ny = (x, y - ln) if vert else (x + ln, y)
        out.append((x, y, nx, ny, ink))
        out.append((x-r*0.07, y, x+r*0.07, y, dark))
        x, y = nx, ny
    out.append((x-r*0.07, y, x+r*0.07, y, dark))
    return out


SHAPES = {'gear': gear, 'gear_pair': gear_pair, 'pump': pump,
          'cog_tower': cog_tower, 'lantern': lantern, 'pipe_run': pipe_run}
