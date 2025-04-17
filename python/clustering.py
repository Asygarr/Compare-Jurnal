import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import joblib

df = pd.read_csv('./dataset/silver-label.csv', encoding='latin-1')

X = df[['cosine_similarity']].values

kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X)
joblib.dump(kmeans, './kmeans_model.joblib')

cluster_avg = df.groupby('cluster')['cosine_similarity'].mean()
sorted_clusters = cluster_avg.sort_values().index.tolist()

labels = ['Rendah', 'Sedang', 'Tinggi']
cluster_labels = dict(zip(sorted_clusters, labels))

df['similarity_level'] = df['cluster'].map(cluster_labels)
df.to_csv('./dataset/silver-label-clustered.csv', index=False)
print("Clustering selesai. Hasil disimpan di silver-label-clustered.csv")

plt.figure(figsize=(8, 5))
for label in ['Rendah', 'Sedang', 'Tinggi']:
    plt.hist(df[df['similarity_level'] == label]['cosine_similarity'], bins=10, alpha=0.6, label=label)
plt.title('Distribusi Similarity per Cluster')
plt.xlabel('Cosine Similarity')
plt.ylabel('Jumlah Data')
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.savefig("./images/cluster_visualization.png")
plt.show()
