import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

df = pd.read_csv('./dataset/journal-pseudo-label.csv', encoding='latin-1')
X = df[['pseudo-label']].values

inertia = []
silhouette = []
db_scores = []
k_range = range(2, 9)

print("📊 Evaluasi Clustering untuk berbagai jumlah cluster:")
print("-" * 60)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    labels = kmeans.labels_
    
    inertia_val = kmeans.inertia_
    silhouette_val = silhouette_score(X, labels)
    db_score = davies_bouldin_score(X, labels)
    
    inertia.append(inertia_val)
    silhouette.append(silhouette_val)
    db_scores.append(db_score)
    
    print(f"k={k:2d} | Inertia: {inertia_val:8.2f} | Silhouette: {silhouette_val:.4f} | DB Score: {db_score:.4f}")

# Tentukan cluster optimal berdasarkan Davies-Bouldin Score
optimal_clusters_db = k_range[np.argmin(db_scores)]
optimal_clusters_sil = k_range[np.argmax(silhouette)]

# Plot Evaluasi Clustering
plt.figure(figsize=(13, 5))

# plt.subplot(1, 3, 1)
plt.subplot(1, 2, 1)
plt.plot(k_range, inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('Jumlah Cluster (k)')
plt.ylabel('Inertia (WCSS)')
plt.grid(True)

# Plot Silhouette Score
plt.subplot(1, 2, 2)
plt.plot(k_range, silhouette, marker='o', color='green')
plt.title('Silhouette Score')
plt.xlabel('Jumlah Cluster (k)')
plt.ylabel('Silhouette Score')
plt.grid(True)

# Plot Davies-Bouldin Score
# plt.subplot(1, 3, 3)
# plt.plot(k_range, db_scores, marker='o', color='red')
# plt.title('Davies-Bouldin Score')
# plt.xlabel('Jumlah Cluster (k)')
# plt.ylabel('Davies-Bouldin Score')
# plt.grid(True)

plt.tight_layout()
plt.savefig('./images/evaluasi_cluster-comprehensive.png', dpi=300, bbox_inches='tight')
plt.show()

# Simpan hasil evaluasi ke file JSON
import json
evaluation_results = {
    'cluster_evaluation': {
        str(k): {
            'inertia': float(inertia[i]),
            'silhouette_score': float(silhouette[i]),
            'davies_bouldin_score': float(db_scores[i])
        }
        for i, k in enumerate(k_range)
    },
    'optimal_clusters': {
        'davies_bouldin': int(optimal_clusters_db),
        'silhouette': int(optimal_clusters_sil)
    },
    'best_scores': {
        'min_davies_bouldin': float(min(db_scores)),
        'max_silhouette': float(max(silhouette))
    }
}

with open('./results/cluster_evaluation_results.json', 'w') as f:
    json.dump(evaluation_results, f, indent=2)

print(f"\n✅ Hasil evaluasi disimpan di:")
print(f"   - Grafik: './images/evaluasi_cluster-comprehensive.png'")
print(f"   - Data: './results/cluster_evaluation_results.json'")
