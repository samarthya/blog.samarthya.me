-- One row per drawing that has at least one heart. Nothing about the people who gave them.
CREATE TABLE IF NOT EXISTS hearts (
  id TEXT PRIMARY KEY,           -- the drawing id from data/bhanuni.yaml, e.g. c93dhk
  n  INTEGER NOT NULL DEFAULT 0  -- how many hearts
);

-- Reactions on blog posts: one row per post and reaction kind. Again, nothing about the people.
CREATE TABLE IF NOT EXISTS reactions (
  slug TEXT NOT NULL,             -- the post's URL name, e.g. security-standards-5-cve-cwe-nvd-cvss
  kind TEXT NOT NULL,             -- like | dislike | heart
  n    INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (slug, kind)
);
