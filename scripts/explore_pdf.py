from electricity_rag.ingestion.loaders import load_pdf

doc = load_pdf("data/raw/cnmc_guia_consumidores_electricidad_2022.pdf", title="Guía informativa CNMC 2022")
print(f"Título: {doc.title}")
print(f"Fuente: {doc.source}")
print(f"Longitud del texto: {len(doc.text)} caracteres")
print(doc.text[:500])