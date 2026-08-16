"""fauna_hd_barbarian.py -- the barbarian of Halas at New Sebilis decor fidelity.

The fauna.py races are ~20-stroke wireframes, which read as stick figures and
have been rejected before. This is the first of the HD replacements: side view,
hatched fill via even-odd scanline, tapered two-edge limbs, a fur cloak with a
ragged hem and tick texture, a kilt (Mac's finest), a planted great axe, and a
consistent shadow side on the figure's back (+x).

barbarian(cx, cy, s): feet on the ground at cy, total height s, facing -x.
Returns [(x1, y1, x2, y2, ink)] in map coordinates.
"""
import math, random

PALETTE = {
    'ink':  (110, 92, 70),
    'dark': (78, 62, 46),
    'axe':  (120, 118, 116),
}


def _hatch(poly, ink, step):
    """Fill a polygon with horizontal hatching (even-odd scanline)."""
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
            if xs[i + 1] - xs[i] > 0.4:
                out.append((xs[i], y, xs[i + 1], y, ink))
        y += step
    return out


def _outline(poly, ink):
    return [(poly[i][0], poly[i][1], poly[(i + 1) % len(poly)][0],
             poly[(i + 1) % len(poly)][1], ink) for i in range(len(poly))]


def barbarian(cx, cy, s, ink=None, dark=None, axe=None, seed=0):
    rnd = random.Random(seed)
    ink = ink or PALETTE['ink']
    dark = dark or PALETTE['dark']
    axe = axe or PALETTE['axe']
    out = []
    def P(x, y):                        # figure space -> map space
        return (cx + x * s, cy + y * s)
    def L(a, b, c):
        out.append((a[0], a[1], b[0], b[1], c))
    def poly_map(pts):
        return [P(x, y) for (x, y) in pts]

    # ---- head, facing -x: brow, nose notch, jaw
    head = poly_map([(-0.170, -0.965), (-0.045, -1.000), (0.080, -0.955),
                     (0.100, -0.870), (0.030, -0.828), (-0.100, -0.822),
                     (-0.152, -0.845), (-0.205, -0.882), (-0.185, -0.925)])
    out += _outline(head, ink)
    out += _hatch(head, ink, s * 0.050)
    # beard wedge under the jaw
    beard = poly_map([(-0.152, -0.845), (-0.095, -0.752), (0.010, -0.822)])
    out += _outline(beard, ink)
    for t in (0.3, 0.55, 0.8):
        a = P(-0.152 + 0.14 * t, -0.845 + 0.02)
        b = P(-0.135 + 0.13 * t, -0.775)
        L(a, b, dark)
    # braid swept back off the crown, two strands with ties
    braid = [(-0.005, -0.992), (0.100, -0.968), (0.163, -0.900), (0.188, -0.812)]
    for i in range(len(braid) - 1):
        L(P(*braid[i]), P(*braid[i + 1]), ink)
        L(P(braid[i][0] + 0.014, braid[i][1] + 0.022),
          P(braid[i + 1][0] + 0.014, braid[i + 1][1] + 0.022), dark)
    for (bx, by) in braid[2:]:
        L(P(bx - 0.006, by + 0.008), P(bx + 0.022, by + 0.016), dark)

    # ---- fur cloak over the torso, ragged hem, fur ticks, shadowed back
    cloak = [(-0.085, -0.840), (-0.200, -0.790), (-0.232, -0.600), (-0.195, -0.385),
             (-0.120, -0.440), (-0.048, -0.372), (0.028, -0.442), (0.108, -0.372),
             (0.180, -0.432), (0.222, -0.388), (0.252, -0.620), (0.212, -0.790),
             (0.062, -0.842)]
    cpoly = poly_map(cloak)
    out += _outline(cpoly, ink)
    out += _hatch(cpoly, ink, s * 0.046)
    back = poly_map([(0.100, -0.790), (0.212, -0.790), (0.252, -0.620),
                     (0.222, -0.388), (0.120, -0.400)])
    out += _hatch(back, dark, s * 0.052)
    # fur ticks along shoulder and hem
    for (fx, fy, ex, ey) in ((-0.19, -0.79, -0.23, -0.83), (-0.05, -0.84, -0.07, -0.90),
                             (0.10, -0.84, 0.12, -0.90), (0.20, -0.78, 0.25, -0.82),
                             (-0.16, -0.41, -0.185, -0.35), (-0.085, -0.40, -0.10, -0.335),
                             (0.065, -0.40, 0.075, -0.335), (0.145, -0.40, 0.165, -0.34)):
        L(P(fx, fy), P(ex, ey), dark)

    # ---- belt with buckle
    L(P(-0.190, -0.392), P(0.218, -0.392), dark)
    L(P(-0.185, -0.368), P(0.212, -0.368), dark)
    L(P(-0.015, -0.395), P(-0.015, -0.365), ink)

    # ---- kilt with pleats, shadow on the trailing third
    kilt = [(-0.160, -0.368), (0.185, -0.368), (0.210, -0.215), (-0.190, -0.215)]
    kpoly = poly_map(kilt)
    out += _outline(kpoly, ink)
    for t in (0.22, 0.42, 0.62, 0.82):
        L(P(-0.160 + 0.345 * t, -0.368), P(-0.190 + 0.40 * t, -0.215), ink)
    L(P(-0.175, -0.290), P(0.198, -0.290), ink)          # tartan band
    out += _hatch(poly_map([(0.075, -0.368), (0.185, -0.368),
                            (0.210, -0.215), (0.085, -0.215)]), dark, s * 0.045)

    # ---- legs: two-edge, tapering to the ankle; front leg striding
    # front leg
    L(P(-0.100, -0.215), P(-0.190, -0.115), ink)
    L(P(-0.190, -0.115), P(-0.238, -0.048), ink)
    L(P(-0.030, -0.215), P(-0.128, -0.115), ink)
    L(P(-0.128, -0.115), P(-0.172, -0.048), ink)
    L(P(-0.180, -0.100), P(-0.152, -0.088), dark)         # calf tick
    # rear leg
    L(P(0.075, -0.215), P(0.148, -0.110), ink)
    L(P(0.148, -0.110), P(0.170, -0.048), ink)
    L(P(0.140, -0.215), P(0.208, -0.112), dark)
    L(P(0.208, -0.112), P(0.228, -0.048), dark)
    L(P(0.160, -0.100), P(0.192, -0.090), dark)
    # fur-topped boots
    bootf = poly_map([(-0.252, -0.052), (-0.310, 0.000), (-0.148, 0.000), (-0.156, -0.052)])
    out += _outline(bootf, ink)
    out += _hatch(bootf, ink, s * 0.022)
    L(P(-0.250, -0.052), P(-0.262, -0.082), dark)
    L(P(-0.200, -0.052), P(-0.206, -0.086), dark)
    bootr = poly_map([(0.152, -0.052), (0.132, 0.000), (0.286, 0.000), (0.242, -0.052)])
    out += _outline(bootr, dark)
    out += _hatch(bootr, dark, s * 0.022)
    L(P(0.170, -0.052), P(0.166, -0.084), dark)

    # ---- leading arm gripping the planted axe haft
    L(P(-0.130, -0.740), P(-0.245, -0.628), ink)
    L(P(-0.095, -0.700), P(-0.222, -0.596), ink)
    L(P(-0.245, -0.628), P(-0.302, -0.542), ink)
    L(P(-0.222, -0.596), P(-0.282, -0.528), ink)
    fist = poly_map([(-0.328, -0.548), (-0.286, -0.560), (-0.272, -0.516), (-0.316, -0.508)])
    out += _outline(fist, ink)

    # ---- great axe, planted: haft foot to head height, crescent blade
    L(P(-0.306, -0.004), P(-0.316, -0.930), dark)
    L(P(-0.298, -0.004), P(-0.308, -0.930), ink)
    blade = poly_map([(-0.312, -0.905), (-0.398, -0.928), (-0.452, -0.848),
                      (-0.408, -0.762), (-0.312, -0.778), (-0.352, -0.845)])
    out += _outline(blade, axe)
    out += _hatch(blade, axe, s * 0.030)
    L(P(-0.398, -0.928), P(-0.452, -0.848), dark)         # cutting edge bevel
    L(P(-0.452, -0.848), P(-0.408, -0.762), dark)
    L(P(-0.312, -0.905), P(-0.312, -0.778), dark)         # haft seat

    # ---- ground: shadow ticks trailing to +x
    for k in range(4):
        x0 = 0.02 + 0.075 * k + rnd.uniform(-0.012, 0.012)
        L(P(x0, 0.012), P(x0 + 0.085, 0.018), dark)
    L(P(-0.32, 0.006), P(-0.14, 0.006), dark)
    L(P(0.10, 0.006), P(0.30, 0.006), dark)
    return out
