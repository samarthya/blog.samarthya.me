-- One row per drawing that has at least one heart. Nothing about the people who gave them.
CREATE TABLE IF NOT EXISTS hearts (
  id TEXT PRIMARY KEY,           -- the drawing id from data/bhanuni.yaml, e.g. c93dhk
  n  INTEGER NOT NULL DEFAULT 0  -- how many hearts
);
