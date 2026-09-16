from electricity_rag.retrieval.vector_store import search_similar_chunks
from electricity_rag.generation.prompt_builder import build_augmented_prompt
from electricity_rag.generation.llm_client import generate_answer


def answer_question(query: str, top_k: int = 5) -> str:
    results = search_similar_chunks(query, top_k=top_k)
    prompt = build_augmented_prompt(query, results)
    return generate_answer(prompt)