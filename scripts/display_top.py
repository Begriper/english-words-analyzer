# scripts/display_top.py
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate

# 1) Load raw HTML from Words.txt
with open("../data/Words.txt", encoding="utf-8") as f:
    html = f.read()

# 2) Parse the HTML
soup = BeautifulSoup(html, "lxml")

# 3) Extract records just like before
records = []
for li in soup.find_all("li", attrs={"data-hw": True, "data-ox5000": True}):
    word      = li["data-hw"].strip()
    level5000 = li["data-ox5000"].strip()
    records.append({"word": word, "level_5000": level5000})

# 4) Build DataFrame and dedupe
df = pd.DataFrame(records)
df = df.drop_duplicates(subset=["word", "level_5000"])

# 5) Subset to only two columns
df = df[["word", "level_5000"]]

# 6) Display first 10 rows as a pretty table
print(tabulate(df.head(10),
               headers=["Word", "Level"],
               showindex=False,
               tablefmt="grid"))

# 7) (Optional) Save full result to CSV
df.to_csv("../output/words_5000.csv", index=False)
