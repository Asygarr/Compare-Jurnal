import pandas as pd
from sentence_transformers import SentenceTransformer, util
from tqdm.auto import tqdm
# import numpy as np

model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

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

df.to_csv("dataset/journal-pseudo-label.csv", index=False)
print("Selesai! Data dengan pseudo-label tersimpan")

# model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

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