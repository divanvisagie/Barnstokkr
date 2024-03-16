from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
from typing import List
import torch

app = FastAPI()


class EmbeddingsRequest(BaseModel):
    text: str


class EmbeddingsResponse(BaseModel):
    embeddings: List[float]


@app.get("/healthcheck")
def read_root():
    return {"status": "Ok"}


@app.post("/embeddings", response_model=EmbeddingsResponse)
async def create_embeddings(item: EmbeddingsRequest):
    try:
        # Load pre-trained model and tokenizer
        embeddings_model = "distilbert-base-uncased"
        e_tokenizer = AutoTokenizer.from_pretrained(embeddings_model)
        e_model = AutoModel.from_pretrained(embeddings_model)
        # Encode text
        inputs = e_tokenizer(item.text, return_tensors="pt",
                             padding=True, truncation=True, max_length=512)
        # Generate model output
        with torch.no_grad():
            outputs = e_model(**inputs)
        # Extract embeddings from the last hidden state,
        # then take the mean of the sequence dimension
        embeddings = outputs.last_hidden_state.mean(dim=1).tolist()[0]
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
