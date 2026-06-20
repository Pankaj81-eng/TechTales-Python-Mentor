from __future__ import annotations

import ast
import contextlib
import io
import multiprocessing
import queue
import traceback
from types import MappingProxyType

from techtales.models import ExecutionResult


# Budget for the learner's code itself, measured only after the sandbox
# interpreter has finished booting (see execute_user_code).
EXECUTION_TIMEOUT_SECONDS = 3
# Separate, generous budget for spawning a fresh Python interpreter. On a
# shared/throttled host (e.g. Streamlit Cloud free tier) a cold spawn can take
# several seconds — that must not eat into the learner's execution budget.
STARTUP_TIMEOUT_SECONDS = 15
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
        # type() lets the Data Types lesson report a value's type. Safe here
        # because the classic type()-based escape needs dunder attribute access
        # (e.g. .__subclasses__()), which _validate_safe_ast already blocks.
        "type": type,
        # __build_class__ is the internal function Python calls when the `class`
        # statement runs (e.g. class Dog: ...). Without it, class definitions
        # raise NameError inside exec. Adding it doesn't weaken the sandbox:
        # class bodies still run through the same AST validator and the same
        # restricted builtins, so no new escape routes are opened.
        "__build_class__": __build_class__,
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
    ready_queue = ctx.Queue()
    result_queue = ctx.Queue()
    process = ctx.Process(target=_run_code_worker, args=(code, ready_queue, result_queue))
    process.start()

    # Wait for the spawned interpreter to boot and signal it is about to run the
    # code. This phase is infrastructure startup, not the learner's program, so
    # it gets its own generous budget and is excluded from the execution timeout.
    try:
        ready_queue.get(timeout=STARTUP_TIMEOUT_SECONDS)
    except queue.Empty:
        _shutdown(process)
        return ExecutionResult(
            stdout="",
            error="The sandbox took too long to start. Please run your code again.",
        )

    # Now time ONLY the learner's code. Retrieving the result also waits for the
    # process to finish — using get(timeout) instead of join + get_nowait avoids
    # a race where the queue's feeder thread hasn't flushed the payload yet.
    try:
        payload = result_queue.get(timeout=EXECUTION_TIMEOUT_SECONDS)
    except queue.Empty:
        _shutdown(process)
        return ExecutionResult(
            stdout="",
            error="The program took too long to finish. Check for an infinite loop or code that never stops.",
        )

    _shutdown(process)

    return ExecutionResult(
        stdout=payload.get("stdout", "")[:MAX_OUTPUT_CHARACTERS],
        error=payload.get("error"),
    )


def _shutdown(process: multiprocessing.Process) -> None:
    """Reap the worker, escalating from a clean join to terminate if needed."""
    process.join(1)
    if process.is_alive():
        process.terminate()
        process.join(1)


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


def _run_code_worker(
    code: str,
    ready_queue: multiprocessing.Queue,
    result_queue: multiprocessing.Queue,
) -> None:
    # Reached only after the fresh interpreter has booted and imported this
    # module, so this is the right moment to start the execution clock in the
    # parent. Signal readiness before running any of the learner's code.
    ready_queue.put("ready")

    stdout = io.StringIO()
    # Run in a single namespace (globals == locals) so the code behaves like a
    # normal module: top-level defs are visible to themselves, which is what
    # makes recursion and mutual function references work. Security still comes
    # only from the __builtins__ allowlist and the AST block list above.
    namespace = {
        "__builtins__": ALLOWED_BUILTINS,
        "__name__": "__techtales_submission__",
    }

    try:
        compiled = compile(code, "<learner submission>", "exec")
        with contextlib.redirect_stdout(stdout):
            exec(compiled, namespace)
    except Exception:
        error = traceback.format_exc(limit=1).strip().splitlines()[-1]
        result_queue.put({"stdout": stdout.getvalue()[:MAX_OUTPUT_CHARACTERS], "error": error})
        return

    result_queue.put({"stdout": stdout.getvalue()[:MAX_OUTPUT_CHARACTERS], "error": None})
