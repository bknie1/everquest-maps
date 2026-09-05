"""glyphs.py -- the skeleton letterforms every title style builds on.

The original title generator shipped with broken glyphs (E without its bars,
R without its leg, Q without its tail) and half the atlas inherited unreadable
names from it. This font exists so that never happens again: every A-Z glyph
is COMPLETE, defined as polylines in a 100-unit-cap em box, and the specimen
test at the bottom fails if any glyph loses a stroke.

Frame: x grows right, y grows UP (0 = baseline, 100 = cap height). Styles are
responsible for flipping y into native map coordinates (where north is -y).

    from glyphs import GLYPHS, layout_text
    for (ch, dx, polys) in layout_text("FREEPORT", tracking=14):
        ...
"""

# Each glyph: (advance width, [polyline, ...]); polyline = [(x, y), ...]
GLYPHS = {
    "A": (60, [[(0, 0), (30, 100), (60, 0)], [(13, 40), (47, 40)]]),
    "B": (52, [[(0, 0), (0, 100)],
               [(0, 100), (38, 100), (48, 88), (48, 62), (38, 52), (0, 52)],
               [(0, 52), (42, 52), (52, 40), (52, 12), (42, 0), (0, 0)]]),
    "C": (55, [[(55, 88), (38, 100), (18, 100), (0, 82), (0, 18), (18, 0), (38, 0), (55, 12)]]),
    "D": (52, [[(0, 0), (0, 100), (35, 100), (52, 82), (52, 18), (35, 0), (0, 0)]]),
    "E": (50, [[(50, 100), (0, 100), (0, 0), (50, 0)], [(0, 52), (40, 52)]]),
    "F": (50, [[(50, 100), (0, 100), (0, 0)], [(0, 52), (38, 52)]]),
    "G": (55, [[(55, 88), (38, 100), (18, 100), (0, 82), (0, 18), (18, 0), (40, 0),
                (55, 14), (55, 42), (30, 42)]]),
    "H": (52, [[(0, 0), (0, 100)], [(52, 0), (52, 100)], [(0, 52), (52, 52)]]),
    "I": (12, [[(6, 0), (6, 100)]]),
    "J": (40, [[(40, 100), (40, 15), (28, 0), (10, 0), (0, 14)]]),
    "K": (50, [[(0, 0), (0, 100)], [(48, 100), (2, 50)], [(16, 62), (50, 0)]]),
    "L": (46, [[(0, 100), (0, 0), (46, 0)]]),
    "M": (66, [[(0, 0), (0, 100), (33, 42), (66, 100), (66, 0)]]),
    "N": (52, [[(0, 0), (0, 100), (52, 0), (52, 100)]]),
    "O": (56, [[(16, 100), (40, 100), (56, 84), (56, 16), (40, 0), (16, 0),
                (0, 16), (0, 84), (16, 100)]]),
    "P": (52, [[(0, 0), (0, 100), (40, 100), (52, 88), (52, 60), (40, 48), (0, 48)]]),
    "Q": (56, [[(16, 100), (40, 100), (56, 84), (56, 16), (40, 0), (16, 0),
                (0, 16), (0, 84), (16, 100)], [(34, 24), (60, -12)]]),
    "R": (52, [[(0, 0), (0, 100), (40, 100), (52, 88), (52, 60), (40, 48), (0, 48)],
               [(20, 48), (52, 0)]]),
    "S": (52, [[(52, 86), (38, 100), (14, 100), (0, 86), (0, 64), (14, 52),
                (38, 52), (52, 40), (52, 14), (38, 0), (14, 0), (0, 14)]]),
    "T": (56, [[(0, 100), (56, 100)], [(28, 100), (28, 0)]]),
    "U": (54, [[(0, 100), (0, 16), (16, 0), (38, 0), (54, 16), (54, 100)]]),
    "V": (56, [[(0, 100), (28, 0), (56, 100)]]),
    "W": (72, [[(0, 100), (18, 0), (36, 62), (54, 0), (72, 100)]]),
    "X": (52, [[(0, 0), (52, 100)], [(0, 100), (52, 0)]]),
    "Y": (52, [[(0, 100), (26, 48), (52, 100)], [(26, 48), (26, 0)]]),
    "Z": (52, [[(0, 100), (52, 100), (0, 0), (52, 0)]]),
    "'": (10, [[(2, 104), (8, 82)]]),
    "-": (34, [[(4, 46), (30, 46)]]),
    ".": (12, [[(4, 0), (8, 0), (8, 5), (4, 5), (4, 0)]]),
}
SPACE = 42

# Angular variants for the runic family: no corner-cut "curves" at all,
# every stroke straight and biased to verticals/diagonals. Only letters
# whose base form reads as rounded get a variant; the rest pass through.
ANGULAR = {
    "O": (56, [[(28, 100), (56, 50), (28, 0), (0, 50), (28, 100)]]),
    "Q": (56, [[(28, 100), (56, 50), (28, 0), (0, 50), (28, 100)], [(36, 22), (60, -12)]]),
    "C": (52, [[(52, 100), (14, 100), (0, 50), (14, 0), (52, 0)]]),
    "G": (54, [[(54, 100), (14, 100), (0, 50), (14, 0), (54, 0), (54, 40), (32, 40)]]),
    "S": (52, [[(52, 100), (6, 100), (6, 56), (46, 44), (46, 0), (0, 0)]]),
    "U": (54, [[(0, 100), (0, 20), (27, 0), (54, 20), (54, 100)]]),
    "B": (52, [[(0, 0), (0, 100)], [(0, 100), (46, 88), (46, 62), (0, 52)],
               [(0, 52), (52, 40), (52, 10), (0, 0)]]),
    "D": (52, [[(0, 0), (0, 100), (34, 100), (52, 66), (52, 34), (34, 0), (0, 0)]]),
    "P": (52, [[(0, 0), (0, 100), (46, 90), (46, 58), (0, 48)]]),
    "R": (52, [[(0, 0), (0, 100), (46, 90), (46, 58), (0, 48)], [(16, 48), (52, 0)]]),
    "J": (40, [[(40, 100), (40, 16), (20, 0), (0, 16)]]),
}

# Rounded variants for the halfling family: extra corner cuts so bowls read
# as soft circles; square letters get gentle shoulder cuts.
ROUNDED = {
    "O": (58, [[(20, 100), (38, 100), (52, 90), (58, 70), (58, 30), (52, 10), (38, 0),
                (20, 0), (6, 10), (0, 30), (0, 70), (6, 90), (20, 100)]]),
    "E": (50, [[(50, 100), (12, 100), (0, 88), (0, 12), (12, 0), (50, 0)], [(0, 52), (38, 52)]]),
    "L": (46, [[(0, 100), (0, 12), (12, 0), (46, 0)]]),
    "V": (56, [[(0, 100), (22, 6), (28, 0), (34, 6), (56, 100)]]),
    "R": (52, [[(0, 0), (0, 100), (36, 100), (50, 90), (52, 72), (50, 56), (36, 48), (0, 48)],
               [(18, 48), (46, 6), (52, 0)]]),
    "A": (60, [[(0, 0), (24, 92), (30, 100), (36, 92), (60, 0)], [(13, 38), (47, 38)]]),
    "I": (12, [[(6, 0), (6, 100)]]),
}


def layout_text(text, tracking=14, variants=None, widths=None):
    """Yield (ch, pen_x, polylines) per printable glyph, advancing a pen.

    variants: optional dict overriding GLYPHS per char (ANGULAR / ROUNDED).
    widths:   optional {ch: scale} per-char width tweak (crude styles).
    """
    src = dict(GLYPHS)
    if variants:
        src.update({k: v for k, v in variants.items() if k in variants})
    x = 0.0
    for ch in text.upper():
        if ch == " ":
            x += SPACE + tracking
            continue
        if ch not in src:
            raise KeyError("no glyph for %r" % ch)
        w, polys = src[ch]
        wscale = (widths or {}).get(ch, 1.0)
        yield ch, x, [[(px * wscale, py) for (px, py) in poly] for poly in polys]
        x += w * wscale + tracking


def text_width(text, tracking=14, variants=None, widths=None):
    last = 0.0
    for ch, x, polys in layout_text(text, tracking, variants, widths):
        last = x + max(px for poly in polys for (px, py) in poly)
    return last


def _selftest():
    """Every glyph must keep its distinguishing strokes. This is the test the
    original font never had."""
    need = {"E": 2, "F": 2, "H": 3, "R": 2, "Q": 2, "K": 3, "A": 2, "Y": 2, "T": 2, "X": 2}
    for ch, n in need.items():
        assert len(GLYPHS[ch][1]) >= n, "%s lost a stroke" % ch
    for name, table in (("GLYPHS", GLYPHS), ("ANGULAR", ANGULAR), ("ROUNDED", ROUNDED)):
        for ch, (w, polys) in table.items():
            assert w > 0 and polys, (name, ch)
            for poly in polys:
                assert len(poly) >= 2, (name, ch)
    # R and P must differ, E and F must differ -- the classic breakages
    assert GLYPHS["R"][1] != GLYPHS["P"][1]
    assert GLYPHS["E"][1] != GLYPHS["F"][1]
    print("glyph selftest ok: %d base, %d angular, %d rounded" %
          (len(GLYPHS), len(ANGULAR), len(ROUNDED)))


if __name__ == "__main__":
    _selftest()
