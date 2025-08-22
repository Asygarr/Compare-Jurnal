import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json

# # Load data
df = pd.read_csv('./dataset/journal-pseudo-label.csv', encoding='latin-1')
X = df[['pseudo-label']].values

# Hasil evaluasi menunjukkan k=4 optimal berdasarkan 3 metrik evaluasi
optimal_clusters = 4
print(f"🎯 Melakukan clustering dengan {optimal_clusters} cluster")
print("   (Jumlah optimal berdasarkan evaluasi 3 metrik)")

# Clustering final
final_kmeans = KMeans(n_clusters=optimal_clusters, random_state=42).fit(X)
df['cluster'] = final_kmeans.labels_

print(f"✅ Clustering selesai dengan {optimal_clusters} cluster")

# Urutkan centroid untuk mapping label
centers = final_kmeans.cluster_centers_.flatten()
sorted_idx = np.argsort(centers)

# Mapping ke label sesuai urutan centroid (rendah ke tinggi)
labels = ["Tidak Relevan", "Sedikit Berkaitan", "Cukup Berkaitan", "Sangat Berkaitan"]
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

# Visualisasi Violin Plot dengan warna berbeda untuk setiap level
plt.figure(figsize=(12, 6))

# Define color palette for different similarity levels
colors = ["#FF6B6B", "#FF8800", "#45D1A0", "#00FF04"]  # Red, Teal, Blue, Green
# Alternatively, you can use seaborn palettes:
# colors = sns.color_palette("Set2", n_colors=4)
# colors = sns.color_palette("husl", n_colors=4)

# Create violin plot with custom colors
ax = sns.violinplot(x='similarity_level', y='pseudo-label', data=df, 
                   inner='quartile', palette=colors)

# Customize the plot
plt.title('Violin Plot Pseudo‑label per Similarity Level', fontsize=14, fontweight='bold')
plt.xlabel('Similarity Level', fontsize=12)
plt.ylabel('Pseudo‑label', fontsize=12)

# Rotate x-axis labels if needed for better readability
plt.xticks(rotation=45, ha='right')

# Add grid for better readability
plt.grid(True, alpha=0.3, axis='y')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save with higher DPI for better quality
plt.savefig('./images/violin_plot_similarity_level.png', dpi=300, bbox_inches='tight')
plt.show()

# Print distribution information
print("\n📊 Distribusi data per similarity level:")
distribution = df['similarity_level'].value_counts().sort_index()
for level, count in distribution.items():
    percentage = (count / len(df)) * 100
    print(f"   {level}: {count} ({percentage:.1f}%)")

# Tabel rentang nilai pseudo-label per cluster
print("\n📋 Tabel Rentang Nilai Pseudo-label per Similarity Level:")
print("=" * 80)

# Buat tabel statistik untuk setiap similarity level
stats_table = []
for level in ["Tidak Relevan", "Sedikit Berkaitan", "Cukup Berkaitan", "Sangat Berkaitan"]:
    if level in df['similarity_level'].values:
        subset = df[df['similarity_level'] == level]['pseudo-label']
        stats = {
            'Similarity Level': level,
            'Count': len(subset),
            'Min': subset.min(),
            'Max': subset.max(), 
            'Mean': subset.mean(),
            'Median': subset.median(),
            'Std': subset.std()
        }
        stats_table.append(stats)

# Convert ke DataFrame untuk tampilan yang rapi
stats_df = pd.DataFrame(stats_table)

# Print tabel dengan format yang rapi
print(f"{'Similarity Level':<20} {'Count':<8} {'Min':<8} {'Max':<8} {'Mean':<8} {'Median':<8} {'Std':<8}")
print("-" * 80)
for _, row in stats_df.iterrows():
    print(f"{row['Similarity Level']:<20} {row['Count']:<8} {row['Min']:<8.3f} {row['Max']:<8.3f} {row['Mean']:<8.3f} {row['Median']:<8.3f} {row['Std']:<8.3f}")

print("\n🎯 Interpretasi Rentang:")
for _, row in stats_df.iterrows():
    level = row['Similarity Level']
    min_val = row['Min']
    max_val = row['Max']
    mean_val = row['Mean']
    print(f"   • {level}: {min_val:.3f} - {max_val:.3f} (rata-rata: {mean_val:.3f})")

# Simpan tabel statistik ke CSV
stats_df.to_csv('./dataset/cluster_statistics.csv', index=False)
print(f"\n✅ Tabel statistik clustering disimpan di './dataset/cluster_statistics.csv'")
