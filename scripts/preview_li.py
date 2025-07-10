# scripts/preview_li.py
import pandas as pd
from bs4 import BeautifulSoup

# 1) Load raw HTML from your Words.txt
with open("../data/Words.txt", encoding="utf-8") as f:
    html = f.read()

# 2) Parse with BeautifulSoup
soup = BeautifulSoup(html, "lxml")

# 3) Extract <li> tags having both data-hw and data-ox5000
records = []
for li in soup.find_all("li", attrs={"data-hw": True, "data-ox5000": True}):
    word      = li["data-hw"].strip()
    level5000 = li["data-ox5000"].strip()
    level3000 = li.get("data-ox3000", "").strip()
    hidden    = "hidden" in (li.get("class") or [])
    records.append({
        "word": word,
        "level_3000": level3000,
        "level_5000": level5000,
        "hidden": hidden
    })

# 4) Create DataFrame and dedupe
df = pd.DataFrame(records)
df.drop_duplicates(subset=["word", "level_5000"], inplace=True)

# 5) Print first 20 rows to console
print(df.head(20).to_string(index=False))
print(f"\nTotal unique rows: {len(df)}")
