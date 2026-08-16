"""fauna_hd_zombie.py -- high-fidelity shambling zombie for the Estate of Unrest.

Side-view shambler built the way the shapes that read well are built (troll_hd,
bookshelf, flora_hd): closed part polygons, even-odd hatched fill, a darker
shadow side, real internal structure. Hunched spine pitched far forward, head
lolling, lead arm dragging to the ground, tattered coat hem, stiff-legged step.
~80-150 strokes depending on scale.

    from fauna_hd_zombie import zombie
    segs = zombie(cx, cy, s, seed=3)      # (cx, cy) = feet, s = height
    segs = zombie(cx, cy, s, face=1)      # face right instead of left
"""
import random

SKIN = (112, 116, 92)        # grave-pale green
DARK = (76, 82, 62)          # shadow side / rot
RAGS = (98, 84, 58)          # burial coat


def _hatch(poly, ink, step, jitter, rnd):
    ys = [p[1] for p in poly]
    out = []
    y = min(ys) + step * 0.5
    while y < max(ys):
        xs = []
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            if (y1 > y) != (y2 > y):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > step * 0.4:
                w = rnd.uniform(-jitter, jitter)
                out.append((xs[i] + jitter * 0.3, y + w,
                            xs[i + 1] - jitter * 0.3, y + w, ink))
        y += step
    return out


def _outline(poly, ink, rnd, jitter, close=True):
    out = []
    n = len(poly) if close else len(poly) - 1
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        out.append((x1, y1 + rnd.uniform(-jitter, jitter),
                    x2, y2 + rnd.uniform(-jitter, jitter), ink))
    return out


def _part(poly, ink, dark, step, rnd, shade_frac=0.45):
    """Outline + hatch; the trailing (right) portion hatches in the dark ink."""
    j = step * 0.18
    out = _outline(poly, ink, rnd, j * 0.6)
    xs = [p[0] for p in poly]
    cut = min(xs) + (max(xs) - min(xs)) * (1.0 - shade_frac)
    for (x1, y1, x2, y2, c) in _hatch(poly, ink, step, j, rnd):
        if (x1 + x2) * 0.5 > cut:
            out.append((x1, y1, x2, y2, dark))
        else:
            out.append((x1, y1, x2, y2, c))
    return out


def zombie(cx, cy, s, seed=0, face=-1):
    """A shambling corpse. (cx, cy) = feet centre, s = standing height,
    face=-1 shambles left, face=1 right."""
    rnd = random.Random(seed)
    f = -1 if face < 0 else 1
    step = max(0.9, s * 0.055)
    out = []

    def X(x):                      # mirror helper
        return cx + f * x

    # hunched torso: pitched forward ~40deg, coat over it
    torso = [(X(s*0.10), cy - s*0.28), (X(s*0.02), cy - s*0.52),
             (X(-s*0.06), cy - s*0.68), (X(-s*0.20), cy - s*0.74),
             (X(-s*0.30), cy - s*0.66), (X(-s*0.26), cy - s*0.50),
             (X(-s*0.10), cy - s*0.36), (X(-s*0.02), cy - s*0.26)]
    out += _part(torso, RAGS, DARK, step, rnd, shade_frac=0.5)

    # tattered coat hem: jagged sawtooth below the torso line
    hem = []
    n = 5
    for i in range(n + 1):
        t = i / n
        hx = X(-s*0.02 - s*0.26 * t)
        hy = cy - s*0.26 - s*0.10 * t + (s*0.07 if i % 2 else 0.0)
        hem.append((hx, hy))
    out += _outline(hem, RAGS, rnd, step * 0.1, close=False)

    # lolling head, drooped in front of the chest
    head = [(X(-s*0.26), cy - s*0.80), (X(-s*0.36), cy - s*0.84),
            (X(-s*0.44), cy - s*0.78), (X(-s*0.42), cy - s*0.68),
            (X(-s*0.32), cy - s*0.64), (X(-s*0.25), cy - s*0.70)]
    out += _part(head, SKIN, DARK, step * 0.8, rnd, shade_frac=0.4)
    # slack jaw
    out.append((X(-s*0.42), cy - s*0.68, X(-s*0.36), cy - s*0.61, SKIN))
    out.append((X(-s*0.36), cy - s*0.61, X(-s*0.31), cy - s*0.63, SKIN))
    # dead eye socket
    out.append((X(-s*0.38), cy - s*0.76, X(-s*0.35), cy - s*0.75, DARK))

    # lead arm: dragging, knuckles at the ground
    drag = [(X(-s*0.24), cy - s*0.62), (X(-s*0.34), cy - s*0.42),
            (X(-s*0.38), cy - s*0.20), (X(-s*0.40), cy - s*0.04),
            (X(-s*0.36), cy - s*0.02), (X(-s*0.33), cy - s*0.18),
            (X(-s*0.28), cy - s*0.38), (X(-s*0.18), cy - s*0.56)]
    out += _part(drag, SKIN, DARK, step, rnd, shade_frac=0.35)
    # trailing fingers scraping
    for k in range(3):
        fx = X(-s*(0.36 + 0.03 * k))
        out.append((fx, cy - s*0.03, fx - f*s*0.02, cy + s*0.005, DARK))

    # trailing arm: stiff, half-raised behind
    trail = [(X(0.0), cy - s*0.58), (X(s*0.12), cy - s*0.48),
             (X(s*0.20), cy - s*0.34), (X(s*0.16), cy - s*0.30),
             (X(s*0.07), cy - s*0.44), (X(-s*0.04), cy - s*0.52)]
    out += _part(trail, SKIN, DARK, step, rnd, shade_frac=0.6)

    # legs: stiff shamble, lead leg planted, rear leg toe-dragging
    lead = [(X(-s*0.10), cy - s*0.30), (X(-s*0.20), cy - s*0.16),
            (X(-s*0.22), cy - s*0.02), (X(-s*0.28), cy),
            (X(-s*0.16), cy), (X(-s*0.13), cy - s*0.14),
            (X(-s*0.04), cy - s*0.28)]
    out += _part(lead, RAGS, DARK, step, rnd, shade_frac=0.4)
    rear = [(X(0.02), cy - s*0.28), (X(s*0.10), cy - s*0.16),
            (X(s*0.16), cy - s*0.03), (X(s*0.22), cy - s*0.01),
            (X(s*0.12), cy + s*0.005), (X(s*0.05), cy - s*0.10),
            (X(-s*0.03), cy - s*0.22)]
    out += _part(rear, RAGS, DARK, step, rnd, shade_frac=0.6)

    # a few loose rag wisps trailing off the back
    for k in range(2):
        wy = cy - s * (0.34 + 0.10 * k)
        out.append((X(s*0.08), wy, X(s*(0.16 + 0.04 * k)), wy + s*0.05, RAGS))
    return out
