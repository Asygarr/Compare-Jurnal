import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json

# Load data
df = pd.read_csv('./dataset/journal-pseudo-label.csv', encoding='latin-1')
X  = df[['pseudo-label']].values

# Range cluster yang diuji
clusters_range = range(2, 10)
db_scores = []

# Cari cluster optimal pakai DB Score
for n_clusters in clusters_range:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(X)
    labels = kmeans.labels_
    db_score = davies_bouldin_score(X, labels)
    db_scores.append(db_score)
    print(f"Clusters: {n_clusters}, DB Score: {db_score:.4f}")

# Tentukan cluster optimal
optimal_clusters = clusters_range[np.argmin(db_scores)]
print(f"\nJumlah cluster optimal: {optimal_clusters} (DB Score: {min(db_scores):.4f})")

# Clustering final pakai jumlah optimal
final_kmeans = KMeans(n_clusters=optimal_clusters, random_state=42).fit(X)
df['cluster'] = final_kmeans.labels_

# Urutkan centroid untuk mapping label
centers = final_kmeans.cluster_centers_.flatten()
sorted_idx = np.argsort(centers)

# Mapping ke label sesuai urutan centroid (rendah ke tinggi)
labels = ['Hampir Tidak Relevan','Kurang Relevan','Sedikit Berkaitan', 'Cukup Berkaitan', 'Sangat Berkaitan', 'Hampir Mirip Sempurna'][:optimal_clusters]  # menyesuaikan jumlah cluster
cluster_map = {
    int(sorted_idx[i]): labels[i]
    for i in range(len(labels))
}

# Terapkan mapping label ke data
df['similarity_level'] = df['cluster'].map(cluster_map)

# Simpan hasil clustering
df.to_csv('./dataset/journal-clustered.csv', index=False)
print("✅ Hasil clustering disimpan di './dataset/journal-clustered.csv'")

# Simpan model clustering
joblib.dump(final_kmeans, './model/kmeans_model.joblib')
print("✅ Model clustering disimpan di './model/kmeans_model.joblib'")

# Simpan mapping cluster ke label
with open('./model/cluster_label_mapping.json', 'w') as f:
    json.dump(cluster_map, f, indent=2)
print("✅ Mapping cluster-label disimpan di './model/cluster_label_mapping.json'")

# Visualisasi Violin Plot
plt.figure(figsize=(10,5))
sns.violinplot(x='similarity_level', y='pseudo-label', data=df, inner='quartile')
plt.title('Violin Plot Pseudo‑label per Similarity Level')
plt.xlabel('Similarity Level')
plt.ylabel('Pseudo‑label')
plt.tight_layout()
plt.savefig('./images/violin_plot_similarity_level.png')
plt.show()
