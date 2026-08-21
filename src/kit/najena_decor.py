"""najena_decor.py -- the signature Najena banner (from Brandon's in-game capture).

A hanging gold banner bearing Najena the dark-elf sorceress in silhouette -- a
robed figure with flowing hair -- beneath a crescent moon. The zone's identity.

    from najena_decor import banner
    segs = banner(cx, cy, w, h, seed=0)   # (cx,cy) = banner centre
"""
import math
import random

GOLD = (176, 150, 104)
FRAME = (150, 120, 70)
DARK = (52, 44, 54)          # near-black silhouette
MOON = (210, 205, 185)


def _hatch(poly, ink, step, rnd, jit=1.0):
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
                w = rnd.uniform(-jit, jit)
                out.append((xs[i], y + w, xs[i + 1], y + w, ink))
        y += step
    return out


def banner(cx, cy, w, h, seed=0):
    rnd = random.Random(seed)
    out = []
    def L(a, b, c, d, ink): out.append((a, b, c, d, ink))
    def arc(ccx, ccy, r, a0, a1, ink, n=10):
        for k in range(n):
            a = a0 + (a1 - a0) * k / n
            b = a0 + (a1 - a0) * (k + 1) / n
            L(ccx + r * math.cos(a), ccy + r * math.sin(a),
              ccx + r * math.cos(b), ccy + r * math.sin(b), ink)

    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    # top rod
    L(x0 - w * 0.10, y0, x1 + w * 0.10, y0, FRAME)
    L(x0 - w * 0.10, y0 - h * 0.02, x1 + w * 0.10, y0 - h * 0.02, FRAME)
    # cloth outline with a pointed pennant bottom
    cloth = [(x0, y0), (x1, y0), (x1, y1 - h * 0.14), (cx, y1), (x0, y1 - h * 0.14)]
    for i in range(len(cloth)):
        L(*cloth[i], *cloth[(i + 1) % len(cloth)], FRAME)
    out += _hatch(cloth, GOLD, h * 0.05, rnd)
    # crescent moon upper area
    mcx, mcy, mr = cx + w * 0.20, y0 + h * 0.15, w * 0.16
    arc(mcx, mcy, mr, 0.6, 2 * math.pi - 0.6, MOON)
    arc(mcx + mr * 0.5, mcy, mr, 1.9, 2 * math.pi - 1.9, MOON, 6)
    # Najena silhouette: head + shoulders + a fuller, flowing robe to a flame point
    hx, hy, hr = cx - w * 0.04, y0 + h * 0.30, w * 0.12
    arc(hx, hy, hr, 0, 2 * math.pi, DARK, 14)
    robe = [(hx - hr * 1.0, hy + hr * 0.6), (hx - w * 0.26, cy + h * 0.06),
            (hx - w * 0.20, y1 - h * 0.16), (hx - w * 0.08, y1 - h * 0.06),
            (hx, y1 - h * 0.12), (hx + w * 0.08, y1 - h * 0.05),
            (hx + w * 0.20, y1 - h * 0.16), (hx + w * 0.26, cy + h * 0.04),
            (hx + hr * 1.0, hy + hr * 0.6)]
    for i in range(len(robe) - 1):
        L(*robe[i], *robe[i + 1], DARK)
    out += _hatch(robe + [robe[0]], DARK, h * 0.032, rnd, 0.6)
    # flowing hair strands off the head
    for k in range(3):
        sx = hx - hr * 0.6 + k * hr * 0.6
        L(sx, hy + hr * 0.4, sx - w * 0.05, cy - h * 0.02, DARK)
    return out
