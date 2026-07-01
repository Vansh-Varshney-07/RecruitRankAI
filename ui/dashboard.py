import streamlit as st

import csv
import io
from html import escape
from pathlib import Path

from recruit_ai.ingestion.pdf_loader import extract_text_from_pdf_bytes
from recruit_ai.job.parser import parse_job
from recruit_ai.ranking.redrob_ranker import filter_rankings, rank_redrob_candidates
from recruit_ai.reasoning.explanation import match_explanation
from recruit_ai.reasoning.recommendation import recommend
from recruit_ai.reasoning.recruiter_brain import apply_llm_score_delta
from recruit_ai.reasoning.recruiter_brain import review_candidate_with_llm
from ui.cards import candidate_card
from ui.charts import score_chart
from ui.styles import load_css


DEFAULT_JOB_PATH = Path("data/raw/jobs/job1.txt")


@st.cache_data(show_spinner=False)
def load_default_job() -> str:
    if DEFAULT_JOB_PATH.exists():
        return DEFAULT_JOB_PATH.read_text(encoding="utf-8")

    return """Machine Learning Engineer

REQUIRED SKILLS

Python
Machine Learning
SQL

PREFERRED SKILLS

Docker
Linux

EXPERIENCE

2+ years
"""


@st.cache_data(show_spinner=False)
def cached_rankings(job_text: str, candidate_limit: int) -> list[dict]:
    job = parse_job(job_text)
    return rank_redrob_candidates(
        job=job,
        limit=candidate_limit,
    )


def _job_text_from_upload(uploaded_job) -> str:
    if uploaded_job is None:
        return load_default_job()

    file_name = uploaded_job.name.lower()
    file_bytes = uploaded_job.getvalue()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf_bytes(file_bytes)

    if file_name.endswith(".txt"):
        return file_bytes.decode("utf-8-sig")

    raise ValueError("Unsupported job description format.")


def _to_card(item: dict, job) -> dict:
    candidate = item["candidate"]
    skills = [
        skill.name
        for skill in candidate.skills
        if skill.name
    ]
    explanation = match_explanation(
        candidate,
        job,
        item["breakdown"],
    )

    return {
        "candidate_id": candidate.candidate_id,
        "name": candidate.name or "Unnamed Candidate",
        "headline": candidate.headline,
        "location": candidate.location,
        "years_of_experience": candidate.years_of_experience,
        "education": [
            {
                "degree": education.degree,
                "institute": education.institute,
                "field_of_study": education.field_of_study,
                "year": education.year,
            }
            for education in candidate.education[:3]
        ],
        "experience": [
            {
                "title": experience.title,
                "company": experience.company,
                "duration_months": experience.duration_months,
                "description": experience.description,
                "is_current": experience.is_current,
            }
            for experience in candidate.experience[:4]
        ],
        "signals": candidate.signals,
        "skills": skills,
        "score": item["score"],
        "breakdown": item["breakdown"],
        "explanation": explanation,
        "llm_review": item.get("llm_review"),
        "recommendation": recommend(item["score"]),
    }


def _review_shortlist_with_llm(items: list[dict], job, limit: int) -> list[dict]:
    reviewed = []

    for index, item in enumerate(items):
        if index >= limit:
            reviewed.append(item)
            continue

        review = review_candidate_with_llm(
            item["candidate"],
            job,
            item["breakdown"],
        )
        reviewed.append(
            apply_llm_score_delta(
                item,
                review,
            )
        )

    reviewed.sort(
        key=lambda item: (
            -item["score"],
            item["candidate"].candidate_id,
        ),
    )
    return reviewed


def _matches_query(item: dict, query: str) -> bool:
    if not query:
        return True

    candidate = item["candidate"]
    haystack = " ".join(
        [
            candidate.name,
            candidate.headline,
            candidate.location,
            " ".join(skill.name for skill in candidate.skills),
        ]
    ).lower()

    return query.lower() in haystack


def _download_csv(items: list[dict], job) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "rank",
            "candidate_id",
            "name",
            "headline",
            "location",
            "score",
            "recommendation",
            "matched_required_skills",
            "missing_required_skills",
        ]
    )

    for rank, item in enumerate(items, start=1):
        card = _to_card(item, job)
        explanation = card["explanation"]
        writer.writerow(
            [
                rank,
                card["candidate_id"],
                card["name"],
                card["headline"],
                card["location"],
                card["score"],
                card["recommendation"],
                "; ".join(explanation["matched_skills"]),
                "; ".join(explanation["missing_skills"]),
            ]
        )

    return buffer.getvalue()


def _control_panel() -> dict:
    with st.container():
        st.markdown(
            """
            <div class="rr-section-head">
                <div>
                    <h2>Ranking Controls</h2>
                    <p>Upload a TXT/PDF job description, tune the scan, then generate a shortlist.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=False):
            upload_col, scan_col, action_col = st.columns([1.4, 1, 1])

            with upload_col:
                uploaded_job = st.file_uploader(
                    "Job Description",
                    type=["txt", "pdf"],
                    help="Supports TXT and PDF job descriptions.",
                    key="main_job_upload",
                )
                search_query = st.text_input(
                    "Search Results",
                    placeholder="Name, skill, location...",
                    key="main_search_query",
                )

            with scan_col:
                minimum_score = st.slider(
                    "Minimum Score",
                    0,
                    100,
                    50,
                    key="main_minimum_score",
                )
                candidate_limit = st.slider(
                    "Candidate Scan Limit",
                    100,
                    10000,
                    2000,
                    step=100,
                    key="main_candidate_limit",
                )
                max_results = st.slider(
                    "Results to Show",
                    5,
                    100,
                    25,
                    step=5,
                    key="main_max_results",
                )

            with action_col:
                show_job_preview = st.toggle(
                    "Show Job Text Preview",
                    value=False,
                    key="main_show_job_preview",
                )
                use_llm = st.toggle(
                    "LLM Recruiter Brain",
                    value=False,
                    help="Uses local Ollama to review and adjust the visible shortlist.",
                    key="main_use_llm",
                )
                llm_limit = st.slider(
                    "LLM Review Depth",
                    3,
                    25,
                    8,
                    step=1,
                    disabled=not use_llm,
                    key="main_llm_limit",
                )

                run_clicked = st.button(
                    "Run Ranking",
                    type="primary",
                    use_container_width=True,
                    key="main_run_ranking",
                )

                back_clicked = st.button(
                    "Back to setup",
                    use_container_width=True,
                    key="main_back_to_setup",
                )

    if "rank_requested" not in st.session_state:
        st.session_state.rank_requested = False

    if run_clicked:
        st.session_state.rank_requested = True

    if back_clicked:
        st.session_state.rank_requested = False
        cached_rankings.clear()

    return {
        "uploaded_job": uploaded_job,
        "minimum_score": minimum_score / 100,
        "candidate_limit": candidate_limit,
        "max_results": max_results,
        "search_query": search_query.strip(),
        "show_job_preview": show_job_preview,
        "use_llm": use_llm,
        "llm_limit": llm_limit,
        "run_ranking": st.session_state.rank_requested,
    }


def _hired_panel() -> None:
    hired = st.session_state.get("hired_candidates", [])

    if not hired:
        return

    rows = "\n".join(
        f"""
        <div class="rr-hire-row">
            <strong>{escape(item["name"])}</strong>
            <span>{escape(item["candidate_id"])} / {item["score"] * 100:.0f}% / {escape(item["recommendation"])}</span>
        </div>
        """
        for item in hired
    )

    st.markdown(
        f"""
        <div class="rr-hire-panel">
            <h3>Recruiter Action Board</h3>
            <p>{len(hired)} candidate(s) marked for hiring or follow-up.</p>
            {rows}
        </div>
        """,
        unsafe_allow_html=True,
    )

    hire_csv = "candidate_id,name,score,recommendation\n" + "\n".join(
        f'{item["candidate_id"]},"{item["name"]}",{item["score"]:.4f},"{item["recommendation"]}"'
        for item in hired
    )

    st.download_button(
        "Download Hire List",
        data=hire_csv,
        file_name="recruitrankai_hire_list.csv",
        mime="text/csv",
        use_container_width=True,
    )


def _skill_chips(label: str, skills: list[str], class_name: str) -> None:
    chips = "\n".join(
        f'<span class="rr-skill {class_name}">{escape(skill)}</span>'
        for skill in skills[:14]
    )

    if not chips:
        chips = '<span class="rr-skill">No skills parsed</span>'

    st.markdown(
        f"""
        <div class="rr-panel">
            <h3>{escape(label)}</h3>
            <div class="rr-skill-grid">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _summary(filtered: list[dict], scanned: int, minimum_score: float) -> None:
    top_score = filtered[0]["score"] if filtered else 0
    avg_score = sum(item["score"] for item in filtered) / len(filtered) if filtered else 0

    st.markdown(
        f"""
        <div class="rr-summary">
            <div class="rr-summary-item">
                <div class="rr-summary-value">{len(filtered)}</div>
                <div class="rr-summary-label">qualified candidates</div>
            </div>
            <div class="rr-summary-item">
                <div class="rr-summary-value">{top_score * 100:.0f}%</div>
                <div class="rr-summary-label">top match score</div>
            </div>
            <div class="rr-summary-item">
                <div class="rr-summary-value">{avg_score * 100:.0f}%</div>
                <div class="rr-summary-label">average qualified score</div>
            </div>
            <div class="rr-summary-item">
                <div class="rr-summary-value">{scanned}</div>
                <div class="rr-summary-label">candidate scan limit at {minimum_score * 100:.0f}% floor</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_dashboard():

    load_css()

    st.markdown(
        """
        <section class="rr-hero">
            <div class="rr-kicker">Recruitment Intelligence</div>
            <h1 class="rr-title">RecruitRank<span>AI</span></h1>
            <p class="rr-copy">
                A signal-first ranking cockpit for comparing real candidates against a structured job profile.
                Built around skills, semantic fit, experience, education, and recruiter-ready scoring.
            </p>
            <div class="rr-strip">
                <span class="rr-chip">Peach / Cyan / Ink</span>
                <span class="rr-chip">Redrob candidate graph</span>
                <span class="rr-chip">Offline deterministic scoring</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    controls = _control_panel()

    try:
        job_text = _job_text_from_upload(controls["uploaded_job"])
    except ValueError as error:
        st.error(str(error))
        return

    if not job_text.strip():
        st.error("The uploaded job description did not contain readable text.")
        return

    job = parse_job(job_text)

    st.markdown(
        f"""
        <section class="rr-job-card">
            <div>
                <p class="rr-job-kicker">Job Intelligence</p>
                <h2>{escape(job.title or "Job Description")}</h2>
                <p>{len(job.required_skills)} required skills / {len(job.preferred_skills)} preferred skills parsed from the active job description.</p>
            </div>
            <div class="rr-job-stats">
                <div>
                    <span>Scan Limit</span>
                    <strong>{controls["candidate_limit"]}</strong>
                </div>
                <div>
                    <span>Minimum Score</span>
                    <strong>{controls["minimum_score"] * 100:.0f}%</strong>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    skill_left, skill_right = st.columns(2)

    with skill_left:
        _skill_chips("Required Signals", job.required_skills, "required")

    with skill_right:
        _skill_chips("Preferred Signals", job.preferred_skills, "preferred")

    if controls["show_job_preview"]:
        st.markdown(
            f"""
            <div class="rr-panel">
                <h3>Parsed Job Preview</h3>
                <p>{escape(job_text[:1200])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="rr-section-head">
            <div>
                <h2>Top Candidates</h2>
                <p>Ranked by weighted match quality.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not controls["run_ranking"]:
        st.markdown(
            """
            <div class="rr-empty">
                Upload a job description or use the sample job, then run ranking.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    with st.spinner("Ranking candidates..."):
        rankings = cached_rankings(
            job_text,
            controls["candidate_limit"],
        )

    filtered = filter_rankings(
        rankings,
        controls["minimum_score"],
    )

    filtered = [
        item
        for item in filtered
        if _matches_query(item, controls["search_query"])
    ]

    if not filtered:
        st.markdown(
            """
            <div class="rr-empty">
                No candidates matched the selected minimum score.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if controls["use_llm"]:
        with st.spinner("Recruiter brain is reviewing the shortlist..."):
            filtered = _review_shortlist_with_llm(
                filtered,
                job,
                controls["llm_limit"],
            )

    _summary(filtered, controls["candidate_limit"], controls["minimum_score"])

    st.download_button(
        "Download Ranked CSV",
        data=_download_csv(filtered, job),
        file_name="recruitrankai_rankings.csv",
        mime="text/csv",
        use_container_width=True,
    )

    _hired_panel()

    top_cards = []

    for rank, item in enumerate(filtered[:10], start=1):
        card = _to_card(item, job)
        card["rank"] = rank
        top_cards.append(card)

    score_chart(top_cards)

    for rank, item in enumerate(filtered[:controls["max_results"]], start=1):
        card = _to_card(item, job)
        card["rank"] = rank
        candidate_card(card)
