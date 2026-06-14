from __future__ import annotations

import ast

from techtales.models import ExecutionResult, RequirementResult, Topic, ValidationResult


GENERIC_NAMES = {
    "a",
    "b",
    "c",
    "data",
    "foo",
    "item",
    "n",
    "num",
    "temp",
    "tmp",
    "value",
    "var",
    "x",
    "y",
    "z",
}

ALLOWED_SHORT_NAMES = {"xp", "id", "db", "hp", "mp"}


class ChallengeValidator:
    def validate(self, topic: Topic, submitted_code: str, execution_result: ExecutionResult | None = None) -> ValidationResult:
        if topic.key == "variables":
            return validate_variables_challenge(submitted_code, execution_result)
        if topic.key == "loops":
            return validate_loops_challenge(submitted_code, execution_result)
        if topic.key == "f_strings":
            return validate_fstrings_challenge(submitted_code, execution_result)
        if topic.key == "write_a_program":
            return validate_write_a_program_challenge(submitted_code, execution_result)
        if topic.key == "elif":
            return validate_elif_challenge(submitted_code, execution_result)
        if topic.key == "lists":
            return validate_lists_challenge(submitted_code, execution_result)
        if topic.key == "dictionaries":
            return validate_dictionaries_challenge(submitted_code, execution_result)
        if topic.key == "string_methods":
            return validate_string_methods_challenge(submitted_code, execution_result)
        if topic.key == "while_loops":
            return validate_while_loops_challenge(submitted_code, execution_result)
        if topic.key == "type_conversion":
            return validate_type_conversion_challenge(submitted_code, execution_result)

        has_code = bool(submitted_code.strip())
        return ValidationResult(
            passed=has_code,
            requirements=(
                RequirementResult(
                    "Submitted Python code",
                    has_code,
                    "Type a few lines of Python code before submitting.",
                ),
            ),
            feedback="Your work was saved. More detailed checks for this topic will be added soon.",
        )


def validate_variables_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("Code can be read as Python", False, "Fix the syntax error so Python can parse the submission."),
                RequirementResult("At least one string variable was created", False, "Assign text in quotes to a variable, such as character_name = \"Ari\"."),
                RequirementResult("At least one integer variable was created", False, "Assign a whole number without quotes, such as badges_earned = 3."),
                RequirementResult("Variables use meaningful names", False, "Use descriptive names like character_name or badges_earned instead of x or var."),
                RequirementResult("print() is used", False, "Call print() to show the values you created."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    assignments = _collect_assignments(tree)
    variable_names = tuple(assignments)
    string_variables = {
        name: value.value
        for name, value in assignments.items()
        if isinstance(value, ast.Constant) and isinstance(value.value, str)
    }
    integer_variables = {
        name: value.value
        for name, value in assignments.items()
        if isinstance(value, ast.Constant)
        and isinstance(value.value, int)
        and not isinstance(value.value, bool)
    }
    empty_string_names = tuple(name for name, value in string_variables.items() if not value.strip())
    non_empty_string_names = tuple(name for name, value in string_variables.items() if value.strip())
    output_names, has_meaningful_print_output = _inspect_print_output(tree)
    stdout = execution_result.stdout if execution_result else ""
    printed_values = _printed_non_empty_lines(stdout)
    challenge_variable_names = tuple(non_empty_string_names) + tuple(integer_variables)
    variables_used_in_output = bool(challenge_variable_names) and all(
        name in output_names for name in challenge_variable_names
    )
    variable_values_printed = bool(challenge_variable_names) and all(
        str(assignments[name].value) in stdout
        for name in challenge_variable_names
        if isinstance(assignments[name], ast.Constant)
    )

    has_non_empty_string = bool(non_empty_string_names)
    has_integer = bool(integer_variables)
    has_meaningful_names = bool(variable_names) and all(_is_meaningful_name(name) for name in variable_names)

    requirements = (
        RequirementResult(
            "String variable created",
            has_non_empty_string,
            _string_suggestion(empty_string_names),
        ),
        RequirementResult(
            "Integer variable created",
            has_integer,
            "Assign a whole number without quotes, such as badges_earned = 3.",
        ),
        RequirementResult(
            "Variables use meaningful names",
            has_meaningful_names,
            "Use descriptive names like character_name or badges_earned instead of x, var, or temp.",
        ),
        RequirementResult(
            "print() has output",
            has_meaningful_print_output and bool(printed_values),
            "Put a variable or meaningful message inside print(), such as print(character_name, badges_earned).",
        ),
        RequirementResult(
            "Variables are used in output",
            variables_used_in_output and variable_values_printed,
            "Print both variables so the output shows the character name and badge count.",
        ),
    )
    passed = all(requirement.passed for requirement in requirements)

    if passed:
        feedback = "Excellent work. Your variables are named clearly, store useful values, and share the result with print()."
    else:
        feedback = "Nice start. Review the red items below, make the suggested changes, then submit again."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def validate_loops_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("Code can be read as Python", False, "Fix the syntax error so Python can parse the submission."),
                RequirementResult("A loop is used", False, "Use a for loop, such as for step in range(1, 4):"),
                RequirementResult("Output includes three steps", False, "Print one line for each of the three training steps."),
                RequirementResult("Step numbers appear in output", False, "Use an f-string like print(f\"Reading Step {step}\")."),
            ),
            feedback="Python could not read this loop yet. Check the syntax, then try again.",
        )

    stdout = execution_result.stdout if execution_result else ""
    output_lines = _printed_non_empty_lines(stdout)
    has_for_loop = any(isinstance(node, ast.For) for node in ast.walk(tree))
    has_print_in_loop = any(
        isinstance(child, ast.Call)
        and isinstance(child.func, ast.Name)
        and child.func.id == "print"
        for node in ast.walk(tree)
        if isinstance(node, ast.For)
        for child in ast.walk(node)
    )
    has_three_lines = len(output_lines) >= 3
    has_step_numbers = all(str(number) in stdout for number in (1, 2, 3))
    has_literal_placeholder = any("[step]" in line or "{step}" in line for line in output_lines)

    requirements = (
        RequirementResult(
            "A loop is used",
            has_for_loop,
            "Use a for loop so Python repeats the training-step message for you.",
        ),
        RequirementResult(
            "print() is inside the loop",
            has_print_in_loop,
            "Indent print() under the for loop so it runs once for each step.",
        ),
        RequirementResult(
            "Output includes three steps",
            has_three_lines,
            "Use range(1, 4) or another three-step sequence so the program prints three lines.",
        ),
        RequirementResult(
            "Step numbers appear in output",
            has_step_numbers and not has_literal_placeholder,
            _loop_step_suggestion(has_literal_placeholder),
        ),
    )
    passed = all(requirement.passed for requirement in requirements)

    if passed:
        feedback = "Great loop. The program repeats the message and the output shows each step number."
    else:
        feedback = "Nice start. Compare your program output with the failed checks below, then adjust the loop."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def validate_fstrings_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("Code can be read as Python", False, "Fix the syntax error so Python can parse the submission."),
                RequirementResult("An f-string is used", False, 'Add an f-string, for example: print(f"Hello {name}!")'),
                RequirementResult("f-string contains a placeholder", False, 'Put a variable inside {} in your f-string, for example: f"Hello {name}!"'),
                RequirementResult("A text variable is used in the f-string", False, 'Assign a name to a variable and include it in {}, for example: learner_name = "Ari".'),
                RequirementResult("A number variable is used in the f-string", False, "Assign a number to a variable and include it in {}, for example: xp = 100."),
                RequirementResult("Output is printed", False, "Call print() with your f-string to show the result."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    fstrings = [node for node in ast.walk(tree) if isinstance(node, ast.JoinedStr)]
    has_fstring = bool(fstrings)
    has_placeholder = any(
        any(isinstance(part, ast.FormattedValue) for part in fstring.values)
        for fstring in fstrings
    )

    fstring_var_names: set[str] = set()
    for fstring in fstrings:
        for node in ast.walk(fstring):
            if isinstance(node, ast.FormattedValue):
                for name_node in ast.walk(node):
                    if isinstance(name_node, ast.Name):
                        fstring_var_names.add(name_node.id)

    assignments = _collect_assignments(tree)
    string_vars = {
        name for name, value in assignments.items()
        if isinstance(value, ast.Constant) and isinstance(value.value, str) and value.value.strip()
    }
    number_vars = {
        name for name, value in assignments.items()
        if isinstance(value, ast.Constant)
        and isinstance(value.value, (int, float))
        and not isinstance(value.value, bool)
    }

    uses_string_var = bool(string_vars & fstring_var_names)
    uses_number_var = bool(number_vars & fstring_var_names)

    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult(
            "An f-string is used",
            has_fstring,
            'Start a string with f to make it an f-string, for example: f"Hello {name}!"',
        ),
        RequirementResult(
            "f-string contains a placeholder",
            has_placeholder,
            'Put a variable name inside {} in your f-string, for example: f"Score: {xp}"',
        ),
        RequirementResult(
            "A text variable is used in the f-string",
            uses_string_var,
            'Assign a name to a variable and include it in {}, for example: learner_name = "Ari" then f"{learner_name}".',
        ),
        RequirementResult(
            "A number variable is used in the f-string",
            uses_number_var,
            "Assign a number to a variable and include it in {}, for example: xp = 100 then f\"{xp}\".",
        ),
        RequirementResult(
            "Output is printed",
            has_output,
            "Call print() with your f-string so the sentence appears on screen.",
        ),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Well done. Your f-string combines both variables into one clean sentence."
    else:
        feedback = "Good start. Review the checks below and update your f-string, then submit again."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def validate_elif_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("An if statement is used", False, "Start with if score >= 90: to check the first condition."),
                RequirementResult("An elif branch is used", False, "Add elif score >= 80: after the if block for the next condition."),
                RequirementResult("An else branch is used", False, "Add else: at the end to catch anything that didn't match."),
                RequirementResult("Program produces output", False, "Make sure each branch has a print() statement inside it."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    if_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.If)]
    has_if = bool(if_nodes)
    has_elif = any(
        len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If)
        for node in if_nodes
    )
    has_else = any(
        node.orelse and not (len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If))
        for node in if_nodes
    )

    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult("An if statement is used", has_if, "Start with if score >= 90: to check the first condition."),
        RequirementResult("An elif branch is used", has_elif, "After your if block, add elif score >= 80: at the same indent level."),
        RequirementResult("An else branch is used", has_else, "Add else: at the end as the catch-all for any score that didn't match."),
        RequirementResult("Program produces output", has_output, "Each branch needs a print() statement inside it, indented 4 spaces."),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Clean conditional chain. Your program now handles multiple conditions without nested if/else."
    else:
        feedback = "Check the red items. Make sure you have if, elif, and else — each with a print() inside."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def validate_lists_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("A list is created", False, 'Create a list: quest_items = ["Map", "Torch", "Key"]'),
                RequirementResult("The list has at least 3 items", False, "Add at least 3 items inside the brackets, separated by commas."),
                RequirementResult("len() is used", False, "Call len(quest_items) to count the items."),
                RequirementResult("An item is accessed by index", False, "Access an item with quest_items[0] — index 0 is the first item."),
                RequirementResult("Output is printed", False, "Add print() to show the list, its length, or an item."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    list_literals = [n for n in ast.walk(tree) if isinstance(n, ast.List)]
    has_list = bool(list_literals)
    has_three_items = any(len(n.elts) >= 3 for n in list_literals)
    has_len = any(
        isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "len"
        for n in ast.walk(tree)
    )
    has_index = any(isinstance(n, ast.Subscript) for n in ast.walk(tree))
    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult("A list is created", has_list, 'Create a list using square brackets: quest_items = ["Map", "Torch", "Key"]'),
        RequirementResult("The list has at least 3 items", has_three_items, "Add at least 3 items inside the brackets, separated by commas."),
        RequirementResult("len() is used", has_len, "Call len(quest_items) to find out how many items are in the list."),
        RequirementResult("An item is accessed by index", has_index, "Access an item by position: quest_items[0] gives the first item."),
        RequirementResult("Output is printed", has_output, "Wrap your results in print() to see the list, its length, and an item."),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Well done. You created, measured, and accessed a list — the three core list operations."
    else:
        feedback = "Good start. Make sure your list has 3+ items, a len() call, and an index access."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def validate_dictionaries_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("A dictionary is created", False, 'Create a dictionary: character = {"name": "Ari", "level": 5, "skill": "Python"}'),
                RequirementResult("The dictionary has at least 3 keys", False, "Add at least 3 key-value pairs inside the curly braces."),
                RequirementResult("A value is accessed by key", False, 'Access a value with: character["name"]'),
                RequirementResult("Output is printed", False, 'Wrap your result in print() to show a value.'),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    dict_literals = [n for n in ast.walk(tree) if isinstance(n, ast.Dict)]
    has_dict = bool(dict_literals)
    has_three_keys = any(len(n.keys) >= 3 for n in dict_literals)
    has_key_access = any(isinstance(n, ast.Subscript) for n in ast.walk(tree))
    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult("A dictionary is created", has_dict, 'Create a dictionary: character = {"name": "Ari", "level": 5, "skill": "Python"}'),
        RequirementResult("The dictionary has at least 3 keys", has_three_keys, "Add at least 3 key-value pairs inside the curly braces, separated by commas."),
        RequirementResult("A value is accessed by key", has_key_access, 'Access a value with: character["name"]. Put the key name in square brackets.'),
        RequirementResult("Output is printed", has_output, 'Wrap your result in print() to show a value: print(character["name"])'),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Solid dictionary work. Named access is what makes dictionaries more readable than lists for structured data."
    else:
        feedback = "Check the requirements. Make sure your dictionary has 3+ keys and you access at least one value."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


_STRING_METHODS = {
    "upper", "lower", "replace", "split", "strip", "join",
    "title", "count", "startswith", "endswith", "find", "format",
}


def validate_string_methods_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("A text variable is created", False, 'Assign a string: message = "Hello, World!"'),
                RequirementResult("At least one string method is used", False, "Call a method on your string: message.upper()"),
                RequirementResult("At least two string methods are used", False, "Try a second method: message.lower() or message.replace(\"old\", \"new\")"),
                RequirementResult("Output is printed", False, "Wrap your transformed text in print() to see the result."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    method_calls = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr in _STRING_METHODS
    ]
    has_string_var = any(
        isinstance(n, ast.Assign)
        and any(
            isinstance(v, ast.Constant) and isinstance(v.value, str)
            for v in ast.walk(n.value)
        )
        for n in ast.walk(tree)
    )
    has_one_method = len(method_calls) >= 1
    has_two_methods = len(method_calls) >= 2
    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult("A text variable is created", has_string_var, 'Assign a string to a variable first: message = "Hello, World!"'),
        RequirementResult("At least one string method is used", has_one_method, "Call a method on your string: message.upper() converts all letters to uppercase."),
        RequirementResult("At least two string methods are used", has_two_methods, 'Try a second method: message.lower() or message.replace("old", "new").'),
        RequirementResult("Output is printed", has_output, "Wrap your transformed text in print() to see the result on screen."),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Great. You've started using Python's built-in string toolkit — these will come up in almost every real project."
    else:
        feedback = "Close. Make sure you have a text variable, call at least two string methods, and print the results."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def validate_while_loops_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("A while loop is used", False, "Use while count <= 5: to keep repeating until the condition is False."),
                RequirementResult("print() is inside the while loop", False, "Indent your print() by 4 spaces inside the while loop."),
                RequirementResult("The loop variable is updated", False, "Add count = count + 1 inside the loop so it eventually stops."),
                RequirementResult("Output has multiple lines", False, "Your loop should print one value per iteration."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    while_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.While)]
    has_while = bool(while_nodes)
    has_print_in_while = any(
        isinstance(child, ast.Call)
        and isinstance(child.func, ast.Name)
        and child.func.id == "print"
        for node in while_nodes
        for child in ast.walk(node)
    )
    has_update = any(
        isinstance(child, (ast.AugAssign, ast.Assign))
        for node in while_nodes
        for child in ast.walk(node)
    )
    stdout = execution_result.stdout if execution_result else ""
    output_lines = _printed_non_empty_lines(stdout)
    has_multiple_output = len(output_lines) >= 3

    requirements = (
        RequirementResult("A while loop is used", has_while, "Use while count <= 5: to keep repeating until the condition becomes False."),
        RequirementResult("print() is inside the while loop", has_print_in_while, "Indent your print() by 4 spaces inside the while loop so it runs each iteration."),
        RequirementResult("The loop variable is updated", has_update, "Add count = count + 1 inside the loop. Without this, the condition never changes and the loop runs forever."),
        RequirementResult("Output has multiple lines", has_multiple_output, "Your output should show several values — one per iteration of the loop."),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Great while loop. You set the condition, printed each value, and updated the counter — every while loop needs all three."
    else:
        feedback = "Almost there. Check that your while loop has a condition, a print() inside, and updates the counter each time."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def validate_type_conversion_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("String variables are defined", False, 'Define your text values as strings: price_text = "25"'),
                RequirementResult("A type conversion function is used", False, "Use int() to turn text into a number: int(price_text)"),
                RequirementResult("Arithmetic is performed", False, "Multiply or add your converted numbers together to calculate a total."),
                RequirementResult("Output is printed", False, "Use print() or an f-string to show the calculated result."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    _CONVERSION_FUNCS = {"int", "float", "str"}
    has_conversion = any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name)
        and n.func.id in _CONVERSION_FUNCS
        for n in ast.walk(tree)
    )
    has_string_input = any(
        isinstance(n, ast.Assign)
        and any(
            isinstance(v, ast.Constant) and isinstance(v.value, str) and v.value.strip()
            for v in ast.walk(n.value)
        )
        for n in ast.walk(tree)
    )
    has_arithmetic = any(isinstance(n, ast.BinOp) for n in ast.walk(tree))
    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult("String variables are defined", has_string_input, 'Define your text values as strings: price_text = "25". The quotes mark it as text, not a number.'),
        RequirementResult("A type conversion function is used", has_conversion, "Use int() to turn text into a number: price = int(price_text). Now Python can do maths with it."),
        RequirementResult("Arithmetic is performed", has_arithmetic, "Once converted, multiply: total = price * quantity. Python can only multiply numbers, not strings."),
        RequirementResult("Output is printed", has_output, 'Use print() or an f-string to show the result: print(f"Total: {total}")'),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Good conversion work. int() and str() are the glue that connects text input to numerical computation."
    else:
        feedback = "Close. Convert your string values with int() or float(), then use them in a calculation and print the result."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def validate_write_a_program_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("A print() statement is used", False, 'Use print() to send your message to the screen: print("Hello, World!")'),
                RequirementResult('Output includes "Hello"', False, "Make sure your output contains the word Hello."),
                RequirementResult('Output includes "World"', False, "Make sure your output contains the word World."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    has_print = any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "print"
        for node in ast.walk(tree)
    )

    stdout = execution_result.stdout if execution_result else ""
    has_hello = "hello" in stdout.lower()
    has_world = "world" in stdout.lower()

    requirements = (
        RequirementResult(
            "A print() statement is used",
            has_print,
            'Use print() to send a message to the screen, for example: print("Hello, World!")',
        ),
        RequirementResult(
            'Output includes "Hello"',
            has_hello,
            'Your output needs to include the word Hello. Try: print("Hello, World!")',
        ),
        RequirementResult(
            'Output includes "World"',
            has_world,
            'Your output needs to include the word World. Try: print("Hello, World!")',
        ),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "You did it. You've written and run a complete Python program. Welcome to the world of programming."
    else:
        feedback = "Nearly there. Check the requirements below and update your program."

    return ValidationResult(passed=passed, requirements=requirements, feedback=feedback)


def _collect_assignments(tree: ast.AST) -> dict[str, ast.AST]:
    assignments: dict[str, ast.AST] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments[target.id] = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            assignments[node.target.id] = node.value
    return assignments


def _inspect_print_output(tree: ast.AST) -> tuple[set[str], bool]:
    output_names: set[str] = set()
    has_meaningful_output = False

    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "print"
        ):
            continue

        for argument in node.args:
            output_names.update(
                name_node.id
                for name_node in ast.walk(argument)
                if isinstance(name_node, ast.Name)
            )
            if _is_meaningful_print_argument(argument):
                has_meaningful_output = True

    return output_names, has_meaningful_output


def _printed_non_empty_lines(stdout: str) -> tuple[str, ...]:
    return tuple(line.strip() for line in stdout.splitlines() if line.strip())


def _is_meaningful_print_argument(argument: ast.AST) -> bool:
    if isinstance(argument, ast.Name):
        return True
    if isinstance(argument, ast.Constant):
        if isinstance(argument.value, str):
            return bool(argument.value.strip())
        return argument.value is not None
    return True


def _string_suggestion(empty_string_names: tuple[str, ...]) -> str:
    if empty_string_names:
        variable_name = empty_string_names[0]
        return f"Give {variable_name} a value, such as {variable_name} = \"Ari\"."
    return "Assign text in quotes to a variable, such as character_name = \"Ari\"."


def _loop_step_suggestion(has_literal_placeholder: bool) -> str:
    if has_literal_placeholder:
        return (
            "Your output printed [step] or {step} as plain text. Use an f-string, "
            "for example print(f\"Reading Step {step}\"), so Python inserts the number."
        )
    return "Print the loop variable so each line shows the current step number."


def _is_meaningful_name(name: str) -> bool:
    clean_name = name.strip("_").lower()
    if clean_name in ALLOWED_SHORT_NAMES:
        return True
    return (
        len(clean_name) >= 3
        and clean_name not in GENERIC_NAMES
        and not clean_name.startswith("my_")
        and any(character.isalpha() for character in clean_name)
    )
