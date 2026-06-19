from techtales.models import MentorCard, Topic


TOPICS: tuple[Topic, ...] = (
    # ───────────────────────── UNIT 1 — FOUNDATIONS ─────────────────────────
    Topic(
        key="write_a_program",
        title="Write a Program",
        summary="Write your very first complete Python program.",
        lesson="""
Every programmer's journey begins with the same two words: Hello World.

In 1972, a programmer named Brian Kernighan wrote the first Hello World example to show
how a program sends a message to the outside world. Since then, it has become the universal
first step for anyone learning to code — a tradition shared by millions of developers.

A program sends information out with `print()`. Whatever you put inside the quotes appears
on the screen. That single line is a complete, working program. One instruction. One result.
        """,
        example_code='''# A complete Python program
message = "Hello, World!"
print(message)''',
        challenge="""
Write a complete Python program that prints the message Hello, World! to the screen.

This is the traditional first program every programmer writes. One line is enough.
        """,
        starter_code='print("")',
        mentor=MentorCard(
            opening="This is the moment every programmer reaches. Hello World is a tradition dating back to 1972 — one line of code, and you and Python are officially talking.",
            pass_message="You did it. You have written and run a complete Python program. That is exactly how every great developer starts.",
            hints=(
                ("A print() statement is used", 'Use print() to send a message to the screen. Try: print("Hello, World!")'),
                ('Output includes "Hello"', 'Your program ran, but the output needs the word Hello. Try: print("Hello, World!")'),
                ('Output includes "World"', 'Almost! Your output has Hello but needs World too. Try: print("Hello, World!")'),
            ),
        ),
        expected_output="Hello, World!",
    ),
    Topic(
        key="variables",
        title="Variables",
        summary="Name a value so your program can remember it and use it later.",
        lesson="""
In Python, a variable is like a label on a useful tool in the workshop. You choose a name,
place a value inside it, and then reuse that name whenever the story needs the value again.

Python creates a variable when you assign a value with `=`. Good names are descriptive,
lowercase, and use underscores when they need more than one word.
        """,
        example_code='''hero_name = "Ari"
quest_points = 12

print(hero_name)
print(quest_points)''',
        challenge="""
Create two variables: one for a character name and one for the number of badges they have earned.
Print a short sentence that uses both variables.
        """,
        starter_code='''character_name = ""
badges = 0

print()''',
        mentor=MentorCard(
            opening="Variables are how programs remember things. Give your values good names and Python will hold onto them for as long as you need.",
            pass_message="Perfect. You've taught Python how to remember. Every program you ever write starts here.",
            hints=(
                ("String variable created", 'Assign text in quotes to a variable — for example: character_name = "Ari". The quotes tell Python this is text, not a command.'),
                ("Integer variable created", "Python is waiting for a whole number. Try: badges = 3 — no quotes needed. Quotes make text; no quotes make numbers."),
                ("Variables use meaningful names", "Names like x or var don't describe the value. Use something like character_name or badges_earned — future you will thank present you."),
                ("print() has output", "Your variables exist but Python hasn't shared them yet. Add print(character_name, badges) to show the world what you created."),
                ("Variables are used in output", "Your print() is there, but it's not using the variables you created. Pass them in: print(character_name, badges)."),
            ),
        ),
        expected_output="Ari 3",
    ),
    Topic(
        key="data_types",
        title="Data Types",
        summary="Understand the kinds of values Python can work with.",
        lesson="""
Values have types, and each type behaves a little differently. Text uses `str`, whole numbers
use `int`, decimal numbers use `float`, and true/false values use `bool`.

You can ask Python for any value's type with the `type()` function:

```python
print(type("Ari"))   # <class 'str'>
print(type(8.5))     # <class 'float'>
```

Knowing the type helps you choose the right operation. You can add numbers together, join strings
with other strings, and use booleans to make decisions.
        """,
        example_code='''artifact_name = "Loop Lantern"   # text
artifact_count = 3               # whole number
power_level = 8.5                # decimal number
is_unlocked = True               # True or False

print(type(artifact_name))
print(type(artifact_count))
print(type(power_level))
print(type(is_unlocked))''',
        challenge="""
Create one variable for each of these types: a string, an integer, a float, and a boolean.
Then use type() to print the type of each one.
        """,
        starter_code='''item_name = "Sword"
item_count = 5
item_power = 8.5
is_ready = True

# Print the type of each variable using type()
print()''',
        mentor=MentorCard(
            opening="Every value in Python has a type. The type() function tells you which one — type(8.5) reports <class 'float'>. Knowing the type tells you what you can do with a value.",
            pass_message="Excellent. You now speak Python's type system — and you can ask type() whenever you're unsure. That will save you from many confusing bugs later.",
            hints=(
                ("A text value (str) is created", 'Create a text variable using quotes: item_name = "Sword".'),
                ("A whole number (int) is created", "Create a whole-number variable without quotes: item_count = 5."),
                ("A decimal number (float) is created", "Create a decimal variable with a dot: item_power = 8.5."),
                ("A true/false value (bool) is created", "Create a boolean variable: is_ready = True (or False) — note the capital letter."),
                ("type() is used", "Ask Python for a value's type with type(): print(type(item_name))."),
                ("Output is printed", "Use print() with type() so the four types appear on screen."),
            ),
        ),
    ),
    Topic(
        key="type_conversion",
        title="Type Conversion",
        summary="Convert values between types so text becomes numbers and numbers become text.",
        lesson="""
Python keeps types separate. `29` is a number you can multiply. `"29"` is text you can search.
They look the same to humans — Python sees them differently.

Three conversion functions:

| Function | Converts to | Example |
|---|---|---|
| `int("29")` | Whole number | 29 |
| `float("3.14")` | Decimal number | 3.14 |
| `str(100)` | Text | "100" |

Mix types without converting and Python raises a `TypeError`. The fix is always explicit
conversion — tell Python exactly which type you want before using the value.
        """,
        example_code='''price_text = "15"
quantity_text = "4"

price = int(price_text)
quantity = int(quantity_text)
total = price * quantity

print(f"Total cost: {total}")''',
        challenge="""
You have a price and a quantity stored as text strings. Convert them to integers,
multiply them together, and print the total using an f-string.
        """,
        starter_code='''price_text = "25"
quantity_text = "4"

total = price_text * quantity_text
print(f"Total: {total}")''',
        mentor=MentorCard(
            opening="Python keeps text and numbers separate. int(), float(), and str() are the bridges — use them whenever you need to switch a value from one type to another.",
            pass_message="Type conversion is one of those quiet skills that prevents many frustrating bugs. You will use it every time you work with user input or external data.",
            hints=(
                ("A type conversion function is used", "Use int(), float(), or str() to convert a value — e.g. price = int(price_text) or label = str(42). Any direction counts."),
                ("Arithmetic is performed", "Once you have a number, do some maths: total = price * quantity. Python can only multiply numbers, not text strings."),
                ("Output is printed", 'Use print() or an f-string to show the result: print(f"Total: {total}")'),
            ),
        ),
    ),
    Topic(
        key="arithmetic_operators",
        title="Arithmetic Operators",
        summary="Do maths with Python: add, subtract, multiply, divide, and more.",
        lesson="""
Python is a powerful calculator. These are the arithmetic operators you will use most:

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Add | `8 + 3` | 11 |
| `-` | Subtract | `8 - 3` | 5 |
| `*` | Multiply | `8 * 3` | 24 |
| `/` | Divide | `8 / 3` | 2.666… |
| `//` | Floor divide (drop the remainder) | `8 // 3` | 2 |
| `%` | Modulo (the remainder) | `8 % 3` | 2 |
| `**` | Power | `2 ** 3` | 8 |

`/` always gives a decimal. `//` and `%` are a pair: one gives the whole part, the other the
leftover. They are surprisingly useful — `%` tells you if a number is even (`n % 2 == 0`).
        """,
        example_code='''a = 8
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a % b)
print(a ** b)''',
        challenge="""
Create two number variables, `a` and `b`. Print their sum, their difference, and their product —
using at least two different arithmetic operators.
        """,
        starter_code='''a = 10
b = 4

print(a + b)
print()''',
        mentor=MentorCard(
            opening="Python is a calculator that never makes arithmetic mistakes. Master the seven operators here and you can express almost any everyday calculation.",
            pass_message="You can now make Python do maths. Every price total, score tally, and progress bar you ever build rests on exactly these operators.",
            hints=(
                ("A calculation is performed", "Combine two numbers with an operator, for example: a + b or a * b."),
                ("At least two different operators are used", "Use two different operators — for example a + b on one line and a * b on another."),
                ("Output is printed", "Wrap each calculation in print() so the results appear on screen."),
            ),
        ),
    ),
    Topic(
        key="f_strings",
        title="F-Strings",
        summary="Embed variable values directly inside a string using {}.",
        lesson="""
An f-string is a string with an `f` in front of the opening quote. Anything you put inside `{}`
gets replaced with the actual value of that variable when the program runs.

This is the cleanest way to build a sentence that mixes fixed text with variable values — no
joining with `+`, no converting numbers to strings manually.
        """,
        example_code='''hero_name = "Ari"
level = 5

print(f"{hero_name} has reached level {level}!")''',
        challenge="""
Create two variables — a learner's name and their XP score. Use a single f-string to print one
sentence that includes both values.
        """,
        starter_code='''learner_name = ""
xp = 0

print(f"")''',
        mentor=MentorCard(
            opening='Before f-strings, programmers joined text and numbers with +. It was awkward. F-strings make it elegant — write f"...{variable}..." and Python fills in the value for you.',
            pass_message="Clean, readable, modern. F-strings are used in real Python code every day — you just learned something professionals reach for constantly.",
            hints=(
                ("An f-string is used", 'Start a string with the letter f before the quote: f"Hello {name}!". The f unlocks the {} magic.'),
                ("f-string contains a placeholder", 'The f is there, but Python needs curly braces {} to know where to put the variable. Try: f"Hi {learner_name}!"'),
                ("f-string embeds a variable", 'Put any variable inside {}: learner_name = "Ari" then f"Hello {learner_name}!". The variable can be any type — text, number, whatever you have.'),
                ("f-string embeds two values", 'Embed two things in your f-string — for example a name and a score: f"{learner_name} has {xp} XP". Each goes in its own {}.'),
                ("Output is printed", "Your f-string exists, but Python hasn't printed it yet. Wrap it in print() so the sentence appears on screen."),
            ),
        ),
        expected_output="Ari has 100 XP",
    ),
    Topic(
        key="exercise_profile_card",
        title="Exercise: Profile Card",
        summary="Your first project — combine variables, maths, and f-strings into one program.",
        lesson="""
Time to put the last few lessons together. You've learned variables, data types, type
conversion, arithmetic, and f-strings. A real program uses them all at once.

In this exercise you'll build a small **profile card**: store some facts in variables, calculate
one value from them, and print a neat summary sentence with an f-string.

This is what programming actually feels like — not one idea in isolation, but several working
together toward a result.
        """,
        example_code='''name = "Ari"
birth_year = 2008
current_year = 2026
age = current_year - birth_year

print(f"{name} is {age} years old.")''',
        challenge="""
Build a profile card program:
1. Create a variable for a name and at least one number (such as a birth year or a score).
2. Calculate a new value from your numbers (for example, an age, or a doubled score).
3. Print a friendly summary sentence using an f-string that includes your calculated value.
        """,
        starter_code='''name = "Ari"
birth_year = 2008
current_year = 2026

age = 0

print(f"")''',
        mentor=MentorCard(
            opening="This is your first real project — small, but complete. Bring together a variable, a calculation, and an f-string. Take it one line at a time.",
            pass_message="You just combined four skills into one working program. That is exactly how all software is built — small pieces, working together.",
            hints=(
                ("A variable is created", 'Start by storing a fact in a variable, such as name = "Ari" or birth_year = 2008.'),
                ("A calculation is performed", "Calculate a new value from your numbers, for example: age = current_year - birth_year."),
                ("An f-string is used", 'Build your summary with an f-string: f"{name} is {age} years old." — the {} insert your values.'),
                ("Output is printed", "Wrap your f-string in print() so the profile card appears on screen."),
            ),
        ),
    ),
    # ───────────────────────── UNIT 2 — WORKING WITH TEXT ─────────────────────────
    Topic(
        key="string_indexing",
        title="String Indexing & Slicing",
        summary="Reach into a string to grab a single character or a section of it.",
        lesson="""
A string is a sequence of characters, each at a numbered **position** called an index —
starting from 0, not 1.

```python
word = "PYTHON"
#       012345
print(word[0])   # P  — the first character
print(word[-1])  # N  — the last character (negative counts from the end)
```

A **slice** grabs a section using `[start:stop]`. The start is included, the stop is not:

```python
print(word[0:3])  # PYT — characters 0, 1, 2
print(word[2:])   # THON — from index 2 to the end
```

Slicing is everywhere: trimming text, reading the first few letters, reversing with `word[::-1]`.
        """,
        example_code='''word = "PYTHON"

print(word[0])
print(word[-1])
print(word[0:3])
print(word[2:])''',
        challenge="""
Create a text variable holding a word. Print one single character using an index (like word[0]),
and print a section of the word using a slice (like word[1:4]).
        """,
        starter_code='''word = "MENTOR"

print(word[0])
print()''',
        mentor=MentorCard(
            opening="A string is really a row of numbered boxes, each holding one character, counting from 0. Once you can point at any position, you can pull out exactly the piece you need.",
            pass_message="Indexing and slicing are core skills — you'll reach for them constantly when cleaning and reading text.",
            hints=(
                ("A text variable is created", 'Create a string first: word = "MENTOR".'),
                ("A character is accessed by index", "Grab a single character by position: word[0] gives the first letter, word[-1] the last."),
                ("A slice is used", "Take a section with a colon: word[1:4] gives characters 1, 2 and 3."),
                ("Output is printed", "Wrap your results in print() to see the character and the slice."),
            ),
        ),
        expected_output="M\nENT",
    ),
    Topic(
        key="string_methods",
        title="String Methods",
        summary="Transform and analyse text using Python's built-in string tools.",
        lesson="""
Strings have built-in tools called **methods** — ready to use without any imports. Call them with
a dot after the variable name.

| Method | What it does |
|---|---|
| `.upper()` | Convert to UPPERCASE |
| `.lower()` | Convert to lowercase |
| `.replace("a", "b")` | Swap every "a" for "b" |
| `.strip()` | Remove surrounding whitespace |
| `.title()` | Capitalise Each Word |

Methods don't change the original string — they return a new one. You can chain them:
`text.strip().lower()` strips first, then lowercases.
        """,
        example_code='''title = "  the python mentor  "

print(title.strip())
print(title.strip().title())
print(title.strip().upper())
print(len(title.strip()))''',
        challenge="""
Create a text variable. Apply at least two different string methods and print the results.
Try .upper(), .lower(), .replace(), or .strip().
        """,
        starter_code='''message = "hello, world"

print(message.upper())
print()''',
        mentor=MentorCard(
            opening="Python's strings come with built-in tools. You don't need to import anything — methods like .upper() and .replace() are always available on any string.",
            pass_message="String manipulation is something you will do in every real program. You now have a reliable toolkit for it.",
            hints=(
                ("At least one string method is used", "Call a method on your string: message.upper() converts all letters to uppercase. The dot connects the method to the string."),
                ("At least two string methods are used", 'Try a second method: message.lower() or message.replace("hello", "hi").'),
                ("Output is printed", "Wrap your transformed text in print() to see the result on screen."),
            ),
        ),
    ),
    Topic(
        key="string_split_join",
        title="Split & Join",
        summary="Break a string into a list of words, and join a list back into a string.",
        lesson="""
Two string methods work as opposites:

`.split()` breaks a string into a **list** of pieces. By default it splits on spaces:

```python
sentence = "learn python step by step"
words = sentence.split()      # ['learn', 'python', 'step', 'by', 'step']
```

`.join()` does the reverse — it glues a list of strings back together, using whatever string you
call it on as the separator:

```python
words = ["a", "b", "c"]
print("-".join(words))        # a-b-c
```

Together they let you take text apart, change the pieces, and put it back together — the heart of
most text processing.
        """,
        example_code='''sentence = "learn python step by step"

words = sentence.split()
print(words)
print(len(words))

joined = "-".join(words)
print(joined)''',
        challenge="""
Create a sentence as a string. Use .split() to break it into a list of words and print the list.
Then use .join() to glue the words back together with a separator and print the result.
        """,
        starter_code='''sentence = "python is fun to learn"

words = sentence.split()
print(words)

print()''',
        mentor=MentorCard(
            opening="split() and join() are mirror images: one takes text apart into a list, the other puts a list back into text. Learn them as a pair.",
            pass_message="You can now move freely between text and lists. That round-trip is the foundation of almost all text processing.",
            hints=(
                ("A text variable is created", 'Create a sentence first: sentence = "python is fun to learn".'),
                (".split() is used", "Break the sentence into words: words = sentence.split() gives you a list."),
                (".join() is used", 'Glue the words back together with a separator: "-".join(words) or " ".join(words).'),
                ("Output is printed", "Use print() to show both the split list and the joined string."),
            ),
        ),
    ),
    # ───────────────────────── UNIT 3 — MAKING DECISIONS ─────────────────────────
    Topic(
        key="comparison_operators",
        title="Comparison Operators",
        summary="Ask yes/no questions about values — Python answers True or False.",
        lesson="""
A comparison asks a question and Python answers with a boolean — `True` or `False`.

| Operator | Question | Example | Result |
|---|---|---|---|
| `==` | Equal? | `5 == 5` | True |
| `!=` | Not equal? | `5 != 3` | True |
| `>` | Greater than? | `5 > 3` | True |
| `<` | Less than? | `5 < 3` | False |
| `>=` | Greater or equal? | `5 >= 5` | True |
| `<=` | Less or equal? | `3 <= 5` | True |

Note the double `==` for "equal." A single `=` *assigns* a value; double `==` *compares*. Mixing
them up is one of the most common beginner bugs.
        """,
        example_code='''score = 7

print(score == 10)
print(score != 10)
print(score > 5)
print(score <= 7)''',
        challenge="""
Create a number variable. Use at least two different comparison operators to ask questions about it,
and print the True/False results.
        """,
        starter_code='''score = 8

print(score > 5)
print()''',
        mentor=MentorCard(
            opening="Comparisons are how a program asks questions. Every decision your code ever makes starts with a comparison that answers True or False.",
            pass_message="You now know how Python answers yes/no questions. Next, you'll use these answers to make your program choose what to do.",
            hints=(
                ("A comparison is made", "Compare two values with an operator like > or ==, for example: score > 5."),
                ("At least two comparisons are used", "Use two different comparisons — for example score > 5 on one line and score == 10 on another."),
                ("Output is printed", "Wrap each comparison in print() to see its True or False answer."),
            ),
        ),
    ),
    Topic(
        key="boolean_logic",
        title="Boolean Logic",
        summary="Combine yes/no answers with and, or, and not.",
        lesson="""
Booleans are the values `True` and `False`. Three keywords combine them:

| Operator | True when… | Example |
|---|---|---|
| `and` | **both** sides are true | `is_member and has_paid` |
| `or` | **either** side is true | `is_admin or is_owner` |
| `not` | flips true ↔ false | `not is_banned` |

```python
age = 20
has_ticket = True
print(age >= 18 and has_ticket)   # True — both conditions hold
```

These are the building blocks of real decisions: "allowed in **if** over 18 **and** has a ticket."
        """,
        example_code='''age = 20
has_ticket = True

print(age >= 18 and has_ticket)
print(age < 13 or has_ticket)
print(not has_ticket)''',
        challenge="""
Create two variables. Combine conditions about them using at least two of: and, or, not.
Print the True/False results.
        """,
        starter_code='''age = 20
has_ticket = True

print(age >= 18 and has_ticket)
print()''',
        mentor=MentorCard(
            opening="Real decisions rarely depend on one thing. and, or, and not let you combine several conditions into a single yes/no answer — just like everyday reasoning.",
            pass_message="You can now express complex conditions in plain logic. This is the language every if-statement speaks.",
            hints=(
                ("A boolean operator is used", "Combine two conditions with and, or, or not — for example: age >= 18 and has_ticket."),
                ("At least two boolean operators are used", "Use two of them — for example an and on one line and a not on another."),
                ("Output is printed", "Wrap each combined condition in print() to see its True or False result."),
            ),
        ),
    ),
    Topic(
        key="if_else",
        title="If/Else",
        summary="Teach a program to choose a path based on a condition.",
        lesson="""
An `if` statement lets Python ask a question and run code only when the answer is true. An `else`
block gives Python a backup path when the condition is false.

Indentation matters: the indented lines belong to the branch above them.
        """,
        example_code='''energy = 7

if energy >= 5:
    print("The mentor opens the green gate.")
else:
    print("The mentor suggests a rest before continuing.")''',
        challenge="""
Create a variable named `score`. If the score is at least 10, print a success message. Otherwise,
print a message that encourages the learner to try again.
        """,
        starter_code='''score = 0

if score >= 10:
    print()
else:
    print()''',
        mentor=MentorCard(
            opening="Every interesting program makes decisions. if is how Python asks a question. else is the backup plan when the answer is no.",
            pass_message="Your program now makes choices. That is the beginning of real logic — and real programming.",
            hints=(
                ("Submitted Python code", "Make sure you have both an if branch and an else branch. Remember: the messages under each branch must be indented by 4 spaces."),
            ),
        ),
    ),
    Topic(
        key="elif",
        title="Elif",
        summary="Handle multiple conditions in sequence with elif chains.",
        lesson="""
You already know `if` checks one condition and `else` is the backup. But what if you need three
paths? Four? `elif` is Python's way of chaining conditions cleanly.

Python reads the chain top-to-bottom and takes the first branch that matches. Once a branch runs,
the rest are skipped — even if later conditions would also be true.

```
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "F"
```

Think of `elif` as "or else if" — Python just says it with fewer letters.
        """,
        example_code='''energy = 65

if energy >= 80:
    print("Full power — ready for anything.")
elif energy >= 50:
    print("Good energy — keep moving.")
elif energy >= 20:
    print("Low energy — rest soon.")
else:
    print("Exhausted — rest now.")''',
        challenge="""
Create a variable named `score`. Use if, elif, and else to print a grade:
A for 90 and above, B for 80 and above, or F for anything below.
        """,
        starter_code='''score = 85

if score >= 90:
    print()
elif score >= 80:
    print()
else:
    print()''',
        mentor=MentorCard(
            opening="If/else gives you two paths. elif gives you as many as you need — and Python reads them almost like English: if this, or else if that, or else something else.",
            pass_message="Your program now navigates multiple conditions cleanly. That is the core of decision-making in any real program.",
            hints=(
                ("An if statement is used", "Start with if score >= 90: and indent the print() below it by 4 spaces."),
                ("An elif branch is used", "After your if block, add elif score >= 80: at the same indent level. Python checks this only when the first condition failed."),
                ("An else branch is used", "Add else: at the end as the catch-all for any score that didn't match the conditions above."),
                ("Program produces output", "Each branch (if, elif, else) needs a print() statement inside it, indented 4 spaces."),
            ),
        ),
    ),
    Topic(
        key="membership_operators",
        title="Membership: in / not in",
        summary="Check whether a value is inside a string, list, or other collection.",
        lesson="""
The `in` operator asks: "is this value somewhere inside that collection?" It answers `True` or
`False`.

```python
print("a" in "cat")          # True  — the letter a is in "cat"
print("dog" in ["cat", "dog"])  # True  — dog is in the list
print(5 in [1, 2, 3])        # False — 5 is not there
```

`not in` is the opposite — it's True when the value is **absent**. Membership tests are perfect
inside an `if`: "if the answer **is in** the list of valid answers…".
        """,
        example_code='''vowels = "aeiou"
letter = "e"

print(letter in vowels)
print("z" in vowels)
print("z" not in vowels)''',
        challenge="""
Create a string or a list. Use the `in` (or `not in`) operator to check whether a value is inside
it, and print the True/False result.
        """,
        starter_code='''vowels = "aeiou"
letter = "e"

print(letter in vowels)
print()''',
        mentor=MentorCard(
            opening="in is one of Python's most readable operators — it asks a question almost in plain English: is this value in that collection?",
            pass_message="Membership tests make your conditions read like sentences. You'll use in constantly with lists, strings, and dictionaries.",
            hints=(
                ("A membership test is used", 'Use in to check for a value: "e" in vowels, or use not in for the opposite.'),
                ("Output is printed", "Wrap your membership test in print() to see the True or False answer."),
            ),
        ),
    ),
    Topic(
        key="conditional_expression",
        title="Conditional Expression",
        summary="Choose between two values on a single line with a one-line if/else.",
        lesson="""
Sometimes a full `if`/`else` is overkill — you just want to pick one of two values. Python's
**conditional expression** (also called a ternary) does it in one line:

```python
value_if_true if condition else value_if_false
```

Read it left to right like a sentence:

```python
age = 20
label = "adult" if age >= 18 else "minor"
print(label)   # adult
```

It's the same logic as if/else, compressed into one expression you can assign or print directly.
Use it for short, simple choices — reach for full if/else when the logic grows.
        """,
        example_code='''score = 72

result = "pass" if score >= 50 else "fail"
print(result)

energy = 30
status = "ready" if energy > 20 else "tired"
print(status)''',
        challenge="""
Create a number variable. Use a one-line conditional expression (value if condition else value)
to choose between two words based on it, and print the chosen word.
        """,
        starter_code='''score = 72

result = "pass" if score >= 50 else "fail"
print()''',
        mentor=MentorCard(
            opening="A conditional expression is if/else folded onto one line. It reads almost like English: this value if the condition holds, else that value.",
            pass_message="You've learned a clean shortcut that experienced Python developers use all the time for simple either/or choices.",
            hints=(
                ("A conditional expression is used", 'Use the one-line form: result = "pass" if score >= 50 else "fail".'),
                ("Output is printed", "Print the chosen value: print(result), or print the expression directly."),
            ),
        ),
    ),
    Topic(
        key="exercise_grade_checker",
        title="Exercise: Grade Checker",
        summary="Build a program that turns a score into a grade — your decisions, working together.",
        lesson="""
You've now learned comparisons, boolean logic, if/elif/else, and conditional expressions. This
exercise brings the decision-making skills together.

You'll build a **grade checker**: take a score, compare it against thresholds, and print a grade.
This is the same logic that powers quiz apps, eligibility checks, and pricing tiers everywhere.

Focus on getting the branches in the right order — Python takes the first one that matches.
        """,
        example_code='''score = 84

if score >= 90:
    print("Grade: A — outstanding!")
elif score >= 75:
    print("Grade: B — well done.")
elif score >= 50:
    print("Grade: C — keep going.")
else:
    print("Grade: F — try again.")''',
        challenge="""
Build a grade checker:
1. Create a `score` variable.
2. Use if, elif, and else with comparison operators to choose a grade for the score.
3. Print a message that includes the grade.
        """,
        starter_code='''score = 84

if score >= 90:
    print()
elif score >= 75:
    print()
else:
    print()''',
        mentor=MentorCard(
            opening="Your second project. Combine comparisons with an if/elif/else chain to sort a score into a grade. Order matters — put the highest threshold first.",
            pass_message="You built a real decision engine. The same pattern — compare, branch, respond — runs underneath most of the software you use every day.",
            hints=(
                ("A comparison is made", "Compare the score against a threshold, for example: score >= 90."),
                ("An elif branch is used", "Add at least one elif for a middle grade: elif score >= 75:."),
                ("An else branch is used", "Finish with else: to catch every score that didn't match above."),
                ("Output is printed", "Each branch needs a print() with the grade message inside it."),
            ),
        ),
    ),
    # ───────────────────────── UNIT 4 — REPETITION (LOOPS) ─────────────────────────
    Topic(
        key="loops",
        title="For Loops & range()",
        summary="Repeat an action without writing the same line again and again.",
        lesson="""
Loops help programs repeat work. A `for` loop is great when you know the range of numbers you
want to move through.

`range(1, 4)` produces 1, 2, 3 — it stops *before* the second number. The loop variable changes
each time through the loop, letting your code respond to the current number.
        """,
        example_code='''for chapter in range(1, 4):
    print(f"Reading chapter {chapter}")''',
        challenge="""
Use a loop to print three training steps for a new Python mentor. Include the step number in each
message.
        """,
        starter_code='''for step in range(1, 4):
    print()''',
        mentor=MentorCard(
            opening="Loops are one of programming's superpowers. Instead of writing the same line three times, you write it once and tell Python to repeat it.",
            pass_message="A loop you understand is worth a hundred lines you'd otherwise copy and paste. Well done.",
            hints=(
                ("A loop is used", "A for loop moves through a sequence for you. Try: for step in range(1, 4): — that gives step = 1, then 2, then 3."),
                ("print() is inside the loop", "Your loop is there, but print() needs to be indented inside it. Indent print() by 4 spaces so it runs once for each step."),
                ("Output includes three steps", "Use range(1, 4) — that's 1, 2, 3. Python stops before the second number, so range(1, 4) gives exactly three steps."),
                ("Output changes each iteration", 'Your output shows the same message every step. Use the loop variable in print() — for example print(f"Training step {step}") — so each line is different.'),
            ),
        ),
        expected_output="Training step 1\nTraining step 2\nTraining step 3",
    ),
    Topic(
        key="for_each",
        title="Looping Over Collections",
        summary="Walk through the items of a list or string one at a time.",
        lesson="""
`range()` is great for numbers, but a `for` loop can walk through **any** collection directly —
no index numbers needed. Python hands you each item in turn.

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

It works on strings too — you get one character at a time:

```python
for letter in "hi":
    print(letter)
```

This is the most common loop in real Python. When you have a collection, loop over the items
directly rather than counting positions.
        """,
        example_code='''skills = ["Variables", "Loops", "Functions"]

for skill in skills:
    print(f"Learning: {skill}")''',
        challenge="""
Create a list of at least three items. Use a for loop to go through the list directly (not with
range) and print each item.
        """,
        starter_code='''colors = ["red", "green", "blue"]

for color in colors:
    print()''',
        mentor=MentorCard(
            opening="When you have a list, you rarely need index numbers — just loop over the items directly. This is the most natural, most common loop in Python.",
            pass_message="Looping over a collection directly is the everyday Python pattern. You'll write this loop more than any other.",
            hints=(
                ("A for loop is used", "Start a loop: for color in colors: — Python will hand you each item in turn."),
                ("The loop goes through a collection directly", "Loop over your list itself (for item in my_list:), not over range() — let Python give you each item."),
                ("Output is printed", "Indent a print() inside the loop so each item appears on its own line."),
            ),
        ),
    ),
    Topic(
        key="enumerate_loop",
        title="Looping with enumerate()",
        summary="Loop through a collection and get both the position and the item.",
        lesson="""
Sometimes you want the item **and** its position number. `enumerate()` gives you both at once:

```python
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(index, fruit)
# 0 apple
# 1 banana
# 2 cherry
```

The loop variable becomes two names: the index first, then the item. By default counting starts
at 0 — exactly like list indexes. This is far cleaner than manually keeping a counter variable.
        """,
        example_code='''steps = ["Warm up", "Practice", "Review"]

for number, step in enumerate(steps):
    print(f"{number}: {step}")''',
        challenge="""
Create a list of at least three items. Use a for loop with enumerate() to print each item
together with its position number.
        """,
        starter_code='''steps = ["Warm up", "Practice", "Review"]

for number, step in enumerate(steps):
    print()''',
        mentor=MentorCard(
            opening="enumerate() answers a common need: looping over items while also knowing where you are. It hands you the position and the item together.",
            pass_message="enumerate() is the clean way to number a list while looping. You'll prefer it over manual counters from now on.",
            hints=(
                ("A for loop is used", "Begin a loop over your list with for ... in ...:."),
                ("enumerate() is used", "Wrap the list in enumerate() and catch two names: for number, step in enumerate(steps):."),
                ("Output is printed", "Indent a print() inside the loop to show each position and item, for example print(number, step)."),
            ),
        ),
    ),
    Topic(
        key="while_loops",
        title="While Loops",
        summary="Repeat code for as long as a condition stays true.",
        lesson="""
A `for` loop repeats for each item in a sequence. A `while` loop repeats **as long as a condition
is true** — you decide when it stops.

```python
count = 1
while count <= 5:
    print(count)
    count = count + 1
```

Three parts to every while loop:
1. **A starting value** — set before the loop begins
2. **A condition** — checked before each run
3. **An update** — changes the value so the loop eventually ends

Forget the update and the loop runs forever.
        """,
        example_code='''lives = 3

while lives > 0:
    print(f"Lives remaining: {lives}")
    lives = lives - 1

print("Game over.")''',
        challenge="""
Use a while loop to count from 1 to 5 and print each number on its own line.
        """,
        starter_code='''count = 1

while count <= 5:
    print()
    count = count + 1''',
        mentor=MentorCard(
            opening="A for loop runs a set number of times. A while loop runs as long as a condition is true — which could be until a counter reaches its target, or until a player runs out of lives.",
            pass_message="You have mastered both loop types. for is for a known sequence, while is for an unknown duration. Together they handle every repetition pattern.",
            hints=(
                ("A while loop is used", "Start with while count <= 5: — Python keeps running the indented block until that condition becomes False."),
                ("print() is inside the while loop", "Indent your print() by 4 spaces inside the while loop so it runs on each iteration."),
                ("The loop variable is updated", "count = count + 1 is already there — make sure it stays inside the loop so the counter moves forward each time."),
                ("Output has multiple lines", "Change print() to print(count) so each iteration prints the current value of count."),
            ),
        ),
        expected_output="1\n2\n3\n4\n5",
    ),
    Topic(
        key="break_continue",
        title="Break & Continue",
        summary="Steer a loop: stop early, or skip an item and keep going.",
        lesson="""
Two keywords give you fine control inside any loop:

`break` — **stop the loop immediately**, even if there are items left:

```python
for n in range(1, 10):
    if n == 4:
        break       # leaves the loop the moment n is 4
    print(n)        # prints 1, 2, 3
```

`continue` — **skip the rest of this turn** and jump to the next item:

```python
for n in range(1, 6):
    if n == 3:
        continue    # skips printing 3
    print(n)        # prints 1, 2, 4, 5
```

Use `break` to stop searching once you've found what you need; use `continue` to ignore items you
don't care about.
        """,
        example_code='''for number in range(1, 10):
    if number == 5:
        break
    print(number)''',
        challenge="""
Write a loop over a range of numbers. Use break to stop the loop early, or continue to skip
certain numbers, and print the numbers that remain.
        """,
        starter_code='''for number in range(1, 10):
    if number == 5:
        break
    print(number)''',
        mentor=MentorCard(
            opening="Loops don't have to run to the end. break stops them on the spot; continue skips a single turn. Together they give you precise control over repetition.",
            pass_message="You can now steer a loop, not just start one. break and continue show up constantly in search and filtering logic.",
            hints=(
                ("A loop is used", "Start a for or while loop over some numbers."),
                ("break or continue is used", "Inside an if, use break to stop the loop early, or continue to skip to the next item."),
                ("Output is printed", "Print the numbers inside the loop so you can see the effect of break or continue."),
            ),
        ),
    ),
    Topic(
        key="nested_loops",
        title="Nested Loops",
        summary="Put one loop inside another to work through grids and combinations.",
        lesson="""
A loop can live **inside** another loop. For every single turn of the outer loop, the inner loop
runs all the way through.

```python
for row in range(1, 4):
    for col in range(1, 4):
        print(row, col)
```

That prints 9 lines — 3 outer turns × 3 inner turns. Nested loops are how you handle anything
grid-shaped: tables, game boards, rows and columns, or every pairing of two lists.

Watch your indentation — the inner loop's body is indented twice (8 spaces).
        """,
        example_code='''for row in range(1, 4):
    for star in range(0, row):
        print("*", end="")
    print()''',
        challenge="""
Write a loop inside another loop. Use the two loops together to print several lines of output
(for example, a small grid or a pattern).
        """,
        starter_code='''for row in range(1, 4):
    for col in range(1, 4):
        print()''',
        mentor=MentorCard(
            opening="Some problems are grid-shaped — rows and columns, every pairing of two lists. A loop inside a loop handles them naturally.",
            pass_message="Nested loops unlock grids, tables, and combinations. They look intimidating at first, but you've just shown they're only loops within loops.",
            hints=(
                ("An outer loop is used", "Start with one loop, for example for row in range(1, 4):."),
                ("A loop is nested inside another loop", "Indent a second loop inside the first: for col in range(1, 4): — it runs fully on every turn of the outer loop."),
                ("Output is printed", "Print something inside the inner loop so each combination appears."),
            ),
        ),
    ),
    Topic(
        key="exercise_pattern_printer",
        title="Exercise: Pattern Printer",
        summary="Use loops to draw a pattern — repetition with a purpose.",
        lesson="""
You've now learned for loops, looping over collections, enumerate, while loops, break/continue,
and nested loops. This exercise puts repetition to work.

You'll build a **pattern printer** — a small program that uses a loop (or loops) to print several
lines of output, like a number list, a multiplication row, or a triangle of stars.

There's no single right answer here. The goal is to make a loop produce a multi-line result you
designed.
        """,
        example_code='''for row in range(1, 6):
    print("*" * row)
# *
# **
# ***
# ****
# *****''',
        challenge="""
Build a pattern printer:
1. Use a loop (you may nest one loop inside another).
2. Produce at least three lines of output.
3. Make each line depend on the loop — a growing row of stars, a countdown, or a times table.
        """,
        starter_code='''for row in range(1, 6):
    print("*" * row)''',
        mentor=MentorCard(
            opening="Your loops project. Make a loop produce a multi-line pattern of your choosing — stars, numbers, a times table. The shape is up to you.",
            pass_message="You turned repetition into a designed result. That same skill renders tables, charts, and game boards in real programs.",
            hints=(
                ("A loop is used", "Start with a for or while loop to drive the repetition."),
                ("Each line depends on the loop", 'Make each line change — use the loop variable in your print (like "*" * row), or nest a loop or an if inside.'),
                ("Output has multiple lines", "Make sure your program prints at least three separate lines."),
            ),
        ),
    ),
    # ───────────────────────── UNIT 5 — COLLECTIONS ─────────────────────────
    Topic(
        key="lists",
        title="Lists",
        summary="Store multiple values together in a single ordered collection.",
        lesson="""
A variable holds one value. A list holds many — in order, one after another.

Create a list with square brackets and commas between items. Each item has a numbered position
called an **index** — starting from 0, not 1. Python always counts from zero.

```python
items = ["Map", "Torch", "Key"]
print(items[0])   # Map — the first item
print(items[2])   # Key — the third item
```

`len()` tells you how many items are in the list. `.append()` adds a new item to the end.
        """,
        example_code='''skills = ["Variables", "Loops", "Functions"]

print(skills)
print(len(skills))
print(skills[0])

skills.append("Lists")
print(skills)''',
        challenge="""
Create a list called `quest_items` with at least 3 items. Print the whole list, print its
length using len(), and print one item by its index number.
        """,
        starter_code='''quest_items = []

print(quest_items)
print(len(quest_items))
print(quest_items[0])''',
        mentor=MentorCard(
            opening="A variable holds one value. A list holds many — in order, with each item at a numbered position starting from 0.",
            pass_message="Lists are the workhorse of Python. Almost every real program uses them — you will see them everywhere from now on.",
            hints=(
                ("A list is created", 'Create a list using square brackets: quest_items = ["Map", "Torch", "Key"]'),
                ("The list has at least 3 items", "Add at least 3 items inside the brackets, separated by commas."),
                ("len() is used", "Call len(quest_items) to find out how many items the list contains."),
                ("An item is accessed by index", "Access an item by its position: quest_items[0] gives the first item, quest_items[1] the second."),
                ("Output is printed", "Wrap your results in print() to see the list, its length, and an item."),
            ),
        ),
    ),
    Topic(
        key="list_methods",
        title="List Methods",
        summary="Add, remove, and reorder items using lists' built-in tools.",
        lesson="""
Lists can change after you create them. Their built-in methods do the work:

| Method | What it does |
|---|---|
| `.append(x)` | Add x to the end |
| `.insert(i, x)` | Insert x at position i |
| `.remove(x)` | Remove the first x |
| `.pop()` | Remove and return the last item |
| `.sort()` | Sort the list in place |
| `.reverse()` | Reverse the order in place |

```python
scores = [30, 10, 20]
scores.append(40)   # [30, 10, 20, 40]
scores.sort()       # [10, 20, 30, 40]
```

Note: `.sort()` and `.reverse()` change the list itself and return nothing — don't write
`scores = scores.sort()`.
        """,
        example_code='''items = ["Torch", "Map"]

items.append("Key")
print(items)

items.sort()
print(items)

items.pop()
print(items)''',
        challenge="""
Create a list. Use at least one list method (like .append(), .remove(), .sort(), or .pop())
to change it, then print the updated list.
        """,
        starter_code='''items = ["Torch", "Map"]

items.append("Key")
print()''',
        mentor=MentorCard(
            opening="Lists aren't frozen — they grow, shrink, and reorder. Their methods are the tools that reshape them as your program runs.",
            pass_message="You can now reshape a list at runtime. Adding, removing, and sorting items is something nearly every program does.",
            hints=(
                ("A list is created", 'Create a list first: items = ["Torch", "Map"].'),
                ("A list method is used", "Call a method on the list: items.append(\"Key\"), items.sort(), or items.pop()."),
                ("Output is printed", "Print the list after changing it so you can see the effect."),
            ),
        ),
    ),
    Topic(
        key="list_slicing",
        title="List Slicing",
        summary="Grab a section of a list with the same [start:stop] syntax as strings.",
        lesson="""
Slicing works on lists exactly as it does on strings. `[start:stop]` returns a **new list** with
the items from start up to (but not including) stop:

```python
nums = [10, 20, 30, 40, 50]
print(nums[1:3])   # [20, 30]
print(nums[:2])    # [10, 20]   — from the start
print(nums[2:])    # [30, 40, 50] — to the end
print(nums[::-1])  # [50, 40, 30, 20, 10] — reversed
```

The `[::-1]` trick (step of -1) reverses any list. Slicing never changes the original — it always
hands back a fresh list.
        """,
        example_code='''nums = [10, 20, 30, 40, 50]

print(nums[1:3])
print(nums[:2])
print(nums[2:])
print(nums[::-1])''',
        challenge="""
Create a list of at least four numbers. Use a slice (like nums[1:3]) to take a section of it,
and print the slice.
        """,
        starter_code='''nums = [10, 20, 30, 40, 50]

print(nums[1:3])
print()''',
        mentor=MentorCard(
            opening="A slice copies out a section of a list without disturbing the original. The [start:stop] rule you learned for strings works identically here.",
            pass_message="Slicing lists is a quiet superpower — taking the top 3, dropping the first item, reversing the order, all in one expression.",
            hints=(
                ("A list is created", "Create a list of several numbers: nums = [10, 20, 30, 40, 50]."),
                ("A slice is used", "Take a section with a colon: nums[1:3] returns items 1 and 2."),
                ("Output is printed", "Print your slice to see the section you selected."),
            ),
        ),
        expected_output="[20, 30]",
    ),
    Topic(
        key="list_comprehensions",
        title="List Comprehensions",
        summary="Build a new list from an old one in a single readable line.",
        lesson="""
A very common task: take a list, do something to each item, collect the results in a new list.
The long way is a loop with `.append()`. The Python way is a **list comprehension** — one line:

```python
numbers = [1, 2, 3, 4]
doubled = [n * 2 for n in numbers]   # [2, 4, 6, 8]
```

Read it right-to-left: "for each `n` in numbers, give me `n * 2`." You can add a condition to keep
only some items:

```python
evens = [n for n in numbers if n % 2 == 0]   # [2, 4]
```

Comprehensions are concise and fast. Once they click, you'll see them everywhere in real Python.
        """,
        example_code='''numbers = [1, 2, 3, 4, 5]

doubled = [n * 2 for n in numbers]
print(doubled)

evens = [n for n in numbers if n % 2 == 0]
print(evens)''',
        challenge="""
Create a list of numbers. Use a list comprehension to build a new list from it (for example,
double each number or keep only some), and print the new list.
        """,
        starter_code='''numbers = [1, 2, 3, 4, 5]

doubled = [n * 2 for n in numbers]
print()''',
        mentor=MentorCard(
            opening="A list comprehension is a loop that builds a list, written on one line. [do_something for item in collection] — concise, readable, and very Python.",
            pass_message="List comprehensions are a hallmark of fluent Python. You just wrote in one line what used to take four.",
            hints=(
                ("A list comprehension is used", "Use the [expression for item in collection] form, for example: [n * 2 for n in numbers]."),
                ("Output is printed", "Print the new list to see what your comprehension built."),
            ),
        ),
    ),
    Topic(
        key="tuples",
        title="Tuples",
        summary="Store a fixed collection of values that cannot be changed.",
        lesson="""
A tuple is like a list, but **frozen**. Once you create it, you cannot add, remove, or change
its items. Write it with parentheses `()` instead of square brackets `[]`.

```python
compass = ("North", "East", "South", "West")
print(compass[0])    # North
print(len(compass))  # 4
```

Use a tuple when the data should stay the same — seasons of the year, compass directions, the
colours of a traffic light. Python enforces the "no changes" rule for you, which prevents
accidental mistakes.
        """,
        example_code='''compass = ("North", "East", "South", "West")

print(compass)
print(len(compass))
print(compass[0])''',
        challenge="""
Create a tuple called `seasons` with four season names. Print the whole tuple, print its
length using len(), and print one item by its index.
        """,
        starter_code='''seasons = ()

print(seasons)
print(len(seasons))
print(seasons[0])''',
        mentor=MentorCard(
            opening="A tuple is a list that cannot change. Once created, its items are locked in place — Python refuses any attempt to add, remove, or swap them. Use a tuple when the values should always stay the same.",
            pass_message="You've learned the difference between a list and a tuple. Lists change; tuples don't. That single distinction shapes how you design data in every real Python program.",
            hints=(
                ("A tuple is created", 'Create a tuple with parentheses: seasons = ("Spring", "Summer", "Autumn", "Winter"). The parentheses — not square brackets — tell Python this is a tuple.'),
                ("The tuple has at least 3 items", "Add at least 3 items inside the parentheses, separated by commas. Four seasons would be perfect."),
                ("len() is used", "Call len(seasons) to find out how many items the tuple contains — the same way you used len() with lists."),
                ("An item is accessed by index", "Access a specific item with seasons[0] for the first item, seasons[1] for the second, and so on."),
                ("Output is printed", "Wrap your results in print() so they appear on screen."),
            ),
        ),
    ),
    Topic(
        key="tuple_unpacking",
        title="Tuple Unpacking",
        summary="Assign several variables at once from a tuple or list.",
        lesson="""
Python lets you assign multiple variables in a single line by **unpacking** a tuple or list:

```python
point = (3, 7)
x, y = point          # x = 3, y = 7
```

You can even skip the tuple variable entirely:

```python
name, level = "Ari", 5
```

A famous trick: swap two variables with no temporary variable at all:

```python
a, b = 1, 2
a, b = b, a           # now a = 2, b = 1
```

Unpacking makes code shorter and clearer — and it's how functions return several values, which
you'll meet soon.
        """,
        example_code='''point = (3, 7)
x, y = point
print(x)
print(y)

a, b = 1, 2
a, b = b, a
print(a, b)''',
        challenge="""
Unpack a tuple (or a pair of values) into two or more variables in a single line, then print
the variables.
        """,
        starter_code='''point = (3, 7)

x, y = point
print()''',
        mentor=MentorCard(
            opening="Unpacking assigns several variables in one line by pulling apart a tuple. It makes code shorter, and it's how Python returns multiple values from a function.",
            pass_message="Tuple unpacking is a small feature with big reach — you'll see it in loops, swaps, and every function that returns more than one value.",
            hints=(
                ("Multiple variables are assigned at once", "Put several names on the left of one =: x, y = point (or x, y = 3, 7)."),
                ("Output is printed", "Print the unpacked variables to confirm each got its value."),
            ),
        ),
    ),
    Topic(
        key="sets",
        title="Sets",
        summary="Store a collection of unique values — duplicates vanish automatically.",
        lesson="""
A set is a collection with **no duplicates and no order**. Add the same value twice and Python
keeps just one. Write a set with curly braces, or build one with `set()`:

```python
colors = {"red", "green", "red"}
print(colors)        # {'red', 'green'} — the duplicate is gone
```

Useful set methods and operations:

| Action | How |
|---|---|
| Add an item | `colors.add("blue")` |
| Remove duplicates from a list | `set(my_list)` |
| Items in both sets | `a.intersection(b)` |
| Items in either set | `a.union(b)` |

Reach for a set whenever uniqueness matters — tags, unique visitors, removing repeats.
        """,
        example_code='''numbers = [1, 2, 2, 3, 3, 3]

unique = set(numbers)
print(unique)

unique.add(4)
print(unique)
print(len(unique))''',
        challenge="""
Create a set (or turn a list with duplicates into a set). Use a set method like .add(), then
print the set.
        """,
        starter_code='''numbers = [1, 2, 2, 3, 3, 3]

unique = set(numbers)
unique.add(4)
print()''',
        mentor=MentorCard(
            opening="A set is a bag of unique values — add a duplicate and it simply disappears. When you care about 'which distinct things are here', a set is the perfect tool.",
            pass_message="Sets make uniqueness effortless. Removing duplicates, checking membership fast, combining groups — all become one-liners.",
            hints=(
                ("A set is created", "Create a set with set(my_list) or with curly braces: unique = {1, 2, 3}."),
                ("A set method is used", "Call a set method such as unique.add(4) to put a new value in."),
                ("Output is printed", "Print the set to see its unique contents."),
            ),
        ),
    ),
    Topic(
        key="dictionaries",
        title="Dictionaries",
        summary="Store information as named key-value pairs for instant lookup by name.",
        lesson="""
A list stores items by position: item at index 0, item at index 1. A **dictionary** stores items
by name — each value gets a label called a **key**.

```python
character = {"name": "Ari", "level": 5}
print(character["name"])   # Ari
```

The key goes in quotes, the value follows a colon. Access any value instantly by its key — no
position numbers to remember.

Add or update a key any time by assigning to it: `character["class"] = "Wizard"`.
        """,
        example_code='''mentor = {
    "name": "Ari",
    "level": 12,
    "language": "Python",
}

print(mentor["name"])
print(mentor["level"])

mentor["streak"] = 7
print(mentor)''',
        challenge="""
Create a dictionary called `character` with at least 3 keys — for example name, level, and
a skill. Print one value by its key.
        """,
        starter_code='''character = {
    "name": "",
    "level": 0,
}

print(character["name"])''',
        mentor=MentorCard(
            opening="A list stores items by position. A dictionary stores them by name — each value has a label called a key that describes what it means.",
            pass_message="Dictionaries are everywhere in real Python code. APIs return them, configs are structured as them, databases use them. You now speak that language.",
            hints=(
                ("A dictionary is created", 'Create a dictionary: character = {"name": "Ari", "level": 5, "skill": "Python"}. Keys and values are separated by colons.'),
                ("The dictionary has at least 3 keys", "Add at least 3 key-value pairs inside the curly braces, separated by commas."),
                ("A value is accessed by key", 'Access a value with: character["name"]. Put the key in square brackets.'),
                ("Output is printed", 'Wrap your result in print() to show a value: print(character["name"])'),
            ),
        ),
    ),
    Topic(
        key="dict_methods",
        title="Dictionary Methods",
        summary="Read a dictionary safely with .get(), .keys(), .values(), and .items().",
        lesson="""
Dictionaries have methods that make them easy and safe to read:

| Method | Returns |
|---|---|
| `.get("key")` | The value, or `None` if the key is missing (no crash) |
| `.keys()` | All the keys |
| `.values()` | All the values |
| `.items()` | Key-value pairs together |

```python
character = {"name": "Ari", "level": 5}
print(character.get("name"))     # Ari
print(character.get("class"))    # None — safe, no error
print(character.keys())          # dict_keys(['name', 'level'])
```

`.get()` is the safe way to read a key you're not sure exists — instead of crashing with a
`KeyError`, it quietly returns `None`.
        """,
        example_code='''character = {"name": "Ari", "level": 5}

print(character.get("name"))
print(character.get("class"))
print(character.keys())
print(character.values())''',
        challenge="""
Create a dictionary. Use at least one dictionary method (.get(), .keys(), .values(), or
.items()) and print the result.
        """,
        starter_code='''character = {"name": "Ari", "level": 5}

print(character.get("name"))
print()''',
        mentor=MentorCard(
            opening="Dictionary methods make reading data safe and easy. .get() in particular never crashes on a missing key — it just returns None.",
            pass_message="You now read dictionaries the professional way. .get() and .items() will save you from countless KeyError crashes.",
            hints=(
                ("A dictionary is created", 'Create a dictionary first: character = {"name": "Ari", "level": 5}.'),
                ("A dictionary method is used", "Call a method such as character.get(\"name\"), character.keys(), or character.values()."),
                ("Output is printed", "Print the result of the method to see what it returns."),
            ),
        ),
    ),
    Topic(
        key="dict_iteration",
        title="Looping Over Dictionaries",
        summary="Walk through every key and value in a dictionary with a loop.",
        lesson="""
To process a whole dictionary, loop over its `.items()` — you get the key and value together each
turn:

```python
scores = {"Ari": 10, "Bo": 7}
for name, score in scores.items():
    print(name, score)
# Ari 10
# Bo 7
```

You can also loop over just `.keys()` or just `.values()` if you only need one side. Looping with
`.items()` is the standard way to read through every entry in a dictionary.
        """,
        example_code='''prices = {"apple": 3, "banana": 2, "cherry": 5}

for fruit, price in prices.items():
    print(f"{fruit} costs {price}")''',
        challenge="""
Create a dictionary with at least two key-value pairs. Use a for loop with .items() to print
each key together with its value.
        """,
        starter_code='''prices = {"apple": 3, "banana": 2}

for fruit, price in prices.items():
    print()''',
        mentor=MentorCard(
            opening="To read a whole dictionary, loop over its .items() — Python hands you each key and value as a pair. This is the standard way to process structured data.",
            pass_message="Looping over .items() is how you process every record in a dictionary. You'll use it whenever data arrives as key-value pairs.",
            hints=(
                ("A dictionary is created", 'Create a dictionary with a few pairs: prices = {"apple": 3, "banana": 2}.'),
                ("A loop goes through the dictionary", "Loop over the pairs: for key, value in prices.items():."),
                ("Output is printed", "Indent a print() inside the loop to show each key and value."),
            ),
        ),
    ),
    Topic(
        key="nested_data",
        title="Nested Data",
        summary="Combine lists and dictionaries to model real-world records.",
        lesson="""
Real data is rarely flat. The most common shape in Python is a **list of dictionaries** — each
dictionary is one record, and the list holds many records:

```python
players = [
    {"name": "Ari", "score": 10},
    {"name": "Bo", "score": 7},
]
```

Loop over the list and read each dictionary's keys:

```python
for player in players:
    print(player["name"], player["score"])
```

This is exactly how data comes back from web APIs, spreadsheets, and databases. Master this shape
and you can model almost any real-world information.
        """,
        example_code='''players = [
    {"name": "Ari", "score": 10},
    {"name": "Bo", "score": 7},
]

for player in players:
    print(f"{player['name']}: {player['score']}")''',
        challenge="""
Create a list of at least two dictionaries (each with the same keys). Loop over the list and
print a value from each dictionary.
        """,
        starter_code='''players = [
    {"name": "Ari", "score": 10},
    {"name": "Bo", "score": 7},
]

for player in players:
    print()''',
        mentor=MentorCard(
            opening="Real data nests — a list of dictionaries, where each dictionary is one record. This single shape models players, products, users, almost anything.",
            pass_message="You can now model real-world data. A list of dictionaries is exactly what web APIs and databases hand you every day.",
            hints=(
                ("A list of dictionaries is created", 'Make a list where each item is a dictionary: players = [{"name": "Ari", "score": 10}, {"name": "Bo", "score": 7}].'),
                ("A loop goes through the data", "Loop over the list: for player in players: — each player is a dictionary."),
                ("Output is printed", 'Inside the loop, print a value from each dictionary: print(player["name"]).'),
            ),
        ),
    ),
    Topic(
        key="exercise_inventory",
        title="Exercise: Inventory Tracker",
        summary="Model and report on a small inventory — collections working together.",
        lesson="""
You've learned lists, list methods, dictionaries, dictionary methods, and nested data. This
exercise combines them into something genuinely useful.

You'll build an **inventory tracker**: a list of item records (each a dictionary), then loop over
it to print a report. This is the bones of every shopping cart, to-do app, and product catalogue.

Keep it simple: a few items, a loop, a printed line per item.
        """,
        example_code='''inventory = [
    {"item": "Torch", "qty": 3},
    {"item": "Map", "qty": 1},
    {"item": "Key", "qty": 5},
]

for entry in inventory:
    print(f"{entry['item']}: {entry['qty']} in stock")

print(f"{len(inventory)} item types tracked")''',
        challenge="""
Build an inventory tracker:
1. Create a list of at least two dictionaries, each describing an item (for example name and quantity).
2. Loop over the list.
3. Print a line for each item.
        """,
        starter_code='''inventory = [
    {"item": "Torch", "qty": 3},
    {"item": "Map", "qty": 1},
]

for entry in inventory:
    print()''',
        mentor=MentorCard(
            opening="Your collections project. Model a small inventory as a list of dictionaries, then loop over it to print a report. This is the shape of real app data.",
            pass_message="You just built the core of a real data app — structured records, iterated and reported. Scale this up and you have a catalogue, a cart, or a dashboard.",
            hints=(
                ("A list of dictionaries is created", 'Make a list where each item is a dictionary: inventory = [{"item": "Torch", "qty": 3}, ...].'),
                ("A loop goes through the items", "Loop over the inventory: for entry in inventory:."),
                ("Output is printed", "Inside the loop, print a line for each item, for example its name and quantity."),
            ),
        ),
    ),
    # ───────────────────────── UNIT 6 — FUNCTIONS IN DEPTH ─────────────────────────
    Topic(
        key="functions",
        title="Functions",
        summary="Package reusable behavior behind a clear name.",
        lesson="""
A function is a named mini-program. Define it once with `def`, then call it whenever you need that
behavior.

Functions can accept inputs called parameters and can send a value back with `return`.
        """,
        example_code='''def mentor_greeting(name):
    return f"Welcome back, {name}. Ready for the next tale?"

message = mentor_greeting("Ari")
print(message)''',
        challenge="""
Write a function that accepts a learner name and returns a friendly mentor message. Call the
function and print the result.
        """,
        starter_code='''def mentor_message(name):
    return ""

print(mentor_message(""))''',
        mentor=MentorCard(
            opening="Functions are how you package a useful idea and give it a name. Once defined, you can use it anywhere — in this program, in any program.",
            pass_message="You've written a function. That is the foundation of everything: reusable, named, testable pieces of logic. This skill scales to any program size.",
            hints=(
                ("Submitted Python code", 'Define your function with def, accept a name parameter, build a message inside, return it, then call it: print(mentor_message("Ari")).'),
            ),
        ),
    ),
    Topic(
        key="function_parameters",
        title="Function Parameters",
        summary="Pass several pieces of information into a function at once.",
        lesson="""
A function becomes far more useful when it accepts **several** inputs. List the parameters inside
the parentheses, separated by commas:

```python
def describe(name, level):
    return f"{name} is level {level}"

print(describe("Ari", 5))     # Ari is level 5
```

When you call the function, you pass the **arguments** in the same order as the parameters. You can
also name them for clarity:

```python
print(describe(level=5, name="Ari"))   # order doesn't matter when named
```

More parameters means a more flexible function — one definition, endless combinations of inputs.
        """,
        example_code='''def add_scores(first, second, third):
    return first + second + third

total = add_scores(10, 20, 30)
print(total)''',
        challenge="""
Write a function that takes at least two parameters, combines them somehow, and returns the result.
Call the function with arguments and print what it returns.
        """,
        starter_code='''def add_scores(first, second):
    return first + second

print(add_scores(10, 20))''',
        mentor=MentorCard(
            opening="One input is useful; several is powerful. List parameters in the parentheses and your function can combine many pieces of information at once.",
            pass_message="Multi-parameter functions are the everyday tools of programming. You now write functions flexible enough for real work.",
            hints=(
                ("A function with parameters is defined", "Define a function with two or more parameters: def add_scores(first, second):."),
                ("The function is called", "Call it with matching arguments: add_scores(10, 20)."),
                ("Output is printed", "Print what the function returns: print(add_scores(10, 20))."),
            ),
        ),
    ),
    Topic(
        key="default_parameters",
        title="Default Parameters",
        summary="Give parameters a fallback value so some arguments become optional.",
        lesson="""
A parameter can have a **default value** — used automatically when the caller doesn't supply one:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Ari"))              # Hello, Ari!   — default used
print(greet("Ari", "Welcome"))   # Welcome, Ari! — default overridden
```

Defaults make arguments optional, which keeps simple calls short while still allowing
customisation. One rule: parameters **with** defaults must come **after** those without.
        """,
        example_code='''def power(base, exponent=2):
    return base ** exponent

print(power(5))
print(power(5, 3))''',
        challenge="""
Write a function with at least one default parameter. Call it once using the default, and once
overriding it. Print both results.
        """,
        starter_code='''def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Ari"))
print()''',
        mentor=MentorCard(
            opening="A default value makes a parameter optional. Callers who want the common case write less; callers who need something special can still override it.",
            pass_message="Default parameters are how flexible, friendly functions are built — short to call, powerful when needed.",
            hints=(
                ("A function with a default parameter is defined", 'Give a parameter a default with =: def greet(name, greeting="Hello"):.'),
                ("The function is called", "Call your function — try it once without the optional argument, once with it."),
                ("Output is printed", "Print the results of both calls to see the default in action."),
            ),
        ),
    ),
    Topic(
        key="multiple_return",
        title="Returning Multiple Values",
        summary="Hand back more than one value from a function using a tuple.",
        lesson="""
A function can return several values at once — just separate them with commas. Python bundles them
into a tuple:

```python
def min_and_max(numbers):
    return min(numbers), max(numbers)

low, high = min_and_max([4, 1, 8, 3])
print(low)    # 1
print(high)   # 8
```

On the calling side you **unpack** the result into separate variables — exactly the tuple
unpacking you learned earlier. This is a clean way to compute and return related results together.
        """,
        example_code='''def stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

low, high, total = stats([4, 1, 8, 3])
print(low)
print(high)
print(total)''',
        challenge="""
Write a function that returns two or more values. Call it, unpack the results into separate
variables, and print them.
        """,
        starter_code='''def min_and_max(numbers):
    return min(numbers), max(numbers)

low, high = min_and_max([4, 1, 8, 3])
print()''',
        mentor=MentorCard(
            opening="A function isn't limited to one answer. Separate values with commas in your return, and Python hands them back as a tuple you can unpack.",
            pass_message="Returning multiple values keeps related results together. Combined with unpacking, it's an elegant, very Pythonic pattern.",
            hints=(
                ("A function returns multiple values", "Return several values separated by commas: return min(numbers), max(numbers)."),
                ("The function is called", "Call the function and unpack the results: low, high = min_and_max(...)."),
                ("Output is printed", "Print the unpacked values to see each returned result."),
            ),
        ),
    ),
    Topic(
        key="none_type",
        title="None",
        summary="Understand Python's way of saying 'no value here yet'.",
        lesson="""
`None` is a special value that means "nothing" or "no value." It is its own type, and it's how
Python represents emptiness deliberately.

A function that doesn't `return` anything gives back `None` automatically:

```python
def shout(text):
    print(text.upper())   # prints, but returns nothing

result = shout("hi")      # HI is printed
print(result)             # None
```

Check for it with `is`:

```python
if result is None:
    print("No value was returned.")
```

`None` shows up constantly — as a starting value, a missing dictionary key (`.get()`), or a
function with no return. Recognising it prevents a lot of confusion.
        """,
        example_code='''def find_winner(scores):
    if len(scores) == 0:
        return None
    return max(scores)

winner = find_winner([])
print(winner)

if winner is None:
    print("No scores yet.")''',
        challenge="""
Use None in a program — for example, set a variable to None, or write a function that returns
None in some case. Then print a message based on whether the value is None.
        """,
        starter_code='''result = None

if result is None:
    print("No value yet.")''',
        mentor=MentorCard(
            opening="None is Python's way of saying 'nothing here'. It's a real value you can check for — and it's what every function without a return quietly hands back.",
            pass_message="Understanding None saves beginners from real confusion. You now recognise Python's signal for 'empty' or 'not set'.",
            hints=(
                ("None is used", "Use None somewhere: set a variable to None, or return None from a function."),
                ("Output is printed", "Print a message, ideally based on an is None check, to show you handled the empty case."),
            ),
        ),
    ),
    Topic(
        key="recursion",
        title="Recursion",
        summary="A function that calls itself to solve a problem in smaller steps.",
        lesson="""
Recursion is a function that **calls itself**. It sounds strange, but it's just a loop expressed a
different way. Every recursion needs two parts:

1. A **base case** — when to stop (or it runs forever).
2. A **recursive case** — call itself on a smaller version of the problem.

```python
def countdown(n):
    if n == 0:           # base case — stop
        print("Liftoff!")
        return
    print(n)
    countdown(n - 1)     # recursive case — smaller problem

countdown(3)             # 3, 2, 1, Liftoff!
```

Each call works on a simpler input until it hits the base case. Recursion shines on problems that
naturally break into smaller copies of themselves.
        """,
        example_code='''def countdown(n):
    if n == 0:
        print("Liftoff!")
        return
    print(n)
    countdown(n - 1)

countdown(5)''',
        challenge="""
Write a function that calls itself (recursion). Give it a base case so it stops, and call it once.
Make sure it prints something on the way.
        """,
        starter_code='''def countdown(n):
    if n == 0:
        print("Liftoff!")
        return
    print(n)
    countdown(n - 1)

countdown(5)''',
        mentor=MentorCard(
            opening="Recursion is a function that calls itself, solving a big problem by reducing it to a smaller one. The secret is the base case — the condition that finally says 'stop'.",
            pass_message="You've grasped one of computer science's most elegant ideas. Recursion feels like magic at first, then becomes a natural tool for the right problems.",
            hints=(
                ("A function is defined", "Define a function that takes a number, for example: def countdown(n):."),
                ("The function calls itself", "Inside the function, call itself on a smaller value: countdown(n - 1). Include an if base case so it stops."),
                ("Output is printed", "Print something inside the function so you can watch the recursion work."),
            ),
        ),
        expected_output="5\n4\n3\n2\n1\nLiftoff!",
    ),
    Topic(
        key="exercise_calculator",
        title="Exercise: Mini Calculator",
        summary="Capstone — build a small program from functions you define and call.",
        lesson="""
This is your capstone. Across this course you've learned variables, types, operators, decisions,
loops, collections, and functions. Now you'll build a small program from your own functions.

Build a **mini calculator**: write one or more functions that take numbers and return a result,
then call them and print the answers. Everything you've practised — parameters, return values,
arithmetic, f-strings — comes together here.

There's no single correct program. Design it, build it, run it. That's what programming is.
        """,
        example_code='''def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

print(f"Sum: {add(8, 5)}")
print(f"Product: {multiply(8, 5)}")''',
        challenge="""
Build a mini calculator:
1. Define at least one function that takes numbers and returns a result.
2. Call your function with some values.
3. Print the returned result (an f-string makes it readable).
        """,
        starter_code='''def add(a, b):
    return a + b

result = add(8, 5)
print()''',
        mentor=MentorCard(
            opening="Your capstone. Define a function or two, call them with real values, and print the results. This is everything you've learned, working as one program.",
            pass_message="You did it — a complete program built from your own functions. You now have the core toolkit of a Python programmer. This is a genuine milestone.",
            hints=(
                ("A function is defined", "Define a function that takes numbers, for example: def add(a, b):."),
                ("The function is called", "Call your function with values: add(8, 5)."),
                ("A value is returned", "Make sure your function uses return to hand back a result."),
                ("Output is printed", 'Print the result, ideally with an f-string: print(f"Sum: {add(8, 5)}").'),
            ),
        ),
    ),
    # ───────────────────────── UNIT 7 — OBJECT-ORIENTED PROGRAMMING ─────────────────────────
    Topic(
        key="classes",
        title="What is a Class?",
        summary="Understand classes as blueprints for creating objects.",
        lesson="""
A **class** is a blueprint — like a recipe or a template. Just as a recipe describes how to
make a cake (ingredients, steps), a class describes what an object looks like and what it can do.

For example, a `Hero` class might describe:
- What data a hero has: name, health, power level
- What actions a hero can do: attack, heal, level_up

Once you have a blueprint, you can create many objects from it — just like you can bake many cakes
from one recipe. Each cake is different (different flavours, toppings), but they all follow the same recipe.

In Python, you define a class with the `class` keyword:

```python
class Hero:
    pass  # we'll add details next
```

The name `Hero` starts with a capital letter — that's Python convention for class names.
        """,
        example_code='''class Hero:
    """A character in an RPG game."""
    pass

print(Hero)
print("Hero class is defined!")''',
        challenge="""
Define a class called `Character`. You don't need to add anything inside it yet — just create the blueprint.
Then print a message showing the class exists.
        """,
        starter_code='''class Character:
    pass

print()''',
        mentor=MentorCard(
            opening="A class is a blueprint. Think of it like a cookie cutter — it defines the shape, and then you stamp out many cookies using that same cutter.",
            pass_message="You've created your first class. It's empty for now, but it's a real blueprint that Python recognizes.",
            hints=(
                ("A class is defined", "Use the class keyword: class Character:. The name starts with a capital letter."),
                ("Output is printed", "Print something to show the class exists, like print('Class created!')."),
            ),
        ),
    ),
    Topic(
        key="class_definition",
        title="Define a Class with __init__",
        summary="Add properties and initialization to a class using __init__.",
        lesson="""
A class without data is just a name. To make it useful, you need to:

1. Define what **data** (properties) each object will have
2. Initialize that data when you create a new object

The **`__init__` method** (pronounced "dunder init") is Python's constructor. It runs automatically
when you create a new object from a class. Use it to set up the object's initial state.

```python
class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health
```

Here:
- `self` refers to the object being created (like "this" in other languages)
- `self.name = name` creates a property called `name` on the object and stores the value
- The parameters (`name`, `health`) are values you pass when creating the object

It looks like magic at first, but think of it this way: `self` is the blank cookie being stamped;
`__init__` fills in the cookie's properties.
        """,
        example_code='''class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

print("Hero class with __init__ is ready!")''',
        challenge="""
Define a class called `Player` with an `__init__` method. Give it two properties: a name and a score.
Print a message showing the class is ready to use.
        """,
        starter_code='''class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

print()''',
        mentor=MentorCard(
            opening="The __init__ method is how you teach a class what data each object should have. When you create a new object, __init__ runs automatically to set it up.",
            pass_message="You've defined a class that knows how to initialize itself. Next you'll create actual objects from it.",
            hints=(
                ("A class is defined", "Start with class Player: and give it an __init__ method."),
                ("__init__ has parameters", "After self, add parameters for the properties: def __init__(self, name, score):."),
                ("Properties are set with self", "Inside __init__, create properties: self.name = name and self.score = score."),
                ("Output is printed", "Print a message to confirm the class is defined."),
            ),
        ),
    ),
    Topic(
        key="instance_creation",
        title="Create Objects from a Class",
        summary="Make real objects (instances) from a class blueprint.",
        lesson="""
Defining a class is like writing a recipe. To actually use it, you create **instances** —
real objects made from that blueprint.

Creating an instance is simple: call the class name like a function:

```python
class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

hero1 = Hero("Ari", 100)
hero2 = Hero("Bard", 80)
```

Each time you call `Hero(...)`, Python:
1. Creates a new blank object
2. Calls `__init__` on it with the values you passed
3. Hands you that object

So `hero1` and `hero2` are two separate objects, each with their own `name` and `health`.
Access properties using dot notation: `hero1.name` is `"Ari"`.
        """,
        example_code='''class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

hero1 = Hero("Ari", 100)
hero2 = Hero("Bard", 80)

print(f"Hero 1: {hero1.name}, Health: {hero1.health}")
print(f"Hero 2: {hero2.name}, Health: {hero2.health}")''',
        challenge="""
Using the Player class you defined earlier, create two player objects with different names and scores.
Print both players' information using their properties.
        """,
        starter_code='''class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

player1 = Player("Alice", 500)
player2 = Player("Bob", 300)

print()
print()''',
        mentor=MentorCard(
            opening="Creating an instance means making a real object from the class blueprint. Each object is separate — changing one doesn't affect the other.",
            pass_message="You've created multiple objects from the same class. This is the power of classes — one blueprint, many objects.",
            hints=(
                ("Objects are created", "Call the class like a function: player1 = Player(\"Alice\", 500)."),
                ("Properties are accessed", "Use dot notation: player1.name gives you Alice."),
                ("Both objects are separate", "player1 and player2 are different objects with different data."),
                ("Output is printed", "Print both players' names and scores."),
            ),
        ),
    ),
    Topic(
        key="class_methods",
        title="Add Methods to a Class",
        summary="Give objects actions they can perform using methods.",
        lesson="""
So far, objects just hold data. But the "blueprint" should also describe **what the object can do**.

A **method** is a function that belongs to a class. It's an action the object can perform.

```python
class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health = self.health - amount
        print(f"{self.name} takes {amount} damage! Health: {self.health}")

hero = Hero("Ari", 100)
hero.take_damage(20)  # Ari takes 20 damage! Health: 80
```

Notice:
- Methods are defined inside the class, like `__init__`
- The first parameter is always `self` (it refers to the object)
- You call a method using dot notation: `hero.take_damage(20)`
- Inside the method, `self.health` refers to that object's health

Methods let objects **act on their own data**. A Hero object knows how to take damage.
        """,
        example_code='''class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def heal(self, amount):
        self.health = self.health + amount
        print(f"{self.name} heals {amount} HP. Health: {self.health}")

hero = Hero("Ari", 50)
hero.heal(30)''',
        challenge="""
Add a method to your Player class. For example, add a method `gain_xp(amount)` that increases the player's score.
Create a player, call the method, and print the updated score.
        """,
        starter_code='''class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def gain_xp(self, amount):
        self.score = self.score + amount
        print(f"{self.name} gained {amount} XP!")

player = Player("Alice", 100)
player.gain_xp(50)
print(f"New score: {player.score}")''',
        mentor=MentorCard(
            opening="Methods are actions objects can perform on themselves. A Hero can attack, heal, level up. Define these as methods inside the class.",
            pass_message="Your class now has behaviour. Objects aren't just data containers — they're active, they do things.",
            hints=(
                ("A method is defined", "Inside the class, define a function: def gain_xp(self, amount):."),
                ("self is used", "Always start with self. Use self.score to access the object's score."),
                ("The method modifies data", "The method changes self.score or another property."),
                ("The method is called", "Use dot notation on the object: player.gain_xp(50)."),
            ),
        ),
    ),
    Topic(
        key="class_attributes",
        title="Work with Object Attributes",
        summary="Access and modify an object's properties after creation.",
        lesson="""
You've created objects and called methods. But sometimes you need to directly **read or change**
an object's properties without calling a method.

You can access and modify attributes (properties) anytime using dot notation:

```python
class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

hero = Hero("Ari", 100)

# Read attributes
print(hero.name)      # Ari
print(hero.health)    # 100

# Modify attributes directly
hero.health = 80
hero.name = "Ari the Brave"

print(hero.health)    # 80
print(hero.name)      # Ari the Brave
```

This is useful for small changes. For complex operations (like taking damage with special rules),
use a method instead. For simple reads and writes, dot notation is fine.
        """,
        example_code='''class Character:
    def __init__(self, name, level):
        self.name = name
        self.level = level

char = Character("Knight", 5)
print(f"Name: {char.name}, Level: {char.level}")

char.level = char.level + 1
print(f"Name: {char.name}, Level: {char.level}")''',
        challenge="""
Create a Player object, then read and modify its attributes. Print the original values, change them,
and print the updated values.
        """,
        starter_code='''class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

player = Player("Alice", 100)
print(f"Original: {player.name}, {player.score}")

player.score = 150
print(f"Updated: {player.name}, {player.score}")''',
        mentor=MentorCard(
            opening="Attributes are an object's properties. You can read them and change them directly using dot notation. Use methods for complex logic, direct access for simple changes.",
            pass_message="You're fluent in objects now — creating them, calling their methods, and modifying their attributes.",
            hints=(
                ("Attributes are read", "Use dot notation: player.name and player.score."),
                ("Attributes are modified", "Assign new values: player.score = 200."),
                ("Both values are printed", "Show the original and updated values."),
            ),
        ),
    ),
    Topic(
        key="inheritance",
        title="Inheritance — Extend a Class",
        summary="Create a new class that extends another, reusing code.",
        lesson="""
Imagine you have a `Hero` class with name, health, and methods like `attack()` and `heal()`.

Now you want a `Warrior` class that has everything a Hero has, **plus** special warrior abilities
like `shield_bash()`.

Instead of copying all the Hero code, you can use **inheritance**: make Warrior extend Hero.

```python
class Hero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def attack(self):
        print(f"{self.name} attacks!")

class Warrior(Hero):
    def shield_bash(self):
        print(f"{self.name} uses shield bash!")

warrior = Warrior("Thorin", 150)
warrior.attack()          # Inherited from Hero
warrior.shield_bash()     # New ability
```

The syntax `class Warrior(Hero):` means "Warrior inherits from Hero."

**Key points:**
- Warrior automatically gets all of Hero's properties and methods
- Warrior can add its own methods
- This avoids code repetition and models real-world hierarchies (Warrior is a kind of Hero)
        """,
        example_code='''class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound")

class Dog(Animal):
    def bark(self):
        print(f"{self.name} barks loudly!")

dog = Dog("Buddy")
dog.speak()
dog.bark()''',
        challenge="""
Create a base class (e.g., Vehicle) with a simple __init__ and a method. Then create a subclass
(e.g., Car) that inherits from it and adds a new method. Create an instance and use both.
        """,
        starter_code='''class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start_engine(self):
        print(f"{self.brand} engine starts!")

class Car(Vehicle):
    def honk(self):
        print(f"{self.brand} car honks!")

car = Car("Toyota")
car.start_engine()
car.honk()''',
        mentor=MentorCard(
            opening="Inheritance lets you create a specialized version of a class. The new class gets everything from the original, plus its own additions. It's code reuse and logical hierarchy.",
            pass_message="You've mastered the core of object-oriented programming. Inheritance is how real programs manage complexity.",
            hints=(
                ("A base class is defined", "Create a parent class: class Vehicle: with __init__ and a method."),
                ("A subclass inherits", "Use class Car(Vehicle): to inherit from Vehicle."),
                ("The subclass has its own method", "Add a new method to Car that doesn't exist in Vehicle."),
                ("Both methods work", "You can call Vehicle's method and Car's method on the same object."),
            ),
        ),
    ),
    Topic(
        key="exercise_class_design",
        title="Exercise: Design a Class",
        summary="Capstone — design a complete class combining all OOP concepts.",
        lesson="""
You've learned classes, methods, attributes, and inheritance. Now combine them all in one capstone project.

**Build a complete class** that represents something real — a student, a book, a game character,
a bank account, anything. Your class should have:

1. An `__init__` method that sets up initial properties
2. At least two methods that do something with those properties
3. Create one or more instances and use them (call methods, read attributes)

Think about what data your object should hold and what actions it should be able to do.
        """,
        example_code='''class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.current_page = 0

    def read(self, pages_read):
        self.current_page = self.current_page + pages_read
        print(f"You read {pages_read} pages. Now at page {self.current_page}.")

    def progress(self):
        percent = (self.current_page / self.pages) * 100
        print(f"Progress: {percent:.0f}%")

book = Book("Python Magic", "A. Wizard", 300)
book.read(50)
book.progress()''',
        challenge="""
Design a class that represents something meaningful to you. Include:
1. An __init__ method with at least 2 properties
2. At least 2 methods that modify or use those properties
3. Create 1 or more instances
4. Call the methods and print results
        """,
        starter_code='''class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        self.balance = self.balance - amount
        print(f"Withdrew {amount}. New balance: {self.balance}")

account = BankAccount("Alice", 1000)
account.deposit(500)
account.withdraw(200)''',
        mentor=MentorCard(
            opening="This is your OOP capstone. Design a class that models something real. Give it properties and methods. Bring it to life by creating objects and using them.",
            pass_message="You've completed Object-Oriented Programming. You now understand one of software engineering's core ideas. You can model the world in code.",
            hints=(
                ("A meaningful class is designed", "Choose something real: a Student, Book, Game, Account, etc."),
                ("__init__ initializes properties", "def __init__(self, ...) sets up at least 2 properties."),
                ("Methods modify or use data", "Write at least 2 methods that do something with self.property."),
                ("Instances are created and used", "Make objects: instance = ClassName(...) then call methods on them."),
            ),
        ),
    ),
)


def get_topic(topic_key: str) -> Topic:
    for topic in TOPICS:
        if topic.key == topic_key:
            return topic
    raise KeyError(f"Unknown topic: {topic_key}")
