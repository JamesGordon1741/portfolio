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

for cluster_id in range(N_CLUSTERS):
    centroid = kmeans.cluster_centers_[cluster_id]

    # top TF-IDF features for this cluster
    top_indices = centroid.argsort()[::-1][:100]
    freqs = {
        feature_names[i]: centroid[i]
        for i in top_indices
        if centroid[i] > 0
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
    plt.title(f"Cluster {cluster_id}", fontsize=16)
    plt.show()


# ----------------------------------------
# SAVE RESULTS
# ----------------------------------------
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved clustered data to {OUTPUT_CSV}")
