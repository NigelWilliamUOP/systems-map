# Plan: integrating the *Systemic Evolution* GraphML as a comparator corpus

Status: **Draft — awaiting curator decision on Packet A**

Owner: **Curator (Benjamin P Taylor), with Nigel Williams proposing**

Human review point: **Packet A cannot start until the licence and provenance gate
in section 2 is cleared.**

This plan describes how a 650-node, 1,320-edge yEd map of the systems sciences
(`systemic_evolution.graphml`) can be brought into this repository without
breaking the atlas's core rule that every published connection must say what it
means.

## 1. What the source actually contains

Measured directly from the file, not summarised from its description:

| Property | Value |
| --- | --- |
| Format | GraphML with yFiles extensions, written by yEd 3.15.0.1 |
| Nodes | 650, all round rectangles, no group or nested-graph structure |
| Edges | 1,320, of which 1,262 are single-headed and 58 double-headed |
| Edge labels | **0** — no edge carries any text |
| Node labels | 650, all non-empty; free text mixing a concept, one or more people and sometimes a year |
| Nodes with an explicit `[year]` | 16 |
| Node border colours | 13 distinct, at widths 2.0, 6.0 and 7.0 |
| Node fills | 618 white, 32 pale yellow (`#FFFF99`) |
| Edge line colours | 15 distinct, at widths 2.0 and 4.0, plus 15 dashed edges |
| `description` / `url` GraphML keys | Declared in the schema, never populated |

The apparent colour streams, by node count:

| Border colour | Nodes | Apparent stream |
| --- | --- | --- |
| `#999999` | 139 | Philosophy, semiotics of meaning, media, epistemology |
| `#FFCC00` | 84 | Social theory, constructivism, psychology, culture |
| `#008000` | 73 | General systems and biology-derived systems theory |
| `#0000FF` | 73 | Mathematics, statistics, formal systems theory |
| `#000000` | 56 | Physical science, astronomy, history of science |
| `#FFFF00` | 52 | Semiotics, linguistics, logic of signs |
| `#800000` | 49 | Computing, information, agents, coordination |
| `#FF0000` | 18 | Cybernetics proper |
| `#00CCFF` | 18 | Operational research and decision science |
| `#00FF00` | 18 | Ecology and environmental systems |
| `#FF00FF` | 19 | Engineering and instrument-making |
| `#666699` | 1 | *International Encyclopedia of Systems & Cybernetics* (François, 1997) |

The 32 pale-yellow nodes form a coherent late cluster — coordination theory,
CSCW, HCI, speech-act theory, agent-based modelling, ubiquitous computing,
Yolles's knowledge cybernetics, Morin's philosophy of complexity — which reads
as the map author's own contribution zone rather than as inherited canon.

### 1.1 The decisive problem

**Every edge in the file is unlabelled.** All 1,320 relationships express their
meaning through line colour, width and dash pattern alone. The atlas's published
semantic contract states the opposite rule:

> Position, colour and algorithmic neighbourhood do not assert an unstated
> relation.
> — `data/public-data.json`, `semantic_contract.visual_rule`

and `documentation/DESIGN_AND_CONTENT_RULES.md` rule 1 forbids generic edges
created to produce reach. So **none of the 1,320 edges can be imported into
`data/public-data.json` as atlas edges in their current form**, and no colour can
be silently translated into a relation type. Doing either would import 1,320
unevidenced claims and inflate `reader_connected_entry_count` dishonestly.

This is not a reason to reject the map. It is the reason the map enters as a
**comparator corpus**, and individual statements are then re-derived from
citable sources — which is exactly the route `corpus_comparator_maps` (issue 6)
already reserves for prior maps.

### 1.2 Overlap with the current atlas

Two measurements against the 691 nodes in `data/public-data.json`:

- **Strict** (first-initial + surname adjacency against the 195 `person`
  entries): **31 of 650** GraphML nodes match **30 distinct atlas people**.
- **Loose** (any atlas label or alias appearing as a substring): 86 of 650, but
  with heavy false-positive noise — most "matches" are the bare words
  *cybernetics*, *systems theory* or *science*.

One real failure from the strict pass is worth keeping in front of the curator:
the GraphML node *"Quaternions / William Hamilton"* matched the atlas person
**W. D. Hamilton**. That is William Rowan Hamilton the mathematician against
W. D. Hamilton the evolutionary biologist — two different people, and a merge
that no automated pass should ever be trusted to make unsupervised.

Ludwig von Bertalanffy, the map's own root node, has **no** `person` entry in
the current atlas at all.

The honest headline: the two datasets overlap far less than their shared subject
suggests. The atlas is strong on UK practice lineage, SCiO, Cynefin, the Viable
System Model, intervention skills and the *Grammar of Systems* laws. The GraphML
is strong on pre-1950 lineage — astronomy, rational mechanics, logic,
instrument-making, early biology — and on computing, semiotics and coordination.
Most of its 650 nodes are genuinely new material, which is why identity
reconciliation, not import, is the expensive step.

## 2. Gates that must clear before any code is written

These are blockers, not preliminaries.

1. **Licence and provenance of the GraphML.** `RIGHTS.md` licenses atlas content
   CC BY-SA 4.0 and states that third-party works keep their own terms. The file
   carries no author, licence, URL or `description` metadata. Before any node
   text or structure is published we need: who made it, when, where it was
   published, and under what terms. Three outcomes:
   - *Open licence, compatible* — the comparator dataset may include raw labels
     with attribution.
   - *Open licence, incompatible, or all-rights-reserved* — publish only the
     comparison and analysis; keep raw labels out of the public dataset.
   - *Unknown* — treat the file as a private working input. Nothing derived from
     it is published until statements are independently re-sourced.

   **Until this clears, the `.graphml` file is not committed to this
   repository.** It is deliberately absent from this plan's file list.

2. **Fork or upstream.** This checkout is `NigelWilliamUOP/systems-map`; the
   dataset's own `meta.repository_url` and every documentation link point to
   `antlerboy/the-necessary-tangle`, and `GOVERNANCE.md` names Benjamin P Taylor
   as accountable for published releases. Decide whether this work is a proposal
   upstream (in which case the comparator dataset should be shaped for a PR) or a
   divergent fork (in which case `meta`, `RIGHTS.md` and the site URLs need an
   explicit statement of the fork's own status).

3. **`documentation/NEXT_WORK.md` currently says no packet is active.** Packet A
   below has to replace the holding content, with curator agreement, before
   implementation begins.

### 2.1 Two repository facts found while preparing this plan

Both affect any data change and should be fixed first.

- **`make validate` fails on Python 3.11.** `scripts/apply_relational_depth_16.py`
  line 989 uses a backslash inside an f-string expression, which is only legal
  from Python 3.12 (PEP 701). On Python 3.12 the full `make validate` passes
  clean. The repository has no `.python-version`, no `pyproject.toml` and no
  documented interpreter floor; `.github/workflows/validate.yml` should be
  checked against this and the minimum recorded.
- **`make build` is not a fixed point of the committed tree.** Running it on a
  clean checkout of `main` changes tracked files: `node_count` 675 → 691,
  `edge_count` 1809 → 1826, `public_link_source_count` 171 → 181,
  `semantic_connected_entry_count` 382 → 397, plus README status figures and
  around 1,400 changed lines across `data/` and `docs/assets/`. The committed
  0.17 artefact was deployed directly rather than regenerated, so the overlay
  scripts still have work to apply.

  This matters because a new comparator overlay would be indistinguishable from
  this pre-existing drift. **Reconcile the tree to a build fixed point, in its own
  commit, before adding anything.**

## 3. Programme shape

Six packets. Only Packet A is specified in full; the rest are sketched so the
sequence and the cost profile are visible. One packet at a time, each through
`NEXT_WORK.md`, each merged by review.

| Packet | Outcome | Depends on | Size |
| --- | --- | --- | --- |
| A | Deterministic extraction to a comparator dataset | Gates 1–3, §2.1 | Small, mechanical |
| B | Identity reconciliation against atlas canonical IDs | A | Large, human-judgement bound |
| C | Bibliographic grounding from OpenAlex and Scopus | B, your exports | Medium |
| D | First promotion cohort: 40–60 evidenced statements | C | Medium, curator-bound |
| E | Public comparator page satisfying issue 6 | A, B | Medium |
| F | Validation, registers, release | all | Small |

---

## Packet A — deterministic extraction

Status: **Ready to specify** (blocked on gates)

### Outcome

The GraphML is represented as a separate, machine-checkable comparator dataset
that asserts nothing about what any line means.

### Primary deliverable

`data/comparator-systemic-evolution.json`, produced by
`scripts/import_comparator_graphml.py`.

### In scope

- Parse the 650 nodes to records of: `source_node_id`, `raw_label` (verbatim,
  line breaks preserved), `parsed_concept`, `parsed_people[]`, `parsed_year`,
  `border_colour`, `border_width`, `fill_colour`, `font_size`, `x`, `y`.
- Parse the 1,320 edges to records of: `source_node_id`, `target_node_id`,
  `line_colour`, `line_width`, `line_style`, `source_arrow`, `target_arrow`,
  and two fixed fields — `relation_type: null` and
  `meaning: "unstated_in_source"`.
- Emit the colour census in section 1 to
  `documentation/comparator-systemic-evolution.md`, with an explicit statement
  that colour is the only available signal and that the atlas does not infer
  relation semantics from it.
- Record parse counts in the dataset's own `meta` block.

### Out of scope

- Any `relation_type`, `relation_family` or `plain_phrase` on a comparator edge.
- Any write to `data/public-data.json`.
- Any colour-to-category translation table presented as the map author's intent.
- Committing the `.graphml` source file (see gate 1).

### Named files or areas

- `scripts/import_comparator_graphml.py` (new)
- `data/comparator-systemic-evolution.json` (new)
- `documentation/comparator-systemic-evolution.md` (new)

### Acceptance checks

- [ ] Output contains exactly 650 node records and 1,320 edge records.
- [ ] Every edge record has `relation_type: null` and
      `meaning: "unstated_in_source"`; zero exceptions.
- [ ] Re-running the script produces a byte-identical file.
- [ ] `git diff data/public-data.json docs/` is empty after the run.
- [ ] `make validate` passes on Python 3.12.
- [ ] Human review occurs before merge.

### Route and model

Surface **Codex**, model **Luna**. This is XML extraction with a fixed schema and
no judgement. Escalate only if the label-parsing heuristic for
concept-versus-person cannot reach a stated accuracy on a 50-node hand check.

---

## Packet B — identity reconciliation

The expensive packet, and the one that must not be automated.

Produce `data/comparator-systemic-evolution-reconciliation.json` sorting all 650
nodes into three buckets:

- `matched` — a proposed atlas `canonical_id`, with the evidence for the match
  and a `confirmed_by` field that stays empty until a human fills it;
- `new_candidate` — no atlas counterpart, with a proposed `entity_type` from the
  existing 18-value vocabulary;
- `ambiguous` — a name collision or an under-determined label, listed for
  decision rather than resolved.

Rules:

- **No node is created in `data/public-data.json` by this packet.** It produces a
  reviewed queue.
- Any node later promoted enters as `status: candidate`,
  `public_visibility: metadata`, `publication_level: research_stub`, matching the
  existing seed-corpus pattern.
- Every proposed match records the matching method, so the William Rowan Hamilton
  / W. D. Hamilton class of error is visible rather than buried.
- Split multi-person labels (for example *"Critical Systems / Michael C. Jackson,
  Robert Flood, Werner Ulrich"*) into separate person candidates plus one concept
  candidate. Do **not** create a relationship between them from co-appearance in
  a box; sharing a rectangle is not evidence of collaboration.

Realistic sizing: roughly 620 nodes need a decision, and the strict automated
pass settles about 31. Batch it — the pre-1950 mathematics and astronomy stream
(56 black nodes) is a coherent first tranche and is where the atlas is emptiest.

---

## Packet C — bibliographic grounding (this is where your Scopus and OpenAlex exports are used)

### What this packet is for

Converting *"there is a coloured line between these two boxes"* into *"this work
cites that work, here is the DOI, and citation is not the same as influence"*.
That is the only route by which anything from this map becomes a publishable
atlas statement.

### OpenAlex — preferred, and yes please

OpenAlex is CC0, which means records can go into a CC BY-SA repository without a
rights problem. Scopus cannot. So OpenAlex should be the primary spine and Scopus
the verification layer.

What is useful, per landmark item (roughly 150–200 works — the 16 nodes with an
explicit year, plus the canonical work behind each named person):

- `id` (Work ID), `doi`, `title`, `publication_year`, `type`
- `authorships` → author `id`, `display_name`, `orcid`
- `referenced_works` — **the critical field**; this is what builds citation edges
- `cited_by_count`, `primary_location.source.display_name`

And per named person (roughly 200 people):

- Author `id`, `display_name`, `display_name_alternatives`, `orcid`,
  `last_known_institutions`, `works_count`

If it is easier to pull than to export, the API is open and needs no key —
`https://api.openalex.org/works?filter=doi:...&mailto=<address>`. A one-off
harvest script under `scripts/` is preferable to a manual export because it is
re-runnable and the provenance is recorded. Either way, an export works.

### Scopus — useful, with a rights constraint

Use Scopus where OpenAlex is thin, which for this map means pre-1970 material and
non-Anglophone lineage: Bogdanov, Ouyang and Yi Lin, Wu Xuemou, Fuenmayor and
López-Garay, Lerner, Myasishchev and Bekhterev, Schwarz.

Export as CSV with these columns selected, and **include the References
field** — it is what makes citation edges possible:

`Authors`, `Author(s) ID`, `Title`, `Year`, `Source title`, `Volume`, `Issue`,
`Page start/end`, `DOI`, `Link`, `Affiliations`, `Abstract`, `Author Keywords`,
`References`, `EID`, `Document Type`, `Publication Stage`, `Open Access`.

**Rights constraint, and it is a hard one:** Scopus records are licensed to your
institution and are not redistributable. They may be used to *verify* an
identifier and to decide whether a source gets a public URL or the existing
`no_public_link` marker — but Scopus abstracts, keyword lists and metadata must
not be pasted into `data/`. `RIGHTS.md` and
`documentation/publication-safety.md` already cover this; the import script
should enforce it by only ever emitting DOI, year and a resolved public URL from
a Scopus row.

### Deliverables

- `data/comparator-bibliographic-spine.json` — resolved identifiers only:
  `atlas_canonical_id`, `openalex_work_id`, `openalex_author_id`, `orcid`,
  `doi`, `year`, `public_url_status`.
- A proposed new relation family, `bibliometric`, added to `relation_types` with
  two types:
  - `cites` — minimum evidence: a resolvable DOI or OpenAlex `referenced_works`
    entry; `plain_phrase: "cites"`;
  - `coauthored_with` — already exists in the atlas with 68 uses; reuse it rather
    than duplicating.

### The rule that governs this packet

A citation is not an influence claim. `GOVERNANCE.md` principle 3 and
`DESIGN_AND_CONTENT_RULES.md` rule 2 both require citation, contact,
collaboration, teaching, influence, precedence and logical dependence to stay
distinct. Every `cites` edge therefore carries `scope_conditions` saying so
explicitly, and no `cites` edge is ever upgraded to `influenced_by` without a
separate source that makes the influence claim directly.

---

## Packet D — first promotion cohort

Promote **40 to 60** statements, not 1,320. Each promoted edge must carry:
`relation_type` from the existing 93-type vocabulary, `relation_family`,
`plain_phrase`, `directed`, `claim_status`, `confidence`, `source_ids`, an exact
`source_locator`, `scope_conditions`, `assertion_mode`, `inference_method`,
`reviewed_by` and `reviewed_at`.

No comparator edge is promoted *as* a comparator edge. Each promoted statement is
re-derived from its own source; the GraphML's role is to have suggested where to
look, and that role is recorded in `inference_method`.

Suggested first cohort: the citation spine among the 16 dated landmark works —
Bertalanffy 1949, Wiener 1948, Bogdanov 1922, Smuts 1926, Cannon 1932, Beer 1972,
Forrester 1956, Pask 1975, von Foerster on second-order cybernetics, Greif and
Cashman 1984, Weiser 1991, Howe 2006, Yolles 2006, Yolles and Fink 2014,
Hirsbrunner 2016, Murrell 1949. These are the nodes where a DOI or a stable
bibliographic record is most likely to exist, so the evidence bar is reachable.

---

## Packet E — the public comparator page

This is what issue 6 actually asks for, and it can be delivered without promoting
a single edge.

`docs/comparator-systemic-evolution.html`, assessing the map against the required
axes: purpose, audience, boundary, categories, meaning of lines, evidence,
strengths, omissions and reifications — and, as
`documentation/coverage-programme.md` section 4 explicitly demands, **where The
Necessary Tangle performs worse**.

On the current evidence that section writes itself:

- the GraphML carries a deep pre-1950 lineage — astronomy from Babylon and
  Eudoxus through Ptolemy, Copernicus and Brahe; rational mechanics; geological
  gradualism; instrument-making from Archimedes to Babbage — which the atlas
  almost entirely lacks;
- it holds non-Anglophone traditions the atlas barely touches: Tektology,
  pansystems, general tropodynamics, interpretive systemology, ergonology;
- it is markedly stronger on semiotics, linguistics and the philosophy of
  meaning, at 52 and 139 nodes in those streams.

Against which the honest counter-statement is that the map states no source for
any node, no meaning for any line, and no evidential status anywhere — which is
the specific failure the atlas exists to correct. Both halves belong on the page.

Follow the existing site constraints: cream and red palette, serif hierarchy,
status legible without relying on colour alone, keyboard access preserved, and
the bottom-right `aria-label="Open updates"` dot untouched.

---

## Packet F — validation, registers and release

- New `scripts/validate_comparator_systemic_evolution.py`, added to the
  `validate` target, asserting: node and edge counts; that no comparator edge has
  an asserted relation type; that no comparator identifier leaks into
  `data/public-data.json` edges without `relation_type` and `source_ids`; that no
  Scopus-derived field beyond DOI, year and public URL appears in `data/`.
- Register updates: `corpus_register.corpus_comparator_maps` status moves off
  `registered_comparator_pass_pending`; add an `external_corpus_review` entry;
  add `meta` counts and a `comparator_systemic_evolution_url`.
- `CHANGELOG.md` entry and a numbered release, since this is a substantive
  curatorial batch.
- `documentation/TANGLE_STATE.md` and `documentation/NEXT_WORK.md` restored to a
  truthful next-decision state.

---

## 4. What this plan deliberately refuses to do

- Import 1,320 unlabelled edges as atlas relationships.
- Derive relation types from line colour, line width or dash pattern.
- Treat co-appearance in a yEd rectangle as collaboration.
- Treat an OpenAlex citation as an influence, teaching or dependence claim.
- Run `refresh_graph_snapshot.py` over imported unlabelled edges — that would
  raise `reader_connected_entry_count` and `substantive_edge_count` without a
  single new evidenced statement, which is precisely the metric-gaming the
  relational-depth programme was built to prevent.
- Publish anything from the file before its licence and provenance are known.

## 5. The immediate next decision

Not a technical one. It is: **who made this map, and under what licence** — and
whether this work is proposed upstream to `antlerboy/the-necessary-tangle` or
maintained as a declared fork. Packet A is ready to write the moment those two
answers exist and the build fixed point in §2.1 is restored.
