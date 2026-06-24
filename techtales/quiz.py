"""
Milestone exam definitions and question banks.

Each exam is triggered when the learner completes all topics in its unit group.
Questions are fill-in-the-blank: show code with ___ and pick from 4 options.
answer must exactly match one of the strings in options.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Question:
    prompt: str
    options: tuple[str, ...]
    answer: str
    code: str = ""

    def __post_init__(self):
        assert self.answer in self.options, f"Answer '{self.answer}' not in options {self.options}"
        assert len(self.options) == 4


@dataclass(frozen=True)
class Exam:
    key: str
    title: str
    badge_emoji: str
    badge_name: str
    trigger_topic: str          # last topic key that must be passed to unlock this exam
    questions: tuple[Question, ...]
    xp_reward: int = 100
    pass_threshold: float = 0.7 # fraction correct needed to pass


def _q(prompt: str, options: tuple, answer: str, code: str = "") -> Question:
    return Question(prompt=prompt, options=options, answer=answer, code=code)


# ---------------------------------------------------------------------------
# Exam 1 — Foundations  (Unit 1)
# ---------------------------------------------------------------------------
_FOUNDATIONS_QUESTIONS: tuple[Question, ...] = (
    _q(
        "Which function prints text to the screen?",
        ("print()", "show()", "display()", "output()"),
        "print()",
        'print("Hello, World!")',
    ),
    _q(
        "Which symbol assigns a value to a variable?",
        ("=", "==", "=>", ":="),
        "=",
        "name ___ 'Alice'",
    ),
    _q(
        "What is the data type of 42?",
        ("int", "str", "float", "bool"),
        "int",
        "x = 42  # type is ___",
    ),
    _q(
        "What is the data type of 3.14?",
        ("float", "int", "str", "double"),
        "float",
        "pi = 3.14  # type is ___",
    ),
    _q(
        "What is the data type of 'hello'?",
        ("str", "text", "char", "string"),
        "str",
        "greeting = 'hello'  # type is ___",
    ),
    _q(
        "Which of these is a boolean value?",
        ("True", "true", "TRUE", "1"),
        "True",
        "is_active = ___",
    ),
    _q(
        "Which function converts '7' (a string) into the integer 7?",
        ("int()", "str()", "float()", "num()"),
        "int()",
        "number = ___('7')",
    ),
    _q(
        "Which function converts 42 into the string '42'?",
        ("str()", "int()", "chr()", "repr()"),
        "str()",
        "text = ___(42)",
    ),
    _q(
        "What is the result of 10 // 3?",
        ("3", "3.33", "1", "0"),
        "3",
        "result = 10 ___ 3  # floor division",
    ),
    _q(
        "What operator gives the remainder of a division?",
        ("%", "//", "/", "**"),
        "%",
        "remainder = 10 ___ 3",
    ),
    _q(
        "What does ** do in Python?",
        ("Exponentiation", "Floor division", "Bitwise XOR", "Modulo"),
        "Exponentiation",
        "result = 2 ** 8  # gives 256",
    ),
    _q(
        "How do you start an f-string?",
        ('f"', '"f', '"', "f'\" (either prefix works)"),
        'f"',
        '___ Hello {name}"',
    ),
    _q(
        "What goes around a variable name inside an f-string?",
        ("{}", "[]", "()", "<>"),
        "{}",
        'f"Hello, ___ name ___!"',
    ),
    _q(
        "Which function tells you the type of a value?",
        ("type()", "typeof()", "kind()", "class()"),
        "type()",
        "___(3.14)  # returns <class 'float'>",
    ),
    _q(
        "What does float('3') return?",
        ("3.0", "3", "'3.0'", "Error"),
        "3.0",
        "result = float('3')  # ___",
    ),
    _q(
        "Which variable name is valid in Python?",
        ("my_score", "my-score", "2score", "my score"),
        "my_score",
    ),
    _q(
        "What is 2 ** 3?",
        ("8", "6", "9", "5"),
        "8",
        "result = 2 ** 3  # ___",
    ),
    _q(
        "Which keyword is used to store a value for later use?",
        ("A variable (just use =)", "store", "let", "var"),
        "A variable (just use =)",
    ),
    _q(
        "What does print(10 / 4) output?",
        ("2.5", "2", "2.0", "Error"),
        "2.5",
        "print(10 / 4)  # ___",
    ),
    _q(
        "How do you combine a number into a string using f-strings?",
        ('f"Score: {score}"', '"Score: " + score', 'f"Score: score"', '"Score: {score}"'),
        'f"Score: {score}"',
    ),
)


# ---------------------------------------------------------------------------
# Exam 2 — Text & Decisions  (Units 2+3)
# ---------------------------------------------------------------------------
_TEXT_DECISIONS_QUESTIONS: tuple[Question, ...] = (
    _q(
        "How do you get the first character of a string?",
        ("s[0]", "s[1]", "s.first()", "s[-1]"),
        "s[0]",
        "first = s___",
    ),
    _q(
        "What does s[-1] return?",
        ("The last character", "The first character", "An error", "Nothing"),
        "The last character",
        "last = s[-1]  # ___",
    ),
    _q(
        "Which method converts a string to uppercase?",
        (".upper()", ".UP()", ".toUpper()", ".capitalize()"),
        ".upper()",
        "result = 'hello'___",
    ),
    _q(
        "Which method removes whitespace from both ends of a string?",
        (".strip()", ".trim()", ".clean()", ".remove()"),
        ".strip()",
        "clean = '  hello  '___",
    ),
    _q(
        "What does 'hello'.replace('l', 'r') return?",
        ("'herro'", "'hello'", "'helo'", "'hrllo'"),
        "'herro'",
        "result = 'hello'.replace('l', 'r')  # ___",
    ),
    _q(
        "Which method splits a string into a list?",
        (".split()", ".divide()", ".cut()", ".break()"),
        ".split()",
        "words = 'a b c'___",
    ),
    _q(
        "How do you join a list of strings with a comma?",
        ("','.join(words)", "words.join(',')", "join(words, ',')", "','.merge(words)"),
        "','.join(words)",
        "result = ___(words)",
    ),
    _q(
        "Which operator checks if two values are equal?",
        ("==", "=", "!=", "==="),
        "==",
        "if score ___ 100:",
    ),
    _q(
        "Which operator checks if two values are NOT equal?",
        ("!=", "!==", "<>", "not ="),
        "!=",
        "if name ___ 'Admin':",
    ),
    _q(
        "What does 'and' do in a condition?",
        ("Both sides must be True", "Either side can be True", "Reverses the condition", "Joins two strings"),
        "Both sides must be True",
        "if age >= 18 and has_id:",
    ),
    _q(
        "What keyword reverses a boolean?",
        ("not", "reverse", "flip", "negate"),
        "not",
        "if ___ is_raining:",
    ),
    _q(
        "What keyword starts a conditional block?",
        ("if", "when", "check", "cond"),
        "if",
        "___ score >= 50:",
    ),
    _q(
        "What keyword runs code when the if condition is False?",
        ("else", "otherwise", "default", "fallback"),
        "else",
        "___ :\n    print('Failed')",
    ),
    _q(
        "What keyword checks an additional condition after if?",
        ("elif", "elseif", "else if", "orif"),
        "elif",
        "___ score >= 70:",
    ),
    _q(
        "Which operator checks if a value is inside a sequence?",
        ("in", "contains", "has", "includes"),
        "in",
        "if 'a' ___ 'banana':",
    ),
    _q(
        "What does 'not in' check?",
        ("Value is absent from a sequence", "Value is present in a sequence", "Logical NOT", "Division remainder"),
        "Value is absent from a sequence",
        "if item ___ basket:",
    ),
    _q(
        "What is s[1:4] called?",
        ("Slicing", "Indexing", "Splitting", "Joining"),
        "Slicing",
        "part = s[1:4]  # ___",
    ),
    _q(
        "What does a conditional expression (ternary) look like?",
        ("x if condition else y", "condition ? x : y", "if condition then x else y", "condition -> x | y"),
        "x if condition else y",
    ),
    _q(
        "What does 'or' return when both sides are False?",
        ("False", "True", "None", "Error"),
        "False",
        "result = False or False  # ___",
    ),
    _q(
        "What is the result of 'hello'[2:4]?",
        ("'ll'", "'el'", "'lo'", "'hel'"),
        "'ll'",
        "result = 'hello'[2:4]  # ___",
    ),
)


# ---------------------------------------------------------------------------
# Exam 3 — Loop Champion  (Unit 4)
# ---------------------------------------------------------------------------
_LOOPS_QUESTIONS: tuple[Question, ...] = (
    _q(
        "Which keyword starts a for loop?",
        ("for", "loop", "repeat", "iterate"),
        "for",
        "___ i in range(5):",
    ),
    _q(
        "What does range(3) produce?",
        ("0, 1, 2", "1, 2, 3", "0, 1, 2, 3", "1, 2"),
        "0, 1, 2",
        "for i in range(3):  # i goes through ___",
    ),
    _q(
        "Which keyword starts a while loop?",
        ("while", "loop", "until", "repeat"),
        "while",
        "___ count < 10:",
    ),
    _q(
        "Which keyword exits a loop immediately?",
        ("break", "exit", "stop", "end"),
        "break",
        "if score > 100:\n    ___",
    ),
    _q(
        "Which keyword skips to the next iteration?",
        ("continue", "skip", "next", "pass"),
        "continue",
        "if item == 'bad':\n    ___",
    ),
    _q(
        "What does enumerate() add to each item in a loop?",
        ("An index", "A key", "A type", "A copy"),
        "An index",
        "for i, item in ___(my_list):",
    ),
    _q(
        "What is range(2, 6)?",
        ("2, 3, 4, 5", "2, 3, 4, 5, 6", "0, 1, 2, 3, 4, 5", "2, 4, 6"),
        "2, 3, 4, 5",
        "for i in range(2, 6):  # i goes through ___",
    ),
    _q(
        "How many times does this loop run? for i in range(0, 10, 2)",
        ("5", "10", "4", "6"),
        "5",
        "for i in range(0, 10, 2):  # runs ___ times",
    ),
    _q(
        "What is a nested loop?",
        ("A loop inside another loop", "A loop with a condition", "A loop that runs once", "A loop with break"),
        "A loop inside another loop",
    ),
    _q(
        "What does a while loop check before each iteration?",
        ("A condition", "A counter", "A list", "An index"),
        "A condition",
        "while ___:",
    ),
    _q(
        "Which loop is best when you know how many times to repeat?",
        ("for loop", "while loop", "do-while loop", "repeat loop"),
        "for loop",
    ),
    _q(
        "What does 'for item in my_list' do?",
        ("Loops over each element", "Loops over indices", "Loops a fixed number of times", "Loops forever"),
        "Loops over each element",
        "for ___ in my_list:",
    ),
    _q(
        "How do you loop through a string character by character?",
        ("for ch in my_string:", "for i in len(my_string):", "while my_string:", "for my_string:"),
        "for ch in my_string:",
    ),
    _q(
        "What happens when a while loop's condition becomes False?",
        ("The loop stops", "The loop restarts", "Python raises an error", "The loop runs once more"),
        "The loop stops",
    ),
    _q(
        "What does range(5, 0, -1) produce?",
        ("5, 4, 3, 2, 1", "0, 1, 2, 3, 4", "5, 4, 3, 2, 1, 0", "4, 3, 2, 1"),
        "5, 4, 3, 2, 1",
        "for i in range(5, 0, -1):  # ___",
    ),
    _q(
        "Which built-in pairs each item with its position?",
        ("enumerate()", "index()", "position()", "range()"),
        "enumerate()",
        "for i, name in ___(names):",
    ),
    _q(
        "What does 'continue' do inside a loop?",
        ("Skips the rest of this iteration", "Exits the loop", "Restarts the loop from the top", "Pauses the loop"),
        "Skips the rest of this iteration",
    ),
    _q(
        "What is printed by: for i in range(3): print(i)?",
        ("0 1 2", "1 2 3", "0 1 2 3", "1 2"),
        "0 1 2",
        "for i in range(3):\n    print(i)  # prints ___",
    ),
    _q(
        "How do you loop with both index and value?",
        ("for i, v in enumerate(lst):", "for i, v in range(lst):", "for i in index(lst):", "for v at i in lst:"),
        "for i, v in enumerate(lst):",
    ),
    _q(
        "What keyword is used to define the body of a loop?",
        ("Indentation (no keyword)", "do", "begin", "then"),
        "Indentation (no keyword)",
    ),
)


# ---------------------------------------------------------------------------
# Exam 4 — Data Wrangler  (Unit 5)
# ---------------------------------------------------------------------------
_COLLECTIONS_QUESTIONS: tuple[Question, ...] = (
    _q(
        "Which brackets create a list?",
        ("[]", "{}", "()", "<>"),
        "[]",
        "fruits = ___ 'apple', 'banana' ___",
    ),
    _q(
        "Which method adds an item to the end of a list?",
        (".append()", ".add()", ".push()", ".insert()"),
        ".append()",
        "fruits___('cherry')",
    ),
    _q(
        "Which method removes and returns the last item of a list?",
        (".pop()", ".remove()", ".delete()", ".discard()"),
        ".pop()",
        "last = fruits___()",
    ),
    _q(
        "How do you get items 1 through 3 from a list?",
        ("lst[1:4]", "lst[1:3]", "lst[1-3]", "lst.slice(1,3)"),
        "lst[1:4]",
        "chunk = lst___",
    ),
    _q(
        "What does a list comprehension look like?",
        ("[x*2 for x in nums]", "{x*2 for x in nums}", "(x*2 for x in nums)", "map(x*2, nums)"),
        "[x*2 for x in nums]",
    ),
    _q(
        "Which collection type cannot be changed after creation?",
        ("tuple", "list", "set", "dict"),
        "tuple",
        "point = (3, 4)  # this is a ___",
    ),
    _q(
        "How do you unpack a tuple (a, b) = ?",
        ("(a, b) = my_tuple", "a = my_tuple[0]; b = my_tuple[1]", "unpack(my_tuple, a, b)", "a, b := my_tuple"),
        "(a, b) = my_tuple",
    ),
    _q(
        "Which collection stores only unique values?",
        ("set", "list", "tuple", "dict"),
        "set",
        "unique = ___ {1, 2, 2, 3} ___  # {1, 2, 3}",
    ),
    _q(
        "Which brackets create a dictionary?",
        ("{}", "[]", "()", "dict[]"),
        "{}",
        "person = ___ 'name': 'Alice' ___",
    ),
    _q(
        "How do you access the value for key 'age' in a dict d?",
        ("d['age']", "d.age", "d->age", "d{age}"),
        "d['age']",
        "age = person___",
    ),
    _q(
        "Which method returns all keys of a dictionary?",
        (".keys()", ".all()", ".index()", ".fields()"),
        ".keys()",
        "for k in person___:",
    ),
    _q(
        "Which method returns key-value pairs for looping?",
        (".items()", ".pairs()", ".entries()", ".tuples()"),
        ".items()",
        "for k, v in person___:",
    ),
    _q(
        "What does set.add() do?",
        ("Adds one element to the set", "Adds a list of elements", "Replaces an element", "Clears the set"),
        "Adds one element to the set",
        "my_set.___('new')",
    ),
    _q(
        "What does list.sort() do to the list?",
        ("Sorts it in place", "Returns a new sorted list", "Sorts in reverse", "Raises an error"),
        "Sorts it in place",
        "numbers.___()",
    ),
    _q(
        "How do you check the number of items in a list?",
        ("len(lst)", "lst.length", "lst.size()", "count(lst)"),
        "len(lst)",
        "n = ___(fruits)",
    ),
    _q(
        "What is a nested list?",
        ("A list that contains other lists", "A sorted list", "A list with no duplicates", "A list inside a dict"),
        "A list that contains other lists",
    ),
    _q(
        "What does dict.get('key', default) do?",
        ("Returns value or default if key missing", "Raises KeyError if missing", "Deletes the key", "Returns the key"),
        "Returns value or default if key missing",
        "age = person.___(  'age', 0  )",
    ),
    _q(
        "Which method returns all values of a dictionary?",
        (".values()", ".items()", ".keys()", ".get()"),
        ".values()",
        "for v in person___:",
    ),
    _q(
        "What is tuple unpacking?",
        ("Assigning tuple elements to variables in one line", "Converting a tuple to a list", "Removing items from a tuple", "Printing a tuple"),
        "Assigning tuple elements to variables in one line",
        "x, y ___ (10, 20)",
    ),
    _q(
        "What does [x for x in range(5) if x % 2 == 0] produce?",
        ("[0, 2, 4]", "[1, 3]", "[0, 1, 2, 3, 4]", "[2, 4]"),
        "[0, 2, 4]",
        "evens = [x for x in range(5) if x % 2 == 0]  # ___",
    ),
)


# ---------------------------------------------------------------------------
# Exam 5 — Code Architect  (Units 6+7)
# ---------------------------------------------------------------------------
_FUNCTIONS_OOP_QUESTIONS: tuple[Question, ...] = (
    _q(
        "Which keyword defines a function?",
        ("def", "fun", "func", "define"),
        "def",
        "___ greet(name):",
    ),
    _q(
        "Which keyword sends a value back from a function?",
        ("return", "send", "output", "give"),
        "return",
        "def add(a, b):\n    ___ a + b",
    ),
    _q(
        "How do you give a parameter a default value?",
        ("def f(x=10):", "def f(x default 10):", "def f(x|10):", "def f(x:10):"),
        "def f(x=10):",
    ),
    _q(
        "What does a function return if there is no return statement?",
        ("None", "0", "False", "Error"),
        "None",
        "def do_nothing():\n    pass\nresult = do_nothing()  # ___",
    ),
    _q(
        "How do you return two values from a function?",
        ("return a, b", "return [a, b]", "return (a) (b)", "double return a b"),
        "return a, b",
        "def minmax(lst):\n    ___ min(lst), max(lst)",
    ),
    _q(
        "What is recursion?",
        ("A function that calls itself", "A loop inside a function", "A function with no return", "A class method"),
        "A function that calls itself",
    ),
    _q(
        "What does *args allow?",
        ("Any number of positional arguments", "Any number of keyword arguments", "A single tuple argument", "Default arguments"),
        "Any number of positional arguments",
        "def f(___args):",
    ),
    _q(
        "What does **kwargs allow?",
        ("Any number of keyword arguments", "Any number of positional arguments", "A single dict argument", "Default arguments"),
        "Any number of keyword arguments",
        "def f(___kwargs):",
    ),
    _q(
        "Which keyword starts a class definition?",
        ("class", "Class", "def class", "object"),
        "class",
        "___ Dog:",
    ),
    _q(
        "What is __init__ used for?",
        ("To initialise a new object's attributes", "To destroy an object", "To print the object", "To copy the object"),
        "To initialise a new object's attributes",
        "def ___(self, name):",
    ),
    _q(
        "What does 'self' refer to inside a class method?",
        ("The current object instance", "The class itself", "The parent class", "The return value"),
        "The current object instance",
        "def bark(___):  # refers to the dog object",
    ),
    _q(
        "How do you create an instance of a class Dog?",
        ("dog = Dog()", "dog = new Dog()", "dog = Dog.create()", "dog = Dog.new()"),
        "dog = Dog()",
    ),
    _q(
        "How do you access attribute 'name' on object dog?",
        ("dog.name", "dog[name]", "dog->name", "Dog.name"),
        "dog.name",
        "print(___)",
    ),
    _q(
        "How does a child class inherit from a parent?",
        ("class Child(Parent):", "class Child extends Parent:", "class Child inherits Parent:", "class Child <- Parent:"),
        "class Child(Parent):",
    ),
    _q(
        "What does super() do in a child class?",
        ("Calls the parent class's method", "Creates a copy of the parent", "Deletes the parent", "Returns the parent class"),
        "Calls the parent class's method",
        "def __init__(self):\n    ___().__init__()",
    ),
    _q(
        "Which value represents 'nothing' in Python?",
        ("None", "null", "undefined", "0"),
        "None",
        "result = None  # ___",
    ),
    _q(
        "How do you call a method 'bark' on object dog?",
        ("dog.bark()", "bark(dog)", "dog->bark()", "Dog.bark()"),
        "dog.bark()",
    ),
    _q(
        "What is a method?",
        ("A function defined inside a class", "A variable inside a class", "A class with one function", "A built-in function"),
        "A function defined inside a class",
    ),
    _q(
        "What does 'return a, b' actually return?",
        ("A tuple (a, b)", "Two separate values", "A list [a, b]", "A dict {'a': a, 'b': b}"),
        "A tuple (a, b)",
        "result = func()  # result is ___",
    ),
    _q(
        "What is the base class of all Python classes if none is specified?",
        ("object", "Base", "Class", "Root"),
        "object",
        "class Dog:  # implicitly inherits from ___",
    ),
)


# ---------------------------------------------------------------------------
# Exam 6 — Python Pro  (Units 8+9+10)
# ---------------------------------------------------------------------------
_ADVANCED_QUESTIONS: tuple[Question, ...] = (
    _q(
        "What does a lambda function look like?",
        ("lambda x: x * 2", "def lambda x: x * 2", "x -> x * 2", "fn x => x * 2"),
        "lambda x: x * 2",
    ),
    _q(
        "What does map(func, lst) do?",
        ("Applies func to every element", "Filters elements by func", "Sorts elements by func", "Zips two lists"),
        "Applies func to every element",
        "doubled = ___(lambda x: x*2, numbers)",
    ),
    _q(
        "What does filter(func, lst) do?",
        ("Keeps elements where func returns True", "Applies func to every element", "Sorts by func", "Removes duplicates"),
        "Keeps elements where func returns True",
        "evens = ___(lambda x: x%2==0, numbers)",
    ),
    _q(
        "How do you sort a list of strings by length?",
        ("sorted(words, key=len)", "sorted(words, len)", "words.sort(key=len)", "sorted(words, by=len)"),
        "sorted(words, key=len)",
    ),
    _q(
        "What does zip(a, b) produce?",
        ("Pairs of items from a and b", "A merged list", "A dict from two lists", "The shortest list"),
        "Pairs of items from a and b",
        "for x, y in ___(list_a, list_b):",
    ),
    _q(
        "What is a decorator?",
        ("A function that wraps another function", "A class method", "A type annotation", "A string prefix"),
        "A function that wraps another function",
        "@___ \ndef my_func(): ...",
    ),
    _q(
        "What is a closure?",
        ("A function that remembers variables from its enclosing scope", "A class with private methods", "A function with no return", "A loop that closes automatically"),
        "A function that remembers variables from its enclosing scope",
    ),
    _q(
        "How do you apply a decorator named 'timer' to a function?",
        ("@timer", "@timer()", "decorator(timer)", "timer.apply()"),
        "@timer",
        "___ \ndef slow_func(): ...",
    ),
    _q(
        "What keyword makes a function a generator?",
        ("yield", "return", "generate", "produce"),
        "yield",
        "def count_up():\n    for i in range(5):\n        ___ i",
    ),
    _q(
        "What is the difference between yield and return?",
        ("yield pauses and resumes; return ends the function", "yield ends the function; return pauses", "They are identical", "yield returns a list; return returns one value"),
        "yield pauses and resumes; return ends the function",
    ),
    _q(
        "What does a generator expression look like?",
        ("(x*2 for x in nums)", "[x*2 for x in nums]", "{x*2 for x in nums}", "gen(x*2 for x in nums)"),
        "(x*2 for x in nums)",
    ),
    _q(
        "Which keyword starts an error-handling block?",
        ("try", "catch", "handle", "except"),
        "try",
        "___:\n    risky_code()",
    ),
    _q(
        "Which keyword catches an exception?",
        ("except", "catch", "handle", "on_error"),
        "except",
        "___ ValueError as e:",
    ),
    _q(
        "Which block always runs, whether or not an error occurred?",
        ("finally", "else", "always", "cleanup"),
        "finally",
        "try:\n    ...\nexcept:\n    ...\n___:",
    ),
    _q(
        "Which keyword raises an exception deliberately?",
        ("raise", "throw", "error", "fail"),
        "raise",
        "___ ValueError('Too small')",
    ),
    _q(
        "What does the 'else' clause after try/except mean?",
        ("Runs only if no exception was raised", "Runs only if an exception was raised", "Always runs", "Handles a specific error"),
        "Runs only if no exception was raised",
        "try:\n    ...\nexcept:\n    ...\n___:\n    print('success')",
    ),
    _q(
        "How do you get the next value from a generator?",
        ("next(gen)", "gen.next()", "gen()", "iter(gen)"),
        "next(gen)",
        "value = ___(my_generator)",
    ),
    _q(
        "What does iter() do?",
        ("Returns an iterator object from an iterable", "Returns the next value", "Creates a generator", "Converts to a list"),
        "Returns an iterator object from an iterable",
        "it = ___(my_list)",
    ),
    _q(
        "What is a dict comprehension?",
        ("{k: v for k, v in items}", "[k: v for k, v in items]", "(k: v for k, v in items)", "{k, v for k, v in items}"),
        "{k: v for k, v in items}",
    ),
    _q(
        "What exception is raised when you access a dict key that doesn't exist?",
        ("KeyError", "IndexError", "ValueError", "TypeError"),
        "KeyError",
        "d = {}\nd['missing']  # raises ___",
    ),
)


# ---------------------------------------------------------------------------
# Exam registry
# ---------------------------------------------------------------------------
EXAMS: dict[str, Exam] = {
    e.key: e for e in (
        Exam(
            key="foundations",
            title="Foundations Exam",
            badge_emoji="🏅",
            badge_name="Python Foundations",
            trigger_topic="exercise_profile_card",
            questions=_FOUNDATIONS_QUESTIONS,
        ),
        Exam(
            key="text_decisions",
            title="Text & Decisions Exam",
            badge_emoji="🎯",
            badge_name="Logic Master",
            trigger_topic="exercise_grade_checker",
            questions=_TEXT_DECISIONS_QUESTIONS,
        ),
        Exam(
            key="loops",
            title="Loop Champion Exam",
            badge_emoji="🔁",
            badge_name="Loop Champion",
            trigger_topic="exercise_pattern_printer",
            questions=_LOOPS_QUESTIONS,
        ),
        Exam(
            key="collections",
            title="Data Wrangler Exam",
            badge_emoji="📦",
            badge_name="Data Wrangler",
            trigger_topic="exercise_inventory",
            questions=_COLLECTIONS_QUESTIONS,
        ),
        Exam(
            key="functions_oop",
            title="Code Architect Exam",
            badge_emoji="⚙️",
            badge_name="Code Architect",
            trigger_topic="exercise_class_design",
            questions=_FUNCTIONS_OOP_QUESTIONS,
        ),
        Exam(
            key="advanced",
            title="Python Pro Exam",
            badge_emoji="🚀",
            badge_name="Python Pro",
            trigger_topic="exercise_custom_range",
            questions=_ADVANCED_QUESTIONS,
        ),
    )
}

# Ordered list for display purposes (unlock order)
EXAM_ORDER: tuple[str, ...] = (
    "foundations",
    "text_decisions",
    "loops",
    "collections",
    "functions_oop",
    "advanced",
)
