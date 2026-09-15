from electricity_rag.ingestion.loaders import load_pdf
from electricity_rag.ingestion.chunking import chunk_text

doc = load_pdf("data/raw/cnmc_guia_consumidores_electricidad_2022.pdf", title="Guía informativa CNMC 2022")
chunks = chunk_text(doc.text)

print(f"Documento: {doc.title}")
print(f"Longitud del texto: {len(doc.text)} caracteres")
print(f"Número de chunks generados: {len(chunks)}")
print(f"Tokens por chunk: {[c.token_count for c in chunks]}")
print("\n--- Primer chunk ---")
print(chunks[0].content)
print("\n--- Chunk intermedio (índice 5) ---")
print(chunks[5].content if len(chunks) > 5 else "[no hay suficientes chunks]")