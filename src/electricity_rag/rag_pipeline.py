from dataclasses import dataclass


from electricity_rag.retrieval.vector_store import SearchResult, search_similar_chunks
from electricity_rag.generation.prompt_builder import build_augmented_prompt
from electricity_rag.generation.llm_client import generate_answer
from electricity_rag.generation.citation_parser import extract_cited_sources


@dataclass
class RagAnswer:
    answer: str
    sources: list[SearchResult]


def answer_question(query: str, top_k: int = 5) -> RagAnswer:
    results = search_similar_chunks(query, top_k=top_k)
    prompt = build_augmented_prompt(query, results)
    answer = generate_answer(prompt)
    sources = extract_cited_sources(answer, results)
    return RagAnswer(answer=answer, sources=sources)