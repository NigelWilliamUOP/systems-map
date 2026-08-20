# The Map of Systemic Evolution: what the source encodes

A colour census of the comparator map, produced by
`scripts/import_comparator_graphml.py`. It exists to make one point checkable:
**the source states no meaning for any of its 1,320 connections.** Everything a
reader might take as a relationship is carried by line colour, width and dash
pattern, and nowhere else in the file.

For the map's provenance, rights position and the programme built around it, see
[`comparator-systemic-evolution-plan.md`](comparator-systemic-evolution-plan.md).

## The rule this document exists to protect

> Position, colour and algorithmic neighbourhood do not assert an unstated
> relation.
> — `data/public-data.json`, `semantic_contract.visual_rule`

The atlas therefore does **not** translate any colour below into a relation
type, a relation family, or an edge in `data/public-data.json`. The census is a
description of a picture, not a set of claims. Every extracted edge carries
`relation_type: null` and `meaning: "unstated_in_source"`, and the extractor
fails rather than writes if that ever stops being true.

## Nodes by border colour

All 650 nodes, counted from the file:

| Border colour | Nodes | Apparent stream |
| --- | --- | --- |
| `#999999` | 139 | philosophy, meaning and media |
| `#000000` | 106 | physical science, astronomy and history of science |
| `#FFCC00` | 84 | social theory, constructivism and psychology |
| `#008000` | 73 | general systems and biology-derived systems theory |
| `#0000FF` | 73 | mathematics, statistics and formal systems theory |
| `#FFFF00` | 52 | semiotics, linguistics and the logic of signs |
| `#800000` | 49 | computing, information, agents and coordination |
| `#FF00FF` | 19 | engineering and instrument-making |
| `#FF0000` | 18 | cybernetics |
| `#00CCFF` | 18 | operational research and decision science |
| `#00FF00` | 18 | ecology and environmental systems |
| `#666699` | 1 | reference work |

The stream names in the third column are **this project's descriptions of a
visual grouping**. The file records no legend, no key and no statement of what
any colour is for. Read them as an editorial reading of the picture, open to
correction by the map's maintainers.

An earlier table in the plan gave `#000000` as 56 rather than 106. That count
excluded the 50 nodes drawn at border width 2.0, which are section headings and
container-like labels rather than ordinary entries. This document counts all 650
nodes, so the two figures differ by exactly those 50.

## Node fills

| Fill | Nodes |
| --- | --- |
| `#FFFFFF` | 618 |
| `#FFFF99` | 32 |

The 32 pale-yellow nodes are a coherent late cluster — coordination theory,
CSCW, HCI, speech-act theory, agent-based modelling, ubiquitous computing —
terminating in the Fribourg group's own work. They correspond to the 2016
extension recorded in the map's provenance.

## Edges

| Property | Value |
| --- | --- |
| Edges | 1,320 |
| Carrying any label text | **0** |
| Single-headed (`none` → `standard`) | 1,262 |
| Double-headed (`standard` → `standard`) | 58 |
| Solid | 1,287 |
| Dashed | 33 |

By line width:

| Width | Edges |
| --- | --- |
| 2.0 | 1,173 |
| 4.0 | 130 |
| 3.0 | 11 |
| 1.0 | 5 |
| 5.0 | 1 |

The six most common line colours are `#999999` (380), `#000000` (258),
`#0000FF` (160), `#FFCC00` (109), `#008000` (105) and `#800000` (88).

Nothing in the file says what any of this means. A reader cannot tell whether a
grey line records influence, teaching, citation, logical dependence, historical
sequence or simple thematic adjacency — and neither can the atlas.

## The two unused fields

The GraphML declares four attribute keys and populates none of them:

| Key | Applies to | Purpose | Populated |
| --- | --- | --- | --- |
| `d4` | node | `url` | 0 of 650 |
| `d5` | node | `description` | 0 of 650 |
| `d8` | edge | `url` | 0 of 1,320 |
| `d9` | edge | `description` | 0 of 1,320 |

The format the map is already kept in has somewhere to put a stated meaning for
every line, and a source for every node. Those fields have simply never been
filled. That is the opportunity Packet G takes up: the most useful thing this
project can give back is an edge `description` for each of the 1,320 connections,
written where evidence supports one and left explicitly unstated where it does
not.

## Regenerating this

```bash
python3 scripts/import_comparator_graphml.py /path/to/systemic_evolution.graphml
```

The output, `data/comparator-systemic-evolution.json`, is **not committed**. It
reproduces all 650 node labels and the full edge list, and the source is
all-rights-reserved third-party material; publishing it in a CC BY-SA repository
would be republication rather than citation. The extractor is committed, so the
dataset can be rebuilt by anyone holding a copy of the map. See section 2 of the
plan.
