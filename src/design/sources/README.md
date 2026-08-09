# Source archive

Kept so a rebuild never depends on a file that has gone missing.

| file | what it is |
|---|---|
| `default_maps.zip` | the stock in-game map pack. The reference for hand-drawn assets — logs, fallen trees, sketched features — that our rebuilds must not lose. Diff against it per line, not per cluster: a partly-copied asset will pass a cluster test while still missing half its lines. |
| `neriak_clean_source.zip` | untouched Neriak base geometry (Norrath Cartographers trace). Those thousands of 2–3 unit segments are the city itself, not texture — thinning them deletes buildings. |

Not archived here: Brewall's and Good's packs. They were consulted once for base
geometry, target EverQuest Live, and carry content that does not exist on EQL or
P1999. POI authority stays with EQL and P1999.
