# Rebuilding the map from nothing

The working container is ephemeral. This file exists so that losing it costs
about twenty minutes rather than the project.

## What lives where

| Thing | Where it is | Recoverable? |
| --- | --- | --- |
| Build scripts, vocabulary, validator, view renderer | this repo | yes, git |
| `map/data/concepts.json`, `map/data/edges.json` | this repo | yes, git |
| Raw Scopus exports (8 files, ~1.7 GB) | the curator's Google Drive | yes, Drive |
| Shrunk corpus (`scopus_works.csv`, `scopus_refs.csv`) | container only | **regenerate, step 2** |
| Map of Systemic Evolution GraphML | received by email; published at uranos.ch | yes, external |

Nothing that cannot be regenerated exists only in the container.

## Rebuild

**1. Fetch the raw exports.** Download the Scopus CSVs from Drive into one
folder. They are ordinary exports; the only thing that matters is that each was
taken with the **References** column selected.

**2. Shrink them** (~2 minutes for 1.7 GB):

```bash
python3 scopus_shrink.py /path/to/raw-exports --out corpus
```

Writes `corpus/scopus_works.csv` and `corpus/scopus_refs.csv`, dropping
abstracts and keywords. Check `corpus/scopus_report.txt` — if it reports
`references 0/N` for any file, that export was taken without the References
column and must be redone.

**3. Build the map** (~12 minutes for 13.8M reference rows):

```bash
python3 map/build/build_map.py --corpus corpus
python3 map/build/validate_map.py
python3 map/build/render_view.py
```

The build is deterministic: the same corpus and the same vocabulary give the
same `concepts.json` and `edges.json` byte for byte.

## Expected output at the current corpus

85,832 documents, 13,792,287 reference rows, 15,406 works matching at least one
concept, 89 of 98 concepts evidenced, 1,856 edges, 291 flagged concentrated.

If your numbers differ, the corpus differs — check the file count and the
per-file document counts in `scopus_report.txt` before suspecting the build.

## Adding coverage

Concepts are tested whether or not they have literature, so widening the map is
a matter of widening the corpus, not editing the data. Add a topic-scoped Scopus
export, re-run steps 2 and 3, and any concept whose literature has arrived will
cross the threshold on its own. `COMPARISON.md` records which areas are still
waiting and the queries that would find them.
