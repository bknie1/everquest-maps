"""add_legend.py -- place an information block OUTSIDE the map, off the left edge.

Legends, key chains, camp notes: they live in open space left of everything
the zone draws, so they can never conflict with geometry, margins, or labels.
They go in the BASE layer (layer 0) so they are always visible.

Re-running replaces the previous block (any base-layer P record left of the
zone's drawn extent is treated as legend content and owned by this tool).

    python src/tools/add_legend.py unrest --line "KEY CHAIN:" --line "K1 ..." ...
    python src/tools/add_legend.py unrest --from-file legend.txt
    python src/tools/add_legend.py unrest --clear
"""
import argparse
import os

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'
INK = (30, 80, 95)


def extent(zone):
    xs, ys = [], []
    for suf in ('', '_1', '_2', '_3'):
        p = os.path.join(MAPS, zone + suf + '.txt')
        if not os.path.isfile(p):
            continue
        for l in open(p, encoding='utf-8'):
            if l.startswith('L'):
                f = l[2:].split(',')
                xs += [float(f[0]), float(f[3])]
                ys += [float(f[1]), float(f[4])]
    return min(xs), max(xs), min(ys), max(ys)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zone')
    ap.add_argument('--line', action='append', default=[], help='legend line (repeatable, underscores or spaces)')
    ap.add_argument('--from-file', help='text file, one legend line per row')
    ap.add_argument('--clear', action='store_true')
    ap.add_argument('--gap-frac', type=float, default=0.06,
                    help='gap between the drawn extent and the block, as span fraction')
    ap.add_argument('--top-frac', type=float, default=0.10,
                    help='block top as fraction below the drawn top edge')
    args = ap.parse_args()

    lines = [l.replace(' ', '_') for l in args.line]
    if args.from_file:
        lines += [l.strip().replace(' ', '_')
                  for l in open(args.from_file, encoding='utf-8') if l.strip()]

    DX0, DX1, DY0, DY1 = extent(args.zone)
    span = max(DX1 - DX0, DY1 - DY0)
    path = os.path.join(MAPS, args.zone + '.txt')
    raw = open(path, encoding='utf-8').read().splitlines()

    kept, removed = [], 0
    for l in raw:
        if l.startswith('P'):
            f = [v.strip() for v in l[2:].split(',')]
            if float(f[0]) < DX0 - span * 0.01:     # previous legend block
                removed += 1
                continue
        if l.strip():
            kept.append(l)

    if not args.clear and lines:
        lx = DX0 - span * args.gap_frac - span * 0.14   # room for text drawn rightward
        ly = DY0 + span * args.top_frac
        step = span * 0.026
        for i, t in enumerate(lines):
            kept.append('P %.4f, %.4f, 0.0000, %d, %d, %d, 2, %s' % (lx, ly + i * step, *INK, t))
    open(path, 'w', newline='', encoding='utf-8').write(CRLF.join(kept) + CRLF)
    print(f'{args.zone}: removed {removed} old legend records, placed {0 if args.clear else len(lines)}')


if __name__ == '__main__':
    main()
