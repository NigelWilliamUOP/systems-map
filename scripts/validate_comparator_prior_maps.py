#!/usr/bin/env python3
"""Validate the Map of Systemic Evolution comparator.

The point of these checks is that the comparator can never leak into the atlas
graph as an unevidenced relationship, and that the public page keeps saying so.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
COMPARATOR_PATH = ROOT / "data" / "comparator-systemic-evolution.json"
DOCS = ROOT / "docs"
PAGE = DOCS / "comparator-prior-maps.html"

EXPECTED_NODES = 650
EXPECTED_EDGES = 1320


def main() -> int:
    errors: list[str] = []

    if not COMPARATOR_PATH.exists():
        print("FAILED: data/comparator-systemic-evolution.json is missing", file=sys.stderr)
        return 1

    comparator = json.loads(COMPARATOR_PATH.read_text(encoding="utf-8"))
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    nodes = comparator["nodes"]
    edges = comparator["edges"]

    if len(nodes) != EXPECTED_NODES:
        errors.append(f"expected {EXPECTED_NODES} comparator nodes, found {len(nodes)}")
    if len(edges) != EXPECTED_EDGES:
        errors.append(f"expected {EXPECTED_EDGES} comparator edges, found {len(edges)}")

    # The central guarantee.
    asserted = [e for e in edges if e.get("relation_type") is not None]
    if asserted:
        errors.append(f"{len(asserted)} comparator edges assert a relation_type")
    unstated = [e for e in edges if e.get("meaning") != "unstated_in_source"]
    if unstated:
        errors.append(f"{len(unstated)} comparator edges are not marked unstated_in_source")
    labelled = [e for e in edges if e.get("edge_label_in_source")]
    if labelled:
        errors.append(
            f"{len(labelled)} comparator edges carry label text; the public page states "
            "that none do and must be rewritten"
        )

    # No comparator identifier may appear in the atlas graph.
    comparator_ids = {n["source_node_id"] for n in nodes}
    atlas_node_ids = {n.get("id") for n in data.get("nodes", [])}
    leaked = comparator_ids & atlas_node_ids
    if leaked:
        errors.append(f"comparator node ids leaked into the atlas graph: {sorted(leaked)[:5]}")

    for edge in data.get("edges", []):
        if not edge.get("relation_type") or not edge.get("source_ids"):
            errors.append(
                f"atlas edge {edge.get('id')} lacks a relation type or a source; "
                "the comparator must not introduce untyped edges"
            )
            break

    # Registration.
    meta = data.get("meta", {})
    for key in (
        "comparator_systemic_evolution_url",
        "comparator_systemic_evolution_node_count",
        "comparator_systemic_evolution_edge_count",
    ):
        if key not in meta:
            errors.append(f"meta is missing {key}")
    if meta.get("comparator_systemic_evolution_node_count") != len(nodes):
        errors.append("meta node count does not match the comparator dataset")
    if meta.get("comparator_systemic_evolution_edge_count") != len(edges):
        errors.append("meta edge count does not match the comparator dataset")

    # Second comparator: every incorporated domain must carry exactly one
    # sourced appearance edge and must not be dressed up as a public entry.
    domains = [n for n in data.get("nodes", [])
               if n.get("inclusion_reason") == "comparator_castellani_map"]
    if not domains:
        errors.append("no domains incorporated from the Map of the Complexity Sciences")
    domain_ids = {n["id"] for n in domains}
    for node in domains:
        if node.get("public_visibility") != "metadata":
            errors.append(f"{node['id']} is presented as a public entry without a written account")
        if node.get("publication_level") != "research_stub":
            errors.append(f"{node['id']} is not marked as a research stub")
        if "src_castellani_map_complexity_sciences" not in (node.get("source_ids") or ""):
            errors.append(f"{node['id']} does not cite the comparator map")
    appearance = [e for e in data.get("edges", []) if e.get("source") in domain_ids]
    if len(appearance) != len(domain_ids):
        errors.append(
            f"{len(domain_ids)} incorporated domains carry {len(appearance)} edges; "
            "each must carry exactly one appearance statement"
        )
    for edge in appearance:
        if edge.get("relation_type") != "member_of":
            errors.append(f"{edge.get('id')} asserts more than an appearance")
        if "not evidence of influence" not in (edge.get("scope_conditions") or ""):
            errors.append(f"{edge.get('id')} lacks the appearance-is-not-influence scope note")

    register = {c.get("id"): c for c in data.get("corpus_register", [])}
    entry = register.get("corpus_comparator_maps", {})
    if entry.get("status") == "registered_comparator_pass_pending":
        errors.append("corpus_comparator_maps still reports the comparator pass as pending")
    if "src_map_of_systemic_evolution" not in entry.get("source_ids", []):
        errors.append("corpus_comparator_maps does not cite the comparator source")
    if not any(
        r.get("id") == "external_map_of_systemic_evolution"
        for r in data.get("external_corpus_review", [])
    ):
        errors.append("no external corpus review recorded for the comparator")

    # The public page must carry the comparison the coverage programme requires.
    if not PAGE.exists():
        errors.append("docs/comparator-prior-maps.html is missing")
    else:
        page = PAGE.read_text(encoding="utf-8")
        for marker, description in (
            ("Purpose", "the purpose axis"),
            ("Boundary", "the boundary axis"),
            ("Meaning of lines", "the meaning-of-lines axis"),
            ("Evidence", "the evidence axis"),
            ("cmp-worse", "at least one axis where this atlas performs worse"),
            ("all rights reserved", "the rights acknowledgement"),
            ("Eric Schwarz", "attribution to the map's originator"),
            ("International Institute for General Systems Studies", "attribution to IIGSS"),
            ("Benjamin Hadorn", "attribution to the 2016 contributor"),
            ("Will Durant", "the qualification on the pre-1950 stratum"),
            ("Map of the Complexity Sciences", "the second comparator"),
            ("Brian Castellani", "attribution to the second comparator's author"),
            ("research queue", "the reason the named researchers were not bulk-added"),
        ):
            if marker not in page:
                errors.append(f"the comparator page is missing {description}")
        if 'href="index.html#view=home"' not in page:
            errors.append("the comparator page does not link back to the atlas")
        if "skip-link" not in page:
            errors.append("the comparator page lacks a skip link")
        index = (DOCS / "index.html").read_text(encoding="utf-8")
        if "comparator-prior-maps.html" not in index:
            errors.append("the atlas home view does not link to the comparator page")

    if errors:
        for message in errors:
            print(f"FAILED: {message}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "comparators": ["Map of Systemic Evolution", "Map of the Complexity Sciences"],
                "systemic_evolution_nodes": len(nodes),
                "systemic_evolution_edges": len(edges),
                "systemic_evolution_edges_marked_unstated": len(edges),
                "systemic_evolution_relationships_created": 0,
                "castellani_domains_incorporated": len(domains),
                "castellani_appearance_statements": len(appearance),
                "checks": 26,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
