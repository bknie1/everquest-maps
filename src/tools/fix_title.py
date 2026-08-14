"""fix_title.py -- surgical title repair for a zone's _2 decoration layer.

Wipe-and-redraw, per BRAIN.md: broken lettering can't be extracted cleanly, so
find letter-like connected components in the band above the map content, remove
them, draw a fresh title with the toolkit stick font, then knock out whatever
still sits under the new title's box. Guards: title_health must not drop, and
the strip must stay narrow (abort if the wipe grabs too much).

    python src/tools/fix_title.py grobb GROBB
    python src/tools/fix_title.py erudsxing "ERUD'S CROSSING" --rules
    python src/tools/fix_title.py halas HALAS --no-wipe     # nothing to wipe, just draw
    python src/tools/fix_title.py innothule --trim-ends     # drop stray end glyphs only
"""
import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'toolkit'))
from eqmap_toolkit import LETTERS, CRLF

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def content_bbox(zone):
    xs, ys = [], []
    for l in open(os.path.join(MAPS, zone + '.txt'), encoding='utf-8'):
        if l.startswith('L'):
            f = l[2:].split(',')
            xs += [float(f[0]), float(f[3])]
            ys += [float(f[1]), float(f[4])]
    return min(xs), max(xs), min(ys), max(ys)


def components(segs, idxs):
    key = lambda q: (round(q[0], 1), round(q[1], 1))
    adj = collections.defaultdict(list)
    for i in idxs:
        s = segs[i]
        adj[key((s[0], s[1]))].append(i)
        adj[key((s[2], s[3]))].append(i)
    seen, comps = set(), []
    for i in idxs:
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
                if k not in seen:
                    stack.append(k)
        comps.append(comp)
    return comps


def bbox(segs, idx):
    xs = [a for j in idx for a in (segs[j][0], segs[j][2])]
    ys = [a for j in idx for a in (segs[j][1], segs[j][3])]
    return min(xs), max(xs), min(ys), max(ys)


def title_health(segs, grid_y0):
    key = lambda q: (round(q[0], 1), round(q[1], 1))
    band = [i for i, s in enumerate(segs) if (s[1] + s[3]) / 2 < grid_y0]
    adj = collections.defaultdict(list)
    for i in band:
        s = segs[i]
        adj[key((s[0], s[1]))].append(i)
        adj[key((s[2], s[3]))].append(i)
    return sum(1 for i in band
               if len(adj[key((segs[i][0], segs[i][1]))]) > 1
               or len(adj[key((segs[i][2], segs[i][3]))]) > 1)


ADV = lambda ch, cw: cw * 0.42 if ch in ("'", "`") else cw


def word_segs(text, ox, ybase, cw, h, gap):
    """Upright lettering in map coords: larger glyph-y means smaller map-y."""
    out, x = [], ox
    for ch in text:
        adv = ADV(ch, cw)
        for poly in LETTERS.get(ch, []):
            for i in range(len(poly) - 1):
                ax, ay = poly[i]
                bx, by = poly[i + 1]
                out.append((x + ax * adv, ybase - ay * h,
                            x + bx * adv, ybase - by * h))
        x += adv + gap
    return out


def group_width(text, cw, gap):
    return sum(ADV(c, cw) for c in text) + (len(text) - 1) * gap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zone')
    ap.add_argument('text', nargs='?', help='title text to draw (omit with --trim-ends)')
    ap.add_argument('--rules', action='store_true', help='rules above and below the title')
    ap.add_argument('--no-wipe', action='store_true', help='skip component wipe (title absent)')
    ap.add_argument('--trim-ends', action='store_true',
                    help='only delete the first and last glyph component of the found title row')
    ap.add_argument('--ink', help='r,g,b override for the new title')
    ap.add_argument('--max-wipe', type=float, default=0.25,
                    help='abort if the wipe exceeds this fraction of all strokes')
    ap.add_argument('--central', type=float, default=1.0,
                    help='restrict the wipe to this central fraction of the grid width')
    ap.add_argument('--allow-health-drop', action='store_true',
                    help='permit title_health to fall (wiping connected GARBAGE '
                         'lowers it by design); only use after a visual check')
    args = ap.parse_args()

    p2 = os.path.join(MAPS, args.zone + '_2.txt')
    raw = open(p2, encoding='utf-8').read().splitlines()
    segs = {i: parse(l) for i, l in enumerate(raw) if l.startswith('L')}
    seglist = list(segs.values())
    CX0, CX1, CY0, CY1 = content_bbox(args.zone)
    CW = CX1 - CX0
    scale = max(CW, CY1 - CY0)
    dtop = min(min(s[1], s[3]) for s in seglist)
    band_h = CY0 - dtop
    health_before = title_health(seglist, CY0)

    # --- find letter-like components strictly above the content, frame excluded
    half = CW * args.central / 2
    cx = (CX0 + CX1) / 2
    band_idx = [i for i, s in segs.items()
                if max(s[1], s[3]) < CY0 and min(s[1], s[3]) > dtop + 80
                and min(s[0], s[2]) > max(CX0 - CW * 0.05, cx - half)
                and max(s[0], s[2]) < min(CX1 + CW * 0.05, cx + half)]
    drop = set()
    if args.trim_ends or not args.no_wipe:
        comps = []
        for comp in components(segs, band_idx):
            x0, x1, y0, y1 = bbox(segs, comp)
            if len(comp) > 60 or (x1 - x0) > CW * 0.40 or (y1 - y0) > band_h * 1.2:
                continue
            comps.append((x0, comp))
        comps.sort()
        if args.trim_ends:
            if len(comps) < 4:
                sys.exit('trim-ends: too few glyph components found, aborting')
            drop.update(comps[0][1])
            drop.update(comps[-1][1])
        else:
            for _, comp in comps:
                drop.update(comp)
            # long horizontal underline rules in the band
            for i in band_idx:
                s = segs[i]
                if abs(s[3] - s[1]) < 12 and abs(s[2] - s[0]) > CW * 0.20:
                    drop.add(i)

    if len(drop) > len(segs) * args.max_wipe:
        sys.exit(f'wipe too broad ({len(drop)} of {len(segs)} strokes), aborting')

    # --- ink: majority ink of what was removed, else override, else warm brown
    ink = (92, 74, 52)
    if args.ink:
        ink = tuple(int(v) for v in args.ink.split(','))
    elif drop:
        ink = collections.Counter(segs[i][4] for i in drop).most_common(1)[0][0]

    new_lines = []
    tbox = None
    if not args.trim_ends:
        if not args.text:
            sys.exit('need title text')
        text = args.text.upper()
        h = min(150.0, band_h * 0.52)
        gap = h * 0.16
        cw = h * 0.66
        while group_width(text, cw, gap) > CW * 0.90:
            h *= 0.86
            gap = h * 0.16
            cw = h * 0.66
        ybase = CY0 - scale * 0.035
        ox = (CX0 + CX1) / 2 - group_width(text, cw, gap) / 2
        tsegs = word_segs(text, ox, ybase, cw, h, gap)
        xs = [a for s in tsegs for a in (s[0], s[2])]
        ys = [a for s in tsegs for a in (s[1], s[3])]
        tbox = (min(xs) - 25, max(xs) + 25, min(ys) - 25, max(ys) + 25)
        # knock out anything still under the new title's box
        for i, s in segs.items():
            if i in drop:
                continue
            if (tbox[0] < (s[0] + s[2]) / 2 < tbox[1]
                    and tbox[2] < (s[1] + s[3]) / 2 < tbox[3]):
                drop.add(i)
        for (a, b, c, d) in tsegs:
            new_lines.append('L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d'
                             % (a, b, c, d, *ink))
        if args.rules:
            for ry in (tbox[2] - 14, tbox[3] + 14):
                new_lines.append('L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d'
                                 % (min(xs) - 30, ry, max(xs) + 30, ry, *ink))

    out = [l for i, l in enumerate(raw) if i not in drop and l.strip()]
    out += new_lines
    after = [parse(l) for l in out if l.startswith('L')]
    health_after = title_health(after, CY0)
    if (health_after < health_before and not args.trim_ends
            and not args.allow_health_drop):
        sys.exit(f'title health would drop {health_before} -> {health_after}, aborting')

    open(p2, 'w', newline='', encoding='utf-8').write(CRLF.join(out) + CRLF)
    print(f'{args.zone}: removed {len(drop)} strokes, added {len(new_lines)}, '
          f'health {health_before} -> {health_after}')


if __name__ == '__main__':
    main()
