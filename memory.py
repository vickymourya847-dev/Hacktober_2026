
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "vyra_memory.db"


def initialize_memory():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_message(role, content):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )


def get_history():
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute(
            "SELECT role, content FROM messages ORDER BY id"
        ).fetchall()


if __name__ == "__main__":
    initialize_memory()
    save_message("user", "Hello VYRA!")
    save_message("assistant", "Hello! I am VYRA.")

    for role, content in get_history():
        print(f"{role}: {content}")

    print("VYRA memory is working!")
