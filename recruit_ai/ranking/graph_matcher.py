from recruit_ai.candidate.graph_schema import CandidateGraph


def graph_skill_score(
    candidate_graph: CandidateGraph,
    job_graph: CandidateGraph,
):
    """
    Compare candidate skills with job required skills.
    """

    candidate_skills = {
        node.value.lower()
        for node in candidate_graph.nodes
        if node.type == "skill"
    }

    required_skills = {
        node.value.lower()
        for node in job_graph.nodes
        if node.id.startswith("required_skill")
    }

    if not required_skills:
        return 0.0

    matched = candidate_skills.intersection(required_skills)

    return len(matched) / len(required_skills)