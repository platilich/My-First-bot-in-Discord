import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "bot.db"


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
                username TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                italian_word TEXT NOT NULL,
                translation TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, italian_word COLLATE NOCASE),
                FOREIGN KEY (user_id) REFERENCES users(discord_id)
            )
            """
        )
        conn.commit()


def add_user(discord_id: int, username: str) -> str:
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT discord_id FROM users WHERE discord_id = ?",
            (discord_id,),
        ).fetchone()

        if existing:
            conn.execute(
                "UPDATE users SET username = ? WHERE discord_id = ?",
                (username, discord_id),
            )
            conn.commit()
            return "Ты уже зарегистрирован!"

        conn.execute(
            "INSERT INTO users (discord_id, username) VALUES (?, ?)",
            (discord_id, username),
        )
        conn.commit()
        return "Добро пожаловать! Ты зарегистрирован."


def _ensure_user(conn: sqlite3.Connection, discord_id: int, username: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO users (discord_id, username) VALUES (?, ?)",
        (discord_id, username),
    )
    conn.execute(
        "UPDATE users SET username = ? WHERE discord_id = ?",
        (username, discord_id),
    )


def new_word(
    discord_id: int,
    username: str,
    italian_word: str,
    translation: str | None = None,
) -> str:
    italian_word = italian_word.strip()
    translation = translation.strip() if translation else None


    if not italian_word:
        return "Слово не может быть пустым."

    with get_connection() as conn:
        _ensure_user(conn, discord_id, username)

        try:
            conn.execute(
                """
                INSERT INTO words (user_id, italian_word, translation)
                VALUES (?, ?, ?)
                """,
                (discord_id, italian_word, translation),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return f"Слово «{italian_word}» уже есть в твоём словаре."

    if translation:
        return f"Добавлено: **{italian_word}** — {translation}"
    return f"Добавлено: **{italian_word}**"


def list_word(discord_id: int, username: str) -> str:
    with get_connection() as conn:
        _ensure_user(conn, discord_id, username)
        conn.commit()

        rows = conn.execute(
            """
            SELECT italian_word, translation
            FROM words
            WHERE user_id = ?
            ORDER BY created_at ASC, id ASC
            """,
            (discord_id,),
        ).fetchall()

    if not rows:
        return "Словарь пуст. Добавь слово командой `/add`."

    lines = [f"Твои итальянские слова ({len(rows)}):"]
    for i, row in enumerate(rows, 1):
        word = row["italian_word"]
        translation = row["translation"]
        if translation:
            lines.append(f"{i}. **{word}** — {translation}")
        else:
            lines.append(f"{i}. **{word}**")

    text = "\n".join(lines)
    if len(text) > 1900:
        text = text[:1900] + "\n…"
    return text
