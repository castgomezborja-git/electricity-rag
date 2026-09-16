import ollama


def generate_answer(prompt: str, model: str = "llama3.1:8b") -> str:
    response = ollama.generate(model=model, prompt=prompt)
    return response["response"]