import re
import glob
import pandas as pd
from itertools import count

# ----------------------------------------
# CONFIG
# ----------------------------------------
INPUT_GLOB = "/Users/jamesgordon/Desktop/James.txt.file.corpus.mini.project_2/*.txt"

# ----------------------------------------
# PROTECTED PHRASES
# ----------------------------------------
PROTECTED_PHRASES = ["le marabout"]

def protect_phrases(text, phrases):
    text = text.lower()
    for phrase in phrases:
        text = text.replace(phrase, phrase.replace(" ", "_"))
    return text

# ----------------------------------------
# NORMALIZATION
# ----------------------------------------
def normalize_text(text):
    text = text.replace("-", " ")
    text = re.sub(r"[’']", " ", text)
    text = re.sub(r"[^\w\sàâçéèêëîïôûùüÿñæœ.!?]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ----------------------------------------
# STOPWORDS & CLITICS
# ----------------------------------------
FRENCH_STOPWORDS = {
    "le","la","les","un","une","des","du","de","et","ou","mais","donc",
    "que","qui","quoi","dont","où","est","sont","être","avoir","avait",
    "ont","il","elle","ils","elles","je","tu","nous","vous","on"
}

FRENCH_CLITICS = {"l","d","j","m","s","t","c","n","qu"}
ALL_STOPWORDS = FRENCH_STOPWORDS | FRENCH_CLITICS

# ----------------------------------------
# LEMMA MAP
# ----------------------------------------
LEMMA_MAP = {
    "été": "etre",
    "etait": "etre",
    "étais": "etre",
    "avait": "avoir",
    "avais": "avoir"
}

def lemma_map(token):
    return LEMMA_MAP.get(token, token)

# ----------------------------------------
# SENTENCE SPLIT
# ----------------------------------------
def split_sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)

# ----------------------------------------
# TOKENIZE + FILTER
# ----------------------------------------
def tokenize_filter(text):
    tokens = re.findall(r"\b[a-zàâçéèêëîïôûùüÿñæœ_]+\b", text)
    tokens = [lemma_map(t) for t in tokens]
    return [t for t in tokens if t not in ALL_STOPWORDS and len(t) > 2]


# ----------------------------------------
# BUILD SENTENCE-LEVEL CORPUS
# ----------------------------------------
rows = []
sent_id = count(start=1)

for filepath in glob.glob(INPUT_GLOB):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    raw = protect_phrases(raw, PROTECTED_PHRASES)
    raw = normalize_text(raw)

    for sent in split_sentences(raw):
        tokens = tokenize_filter(sent)
        if len(tokens) < 5:
            continue

        rows.append({
            "sentence_id": next(sent_id),
            "source_file": filepath.split("/")[-1],
            "tokens": tokens,
            "text": " ".join(tokens)
        })

df_sentences = pd.DataFrame(rows)
df_sentences.to_csv("sentences_canonical3.csv", index=False)

print(f"Saved {len(df_sentences)} sentences to sentences_canonical3.csv")
