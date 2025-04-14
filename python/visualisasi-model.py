import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from sentence_transformers import SentenceTransformer, util

df_gold = pd.read_csv("./dataset/gold-label.csv", encoding="latin-1")

model_awal = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")
model_ft   = SentenceTransformer("./fine_tuned_model")

texts1 = df_gold["abstract1"].tolist()
texts2 = df_gold["abstract2"].tolist()
gold_labels = df_gold["cosine_similarity"].tolist()

embeddings_awal_1 = model_awal.encode(texts1, convert_to_tensor=True)
embeddings_awal_2 = model_awal.encode(texts2, convert_to_tensor=True)
pred_awal = util.cos_sim(embeddings_awal_1, embeddings_awal_2).diagonal().tolist()

embeddings_ft_1 = model_ft.encode(texts1, convert_to_tensor=True)
embeddings_ft_2 = model_ft.encode(texts2, convert_to_tensor=True)
pred_ft = util.cos_sim(embeddings_ft_1, embeddings_ft_2).diagonal().tolist()

df_vis = pd.DataFrame({
    "Gold_Label": gold_labels,
    "Prediksi_Awal": pred_awal,
    "Prediksi_FT": pred_ft
})

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
sns.regplot(x="Gold_Label", y="Prediksi_Awal", data=df_vis, scatter_kws={"s": 30}, line_kws={"color": "red"})
plt.title("Sebelum Fine-Tuning")
plt.xlabel("Gold Label")
plt.ylabel("Prediksi Similarity")

p1, _ = pearsonr(df_vis["Gold_Label"], df_vis["Prediksi_Awal"])
s1, _ = spearmanr(df_vis["Gold_Label"], df_vis["Prediksi_Awal"])
plt.text(0.05, 0.95, f"Pearson: {p1:.2f}\nSpearman: {s1:.2f}", transform=plt.gca().transAxes)

plt.subplot(1, 2, 2)
sns.regplot(x="Gold_Label", y="Prediksi_FT", data=df_vis, scatter_kws={"s": 30}, line_kws={"color": "green"})
plt.title("Setelah Fine-Tuning")
plt.xlabel("Gold Label")
plt.ylabel("Prediksi Similarity")

p2, _ = pearsonr(df_vis["Gold_Label"], df_vis["Prediksi_FT"])
s2, _ = spearmanr(df_vis["Gold_Label"], df_vis["Prediksi_FT"])
plt.text(0.05, 0.95, f"Pearson: {p2:.2f}\nSpearman: {s2:.2f}", transform=plt.gca().transAxes)

plt.tight_layout()
plt.show()
