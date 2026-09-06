"""scale_title.py -- shrink a clipped title IN PLACE until it fits the frame.

!! READ BEFORE USING (2026-09-05 postmortem): every one of the 15 clipped
flags the meter raised proved to be a FALSE POSITIVE -- band decor (border
waves, ridge sketches, corner hatches, margin trees) shares inks and lengths
with letters and stretched the measured bbox. This tool scaled 12 innocent
titles and tore two (felwitheb, neriakb) before band plots told the truth.
Before EVER running it with --write: plot the band, and classify the strokes
that actually cross frame+-60 by ink and length. If they are not letter
strokes, fix nothing. Stick-font letters split into DISCONNECTED strokes
(crossbars never touch stems), so no component analysis can move a glyph as
a unit -- a genuine clip fix must select by row-window + explicit ink probe,
verified visually, per zone.

Doctrine (docs/TITLES.md campaign + stylized-titles rule): a clipped title is
never redrawn in stick font; it is the zone's styled original, scaled about
its own center until it sits inside the frame. Letterforms, inks, spacing all
survive -- only the size changes, and only by the minimum needed.

v2, after the felwitheb lesson: selection is COMPONENT-based via the city
slate campaign's letter_components() (src/titles/apply_title.py) -- whole
connected components scale or stay, so nothing can tear, and canopy hexagons
/ figures / texture are rejected by the campaign's shape gates (median
stroke length, size window, closed-loop test). Per-zone detector overrides
in apply_title.ZONES are honored. Long horizontal rules riding the letters'
strip (title underlines) scale with them.

The v1 bbox+ink selection dragged partial trees into felwitheb's band --
1,529 strokes scaled where ~500 were title. Never select by bbox alone when
letters share decor ink.

    python src/tools/scale_title.py <zone> [--pad 25] [--write]
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(ROOT, "src", "kit"), os.path.join(ROOT, "src", "titles")):
    sys.path.insert(0, p)

from fix_title import content_bbox  # noqa: E402
from layout import layout  # noqa: E402
from apply_title import ZONES, letter_components, components, slen  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"


def adaptive_letters(band):
    """letter_components with gates derived from the band's own letters.

    The campaign gates assume city-slate letter sizes (h 26-115); the big
    stick titles (soldung trio h~500) blow past max_h and tiny decor slips
    in instead. Here: components of medium strokes, letter row = the tallest
    stroke-sparse components, gates scaled to that height.
    """
    skip = {i for i, s in enumerate(band) if slen(s) > 150 or slen(s) < 8}
    comps = components(band, skip=skip)
    stats = []
    for idx in comps:
        segs = [band[i] for i in idx]
        xs = [v for s in segs for v in (s[0], s[2])]
        ys = [v for s in segs for v in (s[1], s[3])]
        lens = sorted(slen(s) for s in segs)
        stats.append((idx, max(xs) - min(xs), max(ys) - min(ys),
                      (min(ys) + max(ys)) / 2, lens[len(lens) // 2]))
    pool = [c for c in stats if c[4] > 12 and c[2] > 25]
    if not pool:
        return set()
    hl = max(c[2] for c in pool)
    row = sorted(c[3] for c in pool if c[2] > 0.5 * hl)
    row_y = row[len(row) // 2]
    out = []
    for idx, w, h, yc, med in pool:
        if not (0.28 * hl <= h <= 1.25 * hl and w <= 2.2 * hl):
            continue
        if abs(yc - row_y) > hl:
            continue
        # closed single loop with landscape aspect = canopy blob, not a letter
        deg = {}
        for i in idx:
            s = band[i]
            for p in ((round(s[0]), round(s[1])), (round(s[2]), round(s[3]))):
                deg[p] = deg.get(p, 0) + 1
        closed = deg and all(v == 2 for v in deg.values())
        if closed and not (h >= 30 and h > w * 1.05):
            continue
        out.append((idx, (min(v for i in idx for v in (band[i][0], band[i][2])),
                          max(v for i in idx for v in (band[i][0], band[i][2])))))
    # flanker trim: letters pack tight (gaps << letter height); an edge
    # component separated from the letter mass by more than 1.2*HL is a
    # decorative flourish riding the row (RIVERVALE's vines), not a letter.
    out.sort(key=lambda c: c[1][0])
    while len(out) > 2 and out[1][1][0] - out[0][1][1] > 1.2 * hl:
        out.pop(0)
    while len(out) > 2 and out[-1][1][0] - out[-2][1][1] > 1.2 * hl:
        out.pop()
    picked = set()
    for idx, _ in out:
        picked.update(idx)
    return picked


def pick_letters(zone, band):
    """Letter stroke indices for a zone's band. One code path for the whole
    pack: adaptive gates derived from the band's own letter row. Per-zone
    ZONES det overrides apply where the campaign recorded one (they encode
    shared-ink lessons the adaptive gates can't know).

    NOTE: ZONES cfg['inks'] are the inks of the OLD titles the slate
    campaign REMOVED -- never select by them; the current styled titles use
    the styles.py family inks. (Tried once: zero strokes matched and the
    empty pick silently skipped the clip check.)

    Adoption pass: the detectors skip tiny serifs (<8u) and
    long swashes (>150u) from their graph, which once left orphan ticks
    behind when their letter scaled (the neriakb tear). Every full component
    -- welded at true distance <=0.7u, immune to snap-grid boundaries --
    that is majority-picked joins wholesale; minority-picked components drop
    out entirely. Nothing can tear."""
    cfg = ZONES.get(zone, {})
    if "det" in cfg:
        picked = letter_components(band, **cfg["det"])
    else:
        picked = adaptive_letters(band)
    if not picked:
        return picked
    # weld full components at true distance (grid + neighbor cells)
    from collections import defaultdict
    parent = list(range(len(band)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    grid = defaultdict(list)
    for i, s in enumerate(band):
        for p in ((s[0], s[1]), (s[2], s[3])):
            grid[(int(p[0]), int(p[1]))].append((i, p))
    for (gx, gy), mem in grid.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j, q in grid.get((gx + dx, gy + dy), []) if (dx, dy) != (0, 0) else []:
                    for i, p in mem:
                        if abs(p[0] - q[0]) <= 0.7 and abs(p[1] - q[1]) <= 0.7:
                            a, b = find(i), find(j)
                            if a != b:
                                parent[a] = b
        for k in range(1, len(mem)):
            a, b = find(mem[0][0]), find(mem[k][0])
            if a != b:
                parent[a] = b
    full = defaultdict(list)
    for i in range(len(band)):
        full[find(i)].append(i)
    out = set()
    for idx in full.values():
        n = sum(1 for i in idx if i in picked)
        if n and n * 2 >= len(idx):
            out.update(idx)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--pad", type=float, default=25.0)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    lo = layout(content_bbox(a.zone))
    gy0 = lo["grid"][2]
    fx0, fx1 = lo["frame"][0], lo["frame"][1]

    path = os.path.join(MAPS, a.zone + "_2.txt")
    lines = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines()
             if l.strip()]
    band_idx, band = [], []
    parsed = {}
    for i, l in enumerate(lines):
        if l[:1] != "L":
            continue
        f = [v.strip() for v in l[2:].split(",")]
        if len(f) < 9:
            continue
        s = (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
             (f[6], f[7], f[8]))
        if (s[1] + s[3]) / 2 < gy0 + 40:
            band_idx.append(i)
            band.append(s)
            parsed[i] = [float(f[0]), float(f[1]), float(f[2]),
                         float(f[3]), float(f[4]), float(f[5]), f[6], f[7], f[8]]

    picked = pick_letters(a.zone, band)
    if not picked:
        print("%s: no letter components found" % a.zone)
        return
    inks = {band[i][4] for i in picked}
    xs = [v for i in picked for v in (band[i][0], band[i][2])]
    ys = [v for i in picked for v in (band[i][1], band[i][3])]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    # title underline rules: long near-horizontal strokes of a letter ink
    # riding the letters' strip
    rules = {i for i, s in enumerate(band)
             if slen(s) > 150 and abs(s[3] - s[1]) < 10 and s[4] in inks
             and by0 - 50 <= (s[1] + s[3]) / 2 <= by1 + 50}
    sel = set(picked) | rules
    xs = [v for i in sel for v in (band[i][0], band[i][2])]
    bx0, bx1 = min(xs), max(xs)

    avail = (fx1 - a.pad) - (fx0 + a.pad)
    width = bx1 - bx0
    s = min(1.0, avail / width) if width > 0 else 1.0
    cx = (bx0 + bx1) / 2
    cy = (by0 + by1) / 2
    ncx = min(max(cx, fx0 + a.pad + s * width / 2), fx1 - a.pad - s * width / 2)
    if s >= 0.999 and abs(ncx - cx) < 1:
        print("%s: fits already (width %.0f vs %.0f)" % (a.zone, width, avail))
        return

    for bi in sel:
        i = band_idx[bi]
        p = parsed[i]
        for k in (0, 3):
            p[k] = ncx + (p[k] - cx) * s
        for k in (1, 4):
            p[k] = cy + (p[k] - cy) * s
        lines[i] = ("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %s, %s, %s"
                    % (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))

    print("%s: scaled %d strokes (%d letters + %d rules) by %.3f "
          "(width %.0f -> %.0f), recenter %+.0f%s"
          % (a.zone, len(sel), len(picked), len(rules), s, width, width * s,
             ncx - cx, "  WRITTEN" if a.write else "  (dry run)"))
    if a.write:
        open(path, "w", newline="", encoding="utf-8").write(CRLF.join(lines) + CRLF)


if __name__ == "__main__":
    main()
