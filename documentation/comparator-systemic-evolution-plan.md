# Plan: integrating the *Systemic Evolution* GraphML as a comparator corpus

Status: **Draft — awaiting curator decision on Packet A**

Owner: **Curator (Benjamin P Taylor), with Nigel Williams proposing**

Human review point: **The rights position in section 2 constrains what may be
published. Packet A and the return track may proceed; atlas ingestion may not.**

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

## 2. Provenance and rights

The file arrived by email from **Benjamin Hadorn** (PhD Computer Science,
CyberTech Engineering GmbH, formerly University of Fribourg), with the request:
*"Would you mind sharing the updated map with us afterwards?"*

It is **not** his sole work. The map is published as the *Map of Systemic
Evolution* at <https://uranos.ch/index.php/research-menu/cybernetcis>, which
states its lineage verbatim:

> Originated in 1996 by Dr. Eric Schwarz, Neuchâtel, Switzerland.
> Extended in 1998, including items from the 'The Story of Philosophy' by Will
> Durant (1933).
> Elaborated in 2000-2001 from many sources for the International Institute for
> General Systems Studies.
> Extended in 2016 by Benjamin Hadorn, Fribourg, Switzerland.

Three internal features of the file corroborate that chain:

- Eric Schwarz appears **as a node in his own map** — *"Neuchatel Evolutionary
  Model / Eric Schwarz"*.
- The IIGSS stage explains an otherwise puzzling cluster: Yi Lin, Sifeng Liu,
  Shoucheng OuYang and Wu Xuemou are all IIGSS-associated, and the institute was
  Yi Lin's.
- The 2016 Hadorn stage explains the 32 pale-yellow nodes exactly. They are his
  own doctoral territory — coordination theory, CSCW, HCI, speech-act theory,
  ubiquitous computing — terminating in *"Generic System Model / Beat
  Hirsbrunner [2016]"* and *"Generic Coordination Model / Beat Hirsbrunner /
  Michele Courant"*, his supervisors in the Fribourg PAI group and co-authors of
  the URANOS work.

### 2.1 What this means for publication

**Permission granted, and it is real.** The uranos.ch page says: *"Feel free to
extend and correct the graph. Please send an updated version to us in order to
keep a current version online."* Hadorn's email repeats it directly. There is a
clear, public, standing invitation to modify the map and return it.

**Permission not granted.** The same site states **"© 2020 CyberTech Engineering
and University of Fribourg. All Rights Reserved."** That is expressly
all-rights-reserved and incompatible with this repository's CC BY-SA 4.0 content
licence. A licence to *extend and return* is not a licence to *republish under a
share-alike licence*, and `RIGHTS.md` is explicit that third-party works keep
their own terms and that a link or citation does not relicense the underlying
work.

**And Hadorn cannot clear it alone.** Rights are layered across at least four
contributions: Schwarz's 1996 original, the 1998 Durant-derived extension, the
2000–01 IIGSS elaboration, and Hadorn's own 2016 layer, with the declared
copyright held by CyberTech Engineering and the University of Fribourg. Will
Durant died in 1981, so *The Story of Philosophy* remains in copyright in the UK
and EU until 2051. Bare names and dates are facts and not protectable; a
selection and arrangement of them can be.

### 2.2 The route this opens

The rights position does not block the work. It splits it into two tracks that
can run at the same time.

**Track 1 — the return (Packet G).** Extract, enrich and export back to valid
yEd-readable GraphML, and send it to Hadorn. This sits squarely inside the
permission already granted and needs no further clearance. It should be done
regardless of what the atlas decides, because it was asked for.

**Track 2 — atlas ingestion (Packets A–F).** The map is treated as a
lead-generating working input and a **cited comparator**, not as importable
content. The atlas may describe, cite, analyse and criticise it — normal
scholarly treatment of a published work, and `RIGHTS.md` permits a concise
evidential summary — but it does not republish the node text or the graph
structure wholesale. Every statement that reaches `data/public-data.json` is
re-derived from its own source.

That distinction lets the whole programme proceed now. Separately, ask Hadorn
whether he will licence the map under CC BY-SA 4.0, and whether he is in a
position to speak for the Schwarz and IIGSS layers. If yes, Track 2 widens and
raw labels can be published; if no, nothing above changes.

### 2.3 A correction this forces to section 1.2

The earlier reading — that the map's deep pre-1950 lineage is material the atlas
should envy — needs qualifying. That stratum is the **1998 Durant import**: the
astronomy, rational mechanics and history-of-philosophy nodes come from a
popular 1926 survey, at one remove, with no per-node sourcing. It is a strong
prompt for where to look. It is not an independently sourced evidence base, and
the comparator page must say so rather than presenting breadth as depth.

## 3. Remaining gates

1. **Fork or upstream.** This checkout is `NigelWilliamUOP/systems-map`; the
   dataset's own `meta.repository_url` and every documentation link point to
   `antlerboy/the-necessary-tangle`, and `GOVERNANCE.md` names Benjamin P Taylor
   as accountable for published releases. Decide whether this work is a proposal
   upstream (in which case the comparator dataset should be shaped for a PR) or a
   divergent fork (in which case `meta`, `RIGHTS.md` and the site URLs need an
   explicit statement of the fork's own status).

2. **`documentation/NEXT_WORK.md` currently says no packet is active.** Packet A
   below has to replace the holding content, with curator agreement, before
   implementation begins.

3. **Attribution.** Any published use requires `ACKNOWLEDGEMENTS.md` and the
   comparator page to credit the full chain: Eric Schwarz (1996), the 1998
   Durant-derived extension, the International Institute for General Systems
   Studies (2000–01), and Benjamin Hadorn (2016), with copyright noted as
   CyberTech Engineering and the University of Fribourg. Crediting only the
   person who emailed the file would misstate the record.

### 3.1 Two repository facts found while preparing this plan

Both affect any data change and should be fixed first.

- **`make validate` fails on Python 3.11.** `scripts/apply_relational_depth_16.py`
  line 989 uses a backslash inside an f-string expression, which is only legal
  from Python 3.12 (PEP 701). The repository has no `.python-version`, no
  `pyproject.toml` and no documented interpreter floor;
  `.github/workflows/validate.yml` should be checked against this and the
  minimum recorded.

- **`make validate` also fails on Python 3.12, from a clean checkout.** An
  earlier note here recorded that it passed. That was wrong, and the reason is
  worth stating because it is easy to repeat: the passing run began from a tree
  already half-patched by an aborted Python 3.11 run, not from `main`. From a
  clean checkout the build fails `scripts/validate_iteration_14.py` with *"the
  update-thread URL must occur exactly once in the rendered page"*.

  The mechanism is exact. `scripts/patch_iteration_14.py` line 72 removes an
  existing update dot with a regex whose lookahead requires the element to sit
  immediately before `</body>`:

  ```
  re.sub(r'\n[ \t]*<a\b(?=[^>]*data-update-thread-dot)[^>]*>.*?</a>[ \t]*(?=\n</body>)', '', text, ...)
  ```

  In the committed `docs/index.html` the dot is followed by
  `<script src="assets/iteration-17.js…">`, not `</body>`. The lookahead
  therefore never matches, the existing dot is not removed, and the script adds
  a second one. `patch_adversarial_experience.py` then finds a dot already
  present and skips, so the page ships two.

  The consequence is larger than drift: **the committed 0.17 artefact cannot be
  regenerated by the documented build.** The commit message on `main` —
  "Deploy the validated 0.17 artefact directly" — says as much. Any packet that
  writes to `data/` inherits this, because `make validate` is the stated gate
  and it cannot pass.

  The fix looks like one line: drop the `(?=\n</body>)` lookahead so the dedupe
  matches the dot wherever it sits. It is not applied here.
  `DESIGN_AND_CONTENT_RULES.md` forbids removing or relocating the magic dot,
  and this is release machinery the curator owns, so it needs a human decision
  rather than an autonomous edit.
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

## 4. Programme shape

Seven packets across two tracks. Only Packet A is specified in full; the rest are
sketched so the sequence and the cost profile are visible. One packet at a time,
each through `NEXT_WORK.md`, each merged by review.

| Packet | Track | Outcome | Depends on | Size |
| --- | --- | --- | --- | --- |
| A | both | Deterministic extraction to a comparator dataset | §3 gates, §3.1 | Small, mechanical |
| B | both | Identity reconciliation against atlas canonical IDs | A | Large, human-judgement bound |
| C | both | Bibliographic grounding from OpenAlex and Scopus | B, your exports | Medium |
| G | return | Enriched GraphML exported and sent back to Hadorn | A, C | Small |
| D | atlas | First promotion cohort: 40–60 evidenced statements | C | Medium, curator-bound |
| E | atlas | Public comparator page satisfying issue 6 | A, B, §2 | Medium |
| F | atlas | Validation, registers, release | all | Small |

Packets A, B and C serve both tracks, so the return to Hadorn is not extra work —
it is the same extraction and grounding, written back out in his format.

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
- Committing the `.graphml` source file. It is all-rights-reserved third-party
  material (§2.1); it stays a local working input, referenced by URL.
- **Committing the extracted dataset either.** This corrects a contradiction in
  an earlier draft of this packet, which listed `raw_label` verbatim among the
  extracted fields while §2.2 forbade republishing the map's node text or
  structure. Both cannot hold: `data/comparator-systemic-evolution.json`
  reproduces all 650 labels and the entire edge list, which is republication of
  the structure wholesale, not the concise evidential summary `RIGHTS.md`
  permits. The file is therefore generated and `.gitignore`d. The extractor is
  committed — it is original MIT-licensed software — so anyone holding a copy of
  the map can rebuild the dataset in one command. If Hadorn and the University
  of Fribourg grant a compatible licence, the ignore entry comes out and nothing
  else changes.

### Named files or areas

- `scripts/import_comparator_graphml.py` (new)
- `data/comparator-systemic-evolution.json` (new)
- `documentation/comparator-systemic-evolution.md` (new)

### Acceptance checks

- [x] Output contains exactly 650 node records and 1,320 edge records.
- [x] Every edge record has `relation_type: null` and
      `meaning: "unstated_in_source"`; zero exceptions, and the extractor exits
      non-zero rather than writing if that is ever violated.
- [x] Re-running the script produces a byte-identical file.
- [x] `git diff data/public-data.json docs/` is empty after the run.
- [ ] ~~`make validate` passes~~ — blocked, and not by this packet. The build
      cannot pass from a clean checkout on any interpreter version; see §3.1.
      This packet writes nothing the validators read, so it neither causes nor
      clears that failure.
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

Note on access: the OpenAlex API is **not** reachable from this working
environment — requests through the session proxy return HTTP 429 with
`"Insufficient budget… you only have $0 remaining"`. A harvest script must
therefore run on a machine with direct access, or the data must arrive as an
export. This raises the value of doing the pull yourself.

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

## Packet G — the return to Hadorn

This is the packet that honours what was actually asked for, and it is the one
with no rights obstacle at all.

### Outcome

A valid yEd-openable GraphML, structurally identical to the original but
materially more useful, sent back to Hadorn for the current version online.

### The opportunity sitting in the file

The GraphML declares four attribute keys and populates **none** of them:

| Key | Target | Purpose | Currently |
| --- | --- | --- | --- |
| `d4` | node | `url` | empty on all 650 |
| `d5` | node | `description` | empty on all 650 |
| `d8` | edge | `url` | empty on all 1,320 |
| `d9` | edge | `description` | empty on all 1,320 |

yEd displays both `description` and `url`, and both survive a round trip. So the
enrichment has a natural home in the file's own declared schema, and the returned
map opens correctly in the tool its maintainers already use.

### What the returned map adds

- **Node `url`** — a resolvable DOI, OpenAlex work page, or archive link for the
  work behind the node.
- **Node `description`** — the resolved identity: full name, dates, the canonical
  work and year, ORCID or OpenAlex author ID, and where a label was ambiguous,
  a note saying so.
- **Edge `description`** — the single highest-value change. Every one of the
  1,320 edges currently means nothing outside its author's head. Where Packet C
  established a citation, the description states it and names the evidence; where
  it did not, the description says `meaning not stated in source` rather than
  inventing one.
- A `<data key="d0">` graph-level note recording what was added, by whom, when,
  and by what method, so the next person to extend the map inherits the
  provenance rather than guessing at it — which is precisely the problem this
  file posed on arrival.

### Constraints

- Preserve every node's geometry, colour, fill, shape and label text exactly.
  This is an annotation pass, not a redesign. The map must remain recognisably
  the same map.
- Never overwrite an existing value; only populate empty fields.
- Do not silently correct the map's content. Where the reconciliation in Packet B
  found an apparent error, record it in `description` as a query, and list the
  queries in the covering note. Corrections are the maintainers' to accept.
- Return the queries as a plain list too, since a covering email is more likely
  to be read than an XML attribute.

### Acceptance checks

- [ ] The exported file opens in yEd without error and renders identically to the
      original at the same zoom.
- [ ] Node and edge counts unchanged at 650 and 1,320.
- [ ] Diff against the source shows changes only inside `d4`, `d5`, `d8`, `d9`
      and the graph-level `d0` note.
- [ ] No edge `description` asserts a relation that Packet C did not evidence.

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
  pansystems, general tropodynamics, interpretive systemology, ergonology, and
  the IIGSS-associated Chinese systems literature — Yi Lin, Sifeng Liu,
  Shoucheng OuYang, Wu Xuemou;
- it is markedly stronger on semiotics, linguistics and the philosophy of
  meaning, at 52 and 139 nodes in those streams.

Against which the honest counter-statement is that the map states no source for
any node, no meaning for any line, and no evidential status anywhere — which is
the specific failure the atlas exists to correct. Both halves belong on the page.

The page must also carry the qualification in §2.3: the pre-1950 breadth is a
1998 import from Will Durant's popular history of philosophy, so it is a research
prompt rather than a sourced lineage. Presenting it as an evidential advantage
would repeat the error the page exists to identify.

The map's own four-stage provenance — 1996, 1998, 2000–01, 2016, across three
countries and four sets of hands, with the meaning of every line living outside
the file — is itself the strongest available argument for the atlas's insistence
on explicit semantics. It should be treated as the page's central case, made
respectfully: this is what happens to a valuable map that is passed on for thirty
years without a way to record what its lines mean.

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

## 5. What this plan deliberately refuses to do

- Import 1,320 unlabelled edges as atlas relationships.
- Derive relation types from line colour, line width or dash pattern.
- Treat co-appearance in a yEd rectangle as collaboration.
- Treat an OpenAlex citation as an influence, teaching or dependence claim.
- Run `refresh_graph_snapshot.py` over imported unlabelled edges — that would
  raise `reader_connected_entry_count` and `substantive_edge_count` without a
  single new evidenced statement, which is precisely the metric-gaming the
  relational-depth programme was built to prevent.
- Republish the map's node text or structure under CC BY-SA 4.0 while it remains
  all-rights-reserved third-party material.
- Credit the map to the person who emailed it, rather than to its four-stage
  chain of authorship.
- Silently correct the map before returning it to its maintainers.

## 6. The immediate next decision

Two, and neither is technical.

1. **Ask Hadorn the three questions in §7.** They are cheap, he has already
   invited correspondence, and the answers determine how wide Track 2 can go.
2. **Fork or upstream** — whether this is proposed to
   `antlerboy/the-necessary-tangle` or maintained as a declared fork.

Packet A is ready to write once the build fixed point in §3.1 is restored. It
does not depend on either answer, because it publishes nothing.

## 7. Questions for Benjamin Hadorn

Short, specific, and answerable in a reply:

1. **Licence.** The uranos.ch page marks the map "© 2020 CyberTech Engineering
   and University of Fribourg. All Rights Reserved", alongside the invitation to
   extend and return it. Would CyberTech and the University consider releasing
   the map under CC BY-SA 4.0, or another open licence, so that derived work can
   be published openly with full attribution? If not, the work can still proceed
   — it simply stays on the return track.
2. **The earlier layers.** Are the Schwarz 1996 original and the 2000–01 IIGSS
   elaboration covered by that copyright, or do they sit with Eric Schwarz's
   estate and the Institute? Who should be approached about them?
3. **Format of the return.** Would enrichment written into the file's existing
   `description` and `url` attributes — DOIs, resolved identities, and stated
   meanings for the edges — be useful, or is a different structure preferred for
   keeping the online version current?

Worth adding, because it is the substance of the offer: the single most valuable
thing that can be given back is a stated meaning for each of the 1,320 edges,
since that is the one thing the file cannot currently carry.
