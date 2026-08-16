"""fauna_hd_ghoul.py -- high-fidelity ghoul for the Estate of Unrest interior.

Brandon's round-2 correction: ghouls are LEANER than the first pass -- lanky,
creepy, small. So: a narrow hunched torso with only a whisper of hatch, long
thin single-stroke limbs with knobbed joints, oversized head on a craned neck,
and long splayed fingers. Draw them SMALLER than the zombies (s ~ 9-11 where
zombies are 15-16). ~55-75 strokes.

    from fauna_hd_ghoul import ghoul
    segs = ghoul(cx, cy, s, seed=1)       # (cx, cy) = ground, s = crouch height
    segs = ghoul(cx, cy, s, face=1)       # face right
"""
import random

HIDE = (86, 80, 94)          # shadowy grey-violet
DARK = (58, 54, 66)
CLAW = (120, 114, 124)


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


def _poly(pts, ink, close=False):
    n = len(pts) if close else len(pts) - 1
    return [(pts[i][0], pts[i][1], pts[(i + 1) % len(pts)][0],
             pts[(i + 1) % len(pts)][1], ink) for i in range(n)]


def _limb(pts, ink, dark):
    """A thin limb: one clean stroke chain plus a broken shadow strand and
    knob ticks at the joints."""
    out = _poly(pts, ink)
    for i in range(1, len(pts) - 1):
        jx, jy = pts[i]
        out.append((jx - 0.4, jy - 0.4, jx + 0.4, jy + 0.4, dark))
    if len(pts) >= 3:
        out.append((pts[0][0] + 0.5, pts[0][1] + 0.4,
                    pts[1][0] + 0.5, pts[1][1] + 0.4, dark))
    return out


def ghoul(cx, cy, s, seed=0, face=-1):
    """A lanky crouched ghoul. (cx, cy) = ground under it, s = crouch height."""
    rnd = random.Random(seed)
    f = -1 if face < 0 else 1
    out = []

    def X(x):
        return cx + f * x

    # narrow hunched torso: high arched spine, hollow belly
    spine = [(X(-s*0.26), cy - s*0.50), (X(-s*0.08), cy - s*0.64),
             (X(s*0.14), cy - s*0.68), (X(s*0.30), cy - s*0.56),
             (X(s*0.34), cy - s*0.34)]
    belly = [(X(-s*0.24), cy - s*0.44), (X(-s*0.02), cy - s*0.50),
             (X(s*0.18), cy - s*0.48), (X(s*0.28), cy - s*0.34)]
    out += _poly(spine, HIDE)
    out += _poly(belly, DARK)
    # ribs: three short ticks between the strands
    for k in range(3):
        t = 0.25 + k * 0.22
        sx = X(-s*0.20 + s*0.50 * t)
        out.append((sx, cy - s*(0.52 + 0.08 * (1 - abs(2*t - 1))),
                    sx + f*s*0.02, cy - s*0.46, DARK))
    # knobbed spine ridge
    for k in range(4):
        t = k / 3.0
        sx = X(-s*0.12 + s*0.38 * t)
        sy = cy - s*(0.62 + 0.05 * (1 - abs(2*t - 1)))
        out.append((sx, sy, sx + f*s*0.025, sy - s*0.04, DARK))

    # craned neck + oversized head thrust low and forward
    out.append((X(-s*0.26), cy - s*0.50, X(-s*0.40), cy - s*0.56, HIDE))
    head = [(X(-s*0.40), cy - s*0.62), (X(-s*0.54), cy - s*0.58),
            (X(-s*0.58), cy - s*0.48), (X(-s*0.48), cy - s*0.41),
            (X(-s*0.38), cy - s*0.46), (X(-s*0.37), cy - s*0.56)]
    out += _poly(head, HIDE, close=True)
    out += _hatch(head, DARK, s*0.09, s*0.01, rnd)[:3]
    # ragged swept-back ears
    out.append((X(-s*0.38), cy - s*0.60, X(-s*0.28), cy - s*0.68, HIDE))
    out.append((X(-s*0.28), cy - s*0.68, X(-s*0.34), cy - s*0.59, DARK))
    # narrow jaw + teeth
    out.append((X(-s*0.56), cy - s*0.44, X(-s*0.44), cy - s*0.38, HIDE))
    for k in range(2):
        tx = X(-s*(0.50 + 0.045 * k))
        out.append((tx, cy - s*0.42, tx - f*s*0.01, cy - s*0.38, CLAW))
    # sunken eye
    out.append((X(-s*0.49), cy - s*0.54, X(-s*0.45), cy - s*0.53, DARK))

    # long thin arms, knuckles at the ground, splayed fingers
    out += _limb([(X(-s*0.20), cy - s*0.52), (X(-s*0.34), cy - s*0.30),
                  (X(-s*0.42), cy - s*0.06)], HIDE, DARK)
    for k in range(3):
        fx = X(-s*(0.40 + 0.045 * k))
        out.append((fx, cy - s*0.05, fx - f*s*0.05, cy + s*0.005, CLAW))
    out += _limb([(X(-s*0.02), cy - s*0.50), (X(-s*0.12), cy - s*0.26),
                  (X(-s*0.10), cy - s*0.04)], DARK, DARK)
    for k in range(2):
        fx = X(-s*(0.09 + 0.05 * k))
        out.append((fx, cy - s*0.03, fx - f*s*0.045, cy + s*0.005, DARK))

    # folded haunch legs: thin double-jointed shanks, long feet
    out += _limb([(X(s*0.28), cy - s*0.38), (X(s*0.42), cy - s*0.24),
                  (X(s*0.34), cy - s*0.06), (X(s*0.16), cy - s*0.02)],
                 HIDE, DARK)
    out += _limb([(X(s*0.20), cy - s*0.36), (X(s*0.30), cy - s*0.20),
                  (X(s*0.24), cy - s*0.04)], DARK, DARK)
    # long toes
    for k in range(3):
        fx = X(s*0.16 - f*0 + s*0.0) - f * s*0.02 * k
        out.append((fx, cy - s*0.02, fx - f*s*0.05, cy + s*0.01, CLAW))
    return out
