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
        if topic.key == "tuples":
            return validate_tuples_challenge(submitted_code, execution_result)
        if topic.key == "data_types":
            return validate_data_types_challenge(submitted_code, execution_result)
        if topic.key == "arithmetic_operators":
            return validate_arithmetic_operators_challenge(submitted_code, execution_result)
        if topic.key == "exercise_profile_card":
            return validate_exercise_profile_card_challenge(submitted_code, execution_result)
        if topic.key == "string_indexing":
            return validate_string_indexing_challenge(submitted_code, execution_result)
        if topic.key == "string_split_join":
            return validate_string_split_join_challenge(submitted_code, execution_result)
        if topic.key == "comparison_operators":
            return validate_comparison_operators_challenge(submitted_code, execution_result)
        if topic.key == "boolean_logic":
            return validate_boolean_logic_challenge(submitted_code, execution_result)
        if topic.key == "membership_operators":
            return validate_membership_operators_challenge(submitted_code, execution_result)
        if topic.key == "conditional_expression":
            return validate_conditional_expression_challenge(submitted_code, execution_result)
        if topic.key == "exercise_grade_checker":
            return validate_exercise_grade_checker_challenge(submitted_code, execution_result)
        if topic.key == "for_each":
            return validate_for_each_challenge(submitted_code, execution_result)
        if topic.key == "enumerate_loop":
            return validate_enumerate_loop_challenge(submitted_code, execution_result)
        if topic.key == "break_continue":
            return validate_break_continue_challenge(submitted_code, execution_result)
        if topic.key == "nested_loops":
            return validate_nested_loops_challenge(submitted_code, execution_result)
        if topic.key == "exercise_pattern_printer":
            return validate_exercise_pattern_printer_challenge(submitted_code, execution_result)
        if topic.key == "list_methods":
            return validate_list_methods_challenge(submitted_code, execution_result)
        if topic.key == "list_slicing":
            return validate_list_slicing_challenge(submitted_code, execution_result)
        if topic.key == "list_comprehensions":
            return validate_list_comprehensions_challenge(submitted_code, execution_result)
        if topic.key == "tuple_unpacking":
            return validate_tuple_unpacking_challenge(submitted_code, execution_result)
        if topic.key == "sets":
            return validate_sets_challenge(submitted_code, execution_result)
        if topic.key == "dict_methods":
            return validate_dict_methods_challenge(submitted_code, execution_result)
        if topic.key == "dict_iteration":
            return validate_dict_iteration_challenge(submitted_code, execution_result)
        if topic.key == "nested_data":
            return validate_nested_data_challenge(submitted_code, execution_result)
        if topic.key == "exercise_inventory":
            return validate_exercise_inventory_challenge(submitted_code, execution_result)
        if topic.key == "function_parameters":
            return validate_function_parameters_challenge(submitted_code, execution_result)
        if topic.key == "default_parameters":
            return validate_default_parameters_challenge(submitted_code, execution_result)
        if topic.key == "multiple_return":
            return validate_multiple_return_challenge(submitted_code, execution_result)
        if topic.key == "none_type":
            return validate_none_type_challenge(submitted_code, execution_result)
        if topic.key == "recursion":
            return validate_recursion_challenge(submitted_code, execution_result)
        if topic.key == "exercise_calculator":
            return validate_exercise_calculator_challenge(submitted_code, execution_result)
        if topic.key == "classes":
            return validate_classes_challenge(submitted_code, execution_result)
        if topic.key == "class_definition":
            return validate_class_definition_challenge(submitted_code, execution_result)
        if topic.key == "instance_creation":
            return validate_instance_creation_challenge(submitted_code, execution_result)
        if topic.key == "class_methods":
            return validate_class_methods_challenge(submitted_code, execution_result)
        if topic.key == "class_attributes":
            return validate_class_attributes_challenge(submitted_code, execution_result)
        if topic.key == "inheritance":
            return validate_inheritance_challenge(submitted_code, execution_result)
        if topic.key == "exercise_class_design":
            return validate_exercise_class_design_challenge(submitted_code, execution_result)

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
    _, has_meaningful_print_output = _inspect_print_output(tree)
    stdout = execution_result.stdout if execution_result else ""
    printed_values = _printed_non_empty_lines(stdout)

    # Accept string/int literals OR explicit conversion calls (str(), int())
    has_non_empty_string = bool(non_empty_string_names) or _calls_builtin(tree, "str")
    has_integer = bool(integer_variables) or _calls_builtin(tree, "int")
    has_meaningful_names = bool(variable_names) and all(_is_meaningful_name(name) for name in variable_names)
    has_output = bool(printed_values)

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
            has_output,
            "Pass your variables into print() so the values appear on screen: print(character_name, badges).",
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
    # Check that output lines vary — meaning the loop variable is being printed,
    # not the same hardcoded string repeated. Accepts any loop range, not just 1-3.
    has_varying_output = has_three_lines and len(set(output_lines)) > 1
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
            "Output changes each iteration",
            has_varying_output and not has_literal_placeholder,
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
                RequirementResult("f-string embeds a variable", False, 'Put a variable name inside {}: learner_name = "Ari" then f"Hello {learner_name}!".'),
                RequirementResult("f-string embeds two values", False, 'Embed two things in your f-string, for example a name and a score: f"{learner_name} has {xp} XP".'),
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

    # Count how many values are interpolated across all f-strings
    formatted_value_count = sum(
        sum(1 for part in fstring.values if isinstance(part, ast.FormattedValue))
        for fstring in fstrings
    )
    # Check that at least one placeholder embeds a variable (Name node), not just a constant
    has_var_in_fstring = any(
        isinstance(part, ast.FormattedValue)
        and any(isinstance(n, ast.Name) for n in ast.walk(part))
        for fstring in fstrings
        for part in fstring.values
    )
    has_two_values = formatted_value_count >= 2

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
            "f-string embeds a variable",
            has_var_in_fstring,
            'Put a variable inside {}: learner_name = "Ari" then f"Hello {learner_name}!". Any variable works — name, number, whatever you have.',
        ),
        RequirementResult(
            "f-string embeds two values",
            has_two_values,
            "Embed two different things in your f-string — for example a name and a score: f\"{learner_name} has {xp} XP\".",
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
    has_one_method = len(method_calls) >= 1
    has_two_methods = len(method_calls) >= 2
    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult("At least one string method is used", has_one_method, "Call a method on your string: message.upper() converts all letters to uppercase. The dot connects the method to the string."),
        RequirementResult("At least two string methods are used", has_two_methods, 'Try a second method: message.lower() or message.replace("old", "new").'),
        RequirementResult("Output is printed", has_output, "Wrap your transformed text in print() to see the result on screen."),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Great. You've started using Python's built-in string toolkit — these will come up in almost every real project."
    else:
        feedback = "Close. Call at least two string methods on your text and print the results."

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
                RequirementResult("A type conversion function is used", False, "Use int(), float(), or str() to convert a value: e.g. int(price_text) or str(102)."),
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
    has_arithmetic = any(isinstance(n, ast.BinOp) for n in ast.walk(tree))
    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult("A type conversion function is used", has_conversion, "Use int(), float(), or str() to convert a value: e.g. int(price_text) or str(102)."),
        RequirementResult("Arithmetic is performed", has_arithmetic, "Once you have a number, do some maths: total = price * quantity or similar."),
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


def validate_tuples_challenge(
    submitted_code: str,
    execution_result: ExecutionResult | None = None,
) -> ValidationResult:
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return ValidationResult(
            passed=False,
            requirements=(
                RequirementResult("A tuple is created", False, 'Create a tuple: seasons = ("Spring", "Summer", "Autumn", "Winter")'),
                RequirementResult("The tuple has at least 3 items", False, "Add at least 3 items inside the parentheses, separated by commas."),
                RequirementResult("len() is used", False, "Call len(seasons) to count the items."),
                RequirementResult("An item is accessed by index", False, "Access an item with seasons[0] — index 0 is the first item."),
                RequirementResult("Output is printed", False, "Add print() to show the tuple, its length, or an item."),
            ),
            feedback="Python could not read this submission yet. Check the syntax, then try again.",
        )

    tuple_literals = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Tuple) and isinstance(n.ctx, ast.Load)
    ]
    has_tuple = bool(tuple_literals)
    has_three_items = any(len(n.elts) >= 3 for n in tuple_literals)
    has_len = any(
        isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "len"
        for n in ast.walk(tree)
    )
    has_index = any(isinstance(n, ast.Subscript) for n in ast.walk(tree))
    stdout = execution_result.stdout if execution_result else ""
    has_output = bool(_printed_non_empty_lines(stdout))

    requirements = (
        RequirementResult("A tuple is created", has_tuple, 'Create a tuple using parentheses: seasons = ("Spring", "Summer", "Autumn", "Winter")'),
        RequirementResult("The tuple has at least 3 items", has_three_items, "Add at least 3 items inside the parentheses, separated by commas."),
        RequirementResult("len() is used", has_len, "Call len(seasons) to find out how many items the tuple contains."),
        RequirementResult("An item is accessed by index", has_index, "Access an item by position: seasons[0] gives the first item."),
        RequirementResult("Output is printed", has_output, "Wrap your results in print() to see the tuple, its length, and an item."),
    )
    passed = all(r.passed for r in requirements)

    if passed:
        feedback = "Well done. You've created, measured, and accessed a tuple — and understood why it's different from a list."
    else:
        feedback = "Good start. Make sure your tuple has 3+ items, a len() call, and an index access, then print the results."

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


# ─────────────────────────────────────────────────────────────────────────────
# Phase 3 — shared helpers for the new topic validators
# ─────────────────────────────────────────────────────────────────────────────

_PASS_FEEDBACK = "Great work — every check passed. On to the next lesson!"
_FAIL_FEEDBACK = "Good progress. Check the red items below, make the change, then submit again."

_ORDER_EQ_OPS = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE)
_AST_INDEX = getattr(ast, "Index", None)


def _build(labels: tuple[tuple[str, str], ...], checks: tuple[bool, ...]) -> ValidationResult:
    """labels = ((label, suggestion), ...) paired positionally with checks (bools)."""
    requirements = tuple(
        RequirementResult(label, bool(passed), suggestion)
        for (label, suggestion), passed in zip(labels, checks)
    )
    passed = all(checks)
    return ValidationResult(
        passed=passed,
        requirements=requirements,
        feedback=_PASS_FEEDBACK if passed else _FAIL_FEEDBACK,
    )


def _all_failed(labels: tuple[tuple[str, str], ...]) -> ValidationResult:
    return _build(labels, tuple(False for _ in labels))


def _has_print_call(tree: ast.AST) -> bool:
    return any(
        isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"
        for n in ast.walk(tree)
    )


def _has_output(tree: ast.AST, execution_result: ExecutionResult | None) -> bool:
    if execution_result is not None:
        return bool(_printed_non_empty_lines(execution_result.stdout))
    return _has_print_call(tree)


def _output_line_count(execution_result: ExecutionResult | None) -> int:
    if execution_result is not None:
        return len(_printed_non_empty_lines(execution_result.stdout))
    return 0


def _calls_builtin(tree: ast.AST, name: str) -> bool:
    return any(
        isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name
        for n in ast.walk(tree)
    )


def _method_calls(tree: ast.AST, names: set[str]) -> list[ast.Call]:
    return [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in names
    ]


def _subscript_is_slice(node: ast.Subscript) -> bool:
    sliced = node.slice
    if isinstance(sliced, ast.Slice):
        return True
    if _AST_INDEX is not None and isinstance(sliced, _AST_INDEX):
        return isinstance(sliced.value, ast.Slice)
    return False


def _has_slice(tree: ast.AST) -> bool:
    return any(isinstance(n, ast.Subscript) and _subscript_is_slice(n) for n in ast.walk(tree))


def _has_index_access(tree: ast.AST) -> bool:
    return any(
        isinstance(n, ast.Subscript) and not _subscript_is_slice(n) for n in ast.walk(tree)
    )


def _has_string_assignment(tree: ast.AST) -> bool:
    return any(
        isinstance(n, ast.Assign)
        and any(isinstance(v, ast.Constant) and isinstance(v.value, str) for v in ast.walk(n.value))
        for n in ast.walk(tree)
    )


def _has_list_literal(tree: ast.AST) -> bool:
    has_literal = any(
        isinstance(n, ast.List) and isinstance(n.ctx, ast.Load) for n in ast.walk(tree)
    )
    return has_literal or _calls_builtin(tree, "list")


def _has_dict_literal(tree: ast.AST) -> bool:
    return any(isinstance(n, ast.Dict) for n in ast.walk(tree)) or _calls_builtin(tree, "dict")


def _has_set(tree: ast.AST) -> bool:
    return any(isinstance(n, ast.Set) for n in ast.walk(tree)) or _calls_builtin(tree, "set")


def _has_list_of_dicts(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.List) and any(isinstance(e, ast.Dict) for e in node.elts):
            return True
    return False


def _has_for_loop(tree: ast.AST) -> bool:
    return any(isinstance(n, ast.For) for n in ast.walk(tree))


def _has_any_loop(tree: ast.AST) -> bool:
    return any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(tree))


def _has_nested_loop(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            for child in ast.walk(node):
                if child is not node and isinstance(child, (ast.For, ast.While)):
                    return True
    return False


def _loop_output_varies(tree: ast.AST) -> bool:
    """True if a loop's body has a nested loop, an if, or a print that uses the
    loop variable — i.e. the output changes from line to line."""
    for loop in ast.walk(tree):
        if not isinstance(loop, (ast.For, ast.While)):
            continue
        for child in ast.walk(loop):
            if child is not loop and isinstance(child, (ast.For, ast.While, ast.If)):
                return True
        targets: set[str] = set()
        if isinstance(loop, ast.For):
            targets = {n.id for n in ast.walk(loop.target) if isinstance(n, ast.Name)}
        if targets:
            for child in ast.walk(loop):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == "print":
                    used = {n.id for n in ast.walk(child) if isinstance(n, ast.Name)}
                    if used & targets:
                        return True
    return False


def _has_direct_for_each(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.For):
            continue
        it = node.iter
        if isinstance(it, ast.Call) and isinstance(it.func, ast.Name) and it.func.id == "range":
            continue
        if isinstance(it, (ast.Name, ast.List, ast.Tuple, ast.Set)):
            return True
        if isinstance(it, ast.Constant) and isinstance(it.value, str):
            return True
        if isinstance(it, ast.Call) and isinstance(it.func, ast.Attribute) and it.func.attr in {
            "items", "keys", "values", "split",
        }:
            return True
    return False


def _loops_over_dict(tree: ast.AST) -> bool:
    dict_vars = {
        name for name, value in _collect_assignments(tree).items() if isinstance(value, ast.Dict)
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.For):
            continue
        it = node.iter
        if isinstance(it, ast.Call) and isinstance(it.func, ast.Attribute) and it.func.attr in {
            "items", "keys", "values",
        }:
            return True
        if isinstance(it, ast.Name) and it.id in dict_vars:
            return True
    return False


def _has_multi_assign(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, (ast.Tuple, ast.List)) and len(target.elts) >= 2:
                    return True
    return False


def _if_nodes(tree: ast.AST) -> list[ast.If]:
    return [n for n in ast.walk(tree) if isinstance(n, ast.If)]


def _has_elif(tree: ast.AST) -> bool:
    return any(len(n.orelse) == 1 and isinstance(n.orelse[0], ast.If) for n in _if_nodes(tree))


def _has_else(tree: ast.AST) -> bool:
    return any(
        n.orelse and not (len(n.orelse) == 1 and isinstance(n.orelse[0], ast.If))
        for n in _if_nodes(tree)
    )


def _comparison_nodes(tree: ast.AST) -> list[ast.Compare]:
    return [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Compare) and any(isinstance(op, _ORDER_EQ_OPS) for op in n.ops)
    ]


def _has_membership(tree: ast.AST) -> bool:
    return any(
        isinstance(n, ast.Compare) and any(isinstance(op, (ast.In, ast.NotIn)) for op in n.ops)
        for n in ast.walk(tree)
    )


def _boolean_op_count(tree: ast.AST) -> int:
    count = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.BoolOp):
            count += 1
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            count += 1
    return count


def _function_defs(tree: ast.AST) -> list[ast.FunctionDef]:
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def _calls_defined_function(tree: ast.AST) -> bool:
    names = {fn.name for fn in _function_defs(tree)}
    return any(
        isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in names
        for n in ast.walk(tree)
    )


def _has_recursive_call(tree: ast.AST) -> bool:
    for fn in _function_defs(tree):
        for child in ast.walk(fn):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == fn.name:
                return True
    return False


def _returns_tuple(tree: ast.AST) -> bool:
    return any(
        isinstance(n, ast.Return) and isinstance(n.value, ast.Tuple) and len(n.value.elts) >= 2
        for n in ast.walk(tree)
    )


def _returns_value(tree: ast.AST) -> bool:
    for fn in _function_defs(tree):
        for child in ast.walk(fn):
            if isinstance(child, ast.Return) and child.value is not None:
                return True
    return False


def _uses_none(tree: ast.AST) -> bool:
    return any(isinstance(n, ast.Constant) and n.value is None for n in ast.walk(tree))


# ─────────────────────────────────────────────────────────────────────────────
# Phase 3 — topic validators
# ─────────────────────────────────────────────────────────────────────────────

def validate_data_types_challenge(submitted_code, execution_result=None):
    labels = (
        ("A text value (str) is created", 'Create a text variable using quotes: item_name = "Sword".'),
        ("A whole number (int) is created", "Create a whole-number variable without quotes: item_count = 5."),
        ("A decimal number (float) is created", "Create a decimal variable with a dot: item_power = 8.5."),
        ("A true/false value (bool) is created", "Create a boolean variable: is_ready = True (or False)."),
        ("type() is used", "Ask Python for a value's type with type(): print(type(item_name))."),
        ("Output is printed", "Use print() with type() so the four types appear on screen."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    values = list(_collect_assignments(tree).values())

    def has_const(predicate):
        return any(isinstance(v, ast.Constant) and predicate(v.value) for v in values)

    checks = (
        has_const(lambda x: isinstance(x, str)),
        has_const(lambda x: isinstance(x, int) and not isinstance(x, bool)),
        has_const(lambda x: isinstance(x, float)),
        has_const(lambda x: isinstance(x, bool)),
        _calls_builtin(tree, "type"),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_arithmetic_operators_challenge(submitted_code, execution_result=None):
    labels = (
        ("A calculation is performed", "Combine two numbers with an operator, for example: a + b."),
        ("At least two different operators are used", "Use two different operators — for example a + b and a * b."),
        ("Output is printed", "Wrap each calculation in print() so the results appear."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    binops = [n for n in ast.walk(tree) if isinstance(n, ast.BinOp)]
    distinct_ops = {type(n.op) for n in binops}
    checks = (
        bool(binops),
        len(distinct_ops) >= 2,
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_exercise_profile_card_challenge(submitted_code, execution_result=None):
    labels = (
        ("A variable is created", 'Store a fact in a variable, such as name = "Ari".'),
        ("A calculation is performed", "Calculate a value from your numbers, for example: age = current_year - birth_year."),
        ("An f-string is used", 'Build your summary with an f-string: f"{name} is {age} years old."'),
        ("Output is printed", "Wrap your f-string in print() so the profile card appears."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        any(isinstance(n, ast.Assign) for n in ast.walk(tree)),
        any(isinstance(n, ast.BinOp) for n in ast.walk(tree)),
        any(isinstance(n, ast.JoinedStr) for n in ast.walk(tree)),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_string_indexing_challenge(submitted_code, execution_result=None):
    labels = (
        ("A text variable is created", 'Create a string first: word = "MENTOR".'),
        ("A character is accessed by index", "Grab one character by position: word[0] or word[-1]."),
        ("A slice is used", "Take a section with a colon: word[1:4]."),
        ("Output is printed", "Wrap your results in print() to see the character and the slice."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_string_assignment(tree),
        _has_index_access(tree),
        _has_slice(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_string_split_join_challenge(submitted_code, execution_result=None):
    labels = (
        ("A text variable is created", 'Create a sentence first: sentence = "python is fun to learn".'),
        (".split() is used", "Break the sentence into words: words = sentence.split()."),
        (".join() is used", 'Glue words back together: "-".join(words).'),
        ("Output is printed", "Use print() to show both the split list and the joined string."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_string_assignment(tree),
        bool(_method_calls(tree, {"split"})),
        bool(_method_calls(tree, {"join"})),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_comparison_operators_challenge(submitted_code, execution_result=None):
    labels = (
        ("A comparison is made", "Compare two values with an operator like > or ==, for example: score > 5."),
        ("At least two comparisons are used", "Use two different comparisons — for example score > 5 and score == 10."),
        ("Output is printed", "Wrap each comparison in print() to see its True or False answer."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    comparisons = _comparison_nodes(tree)
    checks = (
        bool(comparisons),
        len(comparisons) >= 2,
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_boolean_logic_challenge(submitted_code, execution_result=None):
    labels = (
        ("A boolean operator is used", "Combine two conditions with and, or, or not — for example: age >= 18 and has_ticket."),
        ("At least two boolean operators are used", "Use two of them — for example an and on one line and a not on another."),
        ("Output is printed", "Wrap each combined condition in print() to see its result."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    count = _boolean_op_count(tree)
    checks = (
        count >= 1,
        count >= 2,
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_membership_operators_challenge(submitted_code, execution_result=None):
    labels = (
        ("A membership test is used", 'Use in to check for a value: "e" in vowels, or not in for the opposite.'),
        ("Output is printed", "Wrap your membership test in print() to see the True or False answer."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_membership(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_conditional_expression_challenge(submitted_code, execution_result=None):
    labels = (
        ("A conditional expression is used", 'Use the one-line form: result = "pass" if score >= 50 else "fail".'),
        ("Output is printed", "Print the chosen value: print(result)."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        any(isinstance(n, ast.IfExp) for n in ast.walk(tree)),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_exercise_grade_checker_challenge(submitted_code, execution_result=None):
    labels = (
        ("A comparison is made", "Compare the score against a threshold, for example: score >= 90."),
        ("An elif branch is used", "Add at least one elif for a middle grade: elif score >= 75:."),
        ("An else branch is used", "Finish with else: to catch every score that didn't match above."),
        ("Output is printed", "Each branch needs a print() with the grade message inside it."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        bool(_comparison_nodes(tree)),
        _has_elif(tree),
        _has_else(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_for_each_challenge(submitted_code, execution_result=None):
    labels = (
        ("A for loop is used", "Start a loop: for color in colors:."),
        ("The loop goes through a collection directly", "Loop over your list itself (for item in my_list:), not over range()."),
        ("Output is printed", "Indent a print() inside the loop so each item appears."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_for_loop(tree),
        _has_direct_for_each(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_enumerate_loop_challenge(submitted_code, execution_result=None):
    labels = (
        ("A for loop is used", "Begin a loop over your list with for ... in ...:."),
        ("enumerate() is used", "Wrap the list in enumerate(): for number, step in enumerate(steps):."),
        ("Output is printed", "Indent a print() inside the loop to show each position and item."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_for_loop(tree),
        _calls_builtin(tree, "enumerate"),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_break_continue_challenge(submitted_code, execution_result=None):
    labels = (
        ("A loop is used", "Start a for or while loop over some numbers."),
        ("break or continue is used", "Inside an if, use break to stop early, or continue to skip a turn."),
        ("Output is printed", "Print the numbers inside the loop so you can see the effect."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_control = any(isinstance(n, (ast.Break, ast.Continue)) for n in ast.walk(tree))
    checks = (
        _has_any_loop(tree),
        has_control,
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_nested_loops_challenge(submitted_code, execution_result=None):
    labels = (
        ("An outer loop is used", "Start with one loop, for example for row in range(1, 4):."),
        ("A loop is nested inside another loop", "Indent a second loop inside the first: for col in range(1, 4):."),
        ("Output is printed", "Print something inside the inner loop so each combination appears."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_any_loop(tree),
        _has_nested_loop(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_exercise_pattern_printer_challenge(submitted_code, execution_result=None):
    labels = (
        ("A loop is used", "Start with a for or while loop to drive the repetition."),
        ("Each line depends on the loop", "Make each line change — use the loop variable in your print (like \"*\" * row), or nest a loop or an if inside."),
        ("Output has multiple lines", "Make sure your program prints at least three separate lines."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_any_loop(tree),
        _loop_output_varies(tree),
        _output_line_count(execution_result) >= 3,
    )
    return _build(labels, checks)


def validate_list_methods_challenge(submitted_code, execution_result=None):
    labels = (
        ("A list is created", 'Create a list first: items = ["Torch", "Map"].'),
        ("A list method is used", 'Call a method: items.append("Key"), items.sort(), or items.pop().'),
        ("Output is printed", "Print the list after changing it so you can see the effect."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    list_method_names = {"append", "insert", "remove", "pop", "sort", "reverse", "extend", "clear"}
    checks = (
        _has_list_literal(tree),
        bool(_method_calls(tree, list_method_names)),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_list_slicing_challenge(submitted_code, execution_result=None):
    labels = (
        ("A list is created", "Create a list of several numbers: nums = [10, 20, 30, 40, 50]."),
        ("A slice is used", "Take a section with a colon: nums[1:3]."),
        ("Output is printed", "Print your slice to see the section you selected."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_list_literal(tree),
        _has_slice(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_list_comprehensions_challenge(submitted_code, execution_result=None):
    labels = (
        ("A list comprehension is used", "Use the [expression for item in collection] form: [n * 2 for n in numbers]."),
        ("Output is printed", "Print the new list to see what your comprehension built."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        any(isinstance(n, ast.ListComp) for n in ast.walk(tree)),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_tuple_unpacking_challenge(submitted_code, execution_result=None):
    labels = (
        ("Multiple variables are assigned at once", "Put several names on the left of one =: x, y = point."),
        ("Output is printed", "Print the unpacked variables to confirm each got its value."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_multi_assign(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_sets_challenge(submitted_code, execution_result=None):
    labels = (
        ("A set is created", "Create a set with set(my_list) or curly braces: unique = {1, 2, 3}."),
        ("A set method is used", "Call a set method such as unique.add(4)."),
        ("Output is printed", "Print the set to see its unique contents."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    set_method_names = {"add", "update", "union", "intersection", "difference", "discard", "remove"}
    checks = (
        _has_set(tree),
        bool(_method_calls(tree, set_method_names)),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_dict_methods_challenge(submitted_code, execution_result=None):
    labels = (
        ("A dictionary is created", 'Create a dictionary first: character = {"name": "Ari", "level": 5}.'),
        ("A dictionary method is used", 'Call a method such as character.get("name"), character.keys(), or character.values().'),
        ("Output is printed", "Print the result of the method to see what it returns."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    dict_method_names = {"get", "keys", "values", "items", "update", "pop", "setdefault"}
    checks = (
        _has_dict_literal(tree),
        bool(_method_calls(tree, dict_method_names)),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_dict_iteration_challenge(submitted_code, execution_result=None):
    labels = (
        ("A dictionary is created", 'Create a dictionary with a few pairs: prices = {"apple": 3, "banana": 2}.'),
        ("A loop goes through the dictionary", "Loop over the pairs: for key, value in prices.items():."),
        ("Output is printed", "Indent a print() inside the loop to show each key and value."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_dict_literal(tree),
        _loops_over_dict(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_nested_data_challenge(submitted_code, execution_result=None):
    labels = (
        ("A list of dictionaries is created", 'Make a list where each item is a dictionary: players = [{"name": "Ari"}, {"name": "Bo"}].'),
        ("A loop goes through the data", "Loop over the list: for player in players:."),
        ("Output is printed", 'Inside the loop, print a value: print(player["name"]).'),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_list_of_dicts(tree),
        _has_for_loop(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_exercise_inventory_challenge(submitted_code, execution_result=None):
    labels = (
        ("A list of dictionaries is created", 'Make a list of item records: inventory = [{"item": "Torch", "qty": 3}, ...].'),
        ("A loop goes through the items", "Loop over the inventory: for entry in inventory:."),
        ("Output is printed", "Inside the loop, print a line for each item."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_list_of_dicts(tree),
        _has_for_loop(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_function_parameters_challenge(submitted_code, execution_result=None):
    labels = (
        ("A function with parameters is defined", "Define a function with two or more parameters: def add_scores(first, second):."),
        ("The function is called", "Call it with matching arguments: add_scores(10, 20)."),
        ("Output is printed", "Print what the function returns: print(add_scores(10, 20))."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_multi_param_def = any(len(fn.args.args) >= 2 for fn in _function_defs(tree))
    checks = (
        has_multi_param_def,
        _calls_defined_function(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_default_parameters_challenge(submitted_code, execution_result=None):
    labels = (
        ("A function with a default parameter is defined", 'Give a parameter a default with =: def greet(name, greeting="Hello"):.'),
        ("The function is called", "Call your function — try it with and without the optional argument."),
        ("Output is printed", "Print the results of your calls to see the default in action."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_default = any(fn.args.defaults or fn.args.kw_defaults for fn in _function_defs(tree))
    checks = (
        has_default,
        _calls_defined_function(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_multiple_return_challenge(submitted_code, execution_result=None):
    labels = (
        ("A function returns multiple values", "Return several values separated by commas: return min(numbers), max(numbers)."),
        ("The function is called", "Call the function and unpack the results: low, high = min_and_max(...)."),
        ("Output is printed", "Print the unpacked values to see each returned result."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _returns_tuple(tree),
        _calls_defined_function(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_none_type_challenge(submitted_code, execution_result=None):
    labels = (
        ("None is used", "Use None somewhere: set a variable to None, or return None from a function."),
        ("Output is printed", "Print a message, ideally based on an is None check."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _uses_none(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_recursion_challenge(submitted_code, execution_result=None):
    labels = (
        ("A function is defined", "Define a function that takes a number: def countdown(n):."),
        ("The function calls itself", "Inside the function, call itself on a smaller value: countdown(n - 1). Add an if base case."),
        ("Output is printed", "Print something inside the function so you can watch the recursion work."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        bool(_function_defs(tree)),
        _has_recursive_call(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_exercise_calculator_challenge(submitted_code, execution_result=None):
    labels = (
        ("A function is defined", "Define a function that takes numbers: def add(a, b):."),
        ("The function is called", "Call your function with values: add(8, 5)."),
        ("A value is returned", "Make sure your function uses return to hand back a result."),
        ("Output is printed", 'Print the result, ideally with an f-string: print(f"Sum: {add(8, 5)}").'),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        bool(_function_defs(tree)),
        _calls_defined_function(tree),
        _returns_value(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


# ─────────────────────────────────────────────────────────────────────────────
# Unit 7 — Object-Oriented Programming validators
# ─────────────────────────────────────────────────────────────────────────────

def _has_class_definition(tree: ast.AST, class_name: str | None = None) -> bool:
    """True if a class is defined, optionally with a specific name."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if class_name is None or node.name == class_name:
                return True
    return False


def _has_class_method(tree: ast.AST, class_name: str | None = None, method_name: str | None = None) -> bool:
    """True if a class has a method (optionally with a specific name inside a specific class)."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if class_name is not None and node.name != class_name:
                continue
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    if method_name is None or item.name == method_name:
                        return True
    return False


def _class_has_init(tree: ast.AST) -> bool:
    """True if any class has an __init__ method."""
    return _has_class_method(tree, method_name="__init__")


def _class_instantiated(tree: ast.AST) -> bool:
    """True if any class is instantiated (called like a function)."""
    class_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in class_names:
            return True
    return False


def _has_inheritance(tree: ast.AST) -> bool:
    """True if a class inherits from another (has a base class)."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.bases:
            return True
    return False


def validate_classes_challenge(submitted_code, execution_result=None):
    labels = (
        ("A class is defined", "Use the class keyword: class Character:. The name starts with a capital letter."),
        ("Output is printed", "Print something to show the class exists, like print('Class created!')."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    checks = (
        _has_class_definition(tree),
        _has_output(tree, execution_result),
    )
    return _build(labels, checks)


def validate_class_definition_challenge(submitted_code, execution_result=None):
    labels = (
        ("A class is defined", "Start with class Player: and give it an __init__ method."),
        ("The class has __init__", "Define __init__ with self and at least two parameters."),
        ("Properties are set with self", "Inside __init__, create properties like self.name = name."),
        ("Output is printed", "Print a message to confirm the class is defined."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_class = _has_class_definition(tree)
    has_init = _class_has_init(tree)
    has_self_assignments = any(
        isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self"
                for target in (node.targets if isinstance(node.targets, list) else [node.targets]))
        for node in ast.walk(tree)
    )
    has_output = _has_output(tree, execution_result)

    checks = (
        has_class,
        has_init,
        has_self_assignments,
        has_output,
    )
    return _build(labels, checks)


def validate_instance_creation_challenge(submitted_code, execution_result=None):
    labels = (
        ("A class is defined", "Define a class with __init__ and properties."),
        ("Objects are created from the class", "Call the class like a function: player1 = Player(...)."),
        ("Both objects' properties are accessed", "Use dot notation to read properties from both objects."),
        ("Output is printed", "Print both objects' information."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_class = _has_class_definition(tree)
    instantiated = _class_instantiated(tree)
    # Count assignments where right side is a call (crude but works for beginners)
    instance_assignments = sum(
        1 for node in ast.walk(tree)
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
    )
    has_multiple_instances = instance_assignments >= 2
    has_output = _has_output(tree, execution_result)

    checks = (
        has_class,
        instantiated,
        has_multiple_instances,
        has_output,
    )
    return _build(labels, checks)


def validate_class_methods_challenge(submitted_code, execution_result=None):
    labels = (
        ("A class is defined", "Define a class with __init__."),
        ("A method is defined (besides __init__)", "Add a method like def gain_xp(self, amount):."),
        ("The method is called on an object", "Use dot notation: player.gain_xp(50)."),
        ("Output is printed", "Print the results, showing the method worked."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_class = _has_class_definition(tree)
    # Count methods: if there are >1, one is __init__ and at least one other exists
    method_defs = sum(
        1 for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and any(
            isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)
            if isinstance(parent, ast.ClassDef)
        )
    )
    # Simpler: check for __init__ and at least one method call via dot notation
    has_other_method = _has_class_method(tree) and method_defs >= 2
    # Check for method call via attribute access
    has_method_call = any(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        for node in ast.walk(tree)
    )
    has_output = _has_output(tree, execution_result)

    checks = (
        has_class,
        has_other_method,
        has_method_call,
        has_output,
    )
    return _build(labels, checks)


def validate_class_attributes_challenge(submitted_code, execution_result=None):
    labels = (
        ("A class is defined", "Define a class with __init__ and properties."),
        ("An object is created", "Instantiate the class."),
        ("Attributes are read and printed", "Use dot notation to access properties."),
        ("Attributes are modified", "Assign new values to properties like player.score = 200."),
        ("Updated values are printed", "Show the changed attribute values."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_class = _has_class_definition(tree)
    instantiated = _class_instantiated(tree)
    # Count attribute accesses (dot notation reads)
    attr_accesses = sum(
        1 for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    )
    has_attr_access = attr_accesses >= 2
    # Count attribute assignments
    attr_assigns = sum(
        1 for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Attribute) for target in (node.targets if isinstance(node.targets, list) else [node.targets]))
    )
    has_attr_modify = attr_assigns >= 1
    has_output = _has_output(tree, execution_result)

    checks = (
        has_class,
        instantiated,
        has_attr_access,
        has_attr_modify,
        has_output,
    )
    return _build(labels, checks)


def validate_inheritance_challenge(submitted_code, execution_result=None):
    labels = (
        ("A base class is defined", "Create a parent class like class Vehicle:."),
        ("A subclass inherits", "Use class Car(Vehicle): to inherit."),
        ("The subclass has its own method", "Add a method to the subclass that doesn't exist in the parent."),
        ("Both the inherited and new methods work", "Call both a parent method and the child's own method."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_class = _has_class_definition(tree)
    has_inherit = _has_inheritance(tree)
    # Count all method definitions
    all_methods = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
    has_multiple_methods = all_methods >= 3  # At least init + one per class
    # Check for method calls (inherited and new)
    has_method_calls = sum(
        1 for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    ) >= 2

    checks = (
        has_class,
        has_inherit,
        has_multiple_methods,
        has_method_calls,
    )
    return _build(labels, checks)


def validate_exercise_class_design_challenge(submitted_code, execution_result=None):
    labels = (
        ("A meaningful class is designed", "Choose something real and create a class for it."),
        ("__init__ initializes properties", "Define __init__ with at least 2 properties."),
        ("Methods modify or use data", "Write at least 2 methods that work with self.properties."),
        ("Instances are created and used", "Create objects and call their methods."),
    )
    try:
        tree = ast.parse(submitted_code)
    except SyntaxError:
        return _all_failed(labels)

    has_class = _has_class_definition(tree)
    has_init = _class_has_init(tree)
    # Count non-__init__ methods
    methods = sum(
        1 for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name != "__init__"
    )
    has_multiple_methods = methods >= 2
    instantiated = _class_instantiated(tree)

    checks = (
        has_class,
        has_init,
        has_multiple_methods,
        instantiated,
    )
    return _build(labels, checks)
