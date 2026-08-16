"""move_title.py -- relocate a zone's title block to the bottom (or top) margin.

Some zones want their top margin for art (a landmark visible to the north);
the title moves to the bottom margin, otherwise unchanged: same inks, same
letterforms, same rules, re-centered vertically in the destination band.

The title block is taken as EVERY stroke inside the given box (letters, shadow
letters, underline rules), so pass a box that contains the title and nothing
you want left behind.

    python src/tools/move_title.py northkarana --box=-2450,2080,-2560,-2100 --to bottom
"""
import argparse
import os
import sys

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zone')
    ap.add_argument('--box', required=True, help='x0,x1,y0,y1 containing the whole title block')
    ap.add_argument('--to', choices=('bottom', 'top'), default='bottom')
    args = ap.parse_args()
    x0, x1, y0, y1 = (float(v) for v in args.box.split(','))
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)

    # content extent from base; deco extent for the margin depth
    cys = []
    for l in open(os.path.join(MAPS, args.zone + '.txt'), encoding='utf-8'):
        if l.startswith('L'):
            f = l[2:].split(',')
            cys += [float(f[1]), float(f[4])]
    CY0, CY1 = min(cys), max(cys)

    p2 = os.path.join(MAPS, args.zone + '_2.txt')
    raw = open(p2, encoding='utf-8').read().splitlines()
    segs = {i: parse(l) for i, l in enumerate(raw) if l.startswith('L')}
    dys = [v for s in segs.values() for v in (s[1], s[3])]
    DY0, DY1 = min(dys), max(dys)

    block = [i for i, s in segs.items()
             if x0 <= min(s[0], s[2]) and max(s[0], s[2]) <= x1
             and y0 <= min(s[1], s[3]) and max(s[1], s[3]) <= y1]
    if len(block) < 10:
        sys.exit(f'only {len(block)} strokes in the box -- wrong box?')
    bys = [v for i in block for v in (segs[i][1], segs[i][3])]
    bh = max(bys) - min(bys)

    if args.to == 'bottom':
        margin_h = DY1 - CY1
        new_top = CY1 + (margin_h - bh) / 2
    else:
        margin_h = CY0 - DY0
        new_top = DY0 + (margin_h - bh) / 2
    dy = new_top - min(bys)

    out = []
    moved = 0
    for i, l in enumerate(raw):
        if i in block:
            s = segs[i]
            out.append('L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d'
                       % (s[0], s[1] + dy, s[2], s[3] + dy, *s[4]))
            moved += 1
        elif l.strip():
            out.append(l)
    open(p2, 'w', newline='', encoding='utf-8').write(CRLF.join(out) + CRLF)
    print(f'{args.zone}: moved {moved} title strokes {"down" if dy > 0 else "up"} by {abs(dy):.0f}')


if __name__ == '__main__':
    main()
