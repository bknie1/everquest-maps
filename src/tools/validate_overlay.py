"""validate_overlay.py — composite the layers and check they agree.

The layers are authored separately but the player sees them stacked, so mistakes
only visible in combination slip through: a tree scattered into a lake, a figure
standing in a river. Nothing in a single file is wrong, which is exactly why it
survives a per-file check.

Run after any decoration pass.

    python validate_overlay.py            report only
    python validate_overlay.py --fix      remove offending clusters
"""
import os, sys, math, collections

MAPS = os.environ.get('EQ_MAPS', 'Emoda Legends Maps')

# decoration that must never stand in water
FLORA = {(46,72,48),(50,76,50),(54,80,46),(58,66,46),(70,96,58),(84,82,76),
         (56,48,40),(62,52,84),(66,54,88),(70,58,92),(52,42,58),(112,116,112),
         (34,58,38),(66,90,56)}
FAUNA = {(108,104,96),(64,58,66),(86,70,52),(72,58,96),(86,96,124),(68,92,62),
         (96,88,60),(104,76,52),(110,92,70),(78,84,110),(116,88,56),(118,94,62),
         (92,84,116),(74,92,62),(98,88,60),(92,80,68),(74,100,62),(92,96,86),
         (108,100,94)}
PLACED = FLORA | FAUNA


def is_water(ink):
    r, g, b = ink
    return b > 90 and b > r + 30 and b > g + 20


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def load(path):
    out = []
    if not os.path.exists(path): return out
    for l in open(path, encoding='utf-8', errors='replace'):
        if l.startswith('L'):
            try: out.append(parse(l))
            except Exception: pass
    return out


def water_mask(segs, cell):
    """Grid cells inside water, by even-odd across the water lines per row.
    Coincident crossings are collapsed first — borders are often drawn twice and
    duplicates cancel parity."""
    if not segs: return None
    xs = [a for s in segs for a in (s[0], s[2])]
    ys = [a for s in segs for a in (s[1], s[3])]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    W = int((x1-x0)/cell)+2; H = int((y1-y0)/cell)+2
    if W*H > 4_000_000: return None
    wet = bytearray(W*H)
    for gy in range(H):
        py = y0 + gy*cell
        hits = sorted(sx1 + (py-sy1)*(sx2-sx1)/(sy2-sy1)
                      for sx1, sy1, sx2, sy2, _ in segs if (sy1 > py) != (sy2 > py))
        if len(hits) < 2: continue
        ded = [hits[0]]
        for h in hits[1:]:
            if h - ded[-1] > cell*0.75: ded.append(h)
        for i in range(0, len(ded)-1, 2):
            ga = int((ded[i]-x0)/cell); gb = int((ded[i+1]-x0)/cell)
            for gx in range(max(0, ga), min(W-1, gb)+1):
                wet[gy*W+gx] = 1
    return wet, x0, y0, W, H


def clusters(items, gap=44.0):
    cells = collections.defaultdict(list)
    for i, s in enumerate(items):
        cells[(int(((s[0]+s[2])/2)//gap), int(((s[1]+s[3])/2)//gap))].append(i)
    seen = set(); out = []
    for k in list(cells):
        if k in seen: continue
        st = [k]; comp = []
        while st:
            d = st.pop()
            if d in seen or d not in cells: continue
            seen.add(d); comp += cells[d]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nn = (d[0]+dx, d[1]+dy)
                    if nn in cells and nn not in seen: st.append(nn)
        out.append(comp)
    return out


def check(zone, fix=False):
    base = load(f'{MAPS}/{zone}.txt')
    deco_path = f'{MAPS}/{zone}_2.txt'
    deco = load(deco_path)
    water = [s for s in base + deco if is_water(s[4])]
    placed = [s for s in deco if s[4] in PLACED]
    if not water or not placed: return 0, 0
    xs = [a for s in base for a in (s[0], s[2])]
    ys = [a for s in base for a in (s[1], s[3])]
    span = max(max(xs)-min(xs), max(ys)-min(ys))
    cell = max(4.0, span*0.0025)
    m = water_mask(water, cell)
    if not m: return 0, 0
    wet, x0, y0, W, H = m

    def in_water(x, y):
        gx = int((x-x0)/cell); gy = int((y-y0)/cell)
        return 0 <= gx < W and 0 <= gy < H and wet[gy*W+gx]

    bad = set(); n_clusters = 0
    for comp in clusters(placed):
        pts = [((placed[i][0]+placed[i][2])/2, (placed[i][1]+placed[i][3])/2) for i in comp]
        hits = sum(1 for x, y in pts if in_water(x, y))
        if hits*2 > len(pts):                       # mostly in water: it is misplaced
            n_clusters += 1
            bad.update(comp)
    if not bad: return 0, 0
    if fix:
        drop = {id(placed[i]) for i in bad}
        raw = [l.rstrip('\r\n') for l in
               open(deco_path, 'rb').read().decode('utf-8', 'replace')
               .replace('\r\n', '\n').split('\n') if l.strip()]
        head = [l for l in raw if not l.startswith('L')]
        keep = []
        pi = 0
        for l in raw:
            if not l.startswith('L'): continue
            s = parse(l)
            if s[4] in PLACED:
                if pi in bad: pi += 1; continue
                pi += 1
            keep.append(l)
        open(deco_path, 'w', newline='').write('\r\n'.join(head+keep)+'\r\n')
    return n_clusters, len(bad)


if __name__ == '__main__':
    fix = '--fix' in sys.argv
    zones = sorted(b[:-4] for b in os.listdir(MAPS)
                   if b.endswith('.txt') and '_' not in b)
    total_c = total_l = 0
    for z in zones:
        c, n = check(z, fix)
        if c:
            print(f"  {z:14} {c:3} decoration clusters standing in water ({n} lines)")
            total_c += c; total_l += n
    print(f"\n{total_c} clusters, {total_l} lines" +
          (" removed" if fix else " found — rerun with --fix to remove"))
