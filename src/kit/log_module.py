"""Fallen log — reusable module.

Give it TWO /locs (the two ends of the log) and it infers everything else:
orientation, length, thickness, the cut face, bark texture and broken stubs.

    from log_module import log_from_locs
    lines = log_from_locs((106.2, 560.8), (61.4, 402.9), ink=(120,86,54))

Transform is the project standard: native = (-loc2, -loc1).
"""
import math, random

def wn(loc1, loc2):
    """Game /loc -> native map coords."""
    return (-loc2, -loc1)

def log_segs(ax, ay, bx, by, ink=(120, 86, 54), seed=None,
             thickness=None, cut_end='b', stubs=True):
    """Fallen log lying from A to B. Returns [(x1,y1,x2,y2,ink), ...].

    thickness : trunk radius in native units. Default scales with length
                (a log twice as long reads twice as heavy).
    cut_end   : 'a', 'b' or None - which end shows the sawn/broken face.
    """
    rnd = random.Random(seed if seed is not None else int(ax * 31 + ay * 17))
    out = []
    def L(x1, y1, x2, y2): out.append((x1, y1, x2, y2, ink))

    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    if length < 1e-6: return out
    ux, uy = dx / length, dy / length          # along the log
    px, py = -uy, ux                           # across it

    r = thickness if thickness else max(6.0, min(length * 0.085, length * 0.5))
    r_far = r * 0.82                           # slight taper toward the far end

    def P(t, off):
        """t along the log 0..1, off across it."""
        rr = r + (r_far - r) * t
        return (ax + ux * length * t + px * off * rr,
                ay + uy * length * t + py * off * rr)

    # --- the two long sides, with a gentle natural bow ---
    for side in (-1, 1):
        prev = None
        for k in range(13):
            t = k / 12.0
            bow = math.sin(math.pi * t) * r * 0.12 * side
            x, y = P(t, side)
            x += px * bow; y += py * bow
            if prev: L(prev[0], prev[1], x, y)
            prev = (x, y)

    # --- end caps: the cut face reads as an ellipse with rings ---
    def cap(t, rings):
        rr = r + (r_far - r) * t
        cx = ax + ux * length * t
        cy = ay + uy * length * t
        depth = rr * 0.42 * (1 if t > 0.5 else -1)
        prev = None
        for k in range(17):
            a = 2 * math.pi * k / 16
            x = cx + px * math.cos(a) * rr + ux * math.sin(a) * depth
            y = cy + py * math.cos(a) * rr + uy * math.sin(a) * depth
            if prev: L(prev[0], prev[1], x, y)
            prev = (x, y)
        if rings:
            for f in (0.62, 0.34):
                prev = None
                for k in range(13):
                    a = 2 * math.pi * k / 12
                    x = cx + px * math.cos(a) * rr * f + ux * math.sin(a) * depth * f
                    y = cy + py * math.cos(a) * rr * f + uy * math.sin(a) * depth * f
                    if prev: L(prev[0], prev[1], x, y)
                    prev = (x, y)
    cap(0.0, cut_end == 'a')
    cap(1.0, cut_end == 'b')

    # --- bark: short strokes running with the grain ---
    n = max(4, int(length / (r * 1.5)))
    for i in range(n):
        t0 = (i + 0.18) / n
        t1 = t0 + rnd.uniform(0.05, 0.13)
        if t1 > 0.96: continue
        off = rnd.uniform(-0.72, 0.72)
        x0, y0 = P(t0, off); x1, y1 = P(t1, off + rnd.uniform(-0.08, 0.08))
        L(x0, y0, x1, y1)

    # --- broken branch stubs ---
    if stubs:
        for _ in range(rnd.randint(1, 3)):
            t = rnd.uniform(0.18, 0.82)
            side = rnd.choice((-1, 1))
            bx0, by0 = P(t, side * 0.92)
            ln = r * rnd.uniform(0.9, 1.8)
            ang = rnd.uniform(-0.6, 0.6)
            ex = bx0 + (px * side * math.cos(ang) + ux * math.sin(ang)) * ln
            ey = by0 + (py * side * math.cos(ang) + uy * math.sin(ang)) * ln
            L(bx0, by0, ex, ey)
            L(ex, ey, ex + px * side * ln * 0.22, ey + py * side * ln * 0.22)
    return out


def log_from_locs(loc_a, loc_b, **kw):
    """Two in-game /locs (each a (loc1, loc2) pair) -> log geometry."""
    ax, ay = wn(*loc_a); bx, by = wn(*loc_b)
    return log_segs(ax, ay, bx, by, **kw)


def to_map_lines(segs, z=0.0):
    return ["L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"
            % (x1, y1, z, x2, y2, z, c[0], c[1], c[2]) for x1, y1, x2, y2, c in segs]


if __name__ == '__main__':
    import cairosvg
    demos = [((0, 0), (300, 0), 'along X'),
             ((0, 160), (210, 300), 'diagonal'),
             ((360, 0), (360, 250), 'along Y'),
             ((460, 40), (700, 120), 'long & thin')]
    allseg = []
    for a, b, _ in demos:
        allseg += log_segs(a[0], a[1], b[0], b[1])
    xs = [v for s in allseg for v in (s[0], s[2])]
    ys = [v for s in allseg for v in (s[1], s[3])]
    mnx, mxx, mny, mxy = min(xs) - 30, max(xs) + 30, min(ys) - 30, max(ys) + 30
    W = 820; sc = W / (mxx - mnx); H = int((mxy - mny) * sc)
    pr = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
          f'<rect width="{W}" height="{H}" fill="#f4efe0"/>']
    for x1, y1, x2, y2, c in allseg:
        pr.append(f'<line x1="{(x1-mnx)*sc:.1f}" y1="{(y1-mny)*sc:.1f}" '
                  f'x2="{(x2-mnx)*sc:.1f}" y2="{(y2-mny)*sc:.1f}" '
                  f'stroke="rgb{c}" stroke-width="1.8"/>')
    pr.append('</svg>')
    cairosvg.svg2png(bytestring=''.join(pr).encode(),
                     write_to='/mnt/user-data/outputs/_log_module_demo.png',
                     output_width=W, output_height=H)
    print(f"demo: {len(allseg)} segments across {len(demos)} logs")
