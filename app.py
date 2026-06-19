from __future__ import annotations

import json
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

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

# Linear unlock chain — each topic unlocks the next, in the order of the TOPICS tuple.
# write_a_program is the first lesson and has no prerequisite.
TOPIC_PREREQUISITES: dict[str, tuple[str, str]] = {
    "variables": ("write_a_program", "Write a Program"),
    "data_types": ("variables", "Variables"),
    "type_conversion": ("data_types", "Data Types"),
    "arithmetic_operators": ("type_conversion", "Type Conversion"),
    "f_strings": ("arithmetic_operators", "Arithmetic Operators"),
    "exercise_profile_card": ("f_strings", "F-Strings"),
    "string_indexing": ("exercise_profile_card", "Exercise: Profile Card"),
    "string_methods": ("string_indexing", "String Indexing & Slicing"),
    "string_split_join": ("string_methods", "String Methods"),
    "comparison_operators": ("string_split_join", "Split & Join"),
    "boolean_logic": ("comparison_operators", "Comparison Operators"),
    "if_else": ("boolean_logic", "Boolean Logic"),
    "elif": ("if_else", "If/Else"),
    "membership_operators": ("elif", "Elif"),
    "conditional_expression": ("membership_operators", "Membership: in / not in"),
    "exercise_grade_checker": ("conditional_expression", "Conditional Expression"),
    "loops": ("exercise_grade_checker", "Exercise: Grade Checker"),
    "for_each": ("loops", "For Loops & range()"),
    "enumerate_loop": ("for_each", "Looping Over Collections"),
    "while_loops": ("enumerate_loop", "Looping with enumerate()"),
    "break_continue": ("while_loops", "While Loops"),
    "nested_loops": ("break_continue", "Break & Continue"),
    "exercise_pattern_printer": ("nested_loops", "Nested Loops"),
    "lists": ("exercise_pattern_printer", "Exercise: Pattern Printer"),
    "list_methods": ("lists", "Lists"),
    "list_slicing": ("list_methods", "List Methods"),
    "list_comprehensions": ("list_slicing", "List Slicing"),
    "tuples": ("list_comprehensions", "List Comprehensions"),
    "tuple_unpacking": ("tuples", "Tuples"),
    "sets": ("tuple_unpacking", "Tuple Unpacking"),
    "dictionaries": ("sets", "Sets"),
    "dict_methods": ("dictionaries", "Dictionaries"),
    "dict_iteration": ("dict_methods", "Dictionary Methods"),
    "nested_data": ("dict_iteration", "Looping Over Dictionaries"),
    "exercise_inventory": ("nested_data", "Nested Data"),
    "functions": ("exercise_inventory", "Exercise: Inventory Tracker"),
    "function_parameters": ("functions", "Functions"),
    "default_parameters": ("function_parameters", "Function Parameters"),
    "multiple_return": ("default_parameters", "Default Parameters"),
    "none_type": ("multiple_return", "Returning Multiple Values"),
    "recursion": ("none_type", "None"),
    "exercise_calculator": ("recursion", "Recursion"),
    # Unit 7 — Object-Oriented Programming
    "classes": ("exercise_calculator", "Exercise: Mini Calculator"),
    "class_definition": ("classes", "What is a Class?"),
    "instance_creation": ("class_definition", "Define a Class with __init__"),
    "class_methods": ("instance_creation", "Create Objects from a Class"),
    "class_attributes": ("class_methods", "Add Methods to a Class"),
    "inheritance": ("class_attributes", "Work with Object Attributes"),
    "exercise_class_design": ("inheritance", "Inheritance — Extend a Class"),
}

TOPIC_ICONS: dict[str, str] = {
    # Unit 1 — Foundations
    "write_a_program": "🌍",
    "variables": "📦",
    "data_types": "🔢",
    "type_conversion": "⚡",
    "arithmetic_operators": "➕",
    "f_strings": "🪄",
    "exercise_profile_card": "🪪",
    # Unit 2 — Text
    "string_indexing": "🔠",
    "string_methods": "🔤",
    "string_split_join": "✂️",
    # Unit 3 — Decisions
    "comparison_operators": "🟰",
    "boolean_logic": "🚦",
    "if_else": "🔀",
    "elif": "⚖️",
    "membership_operators": "🔎",
    "conditional_expression": "❓",
    "exercise_grade_checker": "🎯",
    # Unit 4 — Loops
    "loops": "🔁",
    "for_each": "🚶",
    "enumerate_loop": "#️⃣",
    "while_loops": "🔄",
    "break_continue": "🛑",
    "nested_loops": "🔲",
    "exercise_pattern_printer": "🎨",
    # Unit 5 — Collections
    "lists": "📋",
    "list_methods": "🧰",
    "list_slicing": "🔪",
    "list_comprehensions": "🧪",
    "tuples": "🧊",
    "tuple_unpacking": "🎁",
    "sets": "🟣",
    "dictionaries": "📖",
    "dict_methods": "🗂️",
    "dict_iteration": "📑",
    "nested_data": "🪆",
    "exercise_inventory": "🎒",
    # Unit 6 — Functions
    "functions": "⚙️",
    "function_parameters": "🎚️",
    "default_parameters": "🔧",
    "multiple_return": "↩️",
    "none_type": "🕳️",
    "recursion": "🌀",
    "exercise_calculator": "🏆",
    # Unit 7 — Object-Oriented Programming
    "classes": "🏗️",
    "class_definition": "📝",
    "instance_creation": "🎭",
    "class_methods": "🤖",
    "class_attributes": "🏷️",
    "inheritance": "🌳",
    "exercise_class_design": "💎",
}

# Unit structure: groups topics by learning unit
UNIT_STRUCTURE: dict[str, tuple[str, ...]] = {
    "🌍 Foundations": (
        "write_a_program", "variables", "data_types", "type_conversion",
        "arithmetic_operators", "f_strings", "exercise_profile_card",
    ),
    "🔠 Text": (
        "string_indexing", "string_methods", "string_split_join",
    ),
    "🟰 Decisions": (
        "comparison_operators", "boolean_logic", "if_else", "elif",
        "membership_operators", "conditional_expression", "exercise_grade_checker",
    ),
    "🔁 Loops": (
        "loops", "for_each", "enumerate_loop", "while_loops",
        "break_continue", "nested_loops", "exercise_pattern_printer",
    ),
    "📋 Collections": (
        "lists", "list_methods", "list_slicing", "list_comprehensions",
        "tuples", "tuple_unpacking", "sets", "dictionaries", "dict_methods",
        "dict_iteration", "nested_data", "exercise_inventory",
    ),
    "⚙️ Functions": (
        "functions", "function_parameters", "default_parameters",
        "multiple_return", "none_type", "recursion", "exercise_calculator",
    ),
    "🏗️ OOP Concepts": (
        "classes", "class_definition", "instance_creation", "class_methods",
        "class_attributes", "inheritance", "exercise_class_design",
    ),
}

_UNIT_DIFFICULTY: dict[str, str] = {
    "🌍 Foundations": "Beginner",
    "🔠 Text": "Beginner",
    "🟰 Decisions": "Intermediate",
    "🔁 Loops": "Intermediate",
    "📋 Collections": "Intermediate",
    "⚙️ Functions": "Advanced",
    "🏗️ OOP Concepts": "Advanced",
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


def get_topic_difficulty(topic_key: str) -> str:
    for unit_name, keys in UNIT_STRUCTURE.items():
        if topic_key in keys:
            return _UNIT_DIFFICULTY.get(unit_name, "Beginner")
    return "Beginner"


def apply_theme() -> None:
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>

        /* Hide Streamlit's built-in sidebar toggle button completely.
           It renders "keyboard_double_arrow_right" via a Material Symbols font
           ligature; when that font fails to load the raw text floods the screen.
           The sidebar can still be toggled with the < keyboard shortcut. */
        [data-testid="collapsedControl"] {
            display: none !important;
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

        /* ── DIFFICULTY BADGE ───────────────────────── */
        .tt-difficulty-badge {
            display: inline-block;
            border-radius: 999px;
            padding: 0.2rem 0.75rem;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            font-family: 'Inter', sans-serif;
            vertical-align: middle;
            margin-left: 0.6rem;
            position: relative;
            top: -2px;
        }
        .tt-difficulty-beginner { background: #d1fae5; color: #065f46; }
        .tt-difficulty-intermediate { background: #fef3c7; color: #92400e; }
        .tt-difficulty-advanced { background: #ede9fe; color: #5b21b6; }

        </style>
        """,
        unsafe_allow_html=True,
    )
    # Inject JS via same-origin iframe to directly remove the broken sidebar
    # toggle button from the parent document. CSS cannot win against Streamlit's
    # Emotion CSS-in-JS which injects after us. JS DOM manipulation always wins.
    components.html(
        """
        <script>
        (function () {
            var ICON_TEXTS = [
                "keyboard_double_arrow_right",
                "keyboard_double_arrow_left",
                "keyboard_arrow_right",
                "keyboard_arrow_left",
                "keyboard_arrow_down",
                "keyboard_arrow_up",
                "expand_more",
                "expand_less",
                "chevron_right",
                "chevron_left",
                "menu",
            ];

            function hideIconElements(doc) {
                // 1. Hide by data-testid (Streamlit sidebar toggle)
                var toggle = doc.querySelector('[data-testid="collapsedControl"]');
                if (toggle) toggle.style.setProperty("display", "none", "important");

                // 2. Hide any span/button whose trimmed text is exactly an icon name
                doc.querySelectorAll("span, button").forEach(function (el) {
                    var txt = (el.textContent || "").trim();
                    if (ICON_TEXTS.indexOf(txt) !== -1) {
                        el.style.setProperty("display", "none", "important");
                        // Also hide the parent button if the span is inside one
                        var parent = el.parentElement;
                        if (parent && (parent.tagName === "BUTTON" || parent.getAttribute("role") === "button")) {
                            parent.style.setProperty("display", "none", "important");
                        }
                    }
                });
            }

            var doc = window.parent.document;
            hideIconElements(doc);

            // Keep hiding on every DOM mutation (Streamlit re-renders frequently)
            var observer = new MutationObserver(function () { hideIconElements(doc); });
            observer.observe(doc.body, { childList: true, subtree: true });
        })();
        </script>
        """,
        height=0,
        scrolling=False,
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

        # Initialise which units are open (all collapsed by default)
        if "sidebar_open_units" not in st.session_state:
            st.session_state.sidebar_open_units = set()

        for unit_name, topic_keys in UNIT_STRUCTURE.items():
            unit_completed = sum(1 for key in topic_keys if key in passed_topic_keys)
            is_open = unit_name in st.session_state.sidebar_open_units
            arrow = "▼" if is_open else "▶"
            unit_label = f"{arrow}  {unit_name}  {unit_completed}/{len(topic_keys)}"

            # Unit header button — toggling open/close without page rerun loss
            st.markdown(
                f'<div style="margin-bottom:2px">',
                unsafe_allow_html=True,
            )
            if st.button(
                unit_label,
                key=f"unit_{unit_name}",
                use_container_width=True,
            ):
                if is_open:
                    st.session_state.sidebar_open_units.discard(unit_name)
                else:
                    st.session_state.sidebar_open_units.add(unit_name)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            if not is_open:
                continue

            for topic_key in topic_keys:
                topic = next((t for t in TOPICS if t.key == topic_key), None)
                if not topic:
                    continue

                completed = topic_key in passed_topic_keys
                item = progress.get(topic_key)
                viewed = bool(item and item.viewed)
                topic_icon = TOPIC_ICONS.get(topic_key, "")

                if completed:
                    state_icon = "✓"
                elif viewed:
                    state_icon = "◉"
                else:
                    state_icon = "○"

                is_active = st.session_state.get("selected_topic") == topic_key
                if st.button(
                    f"  {state_icon}  {topic_icon}  {topic.title}",
                    key=f"nav_{topic_key}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state.selected_topic = topic_key
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

        if is_completed:
            state = "completed"
            dot_content = "✓"
        elif is_active:
            state = "active"
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
    difficulty = get_topic_difficulty(topic.key)
    difficulty_css = difficulty.lower()

    is_completed = latest_submission is not None and latest_submission.challenge_passed

    _render_progress_stepper(topic_key, passed_topic_keys)

    st.markdown(
        html_panel(
            "techtales-topic-card",
            f'<h2>{topic_icon}  {escape(topic.title)}'
            f'<span class="tt-difficulty-badge tt-difficulty-{difficulty_css}">{difficulty}</span>'
            f'</h2>'
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
    render_lesson(selected_topic_key, db_path, passed_topic_keys)


if __name__ == "__main__":
    main()
