# scripts/assign_lowest_level.py
from __future__ import annotations
import pandas as pd
from tabulate import tabulate

# 1) Load raw CSV (still contains duplicates and multiple levels)             #
SRC = "../output/words_5000.csv"          
OUT = "../output"

df = pd.read_csv(SRC, encoding="utf-8")

print(f"Raw rows loaded: {len(df)}")      

# 2) Minimal normalisation: trim + lowercase                                  #
df["word_norm"]  = df["word"].str.strip().str.lower()
df["level_norm"] = df["level_5000"].str.strip().str.lower()

difficulty  = ["a1", "a2", "b1", "b2", "c1"]
rank_map    = {lvl: i for i, lvl in enumerate(difficulty)}
df["rank"]  = df["level_norm"].map(rank_map)

# 3) Keep the row with the lowest rank for each distinct word                 #
idx = (
    df.sort_values(["word_norm", "rank"])      
      .drop_duplicates("word_norm", keep="first")
      .index
)

clean = (
    df.loc[idx, ["word_norm", "level_norm"]]
      .rename(columns={"word_norm": "word",
                       "level_norm": "level"})
      .reset_index(drop=True)
)

clean.insert(0, "ID", clean.index + 1)
clean["Keep"] = "T"

# 4) Export one CSV per level + gather counts                                 #
level_counts: dict[str, int] = {}
for lvl in difficulty:
    subset = clean[clean["level"] == lvl][["ID", "word"]]
    subset.to_csv(f"{OUT}/words_{lvl}.csv", index=False)
    level_counts[lvl] = len(subset)

clean.to_csv(f"{OUT}/words_clean_all_levels.csv", index=False)

# 5) Terminal summary                                                         #
summary = (
    pd.Series(level_counts, name="Words")
      .rename_axis("Level")
      .reset_index()
      .sort_values("Level", key=lambda s: s.map(rank_map))
)

print("\nExclusive-words summary (after trim/lower + dedup):\n")
print(tabulate(summary, headers="keys", tablefmt="github", showindex=False))

print("\nCSV files created in /output/:")
for lvl in difficulty:
    print(f"  • words_{lvl}.csv   ({level_counts[lvl]} words)")
print("  • words_clean_all_levels.csv (full table)")
