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

### 4.1 Syntax rules that govern every query below

These are the rules the first draft of this note got wrong. They are stated here
because each one silently changes or breaks a query rather than raising a clear
error.

| Rule | Correct | Wrong |
| --- | --- | --- |
| `PUBYEAR` takes `IS`, `AFT`, `BEF` — not comparison operators | `PUBYEAR AFT 1969` | `PUBYEAR > 1969` |
| `AUTHOR-NAME` takes an unquoted `surname, initial`; quoting turns it into a loose phrase and loses the name-variant matching | `AUTHOR-NAME(ashby, w)` | `AUTHOR-NAME("Ashby, W*")` |
| `AUTHOR-NAME` already expands variants, so a trailing wildcard is unnecessary | `AUTHOR-NAME(ackoff, r)` | `AUTHOR-NAME(ackoff, r*)` |
| `AUTHLASTNAME` and `REFAUTH` take the bare term unquoted | `AUTHLASTNAME(barney)` | `AUTHLASTNAME("Barney")` |
| A multi-word surname needs a quoted loose phrase, or splitting across fields | `AUTHLASTNAME("von foerster") AND AUTHFIRST(h)` | `AUTHOR-NAME(von foerster, h)` |
| `REFPUBYEAR` accepts `IS` only | `REFPUBYEAR IS 1949` | `REFPUBYEAR AFT 1948` |
| Braces are exact-match; wildcards inside them are literal characters | `{heart-attack}` | `{health care?}` |
| Straight ASCII quotes only — smart quotes cause parse errors | `"general system theory"` | `“general system theory”` |
| Parentheses, commas and brackets inside a term break the expression | strip them first | `AUTHOR-NAME("(HCI), H*")` |

Scopus advises a maximum of roughly 50 boolean operators per query, and queries
over 8,000 characters may need splitting. The generated batches stay at 20
authors and at most 24 operators.

### 4.2 Author resolution (T1)

Batch the 296 Tier 1 authors into groups of 20:

```
AUTHOR-NAME(ackoff, r) OR AUTHOR-NAME(ashby, w) OR AUTHOR-NAME(pask, g)
  OR AUTHOR-NAME(bateson, g) OR AUTHOR-NAME(shannon, c)
  OR AUTHOR-NAME(maturana, h) OR AUTHOR-NAME(varela, f)
  OR AUTHOR-NAME(luhmann, n) OR AUTHOR-NAME(checkland, p)
  OR (AUTHLASTNAME("von foerster") AND AUTHFIRST(h))
```

Notes:

- Dropping the initial (`AUTHLASTNAME(ashby)`) widens recall where the indexed
  form is uncertain. Worth doing for the twenty or so names that matter most —
  the generated CSV carries this as a separate column.
- Mononyms and collective pseudonyms — Bourbaki, Cicero, Aristotle — must use
  `AUTHLASTNAME`; `AUTHOR-NAME` with an initial returns nothing for them.
- Diacritics are indexed inconsistently. Seven names here carry them
  (Poincaré, Gödel, Schrödinger among them); run the ASCII-folded form as a
  fallback.
- The export you want carries **Author(s) ID**. That is the disambiguation key;
  the name string is not.

### 4.3 Incoming citations to the pre-1970 canon (T2)

The documented minimal form is a bare term — the Elsevier example is
`REFAUTH(Wu)` — and it works standalone. Start there and add constraints only if
the result set is unmanageable:

```
REFAUTH(bertalanffy)
REF(bertalanffy AND "general system theory")
REF(bertalanffy AND 1949)
REFAUTH(bertalanffy) AND REFPUBYEAR IS 1949
REFTITLE("general system theory")
```

**The `AND` trap.** Scopus documents this distinction explicitly:

- `REF(darwin 1859)` — both terms in the **same** reference.
- `REF(darwin) AND REF(1859)` — terms may be in **different** references.

So `REFAUTH(x) AND REFTITLE(y)` does not mean *"a reference by x titled y"*. It
means *"this document cites x somewhere, and cites something titled y
somewhere"*. That is a correctness fault, not a syntax one: it returns documents
that cite both independently. Use the grouped `REF( ... AND ... )` form whenever
the terms must belong to one reference.

Do not add `AND PUBYEAR AFT 1969` to a `REF` query. It is redundant — cited
references only exist in the index from 1970 — and combining a reference field
with a document field is the most likely cause of a query being rejected.

Common surnames still need qualifying. Unqualified `REFAUTH(miller)`,
`REFAUTH(beer)` or `REFAUTH(simon)` returns too much to use, so reach for form B
or C there.

**If the `REF` family fails entirely** — not recognised, or returning nothing on
the bare form — it is unavailable on the subscription or interface in use.
Nothing about the plan depends on it. Use OpenAlex, which does the same job
without a licence:

```
https://api.openalex.org/works?search=general+system+theory+bertalanffy
https://api.openalex.org/works?filter=cites:W2043376269&per-page=200&cursor=*
```

Resolve the work in the first call, take its ID, list everything citing it in the
second. For the pre-1970 canon this is the better route regardless, because
OpenAlex indexes the works themselves where Scopus holds only later documents
that cite them.

### 4.4 Topic sweeps, per stream

For the concepts that name no person:

```
TITLE-ABS-KEY("second-order cybernetics")
TITLE-ABS-KEY("viable system model")
TITLE-ABS-KEY("autopoiesis")
TITLE-ABS-KEY("system dynamics" AND "feedback")
TITLE-ABS-KEY("self-organised criticality" OR "self-organized criticality")
```

### 4.5 Export columns

Select all of: `Authors`, `Author(s) ID`, `Title`, `Year`, `Source title`,
`Volume`, `Issue`, `Pages`, `DOI`, `Link`, `Affiliations`, `Abstract`,
`Author Keywords`, **`References`**, `EID`, `Document Type`, `Open Access`.

`References` is the one that does the work. Without it the export cannot produce
a single citation edge.

### 4.6 Rights

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

## 6. What running these queries actually produced

Measured from three Scopus exports run against the author batches in section 4.
Counts only: no Scopus record, abstract or keyword is reproduced here or
anywhere in `data/`, per section 4.6.

### 6.1 The pre-1970 reference gap, measured

Section 3 asserted from Elsevier's documentation that cited references are
indexed only from 1970. A 1,426-document export covering 1845–1978 confirms it
directly:

| Citing document | Documents | Carrying any reference |
| --- | --- | --- |
| pre-1970 | 774 | **1** (0.1%) |
| 1970 onwards | 652 | 405 (62.1%) |

Half that export could not yield a citation edge at all. The practical
consequence is a sequencing rule: export the 1970+ slices first. They are where
the evidence is.

### 6.2 Name-based batching is roughly 90% noise

The same export was about 90% homonyms. The batches pulled in R. K. Pearson
(inorganic chemistry) for Karl Pearson, D. G. Ashby (carrot fly control) for
Ross Ashby, J. S. Shannon (mass spectrometry) for Claude Shannon, T. J. Cicero
(neuropharmacology), and P. Bateson (ethology) for Gregory Bateson. In a larger
34,879-document pair of exports the most common single venue was the *Journal of
High Energy Physics*, because a surname batch collides with author lists running
to thousands of names.

**`Author(s) ID` has to do the disambiguation, not the name string.** That is
the column to insist on at export time, and the reason section 4.2 asks for it.

A filter on journal and title terms cut 34,879 documents to 1,066 plausibly
on-topic ones. That ratio should be expected, not treated as a failed export.

### 6.3 W. Ross Ashby is not a clean homonym case

Do not discard Ashby's medical papers as the wrong person. He was a research
psychiatrist at Barnwood House, and the 1930s–50s papers on cerebral chemistry
and mental deficiency are plausibly the same man as the cybernetician. Papers on
carrot fly and beach erosion are not. No regex can make that call: it needs a
human decision, recorded, and it is a good early test of the reconciliation
queue in Packet B.

### 6.4 Yield

From 34,883 documents and 6,182,223 reference rows, restricted to the on-topic
set: 12,609 references naming a canonical figure, of which 561 are
self-citations and **12,048 are independent**. Most-cited: Bertalanffy (1,477),
Luhmann (880), M. C. Jackson (866), Checkland (749), Beer (705), Ackoff (556).

A coverage cross-check is the more useful output. Of the 400 most-cited authors
in the on-topic set, 34 appear in both this atlas and the comparator map, and
246 appear in neither. The strongest named absences, each with a most-cited
work, include Matjaž Mulej (dialectical systems theory, the single most-cited
author in the set), John Sterman (*Business Dynamics*), George Richardson
(*Feedback Thought in Social Science and Systems Theory*), Donald T. Campbell,
Ralph Stacey, Markus Schwaninger, Karl Weick and Donald Schön.

That list is a research queue, not a finding. Surnames were resolved to people by
taking the most frequent form in the reference strings, which conflates people
who share one: "Scott B." resolved to W. Richard Scott's *Institutions and
Organizations* rather than Bernard Scott the second-order cybernetician. Each
entry needs checking before it becomes a candidate.

And the standing rule still applies: every one of these is a **citation**.
Influence, teaching, collaboration and conceptual dependence remain separate
claims needing separate evidence.

## 7. Suggested order of work

1. **The 17 dated nodes**, then the top 50 T1 nodes by degree. Small, high-value,
   and it tests the whole pipeline before it is pointed at 650 nodes.
2. **T2 incoming citations** via `REFAUTH` and OpenAlex `cites:`. This is the
   evidence base for the map's spine.
3. **T1 author resolution** in batches of 20, cybernetics and general-systems
   streams first, since they overlap most with the existing atlas.
4. **T3 to authority files.** Do not send these to Scopus.
5. Everything unresolved stays unresolved and visible. An empty identifier is a
   fact about coverage; a guessed one is a defect.

## 8. Generated working files

Regenerated from the source map, held outside the repository:

| File | Contents |
| --- | --- |
| `authors_to_resolve.csv` | 501 persons: tier, review flag, summed node degree, streams, concepts, source node IDs, a Scopus author query, an ASCII-folded fallback, a broader surname-only query and an OpenAlex author URL |
| `works_to_resolve.csv` | 650 nodes in degree order: stream, concept, persons, year, raw label, a Scopus query and an OpenAlex URL |
| `scopus_author_batches.txt` | The T1 authors pre-batched into 15 disjunctive queries of 20, each under the boolean-operator guidance |
| `scopus_refauth.txt` | `REFAUTH` targets for the pre-1970 canon |
| `openalex_author_urls.txt` | One resolvable API URL per T1 author |

Sort by `summed_degree` to work the map's structural spine first, and treat any
row with a `needs_review` value as a name to confirm before spending a query on
it.
