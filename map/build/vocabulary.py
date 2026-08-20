#!/usr/bin/env python3
"""Candidate concept vocabulary for our map.

Seeded from the three prior maps and from terms mined out of the corpus's own
titles. Seeding decides only what gets *tested*; whether a concept reaches the
map is decided by evidence in build_map.py.
"""
from __future__ import annotations

# Concepts named by the prior maps or standard in the field. Each entry is
# (canonical label, [aliases matched case-insensitively as whole phrases]).
# Aliases exist to catch spelling variants, not to widen a concept's meaning.
SEED = [
    ("Cybernetics", ["cybernetics", "cybernetic"]),
    ("Second-order cybernetics", ["second-order cybernetics", "second order cybernetics",
                                  "cybernetics of cybernetics"]),
    ("Management cybernetics", ["management cybernetics", "organisational cybernetics",
                                "organizational cybernetics"]),
    ("Viable System Model", ["viable system model", "viable systems model", "vsm"]),
    ("General system theory", ["general system theory", "general systems theory"]),
    ("Requisite variety", ["requisite variety", "law of requisite variety"]),
    ("Homeostasis", ["homeostasis", "homeostatic"]),
    ("Feedback", ["feedback loop", "negative feedback", "positive feedback",
                  "feedback control"]),
    ("Autopoiesis", ["autopoiesis", "autopoietic"]),
    ("Self-organisation", ["self-organisation", "self-organization", "self-organising",
                           "self-organizing"]),
    ("Emergence", ["emergence", "emergent propert", "emergent behaviour", "emergent behavior"]),
    ("Complexity science", ["complexity science", "complexity sciences", "complexity theory"]),
    ("Complex adaptive systems", ["complex adaptive system", "complex adaptive systems"]),
    ("Chaos theory", ["chaos theory", "deterministic chaos", "chaotic dynamics"]),
    ("Self-organised criticality", ["self-organised criticality", "self-organized criticality"]),
    ("Network science", ["network science", "complex network", "complex networks",
                         "small-world network", "scale-free network"]),
    ("Agent-based modelling", ["agent-based model", "agent based model", "agent-based simulation",
                               "multi-agent system", "multiagent system"]),
    ("Cellular automata", ["cellular automat"]),
    ("Artificial life", ["artificial life", "alife"]),
    ("System dynamics", ["system dynamics", "systems dynamics", "stock and flow"]),
    ("Soft systems methodology", ["soft systems methodolog", "soft systems thinking", "ssm"]),
    ("Critical systems thinking", ["critical systems thinking", "critical systems heuristics",
                                   "critical systems practice", "boundary critique"]),
    ("Systems thinking", ["systems thinking"]),
    ("Systems practice", ["systems practice", "systemic practice"]),
    ("Operational research", ["operational research", "operations research", "problem structuring method"]),
    ("Cynefin and sense-making", ["cynefin", "sense-making", "sensemaking"]),
    ("Social systems theory", ["social systems theory", "social system theory",
                               "functional differentiation"]),
    ("Sociocybernetics", ["sociocybernetics", "socio-cybernetics"]),
    ("Information theory", ["information theory", "shannon entropy", "channel capacity"]),
    ("Second law and entropy", ["thermodynamic entropy", "dissipative structure",
                                "far-from-equilibrium", "non-equilibrium thermodynamics"]),
    ("Cognition and enaction", ["enaction", "enactive", "embodied cognition", "structural coupling"]),
    ("Constructivism", ["radical constructivism", "constructivist epistemolog"]),
    ("Semiotics", ["semiotics", "biosemiotics", "semiosis"]),
    ("Hierarchy theory", ["hierarchy theory", "holon", "holarchy"]),
    ("Living systems theory", ["living systems theory", "living system theory"]),
    ("Resilience", ["resilience", "panarchy", "adaptive cycle"]),
    ("Systems ecology", ["systems ecology", "ecosystem model", "energy systems language"]),
    ("Sustainability and limits", ["limits to growth", "planetary boundaries",
                                   "sustainability transition"]),
    ("Socio-technical systems", ["socio-technical system", "sociotechnical system"]),
    ("Systems engineering", ["systems engineering", "system of systems"]),
    ("Control theory", ["control theory", "optimal control", "feedback controller"]),
    ("Game theory", ["game theory", "evolutionary game", "prisoner's dilemma"]),
    ("Decision theory", ["decision theory", "decision analysis", "multi-criteria decision"]),
    ("Organisational learning", ["organisational learning", "organizational learning",
                                 "double-loop learning", "learning organisation",
                                 "learning organization"]),
    ("Action research", ["action research", "participatory action research"]),
    ("Knowledge management", ["knowledge management", "knowledge creation"]),
    ("Design thinking", ["design thinking", "systemic design", "design science"]),
    ("Human-computer interaction", ["human-computer interaction", "computer-supported cooperative work",
                                    "cscw"]),
    ("Coordination theory", ["coordination theory", "coordination mechanism"]),
    ("Ubiquitous computing", ["ubiquitous computing", "pervasive computing", "internet of things"]),
    ("Machine learning and AI", ["artificial intelligence", "machine learning", "neural network",
                                 "deep learning"]),
    ("Cognitive science", ["cognitive science", "cognitive architecture"]),
    ("Evolutionary theory", ["natural selection", "evolutionary dynamics", "coevolution",
                             "co-evolution"]),
    ("Dialectical systems theory", ["dialectical systems theory", "requisite holism"]),
    ("Grey systems", ["grey system", "grey systems"]),
    ("Fuzzy systems", ["fuzzy set", "fuzzy logic", "fuzzy system"]),
    ("Tektology and early systems", ["tektology", "tektologiya"]),
    ("Boundaries and observers", ["boundary judgement", "boundary judgment", "observer dependence",
                                  "second-order observation"]),
    ("Variety engineering", ["variety engineering", "variety attenuat", "variety amplif"]),
    ("Recursion", ["recursive structure", "recursion level", "recursive organisation",
                   "recursive organization"]),
]

def concept_id(label: str) -> str:
    import re
    slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    return f"concept_{slug}"
