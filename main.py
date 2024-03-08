from fastapi import FastAPI, HTTPException
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

app = FastAPI()

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/embeddings/")
async def create_embeddings(text: str):
    try:
        # Encode text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        # Generate embeddings
        with torch.no_grad():
            outputs = model(**inputs)
        # Convert to list for JSON serialization
        embeddings = outputs.logits.tolist()
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
