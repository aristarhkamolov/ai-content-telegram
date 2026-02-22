import sqlite3
from typing import Any


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    niche TEXT,
                    style TEXT,
                    goal TEXT,
                    audience TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def upsert_user_field(self, telegram_id: int, field: str, value: str) -> None:
        if field not in {"niche", "style", "goal", "audience"}:
            raise ValueError("Unsupported field")

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO users(telegram_id, niche, style, goal, audience)
                VALUES(?, '', '', '', '')
                ON CONFLICT(telegram_id) DO NOTHING
                """,
                (telegram_id,),
            )
            conn.execute(
                f"""
                UPDATE users
                SET {field} = ?, updated_at = CURRENT_TIMESTAMP
                WHERE telegram_id = ?
                """,
                (value, telegram_id),
            )

    def get_user(self, telegram_id: int) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT telegram_id, niche, style, goal, audience FROM users WHERE telegram_id = ?",
                (telegram_id,),
            ).fetchone()
            return dict(row) if row else None

    def is_profile_complete(self, telegram_id: int) -> bool:
        user = self.get_user(telegram_id)
        if not user:
            return False
        return all(user.get(key, "").strip() for key in ("niche", "style", "goal", "audience"))
