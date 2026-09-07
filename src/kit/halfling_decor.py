"""halfling_decor.py -- Rivervale halfling-life motif shapes.

The things halflings love, per Brandon's 2026-09-06 review: a fresh pie, a
foaming beer mug, a cheese wheel with the wedge cut, and a pot-bellied wine
jug. Small hand-drawn margin sketches in the same warm ink family as the
existing Rivervale pie basket (185,145,95 pastry / 185,180,172 steam), built
to the BRAIN section-9 bar: closed forms, a hatched shadow side, real internal
structure (lattice, staves, cheese eyes), light jitter so nothing reads
machine-drawn.

Every shape returns [(x1, y1, x2, y2, ink)] in map coordinates.
fn(cx, cy, r, seed=0): (cx, cy) = sketch center, r = half-width.
"""
import math
import random

PALETTE = {
    'pastry':     (185, 145, 95),
    'crust':      (140, 100, 60),
    'steam':      (185, 180, 172),
    'wood':       (110, 86, 60),
    'wood_dark':  (78, 60, 42),
    'foam':       (212, 200, 172),
    'cheese':     (196, 164, 82),
    'rind':       (148, 112, 54),
    'jug':        (118, 76, 48),
    'jug_dark':   (84, 54, 34),
    'cork':       (185, 145, 95),
}


def _hatch(poly, ink, step):
    """Even-odd scanline fill -- the house shadow-side treatment."""
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


def _wobble(pts, rnd, j):
    return [(x + rnd.uniform(-j, j), y + rnd.uniform(-j, j)) for x, y in pts]


def _outline(poly, ink):
    return [(poly[i][0], poly[i][1], poly[(i + 1) % len(poly)][0],
             poly[(i + 1) % len(poly)][1], ink) for i in range(len(poly))]


def _steam(cx, cy, r, rnd, n=2):
    """Rising wisps, same gesture as the existing pie basket's."""
    out = []
    for k in range(n):
        x = cx + (k - (n - 1) / 2) * r * 0.45
        y = cy
        for _ in range(3):
            dx = rnd.uniform(-r * 0.16, r * 0.16)
            out.append((x, y, x + dx, y - r * 0.28, PALETTE['steam']))
            x += dx
            y -= r * 0.28
    return out


def pie(cx, cy, r, seed=0):
    """A whole pie seen slightly from above: crimped rim, domed lattice top,
    two vent slits, steam. Not the basket -- rounder, prouder."""
    rnd = random.Random(seed)
    out = []
    # plate: a wide shallow ellipse under everything
    plate = _wobble([(cx + r * 1.05 * math.cos(t * math.pi / 8),
                      cy + r * 0.30 * math.sin(t * math.pi / 8) + r * 0.42)
                     for t in range(16)], rnd, r * 0.02)
    out += _outline(plate, PALETTE['wood'])
    # pie body: fat dome
    body = _wobble([(cx - r * 0.92, cy + r * 0.38), (cx - r * 0.98, cy + r * 0.10),
                    (cx - r * 0.72, cy - r * 0.22), (cx - r * 0.30, cy - r * 0.42),
                    (cx + r * 0.24, cy - r * 0.44), (cx + r * 0.68, cy - r * 0.26),
                    (cx + r * 0.96, cy + r * 0.06), (cx + r * 0.92, cy + r * 0.38)],
                   rnd, r * 0.025)
    out += _outline(body, PALETTE['crust'])
    # crimped rim: little scallop ticks along the top edge of the plate line
    for k in range(7):
        x = cx - r * 0.85 + k * r * 0.28
        out.append((x, cy + r * 0.36, x + r * 0.13, cy + r * 0.22, PALETTE['crust']))
        out.append((x + r * 0.13, cy + r * 0.22, x + r * 0.26, cy + r * 0.36,
                    PALETTE['crust']))
    # lattice: two diagonal families across the dome
    for k in range(3):
        t = -0.55 + k * 0.42
        out.append((cx + r * (t - 0.30), cy - r * 0.05, cx + r * (t + 0.28),
                    cy - r * 0.38, PALETTE['pastry']))
        out.append((cx + r * (t - 0.30), cy - r * 0.38, cx + r * (t + 0.28),
                    cy - r * 0.05, PALETTE['pastry']))
    # shadow side: hatch the lower-left quarter of the body
    shadow = [(cx - r * 0.92, cy + r * 0.38), (cx - r * 0.98, cy + r * 0.10),
              (cx - r * 0.60, cy + r * 0.10), (cx - r * 0.30, cy + r * 0.38)]
    out += _hatch(shadow, PALETTE['crust'], r * 0.11)
    out += _steam(cx, cy - r * 0.50, r * 0.8, rnd)
    return out


def beer_mug(cx, cy, r, seed=0):
    """A tankard the fauna_sil way: one solid dark silhouette (tight fill),
    a round loop handle, and a pale foam cap boiling over the rim. At map
    scale the ladder-grid of staves and hoops read as a ladder -- solid mass
    plus one accent is what survives."""
    rnd = random.Random(seed)
    out = []
    w, h = r * 0.72, r * 1.0
    # body silhouette: gently waisted tankard, solid-filled
    body = _wobble([(cx - w, cy + h), (cx - w * 1.02, cy + h * 0.35),
                    (cx - w * 0.80, cy - h * 0.20), (cx - w * 0.84, cy - h * 0.72),
                    (cx + w * 0.84, cy - h * 0.72), (cx + w * 0.80, cy - h * 0.20),
                    (cx + w * 1.02, cy + h * 0.35), (cx + w, cy + h)],
                   rnd, r * 0.02)
    out += _hatch(body, PALETTE['wood'], r * 0.055)
    out += _outline(body, PALETTE['wood_dark'])
    # one bright hoop across the belly so it reads as a vessel, not a block
    out.append((cx - w * 0.98, cy + h * 0.38, cx + w * 0.98, cy + h * 0.42,
                PALETTE['cork']))
    # handle: round C-loop off the right side, doubled for weight
    hx = cx + w * 0.95
    loop = [(hx, cy - h * 0.40), (hx + w * 0.62, cy - h * 0.22),
            (hx + w * 0.72, cy + h * 0.10), (hx + w * 0.45, cy + h * 0.36),
            (hx - w * 0.05, cy + h * 0.44)]
    for (a, b) in zip(loop, loop[1:]):
        out.append((a[0], a[1], b[0], b[1], PALETTE['wood_dark']))
    inner = [(hx, cy - h * 0.22), (hx + w * 0.42, cy - h * 0.10),
             (hx + w * 0.50, cy + h * 0.08), (hx + w * 0.28, cy + h * 0.26)]
    for (a, b) in zip(inner, inner[1:]):
        out.append((a[0], a[1], b[0], b[1], PALETTE['wood_dark']))
    # foam cap: two rows of fat scallop bumps, spilling one drip down the left
    for row, (y0, n, rr) in enumerate(((cy - h * 0.72, 4, w * 0.30),
                                       (cy - h * 0.92, 3, w * 0.26))):
        for k in range(n):
            x = cx - w * 0.75 + k * w * 0.5 + row * w * 0.25
            for t in range(4):
                a0 = math.pi * t / 4
                a1 = math.pi * (t + 1) / 4
                out.append((x + rr * math.cos(a0), y0 - rr * 0.9 * math.sin(a0),
                            x + rr * math.cos(a1), y0 - rr * 0.9 * math.sin(a1),
                            PALETTE['foam']))
    out.append((cx - w * 0.98, cy - h * 0.66, cx - w * 0.90, cy - h * 0.30,
                PALETTE['foam']))
    out.append((cx - w * 0.90, cy - h * 0.30, cx - w * 0.96, cy - h * 0.16,
                PALETTE['foam']))
    return out


def cheese_wheel(cx, cy, r, seed=0):
    """A cheese wheel with one wedge cut out; the wedge lies beside it,
    eyes showing."""
    rnd = random.Random(seed)
    out = []
    # wheel: flattened disc with a notch (the cut) at upper right
    pts = []
    for t in range(14):
        a = 0.42 + (2 * math.pi - 0.90) * t / 13
        pts.append((cx + r * 0.85 * math.cos(a), cy - r * 0.52 * math.sin(a)))
    pts.append((cx, cy))                       # into the center for the cut
    wheel = _wobble(pts, rnd, r * 0.02)
    out += _outline(wheel, PALETTE['rind'])
    # rind side line (the wheel has thickness): echo the BOTTOM arc only
    for i in range(len(wheel) - 1):
        (x1, y1), (x2, y2) = wheel[i], wheel[i + 1]
        if y1 > cy + r * 0.28 and y2 > cy + r * 0.28:
            out.append((x1, y1 + r * 0.16, x2, y2 + r * 0.16, PALETTE['rind']))
    # paste face of the cut: two straight radii, pale
    out.append((cx, cy, cx + r * 0.78, cy - r * 0.24, PALETTE['cheese']))
    out.append((cx, cy, cx + r * 0.36, cy - r * 0.50, PALETTE['cheese']))
    # eyes on the face
    for ex, ey, er in ((cx - r * 0.30, cy - r * 0.05, r * 0.08),
                       (cx + r * 0.05, cy + r * 0.18, r * 0.06),
                       (cx - r * 0.10, cy - r * 0.28, r * 0.05)):
        n = 6
        ring = [(ex + er * math.cos(t * 2 * math.pi / n),
                 ey + er * 0.7 * math.sin(t * 2 * math.pi / n)) for t in range(n)]
        out += _outline(ring, PALETTE['cheese'])
    # shadow: hatch INSIDE the lower-left rim (outside reads as whiskers)
    shadow = [(cx - r * 0.62, cy + r * 0.06), (cx - r * 0.30, cy + r * 0.36),
              (cx + r * 0.10, cy + r * 0.42), (cx + r * 0.02, cy + r * 0.22),
              (cx - r * 0.38, cy - r * 0.02)]
    out += _hatch(shadow, PALETTE['rind'], r * 0.13)
    # the cut wedge lying to the right, tip toward the wheel
    wx, wy = cx + r * 1.35, cy + r * 0.30
    wedge = _wobble([(wx - r * 0.42, wy - r * 0.02), (wx + r * 0.30, wy - r * 0.30),
                     (wx + r * 0.38, wy + r * 0.10), (wx - r * 0.30, wy + r * 0.22)],
                    rnd, r * 0.02)
    out += _outline(wedge, PALETTE['rind'])
    out.append((wx - r * 0.05, wy - r * 0.10, wx + r * 0.06, wy - r * 0.02,
                PALETTE['cheese']))
    return out


def wine_bottle(cx, cy, r, seed=0):
    """A pot-bellied wine jug with a cork, halfling-cellar style, and a little
    cup beside it."""
    rnd = random.Random(seed)
    out = []
    w, h = r * 0.60, r * 1.15
    # jug: narrow neck flaring to a fat belly
    body = _wobble([(cx - w * 0.22, cy - h), (cx - w * 0.26, cy - h * 0.62),
                    (cx - w * 0.72, cy - h * 0.28), (cx - w, cy + h * 0.30),
                    (cx - w * 0.78, cy + h * 0.88), (cx - w * 0.30, cy + h),
                    (cx + w * 0.30, cy + h), (cx + w * 0.78, cy + h * 0.88),
                    (cx + w, cy + h * 0.30), (cx + w * 0.72, cy - h * 0.28),
                    (cx + w * 0.26, cy - h * 0.62), (cx + w * 0.22, cy - h)],
                   rnd, r * 0.02)
    out += _outline(body, PALETTE['jug'])
    # cork: little plug on top
    out.append((cx - w * 0.20, cy - h * 1.02, cx + w * 0.20, cy - h * 1.02,
                PALETTE['cork']))
    out.append((cx - w * 0.16, cy - h * 1.16, cx + w * 0.16, cy - h * 1.16,
                PALETTE['cork']))
    out.append((cx - w * 0.16, cy - h * 1.16, cx - w * 0.20, cy - h * 1.02,
                PALETTE['cork']))
    out.append((cx + w * 0.16, cy - h * 1.16, cx + w * 0.20, cy - h * 1.02,
                PALETTE['cork']))
    # neck band + a hanging label tag on a string
    out.append((cx - w * 0.26, cy - h * 0.58, cx + w * 0.26, cy - h * 0.58,
                PALETTE['jug_dark']))
    out.append((cx + w * 0.26, cy - h * 0.56, cx + w * 0.70, cy - h * 0.30,
                PALETTE['cork']))
    tag = [(cx + w * 0.70, cy - h * 0.30), (cx + w * 1.10, cy - h * 0.34),
           (cx + w * 1.14, cy - h * 0.10), (cx + w * 0.74, cy - h * 0.06)]
    out += _outline(tag, PALETTE['cork'])
    # shadow side: hatch the left belly
    shadow = [(cx - w, cy + h * 0.30), (cx - w * 0.78, cy + h * 0.88),
              (cx - w * 0.42, cy + h * 0.96), (cx - w * 0.60, cy + h * 0.24)]
    out += _hatch(shadow, PALETTE['jug_dark'], r * 0.12)
    # little cup at its foot, right side
    ux, uy = cx + r * 1.05, cy + h * 0.72
    cup = _wobble([(ux - r * 0.22, uy - r * 0.16), (ux - r * 0.16, uy + r * 0.22),
                   (ux + r * 0.16, uy + r * 0.22), (ux + r * 0.22, uy - r * 0.16)],
                  rnd, r * 0.015)
    out += _outline(cup, PALETTE['wood'])
    return out


MOTIFS = {'pie': pie, 'beer_mug': beer_mug, 'cheese_wheel': cheese_wheel,
          'wine_bottle': wine_bottle}
