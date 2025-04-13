import pandas as pd
from sentence_transformers import SentenceTransformer, util
from tqdm.auto import tqdm

model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

df = pd.read_csv("./dataset/dataset-jurnal-test.csv", encoding="latin-1")

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
    score = round(score, 2)

    pseudo_scores.append(score)

df["cosine_similarity"] = pseudo_scores

df.to_csv("dataset/data_abstrak_with_pseudo_labels.csv", index=False)
print("Selesai! Data dengan pseudo-label tersimpan di data_abstrak_with_pseudo_labels.csv")