import re
import glob
import pandas as pd
from itertools import count
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

# ----------------------------------------
# CONFIG
# ----------------------------------------
INPUT_GLOB = "/Users/jamesgordon/Desktop/James.txt.file.corpus.mini.project_2/*.txt"
OUTPUT_CSV = "sentences_canonical_keywords_window_clustered.csv"

MIN_TOKENS = 5
SLIDING_WINDOW = 2

N_CLUSTERS = 6
TOP_WORDS = 15

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
# KEYWORD SETUP (soft rule-oriented filtering)
# ----------------------------------------
KEYWORDS_GROUPS = {
    "Mahmadou": ["mahmadou"],
    "Lamine": ["lamine"],
    "Dramé": ["dramé"],
    "Soybou": ["soybou"],
    "Diana": ["diana"],
    "le marabout": ["le_marabout", "le_prophète"],
    "Hadj": ["hadj", "ladj"],
    "Ahmadou": ["ahmadou"],

}

ALL_KEYWORDS = [kw for variants in KEYWORDS_GROUPS.values() for kw in variants]

# ----------------------------------------
# BUILD SENTENCE-LEVEL CANONICAL CORPUS WITH KEYWORD WINDOW
# ----------------------------------------
rows = []
sent_id = count(start=1)

for filepath in glob.glob(INPUT_GLOB):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    raw = protect_phrases(raw, PROTECTED_PHRASES)
    raw = normalize_text(raw)
    sentences = split_sentences(raw)
    tokenized_sents = [tokenize_filter(s) for s in sentences]

    # find sentences with keywords + sliding window
    include_indices = set()
    for i, sent in enumerate(sentences):
        if any(kw in sent.lower() for kw in ALL_KEYWORDS):
            for j in range(max(0, i-SLIDING_WINDOW), min(len(sentences), i+SLIDING_WINDOW+1)):
                include_indices.add(j)

    for i in sorted(include_indices):
        tokens = tokenized_sents[i]
        if len(tokens) < MIN_TOKENS:
            continue
        # find matched keywords for this sentence
        matched_keywords = [kw for kw, variants in KEYWORDS_GROUPS.items() 
                            if any(v in sentences[i].lower() for v in variants)]
        primary_keyword = matched_keywords[0] if matched_keywords else None

        rows.append({
            "sentence_id": next(sent_id),
            "source_file": filepath.split("/")[-1],
            "tokens": tokens,
            "text": " ".join(tokens),
            "matched_keywords": matched_keywords,
            "primary_keyword": primary_keyword
        })

df_sentences = pd.DataFrame(rows)
print(f"Built corpus with {len(df_sentences)} sentences.")

# ----------------------------------------
# TF-IDF VECTORIZE
# ----------------------------------------
documents = df_sentences["text"].tolist()
vectorizer = TfidfVectorizer(
    ngram_range=(1,2),
    min_df=3,
    max_df=0.9
)
X = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

# ----------------------------------------
# KMEANS CLUSTERING
# ----------------------------------------
kmeans = KMeans(
    n_clusters=N_CLUSTERS,
    random_state=42,
    n_init=10
)
df_sentences["cluster"] = kmeans.fit_predict(X)

# ----------------------------------------
# CONTRASTIVE TF-IDF WORD CLOUDS PER CLUSTER
# ----------------------------------------
X_dense = X.toarray()
for cluster_id in range(N_CLUSTERS):
    cluster_mask = (df_sentences["cluster"] == cluster_id).values
    cluster_mean = X_dense[cluster_mask].mean(axis=0)
    other_mean = X_dense[~cluster_mask].mean(axis=0)
    contrast = cluster_mean - other_mean
    top_indices = contrast.argsort()[::-1][:100]
    freqs = {feature_names[i]: contrast[i] for i in top_indices if contrast[i] > 0}

    wc = WordCloud(
        width=900, height=450, background_color="white", max_words=80, colormap="plasma"
    ).generate_from_frequencies(freqs)

    plt.figure(figsize=(11,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Cluster {cluster_id} (contrastive)", fontsize=16)
    plt.show()

# ----------------------------------------
# AUTO CLUSTER LABELS
# ----------------------------------------
def auto_label_cluster(cluster_id, top_n=3):
    centroid = kmeans.cluster_centers_[cluster_id]
    top_indices = centroid.argsort()[::-1][:top_n]
    return " / ".join(feature_names[i] for i in top_indices)

auto_labels = {cid: auto_label_cluster(cid) for cid in range(N_CLUSTERS)}
df_sentences["cluster_label_auto"] = df_sentences["cluster"].map(auto_labels)

print("\n=== AUTO CLUSTER LABELS ===\n")
for cid, label in auto_labels.items():
    print(f"Cluster {cid}: {label}")

# ----------------------------------------
# SAVE RESULTS
# ----------------------------------------
df_sentences.to_csv(OUTPUT_CSV, index=False)
print(f"Saved clustered data to {OUTPUT_CSV}")
