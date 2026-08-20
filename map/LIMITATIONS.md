# What this map cannot yet tell you

Written at v0.1, from the first build. These are properties of the corpus and
the method, not defects to be tidied away later.

## 1. The corpus decides the map, and the corpus is not neutral

The Scopus corpus behind this build was assembled from author-name batches
seeded on the *Map of Systemic Evolution*, plus cited-reference queries against
a pre-1970 canon. That origin shapes everything downstream:

- It over-represents the systems, cybernetics and operational-research journals
  where those authors publish — *Systems Research and Behavioral Science*,
  *Kybernetes*, *Journal of the Operational Research Society*.
- It under-represents the physics-and-mathematics side of complexity, which
  publishes elsewhere and was largely filtered out as off-topic noise.
- 34,883 documents entered; 3,071 passed the topic filter; 1,507 matched a
  concept. The map rests on that 1,507, not on the field.

A concept marked `candidate` is therefore **not** a claim that its literature is
small. Chaos theory, control theory, Cynefin, organisational learning and
cognitive science all fall below threshold here, and all plainly have
substantial literatures. What the label means is: *not present in this corpus
slice, at this threshold*. Fixing that means widening the corpus, not lowering
the bar.

## 2. Broad terms out-compete precise ones

"Systems thinking" matches 377 works and sits on 73 of the 517 edges. That is
partly real centrality and partly an artefact: the phrase appears in titles
across the field, so it absorbs works that a more precise reading would file
elsewhere. Cybernetics (76 edges), emergence and general system theory behave
the same way to a lesser degree.

Treat the hubs as a measurement of *how the field labels itself*, which is a
real finding, and not as a measurement of which ideas matter most.

## 3. A quarter of the edges lean on very few bibliographies

125 of 517 edges are flagged `concentrated`: one citing work supplies half or
more of the supporting references. The worst runs to 89%. Those edges are real
in the sense that the citations exist, and weak in the sense that a single
author's reference list drew the line.

The flag is in the data so a reader can see it. It is not a reason to delete the
edge; it is a reason not to read it as a property of the field.

## 4. Title matching is coarse

Concepts are matched against work titles and reference strings, not abstracts or
keywords — those are licensed Scopus fields and stay out of this repository. A
paper about requisite variety that never says so in its title is invisible here.
This trades recall for a clean rights position, deliberately.

## 5. Citation is the only relation so far

`literature_cites` counts references. It says nothing about influence, teaching,
agreement, derivation or logical dependence, and the map should not be read as
if it did. Those are separate claims needing separate evidence and their own
relation types.

Direction is reliable — citation runs from later work to earlier — so the map
can support "this literature drew on that one". It cannot support "this idea
came from that one" without further work.

## 6. Pre-1970 is structurally thin

Scopus indexes cited references only from 1970. The foundational layer —
Wiener 1948, Bertalanffy 1949, Ashby 1952 and 1956, Bogdanov 1922 — appears here
only as something later work cites, never as work that cites. Any apparent
sparseness before 1970 is a property of the index.

## What would move each of these

| Limitation | What fixes it |
| --- | --- |
| Corpus bias | Journal-scoped and topic-scoped exports, not author-scoped |
| Hub artefacts | Splitting broad concepts into narrower ones with their own tests |
| Concentrated edges | More citing works, from a wider export |
| Coarse matching | An abstract-level pass held outside the repository |
| One relation type | Curated conceptual edges, each separately sourced |
| Pre-1970 thinness | OpenAlex, which indexes the works themselves |
