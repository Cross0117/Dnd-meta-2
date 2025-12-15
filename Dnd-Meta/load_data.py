import sqlite3
from pathlib import Path

DB_PATH = Path("dnd_meta.db")
SQL_PATH = Path("insert_sample_data.sql")

conn = sqlite3.connect(DB_PATH)
try:
    conn.execute("PRAGMA foreign_keys = ON;")
    sql = SQL_PATH.read_text(encoding="utf-8")
    conn.executescript(sql)
    conn.commit()
    print("✅ Sample data inserted into Races, Classes, Players, Campaigns, Sessions, SessionPlayers")
finally:
    conn.close()