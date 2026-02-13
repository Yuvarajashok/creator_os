/*
  # Creator OS Database Schema
  
  1. New Tables
    - `users`
      - `id` (uuid, primary key)
      - `email` (text, unique)
      - `full_name` (text)
      - `hashed_password` (text)
      - `role` (text, default 'user')
      - `is_active` (boolean, default true)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    
    - `pages`
      - `id` (uuid, primary key)
      - `user_id` (uuid, foreign key to users)
      - `instagram_username` (text, unique)
      - `instagram_id` (text, nullable)
      - `follower_count` (integer, default 0)
      - `following_count` (integer, default 0)
      - `post_count` (integer, default 0)
      - `bio` (text, nullable)
      - `profile_pic_url` (text, nullable)
      - `is_active` (boolean, default true)
      - `last_synced_at` (timestamptz, nullable)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    
    - `posts`
      - `id` (uuid, primary key)
      - `page_id` (uuid, foreign key to pages)
      - `instagram_post_id` (text, unique)
      - `post_type` (text: 'image', 'video', 'carousel', 'reel')
      - `caption` (text, nullable)
      - `media_url` (text, nullable)
      - `permalink` (text, nullable)
      - `timestamp` (timestamptz)
      - `like_count` (integer, default 0)
      - `comment_count` (integer, default 0)
      - `share_count` (integer, default 0)
      - `save_count` (integer, default 0)
      - `reach` (integer, default 0)
      - `impressions` (integer, default 0)
      - `engagement_rate` (numeric, default 0)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    
    - `daily_metrics`
      - `id` (uuid, primary key)
      - `page_id` (uuid, foreign key to pages)
      - `date` (date)
      - `follower_count` (integer)
      - `following_count` (integer)
      - `impressions` (integer, default 0)
      - `reach` (integer, default 0)
      - `profile_visits` (integer, default 0)
      - `website_clicks` (integer, default 0)
      - `email_contacts` (integer, default 0)
      - `engagement_total` (integer, default 0)
      - `created_at` (timestamptz)
    
    - `intelligence_scores`
      - `id` (uuid, primary key)
      - `page_id` (uuid, foreign key to pages)
      - `overall_score` (numeric)
      - `posting_consistency_score` (numeric)
      - `reach_trend_score` (numeric)
      - `conversion_health_score` (numeric)
      - `momentum_score` (numeric)
      - `engagement_stability_score` (numeric)
      - `viral_probability_score` (numeric)
      - `content_fatigue_penalty` (numeric)
      - `growth_stage` (text)
      - `recommendations` (jsonb)
      - `confidence_score` (numeric)
      - `metadata` (jsonb)
      - `created_at` (timestamptz)
  
  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users to access their own data
    - Add admin policies for full access
*/

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  email text UNIQUE NOT NULL,
  full_name text NOT NULL,
  hashed_password text NOT NULL,
  role text DEFAULT 'user' CHECK (role IN ('user', 'admin')),
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own data"
  ON users FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own data"
  ON users FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Pages table
CREATE TABLE IF NOT EXISTS pages (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  instagram_username text UNIQUE NOT NULL,
  instagram_id text,
  follower_count integer DEFAULT 0,
  following_count integer DEFAULT 0,
  post_count integer DEFAULT 0,
  bio text,
  profile_pic_url text,
  is_active boolean DEFAULT true,
  last_synced_at timestamptz,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE pages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own pages"
  ON pages FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own pages"
  ON pages FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own pages"
  ON pages FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own pages"
  ON pages FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Posts table
CREATE TABLE IF NOT EXISTS posts (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  page_id uuid NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
  instagram_post_id text UNIQUE NOT NULL,
  post_type text CHECK (post_type IN ('image', 'video', 'carousel', 'reel')),
  caption text,
  media_url text,
  permalink text,
  timestamp timestamptz NOT NULL,
  like_count integer DEFAULT 0,
  comment_count integer DEFAULT 0,
  share_count integer DEFAULT 0,
  save_count integer DEFAULT 0,
  reach integer DEFAULT 0,
  impressions integer DEFAULT 0,
  engagement_rate numeric DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read posts of own pages"
  ON posts FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM pages
      WHERE pages.id = posts.page_id
      AND pages.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert posts for own pages"
  ON posts FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM pages
      WHERE pages.id = posts.page_id
      AND pages.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update posts of own pages"
  ON posts FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM pages
      WHERE pages.id = posts.page_id
      AND pages.user_id = auth.uid()
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM pages
      WHERE pages.id = posts.page_id
      AND pages.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete posts of own pages"
  ON posts FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM pages
      WHERE pages.id = posts.page_id
      AND pages.user_id = auth.uid()
    )
  );

-- Daily metrics table
CREATE TABLE IF NOT EXISTS daily_metrics (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  page_id uuid NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
  date date NOT NULL,
  follower_count integer DEFAULT 0,
  following_count integer DEFAULT 0,
  impressions integer DEFAULT 0,
  reach integer DEFAULT 0,
  profile_visits integer DEFAULT 0,
  website_clicks integer DEFAULT 0,
  email_contacts integer DEFAULT 0,
  engagement_total integer DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  UNIQUE(page_id, date)
);

ALTER TABLE daily_metrics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read metrics of own pages"
  ON daily_metrics FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM pages
      WHERE pages.id = daily_metrics.page_id
      AND pages.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert metrics for own pages"
  ON daily_metrics FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM pages
      WHERE pages.id = daily_metrics.page_id
      AND pages.user_id = auth.uid()
    )
  );

-- Intelligence scores table
CREATE TABLE IF NOT EXISTS intelligence_scores (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  page_id uuid NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
  overall_score numeric NOT NULL,
  posting_consistency_score numeric DEFAULT 0,
  reach_trend_score numeric DEFAULT 0,
  conversion_health_score numeric DEFAULT 0,
  momentum_score numeric DEFAULT 0,
  engagement_stability_score numeric DEFAULT 0,
  viral_probability_score numeric DEFAULT 0,
  content_fatigue_penalty numeric DEFAULT 0,
  growth_stage text CHECK (growth_stage IN ('Dominant Growth', 'Stable Growth', 'At Risk', 'Critical')),
  recommendations jsonb DEFAULT '[]'::jsonb,
  confidence_score numeric DEFAULT 0,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE intelligence_scores ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read intelligence scores of own pages"
  ON intelligence_scores FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM pages
      WHERE pages.id = intelligence_scores.page_id
      AND pages.user_id = auth.uid()
    )
  );

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_pages_user_id ON pages(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_page_id ON posts(page_id);
CREATE INDEX IF NOT EXISTS idx_posts_timestamp ON posts(timestamp);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_page_id ON daily_metrics(page_id);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_date ON daily_metrics(date);
CREATE INDEX IF NOT EXISTS idx_intelligence_scores_page_id ON intelligence_scores(page_id);
CREATE INDEX IF NOT EXISTS idx_intelligence_scores_created_at ON intelligence_scores(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add triggers for updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_pages_updated_at ON pages;
CREATE TRIGGER update_pages_updated_at
  BEFORE UPDATE ON pages
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_posts_updated_at ON posts;
CREATE TRIGGER update_posts_updated_at
  BEFORE UPDATE ON posts
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
