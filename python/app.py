from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

class TextPair(BaseModel):
    text1: str
    text2: str

@app.post("/similarity/")
async def calculate_similarity(data: TextPair):
    embedding1 = model.encode(data.text1, convert_to_tensor=True)
    embedding2 = model.encode(data.text2, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
    return {"similarity_score": similarity}
