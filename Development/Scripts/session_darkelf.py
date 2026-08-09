"""darkelf.py — shared Teir'Dal visual utilities.

One place for the Dark Elf look so Neriak, Najena, Nektulos and any future
cavern/Teir'Dal zone draw from the same well.

    PALETTE        the agreed inks
    triquetra()    the glowing knot over Neriak's gate
    teirdal_sigil() the twin-eared crest (as used on the Nektulos gate block)
    candelabra()   many-armed candle stand
    arched_gate()  gate mouth with sigil above and candelabra flanking
    cavern_edge()  ragged rock ceiling/floor band
    web_corner()   spider web for a frame corner
    torch()        wall sconce
All return [(x1,y1,x2,y2,ink)] in a local, y-DOWN space.
"""
import math, random

PALETTE = {
    'obsidian': (44, 34, 58),      # walls, main structure
    'basalt':   (92, 70, 108),     # secondary structure
    'stone':    (120, 112, 134),   # floors, steps
    'arcane':   (58, 84, 150),     # water, glow, magic
    'glow':     (96, 108, 200),    # the brighter magical accent
    'lamp':     (168, 132, 72),    # lamplight, gold fittings
    'ink':      (60, 48, 76),      # frame / linework
    'web':      (128, 122, 140),   # spider silk
    'tile':     (140, 40, 40),     # the Lodge's red roof
    'tile_lit': (168, 84, 48),     # its lit tile courses
}

def _P(out, pts, ink, close=False):
    for i in range(len(pts) - 1):
        out.append((pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], ink))
    if close and len(pts) > 2:
        out.append((pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], ink))

def _arc(out, cx, cy, r, a0, a1, ink, n=24, squash=1.0):
    prev = None
    for k in range(n + 1):
        a = a0 + (a1 - a0) * k / n
        p = (cx + math.cos(a) * r, cy + math.sin(a) * r * squash)
        if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
        prev = p


def triquetra(cx, cy, r, ink=None):
    """The trinity knot over Neriak's gate: three pointed lobes plus a ring."""
    ink = ink or PALETTE['glow']
    out = []
    for k in range(3):
        a = -math.pi/2 + k * 2*math.pi/3
        tipx, tipy = cx + math.cos(a)*r, cy + math.sin(a)*r
        # two bowed sides from the centre out to the tip = a pointed lobe
        for side in (-1, 1):
            prev = None
            for i in range(15):
                t = i/14
                # straight run from centre to tip, bowed sideways
                bx = cx + (tipx-cx)*t
                by = cy + (tipy-cy)*t
                bow = math.sin(math.pi*t) * r*0.42 * side
                px, py = bx - math.sin(a)*bow, by + math.cos(a)*bow
                if prev: out.append((prev[0], prev[1], px, py, ink))
                prev = (px, py)
    _arc(out, cx, cy, r*1.16, 0, 2*math.pi, ink, n=34)          # containing ring
    for k in range(3):                                            # nodes on the ring
        a = -math.pi/2 + k * 2*math.pi/3 + math.pi/3
        nx, ny = cx + math.cos(a)*r*1.16, cy + math.sin(a)*r*1.16
        _arc(out, nx, ny, r*0.10, 0, 2*math.pi, ink, n=10)
    return out


def teirdal_sigil(cx, cy, w, h, ink=None, shade=True):
    """Twin-eared crest tapering to a point; optionally hatch-shaded solid."""
    ink = ink or PALETTE['obsidian']
    out = []
    P = [(cx - 0.44*w, cy - 0.50*h), (cx, cy - 0.04*h), (cx + 0.44*w, cy - 0.50*h),
         (cx + 0.30*w, cy + 0.02*h), (cx, cy + 0.50*h), (cx - 0.30*w, cy + 0.02*h)]
    _P(out, P, ink, close=True)
    if shade:
        ys = [p[1] for p in P]
        y = min(ys) + 1.6
        while y < max(ys) - 1.0:
            xs = []
            for i in range(len(P)):
                x1, y1 = P[i]; x2, y2 = P[(i+1) % len(P)]
                if (y1 > y) != (y2 > y):
                    xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                if xs[i+1] - xs[i] > 1.2: out.append((xs[i], y, xs[i+1], y, ink))
            y += 2.0
    return out


def candelabra(bx, by, h, arms=5, ink=None, flame=None):
    """Many-armed candle stand: stem, curved arms, candles, flames."""
    ink = ink or PALETTE['obsidian']
    flame = flame or PALETTE['lamp']
    out = []
    out.append((bx, by, bx, by - h, ink))                       # stem
    _P(out, [(bx - h*0.13, by), (bx + h*0.13, by), (bx + h*0.09, by - h*0.07),
             (bx - h*0.09, by - h*0.07)], ink, close=True)       # foot
    for i in range(arms):
        t = (i - (arms - 1) / 2) / max(1, (arms - 1) / 2)
        ax = bx + t * h * 0.34
        ay = by - h * (0.74 - abs(t) * 0.16)
        _arc(out, bx, by - h * 0.70, abs(ax - bx) + 1e-6,
             math.pi if t < 0 else 0, math.pi * 1.5 if t < 0 else math.pi * -0.5,
             ink, n=8, squash=0.5)
        out.append((ax, ay, ax, ay - h * 0.16, ink))             # candle
        out.append((ax - h*0.03, ay - h*0.16, ax, ay - h*0.24, flame))
        out.append((ax, ay - h*0.24, ax + h*0.03, ay - h*0.16, flame))
    return out


def arched_gate(cx, cy, w, h, ink=None):
    """Neriak's gate: stone arch in a wall, sigil above, candelabra flanking."""
    ink = ink or PALETTE['obsidian']
    out = []
    # coursed stone wall
    out.append((cx - w*0.5, cy, cx + w*0.5, cy, ink))
    out.append((cx - w*0.5, cy - h, cx + w*0.5, cy - h, ink))
    out.append((cx - w*0.5, cy, cx - w*0.5, cy - h, ink))
    out.append((cx + w*0.5, cy, cx + w*0.5, cy - h, ink))
    rows = 5
    for r in range(1, rows):
        y = cy - h * r / rows
        out.append((cx - w*0.5, y, cx + w*0.5, y, PALETTE['basalt']))
        off = (r % 2) * 0.5
        for k in range(6):
            x = cx - w*0.5 + w * (k + off) / 6.0
            if cx - w*0.5 < x < cx + w*0.5:
                out.append((x, y, x, y - h/rows, PALETTE['basalt']))
    # the arch, cut dark
    aw, ah = w*0.17, h*0.52
    _arc(out, cx, cy - ah*0.62, aw, math.pi, 2*math.pi, ink, n=18)
    out.append((cx - aw, cy - ah*0.62, cx - aw, cy, ink))
    out.append((cx + aw, cy - ah*0.62, cx + aw, cy, ink))
    y = cy - 2.0
    while y > cy - ah*0.62 - aw*0.94:
        dy = (cy - ah*0.62) - y
        half = aw if dy <= 0 else (aw*aw - dy*dy) ** 0.5 if dy < aw else 0
        if half > 1: out.append((cx - half, y, cx + half, y, ink))
        y -= 2.4
    # the triquetra, glowing above the arch
    out += triquetra(cx, cy - h*0.66, w*0.085)
    # candelabra either side of the mouth
    out += candelabra(cx - aw*1.85, cy, h*0.30)
    out += candelabra(cx + aw*1.85, cy, h*0.30)
    return out


def cavern_edge(x0, x1, y, amp, ink=None, teeth=14, down=True):
    """Ragged rock band — a cavern ceiling or floor edge."""
    ink = ink or PALETTE['obsidian']
    out = []; rnd = random.Random(int(x0 + y))
    pts = [(x0, y)]
    for k in range(teeth):
        t = (k + 0.5) / teeth
        pts.append((x0 + (x1 - x0) * t,
                    y + (amp * rnd.uniform(0.4, 1.0)) * (1 if down else -1) * (1 if k % 2 else 0.35)))
    pts.append((x1, y))
    _P(out, pts, ink)
    return out


def web_corner(cx, cy, r, ink=None, quadrant=0):
    """Quarter spider web for a frame corner."""
    ink = ink or PALETTE['web']
    out = []
    a0 = quadrant * math.pi / 2
    n = 6
    spokes = [a0 + (math.pi/2) * k / (n - 1) for k in range(n)]
    for a in spokes:
        out.append((cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r, ink))
    for f in (0.30, 0.52, 0.74, 0.96):
        prev = None
        for a in spokes:
            p = (cx + math.cos(a) * r * f, cy + math.sin(a) * r * f)
            if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
            prev = p
    return out


def torch(bx, by, h, ink=None):
    """Wall sconce with flame."""
    ink = ink or PALETTE['obsidian']
    out = [(bx, by, bx, by - h, ink),
           (bx - h*0.18, by, bx + h*0.18, by, ink)]
    out += [(bx - h*0.16, by - h, bx, by - h*1.42, PALETTE['lamp']),
            (bx, by - h*1.42, bx + h*0.16, by - h, PALETTE['lamp']),
            (bx - h*0.08, by - h*1.02, bx, by - h*1.22, PALETTE['lamp']),
            (bx, by - h*1.22, bx + h*0.08, by - h*1.02, PALETTE['lamp'])]
    return out


def innoruuk_star(cx, cy, r, ink=None, rim=None):
    """Eight-pointed star on a disc — the medallion over the Commons gate."""
    ink = ink or PALETTE['lamp']; rim = rim or PALETTE['obsidian']
    out = []
    _arc(out, cx, cy, r, 0, 2*math.pi, rim, n=30)              # disc
    _arc(out, cx, cy, r*0.92, 0, 2*math.pi, ink, n=30)         # gold rim
    pts = []
    for k in range(16):
        a = -math.pi/2 + k*math.pi/8
        rr = r*0.66 if k % 2 == 0 else r*0.30
        pts.append((cx + math.cos(a)*rr, cy + math.sin(a)*rr))
    _P(out, pts, ink, close=True)
    _arc(out, cx, cy, r*0.15, 0, 2*math.pi, rim, n=14)         # dark centre
    for k in range(8):                                          # filled centre
        out.append((cx - r*0.13 + k*r*0.033, cy - r*0.12,
                    cx - r*0.13 + k*r*0.033, cy + r*0.12, rim))
    return out


def rune_panel(cx, cy, w, h, ink=None, arc_ink=None):
    """A glowing wall rune inside bracketing arcs, with a curl beneath."""
    ink = ink or PALETTE['glow']; arc_ink = arc_ink or PALETTE['basalt']
    out = []
    for side in (-1, 1):                                        # bracketing arcs
        for f in (1.0, 0.86, 0.72):
            _arc(out, cx + side*w*0.30, cy, w*0.30*f,
                 -math.pi/2, math.pi/2 if side > 0 else -math.pi*1.5, arc_ink, n=14)
    # angular rune: a bolt-like glyph
    _P(out, [(cx - w*0.16, cy - h*0.34), (cx + w*0.04, cy - h*0.16),
             (cx - w*0.06, cy - h*0.02), (cx + w*0.16, cy + h*0.14),
             (cx - w*0.02, cy + h*0.10), (cx - w*0.14, cy + h*0.34)], ink)
    _P(out, [(cx + w*0.12, cy - h*0.30), (cx - w*0.02, cy - h*0.08),
             (cx + w*0.10, cy + h*0.06)], ink)
    # red curl below
    prev = None
    for k in range(16):
        t = k/15.0
        a = t*2.6*math.pi
        rr = w*0.10*(1-t*0.75)
        p = (cx + math.cos(a)*rr, cy + h*0.52 + math.sin(a)*rr + t*h*0.10)
        if prev: out.append((prev[0], prev[1], p[0], p[1], (170, 60, 70)))
        prev = p
    return out


def barred_gate(cx, cy, w, h, ink=None, bar=None):
    """Portcullis: framed opening with vertical bars."""
    ink = ink or PALETTE['obsidian']; bar = bar or PALETTE['lamp']
    out = []
    _P(out, [(cx-w*0.5, cy), (cx-w*0.5, cy-h), (cx+w*0.5, cy-h), (cx+w*0.5, cy)], ink)
    out.append((cx-w*0.56, cy-h, cx+w*0.56, cy-h, ink))          # lintel
    out.append((cx-w*0.56, cy-h*1.10, cx+w*0.56, cy-h*1.10, ink))
    out.append((cx-w*0.56, cy-h, cx-w*0.56, cy-h*1.10, ink))
    out.append((cx+w*0.56, cy-h, cx+w*0.56, cy-h*1.10, ink))
    out.append((cx-w*0.5, cy, cx+w*0.5, cy, ink))                # sill
    for k in range(1, 6):
        x = cx - w*0.5 + w*k/6.0
        out.append((x, cy, x, cy-h, bar))
    return out


def rune_wall(cx, cy, w, h, ink=None):
    """Neriak Commons: coursed wall, twin glowing runes, star medallion, torches,
    barred gate below."""
    ink = ink or PALETTE['obsidian']
    out = []
    _P(out, [(cx-w*0.5, cy), (cx-w*0.5, cy-h), (cx+w*0.5, cy-h), (cx+w*0.5, cy)], ink, close=True)
    rows = 6
    for r in range(1, rows):                                     # brick courses
        y = cy - h*r/rows
        out.append((cx-w*0.5, y, cx+w*0.5, y, PALETTE['basalt']))
        off = (r % 2)*0.5
        for k in range(7):
            x = cx - w*0.5 + w*(k+off)/7.0
            if cx-w*0.5 < x < cx+w*0.5:
                out.append((x, y, x, y-h/rows, PALETTE['basalt']))
    out += rune_panel(cx - w*0.31, cy - h*0.58, w*0.30, h*0.42)
    out += rune_panel(cx + w*0.31, cy - h*0.58, w*0.30, h*0.42)
    out += innoruuk_star(cx, cy - h*0.76, min(w, h)*0.12)
    out += barred_gate(cx, cy, w*0.22, h*0.34)
    out += torch(cx - w*0.17, cy - h*0.30, h*0.12)
    out += torch(cx + w*0.17, cy - h*0.30, h*0.12)
    return out


def waterfall(cx, cy, w, h, ink=None):
    """Sheet of falling water inside a cut opening."""
    ink = ink or PALETTE['arcane']
    out = []
    _P(out, [(cx-w*0.5, cy-h), (cx+w*0.5, cy-h), (cx+w*0.5, cy), (cx-w*0.5, cy)], PALETTE['obsidian'])
    n = max(4, int(w/7))
    for k in range(n):
        x = cx - w*0.5 + w*(k+0.5)/n
        prev = None
        for i in range(9):
            t = i/8.0
            p = (x + math.sin(t*3.4 + k)*w*0.02, cy - h + h*t)
            if prev: out.append((prev[0], prev[1], p[0], p[1], ink))
            prev = p
    for k in range(3):                                           # spray at the base
        out.append((cx-w*0.5+w*(k+0.5)/3-w*0.06, cy+h*0.04,
                    cx-w*0.5+w*(k+0.5)/3+w*0.06, cy+h*0.04, ink))
    return out


def monolith(cx, cy, w, h, ink=None):
    """The leaning spire of rock standing in the Commons pool."""
    ink = ink or PALETTE['obsidian']
    out = []
    _P(out, [(cx-w*0.30, cy), (cx-w*0.12, cy-h), (cx+w*0.10, cy-h*0.96),
             (cx+w*0.34, cy)], ink, close=True)
    out.append((cx-w*0.06, cy-h*0.90, cx+w*0.02, cy-h*0.20, PALETTE['basalt']))
    out.append((cx-w*0.16, cy-h*0.60, cx-w*0.08, cy-h*0.14, PALETTE['basalt']))
    _P(out, [(cx-w*0.52, cy), (cx-w*0.34, cy-h*0.22), (cx+w*0.10, cy-h*0.26),
             (cx+w*0.56, cy)], ink)                              # rubble base
    return out


def commons_scene(cx, cy, w, h, ink=None):
    """Commons cavern: twin falls into the pool, monolith to the right, walkway left."""
    ink = ink or PALETTE['obsidian']
    out = []
    out += cavern_edge(cx-w*0.5, cx+w*0.5, cy-h, h*0.10, ink, teeth=10, down=True)
    out += waterfall(cx - w*0.24, cy - h*0.30, w*0.20, h*0.52)
    out += waterfall(cx - w*0.24, cy - h*0.02, w*0.20, h*0.20)
    out += monolith(cx + w*0.28, cy - h*0.02, w*0.30, h*0.62)
    _P(out, [(cx-w*0.5, cy-h*0.30), (cx-w*0.40, cy-h*0.34),
             (cx-w*0.34, cy-h*0.16), (cx-w*0.5, cy-h*0.12)], ink, close=True)   # walkway
    y = cy
    while y < cy + h*0.14:                                        # the pool
        out.append((cx-w*0.5, y, cx+w*0.5, y, PALETTE['arcane']))
        y += h*0.045
    out += torch(cx + w*0.02, cy - h*0.52, h*0.10)
    return out


def rune_graffiti(cx, cy, w, h, seed=0):
    """Glowing Teir'Dal wall graffiti — a sweeping blue hook, a green eye held
    inside it, and red script scrawled beneath. Layered, three inks."""
    BLUE  = (70, 96, 210)
    GREEN = (60, 170, 90)
    RED   = (196, 62, 48)
    rnd = random.Random(seed)
    out = []

    # --- blue: a broad open hook curling round the eye ---
    for off in (0.0, 0.045):
        prev = None
        for k in range(41):
            t = k/40.0
            a = math.pi*1.18 - t*math.pi*1.72          # sweeps round, left open
            rx, ry = w*(0.46-off), h*(0.34-off)
            p = (cx + math.cos(a)*rx, cy - h*0.10 + math.sin(a)*ry)
            if prev: out.append((prev[0], prev[1], p[0], p[1], BLUE))
            prev = p
    for k in range(7):                                  # spark ticks along the top
        t = 0.18 + k*0.11
        a = math.pi*1.18 - t*math.pi*1.72
        px = cx + math.cos(a)*w*0.46; py = cy - h*0.10 + math.sin(a)*h*0.34
        out.append((px, py, px + rnd.uniform(-w*0.03, w*0.03), py - h*0.07, BLUE))

    # --- green: the eye, an almond with a bright core ---
    for f in (1.0, 0.62):
        prev = None
        for k in range(29):
            t = k/28.0
            a = 2*math.pi*t
            p = (cx + math.cos(a)*w*0.21*f,
                 cy - h*0.06 + math.sin(a)*h*0.075*f*(1.0 if math.sin(a) > 0 else 0.8))
            if prev: out.append((prev[0], prev[1], p[0], p[1], GREEN))
            prev = p
    out.append((cx - w*0.16, cy - h*0.06, cx + w*0.16, cy - h*0.06, GREEN))

    # --- red: script below — a spiral glyph then angular characters ---
    prev = None
    for k in range(30):                                 # spiral 'G'
        t = k/29.0
        a = -math.pi*0.4 + t*2.45*math.pi
        rr = w*0.13*(1 - t*0.62)
        p = (cx - w*0.20 + math.cos(a)*rr, cy + h*0.30 + math.sin(a)*rr)
        if prev: out.append((prev[0], prev[1], p[0], p[1], RED))
        prev = p
    out.append((cx - w*0.33, cy + h*0.16, cx - w*0.33, cy + h*0.42, RED))
    for i in range(2):                                  # two angular runes
        bx = cx + w*0.06 + i*w*0.17
        _P(out, [(bx, cy + h*0.42), (bx + w*0.05, cy + h*0.20),
                 (bx + w*0.11, cy + h*0.40), (bx + w*0.15, cy + h*0.18)], RED)
        out.append((bx + w*0.02, cy + h*0.31, bx + w*0.13, cy + h*0.29, RED))
    return out


def water_fill(segments, ink=None, row=15.0, dash=13.0, min_area=180.0):
    """Shade water with short strokes.

    All loops are scanline-filled TOGETHER under the even-odd rule, so a moat
    ringing an island fills the ring and leaves the island dry — filling each
    loop independently would flood the island too.
    """
    import collections
    ink = ink or PALETTE['arcane']
    key = lambda p: (round(p[0],1), round(p[1],1))
    adj = collections.defaultdict(list)
    for i,s in enumerate(segments):
        adj[key((s[0],s[1]))].append(i); adj[key((s[2],s[3]))].append(i)
    seen=set(); comps=[]
    for i in range(len(segments)):
        if i in seen: continue
        st=[i]; comp=[]
        while st:
            j=st.pop()
            if j in seen: continue
            seen.add(j); comp.append(j)
            for k in adj[key((segments[j][0],segments[j][1]))]+adj[key((segments[j][2],segments[j][3]))]:
                if k not in seen: st.append(k)
        comps.append(comp)

    edges=[]                       # every loop edge that takes part in the fill
    for comp in comps:
        xs=[a for j in comp for a in (segments[j][0],segments[j][2])]
        ys=[a for j in comp for a in (segments[j][1],segments[j][3])]
        if (max(xs)-min(xs))*(max(ys)-min(ys)) < min_area: continue
        # PRUNE DANGLING TAILS: a loop with a spur breaks scanline parity, so
        # repeatedly shave off any edge with a loose end until only loops remain.
        alive={j for j in comp}
        while True:
            deg=collections.Counter()
            for j in alive:
                deg[key((segments[j][0],segments[j][1]))]+=1
                deg[key((segments[j][2],segments[j][3]))]+=1
            spurs={j for j in alive
                   if deg[key((segments[j][0],segments[j][1]))]==1
                   or deg[key((segments[j][2],segments[j][3]))]==1}
            if not spurs: break
            alive -= spurs
            if not alive: break
        if not alive: continue
        # anything still loose after pruning: stitch nearest pairs shut
        deg=collections.Counter()
        for j in alive:
            deg[key((segments[j][0],segments[j][1]))]+=1
            deg[key((segments[j][2],segments[j][3]))]+=1
        ends=[p for p,v in deg.items() if v==1]
        for j in alive: edges.append(segments[j])
        while len(ends) >= 2:
            ax,ay = ends.pop(0)
            best=None
            for k,(bx,by) in enumerate(ends):
                d=(ax-bx)**2+(ay-by)**2
                if best is None or d<best[0]: best=(d,k)
            bx,by = ends.pop(best[1])
            edges.append((ax,ay,bx,by))

    if not edges: return []

    xs=[a for e in edges for a in (e[0],e[2])]
    ys=[a for e in edges for a in (e[1],e[3])]
    out=[]
    y = min(ys)+row*0.5
    while y < max(ys):
        hits=[]
        for (x1,y1,x2,y2) in edges:
            if (y1>y) != (y2>y):
                hits.append(x1 + (y-y1)*(x2-x1)/(y2-y1))
        hits.sort()
        for i in range(0, len(hits)-1, 2):       # even-odd: inside between pairs
            a,b = hits[i], hits[i+1]
            if b-a < 4: continue
            x = a+2
            while x < b-2:
                out.append((x, y, min(x+dash, b-2), y, ink))
                x += dash*1.35
        y += row
    return out


def water_knockout(water_lines, struct_segments, pad=16.0):
    """Drop water strokes lying on a bridge, walkway or building, so the
    structure reads on top of the water. Uses true distance to each structural
    segment (bounding boxes are far too blunt for diagonal walkways)."""
    import collections, math as _m
    CELL = max(24.0, pad*2.5)
    grid = collections.defaultdict(list)
    for (x1,y1,x2,y2) in struct_segments:
        n = max(1, int(_m.hypot(x2-x1, y2-y1)//CELL) + 1)
        for i in range(n+1):
            t = i/n
            px, py = x1+(x2-x1)*t, y1+(y2-y1)*t
            grid[(int(px//CELL), int(py//CELL))].append((x1,y1,x2,y2))
    def near(px, py):
        gx, gy = int(px//CELL), int(py//CELL)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for (x1,y1,x2,y2) in grid.get((gx+dx,gy+dy),()):
                    ddx, ddy = x2-x1, y2-y1
                    L2 = ddx*ddx + ddy*ddy
                    t = 0.0 if L2==0 else max(0.0, min(1.0, ((px-x1)*ddx + (py-y1)*ddy)/L2))
                    if _m.hypot(px-(x1+ddx*t), py-(y1+ddy*t)) <= pad: return True
        return False
    keep=[]
    for (x1,y1,x2,y2,ink) in water_lines:
        if near((x1+x2)/2, (y1+y2)/2): continue
        if near(x1,y1) or near(x2,y2): continue
        keep.append((x1,y1,x2,y2,ink))
    return keep


def innoruuk_face(cx, cy, s, ink=None):
    """The Prince of Hate's mask: horned brow, hollow eyes, tapering jaw."""
    ink = ink or PALETTE['glow']
    out=[]
    _P(out, [(cx-s*0.62, cy-s*0.52), (cx-s*0.30, cy-s*0.14), (cx-s*0.40, cy+s*0.10),
             (cx, cy+s*0.86), (cx+s*0.40, cy+s*0.10), (cx+s*0.30, cy-s*0.14),
             (cx+s*0.62, cy-s*0.52), (cx+s*0.22, cy-s*0.40), (cx, cy-s*0.62),
             (cx-s*0.22, cy-s*0.40)], ink, close=True)
    for sgn in (-1, 1):                                    # hollow eyes
        _P(out, [(cx+sgn*s*0.12, cy-s*0.14), (cx+sgn*s*0.30, cy-s*0.06),
                 (cx+sgn*s*0.16, cy+s*0.16)], ink, close=True)
    out.append((cx, cy+s*0.22, cx, cy+s*0.54, ink))
    return out


def brazier(bx, by, h, ink=None, flame=None):
    """Standing fire bowl."""
    ink = ink or PALETTE['obsidian']; flame = flame or PALETTE['lamp']
    out=[]
    _P(out, [(bx-h*0.30, by), (bx+h*0.30, by), (bx+h*0.20, by-h*0.16),
             (bx-h*0.20, by-h*0.16)], ink, close=True)
    out.append((bx, by-h*0.16, bx, by-h*0.54, ink))
    _P(out, [(bx-h*0.26, by-h*0.54), (bx+h*0.26, by-h*0.54),
             (bx+h*0.18, by-h*0.72), (bx-h*0.18, by-h*0.72)], ink, close=True)
    for k in (-1,0,1):                                     # flames
        out.append((bx+k*h*0.11, by-h*0.72, bx+k*h*0.06, by-h*1.05, flame))
        out.append((bx+k*h*0.06, by-h*1.05, bx+k*h*0.15, by-h*0.78, flame))
    return out


def innoruuk_temple(cx, cy, w, h, ink=None):
    """The Third Gate shrine: stepped dais, arched sanctum with the Prince's
    sigil, braziers flanking, and his mask glowing above the wall."""
    ink = ink or PALETTE['obsidian']
    RED = (168, 48, 52)
    out=[]
    for i in range(3):                                     # stepped dais
        t=i/3.0
        _P(out, [(cx-w*(0.50-t*0.07), cy-h*0.06*i), (cx+w*(0.50-t*0.07), cy-h*0.06*i),
                 (cx+w*(0.50-t*0.07), cy-h*0.06*(i+1)), (cx-w*(0.50-t*0.07), cy-h*0.06*(i+1))],
                ink, close=True)
    top = cy - h*0.18
    _P(out, [(cx-w*0.40, top), (cx-w*0.40, top-h*0.52),
             (cx+w*0.40, top-h*0.52), (cx+w*0.40, top)], ink)      # temple face
    # arched sanctum
    aw, ah = w*0.15, h*0.34
    _P(out, [(cx-aw, top), (cx-aw, top-ah*0.7), (cx-aw*0.6, top-ah),
             (cx+aw*0.6, top-ah), (cx+aw, top-ah*0.7), (cx+aw, top)], ink)
    out += [(cx-aw*0.5, top-ah*0.60, cx+aw*0.16, top-ah*0.34, RED),   # the red sigil
            (cx+aw*0.16, top-ah*0.34, cx-aw*0.10, top-ah*0.16, RED),
            (cx-aw*0.10, top-ah*0.16, cx+aw*0.42, top-ah*0.06, RED)]
    _arc(out, cx+aw*0.55, top-ah*0.46, aw*0.14, 0, 2*math.pi, RED, n=12)
    out += brazier(cx-aw*1.5, top, h*0.16)
    out += brazier(cx+aw*1.5, top, h*0.16)
    # carved faces either side, and the glowing mask above
    out += innoruuk_face(cx-w*0.31, top-h*0.26, h*0.13, PALETTE['basalt'])
    out += innoruuk_face(cx+w*0.31, top-h*0.26, h*0.13, PALETTE['basalt'])
    out += innoruuk_face(cx, top-h*0.74, h*0.15)
    for sgn in (-1,1):                                      # purple arcs round the mask
        for f in (1.0, 0.84):
            _arc(out, cx+sgn*h*0.13, top-h*0.74, h*0.16*f,
                 -math.pi/2, math.pi/2 if sgn>0 else -math.pi*1.5, PALETTE['basalt'], n=12)
    return out


def library_facade(cx, cy, w, h, ink=None, cols=6):
    """Neriak's library seen from the foot of its steps: a low tiled roof over a
    marble colonnade, with the trinity knot hanging above a pedestal within."""
    ink = ink or PALETTE['obsidian']
    out = []
    # --- steps rising toward the portico (drawn nearest-first) ---
    for i in range(3):
        t = i/3.0
        hw = w*(0.56 - t*0.05)
        y0 = cy - h*0.05*i
        _P(out, [(cx-hw, y0), (cx+hw, y0), (cx+hw, y0-h*0.05), (cx-hw, y0-h*0.05)],
           PALETTE['stone'], close=True)
    base = cy - h*0.15

    # --- columns with capitals and plinths ---
    cw = w*0.055
    span_ = w*0.86
    for k in range(cols):
        x = cx - span_*0.5 + span_*k/(cols-1)
        _P(out, [(x-cw*0.5, base), (x-cw*0.5, base-h*0.52),
                 (x+cw*0.5, base-h*0.52), (x+cw*0.5, base)], ink, close=True)
        _P(out, [(x-cw*0.80, base), (x+cw*0.80, base),
                 (x+cw*0.80, base-h*0.05), (x-cw*0.80, base-h*0.05)], ink, close=True)
        _P(out, [(x-cw*0.80, base-h*0.52), (x+cw*0.80, base-h*0.52),
                 (x+cw*0.80, base-h*0.57), (x-cw*0.80, base-h*0.57)], ink, close=True)
        out.append((x, base-h*0.06, x, base-h*0.50, PALETTE['basalt']))   # fluting

    # --- architrave and the pitched tiled roof ---
    ay = base - h*0.57
    _P(out, [(cx-w*0.50, ay), (cx+w*0.50, ay), (cx+w*0.50, ay-h*0.06),
             (cx-w*0.50, ay-h*0.06)], ink, close=True)
    ry = ay - h*0.06
    _P(out, [(cx-w*0.52, ry), (cx, ry-h*0.20), (cx+w*0.52, ry)], ink)
    for r in range(1, 4):                                    # tile courses
        f = r/4.0
        lx = cx - w*0.52*(1-f); rx = cx + w*0.52*(1-f); yy = ry - h*0.20*f
        out.append((lx, yy, rx, yy, PALETTE['basalt']))
        n = max(3, int((rx-lx)/(w*0.045)))
        for k in range(n):
            tx = lx + (rx-lx)*k/n
            out.append((tx, yy, tx, yy + h*0.20/4, PALETTE['basalt']))

    # --- dark interior between the middle columns ---
    iw = span_/(cols-1)*0.92
    y = base - h*0.06
    while y > base - h*0.50:
        out.append((cx-iw*0.5, y, cx+iw*0.5, y, PALETTE['basalt']))
        y -= h*0.035

    # --- pedestal, and the knot floating above it ---
    pw, ph = w*0.10, h*0.14
    _P(out, [(cx-pw*0.5, base), (cx+pw*0.5, base),
             (cx+pw*0.42, base-ph), (cx-pw*0.42, base-ph)], ink, close=True)
    out.append((cx-pw*0.46, base-ph, cx+pw*0.46, base-ph, ink))
    out += triquetra(cx, base - ph - h*0.16, h*0.085)
    return out


def water_flood(water_segments, struct_segments, ink=None,
                cell=5.0, row=11.0, dash=9.0, blue_frac=0.26, max_frac=0.30,
                clearance=2, solid=True):
    """Shade water by FLOOD FILL rather than by polygon.

    Real maps bound a pool partly with a shoreline and partly with the walls of
    the buildings beside it, so an outline-only fill can never resolve them.
    Here every line — shoreline and structure alike — is rasterised as a wall,
    the open regions between them are labelled, and a region counts as water when
    enough of its border is shoreline. Islands, moats, walkways and bridges then
    fall out for free: they are simply walls.

    `solid=True` (the default) draws each row as one continuous run so the body
    reads as filled water rather than hatching — the way in-game map packs do it.
    `clearance` keeps a gutter clear around every structure so paths stay legible.
    """
    import collections
    ink = ink or PALETTE['arcane']
    if not water_segments: return []
    xs=[a for s in water_segments for a in (s[0],s[2])]
    ys=[a for s in water_segments for a in (s[1],s[3])]
    pad = cell*6
    x0,x1 = min(xs)-pad, max(xs)+pad
    y0,y1 = min(ys)-pad, max(ys)+pad
    W = int((x1-x0)/cell)+2; H = int((y1-y0)/cell)+2
    if W*H > 4_000_000: cell *= 2; W//=2; H//=2
    wall = bytearray(W*H)          # 0 free, 1 structure wall, 2 shoreline
    def stamp(segs, mark):
        for (ax,ay,bx,by) in segs:
            n = max(1, int(math.hypot(bx-ax, by-ay)/(cell*0.5)))
            for i in range(n+1):
                t=i/n
                gx=int((ax+(bx-ax)*t - x0)/cell); gy=int((ay+(by-ay)*t - y0)/cell)
                if 0<=gx<W and 0<=gy<H:
                    idx=gy*W+gx
                    if wall[idx]!=2: wall[idx]=mark
    stamp([(s[0],s[1],s[2],s[3]) for s in struct_segments], 1)
    stamp([(s[0],s[1],s[2],s[3]) for s in water_segments], 2)

    # CLEARANCE: grow a gutter out from every structural wall. Paths, bridges and
    # buildings must read clearly, so nothing may be shaded within this band —
    # this is applied before any region is filled, not as a later knockout.
    if clearance > 0:
        import collections as _c
        dist = bytearray(W*H)
        q = _c.deque()
        for i in range(W*H):
            if wall[i]==1:
                dist[i]=1; q.append(i)
        while q:
            i=q.popleft(); d=dist[i]
            if d > clearance: continue
            gx=i%W; gy=i//W
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx,ny=gx+dx,gy+dy
                if not (0<=nx<W and 0<=ny<H): continue
                j=ny*W+nx
                if dist[j]==0 and wall[j]!=1:
                    dist[j]=d+1
                    if d+1 <= clearance: q.append(j)
        gutter = bytes(1 if 0 < dist[i] <= clearance+1 else 0 for i in range(W*H))
    else:
        gutter = bytes(W*H)

    seen = bytearray(W*H)
    total = W*H

    # Parity may only be measured against CLOSED shorelines. An open shoreline
    # has no inside, and a ray crossing one adds a phantom crossing that flips
    # every region beyond it.
    _adj = collections.defaultdict(list)
    _k = lambda p: (round(p[0],1), round(p[1],1))
    for i,sg in enumerate(water_segments):
        _adj[_k((sg[0],sg[1]))].append(i); _adj[_k((sg[2],sg[3]))].append(i)
    _seen=set(); closed=[]
    for i in range(len(water_segments)):
        if i in _seen: continue
        st=[i]; comp=[]
        while st:
            j=st.pop()
            if j in _seen: continue
            _seen.add(j); comp.append(j)
            for kk in _adj[_k((water_segments[j][0],water_segments[j][1]))] + \
                      _adj[_k((water_segments[j][2],water_segments[j][3]))]:
                if kk not in _seen: st.append(kk)
        alive=set(comp)
        while True:                       # shave spurs so a tail cannot open a loop
            d=collections.Counter()
            for j in alive:
                d[_k((water_segments[j][0],water_segments[j][1]))]+=1
                d[_k((water_segments[j][2],water_segments[j][3]))]+=1
            spur={j for j in alive
                  if d[_k((water_segments[j][0],water_segments[j][1]))]==1
                  or d[_k((water_segments[j][2],water_segments[j][3]))]==1}
            if not spur: break
            alive -= spur
            if not alive: break
        if alive:
            _xs=[a for j in alive for a in (water_segments[j][0],water_segments[j][2])]
            _ys=[a for j in alive for a in (water_segments[j][1],water_segments[j][3])]
            closed.append(([water_segments[j] for j in alive],
                           min(_xs), max(_xs), min(_ys), max(_ys)))

    def water_parity(px, py):
        """Cross the SHORELINE only, on a ray to the left. Odd = inside water.

        A region ringed entirely by shoreline scores 100% 'blue border' whether it
        is a pool or the island in the middle of one, so border colour cannot
        decide it. Crossing parity can: the moat is one crossing deep, the island
        two.
        """
        # only loops whose extent actually contains the point can enclose it —
        # counting distant pools adds phantom crossings and flips the answer
        crossings = 0
        for segs, lx0, lx1, ly0, ly1 in closed:
            if not (lx0 <= px <= lx1 and ly0 <= py <= ly1): continue
            for (x1,y1,x2,y2) in segs:
                if (y1 > py) != (y2 > py):
                    if x1 + (py-y1)*(x2-x1)/(y2-y1) < px: crossings += 1
        return crossings % 2 == 1

    # ---- authority 1: even-odd mask from the CLOSED shorelines ----------------
    # Concentric shorelines (a moat ringing an island) only come out right if the
    # mask is built by crossing parity across the whole loop set at once.
    inwater = bytearray(W*H)
    if closed:
        allsegs=[sg for segs,_,_,_,_ in closed for sg in segs]
        for gy in range(H):
            py = y0 + gy*cell + cell*0.5
            hits=[]
            for (sx1,sy1,sx2,sy2) in allsegs:
                if (sy1 > py) != (sy2 > py):
                    hits.append(sx1 + (py-sy1)*(sx2-sx1)/(sy2-sy1))
            if not hits: continue
            hits.sort()
            # The base map draws each shoreline two to four times over itself.
            # Duplicated crossings flip parity an even number of times and cancel,
            # so coincident hits must collapse to one before the even-odd pass.
            eps = cell*0.75
            ded=[hits[0]]
            for h in hits[1:]:
                if h - ded[-1] > eps: ded.append(h)
            hits = ded
            for hi in range(0, len(hits)-1, 2):
                ga = int((hits[hi]-x0)/cell); gb = int((hits[hi+1]-x0)/cell)
                for gx in range(max(0,ga), min(W-1,gb)+1):
                    inwater[gy*W+gx] = 1

    # ---- authority 2: flood regions, for shorelines that are left open --------
    regions=[]
    for start in range(total):
        if wall[start] or seen[start]: continue
        stack=[start]; seen[start]=1; cells=[]; blue=0; solid=0; touches_edge=False
        while stack:
            i=stack.pop(); cells.append(i)
            gx=i%W; gy=i//W
            if gx==0 or gy==0 or gx==W-1 or gy==H-1: touches_edge=True
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx,ny=gx+dx,gy+dy
                if not (0<=nx<W and 0<=ny<H): continue
                j=ny*W+nx
                if wall[j]==2: blue+=1
                elif wall[j]==1: solid+=1
                elif not seen[j]:
                    seen[j]=1; stack.append(j)
        if touches_edge: continue
        border=blue+solid
        if not border or blue/border < blue_frac: continue
        if len(cells) > total*max_frac: continue
        # a flood region only counts where the closed-loop mask agrees, unless the
        # mask has nothing to say there at all (an open shoreline)
        agree = sum(1 for i in cells if inwater[i])
        if closed and agree*2 < len(cells):
            near_closed = any(lx0-cell*3 <= x0+(i%W)*cell <= lx1+cell*3 and
                              ly0-cell*3 <= y0+(i//W)*cell <= ly1+cell*3
                              for i in cells[::max(1,len(cells)//5)]
                              for _,lx0,lx1,ly0,ly1 in closed)
            if near_closed: continue        # the mask says rock — believe it
        regions.append(cells)

    for cells in regions:
        for i in cells: inwater[i] = 1
    regions = [[i for i in range(total) if inwater[i] and not wall[i]]]

    out=[]
    rows = max(1, int(row/cell))
    for cells in regions:
        byrow=collections.defaultdict(list)
        for i in cells: byrow[i//W].append(i%W)
        for gy in sorted(byrow):
            if gy % rows: continue
            cols=sorted(c for c in byrow[gy] if not gutter[gy*W+c])
            if not cols: continue
            runs=[]; s_=cols[0]; p=cols[0]
            for c in cols[1:]:
                if c==p+1: p=c; continue
                runs.append((s_,p)); s_=c; p=c
            runs.append((s_,p))
            yy = y0+gy*cell
            for a,b in runs:
                ax = x0+a*cell; bx = x0+b*cell
                if bx-ax < cell*1.2: continue
                if solid:
                    out.append((ax, yy, bx, yy, ink))      # one continuous run
                else:
                    x = ax
                    while x < bx:
                        out.append((x, yy, min(x+dash, bx), yy, ink))
                        x += dash*1.4
    return out


def serpent_carving(cx, cy, s, ink=None, mirror=False):
    """The gold twin-serpent relief that flanks the Lodge gate: two heads facing
    in, long bodies looping out, a curled tail-knot below."""
    ink = ink or PALETTE['lamp']
    out=[]
    m = -1 if mirror else 1
    def P(pts, close=False): _P(out, [(cx+m*px*s, cy+py*s) for px,py in pts], ink, close)
    # upper serpent: head at the inner side, body sweeping up and out
    P([(0.10,-0.02),(0.02,-0.16),(-0.16,-0.24),(-0.40,-0.20),(-0.58,-0.04),
       (-0.62,0.14),(-0.50,0.26)])
    P([(0.10,-0.02),(0.00,0.10),(-0.18,0.16),(-0.38,0.12)])       # jaw
    _arc(out, cx+m*0.04*s, cy-0.06*s, s*0.045, 0, 2*math.pi, ink, n=10)   # eye
    P([(-0.16,-0.24),(-0.14,-0.36)]); P([(-0.24,-0.24),(-0.24,-0.37)])    # horns
    # lower serpent, mirrored about the horizontal
    P([(0.10,0.30),(0.02,0.44),(-0.16,0.52),(-0.40,0.48),(-0.58,0.32),
       (-0.62,0.14)])
    _arc(out, cx+m*0.04*s, cy+0.34*s, s*0.04, 0, 2*math.pi, ink, n=10)
    # the knot below: two facing spirals over a bar
    for sgn,ox in ((1,-0.42),(-1,-0.14)):
        prev=None
        for k in range(15):
            t=k/14.0; a=sgn*t*2.3*math.pi
            r=s*0.13*(1-t*0.72)
            p=(cx+m*(ox*s+math.cos(a)*r), cy+0.62*s+math.sin(a)*r)
            if prev: out.append((prev[0],prev[1],p[0],p[1],ink))
            prev=p
    P([(-0.44,0.80),(-0.12,0.80)])
    P([(-0.50,0.92),(-0.38,1.00),(-0.18,1.00),(-0.06,0.92)])
    return out


def lodge_of_the_dead(cx, cy, w, h, ink=None, roof=None, tile=None):
    """Neriak's Lodge of the Dead — where the necromancer and shadowknight
    trainers keep hall. East-Asian tiered roof with upswept eaves over a red
    brick face, twin gold serpent reliefs flanking a barred gate.

    The roof is red, as it is in game — the one warm mass on an otherwise
    black-and-violet building."""
    ink = ink or PALETTE['obsidian']
    roof = roof or PALETTE['tile']
    tile = tile or PALETTE['tile_lit']
    out=[]
    # --- brick face ---
    _P(out, [(cx-w*0.5, cy), (cx-w*0.5, cy-h*0.52),
             (cx+w*0.5, cy-h*0.52), (cx+w*0.5, cy)], ink, close=True)
    rows=4
    for r in range(1, rows):
        y=cy-h*0.52*r/rows
        out.append((cx-w*0.5, y, cx+w*0.5, y, PALETTE['basalt']))
        off=(r%2)*0.5
        for k in range(6):
            x=cx-w*0.5+w*(k+off)/6.0
            if cx-w*0.5<x<cx+w*0.5:
                out.append((x, y, x, y-h*0.52/rows, PALETTE['basalt']))
    # --- two tiers of roof, eaves sweeping up at the ends ---
    for tier,(ty,tw,th) in enumerate([(cy-h*0.52, w*0.60, h*0.16),
                                      (cy-h*0.70, w*0.46, h*0.14)]):
        ridge = ty-th
        _P(out, [(cx-tw, ty), (cx-tw*0.86, ridge), (cx+tw*0.86, ridge), (cx+tw, ty)], roof)
        out.append((cx-tw*0.86, ridge, cx+tw*0.86, ridge, roof))
        out.append((cx-tw, ty, cx+tw, ty, roof))              # eave line
        for sgn in (-1,1):                                    # upswept eave
            prev=None
            for k in range(9):
                t=k/8.0
                px = cx + sgn*(tw + t*w*0.16)
                py = ty - (t**2)*th*0.85
                if prev: out.append((prev[0],prev[1],px,py,roof))
                prev=(px,py)
        n=7                                                   # tile courses
        for k in range(1,n):
            f=k/n
            lx=cx-tw*(1-f*0.14); rx=cx+tw*(1-f*0.14); yy=ty-th*f
            out.append((lx,yy,rx,yy,tile))
        for k in range(9):                                    # tile ribs
            xx = cx - tw*0.9 + tw*1.8*k/8.0
            out.append((xx, ty, xx*0.985+cx*0.015, ridge, tile))
    # --- gate and torches ---
    out += barred_gate(cx, cy, w*0.16, h*0.22)
    out += torch(cx-w*0.15, cy-h*0.06, h*0.10)
    out += torch(cx+w*0.15, cy-h*0.06, h*0.10)
    # --- the serpent reliefs ---
    out += serpent_carving(cx-w*0.28, cy-h*0.30, min(w,h)*0.30)
    out += serpent_carving(cx+w*0.28, cy-h*0.30, min(w,h)*0.30, mirror=True)
    return out


def sunburst_medallion(cx, cy, r, ink=None, rim=None):
    """The spiked iron disc set either side of the bastion runes."""
    ink = ink or PALETTE['basalt']; rim = rim or PALETTE['obsidian']
    out=[]
    _arc(out, cx, cy, r*0.52, 0, 2*math.pi, rim, n=20)
    _arc(out, cx, cy, r*0.40, 0, 2*math.pi, ink, n=18)
    for k in range(8):                               # spikes
        a = k*math.pi/4
        _P(out, [(cx+math.cos(a-0.16)*r*0.52, cy+math.sin(a-0.16)*r*0.52),
                 (cx+math.cos(a)*r, cy+math.sin(a)*r),
                 (cx+math.cos(a+0.16)*r*0.52, cy+math.sin(a+0.16)*r*0.52)], rim)
    for k in range(5):                               # boss studs
        a = k*2*math.pi/5 - math.pi/2
        _arc(out, cx+math.cos(a)*r*0.22, cy+math.sin(a)*r*0.22, r*0.06, 0, 2*math.pi, rim, n=8)
    return out


def watcher(cx, cy, s, ink=None):
    """A head and shoulders peering over a parapet."""
    ink = ink or PALETTE['obsidian']
    out=[]
    _arc(out, cx, cy-s*0.34, s*0.30, math.pi, 2*math.pi, ink, n=14)   # skull
    out.append((cx-s*0.30, cy-s*0.34, cx-s*0.42, cy, ink))            # shoulders
    out.append((cx+s*0.30, cy-s*0.34, cx+s*0.42, cy, ink))
    out.append((cx-s*0.42, cy, cx+s*0.42, cy, ink))
    for sgn in (-1,1):                                                # tusks / ears
        out.append((cx+sgn*s*0.30, cy-s*0.40, cx+sgn*s*0.44, cy-s*0.56, ink))
    out.append((cx-s*0.14, cy-s*0.40, cx-s*0.06, cy-s*0.40, ink))     # eyes
    out.append((cx+s*0.06, cy-s*0.40, cx+s*0.14, cy-s*0.40, ink))
    return out


def bastion_gate(cx, cy, w, h, ink=None):
    """The bastion guarding Third Gate's north-east quarter: a battlemented
    tower with watchers at the slots, crossed glowing wards on the face, iron
    medallions either side, and a barred gate reached by a plank bridge."""
    ink = ink or PALETTE['obsidian']
    VIOLET=(104,86,190); EMBER=(198,92,54)
    out=[]
    # --- tower face, angled at the corners ---
    _P(out, [(cx-w*0.44, cy), (cx-w*0.50, cy-h*0.62), (cx-w*0.36, cy-h*0.76),
             (cx+w*0.36, cy-h*0.76), (cx+w*0.50, cy-h*0.62), (cx+w*0.44, cy)],
       ink, close=True)
    rows=5
    for r in range(1, rows):
        y=cy-h*0.76*r/rows
        f=1.0 if y > cy-h*0.62 else 0.9
        out.append((cx-w*0.47*f, y, cx+w*0.47*f, y, PALETTE['basalt']))
    # --- battlements and the watch slots ---
    top=cy-h*0.76
    out.append((cx-w*0.40, top, cx+w*0.40, top, ink))
    for k in range(7):
        x=cx-w*0.40+w*0.80*k/6.0
        out.append((x, top, x, top-h*0.07, ink))
        if k<6: out.append((x, top-h*0.07, x+w*0.80/6.0*(0.55 if k%2==0 else 0), top-h*0.07, ink))
    for k,sx in enumerate((-0.24, 0.0, 0.24)):                # three slots
        _P(out, [(cx+sx*w-w*0.09, top-h*0.05), (cx+sx*w+w*0.09, top-h*0.05),
                 (cx+sx*w+w*0.07, top-h*0.20), (cx+sx*w-w*0.07, top-h*0.20)], ink, close=True)
        if k != 1: out += watcher(cx+sx*w, top-h*0.06, h*0.16)
    # --- the crossed wards ---
    for ink2, sgn in ((VIOLET,-1),(EMBER,1)):
        prev=None
        for i in range(19):
            t=i/18.0
            px = cx + sgn*w*0.22*(1-t) - sgn*w*0.20*t
            py = cy-h*0.52 + t*h*0.34 + math.sin(t*3.2)*h*0.05
            if prev: out.append((prev[0],prev[1],px,py,ink2))
            prev=(px,py)
        hx = cx + sgn*w*0.22; hy = cy-h*0.52
        for a in (-0.9,-0.3,0.3,0.9):                          # splayed claw head
            out.append((hx, hy, hx+math.sin(a)*w*0.10, hy-math.cos(a)*h*0.13, ink2))
        _arc(out, hx, hy, w*0.035, 0, 2*math.pi, ink2, n=10)
    out += sunburst_medallion(cx-w*0.37, cy-h*0.44, w*0.09)
    out += sunburst_medallion(cx+w*0.37, cy-h*0.44, w*0.09)
    # --- gate and the plank bridge running out to it ---
    out += barred_gate(cx, cy, w*0.14, h*0.20)
    for k in range(6):
        y = cy + h*0.05 + k*h*0.045
        hw = w*0.10 + k*w*0.008
        out.append((cx-hw, y, cx+hw, y, PALETTE['basalt']))
    out.append((cx-w*0.10, cy+h*0.05, cx-w*0.15, cy+h*0.30, ink))
    out.append((cx+w*0.10, cy+h*0.05, cx+w*0.15, cy+h*0.30, ink))
    return out


if __name__ == '__main__':
    import cairosvg
    demo = []
    demo += arched_gate(300, 300, 460, 300)
    demo += teirdal_sigil(640, 180, 90, 120)
    demo += triquetra(640, 340, 46)
    demo += candelabra(760, 380, 130)
    demo += cavern_edge(40, 820, 40, 26)
    demo += web_corner(50, 400, 90, quadrant=3)
    demo += torch(830, 300, 60)
    xs = [v for s in demo for v in (s[0], s[2])]
    ys = [v for s in demo for v in (s[1], s[3])]
    mnx, mxx, mny, mxy = min(xs)-20, max(xs)+20, min(ys)-20, max(ys)+20
    W = 880; sc = W/(mxx-mnx); H = int((mxy-mny)*sc)
    pr = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
          f'<rect width="{W}" height="{H}" fill="#f4efe0"/>']
    for x1, y1, x2, y2, c in demo:
        pr.append(f'<line x1="{(x1-mnx)*sc:.1f}" y1="{(y1-mny)*sc:.1f}" x2="{(x2-mnx)*sc:.1f}" '
                  f'y2="{(y2-mny)*sc:.1f}" stroke="rgb{c}" stroke-width="1.5"/>')
    pr.append('</svg>')
    cairosvg.svg2png(bytestring=''.join(pr).encode(),
                     write_to='/mnt/user-data/outputs/_darkelf_kit.png',
                     output_width=W, output_height=H)
    print(f"Dark Elf kit demo: {len(demo)} segments")
