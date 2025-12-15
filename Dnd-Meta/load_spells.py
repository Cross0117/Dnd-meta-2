# load_spells.py
import sqlite3
from pathlib import Path
import pandas as pd

# --- Paths ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

DB_PATH = BASE_DIR / "dnd_meta.db"                  # your existing DB
CSV_PATH = DATA_DIR / "spells_srd_sample.csv"       # adjust name if needed


def load_spells():
    # --- Read CSV ---------------------------------------------
    # on_bad_lines="warn" will keep reading even if a row has extra commas
    spells_df = pd.read_csv(CSV_PATH, on_bad_lines="warn")
    print("== Spells head ==")
    print(spells_df.head())

    # --- Normalise/rename columns so they match your schema ----
    # Adjust these if your CSV headers are slightly different
    rename_map = {
        "Spell Name": "Name",
        "Casting Time": "CastingTime",
        "Range": "Range",
        "Components": "Components",
        "Duration": "Duration",
        "Ritual": "Ritual",
        "Concentration": "Concentration",
        "Level": "Level",
        "School": "School",
        "Classes": "Classes",
    }
    # Only rename keys that actually exist
    spells_df = spells_df.rename(
        columns={k: v for k, v in rename_map.items() if k in spells_df.columns}
    )

    # --- Select just the columns we want to store --------------
    expected_cols = [
        "Name",
        "Level",
        "School",
        "CastingTime",
        "Range",
        "Components",
        "Duration",
        "Ritual",
        "Concentration",
        "Classes",
    ]

    # Keep only columns that both exist in the dataframe AND in expected_cols
    cols_to_keep = [c for c in expected_cols if c in spells_df.columns]
    spells_df = spells_df[cols_to_keep]

    # --- Clean boolean-ish columns (Ritual / Concentration) ----
    for col in ["Ritual", "Concentration"]:
        if col in spells_df.columns:
            spells_df[col] = (
                spells_df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map(
                    {
                        "yes": 1,
                        "y": 1,
                        "true": 1,
                        "t": 1,
                        "1": 1,
                        "no": 0,
                        "n": 0,
                        "false": 0,
                        "f": 0,
                        "0": 0,
                        "": 0,
                        "nan": 0,
                    }
                )
                .fillna(0)
                .astype(int)
            )

    # --- Write to SQLite ---------------------------------------
    with sqlite3.connect(DB_PATH) as conn:
        # This assumes you already created a Spells table in schema.sql
        # with matching column names.
        spells_df.to_sql("Spells", conn, if_exists="replace", index=False)

    print(f"[ok] Loaded {len(spells_df)} spells into Spells table.")


if __name__ == "__main__":
    load_spells()
