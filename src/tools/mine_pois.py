"""mine_pois.py -- add wiki-documented notables that have no POI yet.

The coverage metric's fix. For each zone: take the wiki spawns poi_audit
--coverage reports missing (named notables only -- wandering a/an/the trash
is excluded there), keep the first in-zone coordinate per name, skip anything
within --near of an existing POI, and append house-convention records:

    P x, y, -1.0000, 165, 60, 20, 2, Name_(Notable)

(the regular-notable ink/size from crushbone's slate). Labels are sanitized:
spaces to underscores, commas and pipes dropped -- a comma splits the P
record. z is a placeholder; run ground_pois.py after to set real floors.

    python src/tools/mine_pois.py oasis --probe
    python src/tools/mine_pois.py oasis stonebrunt sro --write
"""
import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from poi_audit import wiki_spawns, pfields, norm, coverage  # noqa: E402
from fix_title import content_bbox  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"


def sanitize(name):
    s = re.sub(r"[,|]", "", name.strip())
    s = re.sub(r"\s+", "_", s)
    return s


def mine(zone, near, write):
    cov = coverage(zone, 500)
    if not cov:
        print("%-13s no wiki/POI data" % zone)
        return 0
    _, _, missing = cov
    if not missing:
        print("%-13s nothing missing" % zone)
        return 0
    missing_keys = {norm(n) for n in missing}
    spawns, _ = wiki_spawns(zone)
    X0, X1, Y0, Y1 = content_bbox(zone)

    p1 = os.path.join(MAPS, zone + "_1.txt")
    lines = [l for l in open(p1, encoding="utf-8", errors="ignore").read().splitlines()
             if l.strip()] if os.path.exists(p1) else []
    existing = []
    for l in lines:
        if l[:1] == "P":
            f = pfields(l)
            if len(f) >= 8:
                existing.append((float(f[0]), float(f[1])))

    added, seen = [], set()
    for nm, sx, sy in spawns:
        key = norm(nm)
        if key not in missing_keys or key in seen:
            continue
        seen.add(key)
        if not (X0 - 300 < sx < X1 + 300 and Y0 - 300 < sy < Y1 + 300):
            continue                       # wiki coord outside the zone: distrust
        if any(math.hypot(px - sx, py - sy) < near for px, py in existing):
            continue
        label = sanitize(nm) + "_(Notable)"
        added.append("P %.4f, %.4f, -1.0000, 165, 60, 20, 2, %s" % (sx, sy, label))
        existing.append((sx, sy))

    print("%-13s +%d POIs (of %d missing)%s"
          % (zone, len(added), len(missing), "  WRITTEN" if write and added else ""))
    if write and added:
        open(p1, "w", newline="", encoding="utf-8").write(
            CRLF.join(lines + added) + CRLF)
    return len(added)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zones", nargs="+")
    ap.add_argument("--near", type=float, default=80.0)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    total = 0
    for z in a.zones:
        total += mine(z, a.near, a.write)
    print("total added:", total)


if __name__ == "__main__":
    main()
