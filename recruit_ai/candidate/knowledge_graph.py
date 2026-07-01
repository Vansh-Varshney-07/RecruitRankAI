from recruit_ai.candidate.schema import CandidateProfile

from recruit_ai.candidate.graph_schema import (
    CandidateGraph,
    GraphNode,
    GraphEdge,
)


def build_graph(profile: CandidateProfile) -> CandidateGraph:

    graph = CandidateGraph()

    candidate_id = "candidate"

    graph.nodes.append(
        GraphNode(
            id=candidate_id,
            type="candidate",
            value=profile.name,
        )
    )

    # --------------------------
    # Skills
    # --------------------------

    for i, skill in enumerate(profile.skills):

        node_id = f"skill_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="skill",
                value=skill.name,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=candidate_id,
                target=node_id,
                relation="HAS_SKILL",
            )
        )

    # --------------------------
    # Education
    # --------------------------

    for i, edu in enumerate(profile.education):

        node_id = f"edu_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="education",
                value=edu.degree,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=candidate_id,
                target=node_id,
                relation="HAS_EDUCATION",
            )
        )

    # --------------------------
    # Projects
    # --------------------------

    for i, project in enumerate(profile.projects):

        node_id = f"project_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="project",
                value=project.title,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=candidate_id,
                target=node_id,
                relation="HAS_PROJECT",
            )
        )

    # --------------------------
    # Certifications
    # --------------------------

    for i, cert in enumerate(profile.certifications):

        node_id = f"cert_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="certification",
                value=cert.name,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=candidate_id,
                target=node_id,
                relation="HAS_CERTIFICATION",
            )
        )

    # --------------------------
    # Research Interests
    # --------------------------

    for i, research in enumerate(profile.research_interests):

        node_id = f"research_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="research",
                value=research.topic,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=candidate_id,
                target=node_id,
                relation="HAS_RESEARCH",
            )
        )

    return graph