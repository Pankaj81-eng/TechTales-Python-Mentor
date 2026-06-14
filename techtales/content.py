from techtales.models import MentorCard, Topic


TOPICS: tuple[Topic, ...] = (
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
Values have types, and each type behaves a little differently. Text uses `str`, whole numbers use
`int`, decimal numbers use `float`, and true/false values use `bool`.

Knowing the type helps you choose the right operation. You can add numbers together, join strings
with other strings, and use booleans to make decisions.
        """,
        example_code='''artifact_name = "Loop Lantern"
artifact_count = 3
power_level = 8.5
is_unlocked = True

print(type(artifact_name))
print(type(artifact_count))
print(type(power_level))
print(type(is_unlocked))''',
        challenge="""
Create one variable for each of these types: string, integer, float, and boolean. Print each value
with a label that explains what it represents.
        """,
        starter_code='''item_name = ""
item_count = 0
item_power = 0.0
is_ready = False

print()''',
        mentor=MentorCard(
            opening="Every value in Python has a type. Numbers, text, decimals, true/false — each behaves differently. Knowing the type tells you what you can do with it.",
            pass_message="Excellent. You now speak Python's type system. It will save you from many confusing bugs later.",
            hints=(
                ("Submitted Python code", "Try creating four variables — one text (str), one whole number (int), one decimal (float), and one True/False (bool). Then print each one."),
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
                ("A text variable is used in the f-string", 'Assign a name to a text variable first — learner_name = "Ari" — then put that variable inside {} in your f-string.'),
                ("A number variable is used in the f-string", 'Assign a number to a variable — xp = 100 — then include it in your f-string: f"Score: {xp}"'),
                ("Output is printed", "Your f-string exists, but Python hasn't printed it yet. Wrap it in print() so the sentence appears on screen."),
            ),
        ),
        expected_output="Ari has 100 XP",
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
        key="loops",
        title="Loops",
        summary="Repeat an action without writing the same line again and again.",
        lesson="""
Loops help programs repeat work. A `for` loop is great when you know the collection or range you
want to move through.

The loop variable changes each time through the loop, letting your code respond to the current item.
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
                ("Step numbers appear in output", 'Your output shows the same message every step instead of the step number. Use print(f"Training step {step}") so Python inserts the current value.'),
            ),
        ),
        expected_output="Training step 1\nTraining step 2\nTraining step 3",
    ),
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
        key="write_a_program",
        title="Write a Program",
        summary="Combine everything you have learned and write your first complete Python program.",
        lesson="""
Every programmer's journey begins with the same two words: Hello World.

In 1972, a programmer named Brian Kernighan wrote the first Hello World example to show
how a program sends a message to the outside world. Since then, it has become the universal
first step for anyone learning to code — a tradition shared by millions of developers.

A complete program has three things: data, processing, and output. Your first program skips
straight to output — `print()` sends a message to the screen. That single line is a complete,
working program. One instruction. One result. That is all programming ever is.
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
A for 90 and above, B for 80 and above, C for 70 and above, or F for anything below.
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
| `.split()` | Split into a list of words |
| `.strip()` | Remove surrounding whitespace |

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
Try .upper(), .lower(), .replace(), .split(), or .strip().
        """,
        starter_code='''message = "hello, world"

print(message.upper())
print()''',
        mentor=MentorCard(
            opening="Python's strings come with built-in tools. You don't need to import anything — methods like .upper() and .replace() are always available on any string.",
            pass_message="String manipulation is something you will do in every real program. You now have a reliable toolkit for it.",
            hints=(
                ("A text variable is created", 'Assign a string to a variable first: message = "Hello, World!"'),
                ("At least one string method is used", "Call a method on your string: message.upper() converts all letters to uppercase. The dot connects the method to the variable."),
                ("At least two string methods are used", 'Try a second method: message.lower() or message.replace("hello", "hi").'),
                ("Output is printed", "Wrap your transformed text in print() to see the result on screen."),
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
                ("String variables are defined", 'Your text values are already defined. Now convert them: price = int(price_text). The quotes mark it as text — int() makes it a number.'),
                ("A type conversion function is used", "Wrap each text variable with int(): price = int(price_text), quantity = int(quantity_text). Now Python can multiply them."),
                ("Arithmetic is performed", "Once converted, multiply: total = price * quantity. Python can only multiply numbers, not text strings."),
                ("Output is printed", 'Use an f-string to show the result: print(f"Total: {total}")'),
            ),
        ),
    ),
)


def get_topic(topic_key: str) -> Topic:
    for topic in TOPICS:
        if topic.key == topic_key:
            return topic
    raise KeyError(f"Unknown topic: {topic_key}")
