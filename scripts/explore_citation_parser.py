from electricity_rag.generation.citation_parser import extract_cited_sources
from electricity_rag.retrieval.vector_store import SearchResult

resultados_fake = [
    SearchResult(document_title="Guía informativa CNMC 2022", document_source="data/raw/cnmc.pdf", chunk_text="...", distance=0.3),
    SearchResult(document_title="Funcionamiento del Mercado Diario (OMIE)", document_source="data/raw/omie.pdf", chunk_text="...", distance=0.5),
]

respuesta_fake = "El PVPC es el precio voluntario para el pequeño consumidor [Fuente: Guía informativa CNMC 2022]."

print(extract_cited_sources(respuesta_fake, resultados_fake))