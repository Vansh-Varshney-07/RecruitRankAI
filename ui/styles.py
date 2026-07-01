import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        :root {
            --ink: #080a12;
            --peach: #ffb199;
            --cyan: #6ff3ff;
            --glass: rgba(255, 255, 255, 0.075);
            --line: rgba(255, 255, 255, 0.14);
            --muted: rgba(246, 247, 251, 0.68);
            --text: #f6f7fb;
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            color: var(--text);
            background:
                conic-gradient(from 210deg at 55% -10%, rgba(111, 243, 255, 0.24), rgba(255, 177, 153, 0.28), rgba(8, 10, 18, 0.0), rgba(111, 243, 255, 0.16)),
                linear-gradient(135deg, #080a12 0%, #10131f 42%, #080a12 100%);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
            background-size: 44px 44px;
            mask-image: linear-gradient(to bottom, black, transparent 82%);
        }

        .block-container {
            max-width: 1240px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        .stDeployButton,
        #MainMenu,
        footer {
            display: none;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(8, 10, 18, 0.96), rgba(8, 10, 18, 0.84)),
                conic-gradient(from 240deg at 50% 0%, rgba(255, 177, 153, 0.18), rgba(111, 243, 255, 0.10), transparent 34%);
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p {
            color: var(--text);
        }

        [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
            background: rgba(255,255,255,0.05);
            border: 1px dashed rgba(111, 243, 255, 0.36);
            border-radius: 8px;
        }

        .stButton > button {
            width: 100%;
            border: 1px solid rgba(111, 243, 255, 0.45);
            border-radius: 8px;
            color: #080a12;
            background: linear-gradient(135deg, var(--cyan), var(--peach));
            font-weight: 800;
            box-shadow: 0 18px 44px rgba(111, 243, 255, 0.16);
        }

        .stButton > button:hover {
            border-color: var(--peach);
            filter: saturate(1.08) brightness(1.04);
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.06);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
        }

        div[data-testid="stAlert"] {
            border-radius: 8px;
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.07);
        }

        .rr-hero {
            position: relative;
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 2.4rem;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.035)),
                conic-gradient(from 155deg at 70% 8%, rgba(255, 177, 153, 0.34), rgba(111, 243, 255, 0.20), transparent 42%, rgba(255, 177, 153, 0.22));
            box-shadow: 0 22px 80px rgba(0,0,0,0.30);
        }

        .rr-hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.10) 45%, transparent 60%),
                repeating-linear-gradient(90deg, rgba(255,255,255,0.04) 0 1px, transparent 1px 18px);
            mix-blend-mode: screen;
            opacity: 0.55;
        }

        .rr-kicker {
            color: var(--cyan);
            font-size: 0.78rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            font-weight: 800;
            margin-bottom: 0.85rem;
        }

        .rr-title {
            position: relative;
            z-index: 1;
            font-size: 4.4rem;
            line-height: 0.95;
            font-weight: 900;
            max-width: 900px;
            margin: 0;
        }

        .rr-title span {
            color: var(--peach);
        }

        .rr-copy {
            position: relative;
            z-index: 1;
            color: var(--muted);
            max-width: 760px;
            font-size: 1.02rem;
            line-height: 1.65;
            margin: 1rem 0 0;
        }

        .rr-strip {
            display: flex;
            gap: 0.65rem;
            flex-wrap: wrap;
            margin-top: 1.4rem;
        }

        .rr-chip {
            border: 1px solid var(--line);
            border-radius: 999px;
            color: var(--text);
            background: rgba(8, 10, 18, 0.55);
            padding: 0.48rem 0.72rem;
            font-size: 0.82rem;
        }

        .rr-panel {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            background: rgba(255,255,255,0.055);
        }

        .rr-job-card {
            display: grid;
            grid-template-columns: minmax(0, 1.5fr) minmax(280px, 0.8fr);
            gap: 1rem;
            align-items: stretch;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1.25rem;
            margin: 1.3rem 0 0.8rem;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.095), rgba(255,255,255,0.035)),
                rgba(8, 10, 18, 0.62);
            box-shadow: 0 18px 60px rgba(0,0,0,0.22);
        }

        .rr-job-card h2 {
            margin: 0;
            font-size: 1.45rem;
        }

        .rr-job-card p {
            color: var(--muted);
            margin: 0.55rem 0 0;
        }

        .rr-job-kicker {
            color: var(--cyan) !important;
            font-size: 0.76rem;
            font-weight: 900;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin: 0 0 0.45rem !important;
        }

        .rr-job-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
        }

        .rr-job-stats div {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.9rem;
            background: rgba(255,255,255,0.055);
        }

        .rr-job-stats span,
        .rr-hire-row span {
            display: block;
            color: var(--muted);
            font-size: 0.82rem;
        }

        .rr-job-stats strong {
            display: block;
            margin-top: 0.35rem;
            color: var(--text);
            font-size: 1.5rem;
        }

        .rr-hire-panel {
            border: 1px solid rgba(111, 243, 255, 0.30);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            background: rgba(111, 243, 255, 0.06);
        }

        .rr-hire-panel h3 {
            margin: 0;
            color: var(--cyan);
        }

        .rr-hire-panel p {
            color: var(--muted);
            margin: 0.35rem 0 0.75rem;
        }

        .rr-hire-row {
            border-top: 1px solid var(--line);
            padding: 0.65rem 0;
        }

        div[data-testid="stFileUploader"],
        div[data-testid="stTextInput"],
        div[data-testid="stSlider"],
        div[data-testid="stCheckbox"] {
            position: relative;
            z-index: 1;
        }

        [data-testid="stFileUploader"] section,
        [data-testid="stTextInput"] input {
            background: rgba(8, 10, 18, 0.48);
            border: 1px solid var(--line);
            border-radius: 8px;
        }

        .rr-panel h3 {
            margin: 0 0 0.5rem;
            font-size: 0.92rem;
            color: var(--cyan);
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }

        .rr-skill-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.55rem;
        }

        .rr-skill {
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: 0.36rem 0.58rem;
            color: var(--text);
            background: rgba(8, 10, 18, 0.42);
            font-size: 0.78rem;
        }

        .rr-skill.required {
            border-color: rgba(111, 243, 255, 0.42);
        }

        .rr-skill.preferred {
            border-color: rgba(255, 177, 153, 0.42);
        }

        .rr-summary {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 1rem 0 0.35rem;
        }

        .rr-summary-item {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.8rem;
            background: rgba(255,255,255,0.055);
        }

        .rr-summary-value {
            font-size: 1.25rem;
            font-weight: 900;
            color: var(--cyan);
        }

        .rr-summary-label {
            color: var(--muted);
            font-size: 0.78rem;
            margin-top: 0.15rem;
        }

        .rr-section-head {
            display: flex;
            justify-content: space-between;
            align-items: end;
            gap: 1rem;
            margin: 1.8rem 0 0.8rem;
        }

        .rr-section-head h2 {
            margin: 0;
            font-size: 1.3rem;
        }

        .rr-section-head p {
            margin: 0;
            color: var(--muted);
        }

        .rr-card {
            position: relative;
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.035)),
                rgba(8, 10, 18, 0.72);
            box-shadow: 0 18px 60px rgba(0,0,0,0.22);
        }

        .rr-card::before {
            content: "";
            position: absolute;
            inset: 0;
            border-left: 3px solid var(--peach);
            pointer-events: none;
        }

        .rr-rank {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 2rem;
            height: 2rem;
            border-radius: 999px;
            margin-bottom: 0.65rem;
            color: #080a12;
            background: linear-gradient(135deg, var(--peach), var(--cyan));
            font-weight: 900;
            font-size: 0.78rem;
        }

        .rr-card-top {
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            gap: 1rem;
            align-items: start;
        }

        .rr-name {
            margin: 0;
            font-size: 1.08rem;
            font-weight: 850;
        }

        .rr-headline,
        .rr-meta,
        .rr-breakdown,
        .rr-explain,
        .rr-missing,
        .rr-brain,
        .rr-question {
            color: var(--muted);
            font-size: 0.86rem;
            line-height: 1.45;
        }

        .rr-mini-skill-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin: 0.2rem 0 0.65rem;
        }

        .rr-mini-skill {
            border: 1px solid rgba(111, 243, 255, 0.28);
            border-radius: 999px;
            padding: 0.28rem 0.5rem;
            color: var(--text);
            background: rgba(111, 243, 255, 0.06);
            font-size: 0.76rem;
        }

        .rr-explain {
            color: rgba(246, 247, 251, 0.82);
            margin-bottom: 0.25rem;
        }

        .rr-missing {
            color: rgba(255, 177, 153, 0.88);
            margin-bottom: 0.45rem;
        }

        .rr-brain {
            color: rgba(111, 243, 255, 0.86);
            margin-bottom: 0.25rem;
        }

        .rr-question {
            color: rgba(246, 247, 251, 0.78);
            margin-bottom: 0.25rem;
        }

        .rr-score {
            color: var(--cyan);
            font-size: 1.45rem;
            font-weight: 900;
            text-align: right;
        }

        .rr-rec {
            color: var(--peach);
            font-weight: 800;
            text-align: right;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .rr-bar {
            height: 8px;
            overflow: hidden;
            border-radius: 999px;
            background: rgba(255,255,255,0.10);
            margin: 0.85rem 0;
        }

        .rr-bar span {
            display: block;
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, var(--peach), var(--cyan));
        }

        .rr-empty {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1rem;
            background: rgba(255,255,255,0.06);
            color: var(--muted);
        }

        @media (max-width: 760px) {
            .rr-hero {
                padding: 1.35rem;
            }

            .rr-title {
                font-size: 2.65rem;
            }

            .rr-summary {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rr-card-top {
                grid-template-columns: 1fr;
            }

            .rr-score,
            .rr-rec {
                text-align: left;
            }

            .rr-job-card,
            .rr-job-stats {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
