"""gen_manifest.py -- write maps-manifest.json for the hosted previewer.

The previewer (preview.html at the repo root) auto-loads maps from this repo
when served over http(s), giving a live view of map progress. It needs to know
which zones and layers exist -- that's this manifest. Regenerate it whenever
zones or layers are added or removed:

    python src/tools/gen_manifest.py
"""
import json
import os

REPO = os.path.join(os.path.dirname(__file__), "..", "..")
FOLDER = "Emoda Legends Maps"


def main():
    src = os.path.join(REPO, FOLDER)
    zones = {}
    for f in sorted(os.listdir(src)):
        if not f.endswith(".txt"):
            continue
        base, key = f[:-4], "0"
        for suf in ("_1", "_2", "_3"):
            if base.endswith(suf):
                base, key = base[:-2], suf[1]
                break
        if os.path.getsize(os.path.join(src, f)) > 0:
            zones.setdefault(base, []).append(key)
    man = {"folder": FOLDER, "zones": {z: sorted(v) for z, v in sorted(zones.items())}}
    out = os.path.join(REPO, "maps-manifest.json")
    with open(out, "w", newline="\n", encoding="utf-8") as fh:
        fh.write(json.dumps(man, separators=(",", ":")))
    print(f"{len(man['zones'])} zones, {sum(len(v) for v in man['zones'].values())} layers -> {out}")


if __name__ == "__main__":
    main()
