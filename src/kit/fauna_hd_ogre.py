"""fauna_hd_ogre.py -- high-fidelity side-view ogre (New Sebilis bar).

The fauna.py ogre is a ~20-line front-view stick figure. This one is a proper
side profile at flora_hd fidelity: hatched fill, massive rounded shoulders and
gut, stubby legs, small head jutting forward off the slab of the back, one
heavy arm carrying a club, a darker shadow side along the trailing edge.
100-300 strokes depending on scale.

    hd_ogre(cx, cy, s, seed=0, flip=False)

cy is the GROUND line (feet); the body rises above it. flip=True faces left.
"""
import math, random

HIDE = (110, 96, 66)          # weathered hide / leathers
DARK = (78, 66, 46)           # shadow side


def _hatch(poly, ink, step):
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
            if xs[i + 1] - xs[i] > 0.6:
                out.append((xs[i], y, xs[i + 1], y, ink))
        y += step
    return out


def _outline(poly, ink, close=True):
    n = len(poly)
    rng = range(n) if close else range(n - 1)
    return [(poly[i][0], poly[i][1], poly[(i + 1) % n][0],
             poly[(i + 1) % n][1], ink) for i in rng]


def _blob(pts, wob, rnd):
    return [(x + rnd.uniform(-wob, wob), y + rnd.uniform(-wob, wob))
            for x, y in pts]


def hd_ogre(cx, cy, s, ink=HIDE, dark=DARK, seed=0, flip=False):
    """Side-view ogre. s ~ overall height. Facing right unless flip."""
    rnd = random.Random(seed)
    out = []
    f = -1.0 if flip else 1.0
    P = lambda x, y: (cx + x * s * f, cy + y * s)

    # ---- body slab: hunched back, massive shoulder hump, gut, seat
    body = [P(-0.02, 0.00),            # rear foot root
            P(-0.30, -0.02),           # heel of rear leg
            P(-0.34, -0.28),           # rump
            P(-0.38, -0.52),           # low back
            P(-0.33, -0.74),           # hunched upper back
            P(-0.20, -0.88),           # shoulder hump rise
            P(0.02, -0.94),            # top of shoulder mass
            P(0.18, -0.88),            # front shoulder slope
            P(0.26, -0.72),            # chest
            P(0.33, -0.50),            # gut swell
            P(0.36, -0.34),            # belly point
            P(0.30, -0.16),            # under-belly tuck
            P(0.22, -0.02),            # front foot root
            ]
    body = _blob(body, s * 0.012, rnd)
    out += _outline(body, ink)
    out += _hatch(body, ink, s * 0.052)
    # shadow: rear/lower third hatched darker (sun from the northwest)
    shadow = [P(-0.30, -0.02), P(-0.34, -0.28), P(-0.38, -0.52),
              P(-0.33, -0.74), P(-0.20, -0.88), P(-0.16, -0.60),
              P(-0.12, -0.30), P(-0.10, -0.02)]
    out += _hatch(_blob(shadow, s * 0.008, rnd), dark, s * 0.075)

    # ---- head: small, jutting forward low off the hump, heavy jaw
    head = [P(0.16, -0.86), P(0.24, -0.95), P(0.36, -0.97), P(0.44, -0.92),
            P(0.46, -0.84), P(0.42, -0.77), P(0.30, -0.74), P(0.20, -0.78)]
    head = _blob(head, s * 0.008, rnd)
    out += _outline(head, ink)
    out += _hatch(head, ink, s * 0.045)
    # brow, eye pit, tusk
    out.append((*P(0.34, -0.92), *P(0.43, -0.89), dark))
    out.append((*P(0.385, -0.875), *P(0.405, -0.865), dark))
    out.append((*P(0.44, -0.79), *P(0.475, -0.83), ink))   # up-tusk
    out.append((*P(0.475, -0.83), *P(0.465, -0.86), ink))
    # ear nub
    out.append((*P(0.20, -0.90), *P(0.17, -0.94), dark))

    # ---- near arm: hangs heavy, gripping a club head-down
    arm = [P(0.10, -0.80), P(0.20, -0.66), P(0.26, -0.46), P(0.30, -0.30),
           P(0.24, -0.24), P(0.16, -0.36), P(0.10, -0.54), P(0.04, -0.72)]
    arm = _blob(arm, s * 0.008, rnd)
    out += _outline(arm, ink)
    out += _hatch(arm, ink, s * 0.055)
    # fist
    fist = [P(0.30, -0.30), P(0.36, -0.28), P(0.37, -0.21), P(0.30, -0.19),
            P(0.26, -0.24)]
    out += _outline(_blob(fist, s * 0.006, rnd), ink)
    # club: thick end down-forward
    out.append((*P(0.30, -0.26), *P(0.52, -0.10), ink))
    out.append((*P(0.34, -0.30), *P(0.56, -0.14), ink))
    clubhead = [P(0.52, -0.10), P(0.62, -0.06), P(0.64, 0.00), P(0.58, 0.02),
                P(0.50, -0.02), P(0.56, -0.14)]
    clubhead = _blob(clubhead, s * 0.006, rnd)
    out += _outline(clubhead, ink)
    out += _hatch(clubhead, dark, s * 0.045)

    # ---- legs: stubby trunks with big flat feet
    for lx, shade in ((-0.24, True), (0.10, False)):
        leg = [P(lx - 0.07, -0.16), P(lx - 0.08, -0.04), P(lx - 0.10, 0.00),
               P(lx + 0.12, 0.00), P(lx + 0.09, -0.04), P(lx + 0.08, -0.16)]
        leg = _blob(leg, s * 0.006, rnd)
        out += _outline(leg, ink, close=False)
        out += _hatch(leg, dark if shade else ink, s * 0.05)
        # toes
        out.append((*P(lx + 0.12, 0.00), *P(lx + 0.15, -0.025), ink))
    # ground shadow
    out.append((*P(-0.34, 0.02), *P(0.30, 0.02), dark))
    out.append((*P(-0.26, 0.045), *P(0.20, 0.045), dark))

    # ---- hide texture: short scar ticks across the flank
    for k in range(6):
        tx = rnd.uniform(-0.26, 0.18); ty = rnd.uniform(-0.66, -0.24)
        out.append((*P(tx, ty), *P(tx + 0.045, ty + 0.02), dark))
    # shoulder plate strap
    out.append((*P(-0.06, -0.92), *P(0.20, -0.60), dark))
    out.append((*P(-0.09, -0.89), *P(0.17, -0.57), dark))
    return out
