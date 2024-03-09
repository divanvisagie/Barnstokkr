from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
from typing import List
import torch

app = FastAPI()

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


class EmbeddingsRequest(BaseModel):
    text: str


class EmbeddingsResponse(BaseModel):
    embeddings: List[float]


@app.get("/healthcheck")
def read_root():
    return {"status": "Ok"}


@app.post("/embeddings/", response_model=EmbeddingsResponse)
async def create_embeddings(item: EmbeddingsRequest):
    try:
        # Encode text
        inputs = tokenizer(item.text, return_tensors="pt",
                           padding=True, truncation=True, max_length=512)
        # Generate model output
        with torch.no_grad():
            outputs = model(**inputs)
        # Extract embeddings from the last hidden state,
        # then take the mean of the sequence dimension
        embeddings = outputs.last_hidden_state.mean(dim=1).tolist()[0]
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
