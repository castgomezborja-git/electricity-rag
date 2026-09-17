from electricity_rag.rag_pipeline import answer_question

pregunta = "¿Qué es el PVPC?"
resultado = answer_question(pregunta)

print(f"Pregunta: {pregunta}\n")
print(f"Respuesta:\n{resultado.answer}\n")
print("Fuentes citadas:")
for fuente in resultado.sources:
    print(f"  - {fuente.document_title} ({fuente.document_source})")