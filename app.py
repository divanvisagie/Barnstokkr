from fastapi import FastAPI, HTTPException
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from pydantic import BaseModel

import torch

app = FastAPI()

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

class TextModel(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/embeddings/")
async def create_embeddings(item: TextModel):  # Use the Pydantic model here
    text = item.text  # Access the text attribute from the model instance
    try:
        # Encode text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        # Generate embeddings
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.logits.tolist()
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
