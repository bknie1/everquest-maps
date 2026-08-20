"""fauna_hd_darkelf.py -- high-fidelity Teir'Dal (dark elf) for Neriak / Befallen.

Side-view slender dark elf built like the other HD fauna (closed part polygons,
even-odd hatched fill, a darker shadow side): upright and lean, a hooded cloak
falling behind, a long swept-back ear, an angular face, and a raised curved
blade. Reads as an elegant, menacing swordsman. 100-240 strokes.

    from fauna_hd_darkelf import dark_elf
    segs = dark_elf(cx, cy, s, seed=3)      # (cx, cy) = feet, s = height
    segs = dark_elf(cx, cy, s, face=1)      # face right
"""
import random

SKIN = (92, 84, 116)         # teir'dal violet-grey (fauna PALETTE['teirdal'])
DARK = (60, 54, 82)          # shadow side
CLOAK = (72, 58, 96)         # dark elf cloak
STEEL = (150, 150, 160)      # blade


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


def dark_elf(cx, cy, s, ink=None, seed=0, face=-1):
    """Side-view dark elf. (cx, cy) = feet, s = full height. face=-1 looks left."""
    rnd = random.Random(seed)
    ink = ink or SKIN
    dark = DARK
    f = face

    def P(pts):
        return [(cx + f * x * s, cy - y * s) for x, y in pts]

    def seg(x1, y1, x2, y2, c):
        out.append((cx + f * x1 * s, cy - y1 * s, cx + f * x2 * s, cy - y2 * s, c))

    step = s * 0.048
    out = []

    # cloak -- falls from the shoulders to the ground behind, wide hem
    cloak = P([(0.04, 0.74), (0.14, 0.66), (0.20, 0.44), (0.24, 0.18),
               (0.30, 0.02), (0.16, 0.02), (0.10, 0.22), (0.04, 0.46),
               (-0.02, 0.66)])
    out += _part(cloak, CLOAK, DARK, step, rnd, shade_from=cx + f * s * 0.02)

    # rear leg (shadow) -- slim, straight
    rear_leg = P([(0.02, 0.46), (0.10, 0.46), (0.10, 0.24), (0.12, 0.02),
                  (0.05, 0.02), (0.04, 0.24), (-0.02, 0.44)])
    out += _part(rear_leg, dark, dark, step * 0.9, rnd)
    # front leg -- forward, boot
    front_leg = P([(-0.10, 0.48), (-0.02, 0.48), (-0.03, 0.24), (-0.06, 0.03),
                   (-0.16, 0.02), (-0.17, 0.00), (-0.05, 0.00), (-0.02, 0.02),
                   (0.02, 0.24), (-0.04, 0.46)])
    out += _part(front_leg, ink, dark, step, rnd, shade_from=cx)

    # torso -- lean, upright, slight forward set
    torso = P([(-0.08, 0.46), (-0.12, 0.58), (-0.10, 0.70), (-0.02, 0.76),
               (0.06, 0.74), (0.12, 0.62), (0.12, 0.50), (0.06, 0.44),
               (-0.02, 0.43)])
    out += _part(torso, ink, dark, step, rnd, shade_from=cx + f * s * 0.0)
    # belt + tunic seam
    seg(-0.09, 0.48, 0.11, 0.50, dark)
    seg(-0.06, 0.66, 0.02, 0.62, dark)

    # neck + angular head, sharp chin, swept-back ear
    neck = P([(-0.06, 0.74), (-0.10, 0.78), (-0.06, 0.80), (-0.02, 0.76)])
    out += _part(neck, ink, dark, step * 0.8, rnd)
    head = P([(-0.06, 0.80), (-0.12, 0.845), (-0.16, 0.845), (-0.19, 0.815),
              (-0.17, 0.79), (-0.20, 0.78), (-0.15, 0.765), (-0.08, 0.775)])
    out += _part(head, ink, dark, step * 0.62, rnd, shade_from=cx - f * s * 0.10)
    seg(-0.15, 0.815, -0.185, 0.805, dark)               # eye
    seg(-0.16, 0.78, -0.20, 0.775, dark)                 # jaw/chin
    # long swept-back ear
    ear = P([(-0.08, 0.83), (0.00, 0.88), (0.05, 0.865), (-0.05, 0.815)])
    out += _part(ear, ink, dark, step * 0.6, rnd)
    # hair falling back
    for k in range(4):
        seg(-0.04 + 0.02 * k, 0.82 - 0.01 * k, 0.06 + 0.02 * k, 0.70 - 0.02 * k, dark)

    # rear arm (shadow) at the side
    rear_arm = P([(0.02, 0.70), (0.08, 0.66), (0.07, 0.52), (0.10, 0.40),
                  (0.06, 0.40), (0.02, 0.52), (-0.02, 0.66)])
    out += _part(rear_arm, dark, dark, step * 0.85, rnd)

    # front arm raised, gripping a curved blade
    front_arm = P([(-0.06, 0.70), (-0.16, 0.68), (-0.24, 0.74), (-0.22, 0.78),
                   (-0.14, 0.72), (-0.06, 0.66)])
    out += _part(front_arm, ink, dark, step * 0.85, rnd, shade_from=cx - f * s * 0.14)
    # curved scimitar sweeping up from the fist
    blade = P([(-0.22, 0.76), (-0.30, 0.92), (-0.40, 1.02), (-0.42, 1.00),
               (-0.34, 0.90), (-0.26, 0.76)])
    out += _outline(blade, STEEL, rnd, step * 0.08)
    seg(-0.22, 0.72, -0.235, 0.80, dark)                 # hilt guard

    return out


if __name__ == "__main__":
    for sd in range(4):
        print("seed", sd, len(dark_elf(0, 0, 100, seed=sd)), "strokes")
