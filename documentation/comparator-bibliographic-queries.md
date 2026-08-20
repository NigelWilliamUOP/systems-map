# Bibliographic query design for the comparator map

Method note for Packet C of
[`comparator-systemic-evolution-plan.md`](comparator-systemic-evolution-plan.md).
It states what to ask OpenAlex and Scopus for, and — more importantly — what
neither can answer.

The query sets themselves are generated from the source map's node labels. They
are held as working files rather than committed here, because the map is
all-rights-reserved third-party material (see §2.1 of the plan). This note
records the method and the syntax so the sets can be regenerated.

## 1. What was extracted

Parsing all 650 node labels into concept, person and year gives:

| Quantity | Count |
| --- | --- |
| Nodes | 650 |
| Nodes naming at least one person | 482 |
| Distinct persons after de-duplication on surname + initial | 501 |
| Persons in a modern stream (Tier 1) | 296 |
| Persons only in the history, philosophy or instruments streams (Tier 3) | 205 |
| Nodes with an explicit year | 17 |

Label parsing is heuristic and imperfect: yEd wraps labels across lines with no
separator between concept and person, so *"Systems Cybernetics / W. Ross Ashby"*
and *"Human-Computer Interaction (HCI)"* arrive in the same shape. A 20-row spot
check of the Tier 1 list gave 18 correct, 1 non-person read as a person
(*"Numbers China"*), and 1 given name taken from the concept
(*"Therapy Watzlewick"*). Every generated row therefore carries its original raw
label alongside the query, so any row can be checked in one glance, and rows the
parser was unsure of carry a `needs_review` value.

Worth passing back to the map's maintainers: the source misspells Paul
Watzlawick as "Watzlewick".

## 2. Tiering — the databases only help for part of this map

The map's highest-degree nodes are Vico, Kant, Newton, Leibniz, Whitehead,
Darwin, Nietzsche, Marx and Comte. That is the 1998 Durant stratum, and it is
the part of the map a citation database cannot serve. Sorting before querying
avoids spending effort where there is nothing to find.

| Tier | Who | Right identifier | Citation edges available? |
| --- | --- | --- | --- |
| **T1** | Twentieth-century and later named authors — cybernetics, general systems, computing, OR, ecology, social theory, semiotics, formal | OpenAlex Author ID, ORCID, Scopus Author ID | Yes, subject to §3 |
| **T2** | The pre-1970 foundational canon: Wiener, Bertalanffy, Ashby, Bogdanov, Smuts, Cannon, Shannon, McCulloch | OpenAlex Work ID, DOI where one exists | **Incoming only** — see §3 |
| **T3** | Pre-1900 figures: Aristotle, Newton, Kant, Vico, Leibniz | VIAF, Wikidata, Library of Congress authority files | No. Do not query Scopus or OpenAlex for these |

296 of the 501 persons fall in T1. Roughly 205 fall in T3 and should be routed to
authority files, not bibliometrics.

## 3. The constraint that shapes the whole packet

**Scopus indexes cited references back to 1970 only.** Records exist from 1788,
but the reference lists attached to pre-1970 records do not. So Scopus can never
return the reference list of *Cybernetics* (1948), *General System Theory*
(1949), *Tektology* (1922) or *Design for a Brain* (1952) — which is precisely
the foundational layer the map is built on.

The workaround is to reverse the direction. Scopus supports cited-reference
fields — `REFAUTH`, `REFTITLE`, `REFSRCTITLE`, `REFPUBYEAR` — which search
*inside* the reference lists of post-1970 records. That finds everything indexed
since 1970 that cites the pre-1970 canon.

This suits the map better than the forward direction would. 1,262 of its 1,320
edges are single-headed and run from earlier work to later work, so the map is
already asserting an influence direction. Later-work-cites-earlier-work is
evidence pointing along the same axis, gathered on the side of the boundary
where Scopus actually has data.

Set expectations honestly: this yields **citation**, which is not influence,
teaching or conceptual dependence. The scope condition in Packet C applies to
every edge produced this way.

## 4. Scopus

### 4.1 Author resolution (T1)

Batch the 296 Tier 1 authors into groups of about 25 — long disjunctions become
unreliable beyond that:

```
AUTHOR-NAME("von Foerster, H*") OR AUTHOR-NAME("Ackoff, R*")
  OR AUTHOR-NAME("Ashby, W*") OR AUTHOR-NAME("Pask, G*")
  OR AUTHOR-NAME("Bateson, G*") OR AUTHOR-NAME("Shannon, C*")
  OR AUTHOR-NAME("Maturana, H*") OR AUTHOR-NAME("Varela, F*")
  OR AUTHOR-NAME("Luhmann, N*") OR AUTHOR-NAME("Checkland, P*")
```

Notes:

- Dropping the initial (`AUTHLASTNAME("Ashby")`) widens recall where the
  indexed form is uncertain. Worth doing for the twenty or so names that matter
  most.
- Mononyms and collective pseudonyms — Bourbaki, Cicero, Aristotle — must use
  `AUTHLASTNAME`; `AUTHOR-NAME` with an initial silently returns nothing.
- The export you want carries **Author(s) ID**. That is the disambiguation key;
  the name string is not.

### 4.2 Incoming citations to the pre-1970 canon (T2)

One query per canonical author, which is the point of §3:

```
REFAUTH("Bertalanffy") AND PUBYEAR > 1969
REFAUTH("Wiener") AND REFPUBYEAR IS 1948
REFTITLE("general system theory")
REFTITLE("design for a brain")
REFAUTH("Ashby") AND REFTITLE("introduction to cybernetics")
```

Pair `REFAUTH` with `REFTITLE` or `REFPUBYEAR` for the common surnames —
unqualified `REFAUTH("Miller")` or `REFAUTH("Beer")` is unusable on its own.

### 4.3 Topic sweeps, per stream

For the concepts that name no person:

```
TITLE-ABS-KEY("second-order cybernetics")
TITLE-ABS-KEY("viable system model")
TITLE-ABS-KEY("autopoiesis")
TITLE-ABS-KEY("system dynamics" AND "feedback")
TITLE-ABS-KEY("self-organised criticality" OR "self-organized criticality")
```

### 4.4 Export columns

Select all of: `Authors`, `Author(s) ID`, `Title`, `Year`, `Source title`,
`Volume`, `Issue`, `Pages`, `DOI`, `Link`, `Affiliations`, `Abstract`,
`Author Keywords`, **`References`**, `EID`, `Document Type`, `Open Access`.

`References` is the one that does the work. Without it the export cannot produce
a single citation edge.

### 4.5 Rights

Scopus records are licensed to the institution and are not redistributable. Only
the DOI, year and a resolved public URL may reach `data/`. Abstracts, keyword
lists and Scopus metadata must not. The import script should enforce that rather
than relying on discipline.

## 5. OpenAlex

CC0, so its records can enter a CC BY-SA repository directly. It is the primary
spine; Scopus is the verification layer.

Note: the API is not reachable from this repository's working environment —
requests return HTTP 429, `"Insufficient budget… $0 remaining"`, through the
session proxy. Run the harvest somewhere with direct access.

### 5.1 Authors

```
https://api.openalex.org/authors?search=Ross%20Ashby
  &per-page=5
  &select=id,display_name,orcid,works_count,last_known_institutions
  &mailto=you@example.org
```

Always keep `works_count` and `last_known_institutions` — they are how you tell
the right W. Hamilton from the wrong one, which is the error class that broke the
naive reconciliation pass in §1.2 of the plan.

### 5.2 Works, and the field that matters

```
https://api.openalex.org/works?search=cybernetics%20Norbert%20Wiener
  &select=id,doi,display_name,publication_year,authorships,referenced_works,cited_by_count
```

`referenced_works` is the outgoing citation list — the OpenAlex equivalent of the
Scopus `References` column, and available for pre-1970 records where Scopus is
silent.

### 5.3 Incoming citations

The direct analogue of `REFAUTH`, and cleaner:

```
https://api.openalex.org/works?filter=cites:W2043376269&per-page=200&cursor=*
```

### 5.4 Bulk retrieval

- `&per-page=200` with `&cursor=*`, then follow `meta.next_cursor`.
- Batch identifier lookups with `|`:
  `?filter=openalex:W123|W456|W789`
- Filter by DOI list: `?filter=doi:10.1000/x|10.1000/y`
- Always send `&mailto=` for the polite pool.

## 6. Suggested order of work

1. **The 17 dated nodes**, then the top 50 T1 nodes by degree. Small, high-value,
   and it tests the whole pipeline before it is pointed at 650 nodes.
2. **T2 incoming citations** via `REFAUTH` and OpenAlex `cites:`. This is the
   evidence base for the map's spine.
3. **T1 author resolution** in batches of 25, cybernetics and general-systems
   streams first, since they overlap most with the existing atlas.
4. **T3 to authority files.** Do not send these to Scopus.
5. Everything unresolved stays unresolved and visible. An empty identifier is a
   fact about coverage; a guessed one is a defect.

## 7. Generated working files

Regenerated from the source map, held outside the repository:

| File | Contents |
| --- | --- |
| `authors_to_resolve.csv` | 501 persons: tier, review flag, summed node degree, streams, concepts, source node IDs, a Scopus author query and an OpenAlex author URL |
| `works_to_resolve.csv` | 650 nodes in degree order: stream, concept, persons, year, raw label, a Scopus query and an OpenAlex URL |
| `scopus_author_batches.txt` | The T1 authors pre-batched into 12 disjunctive queries |
| `scopus_refauth.txt` | `REFAUTH` targets for the pre-1970 canon |
| `openalex_author_urls.txt` | One resolvable API URL per T1 author |

Sort by `summed_degree` to work the map's structural spine first, and treat any
row with a `needs_review` value as a name to confirm before spending a query on
it.
