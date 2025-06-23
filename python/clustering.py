import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import json

df = pd.read_csv('./dataset/journal-pseudo-label.csv', encoding='latin-1')
X  = df[['pseudo-label']].values

kmeans = KMeans(n_clusters=6, random_state=42).fit(X)
df['cluster'] = kmeans.labels_

# Urutkan centroid untuk mapping
centers      = kmeans.cluster_centers_.flatten()
sorted_idx   = np.argsort(centers)
labels       = ['Hampir Tidak Relevan','Kurang Relevan','Sedikit Berkaitan', 'Cukup Berkaitan', 'Sangat Berkaitan', 'Hampir Mirip Sempurna'][:len(sorted_idx)] 
cluster_map = {
    int(sorted_idx[i]): labels[i]
    for i in range(len(labels))
}

# Terapkan label
df['similarity_level'] = df['cluster'].map(cluster_map)
df.to_csv('./dataset/journal-clustered.csv', index=False)

# Persist model, dan mapping
joblib.dump(kmeans, './model/kmeans_model.joblib')
with open('./model/cluster_label_mapping.json','w') as f:
    json.dump(cluster_map, f, indent=2)

print("Selesai: model, dan mapping disimpan.")

plt.figure(figsize=(10,6))
sns.violinplot(x='similarity_level', y='pseudo-label', data=df, inner='quartile')
plt.title('Violin Plot Pseudo‑label per Level')
plt.xlabel('Similarity Level')
plt.ylabel('Pseudo‑label')
plt.tight_layout()
plt.savefig('./images/violin_plot_similarity_level.png')
plt.show()