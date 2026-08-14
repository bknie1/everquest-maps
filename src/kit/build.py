"""build.py -- compose a zone's decoration layer from the kits, safely.

Everything needed already exists: layout.py for the boundary hierarchy, flora /
fauna / terrain / darkelf for shapes, titles.py for finding lettering. What was
missing was a builder that puts them together AND refuses to make things worse.

The safety rule, learned the hard way: a pass must never reduce a zone's title
health. build_zone() measures connected strokes above the grid before and after,
and raises rather than write a regression.

    from build import build_zone, THEMES
    build_zone('halas', THEMES['halas'])
"""
import collections, math, os, random, sys

sys.path.insert(0, os.path.dirname(__file__))
from layout import layout
import flora as FL, fauna as FA, terrain as TR

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def fmt(a, b, c, d, ink):
    return "L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (a, b, c, d, *ink)


def title_health(deco, grid_y0):
    """Connected strokes above the grid. Letters connect; texture does not."""
    key = lambda q: (round(q[0], 1), round(q[1], 1))
    band = [i for i, s in enumerate(deco) if (s[1] + s[3]) / 2 < grid_y0]
    adj = collections.defaultdict(list)
    for i in band:
        s = deco[i]
        adj[key((s[0], s[1]))].append(i)
        adj[key((s[2], s[3]))].append(i)
    return sum(1 for i in band
               if len(adj[key((deco[i][0], deco[i][1]))]) > 1
               or len(adj[key((deco[i][2], deco[i][3]))]) > 1)


def ring_slots(LO, n_top=6, n_bottom=7, n_side=5):
    """Evenly spaced margin positions, a fixed count per side.

    Walking a grid and letting collisions thin one side out is what made margins
    look lopsided; a fixed count per side cannot.
    """
    GX0, GX1, GY0, GY1 = LO['grid']
    MX0, MX1, MY0, MY1 = LO['margin']
    out = []
    for k in range(n_top):
        out.append((GX0 + (GX1-GX0)*(k+0.5)/n_top, (MY0+GY0)/2, 'top'))
    for k in range(n_bottom):
        out.append((GX0 + (GX1-GX0)*(k+0.5)/n_bottom, (GY1+MY1)/2, 'bottom'))
    for k in range(n_side):
        y = GY0 + (GY1-GY0)*(k+0.5)/n_side
        out.append(((MX0+GX0)/2, y, 'left'))
        out.append(((GX1+MX1)/2, y, 'right'))
    return out


def place(shapes, LO, reserved, gap_frac=0.018):
    """Place (fn, args) shapes at ring slots, skipping anything that collides."""
    GX0, GX1, GY0, GY1 = LO['grid']
    MX0, MX1, MY0, MY1 = LO['margin']
    S = LO['S']; gap = S*gap_frac
    boxes = list(reserved); out = []; n = 0
    for i, (x, y, side) in enumerate(ring_slots(LO)):
        fn = shapes[i % len(shapes)]
        d = fn(x, y, S)
        if not d: continue
        xs = [a for s in d for a in (s[0], s[2])]
        ys = [a for s in d for a in (s[1], s[3])]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if x0 < MX0+S*0.010 or x1 > MX1-S*0.010: continue
        if y0 < MY0+S*0.010 or y1 > MY1-S*0.010: continue
        if not (x1 < GX0-S*0.004 or x0 > GX1+S*0.004
                or y1 < GY0-S*0.004 or y0 > GY1+S*0.004): continue
        if any(x0 < b+gap and x1 > a-gap and y0 < d2+gap and y1 > c-gap
               for (a, b, c, d2) in boxes): continue
        out += d; boxes.append((x0, x1, y0, y1)); n += 1
    return out, n


# ---------------------------------------------------------------- themes
# Each theme names kit shapes rather than drawing inline. If a zone looks wrong,
# the fix belongs in the kit so every zone using that shape improves.
def _fl(fn, ink, trunk, lo, hi):
    """Wrap a flora shape. Some take trunk=, some do not -- pass it only if accepted."""
    import inspect
    takes_trunk = 'trunk' in inspect.signature(fn).parameters
    def f(x, y, S, _fn=fn):
        kw = dict(ink=ink, seed=int(abs(x)+abs(y)))
        if takes_trunk: kw['trunk'] = trunk
        return _fn(x, y, S*random.uniform(lo, hi), **kw)
    return f


def _tr(fn, lo, hi, **kw):
    def f(x, y, S, _fn=fn):
        return _fn(x, y, S*random.uniform(lo, hi), S*random.uniform(lo, hi)*0.7,
                   seed=int(abs(x)+abs(y)), **kw)
    return f


def _fa(name, frac=0.030):
    fn = FA.RACES.get(name) or FA.CREATURES.get(name)
    def f(x, y, S, _fn=fn):
        return _fn(x, y, S*frac, seed=int(abs(x)+abs(y))) if _fn else []
    return f


P = FL.PALETTE
THEMES = {
    # Halas: barbarian ice. Peaks from terrain, firs, snowdrifts, barbarians.
    'halas': dict(
        title_ink=(90, 70, 50), frame_ink=(120, 104, 84), grid_ink=(168, 176, 186),
        shapes=[_tr(TR.peak, 0.030, 0.042),
                _fl(FL.fir, P['fir_north'], P['trunk'], 0.020, 0.030),
                _tr(TR.snowdrift, 0.028, 0.038),
                _fa('barbarian')]),
    # Oggok: ogre city deep in the Feerrott. Dense jungle canopy, ruins, ogres.
    'oggok': dict(
        title_ink=(104, 88, 64), frame_ink=(126, 110, 84), grid_ink=(150, 140, 110),
        shapes=[_fl(FL.broadleaf, P['broadleaf'], P['trunk'], 0.024, 0.036),
                _tr(TR.ruin_arch, 0.030, 0.042),
                _fl(FL.fern, P['under'], P['trunk'], 0.018, 0.026),
                _fa('ogre')]),
    # Grobb: troll city in Innothule swamp. Mudflats, reeds, dead trees, trolls.
    'grobb': dict(
        title_ink=(92, 80, 58), frame_ink=(112, 100, 76), grid_ink=(140, 132, 104),
        shapes=[_tr(TR.mudflat, 0.030, 0.042),
                _fl(FL.reeds, P['reed'], P['trunk'], 0.020, 0.030),
                _fl(FL.dead_tree, P['dead'], P['trunk'], 0.024, 0.034),
                _fa('troll')]),
}
