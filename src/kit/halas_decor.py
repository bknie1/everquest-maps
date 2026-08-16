"""halas_decor.py -- Halas (barbarian ice city) motif shapes.

The Gwenavyne raft ferry for the frigid lake, the kennels' sled team, and
angular ice shards for the margins. Built to the BRAIN section-9 bar: hatched
fill via even-odd scanline, tapered two-edge forms, a shadow side, and real
internal structure -- lashings, harness lines, facets -- not wireframes.

Every shape returns [(x1, y1, x2, y2, ink)] in map coordinates.
"""
import math, random

PALETTE = {
    'log':      (110, 86, 60),
    'log_dark': (78, 60, 42),
    'rope':     (140, 120, 90),
    'water':    (96, 146, 176),
    'ice':      (150, 192, 214),
    'ice_deep': (96, 146, 176),
    'dog':      (110, 92, 70),
    'dog_dark': (80, 64, 48),
    'snow':     (176, 196, 212),
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
            if xs[i + 1] - xs[i] > 0.6:
                out.append((xs[i], y, xs[i + 1], y, ink))
        y += step
    return out


def _outline(poly, ink):
    return [(poly[i][0], poly[i][1], poly[(i + 1) % len(poly)][0],
             poly[(i + 1) % len(poly)][1], ink) for i in range(len(poly))]


def raft_ferry(cx, cy, r, ink=None, dark=None, rope=None, water=None, seed=0):
    """The Gwenavyne: a log raft seen from above, slightly skewed, with a low
    rail along one side, cross-lashings, a steering oar at the stern, and the
    ferry rope running off the bow. Logs are hatched, the south pair of logs
    carries the shadow, and a few ripples sit in the lake ink around the hull."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['log']; dark = dark or PALETTE['log_dark']
    rope = rope or PALETTE['rope']; water = water or PALETTE['water']
    ang = math.radians(-11)
    ca, sa = math.cos(ang), math.sin(ang)
    def T(x, y):
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    out = []
    def L(p, q, c):
        out.append((p[0], p[1], q[0], q[1], c))

    W = r * 1.15                       # half-length of the deck
    n = 5                              # logs
    H = r * 0.72                       # half-width of the deck
    logh = 2.0 * H / n
    for k in range(n):
        y0 = -H + k * logh
        y1 = y0 + logh
        c = dark if k == n - 1 else ink        # shadow log on the south edge
        L(T(-W, y0), T(W, y0), c)
        if k == n - 1:
            L(T(-W, y1), T(W, y1), dark)
        # bevelled log ends
        L(T(-W, y0), T(-W - logh * 0.18, (y0 + y1) / 2), c)
        L(T(-W - logh * 0.18, (y0 + y1) / 2), T(-W, y1), c)
        L(T(W, y0), T(W + logh * 0.22, (y0 + y1) / 2), c)
        L(T(W + logh * 0.22, (y0 + y1) / 2), T(W, y1), c)
        # hatch rows inside the log
        for j in range(2):
            yy = y0 + logh * (j + 1) / 3.0
            xr = W * rnd.uniform(0.88, 0.98)
            L(T(-xr, yy), T(xr, yy), dark if k >= n - 2 else c)
        # end grain
        L(T(W + logh * 0.10, (y0 + y1) / 2 - logh * 0.15),
          T(W + logh * 0.10, (y0 + y1) / 2 + logh * 0.15), dark)
    # cross-lashings binding the logs
    for xb in (-W * 0.62, W * 0.62):
        L(T(xb - r * 0.05, -H), T(xb - r * 0.05, H), dark)
        L(T(xb + r * 0.05, -H), T(xb + r * 0.05, H), dark)
        L(T(xb - r * 0.05, -H), T(xb + r * 0.05, -H + logh * 0.5), dark)
        L(T(xb - r * 0.05, H - logh * 0.5), T(xb + r * 0.05, H), dark)
    # low rail along the north edge
    rail_y = -H - r * 0.30
    posts = (-W * 0.80, -W * 0.27, W * 0.27, W * 0.80)
    for px in posts:
        L(T(px, -H), T(px, rail_y), dark)
    for a, b in zip(posts, posts[1:]):
        L(T(a, rail_y), T(b, rail_y), ink)
    L(T(posts[0], -H), T(posts[1], rail_y), ink)        # brace
    # steering oar at the stern
    L(T(W * 0.90, H * 0.40), T(W + r * 0.75, H + r * 0.55), dark)
    blade = [T(W + r * 0.60, H + r * 0.35), T(W + r * 0.95, H + r * 0.55),
             T(W + r * 0.70, H + r * 0.80)]
    L(blade[0], blade[1], dark); L(blade[1], blade[2], dark); L(blade[2], blade[0], dark)
    # ferry rope off the bow, sagging between pulls
    L(T(-W * 0.90, -H * 0.35), T(-W * 0.90, -H * 0.35 - r * 0.30), dark)
    pts = [(-W * 0.92, -H * 0.35 - r * 0.28)]
    for k in range(1, 4):
        pts.append((-W - r * 0.55 * k,
                    -H * 0.35 - r * 0.30 - r * 0.30 * k + r * 0.10 * math.sin(k * 2.2)))
    for a, b in zip(pts, pts[1:]):
        L(T(*a), T(*b), rope)
    # ripples around the hull
    for k in range(5):
        a = rnd.uniform(0, 2 * math.pi)
        d = r * rnd.uniform(1.35, 1.75)
        x, y = cx + math.cos(a) * d * 1.25, cy + math.sin(a) * d * 0.85
        w = r * rnd.uniform(0.22, 0.40)
        out.append((x - w, y, x - w * 0.3, y - r * 0.06, water))
        out.append((x - w * 0.3, y - r * 0.06, x + w, y, water))
    return out


def _dog(cx, cy, s, ink, dark, rnd, gait=0.0):
    """One sled dog, side view facing -x. cy is the ground, s the body length.
    Hatched body, tapered two-edge legs, pricked ears, tail curled over the back."""
    out = []
    bh = s * 0.42
    x0, x1 = cx - s * 0.5, cx + s * 0.5          # x0 = chest end
    top = cy - bh * 1.55
    belly = cy - bh * 0.72
    body = [(x0, top + bh * 0.24), (x0 + s * 0.22, top), (x1 - s * 0.18, top + bh * 0.10),
            (x1, top + bh * 0.36), (x1 - s * 0.04, belly), (x0 + s * 0.30, belly + bh * 0.10),
            (x0 + s * 0.02, belly - bh * 0.06)]
    out += _outline(body, ink)
    out += _hatch(body, ink, bh * 0.30)
    # shadow along the underside
    for t in (0.18, 0.45, 0.72):
        ax = x0 + (x1 - x0) * t
        out.append((ax, belly + bh * 0.04, ax + s * 0.12, belly + bh * 0.07, dark))
    # head and muzzle
    hx, hy = x0 - s * 0.02, top + bh * 0.16
    head = [(hx + s * 0.06, hy - bh * 0.16), (hx - s * 0.16, hy - bh * 0.10),
            (hx - s * 0.28, hy + bh * 0.14), (hx - s * 0.10, hy + bh * 0.30),
            (hx + s * 0.06, hy + bh * 0.22)]
    out += _outline(head, ink)
    # pricked ears
    out.append((hx - s * 0.02, hy - bh * 0.14, hx - s * 0.05, hy - bh * 0.46, ink))
    out.append((hx - s * 0.05, hy - bh * 0.46, hx - s * 0.11, hy - bh * 0.12, ink))
    out.append((hx + s * 0.05, hy - bh * 0.15, hx + s * 0.04, hy - bh * 0.42, ink))
    out.append((hx + s * 0.04, hy - bh * 0.42, hx - s * 0.02, hy - bh * 0.14, ink))
    # legs: two edges converging to the paw, front pair striding with the gait
    for lx, swing in ((x0 + s * 0.14, gait), (x0 + s * 0.24, -gait * 0.6),
                      (x1 - s * 0.22, -gait), (x1 - s * 0.10, gait * 0.6)):
        foot = lx + swing * s * 0.16
        hip = belly + bh * 0.02
        out.append((lx - s * 0.035, hip, foot - s * 0.015, cy, ink))
        out.append((lx + s * 0.035, hip, foot + s * 0.02, cy, ink))
        out.append((foot - s * 0.015, cy, foot + s * 0.05, cy, dark))     # paw
    # tail curled over the back
    tx, ty = x1 - s * 0.02, top + bh * 0.20
    out.append((tx, ty, tx + s * 0.14, ty - bh * 0.42, ink))
    out.append((tx + s * 0.14, ty - bh * 0.42, tx + s * 0.02, ty - bh * 0.62, ink))
    out.append((tx + s * 0.02, ty - bh * 0.62, tx - s * 0.08, ty - bh * 0.44, ink))
    return out


def sled_team(cx, cy, r, ink=None, dark=None, rope=None, seed=0):
    """A dog sled: curved runner, hatched basket with a lashed load, handlebar,
    and three huskies in a harness line pulling to the west. Snow ticks under
    the runners, shadow on the basket's lower half."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['dog']; dark = dark or PALETTE['dog_dark']
    rope = rope or PALETTE['rope']
    out = []
    def L(x1, y1, x2, y2, c):
        out.append((x1, y1, x2, y2, c))

    # --- sled, occupying cx+0.3r .. cx+1.9r
    # runner with upcurled nose, doubled for weight
    L(cx + 1.90 * r, cy, cx + 0.55 * r, cy, ink)
    L(cx + 0.55 * r, cy, cx + 0.36 * r, cy - 0.18 * r, ink)
    L(cx + 0.36 * r, cy - 0.18 * r, cx + 0.30 * r, cy - 0.42 * r, ink)
    L(cx + 1.90 * r, cy + 0.05 * r, cx + 0.55 * r, cy + 0.05 * r, dark)
    # struts
    L(cx + 0.80 * r, cy, cx + 0.80 * r, cy - 0.36 * r, ink)
    L(cx + 1.55 * r, cy, cx + 1.55 * r, cy - 0.36 * r, ink)
    # basket, hatched, shadow band low
    basket = [(cx + 0.58 * r, cy - 0.36 * r), (cx + 1.82 * r, cy - 0.36 * r),
              (cx + 1.72 * r, cy - 0.78 * r), (cx + 0.72 * r, cy - 0.74 * r)]
    out += _outline(basket, ink)
    out += _hatch(basket, ink, r * 0.14)
    low = [(cx + 0.58 * r, cy - 0.36 * r), (cx + 1.82 * r, cy - 0.36 * r),
           (cx + 1.78 * r, cy - 0.55 * r), (cx + 0.65 * r, cy - 0.53 * r)]
    out += _hatch(low, dark, r * 0.14)
    # lashed load on top
    L(cx + 0.85 * r, cy - 0.76 * r, cx + 1.05 * r, cy - 0.98 * r, ink)
    L(cx + 1.05 * r, cy - 0.98 * r, cx + 1.45 * r, cy - 0.98 * r, ink)
    L(cx + 1.45 * r, cy - 0.98 * r, cx + 1.60 * r, cy - 0.77 * r, ink)
    L(cx + 1.02 * r, cy - 0.98 * r, cx + 1.12 * r, cy - 0.75 * r, rope)
    L(cx + 1.35 * r, cy - 0.98 * r, cx + 1.44 * r, cy - 0.76 * r, rope)
    # handlebar
    L(cx + 1.82 * r, cy - 0.36 * r, cx + 1.98 * r, cy - 1.02 * r, ink)
    L(cx + 1.98 * r, cy - 1.02 * r, cx + 1.80 * r, cy - 1.06 * r, ink)

    # --- the team, three dogs with alternating gait
    hitch = (cx + 0.34 * r, cy - 0.30 * r)
    prev = hitch
    for k, dxx in enumerate((-0.45, -1.42, -2.39)):
        dcx = cx + dxx * r + rnd.uniform(-0.04, 0.04) * r
        dcy = cy + (0.02 * r if k % 2 else 0.0)
        s = r * 0.82
        out += _dog(dcx, dcy, s, ink, dark, rnd, gait=(1.0 if k % 2 else -1.0))
        # gangline back to the previous hitch point
        back = (dcx + s * 0.52, dcy - s * 0.30)
        chest = (dcx - s * 0.44, dcy - s * 0.26)
        L(back[0], back[1], prev[0], prev[1], rope)
        prev = chest
    # lead line running out front
    L(prev[0], prev[1], prev[0] - 0.45 * r, prev[1] + 0.10 * r, rope)
    # snow ticks under the team
    for k in range(5):
        x = cx + rnd.uniform(-2.3, 1.7) * r
        w = rnd.uniform(0.12, 0.26) * r
        L(x - w, cy + 0.16 * r, x + w, cy + 0.16 * r, PALETTE['snow'])
    return out


def ice_shard(cx, cy, r, ink=None, deep=None, seed=0):
    """A cluster of angular ice crystals: one tall shard and two leaners, each
    with a facet line and hatched shadow face, rising from a snow scallop."""
    rnd = random.Random(seed)
    ink = ink or PALETTE['ice']; deep = deep or PALETTE['ice_deep']
    out = []
    shards = ((0.00, 1.00, 0.30, -0.08),
              (-0.58, 0.55, 0.20, -0.20),
              (0.52, 0.62, 0.22, 0.16))
    for (ox, hh, ww, lean) in shards:
        h = r * 1.55 * hh * rnd.uniform(0.92, 1.08)
        w = r * ww
        bx = cx + ox * r
        ap = (bx + lean * r, cy - h)
        poly = [(bx - w, cy), (bx - w * 0.55, cy - h * 0.45), ap,
                (bx + w * 0.5, cy - h * 0.55), (bx + w, cy)]
        out += _outline(poly, ink)
        out.append((ap[0], ap[1], bx + w * 0.15, cy, ink))        # facet edge
        shadow = [ap, (bx + w * 0.5, cy - h * 0.55), (bx + w, cy), (bx + w * 0.15, cy)]
        out += _hatch(shadow, deep, max(1.2, h * 0.16))
    # snow scallop at the base
    prev = None
    for k in range(7):
        a = math.pi + math.pi * k / 6
        p = (cx + math.cos(a) * r * 1.2, cy + math.sin(a) * r * 0.18)
        if prev:
            out.append((prev[0], prev[1], p[0], p[1], PALETTE['snow']))
        prev = p
    return out
