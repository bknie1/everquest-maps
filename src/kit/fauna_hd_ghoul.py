"""fauna_hd_ghoul.py -- high-fidelity ghoul for the Estate of Unrest interior.

Shadowy, goblin-like rigging per Brandon's in-game read: a low crouch on bent
haunches, oversized head with tall ears, long arms with claws splayed to the
floor. Built from closed part polygons with even-odd hatch and a darker shadow
side (troll_hd / bookshelf method). ~80-120 strokes.

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


def _outline(poly, ink, rnd, jitter):
    out = []
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        out.append((x1, y1 + rnd.uniform(-jitter, jitter),
                    x2, y2 + rnd.uniform(-jitter, jitter), ink))
    return out


def _part(poly, ink, dark, step, rnd, shade_frac=0.45):
    j = step * 0.18
    out = _outline(poly, ink, rnd, j * 0.6)
    xs = [p[0] for p in poly]
    cut = min(xs) + (max(xs) - min(xs)) * (1.0 - shade_frac)
    for (x1, y1, x2, y2, c) in _hatch(poly, ink, step, j, rnd):
        out.append((x1, y1, x2, y2, dark if (x1 + x2) * 0.5 > cut else c))
    return out


def ghoul(cx, cy, s, seed=0, face=-1):
    """A crouched ghoul. (cx, cy) = ground under it, s = crouched height."""
    rnd = random.Random(seed)
    f = -1 if face < 0 else 1
    step = max(0.8, s * 0.06)
    out = []

    def X(x):
        return cx + f * x

    # crouched body: a low wedge, spine arched high at the haunches
    body = [(X(-s*0.30), cy - s*0.42), (X(-s*0.12), cy - s*0.58),
            (X(s*0.10), cy - s*0.66), (X(s*0.30), cy - s*0.58),
            (X(s*0.38), cy - s*0.38), (X(s*0.30), cy - s*0.18),
            (X(s*0.10), cy - s*0.12), (X(-s*0.16), cy - s*0.16),
            (X(-s*0.28), cy - s*0.28)]
    out += _part(body, HIDE, DARK, step, rnd, shade_frac=0.55)
    # knobbed spine ridge
    for k in range(4):
        t = k / 3.0
        sx = X(-s*0.10 + s*0.36 * t)
        sy = cy - s*(0.60 + 0.06 * (1 - abs(2 * t - 1)))
        out.append((sx, sy, sx + f*s*0.03, sy - s*0.035, DARK))

    # oversized head thrust forward, underslung jaw
    head = [(X(-s*0.30), cy - s*0.56), (X(-s*0.44), cy - s*0.60),
            (X(-s*0.54), cy - s*0.52), (X(-s*0.50), cy - s*0.40),
            (X(-s*0.38), cy - s*0.36), (X(-s*0.28), cy - s*0.44)]
    out += _part(head, HIDE, DARK, step * 0.8, rnd, shade_frac=0.35)
    # goblin ears: short, ragged, swept flat back along the skull
    out.append((X(-s*0.30), cy - s*0.58, X(-s*0.16), cy - s*0.66, HIDE))
    out.append((X(-s*0.16), cy - s*0.66, X(-s*0.24), cy - s*0.57, DARK))
    out.append((X(-s*0.38), cy - s*0.60, X(-s*0.26), cy - s*0.665, HIDE))
    out.append((X(-s*0.26), cy - s*0.665, X(-s*0.33), cy - s*0.585, DARK))
    # jaw + teeth
    out.append((X(-s*0.52), cy - s*0.40, X(-s*0.42), cy - s*0.33, HIDE))
    out.append((X(-s*0.42), cy - s*0.33, X(-s*0.34), cy - s*0.36, HIDE))
    for k in range(2):
        tx = X(-s*(0.44 + 0.04 * k))
        out.append((tx, cy - s*0.37, tx - f*s*0.012, cy - s*0.33, CLAW))
    # sunken eye
    out.append((X(-s*0.44), cy - s*0.52, X(-s*0.40), cy - s*0.51, DARK))

    # near arm: long, down to splayed claws
    arm = [(X(-s*0.22), cy - s*0.46), (X(-s*0.32), cy - s*0.28),
           (X(-s*0.38), cy - s*0.08), (X(-s*0.34), cy - s*0.02),
           (X(-s*0.28), cy - s*0.16), (X(-s*0.18), cy - s*0.36)]
    out += _part(arm, HIDE, DARK, step, rnd, shade_frac=0.4)
    for k in range(3):
        fx = X(-s*(0.30 + 0.05 * k))
        out.append((fx, cy - s*0.03, fx - f*s*0.035, cy, CLAW))

    # far arm hinted behind, darker
    out.append((X(-s*0.06), cy - s*0.40, X(-s*0.14), cy - s*0.18, DARK))
    out.append((X(-s*0.14), cy - s*0.18, X(-s*0.12), cy - s*0.03, DARK))
    out.append((X(-s*0.12), cy - s*0.03, X(-s*0.17), cy, DARK))

    # haunch leg folded under, big foot
    leg = [(X(s*0.16), cy - s*0.36), (X(s*0.30), cy - s*0.30),
           (X(s*0.32), cy - s*0.14), (X(s*0.20), cy - s*0.04),
           (X(s*0.06), cy - s*0.02), (X(s*0.06), cy - s*0.12),
           (X(s*0.14), cy - s*0.22)]
    out += _part(leg, HIDE, DARK, step, rnd, shade_frac=0.6)
    out.append((X(s*0.06), cy - s*0.02, X(-s*0.06), cy, HIDE))
    for k in range(2):
        fx = X(-s*0.02 - s*0.045 * k)
        out.append((fx, cy, fx - f*s*0.03, cy + s*0.01, CLAW))
    return out
