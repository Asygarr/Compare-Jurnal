import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv('./dataset/silver-label.csv', encoding='latin-1')
X = df[['cosine_similarity']].values

inertia = []
silhouette = []
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)
    # silhouette.append(silhouette_score(X, kmeans.labels_))

# Plot Elbow Method
plt.figure(figsize=(12, 5))

# plt.subplot(1, 2, 1)
plt.plot(k_range, inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('Jumlah Cluster (k)')
plt.ylabel('Inertia (WCSS)')
plt.grid(True)

# Plot Silhouette Score
# plt.subplot(1, 2, 2)
# plt.plot(k_range, silhouette, marker='o', color='green')
# plt.title('Silhouette Score')
# plt.xlabel('Jumlah Cluster (k)')
# plt.ylabel('Silhouette Score')
# plt.grid(True)

plt.tight_layout()
# plt.savefig('./images/evaluasi_cluster.png')
plt.show()
