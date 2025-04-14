from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import re

app = FastAPI()
# model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
model = SentenceTransformer("./fine_tuned_model")

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
    
    labelKemiripan = "tidak mirip"
    if similarity >= 0.7:
        labelKemiripan = "sangat mirip"
    elif similarity >= 0.4:
        labelKemiripan = "mirip"
    elif similarity < 0.4:
        labelKemiripan = "tidak mirip"

    return {"similarity_score": similarity, "label_kemiripan": labelKemiripan}





# from transformers import BertTokenizer, BertModel
# from fastapi import FastAPI
# from pydantic import BaseModel
# import torch
# from scipy.spatial.distance import cosine

# app = FastAPI()

# MODEL_NAME = "bert-base-multilingual-cased"
# TOKENIZER = BertTokenizer.from_pretrained(MODEL_NAME)
# MODEL = BertModel.from_pretrained(MODEL_NAME)

# class TextPair(BaseModel):
#     text1: str
#     text2: str

# @app.post("/similarity/")
# async def calculate_similarity(data: TextPair):
#     try:
#         similarity_score = calculate_similarity(data.text1, data.text1, MODEL, TOKENIZER)

#         return {"similarity_score": float(similarity_score)}
#     except Exception as e:
#         return {"error": str(e)}

# def get_bert_embeddings(text, model, tokenizer):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
#     with torch.no_grad():
#         outputs = model(**inputs)

#     embeddings = outputs.last_hidden_state[:, 0, :]
#     return embeddings

# def calculate_similarity(text1, text2, model, tokenizer):
#     embedding1 = get_bert_embeddings(text1, model, tokenizer)
#     embedding2 = get_bert_embeddings(text2, model, tokenizer)

#     embedding1_np = embedding1.cpu().numpy().flatten()
#     embedding2_np = embedding2.cpu().numpy().flatten()

#     similarity = 1 - cosine(embedding1_np, embedding2_np)
#     return similarity

