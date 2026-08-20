"""fauna_hd_gnoll.py -- high-fidelity gnoll for Blackburrow / Splitpaw zones.

The fauna.py gnoll is a stick figure. This is a side-view hyena-folk warrior
built the way the other HD fauna are (closed part polygons, even-odd hatched
fill, a darker shadow side, real anatomy): digitigrade legs, a sloped hyena back
with a bristling neck crest, upright tufted ears, a long snouted muzzle, a
drooping tail, spotted shoulders, and a raised spear.  100-300 strokes.

    from fauna_hd_gnoll import gnoll
    segs = gnoll(cx, cy, s, seed=3)      # (cx, cy) = feet, s = height
    segs = gnoll(cx, cy, s, face=1)      # face right
"""
import random

SKIN = (120, 102, 74)        # gnoll fur (matches fauna PALETTE['gnoll'])
DARK = (86, 72, 50)          # shadow / spots
CLOTH = (96, 76, 52)
BONE = (150, 142, 120)       # spear shaft / tusks


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


def _part(poly, ink, dark, step, rnd, shade_from=None):
    j = step * 0.18
    out = _outline(poly, ink, rnd, j * 0.6)
    if shade_from is None:
        out += _hatch(poly, ink, step, j, rnd)
    else:
        lit = [(min(x, shade_from), y) for x, y in poly]
        shd = [(max(x, shade_from), y) for x, y in poly]
        out += _hatch(lit, ink, step, j, rnd)
        out += _hatch(shd, dark, step * 0.82, j, rnd)
    return out


def gnoll(cx, cy, s, ink=None, seed=0, face=-1):
    """Side-view gnoll. (cx, cy) = point between the feet, s = full height.
    face=-1 looks left (default), face=1 looks right."""
    rnd = random.Random(seed)
    ink = ink or SKIN
    dark = DARK
    f = face

    def P(pts):
        return [(cx + f * x * s, cy - y * s) for x, y in pts]

    def seg(x1, y1, x2, y2, c):
        out.append((cx + f * x1 * s, cy - y1 * s, cx + f * x2 * s, cy - y2 * s, c))

    step = s * 0.050
    out = []

    # rear leg (shadow) -- digitigrade: thigh, back-bent hock, paw
    rear_leg = P([(0.10, 0.50), (0.20, 0.46), (0.22, 0.30), (0.28, 0.16),
                  (0.24, 0.05), (0.31, 0.02), (0.32, 0.00), (0.16, 0.00),
                  (0.15, 0.06), (0.17, 0.16), (0.12, 0.30)])
    out += _part(rear_leg, dark, dark, step * 0.9, rnd)

    # rear arm (shadow) at the side
    rear_arm = P([(-0.04, 0.70), (0.05, 0.66), (0.06, 0.48), (0.04, 0.32),
                  (0.09, 0.30), (0.10, 0.48), (0.02, 0.64)])
    out += _part(rear_arm, dark, dark, step * 0.85, rnd)

    # front leg -- digitigrade, splayed paw with claws
    front_leg = P([(-0.10, 0.50), (0.00, 0.48), (0.02, 0.30), (-0.04, 0.16),
                   (-0.10, 0.05), (-0.17, 0.02), (-0.18, 0.00), (-0.02, 0.00),
                   (-0.01, 0.06), (0.01, 0.16), (-0.04, 0.30)])
    out += _part(front_leg, ink, dark, step, rnd, shade_from=cx + f * s * 0.0)
    for k in range(3):                                   # claws
        tx = -0.16 - 0.028 * k
        seg(tx, 0.02, tx - 0.03, 0.005, ink)

    # tail -- thick, drooping down behind
    tail = P([(0.18, 0.52), (0.28, 0.50), (0.36, 0.40), (0.40, 0.26),
              (0.36, 0.24), (0.31, 0.36), (0.24, 0.46), (0.18, 0.48)])
    out += _part(tail, dark, dark, step * 0.8, rnd)

    # torso -- sloped hyena back: shoulder HIGH forward, hip LOW rear
    torso = P([(-0.14, 0.50), (-0.18, 0.64), (-0.16, 0.78), (-0.06, 0.84),
               (0.06, 0.80), (0.16, 0.68), (0.19, 0.56), (0.16, 0.48),
               (0.06, 0.44), (-0.06, 0.45)])
    out += _part(torso, ink, dark, step, rnd, shade_from=cx + f * s * 0.02)

    # bristling neck/back crest (hyena mane) -- tufts along the spine
    crest = [(-0.14, 0.80), (-0.08, 0.855), (0.00, 0.85), (0.07, 0.81),
             (0.13, 0.72), (0.17, 0.62)]
    for x, y in crest:
        seg(x, y, x + 0.02, y + 0.045, dark)
        seg(x, y, x - 0.015, y + 0.04, dark)

    # spots on the shoulder (lit side)
    for k in range(7):
        wx = rnd.uniform(-0.10, 0.12)
        wy = rnd.uniform(0.50, 0.76)
        seg(wx, wy, wx - 0.018, wy - 0.006, dark)

    # neck -- rises forward off the high shoulder
    neck = P([(-0.14, 0.72), (-0.22, 0.78), (-0.26, 0.82), (-0.22, 0.74),
              (-0.15, 0.66)])
    out += _part(neck, ink, dark, step * 0.85, rnd)

    # head + long muzzle jutting forward
    head = P([(-0.20, 0.78), (-0.28, 0.84), (-0.36, 0.83), (-0.42, 0.79),
              (-0.50, 0.775), (-0.52, 0.75), (-0.44, 0.745), (-0.36, 0.74),
              (-0.28, 0.745), (-0.22, 0.72)])
    out += _part(head, ink, dark, step * 0.75, rnd, shade_from=cx - f * s * 0.30)
    # lower jaw / underbite
    jaw = P([(-0.36, 0.745), (-0.50, 0.745), (-0.505, 0.725), (-0.44, 0.72),
             (-0.36, 0.725)])
    out += _part(jaw, ink, dark, step * 0.7, rnd)
    seg(-0.46, 0.745, -0.47, 0.762, BONE)                # a small tusk
    # snout ridge + nose
    seg(-0.30, 0.83, -0.50, 0.775, dark)
    seg(-0.50, 0.775, -0.515, 0.762, dark)
    # eye + brow
    seg(-0.28, 0.80, -0.315, 0.795, dark)
    seg(-0.265, 0.815, -0.30, 0.812, dark)
    # two upright tufted ears
    ear1 = P([(-0.22, 0.83), (-0.20, 0.90), (-0.15, 0.91), (-0.17, 0.83)])
    out += _part(ear1, ink, dark, step * 0.7, rnd)
    ear2 = P([(-0.16, 0.84), (-0.13, 0.925), (-0.08, 0.92), (-0.12, 0.83)])
    out += _part(ear2, ink, dark, step * 0.7, rnd)

    # front arm -- raised, gripping a spear
    front_arm = P([(-0.12, 0.70), (-0.22, 0.66), (-0.30, 0.72), (-0.34, 0.80),
                   (-0.30, 0.82), (-0.26, 0.74), (-0.20, 0.70), (-0.12, 0.66)])
    out += _part(front_arm, ink, dark, step, rnd, shade_from=cx - f * s * 0.20)
    for k in range(3):                                   # gripping fingers
        kx = -0.32 - 0.015 * k
        seg(kx, 0.80, kx - 0.01, 0.83, ink)

    # spear -- long shaft through the fist, leaf blade up
    seg(-0.30, 0.60, -0.36, 1.02, BONE)
    seg(-0.36, 1.02, -0.33, 1.10, ink)                   # blade
    seg(-0.36, 1.02, -0.39, 1.10, ink)
    seg(-0.33, 1.10, -0.39, 1.10, ink)
    seg(-0.30, 0.60, -0.285, 0.54, BONE)                 # butt of the shaft

    # loincloth over the hips
    cloth = P([(-0.08, 0.48), (0.14, 0.50), (0.16, 0.36), (0.10, 0.40),
               (0.04, 0.33), (-0.02, 0.39), (-0.06, 0.34)])
    out += _outline(cloth, CLOTH, rnd, step * 0.1)
    out += _hatch(cloth, CLOTH, step * 0.7, step * 0.12, rnd)

    return out


if __name__ == "__main__":
    for sd in range(4):
        print("seed", sd, len(gnoll(0, 0, 100, seed=sd)), "strokes")
