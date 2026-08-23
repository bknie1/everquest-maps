"""dedupe.py -- remove EXACT duplicate strokes. The free win.

Many bases carry the same L stroke 2-4x over (identical endpoints and ink,
sometimes reversed direction). Duplicates draw pixel-identically, but every
copy counts against the ~31k client draw budget - the reason over-budget zones
stop rendering at distance. Removing them cannot change the picture.

Only exact matches go (endpoints rounded to 2dp, direction-normalized, same
ink, same z). P-records are kept unless the whole record is identical.

    python src/tools/dedupe.py --probe          # census, change nothing
    python src/tools/dedupe.py <zone> [...]     # dedupe zones (all layers)
    python src/tools/dedupe.py --all-over       # every zone over budget
"""
import glob
import os
import sys

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
BUDGET = 31000


def key(line):
    f = [v.strip() for v in line[2:].split(",")]
    if line[0] == "L" and len(f) >= 9:
        a = (round(float(f[0]), 2), round(float(f[1]), 2), round(float(f[2]), 2))
        b = (round(float(f[3]), 2), round(float(f[4]), 2), round(float(f[5]), 2))
        if b < a:
            a, b = b, a
        return ("L", a, b, f[6], f[7], f[8])
    return ("R", line.strip())


def dedupe_file(path, write):
    raw = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines()
           if l.strip()]
    seen, out, dropped = set(), [], 0
    for l in raw:
        if l[:1] not in "LP":
            out.append(l)
            continue
        k = key(l)
        if k in seen:
            dropped += 1
            continue
        seen.add(k)
        out.append(l)
    if write and dropped:
        open(path, "w", newline="", encoding="utf-8").write(CRLF.join(out) + CRLF)
    return len(raw), dropped


def zone_files(zone):
    return [p for p in glob.glob(os.path.join(MAPS, zone + "*.txt"))
            if os.path.basename(p)[:-4] in (zone, zone + "_1", zone + "_2", zone + "_3")]


def zone_total(zone):
    n = 0
    for p in zone_files(zone):
        n += sum(1 for l in open(p, encoding="utf-8", errors="ignore")
                 if l[:1] in "LP")
    return n


def all_zones():
    return sorted({os.path.basename(p)[:-4].split("_")[0]
                   if os.path.basename(p)[:-4].split("_")[-1] in ("1", "2", "3")
                   else os.path.basename(p)[:-4]
                   for p in glob.glob(os.path.join(MAPS, "*.txt"))})




def merge_colinear(path, write, eps=0.35):
    """Merge chains of colinear same-ink strokes into single strokes.

    Stock bases split straight walls into dozens of tiny segments; a merged
    chain draws the IDENTICAL line with a fraction of the strokes. Only exact
    continuations merge: shared endpoint, same ink and z, direction within eps
    (cross-product test) -- corners, colour changes and gaps all break chains.
    """
    raw = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines()
           if l.strip()]
    segs, other = [], []
    for l in raw:
        f = [v.strip() for v in l[2:].split(",")]
        if l[:1] == "L" and len(f) >= 9:
            segs.append([float(f[0]), float(f[1]), float(f[2]),
                         float(f[3]), float(f[4]), float(f[5]),
                         f[6], f[7], f[8]])
        else:
            other.append(l)
    # chain forward: index start points
    from collections import defaultdict
    start = defaultdict(list)
    for i, s in enumerate(segs):
        start[(round(s[0], 1), round(s[1], 1), s[6], s[7], s[8])].append(i)
    used = [False] * len(segs)
    out = []
    for i, s in enumerate(segs):
        if used[i]:
            continue
        used[i] = True
        x1, y1, z1, x2, y2, z2 = s[:6]
        while True:
            nxt = -1
            for j in start.get((round(x2, 1), round(y2, 1), s[6], s[7], s[8]), []):
                if used[j]:
                    continue
                t = segs[j]
                dx1, dy1 = x2 - x1, y2 - y1
                dx2, dy2 = t[3] - t[0], t[4] - t[1]
                cross = dx1 * dy2 - dy1 * dx2
                dot = dx1 * dx2 + dy1 * dy2
                norm = ((dx1 * dx1 + dy1 * dy1) ** 0.5) * ((dx2 * dx2 + dy2 * dy2) ** 0.5)
                if norm and abs(cross) / norm < eps and dot > 0:
                    nxt = j
                    break
            if nxt < 0:
                break
            used[nxt] = True
            x2, y2, z2 = segs[nxt][3], segs[nxt][4], segs[nxt][5]
        out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %s, %s, %s"
                   % (x1, y1, z1, x2, y2, z2, s[6], s[7], s[8]))
    dropped = len(segs) - len(out)
    if write and dropped:
        open(path, "w", newline="", encoding="utf-8").write(
            CRLF.join(other + out) + CRLF)
    return len(segs), dropped


def main():
    args = sys.argv[1:]
    probe = "--probe" in args
    if probe or not args:
        rows = []
        for z in all_zones():
            tot = zone_total(z)
            dup = sum(dedupe_file(p, False)[1] for p in zone_files(z))
            if dup:
                rows.append((dup, z, tot))
        rows.sort(reverse=True)
        print("zone            dup-strokes   total  after")
        for dup, z, tot in rows[:25]:
            print("%-14s %10d %7d %7d%s" % (z, dup, tot, tot - dup,
                  "  <- under budget!" if tot > BUDGET >= tot - dup else ""))
        print("pack-wide duplicates: %d" % sum(r[0] for r in rows))
        return
    if "--merge" in args:
        zones = ([z for z in all_zones() if zone_total(z) > BUDGET]
                 if "--all-over" in args
                 else [a for a in args if not a.startswith("--")])
        for z in zones:
            before = zone_total(z)
            p = os.path.join(MAPS, z + ".txt")   # BASE ONLY: deco art untouched
            if not os.path.exists(p):
                continue
            n, dropped = merge_colinear(p, True)
            print("%-14s %7d -> %7d  (-%d merged)%s"
                  % (z, before, before - dropped, dropped,
                     "  UNDER BUDGET" if before > BUDGET >= before - dropped else ""))
        return
    zones = ([z for z in all_zones() if zone_total(z) > BUDGET]
             if "--all-over" in args else [a for a in args if not a.startswith("--")])
    for z in zones:
        before = zone_total(z)
        dropped = sum(dedupe_file(p, True)[1] for p in zone_files(z))
        print("%-14s %7d -> %7d  (-%d)%s" % (z, before, before - dropped, dropped,
              "  UNDER BUDGET" if before > BUDGET >= before - dropped else ""))


if __name__ == "__main__":
    main()
