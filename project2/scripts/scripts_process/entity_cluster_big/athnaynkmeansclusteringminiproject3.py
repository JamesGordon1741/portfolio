import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

# ----------------------------------------
# CONFIG
# ----------------------------------------
INPUT_CSV = "chunks_canonical.csv"
OUTPUT_CSV = "chunks_with_clusters.csv"

N_CLUSTERS = 6
TOP_WORDS = 15

# ----------------------------------------
# LOAD CANONICAL DATA
# ----------------------------------------
df = pd.read_csv(INPUT_CSV)

documents = df["text"].tolist()

# ----------------------------------------
# TF-IDF VECTORIZATION
# ----------------------------------------
vectorizer = TfidfVectorizer(
    max_df=0.9,
    min_df=3
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

df["cluster"] = kmeans.fit_predict(X)

# ----------------------------------------
# TOP WORDS PER CLUSTER
# ----------------------------------------
print("\n=== TOP WORDS PER CLUSTER ===\n")

for cluster_id in range(N_CLUSTERS):
    cluster_docs = df[df["cluster"] == cluster_id]["text"]

    tokens = []
    for doc in cluster_docs:
        tokens.extend(doc.split())

    counter = Counter(tokens)
    top_words = [w for w, _ in counter.most_common(TOP_WORDS)]

    print(f"Cluster {cluster_id}:")
    print("  " + ", ".join(top_words))
    print()

# ----------------------------------------
# SAVE RESULTS
# ----------------------------------------
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved clustered data to {OUTPUT_CSV}")
