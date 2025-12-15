from pathlib import Path
import sys, os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- Paths ----------
BASE = Path(__file__).parent
DATA = BASE / "Data"
DATA.mkdir(exist_ok=True)

CSV_IN   = DATA / "dnd_classes_races_starter.csv"
MATRIX_CSV = DATA / "race_class_matrix.csv"
CLASS_BAR  = DATA / "class_counts.png"
RACE_PIE   = DATA / "race_pie.png"
HEATMAP    = DATA / "race_class_heatmap.png"
SESSIONS   = DATA / "sessions_log.csv"  # created if missing

if not CSV_IN.exists():
    raise FileNotFoundError(f"Missing dataset: {CSV_IN}\nPut your CSV in the Data/ folder.")

# ---------- Load ----------
df = pd.read_csv(CSV_IN)

# ---------- Text summaries ----------
print("\n== Head ==")
print(df.head())

print("\n== Classes ==")
print(df["Class"].value_counts())

print("\n== Races ==")
print(df["Race"].value_counts())

# Popularity by Class (optional extra)
if "Popularity" in df.columns:
    print("\n== Popularity by Class ==")
    print(df.groupby("Class")["Popularity"].value_counts())

# ---------- Race × Class matrix ----------
combo = pd.pivot_table(
    df,
    index="Race",
    columns="Class",
    values="Subclass",  # any non-null column works
    aggfunc="count",
    fill_value=0
)
print("\n== Race × Class ==")
print(combo)

combo.to_csv(MATRIX_CSV)
print(f"Saved matrix CSV → {MATRIX_CSV}")

# ---------- Charts ----------
# 1) Class bar chart
plt.figure()
df["Class"].value_counts().plot(kind="bar", title="Class Counts")
plt.xlabel("Class")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(CLASS_BAR)
plt.close()
print(f"Saved class bar → {CLASS_BAR}")

# 2) Race pie chart
plt.figure()
df["Race"].value_counts().plot(kind="pie", autopct="%1.1f%%", title="Race Distribution")
plt.ylabel("")  # cleaner
plt.tight_layout()
plt.savefig(RACE_PIE)
plt.close()
print(f"Saved race pie → {RACE_PIE}")

# 3) Heatmap for Race × Class matrix (with grid & cell labels)
plt.figure(figsize=(6.5, 4.5))
ax = plt.gca()
im = ax.imshow(combo, aspect="auto")  # default colormap

# ticks/labels
ax.set_xticks(range(len(combo.columns)))
ax.set_yticks(range(len(combo.index)))
ax.set_xticklabels(combo.columns, rotation=45, ha="right")
ax.set_yticklabels(combo.index)

# gridlines between cells
ax.set_xticks([x-0.5 for x in range(1, len(combo.columns))], minor=True)
ax.set_yticks([y-0.5 for y in range(1, len(combo.index))], minor=True)
ax.grid(which="minor", linestyle="-", linewidth=0.5)
ax.tick_params(which="minor", bottom=False, left=False)

# numbers in cells
for i in range(len(combo.index)):
    for j in range(len(combo.columns)):
        ax.text(j, i, str(combo.iloc[i, j]), ha="center", va="center")

plt.title("Race × Class Matrix")
plt.colorbar(im, label="Count")
plt.tight_layout()
plt.savefig(HEATMAP)
plt.close()
print(f"Saved heatmap → {HEATMAP}")

# ---------- Sessions log template (first-run helper) ----------
if not SESSIONS.exists():
    pd.DataFrame(columns=["Date", "Player", "Campaign", "Race", "Class", "Subclass"]).to_csv(SESSIONS, index=False)
    print(f"Created sessions log template → {SESSIONS}")

# ---------- Auto-open images on Windows (nice UX) ----------
if sys.platform.startswith("win"):
    for p in (CLASS_BAR, RACE_PIE, HEATMAP):
        try:
            os.startfile(p)  # type: ignore[attr-defined]
        except Exception:
            pass
