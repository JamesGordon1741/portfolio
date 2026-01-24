import pandas as pd

INPUT_CSV = "sentences_chunks_with_clusters3.csv"
OUTPUT_CSV = "sentences_chunks_with_clusters_and_keywords3.csv"

KEYWORDS = [
    "Mahmadou",
    "Lamine",
    "Dramé",
    "Soybou",
    "Diana",
    "le marabout",
    "Ahmadou",
    "Hadj",
    "Ladj"
]

def normalize_keyword(kw):
    return kw.lower().replace("le ", "").strip()

KEYWORDS_NORM = [normalize_keyword(k) for k in KEYWORDS]

df = pd.read_csv(INPUT_CSV)

def find_keywords(text):
    return [kw for kw in KEYWORDS_NORM if kw in text]

df["matched_keywords"] = df["text"].apply(find_keywords)
df["primary_keyword"] = df["matched_keywords"].apply(
    lambda x: x[0] if x else None
)

df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved {OUTPUT_CSV}")


