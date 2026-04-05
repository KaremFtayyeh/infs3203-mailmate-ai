import sqlite3

DATABASE = "database.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def save_reply(original_email, tone, reply_length, generated_reply):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO replies (original_email, tone, reply_length, generated_reply)
        VALUES (?, ?, ?, ?)
        """,
        (original_email, tone, reply_length, generated_reply),
    )
    conn.commit()
    conn.close()


def get_all_replies():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM replies ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows