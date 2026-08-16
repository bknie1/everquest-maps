"""oggok_decor.py -- ruined Greek/Roman grandeur for Oggok (pre-curse ogre empire).

BRAIN-9 fidelity: hatched fill via even-odd scanline, tapered forms, a shadow
side in a darker ink, internal structure (drum joints, cracks, rubble).

Shapes:
    broken_colonnade(cx, cy, r)  -- a row of 3-4 pillars, one toppled
    cracked_dome(cx, cy, r)      -- half-collapsed dome on columns
"""
import math, random

INK  = (126, 110, 84)
DARK = (96, 84, 62)


def _hatch(poly, ink, step):
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


def _column(cx, base_y, h, w, ink, dark, rnd, broken=False):
    """One standing column: plinth, tapered hatched shaft, capital or a
    jagged broken top, drum joints, shadow hatch on the right side."""
    out = []
    # plinth
    pw = w * 1.5
    plinth = [(cx - pw, base_y), (cx + pw, base_y),
              (cx + pw, base_y - h * 0.07), (cx - pw, base_y - h * 0.07)]
    out += _outline(plinth, dark)
    top_y = base_y - h
    wt = w * 0.82
    if broken:
        top_y = base_y - h * rnd.uniform(0.45, 0.65)
        # jagged break
        jag = [(cx - wt, top_y + h * 0.04), (cx - wt * 0.3, top_y - h * 0.03),
               (cx + wt * 0.25, top_y + h * 0.05), (cx + wt, top_y)]
        shaft = [(cx - w, base_y - h * 0.07)] + jag[::1] + \
                [(cx + w, base_y - h * 0.07)]
        shaft = [(cx - w, base_y - h * 0.07), jag[0], jag[1], jag[2], jag[3],
                 (cx + w, base_y - h * 0.07)]
    else:
        shaft = [(cx - w, base_y - h * 0.07), (cx - wt, top_y),
                 (cx + wt, top_y), (cx + w, base_y - h * 0.07)]
    out += _outline(shaft, ink)
    out += _hatch(shaft, ink, h * 0.085)
    # right-side shadow: denser dark hatch over the right 40%
    shadow = [((p[0] + cx + max(w, wt)) / 2 if p[0] < cx else p[0], p[1])
              for p in shaft]
    out += _hatch([(cx + w * 0.15, base_y - h * 0.07),
                   (cx + wt * 0.15, top_y),
                   (cx + wt, top_y), (cx + w, base_y - h * 0.07)],
                  dark, h * 0.13)
    # drum joints
    n = 3 if broken else 4
    for k in range(1, n):
        t = k / n
        yy = base_y - h * 0.07 + (top_y - (base_y - h * 0.07)) * t
        ww = w + (wt - w) * t
        out.append((cx - ww, yy, cx + ww, yy, dark))
    if not broken:
        # capital
        cwid = w * 1.4
        cap = [(cx - cwid, top_y), (cx + cwid, top_y),
               (cx + cwid * 0.8, top_y - h * 0.06), (cx - cwid * 0.8, top_y - h * 0.06)]
        out += _outline(cap, dark)
    return out


def _toppled(cx, cy, L, w, ink, dark, rnd):
    """A fallen column shaft lying on the ground, drum joints showing."""
    out = []
    tilt = rnd.uniform(-0.12, 0.12)
    y0, y1 = cy - w, cy + w
    body = [(cx - L / 2, y0 + L * tilt * -0.5), (cx + L / 2, y0 + L * tilt * 0.5),
            (cx + L / 2 + w * 0.4, (y0 + y1) / 2 + L * tilt * 0.5),
            (cx + L / 2, y1 + L * tilt * 0.5), (cx - L / 2, y1 + L * tilt * -0.5)]
    out += _outline(body, ink)
    out += _hatch(body, ink, w * 0.55)
    # drum joints across the shaft
    for k in range(1, 4):
        x = cx - L / 2 + L * k / 4
        dy = L * tilt * (k / 4 - 0.5)
        out.append((x, y0 + dy, x - w * 0.2, y1 + dy, dark))
    # shadow underside
    out.append((cx - L / 2, y1 + L * tilt * -0.5 + w * 0.25,
                cx + L / 2, y1 + L * tilt * 0.5 + w * 0.25, dark))
    # rubble chunks at the broken end
    for k in range(3):
        rx = cx + L / 2 + w * (0.8 + k * 0.9) + rnd.uniform(-w * 0.2, w * 0.2)
        ry = cy + rnd.uniform(-w, w)
        rr = w * rnd.uniform(0.25, 0.5)
        rub = [(rx - rr, ry), (rx, ry - rr), (rx + rr, ry), (rx, ry + rr * 0.7)]
        out += _outline(rub, dark)
    return out


def broken_colonnade(cx, cy, r, ink=INK, dark=DARK, seed=0):
    """A row of 3-4 pillars sharing a ruined stylobate, one toppled in front."""
    rnd = random.Random(seed)
    out = []
    n = rnd.choice((3, 4))
    h = r * 1.55
    w = r * 0.16
    pitch = r * 0.62
    x0 = cx - pitch * (n - 1) / 2
    # stylobate (base platform), cracked
    sy = cy + r * 0.06
    out.append((x0 - pitch * 0.6, sy, x0 + pitch * (n - 1) + pitch * 0.6, sy, dark))
    out.append((x0 - pitch * 0.55, sy + r * 0.10,
                x0 + pitch * (n - 1) + pitch * 0.55, sy + r * 0.10, dark))
    ckx = cx + rnd.uniform(-pitch, pitch)
    out.append((ckx, sy, ckx + r * 0.08, sy + r * 0.10, dark))
    broken_i = rnd.randrange(n)
    for i in range(n):
        out += _column(x0 + pitch * i, cy, h, w, ink, dark, rnd,
                       broken=(i == broken_i))
    # architrave fragment bridging the tallest neighbours
    span = [i for i in range(n) if i != broken_i]
    if len(span) >= 2 and span[1] - span[0] == 1:
        ax0 = x0 + pitch * span[0] - w * 1.4
        ax1 = x0 + pitch * span[1] + w * 1.4
        ty = cy - h - r * 0.09
        frag = [(ax0, ty), (ax1, ty), (ax1, ty - r * 0.14),
                (ax0 + r * 0.1, ty - r * 0.14)]
        out += _outline(frag, ink)
        out += _hatch(frag, ink, r * 0.07)
    # the toppled shaft in the foreground
    out += _toppled(cx + rnd.uniform(-r * 0.3, r * 0.3), cy + r * 0.45,
                    h * 0.55, w * 1.05, ink, dark, rnd)
    return out


def cracked_dome(cx, cy, r, ink=INK, dark=DARK, seed=0):
    """A half-collapsed rotunda: dome shell intact on the left, sheared away
    on the right; full columns under the standing half, stumps under the gap,
    rock rubble spilling on the ground below the collapse."""
    rnd = random.Random(seed)
    out = []
    R = r * 0.95                        # dome half-span
    base_y = cy
    col_h = r * 1.05
    spring_y = base_y - col_h
    # stylobate
    out.append((cx - R * 1.15, base_y, cx + R * 1.15, base_y, dark))
    out.append((cx - R * 1.1, base_y + r * 0.08, cx + R * 1.1, base_y + r * 0.08, dark))
    # entablature slab (only survives over the standing half)
    ey = spring_y - r * 0.10
    slab = [(cx - R * 1.08, spring_y), (cx + R * 0.28, spring_y),
            (cx + R * 0.18, ey), (cx - R * 1.08, ey)]
    out += _outline(slab, ink)
    # columns
    w = r * 0.10
    for t in (-0.9, -0.5, -0.1, 0.45, 0.9):
        x = cx + R * t
        stump = t > 0.2
        h = col_h * (rnd.uniform(0.32, 0.5) if stump else 1.0)
        shaft = [(x - w, base_y), (x - w * 0.85, base_y - h),
                 (x + w * 0.85, base_y - h), (x + w, base_y)]
        out += _outline(shaft, ink)
        # drum joints + right-edge shade
        for k in range(1, 3 if stump else 5):
            yy = base_y - h * k / (3 if stump else 5)
            out.append((x - w * 0.9, yy, x + w * 0.9, yy, dark))
        out.append((x + w * 0.55, base_y, x + w * 0.5, base_y - h, dark))
        if stump:   # sheared top
            out.append((x - w * 0.85, base_y - h, x + w * 0.5,
                        base_y - h - r * 0.06, dark))
    # dome shell: springs from the entablature, breaks past the crown
    steps = 16
    break_t = rnd.uniform(0.60, 0.70)
    shell = []
    for k in range(steps + 1):
        t = k / steps
        if t > break_t:
            break
        a = math.pi * (1 - t)
        shell.append((cx + math.cos(a) * R, ey - math.sin(a) * R * 0.85))
    bx, by = shell[-1]
    # jagged shear edge back down to the slab line
    shell += [(bx + r * 0.06, by + r * 0.14), (bx - r * 0.03, by + r * 0.22),
              (bx + r * 0.12, by + r * 0.34), (bx + r * 0.04, by + r * 0.46),
              (cx + R * 0.24, ey)]
    out += _outline(shell, ink)
    out += _hatch(shell, ink, r * 0.10)
    # ribs following the curve
    for rt in (0.22, 0.44):
        prev = None
        for k in range(steps + 1):
            t = k / steps
            if t > break_t * 0.96:
                break
            a = math.pi * (1 - t)
            p = (cx + math.cos(a) * R * (1 - rt * 0.35),
                 ey - math.sin(a) * R * 0.85 * (1 - rt))
            if prev and k % 2:
                out.append((prev[0], prev[1], p[0], p[1], dark))
            prev = p
    # shadow along the broken edge
    out += _hatch([(bx - r * 0.16, by + r * 0.05), (bx + r * 0.08, by + r * 0.1),
                   (bx + r * 0.1, by + r * 0.42), (cx + R * 0.22, ey),
                   (cx - r * 0.02, ey)], dark, r * 0.13)
    # rubble: irregular rock lumps on the ground under the gap
    for k in range(4):
        rx = cx + R * rnd.uniform(0.3, 1.0)
        ry = base_y - r * 0.02
        rr = r * rnd.uniform(0.08, 0.16)
        rock = [(rx - rr, ry), (rx - rr * 0.5, ry - rr * rnd.uniform(0.6, 1.0)),
                (rx + rr * rnd.uniform(0.2, 0.6), ry - rr * rnd.uniform(0.4, 0.8)),
                (rx + rr, ry)]
        out += _outline(rock, ink)
        out.append((rock[1][0], rock[1][1], rx + rr * 0.4, ry, dark))
    return out
