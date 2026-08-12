# Sources

Reference material consulted while drawing the atlas. The large third-party map
packs are **not vendored here** — they are tens of megabytes and belong to their
authors. Fetch them yourself if you need to re-derive geometry.

## What was used

- **Community base traces (the "default" pack)** — the geometry these maps were
  built on. Used to restore a zone when its base has accumulated too many passes to
  patch cleanly; that is how Kerra Isle and Paineel were rebuilt.
- **Brewall's pack** — consulted for shoreline outlines when our own trace of a
  water body is fragmentary, and for its Z-level colour convention in multi-floor
  dungeons. Geometry and colour convention only.
- **Norrath Cartographers ("best") pack** — a newer cut of the same community
  traces. Better closed water outlines in several outdoor zones.

No points of interest are taken from any of them. Those target EverQuest Live and
carry content that does not exist on EQL or P1999; POI authority is EQL and P1999.

## What is kept here

- `neriak_clean_source.zip` — small, and specific to this project's Neriak rebuild.

## If you need a pack

Drop it in this folder and point the relevant script at it. Nothing in the build
depends on these being present — they are only used for one-off derivations.
