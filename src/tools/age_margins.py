"""age_margins.py -- old-paper edge treatment for a zone's margin band.

Shades the band just inside the frame with a sepia stipple vignette (dense at
the frame, fading inward) and sketches a small curled-corner fold at each inner
frame corner. Gives the sheet contrast against the off-map background so the
map reads as an object, not a floating drawing.

Avoids: every P-record label position in all the zone's layers, plus any
--avoid x0,x1,y0,y1 boxes (title, compass).

    python src/tools/age_margins.py qey2hh1 --avoid 2403,13717,-4248,-2907
"""
import argparse
import math
import os
import random

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'
SEPIA = (150, 126, 92)
SEPIA_DARK = (124, 102, 72)


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zone')
    ap.add_argument('--avoid', action='append', default=[], help='x0,x1,y0,y1 (repeatable)')
    ap.add_argument('--band', type=float, default=0.30,
                    help='stippled depth as a fraction of the margin width')
    ap.add_argument('--density', type=float, default=1.0)
    ap.add_argument('--seed', type=int, default=7)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    p2 = os.path.join(MAPS, args.zone + '_2.txt')
    raw = [l for l in open(p2, encoding='utf-8').read().splitlines() if l.strip()]
    segs = [parse(l) for l in raw if l.startswith('L')]
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    FX0, FX1, FY0, FY1 = min(xs), max(xs), min(ys), max(ys)     # frame extent

    # content extent from the base layer
    cxs, cys = [], []
    for l in open(os.path.join(MAPS, args.zone + '.txt'), encoding='utf-8'):
        if l.startswith('L'):
            f = l[2:].split(',')
            cxs += [float(f[0]), float(f[3])]
            cys += [float(f[1]), float(f[4])]
    CX0, CX1, CY0, CY1 = min(cxs), max(cxs), min(cys), max(cys)

    # keep-away points: labels from every layer
    marks = []
    for suf in ('', '_1', '_2', '_3'):
        p = os.path.join(MAPS, args.zone + suf + '.txt')
        if not os.path.isfile(p):
            continue
        for l in open(p, encoding='utf-8'):
            if l.startswith('P'):
                f = l[2:].split(',')
                marks.append((float(f[0]), float(f[1])))
    boxes = []
    for a in args.avoid:
        x0, x1, y0, y1 = (float(v) for v in a.split(','))
        boxes.append((min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)))

    span = max(FX1 - FX0, FY1 - FY0)
    out = []

    def blocked(x, y):
        if any(abs(x - mx) < span * 0.035 and abs(y - my) < span * 0.012 for mx, my in marks):
            return True
        return any(b[0] - 40 < x < b[1] + 40 and b[2] - 40 < y < b[3] + 40 for b in boxes)

    def stipple(x, y, ink):
        a = rng.uniform(0, math.pi)
        L = rng.uniform(0.0015, 0.004) * span
        out.append((x - math.cos(a) * L, y - math.sin(a) * L * 0.35,
                    x + math.cos(a) * L, y + math.sin(a) * L * 0.35, ink))

    # four margin strips: for each, walk a grid; probability falls off inward
    margins = [
        ('top',    FX0, FX1, FY0, CY0), ('bottom', FX0, FX1, CY1, FY1),
        ('left',   FX0, CX0, CY0, CY1), ('right',  CX1, FX1, CY0, CY1),
    ]
    step = span * 0.008
    for (side, x0, x1, y0, y1) in margins:
        w = (y1 - y0) if side in ('top', 'bottom') else (x1 - x0)
        if w <= 0:
            continue
        depth = w * args.band
        y = y0 + step / 2
        while y < y1:
            x = x0 + step / 2
            while x < x1:
                # distance to the frame edge of this strip
                if side == 'top':      d = y - y0
                elif side == 'bottom': d = y1 - y
                elif side == 'left':   d = x - x0
                else:                  d = x1 - x
                t = d / max(depth, 1e-9)
                if t < 1.0:
                    p = (1.0 - t) ** 2 * 0.55 * args.density
                    if rng.random() < p and not blocked(x, y):
                        stipple(x + rng.uniform(-step/2, step/2),
                                y + rng.uniform(-step/2, step/2),
                                SEPIA_DARK if t < 0.3 else SEPIA)
                x += step
            y += step

    # curled corners: nested quarter-arcs at each inner frame corner
    r0 = span * 0.018
    for (cx, cy, sx, sy) in ((FX0, FY0, 1, 1), (FX1, FY0, -1, 1),
                             (FX0, FY1, 1, -1), (FX1, FY1, -1, -1)):
        for k, rr in enumerate((r0, r0 * 0.72, r0 * 0.45)):
            prev = None
            for i in range(7):
                a = math.pi / 2 * i / 6
                px = cx + sx * rr * math.cos(a)
                py = cy + sy * rr * math.sin(a)
                if prev:
                    out.append((prev[0], prev[1], px, py, SEPIA_DARK if k == 0 else SEPIA))
                prev = (px, py)

    raw += ['L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d' % (a, b, c, d, *ink)
            for (a, b, c, d, ink) in out]
    open(p2, 'w', newline='', encoding='utf-8').write(CRLF.join(raw) + CRLF)
    print(f'{args.zone}: aged margins with {len(out)} strokes')


if __name__ == '__main__':
    main()
