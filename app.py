from __future__ import annotations

import json
import random
from html import escape

import streamlit as st
import streamlit.components.v1 as components

from techtales.content import TOPICS, get_topic
from techtales.models import Submission
from techtales.db import (
    get_anon_client,
    make_client,
    get_current_xp,
    get_latest_submission,
    get_passed_topic_keys,
    get_progress,
    get_streak,
    initialize_user,
    mark_topic_viewed,
    save_submission,
    save_exam_result,
    get_all_exam_results,
)
from techtales.quiz import EXAMS, EXAM_ORDER
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
    # Unit 8 — Advanced Functions
    "dict_set_comprehensions": ("exercise_class_design", "Exercise: Design a Class"),
    "args_kwargs": ("dict_set_comprehensions", "Dict & Set Comprehensions"),
    "closures": ("args_kwargs", "*args and **kwargs"),
    "lambda_functions": ("closures", "Closures"),
    "map_filter": ("lambda_functions", "Lambda Functions"),
    "sorted_key": ("map_filter", "map() and filter()"),
    "zip_function": ("sorted_key", "Sorting with a Key"),
    "decorators_intro": ("zip_function", "zip()"),
    "exercise_functional": ("decorators_intro", "Decorators"),
    # Unit 9 — Error Handling
    "exceptions_intro": ("exercise_functional", "Exercise: Functional Toolkit"),
    "try_except": ("exceptions_intro", "What are Exceptions?"),
    "multiple_exceptions": ("try_except", "try / except"),
    "finally_clause": ("multiple_exceptions", "Multiple Exception Types"),
    "raising_exceptions": ("finally_clause", "finally and else"),
    "exercise_safe_calculator": ("raising_exceptions", "Raising Exceptions"),
    # Unit 10 — Generators & Iterators
    "generators_yield": ("exercise_safe_calculator", "Exercise: Safe Calculator"),
    "generator_expressions": ("generators_yield", "Generators with yield"),
    "iterator_protocol": ("generator_expressions", "Generator Expressions"),
    "exercise_custom_range": ("iterator_protocol", "The Iterator Protocol"),
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
    # Unit 8 — Advanced Functions
    "dict_set_comprehensions": "🗃️",
    "args_kwargs": "📥",
    "closures": "🧲",
    "lambda_functions": "λ",
    "map_filter": "🔭",
    "sorted_key": "🔤",
    "zip_function": "🤐",
    "decorators_intro": "🎀",
    "exercise_functional": "🏭",
    # Unit 9 — Error Handling
    "exceptions_intro": "💥",
    "try_except": "🛡️",
    "multiple_exceptions": "🎭",
    "finally_clause": "🔚",
    "raising_exceptions": "🚨",
    "exercise_safe_calculator": "🧮",
    # Unit 10 — Generators & Iterators
    "generators_yield": "🔋",
    "generator_expressions": "🌊",
    "iterator_protocol": "🔗",
    "exercise_custom_range": "🎯",
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
    "🔧 Advanced Functions": (
        "dict_set_comprehensions", "args_kwargs", "closures", "lambda_functions",
        "map_filter", "sorted_key", "zip_function", "decorators_intro", "exercise_functional",
    ),
    "🛡️ Error Handling": (
        "exceptions_intro", "try_except", "multiple_exceptions",
        "finally_clause", "raising_exceptions", "exercise_safe_calculator",
    ),
    "🔋 Generators & Iterators": (
        "generators_yield", "generator_expressions", "iterator_protocol", "exercise_custom_range",
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
    "🔧 Advanced Functions": "Advanced",
    "🛡️ Error Handling": "Advanced",
    "🔋 Generators & Iterators": "Advanced",
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

        /* Topic buttons — slate/cool-white, clearly distinct from the lavender unit headers */
        section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
            background: rgba(148, 163, 184, 0.07) !important;
            border: 1px solid rgba(148, 163, 184, 0.13) !important;
            color: #cbd5e1 !important;
        }

        section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {
            background: rgba(148, 163, 184, 0.18) !important;
            border-color: rgba(148, 163, 184, 0.3) !important;
            color: #f1f5f9 !important;
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

        /* ── SIDEBAR UNIT EXPANDERS ─────────────────── */
        /* Container: flush, no card border */
        section[data-testid="stSidebar"] [data-testid="stExpander"] {
            background: transparent !important;
            border: none !important;
            border-top: 1px solid rgba(99, 102, 241, 0.18) !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Header row: lavender uppercase — the "section label" look */
        section[data-testid="stSidebar"] [data-testid="stExpander"] summary,
        section[data-testid="stSidebar"] details > summary {
            color: #a5b4fc !important;
            font-size: 0.7rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.07em !important;
            text-transform: uppercase !important;
            padding: 0.45rem 0.1rem !important;
            background: transparent !important;
            border: none !important;
        }

        /* The expand/collapse arrow icon */
        section[data-testid="stSidebar"] [data-testid="stExpander"] summary svg {
            fill: #6366f1 !important;
        }

        /* Body area inside expander */
        section[data-testid="stSidebar"] [data-testid="stExpander"] > div:last-child {
            padding: 0 0 0.25rem !important;
            background: transparent !important;
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

        /* ── EXAM UI ────────────────────────────────── */
        .tt-exam-card {
            background: #ffffff;
            border: 1px solid #e0e7ff;
            border-radius: 14px;
            padding: 1.6rem 1.8rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 12px rgba(79, 70, 229, 0.08);
        }

        .tt-exam-prompt {
            font-size: 1.05rem;
            font-weight: 600;
            color: #1e1b4b;
            margin-bottom: 0.75rem;
            font-family: 'Inter', sans-serif;
            line-height: 1.5;
        }

        .tt-exam-code {
            background: #0d1117;
            color: #e6edf3;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.85rem;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            white-space: pre-wrap;
        }

        .tt-exam-code .tt-blank {
            background: #fde68a;
            color: #1e1b4b;
            border-radius: 4px;
            padding: 0 0.3rem;
            font-weight: 700;
        }

        .tt-badge-earned {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: #ffffff;
            border-radius: 999px;
            padding: 0.4rem 1.1rem;
            font-size: 0.9rem;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
            margin: 0.5rem 0;
        }

        .tt-exam-result-pass {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            border-radius: 14px;
            padding: 2rem;
            text-align: center;
            color: #ffffff;
            margin-bottom: 1.2rem;
        }

        .tt-exam-result-fail {
            background: #f8fafc;
            border: 2px solid #e0e7ff;
            border-radius: 14px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1.2rem;
        }

        .tt-exam-score {
            font-size: 3rem;
            font-weight: 800;
            line-height: 1;
            font-family: 'Inter', sans-serif;
        }

        .tt-exam-score-label {
            font-size: 0.85rem;
            opacity: 0.85;
            margin-top: 0.2rem;
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar exam entry */
        .tt-exam-sidebar-badge {
            display: inline-block;
            font-size: 0.65rem;
            font-weight: 700;
            background: #fef3c7;
            color: #92400e;
            border-radius: 999px;
            padding: 0.1rem 0.45rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-left: 0.3rem;
            vertical-align: middle;
        }
        .tt-exam-sidebar-badge.earned {
            background: #d1fae5;
            color: #065f46;
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


def get_unlocked_exams(passed_topic_keys: set[str]) -> list[str]:
    """Return exam keys the learner has unlocked (trigger topic passed)."""
    return [key for key in EXAM_ORDER if EXAMS[key].trigger_topic in passed_topic_keys]


def _init_exam_state(exam_key: str) -> None:
    """Randomise question order and option order; store in session state."""
    exam = EXAMS[exam_key]
    q_indices = random.sample(range(len(exam.questions)), min(20, len(exam.questions)))
    shuffled_options = []
    for qi in q_indices:
        opts = list(exam.questions[qi].options)
        random.shuffle(opts)
        shuffled_options.append(opts)
    st.session_state[f"exam_state_{exam_key}"] = {
        "q_indices": q_indices,
        "shuffled_options": shuffled_options,
        "answers": [],
        "xp_saved": False,
    }


def _render_exam_code(code: str) -> str:
    """Render code snippet with ___ highlighted as a yellow blank."""
    parts = code.split("___")
    escaped = []
    for i, part in enumerate(parts):
        escaped.append(escape(part))
        if i < len(parts) - 1:
            escaped.append('<span class="tt-blank">___</span>')
    return "".join(escaped)


def render_exam(exam_key: str, client, user_id: str | None) -> None:
    exam = EXAMS[exam_key]
    state_key = f"exam_state_{exam_key}"

    if state_key not in st.session_state:
        _init_exam_state(exam_key)

    state = st.session_state[state_key]
    answers = state["answers"]
    total = len(state["q_indices"])
    current_q = len(answers)
    is_done = current_q >= total

    if st.button("← Back to lessons", key=f"exam_back_{exam_key}"):
        st.session_state.pop(state_key, None)
        st.session_state.selected_topic = TOPICS[0].key
        st.rerun()

    if is_done:
        _render_exam_results(exam, state, client, user_id)
        return

    # Progress header
    st.markdown(
        f'<div style="font-family:Inter,sans-serif;margin-bottom:0.5rem">'
        f'<span style="font-size:1.3rem">{exam.badge_emoji}</span>'
        f'<strong style="font-size:1.1rem;color:#1e1b4b;margin-left:0.4rem">{escape(exam.title)}</strong>'
        f'<span style="float:right;font-size:0.82rem;color:#6b7280;padding-top:0.25rem">'
        f'Question {current_q + 1} of {total}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.progress((current_q) / total)

    # Current question
    qi = state["q_indices"][current_q]
    question = exam.questions[qi]
    opts = state["shuffled_options"][current_q]

    code_html = ""
    if question.code:
        code_html = (
            f'<div class="tt-exam-code">{_render_exam_code(question.code)}</div>'
        )

    st.markdown(
        f'<div class="tt-exam-card">'
        f'<div class="tt-exam-prompt">{escape(question.prompt)}</div>'
        f'{code_html}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Answer option buttons
    col1, col2 = st.columns(2)
    option_labels = ["A", "B", "C", "D"]
    for i, opt in enumerate(opts):
        col = col1 if i < 2 else col2
        with col:
            if st.button(
                f"**{option_labels[i]}.**  {opt}",
                key=f"exam_{exam_key}_q{current_q}_opt{i}",
                use_container_width=True,
            ):
                state["answers"].append(opt)
                st.rerun()


def _render_exam_results(exam, state: dict, client, user_id: str | None) -> None:
    answers = state["answers"]
    q_indices = state["q_indices"]
    score = sum(
        1 for i, ans in enumerate(answers)
        if ans == exam.questions[q_indices[i]].answer
    )
    total = len(answers)
    passed = score / total >= exam.pass_threshold
    pct = int(score / total * 100)

    # Save to DB once per result
    xp_awarded = 0
    if not state.get("xp_saved") and client is not None and user_id is not None:
        xp_awarded = save_exam_result(client, user_id, exam.key, score, total, passed)
        state["xp_saved"] = True

    if passed:
        badge_html = (
            f'<div class="tt-badge-earned">'
            f'{exam.badge_emoji} {escape(exam.badge_name)}'
            f'</div>'
        )
        xp_text = f"+{xp_awarded} XP" if xp_awarded else "Badge already earned"
        st.markdown(
            f'<div class="tt-exam-result-pass">'
            f'<div class="tt-exam-score">{score}/{total}</div>'
            f'<div class="tt-exam-score-label">{pct}% correct — Exam Passed!</div>'
            f'<div style="margin:0.8rem 0">{badge_html}</div>'
            f'<div style="font-size:0.88rem;opacity:0.9">{xp_text}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if xp_awarded:
            st.balloons()
    else:
        needed = int(exam.pass_threshold * total)
        st.markdown(
            f'<div class="tt-exam-result-fail">'
            f'<div class="tt-exam-score" style="color:#4f46e5">{score}/{total}</div>'
            f'<div class="tt-exam-score-label" style="color:#6b7280">'
            f'{pct}% correct — you need {int(exam.pass_threshold*100)}% ({needed}/{total}) to earn the badge'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Question review
    with st.expander("Review your answers"):
        for i, (qi, ans) in enumerate(zip(q_indices, answers)):
            q = exam.questions[qi]
            correct = ans == q.answer
            icon = "✅" if correct else "❌"
            st.markdown(
                f"**Q{i+1}.** {icon} {q.prompt}  \n"
                f"Your answer: `{ans}`"
                + (f"  \nCorrect answer: `{q.answer}`" if not correct else ""),
            )

    col_retry, col_back = st.columns(2)
    with col_retry:
        if st.button("Try Again", use_container_width=True, key=f"exam_retry_{exam.key}"):
            _init_exam_state(exam.key)
            st.rerun()
    with col_back:
        if st.button("← Back to lessons", use_container_width=True, key=f"exam_done_back_{exam.key}"):
            st.session_state.pop(f"exam_state_{exam.key}", None)
            st.session_state.selected_topic = TOPICS[0].key
            st.rerun()


def is_topic_unlocked(topic_key: str, passed_topic_keys: set[str]) -> bool:
    prereq = TOPIC_PREREQUISITES.get(topic_key)
    if prereq:
        return prereq[0] in passed_topic_keys
    return True


def html_panel(css_class: str, content: str) -> str:
    return f'<div class="{css_class}">{content}</div>'


def _is_authenticated() -> bool:
    return "supabase_session" in st.session_state


def _handle_login(email: str, password: str) -> None:
    try:
        anon = get_anon_client()
        resp = anon.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.supabase_session = {
            "access_token": resp.session.access_token,
            "refresh_token": resp.session.refresh_token,
            "user_id": resp.user.id,
            "user_email": resp.user.email,
        }
        st.session_state.supabase_client = make_client(resp.session.access_token)
        st.rerun()
    except Exception as exc:
        st.error(f"Login failed: {exc}")


def _handle_signup(email: str, password: str) -> None:
    try:
        anon = get_anon_client()
        resp = anon.auth.sign_up({"email": email, "password": password})
        if resp.session:
            st.session_state.supabase_session = {
                "access_token": resp.session.access_token,
                "refresh_token": resp.session.refresh_token,
                "user_id": resp.user.id,
                "user_email": resp.user.email,
            }
            st.session_state.supabase_client = make_client(resp.session.access_token)
            st.rerun()
        else:
            st.success("Account created! Check your email to confirm, then log in.")
    except Exception as exc:
        st.error(f"Sign-up failed: {exc}")


def render_auth_page() -> None:
    st.markdown(
        """
        <div style="text-align:center;padding:3rem 0 1.5rem">
            <div style="font-size:2rem;font-weight:800;color:#1e1b4b;font-family:Inter,sans-serif;letter-spacing:-0.02em">TechTales</div>
            <div style="font-size:0.75rem;font-weight:700;color:#6366f1;letter-spacing:0.1em;text-transform:uppercase;font-family:Inter,sans-serif;margin-top:0.2rem">Python Mentor</div>
            <div style="font-size:0.92rem;color:#6b7280;margin-top:0.6rem;font-family:Inter,sans-serif">Learn Python through interactive lessons and challenges</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

        with tab_login:
            email = st.text_input("Email", key="login_email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Log In", type="primary", use_container_width=True, key="login_btn"):
                if email and password:
                    _handle_login(email, password)
                else:
                    st.warning("Enter your email and password.")

        with tab_signup:
            email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
            password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
            if st.button("Create Account", type="primary", use_container_width=True, key="signup_btn"):
                if email and len(password) >= 6:
                    _handle_signup(email, password)
                else:
                    st.warning("Enter a valid email and a password of at least 6 characters.")


def render_sidebar(client, user_id: str | None, passed_topic_keys: set[str], user_email: str = "", all_exam_results: dict | None = None) -> None:
    is_guest = client is None
    progress = get_progress(client) if not is_guest else {}
    completed_count = len(passed_topic_keys)
    if all_exam_results is None:
        all_exam_results = {}

    if not is_guest:
        current_xp = get_current_xp(client)
        level, level_xp, level_to_next = get_level(current_xp)
        current_streak, longest_streak = get_streak(client)

    with st.sidebar:
        st.markdown(
            '<div style="padding: 1rem 0 0.5rem;">'
            '<span style="font-size: 1.5rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; font-family: Inter, sans-serif;">TechTales</span>'
            '<span style="display: block; font-size: 0.78rem; color: #6366f1; margin-top: 0.15rem; font-family: Inter, sans-serif; letter-spacing: 0.04em; text-transform: uppercase; font-weight: 600;">Python Mentor</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        if is_guest:
            st.markdown(
                '<div style="text-align:center;font-size:0.73rem;color:#818cf8;padding:0.2rem 0 0.5rem;font-family:Inter,sans-serif">Exploring as guest</div>',
                unsafe_allow_html=True,
            )
            tab_l, tab_s = st.tabs(["Log In", "Sign Up"])
            with tab_l:
                g_email = st.text_input("Email", key="g_login_email", placeholder="you@example.com", label_visibility="collapsed")
                g_pass = st.text_input("Password", type="password", key="g_login_pass", placeholder="Password", label_visibility="collapsed")
                if st.button("Log In", type="primary", use_container_width=True, key="g_login_btn"):
                    if g_email and g_pass:
                        _handle_login(g_email, g_pass)
                    else:
                        st.warning("Enter email and password.")
            with tab_s:
                g_email2 = st.text_input("Email", key="g_signup_email", placeholder="you@example.com", label_visibility="collapsed")
                g_pass2 = st.text_input("Password", type="password", key="g_signup_pass", placeholder="Min 6 characters", label_visibility="collapsed")
                if st.button("Sign Up Free", type="primary", use_container_width=True, key="g_signup_btn"):
                    if g_email2 and len(g_pass2) >= 6:
                        _handle_signup(g_email2, g_pass2)
                    else:
                        st.warning("Need email + 6+ char password.")
        else:
            if user_email:
                st.markdown(
                    f'<div style="font-size:0.68rem;color:#818cf8;text-align:center;margin-bottom:0.3rem;font-family:Inter,sans-serif;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{user_email}</div>',
                    unsafe_allow_html=True,
                )
            if st.button("Log Out", use_container_width=True, key="logout_btn"):
                for k in ["supabase_session", "supabase_client", "selected_topic"]:
                    st.session_state.pop(k, None)
                st.rerun()

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

            # ── Earned badges strip ────────────────────
            earned_badges = [
                EXAMS[k] for k in EXAM_ORDER
                if all_exam_results.get(k, {}).get("passed")
            ]
            if earned_badges:
                chips = "".join(
                    f'<span style="display:inline-flex;align-items:center;gap:0.25rem;'
                    f'background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;'
                    f'border-radius:999px;padding:0.22rem 0.65rem;font-size:0.72rem;'
                    f'font-weight:700;font-family:Inter,sans-serif;white-space:nowrap;'
                    f'box-shadow:0 2px 8px rgba(79,70,229,0.35)">'
                    f'{exam.badge_emoji} {exam.badge_name}</span>'
                    for exam in earned_badges
                )
                st.markdown(
                    f'<div style="margin:0.55rem 0 0.1rem">'
                    f'<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.08em;'
                    f'color:#6366f1;text-transform:uppercase;font-family:Inter,sans-serif;'
                    f'margin-bottom:0.35rem">🎖️ My Badges</div>'
                    f'<div style="display:flex;flex-wrap:wrap;gap:0.3rem">{chips}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # ── Profile button ─────────────────────────
            is_profile = st.session_state.get("selected_topic") == "__profile__"
            if st.button(
                "👤 My Profile",
                key="nav_profile",
                use_container_width=True,
                type="primary" if is_profile else "secondary",
            ):
                st.session_state.selected_topic = "__profile__"
                st.rerun()

        if user_email == _ADMIN_EMAIL:
            st.divider()
            is_stats = st.session_state.get("selected_topic") == "__stats__"
            if st.button(
                "📊 Stats",
                key="nav_stats",
                use_container_width=True,
                type="primary" if is_stats else "secondary",
            ):
                st.session_state.selected_topic = "__stats__"
                st.rerun()

        st.divider()

        selected_key = st.session_state.get("selected_topic", "")
        for unit_name, topic_keys in UNIT_STRUCTURE.items():
            unit_completed = sum(1 for key in topic_keys if key in passed_topic_keys)
            has_active = selected_key in topic_keys
            label = f"{unit_name}  ·  {unit_completed}/{len(topic_keys)}"

            with st.expander(label, expanded=has_active):
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

                    is_active = selected_key == topic_key
                    if st.button(
                        f"  {state_icon}  {topic_icon}  {topic.title}",
                        key=f"nav_{topic_key}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary",
                    ):
                        st.session_state.selected_topic = topic_key
                        st.rerun()

        # ── EXAMS section ─────────────────────────────
        unlocked_exams = get_unlocked_exams(passed_topic_keys)
        if unlocked_exams:
            st.divider()
            st.caption("EXAMS")
            for exam_key in unlocked_exams:
                exam = EXAMS[exam_key]
                result = all_exam_results.get(exam_key)
                earned = result is not None and result.get("passed")
                badge_label = "DONE" if earned else "NEW"
                badge_class = "earned" if earned else ""
                is_active_exam = st.session_state.get("selected_topic") == f"__exam__{exam_key}"
                label = (
                    f"  {exam.badge_emoji}  {exam.title}"
                    f'  {"✓" if earned else "→"}'
                )
                if st.button(
                    label,
                    key=f"nav_exam_{exam_key}",
                    use_container_width=True,
                    type="primary" if is_active_exam else "secondary",
                ):
                    st.session_state.selected_topic = f"__exam__{exam_key}"
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


def render_profile_page(
    client,
    user_id: str | None,
    user_email: str,
    passed_topic_keys: set[str],
    all_exam_results: dict,
) -> None:
    current_xp = get_current_xp(client) if client else 0
    level, level_xp, level_to_next = get_level(current_xp)
    current_streak, longest_streak = get_streak(client) if client else (0, 0)
    completed_count = len(passed_topic_keys)

    st.markdown(
        f'<h2 style="color:#1e1b4b;font-family:Inter,sans-serif;margin-bottom:0.25rem">👤 My Profile</h2>'
        f'<div style="color:#6b7280;font-size:0.88rem;font-family:Inter,sans-serif;margin-bottom:1.5rem">{user_email}</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total XP", current_xp)
    c2.metric("Level", level)
    c3.metric("Topics Done", f"{completed_count}/{len(TOPICS)}")
    c4.metric("🔥 Streak", f"{current_streak} day{'s' if current_streak != 1 else ''}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Badge showcase ──────────────────────────────────────────
    st.markdown(
        '<h3 style="color:#1e1b4b;font-family:Inter,sans-serif;margin-bottom:0.75rem">🎖️ Badges</h3>',
        unsafe_allow_html=True,
    )

    badge_cards = []
    for key in EXAM_ORDER:
        exam = EXAMS[key]
        result = all_exam_results.get(key)
        earned = result is not None and result.get("passed")
        score_text = f"{result['score']}/{result['total']}" if result else ""

        if earned:
            card = (
                f'<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);'
                f'border-radius:14px;padding:1.2rem;text-align:center;'
                f'box-shadow:0 4px 18px rgba(79,70,229,0.35)">'
                f'<div style="font-size:2.2rem;line-height:1">{exam.badge_emoji}</div>'
                f'<div style="color:#ffffff;font-weight:700;font-size:0.85rem;'
                f'font-family:Inter,sans-serif;margin-top:0.5rem">{exam.badge_name}</div>'
                f'<div style="color:#c7d2fe;font-size:0.72rem;font-family:Inter,sans-serif;'
                f'margin-top:0.2rem">{score_text} · Passed</div>'
                f'</div>'
            )
        else:
            card = (
                f'<div style="background:#f1f5f9;border:2px dashed #cbd5e1;'
                f'border-radius:14px;padding:1.2rem;text-align:center;opacity:0.55">'
                f'<div style="font-size:2.2rem;line-height:1;filter:grayscale(1)">{exam.badge_emoji}</div>'
                f'<div style="color:#94a3b8;font-weight:700;font-size:0.85rem;'
                f'font-family:Inter,sans-serif;margin-top:0.5rem">{exam.badge_name}</div>'
                f'<div style="color:#cbd5e1;font-size:0.72rem;font-family:Inter,sans-serif;'
                f'margin-top:0.2rem">Locked</div>'
                f'</div>'
            )
        badge_cards.append(card)

    cols = st.columns(3)
    for i, card in enumerate(badge_cards):
        with cols[i % 3]:
            st.markdown(card, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:0.75rem'></div>", unsafe_allow_html=True)

    # ── Progress by unit ────────────────────────────────────────
    st.markdown(
        '<h3 style="color:#1e1b4b;font-family:Inter,sans-serif;margin:1.5rem 0 0.75rem">📚 Progress by Unit</h3>',
        unsafe_allow_html=True,
    )
    for unit_name, topic_keys in UNIT_STRUCTURE.items():
        done = sum(1 for k in topic_keys if k in passed_topic_keys)
        total = len(topic_keys)
        pct = done / total if total else 0
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'font-family:Inter,sans-serif;font-size:0.82rem;margin-bottom:0.15rem">'
            f'<span style="color:#374151">{unit_name}</span>'
            f'<span style="color:#6b7280">{done}/{total}</span></div>',
            unsafe_allow_html=True,
        )
        st.progress(pct)


_ADMIN_EMAIL = "pankajverma.mca@gmail.com"


def render_stats_page(client) -> None:
    st.markdown(
        '<h2 style="color:#1e1b4b;font-family:Inter,sans-serif;margin-bottom:1.2rem">📊 Admin Stats</h2>',
        unsafe_allow_html=True,
    )
    try:
        result = client.rpc("get_visitor_stats").execute()
        s = result.data
    except Exception as exc:
        st.error(f"Could not load stats: {exc}")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Visitors today", s.get("visits_today", 0))
    c2.metric("Visitors this week", s.get("visits_this_week", 0))
    c3.metric("All-time visitors", s.get("total_visits", 0))

    c4, c5, c6 = st.columns(3)
    c4.metric("Registered users", s.get("total_users", 0))
    c5.metric("Total submissions", s.get("total_submissions", 0))
    c6.metric("Challenges passed", s.get("challenges_passed", 0))

    daily = s.get("daily_visits") or []
    if daily:
        st.subheader("Daily visitors — last 14 days")
        import pandas as pd
        df = pd.DataFrame(daily)
        df["day"] = pd.to_datetime(df["day"])
        df = df.set_index("day")
        st.bar_chart(df["visits"])

    top = s.get("top_lessons") or []
    if top:
        st.subheader("Most attempted lessons")
        import pandas as pd
        df2 = pd.DataFrame(top)[["topic_key", "attempts", "passes"]]
        df2.columns = ["Lesson", "Attempts", "Passes"]
        st.dataframe(df2, use_container_width=True, hide_index=True)


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


def render_lesson(topic_key: str, client, user_id: str | None, passed_topic_keys: set[str]) -> None:
    topic = get_topic(topic_key)
    if client is not None:
        mark_topic_viewed(client, user_id, topic.key)
    latest_submission = (
        get_latest_submission(client, topic.key)
        if client is not None
        else st.session_state.get(f"guest_result_{topic.key}")
    )

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
                if client is not None:
                    save_submission(
                        client=client,
                        user_id=user_id,
                        topic_key=topic.key,
                        code=code,
                        evaluator_status=validation.status,
                        evaluator_message=validation.feedback,
                        challenge_passed=validation.passed,
                        validation_details=validation_details,
                        stdout=execution_result.stdout if execution_result else "",
                        runtime_error=execution_result.error if execution_result else None,
                    )
                else:
                    st.session_state[f"guest_result_{topic.key}"] = Submission(
                        id=None,
                        topic_key=topic.key,
                        code=code,
                        evaluator_status=validation.status,
                        evaluator_message=validation.feedback,
                        submitted_at="",
                        challenge_passed=validation.passed,
                        validation_details=json.dumps(validation_details),
                        xp_awarded=0,
                        stdout=execution_result.stdout if execution_result else "",
                        runtime_error=execution_result.error if execution_result else None,
                    )
                    if validation.passed:
                        st.session_state.setdefault("guest_passed_topics", set()).add(topic.key)
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
            if client is None and latest_submission.challenge_passed:
                st.markdown(
                    '<div style="border:1px solid #a5b4fc;background:#eef2ff;border-radius:12px;'
                    'padding:1rem 1.2rem;text-align:center;margin-top:0.75rem">'
                    '<strong style="color:#1e1b4b;font-family:Inter,sans-serif">Sign up to save your progress</strong>'
                    '<p style="color:#4f46e5;font-size:0.85rem;margin:0.3rem 0 0;font-family:Inter,sans-serif">'
                    'Create a free account — your XP, streak, and history are stored in the cloud.'
                    '</p></div>',
                    unsafe_allow_html=True,
                )


def render_guest_banner() -> None:
    """Compact sign-up bar shown to guests at the top of every page — visible on mobile."""
    with st.expander("✨ Sign up free to save your progress, XP and streaks", expanded=False):
        tab_l, tab_s = st.tabs(["Log In", "Sign Up"])
        with tab_l:
            col1, col2 = st.columns(2)
            with col1:
                b_email = st.text_input("Email", key="b_login_email", placeholder="you@example.com", label_visibility="collapsed")
            with col2:
                b_pass = st.text_input("Password", type="password", key="b_login_pass", placeholder="Password", label_visibility="collapsed")
            if st.button("Log In", type="primary", use_container_width=True, key="b_login_btn"):
                if b_email and b_pass:
                    _handle_login(b_email, b_pass)
                else:
                    st.warning("Enter your email and password.")
        with tab_s:
            col3, col4 = st.columns(2)
            with col3:
                b_email2 = st.text_input("Email", key="b_signup_email", placeholder="you@example.com", label_visibility="collapsed")
            with col4:
                b_pass2 = st.text_input("Password", type="password", key="b_signup_pass", placeholder="Min 6 characters", label_visibility="collapsed")
            if st.button("Sign Up Free", type="primary", use_container_width=True, key="b_signup_btn"):
                if b_email2 and len(b_pass2) >= 6:
                    _handle_signup(b_email2, b_pass2)
                else:
                    st.warning("Enter a valid email and a password of at least 6 characters.")


def _record_visit() -> None:
    if "visit_recorded" not in st.session_state:
        st.session_state.visit_recorded = True
        try:
            from datetime import datetime, timezone
            get_anon_client().table("page_views").insert(
                {"viewed_at": datetime.now(timezone.utc).isoformat()}
            ).execute()
        except Exception:
            pass  # analytics must never crash the app


def main() -> None:
    apply_theme()
    _record_visit()

    if _is_authenticated():
        session = st.session_state.supabase_session
        client = st.session_state.supabase_client
        user_id = session["user_id"]
        user_email = session["user_email"]
        initialize_user(client, user_id)
        passed_topic_keys = get_passed_topic_keys(client)
        try:
            all_exam_results = get_all_exam_results(client)
        except Exception:
            all_exam_results = {}
    else:
        client = None
        user_id = None
        user_email = ""
        passed_topic_keys = st.session_state.get("guest_passed_topics", set())
        all_exam_results = {}

    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = TOPICS[0].key

    render_sidebar(client, user_id, passed_topic_keys, user_email, all_exam_results)

    selected_topic_key = st.session_state.selected_topic

    if selected_topic_key == "__profile__" and client is not None:
        render_profile_page(client, user_id, user_email, passed_topic_keys, all_exam_results)
    elif selected_topic_key == "__stats__" and user_email == _ADMIN_EMAIL:
        if st.button("← Back to lessons", key="stats_back"):
            st.session_state.selected_topic = TOPICS[0].key
            st.rerun()
        render_stats_page(client)
    elif selected_topic_key.startswith("__exam__"):
        exam_key = selected_topic_key[len("__exam__"):]
        if exam_key in EXAMS:
            render_exam(exam_key, client, user_id)
        else:
            st.error("Unknown exam.")
    else:
        if client is None:
            render_guest_banner()
        elif user_email == _ADMIN_EMAIL:
            if st.button("📊 Stats", key="main_stats_btn"):
                st.session_state.selected_topic = "__stats__"
                st.rerun()
        render_lesson(selected_topic_key, client, user_id, passed_topic_keys)


if __name__ == "__main__":
    main()
