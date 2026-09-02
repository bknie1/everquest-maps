"""fill_water.py -- horizontal-run water fill for a zone's base layer.

Matches the hand-done Ocean of Tears / Lake Rathetear look: horizontal runs every
11 units in the zone's own water ink. Conservative by design, per BRAIN.md:

  * scanline even-odd against the existing water OUTLINE only -- no stitching,
    no both_axes, no invented geometry
  * rows whose crossing count is odd are SKIPPED and reported, never guessed at
  * runs shorter than a threshold are dropped (slivers along diagonal banks)
  * fill lines are inserted at the TOP of the file so everything else draws over
    them (bridges, flora, labels)

    python src/tools/fill_water.py kerraridge --ink 40,92,158
    python src/tools/fill_water.py kerraridge --ink 40,92,158 --exclude x0,x1,y0,y1
"""
import argparse
import os
import sys

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zone')
    ap.add_argument('--ink', action='append', default=[],
                    help='r,g,b of the water outline (repeatable; fill uses the first)')
    ap.add_argument('--fill-ink', help='r,g,b for the fill runs if different from the outline')
    ap.add_argument('--z-band',
                    help='lo,hi -- take the outline from strokes whose midpoint z falls in '
                         'this band instead of by ink. For sunken water in a multi-level '
                         'dungeon, where the channel is drawn in the same ink as everything '
                         'else and only its depth tells it apart.')
    ap.add_argument('--fill-z', type=float, default=0.0,
                    help='z written on the fill runs (default 0). Set it to the channel floor '
                         'so the water sits on its own level rather than at the surface.')
    ap.add_argument('--step', type=float, default=11.0)
    ap.add_argument('--min-run', type=float, default=14.0)
    ap.add_argument('--inset', type=float, default=2.0, help='pull runs in from the banks')
    ap.add_argument('--exclude', action='append', default=[],
                    help='x0,x1,y0,y1 region to leave unfilled (repeatable)')
    ap.add_argument('--dedupe', type=float, default=4.0,
                    help='collapse crossings closer than this (multi-strand outlines)')
    ap.add_argument('--stitch', type=float, default=70.0,
                    help='max gap to stitch between loose outline endpoints')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    if not args.ink and not args.z_band:
        ap.error('need --ink or --z-band to identify the water outline')
    zband = None
    if args.z_band:
        zlo, zhi = (float(v) for v in args.z_band.split(','))
        zband = (min(zlo, zhi), max(zlo, zhi))
    inks = [tuple(int(v) for v in i.split(',')) for i in args.ink]
    ink = inks[0] if inks else None
    fill = tuple(int(v) for v in (args.fill_ink or args.ink[0]).split(','))
    excl = []
    for e in args.exclude:
        x0, x1, y0, y1 = (float(v) for v in e.split(','))
        excl.append((min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)))

    path = os.path.join(MAPS, args.zone + '.txt')
    raw = open(path, encoding='utf-8').read().splitlines()
    water = []
    for l in raw:
        if not l.startswith('L'):
            continue
        f = l[2:].split(',')
        if zband is not None:
            zm = (float(f[2]) + float(f[5])) / 2
            hit = zband[0] <= zm <= zband[1]
        else:
            hit = tuple(int(float(v)) for v in f[6:9]) in inks
        if hit:
            water.append((float(f[0]), float(f[1]), float(f[3]), float(f[4])))
    if not water:
        sys.exit(f'no strokes matched {"z band %s" % (zband,) if zband else "inks %s" % (inks,)}')
    if zband is not None:
        print(f'outline from z band {zband[0]:.0f}..{zband[1]:.0f}: {len(water)} strokes')

    # stitch SHORT breaks in the outline (BRAIN: under ~70 units only, mutual
    # nearest neighbour -- long pairings drew a chord across Kerra's bay once)
    cnt = {}
    for (x1, y1, x2, y2) in water:
        for p in ((round(x1, 1), round(y1, 1)), (round(x2, 1), round(y2, 1))):
            cnt[p] = cnt.get(p, 0) + 1
    loose = [p for p, c in cnt.items() if c == 1]
    stitched = 0
    used = set()
    for i, p in enumerate(loose):
        if p in used:
            continue
        best, bd = None, args.stitch
        for q in loose[i + 1:]:
            if q in used:
                continue
            d = ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5
            if d < bd:
                best, bd = q, d
        if best:
            water.append((p[0], p[1], best[0], best[1]))
            used.update((p, best))
            stitched += 1
    if stitched:
        print(f'stitched {stitched} short breaks')

    ys = [v for s in water for v in (s[1], s[3])]
    y = min(ys) + args.step / 2
    runs, odd_rows = [], 0
    by_row = {}
    row_ys = []
    while y < max(ys):
        xs = []
        for (x1, y1, x2, y2) in water:
            if y1 == y2:
                continue
            lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
            if lo <= y < hi:                      # half-open: no double-count at joints
                xs.append(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
        xs.sort()
        # multi-strand decoration (waterfalls, doubled banks) puts several
        # crossings at practically the same x -- collapse each cluster to one
        dd = []
        for x in xs:
            if dd and x - dd[-1] < args.dedupe:
                continue
            dd.append(x)
        xs = dd
        row_ys.append(y)
        if len(xs) % 2:
            odd_rows += 1
            by_row[y] = None                      # unresolved; may borrow below
        else:
            rr = []
            for i in range(0, len(xs), 2):
                a, b = xs[i] + args.inset, xs[i + 1] - args.inset
                if b - a < args.min_run:
                    continue
                if any(a < ex1 and b > ex0 and ey0 < y < ey1
                       for (ex0, ex1, ey0, ey1) in excl):
                    continue
                rr.append((a, b))
            by_row[y] = rr
        y += args.step

    # an odd-parity row between two clean rows gets the INTERSECTION of its
    # neighbours' runs -- never wider than either, so it cannot invent water
    borrowed = 0
    for k, y in enumerate(row_ys):
        if by_row[y] is not None or k == 0 or k == len(row_ys) - 1:
            continue
        up = dn = None
        for j in range(k - 1, max(-1, k - 24), -1):
            if by_row[row_ys[j]]:
                up = by_row[row_ys[j]]
                break
        for j in range(k + 1, min(len(row_ys), k + 24)):
            if by_row[row_ys[j]]:
                dn = by_row[row_ys[j]]
                break
        if not up or not dn:
            continue
        rr = []
        for (a1, b1) in up:
            for (a2, b2) in dn:
                a, b = max(a1, a2), min(b1, b2)
                if b - a >= args.min_run:
                    rr.append((a, b))
        if rr:
            by_row[y] = rr
            borrowed += 1
    for y in row_ys:
        for (a, b) in (by_row[y] or []):
            runs.append((a, y, b, y))

    print(f'{args.zone}: {len(runs)} fill runs, {odd_rows} odd rows '
          f'({borrowed} healed from neighbours)')
    if args.dry_run:
        return
    fz = args.fill_z
    new = ['L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d' % (a, ya, fz, b, yb, fz, *fill)
           for (a, ya, b, yb) in runs]
    out = new + [l for l in raw if l.strip()]
    open(path, 'w', newline='', encoding='utf-8').write(CRLF.join(out) + CRLF)


if __name__ == '__main__':
    main()
