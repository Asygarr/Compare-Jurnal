from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import joblib
import re
import numpy as np

app = FastAPI()

# model = SentenceTransformer("./fine_tuned_model")

model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")
kmeans = joblib.load('./kmeans_model.joblib')

cluster_labels = {0: "Rendah", 1: "Sedang", 2: "Tinggi"} 

cluster_centers = kmeans.cluster_centers_.squeeze()
sorted_indices = np.argsort(cluster_centers)
sorted_labels = ['Rendah', 'Sedang', 'Tinggi']
cluster_labels = {idx: label for idx, label in zip(sorted_indices, sorted_labels)}

class TextPair(BaseModel):
    text1: str
    text2: str

def preprocess_text(text: str) -> str:
    text = re.sub(r"[^\w\s]", "", text)  # Menghapus special characters, seperti !, ?, dll
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
    
    predicted_cluster = kmeans.predict([[similarity]])[0]
    similarity_level = cluster_labels[predicted_cluster]

    return {"similarity_score": similarity, "label_kemiripan": similarity_level}