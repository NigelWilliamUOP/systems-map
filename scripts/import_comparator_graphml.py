#!/usr/bin/env python3
"""Extract the Map of Systemic Evolution into a comparator dataset.

Packet A of documentation/comparator-systemic-evolution-plan.md.

This is a deterministic extraction. It asserts nothing about what any line in
the source means. Every edge record carries `relation_type: null` and
`meaning: "unstated_in_source"`, because the source encodes relationships in
line colour alone and `semantic_contract.visual_rule` forbids treating colour,
position or neighbourhood as an unstated relation.

The source file is third-party, all-rights-reserved material (see section 2 of
the plan) and is deliberately not committed. Pass its path explicitly:

    python3 scripts/import_comparator_graphml.py /path/to/systemic_evolution.graphml

Output: data/comparator-systemic-evolution.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "comparator-systemic-evolution.json"

NS = {
    "g": "http://graphml.graphdrawing.org/xmlns",
    "y": "http://www.yworks.com/xml/graphml",
}

EXPECTED_NODES = 650
EXPECTED_EDGES = 1320

# Reader-facing names for the colour streams. These are the extractor's own
# descriptive labels for a visual grouping; they are NOT relation semantics and
# NOT the map author's stated intent, which the file nowhere records.
STREAM_LABELS = {
    "#999999": "philosophy, meaning and media",
    "#FFCC00": "social theory, constructivism and psychology",
    "#008000": "general systems and biology-derived systems theory",
    "#0000FF": "mathematics, statistics and formal systems theory",
    "#000000": "physical science, astronomy and history of science",
    "#FFFF00": "semiotics, linguistics and the logic of signs",
    "#800000": "computing, information, agents and coordination",
    "#FF0000": "cybernetics",
    "#00CCFF": "operational research and decision science",
    "#00FF00": "ecology and environmental systems",
    "#FF00FF": "engineering and instrument-making",
    "#666699": "reference work",
}


def text_of(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext())


def normalise_label(raw: str) -> str:
    """Collapse yEd's line wrapping without losing the original text."""
    lines = [line.strip() for line in raw.split("\n") if line.strip()]
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def parse_year(label: str) -> str:
    """Return a bracketed or trailing year exactly as the source writes it."""
    bracketed = re.search(r"\[([^\]]*)\]", label)
    if bracketed:
        return bracketed.group(1).strip()
    trailing = re.search(r"c?\.?\s*\d{3,4}\s*[-–]\s*\d{3,4}\s*(?:BC)?\s*$", label)
    return trailing.group(0).strip() if trailing else ""


def extract_nodes(root: ET.Element) -> list[dict[str, Any]]:
    records = []
    for node in root.findall(".//g:node", NS):
        shape = node.find(".//y:ShapeNode", NS)
        label_el = node.find(".//y:NodeLabel", NS)
        geometry = shape.find("y:Geometry", NS) if shape is not None else None
        border = shape.find("y:BorderStyle", NS) if shape is not None else None
        fill = shape.find("y:Fill", NS) if shape is not None else None
        shape_type = shape.find("y:Shape", NS) if shape is not None else None

        raw_label = text_of(label_el)
        border_colour = border.get("color") if border is not None else None
        records.append(
            {
                "source_node_id": node.get("id"),
                "raw_label": raw_label,
                "label": normalise_label(raw_label),
                "year_as_written": parse_year(normalise_label(raw_label)),
                "border_colour": border_colour,
                "border_width": border.get("width") if border is not None else None,
                "border_type": border.get("type") if border is not None else None,
                "fill_colour": fill.get("color") if fill is not None else None,
                "shape": shape_type.get("type") if shape_type is not None else None,
                "font_size": label_el.get("fontSize") if label_el is not None else None,
                "x": float(geometry.get("x")) if geometry is not None else None,
                "y": float(geometry.get("y")) if geometry is not None else None,
                "width": float(geometry.get("width")) if geometry is not None else None,
                "height": float(geometry.get("height")) if geometry is not None else None,
                "colour_stream_label": STREAM_LABELS.get(border_colour, "unclassified"),
                "source_url": text_of(node.find("g:data[@key='d4']", NS)).strip(),
                "source_description": text_of(node.find("g:data[@key='d5']", NS)).strip(),
            }
        )
    return records


def extract_edges(root: ET.Element) -> list[dict[str, Any]]:
    records = []
    for index, edge in enumerate(root.findall(".//g:edge", NS)):
        line = edge.find(".//y:LineStyle", NS)
        arrows = edge.find(".//y:Arrows", NS)
        label_el = edge.find(".//y:EdgeLabel", NS)
        records.append(
            {
                "comparator_edge_id": edge.get("id") or f"e{index}",
                "source_node_id": edge.get("source"),
                "target_node_id": edge.get("target"),
                "line_colour": line.get("color") if line is not None else None,
                "line_width": line.get("width") if line is not None else None,
                "line_style": line.get("type") if line is not None else None,
                "source_arrow": arrows.get("source") if arrows is not None else None,
                "target_arrow": arrows.get("target") if arrows is not None else None,
                "edge_label_in_source": text_of(label_el).strip(),
                # The two fields that keep this dataset honest.
                "relation_type": None,
                "meaning": "unstated_in_source",
            }
        )
    return records


def build(graphml_path: Path) -> dict[str, Any]:
    root = ET.parse(graphml_path).getroot()
    nodes = extract_nodes(root)
    edges = extract_edges(root)

    labelled_edges = [e for e in edges if e["edge_label_in_source"]]
    colour_census: dict[str, int] = {}
    for node in nodes:
        colour_census[node["border_colour"]] = colour_census.get(node["border_colour"], 0) + 1

    return {
        "meta": {
            "dataset": "comparator-systemic-evolution",
            "title": "Map of Systemic Evolution",
            "role": "comparator corpus, not atlas content",
            "provenance": [
                "Originated 1996 by Dr Eric Schwarz, Neuchatel, Switzerland.",
                "Extended 1998, including items from 'The Story of Philosophy' by Will Durant.",
                "Elaborated 2000-2001 for the International Institute for General Systems Studies.",
                "Extended 2016 by Benjamin Hadorn, Fribourg, Switzerland.",
            ],
            "published_at": "https://uranos.ch/index.php/research-menu/cybernetcis",
            "rights": (
                "(c) 2020 CyberTech Engineering and University of Fribourg, all rights "
                "reserved. Included here as a cited comparator under RIGHTS.md; the "
                "source file is not redistributed and no node text is republished as "
                "atlas content."
            ),
            "semantics": (
                "The source states no meaning for any edge. Relationships are encoded in "
                "line colour alone. Per semantic_contract.visual_rule, colour, position "
                "and neighbourhood do not assert a relation, so every edge here carries "
                "relation_type null and meaning 'unstated_in_source'."
            ),
            "colour_stream_caveat": (
                "colour_stream_label is this extractor's description of a visual grouping. "
                "It is not the map author's stated intent, which the file nowhere records, "
                "and it is not a relation type."
            ),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "labelled_edge_count": len(labelled_edges),
            "node_colour_census": dict(sorted(colour_census.items(), key=lambda kv: -kv[1])),
        },
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graphml", help="path to systemic_evolution.graphml")
    parser.add_argument("--out", default=str(OUT_PATH))
    args = parser.parse_args()

    path = Path(args.graphml).expanduser()
    if not path.is_file():
        print(f"Not found: {path}", file=sys.stderr)
        return 2

    data = build(path)
    errors = []
    if data["meta"]["node_count"] != EXPECTED_NODES:
        errors.append(f"expected {EXPECTED_NODES} nodes, got {data['meta']['node_count']}")
    if data["meta"]["edge_count"] != EXPECTED_EDGES:
        errors.append(f"expected {EXPECTED_EDGES} edges, got {data['meta']['edge_count']}")
    if data["meta"]["labelled_edge_count"]:
        errors.append(
            f"{data['meta']['labelled_edge_count']} edges carry a label; the extractor "
            "assumed none do and the semantics note must be revisited"
        )
    if any(e["relation_type"] is not None for e in data["edges"]):
        errors.append("an edge carries an asserted relation_type")
    if errors:
        for message in errors:
            print(f"FAILED: {message}", file=sys.stderr)
        return 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(data, indent=1, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}: "
        f"{data['meta']['node_count']} nodes, {data['meta']['edge_count']} edges, "
        f"0 with an asserted relation type."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
