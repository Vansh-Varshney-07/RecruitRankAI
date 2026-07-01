import streamlit as st


def sidebar():

    st.sidebar.title("RecruitRankAI")

    st.sidebar.caption("Rank signal-rich candidates against a live job profile.")

    uploaded_job = st.sidebar.file_uploader(
        "Upload Job Description",
        type=["txt", "pdf"],
        help="Supports TXT and PDF job descriptions.",
    )

    minimum_score = st.sidebar.slider(
        "Minimum Score",
        0,
        100,
        50,
    )

    candidate_limit = st.sidebar.slider(
        "Candidate Scan Limit",
        100,
        10000,
        2000,
        step=100,
    )

    max_results = st.sidebar.slider(
        "Results to Show",
        5,
        100,
        25,
        step=5,
    )

    search_query = st.sidebar.text_input(
        "Search Results",
        placeholder="Name, skill, location...",
    )

    show_job_preview = st.sidebar.toggle(
        "Show Job Text Preview",
        value=False,
    )

    use_llm = st.sidebar.toggle(
        "LLM Recruiter Brain",
        value=False,
        help="Uses local Ollama to review and adjust the visible shortlist. Falls back safely if Ollama is offline.",
    )

    llm_limit = st.sidebar.slider(
        "LLM Review Depth",
        3,
        25,
        8,
        step=1,
        disabled=not use_llm,
    )

    run_ranking = st.sidebar.button(
        "Run Ranking",
        type="primary",
    )

    return {
        "uploaded_job": uploaded_job,
        "minimum_score": minimum_score / 100,
        "candidate_limit": candidate_limit,
        "max_results": max_results,
        "search_query": search_query.strip(),
        "show_job_preview": show_job_preview,
        "use_llm": use_llm,
        "llm_limit": llm_limit,
        "run_ranking": run_ranking,
    }
