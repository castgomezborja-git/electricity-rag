import tiktoken
from dataclasses import dataclass

@dataclass
class TextChunk:
    content: str
    token_count: int

encoding = tiktoken.get_encoding("cl100k_base")


def chunk_text(text: str, chunk_size: int = 200, chunk_overlap: int = 30, merge_threshold: int = 46) -> list[TextChunk]:

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap debe ser menor que chunk_size")

    tokens = encoding.encode(text)

    chunk_ranges = []
    start = 0

    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_ranges.append((start, end))
        start += chunk_size - chunk_overlap

    if len(chunk_ranges) > 1 and chunk_ranges[-1][1] - chunk_ranges[-2][1] < merge_threshold:
        penultimate_start = chunk_ranges[-2][0]
        final_end = chunk_ranges[-1][1]
        chunk_ranges[-2:] = [(penultimate_start, final_end)]

    return [
        TextChunk(content=encoding.decode(tokens[start:end]), token_count=end - start)
        for start, end in chunk_ranges
    ]



texto_prueba = "palabra " * 210  # aproximadamente 210 tokens con este encoding

chunks = chunk_text(texto_prueba)
print(f"Número de chunks texto prueba: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i} texto prueba: {chunk.token_count} tokens")


texto_largo = "palabra " * 416  # bastante más que 2 chunk_size, para tener varios chunks de sobra

chunks = chunk_text(texto_largo)
print(f"Número de chunks texto largo: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i} texto largo: {chunk.token_count} tokens")