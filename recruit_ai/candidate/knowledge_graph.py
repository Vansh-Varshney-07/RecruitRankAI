from recruit_ai.candidate.schema import CandidateProfile

from recruit_ai.candidate.graph_schema import (
    CandidateGraph,
    GraphNode,
    GraphEdge,
)


def build_graph(profile: CandidateProfile) -> CandidateGraph:

    graph = CandidateGraph()

    # ---------------------------------
    # Candidate Node
    # ---------------------------------

    candidate_id = "candidate"

    graph.nodes.append(
        GraphNode(
            id=candidate_id,
            type="candidate",
            value=profile.name,
        )
    )

    return graph