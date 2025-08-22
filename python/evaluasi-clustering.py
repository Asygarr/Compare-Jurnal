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

# 1. Visualisasi Elbow Method (terpisah)
plt.figure(figsize=(10, 6))
plt.plot(k_range, inertia, marker='o', linewidth=2, markersize=8, color='#2E86AB')
plt.title('Elbow Method for Optimal Clusters', fontsize=14, fontweight='bold')
plt.xlabel('Jumlah Cluster (k)', fontsize=12)
plt.ylabel('Inertia (WCSS)', fontsize=12)
plt.grid(True, alpha=0.3)

# Highlight potential elbow point menggunakan metode "knee/elbow detection"
# Metode: mencari titik dengan jarak maksimum dari garis yang menghubungkan titik pertama dan terakhir
def find_elbow_point(k_values, inertia_values):
    # Normalisasi data untuk perhitungan jarak yang akurat
    k_norm = np.array(k_values) - k_values[0]
    inertia_norm = np.array(inertia_values) - inertia_values[-1]
    
    # Titik awal dan akhir
    p1 = np.array([k_norm[0], inertia_norm[0]])
    p2 = np.array([k_norm[-1], inertia_norm[-1]])
    
    # Hitung jarak dari setiap titik ke garis yang menghubungkan p1 dan p2
    distances = []
    for i in range(len(k_norm)):
        p = np.array([k_norm[i], inertia_norm[i]])
        # Jarak titik ke garis menggunakan rumus cross product
        distance = np.abs(np.cross(p2-p1, p1-p)) / np.linalg.norm(p2-p1)
        distances.append(distance)
    
    # Titik dengan jarak maksimum adalah elbow point
    elbow_idx = np.argmax(distances)
    return elbow_idx

elbow_idx = find_elbow_point(list(k_range), inertia)
elbow_k = k_range[elbow_idx]
elbow_inertia = inertia[elbow_idx]

# Sesuaikan posisi annotation agar tidak terlalu tinggi
inertia_range = max(inertia) - min(inertia)
offset_y = inertia_range * 0.1  # 10% dari range sebagai offset

plt.annotate(f'Elbow Point\nk={elbow_k}', 
            xy=(elbow_k, elbow_inertia), 
            xytext=(elbow_k+0.3, elbow_inertia+offset_y),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=10, ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

plt.tight_layout()
plt.savefig('./images/elbow_method.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Visualisasi Silhouette Score dan Davies-Bouldin Index (digabung)
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Silhouette Score (sumbu y kiri)
color1 = '#4ECDC4'
ax1.set_xlabel('Jumlah Cluster (k)', fontsize=12)
ax1.set_ylabel('Silhouette Score', color=color1, fontsize=12)
line1 = ax1.plot(k_range, silhouette, marker='o', linewidth=2, markersize=8, 
                color=color1, label='Silhouette Score')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, alpha=0.3)

# Highlight optimal silhouette score
max_sil_idx = np.argmax(silhouette)
max_sil_k = k_range[max_sil_idx]
max_sil_val = silhouette[max_sil_idx]
ax1.annotate(f'Max Silhouette\nk={max_sil_k}', 
            xy=(max_sil_k, max_sil_val), 
            xytext=(max_sil_k+0.5, max_sil_val+0.02),
            arrowprops=dict(arrowstyle='->', color=color1, lw=1.5),
            fontsize=10, ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))

# Plot Davies-Bouldin Score (sumbu y kanan)
ax2 = ax1.twinx()
color2 = '#FF6B6B'
ax2.set_ylabel('Davies-Bouldin Index', color=color2, fontsize=12)
line2 = ax2.plot(k_range, db_scores, marker='s', linewidth=2, markersize=8, 
                color=color2, label='Davies-Bouldin Index')
ax2.tick_params(axis='y', labelcolor=color2)

# Highlight optimal Davies-Bouldin score
min_db_idx = np.argmin(db_scores)
min_db_k = k_range[min_db_idx]
min_db_val = db_scores[min_db_idx]
ax2.annotate(f'Min DB Index\nk={min_db_k}', 
            xy=(min_db_k, min_db_val), 
            xytext=(min_db_k-0.5, min_db_val+0.05),
            arrowprops=dict(arrowstyle='->', color=color2, lw=1.5),
            fontsize=10, ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))

# Judul dan legend
plt.title('Silhouette Score dan Davies-Bouldin Index', fontsize=14, fontweight='bold')

# Combine legends
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center right', bbox_to_anchor=(0.98, 0.8))

plt.tight_layout()
plt.savefig('./images/silhouette_vs_davies_bouldin.png', dpi=300, bbox_inches='tight')
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
print(f"   - Elbow Method: './images/elbow_method.png'")
print(f"   - Silhouette vs DB Index: './images/silhouette_vs_davies_bouldin.png'")
print(f"   - Data: './results/cluster_evaluation_results.json'")
