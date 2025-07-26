import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr
from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset
import numpy as np

# Load dataset STS Benchmark
dataset = load_dataset("stsb_multi_mt", name="en", split="test")

# Load models
model_mpnet = SentenceTransformer("all-mpnet-base-v2")
model_distilbert = SentenceTransformer("all-distilroberta-v1")
model_qa_mpnet = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

mpnetScores = []
distilbertScores = []
qaMpnetScores = []
ground_truth = []

for data in dataset:
    text1, text2 = data["sentence1"], data["sentence2"]
    true_score = data["similarity_score"] / 5.0

    emb1_distilbert = model_distilbert.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_distilbert = model_distilbert.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    emb1_mpnet = model_mpnet.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_mpnet = model_mpnet.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    emb1_qa_mpnet = model_qa_mpnet.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_qa_mpnet = model_qa_mpnet.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    score_distilbert = util.pytorch_cos_sim(emb1_distilbert, emb2_distilbert).item()
    score_mpnet = util.pytorch_cos_sim(emb1_mpnet, emb2_mpnet).item()
    score_qa_mpnet = util.pytorch_cos_sim(emb1_qa_mpnet, emb2_qa_mpnet).item()

    qaMpnetScores.append(score_qa_mpnet)
    distilbertScores.append(score_distilbert)
    mpnetScores.append(score_mpnet)
    ground_truth.append(true_score)

# Hitung Pearson & Spearman
pearson_qa_mpnet, _ = pearsonr(qaMpnetScores, ground_truth)
spearman_qa_mpnet, _ = spearmanr(qaMpnetScores, ground_truth)

pearson_distilbert, _ = pearsonr(distilbertScores, ground_truth)
spearman_distilbert, _ = spearmanr(distilbertScores, ground_truth)

pearson_mpnet, _ = pearsonr(mpnetScores, ground_truth)
spearman_mpnet, _ = spearmanr(mpnetScores, ground_truth)

print(f"QA MPNet - Pearson: {pearson_qa_mpnet:.4f}, Spearman: {spearman_qa_mpnet:.4f}")
print(f"DistilBERT - Pearson: {pearson_distilbert:.4f}, Spearman: {spearman_distilbert:.4f}")
print(f"MPNet - Pearson: {pearson_mpnet:.4f}, Spearman: {spearman_mpnet:.4f}")

models = ['QA MPNet', 'DistilBERT', 'MPNet']
pearson_scores = [pearson_qa_mpnet, pearson_distilbert, pearson_mpnet]
spearman_scores = [spearman_qa_mpnet, spearman_distilbert, spearman_mpnet]

x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
bars1 = ax.bar(x - width/2, pearson_scores, width, label='Pearson', color='skyblue')
bars2 = ax.bar(x + width/2, spearman_scores, width, label='Spearman', color='lightgreen')

for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height:.4f}',
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
