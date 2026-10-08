import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "users.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                discord_id INTEGER PRIMARY KEY,
                nickname TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                cursing INTEGER
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS gifs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_gif TEXT NOT NULL,
                discord_id INTEGER NOT NULL,
                FOREIGN KEY (discord_id) REFERENCES users (discord_id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()


def save_user(discord_id, nickname):
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT discord_id FROM users WHERE discord_id = ?",
            (discord_id,),
        ).fetchone()

        if existing:
            conn.execute(
                "UPDATE users SET nickname = ? WHERE discord_id = ?",
                (nickname, discord_id),
            )
            conn.commit()
            return

        conn.execute(
            "INSERT INTO users (discord_id, nickname) VALUES (?, ?)",
            (discord_id, nickname),
        )
        conn.commit()

        return



def curse_count(discord_id):
    with get_connection() as conn:
        try:
            conn.execute('UPDATE users SET cursing = cursing + 1 WHERE discord_id = ?', (discord_id, ))

            conn.commit()


        except Exception as e:
            print(e)



def save_gif(discord_id, gif_url):
    with get_connection() as conn:
        try:
            conn.execute(
                """
                INSERT INTO gifs (discord_id, url_gif)
                VALUES (?, ?)
                """,
                (discord_id, gif_url),
            )
            conn.commit()

        except sqlite3.IntegrityError:
            return f"Gif {gif_url} already added."


    return f"Added"



def list_gifs():
    with get_connection() as conn:

        rows = conn.execute('SELECT url_gif FROM gifs').fetchall()

    if not rows:
        return False


    return [gif['url_gif'] for gif in rows]