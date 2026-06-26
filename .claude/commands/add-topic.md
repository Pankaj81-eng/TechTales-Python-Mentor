# /add-topic — Add a new Python lesson to TechTales

Add a complete new topic/lesson to TechTales Python Mentor. This skill enforces
all four required touch points so nothing is accidentally missed.

## Usage

```
/add-topic <topic name>
```

Example: `/add-topic Tuples`

## Arguments

$ARGUMENTS — the display name of the new topic (e.g. "Tuples"). If not
provided, ask the user before proceeding.

---

## Steps — follow in order, do not skip any

### Step 1 — Gather information

If $ARGUMENTS is empty, ask the user for the topic name first.

Then derive or confirm:
- **Display name** — from $ARGUMENTS (e.g. "Tuples")
- **Topic key** — snake_case version (e.g. `tuples`)
- **Prerequisite** — which topic must be completed before this one unlocks. Ask
  the user. Look at `TOPIC_PREREQUISITES` in `app.py` for the existing chain.
- **Expected output** — does the challenge produce deterministic stdout? Ask the
  user. If yes, what should it print?

Do not proceed until all four are confirmed.

---

### Step 2 — Study the codebase for patterns

Read these files before writing anything:
- `techtales/content.py` — study the last two Topic entries for structure
- `techtales/validator.py` — study the last validator function added
- `app.py` lines containing `TOPIC_ICONS` and `TOPIC_PREREQUISITES`

The goal is consistency — new topics must match the style of existing ones.

---

### Step 3 — Design the topic (show the user before writing code)

Briefly outline:
1. **Lesson concept** — one paragraph, beginner language, explains the *why*
2. **Challenge task** — what will the learner write? Keep it achievable in
   10–15 lines
3. **Validation requirements** — 3 to 4 requirements, each a clear label string
   (e.g. `"Uses a tuple"`, `"Prints the first item"`)
4. **Expected output** — exact string if deterministic, None if open-ended

Show this outline to the user and get confirmation before writing any code.

---

### Step 4 — Add to techtales/content.py

Add a new `Topic(...)` to the `TOPICS` tuple:

- Place it in the correct position in the learning sequence
- Write the lesson text in plain English — target audience is absolute beginners
- Write the example code using only sandbox-safe constructs (no import,
  try/except, lambda, input, double-underscore attributes)
- Write the MentorCard:
  - `opening`: warm and encouraging, explains the *why* of the concept
  - `hints`: one `(label, hint_text)` pair per validator requirement — the
    label string must match the RequirementResult label **exactly**
  - `pass_message`: brief congratulation + teaser for the next concept
- Set `expected_output` to the exact stdout string if deterministic, else omit

---

### Step 5 — Add to techtales/validator.py

Add a `validate_<key>_challenge(submitted_code, execution_result)` function:

- Use `ast.parse` and `ast.walk` to check structural requirements
- Each requirement becomes one `RequirementResult(label, passed, suggestion)`
- The `label` must match **exactly** what you used in the MentorCard hints
- The `suggestion` must be a non-empty beginner-friendly string when
  `passed=False`
- Never raise — wrap the body in `try/except SyntaxError` and return a failed
  ValidationResult with a plain-English message
- Never check for constructs the sandbox blocks — no import, try/except, lambda,
  double-underscore attributes. Allowed builtins: print, range, int, str, float,
  bool, list, dict, set, tuple, len, abs, max, min, sum, round, enumerate

Wire the new function into `ChallengeValidator.validate()` — add an `elif`
branch for the new topic key.

---

### Step 6 — Update app.py

Two changes, both in `app.py`:

1. **TOPIC_ICONS** — add `"<key>": "<emoji>"` for the new topic
2. **TOPIC_PREREQUISITES** — add `"<key>": ("<prereq_key>", "<Prereq Title>")`
   using the prerequisite confirmed in Step 1

---

### Step 7 — Verify the full checklist

After all edits, confirm each item:

- [ ] `TOPICS` tuple in `content.py` contains the new Topic in the right position
- [ ] MentorCard hint labels match validator RequirementResult labels exactly
  (copy-paste check — one typo breaks the hint system)
- [ ] Validator function is wired into `ChallengeValidator.validate()`
- [ ] `TOPIC_ICONS` has the new key
- [ ] `TOPIC_PREREQUISITES` has the new key
- [ ] All code in example_code and starter_code is sandbox-safe

Report a summary: which file was changed, what was added, and the exact
position of the new topic in the learning sequence.
