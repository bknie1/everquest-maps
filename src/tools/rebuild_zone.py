"""rebuild_zone.py -- compose a zone's decoration (_2) fresh from clean geometry.

Instead of patching old-title artifacts out of an inherited _2, this throws the
old _2 away and draws a clean one from the base up: frame, title, compass rose,
biome ground cover and margin decoration. The old titles never come along, so we
stop repeating the same artifact-removal mistakes.

Only _2 is regenerated. The base (<zone>.txt), POIs (_1) and historical layer
(_3) are left untouched -- the base carries no title (content_bbox is defined by
it, so nothing sits in the title band) and the POIs are hand/wiki sourced.

    python src/tools/rebuild_zone.py qeytoqrg --theme qeynos_hills --name "QEYNOS HILLS"
    python src/tools/rebuild_zone.py qeytoqrg --theme qeynos_hills --probe

A theme names the biome treatment (interior fill + margin shapes + inks). Add
themes to THEMES below; the frame/title/compass core is biome-independent.
"""
import argparse
import math
import os
import random
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from fix_title import content_bbox, word_segs, group_width  # noqa: E402
from layout import layout  # noqa: E402
import terrain as TR  # noqa: E402
import flora_hd as FH  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"


def L(a, b, c, d, ink):
    return "L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (a, b, c, d, *ink)


# ------------------------------------------------------------------ core pieces
def jag_rect(bounds, ink, amp, seg):
    """A hand-drawn jagged border rectangle at `bounds` = (x0,x1,y0,y1)."""
    x0, x1, y0, y1 = bounds
    rng = random.Random(11)
    out = []

    def edge(ax, ay, bx, by, outx, outy):
        n = max(3, int(math.hypot(bx - ax, by - ay) / seg))
        pts = []
        for k in range(n + 1):
            t = k / n
            jx = outx * (rng.uniform(0.2, 1.0) * amp if 0 < k < n and k % 2 else 0)
            jy = outy * (rng.uniform(0.2, 1.0) * amp if 0 < k < n and k % 2 else 0)
            pts.append((ax + (bx - ax) * t + jx, ay + (by - ay) * t + jy))
        for k in range(n):
            out.append(L(*pts[k], *pts[k + 1], ink))

    edge(x0, y0, x1, y0, 0, -1)   # top    jags up (out = -y)
    edge(x0, y1, x1, y1, 0, 1)    # bottom jags down
    edge(x0, y0, x0, y1, -1, 0)   # left   jags left
    edge(x1, y0, x1, y1, 1, 0)    # right  jags right
    return out


def title(name, band, ink):
    """Center `name` in the title band, scaled to fit its width and height."""
    bx0, bx1, byt, byb = band            # byt < byb  (top is more negative)
    bw, bh = bx1 - bx0, byb - byt
    h = bh * 0.52
    cw = h * 0.64
    gap = h * 0.20
    w = group_width(name, cw, gap)
    if w > bw * 0.86:                     # too wide -> shrink to fit
        k = bw * 0.86 / w
        h *= k; cw *= k; gap *= k; w *= k
    ox = (bx0 + bx1) / 2 - w / 2
    ybase = byb - bh * 0.24               # baseline a little above the band floor
    return [L(a, b, c, d, ink) for (a, b, c, d) in word_segs(name, ox, ybase, cw, h, gap)]


def rose(cx, cy, r, ink):
    """A proper compass rose: 16-seg ring, 8 rays, stroke N/E/S/W (matches
    fix_compass exactly, so rebuilt zones read the same as fixed ones)."""
    out = []
    ring = [(cx + r * math.cos(t), cy + r * math.sin(t))
            for t in [i * 2 * math.pi / 16 for i in range(17)]]
    for i in range(16):
        out.append(L(*ring[i], *ring[i + 1], ink))
    for k in range(8):
        a = k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.55
        out.append(L(cx, cy, cx + rr * math.cos(a), cy + rr * math.sin(a), ink))
    h = max(24.0, r * 0.38); cw = h * 0.66; gap = h * 0.16
    for lbl, (lx, ly) in [("N", (cx - cw / 2, cy - r - 12)),
                          ("S", (cx - cw / 2, cy + r + 12 + h)),
                          ("E", (cx + r + 12, cy + h * 0.5)),
                          ("W", (cx - r - 12 - cw, cy + h * 0.5))]:
        out += [L(a, b, c, d, ink) for (a, b, c, d) in word_segs(lbl, lx, ly, cw, h, gap)]
    return out


def margin_trees(LO, theme, reserved, seed=5):
    """Scatter the theme's tree at fixed slots around the margin ring, skipping
    the title band and any reserved footprint (the compass)."""
    gx0, gx1, gy0, gy1 = LO["grid"]
    mx0, mx1, my0, my1 = LO["margin"]
    S = LO["S"]
    fn = theme["tree"]; ink = theme["tree_ink"]
    rng = random.Random(seed)
    slots = []
    for k in range(theme.get("n_top", 5)):
        slots.append((gx0 + (gx1 - gx0) * (k + 0.5) / theme.get("n_top", 5), (my0 + gy0) / 2))
    for k in range(theme.get("n_bot", 6)):
        slots.append((gx0 + (gx1 - gx0) * (k + 0.5) / theme.get("n_bot", 6), (gy1 + my1) / 2))
    for k in range(theme.get("n_side", 4)):
        y = gy0 + (gy1 - gy0) * (k + 0.5) / theme.get("n_side", 4)
        slots.append(((mx0 + gx0) / 2, y)); slots.append(((gx1 + mx1) / 2, y))
    out = []
    for (x, y) in slots:
        if any(abs(x - rx) < rr and abs(y - ry) < rr for (rx, ry, rr) in reserved):
            continue
        out += [L(*s[:4], s[4]) for s in
                fn(x, y, S * rng.uniform(0.026, 0.036), ink=ink, seed=int(abs(x) + abs(y)))]
    return out


# ------------------------------------------------------------------------ themes
THEMES = {
    # West Antonica hills -- Qeynos Hills signature: dense low tick-grass field,
    # a rocky band across the top (the hills), deciduous margin trees.
    "qeynos_hills": dict(
        title_ink=(92, 76, 52), frame_ink=(120, 104, 80), compass_ink=(78, 70, 92),
        interior="grass", grass_step=52.0, grass_density=0.55,
        grass_ink=[(96, 122, 78), (110, 138, 88), (78, 104, 64)],
        rocky_top_frac=0.32, rock_step=46.0,
        tree=FH.broadleaf, tree_ink=(60, 90, 58), n_top=5, n_bot=6, n_side=4),
    # Gothic castle/dungeon: NO interior fill (base IS the structure), gothic
    # purple-slate ink, dead trees ringing the margin. For Mistmoore et al.
    "castle_gothic": dict(
        title_ink=(96, 84, 112), frame_ink=(108, 94, 122), compass_ink=(92, 80, 108),
        tree=FH.dead_tree, tree_ink=(86, 80, 94), n_top=5, n_bot=6, n_side=4),
    # Faydwer forest: canopy already lives in the base, so NO interior fill --
    # just a clean frame/title/corner-compass and a dense broadleaf tree border.
    "faydark": dict(
        title_ink=(74, 96, 60), frame_ink=(96, 116, 76), compass_ink=(66, 86, 56),
        tree=FH.broadleaf, tree_ink=(56, 84, 54), n_top=8, n_bot=9, n_side=6),
}


def build(zone, name, theme, probe=False):
    CX0, CX1, CY0, CY1 = content_bbox(zone)
    LO = layout((CX0, CX1, CY0, CY1))
    gx0, gx1, gy0, gy1 = LO["grid"]
    mx0, mx1, my0, my1 = LO["margin"]
    band = LO["title_band"]
    out = []

    # frame
    out += jag_rect(LO["frame"], theme["frame_ink"], LO["S"] * 0.010, LO["S"] * 0.018)

    # compass -- bottom-right margin corner
    r = LO["S"] * 0.036
    ccx = (gx1 + mx1) / 2
    ccy = (gy1 + my1) / 2
    out += rose(ccx, ccy, r, theme["compass_ink"])
    reserved = [(ccx, ccy, r * 2.4)]

    # interior biome fill, bounded by the CONTENT box (never the margin)
    def inside(x, y):
        return CX0 <= x <= CX1 and CY0 <= y <= CY1

    if theme.get("interior") == "grass":
        rocky_cut = CY0 + (CY1 - CY0) * theme.get("rocky_top_frac", 0.0)
        if theme.get("rocky_top_frac"):
            out += [L(*s[:4], s[4]) for s in TR.rock_band(
                lambda x, y: inside(x, y) and y < rocky_cut,
                CX0, CY0, CX1, rocky_cut, step=theme.get("rock_step", 46.0), seed=3)]
        out += [L(*s[:4], s[4]) for s in TR.grass_field(
            lambda x, y: inside(x, y) and y >= rocky_cut,
            CX0, rocky_cut, CX1, CY1, step=theme.get("grass_step", 48.0),
            ink=tuple(theme["grass_ink"]) if isinstance(theme["grass_ink"], list) else theme["grass_ink"],
            seed=7, density=theme.get("grass_density", 0.6))]

    # title (drawn last so it sits on top)
    out += title(name, band, theme["title_ink"])

    # margin decoration
    out += margin_trees(LO, theme, reserved)

    if probe:
        print(f"{zone}: would write {len(out)} strokes to _2 "
              f"(content {CX1-CX0:.0f}x{CY1-CY0:.0f}, S={LO['S']:.0f})")
        return
    path = os.path.join(MAPS, zone + "_2.txt")
    open(path, "w", newline="", encoding="utf-8").write(CRLF.join(out) + CRLF)
    print(f"{zone}: rebuilt _2 with {len(out)} strokes (frame+title+compass+biome)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--theme", required=True)
    ap.add_argument("--name", required=True, help="title text to draw")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    if args.theme not in THEMES:
        sys.exit(f"unknown theme {args.theme}; have: {', '.join(THEMES)}")
    build(args.zone, args.name.upper(), THEMES[args.theme], probe=args.probe)


if __name__ == "__main__":
    main()
