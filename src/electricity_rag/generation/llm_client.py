import ollama

from electricity_rag.config import settings

def generate_answer(prompt: str, model: str = "llama3.1:8b") -> str:
    ollama_client = ollama.Client(settings.ollama_host)
    response = ollama_client.generate(model=model, prompt=prompt)
    return response["response"]