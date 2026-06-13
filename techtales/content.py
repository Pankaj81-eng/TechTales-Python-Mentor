from techtales.models import Topic


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
    ),
)


def get_topic(topic_key: str) -> Topic:
    for topic in TOPICS:
        if topic.key == topic_key:
            return topic
    raise KeyError(f"Unknown topic: {topic_key}")
