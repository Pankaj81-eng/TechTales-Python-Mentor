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
