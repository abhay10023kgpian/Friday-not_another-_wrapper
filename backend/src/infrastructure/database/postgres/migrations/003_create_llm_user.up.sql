-- 1. Create the dedicated LLM user
CREATE USER llm_user WITH PASSWORD 'llm_password123';

-- 2. Allow connecting to the database
GRANT CONNECT ON DATABASE ragdb TO llm_user;

-- 3. Allow accessing the public schema
GRANT USAGE ON SCHEMA public TO llm_user;

-- 4. GRANT ONLY SELECT (No INSERT, UPDATE, DELETE, DROP, ALTER)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO llm_user;

-- 5. Ensure future tables created also stay SELECT-only
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT SELECT ON TABLES TO llm_user;