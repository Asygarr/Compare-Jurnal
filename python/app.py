from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import joblib
import re
import numpy as np

app = FastAPI()
model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

kmeans = joblib.load("./kmeans_model.joblib")
cluster_label_mapping = {0: "Rendah", 1: "Sedang", 2: "Tinggi"} 

class TextPair(BaseModel):
    text1: str
    text2: str

def preprocess_text(text: str) -> str:
    text = re.sub(r"\n", " ", text)      # Menghapus newline
    text = re.sub(r"\s+", " ", text)     # Menghapus multiple spaces
    text = text.lower().strip()          # Mengubah teks menjadi lowercase dan menghapus leading/trailing spaces
    return text

@app.post("/similarity/")
async def calculate_similarity(data: TextPair):
    text1 = preprocess_text(data.text1)
    text2 = preprocess_text(data.text2)

    embedding1 = model.encode(text1, convert_to_tensor=True, normalize_embeddings=True)
    embedding2 = model.encode(text2, convert_to_tensor=True, normalize_embeddings=True)
    similarity = util.pytorch_cos_sim(embedding1, embedding2).item()

    similarity_array = np.array([[similarity]])
    predicted_cluster = kmeans.predict(similarity_array)[0]
    label_kemiripan = cluster_label_mapping[predicted_cluster]

    return {
        "similarity_score": similarity,
        "cluster": int(predicted_cluster),
        "label_kemiripan": label_kemiripan
    }
