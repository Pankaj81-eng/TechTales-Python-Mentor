from __future__ import annotations

import json
from html import escape
from pathlib import Path

import streamlit as st

from techtales.content import TOPICS, get_topic
from techtales.db import (
    DEFAULT_DB_PATH,
    get_current_xp,
    get_latest_submission,
    get_passed_topic_keys,
    get_progress,
    initialize_database,
    mark_topic_viewed,
    save_submission,
)
from techtales.validator import ChallengeValidator


st.set_page_config(
    page_title="TechTales Python Mentor",
    page_icon=":snake:",
    layout="wide",
)


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --techtales-green: #15803d;
            --techtales-green-dark: #166534;
            --techtales-green-soft: #dcfce7;
            --techtales-mint: #f0fdf4;
            --techtales-ink: #17281f;
        }

        .stApp {
            background: linear-gradient(180deg, #f7fff9 0%, #ffffff 42%);
            color: var(--techtales-ink);
        }

        h1, h2, h3 {
            color: var(--techtales-green-dark);
            letter-spacing: 0;
        }

        section[data-testid="stSidebar"] {
            background: #f0fdf4;
            border-right: 1px solid #bbf7d0;
        }

        .techtales-panel {
            border: 1px solid #bbf7d0;
            border-radius: 8px;
            background: rgba(240, 253, 244, 0.72);
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
        }

        .techtales-topic-card {
            border-left: 5px solid var(--techtales-green);
            background: #ffffff;
            border-radius: 8px;
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 22px rgba(22, 101, 52, 0.08);
            margin-bottom: 1rem;
        }

        .techtales-status {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            border-radius: 999px;
            background: var(--techtales-green-soft);
            color: var(--techtales-green-dark);
            font-size: 0.85rem;
            font-weight: 700;
            padding: 0.24rem 0.65rem;
            margin-bottom: 0.6rem;
        }

        .techtales-result {
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }

        .techtales-result-pass {
            border: 1px solid #86efac;
            background: #f0fdf4;
        }

        .techtales-result-improve {
            border: 1px solid #fca5a5;
            background: #fff7f7;
        }

        .techtales-checklist {
            display: grid;
            gap: 0.7rem;
            margin: 0.5rem 0 1rem;
        }

        .techtales-check-item {
            border-radius: 8px;
            padding: 0.72rem 0.85rem;
        }

        .techtales-check-pass {
            border: 1px solid #bbf7d0;
            background: #f0fdf4;
            color: #166534;
        }

        .techtales-check-fail {
            border: 1px solid #fecaca;
            background: #fff1f2;
            color: #991b1b;
        }

        .techtales-suggestion {
            margin: 0.35rem 0;
        }

        .techtales-result-section {
            margin: 0.95rem 0 0.35rem;
            font-size: 0.86rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .techtales-passed-title {
            color: #166534;
        }

        .techtales-failed-title {
            color: #991b1b;
        }

        .techtales-suggestions-title {
            color: #17281f;
        }

        .techtales-suggestions {
            border-left: 4px solid #15803d;
            background: #f7fff9;
            padding: 0.7rem 0.9rem;
            border-radius: 8px;
            margin-top: 0.5rem;
        }

        .techtales-locked {
            border: 1px dashed #86efac;
            border-radius: 8px;
            background: #f7fff9;
            padding: 1.25rem;
            margin-top: 1rem;
        }

        div.stButton > button:first-child {
            border-radius: 8px;
            border: 1px solid var(--techtales-green);
            background: var(--techtales-green);
            color: #ffffff;
            font-weight: 700;
        }

        div.stButton > button:first-child:hover {
            border-color: var(--techtales-green-dark);
            background: var(--techtales-green-dark);
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def progress_label(progress: dict[str, object] | None) -> str:
    if not progress:
        return "Not started"
    if progress.get("completed"):
        return "Completed"
    if progress.get("viewed"):
        return "Lesson viewed"
    return "Not started"


def is_topic_unlocked(topic_key: str, passed_topic_keys: set[str]) -> bool:
    if topic_key != "data_types":
        return True

    return "variables" in passed_topic_keys


def topic_label(topic_key: str, title: str, passed_topic_keys: set[str]) -> str:
    if is_topic_unlocked(topic_key, passed_topic_keys):
        return title
    return f"{title} (Locked)"


def html_panel(css_class: str, content: str) -> str:
    return f'<div class="{css_class}">{content}</div>'


def render_sidebar(db_path: Path) -> None:
    progress = get_progress(db_path)
    passed_topic_keys = get_passed_topic_keys(db_path)
    completed_count = len(passed_topic_keys)
    current_xp = get_current_xp(db_path)

    st.sidebar.title("TechTales")
    st.sidebar.caption("Python Mentor")
    st.sidebar.metric("Current XP", current_xp)
    st.sidebar.progress(completed_count / len(TOPICS), text=f"{completed_count}/{len(TOPICS)} topics complete")

    st.sidebar.subheader("Progress")
    for topic in TOPICS:
        item = progress.get(topic.key)
        if topic.key in passed_topic_keys:
            status = "Completed"
        elif item and item.viewed:
            status = "Lesson viewed"
        else:
            status = "Not started"
        if not is_topic_unlocked(topic.key, passed_topic_keys):
            status = "Locked"
        st.sidebar.write(f"**{topic.title}**")
        st.sidebar.caption(status)


def render_results_panel(topic_key: str, submission: object | None) -> None:
    if not submission:
        return

    passed = submission.challenge_passed
    heading = "Challenge Passed" if passed else "Challenge Needs Improvement"
    result_class = "techtales-result-pass" if passed else "techtales-result-improve"
    st.markdown(
        html_panel(
            f"techtales-result {result_class}",
            f"<h3>{escape(heading)}</h3><p>{escape(submission.evaluator_message)}</p>",
        ),
        unsafe_allow_html=True,
    )

    details = json.loads(submission.validation_details or "[]")
    if details:
        passed_items = [item for item in details if item.get("passed")]
        failed_items = [item for item in details if not item.get("passed")]

        sections_html = []
        if passed_items:
            sections_html.append('<div class="techtales-result-section techtales-passed-title">PASSED</div>')
            sections_html.append('<div class="techtales-checklist">')
            for item in passed_items:
                label = escape(str(item.get("label") or "Requirement"))
                sections_html.append(
                    html_panel(
                        "techtales-check-item techtales-check-pass",
                        f"<strong>&#10003;</strong> {label}",
                    )
                )
            sections_html.append("</div>")

        if failed_items:
            sections_html.append('<div class="techtales-result-section techtales-failed-title">FAILED</div>')
            sections_html.append('<div class="techtales-checklist">')
            for item in failed_items:
                label = escape(str(item.get("label") or "Requirement"))
                sections_html.append(
                    html_panel(
                        "techtales-check-item techtales-check-fail",
                        f"<strong>&#10007;</strong> {label}",
                    )
                )
            sections_html.append("</div>")

            sections_html.append('<div class="techtales-result-section techtales-suggestions-title">Suggestions</div>')
            sections_html.append('<div class="techtales-suggestions">')
            for item in failed_items:
                suggestion = escape(str(item.get("suggestion") or "Update this part of your code and try again."))
                sections_html.append(f'<p class="techtales-suggestion">&bull; {suggestion}</p>')
            sections_html.append("</div>")

        st.markdown("".join(sections_html), unsafe_allow_html=True)

    if submission.xp_awarded:
        st.success(f"+{submission.xp_awarded} XP awarded")

    if topic_key == "variables" and passed:
        st.info("Next Topic Unlocked: Data Types")


def render_locked_topic() -> None:
    st.markdown("# TechTales Python Mentor")
    st.caption("A green little corner for learning Python one story at a time.")
    st.markdown(
        html_panel(
            "techtales-locked",
            "<h2>Data Types is locked</h2><p>Pass the Variables challenge first to unlock this lesson.</p>",
        ),
        unsafe_allow_html=True,
    )


def render_lesson(topic_key: str, db_path: Path) -> None:
    topic = get_topic(topic_key)
    mark_topic_viewed(db_path, topic.key)
    latest_submission = get_latest_submission(db_path, topic.key)
    current_xp = get_current_xp(db_path)

    st.markdown(f"# TechTales Python Mentor")
    st.caption("A green little corner for learning Python one story at a time.")
    st.metric("Current XP", current_xp)

    status = "Completed" if latest_submission and latest_submission.challenge_passed else "Lesson in progress"
    st.markdown(f'<span class="techtales-status">{status}</span>', unsafe_allow_html=True)

    st.markdown(
        html_panel(
            "techtales-topic-card",
            f"<h2>{escape(topic.title)}</h2><p>{escape(topic.summary)}</p>",
        ),
        unsafe_allow_html=True,
    )

    lesson_col, challenge_col = st.columns([1.1, 0.9], gap="large")

    with lesson_col:
        st.subheader("Lesson")
        st.markdown(topic.lesson)
        st.subheader("Example")
        st.code(topic.example_code, language="python")

    with challenge_col:
        st.subheader("Challenge")
        st.markdown(
            html_panel("techtales-panel", escape(topic.challenge).replace("\n", "<br>")),
            unsafe_allow_html=True,
        )

        default_code = st.session_state.get(f"code_{topic.key}", topic.starter_code)
        code = st.text_area(
            "Your Python code",
            value=default_code,
            height=260,
            key=f"code_{topic.key}",
        )

        if st.button("Submit challenge", type="primary", use_container_width=True):
            if not code.strip():
                st.warning("Add some Python code before submitting your challenge.")
                return

            validation = ChallengeValidator().validate(topic=topic, submitted_code=code)
            validation_details = [
                {
                    "label": requirement.label,
                    "passed": requirement.passed,
                    "suggestion": requirement.suggestion,
                }
                for requirement in validation.requirements
            ]
            save_submission(
                db_path=db_path,
                topic_key=topic.key,
                code=code,
                evaluator_status=validation.status,
                evaluator_message=validation.feedback,
                challenge_passed=validation.passed,
                validation_details=validation_details,
            )
            st.rerun()

        if latest_submission:
            render_results_panel(topic.key, latest_submission)


def main() -> None:
    db_path = DEFAULT_DB_PATH
    initialize_database(db_path)
    apply_theme()
    render_sidebar(db_path)
    passed_topic_keys = get_passed_topic_keys(db_path)

    topic_titles = [topic_label(topic.key, topic.title, passed_topic_keys) for topic in TOPICS]
    title_to_key = {
        topic_label(topic.key, topic.title, passed_topic_keys): topic.key
        for topic in TOPICS
    }

    selected_title = st.selectbox(
        "Choose a Python topic",
        options=topic_titles,
        index=0,
    )
    selected_topic_key = title_to_key[selected_title]
    if not is_topic_unlocked(selected_topic_key, passed_topic_keys):
        render_locked_topic()
        return

    render_lesson(selected_topic_key, db_path)


if __name__ == "__main__":
    main()
