from recruit_ai.job.schema import JobProfile

from recruit_ai.candidate.graph_schema import (
    CandidateGraph,
    GraphNode,
    GraphEdge,
)


def build_job_graph(job: JobProfile) -> CandidateGraph:

    graph = CandidateGraph()

    job_id = "job"

    graph.nodes.append(
        GraphNode(
            id=job_id,
            type="job",
            value=job.title,
        )
    )

    # --------------------------
    # Required Skills
    # --------------------------

    for i, skill in enumerate(job.required_skills):

        node_id = f"required_skill_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="skill",
                value=skill,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=job_id,
                target=node_id,
                relation="REQUIRES_SKILL",
            )
        )

    # --------------------------
    # Preferred Skills
    # --------------------------

    for i, skill in enumerate(job.preferred_skills):

        node_id = f"preferred_skill_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="skill",
                value=skill,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=job_id,
                target=node_id,
                relation="PREFERS_SKILL",
            )
        )

    # --------------------------
    # Education
    # --------------------------

    for i, edu in enumerate(job.education):

        node_id = f"education_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="education",
                value=edu,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=job_id,
                target=node_id,
                relation="REQUIRES_EDUCATION",
            )
        )

    # --------------------------
    # Experience
    # --------------------------

    for i, exp in enumerate(job.experience):

        node_id = f"experience_{i}"

        graph.nodes.append(
            GraphNode(
                id=node_id,
                type="experience",
                value=exp,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=job_id,
                target=node_id,
                relation="REQUIRES_EXPERIENCE",
            )
        )

    return graph