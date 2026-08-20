# Our map: the data contract

A concept-led map of systems, cybernetics and complexity, with citation
evidence underneath every line.

This is **not** the Necessary Tangle dataset. It is built fresh in `map/` from
the Scopus corpus and public sources. The atlas in `data/` is a reference
implementation we read and learn from; we do not inherit its content, because it
is CC BY-SA 4.0 and carries another curator's editorial decisions.

## What the three prior maps gave us

Ideas and a coverage checklist, not content:

- **Map of Systemic Evolution** (Schwarz 1996 → Hadorn 2016) — the historical
  spread, and the negative lesson: 1,320 lines that say nothing.
- **The Necessary Tangle** (Taylor) — the principle that a line must state its
  meaning, and the vocabulary of distinct relation families.
- **Map of the Complexity Sciences** (Castellani) — the complexity strand and
  its strand-based layout.

## The rule this map is built on

> A concept is on the map because it has a literature.
> A line is on the map because that literature cites across it.

Both are counted, not asserted. Every node carries the number of works that
place it there; every edge carries the number of references that support it and
examples you can look up.

## Nodes

Concepts are primary. Works and people are evidence, not scenery.

| Field | Meaning |
| --- | --- |
| `id` | stable slug, `concept_<name>` |
| `label` | reader-facing name |
| `aliases` | spellings and variants matched when counting |
| `work_count` | works in the on-topic corpus whose title matches |
| `first_year` / `last_year` | earliest and latest matching work |
| `exemplar_works` | up to five DOIs, most cited first |
| `strand` | editorial grouping, provisional and marked as such |
| `status` | `evidenced` (meets threshold) or `candidate` (below it) |

A concept below the evidence threshold stays visible as a `candidate`. Absence
of literature in one database is a fact about the database as much as the idea.

## Edges

One relation type at the base of the map, and it is deliberately modest:

| Field | Meaning |
| --- | --- |
| `source` / `target` | concept ids |
| `relation_type` | `literature_cites` |
| `plain_phrase` | "work on X cites work on Y" |
| `weight` | number of supporting references |
| `citing_work_count` | distinct citing works, so one prolific author cannot carry an edge |
| `first_year` / `last_year` | span of the supporting references |
| `evidence` | up to five citing DOIs with the matched reference string |
| `directed` | always true; citation runs from later work to earlier |

### What `literature_cites` does not mean

It is not influence, teaching, agreement, derivation or logical dependence. It
means what it says: papers about one idea cite papers about another, this many
times. Anything stronger needs its own evidence and its own relation type, added
later and separately.

Edges are omitted below a minimum weight and a minimum distinct-citing-work
count, so a single author citing themselves cannot create a line.

## Rights

Scopus records are licensed and not redistributable. Only counts, DOIs, years
and concept names derived from them enter `map/data/`. No abstract, keyword list
or Scopus metadata field is committed. The build reads the corpus from a path
given at run time; the corpus itself is never committed.
