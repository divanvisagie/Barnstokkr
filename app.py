from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from typing import List
import os
import torch

app = FastAPI()

# Load pre-trained model and tokenizer
embeddings_model = "distilbert-base-uncased"
e_tokenizer = AutoTokenizer.from_pretrained(embeddings_model)
e_model = AutoModel.from_pretrained(embeddings_model)


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


# Set your Hugging Face token
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")
# Load conversational model and tokenizer
model_name = "google/gemma-2b"
tokenizer = AutoTokenizer.from_pretrained(
    model_name, use_auth_token=huggingface_token)
model = AutoModelForCausalLM.from_pretrained(
    model_name, use_auth_token=huggingface_token, device_map="auto")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat(item: ChatRequest):
    try:
        input_ids = tokenizer(item.message, return_tensors="pt")#.to("cuda")

        outputs = model.generate(**input_ids)
        reply = tokenizer.decode(outputs[0])
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
