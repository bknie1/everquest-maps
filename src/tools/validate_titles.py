"""validate_titles.py — every zone must still have a title.

Written after a knockout pass silently deleted the lettering from 64 zones. The
pack validated clean the whole time, because nothing checked that a title existed.
A missing title is invisible to line-count and format checks and obvious to anyone
looking at the map, which is exactly the kind of gap a validator is for.

    python src/tools/validate_titles.py
"""
import os, sys, collections, math

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def has_title(zone):
    p2 = f'{MAPS}/{zone}_2.txt'
    if not os.path.exists(p2): return None
    D = []
    for l in open(p2, encoding='utf-8', errors='replace'):
        if l.startswith('L'):
            try: D.append(parse(l))
            except Exception: pass
    if len(D) < 40: return None
    fx = [a for s in D for a in (s[0], s[2])]
    fy = [a for s in D for a in (s[1], s[3])]
    FX0, FX1, FY0, FY1 = min(fx), max(fx), min(fy), max(fy)
    W, H = FX1 - FX0, FY1 - FY0
    band = [s for s in D if (s[1] + s[3]) / 2 < FY0 + H * 0.22]
    tot = collections.Counter(s[4] for s in D)
    by = collections.defaultdict(list)
    for s in band: by[s[4]].append(s)
    for ink, S in by.items():
        # Keep only short strokes. Frame rules share the title's ink and are long,
        # so including them skews any length statistic and hides a real title.
        S = [s for s in S if math.hypot(s[2] - s[0], s[3] - s[1]) < W * 0.06]
        if len(S) < 18: continue
        xs = [a for s in S for a in (s[0], s[2])]
        ys = [a for s in S for a in (s[1], s[3])]
        span = (max(xs) - min(xs)) / W
        cen = abs(((min(xs) + max(xs)) / 2) - (FX0 + FX1) / 2) / W
        aspect = (max(xs) - min(xs)) / max(max(ys) - min(ys), 1e-6)
        # lettering: a wide, shallow row of short strokes across the centre
        if span > 0.25 and cen < 0.25 and aspect > 2.5:
            return (ink, len(S))
    return False


if __name__ == '__main__':
    zones = sorted(b[:-4] for b in os.listdir(MAPS)
                   if b.endswith('.txt') and '_' not in b)
    missing = []; checked = 0
    for z in zones:
        r = has_title(z)
        if r is None: continue
        checked += 1
        if not r: missing.append(z)
    print(f"checked {checked} zones")
    if missing:
        print(f"MISSING TITLES: {len(missing)}")
        for z in missing: print(f"   {z}")
        sys.exit(1)
    print("every zone has a title")
