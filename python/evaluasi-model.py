import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr
from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset

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

# head dataset
# print("Dataset STS Benchmark:")
# print("ID\tSentence 1\t\t\tSentence 2\t\t\tSimilarity Score")
# for i, data in enumerate(dataset):
#     if i < 5: 
#         print(f"{i}\t{data['sentence1']}\t{data['sentence2']}\t{data['similarity_score']}")

for data in dataset:
    text1, text2 = data["sentence1"], data["sentence2"]
    true_score = data["similarity_score"] / 5.0

    # Encode teks dengan kedua model
    emb1_miniLM_L12 = model_miniLM_L12.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_miniLM_L12 = model_miniLM_L12.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    emb1_distilbert = model_distilbert.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_distilbert = model_distilbert.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    emb1_mpnet = model_mpnet.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    emb2_mpnet = model_mpnet.encode(text2, convert_to_tensor=True, normalize_embeddings=True)

    # Hitung cosine similarity
    score_miniLM_L12 = util.pytorch_cos_sim(emb1_miniLM_L12, emb2_miniLM_L12).item()
    score_distilbert = util.pytorch_cos_sim(emb1_distilbert, emb2_distilbert).item()
    score_mpnet = util.pytorch_cos_sim(emb1_mpnet, emb2_mpnet).item()

    # Simpan skor
    miniLM12_scores.append(score_miniLM_L12)
    distilbert_scores.append(score_distilbert)
    mpnet_scores.append(score_mpnet)
    ground_truth.append(true_score)

#load semua score dari model dan ground truth
# print("Semua Skor Model:")
# print("ID\tAll-MiniLM-L6-v2\tAll-MiniLM-L12-v2\tMulti-QA-MiniLM-L6-cos-v1")
# for i in range(len(miniLM6_scores)):
#     print(f"{i}\t{miniLM6_scores[i]:.4f}\t\t{miniLM12_scores[i]:.4f}\t\t{multi_qa_scores[i]:.4f}")

# Evaluasi Korelasi

pearson_miniLM_L12, _ = pearsonr(miniLM12_scores, ground_truth)
spearman_miniLM_L12, _ = spearmanr(miniLM12_scores, ground_truth)

pearson_distilbert, _ = pearsonr(distilbert_scores, ground_truth)
spearman_distilbert, _ = spearmanr(distilbert_scores, ground_truth)

pearson_mpnet, _ = pearsonr(mpnet_scores, ground_truth)
spearman_mpnet, _ = spearmanr(mpnet_scores, ground_truth)

# Hasil evaluasi
print(f"All-MiniLM-L12-v2: Pearson: {pearson_miniLM_L12:.4f}, Spearman: {spearman_miniLM_L12:.4f}")
print(f"DistilBERT: Pearson: {pearson_distilbert:.4f}, Spearman: {spearman_distilbert:.4f}")
print(f"MPNet: Pearson: {pearson_mpnet:.4f}, Spearman: {spearman_mpnet:.4f}")

# Plot hasil evaluasi
plt.figure(figsize=(10, 5))
plt.scatter(ground_truth, miniLM12_scores, alpha=0.5, label="MiniLM", color="blue")
plt.scatter(ground_truth, distilbert_scores, alpha=0.5, label="DistilBERT", color="red")
plt.scatter(ground_truth, mpnet_scores, alpha=0.5, label="MPNet", color="green")
plt.xlabel("Ground Truth Similarity")
plt.ylabel("Model Similarity Score")
plt.legend()
plt.title("Evaluasi Model dengan STS Benchmark")
plt.show()
