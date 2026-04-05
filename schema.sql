CREATE TABLE IF NOT EXISTS replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_email TEXT NOT NULL,
    tone TEXT NOT NULL,
    reply_length TEXT NOT NULL,
    generated_reply TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);