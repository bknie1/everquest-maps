"""fauna_hd_troll.py -- high-fidelity troll for Grobb, New Sebilis fidelity.

The fauna.py troll is ~16 strokes and reads as a stick figure. This one is a
side-view figure built the way the shapes that read well are built (bookshelf,
root_bunch, flora_hd): closed part polygons, even-odd hatched fill, a darker
shadow side on the trailing half, and real internal structure -- hunched spine,
long knuckle-dragging arms, jutting underbite jaw with tusks up, tattered
loincloth. 100-300 strokes at any scale.

    from fauna_hd_troll import troll
    segs = troll(cx, cy, s, seed=3)          # (cx, cy) = feet, s = height
    segs = troll(cx, cy, s, face=1)          # face right instead of left
"""
import math
import random

SKIN = (74, 92, 62)          # troll green (matches fauna PALETTE['troll'])
DARK = (52, 66, 44)          # shadow side
CLOTH = (86, 70, 52)


def _hatch(poly, ink, step, jitter, rnd):
    """Even-odd horizontal hatch of a polygon, with a little hand wobble."""
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
    """Outline + hatch. shade_from: x past which hatch flips to the dark ink
    (the trailing / shadow half of the part)."""
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


def troll(cx, cy, s, ink=None, seed=0, face=-1):
    """Side-view troll. (cx, cy) = point between the feet, s = full height.
    face=-1 looks left (default), face=1 looks right."""
    rnd = random.Random(seed)
    ink = ink or SKIN
    dark = DARK
    f = face

    def P(pts):
        return [(cx + f * x * s, cy - y * s) for x, y in pts]

    step = s * 0.052
    out = []

    # rear leg (shadow side) -- bent crouch, big flat foot
    rear_leg = P([(0.10, 0.40), (0.22, 0.36), (0.20, 0.20), (0.28, 0.06),
                  (0.34, 0.02), (0.33, 0.00), (0.14, 0.00), (0.13, 0.16),
                  (0.06, 0.28)])
    out += _part(rear_leg, dark, dark, step * 0.9, rnd)

    # rear arm (shadow side) -- from the hump down past the hip
    rear_arm = P([(0.10, 0.68), (0.20, 0.62), (0.22, 0.40), (0.26, 0.18),
                  (0.30, 0.06), (0.24, 0.04), (0.18, 0.20), (0.13, 0.42)])
    out += _part(rear_arm, dark, dark, step * 0.9, rnd)

    # front leg -- bent the other way, toes splayed
    front_leg = P([(-0.08, 0.40), (0.06, 0.38), (0.02, 0.22), (-0.06, 0.08),
                   (-0.16, 0.02), (-0.17, 0.00), (0.02, 0.00), (0.05, 0.12),
                   (0.10, 0.26)])
    out += _part(front_leg, ink, dark, step, rnd, shade_from=cx + f * s * 0.04)
    for k in range(3):                                    # toes
        tx = -0.16 - 0.025 * k
        out.append((cx + f * tx * s, cy - 0.02 * s,
                    cx + f * (tx - 0.03) * s, cy - 0.005 * s, ink))

    # torso -- the hump is the silhouette: shoulder low, spine arched high
    torso = P([(-0.12, 0.44), (-0.16, 0.58), (-0.12, 0.70), (-0.02, 0.80),
               (0.10, 0.82), (0.20, 0.74), (0.24, 0.60), (0.22, 0.46),
               (0.14, 0.38), (0.00, 0.36)])
    out += _part(torso, ink, dark, step, rnd, shade_from=cx + f * s * 0.08)
    # spine knobs along the hump
    spine = [(-0.10, 0.72), (-0.02, 0.79), (0.06, 0.815), (0.14, 0.79),
             (0.20, 0.72)]
    for x, y in spine:
        out.append((cx + f * x * s, cy - y * s,
                    cx + f * x * s, cy - (y + 0.025) * s, dark))
    # belly sag crease
    out.append((cx - f * 0.10 * s, cy - 0.46 * s,
                cx + f * 0.06 * s, cy - 0.40 * s, dark))

    # head -- juts FORWARD off the low shoulder, underbite leads
    head = P([(-0.12, 0.70), (-0.20, 0.74), (-0.30, 0.73), (-0.36, 0.68),
              (-0.35, 0.63), (-0.44, 0.60), (-0.42, 0.56), (-0.28, 0.55),
              (-0.18, 0.58), (-0.12, 0.62)])
    out += _part(head, ink, dark, step * 0.8, rnd, shade_from=cx - f * s * 0.16)
    # jutting lower jaw, wider than the skull
    jaw = P([(-0.30, 0.55), (-0.48, 0.565), (-0.50, 0.60), (-0.44, 0.60),
             (-0.35, 0.585)])
    out += _part(jaw, ink, dark, step * 0.7, rnd)
    # tusks -- up from the jaw
    out.append((cx - f * 0.47 * s, cy - 0.60 * s, cx - f * 0.485 * s, cy - 0.665 * s, ink))
    out.append((cx - f * 0.485 * s, cy - 0.665 * s, cx - f * 0.475 * s, cy - 0.67 * s, ink))
    out.append((cx - f * 0.41 * s, cy - 0.60 * s, cx - f * 0.425 * s, cy - 0.65 * s, ink))
    # nose -- long, hooked over the jaw
    out.append((cx - f * 0.36 * s, cy - 0.66 * s, cx - f * 0.455 * s, cy - 0.635 * s, ink))
    out.append((cx - f * 0.455 * s, cy - 0.635 * s, cx - f * 0.44 * s, cy - 0.615 * s, ink))
    # eye pit + brow shelf
    out.append((cx - f * 0.315 * s, cy - 0.685 * s, cx - f * 0.36 * s, cy - 0.675 * s, dark))
    out.append((cx - f * 0.30 * s, cy - 0.665 * s, cx - f * 0.33 * s, cy - 0.66 * s, dark))
    # long pointed ear swept back
    ear = P([(-0.13, 0.71), (-0.04, 0.76), (0.02, 0.74), (-0.08, 0.68)])
    out += _part(ear, ink, dark, step * 0.8, rnd)

    # front arm -- LONG, knuckles at the ground
    front_arm = P([(-0.14, 0.66), (-0.24, 0.60), (-0.28, 0.42), (-0.30, 0.22),
                   (-0.34, 0.06), (-0.26, 0.03), (-0.22, 0.20), (-0.18, 0.40),
                   (-0.10, 0.56)])
    out += _part(front_arm, ink, dark, step, rnd, shade_from=cx - f * s * 0.20)
    # dangling claw fingers off the knuckle
    for k in range(3):
        kx, ky = -0.335 + 0.028 * k, 0.055
        out.append((cx + f * kx * s, cy - ky * s,
                    cx + f * (kx + 0.012) * s, cy - (ky - 0.05) * s, ink))
    # elbow / muscle creases
    out.append((cx - f * 0.25 * s, cy - 0.55 * s, cx - f * 0.21 * s, cy - 0.50 * s, dark))
    out.append((cx - f * 0.27 * s, cy - 0.33 * s, cx - f * 0.24 * s, cy - 0.30 * s, dark))

    # tattered loincloth over the hips
    cloth = P([(-0.10, 0.42), (0.16, 0.44), (0.18, 0.30), (0.12, 0.34),
               (0.06, 0.27), (0.00, 0.33), (-0.06, 0.28)])
    out += _outline(cloth, CLOTH, rnd, step * 0.1)
    out += _hatch(cloth, CLOTH, step * 0.7, step * 0.12, rnd)

    # warts / hide ticks on the lit side
    for k in range(6):
        wx = cx + f * rnd.uniform(-0.10, 0.16) * s
        wy = cy - rnd.uniform(0.42, 0.76) * s
        out.append((wx, wy, wx + f * s * 0.012, wy - s * 0.012, dark))

    return out


if __name__ == '__main__':
    for sd in range(4):
        print('seed', sd, len(troll(0, 0, 100, seed=sd)), 'strokes')
