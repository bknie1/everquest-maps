"""styles.py -- the racial letterform families for the title campaign.

Each family turns a string into native-map L-strokes (y grows south). All of
them build on the complete skeleton in glyphs.py, so no family can ship a
broken E again; what differs is weight, posture, ink, and flourish -- the
things that make Halas read as carved ice and Neriak as dark-elf filigree.

    from styles import render, STYLES
    segs = render("runic", "HALAS", x=..., baseline_y=..., h=120)

Every renderer returns (segs, bbox) with bbox=(x0,y0,x1,y1) of the lettering
alone (flourishes included), so callers can center and knock out around it.
"""
import math
import random
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from glyphs import GLYPHS, ANGULAR, ROUNDED, layout_text, text_width  # noqa: E402


def _emit(text, x, y, h, tracking=14, variants=None, slant=0.0, seed=0,
          rot_jitter=0.0, base_jitter=0.0, scale_jitter=0.0, condense=1.0):
    """Lay the text out and return per-letter native polylines.

    Returns [(ch, [poly, ...]), ...] with poly = [(nx, ny), ...] in native
    coords: baseline at y, caps at y-h. slant shears tops rightward.
    """
    rng = random.Random(seed)
    s = h / 100.0
    letters = []
    for ch, pen, polys in layout_text(text, tracking=tracking, variants=variants):
        rot = math.radians(rng.uniform(-rot_jitter, rot_jitter))
        dy = rng.uniform(-base_jitter, base_jitter) * h
        ls = 1.0 + rng.uniform(-scale_jitter, scale_jitter)
        w = max(px for poly in polys for (px, _) in poly) or 1
        cx, cy = w / 2.0, 50.0
        out = []
        for poly in polys:
            np = []
            for (gx, gy) in poly:
                px, py = (gx - cx) * ls, (gy - cy) * ls
                if rot:
                    px, py = (px * math.cos(rot) - py * math.sin(rot),
                              px * math.sin(rot) + py * math.cos(rot))
                px, py = px + cx, py + cy
                px += slant * py                    # shear in glyph space
                np.append((x + (pen + px) * s * condense, y - py * s + dy))
            out.append(np)
        letters.append((ch, out))
    return letters


def _lines(letters, ink):
    segs = []
    for _, polys in letters:
        for poly in polys:
            for i in range(len(poly) - 1):
                segs.append((poly[i][0], poly[i][1], poly[i + 1][0], poly[i + 1][1], ink))
    return segs


def _offset(segs, dx, dy, ink):
    return [(a + dx, b + dy, c + dx, d + dy, ink) for (a, b, c, d, _) in segs]


def _thicken(segs, t, ink):
    """Parallel copies either side of each stroke -- poor man's weight."""
    out = []
    for (a, b, c, d, _) in segs:
        L = math.hypot(c - a, d - b) or 1
        nx, ny = -(d - b) / L * t, (c - a) / L * t
        out.append((a + nx, b + ny, c + nx, d + ny, ink))
        out.append((a - nx, b - ny, c - nx, d - ny, ink))
    return out


def _bbox(segs, pad=0.0):
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def _ends(letters):
    """Endpoints of every polyline (for serifs/spikes), with local direction."""
    for _, polys in letters:
        for poly in polys:
            if poly[0] == poly[-1]:
                continue                             # closed loop: no ends
            yield poly[0], poly[1]
            yield poly[-1], poly[-2]


# --------------------------------------------------------------------------
# families
# --------------------------------------------------------------------------

def extruded(text, x, y, h, face=(216, 122, 40), depth_ink=(70, 44, 24),
             depth=0.14, tracking=16, seed=0):
    """The Freeport big-caps: bright face with a dark 3D extrusion behind."""
    letters = _emit(text, x, y, h, tracking=tracking, seed=seed)
    facesegs = _lines(letters, face)
    dx, dy = depth * h * 0.6, depth * h * 0.6
    segs = _offset(facesegs, dx, dy, depth_ink)
    segs += _offset(facesegs, dx * 0.5, dy * 0.5, depth_ink)   # solid flank
    for _, polys in letters:                          # connectors at vertices
        for poly in polys:
            for (px, py) in poly:
                segs.append((px, py, px + dx, py + dy, depth_ink))
    segs += _thicken(facesegs, h * 0.016, face) + facesegs
    return segs, _bbox(segs)


def small_caps(text, x, y, h, ink=(150, 132, 104), tracking=18, seed=0):
    letters = _emit(text, x, y, h, tracking=tracking, seed=seed)
    segs = _lines(letters, ink)
    return segs, _bbox(segs)


def runic(text, x, y, h, ink=(88, 108, 128), ice=(176, 196, 210), seed=0):
    """Halas: angular carved strokes, a pale ice highlight, notch serifs."""
    letters = _emit(text, x, y, h, tracking=20, variants=ANGULAR, seed=seed)
    body = _lines(letters, ink)
    segs = (_thicken(body, h * 0.030, ink)            # carved weight
            + _offset(body, -h * 0.05, -h * 0.05, ice) + body)
    t = h * 0.11
    for (ex, ey), (tx, ty) in _ends(letters):         # chisel notches
        L = math.hypot(tx - ex, ty - ey) or 1
        ux, uy = (tx - ex) / L, (ty - ey) / L
        segs.append((ex - uy * t, ey + ux * t, ex + uy * t, ey - ux * t, ink))
    return segs, _bbox(segs)


def crude(text, x, y, h, ink=(86, 110, 60), shade=(50, 66, 38), seed=3):
    """Grobb/Oggok: thick, lurching, nothing level. Pass ogre inks for Oggok."""
    letters = _emit(text, x, y, h, tracking=24, seed=seed,
                    rot_jitter=5.0, base_jitter=0.05, scale_jitter=0.10)
    body = _lines(letters, ink)
    segs = _thicken(body, h * 0.030, ink) + _thicken(body, h * 0.060, shade) + body
    return segs, _bbox(segs)


def darkelf(text, x, y, h, ink=(112, 72, 152), echo=(70, 46, 96), seed=0):
    """Neriak: condensed, tall, with spiked terminals -- filigree with fangs."""
    letters = _emit(text, x, y, h, tracking=12, condense=0.85, seed=seed)
    body = _lines(letters, ink)
    segs = _offset(body, h * 0.03, h * 0.03, echo) + body
    t = h * 0.065
    for (ex, ey), (tx, ty) in _ends(letters):         # slim spike terminals,
        if abs(tx - ex) > abs(ty - ey):               # vertical strokes only
            continue
        L = math.hypot(tx - ex, ty - ey) or 1
        ux, uy = (ex - tx) / L, (ey - ty) / L         # outward
        segs.append((ex - uy * t * 0.5, ey + ux * t * 0.5, ex + ux * t, ey + uy * t, ink))
        segs.append((ex + uy * t * 0.5, ey - ux * t * 0.5, ex + ux * t, ey + uy * t, ink))
    return segs, _bbox(segs)


def highelf(text, x, y, h, ink=(44, 92, 56), gold=(198, 152, 62), seed=0):
    """Felwithe: light italic strokes with a golden echo and a vine swash."""
    letters = _emit(text, x, y, h, tracking=18, slant=0.14, seed=seed)
    body = _lines(letters, ink)
    segs = _offset(body, -h * 0.03, -h * 0.03, gold) + body
    x0, y0, x1, y1 = _bbox(body)
    yy = y + h * 0.24                                  # vine swash under all
    n = 26
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        f = lambda t: (x0 + (x1 - x0) * t, yy + math.sin(t * math.pi * 3) * h * 0.09)
        a, b = f(t0), f(t1)
        segs.append((a[0], a[1], b[0], b[1], gold))
        segs.append((a[0], a[1] + h * 0.02, b[0], b[1] + h * 0.02, gold))
        if i % 5 == 2:                                 # leaves off the vine
            s = h * 0.13
            segs += [(b[0], b[1], b[0] + s * 0.6, b[1] - s, ink),
                     (b[0] + s * 0.6, b[1] - s, b[0] + s * 1.2, b[1] - s * 0.3, ink),
                     (b[0] + s * 1.2, b[1] - s * 0.3, b[0], b[1], ink)]
    return segs, _bbox(segs)


def rounded(text, x, y, h, ink=(122, 82, 42), cream=(180, 148, 96), seed=0):
    """Rivervale: soft round bowls, doubled for warmth, a full-stop dot."""
    letters = _emit(text, x, y, h, tracking=16, variants=ROUNDED, seed=seed)
    body = _lines(letters, ink)
    segs = _thicken(body, h * 0.028, ink) + _offset(body, -h * 0.045, -h * 0.045, cream) + body
    x0, y0, x1, y1 = _bbox(body)
    r = h * 0.07                                       # the homely full stop
    cxx, cyy = x1 + h * 0.22, y
    for i in range(8):
        a0, a1 = math.pi * i / 4, math.pi * (i + 1) / 4
        segs.append((cxx + r * math.cos(a0), cyy - r + r * math.sin(a0),
                     cxx + r * math.cos(a1), cyy - r + r * math.sin(a1), ink))
    return segs, _bbox(segs)


def clockwork(text, x, y, h, brass=(176, 126, 52), iron=(92, 74, 52), seed=0):
    """Ak'Anon: brass caps; every O becomes a toothed gear, rivets between."""
    letters = _emit(text, x, y, h, tracking=20, seed=seed)
    body = _lines(letters, brass)
    segs = _offset(body, h * 0.035, h * 0.035, iron) + body
    for ch, polys in letters:
        if ch not in "OQ":
            continue
        xs = [p[0] for poly in polys for p in poly]
        ys = [p[1] for poly in polys for p in poly]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        r = (max(xs) - min(xs)) / 2
        for i in range(12):                            # gear teeth
            a = 2 * math.pi * i / 12
            segs.append((cx + math.cos(a) * r * 1.02, cy + math.sin(a) * r * 1.02,
                         cx + math.cos(a) * r * 1.22, cy + math.sin(a) * r * 1.22, iron))
        segs.append((cx - r * 0.3, cy, cx + r * 0.3, cy, iron))   # axle
        segs.append((cx, cy - r * 0.3, cx, cy + r * 0.3, iron))
    return segs, _bbox(segs)


def stately(text, x, y, h, ink=(66, 88, 118), shadow=(38, 50, 70), seed=0):
    """Qeynos: bannered serif caps with a drop shadow -- the crown city."""
    letters = _emit(text, x, y, h, tracking=17, seed=seed)
    body = _lines(letters, ink)
    segs = _offset(body, h * 0.045, h * 0.045, shadow) + body
    t = h * 0.09
    for (ex, ey), (tx, ty) in _ends(letters):          # flat serifs
        if abs(tx - ex) < abs(ty - ey):                # vertical-ish strokes only
            segs.append((ex - t, ey, ex + t, ey, ink))
    return segs, _bbox(segs)


def refined(text, x, y, h, ink=(96, 116, 148), pale=(150, 166, 190), seed=0):
    """Erudin: thin scholarly caps, wide-tracked, ruled above and below."""
    letters = _emit(text, x, y, h, tracking=30, seed=seed)
    segs = _lines(letters, ink)
    x0, y0, x1, y1 = _bbox(segs)
    m = h * 0.28
    for yy in (y0 - m * 0.6, y + m * 0.6):             # over/underline rules
        segs.append((x0 - m, yy, x1 + m, yy, pale))
    d = h * 0.09                                       # diamond finials
    for xx in (x0 - m * 1.9, x1 + m * 1.9):
        yy = (y0 + y) / 2
        segs += [(xx, yy - d, xx + d, yy, ink), (xx + d, yy, xx, yy + d, ink),
                 (xx, yy + d, xx - d, yy, ink), (xx - d, yy, xx, yy - d, ink)]
    return segs, _bbox(segs)


def sylvan(text, x, y, h, ink=(66, 104, 54), bark=(104, 78, 48), seed=0):
    """Surefall Glade: forest caps sprouting leaves at their tips."""
    letters = _emit(text, x, y, h, tracking=18, seed=seed)
    body = _lines(letters, ink)
    segs = _offset(body, h * 0.03, h * 0.03, bark) + body
    rng = random.Random(seed + 1)
    tips = [(p, q) for (p, q) in _ends(letters) if p[1] < y - h * 0.7]
    for (ex, ey), _ in tips:                           # leaves at cap-height tips
        if rng.random() < 0.45:
            continue
        s = h * 0.17
        segs += [(ex, ey, ex + s * 0.55, ey - s, ink),
                 (ex + s * 0.55, ey - s, ex + s * 1.1, ey - s * 0.35, ink),
                 (ex + s * 1.1, ey - s * 0.35, ex, ey, ink),
                 (ex, ey, ex + s * 0.55, ey - s * 0.5, ink)]    # midrib
    return segs, _bbox(segs)


STYLES = {
    "extruded": extruded, "small_caps": small_caps, "runic": runic,
    "crude": crude, "darkelf": darkelf, "highelf": highelf, "rounded": rounded,
    "clockwork": clockwork, "stately": stately, "refined": refined, "sylvan": sylvan,
}


def render(style, text, x, y, h, **kw):
    return STYLES[style](text, x, y, h, **kw)


if __name__ == "__main__":
    for name in STYLES:
        segs, bb = render(name, "AK'ANON QEYNOS", 0, 0, 100)
        print("%-10s %4d strokes  bbox %s" % (name, len(segs),
              " ".join("%.0f" % v for v in bb)))
