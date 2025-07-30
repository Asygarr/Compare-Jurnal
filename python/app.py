from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import joblib, json, re, numpy as np

app = FastAPI()
model = SentenceTransformer("all-mpnet-base-v2")

kmeans = joblib.load("./model/kmeans_model.joblib")

with open("./model/cluster_label_mapping.json", "r") as f:
    raw_map = json.load(f)
cluster_label_mapping = {int(k): v for k, v in raw_map.items()}

bilingual_labels = {
    "Tidak Relevan": "Not Relevant",
    "Sedikit Berkaitan": "Slightly Related",
    "Cukup Berkaitan": "Moderately Related",
    "Sangat Berkaitan": "Highly Related"
}

class TextPair(BaseModel):
    text1: str
    text2: str

def preprocess_text(text: str) -> str:
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

@app.post("/similarity/")
async def calculate_similarity(data: TextPair):
    t1 = preprocess_text(data.text1)
    t2 = preprocess_text(data.text2)

    print(f"Processing texts:\nText 1: {t1}\nText 2: {t2}")

    emb1 = model.encode(t1, convert_to_tensor=True, normalize_embeddings=True)
    emb2 = model.encode(t2, convert_to_tensor=True, normalize_embeddings=True)
    sim  = util.pytorch_cos_sim(emb1, emb2).item()

    cluster_idx     = int(kmeans.predict([[sim]])[0])
    label_kemiripan = cluster_label_mapping[cluster_idx]
    label_english = bilingual_labels.get(label_kemiripan, label_kemiripan)

    return {
        "similarity_score": sim,
        "cluster": cluster_idx,
        "label_kemiripan": label_kemiripan,
        "label_english": label_english,
        "bilingual_labels": {
            "indonesian": {
                "scoreLabel": "Skor Kemiripan",
                "similarity": label_kemiripan
            },
            "english": {
                "scoreLabel": "Similarity Score", 
                "similarity": label_english
            }
        }
    }
