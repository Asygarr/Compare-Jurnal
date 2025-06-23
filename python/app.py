from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import joblib, json, re, numpy as np

app = FastAPI()
model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

kmeans = joblib.load("./model/kmeans_model.joblib")

with open("./model/cluster_label_mapping.json", "r") as f:
    raw_map = json.load(f)
cluster_label_mapping = {int(k): v for k, v in raw_map.items()}

class TextPair(BaseModel):
    text1: str
    text2: str

def preprocess_text(text: str) -> str:
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()

@app.post("/similarity/")
async def calculate_similarity(data: TextPair):
    t1 = preprocess_text(data.text1)
    t2 = preprocess_text(data.text2)

    emb1 = model.encode(t1, convert_to_tensor=True, normalize_embeddings=True)
    emb2 = model.encode(t2, convert_to_tensor=True, normalize_embeddings=True)
    sim  = util.pytorch_cos_sim(emb1, emb2).item()

    cluster_idx     = int(kmeans.predict([[sim]])[0])
    label_kemiripan = cluster_label_mapping[cluster_idx]
    
    # debugging
    # print(f"[DEBUG] t1='{t1}', t2='{t2}', sim={sim}, cluster_idx={cluster_idx}, label_kemiripan={label_kemiripan}")

    # Debugging output 
    # sim = 0.3910
    # similarity_array = np.array([[sim]])
    # cluster_idx = int(kmeans.predict(similarity_array)[0])
    # label_kemiripan = cluster_label_mapping.get(cluster_idx, "Unknown")
    # print(f"[DEBUG] sim={sim}, idx={cluster_idx}, label={label_kemiripan}")

    return {
        "similarity_score": sim,
        "cluster": cluster_idx,
        "label_kemiripan": label_kemiripan
    }
