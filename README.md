# TechTales Python Mentor 🐍

> **Go from zero to Python — one story at a time.**

An interactive Python learning platform that takes absolute beginners all the way to advanced topics through structured lessons, real coding challenges, instant sandboxed execution, and a gamified XP + badge system.

**[▶ Try it live](https://techtales-python-mentor.streamlit.app)**

---

<img width="2940" height="1912" alt="TechTales Python Mentor screenshot" src="https://github.com/user-attachments/assets/2606c31c-dd03-42bd-be06-b852a8167f3b" />

---

## Why TechTales?

Most Python courses throw a wall of text at you and hope something sticks.

TechTales does it differently:

- **Read** a short, plain-English lesson
- **See** a working code example
- **Write** real Python in a live editor — with instant output
- **Get specific feedback** on exactly what passed and what didn't
- **Earn XP and badges** as you progress

No setup. No installs. Just open the app and start coding.

---

## What You'll Learn

**69 lessons across 10 units** — from printing your first line to writing generators and decorators.

| Unit | Topics | Level |
|---|---|---|
| 🌍 Foundations | Write a Program → Variables → Data Types → Type Conversion → Arithmetic → F-Strings → Profile Card | Beginner |
| 🔠 Text | String Indexing → String Methods → Split & Join | Beginner |
| 🟰 Decisions | Comparison Operators → Boolean Logic → If/Else → Elif → Membership → Conditional Expressions → Grade Checker | Intermediate |
| 🔁 Loops | For Loops → Collections → Enumerate → While → Break & Continue → Nested Loops → Pattern Printer | Intermediate |
| 📋 Collections | Lists → List Methods → Slicing → Comprehensions → Tuples → Sets → Dictionaries → Nested Data → Inventory | Intermediate |
| ⚙️ Functions | Functions → Parameters → Defaults → Multiple Returns → None → Recursion → Mini Calculator | Advanced |
| 🏗️ OOP | Classes → `__init__` → Objects → Methods → Attributes → Inheritance → Class Design | Advanced |
| 🔧 Advanced Functions | Dict/Set Comprehensions → `*args/**kwargs` → Closures → Lambda → `map`/`filter` → `sorted` → `zip` → Decorators | Advanced |
| 🛡️ Error Handling | Exceptions → `try/except` → Multiple Exceptions → `finally` → Raising Exceptions → Safe Calculator | Advanced |
| 🔋 Generators & Iterators | `yield` → Generator Expressions → Iterator Protocol → Custom Range | Advanced |

---

## Features

### 🎓 Real Learning, Not Just Reading
Every lesson ends with a **coding challenge** you actually write and run. No multiple choice, no fill-in-the-blank — you write Python, it runs, and you get real feedback.

### ⚡ Instant Sandboxed Execution
Your code runs in an isolated subprocess with:
- **AST validation** before execution (blocks unsafe patterns)
- **2-second timeout** (no infinite loops)
- **Allowlisted builtins** only — safe for everyone

### 🎯 Smart Per-Requirement Feedback
Each challenge checks multiple requirements independently. You see exactly which ones passed (✓) and which failed (✗), with a specific improvement suggestion for each — not just "wrong, try again."

### 🏅 Milestone Exams & Badges
Complete a unit and unlock a **20-question exam**. Pass (≥ 70%) and earn a badge and 100 XP.

| Exam | Badge | Unlocks After |
|---|---|---|
| Foundations Exam | 🏅 Python Foundations | Unit 1 complete |
| Text & Decisions Exam | 🎯 Logic Master | Unit 3 complete |
| Loop Champion Exam | 🔁 Loop Champion | Unit 4 complete |
| Data Wrangler Exam | 📦 Data Wrangler | Unit 5 complete |
| Code Architect Exam | ⚙️ Code Architect | Unit 7 complete |
| Python Pro Exam | 🚀 Python Pro | Unit 10 complete |

### 🔐 Cloud Accounts & Progress Sync
Sign up free. Your XP, streaks, completed topics, and badges are saved to the cloud — pick up exactly where you left off from any device.

### 📈 XP, Levels & Streaks
- **20 XP** per topic on first pass
- **100 XP** per milestone exam passed
- **5 levels** with a progress bar
- **Daily streak** tracking with your personal best

### 🧭 Smart Sidebar Navigation
- 10 collapsible unit sections — only your active unit is open by default
- Visual completion count per unit
- Topic status at a glance: `○` not started · `◉` viewed · `✓` completed

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9 |
| UI | Streamlit ≥ 1.36 |
| Database | Supabase (PostgreSQL + Auth + Row-Level Security) |
| Code execution | Subprocess isolation + AST validation |
| Dev tooling | Built with [Claude Code](https://claude.ai/code) (Anthropic) |

---

## Running Locally

```bash
git clone https://github.com/Pankaj81-eng/TechTales-Python-Mentor
cd TechTales-Python-Mentor

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Add a `.env` file with your Supabase credentials:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

Then run:

```bash
streamlit run app.py
```

Opens at **http://localhost:8501**.

---

## Project Structure

```
app.py                  # Streamlit UI — routing, session state, rendering
techtales/
  content.py            # 69 Topic definitions (lesson, example, challenge, mentor card)
  validator.py          # AST-based challenge validators — one per topic
  execution.py          # Sandboxed subprocess runner
  quiz.py               # 6 milestone exams · 120 fill-in-the-blank questions
  db.py                 # Supabase reads and writes (submissions, XP, progress, exams)
  models.py             # Shared dataclasses (Topic, MentorCard, ValidationResult …)
```

---

## Roadmap

| Version | Status | Work |
|---|---|---|
| v0.1 | ✅ Shipped | Core platform — lessons, sandboxed execution, XP |
| v0.2 | ✅ Shipped | 69-lesson curriculum across 10 units, difficulty badges, full validators |
| v0.3 | ✅ Shipped | Supabase auth, cloud accounts, streak tracking, admin stats |
| v0.4 | ✅ Shipped | Milestone exams — 6 badges, 120 questions, 100 XP rewards |
| v0.5 | 🔄 Next | Quick lesson quiz (3 questions per lesson for instant engagement) |
| v0.6 | Planned | AI Mentor — context-aware tutor that explains your specific mistake |
| v0.7 | Planned | Daily Challenges |
| v0.8 | Planned | Voice Learning |

---

## The Story Behind It

I built TechTales while learning Python myself — the app is both the product *and* the process. Every feature was designed around one question: *what would have helped me when I was just starting out?*

The result is a platform I wish existed when I began: structured, encouraging, and honest about what you got wrong — without making you feel bad about it.

Built with ❤️ using [Claude Code](https://claude.ai/code).
