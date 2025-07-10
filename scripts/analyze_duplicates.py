# scripts/analyze_duplicates.py
import pandas as pd
from tabulate import tabulate

# 1) Load the CSV we just exported
df = pd.read_csv("../output/words_5000.csv", encoding="utf-8")

# 2) How many total rows vs. unique words?
total_rows = len(df)
unique_words = df["word"].nunique()

# 3) Compute frequency of each word
counts = df["word"].value_counts()

# 4) How many words occur more than once?
duplicates = counts[counts > 1]
num_duplicates = len(duplicates)

# 5) Display summary
print(f"Total rows:        {total_rows}")
print(f"Unique words:      {unique_words}")
print(f"Words with dupes:  {num_duplicates}\n")

# 6) Show top 20 duplicate words
top20 = duplicates.head(20).reset_index()
top20.columns = ["word", "count"]
print("Top 20 words with multiple entries:\n")
print(tabulate(top20, headers="keys", tablefmt="psql", showindex=False))

# 7) (Optional) Export full list of duplicates to CSV
duplicates.reset_index().to_csv("../output/duplicate_words.csv",
                               index=False,
                               header=["word", "count"])
print("\nExported full duplicate list to ../output/duplicate_words.csv")
