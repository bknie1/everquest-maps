"""simplify.py -- polyline simplification for over-segmented linework.

Architectural bases draw curves (stair spirals, arcs, ovals) as chains of
tiny segments; at map scale a 1.5u wobble is invisible, but every segment
bills the 31k budget. This walks FILE-ORDER chains of same-ink strokes whose
endpoints connect within --join (default 0.5u), runs Douglas-Peucker at
--tol (default 1.5u) on each chain, and re-emits the survivors. Geometry
moves by at most --tol; straight runs and corners are untouched; nothing is
deleted, only re-segmented. z is interpolated linearly along the chain.

    python src/tools/simplify.py <file.txt> [--tol 1.5] [--join 0.5] [--write]
"""
import argparse
import math
import os

CRLF = "\r\n"


def dp(pts, tol):
    """Douglas-Peucker on [(x, y, z)] -> kept indices."""
    keep = [0, len(pts) - 1]
    stack = [(0, len(pts) - 1)]
    while stack:
        i0, i1 = stack.pop()
        if i1 <= i0 + 1:
            continue
        x0, y0 = pts[i0][0], pts[i0][1]
        x1, y1 = pts[i1][0], pts[i1][1]
        dx, dy = x1 - x0, y1 - y0
        nrm = math.hypot(dx, dy) or 1e-9
        worst, wd = -1, tol
        for j in range(i0 + 1, i1):
            d = abs((pts[j][0] - x0) * dy - (pts[j][1] - y0) * dx) / nrm
            if d > wd:
                worst, wd = j, d
        if worst >= 0:
            keep.append(worst)
            stack.append((i0, worst))
            stack.append((worst, i1))
    return sorted(set(keep))


def geo_simplify(path, tol, write):
    """File order is shuffled in some bases; rebuild chains from geometry.

    Endpoint-adjacency graph on exact (2dp) endpoints per ink+z-plane; every
    maximal degree-2 path is a pen chain, DP-simplified. Junction vertices
    (degree != 2) always survive, so wall intersections cannot move.
    """
    from collections import defaultdict

    lines = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines()
             if l.strip()]
    segs, other = [], []
    for l in lines:
        ok = False
        if l[:1] == "L":
            f = [v.strip() for v in l[2:].split(",")]
            if len(f) >= 9:
                segs.append(((round(float(f[0]), 2), round(float(f[1]), 2), float(f[2])),
                             (round(float(f[3]), 2), round(float(f[4]), 2), float(f[5])),
                             (f[6], f[7], f[8])))
                ok = True
        if not ok:
            other.append(l)

    adj = defaultdict(list)          # (xy, ink) -> [seg index]
    for i, (p, q, ink) in enumerate(segs):
        adj[(p[0], p[1], ink)].append(i)
        adj[(q[0], q[1], ink)].append(i)

    used = [False] * len(segs)
    out, n_out = [], 0

    def emit(pts, ink):
        nonlocal n_out
        kept = dp(pts, tol) if len(pts) > 2 else range(len(pts))
        kept = list(kept)
        for i, j in zip(kept, kept[1:]):
            p, q = pts[i], pts[j]
            out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %s, %s, %s"
                       % (p[0], p[1], p[2], q[0], q[1], q[2], ink[0], ink[1], ink[2]))
            n_out += 1

    for i, (p, q, ink) in enumerate(segs):
        if used[i]:
            continue
        # grow a path both ways through degree-2 vertices
        used[i] = True
        pts = [p, q]
        for end in (1, 0):
            while True:
                v = pts[-1] if end else pts[0]
                key = (v[0], v[1], ink)
                cand = [j for j in adj[key] if not used[j]]
                if len(adj[key]) != 2 or len(cand) != 1:
                    break
                j = cand[0]
                used[j] = True
                a2, b2, _ = segs[j]
                nxt = b2 if (a2[0], a2[1]) == (v[0], v[1]) else a2
                if end:
                    pts.append(nxt)
                else:
                    pts.insert(0, nxt)
        emit(pts, ink)

    print("%s: %d -> %d L strokes (geo, tol %.2f)%s"
          % (os.path.basename(path), len(segs), n_out, tol,
             "  WRITTEN" if write else "  (dry run)"))
    if write and n_out < len(segs):
        open(path, "w", newline="", encoding="utf-8").write(
            CRLF.join(other + out) + CRLF)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--tol", type=float, default=1.5)
    ap.add_argument("--join", type=float, default=0.5)
    ap.add_argument("--geo", action="store_true",
                    help="rebuild chains from endpoint geometry (shuffled files)")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    if a.geo:
        geo_simplify(a.path, a.tol, a.write)
        return

    lines = [l for l in open(a.path, encoding="utf-8", errors="ignore").read().splitlines()
             if l.strip()]
    out, chain, chain_ink = [], [], None
    stats = {"in": 0, "out": 0}

    def flush():
        if not chain:
            return
        pts = [chain[0][:3]] + [s[3:6] for s in chain]
        if len(pts) > 2:
            kept = dp(pts, a.tol)
        else:
            kept = range(len(pts))
        r, g, b = chain_ink
        for i, j in zip(list(kept), list(kept)[1:]):
            p, q = pts[i], pts[j]
            out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %s, %s, %s"
                       % (p[0], p[1], p[2], q[0], q[1], q[2], r, g, b))
            stats["out"] += 1

    for l in lines:
        if l[:1] != "L":
            flush()
            chain, chain_ink = [], None
            out.append(l)
            continue
        f = [v.strip() for v in l[2:].split(",")]
        if len(f) < 9:
            flush()
            chain, chain_ink = [], None
            out.append(l)
            continue
        s = (float(f[0]), float(f[1]), float(f[2]),
             float(f[3]), float(f[4]), float(f[5]))
        ink = (f[6], f[7], f[8])
        stats["in"] += 1
        if chain and ink == chain_ink and \
           math.hypot(s[0] - chain[-1][3], s[1] - chain[-1][4]) <= a.join:
            chain.append(s)
        else:
            flush()
            chain, chain_ink = [s], ink
    flush()

    print("%s: %d -> %d L strokes (tol %.2f)%s"
          % (os.path.basename(a.path), stats["in"], stats["out"], a.tol,
             "  WRITTEN" if a.write else "  (dry run)"))
    if a.write and stats["out"] < stats["in"]:
        open(a.path, "w", newline="", encoding="utf-8").write(CRLF.join(out) + CRLF)


if __name__ == "__main__":
    main()
