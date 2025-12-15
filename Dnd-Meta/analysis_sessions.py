# sessions_analysis.py
"""
Analyze the second dataset (sessions_log.csv) and connect it to the catalog.

Outputs (in Data/):
- sessions_clean.csv
- played_class_counts.png
- played_race_counts.png
- sessions_race_class_matrix.csv
- sessions_race_class_heatmap.png
- sessions_vs_catalog_mismatches.csv (rows that don't match the catalog)
"""

from pathlib import Path
import sys
import argparse
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless save
import matplotlib.pyplot as plt


# --------------------- Paths & CLI ---------------------
def make_parser():
    p = argparse.ArgumentParser(description="Analyze D&D sessions log and join with catalog.")
    p.add_argument("--data-dir", default="Data", help="Folder with CSVs and where outputs are saved")
    p.add_argument("--sessions", default="sessions_log.csv", help="Sessions CSV filename inside data-dir")
    p.add_argument("--catalog", default="dnd_classes_races_starter.csv", help="Catalog CSV filename inside data-dir")
    p.add_argument("--clean-catalog", default="dnd_classes_races_clean.csv",
                   help="If present, use the cleaned catalog first (inside data-dir)")
    p.add_argument("--no-plots", action="store_true", help="Skip PNG plots")
    return p


# --------------------- Utils ---------------------
def tcase(s: pd.Series) -> pd.Series:
    """Normalize to Title Case (safe for NaNs)."""
    return s.astype(str).str.strip().str.title()


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def save_fig(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f"[ok] Saved → {path}")


# --------------------- Loaders ---------------------
def load_sessions(data_dir: Path, fname: str) -> pd.DataFrame:
    fp = data_dir / fname
    if not fp.exists():
        sys.exit(f"[ERROR] Missing sessions CSV: {fp}")
    df = pd.read_csv(fp)
    # expected columns
    expected = {"Date", "Player", "Campaign", "Race", "Class", "Subclass"}
    missing_cols = expected - set(df.columns)
    if missing_cols:
        sys.exit(f"[ERROR] sessions CSV missing columns: {missing_cols}\nFound: {list(df.columns)}")
    # normalize
    for c in ("Race", "Class", "Subclass", "Player", "Campaign"):
        df[c] = tcase(df[c])
    # parse dates
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def load_catalog(data_dir: Path, clean_name: str, raw_name: str) -> pd.DataFrame:
    clean_fp = data_dir / clean_name
    raw_fp = data_dir / raw_name
    if clean_fp.exists():
        cat = pd.read_csv(clean_fp)
        src = clean_fp
    elif raw_fp.exists():
        cat = pd.read_csv(raw_fp)
        src = raw_fp
    else:
        sys.exit(f"[ERROR] Missing catalog CSV. Looked for {clean_fp} and {raw_fp}")

    # normalize join keys
    for c in ("Race", "Class", "Subclass"):
        if c in cat.columns:
            cat[c] = tcase(cat[c])
    # optional numeric conversions if available
    if "Hit Die" in cat.columns and "HitDieNum" not in cat.columns:
        num = cat["Hit Die"].astype(str).str.strip().str.lower().str.replace("d", "", regex=False)
        cat["HitDieNum"] = pd.to_numeric(num, errors="coerce")
    print(f"[info] Loaded catalog from {src}")
    return cat


# --------------------- EDA ---------------------
def inspect_block(df: pd.DataFrame, name: str):
    print(f"\n== {name}.info ==")
    print(df.info())
    print(f"\n== {name}.isna ==")
    print(df.isna().sum())
    print(f"\n== {name}.duplicates ==")
    print(int(df.duplicated().sum()))
    print(f"\n== {name}.describe ==")
    print(df.describe(include="all"))


# --------------------- Analysis ---------------------
def analyze_sessions_only(sessions: pd.DataFrame, data_dir: Path, no_plots: bool):
    # Counts
    cls_counts = sessions["Class"].value_counts().sort_values(ascending=False)
    race_counts = sessions["Race"].value_counts().sort_values(ascending=False)

    print("\n== Most played classes ==")
    print(cls_counts)
    print("\n== Most played races ==")
    print(race_counts)

    # Played Race × Class matrix
    played_matrix = pd.crosstab(sessions["Race"], sessions["Class"])
    print("\n== Played Race × Class (raw sessions) ==")
    print(played_matrix)

    # Save clean sessions
    out_sessions = data_dir / "sessions_clean.csv"
    sessions.to_csv(out_sessions, index=False)
    print(f"[ok] Saved → {out_sessions}")

    # Save matrix
    out_matrix = data_dir / "sessions_race_class_matrix.csv"
    played_matrix.to_csv(out_matrix)
    print(f"[ok] Saved → {out_matrix}")

    # Plots
    if not no_plots:
        plt.figure()
        cls_counts.plot(kind="bar", title="Played Class Counts")
        plt.xlabel("Class"); plt.ylabel("Count")
        save_fig(data_dir / "played_class_counts.png")

        plt.figure()
        race_counts.plot(kind="bar", title="Played Race Counts")
        plt.xlabel("Race"); plt.ylabel("Count")
        save_fig(data_dir / "played_race_counts.png")


def join_with_catalog(sessions: pd.DataFrame, catalog: pd.DataFrame, data_dir: Path, no_plots: bool):
    # we only need distinct catalog keys for validation
    cat_keys = catalog[["Race", "Class", "Subclass"]].drop_duplicates()
    joined = sessions.merge(cat_keys, on=["Race", "Class", "Subclass"], how="left", indicator=True)

    # Find mismatches (session rows that don't exist in catalog)
    mismatches = joined.loc[joined["_merge"] == "left_only",
                            ["Date", "Player", "Campaign", "Race", "Class", "Subclass"]]
    if not mismatches.empty:
        out_bad = data_dir / "sessions_vs_catalog_mismatches.csv"
        mismatches.to_csv(out_bad, index=False)
        print(f"[warn] Found {len(mismatches)} sessions not in catalog → {out_bad}")
    else:
        print("[ok] All session rows match catalog options.")

    # Valid rows only
    valid = joined.loc[joined["_merge"] == "both"].copy()
    if valid.empty:
        print("[warn] No valid session rows matched the catalog; check spelling/casing.")
        return

    # Played matrix (validated)
    matrix = pd.crosstab(valid["Race"], valid["Class"])
    out_matrix = data_dir / "sessions_race_class_matrix.csv"
    matrix.to_csv(out_matrix)
    print(f"[ok] Saved validated matrix → {out_matrix}")
    print("\n== Played Race × Class (validated vs catalog) ==")
    print(matrix)

    # Heatmap
    if not no_plots:
        plt.figure(figsize=(max(6.5, 0.7 * len(matrix.columns)), max(4.5, 0.5 * len(matrix.index))))
        ax = plt.gca()
        im = ax.imshow(matrix, aspect="auto")
        ax.set_xticks(range(len(matrix.columns)))
        ax.set_yticks(range(len(matrix.index)))
        ax.set_xticklabels(matrix.columns, rotation=45, ha="right")
        ax.set_yticklabels(matrix.index)

        # gridlines
        ax.set_xticks([x - 0.5 for x in range(1, len(matrix.columns))], minor=True)
        ax.set_yticks([y - 0.5 for y in range(1, len(matrix.index))], minor=True)
        ax.grid(which="minor", linestyle="-", linewidth=0.5)
        ax.tick_params(which="minor", bottom=False, left=False)

        # numbers in cells
        for i in range(len(matrix.index)):
            for j in range(len(matrix.columns)):
                ax.text(j, i, str(matrix.iloc[i, j]), ha="center", va="center")

        plt.title("Sessions: Race × Class (Validated)")
        plt.colorbar(im, label="Count")
        save_fig(data_dir / "sessions_race_class_heatmap.png")


# --------------------- Main ---------------------
def main():
    args = make_parser().parse_args()
    base = Path(__file__).parent.resolve()
    data_dir = (base / args.data_dir).resolve()
    ensure_dir(data_dir)

    # Load
    sessions = load_sessions(data_dir, args.sessions)
    catalog = load_catalog(data_dir, args.clean_catalog, args.catalog)

    # Inspect
    inspect_block(sessions, "sessions")
    # (catalog inspection optional here)
    # inspect_block(catalog, "catalog")

    # Analyze sessions alone
    analyze_sessions_only(sessions, data_dir, args.no_plots)

    # Join sessions ↔ catalog
    join_with_catalog(sessions, catalog, data_dir, args.no_plots)

    print("\nDone.")


if __name__ == "__main__":
    main()
