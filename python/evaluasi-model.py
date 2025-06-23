import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr
from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset
import numpy as np

# Load dataset STS Benchmark
dataset = load_dataset("stsb_multi_mt", name="en", split="test")

# Load model
model_miniLM_L12 = SentenceTransformer("all-MiniLM-L12-v2")
model_distilbert = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")
model_mpnet = SentenceTransformer("all-mpnet-base-v2")

miniLM12_scores = []
distilbert_scores = []
mpnet_scores = []
ground_truth = []

for data in dataset:
    text1, text2 = data["sentence1"], data["sentence2"]
    true_score = data["similarity_score"] / 5.0

    emb1_miniLM_L12 = model_miniLM_L12.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_miniLM_L12 = model_miniLM_L12.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    emb1_distilbert = model_distilbert.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_distilbert = model_distilbert.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    emb1_mpnet = model_mpnet.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_mpnet = model_mpnet.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    score_miniLM_L12 = util.pytorch_cos_sim(emb1_miniLM_L12, emb2_miniLM_L12).item()
    score_distilbert = util.pytorch_cos_sim(emb1_distilbert, emb2_distilbert).item()
    score_mpnet = util.pytorch_cos_sim(emb1_mpnet, emb2_mpnet).item()

    miniLM12_scores.append(score_miniLM_L12)
    distilbert_scores.append(score_distilbert)
    mpnet_scores.append(score_mpnet)
    ground_truth.append(true_score)

# Hitung Pearson & Spearman
pearson_miniLM_L12, _ = pearsonr(miniLM12_scores, ground_truth)
spearman_miniLM_L12, _ = spearmanr(miniLM12_scores, ground_truth)

pearson_distilbert, _ = pearsonr(distilbert_scores, ground_truth)
spearman_distilbert, _ = spearmanr(distilbert_scores, ground_truth)

pearson_mpnet, _ = pearsonr(mpnet_scores, ground_truth)
spearman_mpnet, _ = spearmanr(mpnet_scores, ground_truth)

print(f"All-MiniLM-L12-v2: Pearson: {pearson_miniLM_L12:.4f}, Spearman: {spearman_miniLM_L12:.4f}")
print(f"DistilBERT: Pearson: {pearson_distilbert:.4f}, Spearman: {spearman_distilbert:.4f}")
print(f"MPNet: Pearson: {pearson_mpnet:.4f}, Spearman: {spearman_mpnet:.4f}")

models = ['MiniLM-L12-v2', 'DistilBERT', 'MPNet']
pearson_scores = [pearson_miniLM_L12, pearson_distilbert, pearson_mpnet]
spearman_scores = [spearman_miniLM_L12, spearman_distilbert, spearman_mpnet]

x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
bars1 = ax.bar(x - width/2, pearson_scores, width, label='Pearson', color='skyblue')
bars2 = ax.bar(x + width/2, spearman_scores, width, label='Spearman', color='lightgreen')

for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

ax.set_ylabel('Correlation Score')
ax.set_title('Pearson & Spearman Correlation per Model')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 1)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
