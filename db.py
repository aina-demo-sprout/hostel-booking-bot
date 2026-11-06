import sqlite3
from datetime import datetime

DB = "bookings.db"
ROOMS = ["DK1", "DK2", "DK3", "Bilik Study A"]


def _conn():
    return sqlite3.connect(DB)


def init():
    with _conn() as c:
        c.execute("CREATE TABLE IF NOT EXISTS bookings (user_id INTEGER, room TEXT, slot TEXT)")


def list_rooms():
    return ROOMS


def is_taken(room: str, slot: datetime) -> bool:
    with _conn() as c:
        row = c.execute("SELECT 1 FROM bookings WHERE room=? AND slot=?", (room, slot.isoformat())).fetchone()
    return row is not None


def add_booking(user_id: int, room: str, slot: datetime):
    with _conn() as c:
        c.execute("INSERT INTO bookings VALUES (?, ?, ?)", (user_id, room, slot.isoformat()))


def bookings_for(user_id: int):
    with _conn() as c:
        return c.execute("SELECT room, slot FROM bookings WHERE user_id=? ORDER BY slot", (user_id,)).fetchall()
