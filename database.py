import sqlite3

DB = "data/leads.db"


def init_db():
    conn = sqlite3.connect(DB)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        message_id INTEGER,
        text TEXT,
        score INTEGER,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(source, message_id)
    )
    """)

    conn.commit()
    conn.close()


def save_lead(source, message_id, text, score, category):
    conn = sqlite3.connect(DB)

    try:
        conn.execute(
            """
            INSERT INTO leads
            (source, message_id, text, score, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (source, message_id, text, score, category)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()
