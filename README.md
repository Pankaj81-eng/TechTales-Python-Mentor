# TechTales Python Mentor

An interactive Python learning platform built for absolute beginners. Learn Python through structured lessons, hands-on coding challenges, instant sandboxed execution, and XP-based progress tracking.

---

## Screenshot

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/2606c31c-dd03-42bd-be06-b852a8167f3b" />


---

## What's Inside

### 50-lesson curriculum across 7 units

| Unit | Topics | Level |
|---|---|---|
| 🌍 Foundations | Write a Program, Variables, Data Types, Type Conversion, Arithmetic Operators, F-Strings, Exercise: Profile Card | Beginner |
| 🔠 Text | String Indexing & Slicing, String Methods, Split & Join | Beginner |
| 🟰 Decisions | Comparison Operators, Boolean Logic, If/Else, Elif, Membership Operators, Conditional Expression, Exercise: Grade Checker | Intermediate |
| 🔁 Loops | For Loops, Looping Over Collections, Enumerate, While Loops, Break & Continue, Nested Loops, Exercise: Pattern Printer | Intermediate |
| 📋 Collections | Lists, List Methods, List Slicing, List Comprehensions, Tuples, Tuple Unpacking, Sets, Dictionaries, Dict Methods, Dict Iteration, Nested Data, Exercise: Inventory Tracker | Intermediate |
| ⚙️ Functions | Functions, Function Parameters, Default Parameters, Multiple Return Values, None, Recursion, Exercise: Mini Calculator | Advanced |
| 🏗️ OOP Concepts | What is a Class?, Define a Class with `__init__`, Create Objects, Add Methods, Work with Attributes, Inheritance, Exercise: Design a Class | Advanced |

### Features

- **Sandboxed code execution** — learner code runs in a subprocess with a 2-second timeout, AST validation, and an allowlist of safe builtins. No imports, no file access, no surprises.
- **Dynamic AST-based validation** — each challenge checks the *concept*, not a specific pattern. Write it your own way as long as you demonstrate the idea.
- **Per-requirement pass/fail checklist** — see exactly what passed, what failed, and get a specific suggestion for each failing requirement.
- **Difficulty badges** — every lesson is tagged Beginner, Intermediate, or Advanced at a glance.
- **Collapsible sidebar units** — 50 lessons organized into 7 collapsible unit sections, each showing completion progress.
- **XP & level system** — earn 20 XP on first pass per topic; level up through 5 levels.
- **Streak tracking** — daily and best streak shown in the sidebar.
- **Progress stepper** — horizontal visual timeline of all 50 lessons at the top of every page.
- **Exercise checkpoints** — 5 applied exercises throughout the curriculum where you build a small real program combining everything learned so far.

---

## Why I Built This

I wanted to strengthen my Python fundamentals while exploring AI-assisted development. Instead of following another tutorial, I built TechTales Python Mentor to learn Python through interactive lessons, coding challenges, and instant feedback — and to learn how to build real software with AI tooling along the way.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9 |
| UI | Streamlit ≥ 1.36 |
| Database | SQLite (local, auto-created at `data/techtales.db`) |
| Code execution | Subprocess isolation + AST validation |
| Development | Built with Claude Code (Anthropic) |

---

## Running Locally

```bash
git clone https://github.com/Pankaj81-eng/TechTales-Python-Mentor
cd TechTales-Python-Mentor

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

The app opens at **http://localhost:8501**. The `data/` directory and SQLite database are created automatically on first run.

---

## Project Structure

```
app.py                  # Streamlit UI — routing, session state, rendering
techtales/
  content.py            # All 50 Topic definitions (lesson, example, challenge, mentor card)
  validator.py          # AST-based challenge validators — one per topic
  execution.py          # Sandboxed subprocess runner
  db.py                 # SQLite reads and writes
  models.py             # Shared dataclasses (Topic, MentorCard, ValidationResult …)
```

---

## Roadmap

| Version | Status | Work |
|---|---|---|
| v0.1 | ✅ Done | First 5 lessons, XP system, challenge validation |
| v0.2 | ✅ Done | 50-lesson curriculum, 7 units, difficulty badges, dynamic validators, collapsible sidebar |
| v0.3 | 🔄 Next | Database migration to Supabase (PostgreSQL + user accounts for public deployment) |
| v0.4 | Planned | AI Mentor — context-aware tutor per lesson |
| v0.5 | Planned | Voice Learning |
| v0.6 | Planned | Daily Challenges |
