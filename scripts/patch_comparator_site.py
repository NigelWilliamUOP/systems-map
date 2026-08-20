#!/usr/bin/env python3
"""Render the public comparator page and link it from the site.

Packet E of documentation/comparator-systemic-evolution-plan.md. Satisfies the
completion test on corpus_comparator_maps (issue 6): a public comparison of
purpose, boundary, categories, meaning of lines, evidence, strengths and
failures - including where The Necessary Tangle performs worse.

Idempotent.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
COMPARATOR_PATH = ROOT / "data" / "comparator-systemic-evolution.json"
DOCS = ROOT / "docs"
PAGE = DOCS / "comparator-prior-maps.html"
INDEX = DOCS / "index.html"
SITEMAP = DOCS / "sitemap.xml"

CARD = (
    '<a class="start-small-card" href="comparator-prior-maps.html">'
    '<span class="eyebrow">Comparing prior maps</span>'
    '<strong>Prior maps of the field</strong>'
    '<span>Two earlier maps read against this atlas: what they cover that we do not, '
    'and why an unlabelled line cannot be published as a relationship.</span></a>'
)

STYLE = """.cmp-shell{max-width:1200px;margin:0 auto;padding:1.4rem 1.3rem 5rem}
.cmp-head{max-width:850px;padding:2rem 0 1rem}
.cmp-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0 1.5rem}
.cmp-grid div{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:.8rem}
.cmp-grid strong{display:block;font-size:1.45rem;color:var(--accent)}
.cmp-section{max-width:850px;margin:2.4rem 0 0}
.cmp-section h2{margin-bottom:.4rem}
.cmp-callout{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);
border-radius:var(--radius);padding:1rem 1.1rem;margin:1.2rem 0;max-width:850px}
.cmp-table-wrap{max-width:100%;overflow-x:auto;border-radius:var(--radius);margin:1rem 0}
table.cmp{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);table-layout:fixed}
table.cmp th,table.cmp td{text-align:left;vertical-align:top;padding:.68rem;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
table.cmp th{font-family:Arial,sans-serif;font-size:.8rem;color:var(--muted)}
.cmp-swatch{display:inline-block;width:.72rem;height:.72rem;border-radius:2px;border:1px solid var(--line);
margin-right:.4rem;vertical-align:baseline}
.cmp-verdict{font:700 .72rem Arial,sans-serif;white-space:nowrap;text-transform:uppercase;letter-spacing:.04em}
.cmp-worse{color:var(--orange)}.cmp-better{color:var(--green)}.cmp-both{color:var(--muted)}
.cmp-nav{max-width:1200px;margin:0 auto;padding:1rem 1.3rem 0}
.cmp-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
clip:rect(0 0 0 0);white-space:nowrap;border:0}
@media(max-width:760px){.cmp-shell{padding-inline:.85rem}.cmp-nav{padding-inline:.85rem}
.cmp-grid{grid-template-columns:1fr 1fr}}"""

COMPARISON = [
    ("Purpose",
     "Show the descent of ideas across the systems sciences at a glance, as one picture.",
     "Make every published connection state what it means, with a source and a scope.",
     "cmp-both", "Different jobs"),
    ("Audience",
     "Readers who already know the field and want its shape recalled.",
     "Readers who need to check a claim, and contributors who need to challenge one.",
     "cmp-both", "Different jobs"),
    ("Boundary",
     "Wide. Astronomy, mechanics, philosophy, semiotics, computing, ecology, engineering.",
     "Narrower, and weighted to UK systems practice, Cynefin, the Viable System Model and intervention skills.",
     "cmp-worse", "Tangle narrower"),
    ("Categories",
     "Thirteen colour streams, with no legend anywhere in the file.",
     "Eighteen entity types and 93 relation types, each defined and evidenced.",
     "cmp-better", "Tangle stronger"),
    ("Meaning of lines",
     "None stated. All 1,320 connections carry colour and direction only.",
     "Every published line carries a relation type, a plain phrase, a scope note and a source.",
     "cmp-better", "Tangle stronger"),
    ("Evidence",
     "No per-node source. The pre-1950 stratum derives from a popular 1926 history of philosophy.",
     "Sources and locators recorded per statement; provisional and disputed claims stay visible.",
     "cmp-better", "Tangle stronger"),
    ("Historical depth",
     "Deep. Babylonian and Greek astronomy through Copernicus, Brahe, Newton and Babbage.",
     "Thin before 1900. Ludwig von Bertalanffy has no person entry at all.",
     "cmp-worse", "Tangle worse"),
    ("Non-anglophone coverage",
     "Tektology, pansystems, general tropodynamics, interpretive systemology, ergonology.",
     "Barely represented.",
     "cmp-worse", "Tangle worse"),
    ("Semiotics and meaning",
     "191 nodes across the semiotics and philosophy streams.",
     "Present but comparatively thin.",
     "cmp-worse", "Tangle worse"),
    ("Provenance of the map itself",
     "Stated on its home page: four contributors across thirty years.",
     "Curator named, releases numbered, decisions preserved in issues and pull requests.",
     "cmp-both", "Both explicit"),
]


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.rstrip().splitlines()) + "\n"


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_page() -> str:
    comparator = json.loads(COMPARATOR_PATH.read_text(encoding="utf-8"))
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    meta = comparator["meta"]
    atlas_meta = data.get("meta", {})
    domains = sorted(
        (n["label"], n.get("description", ""))
        for n in data.get("nodes", [])
        if n.get("inclusion_reason") == "comparator_castellani_map"
    )
    domain_rows = "".join(
        f"<tr><th scope=\"row\">{esc(label)}</th><td>{esc(gloss)}</td></tr>"
        for label, gloss in domains
    )
    nodes = comparator["nodes"]
    edges = comparator["edges"]

    streams = Counter((n["border_colour"], n["colour_stream_label"]) for n in nodes)
    stream_rows = "".join(
        f'<tr><td><span class="cmp-swatch" style="background:{esc(colour)}"></span>'
        f'<code>{esc(colour)}</code></td><td>{count:,}</td><td>{esc(label)}</td></tr>'
        for (colour, label), count in streams.most_common()
    )

    widths = Counter(e["line_width"] for e in edges)
    width_rows = "".join(
        f"<tr><td>{esc(str(w))}</td><td>{c:,}</td></tr>"
        for w, c in sorted(widths.items(), key=lambda kv: -kv[1])
    )

    comparison_rows = "".join(
        f"<tr><th scope=\"row\">{esc(axis)}</th><td>{esc(theirs)}</td><td>{esc(ours)}</td>"
        f'<td class="cmp-verdict {cls}">{esc(verdict)}</td></tr>'
        for axis, theirs, ours, cls, verdict in COMPARISON
    )

    def n(value: int) -> str:
        return f"{value:,}"

    dashed = sum(1 for e in edges if e["line_style"] == "dashed")
    single = sum(1 for e in edges if e["target_arrow"] == "standard" and e["source_arrow"] == "none")
    unstated = sum(1 for e in edges if e["meaning"] == "unstated_in_source")
    worse = sum(1 for row in COMPARISON if row[3] == "cmp-worse")
    WORSE_WORD = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}.get(worse, str(worse))

    cast_total = n(atlas_meta.get("castellani_map_entry_count", 0))
    cast_held = n(atlas_meta.get("castellani_map_already_held_count", 0))
    cast_evo = n(atlas_meta.get("castellani_map_in_systemic_evolution_count", 0))
    cast_gap = n(atlas_meta.get("castellani_map_gap_count", 0))
    cast_domains = n(atlas_meta.get("castellani_map_domains_incorporated", 0))
    cast_people = n(atlas_meta.get("castellani_map_people_queued", 0))

    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="theme-color" content="#9f161b"><title>Prior maps of the field — The Necessary Tangle</title><meta name="description" content="The Necessary Tangle read against two earlier maps of the field: purpose, boundary, categories, the meaning of lines, evidence, and where this atlas performs worse."><link rel="stylesheet" href="assets/styles.css?v=0.16.3-visual"><link rel="stylesheet" href="assets/site-enhancements.css?v=0.16.3-visual"><style>{STYLE}</style></head>
<body>
<a class="skip-link" href="#cmp-main">Skip to the comparison</a>
<nav class="cmp-nav" aria-label="Comparator navigation"><a href="index.html#view=home">← The Necessary Tangle</a></nav>
<main id="cmp-main" class="cmp-shell" tabindex="-1">
<header class="cmp-head">
<p class="eyebrow">Comparing prior maps</p>
<h1>Prior maps of the field</h1>
<p>Earlier maps of this field deserve to be read carefully rather than replaced quietly. This page compares two of them with The Necessary Tangle, and records what they do better.</p>
</header>

<div class="cmp-grid">
<div><strong>{n(meta['node_count'])}</strong>nodes in the map</div>
<div><strong>{n(meta['edge_count'])}</strong>connections drawn</div>
<div><strong>{n(unstated)}</strong>whose meaning is unstated</div>
<div><strong>{worse}</strong>axes where this atlas is weaker</div>
</div>

<section class="cmp-section">
<h2>The Map of Systemic Evolution</h2>
<p>A single large diagram of the descent of the systems sciences, kept in yEd and published by its maintainers at the University of Fribourg. Its own page records a lineage across thirty years and four hands: originated in 1996 by Eric Schwarz in Neuchâtel; extended in 1998 with items drawn from Will Durant's popular history of philosophy; elaborated in 2000–2001 for the International Institute for General Systems Studies; extended in 2016 by Benjamin Hadorn.</p>
<p>Eric Schwarz appears as a node inside his own map. So does the <em>International Encyclopedia of Systems and Cybernetics</em>. It is a working document that has absorbed its own sources.</p>
</section>

<section class="cmp-section">
<h2>The problem it poses</h2>
<div class="cmp-callout">
<p><strong>Not one of its {n(meta['edge_count'])} connections says what it means.</strong> Every line carries a colour, a width and a direction, and nothing else. There is no legend in the file, and no key on the page.</p>
</div>
<p>A reader cannot tell whether a grey line records influence, teaching, citation, logical dependence, historical sequence, or simple thematic adjacency. Neither can we. This atlas holds that position, colour and algorithmic neighbourhood assert nothing, so none of those {n(meta['edge_count'])} connections is published here as a relationship. Importing them would add that many unevidenced claims and inflate our own connectivity figures.</p>
<p>That is a statement about what can be published, not a judgement of the map. The distinctions were in its makers' heads and in the literature; the format simply had nowhere to record them.</p>
</section>

<section class="cmp-section">
<h2>Side by side</h2>
<div class="cmp-table-wrap">
<table class="cmp"><caption class="cmp-sr">Comparison across the axes required by the coverage programme</caption>
<thead><tr><th scope="col">Axis</th><th scope="col">Map of Systemic Evolution</th><th scope="col">The Necessary Tangle</th><th scope="col">Reading</th></tr></thead>
<tbody>{comparison_rows}</tbody></table>
</div>
<p>{WORSE_WORD} of those readings go against us, and they are the useful ones. This atlas is thinner before 1900, thinner outside the anglophone tradition, and thinner on semiotics and the philosophy of meaning. The map is a standing argument that our boundary is narrower than the field.</p>
</section>

<section class="cmp-section">
<h2>Where it is stronger, and why that is qualified</h2>
<p>The map carries a deep pre-1950 lineage — Babylonian and Greek astronomy, Ptolemy, Copernicus, Brahe, rational mechanics, geological gradualism, instrument-making from Archimedes to Babbage — which this atlas almost entirely lacks. It also holds traditions we barely touch: Tektology, pansystems, general tropodynamics, interpretive systemology, ergonology, and the Chinese systems literature associated with the International Institute for General Systems Studies.</p>
<p>One qualification belongs with that credit. The pre-1950 stratum entered in 1998 from Will Durant's <em>The Story of Philosophy</em>, a popular survey first published in 1926, and no node carries a source of its own. It is a strong indication of where to look. It is not an independently sourced account, and presenting its breadth as depth would repeat the error this page exists to name.</p>
</section>

<section class="cmp-section">
<h2>The colour streams</h2>
<p>Thirteen border colours group the {n(meta['node_count'])} nodes. The stream names below are our description of a visual grouping, not the map's stated intent — the file records none. They are open to correction by its maintainers.</p>
<div class="cmp-table-wrap">
<table class="cmp"><caption class="cmp-sr">Nodes by border colour</caption>
<thead><tr><th scope="col">Border colour</th><th scope="col">Nodes</th><th scope="col">Apparent stream</th></tr></thead>
<tbody>{stream_rows}</tbody></table>
</div>
</section>

<section class="cmp-section">
<h2>The connections, as drawn</h2>
<p>Of {n(meta['edge_count'])} connections, {n(single)} are single-headed and {n(dashed)} are dashed. Line width varies across five values. None of this variation is explained anywhere in the file.</p>
<div class="cmp-table-wrap">
<table class="cmp"><caption class="cmp-sr">Connections by line width</caption>
<thead><tr><th scope="col">Line width</th><th scope="col">Connections</th></tr></thead>
<tbody>{width_rows}</tbody></table>
</div>
</section>

<section class="cmp-section">
<h2>What we would give back</h2>
<p>The file declares four attribute fields — a description and a link for every node, and a description and a link for every connection — and leaves all four empty, on all {n(meta['node_count'])} nodes and all {n(meta['edge_count'])} connections. The format the map is already kept in has somewhere to record what each line means. Nobody has filled it in.</p>
<p>That is the most useful thing this project could return: a stated meaning for each connection, written where evidence supports one and marked explicitly unstated where it does not.</p>
</section>


<section class="cmp-section">
<h2>The Map of the Complexity Sciences</h2>
<p>Brian Castellani's map takes the same problem from the complexity side. Its current web edition carries {cast_total} linked entries, arranged by strand and period, and unlike the map above it gives every entry an outward link to a paper, profile or encyclopaedia article. That single decision makes it far more checkable: a reader can follow any node to something that says why it is there.</p>
<p>Read against both this atlas and the Map of Systemic Evolution: {cast_held} of its entries are already held here, {cast_evo} appear in the Map of Systemic Evolution, and {cast_gap} appear in neither.</p>
<div class="cmp-callout">
<p><strong>Its lines are unlabelled too.</strong> The map groups and positions entries meaningfully, but no line states a relation type, so the same rule applies: nothing here is imported as a relationship.</p>
</div>
</section>

<section class="cmp-section">
<h2>What we took from it</h2>
<p>The gap runs almost entirely through <em>applied</em> complexity — the domains where the field meets public health, planning, geography and social data. That is a real weakness in this atlas, and {cast_domains} fields are now registered from it:</p>
<div class="cmp-table-wrap">
<table class="cmp"><caption class="cmp-sr">Fields incorporated from the Map of the Complexity Sciences</caption>
<thead><tr><th scope="col">Field</th><th scope="col">What it covers</th></tr></thead>
<tbody>{domain_rows}</tbody></table>
</div>
<p>Each carries one relationship and one only: that it appears in Castellani's map. That is a documentary fact about the map. It is not evidence of influence, endorsement, teaching or conceptual dependence, and the scope note on every one of those {cast_domains} statements says so.</p>
<p>Each also enters as a research stub rather than a finished entry, so none of them is counted as a developed public entry. The atlas's public figures — entries, connected entries, evidential depth — are unchanged by this pass. Registering a gap is not the same as filling it.</p>
</section>

<section class="cmp-section">
<h2>What we did not take, and why</h2>
<p>The map also names {cast_people} individual contemporary researchers this atlas does not hold. They are recorded as a research queue and left out of the dataset.</p>
<p>Adding them would have raised the entry count by {cast_people} while adding nothing that could be checked: no source beyond an appearance, no relationship, no account of what each person contributed. That is precisely the coverage inflation the relational-depth programme exists to prevent, and it would have made the atlas measurably worse while appearing to make it bigger. The names are better added one at a time, each with its own evidence.</p>
</section>

<section class="cmp-section">
<h2>Rights and acknowledgement</h2>
<p>The Map of Systemic Evolution is © CyberTech Engineering and the University of Fribourg, all rights reserved, and remains under its own terms. The Map of the Complexity Sciences remains Brian Castellani's. Both are cited and described here, not relicensed.</p>
<p>Our thanks to Eric Schwarz, the International Institute for General Systems Studies, Benjamin Hadorn and Brian Castellani, whose work this page compares itself against — and which, in the second case, has already corrected a gap in ours.</p>
<p><a href="https://uranos.ch/index.php/research-menu/cybernetcis" target="_blank" rel="noopener">The Map of Systemic Evolution</a> · <a href="https://www.art-sciencefactory.com/complexity-map_feb09.html" target="_blank" rel="noopener">The Map of the Complexity Sciences</a> · <a href="index.html#view=home">Back to the atlas</a></p>
</section>
</main>
</body>
</html>
"""


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    if "comparator-prior-maps.html" in text:
        return
    # Anchor on the last start-small card rather than a named one: later
    # release scripts rewrite which cards appear, so any specific href is
    # a moving target.
    position = text.rfind('<a class="start-small-card"')
    if position == -1:
        raise RuntimeError("Could not locate any start-small card to anchor to")
    line_start = text.rfind("\n", 0, position) + 1
    indent = text[line_start:position]
    end = text.find("</a>", position) + len("</a>")
    INDEX.write_text(
        clean(text[:end] + "\n" + indent + CARD + text[end:]), encoding="utf-8"
    )


def patch_sitemap() -> None:
    text = SITEMAP.read_text(encoding="utf-8")
    loc = "https://transduction.systems/comparator-prior-maps.html"
    if loc in text:
        return
    entry = f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-08-20</lastmod>\n  </url>\n"
    SITEMAP.write_text(text.replace("</urlset>", entry + "</urlset>"), encoding="utf-8")


def main() -> int:
    PAGE.write_text(clean(build_page()), encoding="utf-8")
    patch_index()
    patch_sitemap()
    print("Rendered the comparator page and linked it from the atlas home view")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
