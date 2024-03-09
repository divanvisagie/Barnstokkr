from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from typing import List
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


# Load conversational model and tokenizer
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat(item: ChatRequest):
    try:
        # Encode the input text
        input_ids = tokenizer.encode(
            item.message + tokenizer.eos_token, return_tensors="pt")
        # Generate a response from the model
        chat_history_ids = model.generate(
            input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        # Decode the generated tokens to a string
        reply = tokenizer.decode(
            chat_history_ids[:, input_ids.shape[-1]:][0],
            skip_special_tokens=True
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
