"""fauna_hd_wolf.py -- high-fidelity prowling wolf / sabertooth (quadruped).

A side-view four-legged predator built the way the other HD fauna are (closed
part polygons, even-odd hatched fill, a darker shadow side on the far limbs, real
anatomy): deep chest, tucked belly, low prowling head with a snarling muzzle,
pricked ears, a bushy tail. Pass fangs=True for a sabertooth (Blackburrow's
Sabertooth clan). 120-260 strokes.

    from fauna_hd_wolf import wolf
    segs = wolf(cx, cy, s, seed=3)            # (cx, cy) = ground under the chest, s = shoulder height
    segs = wolf(cx, cy, s, fangs=True)        # sabertooth
    segs = wolf(cx, cy, s, face=1)            # face right
"""
import random

FUR = (110, 100, 92)         # grey wolf (near fauna PALETTE['rat']/'fur')
DARK = (76, 68, 62)          # shadow side / markings
BONE = (150, 142, 120)       # fangs


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


def _part(poly, ink, dark, step, rnd, shade=False):
    j = step * 0.18
    out = _outline(poly, ink, rnd, j * 0.6)
    out += _hatch(poly, dark if shade else ink, step, j, rnd)
    return out


def wolf(cx, cy, s, ink=None, seed=0, face=-1, fangs=False):
    """Side-view prowling wolf. (cx, cy) = ground under the chest, s = shoulder
    height. Body runs ~1.7*s long. face=-1 head to the left (default)."""
    rnd = random.Random(seed)
    ink = ink or FUR
    dark = DARK
    f = face

    def P(pts):
        return [(cx + f * x * s, cy - y * s) for x, y in pts]

    def seg(x1, y1, x2, y2, c):
        out.append((cx + f * x1 * s, cy - y1 * s, cx + f * x2 * s, cy - y2 * s, c))

    step = s * 0.055
    out = []

    # far legs (shadow) -- hind then front, thin, set slightly inboard
    far_hind = P([(0.46, 0.46), (0.56, 0.46), (0.55, 0.24), (0.58, 0.02),
                  (0.52, 0.02), (0.49, 0.24), (0.44, 0.44)])
    out += _part(far_hind, dark, dark, step * 0.9, rnd)
    far_front = P([(-0.34, 0.50), (-0.26, 0.50), (-0.27, 0.26), (-0.24, 0.02),
                   (-0.30, 0.02), (-0.33, 0.26), (-0.40, 0.46)])
    out += _part(far_front, dark, dark, step * 0.9, rnd)

    # tail -- bushy, sweeping down and back off the hindquarters
    tail = P([(0.60, 0.56), (0.74, 0.54), (0.86, 0.44), (0.92, 0.30),
              (0.86, 0.28), (0.78, 0.40), (0.66, 0.48), (0.58, 0.52)])
    out += _part(tail, ink, dark, step * 0.85, rnd)

    # body -- arched topline, deep dropped chest at the front, belly tucked UP
    # toward the loins, muscular haunch at the rear. NOT a flat slab.
    body = P([(-0.40, 0.54),          # base of neck / shoulder
              (-0.34, 0.66), (-0.16, 0.72), (0.06, 0.73), (0.28, 0.71),  # arched back
              (0.48, 0.68), (0.60, 0.60), (0.63, 0.50),                  # rump
              (0.58, 0.44), (0.50, 0.52), (0.40, 0.50),                  # haunch notch
              (0.24, 0.44), (0.12, 0.40), (0.02, 0.42),                  # tucked belly (rises)
              (-0.12, 0.40), (-0.26, 0.36), (-0.36, 0.40)])              # deep chest drop
    out += _part(body, ink, dark, step, rnd)
    # deep-chest shadow (front underside) + haunch mass shading
    out += _hatch(P([(-0.36, 0.40), (-0.20, 0.54), (-0.06, 0.44), (-0.24, 0.36)]),
                  dark, step * 0.9, step * 0.16, rnd)
    out += _hatch(P([(0.34, 0.50), (0.58, 0.64), (0.62, 0.50), (0.44, 0.46)]),
                  dark, step * 0.9, step * 0.16, rnd)
    # a couple of back / flank markings
    for k in range(5):
        mx = rnd.uniform(-0.05, 0.45); my = rnd.uniform(0.48, 0.64)
        seg(mx, my, mx - 0.05, my - 0.01, dark)

    # near hind + front legs (lit)
    near_hind = P([(0.40, 0.48), (0.52, 0.48), (0.52, 0.24), (0.55, 0.00),
                   (0.47, 0.00), (0.45, 0.24), (0.38, 0.46)])
    out += _part(near_hind, ink, dark, step, rnd)
    near_front = P([(-0.28, 0.52), (-0.18, 0.52), (-0.19, 0.26), (-0.16, 0.00),
                    (-0.24, 0.00), (-0.27, 0.26), (-0.34, 0.48)])
    out += _part(near_front, ink, dark, step, rnd)
    for x0 in (0.47, -0.20):                                 # paws
        seg(x0, 0.00, x0 - 0.06, 0.00, ink)

    # neck -- from the chest up and forward to the head
    neck = P([(-0.40, 0.56), (-0.52, 0.62), (-0.60, 0.60), (-0.56, 0.50),
              (-0.44, 0.48)])
    out += _part(neck, ink, dark, step * 0.9, rnd)

    # head -- low, level; long muzzle to the left, domed skull, pricked ears
    head = P([(-0.54, 0.62), (-0.62, 0.66), (-0.72, 0.64), (-0.82, 0.585),
              (-0.90, 0.57), (-0.905, 0.55), (-0.82, 0.545), (-0.72, 0.55),
              (-0.62, 0.55), (-0.56, 0.56)])
    out += _part(head, ink, dark, step * 0.7, rnd)
    # lower jaw slightly open (snarl)
    jaw = P([(-0.70, 0.55), (-0.86, 0.535), (-0.88, 0.515), (-0.74, 0.52),
             (-0.64, 0.53)])
    out += _part(jaw, ink, dark, step * 0.65, rnd)
    seg(-0.83, 0.575, -0.90, 0.565, dark)                   # muzzle top ridge
    seg(-0.60, 0.63, -0.66, 0.615, dark)                    # eye slit
    # pricked ears
    ear1 = P([(-0.58, 0.66), (-0.56, 0.74), (-0.50, 0.72), (-0.53, 0.64)])
    out += _part(ear1, ink, dark, step * 0.6, rnd)
    ear2 = P([(-0.52, 0.66), (-0.485, 0.735), (-0.43, 0.71), (-0.47, 0.635)])
    out += _part(ear2, ink, dark, step * 0.6, rnd)
    # fangs (sabertooth) -- long down from the upper jaw
    if fangs:
        seg(-0.80, 0.545, -0.815, 0.46, BONE)
        seg(-0.815, 0.46, -0.80, 0.455, BONE)
        seg(-0.75, 0.545, -0.762, 0.475, BONE)
    else:
        seg(-0.84, 0.535, -0.85, 0.52, BONE)                # small canine

    return out


if __name__ == "__main__":
    for sd in range(4):
        print("seed", sd, len(wolf(0, 0, 100, seed=sd, fangs=True)), "strokes")
