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
    get_streak,
    initialize_database,
    mark_topic_viewed,
    save_submission,
)
from techtales.validator import ChallengeValidator
from techtales.execution import execute_user_code


st.set_page_config(
    page_title="TechTales Python Mentor",
    page_icon=":snake:",
    layout="wide",
)

TOPIC_PREREQUISITES: dict[str, tuple[str, str]] = {
    "data_types": ("variables", "Variables"),
    "f_strings": ("data_types", "Data Types"),
    "write_a_program": ("functions", "Functions"),
    "elif": ("write_a_program", "Write a Program"),
    "lists": ("elif", "Elif"),
    "dictionaries": ("lists", "Lists"),
    "string_methods": ("dictionaries", "Dictionaries"),
    "while_loops": ("string_methods", "String Methods"),
    "type_conversion": ("while_loops", "While Loops"),
}

TOPIC_ICONS: dict[str, str] = {
    "variables": "📦",
    "data_types": "🔢",
    "f_strings": "🪄",
    "if_else": "🔀",
    "loops": "🔁",
    "functions": "⚙️",
    "write_a_program": "🌍",
    "elif": "⚖️",
    "lists": "📋",
    "dictionaries": "📖",
    "string_methods": "🔤",
    "while_loops": "🔄",
    "type_conversion": "⚡",
}

_LEVEL_THRESHOLDS = [0, 40, 100, 160, 240]
_MAX_LEVEL = len(_LEVEL_THRESHOLDS)

_ERROR_TRANSLATIONS: list[tuple[str, str]] = [
    ("NameError", "Python can't find that name. Check spelling, or make sure you created the variable before using it."),
    ("IndentationError", "Indentation issue — Python uses spacing to understand structure. Lines inside if, for, or def must be indented by 4 spaces."),
    ("SyntaxError", "Python couldn't read this line. Look for a missing colon, unmatched parenthesis, or an unclosed quote."),
    ("TypeError: can only concatenate str", 'You\'re trying to join text with a number using +. Use an f-string instead: f"{variable}"'),
    ("TypeError: unsupported operand", "Type mismatch — you may be adding or comparing values of different types, like a number and a string."),
    ("ZeroDivisionError", "Python can't divide by zero. Check the value of your denominator."),
    ("IndexError", "You're accessing a position that doesn't exist. Remember: Python lists start at index 0."),
    ("ValueError", "Python received a value it can't work with here. Check what type of value is expected."),
]


def get_level(xp: int) -> tuple[int, int, int]:
    """Returns (level, xp_earned_in_current_level, xp_needed_for_next_level)."""
    for i in range(len(_LEVEL_THRESHOLDS) - 1):
        if xp < _LEVEL_THRESHOLDS[i + 1]:
            return i + 1, xp - _LEVEL_THRESHOLDS[i], _LEVEL_THRESHOLDS[i + 1] - _LEVEL_THRESHOLDS[i]
    return _MAX_LEVEL, xp - _LEVEL_THRESHOLDS[-1], 40


def get_next_topic_key(current_key: str) -> str | None:
    keys = [t.key for t in TOPICS]
    try:
        idx = keys.index(current_key)
    except ValueError:
        return None
    return keys[idx + 1] if idx + 1 < len(keys) else None


def _translate_error(error: str) -> str | None:
    for pattern, message in _ERROR_TRANSLATIONS:
        if pattern in error:
            return message
    return None


def apply_theme() -> None:
    st.markdown(
        '<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        @font-face {
            font-family: 'Material Icons';
            font-style: normal;
            font-weight: 400;
            src: url(https://fonts.gstatic.com/s/materialicons/v140/flUhRq6tzZclQEJ-Vdg-IuiaDsNc.woff2) format('woff2');
        }

        .material-icons {
            font-family: 'Material Icons' !important;
            font-weight: normal;
            font-style: normal;
            font-size: 20px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
        }

        /* Prevent broken icon text from overflowing if font fails to load */
        [data-testid="collapsedControl"] {
            overflow: hidden !important;
            max-width: 2.5rem !important;
        }

        :root {
            --tt-indigo: #4f46e5;
            --tt-indigo-dark: #4338ca;
            --tt-indigo-deep: #312e81;
            --tt-soft: #eef2ff;
            --tt-mid: #e0e7ff;
            --tt-ink: #1e1b4b;
            --tt-body: #374151;
            --tt-muted: #6b7280;
        }

        .stApp {
            font-family: 'Inter', -apple-system, sans-serif !important;
            background: #f8f8ff !important;
        }

        h1, h2, h3 {
            font-family: 'Inter', sans-serif !important;
            color: var(--tt-ink) !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
        }

        p, li, span { font-family: 'Inter', sans-serif !important; }

        /* ── SIDEBAR (dark) ─────────────────────────── */
        section[data-testid="stSidebar"] {
            background: var(--tt-ink) !important;
            border-right: none !important;
            min-width: 230px !important;
            max-width: 260px !important;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label {
            color: #a5b4fc !important;
            font-family: 'Inter', sans-serif !important;
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] hr {
            border-color: #312e81 !important;
            margin: 0.6rem 0 !important;
        }

        section[data-testid="stSidebar"] [data-testid="metric-container"] {
            background: #312e81 !important;
            border-radius: 10px !important;
            padding: 8px 12px !important;
            border: none !important;
        }

        section[data-testid="stSidebar"] [data-testid="metric-container"] * {
            color: #e0e7ff !important;
        }

        section[data-testid="stSidebar"] [data-testid="stProgressBar"] > div {
            background: rgba(255,255,255,0.1) !important;
            border-radius: 999px !important;
        }

        section[data-testid="stSidebar"] [data-testid="stProgressBar"] > div > div {
            background: #818cf8 !important;
            border-radius: 999px !important;
        }

        /* ── SIDEBAR NAV ────────────────────────────── */
        section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"],
        section[data-testid="stSidebar"] button[data-testid="baseButton-primary"] {
            text-align: left !important;
            justify-content: flex-start !important;
            border-radius: 8px !important;
            width: 100% !important;
            font-size: 0.88rem !important;
            font-family: 'Inter', sans-serif !important;
            padding: 0.45rem 0.75rem !important;
            margin: 0.06rem 0 !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease !important;
        }

        section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover,
        section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover {
            transform: scale(1.03) !important;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
        }

        /* Active lesson: solid indigo + left accent bar */
        section[data-testid="stSidebar"] button[data-testid="baseButton-primary"] {
            background: var(--tt-indigo) !important;
            color: #ffffff !important;
            border: none !important;
            border-left: 3px solid #a5b4fc !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 12px rgba(79, 70, 229, 0.3) !important;
        }

        section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
            background: rgba(165, 180, 252, 0.1) !important;
            border: 1px solid rgba(165, 180, 252, 0.2) !important;
            color: #e0e7ff !important;
        }

        section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {
            background: rgba(165, 180, 252, 0.22) !important;
            border-color: rgba(165, 180, 252, 0.4) !important;
            color: #ffffff !important;
        }

        /* Locked lessons: faded, no hover zoom */
        section[data-testid="stSidebar"] button[disabled] {
            opacity: 0.38 !important;
            cursor: not-allowed !important;
        }

        section[data-testid="stSidebar"] button[disabled]:hover {
            transform: none !important;
            box-shadow: none !important;
        }

        /* ── MAIN PROGRESS BAR ──────────────────────── */
        [data-testid="stProgressBar"] > div {
            background: var(--tt-mid) !important;
            border-radius: 999px !important;
        }

        [data-testid="stProgressBar"] > div > div {
            background: var(--tt-indigo) !important;
            border-radius: 999px !important;
        }

        /* ── ALL PRIMARY BUTTONS ────────────────────── */
        button[data-testid="baseButton-primary"] {
            background: var(--tt-indigo) !important;
            border: none !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            border-radius: 8px !important;
            letter-spacing: 0.01em !important;
        }

        button[data-testid="baseButton-primary"]:hover {
            background: var(--tt-indigo-dark) !important;
        }

        /* ── TOPIC HERO CARD ────────────────────────── */
        .techtales-topic-card {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            border: none;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 8px 32px rgba(79, 70, 229, 0.28);
            margin-bottom: 1.5rem;
        }

        .techtales-topic-card h2 {
            color: #ffffff !important;
            font-size: 1.6rem !important;
            margin-bottom: 0.25rem !important;
        }

        .techtales-topic-card .topic-summary {
            color: #c7d2fe !important;
            font-size: 0.95rem !important;
            margin: 0 0 0.9rem !important;
        }

        .techtales-lesson-meta {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-top: 0.6rem;
        }

        .techtales-lesson-badge {
            background: rgba(255,255,255,0.15);
            color: #e0e7ff;
            border-radius: 999px;
            padding: 0.22rem 0.7rem;
            font-size: 0.75rem;
            font-weight: 600;
            white-space: nowrap;
            font-family: 'Inter', sans-serif;
        }

        .techtales-hero-progress-bar {
            flex: 1;
            height: 5px;
            background: rgba(255,255,255,0.18);
            border-radius: 999px;
            overflow: hidden;
        }

        .techtales-hero-progress-fill {
            height: 100%;
            background: #a5b4fc;
            border-radius: 999px;
        }

        /* ── PANELS ─────────────────────────────────── */
        .techtales-panel {
            background: #ffffff;
            border: 1px solid #e0e7ff;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(79, 70, 229, 0.06);
        }

        /* ── CODE EDITOR TEXTAREA ───────────────────── */
        textarea {
            border-radius: 10px !important;
            border: 1.5px solid #c7d2fe !important;
            font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace !important;
            font-size: 0.875rem !important;
            background: #fafafe !important;
            line-height: 1.6 !important;
        }

        textarea:focus {
            border-color: var(--tt-indigo) !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important;
        }

        /* ── TERMINAL OUTPUT ────────────────────────── */
        .techtales-terminal {
            background: #0d1117;
            border-radius: 10px;
            border: 1px solid #30363d;
            overflow: hidden;
            margin: 0 0 0.75rem;
        }

        .techtales-terminal-header {
            background: #161b22;
            border-bottom: 1px solid #30363d;
            padding: 0.38rem 0.85rem;
            color: #8b949e;
            font-size: 0.75rem;
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }

        .terminal-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            flex-shrink: 0;
        }

        .terminal-dot-green  { background: #3fb950; }
        .terminal-dot-red    { background: #f85149; }
        .terminal-dot-yellow { background: #d29922; }
        .terminal-dot-grey   { background: #484f58; }

        .techtales-terminal-body {
            padding: 0.75rem 0.9rem;
            color: #e6edf3;
            font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
            font-size: 0.82rem;
            white-space: pre-wrap;
            word-break: break-all;
            min-height: 2.5rem;
            line-height: 1.6;
        }

        .techtales-terminal-footer {
            border-top: 1px solid #30363d;
            padding: 0.3rem 0.9rem;
            color: #3fb950;
            font-size: 0.73rem;
            font-family: 'Inter', sans-serif;
        }

        .techtales-terminal-empty {
            padding: 0.75rem 0.9rem;
            color: #484f58;
            font-style: italic;
            font-size: 0.82rem;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            min-height: 2.5rem;
        }

        .techtales-terminal-error {
            padding: 0.75rem 0.9rem;
            color: #f85149;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.82rem;
            white-space: pre-wrap;
        }

        /* ── OUTPUT SECTION LABEL ───────────────────── */
        .techtales-section-label {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            color: #6b7280;
            margin: 0 0 0.35rem;
            font-family: 'Inter', sans-serif;
        }

        /* ── RESULT PANELS ──────────────────────────── */
        .techtales-result {
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 0.5rem 0;
        }

        .techtales-result-improve {
            border: 1px solid #fca5a5;
            background: #fff7f7;
        }

        .techtales-checklist {
            display: grid;
            gap: 0.6rem;
            margin: 0.5rem 0 1rem;
        }

        .techtales-check-item {
            border-radius: 8px;
            padding: 0.65rem 0.9rem;
            font-size: 0.9rem;
        }

        .techtales-check-pass {
            border: 1px solid #c7d2fe;
            background: #eef2ff;
            color: #4338ca;
        }

        .techtales-check-fail {
            border: 1px solid #fecaca;
            background: #fff1f2;
            color: #991b1b;
        }

        .techtales-suggestion { margin: 0.35rem 0; }

        .techtales-result-section {
            margin: 0.95rem 0 0.35rem;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .techtales-passed-title { color: #4338ca; }
        .techtales-failed-title { color: #dc2626; }
        .techtales-suggestions-title { color: var(--tt-ink); }

        .techtales-suggestions {
            border-left: 3px solid var(--tt-indigo);
            background: #f5f3ff;
            padding: 0.75rem 1rem;
            border-radius: 0 8px 8px 0;
            margin-top: 0.5rem;
        }

        /* ── CELEBRATION CARD ────────────────────────── */
        .techtales-celebration {
            background: linear-gradient(135deg, #312e81 0%, #4f46e5 50%, #7c3aed 100%);
            border-radius: 14px;
            padding: 1.5rem 1.6rem;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 8px 32px rgba(79, 70, 229, 0.35);
        }

        .techtales-celebration h3 {
            color: #ffffff !important;
            font-size: 1.25rem !important;
            margin: 0 0 0.3rem !important;
        }

        .techtales-celebration .xp-badge {
            display: inline-block;
            background: rgba(255,255,255,0.18);
            color: #e0e7ff;
            border-radius: 999px;
            padding: 0.25rem 0.9rem;
            font-size: 0.88rem;
            font-weight: 700;
            margin: 0.4rem 0 0.2rem;
            letter-spacing: 0.04em;
            font-family: 'Inter', sans-serif;
        }

        .techtales-celebration p {
            color: #c7d2fe !important;
            font-size: 0.88rem !important;
            margin: 0.2rem 0 0 !important;
        }

        /* ── LOCKED ─────────────────────────────────── */
        .techtales-locked {
            border: 2px dashed #a5b4fc;
            border-radius: 14px;
            background: #f5f3ff;
            padding: 1.75rem;
            margin-top: 1rem;
            text-align: center;
        }

        /* ── CODE BLOCKS ────────────────────────────── */
        .stCode, [data-testid="stCode"] {
            border-radius: 10px !important;
            overflow: hidden !important;
        }

        /* ── COLUMN GAP TIGHTENING ──────────────────── */
        [data-testid="column"] > div {
            padding-left: 0.3rem !important;
            padding-right: 0.3rem !important;
        }

        /* ── PROGRESS STEPPER ───────────────────────── */
        .tt-stepper {
            display: flex;
            align-items: flex-start;
            padding: 0 0 1.1rem;
            overflow-x: auto;
            scrollbar-width: none;
        }
        .tt-stepper::-webkit-scrollbar { display: none; }

        .tt-step-wrap {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.2rem;
            flex: 0 0 auto;
            min-width: 62px;
        }

        .tt-dot {
            width: 26px;
            height: 26px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.72rem;
            font-weight: 700;
            border: 2px solid #d1d5db;
            background: transparent;
            color: #9ca3af;
            flex-shrink: 0;
        }

        .tt-step-wrap.completed .tt-dot {
            background: #4f46e5;
            border-color: #4f46e5;
            color: #ffffff;
        }

        .tt-step-wrap.active .tt-dot {
            background: #eef2ff;
            border-color: #4f46e5;
            color: #4f46e5;
            border-width: 2.5px;
            box-shadow: 0 0 0 3px rgba(79,70,229,0.15);
        }

        .tt-step-wrap.locked .tt-dot {
            background: #f9fafb;
            border-color: #e5e7eb;
            color: #d1d5db;
        }

        .tt-step-icon {
            font-size: 0.9rem;
            line-height: 1;
        }

        .tt-step-label {
            font-size: 0.58rem;
            font-weight: 600;
            color: #9ca3af;
            text-align: center;
            font-family: 'Inter', sans-serif;
            white-space: nowrap;
            letter-spacing: 0.02em;
        }

        .tt-step-wrap.completed .tt-step-label { color: #4338ca; }
        .tt-step-wrap.active .tt-step-label { color: #4f46e5; font-weight: 700; }
        .tt-step-wrap.locked .tt-step-label { color: #d1d5db; }

        .tt-line {
            flex: 1;
            min-width: 14px;
            height: 2px;
            background: #e5e7eb;
            margin-top: 12px;
            align-self: flex-start;
            flex-shrink: 1;
        }

        .tt-line.completed { background: #4f46e5; }

        /* ── MENTOR CARD ────────────────────────────── */
        .tt-mentor {
            display: flex;
            align-items: flex-start;
            gap: 0.55rem;
            background: #f5f3ff;
            border: 1px solid #e0e7ff;
            border-left: 3px solid #6366f1;
            border-radius: 8px;
            padding: 0.65rem 0.85rem;
            margin-bottom: 0.75rem;
            font-family: 'Inter', sans-serif;
        }

        .tt-mentor-hint {
            background: #fffbeb;
            border-color: #fde68a;
            border-left-color: #f59e0b;
        }

        .tt-mentor-icon {
            font-size: 1rem;
            flex-shrink: 0;
            margin-top: 0.05rem;
        }

        .tt-mentor-text {
            font-size: 0.855rem;
            color: #374151;
            line-height: 1.55;
        }

        /* ── EXPECTED OUTPUT ────────────────────────── */
        .tt-expected {
            border: 1px solid #e0e7ff;
            border-radius: 8px;
            overflow: hidden;
            margin-top: 0.5rem;
        }

        .tt-expected-label {
            background: #eef2ff;
            color: #6366f1;
            font-size: 0.67rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            padding: 0.22rem 0.75rem;
            font-family: 'Inter', sans-serif;
        }

        .tt-expected-pre {
            background: #f8f8ff;
            color: #374151;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.78rem;
            padding: 0.4rem 0.75rem;
            margin: 0;
            white-space: pre-wrap;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def is_topic_unlocked(topic_key: str, passed_topic_keys: set[str]) -> bool:
    prereq = TOPIC_PREREQUISITES.get(topic_key)
    if prereq:
        return prereq[0] in passed_topic_keys
    return True


def html_panel(css_class: str, content: str) -> str:
    return f'<div class="{css_class}">{content}</div>'


def render_sidebar(db_path: Path, passed_topic_keys: set[str]) -> None:
    progress = get_progress(db_path)
    completed_count = len(passed_topic_keys)
    current_xp = get_current_xp(db_path)
    level, level_xp, level_to_next = get_level(current_xp)
    current_streak, longest_streak = get_streak(db_path)

    with st.sidebar:
        st.markdown(
            '<div style="padding: 1rem 0 0.5rem;">'
            '<span style="font-size: 1.5rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; font-family: Inter, sans-serif;">TechTales</span>'
            '<span style="display: block; font-size: 0.78rem; color: #6366f1; margin-top: 0.15rem; font-family: Inter, sans-serif; letter-spacing: 0.04em; text-transform: uppercase; font-weight: 600;">Python Mentor</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.divider()

        xp_col, done_col = st.columns(2)
        xp_col.metric("XP", current_xp)
        done_col.metric("Done", f"{completed_count}/{len(TOPICS)}")

        if current_streak >= 1:
            streak_text = f"🔥 {current_streak} day{'s' if current_streak != 1 else ''} streak"
            if longest_streak > current_streak:
                streak_text += f" · best {longest_streak}"
            st.markdown(
                f'<div style="text-align:center;font-size:0.72rem;font-weight:600;color:#fb923c;font-family:Inter,sans-serif;margin-top:0.15rem">{streak_text}</div>',
                unsafe_allow_html=True,
            )

        level_pct = min(level_xp / level_to_next, 1.0) if level_to_next else 1.0
        st.progress(level_pct)
        if level >= _MAX_LEVEL:
            level_label = f"Level {level}  ·  Max Level!"
        else:
            level_label = f"Level {level}  ·  {level_xp} / {level_to_next} XP to next"
        st.markdown(
            f'<div style="font-size: 0.72rem; color: #818cf8; text-align: center; margin-top: -0.3rem; font-family: Inter, sans-serif; font-weight: 600; letter-spacing: 0.03em;">{level_label}</div>',
            unsafe_allow_html=True,
        )

        st.divider()
        st.caption("LESSONS")

        for topic in TOPICS:
            unlocked = is_topic_unlocked(topic.key, passed_topic_keys)
            completed = topic.key in passed_topic_keys
            item = progress.get(topic.key)
            viewed = bool(item and item.viewed)
            topic_icon = TOPIC_ICONS.get(topic.key, "")

            if not unlocked:
                state_icon = "🔒"
                _, prereq_title = TOPIC_PREREQUISITES.get(topic.key, ("", "previous topic"))
                lock_help: str | None = f"Complete {prereq_title} first to unlock this lesson."
            elif completed:
                state_icon = "✓"
                lock_help = None
            elif viewed:
                state_icon = "◉"
                lock_help = None
            else:
                state_icon = "○"
                lock_help = None

            is_active = st.session_state.get("selected_topic") == topic.key
            if st.button(
                f"{state_icon}  {topic_icon}  {topic.title}",
                key=f"nav_{topic.key}",
                use_container_width=True,
                disabled=not unlocked,
                type="primary" if is_active else "secondary",
                help=lock_help,
            ):
                st.session_state.selected_topic = topic.key
                st.rerun()


def _translate_terminal_error(error: str) -> str | None:
    return _translate_error(error)


def _render_terminal(execution_result: object | None) -> None:
    if execution_result is None:
        body = html_panel("techtales-terminal-empty", "Run your code to see output here.")
        dot_class = "terminal-dot-grey"
        header_label = "Output"
        footer = ""
    elif execution_result.error:
        translation = _translate_error(execution_result.error)
        if translation:
            raw_html = (
                '<details style="margin-top:0.5rem">'
                '<summary style="cursor:pointer;color:#8b949e;font-size:0.73rem;font-family:Inter,sans-serif;font-style:normal">Show Python details</summary>'
                f'<pre style="margin-top:0.35rem;color:#f85149;opacity:0.7;font-size:0.78rem;'
                f'font-family:\'JetBrains Mono\',monospace;white-space:pre-wrap;margin-bottom:0">'
                f'{escape(execution_result.error)}</pre>'
                '</details>'
            )
            body = (
                f'<div class="techtales-terminal-error">'
                f'<strong>{escape(translation)}</strong>'
                f'{raw_html}'
                f'</div>'
            )
        else:
            body = html_panel("techtales-terminal-error", escape(execution_result.error))
        dot_class = "terminal-dot-red"
        header_label = "Error"
        footer = '<div class="techtales-terminal-footer">Runtime error — check your code above.</div>'
    elif execution_result.stdout:
        body = html_panel("techtales-terminal-body", escape(execution_result.stdout))
        dot_class = "terminal-dot-green"
        header_label = "Output"
        footer = '<div class="techtales-terminal-footer">Execution completed successfully.</div>'
    else:
        body = html_panel("techtales-terminal-empty", "No output — add a print() to see results.")
        dot_class = "terminal-dot-yellow"
        header_label = "No output"
        footer = ""

    st.markdown(
        f'<div class="techtales-terminal">'
        f'<div class="techtales-terminal-header">'
        f'<span class="terminal-dot {dot_class}"></span>{header_label}'
        f'</div>'
        f'{body}'
        f'{footer}'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_mentor_card(topic: object, latest_submission: object | None) -> None:
    mentor = topic.mentor
    if not mentor.opening:
        return

    is_passed = latest_submission is not None and latest_submission.challenge_passed
    if is_passed:
        return

    if latest_submission is None:
        message = mentor.opening
        card_class = "tt-mentor"
        icon = "💬"
    else:
        # Runtime/syntax errors take priority — they explain why everything else failed
        runtime_hint = _translate_error(latest_submission.runtime_error or "")
        if runtime_hint:
            message = runtime_hint
            card_class = "tt-mentor tt-mentor-hint"
            icon = "💡"
        else:
            details = json.loads(latest_submission.validation_details or "[]")
            failed = [d for d in details if not d.get("passed")]
            hint = None
            for item in failed:
                h = mentor.hint_for(item.get("label", ""))
                if h:
                    hint = h
                    break
            if hint:
                message = hint
                card_class = "tt-mentor tt-mentor-hint"
                icon = "💡"
            else:
                message = mentor.opening
                card_class = "tt-mentor"
                icon = "💬"

    st.markdown(
        f'<div class="{card_class}">'
        f'<span class="tt-mentor-icon">{icon}</span>'
        f'<span class="tt-mentor-text">{escape(message)}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_progress_stepper(topic_key: str, passed_topic_keys: set[str]) -> None:
    parts: list[str] = ['<div class="tt-stepper">']
    for i, topic in enumerate(TOPICS):
        is_completed = topic.key in passed_topic_keys
        is_active = topic.key == topic_key
        is_locked = not is_topic_unlocked(topic.key, passed_topic_keys)

        if is_completed:
            state = "completed"
            dot_content = "✓"
        elif is_active:
            state = "active"
            dot_content = ""
        elif is_locked:
            state = "locked"
            dot_content = ""
        else:
            state = ""
            dot_content = ""

        icon = TOPIC_ICONS.get(topic.key, "")
        parts.append(f'<div class="tt-step-wrap {state}">')
        parts.append(f'<div class="tt-dot"><span>{dot_content}</span></div>')
        parts.append(f'<div class="tt-step-icon">{icon}</div>')
        parts.append(f'<div class="tt-step-label">{escape(topic.title)}</div>')
        parts.append('</div>')

        if i < len(TOPICS) - 1:
            line_class = "completed" if is_completed else ""
            parts.append(f'<div class="tt-line {line_class}"></div>')

    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_results_panel(topic_key: str, submission: object | None) -> None:
    if not submission:
        return

    passed = submission.challenge_passed

    if passed:
        xp_text = f"+{submission.xp_awarded} XP" if submission.xp_awarded else "Already earned"
        st.markdown(
            html_panel(
                "techtales-celebration",
                f'<h3>🎉 Challenge Passed!</h3>'
                f'<div class="xp-badge">{xp_text}</div>'
                f'<p>{escape(submission.evaluator_message)}</p>',
            ),
            unsafe_allow_html=True,
        )

        if st.session_state.pop(f"celebrate_{topic_key}", False):
            st.balloons()

        next_key = get_next_topic_key(topic_key)
        if next_key:
            next_topic = get_topic(next_key)
            if st.button(
                f"Next Lesson: {next_topic.title} →",
                key=f"next_{topic_key}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.selected_topic = next_key
                st.rerun()
    else:
        st.markdown(
            html_panel(
                "techtales-result techtales-result-improve",
                f"<h3>Almost there!</h3><p>{escape(submission.evaluator_message)}</p>",
            ),
            unsafe_allow_html=True,
        )

    details = json.loads(submission.validation_details or "[]")
    if not details:
        return

    passed_items = [item for item in details if item.get("passed")]
    failed_items = [item for item in details if not item.get("passed")]

    sections_html = []
    if passed_items:
        sections_html.append('<div class="techtales-result-section techtales-passed-title">PASSED</div>')
        sections_html.append('<div class="techtales-checklist">')
        for item in passed_items:
            label = escape(str(item.get("label") or "Requirement"))
            sections_html.append(
                html_panel("techtales-check-item techtales-check-pass", f"<strong>&#10003;</strong> {label}")
            )
        sections_html.append("</div>")

    if failed_items:
        sections_html.append('<div class="techtales-result-section techtales-failed-title">FAILED</div>')
        sections_html.append('<div class="techtales-checklist">')
        for item in failed_items:
            label = escape(str(item.get("label") or "Requirement"))
            sections_html.append(
                html_panel("techtales-check-item techtales-check-fail", f"<strong>&#10007;</strong> {label}")
            )
        sections_html.append("</div>")

        sections_html.append('<div class="techtales-result-section techtales-suggestions-title">Suggestions</div>')
        sections_html.append('<div class="techtales-suggestions">')
        for item in failed_items:
            suggestion = escape(str(item.get("suggestion") or "Update this part of your code and try again."))
            sections_html.append(f'<p class="techtales-suggestion">&bull; {suggestion}</p>')
        sections_html.append("</div>")

    st.markdown("".join(sections_html), unsafe_allow_html=True)


def render_locked_topic(topic_key: str) -> None:
    topic = get_topic(topic_key)
    _, prereq_title = TOPIC_PREREQUISITES.get(topic_key, ("", "the previous topic"))
    st.markdown(
        html_panel(
            "techtales-locked",
            f"<h2>🔒 {escape(topic.title)} is locked</h2>"
            f"<p>Complete the <strong>{escape(prereq_title)}</strong> challenge first to unlock this lesson.</p>",
        ),
        unsafe_allow_html=True,
    )


def render_lesson(topic_key: str, db_path: Path, passed_topic_keys: set[str]) -> None:
    topic = get_topic(topic_key)
    mark_topic_viewed(db_path, topic.key)
    latest_submission = get_latest_submission(db_path, topic.key)

    topic_index = next((i for i, t in enumerate(TOPICS) if t.key == topic.key), 0)
    lesson_num = topic_index + 1
    total_lessons = len(TOPICS)
    progress_pct = int((lesson_num / total_lessons) * 100)
    topic_icon = TOPIC_ICONS.get(topic.key, "")

    is_completed = latest_submission is not None and latest_submission.challenge_passed

    _render_progress_stepper(topic_key, passed_topic_keys)

    st.markdown(
        html_panel(
            "techtales-topic-card",
            f'<h2>{topic_icon}  {escape(topic.title)}</h2>'
            f'<p class="topic-summary">{escape(topic.summary)}</p>'
            f'<div class="techtales-lesson-meta">'
            f'<span class="techtales-lesson-badge">Lesson {lesson_num} of {total_lessons}</span>'
            f'<div class="techtales-hero-progress-bar">'
            f'<div class="techtales-hero-progress-fill" style="width: {progress_pct}%;"></div>'
            f'</div>'
            f'</div>',
        ),
        unsafe_allow_html=True,
    )

    lesson_col, challenge_col = st.columns([1, 1.5], gap="large")

    with lesson_col:
        with st.expander("📖 Lesson & Example", expanded=True):
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

        _render_mentor_card(topic, latest_submission)

        editor_col, output_col = st.columns([3, 2], gap="small")

        with editor_col:
            default_code = st.session_state.get(f"code_{topic.key}", topic.starter_code)
            code = st.text_area(
                "Your Python code",
                value=default_code,
                height=340,
                key=f"code_{topic.key}",
            )
            execution_result = execute_user_code(code) if code.strip() else None

            if st.button("Submit challenge", type="primary", use_container_width=True):
                if not code.strip():
                    st.warning("Add some Python code before submitting.")
                    return

                validation = ChallengeValidator().validate(
                    topic=topic, submitted_code=code, execution_result=execution_result
                )
                validation_details = [
                    {"label": r.label, "passed": r.passed, "suggestion": r.suggestion}
                    for r in validation.requirements
                ]
                save_submission(
                    db_path=db_path,
                    topic_key=topic.key,
                    code=code,
                    evaluator_status=validation.status,
                    evaluator_message=validation.feedback,
                    challenge_passed=validation.passed,
                    validation_details=validation_details,
                    stdout=execution_result.stdout if execution_result else "",
                    runtime_error=execution_result.error if execution_result else None,
                )
                if validation.passed:
                    st.session_state[f"celebrate_{topic.key}"] = True
                st.rerun()

        with output_col:
            st.markdown('<p class="techtales-section-label">Program Output</p>', unsafe_allow_html=True)
            _render_terminal(execution_result)
            if topic.expected_output and not is_completed:
                st.markdown(
                    '<div class="tt-expected">'
                    '<div class="tt-expected-label">Example output</div>'
                    f'<pre class="tt-expected-pre">{escape(topic.expected_output)}</pre>'
                    '</div>',
                    unsafe_allow_html=True,
                )

        if latest_submission:
            render_results_panel(topic.key, latest_submission)


def main() -> None:
    db_path = DEFAULT_DB_PATH
    initialize_database(db_path)
    apply_theme()

    passed_topic_keys = get_passed_topic_keys(db_path)

    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = TOPICS[0].key

    render_sidebar(db_path, passed_topic_keys)

    selected_topic_key = st.session_state.selected_topic
    if not is_topic_unlocked(selected_topic_key, passed_topic_keys):
        render_locked_topic(selected_topic_key)
        return

    render_lesson(selected_topic_key, db_path, passed_topic_keys)


if __name__ == "__main__":
    main()
