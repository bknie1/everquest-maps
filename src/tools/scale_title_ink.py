"""scale_title_ink.py -- select title strokes by INK + WINDOW, plot the
selection alone, and scale them in place about their own center.

The ink-window selector is the simple sibling of scale_title.py's
component detector: most styled titles are drawn in one or two inks that
nothing else in the band uses, so ink + a y-window (+ an x-window / min
stroke length when the ink is shared with a rule, a boulder field or corner
flourishes) picks exactly the letters -- and the PLOT proves it before any
write. The 2026-09-12 size sweep shrank fifteen titles this way with zero
tears; the one miss (soldungb's R leg in a second ink) is why --center
exists: a follow-up pass can reuse the first pass's pivot exactly.

    python src/tools/scale_title_ink.py plot  <zone> --inks r,g,b [...]
        [--ywin y0,y1] [--xwin x0,x1] [--minlen L] --out band.png
    python src/tools/scale_title_ink.py scale <zone> --inks ... [windows]
        --factor 0.8 [--anchor center|baseline] [--center x,y] [--write]

Selection = strokes whose midpoint is inside the window AND whose ink is in
--inks. Default y-window = the title band (mid-y < grid_top + 40). The plot
draws the band grey, the selection red, and the frame edges blue -- if any
red is not a letter, tighten the window; if any letter is grey, widen it.
Then render the zone and look at the title before committing.
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(ROOT, "src", "kit")):
    sys.path.insert(0, p)
from fix_title import content_bbox  # noqa: E402
from layout import layout  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", os.path.join(ROOT, "Emoda Legends Maps"))
CRLF = "\r\n"


def load(path):
    lines = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines() if l.strip()]
    segs = {}
    for i, l in enumerate(lines):
        if l[:1] != "L":
            continue
        f = [v.strip() for v in l[1:].lstrip().split(",")]
        if len(f) < 9:
            continue
        segs[i] = [float(f[0]), float(f[1]), float(f[2]), float(f[3]), float(f[4]), float(f[5]),
                   int(float(f[6])), int(float(f[7])), int(float(f[8]))]
    return lines, segs


def select(zone, segs, inks, xwin, ywin, ycut, minlen=0.0):
    lo = layout(content_bbox(zone))
    gy0 = lo["grid"][2]
    if ywin is None:
        ywin = (-1e9, (ycut if ycut is not None else gy0 + 40))
    sel = set()
    for i, s in segs.items():
        mx, my = (s[0] + s[3]) / 2, (s[1] + s[4]) / 2
        if not (ywin[0] <= my <= ywin[1]):
            continue
        if xwin and not (xwin[0] <= mx <= xwin[1]):
            continue
        if inks and (s[6], s[7], s[8]) not in inks:
            continue
        if minlen and math.hypot(s[3] - s[0], s[4] - s[1]) < minlen:
            continue
        sel.add(i)
    return sel, lo


def plot(segs, sel, out, ymax, lo):
    from PIL import Image, ImageDraw
    fx0, fx1 = lo["frame"][0], lo["frame"][1]
    band = {i: s for i, s in segs.items() if (s[1] + s[4]) / 2 <= ymax + 60}
    if not band:
        print("nothing in band")
        return
    xs = [v for s in band.values() for v in (s[0], s[3])]
    ys = [v for s in band.values() for v in (s[1], s[4])]
    x0, x1, y0, y1 = min(xs) - 20, max(xs) + 20, min(ys) - 20, max(ys) + 20
    W = 1400
    sc = W / (x1 - x0)
    H = int((y1 - y0) * sc) + 1
    im = Image.new("RGB", (W, H), (240, 232, 210))
    d = ImageDraw.Draw(im)
    for fx in (fx0, fx1):
        d.line([((fx - x0) * sc, 0), ((fx - x0) * sc, H)], fill=(120, 170, 220))
    for i, s in band.items():
        col = (200, 30, 30) if i in sel else (150, 150, 150)
        d.line([((s[0] - x0) * sc, (s[1] - y0) * sc), ((s[3] - x0) * sc, (s[4] - y0) * sc)],
               fill=col, width=2 if i in sel else 1)
    im.save(out)
    print("plot ->", out, "band strokes", len(band), "selected", len(sel))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plot", "scale"])
    ap.add_argument("zone")
    ap.add_argument("--file", help="read this _2 file instead (e.g. a git show export)")
    ap.add_argument("--inks", nargs="*", default=[])
    ap.add_argument("--xwin")
    ap.add_argument("--ywin")
    ap.add_argument("--ycut", type=float)
    ap.add_argument("--factor", type=float, default=1.0)
    ap.add_argument("--anchor", default="center")
    ap.add_argument("--minlen", type=float, default=0.0)
    ap.add_argument("--center", help="x,y pivot override (to match a previous scale)")
    ap.add_argument("--out")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    path = a.file or os.path.join(MAPS, a.zone + "_2.txt")
    lines, segs = load(path)
    inks = {tuple(int(v) for v in t.split(",")) for t in a.inks}
    xwin = tuple(float(v) for v in a.xwin.split(",")) if a.xwin else None
    ywin = tuple(float(v) for v in a.ywin.split(",")) if a.ywin else None
    sel, lo = select(a.zone, segs, inks, xwin, ywin, a.ycut, a.minlen)
    if not sel:
        print("no strokes selected")
        return
    xs = [v for i in sel for v in (segs[i][0], segs[i][3])]
    ys = [v for i in sel for v in (segs[i][1], segs[i][4])]
    print("%s: selected %d strokes, bbox x[%.0f,%.0f] y[%.0f,%.0f] h=%.0f w=%.0f"
          % (a.zone, len(sel), min(xs), max(xs), min(ys), max(ys), max(ys) - min(ys), max(xs) - min(xs)))
    if a.cmd == "plot":
        ymax = ywin[1] if ywin else (a.ycut if a.ycut is not None else lo["grid"][2] + 40)
        plot(segs, sel, a.out, ymax, lo)
        return
    cx = (min(xs) + max(xs)) / 2
    cy = max(ys) if a.anchor == "baseline" else (min(ys) + max(ys)) / 2
    if a.center:
        cx, cy = (float(v) for v in a.center.split(","))
    f = a.factor
    for i in sel:
        s = segs[i]
        s[0] = cx + (s[0] - cx) * f
        s[3] = cx + (s[3] - cx) * f
        s[1] = cy + (s[1] - cy) * f
        s[4] = cy + (s[4] - cy) * f
        lines[i] = "L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d" % tuple(s)
    xs = [v for i in sel for v in (segs[i][0], segs[i][3])]
    ys = [v for i in sel for v in (segs[i][1], segs[i][4])]
    print("  -> scaled x%.2f about (%.0f,%.0f): bbox x[%.0f,%.0f] y[%.0f,%.0f] h=%.0f w=%.0f%s"
          % (f, cx, cy, min(xs), max(xs), min(ys), max(ys), max(ys) - min(ys), max(xs) - min(xs),
             "  WRITTEN" if a.write else "  (dry run)"))
    if a.write:
        open(path, "w", newline="", encoding="utf-8").write(CRLF.join(lines) + CRLF)


if __name__ == "__main__":
    main()
