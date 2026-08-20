"""clear_title_artifacts.py -- delete stray EQOA arrows that pierce the title.

Across the pack, many zones carry bare up-arrows in the _3 (EQOA historical)
layer, ink (150,90,150), parked in the TOP MARGIN where the title lives. They
have no label and no business above the map -- legit historical markers sit over
the content, and legit zone-exit arrows carry a P-label in the side/bottom
margins. So the rule is safe and mechanical:

    remove _3 strokes whose midpoint is above the grid top AND ink is EQOA violet

The _2 (title/frame/compass) and everything over content are never touched.

    python src/tools/clear_title_artifacts.py --scan          # list affected zones
    python src/tools/clear_title_artifacts.py qeytoqrg misty  # clean these
    python src/tools/clear_title_artifacts.py --all           # clean every affected zone
"""
import glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kit"))
from fix_title import content_bbox
from layout import layout

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
EQOA = (150, 90, 150)


def grid_top(zone):
    return layout(content_bbox(zone))["grid"][2]


LABEL_R = 380.0  # a stroke this close to a _3 label belongs to a labeled exit


def artifacts(zone):
    """Indices/lines of _3 violet strokes above the grid top that are BARE --
    not part of a labeled zone-exit. A labeled north-exit ('To Mt. Hatespike')
    is legit and kept; a bare arrow piercing the title is the artifact."""
    p = os.path.join(MAPS, zone + "_3.txt")
    if not os.path.exists(p):
        return None, []
    gy0 = grid_top(zone)
    raw = [l for l in open(p, encoding="utf-8").read().splitlines() if l.strip()]
    labels = []  # _3 P-records anywhere in the top margin
    for l in raw:
        if l[:1] == "P":
            f = l[2:].split(",")
            if float(f[1]) < gy0:
                labels.append((float(f[0]), float(f[1])))
    hits = []
    for i, l in enumerate(raw):
        if l[:1] != "L":
            continue
        f = l[2:].split(",")
        mx = (float(f[0]) + float(f[3])) / 2
        my = (float(f[1]) + float(f[4])) / 2
        ink = (int(f[6]), int(f[7]), int(f[8]))
        if my < gy0 and ink == EQOA:
            near_label = any((mx - lx) ** 2 + (my - ly) ** 2 < LABEL_R ** 2
                             for (lx, ly) in labels)
            if not near_label:
                hits.append(i)
    return raw, hits


def clean(zone, probe=False):
    raw, hits = artifacts(zone)
    if raw is None:
        return None
    if not hits:
        return 0
    if probe:
        return len(hits)
    keep = [l for i, l in enumerate(raw) if i not in set(hits)]
    open(os.path.join(MAPS, zone + "_3.txt"), "w", newline="", encoding="utf-8").write(
        CRLF.join(keep) + CRLF)
    return len(hits)


def all_zones():
    zs = set()
    for p in glob.glob(os.path.join(MAPS, "*_3.txt")):
        zs.add(os.path.basename(p)[:-6])
    return sorted(zs)


def main():
    args = sys.argv[1:]
    if not args or "--scan" in args:
        total = 0
        for z in all_zones():
            n = clean(z, probe=True)
            if n:
                print(f"  {z:16s} {n} stray arrow-strokes")
                total += n
        print(f"scan: {total} strokes across affected zones")
        return
    zones = all_zones() if "--all" in args else [a for a in args if not a.startswith("--")]
    grand = 0
    for z in zones:
        n = clean(z)
        if n:
            print(f"{z}: removed {n} stray _3 arrow-strokes")
            grand += n
    print(f"done: removed {grand} strokes across {len(zones)} zones")


if __name__ == "__main__":
    main()
