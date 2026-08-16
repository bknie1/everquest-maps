"""shade_diamonds.py -- fill the Historical (EQOA) diamond markers solid-ish.

Finds small closed diamond outlines in each zone's _3 layer (and any declared
extra ink/layer), then lays a few horizontal runs inside each so they read as
filled gems rather than empty outlines.

    python src/tools/shade_diamonds.py            # all zones, _3 violet
    python src/tools/shade_diamonds.py eastkarana --layer 2 --ink 130,82,12
"""
import argparse
import collections
import os

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def shade_file(path, ink, min_d=18, max_d=150):
    raw = open(path, encoding='utf-8').read().splitlines()
    segs = [(i, parse(l)) for i, l in enumerate(raw) if l.startswith('L')]
    cand = [(i, s) for i, s in segs if s[4] == ink]
    key = lambda q: (round(q[0], 1), round(q[1], 1))
    adj = collections.defaultdict(list)
    for i, s in cand:
        adj[key((s[0], s[1]))].append(i)
        adj[key((s[2], s[3]))].append(i)
    by_i = dict(cand)
    seen, new = set(), []
    filled = 0
    for i, _s in cand:
        if i in seen:
            continue
        stack, comp = [i], []
        while stack:
            j = stack.pop()
            if j in seen:
                continue
            seen.add(j)
            comp.append(j)
            s = by_i[j]
            for k in adj[key((s[0], s[1]))] + adj[key((s[2], s[3]))]:
                stack.append(k)
        if not 3 <= len(comp) <= 6:
            continue
        xs = [v for j in comp for v in (by_i[j][0], by_i[j][2])]
        ys = [v for j in comp for v in (by_i[j][1], by_i[j][3])]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        if not (min_d < w < max_d and min_d < h < max_d and 0.5 < w / h < 2.0):
            continue
        # scanline fill against the component
        strokes = [by_i[j] for j in comp]
        step = h / 5.0
        y = min(ys) + step * 0.7
        runs = []
        ok = True
        while y < max(ys):
            crossings = []
            for (x1, y1, x2, y2, _c) in strokes:
                if y1 == y2:
                    continue
                lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
                if lo <= y < hi:
                    crossings.append(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
            crossings.sort()
            if len(crossings) % 2:
                ok = False
                break
            for k in range(0, len(crossings), 2):
                a, b = crossings[k] + 1.2, crossings[k + 1] - 1.2
                if b - a > 2:
                    runs.append((a, y, b))
            y += step
        if ok and runs:
            filled += 1
            for (a, y0, b) in runs:
                new.append('L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d'
                           % (a, y0, b, y0, *ink))
    if new:
        out = [l for l in raw if l.strip()] + new
        open(path, 'w', newline='', encoding='utf-8').write(CRLF.join(out) + CRLF)
    return filled


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zones', nargs='*', help='default: every zone with a _3 file')
    ap.add_argument('--layer', default='3')
    ap.add_argument('--ink', default='150,90,150')
    args = ap.parse_args()
    ink = tuple(int(v) for v in args.ink.split(','))
    zones = args.zones
    if not zones:
        zones = sorted({f[:-6] for f in os.listdir(MAPS) if f.endswith('_3.txt')})
    total = 0
    for z in zones:
        p = os.path.join(MAPS, f'{z}_{args.layer}.txt')
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            continue
        n = shade_file(p, ink)
        if n:
            print(f'  {z}: {n} diamonds shaded')
            total += n
    print(f'{total} diamonds shaded')


if __name__ == '__main__':
    main()
