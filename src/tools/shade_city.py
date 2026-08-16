"""shade_city.py -- detect building footprints in a city base layer and style them.

The algorithm:
  1. take the base layer's strokes in the declared wall ink(s)
  2. connected components over shared endpoints = candidate structures
  3. a component is a BUILDING if it is closed enough to fill (scanline parity
     works row by row), building-sized (bbox between --min-frac and --max-frac
     of the map span), and dense (enough strokes to be a footprint, not a stray)
  4. fill each building's interior with tinted roof runs, then overpaint the
     lower third with a darker shadow ink offset slightly right -- the hand-drawn
     "sun from the northwest" look
  5. fills are inserted at the TOP of the file so all linework draws over them

Per-city palettes live in STYLES. A zone can list several wall inks; each may
carry its own roof/shadow override, else the zone default applies.

    python src/tools/shade_city.py qeynos --probe     # ink census + component sizes
    python src/tools/shade_city.py qeynos             # apply styling
    python src/tools/shade_city.py qeynos --dry-run
"""
import argparse
import collections
import os
import sys

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')
CRLF = '\r\n'

# zone -> dict(walls=[ink,...], roof=(r,g,b), shadow=(r,g,b), step=..., style=...)
# Palettes follow src/docs/CITY_MOTIFS.md. "A LOT of color" -- tints are strong
# enough to read at a glance but stay under the linework and labels.
STYLES = {
    'qeynos':    dict(roof=(96, 128, 170), shadow=(64, 92, 130)),    # slate blue, Camelot
    'qeynos2':   dict(roof=(96, 128, 170), shadow=(64, 92, 130)),
    'freportn':  dict(roof=(196, 150, 96), shadow=(150, 108, 62)),   # sandstone
    'freportw':  dict(roof=(196, 150, 96), shadow=(150, 108, 62)),
    'freporte':  dict(roof=(196, 150, 96), shadow=(150, 108, 62)),
    'halas':     dict(roof=(206, 216, 226), shadow=(150, 168, 186)), # snow-capped
    'rivervale': dict(roof=(150, 170, 90), shadow=(110, 128, 66)),   # turf roofs
    'erudnext':  dict(roof=(170, 178, 186), shadow=(120, 132, 146)), # pale stone
    'erudnint':  dict(roof=(170, 178, 186), shadow=(120, 132, 146)),
    'paineel':   dict(roof=(130, 110, 150), shadow=(90, 70, 110)),   # heretic violet
    'akanon':    dict(roof=(180, 140, 80), shadow=(130, 96, 52)),    # brass
    'kaladima':  dict(roof=(160, 140, 120), shadow=(116, 100, 84)),  # hewn stone
    'kaladimb':  dict(roof=(160, 140, 120), shadow=(116, 100, 84)),
    'felwithea': dict(roof=(200, 176, 110), shadow=(156, 132, 74)),  # gold
    'felwitheb': dict(roof=(200, 176, 110), shadow=(156, 132, 74)),
    'neriaka':   dict(roof=(120, 90, 150), shadow=(84, 60, 110)),    # teir'dal indigo
    'neriakb':   dict(roof=(120, 90, 150), shadow=(84, 60, 110)),
    'neriakc':   dict(roof=(120, 90, 150), shadow=(84, 60, 110)),
    'oggok':     dict(roof=(140, 128, 96), shadow=(100, 90, 64)),    # weathered marble
    'grobb':     dict(roof=(120, 104, 72), shadow=(86, 74, 50)),     # mud
    'kerraridge': dict(roof=(180, 160, 110), shadow=(136, 118, 76)), # thatch
    'rathemtn':  dict(roof=(110, 140, 110), shadow=(78, 104, 78)),   # froglok moss
    'gfaydark':  dict(roof=(130, 110, 76), shadow=(94, 78, 52)),     # kelethin timber
    'qcat':      dict(roof=(120, 112, 100), shadow=(86, 80, 70)),    # catacomb stone
}


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def components(segs):
    key = lambda q: (round(q[0], 1), round(q[1], 1))
    adj = collections.defaultdict(list)
    for i, s in enumerate(segs):
        adj[key((s[0], s[1]))].append(i)
        adj[key((s[2], s[3]))].append(i)
    seen, out = set(), []
    for i in range(len(segs)):
        if i in seen:
            continue
        stack, comp = [i], []
        while stack:
            j = stack.pop()
            if j in seen:
                continue
            seen.add(j)
            comp.append(j)
            s = segs[j]
            for k in adj[key((s[0], s[1]))] + adj[key((s[2], s[3]))]:
                stack.append(k)
        out.append(comp)
    return out


def fill_component(strokes, step, inset=1.5, dedupe=3.0, min_run=4.0, stitch=40.0):
    """Even-odd scanline fill of one component. Returns runs; odd rows skipped.

    Loose endpoints (doorways, sloppy corners) are stitched shut first when the
    gap is small -- a building with an open door should still get a roof.
    """
    cnt = {}
    for (x1, y1, x2, y2, _c) in strokes:
        for p in ((round(x1, 1), round(y1, 1)), (round(x2, 1), round(y2, 1))):
            cnt[p] = cnt.get(p, 0) + 1
    loose = [p for p, c in cnt.items() if c == 1]
    used = set()
    strokes = list(strokes)
    for i, p in enumerate(loose):
        if p in used:
            continue
        best, bd = None, stitch
        for q in loose[i + 1:]:
            if q in used:
                continue
            d = ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5
            if d < bd:
                best, bd = q, d
        if best:
            strokes.append((p[0], p[1], best[0], best[1], None))
            used.update((p, best))
    ys = [v for s in strokes for v in (s[1], s[3])]
    y = min(ys) + step * 0.6
    runs = []
    while y < max(ys):
        xs = []
        for (x1, y1, x2, y2, _c) in strokes:
            if y1 == y2:
                continue
            lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
            if lo <= y < hi:
                xs.append(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
        xs.sort()
        dd = []
        for x in xs:
            if dd and x - dd[-1] < dedupe:
                continue
            dd.append(x)
        if len(dd) % 2 == 0:
            for i in range(0, len(dd), 2):
                a, b = dd[i] + inset, dd[i + 1] - inset
                if b - a >= min_run:
                    runs.append((a, y, b))
        y += step
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zone')
    ap.add_argument('--walls', action='append', default=[],
                    help='r,g,b wall ink (repeatable); required unless --probe')
    ap.add_argument('--roof', help='r,g,b override')
    ap.add_argument('--shadow', help='r,g,b override')
    ap.add_argument('--step', type=float, default=7.0)
    ap.add_argument('--min-frac', type=float, default=0.004,
                    help='min building bbox size as fraction of map span')
    ap.add_argument('--max-frac', type=float, default=0.12,
                    help='max building bbox size as fraction of map span')
    ap.add_argument('--min-strokes', type=int, default=4)
    ap.add_argument('--probe', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    path = os.path.join(MAPS, args.zone + '.txt')
    raw = open(path, encoding='utf-8').read().splitlines()
    segs = [parse(l) for l in raw if l.startswith('L')]
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    span = max(max(xs) - min(xs), max(ys) - min(ys))

    if args.probe:
        census = collections.Counter(s[4] for s in segs)
        print('ink census (top 12):')
        for ink, n in census.most_common(12):
            print('   ', ink, n)
        for ink, n in census.most_common(6):
            sub = [s for s in segs if s[4] == ink]
            comps = components(sub)
            sized = 0
            for c in comps:
                cx = [v for j in c for v in (sub[j][0], sub[j][2])]
                cy = [v for j in c for v in (sub[j][1], sub[j][3])]
                d = max(max(cx) - min(cx), max(cy) - min(cy))
                if args.min_frac * span < d < args.max_frac * span and len(c) >= args.min_strokes:
                    sized += 1
            print(f'ink {ink}: {len(comps)} components, {sized} building-sized')
        return

    style = STYLES.get(args.zone, {})
    roof = tuple(int(v) for v in args.roof.split(',')) if args.roof else style.get('roof')
    shadow = tuple(int(v) for v in args.shadow.split(',')) if args.shadow else style.get('shadow')
    if not (args.walls and roof and shadow):
        sys.exit('need --walls and a palette (STYLES entry or --roof/--shadow); try --probe first')
    wall_inks = [tuple(int(v) for v in w.split(',')) for w in args.walls]

    sub = [s for s in segs if s[4] in wall_inks]
    new = []
    n_build = 0
    for comp in components(sub):
        strokes = [sub[j] for j in comp]
        cx = [v for s in strokes for v in (s[0], s[2])]
        cy = [v for s in strokes for v in (s[1], s[3])]
        d = max(max(cx) - min(cx), max(cy) - min(cy))
        if not (args.min_frac * span < d < args.max_frac * span):
            continue
        if len(comp) < args.min_strokes:
            continue
        runs = fill_component(strokes, args.step)
        if not runs:
            continue
        n_build += 1
        y_shadow = min(cy) + (max(cy) - min(cy)) * 0.62   # lower third = shadow side
        for (a, y, b) in runs:
            ink = shadow if y > y_shadow else roof
            off = 1.5 if y > y_shadow else 0.0            # nudge shadow right
            new.append('L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d'
                       % (a + off, y, b + off, y, *ink))

    print(f'{args.zone}: {n_build} buildings styled, {len(new)} fill runs')
    if args.dry_run or not new:
        return
    out = new + [l for l in raw if l.strip()]
    open(path, 'w', newline='', encoding='utf-8').write(CRLF.join(out) + CRLF)


if __name__ == '__main__':
    main()
