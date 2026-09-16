from electricity_rag.retrieval.vector_store import SearchResult


def build_augmented_prompt(query: str, results: list[SearchResult]) -> str:
    context = "\n\n".join(
        f"[Fuente: {result.document_title}]\n{result.chunk_text}"
        for result in results
    )

    return f"""Eres un asistente que responde preguntas sobre el mercado eléctrico español, basándote ÚNICAMENTE en el siguiente contexto. No uses ningún conocimiento externo al contexto proporcionado.

Si el contexto no contiene información suficiente para responder la pregunta, dilo explícitamente en vez de inventar una respuesta.

Cuando uses información de un fragmento, cita el documento de origen entre corchetes, por ejemplo: [Fuente: nombre del documento].

Contexto:
{context}

Pregunta: {query}

Respuesta:"""