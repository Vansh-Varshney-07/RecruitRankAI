from dataclasses import dataclass, field


@dataclass
class GraphNode:

    id: str

    type: str

    value: str


@dataclass
class GraphEdge:

    source: str

    target: str

    relation: str


@dataclass
class CandidateGraph:

    nodes: list[GraphNode] = field(default_factory=list)

    edges: list[GraphEdge] = field(default_factory=list)