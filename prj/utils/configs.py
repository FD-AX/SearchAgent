import torch
import os

evice = "cuda" if torch.cuda.is_available() else "cpu"
api_key = os.environ.get("MISTRAL_API_KEY")
model_name = "mistral-large-latest"