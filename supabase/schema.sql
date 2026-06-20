-- TechTales Python Mentor — Supabase schema
-- Run this once in the Supabase SQL Editor (Dashboard → SQL Editor → New query)

-- ── TABLES ────────────────────────────────────────────────────────────────────

create table if not exists progress (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid references auth.users(id) on delete cascade not null,
    topic_key   text not null,
    viewed      boolean not null default false,
    completed   boolean not null default false,
    viewed_at   timestamptz,
    completed_at timestamptz,
    updated_at  timestamptz not null default now(),
    unique (user_id, topic_key)
);

create table if not exists submissions (
    id                  uuid primary key default gen_random_uuid(),
    user_id             uuid references auth.users(id) on delete cascade not null,
    topic_key           text not null,
    code                text not null,
    evaluator_status    text not null,
    evaluator_message   text not null,
    challenge_passed    boolean not null default false,
    validation_details  text,
    xp_awarded          integer not null default 0,
    stdout              text not null default '',
    runtime_error       text,
    submitted_at        timestamptz not null default now()
);

create table if not exists learner_stats (
    user_id    uuid primary key references auth.users(id) on delete cascade,
    xp         integer not null default 0,
    updated_at timestamptz not null default now()
);

-- ── INDEXES ───────────────────────────────────────────────────────────────────

create index if not exists idx_submissions_user_topic
    on submissions (user_id, topic_key, submitted_at desc);

create index if not exists idx_progress_user
    on progress (user_id, topic_key);

create table if not exists page_views (
    id         uuid primary key default gen_random_uuid(),
    viewed_at  timestamptz not null default now()
);

-- ── ROW LEVEL SECURITY ────────────────────────────────────────────────────────

alter table progress       enable row level security;
alter table submissions    enable row level security;
alter table learner_stats  enable row level security;

create policy "Users access own progress"
    on progress for all using (auth.uid() = user_id);

create policy "Users access own submissions"
    on submissions for all using (auth.uid() = user_id);

create policy "Users access own stats"
    on learner_stats for all using (auth.uid() = user_id);

alter table page_views enable row level security;

-- Anyone (including guests using the anon key) can insert a visit.
-- No one can read raw rows — query via the Supabase SQL editor only.
create policy "Anyone can record a visit"
    on page_views for insert with check (true);
