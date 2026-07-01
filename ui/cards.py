from html import escape

import streamlit as st

from recruit_ai.reasoning.recommendation import recommend


def _pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def candidate_card(candidate):
    score = max(0.0, min(float(candidate["score"]), 1.0))
    breakdown = candidate.get("breakdown", {})
    recommendation = candidate.get("recommendation") or recommend(score)
    candidate_id = candidate.get("candidate_id", "")
    headline = candidate.get("headline", "")
    rank = candidate.get("rank", "")
    location = candidate.get("location", "")
    years = candidate.get("years_of_experience", 0)
    skills = candidate.get("skills", [])
    explanation = candidate.get("explanation", {})
    llm_review = candidate.get("llm_review")

    details = [
        f"Skills {breakdown.get('skill', 0):.2f}",
        f"Semantic {breakdown.get('semantic', 0):.2f}",
        f"Experience {breakdown.get('experience', 0):.2f}",
        f"Education {breakdown.get('education', 0):.2f}",
    ]
    meta = " / ".join(
        item
        for item in [
            candidate_id,
            location,
            f"{years:.1f} yrs" if years else "",
        ]
        if item
    )
    skill_chips = "".join(
        f'<span class="rr-mini-skill">{escape(skill)}</span>'
        for skill in skills[:6]
    )
    reasons = " ".join(explanation.get("reasons", []))
    missing = explanation.get("missing_skills", [])
    missing_text = ""
    brain_text = ""
    question_text = ""

    if missing:
        missing_text = f"Missing: {', '.join(missing[:4])}"

    if llm_review:
        mode = "LLM" if llm_review.used_llm else "Fallback"
        brain_text = f"{mode} brain: {llm_review.summary}"

        if llm_review.interview_questions:
            question_text = f"Probe: {llm_review.interview_questions[0]}"

    st.markdown(
        f"""
        <article class="rr-card">
            <div class="rr-rank">{escape(str(rank))}</div>
            <div class="rr-card-top">
                <div>
                    <h3 class="rr-name">{escape(candidate["name"])}</h3>
                    <div class="rr-headline">{escape(headline)}</div>
                    <div class="rr-meta">{escape(meta)}</div>
                </div>
                <div>
                    <div class="rr-score">{_pct(score)}</div>
                    <div class="rr-rec">{escape(recommendation)}</div>
                </div>
            </div>
            <div class="rr-bar"><span style="width: {_pct(score)}"></span></div>
            <div class="rr-mini-skill-grid">{skill_chips}</div>
            <div class="rr-explain">{escape(reasons)}</div>
            <div class="rr-brain">{escape(brain_text)}</div>
            <div class="rr-question">{escape(question_text)}</div>
            <div class="rr-missing">{escape(missing_text)}</div>
            <div class="rr-breakdown">{escape(" / ".join(details))}</div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    action_left, action_right = st.columns([1, 1])

    with action_left:
        with st.expander(
            f"Review profile - {candidate['name']}",
            expanded=False,
        ):
            st.markdown("#### Candidate Snapshot")
            st.write(
                {
                    "Candidate ID": candidate_id,
                    "Headline": headline,
                    "Location": location,
                    "Experience": f"{years:.1f} years" if years else "Not available",
                    "Recommendation": recommendation,
                    "Score": _pct(score),
                }
            )

            st.markdown("#### Skills")
            st.write(", ".join(skills[:20]) or "No skills available.")

            st.markdown("#### Experience")
            for item in candidate.get("experience", []):
                title = item.get("title") or "Role"
                company = item.get("company") or "Company unavailable"
                months = item.get("duration_months", 0)
                description = item.get("description", "")
                st.markdown(f"**{title}** at {company} ({months} months)")
                if description:
                    st.caption(description[:700])

            st.markdown("#### Education")
            for item in candidate.get("education", []):
                degree = item.get("degree") or "Degree"
                institute = item.get("institute") or "Institute unavailable"
                field = item.get("field_of_study") or ""
                st.markdown(f"**{degree}** {field} - {institute}")

            st.markdown("#### Activity Signals")
            signals = candidate.get("signals", {})
            st.write(
                {
                    "Open to work": signals.get("open_to_work_flag"),
                    "Profile completeness": signals.get("profile_completeness_score"),
                    "Recruiter response rate": signals.get("recruiter_response_rate"),
                    "Notice period days": signals.get("notice_period_days"),
                    "GitHub activity": signals.get("github_activity_score"),
                }
            )

    with action_right:
        hire_key = f"hire_{candidate_id}_{rank}"

        if st.button(
            "Hire / Shortlist",
            key=hire_key,
            use_container_width=True,
        ):
            if "hired_candidates" not in st.session_state:
                st.session_state.hired_candidates = []

            existing = {
                item["candidate_id"]
                for item in st.session_state.hired_candidates
            }

            if candidate_id not in existing:
                st.session_state.hired_candidates.append(
                    {
                        "candidate_id": candidate_id,
                        "name": candidate["name"],
                        "score": score,
                        "recommendation": recommendation,
                    }
                )
                st.success(f"{candidate['name']} added to hire list.")
            else:
                st.info(f"{candidate['name']} is already in the hire list.")
