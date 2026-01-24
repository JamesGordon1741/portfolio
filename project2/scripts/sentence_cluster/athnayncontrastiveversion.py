import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

# ----------------------------------------
# CONFIG
# ----------------------------------------
INPUT_CSV = "sentences_canonical3.csv"
OUTPUT_CSV = "sentences_chunks_with_clusters4.csv"


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
    ngram_range=(1, 2),   # unigrams + bigrams
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

df["cluster"] = kmeans.fit_predict(X)

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

# ----------------------------------------
# TF-IDF WORD CLOUDS PER CLUSTER
# ----------------------------------------

# ----------------------------------------
# CONTRASTIVE TF-IDF WORD CLOUDS
# ----------------------------------------

import numpy as np

X_dense = X.toarray()

for cluster_id in range(N_CLUSTERS):
    cluster_mask = (df["cluster"] == cluster_id).values

    cluster_mean = X_dense[cluster_mask].mean(axis=0)
    other_mean = X_dense[~cluster_mask].mean(axis=0)

    # contrast score
    contrast = cluster_mean - other_mean

    top_indices = contrast.argsort()[::-1][:100]
    freqs = {
        feature_names[i]: contrast[i]
        for i in top_indices
        if contrast[i] > 0
    }

    wc = WordCloud(
        width=900,
        height=450,
        background_color="white",
        max_words=80,
        colormap="plasma"
    ).generate_from_frequencies(freqs)

    plt.figure(figsize=(11, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Cluster {cluster_id} (contrastive)", fontsize=16)
    plt.show()


    # ----------------------------------------
# AUTO CLUSTER LABELS (TF-IDF CENTROIDS)
# ----------------------------------------

def auto_label_cluster(cluster_id, top_n=3):
    centroid = kmeans.cluster_centers_[cluster_id]
    top_indices = centroid.argsort()[::-1][:top_n]
    return " / ".join(feature_names[i] for i in top_indices)

auto_labels = {
    cid: auto_label_cluster(cid)
    for cid in range(N_CLUSTERS)
}

df["cluster_label_auto"] = df["cluster"].map(auto_labels)

print("\n=== AUTO CLUSTER LABELS ===\n")
for cid, label in auto_labels.items():
    print(f"Cluster {cid}: {label}")



# ----------------------------------------
# SAVE RESULTS
# ----------------------------------------
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved clustered data to {OUTPUT_CSV}")
