from __future__ import annotations

import json
from pathlib import Path
import sqlite3

from techtales.models import Progress, Submission


DEFAULT_DB_PATH = Path("data/techtales.db")


def connect(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Path = DEFAULT_DB_PATH) -> None:
    with connect(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS progress (
                topic_key TEXT PRIMARY KEY,
                viewed INTEGER NOT NULL DEFAULT 0,
                completed INTEGER NOT NULL DEFAULT 0,
                viewed_at TEXT,
                completed_at TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_key TEXT NOT NULL,
                code TEXT NOT NULL,
                evaluator_status TEXT NOT NULL,
                evaluator_message TEXT NOT NULL,
                challenge_passed INTEGER NOT NULL DEFAULT 0,
                validation_details TEXT,
                xp_awarded INTEGER NOT NULL DEFAULT 0,
                stdout TEXT NOT NULL DEFAULT '',
                runtime_error TEXT,
                submitted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS learner_stats (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                xp INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_submissions_topic_submitted
                ON submissions(topic_key, submitted_at DESC);

            INSERT OR IGNORE INTO learner_stats (id, xp)
            VALUES (1, 0);
            """
        )
        _ensure_column(connection, "submissions", "challenge_passed", "INTEGER NOT NULL DEFAULT 0")
        _ensure_column(connection, "submissions", "validation_details", "TEXT")
        _ensure_column(connection, "submissions", "xp_awarded", "INTEGER NOT NULL DEFAULT 0")
        _ensure_column(connection, "submissions", "stdout", "TEXT NOT NULL DEFAULT ''")
        _ensure_column(connection, "submissions", "runtime_error", "TEXT")


def _ensure_column(connection: sqlite3.Connection, table_name: str, column_name: str, definition: str) -> None:
    columns = {
        row["name"]
        for row in connection.execute(f"PRAGMA table_info({table_name});").fetchall()
    }
    if column_name not in columns:
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition};")


def mark_topic_viewed(db_path: Path, topic_key: str) -> None:
    with connect(db_path) as connection:
        connection.execute(
            """
            INSERT INTO progress (topic_key, viewed, viewed_at, updated_at)
            VALUES (?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(topic_key) DO UPDATE SET
                viewed = 1,
                viewed_at = COALESCE(progress.viewed_at, CURRENT_TIMESTAMP),
                updated_at = CURRENT_TIMESTAMP;
            """,
            (topic_key,),
        )


def save_submission(
    db_path: Path,
    topic_key: str,
    code: str,
    evaluator_status: str,
    evaluator_message: str,
    challenge_passed: bool = False,
    validation_details: list[dict[str, object]] | None = None,
    stdout: str = "",
    runtime_error: str | None = None,
) -> int:
    with connect(db_path) as connection:
        existing_pass = connection.execute(
            """
            SELECT 1
            FROM submissions
            WHERE topic_key = ? AND challenge_passed = 1
            LIMIT 1;
            """,
            (topic_key,),
        ).fetchone()
        was_passed = existing_pass is not None
        xp_awarded = 20 if challenge_passed and not was_passed else 0

        connection.execute(
            """
            INSERT INTO submissions (
                topic_key,
                code,
                evaluator_status,
                evaluator_message,
                challenge_passed,
                validation_details,
                xp_awarded,
                stdout,
                runtime_error
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                topic_key,
                code,
                evaluator_status,
                evaluator_message,
                int(challenge_passed),
                json.dumps(validation_details or []),
                xp_awarded,
                stdout,
                runtime_error,
            ),
        )
        if challenge_passed:
            connection.execute(
                """
                INSERT INTO progress (topic_key, viewed, completed, viewed_at, completed_at, updated_at)
                VALUES (?, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(topic_key) DO UPDATE SET
                    viewed = 1,
                    completed = 1,
                    viewed_at = COALESCE(progress.viewed_at, CURRENT_TIMESTAMP),
                    completed_at = COALESCE(progress.completed_at, CURRENT_TIMESTAMP),
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (topic_key,),
            )
        else:
            connection.execute(
                """
                INSERT INTO progress (topic_key, viewed, viewed_at, updated_at)
                VALUES (?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(topic_key) DO UPDATE SET
                    viewed = 1,
                    viewed_at = COALESCE(progress.viewed_at, CURRENT_TIMESTAMP),
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (topic_key,),
            )

        if xp_awarded:
            connection.execute(
                """
                UPDATE learner_stats
                SET xp = xp + ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = 1;
                """,
                (xp_awarded,),
            )

    return xp_awarded


def get_progress(db_path: Path) -> dict[str, Progress]:
    with connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT topic_key, viewed, completed, viewed_at, completed_at, updated_at
            FROM progress
            ORDER BY topic_key;
            """
        ).fetchall()

    return {
        row["topic_key"]: Progress(
            topic_key=row["topic_key"],
            viewed=bool(row["viewed"]),
            completed=bool(row["completed"]),
            viewed_at=row["viewed_at"],
            completed_at=row["completed_at"],
            updated_at=row["updated_at"],
        )
        for row in rows
    }


def get_latest_submission(db_path: Path, topic_key: str) -> Submission | None:
    with connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT
                id,
                topic_key,
                code,
                evaluator_status,
                evaluator_message,
                submitted_at,
                challenge_passed,
                validation_details,
                xp_awarded,
                stdout,
                runtime_error
            FROM submissions
            WHERE topic_key = ?
            ORDER BY submitted_at DESC, id DESC
            LIMIT 1;
            """,
            (topic_key,),
        ).fetchone()

    if row is None:
        return None

    return Submission(
        id=row["id"],
        topic_key=row["topic_key"],
        code=row["code"],
        evaluator_status=row["evaluator_status"],
        evaluator_message=row["evaluator_message"],
        submitted_at=row["submitted_at"],
        challenge_passed=bool(row["challenge_passed"]),
        validation_details=row["validation_details"],
        xp_awarded=row["xp_awarded"],
        stdout=row["stdout"],
        runtime_error=row["runtime_error"],
    )


def get_current_xp(db_path: Path) -> int:
    with connect(db_path) as connection:
        row = connection.execute("SELECT xp FROM learner_stats WHERE id = 1;").fetchone()
    return int(row["xp"]) if row else 0


def get_passed_topic_keys(db_path: Path) -> set[str]:
    with connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT DISTINCT topic_key
            FROM submissions
            WHERE challenge_passed = 1;
            """
        ).fetchall()
    return {row["topic_key"] for row in rows}
