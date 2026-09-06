"""declutter.py -- whole-asset removal from the most crowded spots.

For zones whose budget fat is placed assets (blob rocks, pine glyphs, bushes)
rather than scribble texture. Stroke-level thinning breaks drawn outlines;
this removes ASSETS whole, greedily from wherever they crowd worst, so every
survivor stays intact and coverage stays even. The counterpart to the
uniform-random rule for scribble texture (feerrott e0142ae).

Assets are recovered as file-order runs of one ink (generators emit each
placed asset contiguously): a run breaks on a centroid jump >120u or a
line-index gap >8. Removal is greedy by neighbor count within --radius,
updated as neighbors die; ties break on a centroid md5, so runs are
deterministic. The title box (--titlebox, pad it yourself) is keep-out by
bbox-intersect -- titles often share the asset ink.

    python src/tools/declutter.py <file.txt> --ink R,G,B --target N \
        [--radius 130] [--titlebox x0,y0,x1,y1] [--keep-rect x0,y0,x1,y1] \
        [--write]

--keep-rect protects a region entirely (e.g. the playable interior when only
margins should thin). --target is strokes to remove, not assets.
"""
import argparse
import hashlib
import os

CRLF = "\r\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--ink", required=True)
    ap.add_argument("--target", type=int, required=True)
    ap.add_argument("--radius", type=float, default=130.0)
    ap.add_argument("--titlebox")
    ap.add_argument("--keep-rect")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    ink = tuple(a.ink.split(","))
    tb = tuple(float(v) for v in a.titlebox.split(",")) if a.titlebox else None
    kr = tuple(float(v) for v in a.keep_rect.split(",")) if a.keep_rect else None

    lines = [l for l in open(a.path, encoding="utf-8", errors="ignore").read().splitlines()
             if l.strip()]
    seq = []
    for i, l in enumerate(lines):
        if l[:1] != "L":
            continue
        f = [v.strip() for v in l[2:].split(",")]
        if len(f) < 9 or (f[6], f[7], f[8]) != ink:
            continue
        x1, y1, x2, y2 = float(f[0]), float(f[1]), float(f[3]), float(f[4])
        seq.append((i, (x1 + x2) / 2, (y1 + y2) / 2,
                    min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)))
    if not seq:
        print("no strokes of ink", ink)
        return

    runs, cur = [], [seq[0]]
    for p, q in zip(seq, seq[1:]):
        if ((q[1] - p[1]) ** 2 + (q[2] - p[2]) ** 2) ** 0.5 > 120 or q[0] - p[0] > 8:
            runs.append(cur)
            cur = []
        cur.append(q)
    runs.append(cur)

    blobs = []
    for r in runs:
        bx0, bx1 = min(s[3] for s in r), max(s[4] for s in r)
        by0, by1 = min(s[5] for s in r), max(s[6] for s in r)
        if tb and bx0 <= tb[2] and bx1 >= tb[0] and by0 <= tb[3] and by1 >= tb[1]:
            continue
        if kr and bx0 <= kr[2] and bx1 >= kr[0] and by0 <= kr[3] and by1 >= kr[1]:
            continue
        cx = sum(s[1] for s in r) / len(r)
        cy = sum(s[2] for s in r) / len(r)
        blobs.append(dict(idx=[s[0] for s in r], cx=cx, cy=cy, n=len(r), dead=False,
                          tie=hashlib.md5(("%.1f,%.1f" % (cx, cy)).encode()).hexdigest()))

    R2 = a.radius * a.radius
    for b in blobs:
        b["nb"] = [o for o in blobs if o is not b
                   and (o["cx"] - b["cx"]) ** 2 + (o["cy"] - b["cy"]) ** 2 < R2]
        b["crowd"] = len(b["nb"])

    dropped, killed = 0, []
    while dropped < a.target:
        live = [b for b in blobs if not b["dead"] and b["crowd"] > 0]
        if not live:
            break
        pick = max(live, key=lambda b: (b["crowd"], b["tie"]))
        pick["dead"] = True
        dropped += pick["n"]
        killed.append(pick)
        for o in pick["nb"]:
            o["crowd"] -= 1

    kill = set(i for b in killed for i in b["idx"])
    print("%s: %d assets eligible, removed %d (-%d strokes), %d -> %d%s"
          % (os.path.basename(a.path), len(blobs), len(killed), dropped,
             len(lines), len(lines) - len(kill),
             "  WRITTEN" if a.write else "  (dry run)"))
    if a.write and kill:
        out = [l for i, l in enumerate(lines) if i not in kill]
        open(a.path, "w", newline="", encoding="utf-8").write(CRLF.join(out) + CRLF)


if __name__ == "__main__":
    main()
