"""freeport_decor.py -- Freeport (Ottoman/Dornish mercantile port) motif shapes.

Caravels for the harbor, dockside anchor and rope coil, striped awning stalls,
and the minaret/dome skyline for the margins. Built to the BRAIN section-9 bar:
hatched fill via even-odd scanline, tapered two-edge forms, a shadow side, and
real internal structure -- planking, rigging, awning stripes -- not wireframes.

Colour directive: no pale yellows; warm accents stay in the dark bronze
(130, 82, 12) family, canvas leans grey-parchment, never lemon.

Every shape returns [(x1, y1, x2, y2, ink)] in map coordinates (y downward).
"""
import math

PALETTE = {
    # (116,88,56) is claimed by validate_overlay's FAUNA set -- shifted 2 points
    # so water-legitimate ships are not stripped by the flora/fauna water check.
    'hull':      (118, 90, 54),
    'hull_dark': (78, 58, 38),
    'canvas':    (204, 194, 172),
    'canvas_sh': (164, 152, 128),
    'bronze':    (130, 82, 12),
    'flag':      (155, 48, 36),
    'rope':      (140, 116, 82),
    'ripple':    (72, 118, 168),
    'stone':     (176, 150, 104),
    'stone_dark': (140, 116, 78),
}


def _hatch(poly, ink, step):
    """Fill a polygon with horizontal hatching (even-odd scanline)."""
    ys = [p[1] for p in poly]
    out = []
    y = min(ys) + step * 0.5
    while y < max(ys):
        xs = []
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            if (y1 > y) != (y2 > y):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.6:
                out.append((xs[i], y, xs[i + 1], y, ink))
        y += step
    return out


def _poly(out, pts, ink, close=False):
    for i in range(len(pts) - 1):
        out.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], ink))
    if close:
        out.append((pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], ink))


def caravel(cx, cy, r, seed=0, flip=False):
    """A two-masted caravel seen in profile: hatched hull with planking and a
    dark shadow strake, raked masts, a full mainsail and a lateen mizzen,
    rigging, a bronze pennant, and ripples under the keel.

    (cx, cy) is the waterline midpoint; the ship spans about 2.2*r wide and
    1.7*r above the waterline. flip mirrors the heading.
    """
    P = PALETTE
    out = []
    f = -1.0 if flip else 1.0

    def X(dx):
        return cx + f * dx * r

    def Y(dy):
        return cy + dy * r

    # --- hull: sheer line bow->stern, tapered, with tuck at both ends
    deck = [(X(-1.10), Y(-0.30)), (X(-0.60), Y(-0.20)), (X(0.20), Y(-0.16)),
            (X(0.80), Y(-0.24)), (X(1.05), Y(-0.40))]
    keel = [(X(-0.88), Y(0.16)), (X(-0.30), Y(0.26)), (X(0.35), Y(0.26)),
            (X(0.82), Y(0.12))]
    hull_poly = deck + list(reversed(keel))
    _poly(out, deck, P['hull'])
    _poly(out, keel, P['hull_dark'])
    out.append((deck[0][0], deck[0][1], keel[0][0], keel[0][1], P['hull']))
    out.append((deck[-1][0], deck[-1][1], keel[-1][0], keel[-1][1], P['hull']))
    # hull fill + planking
    out += _hatch(hull_poly, P['hull'], r * 0.11)
    # shadow strake along the waterline (lower third reads dark)
    out += _hatch([(X(-0.92), Y(0.02)), (X(0.88), Y(0.02)),
                   (X(0.82), Y(0.16)), (X(-0.86), Y(0.16))],
                  P['hull_dark'], r * 0.07)
    # gunwale rub line
    out.append((X(-1.00), Y(-0.22), X(0.95), Y(-0.24), P['hull_dark']))
    # bowsprit
    out.append((X(1.02), Y(-0.38), X(1.45), Y(-0.62), P['hull']))

    # --- masts (slight rake aft)
    out.append((X(0.28), Y(-0.16), X(0.16), Y(-1.62), P['hull_dark']))   # main
    out.append((X(-0.62), Y(-0.20), X(-0.70), Y(-1.18), P['hull_dark']))  # mizzen

    # --- mainsail: full square course, curved foot, hatched shade on the lee edge
    main = [(X(0.66), Y(-1.44)), (X(0.70), Y(-0.52)), (X(0.30), Y(-0.38)),
            (X(-0.24), Y(-0.48)), (X(-0.28), Y(-1.38)), (X(0.20), Y(-1.52))]
    _poly(out, main, P['canvas'], close=True)
    out += _hatch([main[0], main[1], (X(0.42), Y(-0.46)), (X(0.36), Y(-1.48))],
                  P['canvas_sh'], r * 0.10)
    # billow lines
    out.append((X(-0.16), Y(-1.20), X(0.52), Y(-1.26), P['canvas_sh']))
    out.append((X(-0.20), Y(-0.86), X(0.56), Y(-0.92), P['canvas_sh']))
    # main yard
    out.append((X(-0.30), Y(-1.42), X(0.68), Y(-1.48), P['hull_dark']))

    # --- mizzen: lateen triangle on a long angled yard
    out.append((X(-1.22), Y(-0.62), X(-0.30), Y(-1.30), P['hull_dark']))  # yard
    lateen = [(X(-1.18), Y(-0.60)), (X(-0.34), Y(-1.24)), (X(-0.40), Y(-0.36))]
    _poly(out, lateen, P['canvas'], close=True)
    out += _hatch(lateen, P['canvas_sh'], r * 0.13)

    # --- rigging
    out.append((X(0.16), Y(-1.60), X(1.40), Y(-0.60), P['rope']))   # forestay
    out.append((X(0.16), Y(-1.60), X(-0.66), Y(-1.14), P['rope']))  # triatic
    out.append((X(0.70), Y(-0.50), X(0.90), Y(-0.26), P['rope']))   # main sheet

    # --- bronze pennant at the masthead
    out.append((X(0.16), Y(-1.62), X(0.44), Y(-1.56), P['flag']))
    out.append((X(0.44), Y(-1.56), X(0.18), Y(-1.50), P['flag']))
    out.append((X(0.18), Y(-1.56), X(0.34), Y(-1.54), P['flag']))

    # --- ripples under the keel
    for k, (dx0, dx1, dy) in enumerate(((-1.05, -0.55, 0.30), (-0.15, 0.55, 0.34),
                                        (0.70, 1.15, 0.28))):
        out.append((X(dx0), Y(dy), X(dx1), Y(dy), P['ripple']))
    return out


def anchor(cx, cy, r, seed=0):
    """A dockside anchor leaning on its stock, hatched flukes, with a ring."""
    P = PALETTE
    out = []
    # shank
    out.append((cx - r * 0.04, cy - r * 0.95, cx, cy + r * 0.72, P['hull_dark']))
    out.append((cx + r * 0.06, cy - r * 0.93, cx + r * 0.09, cy + r * 0.70, P['hull_dark']))
    # ring
    n = 10
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = 2 * math.pi * (i + 1) / n
        out.append((cx + r * 0.14 * math.cos(a0), cy - r * 1.06 + r * 0.14 * math.sin(a0),
                    cx + r * 0.14 * math.cos(a1), cy - r * 1.06 + r * 0.14 * math.sin(a1),
                    P['bronze']))
    # stock (crossbar, slightly tilted)
    out.append((cx - r * 0.52, cy - r * 0.66, cx + r * 0.56, cy - r * 0.74, P['hull']))
    out.append((cx - r * 0.52, cy - r * 0.60, cx + r * 0.56, cy - r * 0.68, P['hull']))
    # arms: sweep to both flukes
    arm = [(cx + r * 0.02, cy + r * 0.72), (cx - r * 0.46, cy + r * 0.52),
           (cx - r * 0.66, cy + r * 0.12)]
    _poly(out, arm, P['hull_dark'])
    arm2 = [(cx + r * 0.06, cy + r * 0.72), (cx + r * 0.54, cy + r * 0.50),
            (cx + r * 0.72, cy + r * 0.10)]
    _poly(out, arm2, P['hull_dark'])
    # flukes (hatched triangles)
    fl = [(cx - r * 0.66, cy + r * 0.12), (cx - r * 0.88, cy + r * 0.40),
          (cx - r * 0.50, cy + r * 0.44)]
    _poly(out, fl, P['hull_dark'], close=True)
    out += _hatch(fl, P['hull'], r * 0.08)
    fr = [(cx + r * 0.72, cy + r * 0.10), (cx + r * 0.94, cy + r * 0.36),
          (cx + r * 0.56, cy + r * 0.42), ]
    _poly(out, fr, P['hull_dark'], close=True)
    out += _hatch(fr, P['hull'], r * 0.08)
    return out


def rope_coil(cx, cy, r, seed=0):
    """A coiled mooring line: nested ellipse arcs with a trailing tail."""
    P = PALETTE
    out = []
    for ring in range(3):
        rr = r * (0.35 + 0.28 * ring)
        n = 14
        for i in range(n):
            a0 = 2 * math.pi * i / n
            a1 = 2 * math.pi * (i + 1) / n
            out.append((cx + rr * math.cos(a0), cy + rr * 0.55 * math.sin(a0),
                        cx + rr * math.cos(a1), cy + rr * 0.55 * math.sin(a1),
                        P['rope'] if ring % 2 == 0 else P['hull']))
    # tail running off the coil
    tail = [(cx + r * 0.92, cy + r * 0.18), (cx + r * 1.35, cy + r * 0.34),
            (cx + r * 1.70, cy + r * 0.28)]
    _poly(out, tail, P['rope'])
    tail2 = [(cx + r * 0.92, cy + r * 0.24), (cx + r * 1.33, cy + r * 0.40),
             (cx + r * 1.68, cy + r * 0.34)]
    _poly(out, tail2, P['hull'])
    return out


def awning_stall(cx, cy, r, seed=0):
    """A market stall under a striped awning: posts, counter, crate, and
    alternating dark-red / canvas awning panels with a scalloped hem."""
    P = PALETTE
    out = []
    # posts
    out.append((cx - r * 0.85, cy, cx - r * 0.85, cy - r * 0.95, P['hull']))
    out.append((cx + r * 0.85, cy, cx + r * 0.85, cy - r * 0.95, P['hull']))
    out.append((cx - r * 0.80, cy, cx - r * 0.80, cy - r * 0.92, P['hull_dark']))
    # counter (hatched slab)
    counter = [(cx - r * 0.85, cy - r * 0.34), (cx + r * 0.85, cy - r * 0.34),
               (cx + r * 0.85, cy - r * 0.16), (cx - r * 0.85, cy - r * 0.16)]
    _poly(out, counter, P['hull'], close=True)
    out += _hatch(counter, P['hull'], r * 0.09)
    # awning: sloped panel with stripes
    n = 5
    for k in range(n):
        x0 = cx - r * 1.0 + 2.0 * r * k / n
        x1 = cx - r * 1.0 + 2.0 * r * (k + 1) / n
        ink = P['flag'] if k % 2 == 0 else P['canvas']
        panel = [(x0, cy - r * 0.95), (x1, cy - r * 0.95),
                 (x1 + r * 0.10, cy - r * 1.20), (x0 + r * 0.10, cy - r * 1.20)]
        _poly(out, panel, ink, close=True)
        out += _hatch(panel, ink, r * 0.10)
        # scalloped hem
        out.append((x0, cy - r * 0.95, (x0 + x1) / 2, cy - r * 0.88, ink))
        out.append(((x0 + x1) / 2, cy - r * 0.88, x1, cy - r * 0.95, ink))
    # crate beside the stall
    crate = [(cx + r * 0.95, cy), (cx + r * 1.35, cy),
             (cx + r * 1.35, cy - r * 0.38), (cx + r * 0.95, cy - r * 0.38)]
    _poly(out, crate, P['hull_dark'], close=True)
    out.append((cx + r * 0.95, cy - r * 0.19, cx + r * 1.35, cy - r * 0.19, P['hull_dark']))
    out.append((cx + r * 1.05, cy, cx + r * 1.05, cy - r * 0.38, P['hull_dark']))
    return out


def minaret_tower(cx, cy, r, seed=0):
    """A slender minaret: tapered hatched shaft, balcony ring, onion cap and
    bronze finial. (cx, cy) is the base midpoint; rises ~2.4*r."""
    P = PALETTE
    out = []
    shaft = [(cx - r * 0.20, cy), (cx - r * 0.12, cy - r * 1.70),
             (cx + r * 0.12, cy - r * 1.70), (cx + r * 0.20, cy)]
    _poly(out, shaft, P['stone'], close=True)
    out += _hatch(shaft, P['stone'], r * 0.16)
    # shadow edge on the right
    out.append((cx + r * 0.16, cy - r * 0.10, cx + r * 0.10, cy - r * 1.68, P['stone_dark']))
    # balcony
    out.append((cx - r * 0.28, cy - r * 1.70, cx + r * 0.28, cy - r * 1.70, P['stone_dark']))
    out.append((cx - r * 0.24, cy - r * 1.80, cx + r * 0.24, cy - r * 1.80, P['stone_dark']))
    out.append((cx - r * 0.28, cy - r * 1.70, cx - r * 0.24, cy - r * 1.80, P['stone_dark']))
    out.append((cx + r * 0.28, cy - r * 1.70, cx + r * 0.24, cy - r * 1.80, P['stone_dark']))
    # cap: onion profile
    cap = [(cx - r * 0.22, cy - r * 1.80), (cx - r * 0.16, cy - r * 2.10),
           (cx, cy - r * 2.30), (cx + r * 0.16, cy - r * 2.10),
           (cx + r * 0.22, cy - r * 1.80)]
    _poly(out, cap, P['stone_dark'])
    out += _hatch(cap + [(cx - r * 0.22, cy - r * 1.80)], P['stone_dark'], r * 0.10)
    # bronze finial
    out.append((cx, cy - r * 2.30, cx, cy - r * 2.48, P['bronze']))
    out.append((cx - r * 0.05, cy - r * 2.40, cx + r * 0.05, cy - r * 2.40, P['bronze']))
    return out


def dome_roof(cx, cy, r, seed=0):
    """A ribbed dome on a low drum block -- the mercantile skyline glyph."""
    P = PALETTE
    out = []
    # drum
    drum = [(cx - r * 0.85, cy), (cx + r * 0.85, cy),
            (cx + r * 0.85, cy - r * 0.35), (cx - r * 0.85, cy - r * 0.35)]
    _poly(out, drum, P['stone'], close=True)
    out += _hatch(drum, P['stone'], r * 0.12)
    # dome: half-ellipse of chords
    n = 12
    pts = []
    for i in range(n + 1):
        a = math.pi * i / n
        pts.append((cx - r * 0.80 * math.cos(a),
                    cy - r * 0.35 - r * 0.72 * math.sin(a)))
    _poly(out, pts, P['stone_dark'])
    # ribs
    for fx in (-0.45, 0.0, 0.45):
        a = math.acos(max(-1.0, min(1.0, -fx / 0.80)))
        out.append((cx + fx * r, cy - r * 0.35,
                    cx + fx * r * 0.25, cy - r * 0.35 - r * 0.70,
                    P['stone_dark']))
    # shade the right flank of the dome
    out += _hatch([(cx + r * 0.30, cy - r * 0.35), (cx + r * 0.78, cy - r * 0.35),
                   (cx + r * 0.40, cy - r * 0.95), (cx + r * 0.16, cy - r * 1.02)],
                  P['stone_dark'], r * 0.10)
    # bronze crescent-tip finial
    out.append((cx, cy - r * 1.07, cx, cy - r * 1.22, P['bronze']))
    return out


def crescent_standard(cx, cy, r, seed=0):
    """A hanging market standard: pole, crossbar, swallowtail pennant with a
    hatched red fill, bronze crescent finial. Replaces the wireframe banner,
    which read as lettering at map scale."""
    P = PALETTE
    out = []
    # pole (two strokes for weight)
    out.append((cx, cy, cx, cy - r * 2.00, P['stone_dark']))
    out.append((cx + r * 0.05, cy, cx + r * 0.05, cy - r * 1.96, P['stone_dark']))
    # crossbar with drop cords
    out.append((cx - r * 0.52, cy - r * 1.74, cx + r * 0.56, cy - r * 1.78, P['stone_dark']))
    out.append((cx - r * 0.46, cy - r * 1.74, cx - r * 0.46, cy - r * 1.66, P['stone_dark']))
    out.append((cx + r * 0.48, cy - r * 1.77, cx + r * 0.48, cy - r * 1.69, P['stone_dark']))
    # swallowtail pennant, outlined and hatched
    pen = [(cx - r * 0.46, cy - r * 1.66), (cx + r * 0.48, cy - r * 1.69),
           (cx + r * 0.46, cy - r * 0.92), (cx + r * 0.01, cy - r * 1.12),
           (cx - r * 0.44, cy - r * 0.90)]
    _poly(out, pen, P['flag'], close=True)
    out += _hatch(pen, P['flag'], r * 0.10)
    # bronze crescent finial
    n = 6
    for i in range(n):
        a0 = math.pi * (0.15 + 0.85 * i / n)
        a1 = math.pi * (0.15 + 0.85 * (i + 1) / n)
        out.append((cx + r * 0.12 * math.cos(a0), cy - r * 2.10 + r * 0.12 * math.sin(a0) * -1,
                    cx + r * 0.12 * math.cos(a1), cy - r * 2.10 + r * 0.12 * math.sin(a1) * -1,
                    P['bronze']))
    return out


def sand_sweep(x0, y0, x1, y1, ink=None, bow=0.06, seed=0):
    """A long dashed ground sweep: one lazy arc drawn as spaced dashes.
    Ground accent for the margins -- fewer, longer, stylized strokes."""
    ink = ink or PALETTE['bronze']
    out = []
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    if L < 1:
        return out
    px, py = -dy / L, dx / L                 # perpendicular bow
    mx = (x0 + x1) / 2 + px * L * bow
    my = (y0 + y1) / 2 + py * L * bow
    n = 7                                    # dashes: fewer, longer
    for k in range(0, n, 2):
        u0, u1 = k / n, (k + 0.78) / n
        pts = []
        for u in (u0, u1):
            a, b, c = (1 - u) ** 2, 2 * (1 - u) * u, u ** 2
            pts.append((a * x0 + b * mx + c * x1, a * y0 + b * my + c * y1))
        out.append((pts[0][0], pts[0][1], pts[1][0], pts[1][1], ink))
    return out


SHAPES = {
    'caravel': caravel,
    'anchor': anchor,
    'rope_coil': rope_coil,
    'awning_stall': awning_stall,
    'minaret_tower': minaret_tower,
    'dome_roof': dome_roof,
    'sand_sweep': sand_sweep,
}
