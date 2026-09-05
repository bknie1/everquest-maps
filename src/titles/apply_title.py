"""apply_title.py -- swap a zone's old title lettering for a styled family.

The campaign tool: removes the OLD letter strokes from the _2 band (by ink
where the zone has a letter ink, by connected-component shape analysis where
letters share their ink with decor), then composes the zone's new themed
title into the old letters' slot. Decor in the band is preserved.

    python src/titles/apply_title.py qeynos --dry-run    # plots only
    python src/titles/apply_title.py qeynos              # writes the _2

Shape analysis: strokes are chained into components on shared endpoints.
A component is LETTER-LIKE when it is tall enough to be a cap, narrow enough
to be one glyph, and its strokes are long (figures/trees/dash textures are
dense SHORT strokes; a stick glyph is a few LONG ones). Closed loops (canopy
hexagons, eyes) only count as letters when cap-height and taller than wide
(a stick-font O). After removal, any stray stroke whose midpoint falls in a
removed glyph's padded bbox goes too (two-tone highlights, shadows).
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "src", "tools"))
sys.path.insert(0, os.path.join(ROOT, "src", "kit"))

from styles import render, _bbox  # noqa: E402
from fix_title import parse, content_bbox  # noqa: E402
from layout import layout  # noqa: E402

MAPS = os.path.join(ROOT, "Emoda Legends Maps")
CRLF = "\r\n"


def slen(s):
    return math.hypot(s[2] - s[0], s[3] - s[1])


def components(segs, snap=0.6, skip=None):
    """Chain strokes into components on shared (rounded) endpoints.
    Strokes whose index is in `skip` stay out of the graph entirely (long
    rules would otherwise weld every letter they touch into one giant
    component; short texture dashes would weld the canopy to the caps)."""
    parent = list(range(len(segs)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    skip = skip or set()
    pts = {}
    for i, s in enumerate(segs):
        if i in skip:
            continue
        for p in ((round(s[0] / snap), round(s[1] / snap)),
                  (round(s[2] / snap), round(s[3] / snap))):
            if p in pts:
                a, b = find(pts[p]), find(i)
                parent[a] = b
            else:
                pts[p] = i
    comps = {}
    for i in range(len(segs)):
        if i not in skip:
            comps.setdefault(find(i), []).append(i)
    return list(comps.values())


def letter_components(band, min_h=26, max_h=115, max_w=135, min_med_len=9.0,
                      graph_min_len=0.0, x_frac=None, loop_any_aspect=False):
    """Indices of band strokes that belong to letter-like components."""
    skip = {i for i, s in enumerate(band) if slen(s) > 150 or slen(s) < graph_min_len}
    if x_frac:
        xs = [v for s in band for v in (s[0], s[2])]
        lo = min(xs) + (max(xs) - min(xs)) * x_frac[0]
        hi = min(xs) + (max(xs) - min(xs)) * x_frac[1]
    comps = components(band, skip=skip)
    out = set()
    for idx in comps:
        segs = [band[i] for i in idx]
        xs2 = [v for s in segs for v in (s[0], s[2])]
        ys = [v for s in segs for v in (s[1], s[3])]
        w, h = max(xs2) - min(xs2), max(ys) - min(ys)
        if not (min_h <= h <= max_h and w <= max_w):
            continue
        if x_frac and not (lo <= (min(xs2) + max(xs2)) / 2 <= hi):
            continue
        lens = sorted(slen(s) for s in segs)
        if lens[len(lens) // 2] < min_med_len:
            continue                                  # dense texture / figure
        # closed single loop (canopy hexagon, pond eye) vs a stick-font O:
        deg = {}
        for s in segs:
            for p in ((round(s[0]), round(s[1])), (round(s[2]), round(s[3]))):
                deg[p] = deg.get(p, 0) + 1
        closed = deg and all(v == 2 for v in deg.values())
        if closed and not loop_any_aspect and not (h >= 30 and h > w * 1.05):
            continue
        out.update(idx)
    return out


def sweep_bboxes(band, removed_idx, pad=4.0):
    """Also remove strays inside removed components' padded boxes."""
    comps = components([band[i] for i in sorted(removed_idx)])
    idx_map = sorted(removed_idx)
    boxes = []
    for c in comps:
        segs = [band[idx_map[i]] for i in c]
        xs = [v for s in segs for v in (s[0], s[2])]
        ys = [v for s in segs for v in (s[1], s[3])]
        boxes.append((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad))
    extra = set()
    for i, s in enumerate(band):
        if i in removed_idx:
            continue
        mx, my = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
        if any(x0 <= mx <= x1 and y0 <= my <= y1 for (x0, y0, x1, y1) in boxes):
            extra.add(i)
    return extra


def garland(x0, x1, y, h, warm=(205, 120, 45), red=(178, 52, 38)):
    """The beta Freeport border: double rule, hanging arc swags, corner gems."""
    segs = [(x0, y, x1, y, (45, 40, 38)), (x0, y + h * 0.06, x1, y + h * 0.06, (45, 40, 38))]
    n = max(6, int((x1 - x0) / (h * 1.35)))
    for k in range(n):
        a, b = x0 + (x1 - x0) * k / n, x0 + (x1 - x0) * (k + 1) / n
        cx, r = (a + b) / 2, (b - a) / 2 * 0.72
        ink = warm if k % 2 else red
        pts = [(cx + r * math.cos(t), y + h * 0.10 + r * 0.9 * math.sin(t))
               for t in [math.pi * i / 8 for i in range(9)]]
        for i in range(len(pts) - 1):
            segs.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], ink))
    for xx in (x0, x1):                               # corner gems
        d = h * 0.30
        segs += [(xx, y - d, xx + d, y, red), (xx + d, y, xx, y + d, red),
                 (xx, y + d, xx - d, y, red), (xx - d, y, xx, y - d, red),
                 (xx, y - d * 0.5, xx + d * 0.5, y, warm), (xx + d * 0.5, y, xx, y + d * 0.5, warm),
                 (xx, y + d * 0.5, xx - d * 0.5, y, warm), (xx - d * 0.5, y, xx, y - d * 0.5, warm)]
    return segs


def fit(style, text, box, kw=None, pad=0.94):
    """Render style text scaled+centred into box=(x0,y0,x1,y1)."""
    kw = dict(kw or {})
    segs, bb = render(style, text, 0, 0, 100, **kw)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    sc = min((box[2] - box[0]) * pad / bw, (box[3] - box[1]) * pad / bh)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    mx, my = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    return [((a - mx) * sc + cx, (b - my) * sc + cy,
             (c - mx) * sc + cx, (d - my) * sc + cy, ink)
            for (a, b, c, d, ink) in segs]


L = slen
ZONES = {
    # zone: dict(text, style, kw, mode, inks / detector overrides, notes)
    "freporte": dict(text="FREEPORT", word="EAST", style="extruded", mode="all"),
    "freportw": dict(text="FREEPORT", word="WEST", style="extruded", mode="all"),
    "freportn": dict(text="FREEPORT", word="NORTH", style="extruded", mode="ink",
                     inks={(45, 40, 38), (205, 120, 45)}),
    "qeynos": dict(text="SOUTH QEYNOS", style="stately", mode="ink",
                   inks={(70, 86, 92)}),
    "qeynos2": dict(text="NORTH QEYNOS", style="stately", mode="ink",
                    inks={(70, 86, 92)}),
    "qcat": dict(text="QEYNOS CATACOMBS", style="stately", mode="ink",
                 inks={(58, 74, 42)}, frame_wide=True,
                 kw=dict(ink=(74, 66, 58), shadow=(44, 40, 36))),
    "erudnext": dict(text="ERUDIN", style="refined", mode="ink",
                     inks={(70, 86, 92)}, rule_ink=(150, 164, 168)),
    "erudnint": dict(text="ERUDIN PALACE", style="refined", mode="ink",
                     inks={(70, 86, 92)}, grow=1.5,
                     rule_ink=(104, 122, 128)),
    "halas": dict(text="HALAS", style="runic", mode="ink", inks={(92, 74, 52)},
                  grow=1.0, dy=8),
    "grobb": dict(text="GROBB", style="crude", mode="ink",
                  inks={(112, 100, 76)}, xwin=(0.245, 0.68),
                  protect=[(0.20, 0.31, -975, -905)]),
    "oggok": dict(text="OGGOK", style="crude", mode="ink", knockout=True,
                  inks={(98, 88, 60), (120, 96, 54)}, xwin=(0.36, 0.61),
                  protect=[(0.0, 1.0, -1300, -1130)],
                  kw=dict(ink=(122, 86, 54), shade=(70, 50, 34), seed=7)),
    "neriaka": dict(text="NERIAK FOREIGN QUARTER", style="darkelf", mode="ink",
                    inks={(44, 34, 58), (50, 40, 64)}),
    "neriakb": dict(text="NERIAK COMMONS", style="darkelf", mode="ink",
                    inks={(44, 34, 58), (50, 40, 64), (168, 132, 72)}),
    "neriakc": dict(text="NERIAK THIRD GATE", style="darkelf", mode="ink",
                    inks={(44, 34, 58), (50, 40, 64)}),
    "felwithea": dict(text="NORTHERN FELWITHE", style="highelf", mode="generic",
                      det=dict(graph_min_len=12.0, min_med_len=13.0, min_h=30),
                      knockout=True, grow=1.2),
    "felwitheb": dict(text="SOUTHERN FELWITHE", style="highelf", mode="generic",
                      det=dict(graph_min_len=12.0, min_med_len=13.0, min_h=30),
                      knockout=True, grow=1.2),
    "rivervale": dict(text="RIVERVALE", style="rounded", mode="generic",
                      knockout=True),
    "akanon": dict(text="AK'ANON", style="clockwork", mode="ink",
                   inks={(62, 104, 56)}, grow=1.2),
    "qrg": dict(text="SUREFALL GLADE", style="sylvan", mode="generic",
                knockout=True),
    "freeportsewers": dict(text="FREEPORT SEWERS", style="extruded", mode="ink",
                           inks={(92, 80, 66)},
                           kw=dict(face=(122, 128, 74), depth_ink=(56, 58, 40))),
}


def apply_zone(zone, dry=False):
    cfg = ZONES[zone]
    lo = layout(content_bbox(zone))
    gy0 = lo["grid"][2]
    fx0, fx1 = lo["frame"][0], lo["frame"][1]
    path = os.path.join(MAPS, zone + "_2.txt")
    raw = [l for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]
    keep_lines, band, band_lines = [], [], []
    for l in raw:
        if l[:1] == "L":
            s = parse(l)
            if (s[1] + s[3]) / 2 < gy0 + 40:
                band.append(s)
                band_lines.append(l)
                continue
        keep_lines.append(l)

    if cfg["mode"] == "all":
        removed = set(range(len(band)))
    elif cfg["mode"] == "ink":
        removed = {i for i, s in enumerate(band) if s[4] in cfg["inks"]}
        if "xwin" in cfg:                             # letters share ink with
            bx = [v for s in band for v in (s[0], s[2])]  # decor: x-window it
            b0, bw = min(bx), max(bx) - min(bx)
            f0, f1 = cfg["xwin"]
            removed = {i for i in removed
                       if f0 <= ((band[i][0] + band[i][2]) / 2 - b0) / bw <= f1
                       and slen(band[i]) < 150}
        for (pf0, pf1, py0, py1) in cfg.get("protect", []):
            bx = [v for s in band for v in (s[0], s[2])]
            b0, bw = min(bx), max(bx) - min(bx)
            removed = {i for i in removed
                       if not (pf0 <= ((band[i][0] + band[i][2]) / 2 - b0) / bw <= pf1
                               and py0 <= (band[i][1] + band[i][3]) / 2 <= py1)}
    elif cfg["mode"] == "ink_comp":
        # letters share ink with other art (guards, trees): restrict to the
        # letter inks, then keep only letter-shaped components of them
        pool = [i for i, s in enumerate(band) if s[4] in cfg["inks"]]
        sub = [band[i] for i in pool]
        picked = letter_components(sub, **cfg.get("det", {}))
        removed = {pool[i] for i in picked}
    else:
        removed = letter_components(band, **cfg.get("det", {}))
    if cfg["mode"] != "all":
        removed |= sweep_bboxes(band, removed)
    if "rule_ink" in cfg:
        # long ruled lines tied to the old lettering (underlines), taken by
        # ink + proximity to the letters' strip so frame crests survive
        ys0 = [v for i in removed for v in (band[i][1], band[i][3])]
        lo, hi = min(ys0) - 30, max(ys0) + 30
        removed |= {i for i, s in enumerate(band)
                    if s[4] == cfg["rule_ink"] and slen(s) > 60
                    and lo <= (s[1] + s[3]) / 2 <= hi}

    old = [band[i] for i in removed]
    if not old:
        raise SystemExit("%s: nothing selected for removal" % zone)
    xs = [v for s in old for v in (s[0], s[2])]
    ys = [v for s in old for v in (s[1], s[3])]
    slot = (min(xs), min(ys), max(xs), max(ys))

    new = []
    if zone.startswith("freport"):
        # two-tier: garland at the frame top, pale word, big extruded name
        bh = 46.0
        y0 = slot[1] + 14 if cfg["mode"] == "all" else slot[1]
        if zone == "freportn":
            y0 = slot[1] + 26                         # sit under the decor row
        new += garland(fx0 + 30, fx1 - 30, y0, bh)
        H = min(120.0, (fx1 - fx0) * 0.72 / 6.2)      # FREEPORT is long
        base = y0 + bh * 2.1 + H
        if cfg["mode"] == "all":                      # centre in the open band
            base = max(base, (y0 + bh * 2 + gy0) / 2 + H * 0.45)
        big, bb = render(cfg["style"], cfg["text"], 0, 0, H, **cfg.get("kw", {}))
        bw = bb[2] - bb[0]
        bx = (fx0 + fx1) / 2 - bw / 2 + H * 0.55      # room for the word
        big = [(a + bx, b + base, c + bx, d + base, ink) for (a, b, c, d, ink) in big]
        word, wb = render("small_caps", cfg["word"], 0, 0, H * 0.40)
        wx, wy = bx - (wb[2] - wb[0]) - H * 0.35, base - H * 0.52
        new += [(a + wx, b + wy, c + wx, d + wy, ink) for (a, b, c, d, ink) in word]
        new += big
    else:
        grow = cfg.get("grow", 1.9 if zone == "qcat" else 1.35)
        cy = (slot[1] + slot[3]) / 2 + cfg.get("dy", 0)
        hh = (slot[3] - slot[1]) / 2 * grow
        if cfg.get("frame_wide"):
            bx0, bx1 = fx0 + 25, fx1 - 25
        else:
            bx0 = max(slot[0] - 40, fx0 + 25)
            bx1 = min(slot[2] + 40, fx1 - 25)
        box = (bx0, cy - hh, bx1, cy + hh)
        new = fit(cfg["style"], cfg["text"], box, cfg.get("kw"))

    if cfg.get("knockout") and new:
        # clear surrounding texture out from under the fresh lettering
        nb = _bbox(new, pad=6.0)
        removed |= {i for i, s in enumerate(band)
                    if i not in removed and slen(s) < 25
                    and nb[0] <= (s[0] + s[2]) / 2 <= nb[2]
                    and nb[1] <= (s[1] + s[3]) / 2 <= nb[3]}

    if dry:
        return band, removed, new
    out = []
    for i, l in enumerate(band_lines):
        if i not in removed:
            out.append(l)
    for (a, b, c, d, ink) in new:
        out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"
                   % (a, b, 0.0, c, d, 0.0, *ink))
    out += keep_lines
    open(path, "w", newline="", encoding="utf-8").write(CRLF.join(out) + CRLF)
    print("%s: removed %d, drew %d (%s/%s)" %
          (zone, len(removed), len(new), cfg["style"], cfg["text"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("zones", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    for z in a.zones:
        apply_zone(z, dry=a.dry_run)
