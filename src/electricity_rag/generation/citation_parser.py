import re

from electricity_rag.retrieval.vector_store import SearchResult


def extract_cited_sources(answer_text: str, results: list[SearchResult]) -> list[SearchResult]:
    cited_titles = set(re.findall(r"\[Fuente:\s*(.+?)\]", answer_text))

    seen = set()
    cited_sources = []
    for result in results:
        if result.document_title in cited_titles and result.document_title not in seen:
            cited_sources.append(result)
            seen.add(result.document_title)

    return cited_sources