from electricity_rag.ingestion.embeddings import embed_chunks

vectores = embed_chunks(["El PVPC es el precio voluntario para el pequeño consumidor.", "Los peajes son costes regulados de la red."])
print(f"Número de vectores: {len(vectores)}")
print(f"Dimensión del primer vector: {len(vectores[0])}")
print(f"Primeros 5 valores: {vectores[0][:5]}")