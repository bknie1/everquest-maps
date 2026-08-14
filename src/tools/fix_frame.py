"""fix_frame.py -- find and fill gaps in a zone's drawn frame (the jagged border).

Title knockouts have repeatedly eaten frame segments under the title band, and
some rebuilt zones shipped with sides missing entirely. This walks each side of
the deco layer's bounding box, measures which stretches a frame ink actually
covers, and fills the gaps with a matching jagged line.

  * rails are declared by ink (--ink, repeatable), probed with --probe
  * per side, covered intervals come from projecting that ink's strokes near the
    edge; gaps wider than --min-gap get filled
  * fill jags match the measured amplitude of the existing rail and jag OUTWARD
    (away from content), so they cannot cross titles or the map
  * obstacle clusters (a compass, a candle) in the band are skipped, leaving
    their span open rather than drawing through them

    python src/tools/fix_frame.py tox --probe
    python src/tools/fix_frame.py tox --ink 150,60,25 --ink 45,95,55
"""
import argparse
import collections
import math
import os
import random
import sys

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'
SIDES = ('top', 'bottom', 'left', 'right')


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def side_of(s, bb, band):
    """Which edge band a stroke's midpoint sits in, if any."""
    x0, x1, y0, y1 = bb
    mx, my = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
    if my < y0 + band: return 'top'
    if my > y1 - band: return 'bottom'
    if mx < x0 + band: return 'left'
    if mx > x1 - band: return 'right'
    return None


def project(s, side):
    """(lo, hi) of the stroke along the side's axis, plus its rail offset coord."""
    if side in ('top', 'bottom'):
        return min(s[0], s[2]), max(s[0], s[2]), (s[1] + s[3]) / 2
    return min(s[1], s[3]), max(s[1], s[3]), (s[0] + s[2]) / 2


def union(intervals):
    out = []
    for a, b in sorted(intervals):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zone')
    ap.add_argument('--ink', action='append', default=[], help='r,g,b of a frame rail (repeatable)')
    ap.add_argument('--probe', action='store_true', help='report per-side ink coverage and exit')
    ap.add_argument('--band-frac', type=float, default=0.035,
                    help='edge band as a fraction of the deco span')
    ap.add_argument('--min-gap', type=float, default=None,
                    help='smallest gap to fill (default 2.5%% of span)')
    ap.add_argument('--sides', default='top,bottom,left,right')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    path = os.path.join(MAPS, args.zone + '_2.txt')
    raw = open(path, encoding='utf-8').read().splitlines()
    segs = [parse(l) for l in raw if l.startswith('L')]
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    bb = (min(xs), max(xs), min(ys), max(ys))
    span = max(bb[1] - bb[0], bb[3] - bb[2])
    band = span * args.band_frac
    min_gap = args.min_gap if args.min_gap is not None else span * 0.025

    by_side = collections.defaultdict(lambda: collections.defaultdict(list))
    for s in segs:
        sd = side_of(s, bb, band)
        if sd:
            by_side[sd][s[4]].append(s)

    side_len = {sd: (bb[1] - bb[0]) if sd in ('top', 'bottom') else (bb[3] - bb[2])
                for sd in SIDES}

    if args.probe:
        for sd in SIDES:
            for ink, ss in sorted(by_side[sd].items(), key=lambda t: -len(t[1]))[:5]:
                cov = sum(b - a for a, b in union([project(s, sd)[:2] for s in ss]))
                print(f'{sd:6s} ink {ink}  strokes {len(ss):4d}  coverage {cov/side_len[sd]*100:4.0f}%')
        return

    inks = [tuple(int(v) for v in i.split(',')) for i in args.ink]
    if not inks:
        sys.exit('give at least one --ink (use --probe first)')

    # per ink and side: rail strokes = that ink's strokes whose midpoint offset
    # sits in the outer 15% toward the side (the deco bbox can start at a title
    # or margin art well outside the frame, so a thin edge band misses rails)
    def rail_strokes(ink, sd):
        deep = span * 0.15
        out = []
        for s in segs:
            if s[4] != ink:
                continue
            mx, my = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
            if sd == 'top' and my < bb[2] + deep: out.append(s)
            elif sd == 'bottom' and my > bb[3] - deep: out.append(s)
            elif sd == 'left' and mx < bb[0] + deep: out.append(s)
            elif sd == 'right' and mx > bb[1] - deep: out.append(s)
        return out

    new = []
    rng = random.Random(7)
    for sd in [s.strip() for s in args.sides.split(',')]:
        lo_edge = bb[0] if sd in ('top', 'bottom') else bb[2]
        hi_edge = bb[1] if sd in ('top', 'bottom') else bb[3]
        # obstacle spans: non-rail strokes in this band (compass, sketches),
        # kept with their offset so only things ON the rail line block a fill
        obstacle_raw = []
        for ink, ss in by_side[sd].items():
            if ink in inks:
                continue
            if len(ss) >= 12:
                obstacle_raw += [project(s, sd) for s in ss]
        for ink in inks:
            ss = rail_strokes(ink, sd)
            OPP = {'top': 'bottom', 'bottom': 'top', 'left': 'right', 'right': 'left'}
            if len(ss) >= 4:
                ivs = union([project(s, sd)[:2] for s in ss])
                rails = [project(s, sd)[2] for s in ss]
                rail = sorted(rails)[len(rails) // 2]
            else:
                # side missing entirely: mirror the opposite side's inset
                os_ = rail_strokes(ink, OPP[sd])
                if len(os_) < 4:
                    continue
                orails = sorted(project(s, OPP[sd])[2] for s in os_)
                orail = orails[len(orails) // 2]
                if sd == 'top':    rail = bb[2] + (bb[3] - orail)
                elif sd == 'bottom': rail = bb[3] - (orail - bb[2])
                elif sd == 'left': rail = bb[0] + (bb[1] - orail)
                else:              rail = bb[1] - (orail - bb[0])
                ivs = []
                rails = [rail]
            amp = max(8.0, (sorted(abs(r - rail) for r in rails)[int(len(rails) * 0.8)])
                      if len(rails) > 4 else 12.0)
            amp = min(amp, span * 0.012)   # corner strokes can inflate the estimate
            # the side runs corner to corner between the PERPENDICULAR rails,
            # not to the deco bbox (which may include margin art beyond them)
            lo, hi = lo_edge, hi_edge
            perp = ('left', 'right') if sd in ('top', 'bottom') else ('top', 'bottom')
            ps = rail_strokes(ink, perp[0])
            if len(ps) >= 4:
                pr = sorted(project(s, perp[0])[2] for s in ps)
                lo = pr[len(pr) // 2]
            ps = rail_strokes(ink, perp[1])
            if len(ps) >= 4:
                pr = sorted(project(s, perp[1])[2] for s in ps)
                hi = pr[len(pr) // 2]
            # outward direction: negative for top/left, positive for bottom/right
            out_sign = -1 if sd in ('top', 'left') else 1
            gaps = []
            prev = lo
            for a, b in ivs:
                if a - prev > min_gap:
                    gaps.append((prev, min(a, hi)))
                prev = max(prev, b)
            if hi - prev > min_gap:
                gaps.append((prev, hi))
            obstacles = union([(a, b) for (a, b, off) in obstacle_raw
                               if abs(off - rail) < amp * 2.5])
            for (a, b) in gaps:
                # carve out obstacle spans
                pieces = [(a, b)]
                for (oa, ob) in obstacles:
                    nxt = []
                    for (pa, pb) in pieces:
                        if ob < pa or oa > pb:
                            nxt.append((pa, pb))
                        else:
                            if oa - pa > min_gap * 0.6: nxt.append((pa, oa - 10))
                            if pb - ob > min_gap * 0.6: nxt.append((ob + 10, pb))
                    pieces = nxt
                for (pa, pb) in pieces:
                    n = max(2, int((pb - pa) / (span * 0.012)))
                    pts = []
                    for k in range(n + 1):
                        t = pa + (pb - pa) * k / n
                        off = rail + (out_sign * rng.uniform(0.35, 1.0) * amp if k % 2 else 0)
                        pts.append((t, off))
                    for k in range(n):
                        (t1, o1), (t2, o2) = pts[k], pts[k + 1]
                        if sd in ('top', 'bottom'):
                            new.append('L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d'
                                       % (t1, o1, t2, o2, *ink))
                        else:
                            new.append('L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d'
                                       % (o1, t1, o2, t2, *ink))
                    print(f'{sd:6s} ink {ink} filled {pa:.0f}..{pb:.0f} at rail {rail:.0f}')

    if not new:
        print(f'{args.zone}: no gaps to fill')
        return
    print(f'{args.zone}: adding {len(new)} strokes')
    if args.dry_run:
        return
    out = [l for l in raw if l.strip()] + new
    open(path, 'w', newline='', encoding='utf-8').write(CRLF.join(out) + CRLF)


if __name__ == '__main__':
    main()
