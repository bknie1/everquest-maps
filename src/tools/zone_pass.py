"""zone_pass.py -- the ONE idiot-proof command for enriching a zone's margins.

Every rule learned the hard way is enforced HERE so the operator (human or
model) cannot repeat the old mistakes:

  RULE 1  Never touch the base map, POIs (_1) or history (_3). Only _2 grows.
  RULE 2  Never delete anything. This tool only APPENDS decoration.
  RULE 3  Stay under the ~31k stroke budget or the client stops rendering.
  RULE 4  Don't decorate margins that are already rich (fog, cave walls...).
  RULE 5  Never place anything in the title band or over the compass.
  RULE 6  Figures come from fauna_sil (solid silhouettes) -- the ONLY figure
          style that reads at map scale. Race mix comes from the zone's wiki
          page unless --figures overrides it.
  RULE 7  CRLF line endings, always.

    python src/tools/zone_pass.py <zone> --probe          # report, change nothing
    python src/tools/zone_pass.py <zone>                  # wiki-driven figures
    python src/tools/zone_pass.py <zone> --figures dark_elf,skeleton --flora dead_tree
    python src/tools/zone_pass.py <zone> --force          # override the density guard

After any pass:  python src/tools/render_zone.py <zone>  and LOOK at it.
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from fix_title import content_bbox, parse  # noqa: E402
from layout import layout  # noqa: E402
from fauna_sil import SIL, HEIGHT  # noqa: E402
import flora_hd as FH  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
BUDGET = 31000            # client draw cap, all layers
MARGIN_DENSE = 650        # margin strokes above this = already decorated, skip

FLORA = {n: getattr(FH, n) for n in
         ("fir", "broadleaf", "palm", "dead_tree", "willow", "redwood")}


def count_records(zone):
    n = 0
    for suf in ("", "_1", "_2", "_3"):
        p = os.path.join(MAPS, zone + suf + ".txt")
        if os.path.exists(p):
            n += sum(1 for l in open(p, encoding="utf-8") if l[:1] in "LP")
    return n


def wiki_figures(zone, top=3):
    """Rank the zone's wiki creatures onto SIL figure names."""
    try:
        import enrich_margins as EM
        motifs, hits = EM.wiki_motifs(zone, top=6)
    except Exception:
        return []
    return [m for m in motifs if m in SIL][:top]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--figures", help="comma list of fauna_sil names (default: wiki)")
    ap.add_argument("--flora", help="comma list of flora_hd names, e.g. fir,dead_tree")
    ap.add_argument("--scale", type=float, default=0.055,
                    help="human height as a fraction of the zone span")
    ap.add_argument("--force", action="store_true", help="override the density guard")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    z = args.zone

    # ---- verdicts first
    p2 = os.path.join(MAPS, z + "_2.txt")
    if not os.path.exists(os.path.join(MAPS, z + ".txt")):
        sys.exit(f"{z}: no base map")
    LO = layout(content_bbox(z))
    gx0, gx1, gy0, gy1 = LO["grid"]
    fx0, fx1, fy0, fy1 = LO["frame"]
    S = LO["S"]
    raw = [l for l in open(p2, encoding="utf-8").read().splitlines() if l.strip()] \
        if os.path.exists(p2) else []
    segs = [parse(l) for l in raw if l[:1] == "L"]
    margin_n = sum(1 for s_ in segs
                   if not (gx0 < (s_[0] + s_[2]) / 2 < gx1 and gy0 < (s_[1] + s_[3]) / 2 < gy1))
    total = count_records(z)
    figures = ([f.strip() for f in args.figures.split(",")] if args.figures
               else wiki_figures(z))
    bad = [f for f in figures if f not in SIL]
    if bad:
        sys.exit(f"{z}: unknown figures {bad}; valid: {', '.join(sorted(set(SIL)))}")
    flora = [f.strip() for f in args.flora.split(",")] if args.flora else []
    badf = [f for f in flora if f not in FLORA]
    if badf:
        sys.exit(f"{z}: unknown flora {badf}; valid: {', '.join(FLORA)}")

    print(f"{z}: total={total}/{BUDGET}  margin_deco={margin_n} "
          f"(dense>{MARGIN_DENSE})  figures={figures or 'NONE'}")
    if args.probe:
        return
    if not figures:
        sys.exit(f"{z}: no wiki figures found -- pass --figures explicitly")
    if total > BUDGET - 1500:
        sys.exit(f"{z}: too close to the {BUDGET} budget -- dedupe first, don't add")
    if margin_n > MARGIN_DENSE and not args.force:
        sys.exit(f"{z}: margins already rich ({margin_n} strokes) -- this zone "
                 f"keeps its existing flavor. Use --force only after LOOKING at it")

    # ---- keep-out zones: title band (top margin) + detected compass + POI labels
    keepout = [(gx0 - S, gx1 + S, fy0 - S, gy0)]        # entire top margin
    try:
        from fix_compass import find_center, find_cluster_compass
        det = find_center(z, raw) or find_cluster_compass(z, raw)
        if det:
            cx_, cy_, r_, _ = det
            r_ = (r_ or 80) * 2.0
            keepout.append((cx_ - r_, cx_ + r_, cy_ - r_, cy_ + r_))
    except Exception:
        pass

    def blocked(x0, x1, y0, y1):
        return any(x0 < b and x1 > a and y0 < d and y1 > c
                   for (a, b, c, d) in keepout)

    # ---- ring slots along bottom + sides (title owns the top)
    mx0, mx1, my0, my1 = LO["margin"]
    boty = (gy1 + my1) / 2
    slots = [(gx0 + (gx1 - gx0) * (k + 0.5) / 7, boty) for k in range(7)]
    for k in range(4):
        y = gy0 + (gy1 - gy0) * (k + 0.5) / 4
        slots.append(((mx0 + gx0) / 2, y))
        slots.append(((gx1 + mx1) / 2, y))

    shapes = []
    for i, f in enumerate(figures):
        shapes.append(("fig", f))
        if flora:
            shapes.append(("flora", flora[i % len(flora)]))

    new, boxes, placed = [], list(keepout), 0
    hs = S * args.scale
    for i, (x, y) in enumerate(slots):
        kind, name = shapes[i % len(shapes)]
        if kind == "fig":
            segs_ = SIL[name](x, y + hs * 0.5, hs * HEIGHT.get(name, 1.0),
                              seed=i, face=(-1 if i % 2 else 1))
        else:
            segs_ = FLORA[name](x, y, S * 0.030, seed=i)
        xs = [v for s_ in segs_ for v in (s_[0], s_[2])]
        ys = [v for s_ in segs_ for v in (s_[1], s_[3])]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        if blocked(bx0, bx1, by0, by1):
            continue
        if bx0 < fx0 or bx1 > fx1 or by1 > fy1:
            continue
        if not (bx1 < gx0 or bx0 > gx1 or by1 < gy0 or by0 > gy1):
            continue                                     # never inside the grid
        if any(bx0 < b + 20 and bx1 > a - 20 and by0 < d + 20 and by1 > c - 20
               for (a, b, c, d) in boxes[len(keepout):]):
            continue
        boxes.append((bx0, bx1, by0, by1))
        for s_ in segs_:
            new.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
                       % (s_[0], s_[1], s_[2], s_[3], *s_[4]))
        placed += 1

    if not new:
        sys.exit(f"{z}: nothing placed (all slots blocked)")
    if total + len(new) > BUDGET:
        sys.exit(f"{z}: adding {len(new)} would burst the budget -- aborting")
    open(p2, "w", newline="", encoding="utf-8").write(CRLF.join(raw + new) + CRLF)
    print(f"{z}: APPENDED {placed} items ({len(new)} strokes). "
          f"Now render it and LOOK: python src/tools/render_zone.py {z}")


if __name__ == "__main__":
    main()
