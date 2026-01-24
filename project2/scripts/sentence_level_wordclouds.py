import numpy as np

X = vectorizer.transform(df["text"])
feature_names = vectorizer.get_feature_names_out()

for cluster_id in range(N_CLUSTERS):
    centroid = kmeans.cluster_centers_[cluster_id]

    top_indices = centroid.argsort()[::-1][:100]
    freqs = {
        feature_names[i]: centroid[i]
        for i in top_indices if centroid[i] > 0
    }

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        max_words=100,
        colormap="plasma"
    ).generate_from_frequencies(freqs)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Cluster {cluster_id} (TF-IDF)", fontsize=16)
    plt.show()
