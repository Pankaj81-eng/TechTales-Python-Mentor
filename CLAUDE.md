# TechTales Python Mentor

## Purpose

TechTales Python Mentor is a beginner-friendly Python learning platform.

The goal is to help users learn Python through:

* Stories
* Interactive lessons
* Coding challenges
* AI-assisted feedback
* Gamification (XP and progress tracking)

## Target Learner

Absolute beginners. Assume no prior programming knowledge. Explanations, feedback, and challenge prompts must be readable by someone who has never written a line of code.

## Technology Stack

* Python 3.9
* Streamlit >= 1.36 (no lockfile; `requirements.txt` is a lower-bound only)
* SQLite (runtime database auto-created at `data/techtales.db` on first run)

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The `data/` directory is created automatically. Never commit its contents.

## Module Structure

| File | Responsibility |
|---|---|
| `app.py` | Streamlit UI — rendering, routing, session state |
| `techtales/content.py` | Topic definitions (`TOPICS` tuple) |
| `techtales/db.py` | All SQLite reads and writes |
| `techtales/execution.py` | Sandboxed learner code execution |
| `techtales/evaluation.py` | Evaluator abstraction (unused stub — see Technical Debt) |
| `techtales/models.py` | Frozen dataclasses shared across the package |
| `techtales/validator.py` | AST-based challenge validation logic |

## Architecture Rules

* `app.py` may import from `techtales/`; `techtales/` must never import from `app.py`.
* Business logic (validation, execution, data access) belongs in `techtales/`. UI logic belongs in `app.py`.
* The validator receives only `submitted_code: str` and `ExecutionResult | None`. It must not call the database or the executor.
* Keep functions small and focused on one task.
* Prefer readability over cleverness.
* Do not add dependencies without a clear, concrete reason.

## Security Model

Learner code runs in a restricted sandbox defined in `execution.py`:

1. **AST validation** — the submission is parsed and walked before execution. Blocked node types include `Import`, `ImportFrom`, `Global`, `Delete`, `Raise`, `Try`, `With`, `Lambda`, async constructs, and double-underscore attributes.
2. **Subprocess isolation** — execution happens in a spawned child process (not a thread), so the learner's globals and memory are fully isolated from the app process.
3. **Timeout** — the child process is killed after 2 seconds to prevent infinite loops.
4. **Builtin allowlist** — only an explicit set of builtins is available (`print`, `range`, `int`, `str`, `float`, `bool`, `list`, `dict`, `set`, `tuple`, `len`, `abs`, `max`, `min`, `sum`, `round`, `enumerate`).

Any extension to the sandbox (new builtins, new allowed nodes) must be deliberate and reviewed.

## How to Add a New Topic

1. Add a `Topic(...)` entry to the `TOPICS` tuple in `techtales/content.py`.
2. Add a `validate_<key>_challenge` function in `techtales/validator.py` and wire it into `ChallengeValidator.validate`.
3. If the topic should be gated behind another, update `is_topic_unlocked` in `app.py`.
4. Topics without a dedicated validator fall back to a generic "has code" check — acceptable for early-stage topics, not a permanent state.

## Validator Contract

Each validator function must:

* Accept `submitted_code: str` and `execution_result: ExecutionResult | None`
* Return a `ValidationResult` with a tuple of `RequirementResult` items
* Each `RequirementResult` must have a `label`, a `passed` bool, and a non-empty `suggestion` string when `passed` is `False`
* Never raise — catch `SyntaxError` and return a `ValidationResult(passed=False, ...)` with human-readable feedback

## Business Rules

**XP**
* 20 XP is awarded once per topic, on the first passing submission only.
* Re-submitting a passing solution awards 0 XP.

**Progress states** (per topic)
* Not started → Lesson viewed → Completed

**Topic unlock gating**
* Only Data Types is currently gated — it is locked until the Variables challenge is passed.
* The check in `is_topic_unlocked` (`app.py`) is currently hardcoded, not a general dependency chain.

## Current Features

* Five lessons: Variables, Data Types, If/Else, Loops, Functions
* Topic unlock gating (Data Types locked until Variables is passed)
* Sandboxed code execution (AST validation + subprocess isolation + 2-second timeout)
* Program output panel (stdout shown live after each edit)
* Per-requirement pass/fail checklist with improvement suggestions
* Full AST-based validation for Variables and Loops; generic check for Data Types, If/Else, Functions
* XP tracking (20 XP on first pass per topic)
* Progress tracking (viewed / completed per topic)

## Known Technical Debt

* **`evaluation.py` is unused.** `SaveOnlyEvaluator` was a precursor to AI evaluation but is not imported anywhere. Wire it in or delete it.
* **Hardcoded unlock logic.** `is_topic_unlocked` in `app.py` explicitly checks `if topic_key != "data_types"`. Adding more gated topics requires changing this function rather than declaring a dependency in content.
* **Partial validator coverage.** Data Types, If/Else, and Functions fall back to a generic "has code" check. These need dedicated validators before those lessons can give meaningful feedback.

## Roadmap

### v0.2 (in progress)

* Show expected output alongside actual program output

### v0.3

* Full AST-based validation for Data Types, If/Else, and Functions
* AI Mentor — ask questions about the current lesson, get explanations for mistakes

### v0.4

* Voice Learning

### v0.5

* Daily Challenges

## Testing Strategy

There are currently no automated tests. The intent:

* Unit tests for `validator.py` — pure functions, straightforward to test with code strings
* Unit tests for `execution.py` — sandbox safety, timeout behaviour, allowed builtins
* No UI tests for now

When adding tests, place them in a `tests/` directory mirroring the `techtales/` package structure.

## Coding Standards

* Default to writing no comments. Only add one when the *why* is non-obvious — a hidden constraint, a workaround, a subtle invariant.
* Update the README when a major feature ships.
* Keep functions focused on one task.
* Prefer maintainability over clever code.
* No linting or formatting tooling is enforced yet. Use `ruff` for linting and `ruff format` for formatting if you add tooling.

## Git Rules

* Never commit SQLite database files (`data/`).
* Never commit secrets or `.env` files.
* Respect `.gitignore`.

## UX Principles

The learner should always understand:

* What passed
* What failed
* Why it failed
* How to improve

Feedback must be educational, not punitive. A failed check is an invitation to try again, not a judgment.
