import pandas as pd
from sentence_transformers import SentenceTransformer, util
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

model = SentenceTransformer("all-mpnet-base-v2")

df = pd.read_csv("./dataset/dataset-journal.csv", encoding="latin-1")

print(df.head())

all_sentences = pd.concat([df["abstract1"], df["abstract2"]]).unique().tolist()
sentence_to_emb = {}
for sent, emb in zip(all_sentences, model.encode(all_sentences, show_progress_bar=True, convert_to_tensor=True)):
    sentence_to_emb[sent] = emb

pseudo_scores = []
for a, b in tqdm(zip(df["abstract1"], df["abstract2"]), total=len(df)):
    emb_a = sentence_to_emb[a]
    emb_b = sentence_to_emb[b]
    score = util.cos_sim(emb_a, emb_b).item()

    pseudo_scores.append(score)

df["pseudo-label"] = pseudo_scores

# Hitung statistik deskriptif
mean_score = np.mean(pseudo_scores)
std_score = np.std(pseudo_scores)
skewness = stats.skew(pseudo_scores)
kurtosis = stats.kurtosis(pseudo_scores)

print("\n📊 Statistik Pseudo-label:")
print(f"   Mean: {mean_score:.4f}")
print(f"   Std Dev: {std_score:.4f}")
print(f"   Skewness: {skewness:.4f}")
print(f"   Kurtosis: {kurtosis:.4f}")
print(f"   Min: {min(pseudo_scores):.4f}")
print(f"   Max: {max(pseudo_scores):.4f}")

# Hitung distribusi per rentang
ranges = [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)]
range_counts = []

print("\n📊 Distribusi per Rentang Skor:")
for start, end in ranges:
    count = sum(1 for score in pseudo_scores if start <= score < end)
    percentage = (count / len(pseudo_scores)) * 100
    range_counts.append(percentage)
    print(f"   [{start:.2f} - {end:.2f}): {count:4d} pasangan ({percentage:5.1f}%)")

# Tambahkan kalimat deskriptif
max_range_idx = range_counts.index(max(range_counts))
min_range_idx = range_counts.index(min(range_counts))

print(f"\nSebagian besar pasangan jurnal ({range_counts[max_range_idx]:.0f}%) terkonsentrasi pada rentang skor {ranges[max_range_idx][0]:.1f}–{ranges[max_range_idx][1]:.1f}, ")
print(f"sementara sedikit pasangan ({range_counts[min_range_idx]:.0f}%) berada di rentang {ranges[min_range_idx][0]:.1f}–{ranges[min_range_idx][1]:.1f}.")

# Simpan dataset dengan pseudo-label
df.to_csv("dataset/journal-pseudo-label.csv", index=False)

# ========================= VISUALISASI PSEUDO-LABELING =========================
print("\n📊 Membuat visualisasi histogram dengan KDE...")

# Histogram Distribusi Pseudo-label dengan KDE
plt.figure(figsize=(10, 6))
plt.hist(pseudo_scores, bins=50, alpha=0.7, color='skyblue', edgecolor='black', density=True)
sns.kdeplot(pseudo_scores, color='red', linewidth=2)

# Tambahkan garis vertikal untuk mean
plt.axvline(mean_score, color='green', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.3f}')

# Tambahkan area rentang mean ± std
plt.axvspan(mean_score - std_score, mean_score + std_score, alpha=0.2, color='green', 
            label=f'Mean ± STD: [{mean_score-std_score:.3f}, {mean_score+std_score:.3f}]')

# Tambahkan informasi skewness
skew_text = f'Skewness: {skewness:.3f}'
if skewness > 0.5:
    skew_text += ' (Right-skewed)'
elif skewness < -0.5:
    skew_text += ' (Left-skewed)'
else:
    skew_text += ' (Fairly symmetric)'

plt.text(0.02, 0.95, skew_text, transform=plt.gca().transAxes, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
         verticalalignment='top')

plt.title('Distribusi Pseudo-label dengan KDE', fontsize=14, fontweight='bold')
plt.xlabel('Cosine Similarity Score')
plt.ylabel('Density')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('./images/pseudo_labeling_histogram-3.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\n✅ Visualisasi pseudo-labeling disimpan:")
print(f"   📊 Histogram dengan KDE: './images/pseudo_labeling_histogram-3.png'")
print(f"   📄 Dataset: 'dataset/journal-pseudo-label.csv'")

# model = SentenceTransformer("all-mpnet-base-v2")

# # 1. Muat dataset
# df = pd.read_csv("./dataset/dataset-journal.csv", encoding="latin-1")

# # 2. Pilih baris pertama
# abs1 = df.loc[0, "abstract1"]
# abs2 = df.loc[0, "abstract2"]

# # 3. Inisialisasi model dan encode kedua abstrak (L2-normalized, sebagai tensor)
# emb1 = model.encode(abs1, normalize_embeddings=True, convert_to_tensor=True)
# emb2 = model.encode(abs2, normalize_embeddings=True, convert_to_tensor=True)

# # 4. Pindahkan ke CPU dan ke numpy
# v1 = emb1.cpu().numpy()
# v2 = emb2.cpu().numpy()
# dot   = np.dot(v1, v2)
# norm1 = np.linalg.norm(v1)
# norm2 = np.linalg.norm(v2)

# print("vektor 1:", v1)
# print("vektor 2:", v2)

# # 5. Hitung cosine similarity
# cos_sim = dot / (norm1 * norm2)

# print(f"Dot product: {dot:.4f}")
# print(f"||v1|| = {norm1:.4f}, ||v2|| = {norm2:.4f}")
# print(f"Cosine similarity: {cos_sim:.4f}")