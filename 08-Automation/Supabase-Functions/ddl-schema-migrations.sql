-- FAIOS Production Supabase Database Schema Migration (v1.0.0)
-- Target: Supabase Postgres Free Tier
-- Features: Row Level Security (RLS), Vector Search (pgvector), Realtime & Triggers

-- 1. Enable Vector Extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. System Approvals Table (Founder Telegram Gate)
CREATE TABLE IF NOT EXISTS public.system_approvals (
    proposal_id VARCHAR(64) PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    executive VARCHAR(32) NOT NULL,
    category VARCHAR(32) NOT NULL,
    title TEXT NOT NULL,
    impact_summary TEXT NOT NULL,
    risk_assessment VARCHAR(16) NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policy for System Approvals
ALTER TABLE public.system_approvals ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow authenticated service role read write" ON public.system_approvals
    FOR ALL USING (auth.role() = 'service_role');

-- 3. Scheduled Posts Table (AI CMO Social Reels Buffer Queue)
CREATE TABLE IF NOT EXISTS public.scheduled_posts (
    post_id VARCHAR(64) PRIMARY KEY,
    platform VARCHAR(32) NOT NULL,
    post_time TIMESTAMPTZ NOT NULL,
    caption TEXT NOT NULL,
    media_url TEXT NOT NULL,
    approval_status VARCHAR(16) NOT NULL DEFAULT 'PENDING',
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policy for Scheduled Posts
ALTER TABLE public.scheduled_posts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read of published posts" ON public.scheduled_posts
    FOR SELECT USING (published = true);

-- 4. Student Mastery Vectors Table (pgvector Memory)
CREATE TABLE IF NOT EXISTS public.student_mastery_vectors (
    student_id UUID NOT NULL,
    subject VARCHAR(32) NOT NULL,
    topic_id VARCHAR(64) NOT NULL,
    mastery_score FLOAT NOT NULL DEFAULT 0.0,
    embedding VECTOR(1536),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (student_id, topic_id)
);

-- Index for Fast Vector Search
CREATE INDEX IF NOT EXISTS idx_student_mastery_embedding 
ON public.student_mastery_vectors USING ivfflat (embedding vector_cosine_ops);
