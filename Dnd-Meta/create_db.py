from pathlib import Path
import sqlite3
import pandas as pd

BASE = Path(__file__).parent
DB   = BASE / "dnd_meta.db"
SCHEMA = BASE / "schema.sql"

DATA = BASE / "Data"
CATALOG_CSV = DATA / "dnd_classes_races_starter.csv"
SESSIONS_CSV = DATA / "sessions_log.csv"
SESSION_PLAYERS_CSV = DATA / "session_players.csv"  # if you created it

def run_schema(conn: sqlite3.Connection, schema_path: Path):
    with schema_path.open("r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)

def load_csv_if_exists(conn, csv_path: Path, table: str):
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        df.to_sql(table, conn, if_exists="append", index=False)
        print(f"[ok] Loaded {csv_path.name} -> {table} ({len(df)} rows)")
    else:
        print(f"[skip] {csv_path.name} not found; skipping {table}")

def main():
    # create/overwrite DB
    if DB.exists():
        DB.unlink()
        print("[info] Removed previous DB")

    conn = sqlite3.connect(DB)
    try:
        # 1) Create tables
        run_schema(conn, SCHEMA)
        print("[ok] Applied schema.sql")

        # 2) Load seed data (if you want to pre-populate)
        load_csv_if_exists(conn, CATALOG_CSV, "CatalogRaw")
        load_csv_if_exists(conn, SESSIONS_CSV, "SessionsRaw")
        load_csv_if_exists(conn, SESSION_PLAYERS_CSV, "SessionPlayersRaw")  # if using a raw staging table

        conn.commit()
        print(f"[done] Database created at {DB}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()