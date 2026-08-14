"""titles.py -- find a zone's title reliably, so it can be replaced without collateral.

The problem this solves: a title drawn in the same ink as margin texture cannot be
picked out by colour, and every attempt to do so removed letters or left ghosts.

The discriminator is CONNECTIVITY. Letters are small connected components -- strokes
sharing endpoints. Hatching is isolated parallel strokes. Frame rules are connected
but far too long. So:

    1. take everything above the grid
    2. group strokes into connected components by shared endpoints
    3. keep components that are letter-sized (2-30 strokes, under 16% of grid width)
    4. keep those sharing a baseline

Verification: the letter count should match the zone name's letter count. If it
doesn't, do not touch the zone.
"""
import collections, math


def parse(line):
    f = line[2:].split(',')
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def find_title(deco, grid):
    """deco: list of parsed segments. grid: (x0,x1,y0,y1).
    Returns (indices, x0, x1, y0, y1, n_letters) or None."""
    GX0, GX1, GY0, GY1 = grid
    GW = GX1 - GX0
    band = [i for i, s in enumerate(deco) if (s[1] + s[3]) / 2 < GY0]
    key = lambda q: (round(q[0], 1), round(q[1], 1))
    adj = collections.defaultdict(list)
    for i in band:
        s = deco[i]
        adj[key((s[0], s[1]))].append(i)
        adj[key((s[2], s[3]))].append(i)
    seen = set(); glyphs = []
    for i in band:
        if i in seen: continue
        stack = [i]; comp = []
        while stack:
            j = stack.pop()
            if j in seen: continue
            seen.add(j); comp.append(j)
            for k in (adj[key((deco[j][0], deco[j][1]))] +
                      adj[key((deco[j][2], deco[j][3]))]):
                if k not in seen: stack.append(k)
        if not (2 <= len(comp) <= 30): continue
        xs = [a for j in comp for a in (deco[j][0], deco[j][2])]
        ys = [a for j in comp for a in (deco[j][1], deco[j][3])]
        w = max(xs) - min(xs); h = max(ys) - min(ys)
        if w > GW*0.16 or h > GW*0.16 or max(w, h) < GW*0.008: continue
        glyphs.append((comp, (min(xs)+max(xs))/2, (min(ys)+max(ys))/2, w, h))
    if len(glyphs) < 3: return None
    # letters share a baseline AND a height. Filtering on height alone removes
    # frame fragments and margin doodles that happen to sit near the baseline.
    hs = sorted(g[4] for g in glyphs)
    hmed = hs[len(hs)//2]
    glyphs = [g for g in glyphs if 0.55*hmed <= g[4] <= 1.8*hmed]
    if len(glyphs) < 3: return None
    ys = sorted(g[2] for g in glyphs)
    med = ys[len(ys)//2]
    row = [g for g in glyphs if abs(g[2] - med) < hmed * 0.8]
    if len(row) < 3: return None
    # letters are evenly pitched: drop outliers far from their neighbours
    row.sort(key=lambda g: g[1])
    if len(row) > 3:
        gaps = [row[i+1][1]-row[i][1] for i in range(len(row)-1)]
        gm = sorted(gaps)[len(gaps)//2]
        kept = [row[0]]
        for i in range(1, len(row)):
            if row[i][1] - kept[-1][1] <= gm*3.0: kept.append(row[i])
        row = kept
    if len(row) < 3: return None
    idx = [j for g in row for j in g[0]]
    xs = [a for j in idx for a in (deco[j][0], deco[j][2])]
    ys2 = [a for j in idx for a in (deco[j][1], deco[j][3])]
    return (idx, min(xs), max(xs), min(ys2), max(ys2), len(row))


def expected_letters(name):
    """Letters the title routine will draw for a zone name."""
    return sum(1 for ch in name if ch.isalnum())


def verify(deco, grid, name):
    """Template match: we know the text, so check the found strokes fall into as many
    columns as the name has letters. Returns (indices, box, ok) or None.

    Use this as a GATE. If ok is False, do not modify the zone's title -- every time
    a title has been damaged it was because something was removed without this check.
    """
    r = find_title(deco, grid)
    if not r: return None
    idx, X0, X1, Y0, Y1, n = r
    letters = sum(1 for c in name.upper() if c != ' ')
    if letters == 0 or X1 <= X0: return None
    cols = set()
    for j in idx:
        cx = (deco[j][0] + deco[j][2]) / 2
        cols.add(int((cx - X0) / (X1 - X0) * letters))
    ok = abs(len(cols) - letters) <= 2
    return (idx, (X0, X1, Y0, Y1), ok)


def find_ghosts(deco, grid, new_height, scale):
    """Old titles that bleed BELOW the grid top and sit over the map.

    A wipe of the band above the grid cannot reach these -- that is why Halas kept
    its ghost through several passes. They are letter-shaped connected components
    much taller than the current title, sharing a baseline.

    Returns the stroke indices to remove.
    """
    key = lambda q: (round(q[0], 1), round(q[1], 1))
    adj = collections.defaultdict(list)
    for i, s in enumerate(deco):
        adj[key((s[0], s[1]))].append(i)
        adj[key((s[2], s[3]))].append(i)
    seen = set(); big = []
    for i in range(len(deco)):
        if i in seen: continue
        stack = [i]; comp = []
        while stack:
            j = stack.pop()
            if j in seen: continue
            seen.add(j); comp.append(j)
            for k in (adj[key((deco[j][0], deco[j][1]))] +
                      adj[key((deco[j][2], deco[j][3]))]):
                if k not in seen: stack.append(k)
        if not (2 <= len(comp) <= 40): continue
        xs = [a for j in comp for a in (deco[j][0], deco[j][2])]
        ys = [a for j in comp for a in (deco[j][1], deco[j][3])]
        w = max(xs) - min(xs); h = max(ys) - min(ys)
        if h < new_height*1.4: continue
        if h > scale*0.30 or w > scale*0.30: continue
        if w <= 0 or not (0.25 < w/h < 2.2): continue
        big.append((comp, (min(xs)+max(xs))/2, (min(ys)+max(ys))/2, w, h))
    if len(big) < 3: return set()
    ys = sorted(b[2] for b in big)
    med = ys[len(ys)//2]
    tall = max(b[4] for b in big)
    row = [b for b in big if abs(b[2] - med) < tall*0.9]
    if len(row) < 3: return set()
    return set(j for b in row for j in b[0])
