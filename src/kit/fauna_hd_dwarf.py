"""fauna_hd_dwarf.py -- high-fidelity dwarf for Kaladim / Butcherblock / the Karanas.

Side-view stout dwarf built like the other HD fauna (closed part polygons,
even-odd hatched fill, a darker shadow side): short and broad, a barrel chest, a
great forked beard covering it, a horned/winged helm, thick boots, and a
two-handed warhammer over one shoulder. 100-240 strokes.

    from fauna_hd_dwarf import dwarf
    segs = dwarf(cx, cy, s, seed=3)      # (cx, cy) = feet, s = height
    segs = dwarf(cx, cy, s, face=1)      # face right
"""
import random

CLOTH = (104, 76, 52)        # dwarf leather/russet (fauna PALETTE['dwarf'])
DARK = (72, 52, 36)          # shadow side
BEARD = (150, 130, 96)       # pale beard
MAIL = (120, 116, 108)       # helm / mail
STEEL = (150, 150, 160)      # hammer head
WOOD = (110, 84, 56)         # haft


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
    j = step * 0.16
    out = _outline(poly, ink, rnd, j * 0.6)
    if shade_from is None:
        out += _hatch(poly, ink, step, j, rnd)
    else:
        lit = [(min(x, shade_from), y) for x, y in poly]
        shd = [(max(x, shade_from), y) for x, y in poly]
        out += _hatch(lit, ink, step, j, rnd)
        out += _hatch(shd, dark, step * 0.82, j, rnd)
    return out


def dwarf(cx, cy, s, ink=None, seed=0, face=-1):
    """Side-view dwarf. (cx, cy) = feet, s = full height. face=-1 looks left.
    Proportions are stout: the head+helm is a big fraction of the height."""
    rnd = random.Random(seed)
    ink = ink or CLOTH
    dark = DARK
    f = face

    def P(pts):
        return [(cx + f * x * s, cy - y * s) for x, y in pts]

    def seg(x1, y1, x2, y2, c):
        out.append((cx + f * x1 * s, cy - y1 * s, cx + f * x2 * s, cy - y2 * s, c))

    step = s * 0.050
    out = []

    # thick stubby legs / boots (short -- dwarf stands low)
    rear_leg = P([(0.04, 0.34), (0.16, 0.34), (0.17, 0.16), (0.20, 0.02),
                  (0.08, 0.02), (0.05, 0.16), (0.00, 0.32)])
    out += _part(rear_leg, dark, dark, step * 0.9, rnd)
    front_leg = P([(-0.12, 0.34), (0.00, 0.34), (0.01, 0.16), (0.03, 0.02),
                   (-0.16, 0.02), (-0.17, 0.00), (-0.02, 0.00), (0.00, 0.02),
                   (-0.10, 0.16), (-0.06, 0.32)])
    out += _part(front_leg, ink, dark, step, rnd, shade_from=cx)

    # barrel torso -- very broad
    torso = P([(-0.16, 0.32), (-0.20, 0.46), (-0.18, 0.58), (-0.08, 0.64),
               (0.06, 0.63), (0.18, 0.56), (0.20, 0.44), (0.17, 0.32),
               (0.06, 0.30), (-0.06, 0.30)])
    out += _part(torso, ink, dark, step, rnd, shade_from=cx + f * s * 0.02)
    seg(-0.17, 0.40, 0.18, 0.41, dark)                   # broad belt
    for k in range(3):                                   # belt studs
        seg(-0.08 + 0.08 * k, 0.405, -0.06 + 0.08 * k, 0.405, MAIL)

    # great forked beard spilling over the chest to the belt
    beard = P([(-0.14, 0.60), (-0.20, 0.52), (-0.22, 0.40), (-0.16, 0.36),
               (-0.10, 0.42), (-0.13, 0.34), (-0.06, 0.36), (-0.03, 0.44),
               (0.00, 0.36), (0.04, 0.46), (0.06, 0.58)])
    out += _part(beard, BEARD, (120, 100, 72), step * 0.8, rnd)
    for k in range(4):                                   # beard strands
        bx = -0.18 + 0.06 * k
        seg(bx, 0.56, bx + 0.01, 0.38, (120, 100, 72))

    # head -- small, mostly helm + a nose poking from the beard
    head = P([(-0.06, 0.62), (-0.12, 0.655), (-0.16, 0.645), (-0.18, 0.62),
              (-0.15, 0.60), (-0.07, 0.60)])
    out += _part(head, ink, dark, step * 0.6, rnd)
    seg(-0.17, 0.625, -0.20, 0.615, ink)                 # big nose
    # horned / winged helm dome
    helm = P([(-0.05, 0.645), (-0.11, 0.685), (-0.16, 0.675), (-0.18, 0.65),
              (-0.05, 0.645)])
    out += _part(helm, MAIL, (84, 80, 74), step * 0.55, rnd)
    seg(-0.18, 0.66, -0.24, 0.72, MAIL)                  # horn back
    seg(-0.05, 0.66, 0.01, 0.72, MAIL)                   # horn front

    # rear arm shouldering the hammer haft
    rear_arm = P([(0.02, 0.58), (0.10, 0.54), (0.11, 0.42), (0.14, 0.34),
                  (0.08, 0.34), (0.05, 0.42), (-0.01, 0.54)])
    out += _part(rear_arm, dark, dark, step * 0.85, rnd)
    # two-handed warhammer over the shoulder
    seg(0.10, 0.44, -0.08, 0.86, WOOD)                   # haft
    hammer = P([(-0.02, 0.80), (-0.14, 0.84), (-0.16, 0.94), (-0.04, 0.90)])
    out += _part(hammer, STEEL, (96, 96, 104), step * 0.6, rnd)

    # front arm -- thick, fist on the belt
    front_arm = P([(-0.10, 0.56), (-0.18, 0.50), (-0.20, 0.42), (-0.15, 0.38),
                   (-0.12, 0.42), (-0.13, 0.48), (-0.06, 0.52)])
    out += _part(front_arm, ink, dark, step * 0.85, rnd, shade_from=cx - f * s * 0.12)

    return out


if __name__ == "__main__":
    for sd in range(4):
        print("seed", sd, len(dwarf(0, 0, 100, seed=sd)), "strokes")
