
import sqlite3
import uuid
from datetime import datetime, timezone
from memory import DB_PATH


def connect():
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def initialize_conversations():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS conversation_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            )
        """)


def create_conversation(title="New Chat"):
    chat_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    with connect() as db:
        db.execute(
            """
            INSERT INTO conversations (id, title, created_at)
            VALUES (?, ?, ?)
            """,
            (chat_id, title, created_at)
        )

    return {
        "id": chat_id,
        "title": title,
        "created_at": created_at
    }


def list_conversations():
    with connect() as db:
        rows = db.execute(
            """
            SELECT * FROM conversations
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def conversation_exists(chat_id):
    with connect() as db:
        row = db.execute(
            "SELECT id FROM conversations WHERE id = ?",
            (chat_id,)
        ).fetchone()

    return row is not None


def get_messages(chat_id):
    with connect() as db:
        rows = db.execute(
            """
            SELECT role, content, created_at
            FROM conversation_messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (chat_id,)
        ).fetchall()

    return [dict(row) for row in rows]


def save_exchange(chat_id, user_text, assistant_text):
    with connect() as db:
        if not db.execute(
            "SELECT 1 FROM conversations WHERE id = ?",
            (chat_id,)
        ).fetchone():
            raise ValueError("Conversation does not exist")

        db.executemany(
            """
            INSERT INTO conversation_messages
                (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            [
                (chat_id, "user", user_text),
                (chat_id, "assistant", assistant_text)
            ]
        )


def rename_conversation(chat_id, title):
    with connect() as db:
        cursor = db.execute(
            "UPDATE conversations SET title = ? WHERE id = ?",
            (title, chat_id)
        )
        return cursor.rowcount > 0


def delete_conversation(chat_id):
    with connect() as db:
        cursor = db.execute(
            "DELETE FROM conversations WHERE id = ?",
            (chat_id,)
        )
        return cursor.rowcount > 0
