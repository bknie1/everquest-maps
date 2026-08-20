"""fauna_hd_kobold.py -- high-fidelity kobold for the Warrens / Runnyeye.

Side-view dog-lizard biped built like the other HD fauna (closed part polygons,
even-odd hatched fill, a darker shadow side, real anatomy): short and hunched,
a long down-pointed snout, a backswept spiky head-crest, digitigrade legs, a low
dragging tail, and a mining pick over one shoulder. 100-260 strokes.

    from fauna_hd_kobold import kobold
    segs = kobold(cx, cy, s, seed=3)     # (cx, cy) = feet, s = height
    segs = kobold(cx, cy, s, face=1)     # face right
"""
import random

HIDE = (104, 88, 70)         # kobold hide (matches fauna PALETTE['kobold'])
DARK = (74, 60, 46)          # shadow / scales
BONE = (150, 142, 120)       # pick head / claws


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


def kobold(cx, cy, s, ink=None, seed=0, face=-1):
    """Side-view kobold. (cx, cy) = point between the feet, s = full height.
    face=-1 looks left (default)."""
    rnd = random.Random(seed)
    ink = ink or HIDE
    dark = DARK
    f = face

    def P(pts):
        return [(cx + f * x * s, cy - y * s) for x, y in pts]

    def seg(x1, y1, x2, y2, c):
        out.append((cx + f * x1 * s, cy - y1 * s, cx + f * x2 * s, cy - y2 * s, c))

    step = s * 0.055
    out = []

    # rear leg (shadow) -- digitigrade, short
    rear_leg = P([(0.10, 0.42), (0.20, 0.38), (0.22, 0.24), (0.28, 0.12),
                  (0.24, 0.04), (0.30, 0.02), (0.31, 0.00), (0.16, 0.00),
                  (0.15, 0.05), (0.17, 0.12), (0.12, 0.24)])
    out += _part(rear_leg, dark, dark, step * 0.9, rnd)

    # low dragging tail behind
    tail = P([(0.16, 0.40), (0.30, 0.34), (0.44, 0.22), (0.52, 0.10),
              (0.49, 0.07), (0.40, 0.18), (0.28, 0.28), (0.16, 0.34)])
    out += _part(tail, dark, dark, step * 0.85, rnd)

    # front leg -- digitigrade with clawed toes
    front_leg = P([(-0.08, 0.42), (0.02, 0.40), (0.03, 0.24), (-0.03, 0.12),
                   (-0.10, 0.04), (-0.16, 0.02), (-0.17, 0.00), (-0.02, 0.00),
                   (-0.01, 0.05), (0.01, 0.12), (-0.04, 0.24)])
    out += _part(front_leg, ink, dark, step, rnd, shade_from=cx)
    for k in range(3):
        tx = -0.15 - 0.026 * k
        seg(tx, 0.02, tx - 0.028, 0.006, ink)

    # torso -- HUNCHED: high rounded back, low chest, leaning forward
    torso = P([(-0.10, 0.44), (-0.16, 0.56), (-0.14, 0.66), (-0.04, 0.70),
               (0.08, 0.66), (0.16, 0.56), (0.17, 0.46), (0.12, 0.40),
               (0.02, 0.38), (-0.06, 0.40)])
    out += _part(torso, ink, dark, step, rnd, shade_from=cx + f * s * 0.02)
    # backswept spines down the hunched spine
    for x, y in [(-0.12, 0.62), (-0.04, 0.68), (0.05, 0.65), (0.12, 0.56)]:
        seg(x, y, x + 0.04, y + 0.02, dark)
    # scale ticks on the flank
    for k in range(6):
        wx = rnd.uniform(-0.08, 0.10); wy = rnd.uniform(0.42, 0.62)
        seg(wx, wy, wx - 0.02, wy - 0.006, dark)

    # neck -- short, thrust FORWARD low off the hunched shoulder
    neck = P([(-0.12, 0.60), (-0.20, 0.62), (-0.24, 0.60), (-0.18, 0.54),
              (-0.11, 0.52)])
    out += _part(neck, ink, dark, step * 0.85, rnd)

    # head -- long snout pointing forward and slightly DOWN
    head = P([(-0.20, 0.62), (-0.26, 0.66), (-0.34, 0.645), (-0.42, 0.60),
              (-0.50, 0.575), (-0.515, 0.555), (-0.44, 0.55), (-0.34, 0.555),
              (-0.26, 0.565), (-0.19, 0.56)])
    out += _part(head, ink, dark, step * 0.7, rnd, shade_from=cx - f * s * 0.30)
    # lower jaw
    jaw = P([(-0.34, 0.555), (-0.50, 0.555), (-0.505, 0.535), (-0.42, 0.535),
             (-0.34, 0.54)])
    out += _part(jaw, ink, dark, step * 0.65, rnd)
    seg(-0.28, 0.66, -0.50, 0.575, dark)                 # snout ridge
    seg(-0.24, 0.635, -0.28, 0.628, dark)                # eye
    seg(-0.47, 0.55, -0.485, 0.51, BONE)                 # a fang
    # backswept spiky crest off the skull
    for k, (bx, by) in enumerate([(-0.20, 0.66), (-0.15, 0.67), (-0.10, 0.66)]):
        seg(bx, by, bx + 0.10 + 0.02 * k, by + 0.09, dark)

    # front arm -- hangs forward, clawed hand
    front_arm = P([(-0.10, 0.56), (-0.18, 0.50), (-0.20, 0.36), (-0.16, 0.26),
                   (-0.12, 0.28), (-0.14, 0.38), (-0.12, 0.50), (-0.06, 0.54)])
    out += _part(front_arm, ink, dark, step * 0.9, rnd, shade_from=cx - f * s * 0.12)
    for k in range(3):
        seg(-0.17 + 0.02 * k, 0.25, -0.18 + 0.02 * k, 0.21, ink)

    # a mining pick shouldered over the back
    seg(0.02, 0.52, -0.20, 0.86, BONE)                   # handle
    seg(-0.20, 0.86, -0.30, 0.83, DARK)                  # pick head
    seg(-0.20, 0.86, -0.12, 0.90, DARK)

    return out


if __name__ == "__main__":
    for sd in range(4):
        print("seed", sd, len(kobold(0, 0, 100, seed=sd)), "strokes")
