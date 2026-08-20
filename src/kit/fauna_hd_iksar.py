"""fauna_hd_iksar.py -- high-fidelity Iksar / lizardman for Cazic-Thule, Cabilis.

Side-view reptilian biped built like the other HD fauna (closed part polygons,
even-odd hatched fill, a darker shadow side): upright but forward-leaning, a
counter-balancing tail, a row of back spines, a long snouted head with a low
brow, digitigrade clawed legs, and a levelled spear. 100-260 strokes.

    from fauna_hd_iksar import iksar
    segs = iksar(cx, cy, s, seed=3)      # (cx, cy) = feet, s = height
    segs = iksar(cx, cy, s, face=1)      # face right
"""
import random

SCALE = (92, 96, 86)         # iksar green-grey (fauna PALETTE['iksar'])
DARK = (60, 66, 56)          # shadow / scales
BONE = (150, 142, 120)       # spear / claws


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
    j = step * 0.17
    out = _outline(poly, ink, rnd, j * 0.6)
    if shade_from is None:
        out += _hatch(poly, ink, step, j, rnd)
    else:
        lit = [(min(x, shade_from), y) for x, y in poly]
        shd = [(max(x, shade_from), y) for x, y in poly]
        out += _hatch(lit, ink, step, j, rnd)
        out += _hatch(shd, dark, step * 0.82, j, rnd)
    return out


def iksar(cx, cy, s, ink=None, seed=0, face=-1):
    """Side-view iksar. (cx, cy) = feet, s = full height. face=-1 looks left."""
    rnd = random.Random(seed)
    ink = ink or SCALE
    dark = DARK
    f = face

    def P(pts):
        return [(cx + f * x * s, cy - y * s) for x, y in pts]

    def seg(x1, y1, x2, y2, c):
        out.append((cx + f * x1 * s, cy - y1 * s, cx + f * x2 * s, cy - y2 * s, c))

    step = s * 0.052
    out = []

    # long tail -- thick root at the hips, tapering back and down for balance
    tail = P([(0.14, 0.48), (0.28, 0.44), (0.44, 0.34), (0.58, 0.18),
              (0.64, 0.06), (0.60, 0.04), (0.50, 0.16), (0.36, 0.30),
              (0.22, 0.40), (0.14, 0.42)])
    out += _part(tail, ink, dark, step * 0.9, rnd, shade_from=cx + f * s * 0.3)

    # rear leg (shadow) -- digitigrade
    rear_leg = P([(0.08, 0.46), (0.18, 0.42), (0.20, 0.26), (0.26, 0.12),
                  (0.22, 0.04), (0.30, 0.02), (0.31, 0.00), (0.15, 0.00),
                  (0.14, 0.06), (0.16, 0.14), (0.10, 0.28)])
    out += _part(rear_leg, dark, dark, step * 0.9, rnd)
    # front leg -- digitigrade, splayed claws
    front_leg = P([(-0.08, 0.46), (0.02, 0.44), (0.03, 0.26), (-0.03, 0.12),
                   (-0.10, 0.04), (-0.17, 0.02), (-0.18, 0.00), (-0.02, 0.00),
                   (-0.01, 0.06), (0.01, 0.14), (-0.04, 0.28)])
    out += _part(front_leg, ink, dark, step, rnd, shade_from=cx)
    for k in range(3):
        tx = -0.16 - 0.028 * k
        seg(tx, 0.02, tx - 0.03, 0.005, ink)

    # torso -- forward-leaning, deep chest
    torso = P([(-0.12, 0.48), (-0.18, 0.60), (-0.16, 0.72), (-0.06, 0.78),
               (0.06, 0.74), (0.15, 0.62), (0.17, 0.52), (0.12, 0.46),
               (0.02, 0.44), (-0.06, 0.45)])
    out += _part(torso, ink, dark, step, rnd, shade_from=cx + f * s * 0.02)
    # row of back spines along the spine
    spine = [(-0.15, 0.70), (-0.08, 0.76), (0.00, 0.75), (0.08, 0.70), (0.14, 0.62)]
    for x, y in spine:
        seg(x, y, x - 0.03, y + 0.06, dark)
        seg(x, y, x + 0.01, y + 0.05, dark)
    for k in range(6):                                   # scale ticks
        wx = rnd.uniform(-0.08, 0.10); wy = rnd.uniform(0.48, 0.68)
        seg(wx, wy, wx - 0.02, wy - 0.006, dark)

    # neck + long low reptilian head, snout forward
    neck = P([(-0.13, 0.70), (-0.22, 0.74), (-0.26, 0.72), (-0.18, 0.64),
              (-0.12, 0.62)])
    out += _part(neck, ink, dark, step * 0.85, rnd)
    head = P([(-0.22, 0.74), (-0.30, 0.775), (-0.40, 0.76), (-0.48, 0.72),
              (-0.55, 0.695), (-0.565, 0.675), (-0.48, 0.67), (-0.38, 0.675),
              (-0.30, 0.685), (-0.22, 0.70)])
    out += _part(head, ink, dark, step * 0.72, rnd, shade_from=cx - f * s * 0.34)
    jaw = P([(-0.38, 0.675), (-0.55, 0.675), (-0.555, 0.655), (-0.46, 0.655),
             (-0.38, 0.66)])
    out += _part(jaw, ink, dark, step * 0.65, rnd)
    seg(-0.30, 0.775, -0.55, 0.695, dark)                # snout ridge
    seg(-0.28, 0.745, -0.32, 0.738, dark)                # eye
    seg(-0.52, 0.67, -0.535, 0.63, BONE)                 # a fang
    # a couple of small head frills swept back
    for k in range(2):
        seg(-0.22 + 0.03 * k, 0.755, -0.13 + 0.03 * k, 0.80, dark)

    # front arm -- levels a spear forward
    front_arm = P([(-0.10, 0.68), (-0.20, 0.62), (-0.28, 0.60), (-0.30, 0.58),
                   (-0.22, 0.56), (-0.14, 0.60), (-0.08, 0.64)])
    out += _part(front_arm, ink, dark, step * 0.85, rnd, shade_from=cx - f * s * 0.16)
    seg(-0.30, 0.59, -0.62, 0.55, BONE)                  # spear shaft
    seg(-0.62, 0.55, -0.70, 0.575, ink)                  # spear head
    seg(-0.62, 0.55, -0.70, 0.525, ink)
    seg(-0.70, 0.575, -0.70, 0.525, ink)

    return out


if __name__ == "__main__":
    for sd in range(4):
        print("seed", sd, len(iksar(0, 0, 100, seed=sd)), "strokes")
