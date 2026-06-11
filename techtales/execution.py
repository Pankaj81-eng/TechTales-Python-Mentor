from __future__ import annotations

import ast
import contextlib
import io
import multiprocessing
import queue
import traceback
from types import MappingProxyType

from techtales.models import ExecutionResult


EXECUTION_TIMEOUT_SECONDS = 2
MAX_OUTPUT_CHARACTERS = 4000

ALLOWED_BUILTINS = MappingProxyType(
    {
        "abs": abs,
        "bool": bool,
        "dict": dict,
        "enumerate": enumerate,
        "float": float,
        "int": int,
        "len": len,
        "list": list,
        "max": max,
        "min": min,
        "print": print,
        "range": range,
        "round": round,
        "set": set,
        "str": str,
        "sum": sum,
        "tuple": tuple,
    }
)

BLOCKED_NODES = (
    ast.AsyncFor,
    ast.AsyncFunctionDef,
    ast.Await,
    ast.Delete,
    ast.Global,
    ast.Import,
    ast.ImportFrom,
    ast.Lambda,
    ast.Nonlocal,
    ast.Raise,
    ast.Try,
    ast.With,
)


def execute_user_code(code: str) -> ExecutionResult:
    safety_error = _validate_safe_ast(code)
    if safety_error:
        return ExecutionResult(stdout="", error=safety_error)

    ctx = multiprocessing.get_context("spawn")
    result_queue = ctx.Queue()
    process = ctx.Process(target=_run_code_worker, args=(code, result_queue))
    process.start()
    process.join(EXECUTION_TIMEOUT_SECONDS)

    if process.is_alive():
        process.terminate()
        process.join(1)
        return ExecutionResult(
            stdout="",
            error="The program took too long to finish. Check for an infinite loop or code that never stops.",
        )

    try:
        payload = result_queue.get_nowait()
    except queue.Empty:
        return ExecutionResult(stdout="", error="The program stopped before returning output.")

    return ExecutionResult(
        stdout=payload.get("stdout", "")[:MAX_OUTPUT_CHARACTERS],
        error=payload.get("error"),
    )


def _validate_safe_ast(code: str) -> str | None:
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} on line {error.lineno}"

    for node in ast.walk(tree):
        if isinstance(node, BLOCKED_NODES):
            return f"{type(node).__name__} is not available in the learning sandbox."
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return "Double-underscore attributes are not available in the learning sandbox."
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            return "Double-underscore names are not available in the learning sandbox."

    return None


def _run_code_worker(code: str, result_queue: multiprocessing.Queue) -> None:
    stdout = io.StringIO()
    globals_scope = {
        "__builtins__": ALLOWED_BUILTINS,
        "__name__": "__techtales_submission__",
    }
    locals_scope: dict[str, object] = {}

    try:
        compiled = compile(code, "<learner submission>", "exec")
        with contextlib.redirect_stdout(stdout):
            exec(compiled, globals_scope, locals_scope)
    except Exception:
        error = traceback.format_exc(limit=1).strip().splitlines()[-1]
        result_queue.put({"stdout": stdout.getvalue()[:MAX_OUTPUT_CHARACTERS], "error": error})
        return

    result_queue.put({"stdout": stdout.getvalue()[:MAX_OUTPUT_CHARACTERS], "error": None})
