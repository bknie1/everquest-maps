"""poi_audit.py -- check every zone's POIs against its wiki page.

Born from a real bug: Butcherblock's "Aqua Goblin Camp (Shore)" sat inland by
Kaladim's gate because its coordinate came from an unlabelled wiki row whose
neighbour row read "Lake Rathetear:". Shared mobs appear on many zone pages and
their Location cells often carry ANOTHER zone's coordinates. Take those at face
value and you place a camp in the wrong zone entirely.

So this reads each mob's own Location cell, drops any cell naming a different
zone, converts with the project transform (native = -loc_b, -loc_a), and reports
POIs that match nothing nearby.

    python src/tools/poi_audit.py                 # whole pack
    python src/tools/poi_audit.py butcher paw     # named zones
    python src/tools/poi_audit.py --far 400       # tighten the match radius
"""
import argparse
import glob
import math
import os
import re
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))
from fix_title import content_bbox  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
WIKI = os.path.join(HERE, "..", "data", "wiki")

# a Location cell that names one of these is quoting another zone's coordinates
ZONE_WORDS = (r"Lake Rathetear|Ocean of Tears|Greater Faydark|Lesser Faydark|Dagnor|Steamfont|"
              r"Crushbone|Unrest|Mistmoore|Kithicor|Commonlands|East Commons|West Commons|"
              r"Freeport|Qeynos|Nektulos|Innothule|Befallen|Oasis|Desert of Ro|North Ro|South Ro|"
              r"Everfrost|Halas|Blackburrow|Erudin|Paineel|Kerra|Highpass|Rathe|Feerrott|Oggok|"
              r"Grobb|Neriak|Kaladim|Butcherblock|Guk|Splitpaw|Runnyeye|Permafrost|Solusek|"
              r"Najena|Cazic|Toxxulia|Warrens|Stonebrunt|Karana|Misty|Rivervale|Gorge")
CROSS = re.compile(r"(%s)[^,]{0,24}:" % ZONE_WORDS, re.I)
SKIP = ("Slot", "Class", "Race", "WT", "AC", "DMG", "SV", "Skill", "Size", "MAGIC",
        "Focus", "Attunable", "|", "(", "*", "Effect", "HP", "Atk", "Quest")
# these legitimately have no mob to match: mechanics and doorways
NO_MOB = re.compile(r"^(to_|To_|Succor|zone_line)|Succor|_Gate$|Portal", re.I)
# speculative LDoN arrows live in the margin on purpose -- not errors
SPECULATIVE = re.compile(r"\(LDoN\?\)$")


def wiki_spawns(zone):
    """Every in-zone spawn coordinate the page documents, as native (x, y)."""
    p = os.path.join(WIKI, zone + ".md")
    if not os.path.exists(p):
        return None
    lines = [l.rstrip("\n") for l in open(p, encoding="utf-8")]
    out, dropped = [], 0
    for i, l in enumerate(lines):
        if l.strip() != "|" or i < 1:
            continue
        nm = lines[i - 1].strip()
        if not nm or len(nm) > 46 or nm.startswith(SKIP):
            continue
        cells = [x.strip().rstrip("|").strip() for x in lines[i + 1:i + 6]]
        if len(cells) < 4:
            continue
        cell = cells[3]
        if CROSS.search(cell):
            dropped += 1
            continue
        for a, b in re.findall(r"\(\s*(-?\d{1,5})\s*,\s*(-?\d{1,5})\s*\)", cell):
            out.append((nm, -int(b), -int(a)))
    return out, dropped


def pfields(l):
    """'P-922...' and 'P 922...' both occur; [2:] would eat the minus sign."""
    return [x.strip() for x in l[1:].lstrip().split(",")]


def audit(zone, far):
    spawns = wiki_spawns(zone)
    if spawns is None:
        return None
    spawns, dropped = spawns
    p1 = os.path.join(MAPS, zone + "_1.txt")
    if not os.path.exists(p1):
        return None
    X0, X1, Y0, Y1 = content_bbox(zone)
    rows = []
    for l in open(p1, encoding="utf-8"):
        l = l.strip()
        if l[:1] != "P":
            continue
        f = pfields(l)
        if len(f) < 8:
            continue
        x, y, lab = float(f[0]), float(f[1]), f[7]
        if SPECULATIVE.search(lab):
            continue
        outside = not (X0 - 300 < x < X1 + 300 and Y0 - 300 < y < Y1 + 300)
        if NO_MOB.search(lab):
            rows.append((lab, x, y, None, None, outside))
            continue
        if not spawns:
            rows.append((lab, x, y, None, None, outside))
            continue
        best = min(spawns, key=lambda s: math.hypot(s[1] - x, s[2] - y))
        rows.append((lab, x, y, best[0], math.hypot(best[1] - x, best[2] - y), outside))
    return rows, len(spawns), dropped


def norm(name):
    return re.sub(r"[^a-z0-9 ]", "", name.replace("_", " ").lower()).strip()


def coverage(zone, far):
    """The inverse audit: which wiki-documented spawns have NO POI at all?
    A spawn counts as covered by a nearby POI (within --far of its
    transformed coordinate) or by a name match (normalized substring either
    way). Returns (documented, covered, [missing names])."""
    spawns = wiki_spawns(zone)
    p1 = os.path.join(MAPS, zone + "_1.txt")
    if spawns is None or not os.path.exists(p1):
        return None
    spawns, _ = spawns
    if not spawns:
        return None
    pois = []
    for l in open(p1, encoding="utf-8"):
        l = l.strip()
        if l[:1] != "P":
            continue
        f = pfields(l)
        if len(f) >= 8:
            pois.append((float(f[0]), float(f[1]), norm(f[7])))
    missing = []
    covered = 0
    seen = set()
    generic = re.compile(r"^(a|an|the)\s", re.I)
    for nm, sx, sy in spawns:
        key = norm(nm)
        if key in seen:            # multi-loc spawns count once
            continue
        if generic.match(nm):      # wandering trash is not POI material
            continue
        seen.add(key)
        by_dist = any(math.hypot(px - sx, py - sy) < far for px, py, _ in pois)
        by_name = any(key and (key in pl or pl in key) and len(key) > 5
                      for _, _, pl in pois)
        if by_dist or by_name:
            covered += 1
        else:
            missing.append(nm)
    return len(seen), covered, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zones", nargs="*")
    ap.add_argument("--far", type=float, default=700.0,
                    help="flag a POI whose nearest documented spawn is beyond this")
    ap.add_argument("--coverage", action="store_true",
                    help="report wiki spawns with no POI (completeness, not accuracy)")
    args = ap.parse_args()
    if args.coverage:
        zones = args.zones or sorted(
            os.path.basename(q)[:-4] for q in glob.glob(os.path.join(MAPS, "*_1.txt")))
        zones = [z[:-2] if z.endswith("_1") else z for z in zones]
        rows = []
        for z in zones:
            r = coverage(z, args.far)
            if r:
                rows.append((r[1] / r[0], z) + r)
        rows.sort()
        print("%-15s %9s  %s" % ("zone", "coverage", "missing (first few)"))
        for frac, z, doc, cov, missing in rows:
            print("%-15s %4d/%-4d  %s" % (z, cov, doc,
                  "; ".join(missing[:4]) + (" ..." if len(missing) > 4 else "")))
        return
    zones = args.zones or sorted(
        os.path.basename(q)[:-4] for q in glob.glob(os.path.join(MAPS, "*_1.txt")))
    zones = [z[:-2] if z.endswith("_1") else z for z in zones]
    flagged = 0
    for z in zones:
        r = audit(z, args.far)
        if not r:
            continue
        rows, nspawn, dropped = r
        bad = [t for t in rows if t[5] or (t[4] is not None and t[4] > args.far)]
        if not bad:
            continue
        print("%s  (%d in-zone spawns documented, %d cross-zone rows dropped)"
              % (z, nspawn, dropped))
        for lab, x, y, near, d, outside in bad:
            why = "OUTSIDE ZONE" if outside else "nearest '%s' %.0f away" % (near, d)
            print("    %-42s (%8.1f,%9.1f)  %s" % (lab[:42], x, y, why))
            flagged += 1
    print("\n%d POIs flagged across %d zones" % (flagged, len(zones)))


if __name__ == "__main__":
    main()
