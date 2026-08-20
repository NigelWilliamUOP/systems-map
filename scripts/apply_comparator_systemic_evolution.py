#!/usr/bin/env python3
"""Register the Map of Systemic Evolution comparator in the public dataset.

Packet E/F of documentation/comparator-systemic-evolution-plan.md.

This records that the comparator pass named by corpus_comparator_maps (issue 6)
has been carried out for one prior map, and publishes a browser copy of the
extracted dataset. It adds no edge and no node to the atlas graph: the map's
1,320 connections state no meaning, and none of them is promoted here.

Idempotent.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "public-data.json"
COMPARATOR_PATH = ROOT / "data" / "comparator-systemic-evolution.json"
DOCS_ASSETS = ROOT / "docs" / "assets"

PAGE_URL = "https://transduction.systems/comparator-systemic-evolution.html"
REPO_DOC = (
    "https://github.com/antlerboy/the-necessary-tangle/blob/main/"
    "documentation/comparator-systemic-evolution.md"
)
SOURCE_ID = "src_map_of_systemic_evolution"


def source_record() -> dict[str, Any]:
    return {
        "id": SOURCE_ID,
        "title": "Map of Systemic Evolution",
        "source_type": "comparator_map",
        "quality_tier": "C",
        "access": "public_metadata",
        "url": "https://uranos.ch/index.php/research-menu/cybernetcis",
        "date": "2016",
        "notes": (
            "A 650-node, 1,320-edge yEd map of the systems sciences. Originated 1996 by "
            "Eric Schwarz; extended 1998 with items from Will Durant's popular history of "
            "philosophy; elaborated 2000-2001 for the International Institute for General "
            "Systems Studies; extended 2016 by Benjamin Hadorn. Used as a comparator for "
            "coverage and structure. Not evidence for any relationship: the map states no "
            "meaning for any of its connections."
        ),
        "creators": json.dumps(
            [
                "Eric Schwarz",
                "International Institute for General Systems Studies",
                "Benjamin Hadorn",
            ]
        ),
        "doi": "",
        "isbn": "",
        "publisher": "CyberTech Engineering and University of Fribourg",
        "licence": "all_rights_reserved",
        "archived_url": "",
        "content_hash": "",
        "review_status": "checked",
        "last_checked": "2026-08-20",
        "public_link_status": "public_link",
    }


def review_record(comparator: dict[str, Any]) -> dict[str, Any]:
    meta = comparator["meta"]
    return {
        "id": "external_map_of_systemic_evolution",
        "corpus": "Map of Systemic Evolution",
        "pages_traversed": [
            "uranos.ch cybernetics page, provenance statement and contribution invitation",
            "the supplied GraphML file, all 650 nodes",
            "the supplied GraphML file, all 1,320 edges",
            "the four declared but unpopulated description and url attribute keys",
        ],
        "reference_trails": [
            "provenance statement -> Schwarz 1996 -> Durant 1998 -> IIGSS 2000-2001 -> Hadorn 2016",
            "pale-yellow node cluster -> Fribourg coordination and CSCW work",
            "IIGSS stage -> Yi Lin, Sifeng Liu, Shoucheng OuYang, Wu Xuemou",
        ],
        "relationship_ids": [],
        "disagreement": (
            "The map asserts connection through line colour alone. This atlas holds that "
            "colour, position and neighbourhood assert nothing, so none of its 1,320 "
            "connections is imported as a relationship."
        ),
        "uncertainty": (
            "The map's pre-1950 breadth derives from a popular 1926 history of philosophy "
            "rather than from per-node sources, so it indicates where to look rather than "
            "what is established."
        ),
        "decision": (
            f"Recorded as a comparator. {meta['node_count']} nodes and "
            f"{meta['edge_count']} edges are held separately from the atlas graph, every "
            "edge marked unstated_in_source. Nothing is promoted without its own source."
        ),
    }


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    comparator = json.loads(COMPARATOR_PATH.read_text(encoding="utf-8"))
    meta = data["meta"]

    sources = data.setdefault("sources", [])
    if not any(s.get("id") == SOURCE_ID for s in sources):
        sources.append(source_record())
        sources.sort(key=lambda s: s.get("id", ""))

    for entry in data.get("corpus_register", []):
        if entry.get("id") == "corpus_comparator_maps":
            entry["status"] = "one_comparator_reviewed_programme_continuing"
            if SOURCE_ID not in entry.get("source_ids", []):
                entry.setdefault("source_ids", []).append(SOURCE_ID)

    reviews = data.setdefault("external_corpus_review", [])
    record = review_record(comparator)
    for index, existing in enumerate(reviews):
        if existing.get("id") == record["id"]:
            reviews[index] = record
            break
    else:
        reviews.append(record)

    meta["external_corpus_review_count"] = len(reviews)
    meta["source_count"] = len(sources)
    meta["comparator_systemic_evolution_url"] = PAGE_URL
    meta["comparator_systemic_evolution_documentation_url"] = REPO_DOC
    meta["comparator_systemic_evolution_node_count"] = comparator["meta"]["node_count"]
    meta["comparator_systemic_evolution_edge_count"] = comparator["meta"]["edge_count"]
    meta["comparator_systemic_evolution_unstated_edge_count"] = sum(
        1 for e in comparator["edges"] if e.get("meaning") == "unstated_in_source"
    )
    meta["comparator_count"] = 1

    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    DATA_PATH.write_text(rendered, encoding="utf-8")
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
    # Re-sync the browser copies: this script edits the canonical dataset after
    # build_public_data.py has already written them.
    (DOCS_ASSETS / "public-data.json").write_text(rendered, encoding="utf-8")
    (DOCS_ASSETS / "public-data.js").write_text(
        "window.TANGLE_DATA = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    (DOCS_ASSETS / "comparator-systemic-evolution.json").write_text(
        json.dumps(comparator, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        "Registered the Map of Systemic Evolution comparator: "
        f"{comparator['meta']['node_count']} nodes, {comparator['meta']['edge_count']} edges, "
        f"{meta['comparator_systemic_evolution_unstated_edge_count']} marked unstated_in_source, "
        "0 promoted to atlas relationships."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
