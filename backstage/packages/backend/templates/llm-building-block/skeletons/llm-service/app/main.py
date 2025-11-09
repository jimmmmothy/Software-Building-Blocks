from fastapi import FastAPI
from pydantic import BaseModel
import yaml

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

app = FastAPI(title="LLM Service", version="1.0.0")

class Prompt(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": f"LLM Service running with model: {config['model']['name']}"}

@app.post("/generate")
def generate(prompt: Prompt):
    response = f"[{config['model']['name']}] response to: {prompt.text}"
    if config["logging"]["enabled"]:
        print(f"LOG: {prompt.text} -> {response}")
    return {"model": config["model"]["name"], "response": response}
