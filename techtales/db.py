from __future__ import annotations

import json
import os
from datetime import date, timedelta, datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from supabase import create_client, Client

from techtales.models import Progress, Submission


SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")


def get_anon_client() -> Client:
    """Anonymous client — used only for auth (login / sign-up)."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def make_client(access_token: str) -> Client:
    """Authenticated client — PostgREST requests carry the user's JWT for RLS."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    client.postgrest.auth(access_token)
    return client


def initialize_user(client: Client, user_id: str) -> None:
    """Create a learner_stats row for a brand-new user; no-op if it exists."""
    client.table("learner_stats").upsert(
        {"user_id": user_id, "xp": 0},
        on_conflict="user_id",
        ignore_duplicates=True,
    ).execute()


def mark_topic_viewed(client: Client, user_id: str, topic_key: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    existing = client.table("progress").select("viewed_at").eq("topic_key", topic_key).execute()

    if existing.data:
        if not existing.data[0].get("viewed_at"):
            client.table("progress").update({"viewed": True, "viewed_at": now}).eq("topic_key", topic_key).execute()
    else:
        client.table("progress").insert({
            "user_id": user_id,
            "topic_key": topic_key,
            "viewed": True,
            "viewed_at": now,
        }).execute()


def save_submission(
    client: Client,
    user_id: str,
    topic_key: str,
    code: str,
    evaluator_status: str,
    evaluator_message: str,
    challenge_passed: bool = False,
    validation_details: list[dict] | None = None,
    stdout: str = "",
    runtime_error: str | None = None,
) -> int:
    # Check whether this topic was already passed (XP is awarded only once).
    existing_pass = client.table("submissions").select("id").eq("topic_key", topic_key).eq("challenge_passed", True).limit(1).execute()
    was_passed = bool(existing_pass.data)
    xp_awarded = 20 if challenge_passed and not was_passed else 0

    client.table("submissions").insert({
        "user_id": user_id,
        "topic_key": topic_key,
        "code": code,
        "evaluator_status": evaluator_status,
        "evaluator_message": evaluator_message,
        "challenge_passed": challenge_passed,
        "validation_details": json.dumps(validation_details or []),
        "xp_awarded": xp_awarded,
        "stdout": stdout,
        "runtime_error": runtime_error,
    }).execute()

    now = datetime.now(timezone.utc).isoformat()

    if challenge_passed:
        existing_prog = client.table("progress").select("id, viewed_at").eq("topic_key", topic_key).execute()
        if existing_prog.data:
            client.table("progress").update({
                "viewed": True, "completed": True, "completed_at": now,
            }).eq("topic_key", topic_key).execute()
        else:
            client.table("progress").insert({
                "user_id": user_id, "topic_key": topic_key,
                "viewed": True, "completed": True,
                "viewed_at": now, "completed_at": now,
            }).execute()
    else:
        existing_prog = client.table("progress").select("id, viewed_at").eq("topic_key", topic_key).execute()
        if not existing_prog.data:
            client.table("progress").insert({
                "user_id": user_id, "topic_key": topic_key,
                "viewed": True, "viewed_at": now,
            }).execute()

    if xp_awarded:
        stats = client.table("learner_stats").select("xp").eq("user_id", user_id).execute()
        current_xp = stats.data[0]["xp"] if stats.data else 0
        client.table("learner_stats").update({
            "xp": current_xp + xp_awarded,
            "updated_at": now,
        }).eq("user_id", user_id).execute()

    return xp_awarded


def get_progress(client: Client) -> dict[str, Progress]:
    result = client.table("progress").select("*").execute()
    return {
        row["topic_key"]: Progress(
            topic_key=row["topic_key"],
            viewed=bool(row["viewed"]),
            completed=bool(row["completed"]),
            viewed_at=row.get("viewed_at"),
            completed_at=row.get("completed_at"),
            updated_at=row.get("updated_at") or "",
        )
        for row in (result.data or [])
    }


def get_latest_submission(client: Client, topic_key: str) -> Submission | None:
    result = (
        client.table("submissions")
        .select("*")
        .eq("topic_key", topic_key)
        .order("submitted_at", desc=True)
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    row = result.data[0]
    return Submission(
        id=row.get("id"),
        topic_key=row["topic_key"],
        code=row["code"],
        evaluator_status=row["evaluator_status"],
        evaluator_message=row["evaluator_message"],
        submitted_at=row.get("submitted_at") or "",
        challenge_passed=bool(row["challenge_passed"]),
        validation_details=row.get("validation_details"),
        xp_awarded=row.get("xp_awarded") or 0,
        stdout=row.get("stdout") or "",
        runtime_error=row.get("runtime_error"),
    )


def get_current_xp(client: Client) -> int:
    result = client.table("learner_stats").select("xp").execute()
    return int(result.data[0]["xp"]) if result.data else 0


def get_passed_topic_keys(client: Client) -> set[str]:
    result = (
        client.table("submissions")
        .select("topic_key")
        .eq("challenge_passed", True)
        .execute()
    )
    return {row["topic_key"] for row in (result.data or [])}


def get_streak(client: Client) -> tuple[int, int]:
    result = client.table("submissions").select("submitted_at").execute()

    if not result.data:
        return 0, 0

    days = sorted(
        {date.fromisoformat(row["submitted_at"][:10]) for row in result.data},
        reverse=True,
    )
    today = date.today()

    current = 0
    if days and days[0] >= today - timedelta(days=1):
        expected = days[0]
        for day in days:
            if day == expected:
                current += 1
                expected -= timedelta(days=1)
            else:
                break

    days_asc = sorted(days)
    longest = 1 if days_asc else 0
    run = 1
    for i in range(1, len(days_asc)):
        if days_asc[i] - days_asc[i - 1] == timedelta(days=1):
            run += 1
            longest = max(longest, run)
        else:
            run = 1

    return current, longest
